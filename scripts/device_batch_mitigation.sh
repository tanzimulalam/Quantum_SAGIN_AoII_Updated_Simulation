#!/usr/bin/env bash
# Error-suppression comparison on the two largest device domains (24-qubit 6-UE seed 3 domain 0 and 38-qubit 10-UE
# seed 1 domain 0), same device as the unmitigated runs: dynamical decoupling alone, then DD + Pauli twirling.
# About 4 s of QPU time per job. Run from the sentinel_sim folder:
#   bash scripts/device_batch_mitigation.sh > logs/device_batch_mitigation.log 2>&1
set -u
cd "/c/Users/mf9i/Desktop/Quantum SAGIN AoII Paper/sentinel_sim"
PY=.venv/Scripts/python.exe
run() { echo "=== $(date -u +%FT%TZ) $*"; "$PY" scripts/hardware_run.py --mode device --init greedy --backend ibm_kingston --shots 4096 "$@"; echo "=== exit $?"; }
run --ues 6 --seed 3 --domains 0 --mitigation dd       --tag device_U6_k4_p1_s3_greedy_dd
run --ues 10 --seed 1 --domains 0 --mitigation dd      --tag device_U10_k4_p1_s1_greedy_dd
run --ues 6 --seed 3 --domains 0 --mitigation dd_twirl --tag device_U6_k4_p1_s3_greedy_ddtwirl
run --ues 10 --seed 1 --domains 0 --mitigation dd_twirl --tag device_U10_k4_p1_s1_greedy_ddtwirl
echo "=== mitigation batch done $(date -u +%FT%TZ)"
