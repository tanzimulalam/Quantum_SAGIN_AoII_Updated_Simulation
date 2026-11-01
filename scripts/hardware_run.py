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
  --job-id ID       with --mode device: retrieve a finished job by id instead of submitting one, with the arguments
                    of the original submission (the circuits are re-transpiled with the same seed and checked
                    against the stored results); for a submitting process that lost its connection

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
from sentinel.sample_stats import enumerate_onehot, shot_statistics
from run_validation import make_instance

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "hardware"


def prepare(args):
    """Optimize everything on the simulator; return the instance, per-domain QUBOs with final weights, angles, and references."""
    radio = {}
    if getattr(args, "sat_bw_mhz", None):
        radio["radio__sat_bandwidth_mhz"] = float(args.sat_bw_mhz)
    if getattr(args, "bs_bw_mhz", None):
        radio["radio__bs_bandwidth_mhz"] = float(args.bs_bw_mhz)
    cfg = configure(FullConfig(), net__num_ues=args.ues, net__num_bs=2, net__num_sat=2, net__num_domains=2, **radio,
                    solver__solver=args.dual_solver, solver__qaoa_depth=args.depth, solver__qaoa_shots=512,
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
        if dq.n <= args.max_sim_qubits:
            sim = qaoa_xy(dq, pruned, depth=args.depth, shots=512, maxiter=args.iters, seed=args.seed, warm_start_sel=g, init=args.init)
            src = "simulator"
        else:
            # too large for the statevector simulator: angles are transferred (parameter concentration) from the
            # largest simulated domain of this run, or from --transfer-from, and the greedy assignment is the reference
            sim = {"params": None, "param_names": None, "feasible_sample_fraction": float("nan"),
                   "best_energy": dq.assignment_energy(g, pruned), "best_sel": g}
            src = "transferred"
        domains.append({"k": k, "dq": dq, "params": sim["params"], "param_names": sim["param_names"], "sim": sim,
                        "greedy_sel": g, "params_source": src})
    donors = [d for d in domains if d["params"] is not None]
    if args.transfer_from:
        tr = json.loads((OUT / args.transfer_from / "summary.json").read_text())
        cand = [dd for dd in tr["domains"] if dd.get("params")]
        if cand:
            big = max(cand, key=lambda dd: dd["n_qubits"])
            donors.append({"params": np.array(big["params"]), "param_names": big.get("param_names"), "dq": None,
                           "k": f"{args.transfer_from}/domain{big['domain']}"})
    for d in domains:
        if d["params"] is None:
            if not donors:
                raise SystemExit(f"domain {d['k']} has {d['dq'].n} qubits (> {args.max_sim_qubits}) and no angle donor; pass --transfer-from <tag>")
            donor = max(donors, key=lambda dd: dd["dq"].n if dd["dq"] is not None else 0)
            d["params"] = np.array(donor["params"]); d["param_names"] = donor["param_names"]
            d["params_source"] = f"transferred from domain {donor['k']}"
            print(f"  domain {d['k']}: {d['dq'].n} qubits > {args.max_sim_qubits}, angles transferred from domain {donor['k']}", flush=True)
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
    ap.add_argument("--job-id", default=None,
                    help="retrieve this finished Sampler job instead of submitting one (--mode device; pass the same arguments as the original submission)")
    ap.add_argument("--max-sim-qubits", type=int, default=26, help="largest domain optimized on the statevector simulator; larger domains get transferred angles")
    ap.add_argument("--transfer-from", default=None, help="results/hardware/<tag> whose largest simulated domain donates angles to oversized domains")
    ap.add_argument("--sat-bw-mhz", type=float, default=None, help="satellite bandwidth capacity (default: config, 50 MHz); smaller values make capacity bind")
    ap.add_argument("--bs-bw-mhz", type=float, default=None, help="BS bandwidth capacity (default: config, 20 MHz)")
    ap.add_argument("--dual-solver", choices=["sa_xy", "qaoa_xy"], default="sa_xy",
                    help="inner solver of the scenario-weight/ADMM loop that builds the domain QUBOs (qaoa_xy reproduces runs made before 28 Oct 2026)")
    ap.add_argument("--reanalyze", action="store_true",
                    help="recompute per-shot statistics of an existing run (its --tag folder) from the saved counts; nothing is sampled")
    ap.add_argument("--mitigation", choices=["none", "dd", "dd_twirl"], default="none",
                    help="device-side error suppression: dynamical decoupling (XY4) and optionally Pauli twirling of gates and measurements")
    args = ap.parse_args()
    tag = args.tag or f"{args.mode}_U{args.ues}_k{args.k_cand}_p{args.depth}_s{args.seed}_{args.init}"
    out = OUT / tag; out.mkdir(parents=True, exist_ok=True)

    print("preparing on the simulator ...", flush=True)
    cfg, inst, pruned, ref, res, domains = prepare(args)
    all_domains = list(domains)
    print(f"instance: {args.ues} UEs, pruned vars {pruned.num_vars}; ILP optimum eta = {ref:.4f}; simulator compact-QAOA eta = {res.eta:.4f}", flush=True)

    # backend
    if args.reanalyze:
        old = json.loads((out / "summary.json").read_text())
        class _B: name = old["backend"]
        backend = _B()
        print("re-analysis of", tag, "on saved counts from", backend.name, flush=True)
    elif args.mode == "device":
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService()
        backend = service.backend(args.backend) if args.backend else service.least_busy(operational=True, simulator=False)
        print("device:", backend.name, flush=True)
    else:
        import qiskit_ibm_runtime.fake_provider as fp
        backend = getattr(fp, args.fake)()
        print("fake backend:", backend.name, flush=True)

    summary = {"mode": args.mode, "backend": backend.name, "ues": args.ues, "k_cand": args.k_cand, "depth": args.depth,
               "shots": args.shots, "ilp_eta": ref, "sim_compact_qaoa_eta": res.eta, "max_sim_qubits": args.max_sim_qubits, "mitigation": args.mitigation,
               "init": args.init, "dual_solver": args.dual_solver, "sat_bw_mhz": args.sat_bw_mhz, "bs_bw_mhz": args.bs_bw_mhz, "domains": []}
    circuits = []
    if args.domains != "all":
        keep = {int(v) for v in args.domains.split(",")}
        domains = [d for d in domains if d["k"] in keep]
    for d in domains:
        dq = d["dq"]
        if args.reanalyze:
            od = next(dd for dd in old["domains"] if dd["domain"] == d["k"])
            two_q, depth_t = od["two_qubit_gates"], od["transpiled_depth"]
        else:
            bound, two_q, depth_t = transpile_for(backend, dq, d["params"], args.depth, init=args.init, warm_start_sel=d["greedy_sel"], seed=args.seed)
            circuits.append(bound)
        # rough QPU-time estimate: ~ shots * (circuit time ~ depth * 0.5 us + readout ~ 1 ms per shot batch) -> use 2 ms/shot upper bound
        est_s = args.shots * 2e-3
        d_sum = {"domain": d["k"], "n_qubits": dq.n, "decision_qubits": dq.n_x, "two_qubit_gates": two_q, "transpiled_depth": depth_t,
                 "sim_feasible_sample_fraction": d["sim"]["feasible_sample_fraction"], "sim_best_energy": d["sim"]["best_energy"],
                 "greedy_energy": dq.assignment_energy(d["greedy_sel"], pruned), "estimated_qpu_s_upper": est_s,
                 "params": [float(v) for v in d["params"]], "param_names": d.get("param_names"), "params_source": d.get("params_source", "simulator")}
        print(f"  domain {d['k']}: {dq.n} qubits ({dq.n_x} decision), {two_q} two-qubit gates, depth {depth_t}; "
              f"simulator feasible-sample fraction {d['sim']['feasible_sample_fraction']:.2f}; est. QPU time <= {est_s:.1f} s", flush=True)
        summary["domains"].append(d_sum)
    if args.mode == "estimate":
        (out / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
        print("estimate only; nothing submitted. total estimated QPU time <= %.1f s" % sum(d["estimated_qpu_s_upper"] for d in summary["domains"]))
        return

    # sampling
    t0 = time.time()
    if args.reanalyze:
        results = [json.loads((out / f"counts_domain{d['k']}.json").read_text()) for d in domains]
        for key in ("job_id", "usage_s", "sampling_wall_s", "mitigation"):
            if key in old:
                summary[key] = old[key]
    elif args.mode == "fake":
        from qiskit_aer import AerSimulator
        sim = AerSimulator.from_backend(backend)
        results = [sim.run(c, shots=args.shots).result().get_counts() for c in circuits]
    else:
        from qiskit_ibm_runtime import SamplerV2 as Sampler
        sampler = Sampler(mode=backend)
        if args.mitigation in ("dd", "dd_twirl"):
            sampler.options.dynamical_decoupling.enable = True
            sampler.options.dynamical_decoupling.sequence_type = "XY4"
        if args.mitigation == "dd_twirl":
            sampler.options.twirling.enable_gates = True
            sampler.options.twirling.enable_measure = True
            sampler.options.twirling.num_randomizations = "auto"
        if args.job_id:
            # A finished job whose submitting process lost the connection: retrieve it by id. The circuits above are
            # re-transpiled with the same seed, so the gate counts and decoding match the submitted job.
            job = service.job(args.job_id)
            if job.backend().name != backend.name:
                raise SystemExit(f"job {args.job_id} ran on {job.backend().name}, not {backend.name}")
            print("retrieving job id:", job.job_id(), "status:", job.status(), flush=True)
            summary["retrieved_job"] = True
            try:
                summary["job_timestamps"] = job.metrics().get("timestamps", {})
            except Exception:
                pass
        else:
            job = sampler.run(circuits, shots=args.shots)
            print("job id:", job.job_id(), flush=True)
        job_result = job.result()
        if len(job_result) != len(domains):
            raise SystemExit(f"job returned {len(job_result)} results for {len(domains)} circuits")
        results = []
        for pub, d in zip(job_result, domains):
            counts = pub.data.meas.get_counts()
            nbits = len(next(iter(counts)))
            if nbits != d["dq"].n:
                raise SystemExit(f"domain {d['k']}: job bitstrings have {nbits} bits, circuit has {d['dq'].n} qubits")
            results.append(counts)
        summary["job_id"] = job.job_id()
        try:
            summary["usage_s"] = job.usage()
        except Exception:
            pass
    if args.job_id:
        # device time from the job metrics (running -> finished) rather than the retrieval time
        try:
            from datetime import datetime
            ts = summary["job_timestamps"]
            iso = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
            summary["sampling_wall_s"] = (iso(ts["finished"]) - iso(ts["running"])).total_seconds()
        except Exception:
            summary["sampling_wall_s"] = None
    elif not args.reanalyze:
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
        enum = enumerate_onehot(dq, pruned)
        st = shot_statistics(dq, pruned, counts, enum)
        if enum is not None and enum.get("n_feasible", 0):
            d_sum.update({"onehot_states": enum["n_states"], "feasible_states": enum["n_feasible"], "optimal_states": enum["n_optimal"],
                          "exact_domain_optimum": enum["e_opt"], "p_uniform_optimal": enum["p_uniform_optimal"],
                          "uniform_approx_ratio": enum["uniform_approx_ratio"], "energy_spread_rel": enum["spread_rel"],
                          "best_equals_exact_optimum": bool(best_sel is not None and abs(best_e - enum["e_opt"]) <= 1e-9 * max(1.0, abs(enum["e_opt"])))})
        d_sum.update({"p_optimal_shot": st["p_optimal_shot"], "p_optimal_given_feasible": st["p_optimal_given_feasible"],
                      "approx_ratio_feasible": st["approx_ratio_feasible"]})
        print(f"  domain {d['k']}: P(optimal shot) {st['p_optimal_shot']:.3f}, P(optimal | feasible) {st['p_optimal_given_feasible']:.3f}, "
              f"approx. ratio {st['approx_ratio_feasible']:.3f}; uniform-feasible baseline P {d_sum.get('p_uniform_optimal', float('nan')):.3f}, "
              f"ratio {d_sum.get('uniform_approx_ratio', float('nan')):.3f}; feasible-set energy spread {100*d_sum.get('energy_spread_rel', float('nan')):.2f}% "
              f"({d_sum.get('optimal_states', 0)} optimal of {d_sum.get('feasible_states', 0)} feasible states)", flush=True)
        sel = best_sel if best_sel is not None else d["greedy_sel"]
        x[dq.x_vars] = dq.x_from_sel(sel)
        print(f"  domain {d['k']}: one-hot samples {onehot:.3f}, feasible {feas:.3f}, best energy {best_e:.4f} (sim {d['sim']['best_energy']:.4f})", flush=True)
    eta, l = pruned.worst_case(x)
    summary.update({"hw_schedule_eta": eta, "hw_schedule_feasible": bool(pruned.is_feasible(x)), "hw_gap_pct_vs_ilp": 100 * (eta / ref - 1)})
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
    md = [f"# Hardware run `{tag}`", "", f"backend: {backend.name}; {args.ues} UEs; k_cand {args.k_cand}; depth {args.depth}; {args.shots} shots per domain; mitigation {args.mitigation}", "",
          f"ILP optimum eta = {ref:.4f}; simulator compact-QAOA eta = {res.eta:.4f}; device-decoded schedule eta = {eta:.4f} "
          f"(gap {100*(eta/ref-1):+.2f}%), feasible = {pruned.is_feasible(x)}", "",
          "| domain | qubits | 2q gates | depth | hw feasible frac | P(opt shot) | P(opt | feasible) | approx ratio | uniform P(opt) | uniform ratio | best = exact opt |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for d_sum in summary["domains"]:
        md.append(f"| {d_sum['domain']} | {d_sum['n_qubits']} | {d_sum['two_qubit_gates']} | {d_sum['transpiled_depth']} | "
                  f"{d_sum['hw_feasible_sample_fraction']:.3f} | {d_sum.get('p_optimal_shot', float('nan')):.3f} | {d_sum.get('p_optimal_given_feasible', float('nan')):.3f} | "
                  f"{d_sum.get('approx_ratio_feasible', float('nan')):.3f} | {d_sum.get('p_uniform_optimal', float('nan')):.3f} | {d_sum.get('uniform_approx_ratio', float('nan')):.3f} | "
                  f"{d_sum.get('best_equals_exact_optimum', d_sum.get('hw_matches_sim_best'))} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
