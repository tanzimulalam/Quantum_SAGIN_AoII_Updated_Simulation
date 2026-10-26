"""Compact (slack-free) robust formulation: scenario-weight dualization of the minimax.

The epigraph formulation of Section V needs M_eta epigraph bits plus L x M_eta scenario-slack bits per domain,
which dominate the qubit count and make the landscape unsearchable. Here the minimax

    min_x max_l  c_l(x)        (c_l = per-scenario network-average AoII, linear in x)

is handled by its dual: for weights w on the simplex the inner problem  min_x sum_l w_l c_l(x)  is a plain linear
objective over the decision variables, and an outer exponentiated-gradient loop moves weight onto the scenarios
that are currently worst. Every inner solution is still certified exactly by max_l c_l(x), so nothing is lost on
the guarantee; what is gained is a domain QUBO with decision qubits plus a few capacity-slack bits only.

Candidate pruning keeps the k_cand lowest-worst-case admissible combinations per UE (configurable), which bounds
the number of decision qubits per UE independently of Q x H x M.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from .config import SolverConfig
from .problem import RobustInstance
from .solvers.greedy import greedy_assign, local_search


# ----------------------------------------------------------------------------------------------
# pruning
# ----------------------------------------------------------------------------------------------
def prune_candidates(inst: RobustInstance, k_cand: int) -> RobustInstance:
    """Keep the k_cand admissible combinations with the smallest worst-case cost per UE (ties: less bandwidth)."""
    if k_cand is None or k_cand <= 0:
        return inst
    worst = inst.cost.max(1)
    keep = []
    for i in range(inst.num_ues):
        idx = inst.vars_of_ue(i)
        order = sorted(idx, key=lambda v: (worst[v], inst.var_bw_units[v], inst.var_period[v]))
        # keep at least one combination per distinct node so the capacity coupling stays meaningful
        chosen = list(order[:k_cand])
        seen_nodes = {int(inst.var_node[v]) for v in chosen}
        for v in order[k_cand:]:
            if int(inst.var_node[v]) not in seen_nodes:
                chosen.append(v); seen_nodes.add(int(inst.var_node[v]))
        keep.extend(chosen)
    keep = np.array(sorted(keep), dtype=int)
    import copy
    out = copy.copy(inst)
    for name in ("var_ue", "var_node", "var_q", "var_h", "var_bw_units", "var_bw_mhz", "var_period"):
        setattr(out, name, getattr(inst, name)[keep])
    out.cost = inst.cost[keep]
    return out


# ----------------------------------------------------------------------------------------------
# compact domain QUBO
# ----------------------------------------------------------------------------------------------
@dataclass
class CompactDomainQubo:
    k: int
    Q: np.ndarray
    const: float
    n_x: int
    x_vars: np.ndarray            # instance variable indices of the decision qubits
    ue_list: np.ndarray
    groups: List[np.ndarray]      # per UE: positions (0..n_x-1) of its decision qubits
    own_nodes: np.ndarray
    shared_sats: np.ndarray
    bw_units: np.ndarray          # (n_x,)
    lin: np.ndarray               # (n_x,) weighted cost coefficients a_v = sum_l w_l psi_v / U
    lam_onehot: float
    lam_cap: float
    layout: Dict[str, Tuple[int, int]]
    z: Dict[int, float]
    u: Dict[int, float]
    rho: float
    node_of: np.ndarray           # (n_x,)

    @property
    def n(self) -> int:
        return self.Q.shape[0]

    def energy(self, w: np.ndarray) -> float:
        return float(w @ self.Q @ w + self.const)

    # objective of an assignment (one chosen position per UE) with slack bits implied
    def assignment_energy(self, sel: np.ndarray, inst: RobustInstance) -> float:
        a = float(self.lin[sel].sum())
        use = np.bincount(self.node_of[sel], weights=self.bw_units[sel], minlength=inst.num_nodes)
        pen = self.lam_cap * float(np.sum(np.maximum(use[self.own_nodes] - inst.cap_units[self.own_nodes], 0.0) ** 2)) if len(self.own_nodes) else 0.0
        gam = sum(0.5 * self.rho * (use[j] - self.z[j] + self.u[j]) ** 2 for j in self.shared_sats)
        return a + pen + gam

    def decode_x(self, w: np.ndarray) -> np.ndarray:
        return np.asarray(w[: self.n_x]).round().astype(float)

    def is_onehot(self, xk: np.ndarray) -> bool:
        return all(xk[g].sum() == 1 for g in self.groups)

    def local_feasible(self, xk: np.ndarray, inst: RobustInstance) -> bool:
        if not self.is_onehot(xk):
            return False
        use = np.bincount(self.node_of, weights=self.bw_units * xk, minlength=inst.num_nodes)
        return bool(np.all(use[self.own_nodes] <= inst.cap_units[self.own_nodes] + 1e-9))

    def sel_from_x(self, xk: np.ndarray) -> np.ndarray:
        return np.array([g[int(np.argmax(xk[g]))] for g in self.groups], dtype=int)

    def x_from_sel(self, sel: np.ndarray) -> np.ndarray:
        x = np.zeros(self.n_x); x[sel] = 1.0; return x


def _add_square(Q: np.ndarray, a: np.ndarray, c: float, lam: float) -> float:
    nz = np.flatnonzero(a); av = a[nz]
    Q[np.ix_(nz, nz)] += lam * np.outer(av, av)
    Q[nz, nz] += 2.0 * lam * c * av
    return lam * c * c


def build_compact_qubo(inst: RobustInstance, k: int, weights: np.ndarray, z: Dict[int, float], u: Dict[int, float],
                       rho: float, shared_sats: np.ndarray, onehot_penalty: bool = True) -> CompactDomainQubo:
    ue_list = np.flatnonzero(inst.domain_of_ue == k)
    x_vars = np.flatnonzero(np.isin(inst.var_ue, ue_list))
    n_x = len(x_vars)
    ue = inst.var_ue[x_vars]; node = inst.var_node[x_vars]
    bw = inst.var_bw_units[x_vars].astype(float)
    lin = (inst.cost[x_vars] @ weights) / inst.num_ues                       # a_v
    groups = [np.flatnonzero(ue == i) for i in ue_list if (ue == i).any()]
    own_bs = np.flatnonzero(inst.domain_of_bs == k)
    sat_nodes = np.arange(inst.num_bs, inst.num_bs + inst.num_sat)
    shared_set = set(int(j) for j in shared_sats)
    own_sats = np.array([j for j in sat_nodes if j not in shared_set and (node == j).any()], dtype=int)
    own_nodes = np.concatenate([own_bs, own_sats]).astype(int)
    # penalty weights: objective range over one-hot states
    a_max = float(sum(lin[g].max() for g in groups)); a_min = float(sum(lin[g].min() for g in groups))
    gam_range = 0.0
    for j in shared_sats:
        j = int(j)
        if not (node == j).any():
            continue
        bmax = sum(float(bw[(ue == i) & (node == j)].max()) if ((ue == i) & (node == j)).any() else 0.0 for i in ue_list)
        vals = [0.5 * rho * (b - z[j] + u[j]) ** 2 for b in (0.0, bmax)]
        gam_range += max(vals)
    lam = (a_max - a_min) + gam_range + 1e-3
    lam_cap = lam                       # residual >= 1 bandwidth unit
    lam_onehot = lam if onehot_penalty else 0.0
    # layout: decision bits, then capacity slack bits for own nodes
    layout = {"x": (0, n_x)}; pos = n_x
    cap_bits = {}
    for m in own_nodes:
        if not (node == m).any():
            continue
        cap_bits[int(m)] = int(np.ceil(np.log2(inst.cap_units[m] + 1)))
        layout[f"cap{m}"] = (pos, pos + cap_bits[int(m)]); pos += cap_bits[int(m)]
    n = pos
    Q = np.zeros((n, n)); const = 0.0
    Q[np.arange(n_x), np.arange(n_x)] += lin
    if onehot_penalty:
        for g in groups:
            a = np.zeros(n); a[g] = 1.0
            const += _add_square(Q, a, -1.0, lam_onehot)
    for m, bits in cap_bits.items():
        a = np.zeros(n); a[np.flatnonzero(node == m)] = bw[node == m]
        s0, _ = layout[f"cap{m}"]
        for b in range(bits):
            a[s0 + b] = 2.0 ** b
        const += _add_square(Q, a, -float(inst.cap_units[m]), lam_cap)
    for j in shared_sats:
        j = int(j)
        if not (node == j).any():
            continue
        a = np.zeros(n); a[np.flatnonzero(node == j)] = bw[node == j]
        const += _add_square(Q, a, -(z[j] - u[j]), 0.5 * rho)
    if not onehot_penalty:
        # on the one-hot subspace x_v x_v' = 0 for two candidates of the same UE, so their couplings carry no energy:
        # drop them (exact on every reachable state; removes a large share of the ZZ terms in the circuit)
        for g in groups:
            if len(g) > 1:
                gi = np.ix_(g, g)
                diag = np.diag(Q[gi]).copy()
                Q[gi] = 0.0
                Q[g, g] = diag
    dq = CompactDomainQubo(k=k, Q=Q, const=const, n_x=n_x, x_vars=x_vars, ue_list=ue_list, groups=groups,
                             own_nodes=own_nodes, shared_sats=np.asarray(shared_sats, dtype=int), bw_units=bw, lin=lin,
                             lam_onehot=lam_onehot, lam_cap=lam_cap, layout=layout, z=dict(z), u=dict(u), rho=rho, node_of=node)
    dq.weights = np.asarray(weights, dtype=float)
    return dq


def _weights_of(dq, inst):
    return getattr(dq, "weights", np.ones(inst.L) / inst.L)


# ----------------------------------------------------------------------------------------------
# classical inner solvers on the compact QUBO
# ----------------------------------------------------------------------------------------------
def greedy_sel(dq: CompactDomainQubo, inst: RobustInstance) -> np.ndarray:
    """Greedy one-hot assignment by weighted cost that respects own-node capacities where possible."""
    use = np.zeros(inst.num_nodes)
    sel = np.zeros(len(dq.groups), dtype=int)
    order = sorted(range(len(dq.groups)), key=lambda gi: -(dq.lin[dq.groups[gi]].max() - dq.lin[dq.groups[gi]].min()))
    for gi in order:
        g = dq.groups[gi]
        cands = sorted(g, key=lambda v: dq.lin[v])
        pick = None
        for v in cands:
            m = dq.node_of[v]
            if m in dq.own_nodes and use[m] + dq.bw_units[v] > inst.cap_units[m]:
                continue
            pick = v; break
        if pick is None:
            pick = cands[0]
        sel[gi] = pick; use[dq.node_of[pick]] += dq.bw_units[pick]
    return sel


def anneal_compact(dq: CompactDomainQubo, inst: RobustInstance, sweeps: int = 400, restarts: int = 2,
                   rng: Optional[np.random.Generator] = None, init: Optional[np.ndarray] = None):
    """One-hot-preserving annealing on the compact objective (classical analogue of the XY-mixer search)."""
    rng = np.random.default_rng() if rng is None else rng
    G = len(dq.groups)
    spread = np.mean([dq.lin[g].max() - dq.lin[g].min() for g in dq.groups]) if G else 1.0
    scale = max(float(spread), 1e-3)
    temps = scale * np.geomspace(2.0, 0.01, sweeps)
    best_sel, best_e = None, np.inf
    for r in range(restarts):
        sel = (init.copy() if (init is not None and r == 0) else np.array([g[rng.integers(len(g))] for g in dq.groups]))
        e = dq.assignment_energy(sel, inst)
        for T in temps:
            for gi in rng.permutation(G):
                g = dq.groups[gi]
                if len(g) == 1:
                    continue
                v = g[rng.integers(len(g))]
                if v == sel[gi]:
                    continue
                old = sel[gi]; sel[gi] = v
                e2 = dq.assignment_energy(sel, inst)
                if e2 <= e or rng.random() < np.exp(-(e2 - e) / T):
                    e = e2
                    if e < best_e:
                        best_e, best_sel = e, sel.copy()
                else:
                    sel[gi] = old
        if e < best_e:
            best_e, best_sel = e, sel.copy()
    return best_sel, float(best_e)


# ----------------------------------------------------------------------------------------------
# ADMM over domains for fixed scenario weights
# ----------------------------------------------------------------------------------------------
@dataclass
class CompactResult:
    x: np.ndarray
    eta: float
    scenario: int
    feasible: bool
    outer_iterations: int
    admm_rounds_total: int
    solver_used: str
    qubits_per_domain: List[int]
    time_s: float
    weights_trace: List[np.ndarray] = field(default_factory=list)
    eta_trace: List[float] = field(default_factory=list)
    qaoa_info: List[dict] = field(default_factory=list)


def _shared_sats(inst: RobustInstance) -> np.ndarray:
    sat_nodes = np.arange(inst.num_bs, inst.num_bs + inst.num_sat)
    return np.array([j for j in sat_nodes if len(set(inst.domain_of_ue[inst.var_ue[inst.var_node == j]].tolist())) >= 2], dtype=int)


def _solve_domain(dq: CompactDomainQubo, inst: RobustInstance, cfg: SolverConfig, rng, seed: int, qaoa_params=None):
    """Return (sel, method, info). Uses QAOA when configured and the QUBO is small enough, else annealing."""
    choice = cfg.solver
    if choice == "auto":
        choice = "qaoa_xy" if dq.n <= cfg.max_qaoa_qubits else "sa_xy"
    info = {}
    if choice == "qaoa_xy":
        from .solvers.qaoa_xy import qaoa_xy
        # the XY mixer keeps every UE group one-hot, so the one-hot penalty is a constant on the reachable subspace:
        # rebuild the QUBO without it (far fewer ZZ couplings, shallower circuits)
        dq = build_compact_qubo(inst, dq.k, _weights_of(dq, inst), dq.z, dq.u, dq.rho, dq.shared_sats, onehot_penalty=False)
        g_init = greedy_sel(dq, inst)
        res = qaoa_xy(dq, inst, depth=cfg.qaoa_depth, shots=cfg.qaoa_shots, maxiter=cfg.qaoa_maxiter, seed=seed,
                      init_params=qaoa_params, warm_start_sel=g_init)
        info = {"n_qubits": res["n_qubits"], "params": res["params"], "energies": res["energies"], "time_s": res["time_s"],
                "feasible_sample_fraction": res["feasible_sample_fraction"], "best_sample_energy": res["best_energy"],
                "greedy_energy": dq.assignment_energy(g_init, inst), "method": res["method"],
                "two_qubit_gates": res["two_qubit_gates"], "circuit_depth_transpiled": res["circuit_depth_transpiled"],
                "onehot_sample_fraction": res["onehot_sample_fraction"]}
        sel = res["best_sel"]
        # classical fallback if every sample violated own-node capacity
        if sel is None:
            sel = g_init
        return sel, "qaoa_xy", info
    if choice == "exact":
        from .solvers.exact import brute_force_qubo
        w, _ = brute_force_qubo(dq.Q)
        xk = dq.decode_x(w)
        if dq.is_onehot(xk):
            return dq.sel_from_x(xk), "exact", info
        return greedy_sel(dq, inst), "exact", info
    sel, e = anneal_compact(dq, inst, sweeps=cfg.sa_sweeps, restarts=cfg.sa_restarts, rng=rng, init=greedy_sel(dq, inst))
    return sel, "sa_xy", info


def admm_compact(inst: RobustInstance, weights: np.ndarray, cfg: SolverConfig, rng, seed: int, qaoa_params=None,
                 max_rounds: Optional[int] = None):
    K = int(inst.domain_of_ue.max()) + 1
    shared = _shared_sats(inst)
    Kj = {int(j): sorted(set(inst.domain_of_ue[inst.var_ue[inst.var_node == j]].tolist())) for j in shared}
    z = {int(j): {k: inst.cap_units[j] / len(Kj[int(j)]) for k in Kj[int(j)]} for j in shared}
    u = {int(j): {k: 0.0 for k in Kj[int(j)]} for j in shared}
    # rho on the scale of the objective: one bandwidth unit of deviation at a shared SAT should cost about the
    # typical per-UE cost difference, not dominate the whole network objective
    a_w = (inst.cost @ weights) / inst.num_ues
    spread = float(np.mean([a_w[inst.vars_of_ue(i)].max() - a_w[inst.vars_of_ue(i)].min()
                            for i in range(inst.num_ues) if len(inst.vars_of_ue(i))]))
    rho = cfg.admm_rho * max(spread, 1e-6)
    best_x, best_val = None, np.inf
    methods = set(); qubits = []; infos = []; params = qaoa_params
    rounds = max_rounds or cfg.admm_max_rounds
    r = 0
    for r in range(rounds):
        x = np.zeros(inst.num_vars); usage = {int(j): {} for j in shared}; qubits = []
        warm = (r == 0)          # round 0: uncoupled domain solves (rho = 0) initialise the ADMM targets
        for k in range(K):
            if not (inst.domain_of_ue == k).any():
                continue
            zk = {int(j): z[int(j)].get(k, 0.0) for j in shared}; uk = {int(j): u[int(j)].get(k, 0.0) for j in shared}
            dq = build_compact_qubo(inst, k, weights, zk, uk, 0.0 if warm else rho, shared)
            qubits.append(dq.n)
            sel, method, info = _solve_domain(dq, inst, cfg, rng, seed * 100 + r * 10 + k, qaoa_params=params)
            methods.add(method)
            if info:
                infos.append(dict(info, domain=k, round=r)); params = info.get("params", params)
            xk = dq.x_from_sel(sel)
            x[dq.x_vars] = xk
            for j in shared:
                usage[int(j)][k] = float((dq.bw_units * xk * (dq.node_of == int(j))).sum())
        p_res = d_res = 0.0
        for j in shared:
            j = int(j)
            a = {k: usage[j].get(k, 0.0) + u[j][k] for k in Kj[j]}
            excess = max(0.0, sum(a.values()) - inst.cap_units[j])
            for k in Kj[j]:
                z_new = a[k] - excess / len(Kj[j])
                d_res += (z_new - z[j][k]) ** 2; z[j][k] = z_new
                u[j][k] += usage[j].get(k, 0.0) - z_new
                p_res += (usage[j].get(k, 0.0) - z_new) ** 2
        p_res, d_res = np.sqrt(p_res), rho * np.sqrt(d_res)
        # incumbent on the weighted objective, only among network-feasible schedules
        if inst.is_feasible(x):
            val = float((inst.cost @ weights) @ x / inst.num_ues)
            if val < best_val:
                best_x, best_val = x.copy(), val
        if warm:
            continue             # start coupling from the next round
        if p_res > 10 * d_res: rho *= 2.0
        elif d_res > 10 * p_res: rho /= 2.0
        if len(shared) == 0 or (p_res <= cfg.admm_tol and best_x is not None):
            break
    if best_x is None:
        # feasibility repair on the weighted objective (shared-satellite overload): move cheapest-to-move UEs
        best_x = _repair_weighted(inst, x, weights)
    used = methods.pop() if len(methods) == 1 else "mixed"
    return best_x, used, qubits, infos, params, r + 1


def _repair_weighted(inst: RobustInstance, x: np.ndarray, weights: np.ndarray) -> np.ndarray:
    x = x.copy()
    a = (inst.cost @ weights) / inst.num_ues
    for i in range(inst.num_ues):
        idx = inst.vars_of_ue(i)
        if x[idx].sum() != 1:
            x[idx] = 0.0; x[idx[np.argmin(a[idx])]] = 1.0
    for _ in range(10 * inst.num_ues):
        use = inst.node_usage_units(x)
        over = np.flatnonzero(use > inst.cap_units + 1e-9)
        if len(over) == 0:
            break
        m = over[0]
        best, best_delta = None, np.inf
        for v in np.flatnonzero((inst.var_node == m) & (x > 0.5)):
            for v2 in inst.vars_of_ue(inst.var_ue[v]):
                m2 = inst.var_node[v2]
                if v2 == v or (m2 == m and inst.var_bw_units[v2] >= inst.var_bw_units[v]):
                    continue
                if m2 != m and use[m2] + inst.var_bw_units[v2] > inst.cap_units[m2]:
                    continue
                delta = a[v2] - a[v]
                if delta < best_delta:
                    best, best_delta = (v, v2), delta
        if best is None:
            break
        x[best[0]] = 0.0; x[best[1]] = 1.0
    return x


# ----------------------------------------------------------------------------------------------
# outer loop: exponentiated gradient on scenario weights
# ----------------------------------------------------------------------------------------------
def compact_sentinel_solve(inst: RobustInstance, cfg: SolverConfig, seed: int = 0, outer_iterations: int = 8,
                           step: float = 2.0, k_cand: Optional[int] = None, polish: bool = False) -> CompactResult:
    t0 = time.time()
    rng = np.random.default_rng(seed)
    work = prune_candidates(inst, k_cand) if k_cand else inst
    L = inst.L
    w = np.ones(L) / L
    best_x, best_eta, best_l = None, np.inf, -1
    w_trace, eta_trace, infos = [], [], []
    methods = set(); qubits = []; params = None; rounds_total = 0
    for it in range(outer_iterations):
        x, used, qubits, info, params, rounds = admm_compact(work, w, cfg, rng, seed + it, qaoa_params=params)
        rounds_total += rounds; methods.add(used); infos.extend(info)
        c = work.network_cost(x)                               # exact per-scenario costs (certificate)
        eta, l = float(c.max()), int(np.argmax(c))
        feasible = work.is_feasible(x)
        if feasible and eta < best_eta - 1e-12:
            best_x, best_eta, best_l = x.copy(), eta, l
        w_trace.append(w.copy()); eta_trace.append(eta)
        # exponentiated gradient toward the worst scenarios
        w = w * np.exp(step * c / max(eta, 1e-9)); w /= w.sum()
    if best_x is None:
        best_x = _repair_weighted(work, x, w); best_eta, best_l = work.worst_case(best_x)
    if polish and work.is_feasible(best_x):
        best_x = local_search(work, best_x, max_passes=5); best_eta, best_l = work.worst_case(best_x)
    # map back to the unpruned instance's variable indexing
    x_full = np.zeros(inst.num_vars)
    if work is not inst:
        key = {(int(inst.var_ue[v]), int(inst.var_node[v]), int(inst.var_q[v]), int(inst.var_h[v])): v for v in range(inst.num_vars)}
        for v in np.flatnonzero(best_x > 0.5):
            x_full[key[(int(work.var_ue[v]), int(work.var_node[v]), int(work.var_q[v]), int(work.var_h[v]))]] = 1.0
    else:
        x_full = best_x
    used = methods.pop() if len(methods) == 1 else "mixed"
    return CompactResult(x=x_full, eta=best_eta, scenario=best_l, feasible=inst.is_feasible(x_full),
                         outer_iterations=outer_iterations, admm_rounds_total=rounds_total, solver_used=used,
                         qubits_per_domain=qubits, time_s=time.time() - t0, weights_trace=w_trace, eta_trace=eta_trace,
                         qaoa_info=infos)
