"""Domain-level QUBO of P3^{(k)} (paper Section V-A) and its Ising form (Section V-B).

All quantities are integer-scaled: costs in units of Delta_eta (rounded up, so eta_k stays an upper
bound), bandwidth in units of Delta_beta. With that choice every penalized constraint has an integer
residual and binary slacks can represent the gap exactly (Proposition 1).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from .problem import RobustInstance


@dataclass
class DomainQubo:
    k: int
    Q: np.ndarray                 # (n, n) symmetric
    const: float
    n_x: int                      # decision variables first
    x_vars: np.ndarray            # (n_x,) indices into instance variables
    ue_list: np.ndarray           # UEs of the domain
    own_nodes: np.ndarray         # nodes whose capacity is enforced locally
    shared_sats: np.ndarray       # node indices of shared satellites
    eta_bits: int
    delta_eta: float
    cost_units: np.ndarray        # (n_x, L) integer costs (already /|U| and rounded up)
    bw_units: np.ndarray          # (n_x,)
    lambdas: Tuple[float, float, float, float]
    layout: Dict[str, Tuple[int, int]]   # name -> (start, stop) in the binary vector

    @property
    def n(self) -> int:
        return self.Q.shape[0]

    def energy(self, w: np.ndarray) -> float:
        return float(w @ self.Q @ w + self.const)

    def ising(self):
        """h_a = -1/2 sum_a' Q_aa', J_aa' = 1/2 Q_aa' (a<a'), plus constant, for w = (1 - z)/2."""
        Q = self.Q
        h = -0.5 * Q.sum(1)
        J = 0.5 * np.triu(Q, 1)
        const = self.const + 0.25 * Q.sum() + 0.25 * np.trace(Q)
        return h, J, const

    # --- decoding -------------------------------------------------------------------------------
    def decode(self, w: np.ndarray) -> np.ndarray:
        """Return 0/1 vector over the domain's decision variables."""
        return np.asarray(w[: self.n_x]).round().astype(float)

    def local_feasible(self, xk: np.ndarray, inst: RobustInstance) -> bool:
        ue = inst.var_ue[self.x_vars]
        counts = np.bincount(ue, weights=xk, minlength=inst.num_ues)[self.ue_list]
        if np.any(counts != 1):
            return False
        node = inst.var_node[self.x_vars]
        use = np.bincount(node, weights=self.bw_units * xk, minlength=inst.num_nodes)
        return bool(np.all(use[self.own_nodes] <= inst.cap_units[self.own_nodes] + 1e-9))

    def local_objective(self, xk: np.ndarray, z: Dict[int, float], u: Dict[int, float], rho: float,
                        inst: RobustInstance) -> float:
        """eta_k + Gamma_k, in cost units (what F reduces to on the feasible set with optimal slacks)."""
        c = (self.cost_units * xk[:, None]).sum(0).max()
        node = inst.var_node[self.x_vars]
        gam = 0.0
        for j in self.shared_sats:
            b = float((self.bw_units * xk * (node == j)).sum())
            gam += 0.5 * rho * (b - z[j] + u[j]) ** 2
        return float(c + gam)

    def repair(self, xk: np.ndarray, z: Dict[int, float], u: Dict[int, float], rho: float,
               inst: RobustInstance) -> np.ndarray:
        """Greedy repair of a decoded sample: enforce one-hot per UE, then own-node capacities."""
        xk = xk.copy()
        ue = inst.var_ue[self.x_vars]
        node = inst.var_node[self.x_vars]
        for i in self.ue_list:
            idx = np.flatnonzero(ue == i)
            if xk[idx].sum() != 1:
                best, best_val = None, np.inf
                for v in idx:
                    trial = xk.copy()
                    trial[idx] = 0.0
                    trial[v] = 1.0
                    val = self.local_objective(trial, z, u, rho, inst)
                    if val < best_val:
                        best, best_val = v, val
                xk[idx] = 0.0
                xk[best] = 1.0
        # capacity repair on own nodes: move the UE whose move costs least
        for _ in range(10 * len(self.ue_list) + 1):
            use = np.bincount(node, weights=self.bw_units * xk, minlength=inst.num_nodes)
            over = [m for m in self.own_nodes if use[m] > inst.cap_units[m] + 1e-9]
            if not over:
                break
            m = over[0]
            cands = np.flatnonzero((node == m) & (xk > 0.5))
            best, best_val = None, np.inf
            for v in cands:
                i = ue[v]
                for v2 in np.flatnonzero(ue == i):
                    if v2 == v:
                        continue
                    trial = xk.copy()
                    trial[v] = 0.0
                    trial[v2] = 1.0
                    use2 = np.bincount(node, weights=self.bw_units * trial, minlength=inst.num_nodes)
                    if use2[m] >= use[m] or np.any(use2[self.own_nodes] > inst.cap_units[self.own_nodes] + 1e-9):
                        if use2[m] >= use[m]:
                            continue
                    val = self.local_objective(trial, z, u, rho, inst)
                    if val < best_val:
                        best, best_val = trial, val
            if best is None:
                break
            xk = best
        return xk


def _add_square(Q: np.ndarray, a: np.ndarray, c: float, lam: float) -> float:
    """Add lam*(a.w + c)^2 to Q (w binary). Returns added constant."""
    nz = np.flatnonzero(a)
    av = a[nz]
    # quadratic: lam * a_i a_j for i != j (both symmetric halves), lam*a_i^2 + 2 lam c a_i on diagonal
    Q[np.ix_(nz, nz)] += lam * np.outer(av, av)
    Q[nz, nz] += 2.0 * lam * c * av       # diagonal already got lam*a_i^2 from the outer product
    return lam * c * c


def build_domain_qubo(inst: RobustInstance, k: int, z: Dict[int, float], u: Dict[int, float], rho: float,
                      delta_eta: float, shared_sats: np.ndarray, eta_bits_cap: int = 10) -> DomainQubo:
    ue_list = np.flatnonzero(inst.domain_of_ue == k)
    x_vars = np.flatnonzero(np.isin(inst.var_ue, ue_list))
    n_x = len(x_vars)
    L = inst.L
    # integer costs: ceil(psi / (|U| Delta_eta))
    cost_units = np.ceil(inst.cost[x_vars] / inst.num_ues / delta_eta - 1e-9).astype(int)
    bw_units = inst.var_bw_units[x_vars].astype(int)
    node = inst.var_node[x_vars]
    ue = inst.var_ue[x_vars]
    # own nodes: BSs of this domain and SATs that are visible only to this domain
    own_bs = np.flatnonzero(inst.domain_of_bs == k)
    sat_nodes = np.arange(inst.num_bs, inst.num_bs + inst.num_sat)
    own_sats = np.array([j for j in sat_nodes if j not in set(shared_sats.tolist()) and (node == j).any()], dtype=int)
    own_nodes = np.concatenate([own_bs, own_sats]).astype(int)
    # epigraph range: eta_k <= sum over UEs of their max admissible cost (tight), in units
    eta_max_units = 0
    for i in ue_list:
        idx = np.flatnonzero(ue == i)
        eta_max_units += int(cost_units[idx].max(1).max()) if len(idx) else 0
    eta_max_units = max(eta_max_units, 1)
    M_eta = min(int(np.ceil(np.log2(eta_max_units + 1))), eta_bits_cap)
    eta_max_units = 2 ** M_eta - 1
    # slack widths
    cap_bits = {int(m): int(np.ceil(np.log2(inst.cap_units[m] + 1))) for m in own_nodes}
    scen_bits = M_eta
    # layout
    layout = {}
    pos = 0
    layout["x"] = (0, n_x); pos = n_x
    layout["eta"] = (pos, pos + M_eta); pos += M_eta
    for m in own_nodes:
        layout[f"cap{m}"] = (pos, pos + cap_bits[int(m)]); pos += cap_bits[int(m)]
    for l in range(L):
        layout[f"scen{l}"] = (pos, pos + scen_bits); pos += scen_bits
    n = pos
    Q = np.zeros((n, n))
    const = 0.0
    # Gamma range for penalty weights (Prop. 1)
    # Proposition 1 needs lambda > eta_max + Gamma(w*) - Gamma_min for a FEASIBLE w*, so Gamma_max may be taken over
    # feasible assignments (each UE selects one combination): b_j <= sum_i max_q beta, not over the whole hypercube.
    gam_max, gam_min = 0.0, 0.0
    for j in shared_sats:
        if not (node == j).any():
            continue
        bmax = 0.0
        for i in ue_list:
            sel = (ue == i) & (node == j)
            bmax += float(bw_units[sel].max()) if sel.any() else 0.0
        vals = [0.5 * rho * (b - z[j] + u[j]) ** 2 for b in (0.0, bmax)]
        gam_max += max(vals)
        gam_min += 0.0 if (0.0 <= z[j] - u[j] <= bmax) else min(vals)
    lam = eta_max_units + gam_max - gam_min + 1.0          # delta_l = 1 in integer units
    lam1 = lam2 = lam3 = lam4 = lam
    # F_epi
    e0, e1 = layout["eta"]
    for b in range(M_eta):
        Q[e0 + b, e0 + b] += 2.0 ** b
    # F_assoc: lam1 * (sum_x - 1)^2 per UE
    for i in ue_list:
        a = np.zeros(n); a[np.flatnonzero(ue == i)] = 1.0
        const += _add_square(Q, a, -1.0, lam1)
    # F_cap: lam * (b_m(x) + nu_m - B_m)^2
    for m in own_nodes:
        a = np.zeros(n)
        a[np.flatnonzero(node == m)] = bw_units[node == m]
        s0, s1 = layout[f"cap{m}"]
        for b in range(s1 - s0):
            a[s0 + b] = 2.0 ** b
        const += _add_square(Q, a, -float(inst.cap_units[m]), lam2)
    # F_scen: lam4 * (c_l(x) + nu_l - eta_k)^2
    for l in range(L):
        a = np.zeros(n)
        a[:n_x] = cost_units[:, l]
        s0, s1 = layout[f"scen{l}"]
        for b in range(s1 - s0):
            a[s0 + b] = 2.0 ** b
        for b in range(M_eta):
            a[e0 + b] = -(2.0 ** b)
        const += _add_square(Q, a, 0.0, lam4)
    # Gamma: rho/2 * (b_j(x) - z_jk + u_jk)^2 for shared SATs
    for j in shared_sats:
        if not (node == j).any():
            continue
        a = np.zeros(n)
        a[np.flatnonzero(node == j)] = bw_units[node == j]
        const += _add_square(Q, a, -(z[j] - u[j]), 0.5 * rho)
    return DomainQubo(k=k, Q=Q, const=const, n_x=n_x, x_vars=x_vars, ue_list=ue_list, own_nodes=own_nodes,
                      shared_sats=np.asarray(shared_sats, dtype=int), eta_bits=M_eta, delta_eta=delta_eta,
                      cost_units=cost_units, bw_units=bw_units, lambdas=(lam1, lam2, lam3, lam4), layout=layout)
