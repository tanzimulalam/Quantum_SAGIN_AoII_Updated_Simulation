"""Does a gentler exponentiated-gradient step reduce the 100-UE oscillation of the compact dual loop?"""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.compact import compact_sentinel_solve
from run_validation import make_instance

cfg = configure(FullConfig(), net__num_ues=100, net__num_bs=8, net__num_sat=5, net__num_domains=8, solver__solver="sa_xy",
                solver__sa_sweeps=400, solver__sa_restarts=4, solver__admm_max_rounds=20)
for seed in (1, 2):
    inst = make_instance(cfg, seed, 6)
    ilp = solve_p3_exact(inst)["eta"]
    for step in (0.5, 1.0):
        t0 = time.time()
        r = compact_sentinel_solve(inst, cfg.solver, seed=seed, outer_iterations=8, step=step, k_cand=4)
        print(f"U=100 K=8 seed {seed} step={step}: ILP {ilp:.3f} | eta {r.eta:.3f} ({100*(r.eta/ilp-1):+.1f}%) feas={r.feasible} "
              f"{time.time()-t0:.0f}s trace={[round(e, 3) for e in r.eta_trace]}", flush=True)
