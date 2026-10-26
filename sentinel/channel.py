"""Link budgets and rates (paper Section III-A).

PL(dB) = varsigma + zeta*log10(f) + xi*log10(d) + margin
R      = beta * min(log2(1 + SNR), SE_cap)
"""
from __future__ import annotations

import numpy as np

from .config import RadioConfig, C_LIGHT


def pathloss_db(dist_m, f_hz: float, xi: float, margin_db: float, rc: RadioConfig):
    dist_m = np.maximum(dist_m, 1.0)
    return rc.varsigma_db + rc.zeta * np.log10(f_hz) + xi * np.log10(dist_m) + margin_db


def noise_dbm(bw_hz, nf_db: float, rc: RadioConfig):
    return rc.noise_density_dbm_hz + 10.0 * np.log10(np.maximum(bw_hz, 1.0)) + nf_db


def rate_bps(bw_hz, snr_db, se_cap: float):
    snr_lin = 10.0 ** (np.asarray(snr_db, dtype=float) / 10.0)
    se = np.minimum(np.log2(1.0 + snr_lin), se_cap)
    return np.asarray(bw_hz) * se


def bs_rx_power_dbm(dist_m, rc: RadioConfig):
    pl = pathloss_db(dist_m, rc.bs_carrier_ghz * 1e9, rc.bs_xi, rc.bs_margin_db, rc)
    return rc.ue_tx_power_dbm + rc.ue_sub6_gain_dbi + rc.bs_antenna_gain_dbi - pl


def sat_rx_power_dbm(range_m, rc: RadioConfig, extra_loss_db=0.0):
    pl = pathloss_db(range_m, rc.sat_carrier_ghz * 1e9, rc.sat_xi, rc.sat_margin_db, rc)
    return rc.ue_tx_power_dbm + rc.ue_ku_gain_dbi + rc.sat_antenna_gain_dbi - pl - extra_loss_db


def bs_rate_bps(dist_m, bw_hz, rc: RadioConfig, fading_db=0.0):
    prx = bs_rx_power_dbm(dist_m, rc) + fading_db
    snr = prx - noise_dbm(bw_hz, rc.bs_noise_figure_db, rc)
    return rate_bps(bw_hz, snr, rc.bs_se_cap_bps_hz)


def sat_rate_bps(range_m, bw_hz, rc: RadioConfig, extra_loss_db=0.0, fading_db=0.0):
    prx = sat_rx_power_dbm(range_m, rc, extra_loss_db) + fading_db
    snr = prx - noise_dbm(bw_hz, rc.sat_noise_figure_db, rc)
    out = rate_bps(bw_hz, snr, rc.sat_se_cap_bps_hz)
    return np.where(np.isfinite(range_m) & np.isfinite(np.asarray(extra_loss_db, dtype=float)), out, 0.0)


def propagation_delay_s(dist_m):
    return np.asarray(dist_m) / C_LIGHT


def nominal_rate_table(topology, interval: int, rc: RadioConfig, extra_sat_loss_db=None):
    """R[i, m, q]: nominal rate of UE i at node m (BSs first, then SATs) with bandwidth level q.

    extra_sat_loss_db: optional (S,) array of scenario losses per satellite (inf = handover).
    Returns (rates, visible) with visible[i, m] bool.
    """
    U, B, S = topology.num_ues, topology.num_bs, topology.num_sat
    levels = np.array(rc.bandwidth_levels_mhz) * 1e6
    Q = len(levels)
    rates = np.zeros((U, B + S, Q))
    visible = np.zeros((U, B + S), dtype=bool)
    if B > 0:
        d = topology.ue_bs_distance_m()                       # (U,B)
        for q, bw in enumerate(levels):
            rates[:, :B, q] = bs_rate_bps(d, bw, rc)
        visible[:, :B] = True
    for j in range(S):
        vis = topology.sat_visible[j, interval]               # (U,)
        rg = topology.sat_range_m[j, interval]
        loss = 0.0 if extra_sat_loss_db is None else float(extra_sat_loss_db[j])
        for q, bw in enumerate(levels):
            r = sat_rate_bps(rg, bw, rc, extra_loss_db=loss)
            rates[:, B + j, q] = np.where(vis, r, 0.0)
        visible[:, B + j] = vis
    return rates, visible
