import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.solvers.greedy import greedy_assign, local_search
from sentinel.compact import compact_sentinel_solve, prune_candidates
from run_validation import make_instance

print("=== classical inner solver (one-hot annealer), L=6, k_cand=4 ===", flush=True)
for U, B, S in ((10, 2, 2), (20, 2, 2), (50, 4, 3), (100, 8, 5)):
    cfg = configure(FullConfig(), net__num_ues=U, net__num_bs=B, net__num_sat=S, solver__solver="sa_xy",
                    solver__sa_sweeps=200, solver__sa_restarts=2)
    for seed in (1, 2):
        inst = make_instance(cfg, seed, 6)
        ilp = solve_p3_exact(inst)["eta"]
        gl = inst.worst_case(local_search(inst, greedy_assign(inst)))[0]
        ilp_pruned = solve_p3_exact(prune_candidates(inst, 4))["eta"]
        t0 = time.time()
        r = compact_sentinel_solve(inst, cfg.solver, seed=seed, outer_iterations=8, k_cand=4)
        print(f"U={U:>3} seed {seed}: ILP {ilp:.3f} | ILP on pruned(k=4) {100*(ilp_pruned/ilp-1):+.1f}% | Greedy+LS {100*(gl/ilp-1):+.1f}% | "
              f"compact dual {r.eta:.3f} ({100*(r.eta/ilp-1):+.1f}%) feas={r.feasible} qubits={max(r.qubits_per_domain)} "
              f"admm rounds={r.admm_rounds_total} {time.time()-t0:.1f}s", flush=True)

print("\n=== XY-mixer QAOA inner solver (2 BS + 2 SAT, L=6, k_cand=4, depth 1) ===", flush=True)
for U in (4, 6, 8):
    cfg = configure(FullConfig(), net__num_ues=U, net__num_bs=2, net__num_sat=2, solver__solver="qaoa_xy",
                    solver__qaoa_depth=1, solver__qaoa_shots=512, solver__qaoa_maxiter=40, solver__max_qaoa_qubits=40,
                    solver__admm_max_rounds=4)
    for seed in (1, 2):
        inst = make_instance(cfg, seed, 6)
        ilp = solve_p3_exact(inst)["eta"]
        t0 = time.time()
        r = compact_sentinel_solve(inst, cfg.solver, seed=seed, outer_iterations=4, k_cand=4)
        qi = r.qaoa_info[-1] if r.qaoa_info else {}
        print(f"U={U} seed {seed}: ILP {ilp:.3f} | compact QAOA-XY {r.eta:.3f} ({100*(r.eta/ilp-1):+.1f}%) feas={r.feasible} "
              f"qubits={r.qubits_per_domain} solves={len(r.qaoa_info)} feasible-sample-frac={qi.get('feasible_sample_fraction', float('nan')):.2f} "
              f"2q-gates={qi.get('two_qubit_gates', '?')} depth={qi.get('circuit_depth_transpiled', '?')} {time.time()-t0:.0f}s", flush=True)
