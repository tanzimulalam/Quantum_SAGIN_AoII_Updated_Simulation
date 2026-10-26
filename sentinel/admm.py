"""SENTINEL: distributed robust QAOA with ADMM coordination (paper Algorithm 1).

Local solver per domain: QAOA on Aer when the domain QUBO has at most max_qaoa_qubits qubits,
otherwise simulated annealing on the same QUBO (reported as such). The returned schedule always
carries its exact worst-case AoII over the scenario set (the certificate of Section V-C).
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

from .config import SolverConfig
from .problem import RobustInstance
from .qubo import build_domain_qubo, DomainQubo
from .solvers.sa import anneal_qubo, anneal_assignment
from .solvers.exact import brute_force_qubo
from .solvers.greedy import local_search


@dataclass
class SentinelResult:
    x: np.ndarray                       # network 0/1 assignment over instance variables
    eta: float                          # certified worst-case network-average AoII
    scenario: int                       # worst-case scenario index
    feasible: bool
    rounds: int
    solver_used: str                    # "qaoa" | "sa" | "exact" | "mixed"
    qubits_per_domain: List[int]
    time_s: float
    repaired: bool = False
    primal_residuals: List[float] = field(default_factory=list)
    dual_residuals: List[float] = field(default_factory=list)
    incumbent_trace: List[float] = field(default_factory=list)
    qaoa_traces: List[list] = field(default_factory=list)
    local_gap_to_exact: List[float] = field(default_factory=list)   # (local QUBO energy - brute-force optimum) when checkable
    local_feasible_fraction: float = np.nan                          # share of local solves whose best sample was feasible without repair
    onehot_fraction_raw: float = np.nan                              # mean share of UEs with exactly one selected combo in the raw best sample


def _shared_sats(inst: RobustInstance) -> np.ndarray:
    sat_nodes = np.arange(inst.num_bs, inst.num_bs + inst.num_sat)
    shared = []
    for j in sat_nodes:
        doms = set(inst.domain_of_ue[inst.var_ue[inst.var_node == j]].tolist())
        if len(doms) >= 2:
            shared.append(j)
    return np.array(shared, dtype=int)


def _solve_local(dq: DomainQubo, cfg: SolverConfig, rng: np.random.Generator, seed: int, check_exact: bool,
                 inst: RobustInstance = None, zk=None, uk=None, rho: float = 1.0):
    n = dq.n
    choice = cfg.solver
    if choice == "auto":
        choice = "qaoa" if n <= cfg.max_qaoa_qubits else "sa_xy"
    trace = None
    if choice == "sa_xy":
        w, e = anneal_assignment(dq, inst, zk, uk, rho, sweeps=cfg.sa_sweeps, restarts=cfg.sa_restarts,
                                 t_start=cfg.sa_t_start, t_end=cfg.sa_t_end, rng=rng)
        samples = w[None, :]
    elif choice == "qaoa":
        from .solvers.qaoa import qaoa_qubo
        res = qaoa_qubo(dq.Q, depth=cfg.qaoa_depth, shots=cfg.qaoa_shots, maxiter=cfg.qaoa_maxiter, seed=seed)
        w, e, trace = res.best_w, res.best_energy, res.energies
        samples = res.samples
    elif choice == "exact":
        w, e = brute_force_qubo(dq.Q)
        samples = w[None, :]
    else:
        w, e = anneal_qubo(dq.Q, sweeps=cfg.sa_sweeps, restarts=cfg.sa_restarts, t_start=cfg.sa_t_start,
                           t_end=cfg.sa_t_end, rng=rng)
        samples = w[None, :]
    gap = np.nan
    if check_exact and n <= 20 and choice not in ("exact", "sa_xy"):
        _, e_opt = brute_force_qubo(dq.Q)
        gap = float(e - e_opt)
    return choice, w, samples, trace, gap


def sentinel_solve(inst: RobustInstance, cfg: SolverConfig, seed: int = 0, check_exact: bool = False,
                   polish: bool = True) -> SentinelResult:
    t0 = time.time()
    rng = np.random.default_rng(seed)
    K = int(inst.domain_of_ue.max()) + 1 if inst.num_ues else 1
    shared = _shared_sats(inst)
    # ADMM state per shared SAT and domain
    Kj = {int(j): sorted(set(inst.domain_of_ue[inst.var_ue[inst.var_node == j]].tolist())) for j in shared}
    z = {int(j): {k: inst.cap_units[j] / len(Kj[int(j)]) for k in Kj[int(j)]} for j in shared}
    u = {int(j): {k: 0.0 for k in Kj[int(j)]} for j in shared}
    worst_cost = inst.cost.max(1) / inst.num_ues
    spread = float(np.mean([worst_cost[inst.vars_of_ue(i)].max() - worst_cost[inst.vars_of_ue(i)].min()
                            for i in range(inst.num_ues) if len(inst.vars_of_ue(i))]))
    rho = cfg.admm_rho * max(spread, 1e-6) / max(cfg.eta_resolution, 1e-9)   # in the integer cost units of the QUBO
    best_x, best_eta, best_l = None, np.inf, -1
    primal, dual, inc = [], [], []
    solvers_used = set()
    qubits = []
    traces, gaps = [], []
    last_xk: Dict[int, np.ndarray] = {}
    r = 0
    n_local, n_local_feasible = 0, 0
    onehot_acc = []
    for r in range(cfg.admm_max_rounds):
        x = np.zeros(inst.num_vars)
        usage = {int(j): {} for j in shared}
        qubits = []
        for k in range(K):
            if not (inst.domain_of_ue == k).any():
                continue
            zk = {int(j): z[int(j)].get(k, 0.0) for j in shared}
            uk = {int(j): u[int(j)].get(k, 0.0) for j in shared}
            dq = build_domain_qubo(inst, k, zk, uk, 0.0 if r == 0 else rho, cfg.eta_resolution, shared)
            qubits.append(dq.n)
            choice, w, samples, trace, gap = _solve_local(dq, cfg, rng, seed * 1000 + r * 10 + k, check_exact,
                                                          inst=inst, zk=zk, uk=uk, rho=rho)
            solvers_used.add(choice)
            if trace is not None:
                traces.append(trace)
            if not np.isnan(gap):
                gaps.append(gap)
            # best locally feasible sample; else repair
            xk = None
            best_val = np.inf
            for s in samples[: min(len(samples), 64)]:
                cand = dq.decode(s)
                if dq.local_feasible(cand, inst):
                    val = dq.local_objective(cand, zk, uk, rho, inst)
                    if val < best_val:
                        xk, best_val = cand, val
            n_local += 1
            raw = dq.decode(samples[0])
            cnt = np.bincount(inst.var_ue[dq.x_vars], weights=raw, minlength=inst.num_ues)[dq.ue_list]
            onehot_acc.append(float((cnt == 1).mean()) if len(cnt) else np.nan)
            if xk is None:
                xk = dq.repair(dq.decode(samples[0]), zk, uk, rho, inst)
            else:
                n_local_feasible += 1
            last_xk[k] = xk
            x[dq.x_vars] = xk
            node = inst.var_node[dq.x_vars]
            for j in shared:
                usage[int(j)][k] = float((dq.bw_units * xk * (node == int(j))).sum())
        # consensus update (sharing ADMM, eq. z_update / u_update)
        p_res, d_res = 0.0, 0.0
        for j in shared:
            j = int(j)
            a = {k: usage[j].get(k, 0.0) + u[j][k] for k in Kj[j]}
            excess = max(0.0, sum(a.values()) - inst.cap_units[j])
            for k in Kj[j]:
                z_new = a[k] - excess / len(Kj[j])
                d_res += (z_new - z[j][k]) ** 2
                z[j][k] = z_new
                u[j][k] = u[j][k] + usage[j].get(k, 0.0) - z_new
                p_res += (usage[j].get(k, 0.0) - z_new) ** 2
        p_res, d_res = np.sqrt(p_res), rho * np.sqrt(d_res)
        primal.append(p_res); dual.append(d_res)
        # incumbent update with exact certificate
        if inst.is_feasible(x):
            eta, l = inst.worst_case(x)
            if eta < best_eta - 1e-12:
                best_x, best_eta, best_l = x.copy(), eta, l
        inc.append(best_eta)
        if r == 0:
            continue             # round 0 was the uncoupled warm start of the ADMM targets
        # residual balancing
        if p_res > 10 * d_res:
            rho *= 2.0
        elif d_res > 10 * p_res:
            rho /= 2.0
        if len(shared) == 0 or (p_res <= cfg.admm_tol and best_x is not None):
            break
    repaired = False
    if best_x is None:
        # greedy repair of the last assembled schedule (Algorithm 1, final step)
        x = np.zeros(inst.num_vars)
        for k, xk in last_xk.items():
            dq_vars = np.flatnonzero(np.isin(inst.var_ue, np.flatnonzero(inst.domain_of_ue == k)))
            x[dq_vars] = xk
        x = _network_repair(inst, x)
        if not inst.is_feasible(x):
            x = local_search(inst, x, max_passes=20)       # local search also accepts feasibility-restoring moves
        best_x = x
        best_eta, best_l = inst.worst_case(x)
        repaired = True
    if polish and inst.is_feasible(best_x):
        # cheap classical polish on the exact objective (does not change certification semantics)
        best_x = local_search(inst, best_x, max_passes=5)
        best_eta, best_l = inst.worst_case(best_x)
    used = solvers_used.pop() if len(solvers_used) == 1 else "mixed"
    return SentinelResult(x=best_x, eta=best_eta, scenario=best_l, feasible=inst.is_feasible(best_x), rounds=r + 1,
                          solver_used=used, qubits_per_domain=qubits, time_s=time.time() - t0, repaired=repaired,
                          primal_residuals=primal, dual_residuals=dual, incumbent_trace=inc, qaoa_traces=traces,
                          local_gap_to_exact=gaps, local_feasible_fraction=(n_local_feasible / n_local if n_local else np.nan),
                          onehot_fraction_raw=float(np.nanmean(onehot_acc)) if onehot_acc else np.nan)


def _network_repair(inst: RobustInstance, x: np.ndarray) -> np.ndarray:
    """Move UEs off overloaded nodes to the admissible combination with the smallest worst-case cost increase."""
    x = x.copy()
    # enforce one-hot
    for i in range(inst.num_ues):
        idx = inst.vars_of_ue(i)
        if x[idx].sum() != 1:
            x[idx] = 0.0
            x[idx[np.argmin(inst.cost[idx].max(1))]] = 1.0
    for _ in range(5 * inst.num_ues + 5):
        use = inst.node_usage_units(x)
        over = np.flatnonzero(use > inst.cap_units + 1e-9)
        if len(over) == 0:
            break
        m = over[0]
        best_trial, best_val = None, np.inf
        for v in np.flatnonzero((inst.var_node == m) & (x > 0.5)):
            i = inst.var_ue[v]
            for v2 in inst.vars_of_ue(i):
                if v2 == v:
                    continue
                m2 = inst.var_node[v2]
                if m2 == m and inst.var_bw_units[v2] >= inst.var_bw_units[v]:
                    continue
                if m2 != m and use[m2] + inst.var_bw_units[v2] > inst.cap_units[m2]:
                    continue
                trial = x.copy(); trial[v] = 0.0; trial[v2] = 1.0
                val, _ = inst.worst_case(trial)
                if val < best_val:
                    best_trial, best_val = trial, val
        if best_trial is None:
            break
        x = best_trial
    return x
