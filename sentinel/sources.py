"""Markov sources and the renewal-interval AoII decomposition (paper Section III-B, III-D).

Psi_i(Y) = sum_{xhat} pi(xhat) sum_{s=1}^{Y-1} sum_{a=1}^{s} a [P^{s-a}]_{xhat,xhat} [Ptilde_xhat^a f_xhat]_{xhat}
The time-average AoII of a UE whose deliveries are Y slots apart is Psi(Y)/Y.
"""
from __future__ import annotations

from typing import List

import numpy as np

from .config import SourceConfig


def birth_death_matrix(n: int, p_stay: float) -> np.ndarray:
    P = np.zeros((n, n))
    for i in range(n):
        P[i, i] = p_stay
        nb = [j for j in (i - 1, i + 1) if 0 <= j < n]
        for j in nb:
            P[i, j] = (1.0 - p_stay) / len(nb)
    return P


def stationary_distribution(P: np.ndarray) -> np.ndarray:
    n = P.shape[0]
    A = np.vstack([P.T - np.eye(n), np.ones((1, n))])
    b = np.zeros(n + 1)
    b[-1] = 1.0
    pi, *_ = np.linalg.lstsq(A, b, rcond=None)
    pi = np.clip(pi, 0, None)
    return pi / pi.sum()


def distortion_matrix(n: int) -> np.ndarray:
    idx = np.arange(n)
    return np.abs(idx[:, None] - idx[None, :]).astype(float)


def psi_table(P: np.ndarray, f: np.ndarray, y_max: int) -> np.ndarray:
    """Return Psi[Y] for Y = 0..y_max (Psi[0] = Psi[1] = 0)."""
    n = P.shape[0]
    pi = stationary_distribution(P)
    # powers of P: diag entries d[s] = [P^s]_{xx}
    Ppow = np.empty((y_max + 1, n, n))
    Ppow[0] = np.eye(n)
    for s in range(1, y_max + 1):
        Ppow[s] = Ppow[s - 1] @ P
    psi = np.zeros(y_max + 1)
    for xh in range(n):
        d = Ppow[:, xh, xh]                                   # (y_max+1,)
        Pt = P.copy()
        Pt[:, xh] = 0.0                                       # taboo matrix: never (re)enter xhat
        fvec = f[:, xh]                                       # f(y, xhat)
        g = np.zeros(y_max + 1)                               # g[a] = [Pt^a f]_{xhat}
        v = fvec.copy()
        for a in range(1, y_max + 1):
            v = Pt @ v
            g[a] = v[xh]
        a_g = np.arange(y_max + 1) * g
        # E[s] = sum_{a=1}^{s} a g[a] d[s-a]  -> convolution
        E = np.convolve(a_g, d)[: y_max + 1]
        # Psi(Y|xhat) = sum_{s=1}^{Y-1} E[s]
        cum = np.cumsum(E)
        psi_x = np.zeros(y_max + 1)
        psi_x[2:] = cum[1:y_max]
        psi += pi[xh] * psi_x
    return psi


def time_average_aoii(psi: np.ndarray, Y: int) -> float:
    return float(psi[Y] / Y) if Y > 0 else float("inf")


class SourceSet:
    """Per-UE Markov sources with precomputed Psi tables."""

    def __init__(self, num_ues: int, cfg: SourceConfig, seed: int):
        rng = np.random.default_rng(seed + 10_007)
        self.cfg = cfg
        self.n = cfg.num_states
        self.p_stay = rng.uniform(cfg.p_stay_range[0], cfg.p_stay_range[1], size=num_ues)
        self.P = np.stack([birth_death_matrix(self.n, p) for p in self.p_stay])
        self.f = distortion_matrix(self.n)
        self.pi = np.stack([stationary_distribution(P) for P in self.P])
        self.psi = np.stack([psi_table(P, self.f, cfg.psi_y_max) for P in self.P])   # (U, y_max+1)
        self.cumP = np.cumsum(self.P, axis=2)

    def avg_aoii_for_interval(self, Y: np.ndarray) -> np.ndarray:
        """Vectorized Psi_i(Y_i)/Y_i, Y clipped to the table length (longer intervals are extrapolated linearly)."""
        Y = np.asarray(Y)
        Yc = np.clip(Y, 1, self.cfg.psi_y_max)
        base = self.psi[np.arange(self.psi.shape[0]), Yc] / Yc
        # beyond the table AoII grows ~linearly in Y; extrapolate with the last slope
        slope = (self.psi[:, -1] / self.cfg.psi_y_max - self.psi[:, -2] / (self.cfg.psi_y_max - 1))
        return np.where(Y > self.cfg.psi_y_max, base + slope * (Y - self.cfg.psi_y_max), base)

    def simulate(self, num_slots: int, rng: np.random.Generator) -> np.ndarray:
        """Sample all source trajectories: returns X of shape (num_slots, U) with stationary start."""
        U = self.P.shape[0]
        X = np.empty((num_slots, U), dtype=np.int8)
        x = np.array([rng.choice(self.n, p=self.pi[i]) for i in range(U)])
        u = rng.random((num_slots, U))
        rows = np.arange(U)
        for t in range(num_slots):
            X[t] = x
            c = self.cumP[rows, x]                       # (U, n)
            x = (u[t][:, None] > c).sum(axis=1)
            x = np.minimum(x, self.n - 1)
        return X
