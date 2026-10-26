"""Run the final QAOA sampling of SENTINEL's domain QUBOs on an IBM Quantum device (or a noisy fake backend).

Budget-aware design for the IBM Quantum Open Plan (10 min QPU time / 28 days):
  1. the whole optimization (scenario weights, ADMM targets, QAOA angles) runs on the local simulator;
  2. only ONE sampling job per domain is sent to the device, with the optimized angles, N shots;
  3. the device counts are decoded classically and certified exactly, like any other SENTINEL schedule.

Modes
  --mode estimate   build and transpile the circuits for the target, print qubits, depth, 2-qubit gates and an
                    estimated QPU time; nothing is submitted (no account needed when --fake is given)
  --mode fake       run the final sampling on a local noisy simulator built from an IBM fake backend
                    (qiskit_ibm_runtime.fake_provider, e.g. FakeTorino) - no account needed
  --mode device     submit to the least-busy open device (or --backend NAME) through qiskit-ibm-runtime.
                    Requires a saved account: run once, in your own Python session, with your token:
                        from qiskit_ibm_runtime import QiskitRuntimeService
                        QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token="<your token>", overwrite=True)
                    This script never reads or stores tokens itself.

Outputs: results/hardware/<tag>/  (instance.json, circuits.qpy, counts_*.json, summary.json, summary.md)
"""
import sys, pathlib, time, argparse, json, os, copy
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.compact import (compact_sentinel_solve, prune_candidates, build_compact_qubo, _shared_sats, greedy_sel)
from sentinel.solvers.qaoa_xy import build_xy_circuit, decode_xy_counts, qaoa_xy
from run_validation import make_instance

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "hardware"


def prepare(args):
    """Optimize everything on the simulator; return the instance, per-domain QUBOs with final weights, angles, and references."""
    cfg = configure(FullConfig(), net__num_ues=args.ues, net__num_bs=2, net__num_sat=2, net__num_domains=2,
                    solver__solver="qaoa_xy", solver__qaoa_depth=args.depth, solver__qaoa_shots=512,
                    solver__qaoa_maxiter=args.iters, solver__max_qaoa_qubits=64, solver__admm_max_rounds=4)
    inst = make_instance(cfg, args.seed, 6)
    ref = solve_p3_exact(inst)["eta"]
    pruned = prune_candidates(inst, args.k_cand)
    res = compact_sentinel_solve(inst, cfg.solver, seed=args.seed, outer_iterations=args.outer, k_cand=args.k_cand)
    # final scenario weights (last trace entry) and final ADMM state are re-derived for the showcase:
    # rebuild each domain QUBO at the final weights with the warm-started (uncoupled) targets, as in the last round
    w = res.weights_trace[-1]
    shared = _shared_sats(pruned)
    z = {int(j): pruned.cap_units[j] / 2 for j in shared}; u = {int(j): 0.0 for j in shared}
    domains = []
    for k in range(int(pruned.domain_of_ue.max()) + 1):
        dq = build_compact_qubo(pruned, k, w, z, u, 0.0, shared, onehot_penalty=False)   # uncoupled domain problem for the device
        g = greedy_sel(dq, pruned)
        sim = qaoa_xy(dq, pruned, depth=args.depth, shots=512, maxiter=args.iters, seed=args.seed, warm_start_sel=g, init=args.init)
        domains.append({"k": k, "dq": dq, "params": sim["params"], "param_names": sim["param_names"], "sim": sim, "greedy_sel": g})
    return cfg, inst, pruned, ref, res, domains


def transpile_for(backend, dq, params, depth, init="w", warm_start_sel=None, seed=1):
    from qiskit import transpile
    qc, gammas, betas, scale = build_xy_circuit(dq, depth=depth, init=init, warm_start_sel=warm_start_sel)
    best = None
    for st in range(seed, seed + 8):          # a few SABRE trials; keep the shallowest routing
        cand = transpile(qc, backend, optimization_level=3, seed_transpiler=st)
        n2 = sum(1 for ins in cand.data if ins.operation.num_qubits == 2)
        if best is None or n2 < best[1]:
            best = (cand, n2)
    tqc = best[0]
    bound = tqc.assign_parameters({p: v for p, v in zip(sorted(tqc.parameters, key=lambda p: p.name), params)})
    two_q = sum(1 for ins in bound.data if ins.operation.num_qubits == 2)
    return bound, two_q, bound.depth()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["estimate", "fake", "device"], default="estimate")
    ap.add_argument("--fake", default="FakeTorino", help="fake backend class name for --mode fake/estimate")
    ap.add_argument("--backend", default=None, help="device name for --mode device (default: least busy open device)")
    ap.add_argument("--ues", type=int, default=6)
    ap.add_argument("--k-cand", type=int, default=4)
    ap.add_argument("--depth", type=int, default=1)
    ap.add_argument("--iters", type=int, default=40)
    ap.add_argument("--outer", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--shots", type=int, default=4096)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--init", choices=["w", "greedy"], default="greedy", help="initial state: W state per UE or the greedy basis state")
    ap.add_argument("--domains", default="all", help="comma-separated domain indices to sample on the device (default all)")
    args = ap.parse_args()
    tag = args.tag or f"{args.mode}_U{args.ues}_k{args.k_cand}_p{args.depth}_s{args.seed}_{args.init}"
    out = OUT / tag; out.mkdir(parents=True, exist_ok=True)

    print("preparing on the simulator ...", flush=True)
    cfg, inst, pruned, ref, res, domains = prepare(args)
    all_domains = list(domains)
    print(f"instance: {args.ues} UEs, pruned vars {pruned.num_vars}; ILP optimum eta = {ref:.4f}; simulator compact-QAOA eta = {res.eta:.4f}", flush=True)

    # backend
    if args.mode == "device":
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService()
        backend = service.backend(args.backend) if args.backend else service.least_busy(operational=True, simulator=False)
        print("device:", backend.name, flush=True)
    else:
        import qiskit_ibm_runtime.fake_provider as fp
        backend = getattr(fp, args.fake)()
        print("fake backend:", backend.name, flush=True)

    summary = {"mode": args.mode, "backend": backend.name, "ues": args.ues, "k_cand": args.k_cand, "depth": args.depth,
               "shots": args.shots, "ilp_eta": ref, "sim_compact_qaoa_eta": res.eta, "domains": []}
    circuits = []
    if args.domains != "all":
        keep = {int(v) for v in args.domains.split(",")}
        domains = [d for d in domains if d["k"] in keep]
    for d in domains:
        dq = d["dq"]
        bound, two_q, depth_t = transpile_for(backend, dq, d["params"], args.depth, init=args.init, warm_start_sel=d["greedy_sel"], seed=args.seed)
        circuits.append(bound)
        # rough QPU-time estimate: ~ shots * (circuit time ~ depth * 0.5 us + readout ~ 1 ms per shot batch) -> use 2 ms/shot upper bound
        est_s = args.shots * 2e-3
        d_sum = {"domain": d["k"], "n_qubits": dq.n, "decision_qubits": dq.n_x, "two_qubit_gates": two_q, "transpiled_depth": depth_t,
                 "sim_feasible_sample_fraction": d["sim"]["feasible_sample_fraction"], "sim_best_energy": d["sim"]["best_energy"],
                 "greedy_energy": dq.assignment_energy(d["greedy_sel"], pruned), "estimated_qpu_s_upper": est_s}
        print(f"  domain {d['k']}: {dq.n} qubits ({dq.n_x} decision), {two_q} two-qubit gates, depth {depth_t}; "
              f"simulator feasible-sample fraction {d['sim']['feasible_sample_fraction']:.2f}; est. QPU time <= {est_s:.1f} s", flush=True)
        summary["domains"].append(d_sum)
    if args.mode == "estimate":
        (out / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
        print("estimate only; nothing submitted. total estimated QPU time <= %.1f s" % sum(d["estimated_qpu_s_upper"] for d in summary["domains"]))
        return

    # sampling
    t0 = time.time()
    if args.mode == "fake":
        from qiskit_aer import AerSimulator
        sim = AerSimulator.from_backend(backend)
        results = [sim.run(c, shots=args.shots).result().get_counts() for c in circuits]
    else:
        from qiskit_ibm_runtime import SamplerV2 as Sampler
        sampler = Sampler(mode=backend)
        job = sampler.run(circuits, shots=args.shots)
        print("job id:", job.job_id(), flush=True)
        job_result = job.result()
        results = []
        for pub in job_result:
            counts = pub.data.meas.get_counts()
            results.append(counts)
        summary["job_id"] = job.job_id()
        try:
            summary["usage_s"] = job.usage()
        except Exception:
            pass
    summary["sampling_wall_s"] = time.time() - t0

    # decode and certify
    x = np.zeros(pruned.num_vars)
    for d in all_domains:
        if d not in domains:
            sel = d["sim"]["best_sel"] if d["sim"]["best_sel"] is not None else d["greedy_sel"]
            x[d["dq"].x_vars] = d["dq"].x_from_sel(sel)
    for d, counts, d_sum in zip(domains, results, summary["domains"]):
        dq = d["dq"]
        best_sel, best_e, e_mean, onehot, feas = decode_xy_counts(dq, pruned, counts)
        (out / f"counts_domain{d['k']}.json").write_text(json.dumps(counts))
        d_sum.update({"hw_onehot_sample_fraction": onehot, "hw_feasible_sample_fraction": feas, "hw_best_energy": best_e,
                      "hw_mean_qubo_energy": e_mean, "hw_matches_sim_best": bool(best_sel is not None and abs(best_e - d["sim"]["best_energy"]) < 1e-9)})
        sel = best_sel if best_sel is not None else d["greedy_sel"]
        x[dq.x_vars] = dq.x_from_sel(sel)
        print(f"  domain {d['k']}: one-hot samples {onehot:.3f}, feasible {feas:.3f}, best energy {best_e:.4f} (sim {d['sim']['best_energy']:.4f})", flush=True)
    eta, l = pruned.worst_case(x)
    summary.update({"hw_schedule_eta": eta, "hw_schedule_feasible": bool(pruned.is_feasible(x)), "hw_gap_pct_vs_ilp": 100 * (eta / ref - 1)})
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
    md = [f"# Hardware run `{tag}`", "", f"backend: {backend.name}; {args.ues} UEs; k_cand {args.k_cand}; depth {args.depth}; {args.shots} shots per domain", "",
          f"ILP optimum eta = {ref:.4f}; simulator compact-QAOA eta = {res.eta:.4f}; device-decoded schedule eta = {eta:.4f} "
          f"(gap {100*(eta/ref-1):+.2f}%), feasible = {pruned.is_feasible(x)}", "",
          "| domain | qubits | 2q gates | depth | sim feasible frac | hw one-hot frac | hw feasible frac | sim best E | hw best E |", "|---|---|---|---|---|---|---|---|---|"]
    for d_sum in summary["domains"]:
        md.append(f"| {d_sum['domain']} | {d_sum['n_qubits']} | {d_sum['two_qubit_gates']} | {d_sum['transpiled_depth']} | {d_sum['sim_feasible_sample_fraction']:.2f} | "
                  f"{d_sum['hw_onehot_sample_fraction']:.3f} | {d_sum['hw_feasible_sample_fraction']:.3f} | {d_sum['sim_best_energy']:.4f} | {d_sum['hw_best_energy']:.4f} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
