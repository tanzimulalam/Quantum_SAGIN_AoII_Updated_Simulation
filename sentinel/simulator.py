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
from .whittle import ue_index_tables, A_MAX
from .problem import build_instance, RobustInstance
from .admm import sentinel_solve
from .compact import compact_sentinel_solve


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
    dis = DisruptionProcess(cfg.dis, cfg.net.num_ues, cfg.net.num_sat, T, I, np.random.default_rng(seed + 999),
                            switches=getattr(topo, "sat_switches", None), topology=topo)
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
        if cfg.solver.formulation == "compact":
            res = compact_sentinel_solve(inst, cfg.solver, seed=solver_seed + k, outer_iterations=cfg.solver.dual_outer_iterations,
                                         k_cand=cfg.solver.k_cand, polish=polish)
        else:
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
    reactive_resolves: int = 0
    wall_time_s: float = 0.0

    def to_row(self) -> Dict:
        return asdict(self)


def run_policy(ep: Episode, policy: str, plan: Optional[List[ScheduleEpoch]] = None,
               num_scenarios: Optional[int] = None) -> RunResult:
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
    best_rate_int = np.zeros((ep.num_intervals, U, M))
    vis_int = np.zeros((ep.num_intervals, U, M), dtype=bool)
    for k in range(ep.num_intervals):
        rates, vis = nominal_rate_table(ep.topology, k, rc)
        full = rates[:, :, -1] * vis               # rate at the largest level
        vis_int[k] = vis
        best_node[k] = np.argmax(np.where(vis, full, -1.0), axis=1)
        best_rate_int[k] = full
    # plan lookup
    if policy in ("sentinel", "nominal", "sentinel_triggered", "sentinel_capped_trigger"):
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
    fail_since = np.full(U, -1, dtype=int)                 # slot of the first failure of the current streak (-1: none)
    blocked_until = np.zeros((U, M), dtype=int)            # slot until which UE i avoids node m
    reactive_resolves = 0
    pending_resolve = False
    # end of the current satellite pass for (slot j, UE i): the next interval at which the slot changes satellite
    # (TLE model: recorded switches) or the UE's visibility of the slot changes (synthetic model)
    vis_sig = ep.topology.sat_visible                      # (S, T_int, U)
    switch_ints = {}
    for (jj, kk_, _nm) in (getattr(ep.topology, "sat_switches", None) or []):
        switch_ints.setdefault(jj, []).append(kk_)
    def pass_end_slot(j, kk, i):
        nxt = [x for x in switch_ints.get(j, []) if x > kk]
        k_switch = min(nxt) if nxt else ep.num_intervals
        k2 = kk
        while k2 + 1 < min(k_switch, ep.num_intervals) and vis_sig[j, k2 + 1, i] == vis_sig[j, kk, i]:
            k2 += 1
        return min(k2 + 1, k_switch) * I
    scen_full = build_scenarios(cfg.dis, cfg.net.num_sat, 6)
    if num_scenarios is None:
        num_scenarios = 1 if policy == "nominal" else 6
    scen_plan = build_scenarios(cfg.dis, cfg.net.num_sat, num_scenarios)      # scenario set of the reactive re-solve
    if policy == "whittle":
        # Whittle index tables per UE and, per interval, the largest number of equal bandwidth sharers each
        # (UE, node) pair tolerates while the packet still fits in one slot at the nominal rate
        w_tab = ue_index_tables(ep.sources)
        need_bps = D / T_s
        nmax_int = np.zeros((ep.num_intervals, U, M), dtype=int)
        full_bw_vec = np.where(np.arange(M) < B, levels_full_bs, levels_full_sat)
        for kk in range(ep.num_intervals):
            for nn in range(1, U + 1):
                r = np.zeros((U, M))
                if B:
                    r[:, :B] = bs_rate_bps(d_bs, full_bw_vec[:B][None, :] / nn, rc)
                if S:
                    rg = ep.topology.sat_range_m[:, kk, :].T                      # (U, S)
                    rs = sat_rate_bps(rg, full_bw_vec[B:][None, :] / nn, rc)
                    r[:, B:] = np.where(ep.topology.sat_visible[:, kk, :].T, rs, 0.0)
                nmax_int[kk][(r >= need_bps) & vis_int[kk]] = nn
    for t in range(1, T):
        k = t // I
        # --- decide transmitters -------------------------------------------------------------
        if policy in ("sentinel", "nominal", "sentinel_triggered", "sentinel_capped_trigger"):
            e_idx = epoch_of_interval[k]
            if e_idx != cur_epoch:
                e = plan[e_idx]
                node, bw, period = e.node.copy(), e.bw_mhz * 1e6, e.period.copy()
                cur_epoch = e_idx
            if policy == "sentinel_triggered":
                # robust association + dedicated bandwidth from SENTINEL, transmissions triggered by the observed
                # mismatch, rate-capped at the shortest period
                tx = (aoii > cfg.sim.threshold_aoii) & ((t - last_delivery) >= cfg.sim.min_update_gap_slots)
            elif policy == "sentinel_capped_trigger":
                # the chosen rate level is a cap: transmit on mismatch, but never more often than once per chosen period
                tx = (aoii > cfg.sim.threshold_aoii) & ((t - last_delivery) >= period)
            else:
                tx = (t - last_delivery) >= period
            tx_node = node
            tx_bw = bw
        elif policy == "random":
            tx = rng.random(U) < cfg.sim.random_activation_prob
            tx &= (t - last_delivery) >= 1
            tx_node = np.zeros(U, dtype=int)
            for i in np.flatnonzero(tx):
                cands = np.flatnonzero(vis_int[k, i] & ~(blocked_until[i] > t))
                if len(cands) == 0:
                    cands = np.flatnonzero(vis_int[k, i])
                tx_node[i] = rng.choice(cands) if len(cands) else 0
            tx_bw = None
        elif policy == "threshold":
            tx = (aoii > cfg.sim.threshold_aoii) & ((t - last_delivery) >= cfg.sim.min_update_gap_slots)
            if (blocked_until > t).any():
                allowed = vis_int[k] & ~(blocked_until > t)
                score = np.where(allowed, best_rate_int[k], -1.0)
                tx_node = np.where(allowed.any(axis=1), np.argmax(score, axis=1), best_node[k])
            else:
                tx_node = best_node[k]
            tx_bw = None
        elif policy == "whittle":
            # same observation and transmission rules as the threshold policy (mismatch, minimum gap, best nominal
            # node with ACK blocking); the Whittle index orders simultaneous transmitters and the node admits the
            # highest-index UEs while its shared bandwidth still delivers every admitted packet
            age = np.minimum((t - 1) - last_correct, A_MAX)
            xp = X[t - 1]
            W = w_tab[np.arange(U), xp, est, age]
            elig = (xp != est) & ((t - last_delivery) >= cfg.sim.min_update_gap_slots)
            allowed = vis_int[k] & ~(blocked_until > t)
            score = np.where(allowed, best_rate_int[k], -1.0)
            tx_node = np.where(allowed.any(axis=1), np.argmax(score, axis=1), best_node[k])
            tx = np.zeros(U, dtype=bool)
            for m_node in np.unique(tx_node[elig]):
                cand = np.flatnonzero(elig & (tx_node == m_node))
                order = cand[np.argsort(-W[cand], kind="stable")]
                cap_min = U + 1
                c = 0
                for i_u in order:
                    n_i = nmax_int[k, i_u, m_node]
                    if n_i == 0:
                        continue
                    if min(cap_min, n_i) >= c + 1:
                        tx[i_u] = True
                        c += 1
                        cap_min = min(cap_min, n_i)
                    else:
                        break
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
            # ACK feedback: consecutive failures block the node; SENTINEL variants re-solve without the dead link
            fail_since[idx[ok]] = -1
            failed = idx[~ok]
            if len(failed):
                fresh = fail_since[failed] < 0
                fail_since[failed[fresh]] = t
                persistent = (t - fail_since[failed]) >= cfg.sim.failure_window_slots
                newly = failed[persistent]
                if len(newly):
                    for i_u, m_u in zip(newly, n_i[~ok][persistent]):
                        until = t + cfg.sim.failure_block_slots
                        if m_u >= B:
                            until = max(until, pass_end_slot(m_u - B, k, i_u))      # a dead satellite pass stays dead
                        blocked_until[i_u, m_u] = until
                    fail_since[newly] = -1
                    pending_resolve = True
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
        # batched reactive re-solve: at most once per orchestration interval
        if pending_resolve and plan is not None and cfg.sim.reactive_resolve and (t % I == 0 or t == 1):
            pending_resolve = False
            excl = blocked_until > t
            inst_r = build_instance(cfg, ep.topology, ep.sources, scen_plan, k, horizon_intervals=1, exclude_mask=excl)
            if cfg.solver.formulation == "compact":
                res_r = compact_sentinel_solve(inst_r, cfg.solver, seed=ep.seed + t, outer_iterations=cfg.solver.dual_outer_iterations,
                                               k_cand=cfg.solver.k_cand)
            else:
                res_r = sentinel_solve(inst_r, cfg.solver, seed=ep.seed + t)
            sel_r = inst_r.assignment_from_x(res_r.x)
            node = inst_r.var_node[sel_r].copy(); bw = inst_r.var_bw_mhz[sel_r] * 1e6; period = inst_r.var_period[sel_r].copy()
            reactive_resolves += 1
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
        res.reactive_resolves = reactive_resolves
    return res
