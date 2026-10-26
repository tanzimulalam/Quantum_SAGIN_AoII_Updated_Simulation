import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sentinel.config import FullConfig
from sentinel.experiments import configure, run_seed
cfg = FullConfig(); cfg.solver.solver = "sa"
cfg = configure(cfg, net__num_ues=8, net__num_bs=2, net__num_sat=2, sim__duration_slots=6000)
t0 = time.time()
rows = run_seed({"cfg": cfg, "seed": 2, "policies": ["random", "threshold", "nominal", "sentinel", "sentinel_triggered"], "sweep": "t", "x_label": "U", "x_value": 8, "disruption_modes": ["on"]})
print(f"{time.time()-t0:.0f}s")
for r in rows:
    print(f"{r['policy']:>18} aoii={r['average_aoii']:.3f} peak={r['peak_aoii']:.0f} deliv={r['delivery_ratio']:.3f} info={r['informative_ratio']:.3f} sat={r['sat_delivery_share']:.2f} cert={r['certified_eta_mean']:.3f} holds={r['certificate_holds']}")
