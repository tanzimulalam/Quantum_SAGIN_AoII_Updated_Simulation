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

### Real devices: ibm_kingston and ibm_fez (Heron r2, 156 qubits), 27 and 28 October 2026

`results/hardware/runs.md` (all runs), `results/hardware/device_*/` (summary, raw counts, job ids). Depth 1, greedy
warm start, 4096 shots per domain. All scenario weights, ADMM targets and QAOA angles are optimized on the local
simulator; each device job executes only the final sampling circuit of one or two domains. Domains above 26 qubits
cannot be simulated, so their angles are transferred from the largest simulated domain of the same run (recorded as
`params_source` in the summary); the batch script skips instances whose only domain is that large (seed 4: 44 qubits).

| Instance | Domain | Qubits | 2q gates | Depth | Device | Feasible shots | Best sample = noiseless optimum | Decoded schedule vs ILP |
|---|---|---|---|---|---|---|---|---|
| 6 UEs, seed 1 | 0 | 18 | 139 | 187 | kingston | 63.3% | yes | 0.00% |
| 6 UEs, seed 1 | 1 | 20 | 301 | 428 | kingston | 42.7% | yes | 0.00% |
| 6 UEs, seed 2 | 0 | 18 | 139 | 187 | kingston | 60.9% | yes | 0.00% |
| 6 UEs, seed 2 | 1 | 12 | 58 | 76 | kingston | 73.5% | yes | 0.00% |
| 6 UEs, seed 3 | 0 | 24 | 305 | 387 | kingston | 34.8% | yes | 0.00% |
| 6 UEs, seed 3 | 1 | 14 | 120 | 187 | kingston | 69.6% | yes | 0.00% |
| 6 UEs, seed 5 | 0 | 12 | 58 | 74 | kingston | 75.9% | yes | 0.00% |
| 6 UEs, seed 5 | 1 | 12 | 58 | 74 | kingston | 76.4% | yes | 0.00% |
| 6 UEs, seed 6 | 0 | 8 | 38 | 77 | fez | 86.5% | yes | 0.00% |
| 6 UEs, seed 6 | 1 | 16 | 79 | 77 | fez | 61.8% | yes | 0.00% |
| 6 UEs, seed 7 | 0 | 12 | 58 | 76 | fez | 71.9% | yes | 0.00% |
| 6 UEs, seed 7 | 1 | 18 | 142 | 171 | fez | 59.4% | yes | 0.00% |
| 10 UEs, seed 1 | 0 | 38 | 606 | 626 | kingston | 2.6% | yes (greedy reference) | 0.00% |

Thirteen device domains on six 6-UE instances and one 10-UE instance, 29 s of QPU time over eight jobs. In every
domain the best feasible device sample equals the noiseless optimum (for the 38-qubit domain, the greedy assignment,
which the exact ILP confirms as optimal), and every decoded network schedule attains the exact ILP optimum. The
feasible-shot fraction is the honest measure of device noise: 60 to 86% at 8 to 18 qubits and up to 139 two-qubit
gates, 35 to 43% at 20 to 24 qubits and about 300 gates, and 2.6% (107 of 4096 shots) at 38 qubits and 606 gates. The
noise-model predictions bracket the device values at 18 to 20 qubits (FakeTorino 52 and 33%, FakeFez 70 and 48%,
device 63 and 43%). At the 38-qubit scale the device still contains the optimum in 4096 shots, but a few hundred more
two-qubit gates would push the feasible fraction below one shot in a thousand; that, and not the simulator, is now the
documented limit of the quantum step.

### What the QAOA layers contribute (noiseless, 6-UE domains of 12 to 24 qubits, 3 seeds x 2 domains x 3 restarts)

`scripts/qaoa_depth_shots_study.py`, `results/qaoa_depth_shots.csv`, `figures/qaoa_depth_shots.*`. The optimizer
minimizes the mean implied-slack assignment energy of the samples; P(opt) is the probability that a final sample lies in
the set of optimal assignments (the optimum is degenerate: 3 to 27 of 24 to 576 one-hot states), compared with uniform
sampling of the one-hot subspace (0.219 on average).

| Initial state | Depth | P(sample in optimal set) at 128 / 512 / 2048 shots | Lift over uniform | Optimum found |
|---|---|---|---|---|
| W state | 1 | 0.274 / 0.275 / 0.283 | 1.45 to 1.48 | 100% |
| W state | 2 | 0.389 / 0.400 / 0.422 | 1.96 to 2.28 | 100% |
| Greedy basis state | 1 | 0.988 / 0.999 / 1.000 | 14.4 (greedy is already optimal) | 100% |
| Greedy basis state | 2 | 0.780 / 0.811 / 0.832 | 10.0 to 10.3 | 100% |

Three facts for the paper. (i) On every one of these domain instances the greedy assignment is already optimal, so the
warm-started circuit "finds" the optimum trivially and deeper circuits only diffuse away from it. (ii) From the W
state, one QAOA layer concentrates the distribution on the optimal set by a factor of about 1.5 and two layers by
about 2.2; the shot count per COBYLA evaluation hardly matters above 128. (iii) The optimum is always among the
samples because the feasible subspace is small; the quantum step is a correct constrained sampler at this scale, not a
stronger optimizer than greedy. Instances where greedy fails (50 UEs and above, 6 to 14% gaps) need 140 to 200 qubits
per domain and cannot be simulated. An earlier version of this study compared samples with a single optimal assignment
and therefore reported P(opt) about 0.02; those files are kept as `results/qaoa_depth_shots_singleopt_metric.csv` and
`results/qaoa_depth_shots_qubo_objective*.csv` (the latter also used the raw QUBO energy, dominated by slack bits, as
the optimizer objective).

## Real passes and the NTN channel (TLE + TR 38.811, 30 seeds, compact formulation)

`results/sweeps_tle_ntn_*`, `figures/tle_ntn/`, `results/tables_sweeps_tle_ntn.md`. Starlink snapshot passes at a
25 degree mask (9 natural handovers per 10 min), suburban NTN channel (4.9% of pass segments NLOS), stochastic
shadowing and handover-failure events as before, ACK-based link-failure handling for every policy.

Median average AoII, disruption on:

| UEs | Random | PPO (trained) | AoII threshold | Nominal | Robust SENTINEL | SENTINEL + trigger |
|---|---|---|---|---|---|---|
| 5 | 5.94 | 0.280 | 0.134 | 0.253 | 0.265 | 0.155 |
| 10 | 6.06 | 0.372 | 0.142 | 0.270 | 0.269 | 0.168 |
| 15 | 5.87 | 0.413 | 0.142 | 0.269 | 0.264 | 0.155 |
| 20 | 6.05 | 0.446 | 0.149 | 0.276 | 0.278 | 0.175 |

**PPO baseline** (`sentinel/rl.py`, `scripts/train_rl.py`, models in `models/`): an actor-critic agent that chooses,
once per orchestration interval, a serving node and an update-period level for every UE (invisible or ACK-blocked
nodes masked, equal bandwidth sharing), rewarded with minus the mean AoII of the interval plus a small delivery
bonus; trained for 5000 episodes of 60 intervals per network size on seeds 101 to 130 (disjoint from the evaluation
seeds), best trailing-average checkpoint kept, evaluated deterministically on the same 30 episodes as every other
policy. It reaches delivery ratios of 0.93 to 0.94 and a median AoII of 0.28 at 5 UEs, close to the nominal SENTINEL
schedule, but degrades with the size of its action space (0.45 at 20 UEs), routes 100% of traffic to satellites (it
never learns the BS hedge), and samples periodically (informative ratio 0.22 to 0.24, like SENTINEL). A first
training pass of 1500 episodes without ACK masking gave 0.5 to 16 and is kept in `models/v1_1500ep/`.

Topology at 10 UEs (median): ground-only 63 to 73 for every policy; satellite-only 0.14 (threshold) / 0.28 (robust) /
0.18 (trigger); integrated 2+2 and 3+3 as in the table; integrated 1+1 0.90 / 1.56 / 5.4.

- The certificate held in 98.7% of epochs (98.5% nominal): the dense constellation has no coverage gaps, and the
  remaining violations are NLOS passes whose clutter loss exceeds the 12 dB severe-shadowing scenario.
- Robust and nominal schedules are indistinguishable in realized median AoII (robust lower in 43 to 67% of seeds);
  the robust schedule's certificate is 4 to 8% lower (4.26 to 4.47 vs 4.40 to 4.84) and its mean at 20 UEs is lower
  (0.39 vs 0.46). SENTINEL routes 21 to 27% of deliveries to BSs, the threshold policy 2 to 3%.
- With ACK feedback the state-aware threshold policy is the strongest on average AoII; SENTINEL + trigger is within
  10 to 20% of it while keeping the certificate. Without feedback the threshold policy collapsed (AoII 32 on a test
  seed), so any state-aware baseline must be given the same feedback.
- Peak AoII is 100 to 250 for every policy, set by 20-slot handover interruptions and NLOS passes.
- Cost: 20 to 58 qubits per domain, 34 re-solve epochs plus 8 to 28 reactive re-solves per run, 34 to 223 s of
  solver time per 10-minute run.

### Paired statistical tests across seeds (`scripts/paired_stats.py`, `results/sweeps_tle_ntn_paired_stats.md`)

All policies run on the same 30 episodes (common random numbers), so every comparison is paired. For each sweep point
the table reports the median paired ratio, the fraction of seeds in which A is lower, the Hodges-Lehmann median
difference with a bootstrap 95% CI, the two-sided Wilcoxon signed-rank p (Holm-corrected within the sweep) and the
paired t p. With ACK feedback, disruption on:

| Comparison (A vs B) | 5 UEs | 10 UEs | 15 UEs | 20 UEs |
|---|---|---|---|---|
| Robust vs nominal SENTINEL, realized AoII | ratio 0.99, p = 0.35 | 1.01, p = 0.82 | 1.00, p = 0.22 | 0.99, p = 0.08 |
| Robust vs nominal, certified eta | 0.93, lower in 67%, p = 9e-5 | 0.95, 90%, p = 6e-6 | 0.97, 100%, p = 2e-9 | 0.98, 100%, p = 2e-9 |
| SENTINEL + capped trigger vs threshold | +0.027 [+0.009, +0.050], p = 0.013 | +0.024 [+0.012, +0.040], p = 7e-4 | +0.020 [+0.010, +0.038], p = 6e-4 | +0.027 [+0.013, +0.054], p = 1e-3 |
| Robust SENTINEL vs PPO | -0.028 [-0.068, +0.001], p = 0.50 | -0.118 [-0.157, -0.087], p = 5e-7 | -0.148 [-0.173, -0.126], p = 5e-8 | -0.151 [-0.206, -0.102], p = 6e-5 |
| Robust SENTINEL vs threshold | +0.130, p = 5e-8 | +0.127, p = 5e-8 | +0.124, p = 5e-8 | +0.127, p = 6e-5 |

(p values Holm-corrected.) So: the robust and nominal schedules are statistically indistinguishable in realized AoII
at every size, while the robust certificate is lower in 67 to 100% of seeds; the hybrid's gap to the threshold policy
(0.02 to 0.03 AoII) is small but significant; PPO is significantly worse than SENTINEL from 10 UEs on and tied at 5.

### Whittle-index baseline and the capacity-limited regime (`sentinel/whittle.py`, `--which cap`)

The Whittle index of each UE's restless arm (state = source state, estimate, age of the mismatch; cost = AoII;
action = transmit) is computed numerically per source by relative value iteration on a grid of transmission prices.
The scheduler ranks mismatched UEs by index every slot and admits them at their best node while the node's equally
shared bandwidth still delivers every admitted packet within the slot; observations, rate cap and ACK handling are
those of the threshold policy.

- At the default bandwidths (20 MHz BS, 50 MHz satellite) one node delivers 19 to 40 simultaneous sharers, so
  capacity never binds and the Whittle scheduler coincides with the threshold policy: identical medians (0.134 /
  0.141 / 0.142 / 0.146 at 5 / 10 / 15 / 20 UEs), Wilcoxon p >= 0.18 at every size and in every integrated or
  satellite-only topology, 1 to 2% fewer attempts (it does not try nodes that cannot deliver even alone). The
  threshold baseline of this study is therefore the Whittle-index policy of the AoII literature in this regime.
- Reducing the bandwidth per node at 20 UEs (`results/sweeps_tle_ntn_summary.csv`, sweep `capacity_limited`,
  `figures/tle_ntn/capacity_*`) separates them:

| Bandwidth per node | Random | AoII threshold | Whittle index |
|---|---|---|---|
| 20 MHz | 6.05 | 0.152 | 0.145 |
| 10 MHz | 6.10 | 0.152 | 0.148 |
| 5 MHz | 6.11 | 0.239 (delivery 0.87) | 0.152 (0.94) |
| 2 MHz | 6.31 | 33.5 (delivery 0.16) | 0.161 (0.95) |

  At 5 MHz the threshold policy is 57% worse (Whittle lower in 97% of seeds, p = 4e-9); at 2 MHz its simultaneous
  transmissions collapse every shared link (peak AoII 3654) while the capacity-aware index scheduler is unaffected.
- Ground-only topology is the one place the index policy loses (81 vs 63): its admission rule never tries a node
  that cannot deliver at the nominal rate, whereas the threshold policy's blind attempts occasionally succeed on a
  fading upswing. In the 1+1 topology they tie (0.87 vs 0.90, p = 0.14).

### Scenario-set size (`--which scen`, 10 UEs, 2 BS + 2 SAT, robust SENTINEL, 30 seeds)

The scenario list is nominal, +mild shadowing (6 dB), +severe shadowing (12 dB), +handover of satellite 1,
+handover of satellite 2, +joint outage; L truncates it in that order. `figures/tle_ntn/scenario_set_*`.

| L | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Median AoII, ACK on | 0.270 | 0.270 | 0.265 | 0.278 | 0.266 | 0.269 |
| Certified eta (mean) | 4.48 | 4.48 | 4.51 | 4.57 | 4.28 | 4.28 |
| Satellite delivery share | 0.77 | 0.77 | 0.78 | 0.79 | 0.74 | 0.74 |
| Certificate holds | 0.990 | 0.990 | 0.991 | 0.989 | 0.989 | 0.989 |
| Solver time per run (s) | 54 | 56 | 64 | 70 | 65 | 56 |
| Median AoII, no ACK | 1.16 | 1.16 | 1.88 | 2.29 | 1.47 | 1.50 |

The mild scenario never changes the schedule (L = 2 equals L = 1 on every seed) and the two shadowing scenarios
alone do not lower the certificate (the 1 to 2% rise at L = 3 and 4 is annealer noise); the hedge appears only once
the handover of the second shared satellite is in the set (L >= 5): the certificate drops 6% and a further 5% of
deliveries move to BSs. Realized AoII with feedback is flat in L. Without feedback it is non-monotone and noisy
(L = 6 lower than L = 1 in 47% of seeds, median ratio 1.006), i.e. the value of the scenario set lies in the
certificate, not in realized AoII at this size. Two scenarios (nominal and the joint/handover outage) would give the
same schedule as six at a third of the dual iterations.

### Ablation: no ACK-based link-failure handling (same model, UE sweep, 60 seeds)

`results/sweeps_tle_ntn_noack_*`, `figures/tle_ntn_noack/`, `results/sweeps_tle_ntn_noack_paired_stats.md`. The
first 30 seeds suggested a large robust-versus-nominal advantage; the paired tests did not support it, so the sweep
was extended to 60 seeds. Median (mean) average AoII, disruption on:

| UEs | Random | AoII threshold | Nominal | Robust SENTINEL | SENTINEL + trigger |
|---|---|---|---|---|---|
| 5 | 6.65 (6.71) | 0.97 (2.49) | 1.18 (2.78) | 1.01 (2.70) | 0.90 (2.70) |
| 10 | 6.70 (6.74) | 1.72 (2.52) | 1.12 (2.33) | 1.69 (2.34) | 1.57 (2.22) |
| 15 | 6.77 (6.79) | 2.47 (3.18) | 2.17 (2.63) | 1.58 (2.26) | 1.43 (2.11) |
| 20 | 6.73 (6.75) | 2.53 (2.83) | 1.90 (2.48) | 1.73 (2.41) | 1.61 (2.25) |

Paired tests (Wilcoxon, Holm-corrected within the sweep, 60 seeds):

- Without feedback every policy is an order of magnitude worse (a dead NLOS pass is simply ridden out) and the
  distributions are heavy-tailed (means 2 to 3 times the medians), which is why 30 seeds misled.
- Robust versus nominal SENTINEL: no significant difference at any size (robust lower in 45 to 65% of seeds,
  p >= 0.1 raw, >= 0.41 corrected). The robust certificate stays lower (77 to 100% of seeds, p <= 4e-9) and holds in
  87 to 92% of epochs versus 86 to 91% for the nominal one.
- The state-aware threshold policy loses its advantage: it ties the SENTINEL schedules at 5 and 10 UEs and is
  significantly worse than SENTINEL + trigger at 15 and 20 UEs (Hodges-Lehmann -0.77 [-1.29, -0.26] and -0.71
  [-1.13, -0.25], corrected p = 0.023 and 0.029, hybrid lower in 70 to 72% of seeds); robust SENTINEL alone is lower
  in 60 to 62% of seeds there (raw p 0.01 to 0.02, corrected 0.11 to 0.19). The threshold policy puts 98% of
  traffic on the best nominal satellite, the SENTINEL schedules 73 to 82%.
- So the value of failure feedback is a factor of ten for every policy, and the value of the scheduled BS share is a
  significant 25 to 30% at 15 to 20 UEs for the hybrid without feedback; the specific value of the robust scenario set
  over the nominal schedule remains the lower certificate, not a measurable gain in realized AoII. The earlier
  30-seed statement that the robust hedge was "worth 20 to 45%" is withdrawn.

## Summary of what the results support

- The renewal-interval decomposition is correct (Monte Carlo agreement within 1%), and the exact ILP of P3 is solvable
  in well under a second at every size considered.
- The certified worst-case AoII is valid against the modelled scenario set: 98.7% of epochs with real passes, 86 to
  98% with the synthetic pass model whose coverage gaps exceed every scenario window.
- The robust schedule's certificate is 4 to 8% below the nominal one at essentially no cost in median realized AoII,
  with a lower mean at high load; the robust schedule hedges by routing a quarter of deliveries to BSs.
- The satellite tier is essential in a 20 km area; ground-only monitoring fails, integrated 2+2 or 3+3 is best.
- A state-aware threshold policy with ACK feedback has the lowest average AoII in every setting; SENTINEL with
  state-aware triggering is within 10 to 20% of it while keeping the certificate (paired difference 0.02 to 0.03,
  Wilcoxon p <= 0.013 at every size). At the default bandwidths the threshold policy coincides with the Whittle-index
  scheduler; when bandwidth per node is cut to 5 MHz or less at 20 UEs, only the capacity-aware index scheduler
  survives (0.15 to 0.16 versus 0.24 and 33.5).
- Robust versus nominal SENTINEL is a statistical tie in realized AoII with and without ACK feedback (p >= 0.08,
  30 and 60 paired seeds) while the robust certificate is lower in 67 to 100% of seeds (p <= 9e-5). The scenario set
  earns its certificate only once the handover of the second shared satellite is included (L >= 5).
- Without failure feedback every policy is ten times worse; the SENTINEL hybrid is then significantly better than the
  threshold policy at 15 to 20 UEs (25 to 30%, corrected p <= 0.03, 60 seeds) because it keeps 20 to 27% of
  deliveries on BSs.
- The compact (dualized, slack-free) formulation is exact through 25 UEs with 4 to 5 times fewer qubits than the
  epigraph encoding, within 12% at 50 UEs, and limited by shared-satellite coordination at 75 to 100 UEs; the epigraph
  encoding is unusable beyond a few UEs.
- XY-mixer QAOA solves hardware-sized domains (12 to 24 qubits) to optimality in simulation and recovers the optimum
  from 36 to 70% surviving shots on Heron noise models and, on the real ibm_kingston and ibm_fez devices, from 35 to
  86% surviving shots at 8 to 24 qubits and 2.6% at 38 qubits (13 of 13 domains with the best sample at the noiseless
  optimum, every decoded schedule at the exact ILP optimum, 29 s of QPU time); it is a correct constrained sampler (1.5 to 2.2 times the
  uniform concentration on the optimal set at depth 1 to 2), not a better optimizer than greedy, which is already
  optimal on these domains.
