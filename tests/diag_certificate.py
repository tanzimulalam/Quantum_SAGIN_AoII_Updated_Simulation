"""Why did the certificate-holds fraction drop from 0.98 (epigraph run) to 0.86 (compact run)? Per-epoch comparison."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.simulator import make_episode, plan_schedule, run_policy

for seed in (3, 7):
    for form in ("epigraph", "compact"):
        cfg = configure(FullConfig(), net__num_ues=10, net__num_bs=2, net__num_sat=2, solver__solver="sa_xy", solver__formulation=form)
        ep = make_episode(cfg, seed)
        plan = plan_schedule(ep, num_scenarios=6, solver_seed=seed)
        res = run_policy(ep, "sentinel", plan=plan)
        certs = np.array([e.eta_certified for e in plan]); solver_eta = np.array([e.eta_solver for e in plan])
        forced = np.array([e.forced for e in plan]); lens = np.array([e.end_interval - e.start_interval for e in plan])
        print(f"seed {seed} {form:9s}: avg AoII {res.average_aoii:.3f}, holds {res.certificate_holds:.3f}, epochs {len(plan)}, "
              f"cert mean {certs.mean():.2f} min {certs.min():.2f} max {certs.max():.2f}; solver-eta mean {solver_eta.mean():.2f}; "
              f"epochs with forced UEs {int((forced>0).sum())}; cert==solver-eta in {int(np.isclose(certs, solver_eta).sum())} epochs")
        if form == "compact":
            bad = [(e.start_interval, e.end_interval, round(e.eta_certified, 2), round(e.eta_solver, 2), e.forced) for e in plan if e.eta_certified < e.eta_solver - 1e-6]
            print("   epochs where certificate < solver eta (should not happen):", bad[:5])
