"""Whittle-index scheduling baseline for AoII (restless-bandit relaxation).

Each UE is one arm of a restless multi-armed bandit. The arm state is (x, e, a): true source state x, edge estimate e,
and the age a of the current mismatch (slots since the estimate was last correct), capped at A. The per-slot cost is
the simulator's AoII, a * |x - e|. "Pulling" the arm transmits an update that succeeds with probability q, after which
the estimate equals the new source state. The Whittle index W(x, e, a) is the smallest Lagrangian transmission price
at which idling is optimal in that state, computed numerically by relative value iteration of the average-cost
single-arm MDP on a grid of prices (the arm is treated as indexable; where the idle set is not monotone in the price,
the conservative value is used). The scheduler then, in every slot, ranks the UEs by index and admits them at their
best node while the node's shared bandwidth still delivers every admitted packet within the slot.

With equal bandwidth sharing and the sizes of this study, capacity rarely binds, so the Whittle scheduler coincides
with the state-aware AoII-threshold policy except in the ordering of simultaneous transmissions; it is included
because it is the standard reference policy of the AoII scheduling literature.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np

from .sources import birth_death_matrix

A_MAX = 60
CACHE = Path(__file__).resolve().parents[1] / "cache" / "whittle"
LAMBDAS = np.concatenate([[0.0], np.logspace(-2, 4, 85)])


@lru_cache(maxsize=512)
def whittle_table(n_states: int, p_stay_milli: int, q_milli: int, a_max: int = A_MAX) -> np.ndarray:
    """Index table W[x, e, a] for a birth-death source with p_stay = p_stay_milli/1000 and success prob q_milli/1000."""
    cache_file = CACHE / f"w_n{n_states}_p{p_stay_milli}_q{q_milli}_a{a_max}.npy"
    if cache_file.exists():
        return np.load(cache_file)
    p_stay = p_stay_milli / 1000.0
    q = q_milli / 1000.0
    n = n_states
    P = birth_death_matrix(n, p_stay)
    A = a_max
    S = n * n * (A + 1)
    sid = np.arange(S).reshape(n, n, A + 1)
    xs, es, as_ = np.meshgrid(np.arange(n), np.arange(n), np.arange(A + 1), indexing="ij")
    xs, es, as_ = xs.ravel(), es.ravel(), as_.ravel()
    xp = np.arange(n)[None, :]                                   # next source state candidates
    # idle: e' = e, a' = 0 if x' == e else min(a+1, A)
    a_idle = np.where(xp == es[:, None], 0, np.minimum(as_[:, None] + 1, A))
    nxt_idle = sid[xp, es[:, None], a_idle]                      # (S, n)
    c_idle = a_idle * np.abs(xp - es[:, None])
    # successful transmission: e' = x', a' = 0, cost 0
    nxt_succ = sid[xp, xp, 0]                                    # (1, n) broadcast
    nxt_succ = np.broadcast_to(nxt_succ, (S, n))
    Pr = P[xs]                                                   # (S, n) transition rows
    L = LAMBDAS
    V = np.zeros((len(L), S))
    ref = sid[0, 0, 0]
    for _ in range(3000):
        Q_idle = (Pr[None] * (c_idle[None] + V[:, nxt_idle])).sum(axis=2)         # (L, S)
        Q_succ = (Pr[None] * V[:, nxt_succ]).sum(axis=2)
        Q_tx = L[:, None] + q * Q_succ + (1.0 - q) * Q_idle
        V_new = np.minimum(Q_idle, Q_tx)
        V_new = V_new - V_new[:, ref:ref + 1]
        if np.abs(V_new - V).max() < 1e-7:
            V = V_new
            break
        V = V_new
    Q_idle = (Pr[None] * (c_idle[None] + V[:, nxt_idle])).sum(axis=2)
    Q_succ = (Pr[None] * V[:, nxt_succ]).sum(axis=2)
    Q_tx = L[:, None] + q * Q_succ + (1.0 - q) * Q_idle
    idle_opt = Q_idle <= Q_tx + 1e-9                             # (L, S)
    # conservative index: smallest price above which idling stays optimal for every larger price
    trailing = np.flip(np.cumprod(np.flip(idle_opt, axis=0), axis=0), axis=0).astype(bool)
    idx = np.where(trailing.any(axis=0), trailing.argmax(axis=0), len(L) - 1)
    W = L[idx]
    W = np.where(trailing.any(axis=0), W, L[-1] * 10).reshape(n, n, A + 1)
    try:
        CACHE.mkdir(parents=True, exist_ok=True)
        np.save(cache_file, W)
    except OSError:
        pass
    return W


def ue_index_tables(sources, q: float = 1.0) -> np.ndarray:
    """Stack of per-UE index tables, (U, n, n, A+1)."""
    tabs = [whittle_table(sources.n, int(5 * round(200 * p)), int(round(1000 * q))) for p in sources.p_stay]
    return np.stack(tabs)


def max_sharers(rate_fn, bw_full: float, need_bps: float, max_n: int) -> int:
    """Largest number of equal sharers of bw_full for which rate_fn(bw_full / n) still meets need_bps."""
    for n in range(max_n, 0, -1):
        if rate_fn(bw_full / n) >= need_bps:
            return n
    return 0
