#!/usr/bin/env bash
# Submit the remaining W-state device jobs concurrently so that their queue waits overlap (seed 1 is already queued by
# device_batch_wstate.sh). Each job: a few minutes of local preparation, then one 4096-shot sampling job (~4 s QPU).
cd "/c/Users/mf9i/Desktop/Quantum SAGIN AoII Paper/sentinel_sim"
PY=.venv/Scripts/python.exe
for s in 2 3 5 6 7; do
  "$PY" scripts/hardware_run.py --mode device --init w --backend ibm_kingston --shots 4096 --ues 6 --seed $s --tag device_U6_k4_p1_s${s}_w > logs/wstate_s${s}.log 2>&1 &
done
"$PY" scripts/hardware_run.py --mode device --init w --backend ibm_kingston --shots 4096 --ues 10 --seed 1 --domains 0 --tag device_U10_k4_p1_s1_w > logs/wstate_u10.log 2>&1 &
wait
echo "=== parallel wstate batch done $(date -u +%FT%TZ)"
