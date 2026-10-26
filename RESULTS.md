# Results of the current run

All numbers below were produced by this repository with the parameters in `sentinel/config.py`: 30 seeds per point,
60,000 slots (10 min) per run, five policies sharing topology, source trajectories, fading and disruption realization
for each seed. CSVs are in `results/`, figures in `figures/`, and `results/tables.md` lists every table with means,
95% confidence intervals, medians and quartiles.

## Parameters

| Group | Value |
|---|---|
| Network | 20 x 20 km area; 2 BSs on a jittered grid (25 m); 2 LEO planes at 550 km, passes with maximum elevation U[30, 90] deg and handover gaps U[5, 40] s; minimum elevation 10 deg; K = 2 domains (one BS each, satellites shared) |
| UE-BS link | 3.5 GHz, 20 MHz, PL = -147.55 + 20 log10 f + 26 log10 d + 6 dB, 23 dBm, BS gain 15 dBi, NF 7 dB, SE cap 6 bit/s/Hz |
| UE-SAT link | 12 GHz, 50 MHz, free space + 1 dB, 30 dBi + 30 dBi, NF 9 dB, SE cap 4 bit/s/Hz; spherical-earth slant range |
| Bandwidth levels | 2.5, 5, 10 MHz (Delta_beta = 2.5 MHz) |
| Sources | 4-state birth-death chains, self-transition U[0.90, 0.99] per UE, f(x, x_hat) = \|x - x_hat\| |
| Update periods | 5, 10, 20, 50 slots (H = 4); slot 10 ms; packet 20 kbit; AoII budget 10 |
| Scenario set (L = 6) | nominal; mild shadowing 6 dB / 20 slots; severe 12 dB / 30 slots; handover of each SAT (complete loss, 20 slots); joint (all SATs lost, 30 slots) |
| Realized disruption | per orchestration interval: shadowing event per UE-SAT link w.p. 0.07 (mild or severe), handover failure per SAT w.p. 0.03; plus natural pass gaps |
| Orchestration | re-solve on every visibility change and at least every 30 s; ADMM rho 1, tolerance 1e-2, up to 20 rounds; Delta_eta 0.05 |
| Local solver (sweeps) | one-hot-preserving annealer on the domain QUBO objective (400 sweeps x 4 restarts). QAOA (Qiskit Aer, depth 2) is used in the validation for domains of at most 26 qubits |
| Baselines | Random: P(tx) = 0.1 per slot, uniform visible node, equal share. AoII threshold: transmit when AoII > 0 on the best nominal node, equal share, at least 5 slots between deliveries. Nominal SENTINEL: same solver with L = 1. SENTINEL + trigger: SENTINEL's association and bandwidth with transmissions triggered by the observed mismatch |

## UE sweep (2 BS + 2 SAT, stochastic disruption on)

Average AoII per UE and slot, median over 30 seeds (means and CIs in `results/tables.md`; the mean is dominated by two
seeds in which both satellite planes were in a pass gap simultaneously):

| UEs | Random | AoII threshold | Nominal SENTINEL | Robust SENTINEL | SENTINEL + trigger |
|---|---|---|---|---|---|
| 5 | 6.93 | 0.138 | 0.278 | 0.271 | 0.157 |
| 10 | 6.81 | 0.141 | 0.296 | 0.271 | 0.150 |
| 15 | 6.80 | 0.145 | 0.353 | 0.283 | 0.151 |
| 20 | 6.80 | 0.145 | 0.468 | 0.325 | 0.151 |

Selected means at 10 UEs: delivery ratio 0.55 / 0.92 / 0.93 / 0.92 / 0.90; informative-update ratio 0.39 / 0.96 /
0.24 / 0.23 / 0.96; satellite delivery share 0.87 / 0.94 / 0.98 / 0.74 / 0.73; certified worst-case AoII
(time-weighted) 5.72 for the nominal and 4.27 for the robust schedule.

Observations:

1. The robust schedule's certified worst case is 22 to 25% below the nominal schedule's at every size. Its realized
   AoII is lower in 80% of seeds at 5 UEs and 97 to 100% of seeds at 10 to 20 UEs; the median improvement grows from
   3% at 5 UEs to 31% at 20 UEs. The robust schedule moves 20 to 25% of deliveries from satellites to BSs.
2. Realized average AoII stayed at or below the certified worst case in 98.0% of epochs and 96.7% of runs. Every
   violation coincides with a satellite pass gap (5 to 40 s) longer than any window in the scenario set; the certificate
   is valid against the modelled scenario set only.
3. The state-aware threshold policy has about half the AoII of robust SENTINEL because it transmits the moment the
   estimate is wrong, whereas SENTINEL samples periodically without observing the source.
4. SENTINEL's robust association with state-aware triggering matches the threshold policy (median 0.15 vs 0.14) at
   every size while keeping the worst-case certificate and raising the informative-update ratio from 0.23 to 0.96.
5. Switching the stochastic disruption process off (same seeds) lowers every policy's median AoII by about 25%.

## Topology comparison (10 UEs, disruption on)

Average AoII, median over 30 seeds:

| Topology | Random | AoII threshold | Nominal | Robust SENTINEL | + trigger |
|---|---|---|---|---|---|
| Ground only (2 BS) | 68.8 | 60.6 | 78.0 | 78.0 | 78.0 |
| Satellite only (2 SAT) | 2.79 | 0.154 | 0.312 | 0.281 | 0.158 |
| Integrated (1 BS + 1 SAT) | 10.1 | 3.85 | 4.19 | 4.11 | 3.83 |
| Integrated (2 BS + 2 SAT) | 6.81 | 0.141 | 0.296 | 0.271 | 0.150 |
| Integrated (3 BS + 3 SAT) | 6.53 | 0.139 | 0.294 | 0.262 | 0.138 |

Two BSs reach only UEs within about 5 to 7 km of a 20 x 20 km area, so ground-only monitoring fails. Two satellite planes
alone bring every policy below 0.4; a single plane is dominated by its pass gaps. In the integrated topologies robust
SENTINEL routes 21 to 30% of deliveries to BSs as a hedge against satellite disruption.

## Solver cost

| UEs | Qubits per domain (max) | Epochs per run | Solver time per 10-min run (s) |
|---|---|---|---|
| 5 | 120 | 29 | 11 |
| 10 | 164 | 30 | 34 |
| 15 | 212 | 31 | 42 |
| 20 | 261 | 32 | 43 |

The scenario slack bits (L x M_eta = 42) and epigraph bits dominate the auxiliary qubit count. These domains exceed
any statevector simulator, so the sweeps use the classical one-hot-preserving annealer.

## Validation against the exact optimum of P3

Reference: exact ILP of P3 (same variables, objective and constraints) solved with HiGHS. Gaps are reported over feasible
schedules only. One ILP instance (100 UEs, seed 1) hit the 300 s limit; all others solved in under 0.4 s.

### A. QAOA on Qiskit Aer (2 BS + 1 SAT, Q = 1, H = 2, L = 2, Delta_eta = 0.5, depth 2, 512 shots, 100 COBYLA iterations)

| UEs | Qubits per domain | Instances | QAOA optimal | Mean gap | Absolute eta: ILP / QAOA | Time per instance |
|---|---|---|---|---|---|---|
| 2 | 12 to 25 | 5 | 5 of 5 | 0% | 0.236 / 0.236 | 3 s to 12 min |
| 3 | 17 to 26 | 5 | 5 of 5 | 0% | 0.212 / 0.212 | 41 s to 25 min |
| 4 | 17 to 22 | 4 | 2 of 4 | 34% | 0.626 / 0.961 | 31 s to 5 min |
| 5 | 21 to 24 | 4 | 0 of 4 | 226% | 1.141 / 1.620 | 2 to 16 min |
| 6 | 18 to 25 | 4 | 0 of 4 | 266% | 0.195 / 0.641 | 35 s to 23 min |

Three further instances produced domains of 33 to 39 qubits and could not be simulated (Aer limit 31). QAOA reached its
local QUBO ground state in 5 of 18 checkable solves. The 4 to 6 UE gaps are caused by the coarse cost quantization
(Delta_eta = 0.5) needed to stay under about 26 qubits: the classical annealer on the identical QUBOs shows the same
gaps, and the same two-domain ADMM with Delta_eta = 0.05 matches the ILP exactly on all 16 instances. Restoring the
fine resolution adds about 4 bits per encoding and pushes even a 3-UE domain past 36 qubits.

### B. Network size (nodes scaled to 2+2, 2+2, 4+3, 6+4, 8+5; Q = 3, H = 4, L = 6, 10 seeds)

Mean gap (%) over feasible schedules; feasible fraction in brackets when below 1:

| UEs | Greedy | Greedy+LS | SA on penalty QUBO | Monolithic SA | SENTINEL (SA-XY ADMM) | SENTINEL + LS polish | Qubits per domain |
|---|---|---|---|---|---|---|---|
| 10 | 0.0 | 0.0 | 1.4 | 8.0 | 0.04 | 0.0 | 213 |
| 25 | 0.0 | 0.0 | 2.9 | 10.5 | 2.3 | 0.0 | 353 |
| 50 | 18.2 | 6.0 | 33.2 | 31.8 | 28.6 | 4.6 | 1008 |
| 75 | 15.8 | 14.4 | 133 | 113 | 237 [0.7] | 71 [0.7] | 1925 |
| 100 | 20.0 | 11.5 | 167 [0.7] | 126 | 292 [0.4] | 61 [0.4] | 3460 |

Greedy with local search is optimal through 25 UEs and within 6 to 14% beyond. The distributed loop is optimal through
25 UEs, degrades from 50 UEs, and fails to return a capacity-feasible schedule in 30 to 60% of the 75 and 100 UE
instances within 20 ADMM rounds. Single-flip annealing on the penalty QUBO never produced an exactly feasible domain
assignment (0 of 50 solves; 28% of UEs one-hot in the raw best sample).

### C. Disruption severity (20 UEs) and D. scenario count (20 UEs)

| Setting | Greedy+LS | SENTINEL (SA-XY ADMM) | + polish | Absolute eta (ILP) |
|---|---|---|---|---|
| mild (3/6 dB) | 0.0 | 3.1 | 0.0 | 2.77 |
| moderate (6/12 dB) | 0.0 | 1.1 | 0.0 | 4.54 |
| severe (9/15 dB) | 0.0 | 0.4 | 0.0 | 8.38 |
| extreme (12/20 dB) | 0.0 | 0.2 | 0.0 | 17.87 |
| L = 1 | 0.0 | 93 (0.215 vs 0.414 absolute) | 0.0 | 0.215 |
| L = 3 | 0.0 | 61 (2.94 vs 3.09) | 0.0 | 2.94 |
| L = 5 | 1.1 | 3.9 | 1.4 | 3.45 |
| L = 6 | 0.0 | 1.1 | 0.0 | 4.54 |

## Compact (slack-free) formulation

The results above use the manuscript's epigraph QUBO (Section V). `sentinel/compact.py` replaces it with a
scenario-weight dualization of the minimax, candidate pruning (k_cand = 4), and one-hot enforcement by XY mixers or
one-hot-preserving moves; `docs/compact_formulation.md` gives the mathematics. Both ADMM loops were also corrected
(warm start from an uncoupled round, rho scaled to the objective). Figures for the compact run are in
`figures/compact/`, tables in `results/tables_sweeps_compact.md`.

### Time-domain sweeps with the compact formulation (30 seeds, disruption on)

Average AoII, median over seeds:

| UEs | Random | AoII threshold | Nominal | Robust SENTINEL | + trigger | + rate-capped trigger |
|---|---|---|---|---|---|---|
| 5 | 6.93 | 0.138 | 0.279 | 0.268 | 0.149 | 0.149 |
| 10 | 6.81 | 0.141 | 0.282 | 0.265 | 0.145 | 0.145 |
| 15 | 6.80 | 0.145 | 0.270 | 0.261 | 0.147 | 0.147 |
| 20 | 6.80 | 0.145 | 0.269 | 0.265 | 0.149 | 0.149 |

Compared with the epigraph run, robust SENTINEL's AoII no longer grows with load (0.265 at 20 UEs versus 0.325), the
nominal schedule improves even more (0.269 versus 0.468), and the certified worst case of the robust schedule is 4 to
7% below the nominal one (4.27 versus 4.52 at 10 UEs) instead of 22 to 25%. Part of the earlier robust-versus-nominal
margin was therefore an artifact of the weaker solver, which is why both runs are reported. Robust SENTINEL still has
the lower realized AoII in 80 to 93% of seeds. Qubits per domain: 22 (5 UEs), 34 (10), 46 (15), 58 (20).

The certificate held in 86% of epochs (98% with the epigraph solver). The compact solver's certificates are tighter
(for example 3.50 versus 5.06 on the same seed with the same realized AoII), so fewer coverage-gap epochs fall under
the bound; every violation is still a satellite pass gap longer than any scenario window.

### Exact-optimum validation of the compact formulation

| Setting | Qubits per domain (compact / epigraph) | Compact + one-hot annealer | Epigraph + one-hot annealer | ILP on pruned instance |
|---|---|---|---|---|
| 20 UEs, K = 2 | 50 to 59 / 248 to 261 | 0.0% | 1.3 to 1.6% | 0.0% |
| 50 UEs, K = 2 | 149 to 161 / 725 to 842 | 0.0% | 12.6 to 21.5% | 0.0% |
| 50 UEs, K = 4 | 87 to 88 / 417 to 459 | 0.0% | 7.7 to 26.3% | 0.0% |
| 100 UEs, K = 8 | 156 to 171 / 1038 | 27 to 77% | 150% | 0.0% |

At 100 UEs the gap does not close with 60 ADMM rounds or 12 outer iterations (27 to 32%); with five satellites shared
by eight domains the coordination, not the inner solver, is the limit. Pruning to four candidates per UE never changed
the exact optimum.

Full validation (`scripts/run_validation_compact.py`; 10 seeds, 5 for the QAOA sets; gaps over feasible schedules):

| Setting (K = number of BSs) | Qubits per domain, compact / epigraph | Compact + XY-QAOA (Aer) | Compact + one-hot annealer | Epigraph + one-hot annealer | Greedy+LS |
|---|---|---|---|---|---|
| 4 / 6 / 8 UEs, 2 BS + 2 SAT | 8 to 24 / 133 to 193 | 0.0% (15 of 15 optimal) | 0.0% | 38 to 51% | 0.0% |
| 10 / 25 UEs, 2 + 2 | 44 / 78 vs 213 / 353 | - | 0.0% | 42.7 / 1.8% | 0.0% |
| 50 UEs, 4 + 3 | 142 / 704 | - | 11.5% | 38.8% | 6.0% |
| 75 / 100 UEs, 6 + 4 / 8 + 5 | 159 / 205 | - | 49.9 / 60.5% | not run | 14.4 / 11.5% |
| 20 UEs, severity mild to extreme | 29 to 66 | - | 0.0% at all levels | 0.2 to 4.7% | 0.0% |
| 20 UEs, L = 1 / 3 / 5 / 6 | 60 to 77 | - | 0.0 / 3.2 / 6.9 / 0.0% | 74 / 233 / 9.0 / 3.8% | 0 / 0 / 1.1 / 0% |

XY-mixer QAOA (depth 1, 512 shots, 40 COBYLA iterations) reached the exact optimum on every instance whose domains fit
the 26-qubit statevector cap (12 of 15; the other 3 fell back to the one-hot annealer and were also optimal), with 100%
one-hot and capacity-feasible samples in every solve. Pruning never changed the exact optimum. The scale limit is at
50 UEs and beyond, where coordinating five shared satellites across six to eight domains, not the inner solver, is the
bottleneck. Figures: `figures/validation_compact_*_gap.*`, `figures/qubits_compact_vs_epigraph.*`.

### Circuit sizes on a Heron processor model (FakeTorino, depth 1, optimization level 3)

| Domain | Qubits | ZZ couplings | Two-qubit gates (W start) | Two-qubit gates (greedy start) |
|---|---|---|---|---|
| 6 UEs, domain 0 | 18 | 22 | 206 | 144 |
| 6 UEs, domain 1 | 20 | 54 | 373 | 327 |
| 10 UEs, domain 1 | 19 | 46 | 318 | 287 |
| 10 UEs, domain 0 | 38 | 102 | 755 | 666 |
| 16 UEs, domain 1 | 36 | 54 | 517 | 406 |

Removing the one-hot penalty and the within-UE couplings cut the counts by 25 to 45%. Domains of about 20 qubits with
150 to 300 two-qubit gates are the realistic target for a device run; `scripts/hardware_run.py` prepares exactly that.

### Noisy simulation with the Heron device model (FakeTorino, 6 UEs, k_cand 4, depth 1, greedy start, 2048 shots)

| Domain | Qubits | Two-qubit gates | Depth | Noiseless feasible samples | Noisy one-hot samples | Noisy feasible samples | Best decoded energy (noisy = noiseless) |
|---|---|---|---|---|---|---|---|
| 0 | 18 | 137 | 169 | 100% | 54.4% | 54.4% | yes |
| 1 | 20 | 279 | 355 | 100% | 35.5% | 35.5% | yes |

Device noise breaks the one-hot structure in 46 to 65% of the shots, but the classical decoder discards those, and the
best surviving sample equals the noiseless optimum in both domains. The schedule decoded from the noisy samples has
eta = 2.5062, identical to the exact ILP optimum (`results/hardware/fake_U6_k4_p1_s1_greedy/`).

On the Heron r2 model (FakeFez) the same circuits (139 and 301 two-qubit gates) keep 69.6% and 47.6% of the shots
valid, and the decoded schedule is again the exact optimum. The same script submits these circuits to a real device
with `--mode device`, one sampling job per domain (a few seconds of QPU time).

## Summary of what the results support

- The renewal-interval decomposition is correct (Monte Carlo agreement within 1%), and the exact ILP of P3 is solvable
  in well under a second at every size considered.
- The certified worst-case AoII is valid against the modelled scenario set, and the robust schedule lowers both the
  certificate and the realized AoII relative to the nominal schedule.
- The satellite tier is essential in a 20 km area, and the robust schedule uses the BS tier as a hedge.
- Robust association combined with state-aware triggering matches the best state-aware baseline while keeping the
  certificate.
- Depth-2 QAOA reaches the optimum only on domains of at most 26 qubits, and only at a cost resolution too coarse to be
  useful beyond 3 UEs; the penalty-slack QUBO is not practically solvable by single-flip search at 200+ qubits;
  constraint-preserving moves are required. Greedy plus local search matches or beats the distributed loop at every
  size.
