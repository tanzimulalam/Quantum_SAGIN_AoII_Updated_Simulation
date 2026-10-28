#!/usr/bin/env bash
# after the capacity/Whittle chain: extend the no-ACK ablation (UE sweep) to seeds 31-60 for a 60-seed paired test
cd "/c/Users/mf9i/Desktop/Quantum SAGIN AoII Paper/sentinel_sim"
while ! grep -q "whittle topo done" logs/queue_after_scen.log 2>/dev/null; do sleep 60; done
echo "=== chain finished $(date -u +%FT%TZ)"
.venv/Scripts/python.exe scripts/run_sweeps.py --seed-start 31 --seeds 60 --workers 14 --which ue --formulation compact --sat-model tle --ntn --no-ack --append --out-prefix sweeps_tle_ntn_noack
echo "=== noack seeds 31-60 done $(date -u +%FT%TZ)"
