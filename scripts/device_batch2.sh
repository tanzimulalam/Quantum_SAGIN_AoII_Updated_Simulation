#!/usr/bin/env bash
# Second device batch: two more small 6-UE instances (seeds 6 and 7: 8/16 and 12/18 qubit domains), both domains each.
# Waits for the first batch to finish. Run from the sentinel_sim folder:
#   bash scripts/device_batch2.sh > logs/device_batch2.log 2>&1
set -u
cd "/c/Users/mf9i/Desktop/Quantum SAGIN AoII Paper/sentinel_sim"
while ! grep -q "batch done" logs/device_batch.log 2>/dev/null; do sleep 60; done
PY=.venv/Scripts/python.exe
run() { echo "=== $(date -u +%FT%TZ) $*"; "$PY" scripts/hardware_run.py --mode device --init greedy "$@"; echo "=== exit $?"; }
for s in 6 7; do run --ues 6 --seed "$s" --shots 4096; done
echo "=== batch2 done $(date -u +%FT%TZ)"
