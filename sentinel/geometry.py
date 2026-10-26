"""Topology: UE/BS placement and LEO satellite passes with real elevation geometry.

Each satellite "slot" j is a succession of passes: a satellite rises, culminates at a
random maximum elevation, sets below the minimum elevation, and after a handover gap
the next satellite of the plane rises. Elevation and slant range are computed on a
spherical Earth from the along-track and cross-track ground offsets, so the minimum
elevation constraint C5 really binds and handovers really happen.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from .config import NetworkConfig, EARTH_RADIUS_M


@dataclass
class Topology:
    ue_xy_m: np.ndarray          # (U, 2)
    bs_xy_m: np.ndarray          # (B, 2)
    bs_height_m: float
    ue_height_m: float
    # satellite geometry per orchestration interval
    sat_elev_deg: np.ndarray     # (S, T_int, U)  elevation of the active satellite of slot j seen from UE i; -inf if none
    sat_range_m: np.ndarray      # (S, T_int, U)  slant range
    sat_visible: np.ndarray      # (S, T_int, U)  bool, elevation >= Theta
    domain_of_ue: np.ndarray     # (U,) domain index (nearest BS)
    domain_of_bs: np.ndarray     # (B,)
    num_intervals: int

    @property
    def num_ues(self) -> int:
        return self.ue_xy_m.shape[0]

    @property
    def num_bs(self) -> int:
        return self.bs_xy_m.shape[0]

    @property
    def num_sat(self) -> int:
        return self.sat_elev_deg.shape[0]

    def ue_bs_distance_m(self) -> np.ndarray:
        d2 = ((self.ue_xy_m[:, None, :] - self.bs_xy_m[None, :, :]) ** 2).sum(-1)
        dh = self.bs_height_m - self.ue_height_m
        return np.sqrt(d2 + dh * dh)


def _ground_speed_m_s(altitude_m: float) -> float:
    mu = 3.986004418e14
    r = EARTH_RADIUS_M + altitude_m
    v_orb = np.sqrt(mu / r)
    return v_orb * EARTH_RADIUS_M / r


def _elevation_and_range(ground_dist_m: np.ndarray, altitude_m: float):
    """Spherical-earth elevation (deg) and slant range (m) from ground distance."""
    R = EARTH_RADIUS_M
    gamma = ground_dist_m / R
    rng = np.sqrt(R * R + (R + altitude_m) ** 2 - 2 * R * (R + altitude_m) * np.cos(gamma))
    el = np.degrees(np.arctan2(np.cos(gamma) - R / (R + altitude_m), np.sin(gamma)))
    return el, rng


def _cross_track_for_max_elevation(el_max_deg: float, altitude_m: float) -> float:
    """Ground cross-track offset that yields a given maximum elevation at culmination."""
    R = EARTH_RADIUS_M
    el = np.radians(el_max_deg)
    # elevation at culmination: tan(el) = (cos g - R/(R+h)) / sin g ; solve for g by bisection
    lo, hi = 0.0, np.pi / 2
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        e = np.arctan2(np.cos(mid) - R / (R + altitude_m), np.sin(mid))
        if e > el:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi) * R


def build_topology(cfg: NetworkConfig, seed: int, num_intervals: int, interval_s: float) -> Topology:
    rng = np.random.default_rng(seed)
    A = cfg.area_km * 1e3
    ue_xy = rng.uniform(0.0, A, size=(cfg.num_ues, 2))

    # BSs on a jittered grid so that every BS has a service region
    bs_xy = []
    cols = max(int(np.ceil(np.sqrt(cfg.num_bs))), 1)
    rows = int(np.ceil(cfg.num_bs / cols)) if cfg.num_bs > 0 else 0
    k = 0
    for r in range(rows):
        for c in range(cols):
            if k >= cfg.num_bs:
                break
            x = (c + 0.5) * A / cols + rng.uniform(-0.1, 0.1) * A / cols
            y = (r + 0.5) * A / rows + rng.uniform(-0.1, 0.1) * A / rows
            bs_xy.append([x, y])
            k += 1
    bs_xy = np.array(bs_xy).reshape(-1, 2)

    # domains: UE belongs to the domain of its nearest BS; each BS is its own domain (K = num_bs, capped at num_domains)
    K = min(cfg.num_domains, max(cfg.num_bs, 1))
    domain_of_bs = np.arange(cfg.num_bs) % K if cfg.num_bs > 0 else np.zeros(0, dtype=int)
    if cfg.num_bs > 0:
        d2 = ((ue_xy[:, None, :] - bs_xy[None, :, :]) ** 2).sum(-1)
        domain_of_ue = domain_of_bs[np.argmin(d2, axis=1)]
    else:
        # no BS: split UEs geographically into K domains by x coordinate
        domain_of_ue = (ue_xy[:, 0] * K / A).astype(int).clip(0, K - 1)

    # satellite passes
    h = cfg.sat_altitude_km * 1e3
    v_g = _ground_speed_m_s(h)
    t_int = (np.arange(num_intervals) + 0.5) * interval_s
    center = np.array([A / 2, A / 2])
    S = cfg.num_sat
    el = np.full((S, num_intervals, cfg.num_ues), -np.inf)
    rg = np.full((S, num_intervals, cfg.num_ues), np.inf)
    horizon_s = num_intervals * interval_s
    for j in range(S):
        # heading of the ground track (random azimuth), random initial phase
        az = rng.uniform(0, 2 * np.pi)
        u_along = np.array([np.cos(az), np.sin(az)])
        u_cross = np.array([-np.sin(az), np.cos(az)])
        t = -rng.uniform(0.0, 300.0)   # time at which the first pass culminates (may be in the past)
        while t < horizon_s + 600.0:
            el_max = rng.uniform(*cfg.sat_max_elevation_range_deg)
            c_off = _cross_track_for_max_elevation(el_max, h) * rng.choice([-1.0, 1.0])
            # pass duration: ground distance at which elevation drops to Theta
            g_theta = _cross_track_for_max_elevation(cfg.min_elevation_deg, h)
            half_len = np.sqrt(max(g_theta ** 2 - c_off ** 2, 0.0))
            half_dur = half_len / v_g
            t0, t1 = t - half_dur, t + half_dur
            mask = (t_int >= t0) & (t_int <= t1)
            if mask.any():
                s_along = v_g * (t_int[mask] - t)                       # along-track ground offset of sub-satellite point
                # UE-relative offsets (UE positions relative to area centre, projected)
                rel = ue_xy - center                                     # (U,2)
                rel_along = rel @ u_along
                rel_cross = rel @ u_cross
                gd = np.sqrt((s_along[:, None] - rel_along[None, :]) ** 2 + (c_off - rel_cross[None, :]) ** 2)
                e, r = _elevation_and_range(gd, h)
                el[j][mask] = e
                rg[j][mask] = r
            gap = rng.uniform(*cfg.sat_handover_gap_s)
            t = t1 + gap + half_dur  # next pass culminates after the gap
    visible = el >= cfg.min_elevation_deg
    return Topology(
        ue_xy_m=ue_xy, bs_xy_m=bs_xy, bs_height_m=cfg.bs_height_m, ue_height_m=cfg.ue_height_m,
        sat_elev_deg=el, sat_range_m=rg, sat_visible=visible,
        domain_of_ue=domain_of_ue, domain_of_bs=domain_of_bs, num_intervals=num_intervals,
    )
