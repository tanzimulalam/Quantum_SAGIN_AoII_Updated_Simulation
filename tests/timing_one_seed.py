import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure, run_seed
cfg = FullConfig(); cfg.solver.solver = "sa"
cfg = configure(cfg, net__num_ues=10, net__num_bs=2, net__num_sat=2)
t0 = time.time()
rows = run_seed({"cfg": cfg, "seed": 1, "policies": ["random", "threshold", "nominal", "sentinel"], "sweep": "t", "x_label": "U", "x_value": 10})
print(f"one seed, 10 UEs, all policies, both disruption modes: {time.time()-t0:.0f}s")
cols = ["policy","disruption_mode","average_aoii","peak_aoii","delivery_ratio","informative_ratio","sum_rate_mbps","latency_ms","sat_delivery_share","sat_scheduling_share","budget_violation_fraction","certified_eta_mean","certificate_holds","epochs","qubits_max","solve_time_s","forced_fallback_ues","disruption_events","wall_time_s"]
print(" ".join(f"{c[:14]:>14}" for c in cols))
for r in rows:
    print(" ".join(f"{(round(r[c],3) if isinstance(r[c], float) else r[c])!s:>14}" for c in cols))
