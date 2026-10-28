# Paired comparisons, `sweeps_tle_ntn`, metric `average_aoii`, disruption on

Each row: 30 paired seeds (common random numbers). HL = Hodges-Lehmann median of the paired differences with a
bootstrap 95% CI; Wilcoxon p is two-sided signed-rank, Holm-corrected within the sweep.

| sweep | x | A | B | median A | median B | median A/B | A lower in | HL diff [95% CI] | Wilcoxon p (Holm) | paired t p |
|---|---|---|---|---|---|---|---|---|---|---|
| capacity_limited | 10.0 | whittle | threshold | 0.148 | 0.152 | 1.00 | 0.27 | +0.000 [-0.006, +0.000] | 2.5e-01 (5.0e-01) | 9.3e-01 |
| capacity_limited | 2.0 | whittle | threshold | 0.161 | 33.454 | 0.00 | 1.00 | -35.016 [-45.612, -26.393] | 1.9e-09 (7.5e-09) | 2.9e-08 |
| capacity_limited | 20.0 | whittle | threshold | 0.145 | 0.152 | 1.00 | 0.23 | +0.000 [-0.000, +0.000] | 7.9e-01 (7.9e-01) | 2.2e-01 |
| capacity_limited | 5.0 | whittle | threshold | 0.152 | 0.239 | 0.62 | 0.97 | -0.106 [-0.150, -0.074] | 3.7e-09 (1.1e-08) | 4.5e-03 |
| topology | Ground only (2 BS) | sentinel | nominal | 73.092 | 73.092 | 1.00 | 0.00 | +0.000 [+0.000, +0.000] | 1.0e+00 (1.0e+00) | nan |
| topology | Ground only (2 BS) | sentinel | random | 73.092 | 70.682 | 0.98 | 0.60 | -0.606 [-2.485, +2.885] | 4.8e-01 (1.0e+00) | 7.3e-01 |
| topology | Ground only (2 BS) | sentinel | threshold | 73.092 | 62.669 | 1.10 | 0.20 | +8.931 [+2.909, +14.391] | 1.1e-04 (1.5e-03) | 4.1e-04 |
| topology | Ground only (2 BS) | sentinel_capped_trigger | threshold | 71.426 | 62.669 | 1.09 | 0.17 | +8.110 [+2.824, +12.620] | 1.2e-04 (1.6e-03) | 4.5e-04 |
| topology | Ground only (2 BS) | sentinel_capped_trigger | whittle | 71.426 | 81.278 | 0.97 | 0.57 | -4.219 [-9.504, -0.191] | 4.0e-02 (4.0e-01) | 2.0e-02 |
| topology | Ground only (2 BS) | sentinel_triggered | threshold | 71.426 | 62.669 | 1.09 | 0.17 | +8.110 [+3.060, +12.127] | 1.2e-04 (1.6e-03) | 4.5e-04 |
| topology | Ground only (2 BS) | whittle | threshold | 81.278 | 62.669 | 1.16 | 0.13 | +14.294 [+8.025, +23.052] | 1.8e-05 (3.6e-04) | 1.0e-04 |
| topology | Integrated (1 BS + 1 SAT) | sentinel | nominal | 1.559 | 1.912 | 1.00 | 0.57 | -0.000 [-0.001, +0.000] | 4.0e-01 (1.0e+00) | 1.8e-01 |
| topology | Integrated (1 BS + 1 SAT) | sentinel | random | 1.559 | 6.829 | 0.22 | 0.90 | -4.806 [-5.215, -3.035] | 1.1e-05 (2.3e-04) | 1.5e-05 |
| topology | Integrated (1 BS + 1 SAT) | sentinel | threshold | 1.559 | 0.898 | 1.34 | 0.03 | +0.616 [+0.177, +1.495] | 3.7e-09 (1.1e-07) | 3.7e-03 |
| topology | Integrated (1 BS + 1 SAT) | sentinel_capped_trigger | threshold | 5.375 | 0.898 | 3.53 | 0.07 | +3.663 [+2.238, +5.682] | 1.9e-08 (5.2e-07) | 3.6e-04 |
| topology | Integrated (1 BS + 1 SAT) | sentinel_capped_trigger | whittle | 5.375 | 0.866 | 2.73 | 0.13 | +3.800 [+2.049, +5.808] | 2.3e-06 (5.4e-05) | 1.6e-04 |
| topology | Integrated (1 BS + 1 SAT) | sentinel_triggered | threshold | 5.375 | 0.898 | 3.53 | 0.07 | +3.663 [+2.335, +5.563] | 1.9e-08 (5.2e-07) | 3.6e-04 |
| topology | Integrated (1 BS + 1 SAT) | whittle | threshold | 0.866 | 0.898 | 0.98 | 0.70 | -0.029 [-0.058, +0.011] | 1.4e-01 (1.0e+00) | 3.5e-01 |
| topology | Integrated (2 BS + 2 SAT) | sentinel | nominal | 0.269 | 0.270 | 1.01 | 0.43 | +0.000 [-0.005, +0.004] | 8.2e-01 (1.0e+00) | 9.5e-01 |
| topology | Integrated (2 BS + 2 SAT) | sentinel | random | 0.269 | 6.056 | 0.05 | 1.00 | -5.640 [-5.939, -5.423] | 1.9e-09 (6.5e-08) | 5.9e-30 |
| topology | Integrated (2 BS + 2 SAT) | sentinel | threshold | 0.269 | 0.142 | 1.92 | 0.00 | +0.127 [+0.118, +0.138] | 1.9e-09 (6.5e-08) | 6.9e-20 |
| topology | Integrated (2 BS + 2 SAT) | sentinel_capped_trigger | threshold | 0.168 | 0.142 | 1.12 | 0.20 | +0.024 [+0.012, +0.038] | 5.0e-05 (9.4e-04) | 1.3e-03 |
| topology | Integrated (2 BS + 2 SAT) | sentinel_capped_trigger | whittle | 0.168 | 0.141 | 1.13 | 0.20 | +0.025 [+0.013, +0.040] | 1.6e-05 (3.4e-04) | 8.5e-04 |
| topology | Integrated (2 BS + 2 SAT) | sentinel_triggered | threshold | 0.168 | 0.142 | 1.12 | 0.20 | +0.024 [+0.011, +0.039] | 5.0e-05 (9.4e-04) | 1.3e-03 |
| topology | Integrated (2 BS + 2 SAT) | whittle | threshold | 0.141 | 0.142 | 1.00 | 0.07 | +0.000 [+0.000, +0.000] | 2.9e-01 (1.0e+00) | 1.7e-01 |
| topology | Integrated (3 BS + 3 SAT) | sentinel | nominal | 0.263 | 0.273 | 0.98 | 0.67 | -0.008 [-0.016, -0.001] | 1.5e-02 (1.7e-01) | 1.8e-02 |
| topology | Integrated (3 BS + 3 SAT) | sentinel | random | 0.263 | 6.035 | 0.04 | 1.00 | -5.797 [-5.977, -5.643] | 1.9e-09 (6.5e-08) | 7.8e-33 |
| topology | Integrated (3 BS + 3 SAT) | sentinel | threshold | 0.263 | 0.143 | 1.90 | 0.00 | +0.124 [+0.117, +0.131] | 1.9e-09 (6.5e-08) | 4.1e-24 |
| topology | Integrated (3 BS + 3 SAT) | sentinel_capped_trigger | threshold | 0.160 | 0.143 | 1.14 | 0.17 | +0.023 [+0.012, +0.031] | 8.9e-05 (1.5e-03) | 4.5e-05 |
| topology | Integrated (3 BS + 3 SAT) | sentinel_capped_trigger | whittle | 0.160 | 0.143 | 1.14 | 0.17 | +0.023 [+0.012, +0.031] | 8.9e-05 (1.5e-03) | 4.5e-05 |
| topology | Integrated (3 BS + 3 SAT) | sentinel_triggered | threshold | 0.160 | 0.143 | 1.14 | 0.17 | +0.023 [+0.012, +0.032] | 8.9e-05 (1.5e-03) | 4.5e-05 |
| topology | Integrated (3 BS + 3 SAT) | whittle | threshold | 0.143 | 0.143 | 1.00 | 0.00 | +0.000 [+0.000, +0.000] | 1.0e+00 (1.0e+00) | nan |
| topology | Satellite only (2 SAT) | sentinel | nominal | 0.278 | 0.278 | 1.00 | 0.37 | +0.001 [-0.007, +0.005] | 7.9e-01 (1.0e+00) | 6.0e-01 |
| topology | Satellite only (2 SAT) | sentinel | random | 0.278 | 2.720 | 0.11 | 1.00 | -2.441 [-2.516, -2.354] | 1.9e-09 (6.5e-08) | 1.5e-32 |
| topology | Satellite only (2 SAT) | sentinel | threshold | 0.278 | 0.141 | 1.94 | 0.00 | +0.139 [+0.129, +0.152] | 1.9e-09 (6.5e-08) | 6.0e-21 |
| topology | Satellite only (2 SAT) | sentinel_capped_trigger | threshold | 0.184 | 0.141 | 1.25 | 0.13 | +0.040 [+0.026, +0.056] | 2.6e-07 (6.6e-06) | 9.5e-02 |
| topology | Satellite only (2 SAT) | sentinel_capped_trigger | whittle | 0.184 | 0.141 | 1.26 | 0.13 | +0.040 [+0.026, +0.057] | 2.6e-07 (6.6e-06) | 9.5e-02 |
| topology | Satellite only (2 SAT) | sentinel_triggered | threshold | 0.184 | 0.141 | 1.25 | 0.13 | +0.040 [+0.026, +0.056] | 2.6e-07 (6.6e-06) | 9.5e-02 |
| topology | Satellite only (2 SAT) | whittle | threshold | 0.141 | 0.141 | 1.00 | 0.03 | +0.000 [+0.000, +0.000] | 3.2e-01 (1.0e+00) | 3.3e-01 |
| ue_sweep | 10 | nominal | ppo | 0.270 | 0.372 | 0.70 | 0.97 | -0.118 [-0.155, -0.088] | 3.7e-09 (1.0e-07) | 1.4e-08 |
| ue_sweep | 10 | sentinel | nominal | 0.269 | 0.270 | 1.01 | 0.43 | +0.000 [-0.005, +0.004] | 8.2e-01 (1.0e+00) | 9.5e-01 |
| ue_sweep | 10 | sentinel | ppo | 0.269 | 0.372 | 0.71 | 0.97 | -0.118 [-0.157, -0.088] | 2.6e-08 (6.8e-07) | 2.5e-08 |
| ue_sweep | 10 | sentinel | random | 0.269 | 6.056 | 0.05 | 1.00 | -5.640 [-5.924, -5.421] | 1.9e-09 (6.7e-08) | 5.9e-30 |
| ue_sweep | 10 | sentinel | threshold | 0.269 | 0.142 | 1.92 | 0.00 | +0.127 [+0.118, +0.138] | 1.9e-09 (6.7e-08) | 6.9e-20 |
| ue_sweep | 10 | sentinel_capped_trigger | threshold | 0.168 | 0.142 | 1.12 | 0.20 | +0.024 [+0.011, +0.041] | 5.0e-05 (9.4e-04) | 1.3e-03 |
| ue_sweep | 10 | sentinel_capped_trigger | whittle | 0.168 | 0.141 | 1.13 | 0.20 | +0.025 [+0.014, +0.040] | 1.6e-05 (3.7e-04) | 8.5e-04 |
| ue_sweep | 10 | sentinel_triggered | threshold | 0.168 | 0.142 | 1.12 | 0.20 | +0.024 [+0.012, +0.040] | 5.0e-05 (9.4e-04) | 1.3e-03 |
| ue_sweep | 10 | whittle | threshold | 0.141 | 0.142 | 1.00 | 0.07 | +0.000 [+0.000, +0.000] | 2.9e-01 (1.0e+00) | 1.7e-01 |
| ue_sweep | 15 | nominal | ppo | 0.269 | 0.413 | 0.66 | 1.00 | -0.146 [-0.169, -0.123] | 1.9e-09 (6.7e-08) | 7.6e-14 |
| ue_sweep | 15 | sentinel | nominal | 0.264 | 0.269 | 1.00 | 0.57 | -0.003 [-0.008, +0.002] | 2.2e-01 (1.0e+00) | 2.2e-01 |
| ue_sweep | 15 | sentinel | ppo | 0.264 | 0.413 | 0.66 | 1.00 | -0.148 [-0.173, -0.126] | 1.9e-09 (6.7e-08) | 4.4e-13 |
| ue_sweep | 15 | sentinel | random | 0.264 | 5.873 | 0.05 | 1.00 | -5.630 [-5.805, -5.455] | 1.9e-09 (6.7e-08) | 5.5e-34 |
| ue_sweep | 15 | sentinel | threshold | 0.264 | 0.142 | 1.81 | 0.00 | +0.124 [+0.114, +0.137] | 1.9e-09 (6.7e-08) | 3.0e-21 |
| ue_sweep | 15 | sentinel_capped_trigger | threshold | 0.155 | 0.142 | 1.11 | 0.23 | +0.020 [+0.010, +0.042] | 3.9e-05 (8.6e-04) | 5.3e-02 |
| ue_sweep | 15 | sentinel_capped_trigger | whittle | 0.155 | 0.142 | 1.11 | 0.23 | +0.020 [+0.010, +0.039] | 3.9e-05 (8.6e-04) | 5.3e-02 |
| ue_sweep | 15 | sentinel_triggered | threshold | 0.155 | 0.142 | 1.11 | 0.23 | +0.020 [+0.010, +0.041] | 3.9e-05 (8.6e-04) | 5.3e-02 |
| ue_sweep | 15 | whittle | threshold | 0.142 | 0.142 | 1.00 | 0.07 | +0.000 [+0.000, +0.000] | 1.8e-01 (1.0e+00) | 3.3e-01 |
| ue_sweep | 20 | nominal | ppo | 0.276 | 0.446 | 0.73 | 0.93 | -0.129 [-0.166, -0.086] | 1.5e-04 (2.3e-03) | 3.4e-01 |
| ue_sweep | 20 | sentinel | nominal | 0.278 | 0.276 | 0.99 | 0.60 | -0.004 [-0.014, +0.000] | 8.4e-02 (8.4e-01) | 1.4e-01 |
| ue_sweep | 20 | sentinel | ppo | 0.278 | 0.446 | 0.69 | 0.97 | -0.151 [-0.203, -0.102] | 3.8e-06 (9.5e-05) | 4.4e-02 |
| ue_sweep | 20 | sentinel | random | 0.278 | 6.051 | 0.05 | 1.00 | -5.722 [-5.838, -5.597] | 1.9e-09 (6.7e-08) | 1.4e-37 |
| ue_sweep | 20 | sentinel | threshold | 0.278 | 0.149 | 1.92 | 0.03 | +0.127 [+0.114, +0.137] | 3.8e-06 (9.5e-05) | 2.5e-04 |
| ue_sweep | 20 | sentinel_capped_trigger | threshold | 0.175 | 0.149 | 1.15 | 0.17 | +0.027 [+0.013, +0.057] | 1.2e-04 (2.1e-03) | 3.1e-02 |
| ue_sweep | 20 | sentinel_capped_trigger | whittle | 0.175 | 0.146 | 1.12 | 0.17 | +0.023 [+0.011, +0.040] | 4.6e-04 (6.4e-03) | 3.4e-01 |
| ue_sweep | 20 | sentinel_triggered | threshold | 0.175 | 0.149 | 1.15 | 0.17 | +0.027 [+0.013, +0.057] | 1.2e-04 (2.1e-03) | 3.1e-02 |
| ue_sweep | 20 | whittle | threshold | 0.146 | 0.149 | 1.00 | 0.20 | +0.000 [-0.000, +0.000] | 7.2e-01 (1.0e+00) | 2.2e-01 |
| ue_sweep | 5 | nominal | ppo | 0.253 | 0.280 | 0.98 | 0.57 | -0.020 [-0.066, +0.003] | 1.5e-01 (1.0e+00) | 6.9e-01 |
| ue_sweep | 5 | sentinel | nominal | 0.265 | 0.253 | 0.99 | 0.67 | -0.003 [-0.008, +0.005] | 3.5e-01 (1.0e+00) | 6.0e-01 |
| ue_sweep | 5 | sentinel | ppo | 0.265 | 0.280 | 0.97 | 0.63 | -0.028 [-0.068, +0.001] | 8.4e-02 (8.4e-01) | 6.4e-01 |
| ue_sweep | 5 | sentinel | random | 0.265 | 5.936 | 0.05 | 1.00 | -5.667 [-5.984, -5.350] | 1.9e-09 (6.7e-08) | 2.7e-26 |
| ue_sweep | 5 | sentinel | threshold | 0.265 | 0.134 | 2.00 | 0.00 | +0.130 [+0.117, +0.147] | 1.9e-09 (6.7e-08) | 2.0e-04 |
| ue_sweep | 5 | sentinel_capped_trigger | threshold | 0.155 | 0.134 | 1.10 | 0.27 | +0.027 [+0.009, +0.054] | 1.6e-03 (2.1e-02) | 2.1e-01 |
| ue_sweep | 5 | sentinel_capped_trigger | whittle | 0.155 | 0.134 | 1.10 | 0.27 | +0.027 [+0.009, +0.050] | 1.6e-03 (2.1e-02) | 2.2e-01 |
| ue_sweep | 5 | sentinel_triggered | threshold | 0.155 | 0.134 | 1.10 | 0.27 | +0.027 [+0.009, +0.052] | 1.6e-03 (2.1e-02) | 2.1e-01 |
| ue_sweep | 5 | whittle | threshold | 0.134 | 0.134 | 1.00 | 0.03 | +0.000 [+0.000, +0.000] | 6.5e-01 (1.0e+00) | 4.1e-01 |

## Certificates

- Certificate holds (fraction of epochs, all sweep points): nominal 0.852, sentinel 0.908
- topology x=Ground only (2 BS): certified eta robust/nominal median 1.000, robust lower in 0.00 of seeds, Wilcoxon p=1.00e+00
- topology x=Integrated (1 BS + 1 SAT): certified eta robust/nominal median 0.984, robust lower in 0.63 of seeds, Wilcoxon p=1.32e-04
- topology x=Integrated (2 BS + 2 SAT): certified eta robust/nominal median 0.950, robust lower in 0.90 of seeds, Wilcoxon p=5.61e-06
- topology x=Integrated (3 BS + 3 SAT): certified eta robust/nominal median 0.663, robust lower in 1.00 of seeds, Wilcoxon p=1.86e-09
- topology x=Satellite only (2 SAT): certified eta robust/nominal median 1.000, robust lower in 0.00 of seeds, Wilcoxon p=1.00e+00
- ue_sweep x=10: certified eta robust/nominal median 0.950, robust lower in 0.90 of seeds, Wilcoxon p=5.61e-06
- ue_sweep x=15: certified eta robust/nominal median 0.969, robust lower in 1.00 of seeds, Wilcoxon p=1.86e-09
- ue_sweep x=20: certified eta robust/nominal median 0.976, robust lower in 1.00 of seeds, Wilcoxon p=1.86e-09
- ue_sweep x=5: certified eta robust/nominal median 0.927, robust lower in 0.67 of seeds, Wilcoxon p=8.86e-05
