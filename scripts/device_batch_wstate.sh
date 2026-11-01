#!/usr/bin/env bash
# W-state (no warm start) device sampling of the hardware-sized domains, same device as the greedy-start runs, with
# per-shot statistics against the enumerated optimal set and the uniform-feasible baseline. About 4 s QPU per job.
cd "/c/Users/mf9i/Desktop/Quantum SAGIN AoII Paper/sentinel_sim"
PY=.venv/Scripts/python.exe
run() { echo "=== $(date -u +%FT%TZ) $*"; "$PY" scripts/hardware_run.py --mode device --init w --backend ibm_kingston --shots 4096 "$@" 2>&1 | grep -v -i warning; echo "=== exit $?"; }
for s in 1 2 3 5 6 7; do run --ues 6 --seed $s --tag device_U6_k4_p1_s${s}_w; done
run --ues 10 --seed 1 --domains 0 --tag device_U10_k4_p1_s1_w
echo "=== wstate batch done $(date -u +%FT%TZ)"
