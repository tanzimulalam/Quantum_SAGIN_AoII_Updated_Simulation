"""Robust binary instance of VANGUARD (paper Section IV-A).

Builds, for one decision horizon, the admissible combinations (m, q, h) of every UE and their
scenario-dependent time-average AoII cost coefficients psi_{imqh}^{(l)} = Psi_i(Y(l)) / Y(l).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np

from .config import FullConfig
from .channel import nominal_rate_table
from .scenarios import Scenario
from .sources import SourceSet


@dataclass
class RobustInstance:
    num_ues: int
    num_bs: int
    num_sat: int
    scenarios: List[Scenario]
    # variables
    var_ue: np.ndarray        # (N,) UE index
    var_node: np.ndarray      # (N,) node index (BSs first, then SATs)
    var_q: np.ndarray         # (N,) bandwidth level index
    var_h: np.ndarray         # (N,) period index
    var_bw_units: np.ndarray  # (N,) bandwidth in units of Delta_beta (integer)
    var_bw_mhz: np.ndarray    # (N,)
    var_period: np.ndarray    # (N,) slots
    cost: np.ndarray          # (N, L) psi^{(l)} (per-UE time-average AoII, NOT divided by |U|)
    cap_units: np.ndarray     # (M,) node capacities in units of Delta_beta
    cap_mhz: np.ndarray       # (M,)
    domain_of_ue: np.ndarray  # (U,)
    domain_of_bs: np.ndarray  # (B,)
    forced_fallback: np.ndarray  # (U,) True if UE had no admissible combination and got its least-bad one
    nominal_rate: np.ndarray  # (U, M, Q) bps
    visible: np.ndarray       # (U, M)

    @property
    def num_vars(self) -> int:
        return self.var_ue.shape[0]

    @property
    def num_nodes(self) -> int:
        return self.num_bs + self.num_sat

    @property
    def L(self) -> int:
        return len(self.scenarios)

    def vars_of_ue(self, i: int) -> np.ndarray:
        return np.flatnonzero(self.var_ue == i)

    def network_cost(self, x: np.ndarray) -> np.ndarray:
        """Per-scenario network-average AoII of a 0/1 assignment x (length N)."""
        return (self.cost * x[:, None]).sum(0) / self.num_ues

    def worst_case(self, x: np.ndarray):
        c = self.network_cost(x)
        l = int(np.argmax(c))
        return float(c[l]), l

    def node_usage_units(self, x: np.ndarray) -> np.ndarray:
        return np.bincount(self.var_node, weights=self.var_bw_units * x, minlength=self.num_nodes)

    def is_feasible(self, x: np.ndarray) -> bool:
        if x.shape[0] != self.num_vars:
            return False
        if np.any(np.bincount(self.var_ue, weights=x, minlength=self.num_ues) != 1):
            return False
        return bool(np.all(self.node_usage_units(x) <= self.cap_units + 1e-9))

    def assignment_from_x(self, x: np.ndarray) -> np.ndarray:
        """Return (U,) index of selected variable per UE (-1 if none)."""
        sel = np.full(self.num_ues, -1, dtype=int)
        for v in np.flatnonzero(x > 0.5):
            sel[self.var_ue[v]] = v
        return sel

    def x_from_assignment(self, sel: np.ndarray) -> np.ndarray:
        x = np.zeros(self.num_vars)
        x[sel[sel >= 0]] = 1.0
        return x


def build_instance(cfg: FullConfig, topology, sources: SourceSet, scenarios: List[Scenario],
                   interval: int, horizon_intervals: int = 1, overhead_slots: int = 0,
                   budget: Optional[float] = None) -> RobustInstance:
    rc, sc, so = cfg.radio, cfg.src, cfg.solver
    U, B, S = topology.num_ues, topology.num_bs, topology.num_sat
    M = B + S
    levels_mhz = np.array(rc.bandwidth_levels_mhz)
    Q, H = len(levels_mhz), len(sc.update_periods_slots)
    T_s = sc.slot_ms * 1e-3
    D = sc.packet_bits
    budget = sc.aoii_budget if budget is None else budget
    # predictive visibility over the horizon (ephemeris): a SAT is usable only if visible throughout
    rates, visible = nominal_rate_table(topology, interval, rc)
    for k in range(1, horizon_intervals):
        t = min(interval + k, topology.num_intervals - 1)
        r2, v2 = nominal_rate_table(topology, t, rc)
        visible &= v2
        rates = np.minimum(rates, r2)
    # scenario rates (only satellites are affected)
    L = len(scenarios)
    scen_rates = np.empty((L, U, M, Q))
    for l, sc_ in enumerate(scenarios):
        if np.all(sc_.sat_loss_db == 0):
            scen_rates[l] = rates
        else:
            r_l, _ = nominal_rate_table(topology, interval, rc, extra_sat_loss_db=sc_.sat_loss_db)
            for k in range(1, horizon_intervals):
                t = min(interval + k, topology.num_intervals - 1)
                r2, _ = nominal_rate_table(topology, t, rc, extra_sat_loss_db=sc_.sat_loss_db)
                r_l = np.minimum(r_l, r2)
            scen_rates[l] = r_l
    periods = np.array(sc.update_periods_slots)
    windows = np.array([s.window_slots for s in scenarios])
    # enumerate all combinations
    ii, mm, qq, hh = np.meshgrid(np.arange(U), np.arange(M), np.arange(Q), np.arange(H), indexing="ij")
    ii, mm, qq, hh = ii.ravel(), mm.ravel(), qq.ravel(), hh.ravel()
    vis = visible[ii, mm]
    nominal_ok = rates[ii, mm, qq] * T_s >= D
    # outage duration tau_{imq}(l): window if SAT link cannot deliver within a slot under scenario l
    is_sat = mm >= B
    deliver_l = scen_rates[:, ii, mm, qq] * T_s >= D                   # (L, N_all)
    tau = np.where(is_sat[None, :] & ~deliver_l, windows[:, None], 0)  # (L, N_all)
    Y = periods[hh][None, :] + tau + overhead_slots                    # (L, N_all)
    # psi^{(l)} = Psi_i(Y)/Y
    cost = np.empty_like(Y, dtype=float)
    for l in range(L):
        psi_rows = sources.psi[ii]                                     # (N_all, y_max+1)
        Yc = np.clip(Y[l], 1, sc.psi_y_max)
        base = psi_rows[np.arange(len(ii)), Yc] / Yc
        slope = sources.psi[ii, -1] / sc.psi_y_max - sources.psi[ii, -2] / (sc.psi_y_max - 1)
        cost[l] = np.where(Y[l] > sc.psi_y_max, base + slope * (Y[l] - sc.psi_y_max), base)
    cost = cost.T                                                      # (N_all, L)
    worst = cost.max(1)
    admissible = vis & nominal_ok & (worst <= budget + 1e-12)
    forced = np.zeros(U, dtype=bool)
    # UEs with no admissible combination: keep their least-bad reachable combination (flagged)
    for i in range(U):
        sel = (ii == i)
        if not admissible[sel].any():
            cand = sel & vis & nominal_ok
            if not cand.any():
                cand = sel & vis          # unreachable even nominally: keep visible combos, cost already huge
            if not cand.any():
                cand = sel                # nothing visible at all (no BS, no SAT): keep all, will have cost from long Y
            idx = np.flatnonzero(cand)
            best = idx[np.argmin(worst[idx])]
            admissible[best] = True
            forced[i] = True
    keep = np.flatnonzero(admissible)
    bw_units = np.round(levels_mhz / so.bandwidth_resolution_mhz).astype(int)
    cap_mhz = np.concatenate([np.full(B, rc.bs_bandwidth_mhz), np.full(S, rc.sat_bandwidth_mhz)])
    cap_units = np.round(cap_mhz / so.bandwidth_resolution_mhz).astype(int)
    return RobustInstance(
        num_ues=U, num_bs=B, num_sat=S, scenarios=scenarios,
        var_ue=ii[keep], var_node=mm[keep], var_q=qq[keep], var_h=hh[keep],
        var_bw_units=bw_units[qq[keep]], var_bw_mhz=levels_mhz[qq[keep]], var_period=periods[hh[keep]],
        cost=cost[keep], cap_units=cap_units, cap_mhz=cap_mhz,
        domain_of_ue=topology.domain_of_ue.copy(), domain_of_bs=topology.domain_of_bs.copy(),
        forced_fallback=forced, nominal_rate=rates, visible=visible,
    )
