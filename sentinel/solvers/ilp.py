"""Exact solution of the robust problem P3 (epigraph ILP) with scipy's HiGHS backend.

This is the exact minimax reference the paper's TODO asked for: same variables, same objective
(min over x of max over scenarios of the UE-average AoII), same constraints D1-D3.
"""
from __future__ import annotations

import time
from typing import Optional

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix

from ..problem import RobustInstance


def solve_p3_exact(inst: RobustInstance, time_limit_s: float = 120.0, ue_subset: Optional[np.ndarray] = None,
                   cap_override: Optional[np.ndarray] = None):
    """Return dict(x, eta, scenario, status, time_s). ue_subset restricts to a domain (used for local checks)."""
    t0 = time.time()
    if ue_subset is None:
        vars_idx = np.arange(inst.num_vars)
        ues = np.arange(inst.num_ues)
    else:
        ues = np.asarray(ue_subset)
        vars_idx = np.flatnonzero(np.isin(inst.var_ue, ues))
    N = len(vars_idx)
    L = inst.L
    cap = inst.cap_units if cap_override is None else cap_override
    # variables: x (N binary), eta (continuous)
    c = np.zeros(N + 1); c[-1] = 1.0
    rows = []
    lo, hi = [], []
    A = lil_matrix((len(ues) + inst.num_nodes + L, N + 1))
    r = 0
    ue_of = inst.var_ue[vars_idx]
    node_of = inst.var_node[vars_idx]
    for i in ues:
        A[r, np.flatnonzero(ue_of == i)] = 1.0
        lo.append(1.0); hi.append(1.0); r += 1
    for m in range(inst.num_nodes):
        idx = np.flatnonzero(node_of == m)
        if len(idx):
            A[r, idx] = inst.var_bw_units[vars_idx][idx]
        lo.append(-np.inf); hi.append(float(cap[m])); r += 1
    for l in range(L):
        A[r, :N] = inst.cost[vars_idx, l] / inst.num_ues
        A[r, N] = -1.0
        lo.append(-np.inf); hi.append(0.0); r += 1
    cons = LinearConstraint(csr_matrix(A), np.array(lo), np.array(hi))
    integrality = np.concatenate([np.ones(N), [0.0]])
    bounds = Bounds(np.zeros(N + 1), np.concatenate([np.ones(N), [np.inf]]))
    res = milp(c, constraints=cons, integrality=integrality, bounds=bounds,
               options={"time_limit": time_limit_s, "disp": False})
    out = {"status": res.status, "time_s": time.time() - t0, "x": None, "eta": np.inf, "scenario": -1,
           "message": res.message}
    if res.x is not None and res.status in (0, 1, 3):
        x_full = np.zeros(inst.num_vars)
        x_full[vars_idx] = np.round(res.x[:N])
        out["x"] = x_full
        if ue_subset is None:
            out["eta"], out["scenario"] = inst.worst_case(x_full)
        else:
            out["eta"] = float(res.x[N])
    return out
