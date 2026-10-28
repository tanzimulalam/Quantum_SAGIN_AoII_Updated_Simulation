#!/usr/bin/env bash
# wait for the running scenario-set sweeps, then run the capacity sweep and the Whittle rows of the UE and topology sweeps
cd "/c/Users/mf9i/Desktop/Quantum SAGIN AoII Paper/sentinel_sim"
count() { powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*run_sweeps.py*' -and \$_.CommandLine -like '*scen*' }).Count"; }
while [ "$(count | tr -d '[:space:]')" != "0" ]; do sleep 60; done
echo "=== scen sweeps finished $(date -u +%FT%TZ)"
.venv/Scripts/python.exe scripts/run_sweeps.py --seeds 30 --workers 14 --which cap --formulation compact --sat-model tle --ntn --append --out-prefix sweeps_tle_ntn
echo "=== cap done $(date -u +%FT%TZ)"
.venv/Scripts/python.exe scripts/run_sweeps.py --seeds 30 --workers 14 --which ue --formulation compact --sat-model tle --ntn --policies whittle --append --out-prefix sweeps_tle_ntn
echo "=== whittle ue done $(date -u +%FT%TZ)"
.venv/Scripts/python.exe scripts/run_sweeps.py --seeds 30 --workers 14 --which topo --formulation compact --sat-model tle --ntn --policies whittle --append --out-prefix sweeps_tle_ntn
echo "=== whittle topo done $(date -u +%FT%TZ)"
