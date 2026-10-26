"""Classical heuristics for the robust assignment: Greedy and Greedy + local search."""
from __future__ import annotations

import numpy as np

from ..problem import RobustInstance


def greedy_assign(inst: RobustInstance) -> np.ndarray:
    """Most-constrained UE first; pick the admissible combination with the smallest worst-case cost that fits."""
    worst = inst.cost.max(1)
    order = sorted(range(inst.num_ues), key=lambda i: -worst[inst.vars_of_ue(i)].min() if len(inst.vars_of_ue(i)) else 0)
    use = np.zeros(inst.num_nodes)
    x = np.zeros(inst.num_vars)
    for i in order:
        idx = inst.vars_of_ue(i)
        cand = sorted(idx, key=lambda v: (worst[v], inst.var_bw_units[v]))
        chosen = None
        for v in cand:
            m = inst.var_node[v]
            if use[m] + inst.var_bw_units[v] <= inst.cap_units[m]:
                chosen = v
                break
        if chosen is None:
            chosen = cand[0]            # infeasible fallback (capacity violated); LS/repair may fix it
        x[chosen] = 1.0
        use[inst.var_node[chosen]] += inst.var_bw_units[chosen]
    return x


def local_search(inst: RobustInstance, x: np.ndarray, max_passes: int = 50) -> np.ndarray:
    """First-improvement single-UE reassignment on the exact minimax objective (feasibility-preserving)."""
    x = x.copy()
    best, _ = inst.worst_case(x)
    feasible = inst.is_feasible(x)
    for _ in range(max_passes):
        improved = False
        for i in range(inst.num_ues):
            idx = inst.vars_of_ue(i)
            cur = idx[np.argmax(x[idx])]
            for v in idx:
                if v == cur:
                    continue
                trial = x.copy()
                trial[cur] = 0.0; trial[v] = 1.0
                f = inst.is_feasible(trial)
                val, _ = inst.worst_case(trial)
                if (f and not feasible) or (f == feasible and val < best - 1e-12):
                    x, best, feasible, cur = trial, val, f, v
                    improved = True
        if not improved:
            break
    return x
