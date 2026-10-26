"""Disruption scenario set L for the robust optimizer and the stochastic disruption process for the simulator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from .config import DisruptionConfig


@dataclass
class Scenario:
    name: str
    sat_loss_db: np.ndarray    # (S,) extra path loss per satellite; inf = complete link loss (handover)
    window_slots: int          # T^dis


def build_scenarios(cfg: DisruptionConfig, num_sat: int, num_scenarios: int = 6) -> List[Scenario]:
    """Scenario set: nominal, mild shadowing, severe shadowing, handover of each SAT, joint.

    num_scenarios lets the validation experiments use L in {1, 3, 5, 6}: the list is truncated in
    order of increasing severity so that L=1 is the nominal-only (non-robust) problem.
    """
    S = num_sat
    scen = [Scenario("nominal", np.zeros(S), 0)]
    scen.append(Scenario("mild_shadowing", np.full(S, cfg.mild_shadowing_db), cfg.mild_window_slots))
    scen.append(Scenario("severe_shadowing", np.full(S, cfg.severe_shadowing_db), cfg.severe_window_slots))
    for j in range(S):
        loss = np.zeros(S)
        loss[j] = np.inf
        scen.append(Scenario(f"handover_sat{j}", loss, cfg.handover_window_slots))
    scen.append(Scenario("joint", np.full(S, np.inf), cfg.severe_window_slots))
    return scen[:num_scenarios]


class DisruptionProcess:
    """Realized extra loss on each UE-SAT link per slot, drawn per orchestration interval.

    - shadowing events are per link (local obstruction, rain cell): mild or severe, lasting their window
    - handover failures are per satellite (affects all its UEs): complete loss for handover_window_slots
    Natural handovers between successive passes are already in the geometry (visibility gaps).
    """

    def __init__(self, cfg: DisruptionConfig, num_ues: int, num_sat: int, num_slots: int, interval_slots: int,
                 rng: np.random.Generator):
        self.loss_db = np.zeros((num_slots, num_sat, num_ues), dtype=np.float32)
        self.events = 0
        if not cfg.enabled:
            return
        n_int = int(np.ceil(num_slots / interval_slots))
        for k in range(n_int):
            t0 = k * interval_slots
            for j in range(num_sat):
                if rng.random() < cfg.p_handover_failure_per_sat:
                    t1 = min(t0 + cfg.handover_window_slots, num_slots)
                    self.loss_db[t0:t1, j, :] = np.inf
                    self.events += 1
                sh = rng.random(num_ues) < cfg.p_shadowing_event_per_link
                for i in np.flatnonzero(sh):
                    if rng.random() < 0.5:
                        t1 = min(t0 + cfg.mild_window_slots, num_slots)
                        self.loss_db[t0:t1, j, i] = np.maximum(self.loss_db[t0:t1, j, i], cfg.mild_shadowing_db)
                    else:
                        t1 = min(t0 + cfg.severe_window_slots, num_slots)
                        self.loss_db[t0:t1, j, i] = np.maximum(self.loss_db[t0:t1, j, i], cfg.severe_shadowing_db)
                    self.events += 1
