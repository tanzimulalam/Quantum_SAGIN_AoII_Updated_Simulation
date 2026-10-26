"""Simulated annealing for a dense QUBO (classical stand-in for QAOA on domains too large to simulate)."""
from __future__ import annotations

import numpy as np


def anneal_qubo(Q: np.ndarray, sweeps: int = 400, restarts: int = 4, t_start: float = 2.0, t_end: float = 0.01,
                rng: np.random.Generator | None = None, init: np.ndarray | None = None):
    """Return (best_w, best_energy_without_const). Single-flip Metropolis with geometric cooling."""
    rng = np.random.default_rng() if rng is None else rng
    n = Q.shape[0]
    scale = float(np.median(np.abs(np.diag(Q))) + 1e-9)
    temps = scale * np.geomspace(t_start, t_end, sweeps)
    best_w, best_e = None, np.inf
    for r in range(restarts):
        w = (rng.random(n) < 0.5).astype(float) if (init is None or r > 0) else init.astype(float).copy()
        h = Q @ w
        e = float(w @ h)
        for T in temps:
            order = rng.permutation(n)
            logu = np.log(rng.random(n))
            for idx in range(n):
                i = order[idx]
                delta = 1.0 - 2.0 * w[i]
                dE = 2.0 * delta * h[i] + Q[i, i]
                if dE <= 0.0 or logu[idx] < -dE / T:
                    w[i] += delta
                    h += delta * Q[:, i]
                    e += dE
                    if e < best_e:
                        best_e, best_w = e, w.copy()
    return best_w, best_e


def anneal_assignment(dq, inst, z, u, rho, sweeps: int = 2000, restarts: int = 2, t_start: float = 2.0,
                      t_end: float = 0.01, rng: np.random.Generator | None = None):
    """Constraint-preserving annealing on the same domain objective (classical analogue of an XY-mixer QAOA).

    The state is one selected combination per UE (one-hot by construction); slack bits are implied (set optimally),
    so the energy is  eta_k(x) + Gamma_k(x) + lambda * sum_m max(0, b_m(x) - B_m)^2  over own nodes.
    Returns (w, energy) with w a full binary vector whose x-part is the assignment (slack bits zero).
    """
    rng = np.random.default_rng() if rng is None else rng
    ue = inst.var_ue[dq.x_vars]
    node = inst.var_node[dq.x_vars]
    groups = [np.flatnonzero(ue == i) for i in dq.ue_list]
    groups = [g for g in groups if len(g)]
    cost = dq.cost_units.astype(float)
    bw = dq.bw_units.astype(float)
    lam = float(dq.lambdas[1])
    own = np.asarray(dq.own_nodes, dtype=int)
    cap = inst.cap_units.astype(float)
    shared = [int(j) for j in dq.shared_sats]
    zz = np.array([z[j] for j in shared]); uu = np.array([u[j] for j in shared])

    def energy(sel):
        c = cost[sel].sum(0).max() if len(sel) else 0.0
        use = np.bincount(node[sel], weights=bw[sel], minlength=inst.num_nodes)
        pen = lam * float(np.sum(np.maximum(use[own] - cap[own], 0.0) ** 2)) if len(own) else 0.0
        gam = float(np.sum(0.5 * rho * (use[shared] - zz + uu) ** 2)) if shared else 0.0
        return c + pen + gam

    spread = np.mean([cost[g].max(1).max() - cost[g].max(1).min() for g in groups]) if groups else 1.0
    scale = max(float(spread), 1.0)
    temps = scale * np.geomspace(t_start, t_end, sweeps)
    best_sel, best_e = None, np.inf
    for _ in range(restarts):
        sel = np.array([g[rng.integers(len(g))] for g in groups])
        e = energy(sel)
        for T in temps:
            for gi in rng.permutation(len(groups)):
                g = groups[gi]
                if len(g) == 1:
                    continue
                v = g[rng.integers(len(g))]
                if v == sel[gi]:
                    continue
                old = sel[gi]
                sel[gi] = v
                e2 = energy(sel)
                if e2 <= e or rng.random() < np.exp(-(e2 - e) / T):
                    e = e2
                    if e < best_e:
                        best_e, best_sel = e, sel.copy()
                else:
                    sel[gi] = old
        if e < best_e:
            best_e, best_sel = e, sel.copy()
    w = np.zeros(dq.n)
    if best_sel is not None:
        w[best_sel] = 1.0
    return w, float(best_e)
