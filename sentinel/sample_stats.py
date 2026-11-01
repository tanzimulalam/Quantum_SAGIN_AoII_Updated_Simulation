"""Per-shot statistics of a domain's samples against the exact optimum of its one-hot subspace.

Enumerates every one-hot assignment of the domain (product of the candidate-group sizes; at most a few million for
hardware-sized domains), evaluates the assignment energy with slack bits implied, and returns the optimal set, the
uniform-feasible-sampling baseline, and, for a dictionary of measured counts, the probability that a shot is an optimal
assignment and the mean approximation ratio E_opt / E over feasible shots.
"""
from __future__ import annotations

from math import prod
from typing import Dict, Optional

import numpy as np


def enumerate_onehot(dq, inst, max_states: int = 4_000_000) -> Optional[dict]:
    groups = dq.groups
    sizes = [len(g) for g in groups]
    N = prod(sizes)
    if N > max_states:
        return None
    U = len(groups)
    idx = np.indices(sizes).reshape(U, -1).T                                   # (N, U) position within each group
    sel = np.stack([groups[i][idx[:, i]] for i in range(U)], axis=1)           # (N, U) decision-qubit positions
    lin = dq.lin[sel].sum(axis=1)
    use = np.zeros((N, inst.num_nodes))
    rows = np.arange(N)
    for u in range(U):
        np.add.at(use, (rows, dq.node_of[sel[:, u]]), dq.bw_units[sel[:, u]])
    own = np.asarray(dq.own_nodes, dtype=int)
    feas = np.ones(N, dtype=bool)
    pen = np.zeros(N)
    if len(own):
        over = np.maximum(use[:, own] - inst.cap_units[own][None, :], 0.0)
        feas = np.all(over <= 1e-9, axis=1)
        pen = dq.lam_cap * (over ** 2).sum(axis=1)
    gam = np.zeros(N)
    for j in dq.shared_sats:
        gam += 0.5 * dq.rho * (use[:, j] - dq.z[j] + dq.u[j]) ** 2
    E = lin + pen + gam
    if not feas.any():
        return {"n_states": int(N), "n_feasible": 0}
    e_opt = float(E[feas].min())
    optimal = feas & (np.abs(E - e_opt) <= 1e-9 * max(1.0, abs(e_opt)))
    return {"n_states": int(N), "n_feasible": int(feas.sum()), "n_optimal": int(optimal.sum()), "e_opt": e_opt,
            "p_uniform_optimal": float(optimal.sum() / feas.sum()),
            "uniform_approx_ratio": float(np.mean(e_opt / E[feas])),
            "spread_rel": float((E[feas].max() - e_opt) / max(abs(e_opt), 1e-12)),
            "e_feasible_max": float(E[feas].max()),
            "sel": sel, "E": E, "feas": feas, "optimal": optimal}


def shot_statistics(dq, inst, counts: Dict[str, int], enum: Optional[dict]) -> dict:
    """P(shot is an optimal assignment), P(optimal | feasible), mean approximation ratio over feasible shots."""
    n = dq.n
    total = sum(counts.values())
    if enum is None or enum.get("n_feasible", 0) == 0:
        return {"p_optimal_shot": float("nan"), "p_optimal_given_feasible": float("nan"), "approx_ratio_feasible": float("nan")}
    e_opt = enum["e_opt"]
    opt_shots = 0
    feas_shots = 0
    ratio_sum = 0.0
    for key, c in counts.items():
        w = np.array([int(key[n - 1 - a]) for a in range(n)], dtype=float)
        xk = w[: dq.n_x]
        if not dq.is_onehot(xk):
            continue
        if not dq.local_feasible(xk, inst):
            continue
        e = dq.assignment_energy(dq.sel_from_x(xk), inst)
        feas_shots += c
        ratio_sum += c * (e_opt / e if e > 0 else 1.0)
        if abs(e - e_opt) <= 1e-9 * max(1.0, abs(e_opt)):
            opt_shots += c
    return {"p_optimal_shot": opt_shots / total, "p_optimal_given_feasible": (opt_shots / feas_shots) if feas_shots else float("nan"),
            "approx_ratio_feasible": (ratio_sum / feas_shots) if feas_shots else float("nan"), "feasible_shots": feas_shots, "total_shots": total}
