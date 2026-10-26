"""Visibility statistics of the TLE-driven pass model over the MTSU site for a 10-minute window."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.geometry import build_topology
from sentinel.tle_geometry import load_tles, DATA_DIR

t0 = time.time(); arr, names, sats = load_tles(str(DATA_DIR / "starlink_tle_snapshot.txt")); print(f"{len(sats)} satellites loaded in {time.time()-t0:.1f}s")
for min_el in (10.0, 25.0):
    for seed in (1, 2, 3):
        cfg = configure(FullConfig(), net__num_ues=10, net__num_bs=2, net__num_sat=2, net__sat_model="tle", net__min_elevation_deg=min_el)
        t0 = time.time(); topo = build_topology(cfg.net, seed, 600, 1.0); dt_ = time.time() - t0
        vis = topo.sat_visible.mean(axis=(1, 2))
        el = topo.sat_elev_deg[topo.sat_visible]
        rg = topo.sat_range_m[topo.sat_visible]
        sw = topo.sat_switches
        print(f"min_el={min_el:>4} seed {seed}: build {dt_:.1f}s | visible fraction per slot {np.round(vis, 3)} | elevation {el.min():.0f}-{el.max():.0f} deg "
              f"(median {np.median(el):.0f}) | slant range {rg.min()/1e3:.0f}-{rg.max()/1e3:.0f} km | handovers {len(sw)} "
              f"(slot0: {sum(1 for s in sw if s[0]==0)}, slot1: {sum(1 for s in sw if s[0]==1)})")
