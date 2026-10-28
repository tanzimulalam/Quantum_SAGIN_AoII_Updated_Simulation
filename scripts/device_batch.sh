#!/usr/bin/env bash
# Sequential device sampling batch (IBM Quantum Open Plan). Each job is a few seconds of QPU time; the
# simulator-side preparation and the queue dominate the wall time. Run from the sentinel_sim folder:
#   bash scripts/device_batch.sh > logs/device_batch.log 2>&1
set -u
PY=.venv/Scripts/python.exe
run() { echo "=== $(date -u +%FT%TZ) $*"; "$PY" scripts/hardware_run.py --mode device --init greedy "$@"; echo "=== exit $?"; }
# seed 1: the second (20-qubit) domain, kept in its own folder so the domain-0 run stays untouched
run --ues 6 --seed 1 --shots 4096 --domains 1 --tag device_U6_k4_p1_s1_greedy_d1
# seeds 2 to 5: both domains each
for s in 2 3 4 5; do run --ues 6 --seed "$s" --shots 4096; done
# scale probe: the 36 to 46 qubit domain of a 10-UE instance (400 to 800 two-qubit gates)
run --ues 10 --seed 1 --shots 4096 --domains 0
echo "=== batch done $(date -u +%FT%TZ)"
