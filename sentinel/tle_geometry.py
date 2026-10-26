"""Satellite passes from a real constellation snapshot (two-line elements, SGP4).

Each satellite "serving slot" j tracks one physical satellite at a time: the slot keeps its satellite while it is above
the minimum elevation and switches to the best newly visible satellite when it sets (a natural handover). Per
orchestration interval and per UE this yields elevation and slant range exactly as the synthetic pass model does, so
the rest of the simulator is unchanged. The TLE snapshot and its fetch time are stored in data/ for reproducibility.
"""
from __future__ import annotations

import datetime as dt
import functools
import pathlib
from typing import List, Tuple

import numpy as np

from .config import EARTH_RADIUS_M

DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "data"


@functools.lru_cache(maxsize=4)
def load_tles(path: str):
    from sgp4.api import Satrec, SatrecArray
    lines = [ln.rstrip() for ln in pathlib.Path(path).read_text().splitlines() if ln.strip()]
    sats, names = [], []
    i = 0
    while i + 2 < len(lines) + 1:
        if lines[i].startswith("1 ") and i + 1 < len(lines) and lines[i + 1].startswith("2 "):
            sats.append(Satrec.twoline2rv(lines[i], lines[i + 1])); names.append("")
            i += 2
        elif i + 2 < len(lines) and lines[i + 1].startswith("1 ") and lines[i + 2].startswith("2 "):
            sats.append(Satrec.twoline2rv(lines[i + 1], lines[i + 2])); names.append(lines[i].strip())
            i += 3
        else:
            i += 1
    return SatrecArray(sats), names, sats


def _gmst_rad(jd: np.ndarray) -> np.ndarray:
    T = (jd - 2451545.0) / 36525.0
    gmst_s = 67310.54841 + (876600.0 * 3600 + 8640184.812866) * T + 0.093104 * T ** 2 - 6.2e-6 * T ** 3
    return np.deg2rad((gmst_s / 240.0) % 360.0)


def _teme_to_ecef(r_teme: np.ndarray, jd: np.ndarray) -> np.ndarray:
    """r_teme: (..., T, 3) km; jd: (T,). Rotation about z by GMST (polar motion neglected)."""
    g = _gmst_rad(jd)
    c, s = np.cos(g), np.sin(g)
    x, y, z = r_teme[..., 0], r_teme[..., 1], r_teme[..., 2]
    return np.stack([c * x + s * y, -s * x + c * y, z], axis=-1)


def _geodetic_to_ecef(lat_deg, lon_deg, alt_m):
    a = 6378137.0; e2 = 6.69437999014e-3
    lat, lon = np.deg2rad(lat_deg), np.deg2rad(lon_deg)
    N = a / np.sqrt(1 - e2 * np.sin(lat) ** 2)
    return np.array([(N + alt_m) * np.cos(lat) * np.cos(lon), (N + alt_m) * np.cos(lat) * np.sin(lon), (N * (1 - e2) + alt_m) * np.sin(lat)])


def _enu_matrix(lat_deg, lon_deg):
    lat, lon = np.deg2rad(lat_deg), np.deg2rad(lon_deg)
    return np.array([[-np.sin(lon), np.cos(lon), 0.0],
                     [-np.sin(lat) * np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lat)],
                     [np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)]])


def _elev_range(r_sat_ecef_m: np.ndarray, site_ecef: np.ndarray, enu: np.ndarray):
    d = r_sat_ecef_m - site_ecef                       # (..., 3)
    local = d @ enu.T
    rng = np.linalg.norm(local, axis=-1)
    el = np.degrees(np.arcsin(np.clip(local[..., 2] / np.maximum(rng, 1.0), -1, 1)))
    return el, rng


def tle_passes(tle_path: str, site_lat_deg: float, site_lon_deg: float, ue_xy_m: np.ndarray, area_m: float,
               start_utc: dt.datetime, num_intervals: int, interval_s: float, num_slots: int, min_elevation_deg: float,
               shortlist_margin_deg: float = 5.0):
    """Return (elev (S,T,U), range (S,T,U), visible (S,T,U), switches: list of (slot, interval, sat_name), n_visible (T,))."""
    from sgp4.api import jday
    arr, names, _ = load_tles(tle_path)
    t = np.array([start_utc + dt.timedelta(seconds=(k + 0.5) * interval_s) for k in range(num_intervals)])
    jd = np.empty(num_intervals); fr = np.empty(num_intervals)
    for k, tk in enumerate(t):
        jd[k], fr[k] = jday(tk.year, tk.month, tk.day, tk.hour, tk.minute, tk.second + tk.microsecond * 1e-6)
    e, r_teme, _ = arr.sgp4(jd, fr)                   # r_teme: (N, T, 3) km
    ok = (e == 0).all(axis=1)
    r_ecef = _teme_to_ecef(r_teme, jd + fr) * 1e3    # m
    # site-level shortlist
    site = _geodetic_to_ecef(site_lat_deg, site_lon_deg, 0.0)
    enu = _enu_matrix(site_lat_deg, site_lon_deg)
    el_site, _ = _elev_range(r_ecef, site, enu)      # (N, T)
    el_site[~ok] = -90.0
    short = np.flatnonzero(el_site.max(axis=1) >= min_elevation_deg - shortlist_margin_deg)
    n_visible = (el_site >= min_elevation_deg).sum(axis=0)
    # per-UE geometry: UE offsets (east, north) in metres from the site at the area centre
    U = ue_xy_m.shape[0]
    offs = ue_xy_m - np.array([area_m / 2, area_m / 2])
    el_ue = np.empty((len(short), num_intervals, U)); rg_ue = np.empty_like(el_ue)
    for i in range(U):
        ue_ecef = site + enu.T @ np.array([offs[i, 0], offs[i, 1], 0.0])
        e_i, r_i = _elev_range(r_ecef[short], ue_ecef, enu)
        el_ue[:, :, i] = e_i; rg_ue[:, :, i] = r_i
    # serving-slot assignment with persistence (natural handovers)
    S = num_slots
    el = np.full((S, num_intervals, U), -np.inf); rg = np.full((S, num_intervals, U), np.inf)
    current = [-1] * S
    switches: List[Tuple[int, int, str]] = []
    for k in range(num_intervals):
        vis_k = el_site[short, k] >= min_elevation_deg
        taken = set(c for c in current if c >= 0)
        for j in range(S):
            c = current[j]
            if c >= 0 and vis_k[c]:
                continue
            # pick the best visible satellite (by site elevation) not held by another slot
            cands = [idx for idx in np.flatnonzero(vis_k) if idx not in taken]
            if cands:
                best = max(cands, key=lambda idx: el_site[short[idx], k])
                current[j] = best; taken.add(best)
                switches.append((j, k, names[short[best]] if names[short[best]] else str(short[best])))
            else:
                current[j] = -1
        for j in range(S):
            c = current[j]
            if c >= 0:
                el[j, k] = el_ue[c, k]; rg[j, k] = rg_ue[c, k]
    visible = el >= min_elevation_deg
    return el, rg, visible, switches, n_visible


def default_start_utc(tle_path: str, seed: int) -> dt.datetime:
    """A deterministic start time near the snapshot epoch: snapshot day at a seed-dependent minute of the day."""
    _, _, sats = load_tles(tle_path)
    epochs = np.array([s.jdsatepoch + s.jdsatepochF for s in sats[:200]])
    jd0 = float(np.median(epochs))
    base = dt.datetime(2000, 1, 1, 12, tzinfo=dt.timezone.utc) + dt.timedelta(days=jd0 - 2451545.0)
    base = base.replace(hour=0, minute=0, second=0, microsecond=0)
    return base + dt.timedelta(minutes=int((seed * 37) % 1440))
