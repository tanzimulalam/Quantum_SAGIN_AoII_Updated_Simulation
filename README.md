# SENTINEL / VANGUARD reference simulator

Reference simulator for the manuscript "Distributed Quantum-Assisted Robust AoII Minimization in
Satellite-Ground Integrated Edge Networks" (SENTINEL framework, VANGUARD problem). Every modelling choice
follows the manuscript (Sections III to V), and every parameter the experiments use lives in
`sentinel/config.py`, so the paper's parameter table can be regenerated from the code that produced the figures.

Author: Tanzimul Alam Fahim (Computational Science PhD Program, Middle Tennessee State University).
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
| `sentinel/qubo.py` | Domain QUBO: epigraph, one-hot, capacity, scenario and ADMM terms with binary slacks; penalty weights from Proposition 1; Ising map |
| `sentinel/solvers/qaoa.py` | Depth-p QAOA on Qiskit Aer (COBYLA on sampled energy), classical decoding |
| `sentinel/solvers/sa.py` | Simulated annealing on the same QUBO (used when a domain exceeds the simulable qubit count) |
| `sentinel/solvers/exact.py` | Brute-force QUBO minimizer (ground truth for small QUBOs) |
| `sentinel/solvers/ilp.py` | Exact ILP of P3 with HiGHS (the exact minimax reference) |
| `sentinel/solvers/greedy.py` | Greedy and Greedy + local search |
| `sentinel/admm.py` | SENTINEL: domain decomposition, sharing-ADMM consensus, incumbent with exact worst-case certificate, greedy repair |
| `sentinel/simulator.py` | Slot-level simulation: policies, realized channel with fading and disruption, AoII tracking, metrics |
| `sentinel/experiments.py` | Per-seed worker (common random numbers across policies) and summaries with 95% CIs |
| `scripts/run_sweeps.py` | UE sweep (5/10/15/20 UEs) and topology sweep, N seeds in parallel |
| `scripts/run_validation.py` | Optimality gaps vs the exact ILP (QAOA at small scale, SA at large scale, severity and L sweeps) |
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
.venv/Scripts/python.exe scripts/run_sweeps.py --seeds 30 --workers 16
.venv/Scripts/python.exe scripts/run_validation.py --exp all --seeds 10 --seeds-small 5
.venv/Scripts/python.exe scripts/make_figures.py
```

The 30-seed sweeps take about 25 minutes on 16 cores; the validation about 45 minutes on 8 cores (the QAOA
instances dominate). Outputs go to `results/` (CSV) and `figures/` (PDF and PNG).

## Policies

- `random`: each slot each UE transmits with probability 0.1 over a uniformly chosen visible node; equal bandwidth share.
- `threshold`: the UE observes its own AoII and transmits whenever it is positive (rate-capped at one update per 5 slots) on the node with the best nominal rate. A state-aware closed-loop baseline.
- `nominal`: the SENTINEL solver run on the nominal scenario only (L = 1), i.e. the non-robust counterpart. Its schedule is still certified on the full scenario set.
- `sentinel`: robust SENTINEL (L = 6). Periodic sampling at the chosen rate, dedicated bandwidth level, chosen node, re-solved on every satellite visibility change and at least every 30 s.
- `sentinel_triggered`: the hybrid proposed in the paper's conclusion: SENTINEL's robust association and bandwidth, with transmissions triggered by the observed mismatch.

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
