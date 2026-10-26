"""Validation of the compact (dualized, slack-free) formulation against the exact ILP of P3.

Solvers compared on every instance
  ILP exact                              reference
  Greedy+LS                              classical heuristic
  Epigraph QUBO + SA-XY ADMM             the paper's original encoding (Section V), with the warm-started ADMM
  Compact dual + SA-XY ADMM              new encoding, classical one-hot-preserving inner solver, K = number of BSs
  Compact dual + QAOA-XY (Aer)           new encoding, XY-mixer QAOA inner solver (small networks only)

Experiments
  A  QAOA:  U in {4, 6, 8}, 2 BS + 2 SAT, L = 6, k_cand = 4, depth 1           (5 seeds)
  B  size:  (U, BS, SAT) in (10,2,2) (25,2,2) (50,4,3) (75,6,4) (100,8,5), L = 6 (10 seeds)
  C  severity sweep at 20 UEs, D scenario-count sweep at 20 UEs                  (10 seeds)
"""
import sys, pathlib, time, argparse, json, os, copy
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.solvers.greedy import greedy_assign, local_search
from sentinel.admm import sentinel_solve
from sentinel.compact import compact_sentinel_solve, prune_candidates
from run_validation import make_instance

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = ROOT / "results"
K_CAND = 4


def evaluate(task):
    exp, cfg, seed, L, label = task["exp"], task["cfg"], task["seed"], task["L"], task["label"]
    inst = make_instance(cfg, seed, L)
    base = dict(exp=exp, label=label, seed=seed, L=L, num_ues=cfg.net.num_ues, num_domains=cfg.net.num_domains,
                num_vars=inst.num_vars, num_vars_pruned=prune_candidates(inst, K_CAND).num_vars, forced=int(inst.forced_fallback.sum()))
    rows = []
    ilp = solve_p3_exact(inst, time_limit_s=300)
    ref = ilp["eta"] if (ilp["x"] is not None and inst.is_feasible(ilp["x"])) else np.nan
    rows.append(dict(base, solver="ILP exact", eta=ref, feasible=True, time_s=ilp["time_s"], gap_pct=0.0, qubits=0,
                     ilp_time_limit=ilp["time_s"] >= 299.0))
    ilp_p = solve_p3_exact(prune_candidates(inst, K_CAND), time_limit_s=300)["eta"]
    rows.append(dict(base, solver=f"ILP on pruned (k={K_CAND})", eta=ilp_p, feasible=True, time_s=0.0, gap_pct=100 * (ilp_p / ref - 1), qubits=0))
    t0 = time.time(); gl = local_search(inst, greedy_assign(inst)); egl, _ = inst.worst_case(gl)
    rows.append(dict(base, solver="Greedy+LS", eta=egl, feasible=inst.is_feasible(gl), time_s=time.time() - t0, gap_pct=100 * (egl / ref - 1), qubits=0))
    if task.get("epigraph", True):
        sc = copy.deepcopy(cfg.solver); sc.solver = "sa_xy"
        e = sentinel_solve(inst, sc, seed=seed, polish=False)
        rows.append(dict(base, solver="Epigraph QUBO + SA-XY ADMM", eta=e.eta, feasible=e.feasible, time_s=e.time_s, gap_pct=100 * (e.eta / ref - 1),
                         qubits=max(e.qubits_per_domain) if e.qubits_per_domain else 0, rounds=e.rounds))
    sc = copy.deepcopy(cfg.solver); sc.solver = "sa_xy"
    c = compact_sentinel_solve(inst, sc, seed=seed, outer_iterations=8, k_cand=K_CAND)
    rows.append(dict(base, solver="Compact dual + SA-XY ADMM", eta=c.eta, feasible=c.feasible, time_s=c.time_s, gap_pct=100 * (c.eta / ref - 1),
                     qubits=max(c.qubits_per_domain) if c.qubits_per_domain else 0, rounds=c.admm_rounds_total,
                     eta_trace=json.dumps([round(v, 4) for v in c.eta_trace])))
    if task.get("qaoa", False):
        sc = copy.deepcopy(cfg.solver); sc.solver = "qaoa_xy"
        q = compact_sentinel_solve(inst, sc, seed=seed, outer_iterations=task.get("qaoa_outer", 4), k_cand=K_CAND)
        qi = [i for i in q.qaoa_info]
        rows.append(dict(base, solver="Compact dual + QAOA-XY (Aer)", eta=q.eta, feasible=q.feasible, time_s=q.time_s, gap_pct=100 * (q.eta / ref - 1),
                         qubits=max(q.qubits_per_domain) if q.qubits_per_domain else 0, rounds=q.admm_rounds_total,
                         qaoa_solves=len(qi), feasible_sample_fraction=float(np.mean([i["feasible_sample_fraction"] for i in qi])) if qi else np.nan,
                         two_qubit_gates=int(np.max([i["two_qubit_gates"] for i in qi])) if qi else 0,
                         circuit_depth=int(np.max([i["circuit_depth_transpiled"] for i in qi])) if qi else 0,
                         qaoa_trace=json.dumps([round(v, 3) for v in qi[-1]["energies"]]) if qi else ""))
    for r_ in rows:
        if not r_.get("feasible", True):
            r_["gap_pct"] = np.nan
    return rows


def build_tasks(args):
    base = FullConfig()
    tasks = []
    if args.exp in ("A", "all"):
        for U in (4, 6, 8):
            cfg = configure(base, net__num_ues=U, net__num_bs=2, net__num_sat=2, net__num_domains=2, solver__qaoa_depth=1,
                            solver__qaoa_shots=512, solver__qaoa_maxiter=args.qaoa_iters, solver__max_qaoa_qubits=40, solver__admm_max_rounds=6)
            for s in range(1, args.seeds_small + 1):
                tasks.append(dict(exp="A", cfg=cfg, seed=s, L=6, label=f"U={U}", qaoa=True, epigraph=True))
    if args.exp in ("B", "all"):
        for U, B, S in ((10, 2, 2), (25, 2, 2), (50, 4, 3), (75, 6, 4), (100, 8, 5)):
            cfg = configure(base, net__num_ues=U, net__num_bs=B, net__num_sat=S, net__num_domains=B)
            for s in range(1, args.seeds + 1):
                tasks.append(dict(exp="B", cfg=cfg, seed=s, L=6, label=f"U={U}", epigraph=(U <= 50)))
    if args.exp in ("C", "all"):
        sev = {"mild": (3.0, 6.0, 10, 20, 10), "moderate": (6.0, 12.0, 20, 30, 20), "severe": (9.0, 15.0, 30, 50, 30), "extreme": (12.0, 20.0, 50, 100, 50)}
        for name, (m, s_, wm, ws, wh) in sev.items():
            cfg = configure(base, net__num_ues=20, net__num_bs=2, net__num_sat=2, dis__mild_shadowing_db=m, dis__severe_shadowing_db=s_,
                            dis__mild_window_slots=wm, dis__severe_window_slots=ws, dis__handover_window_slots=wh)
            for s in range(1, args.seeds + 1):
                tasks.append(dict(exp="C", cfg=cfg, seed=s, L=6, label=name))
    if args.exp in ("D", "all"):
        for L in (1, 3, 5, 6):
            cfg = configure(base, net__num_ues=20, net__num_bs=2, net__num_sat=2)
            for s in range(1, args.seeds + 1):
                tasks.append(dict(exp="D", cfg=cfg, seed=s, L=L, label=f"L={L}"))
    return tasks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="all")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--seeds-small", type=int, default=5)
    ap.add_argument("--qaoa-iters", type=int, default=40)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()
    tasks = build_tasks(args)
    print(f"{len(tasks)} tasks on {args.workers} workers", flush=True)
    t0 = time.time(); rows = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(evaluate, t): (t["exp"], t["label"], t["seed"]) for t in tasks}
        done = 0
        for f in as_completed(futs):
            done += 1
            try:
                rows.extend(f.result())
            except Exception as e:
                print("FAILED", futs[f], repr(e), flush=True)
            print(f"  {done}/{len(tasks)} {futs[f]} {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(RES / "validation_compact_raw.csv", index=False)
    summ = df.groupby(["exp", "label", "solver"]).agg(
        gap_mean=("gap_pct", "mean"), gap_max=("gap_pct", "max"),
        optimal_frac=("gap_pct", lambda v: (np.abs(v.dropna()) < 1e-6).mean() if v.notna().any() else np.nan),
        feasible_frac=("feasible", "mean"), eta_mean=("eta", "mean"), time_mean_s=("time_s", "mean"),
        qubits_max=("qubits", "max"), qubits_mean=("qubits", "mean"), n=("seed", "count")).reset_index()
    summ.to_csv(RES / "validation_compact_summary.csv", index=False)
    pd.set_option("display.width", 250)
    for exp in sorted(summ.exp.unique()):
        d = summ[summ.exp == exp]
        print(f"\n=== Exp {exp}: mean gap % (feasible solutions) ===")
        print(d.pivot_table(index="label", columns="solver", values="gap_mean").round(2).to_string())
        print("-- qubits (max) --"); print(d.pivot_table(index="label", columns="solver", values="qubits_max").round(0).to_string())
    print(f"done in {time.time()-t0:.0f}s", flush=True)
