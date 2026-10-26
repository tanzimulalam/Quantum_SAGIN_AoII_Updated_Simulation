# SENTINEL / VANGUARD reference simulator

Reference simulator for the manuscript "Distributed Quantum-Assisted Robust AoII Minimization in
Satellite-Ground Integrated Edge Networks" (SENTINEL framework, VANGUARD problem). Every modelling choice
follows the manuscript (Sections III to V), and every parameter the experiments use lives in
`sentinel/config.py`, so the paper's parameter table can be regenerated from the code that produced the figures.

Results and figures of the current run are summarised in `RESULTS.md`.

## Layout

| Path | Contents |
|---|---|
| `sentinel/config.py` | All parameters (network, radio, sources, disruption, solver, simulation) as dataclasses |
| `sentinel/geometry.py` | UE/BS placement; LEO passes with spherical-earth elevation, slant range, handover gaps |
| `sentinel/channel.py` | Path loss `varsigma + zeta log f + xi log d + margin`, antenna gains, Shannon rate with SE cap |
| `sentinel/sources.py` | Birth-death Markov sources, stationary distribution, the renewal-interval table Psi(Y) (Eqs. aoii_slot, psi_cond, psi_def) |
| `sentinel/scenarios.py` | Scenario set L (nominal, mild/severe shadowing, handover per SAT, joint) and the stochastic disruption process |
| `sentinel/problem.py` | Admissible sets A_i, outage tau_imq(l), inter-delivery interval Y, cost coefficients psi_imqh^(l) (Section IV-A) |
| `sentinel/qubo.py` | Epigraph domain QUBO (manuscript Section V): one-hot, capacity, scenario and ADMM terms with binary slacks; penalty weights from Proposition 1; Ising map |
| `sentinel/compact.py` | Compact slack-free formulation: scenario-weight dualization of the minimax, candidate pruning, compact domain QUBO (decision + capacity-slack qubits), one-hot-preserving annealer, warm-started ADMM |
| `sentinel/solvers/qaoa_xy.py` | XY-mixer QAOA for the compact QUBO (W-state or greedy warm start), classical decoding; shared with the hardware runner |
| `sentinel/solvers/qaoa.py` | Depth-p QAOA on Qiskit Aer (COBYLA on sampled energy), classical decoding |
| `sentinel/solvers/sa.py` | Simulated annealing on the same QUBO (used when a domain exceeds the simulable qubit count) |
| `sentinel/solvers/exact.py` | Brute-force QUBO minimizer (ground truth for small QUBOs) |
| `sentinel/solvers/ilp.py` | Exact ILP of P3 with HiGHS (the exact minimax reference) |
| `sentinel/solvers/greedy.py` | Greedy and Greedy + local search |
| `sentinel/admm.py` | SENTINEL: domain decomposition, sharing-ADMM consensus, incumbent with exact worst-case certificate, greedy repair |
| `sentinel/simulator.py` | Slot-level simulation: policies, realized channel with fading and disruption, AoII tracking, metrics |
| `sentinel/experiments.py` | Per-seed worker (common random numbers across policies) and summaries with 95% CIs |
| `scripts/run_sweeps.py` | UE sweep (5/10/15/20 UEs) and topology sweep, N seeds in parallel |
| `scripts/run_validation.py` | Optimality gaps of the epigraph encoding vs the exact ILP (QAOA at small scale, SA at large scale, severity and L sweeps) |
| `scripts/run_validation_compact.py` | Same protocol for the compact formulation: ILP, Greedy+LS, epigraph ADMM, compact ADMM, compact QAOA-XY |
| `scripts/hardware_run.py` | IBM Quantum runner: optimize on the simulator, sample once per domain on a device or a fake-backend noise model, decode and certify |
| `scripts/qaoa_depth_shots_study.py` | Depth / shots / initial-state study of the XY-QAOA on hardware-sized domains (P of sampling the optimal set vs uniform) |
| `sentinel/tle_geometry.py` | SGP4 propagation of the Starlink TLE snapshot in `data/`; persistent serving slots with natural handovers |
| `docs/section_V_draft.tex`, `docs/section_VI_draft.tex`, `docs/hardware_howto.md` | LaTeX drafts of the revised Sections V and VI (with Table I of values actually used) and the device-run guide |
| `docs/compact_formulation.md` | Mathematics of the compact formulation, XY mixers, ADMM fixes and the hardware protocol, in the manuscript's notation |
| `scripts/make_figures.py` | All figures (`figures/`) and tables (`results/tables.md`) |
| `tests/` | Smoke tests |

## Installation

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt      # Windows; use .venv/bin/python on Linux/macOS
```

Python 3.12, numpy, scipy, pandas, matplotlib, qiskit 2.x and qiskit-aer are required (pinned in `requirements.txt`).

## Running

```bash
.venv/Scripts/python.exe tests/smoke_core.py                      # end-to-end check on a small instance
.venv/Scripts/python.exe tests/test_psi_monte_carlo.py            # Psi(Y) vs Monte Carlo
.venv/Scripts/python.exe scripts/run_sweeps.py --seeds 30 --workers 16 --formulation compact --out-prefix sweeps_compact
.venv/Scripts/python.exe scripts/run_sweeps.py --seeds 30 --workers 16 --formulation epigraph
.venv/Scripts/python.exe scripts/run_validation.py --exp all --seeds 10 --seeds-small 5
.venv/Scripts/python.exe scripts/run_validation_compact.py --exp all --seeds 10 --seeds-small 5
.venv/Scripts/python.exe scripts/make_figures.py                                   # epigraph sweeps -> figures/
.venv/Scripts/python.exe scripts/make_figures.py --prefix sweeps_compact --fig-prefix compact   # -> figures/compact/
.venv/Scripts/python.exe tests/test_xy_mixer.py
```

Hardware (IBM Quantum Open Plan). Everything is optimized on the simulator; the device only samples once per domain:

```bash
.venv/Scripts/python.exe scripts/hardware_run.py --mode estimate --fake FakeTorino --ues 6      # sizes and QPU-time estimate, nothing submitted
.venv/Scripts/python.exe scripts/hardware_run.py --mode fake --fake FakeTorino --ues 6          # noisy local simulation with the device noise model
.venv/Scripts/python.exe scripts/hardware_run.py --mode device --ues 6 --domains 0              # real device; needs a saved IBM Quantum account
```

The device mode never reads a token from the command line or the repository. Save your account once in your own
Python session with `QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=..., overwrite=True)`.

The 30-seed sweeps take about 25 minutes on 16 cores; the validation about 45 minutes on 8 cores (the QAOA
instances dominate). Outputs go to `results/` (CSV) and `figures/` (PDF and PNG).

## Policies

- `random`: each slot each UE transmits with probability 0.1 over a uniformly chosen visible node; equal bandwidth share.
- `threshold`: the UE observes its own AoII and transmits whenever it is positive (rate-capped at one update per 5 slots) on the node with the best nominal rate. A state-aware closed-loop baseline.
- `nominal`: the SENTINEL solver run on the nominal scenario only (L = 1), i.e. the non-robust counterpart. Its schedule is still certified on the full scenario set.
- `sentinel`: robust SENTINEL (L = 6). Periodic sampling at the chosen rate, dedicated bandwidth level, chosen node, re-solved on every satellite visibility change and at least every 30 s.
- `sentinel_triggered`: the hybrid proposed in the paper's conclusion: SENTINEL's robust association and bandwidth, with transmissions triggered by the observed mismatch.
- `sentinel_capped_trigger`: same, with the chosen update period acting as a rate cap.
- `ppo`: a trained actor-critic agent (`sentinel/rl.py`) deciding node and update-period level per UE once per orchestration interval with an AoII reward; train with `scripts/train_rl.py --ues 5,10,15,20 --episodes 5000 --sat-model tle --ntn`, then evaluate with `run_sweeps.py --policies ppo --append`.

## Physical-layer options

- `net.sat_model = "synthetic"` (random passes with configurable maximum elevation and handover gaps) or `"tle"`:
  passes propagated with SGP4 from the Starlink snapshot in `data/starlink_tle_snapshot.txt` (10,636 satellites,
  fetched at the time recorded in `data/starlink_tle_snapshot.fetched_utc.txt`) over the MTSU site; each serving slot
  keeps its satellite until it sets and then hands over to the best visible one (6 to 12 natural handovers per 10 min
  at a 25 degree mask). Natural handovers interrupt the slot for `handover_window_slots`.
- `dis.ntn_model = True` adds the 3GPP TR 38.811 large-scale NTN channel: elevation-dependent LOS probability per
  pass, clutter loss in NLOS, slow shadow fading per pass, and atmospheric absorption (suburban or urban tables; Ku
  values interpolated between the S- and Ka-band entries).
- All policies use ACK feedback: a link with `failure_window_slots` (60) consecutive failed slots is blocked for
  `failure_block_slots` (600) and, for the SENTINEL variants, the schedule is re-solved with that link excluded
  (`sim.reactive_resolve`). Transient outages inside the scenario windows never trigger it.

```bash
.venv/Scripts/python.exe scripts/run_sweeps.py --seeds 30 --workers 16 --sat-model tle --ntn --out-prefix sweeps_tle_ntn
.venv/Scripts/python.exe scripts/make_figures.py --prefix sweeps_tle_ntn --fig-prefix tle_ntn
.venv/Scripts/python.exe scripts/run_sweeps.py --seeds 30 --workers 16 --which ue --sat-model tle --ntn --no-ack --out-prefix sweeps_tle_ntn_noack   # ablation
```

## Two formulations

`solver.formulation = "compact"` (default) uses the scenario-weight dual with candidate pruning (`k_cand = 4`): the
domain QUBO holds only decision qubits and a few capacity-slack bits, and one-hot is enforced by the XY mixer or by the
one-hot-preserving annealer. `"epigraph"` is the manuscript's original Section V encoding with epigraph and scenario
slack bits. Both are certified exactly by the worst case over the scenario set. See `docs/compact_formulation.md`.

## Honesty notes

- Domain QUBOs for the 5 to 20 UE sweeps have 100 to 400 qubits (the scenario slack bits dominate). They cannot be
  simulated with Aer. Real QAOA runs (Aer, depth 2, transverse-field mixer) are reported only for domains with at most
  26 qubits (validation experiment A).
- Two classical local solvers stand in at scale. `sa` is single-flip simulated annealing on the penalty QUBO itself
  (the classical analogue of the transverse-field mixer); it essentially never reaches an exactly feasible state at
  200+ qubits, which is reported as a finding. `sa_xy` anneals over one-hot-preserving moves with slack bits set
  optimally (the classical analogue of the XY mixer the paper mentions); it is the local solver used in the sweeps.
- Proposition 1's penalty weight is computed with the ADMM term bounded over feasible assignments (one combination per
  UE) rather than the whole hypercube; the proof only needs the bound at a feasible point, and the hypercube bound
  inflates the weight by about 50x.
- The exact reference is the ILP of P3 itself (same objective and constraints), not a bottleneck-assignment surrogate.
- All policies for a seed share topology, source trajectories, fading and disruption realization.
