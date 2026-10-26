"""Does the 100-UE compact gap close with more ADMM rounds / outer iterations?"""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.compact import compact_sentinel_solve
from run_validation import make_instance

for seed in (1, 2):
    cfg = configure(FullConfig(), net__num_ues=100, net__num_bs=8, net__num_sat=5, net__num_domains=8, solver__solver="sa_xy",
                    solver__sa_sweeps=400, solver__sa_restarts=4)
    inst = make_instance(cfg, seed, 6)
    ilp = solve_p3_exact(inst)["eta"]
    for rounds, outer, tol in ((20, 8, 1e-2), (60, 8, 1e-2), (60, 12, 1e-3)):
        cfg.solver.admm_max_rounds = rounds; cfg.solver.admm_tol = tol
        t0 = time.time()
        r = compact_sentinel_solve(inst, cfg.solver, seed=seed, outer_iterations=outer, k_cand=4)
        print(f"U=100 K=8 seed {seed}: ILP {ilp:.3f} | rounds<={rounds}, outer={outer}, tol={tol}: eta {r.eta:.3f} ({100*(r.eta/ilp-1):+.1f}%) "
              f"feas={r.feasible} total rounds={r.admm_rounds_total} qubits={max(r.qubits_per_domain)} {time.time()-t0:.0f}s "
              f"trace={[round(e, 3) for e in r.eta_trace]}", flush=True)
