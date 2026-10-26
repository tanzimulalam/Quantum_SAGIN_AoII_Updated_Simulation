"""Brute-force QUBO minimizer for small n (ground truth for the QUBO itself)."""
from __future__ import annotations

import numpy as np


def brute_force_qubo(Q: np.ndarray, max_n: int = 22):
    n = Q.shape[0]
    if n > max_n:
        raise ValueError(f"brute force limited to {max_n} variables, got {n}")
    best_w, best_e = None, np.inf
    # enumerate in chunks to bound memory
    total = 1 << n
    chunk = 1 << min(n, 16)
    for start in range(0, total, chunk):
        idx = np.arange(start, min(start + chunk, total), dtype=np.int64)
        W = ((idx[:, None] >> np.arange(n)) & 1).astype(float)          # (chunk, n)
        E = np.einsum("ki,ij,kj->k", W, Q, W)
        k = int(np.argmin(E))
        if E[k] < best_e:
            best_e, best_w = float(E[k]), W[k].copy()
    return best_w, best_e
