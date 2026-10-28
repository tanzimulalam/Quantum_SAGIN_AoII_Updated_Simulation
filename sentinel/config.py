"""All simulation parameters in one place.

Every value here is the value actually used by the code; the results write-up
regenerates its parameter table from these dataclasses so that the paper's
Table I cannot drift from the experiments again.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Tuple, Dict, Any


@dataclass
class NetworkConfig:
    num_ues: int = 10
    num_bs: int = 2
    num_sat: int = 2                 # number of satellite "serving slots" (orbital planes); each is a succession of passes
    area_km: float = 20.0            # UEs uniform over area_km x area_km
    bs_height_m: float = 25.0
    ue_height_m: float = 1.5
    sat_altitude_km: float = 550.0
    min_elevation_deg: float = 10.0  # minimum usable elevation Theta
    num_domains: int = 2             # one BS per domain; all SATs are shared across domains
    # satellite pass model: "synthetic" (random passes) or "tle" (real constellation snapshot via SGP4)
    sat_model: str = "synthetic"
    sat_max_elevation_range_deg: Tuple[float, float] = (30.0, 90.0)
    sat_handover_gap_s: Tuple[float, float] = (5.0, 40.0)   # gap between consecutive passes in the same slot (synthetic)
    tle_file: str = "data/starlink_tle_snapshot.txt"
    site_lat_deg: float = 35.8456                           # Murfreesboro, TN (MTSU)
    site_lon_deg: float = -86.3903


@dataclass
class RadioConfig:
    ue_tx_power_dbm: float = 23.0
    noise_density_dbm_hz: float = -174.0
    # Path-loss model: PL = varsigma + zeta*log10(f_Hz) + xi*log10(d_m) + margin   (paper eq. for phi^us / phi^ub)
    varsigma_db: float = -147.55     # 20*log10(4*pi/c)
    zeta: float = 20.0
    # UE-BS link (sub-6 GHz)
    bs_carrier_ghz: float = 3.5
    bs_bandwidth_mhz: float = 20.0
    bs_xi: float = 26.0              # distance coefficient (exponent 2.6, suburban)
    bs_margin_db: float = 6.0        # NLOS / shadow margin
    bs_antenna_gain_dbi: float = 15.0
    ue_sub6_gain_dbi: float = 0.0
    bs_noise_figure_db: float = 7.0
    bs_se_cap_bps_hz: float = 6.0
    # UE-SAT link (Ku band)
    sat_carrier_ghz: float = 12.0
    sat_bandwidth_mhz: float = 50.0
    sat_xi: float = 20.0             # free space
    sat_margin_db: float = 1.0       # atmospheric absorption
    sat_antenna_gain_dbi: float = 30.0
    ue_ku_gain_dbi: float = 30.0     # fixed monitoring terminal with a small Ku dish
    sat_noise_figure_db: float = 9.0
    sat_se_cap_bps_hz: float = 4.0
    # discrete bandwidth levels (same for BS and SAT)
    bandwidth_levels_mhz: Tuple[float, ...] = (2.5, 5.0, 10.0)
    # slot-level realized fading (log-normal, dB) applied in the time-domain simulator only
    fading_std_db: float = 1.0


@dataclass
class SourceConfig:
    num_states: int = 4
    p_stay_range: Tuple[float, float] = (0.90, 0.99)
    aoii_budget: float = 10.0                      # Delta_i^{II,max} (5 is unsatisfiable for SAT-only UEs under a 30-slot outage)
    update_periods_slots: Tuple[int, ...] = (5, 10, 20, 50)   # 1/(rho_i^h T_s), H = 4 levels
    slot_ms: float = 10.0                          # T_s
    packet_bits: float = 20_000.0                  # D_i
    psi_y_max: int = 400                           # table length for Psi(Y)


@dataclass
class DisruptionConfig:
    """Scenario set L used by the robust optimizer and the stochastic process used by the simulator."""
    mild_shadowing_db: float = 6.0
    mild_scenario: bool = True                     # include the mild-shadowing scenario in L (never binds; see the L sweep)
    severe_shadowing_db: float = 12.0
    mild_window_slots: int = 20
    severe_window_slots: int = 30
    handover_window_slots: int = 20
    # realization process (per orchestration interval)
    p_shadowing_event_per_link: float = 0.07       # per UE-SAT link per interval; mild/severe equiprobable
    p_handover_failure_per_sat: float = 0.03       # per SAT per interval (random blockage, affects all its UEs)
    enabled: bool = True                           # False -> nominal channel (no stochastic disruption)
    # 3GPP TR 38.811 style NTN large-scale channel: elevation-dependent LOS probability, clutter loss in NLOS,
    # slow shadow fading per pass, atmospheric absorption. Applied to every UE-satellite link in the time domain.
    ntn_model: bool = False
    ntn_environment: str = "suburban"
    ntn_zenith_atmospheric_db: float = 0.5


@dataclass
class SolverConfig:
    # robust reformulation
    eta_resolution: float = 0.05                   # Delta_eta
    bandwidth_resolution_mhz: float = 2.5          # Delta_beta
    # ADMM
    admm_rho: float = 1.0
    admm_tol: float = 1e-2
    admm_max_rounds: int = 20
    # simulated annealing (classical QUBO solver used for large domains)
    sa_sweeps: int = 400
    sa_restarts: int = 4
    sa_t_start: float = 2.0
    sa_t_end: float = 0.01
    # QAOA (used when the domain QUBO fits in max_qaoa_qubits)
    qaoa_depth: int = 2
    qaoa_shots: int = 1024
    qaoa_maxiter: int = 200
    max_qaoa_qubits: int = 18
    solver: str = "auto"                           # "auto" | "qaoa" | "sa" (penalty QUBO, transverse-mixer analogue) | "sa_xy" (one-hot-preserving) | "qaoa_xy" | "exact"
    formulation: str = "compact"                   # "compact" (scenario-weight dual, slack-free) | "epigraph" (Section V encoding)
    dual_outer_iterations: int = 6                 # exponentiated-gradient iterations on the scenario weights
    k_cand: int = 4                                # candidate pruning: admissible combinations kept per UE (0 = all)


@dataclass
class SimConfig:
    duration_slots: int = 60_000                   # 10 min at 10 ms
    orchestration_interval_slots: int = 100        # 1 s
    resolve_every_intervals: int = 30              # re-solve robust schedule at least every 30 s, and on visibility change
    random_activation_prob: float = 0.10           # Random baseline: P(transmit) per slot
    threshold_aoii: float = 0.0                    # AoII-threshold baseline: transmit when AoII > threshold (0 = on any mismatch)
    min_update_gap_slots: int = 5                  # rate cap rho^max for baselines (same as shortest SENTINEL period)
    # ACK-based link-failure handling (all policies): after failure_threshold consecutive failed attempts on a node the
    # UE blocks that node for failure_block_slots; SENTINEL variants additionally re-solve with the link excluded
    failure_window_slots: int = 60                 # a link is declared down after 60 slots (0.6 s) of failures with no success
    failure_block_slots: int = 600
    reactive_resolve: bool = True
    bs_compute_gcycles_s: float = 120.0
    sat_compute_gcycles_s: float = 60.0
    cycles_per_bit: float = 500.0


@dataclass
class FullConfig:
    net: NetworkConfig = field(default_factory=NetworkConfig)
    radio: RadioConfig = field(default_factory=RadioConfig)
    src: SourceConfig = field(default_factory=SourceConfig)
    dis: DisruptionConfig = field(default_factory=DisruptionConfig)
    solver: SolverConfig = field(default_factory=SolverConfig)
    sim: SimConfig = field(default_factory=SimConfig)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


C_LIGHT = 299_792_458.0
EARTH_RADIUS_M = 6_371_000.0
