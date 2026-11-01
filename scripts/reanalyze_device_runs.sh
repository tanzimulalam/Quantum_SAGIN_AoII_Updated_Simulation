#!/usr/bin/env bash
# Recompute per-shot statistics (P(optimal shot), approximation ratio, uniform-feasible baseline, energy spread) for
# every saved device run from its stored counts. Runs made before 28 Oct 2026 built their QUBOs with the QAOA inner
# solver in the dual loop (--dual-solver qaoa_xy); later runs used the annealer.
cd "/c/Users/mf9i/Desktop/Quantum SAGIN AoII Paper/sentinel_sim"
PY=.venv/Scripts/python.exe
for s in 1 2 3 5 6 7; do
  for tag in device_U6_k4_p1_s${s}_greedy device_U6_k4_p1_s${s}_greedy_d1; do
    [ -f results/hardware/$tag/summary.json ] || continue
    dom=$( [ "$tag" = "device_U6_k4_p1_s1_greedy" ] && echo 0 || ( [ "$tag" = "device_U6_k4_p1_s1_greedy_d1" ] && echo 1 || echo all ) )
    echo "=== $tag (domains $dom)"
    "$PY" scripts/hardware_run.py --mode device --init greedy --ues 6 --seed $s --shots 4096 --reanalyze --dual-solver qaoa_xy --domains $dom --tag $tag 2>&1 | grep -E 'P\(optimal|re-analysis|domain .*one-hot'
  done
done
for tag in device_U10_k4_p1_s1_greedy device_U10_k4_p1_s1_greedy_ctrl device_U10_k4_p1_s1_greedy_dd device_U10_k4_p1_s1_greedy_ddtwirl; do
  echo "=== $tag"; "$PY" scripts/hardware_run.py --mode device --init greedy --ues 10 --seed 1 --shots 4096 --reanalyze --dual-solver sa_xy --domains 0 --tag $tag 2>&1 | grep -E 'P\(optimal|re-analysis'
done
for tag in device_U6_k4_p1_s3_greedy_ctrl device_U6_k4_p1_s3_greedy_dd device_U6_k4_p1_s3_greedy_ddtwirl; do
  echo "=== $tag"; "$PY" scripts/hardware_run.py --mode device --init greedy --ues 6 --seed 3 --shots 4096 --reanalyze --dual-solver sa_xy --domains 0 --tag $tag 2>&1 | grep -E 'P\(optimal|re-analysis'
done
echo "=== reanalysis done"
