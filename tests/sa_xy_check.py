import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.geometry import build_topology
from sentinel.sources import SourceSet
from sentinel.scenarios import build_scenarios
from sentinel.problem import build_instance
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.solvers.greedy import greedy_assign, local_search
from sentinel.admm import sentinel_solve
for U, B, S in ((10, 2, 2), (20, 2, 2), (50, 4, 3)):
    cfg = configure(FullConfig(), net__num_ues=U, net__num_bs=B, net__num_sat=S)
    for seed in (1, 2):
        topo = build_topology(cfg.net, seed, 120, 1.0); src = SourceSet(U, cfg.src, seed)
        k = int(np.argmax(topo.sat_visible.sum(axis=(0, 2))))
        inst = build_instance(cfg, topo, src, build_scenarios(cfg.dis, S, 6), k, 3)
        ilp = solve_p3_exact(inst)
        g = local_search(inst, greedy_assign(inst)); eg = inst.worst_case(g)[0]
        out = [f"U={U:>3} seed {seed}: ILP {ilp['eta']:.4f} | Greedy+LS gap {100*(eg/ilp['eta']-1):5.2f}%"]
        for solver in ("sa", "sa_xy"):
            cfg.solver.solver = solver
            t0 = time.time(); r = sentinel_solve(inst, cfg.solver, seed=seed, polish=False)
            out.append(f"{solver}: gap {100*(r.eta/ilp['eta']-1):6.2f}% feas={r.feasible} localfeas={r.local_feasible_fraction:.2f} onehot={r.onehot_fraction_raw:.2f} rounds={r.rounds} {time.time()-t0:.1f}s")
        print(" | ".join(out), flush=True)
