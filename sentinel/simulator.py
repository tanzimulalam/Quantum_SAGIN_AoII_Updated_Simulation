"""Slot-level SAGIN simulator: Markov sources, AoII tracking, realized channel with disruption, and policies.

Policies
  random      : each slot each UE transmits w.p. p over a uniformly chosen visible node; equal bandwidth share
  threshold   : UE observes its own AoII and transmits when it exceeds a threshold (rate-capped); best nominal node
  sentinel    : robust schedule (m, beta_q, period) from the SENTINEL solver, re-solved on visibility changes
  nominal     : same solver with the nominal scenario only (L = 1), i.e. the non-robust counterpart
All policies for a given seed share the same topology, source trajectories, disruption realization and fading
(common random numbers).
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

import numpy as np

from .config import FullConfig, C_LIGHT
from .geometry import Topology, build_topology
from .channel import bs_rate_bps, sat_rate_bps, nominal_rate_table
from .sources import SourceSet
from .scenarios import build_scenarios, DisruptionProcess
from .problem import build_instance, RobustInstance
from .admm import sentinel_solve


@dataclass
class Episode:
    """Everything shared across policies for one seed."""
    cfg: FullConfig
    seed: int
    topology: Topology
    sources: SourceSet
    X: np.ndarray                 # (T, U) source states
    disruption: DisruptionProcess
    fading_db: np.ndarray         # (T, U)
    num_slots: int
    num_intervals: int


def make_episode(cfg: FullConfig, seed: int) -> Episode:
    T = cfg.sim.duration_slots
    I = cfg.sim.orchestration_interval_slots
    n_int = int(np.ceil(T / I))
    topo = build_topology(cfg.net, seed, n_int, I * cfg.src.slot_ms * 1e-3)
    sources = SourceSet(cfg.net.num_ues, cfg.src, seed)
    rng = np.random.default_rng(seed + 777)
    X = sources.simulate(T, rng)
    dis = DisruptionProcess(cfg.dis, cfg.net.num_ues, cfg.net.num_sat, T, I, np.random.default_rng(seed + 999))
    fading = np.random.default_rng(seed + 4242).normal(0.0, cfg.radio.fading_std_db, size=(T, cfg.net.num_ues)).astype(np.float32)
    return Episode(cfg=cfg, seed=seed, topology=topo, sources=sources, X=X, disruption=dis, fading_db=fading,
                   num_slots=T, num_intervals=n_int)


# ----------------------------------------------------------------------------------------------
# SENTINEL schedule plan
# ----------------------------------------------------------------------------------------------
@dataclass
class ScheduleEpoch:
    start_interval: int
    end_interval: int             # exclusive
    node: np.ndarray              # (U,) node index
    bw_mhz: np.ndarray            # (U,)
    period: np.ndarray            # (U,) slots
    eta_certified: float          # worst case over the full scenario set
    eta_solver: float             # worst case over the scenario set the solver saw
    scenario: int
    solver: str
    qubits: List[int]
    time_s: float
    forced: int
    feasible: bool


def _visibility_signature(topo: Topology, interval: int) -> bytes:
    return np.packbits(topo.sat_visible[:, interval, :].ravel()).tobytes()


def plan_schedule(ep: Episode, num_scenarios: int, solver_seed: int = 0, check_exact: bool = False,
                  polish: bool = False) -> List[ScheduleEpoch]:
    cfg = ep.cfg
    full_scen = build_scenarios(cfg.dis, cfg.net.num_sat, 6)
    scen = build_scenarios(cfg.dis, cfg.net.num_sat, num_scenarios)
    epochs: List[ScheduleEpoch] = []
    k = 0
    while k < ep.num_intervals:
        sig = _visibility_signature(ep.topology, k)
        k_end = k + 1
        while k_end < ep.num_intervals and k_end - k < cfg.sim.resolve_every_intervals and \
                _visibility_signature(ep.topology, k_end) == sig:
            k_end += 1
        inst = build_instance(cfg, ep.topology, ep.sources, scen, k, horizon_intervals=k_end - k)
        res = sentinel_solve(inst, cfg.solver, seed=solver_seed + k, check_exact=check_exact, polish=polish)
        sel = inst.assignment_from_x(res.x)
        # certificate on the full scenario set (so the nominal solver's schedule is judged robustly too)
        inst_full = build_instance(cfg, ep.topology, ep.sources, full_scen, k, horizon_intervals=k_end - k, budget=np.inf)
        eta_full = _certify_on(inst_full, inst, sel)
        epochs.append(ScheduleEpoch(
            start_interval=k, end_interval=k_end,
            node=inst.var_node[sel].copy(), bw_mhz=inst.var_bw_mhz[sel].copy(), period=inst.var_period[sel].copy(),
            eta_certified=eta_full, eta_solver=res.eta, scenario=res.scenario, solver=res.solver_used,
            qubits=list(res.qubits_per_domain), time_s=res.time_s, forced=int(inst.forced_fallback.sum()),
            feasible=res.feasible))
        k = k_end
    return epochs


def _certify_on(inst_full: RobustInstance, inst: RobustInstance, sel: np.ndarray) -> float:
    """Exact worst case of the chosen (m,q,h) per UE over inst_full's scenarios (combination may be inadmissible there)."""
    U = inst.num_ues
    worst = np.zeros(inst_full.L)
    key = {(int(inst_full.var_ue[v]), int(inst_full.var_node[v]), int(inst_full.var_q[v]), int(inst_full.var_h[v])): v
           for v in range(inst_full.num_vars)}
    for i in range(U):
        v = sel[i]
        kk = (i, int(inst.var_node[v]), int(inst.var_q[v]), int(inst.var_h[v]))
        if kk in key:
            worst += inst_full.cost[key[kk]]
        else:
            # not admissible under the full set: recompute its cost from scratch (same formula)
            worst += _cost_of_combination(inst_full, i, *kk[1:])
    return float(worst.max() / U)


def _cost_of_combination(inst_full: RobustInstance, i: int, m: int, q: int, h: int) -> np.ndarray:
    # fall back: find any variable of UE i at node m / level q / period h in the full instance's cost table is
    # impossible (it was pruned); approximate with the worst admissible of that UE (conservative upper bound)
    idx = inst_full.vars_of_ue(i)
    if len(idx) == 0:
        return np.zeros(inst_full.L)
    return inst_full.cost[idx].max(0)


# ----------------------------------------------------------------------------------------------
# Time-domain run
# ----------------------------------------------------------------------------------------------
@dataclass
class RunResult:
    policy: str
    seed: int
    num_ues: int
    num_bs: int
    num_sat: int
    disruption: bool
    average_aoii: float
    peak_aoii: float
    delivery_ratio: float
    informative_ratio: float
    sum_rate_mbps: float
    latency_ms: float
    bs_latency_ms: float
    sat_latency_ms: float
    sat_delivery_share: float
    sat_scheduling_share: float
    attempts: int
    deliveries: int
    budget_violation_fraction: float      # fraction of UEs whose realized time-average AoII exceeds the budget
    certified_eta_mean: float = np.nan    # SENTINEL only: time-weighted mean of certified worst-case AoII
    certificate_holds: float = np.nan     # SENTINEL only: fraction of epochs with realized avg AoII <= certified
    solver: str = ""
    qubits_max: int = 0
    solve_time_s: float = 0.0
    epochs: int = 0
    forced_fallback_ues: int = 0
    wall_time_s: float = 0.0

    def to_row(self) -> Dict:
        return asdict(self)


def run_policy(ep: Episode, policy: str, plan: Optional[List[ScheduleEpoch]] = None) -> RunResult:
    t_wall = time.time()
    cfg = ep.cfg
    U, B, S = ep.topology.num_ues, ep.topology.num_bs, ep.topology.num_sat
    M = B + S
    T, I = ep.num_slots, cfg.sim.orchestration_interval_slots
    T_s = cfg.src.slot_ms * 1e-3
    D = cfg.src.packet_bits
    rc = cfg.radio
    rng = np.random.default_rng(ep.seed + 31337)
    X = ep.X
    d_bs = ep.topology.ue_bs_distance_m() if B else np.zeros((U, 0))
    # per-interval best nominal node for the threshold policy and visible-node lists for random
    best_node = np.zeros((ep.num_intervals, U), dtype=int)
    vis_int = np.zeros((ep.num_intervals, U, M), dtype=bool)
    for k in range(ep.num_intervals):
        rates, vis = nominal_rate_table(ep.topology, k, rc)
        full = rates[:, :, -1] * vis               # rate at the largest level
        vis_int[k] = vis
        best_node[k] = np.argmax(np.where(vis, full, -1.0), axis=1)
    # plan lookup
    if policy in ("sentinel", "nominal", "sentinel_triggered"):
        assert plan is not None
        epoch_of_interval = np.zeros(ep.num_intervals, dtype=int)
        for e_idx, e in enumerate(plan):
            epoch_of_interval[e.start_interval:e.end_interval] = e_idx
    # state
    est = X[0].copy()                      # initial estimate = true state (delivery at t = 0)
    last_correct = np.zeros(U, dtype=int)
    last_delivery = np.zeros(U, dtype=int)
    aoii = np.zeros(U)
    aoii_sum = np.zeros(U)
    aoii_peak = 0.0
    attempts = 0; deliveries = 0; informative = 0
    bits = 0.0
    lat_sum = 0.0; lat_bs = 0.0; lat_sat = 0.0; n_bs = 0; n_sat = 0; sat_sched = 0
    # per-epoch realized AoII for the certificate check
    epoch_aoii_sum = np.zeros(len(plan) if plan else 1)
    epoch_slots = np.zeros(len(plan) if plan else 1)
    levels_full_bs = rc.bs_bandwidth_mhz * 1e6
    levels_full_sat = rc.sat_bandwidth_mhz * 1e6
    cap_bs = cfg.sim.bs_compute_gcycles_s * 1e9
    cap_sat = cfg.sim.sat_compute_gcycles_s * 1e9
    node = np.zeros(U, dtype=int); bw = np.zeros(U); period = np.zeros(U, dtype=int)
    cur_epoch = -1
    for t in range(1, T):
        k = t // I
        # --- decide transmitters -------------------------------------------------------------
        if policy in ("sentinel", "nominal", "sentinel_triggered"):
            e_idx = epoch_of_interval[k]
            if e_idx != cur_epoch:
                e = plan[e_idx]
                node, bw, period = e.node, e.bw_mhz * 1e6, e.period
                cur_epoch = e_idx
            if policy == "sentinel_triggered":
                # robust association + dedicated bandwidth from SENTINEL, but transmissions are triggered by the
                # observed mismatch (as the paper's conclusion proposes), rate-capped at the shortest period
                tx = (aoii > cfg.sim.threshold_aoii) & ((t - last_delivery) >= cfg.sim.min_update_gap_slots)
            else:
                tx = (t - last_delivery) >= period
            tx_node = node
            tx_bw = bw
        elif policy == "random":
            tx = rng.random(U) < cfg.sim.random_activation_prob
            tx &= (t - last_delivery) >= 1
            tx_node = np.zeros(U, dtype=int)
            for i in np.flatnonzero(tx):
                cands = np.flatnonzero(vis_int[k, i])
                tx_node[i] = rng.choice(cands) if len(cands) else 0
            tx_bw = None
        elif policy == "threshold":
            tx = (aoii > cfg.sim.threshold_aoii) & ((t - last_delivery) >= cfg.sim.min_update_gap_slots)
            tx_node = best_node[k]
            tx_bw = None
        else:
            raise ValueError(policy)
        idx = np.flatnonzero(tx)
        if len(idx):
            if tx_bw is None:
                # equal share of the node's bandwidth among this slot's transmitters
                counts = np.bincount(tx_node[idx], minlength=M)
                full_bw = np.where(np.arange(M) < B, levels_full_bs, levels_full_sat)
                share = full_bw / np.maximum(counts, 1)
                bw_i = share[tx_node[idx]]
            else:
                bw_i = tx_bw[idx]
            n_i = tx_node[idx]
            rate = np.zeros(len(idx))
            dist = np.zeros(len(idx))
            is_bs = n_i < B
            if is_bs.any():
                dd = d_bs[idx[is_bs], n_i[is_bs]]
                rate[is_bs] = bs_rate_bps(dd, bw_i[is_bs], rc, fading_db=ep.fading_db[t, idx[is_bs]])
                dist[is_bs] = dd
            if (~is_bs).any():
                j = n_i[~is_bs] - B
                ii = idx[~is_bs]
                rg = ep.topology.sat_range_m[j, k, ii]
                vis = ep.topology.sat_visible[j, k, ii]
                loss = ep.disruption.loss_db[t, j, ii]
                r = sat_rate_bps(rg, bw_i[~is_bs], rc, extra_loss_db=loss, fading_db=ep.fading_db[t, ii])
                rate[~is_bs] = np.where(vis, r, 0.0)
                dist[~is_bs] = np.where(np.isfinite(rg), rg, 0.0)
                sat_sched += int((~is_bs).sum())
            ok = rate * T_s >= D
            attempts += len(idx)
            if ok.any():
                good = idx[ok]
                deliveries += len(good)
                informative += int((X[t, good] != est[good]).sum())
                est[good] = X[t, good]
                last_delivery[good] = t
                bits += D * len(good)
                # latency: transmission + propagation + edge processing (shared compute per node this slot)
                gn = n_i[ok]
                served = np.bincount(gn, minlength=M)
                comp = np.where(gn < B, cap_bs, cap_sat) / served[gn]
                lat = D / rate[ok] + dist[ok] / C_LIGHT + D * cfg.sim.cycles_per_bit / comp
                lat_sum += lat.sum()
                bsm = gn < B
                lat_bs += lat[bsm].sum(); n_bs += int(bsm.sum())
                lat_sat += lat[~bsm].sum(); n_sat += int((~bsm).sum())
        # --- AoII update --------------------------------------------------------------------
        correct = X[t] == est
        last_correct[correct] = t
        aoii = np.where(correct, 0.0, (t - last_correct) * np.abs(X[t] - est))
        aoii_sum += aoii
        m = aoii.max()
        if m > aoii_peak:
            aoii_peak = m
        if plan is not None:
            epoch_aoii_sum[epoch_of_interval[k]] += aoii.mean()
            epoch_slots[epoch_of_interval[k]] += 1
    avg_per_ue = aoii_sum / (T - 1)
    res = RunResult(
        policy=policy, seed=ep.seed, num_ues=U, num_bs=B, num_sat=S, disruption=cfg.dis.enabled,
        average_aoii=float(avg_per_ue.mean()), peak_aoii=float(aoii_peak),
        delivery_ratio=deliveries / attempts if attempts else 0.0,
        informative_ratio=informative / deliveries if deliveries else 0.0,
        sum_rate_mbps=bits / ((T - 1) * T_s) / 1e6,
        latency_ms=1e3 * lat_sum / deliveries if deliveries else np.nan,
        bs_latency_ms=1e3 * lat_bs / n_bs if n_bs else np.nan,
        sat_latency_ms=1e3 * lat_sat / n_sat if n_sat else np.nan,
        sat_delivery_share=n_sat / deliveries if deliveries else 0.0,
        sat_scheduling_share=sat_sched / attempts if attempts else 0.0,
        attempts=attempts, deliveries=deliveries,
        budget_violation_fraction=float((avg_per_ue > cfg.src.aoii_budget).mean()),
        wall_time_s=time.time() - t_wall,
    )
    if plan is not None:
        w = np.array([e.end_interval - e.start_interval for e in plan], dtype=float)
        cert = np.array([e.eta_certified for e in plan])
        realized = epoch_aoii_sum / np.maximum(epoch_slots, 1)
        res.certified_eta_mean = float((cert * w).sum() / w.sum())
        res.certificate_holds = float((realized <= cert + 1e-9).mean())
        res.solver = plan[0].solver
        res.qubits_max = int(max(max(e.qubits) if e.qubits else 0 for e in plan))
        res.solve_time_s = float(sum(e.time_s for e in plan))
        res.epochs = len(plan)
        res.forced_fallback_ues = int(max(e.forced for e in plan))
    return res
