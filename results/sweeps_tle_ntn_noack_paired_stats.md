# Paired comparisons, `sweeps_tle_ntn_noack`, metric `average_aoii`, disruption on

Each row: 30 paired seeds (common random numbers). HL = Hodges-Lehmann median of the paired differences with a
bootstrap 95% CI; Wilcoxon p is two-sided signed-rank, Holm-corrected within the sweep.

| sweep | x | A | B | median A | median B | median A/B | A lower in | HL diff [95% CI] | Wilcoxon p (Holm) | paired t p |
|---|---|---|---|---|---|---|---|---|---|---|
| ue_sweep | 5 | sentinel | nominal | 1.013 | 1.182 | 0.98 | 0.65 | -0.042 [-0.396, +0.005] | 1.0e-01 (9.3e-01) | 8.6e-01 |
| ue_sweep | 5 | sentinel | random | 1.013 | 6.654 | 0.15 | 0.88 | -5.141 [-5.722, -4.358] | 4.3e-08 (7.4e-07) | 9.0e-09 |
| ue_sweep | 5 | sentinel | threshold | 1.013 | 0.967 | 1.57 | 0.33 | +0.106 [-0.093, +0.294] | 3.4e-01 (1.0e+00) | 6.3e-01 |
| ue_sweep | 5 | sentinel_capped_trigger | threshold | 0.904 | 0.967 | 1.00 | 0.52 | -0.003 [-0.230, +0.212] | 8.1e-01 (1.0e+00) | 6.4e-01 |
| ue_sweep | 5 | sentinel_triggered | threshold | 0.904 | 0.967 | 1.00 | 0.52 | -0.003 [-0.201, +0.206] | 8.1e-01 (1.0e+00) | 6.4e-01 |
| ue_sweep | 10 | sentinel | nominal | 1.687 | 1.119 | 1.01 | 0.45 | +0.059 [-0.204, +0.341] | 5.5e-01 (1.0e+00) | 9.5e-01 |
| ue_sweep | 10 | sentinel | random | 1.687 | 6.704 | 0.27 | 0.95 | -4.746 [-5.208, -4.190] | 5.7e-11 (1.1e-09) | 7.0e-23 |
| ue_sweep | 10 | sentinel | threshold | 1.687 | 1.721 | 1.18 | 0.38 | +0.044 [-0.398, +0.271] | 7.9e-01 (1.0e+00) | 5.1e-01 |
| ue_sweep | 10 | sentinel_capped_trigger | threshold | 1.571 | 1.721 | 0.96 | 0.53 | -0.100 [-0.464, +0.108] | 4.3e-01 (1.0e+00) | 2.6e-01 |
| ue_sweep | 10 | sentinel_triggered | threshold | 1.571 | 1.721 | 0.96 | 0.53 | -0.100 [-0.488, +0.117] | 4.3e-01 (1.0e+00) | 2.6e-01 |
| ue_sweep | 15 | sentinel | nominal | 1.583 | 2.172 | 0.85 | 0.60 | -0.329 [-0.680, -0.018] | 4.1e-02 (4.1e-01) | 1.3e-01 |
| ue_sweep | 15 | sentinel | random | 1.583 | 6.766 | 0.24 | 0.97 | -4.957 [-5.291, -4.504] | 3.6e-11 (7.3e-10) | 2.0e-25 |
| ue_sweep | 15 | sentinel | threshold | 1.583 | 2.465 | 0.76 | 0.60 | -0.639 [-1.132, -0.184] | 9.6e-03 (1.1e-01) | 1.7e-02 |
| ue_sweep | 15 | sentinel_capped_trigger | threshold | 1.432 | 2.465 | 0.70 | 0.70 | -0.774 [-1.286, -0.258] | 1.4e-03 (2.3e-02) | 6.3e-03 |
| ue_sweep | 15 | sentinel_triggered | threshold | 1.432 | 2.465 | 0.70 | 0.70 | -0.774 [-1.312, -0.258] | 1.4e-03 (2.3e-02) | 6.3e-03 |
| ue_sweep | 20 | sentinel | nominal | 1.728 | 1.895 | 0.97 | 0.57 | -0.099 [-0.358, +0.117] | 3.9e-01 (1.0e+00) | 7.5e-01 |
| ue_sweep | 20 | sentinel | random | 1.728 | 6.725 | 0.27 | 0.95 | -4.717 [-5.104, -4.262] | 3.7e-10 (6.7e-09) | 6.6e-22 |
| ue_sweep | 20 | sentinel | threshold | 1.728 | 2.525 | 0.74 | 0.62 | -0.525 [-0.954, -0.118] | 1.7e-02 (1.9e-01) | 1.7e-01 |
| ue_sweep | 20 | sentinel_capped_trigger | threshold | 1.612 | 2.525 | 0.65 | 0.72 | -0.709 [-1.127, -0.251] | 2.0e-03 (2.9e-02) | 5.4e-02 |
| ue_sweep | 20 | sentinel_triggered | threshold | 1.612 | 2.525 | 0.65 | 0.72 | -0.709 [-1.089, -0.271] | 2.0e-03 (2.9e-02) | 5.4e-02 |

## Certificates

- Certificate holds (fraction of epochs, all sweep points): nominal 0.881, sentinel 0.889
- ue_sweep x=5: certified eta robust/nominal median 0.926, robust lower in 0.77 of seeds, Wilcoxon p=3.52e-09
- ue_sweep x=10: certified eta robust/nominal median 0.952, robust lower in 0.95 of seeds, Wilcoxon p=5.14e-11
- ue_sweep x=15: certified eta robust/nominal median 0.967, robust lower in 1.00 of seeds, Wilcoxon p=1.63e-11
- ue_sweep x=20: certified eta robust/nominal median 0.977, robust lower in 1.00 of seeds, Wilcoxon p=1.63e-11
