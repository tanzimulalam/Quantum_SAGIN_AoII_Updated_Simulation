"""Experiment drivers: one worker function per seed so sweeps can run in parallel processes."""
from __future__ import annotations

import copy
import time
from dataclasses import replace
from typing import Dict, List, Tuple

import numpy as np

from .config import FullConfig
from .simulator import make_episode, plan_schedule, run_policy


def configure(base: FullConfig, **over) -> FullConfig:
    cfg = copy.deepcopy(base)
    for key, val in over.items():
        sect, name = key.split("__")
        setattr(getattr(cfg, sect), name, val)
    return cfg


def run_seed(task: Dict) -> List[Dict]:
    """task: {cfg: FullConfig, seed: int, policies: [...], sweep: str, x_label: str, x_value: ...}"""
    cfg: FullConfig = task["cfg"]
    seed = task["seed"]
    t0 = time.time()
    rows: List[Dict] = []
    # episode with the stochastic disruption process
    cfg_on = configure(cfg, dis__enabled=True)
    ep_on = make_episode(cfg_on, seed)
    # same episode without disruption events (identical topology, sources, fading)
    cfg_off = configure(cfg, dis__enabled=False)
    ep_off = make_episode(cfg_off, seed)
    plans = {}
    if any(p in task["policies"] for p in ("sentinel", "sentinel_triggered", "sentinel_capped_trigger")):
        plans["sentinel"] = plan_schedule(ep_on, num_scenarios=6, solver_seed=seed)
        plans["sentinel_triggered"] = plans["sentinel"]
        plans["sentinel_capped_trigger"] = plans["sentinel"]
    if "nominal" in task["policies"]:
        plans["nominal"] = plan_schedule(ep_on, num_scenarios=1, solver_seed=seed)
    for dis_flag, ep in (("on", ep_on), ("off", ep_off)):
        if task.get("disruption_modes") and dis_flag not in task["disruption_modes"]:
            continue
        for pol in task["policies"]:
            r = run_policy(ep, pol, plan=plans.get(pol))
            row = r.to_row()
            row.update({"sweep": task["sweep"], "x_label": task["x_label"], "x_value": task["x_value"],
                        "disruption_mode": dis_flag, "num_scenarios": 6 if pol in ("sentinel", "sentinel_triggered", "sentinel_capped_trigger") else (1 if pol == "nominal" else 0),
                        "disruption_events": ep.disruption.events, "natural_handovers": ep.disruption.natural_handovers,
                        "nlos_pass_fraction": ep.disruption.nlos_fraction, "sat_model": cfg.net.sat_model, "ntn_model": cfg.dis.ntn_model})
            rows.append(row)
    for row in rows:
        row["seed_wall_s"] = time.time() - t0
    return rows


def summarize(rows: List[Dict], keys=("sweep", "x_value", "policy", "disruption_mode")) -> List[Dict]:
    import pandas as pd
    df = pd.DataFrame(rows)
    num = [c for c in df.columns if df[c].dtype.kind in "fi" and c not in ("seed", "x_value", "num_scenarios")]
    out = []
    for key, g in df.groupby(list(keys)):
        d = dict(zip(keys, key))
        d["n"] = len(g)
        for c in num:
            v = g[c].astype(float)
            d[f"{c}_mean"] = v.mean()
            d[f"{c}_std"] = v.std(ddof=1) if len(v) > 1 else 0.0
            d[f"{c}_ci95"] = 1.96 * d[f"{c}_std"] / np.sqrt(len(v)) if len(v) > 1 else 0.0
            d[f"{c}_median"] = v.median()
            d[f"{c}_q25"] = v.quantile(0.25)
            d[f"{c}_q75"] = v.quantile(0.75)
        out.append(d)
    return out
