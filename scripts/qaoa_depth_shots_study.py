"""QAOA depth / shots / initial-state study on hardware-sized compact domain QUBOs (noiseless Aer).

For each domain of the 6-UE instances (seeds 1..3): depth in {1, 2}, shots in {128, 512, 2048}, init in {w, greedy},
3 COBYLA restarts. Records the probability that a final sample is the optimal assignment, the best decoded energy,
the fraction of feasible samples, and wall time. Output: results/qaoa_depth_shots.csv and figures/qaoa_depth_shots.*
"""
import sys, pathlib, time, argparse, itertools, os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.compact import prune_candidates, build_compact_qubo, _shared_sats, greedy_sel
from sentinel.solvers.qaoa_xy import build_xy_circuit, decode_xy_counts, qaoa_xy
from sentinel.solvers.ilp import solve_p3_exact
from run_validation import make_instance

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def domain_qubos(seed):
    cfg = configure(FullConfig(), net__num_ues=6, net__num_bs=2, net__num_sat=2, net__num_domains=2)
    inst = prune_candidates(make_instance(cfg, seed, 6), 4)
    shared = _shared_sats(inst)
    w = np.ones(6) / 6
    z = {int(j): inst.cap_units[j] / 2 for j in shared}; u = {int(j): 0.0 for j in shared}
    out = []
    for k in range(2):
        dq = build_compact_qubo(inst, k, w, z, u, 0.0, shared, onehot_penalty=False)
        # exact optimum of the domain objective (uncoupled) by enumeration over one-hot assignments; the optimum is
        # typically degenerate (several bandwidth/period combinations with identical cost), so keep the whole set
        energies = {sel: dq.assignment_energy(np.array(sel), inst) for sel in itertools.product(*[list(g) for g in dq.groups])}
        best_e = min(energies.values())
        opt_set = {sel for sel, e in energies.items() if abs(e - best_e) < 1e-9}
        best_sel = np.array(next(iter(opt_set)))
        out.append((k, dq, inst, best_e, best_sel, opt_set, len(energies)))
    return out


def run(task):
    seed, k, depth, shots, init, restart, scale_mode = task
    for kk, dq, inst, best_e, best_sel, opt_set, n_states in domain_qubos(seed):
        if kk != k:
            continue
        g = greedy_sel(dq, inst)
        t0 = time.time()
        res = qaoa_xy(dq, inst, depth=depth, shots=shots, maxiter=60, seed=1000 * restart + seed, warm_start_sel=g, init=init, final_shots=4096, scale_mode=scale_mode)
        # probability of the optimal assignment among final samples: re-decode counts is not returned, so recompute from best/mean
        from qiskit import transpile
        from qiskit_aer import AerSimulator
        qc, _, _, _ = build_xy_circuit(dq, depth=depth, init=init, warm_start_sel=g, scale_mode=scale_mode)
        backend = AerSimulator(seed_simulator=7)
        tqc = transpile(qc, backend, optimization_level=1)
        bound = tqc.assign_parameters(dict(zip(list(tqc.parameters), res["params"])))
        counts = backend.run(bound, shots=4096).result().get_counts()
        n = dq.n; p_opt = 0
        for key, c in counts.items():
            wv = np.array([int(key[n - 1 - a]) for a in range(n)], dtype=float)
            xk = wv[: dq.n_x]
            if dq.is_onehot(xk) and tuple(dq.sel_from_x(xk)) in opt_set:
                p_opt += c
        return dict(seed=seed, domain=k, qubits=dq.n, depth=depth, shots=shots, init=init, restart=restart, scale_mode=scale_mode,
                    p_optimal_sample=p_opt / 4096, p_uniform=len(opt_set) / n_states, optimal_states=len(opt_set), one_hot_states=n_states,
                    best_energy=res["best_energy"], optimum=best_e,
                    found_optimum=abs(res["best_energy"] - best_e) < 1e-9, feasible_sample_fraction=res["feasible_sample_fraction"],
                    greedy_is_optimal=abs(dq.assignment_energy(g, inst) - best_e) < 1e-9, iterations=len(res["energies"]),
                    time_s=time.time() - t0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--scale-modes", default="max,cost"); ap.add_argument("--inits", default="w,greedy"); ap.add_argument("--out", default="qaoa_depth_shots.csv")
    args = ap.parse_args()
    tasks = [(s, k, d, sh, init, r, sm) for s in range(1, args.seeds + 1) for k in (0, 1) for d in (1, 2) for sh in (128, 512, 2048)
             for init in args.inits.split(",") for r in range(3) for sm in args.scale_modes.split(",")]
    print(len(tasks), "tasks", flush=True)
    rows = []; t0 = time.time()
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run, t): t for t in tasks}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                rows.append(f.result())
                pd.DataFrame(rows).to_csv(RES / args.out, index=False)
            except Exception as e:
                print("FAILED", futs[f], repr(e), flush=True)
            if i % 10 == 0:
                print(f"  {i}/{len(tasks)} {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 200)
    print(df.groupby(["scale_mode", "init", "depth", "shots"]).agg(p_opt=("p_optimal_sample", "mean"), found=("found_optimum", "mean"),
                                                   feas=("feasible_sample_fraction", "mean"), time=("time_s", "mean")).round(3).to_string())
    print("greedy already optimal in", df.greedy_is_optimal.mean().round(3), "of domain instances")
