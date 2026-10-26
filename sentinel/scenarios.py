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


# TR 38.811 Tables 6.6.1-1 / 6.6.2-1 / 6.6.2-2 (suburban; Ku values interpolated between the S- and Ka-band entries)
_NTN_EL = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90], dtype=float)
_NTN = {
    "suburban": {
        "p_los": np.array([78.2, 86.9, 91.9, 92.9, 93.5, 94.0, 94.9, 95.2, 99.8]) / 100.0,
        "clutter_db": np.array([24.5, 21.4, 20.2, 19.1, 18.7, 17.7, 16.9, 16.6, 16.6]),
        "sf_los_db": np.array([1.9, 1.6, 1.9, 2.3, 2.7, 3.1, 3.0, 3.6, 0.4]),
        "sf_nlos_db": np.array([10.7, 10.0, 11.2, 11.6, 11.8, 10.8, 10.8, 10.8, 10.8]),
    },
    "urban": {
        "p_los": np.array([24.6, 38.6, 49.3, 61.3, 72.6, 80.5, 91.9, 96.8, 99.2]) / 100.0,
        "clutter_db": np.array([34.3, 30.9, 29.0, 27.7, 26.8, 26.2, 25.8, 25.5, 25.5]),
        "sf_los_db": np.array([4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]),
        "sf_nlos_db": np.array([6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0]),
    },
}


def ntn_large_scale_loss(topology, cfg: DisruptionConfig, interval_slots: int, num_slots: int, rng: np.random.Generator):
    """Per-slot extra loss (T, S, U) on each UE-satellite link from the NTN large-scale model.

    For each (slot j, UE i, pass) the LOS/NLOS state and a slow shadow-fading value are drawn once at the elevation at
    which the pass starts (or the window starts); NLOS adds the clutter loss. Atmospheric absorption is
    zenith_db / sin(elevation) every interval. Returns (loss, nlos_fraction_of_pass_segments).
    """
    tab = _NTN[cfg.ntn_environment]
    S, T_int, U = topology.sat_elev_deg.shape
    loss = np.zeros((num_slots, S, U), dtype=np.float32)
    n_seg = 0; n_nlos = 0
    for j in range(S):
        vis = topology.sat_visible[j]                                   # (T_int, U)
        # pass segments: maximal runs of consecutive visible intervals; a TLE handover also starts a new segment
        switch_ints = {k for (jj, k, _n) in (topology.sat_switches or []) if jj == j}
        for i in range(U):
            k = 0
            while k < T_int:
                if not vis[k, i]:
                    k += 1; continue
                k0 = k
                while k + 1 < T_int and vis[k + 1, i] and (k + 1) not in switch_ints:
                    k += 1
                k1 = k                                                   # inclusive
                el0 = float(np.clip(topology.sat_elev_deg[j, k0, i], 10.0, 90.0))
                p_los = float(np.interp(el0, _NTN_EL, tab["p_los"]))
                los = rng.random() < p_los
                sf = rng.normal(0.0, float(np.interp(el0, _NTN_EL, tab["sf_los_db" if los else "sf_nlos_db"])))
                extra = sf + (0.0 if los else float(np.interp(el0, _NTN_EL, tab["clutter_db"])))
                n_seg += 1; n_nlos += int(not los)
                for kk in range(k0, k1 + 1):
                    el = float(np.clip(topology.sat_elev_deg[j, kk, i], 5.0, 90.0))
                    atm = cfg.ntn_zenith_atmospheric_db / np.sin(np.radians(el))
                    t0, t1 = kk * interval_slots, min((kk + 1) * interval_slots, num_slots)
                    loss[t0:t1, j, i] = extra + atm
                k = k1 + 1
    return loss, (n_nlos / n_seg if n_seg else 0.0)


class DisruptionProcess:
    """Realized extra loss on each UE-SAT link per slot, drawn per orchestration interval.

    - shadowing events are per link (local obstruction, rain cell): mild or severe, lasting their window
    - handover failures are per satellite (affects all its UEs): complete loss for handover_window_slots
    Natural handovers between successive passes are already in the geometry (visibility gaps).
    """

    def __init__(self, cfg: DisruptionConfig, num_ues: int, num_sat: int, num_slots: int, interval_slots: int,
                 rng: np.random.Generator, switches=None, topology=None):
        self.loss_db = np.zeros((num_slots, num_sat, num_ues), dtype=np.float32)
        self.events = 0
        self.natural_handovers = 0
        self.nlos_fraction = 0.0
        if cfg.ntn_model and topology is not None and num_sat > 0:
            ntn, self.nlos_fraction = ntn_large_scale_loss(topology, cfg, interval_slots, num_slots, rng)
            self.loss_db += ntn
        if switches:
            # a natural handover between successive satellites interrupts the slot for handover_window_slots
            for (j, k, _name) in switches:
                if k == 0:
                    continue
                t0 = k * interval_slots; t1 = min(t0 + cfg.handover_window_slots, num_slots)
                self.loss_db[t0:t1, j, :] = np.inf
                self.natural_handovers += 1
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
