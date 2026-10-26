"""Validation against the exact minimax optimum of P3 (replaces the paper's Table II).

Experiments
  A  small scale, real QAOA on Aer:  U in {2,3,4,5,6}, 2 BS + 1 SAT, Q=1, H=2, L=2 (nominal + severe shadowing)
  B  network-size sweep (SA local solver): U in {10,25,50,75,100}, 2 BS + 2 SAT, Q=3, H=4, L=6
  C  disruption-severity sweep at U=20
  D  scenario-count sweep L in {1,3,5,6} at U=20 (gap measured on the L-scenario problem the solver saw)
Solvers: ILP exact (reference), SENTINEL (QAOA or SA + ADMM), monolithic SA on the centralized QUBO, Greedy, Greedy+LS.
"""
import sys, pathlib, time, argparse, json, os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.geometry import build_topology
from sentinel.sources import SourceSet
from sentinel.scenarios import build_scenarios
from sentinel.problem import build_instance
from sentinel.qubo import build_domain_qubo
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.solvers.sa import anneal_qubo
from sentinel.solvers.greedy import greedy_assign, local_search
from sentinel.admm import sentinel_solve, _network_repair

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def make_instance(cfg: FullConfig, seed: int, L: int):
    topo = build_topology(cfg.net, seed, num_intervals=120, interval_s=1.0)
    src = SourceSet(cfg.net.num_ues, cfg.src, seed)
    scen = build_scenarios(cfg.dis, cfg.net.num_sat, L)
    # choose the interval where the most satellites are visible to the most UEs
    score = topo.sat_visible.sum(axis=(0, 2))
    k = int(np.argmax(score))
    inst = build_instance(cfg, topo, src, scen, interval=k, horizon_intervals=3)
    return inst


def monolithic_sa(inst, cfg, seed):
    import copy
    inst1 = copy.copy(inst)
    inst1.domain_of_ue = np.zeros(inst.num_ues, dtype=int)
    inst1.domain_of_bs = np.zeros(inst.num_bs, dtype=int)
    dq = build_domain_qubo(inst1, 0, {}, {}, 1.0, cfg.solver.eta_resolution, np.array([], dtype=int))
    t0 = time.time()
    w, e = anneal_qubo(dq.Q, sweeps=cfg.solver.sa_sweeps, restarts=cfg.solver.sa_restarts, rng=np.random.default_rng(seed))
    x = np.zeros(inst.num_vars); x[dq.x_vars] = dq.decode(w)
    feasible_raw = inst.is_feasible(x)
    if not feasible_raw:
        x = _network_repair(inst, x)
    return x, dq.n, time.time() - t0, feasible_raw


def evaluate(task):
    exp, cfg, seed, L, label = task["exp"], task["cfg"], task["seed"], task["L"], task["label"]
    inst = make_instance(cfg, seed, L)
    rows = []
    base = dict(exp=exp, label=label, seed=seed, L=L, num_ues=cfg.net.num_ues, num_vars=inst.num_vars,
                forced=int(inst.forced_fallback.sum()))
    ilp = solve_p3_exact(inst, time_limit_s=300)
    ref = ilp["eta"] if (ilp["x"] is not None and inst.is_feasible(ilp["x"])) else np.nan   # NaN gap if the instance is infeasible
    rows.append(dict(base, solver="ILP exact", eta=ref, feasible=ilp["x"] is not None and inst.is_feasible(ilp["x"]),
                     time_s=ilp["time_s"], gap_pct=0.0, qubits=0, local_feasible_fraction=np.nan))
    g = greedy_assign(inst); eg, _ = inst.worst_case(g)
    rows.append(dict(base, solver="Greedy", eta=eg, feasible=inst.is_feasible(g), time_s=0.0, gap_pct=100 * (eg / ref - 1), qubits=0, local_feasible_fraction=np.nan))
    t0 = time.time(); gl = local_search(inst, g); egl, _ = inst.worst_case(gl)
    rows.append(dict(base, solver="Greedy+LS", eta=egl, feasible=inst.is_feasible(gl), time_s=time.time() - t0, gap_pct=100 * (egl / ref - 1), qubits=0, local_feasible_fraction=np.nan))
    if task.get("monolithic", True):
        x, n, t, fr = monolithic_sa(inst, cfg, seed); em, _ = inst.worst_case(x)
        rows.append(dict(base, solver="SA (monolithic QUBO)", eta=em, feasible=inst.is_feasible(x), time_s=t, gap_pct=100 * (em / ref - 1), qubits=n, local_feasible_fraction=float(fr)))
    import copy
    variants = []
    if cfg.solver.solver == "qaoa":
        variants.append(("SENTINEL (QAOA, Aer)", "qaoa", False))
        variants.append(("SENTINEL (SA-XY, one-hot-preserving)", "sa_xy", False))
    else:
        variants.append(("SENTINEL (SA on penalty QUBO)", "sa", False))
        variants.append(("SENTINEL (SA-XY, one-hot-preserving)", "sa_xy", False))
        variants.append(("SENTINEL (SA-XY) + LS polish", "sa_xy", True))
    for name, solver, polish in variants:
        scfg = copy.deepcopy(cfg.solver); scfg.solver = solver
        res = sentinel_solve(inst, scfg, seed=seed, check_exact=(solver == "qaoa"), polish=polish)
        rows.append(dict(base, solver=name, eta=res.eta, feasible=res.feasible, time_s=res.time_s, gap_pct=100 * (res.eta / ref - 1),
                         qubits=max(res.qubits_per_domain) if res.qubits_per_domain else 0, rounds=res.rounds,
                         local_feasible_fraction=res.local_feasible_fraction, onehot_fraction_raw=res.onehot_fraction_raw,
                         local_qubo_gap_mean=float(np.mean(res.local_gap_to_exact)) if res.local_gap_to_exact else np.nan,
                         qaoa_trace=json.dumps([round(v, 3) for v in res.qaoa_traces[0]]) if res.qaoa_traces else ""))
    return rows


def build_tasks(args):
    tasks = []
    base = FullConfig()
    if args.exp in ("A", "all"):
        for U in (2, 3, 4, 5, 6):
            cfg = configure(base, net__num_ues=U, net__num_bs=2, net__num_sat=1, radio__bandwidth_levels_mhz=(5.0,),
                            src__update_periods_slots=(5, 20), solver__eta_resolution=0.5, solver__solver="qaoa",
                            solver__max_qaoa_qubits=26, solver__qaoa_maxiter=args.qaoa_iters, solver__qaoa_shots=512,
                            solver__admm_max_rounds=6)
            for s in range(1, args.seeds_small + 1):
                tasks.append(dict(exp="A", cfg=cfg, seed=s, L=2, label=f"U={U}", monolithic=False))
    if args.exp in ("B", "all"):
        # node count scales with the network so that the instances stay capacity-feasible
        for U, B, S in ((10, 2, 2), (25, 2, 2), (50, 4, 3), (75, 6, 4), (100, 8, 5)):
            cfg = configure(base, net__num_ues=U, net__num_bs=B, net__num_sat=S, solver__solver="sa")
            for s in range(1, args.seeds + 1):
                tasks.append(dict(exp="B", cfg=cfg, seed=s, L=6, label=f"U={U}"))
    if args.exp in ("C", "all"):
        sev = {"mild": (3.0, 6.0, 10, 20, 10), "moderate": (6.0, 12.0, 20, 30, 20), "severe": (9.0, 15.0, 30, 50, 30),
               "extreme": (12.0, 20.0, 50, 100, 50)}
        for name, (m, s_, wm, ws, wh) in sev.items():
            cfg = configure(base, net__num_ues=20, net__num_bs=2, net__num_sat=2, solver__solver="sa",
                            dis__mild_shadowing_db=m, dis__severe_shadowing_db=s_, dis__mild_window_slots=wm,
                            dis__severe_window_slots=ws, dis__handover_window_slots=wh)
            for s in range(1, args.seeds + 1):
                tasks.append(dict(exp="C", cfg=cfg, seed=s, L=6, label=name))
    if args.exp in ("D", "all"):
        for L in (1, 3, 5, 6):
            cfg = configure(base, net__num_ues=20, net__num_bs=2, net__num_sat=2, solver__solver="sa")
            for s in range(1, args.seeds + 1):
                tasks.append(dict(exp="D", cfg=cfg, seed=s, L=L, label=f"L={L}"))
    return tasks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="all")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--seeds-small", type=int, default=5)
    ap.add_argument("--qaoa-iters", type=int, default=100)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    tasks = build_tasks(args)
    print(f"{len(tasks)} validation tasks on {args.workers} workers", flush=True)
    t0 = time.time(); rows = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(evaluate, t): (t["exp"], t["label"], t["seed"]) for t in tasks}
        done = 0
        for f in as_completed(futs):
            done += 1
            try:
                rows.extend(f.result())
                pd.DataFrame(rows).to_csv(RES / "validation_raw_partial.csv", index=False)   # incremental save
            except Exception as e:
                print("FAILED", futs[f], repr(e), flush=True)
            print(f"  {done}/{len(tasks)} {futs[f]} {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(rows)
    tag = f"_{args.tag}" if args.tag else ""
    df.to_csv(RES / f"validation_raw{tag}.csv", index=False)
    df["instance_feasible"] = df.groupby(["exp", "label", "seed"]).gap_pct.transform(lambda v: v.notna().any())
    df["gap_pct"] = np.where(df.feasible.astype(bool), df.gap_pct, np.nan)   # a gap is only meaningful for a feasible schedule
    summ = df.groupby(["exp", "label", "solver"]).agg(gap_mean=("gap_pct", "mean"), gap_max=("gap_pct", "max"),
                                                       optimal_frac=("gap_pct", lambda v: (np.abs(v.dropna()) < 1e-6).mean() if v.notna().any() else np.nan),
                                                       instances_feasible=("instance_feasible", "mean"),
                                                       eta_mean=("eta", lambda v: v[np.isfinite(v)].mean()),
                                                       feasible_frac=("feasible", "mean"), time_mean_s=("time_s", "mean"),
                                                       qubits_max=("qubits", "max"), n=("seed", "count"),
                                                       local_feasible=("local_feasible_fraction", "mean")).reset_index()
    summ.to_csv(RES / f"validation_summary{tag}.csv", index=False)
    print(summ.to_string(), flush=True)
    print(f"done in {time.time()-t0:.0f}s", flush=True)
