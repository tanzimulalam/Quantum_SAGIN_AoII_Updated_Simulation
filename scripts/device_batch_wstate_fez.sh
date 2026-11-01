#!/usr/bin/env bash
# Replicate of the W-state batch on ibm_fez, submitted concurrently (queue waits overlap). ~4 s QPU per job.
cd "/c/Users/mf9i/Desktop/Quantum SAGIN AoII Paper/sentinel_sim"
PY=.venv/Scripts/python.exe
for s in 1 2 3 5 6 7; do
  "$PY" scripts/hardware_run.py --mode device --init w --backend ibm_fez --shots 4096 --ues 6 --seed $s --tag device_U6_k4_p1_s${s}_w_fez > logs/wstate_fez_s${s}.log 2>&1 &
done
"$PY" scripts/hardware_run.py --mode device --init w --backend ibm_fez --shots 4096 --ues 10 --seed 1 --domains 0 --tag device_U10_k4_p1_s1_w_fez > logs/wstate_fez_u10.log 2>&1 &
wait
echo "=== fez wstate batch done $(date -u +%FT%TZ)"
