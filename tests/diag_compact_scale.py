import sys, pathlib, time, copy
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.compact import compact_sentinel_solve, prune_candidates, admm_compact, build_compact_qubo, _shared_sats, greedy_sel, anneal_compact
from run_validation import make_instance

for U, B, S in ((50, 4, 3), (100, 8, 5)):
    cfg = configure(FullConfig(), net__num_ues=U, net__num_bs=B, net__num_sat=S, solver__solver="sa_xy", solver__sa_sweeps=200, solver__sa_restarts=2)
    inst = make_instance(cfg, 1, 6)
    ilp = solve_p3_exact(inst)["eta"]
    pr = prune_candidates(inst, 4)
    print(f"\n### U={U}: ILP {ilp:.3f}; vars {inst.num_vars} -> pruned {pr.num_vars}; domains {np.bincount(inst.domain_of_ue)}; shared sats {_shared_sats(pr)}; caps {inst.cap_units}")
    # (i) centralized (K=1) compact with dual loop
    c1 = copy.copy(pr); c1.domain_of_ue = np.zeros(pr.num_ues, dtype=int); c1.domain_of_bs = np.zeros(pr.num_bs, dtype=int)
    r = compact_sentinel_solve(c1, cfg.solver, seed=1, outer_iterations=8)
    print(f"  centralized compact dual: eta {r.eta:.3f} ({100*(r.eta/ilp-1):+.1f}%) feas={r.feasible}; eta trace {[round(e,3) for e in r.eta_trace]}")
    # (ii) centralized, uniform weights only
    r = compact_sentinel_solve(c1, cfg.solver, seed=1, outer_iterations=1)
    print(f"  centralized, uniform weights only: eta {r.eta:.3f} ({100*(r.eta/ilp-1):+.1f}%)")
    # (iii) K=2 ADMM with uniform weights, inspect rounds
    rng = np.random.default_rng(1); w = np.ones(6)/6
    x, used, qubits, infos, params, rounds = admm_compact(pr, w, cfg.solver, rng, 1)
    print(f"  K=2 ADMM uniform weights: eta {pr.worst_case(x)[0]:.3f} ({100*(pr.worst_case(x)[0]/ilp-1):+.1f}%) feasible={pr.is_feasible(x)} rounds={rounds} qubits={qubits} usage={pr.node_usage_units(x)}")
    # (iv) K=2 full dual loop with trace
    r = compact_sentinel_solve(pr, cfg.solver, seed=1, outer_iterations=8)
    print(f"  K=2 compact dual: eta {r.eta:.3f} ({100*(r.eta/ilp-1):+.1f}%) feas={r.feasible}; eta trace {[round(e,3) for e in r.eta_trace]}")
    # (v) quality of a single domain solve: anneal vs exact ILP on that domain alone (uniform weights, no coupling)
    shared = _shared_sats(pr)
    z = {int(j): pr.cap_units[j]/2 for j in shared}; u = {int(j): 0.0 for j in shared}
    for k in range(2):
        dq = build_compact_qubo(pr, k, w, z, u, 1.0, shared)
        g = greedy_sel(dq, pr); eg = dq.assignment_energy(g, pr)
        t0 = time.time(); sel, e = anneal_compact(dq, pr, sweeps=200, restarts=2, rng=np.random.default_rng(0), init=g)
        print(f"  domain {k}: n={dq.n}, greedy energy {eg:.3f}, anneal energy {e:.3f} ({time.time()-t0:.1f}s), own nodes {dq.own_nodes}, lam_cap {dq.lam_cap:.2f}")
