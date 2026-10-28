#!/usr/bin/env bash
# Regenerates every result table and figure of the study from scratch, in the order the paper reports them.
# Run from the sentinel_sim folder after installing requirements.txt into .venv:
#   bash scripts/reproduce_all.sh 2>&1 | tee logs/reproduce_all.log
# Approximate wall times are for a 16-core desktop. Device sampling (Section 9) needs a saved IBM Quantum account and
# is the only step that is not deterministic; everything else uses fixed seeds. Set WORKERS to your core count.
set -eu
cd "$(dirname "$0")/.."
PY=${PY:-.venv/Scripts/python.exe}; [ -x "$PY" ] || PY=.venv/bin/python
WORKERS=${WORKERS:-16}
mkdir -p logs results figures

echo "## 1. Checks (about 3 min): renewal-interval AoII vs Monte Carlo, XY mixers, end-to-end smoke tests"
"$PY" tests/test_psi_monte_carlo.py
"$PY" tests/test_xy_mixer.py
"$PY" tests/smoke_core.py
"$PY" tests/smoke_compact.py

echo "## 2. Synthetic-pass sweeps, epigraph and compact formulations (about 25 min each)"
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --formulation epigraph
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --formulation compact --out-prefix sweeps_compact

echo "## 3. Exact-optimum validation of both formulations (about 45 min each; QAOA instances dominate)"
"$PY" scripts/run_validation.py --exp all --seeds 10 --seeds-small 5 --workers "$WORKERS"
"$PY" scripts/run_validation_compact.py --exp all --seeds 10 --seeds-small 5 --workers "$WORKERS"

echo "## 4. Real passes (Starlink TLE) and the TR 38.811 channel: UE and topology sweeps (about 30 min)"
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --which ue --sat-model tle --ntn --out-prefix sweeps_tle_ntn
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --which topo --sat-model tle --ntn --append --out-prefix sweeps_tle_ntn
echo "##    Whittle-index rows, scenario-set size and bandwidth sweeps (about 15 min)"
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --which ue --sat-model tle --ntn --policies whittle --append --out-prefix sweeps_tle_ntn
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --which topo --sat-model tle --ntn --policies whittle --append --out-prefix sweeps_tle_ntn
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --which scen --sat-model tle --ntn --append --out-prefix sweeps_tle_ntn
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --which cap --sat-model tle --ntn --append --out-prefix sweeps_tle_ntn

echo "## 5. PPO baseline: training (about 2 h for 4 sizes x 5000 episodes) and evaluation on the same episodes"
"$PY" scripts/train_rl.py --ues 5,10,15,20 --episodes 5000 --train-slots 6000 --sat-model tle --ntn --train-seeds 101-130 --workers 4
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --which ue --sat-model tle --ntn --policies ppo --append --out-prefix sweeps_tle_ntn

echo "## 6. Ablation without ACK feedback: UE sweep on 60 seeds, scenario-set sweep on 30 (about 1 h)"
"$PY" scripts/run_sweeps.py --seeds 60 --workers "$WORKERS" --which ue --sat-model tle --ntn --no-ack --out-prefix sweeps_tle_ntn_noack
"$PY" scripts/run_sweeps.py --seeds 30 --workers "$WORKERS" --which scen --sat-model tle --ntn --no-ack --append --out-prefix sweeps_tle_ntn_noack

echo "## 7. Paired statistics across seeds"
"$PY" scripts/paired_stats.py --prefix sweeps_tle_ntn
"$PY" scripts/paired_stats.py --prefix sweeps_tle_ntn_noack

echo "## 8. QAOA depth / shots / initial-state study on hardware-sized domains (about 40 min)"
"$PY" scripts/qaoa_depth_shots_study.py --workers "$WORKERS" --seeds 3 --scale-modes max --inits w,greedy --out qaoa_depth_shots.csv

echo "## 9. Hardware: circuit sizes and noise-model runs (no account needed); device runs need a saved account"
"$PY" tests/circuit_size_check.py
"$PY" scripts/hardware_run.py --mode fake --fake FakeFez --ues 6 --init greedy --shots 2048
"$PY" scripts/hardware_run.py --mode fake --fake FakeTorino --ues 6 --init greedy --shots 2048 --tag fake_U6_k4_p1_s1_greedy_torino
if "$PY" -c "from qiskit_ibm_runtime import QiskitRuntimeService as S; S()" >/dev/null 2>&1; then
  bash scripts/device_batch.sh          # seeds 1-5 and the 10-UE probe
  bash scripts/device_batch2.sh         # seeds 6-7
  bash scripts/device_batch_mitigation.sh
else
  echo "no saved IBM Quantum account: device runs skipped (see docs/hardware_howto.md)"
fi
"$PY" scripts/collect_hardware.py

echo "## 10. Figures and tables"
"$PY" scripts/make_figures.py
"$PY" scripts/make_figures.py --prefix sweeps_compact --fig-prefix compact
"$PY" scripts/make_figures.py --prefix sweeps_tle_ntn --fig-prefix tle_ntn
"$PY" scripts/make_figures.py --prefix sweeps_tle_ntn_noack --fig-prefix tle_ntn_noack
echo "done"
