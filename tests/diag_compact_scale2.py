import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.compact import compact_sentinel_solve
from sentinel.admm import sentinel_solve
from run_validation import make_instance

for U, B, S in ((20, 2, 2), (50, 4, 3), (100, 8, 5)):
    for K in sorted({2, B}):
        cfg = configure(FullConfig(), net__num_ues=U, net__num_bs=B, net__num_sat=S, net__num_domains=K,
                        solver__solver="sa_xy", solver__sa_sweeps=400, solver__sa_restarts=4)
        for seed in (1, 2):
            inst = make_instance(cfg, seed, 6)
            ilp = solve_p3_exact(inst)["eta"]
            t0 = time.time(); r = compact_sentinel_solve(inst, cfg.solver, seed=seed, outer_iterations=8, k_cand=4); t1 = time.time() - t0
            t0 = time.time(); e = sentinel_solve(inst, cfg.solver, seed=seed, polish=False); t2 = time.time() - t0
            print(f"U={U:>3} K={K} seed {seed}: ILP {ilp:.3f} | compact dual {r.eta:.3f} ({100*(r.eta/ilp-1):+.1f}%) feas={r.feasible} "
                  f"qubits={max(r.qubits_per_domain)} rounds={r.admm_rounds_total} {t1:.0f}s | epigraph(SA-XY) {e.eta:.3f} "
                  f"({100*(e.eta/ilp-1):+.1f}%) feas={e.feasible} qubits={max(e.qubits_per_domain)} rounds={e.rounds} {t2:.0f}s", flush=True)
