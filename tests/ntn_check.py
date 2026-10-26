"""One short seed with TLE passes + NTN channel: plausibility of NLOS fraction, satellite usage and AoII."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure, run_seed

for sat_model, ntn in (("synthetic", False), ("tle", False), ("tle", True)):
    cfg = configure(FullConfig(), net__num_ues=10, net__num_bs=2, net__num_sat=2, sim__duration_slots=12000, solver__solver="sa_xy",
                    solver__formulation="compact", net__sat_model=sat_model, dis__ntn_model=ntn,
                    net__min_elevation_deg=25.0 if sat_model == "tle" else 10.0)
    t0 = time.time()
    rows = run_seed({"cfg": cfg, "seed": 4, "policies": ["threshold", "nominal", "sentinel", "sentinel_capped_trigger"], "sweep": "t",
                     "x_label": "U", "x_value": 10, "disruption_modes": ["on"]})
    print(f"\n=== sat_model={sat_model} ntn={ntn}  ({time.time()-t0:.0f}s) natural handovers={rows[0]['natural_handovers']} nlos pass fraction={rows[0]['nlos_pass_fraction']:.2f} events={rows[0]['disruption_events']}")
    for r in rows:
        print(f"{r['policy']:>24} aoii={r['average_aoii']:.3f} peak={r['peak_aoii']:.0f} deliv={r['delivery_ratio']:.3f} sat={r['sat_delivery_share']:.2f} "
              f"cert={r['certified_eta_mean']:.3f} holds={r['certificate_holds']} qubits={r['qubits_max']}")
