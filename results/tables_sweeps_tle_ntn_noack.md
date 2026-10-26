# Regenerated results tables

## Certificate validity (fraction of epochs with realized avg AoII <= certified worst case)

| policy   |   certificate_holds |
|:---------|--------------------:|
| nominal  |            0.872547 |
| sentinel |            0.884222 |

## ue_sweep, disruption off

|   x | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   5 | AoII threshold (state-aware)   |  30 |          2.284 |     686.967 |            0.753 |               0.957 |           0.484 |        2.791 |                0.97  |              nan     |       0.809 |         1.852 |
|   5 | Nominal (non-robust) SENTINEL  |  30 |          3.5   |     973.5   |            0.866 |               0.223 |           1.935 |        4.975 |                0.855 |                4.84  |       1.618 |         1.521 |
|   5 | Random                         |  30 |          6.778 |     416     |            0.538 |               0.385 |           0.539 |        3.247 |                0.902 |              nan     |       0.354 |         6.754 |
|   5 | SENTINEL (robust)              |  30 |          2.726 |     806.1   |            0.869 |               0.223 |           1.937 |        4.658 |                0.789 |                4.47  |       1.219 |         1.325 |
|   5 | SENTINEL + rate-capped trigger |  30 |          2.85  |     835.433 |            0.747 |               0.957 |           0.484 |        4.396 |                0.762 |                4.47  |       1.29  |         1.296 |
|   5 | SENTINEL + state-aware trigger |  30 |          2.85  |     835.433 |            0.747 |               0.957 |           0.484 |        4.396 |                0.762 |                4.47  |       1.29  |         1.296 |
|  10 | AoII threshold (state-aware)   |  30 |          2.69  |    1213.6   |            0.738 |               0.955 |           1     |        2.836 |                0.976 |              nan     |       0.861 |         2.118 |
|  10 | Nominal (non-robust) SENTINEL  |  30 |          2.21  |     800.7   |            0.861 |               0.231 |           3.869 |        5.486 |                0.771 |                4.483 |       0.967 |         1.098 |
|  10 | Random                         |  30 |          6.66  |     424.633 |            0.554 |               0.385 |           1.108 |        3.318 |                0.878 |              nan     |       0.301 |         6.669 |
|  10 | SENTINEL (robust)              |  30 |          2.193 |     897.4   |            0.864 |               0.231 |           3.874 |        5.13  |                0.733 |                4.278 |       0.736 |         1.481 |
|  10 | SENTINEL + rate-capped trigger |  30 |          2.014 |     881     |            0.755 |               0.955 |           1.004 |        4.57  |                0.725 |                4.278 |       0.718 |         1.454 |
|  10 | SENTINEL + state-aware trigger |  30 |          2.014 |     881     |            0.755 |               0.955 |           1.004 |        4.57  |                0.725 |                4.278 |       0.718 |         1.454 |
|  15 | AoII threshold (state-aware)   |  30 |          2.884 |    1366.7   |            0.737 |               0.955 |           1.524 |        2.947 |                0.979 |              nan     |       1.061 |         2.37  |
|  15 | Nominal (non-robust) SENTINEL  |  30 |          2.714 |    1331.13  |            0.876 |               0.234 |           5.827 |        5.866 |                0.748 |                4.404 |       0.967 |         1.994 |
|  15 | Random                         |  30 |          6.764 |     505.5   |            0.555 |               0.388 |           1.663 |        3.319 |                0.875 |              nan     |       0.34  |         6.702 |
|  15 | SENTINEL (robust)              |  30 |          2.181 |    1249.43  |            0.888 |               0.234 |           5.848 |        5.476 |                0.724 |                4.256 |       0.855 |         1.545 |
|  15 | SENTINEL + rate-capped trigger |  30 |          2.028 |    1228.2   |            0.784 |               0.955 |           1.535 |        4.658 |                0.718 |                4.256 |       0.87  |         1.394 |
|  15 | SENTINEL + state-aware trigger |  30 |          2.028 |    1228.2   |            0.784 |               0.955 |           1.535 |        4.658 |                0.718 |                4.256 |       0.87  |         1.394 |
|  20 | AoII threshold (state-aware)   |  30 |          2.94  |    1792.17  |            0.724 |               0.955 |           2.008 |        3.017 |                0.979 |              nan     |       0.799 |         2.468 |
|  20 | Nominal (non-robust) SENTINEL  |  30 |          2.487 |    1284.5   |            0.871 |               0.232 |           7.762 |        6.399 |                0.766 |                4.466 |       0.818 |         1.877 |
|  20 | Random                         |  30 |          6.769 |     581.033 |            0.549 |               0.389 |           2.194 |        3.368 |                0.881 |              nan     |       0.198 |         6.69  |
|  20 | SENTINEL (robust)              |  30 |          2.12  |    1332.07  |            0.876 |               0.232 |           7.775 |        5.896 |                0.746 |                4.341 |       0.579 |         1.74  |
|  20 | SENTINEL + rate-capped trigger |  30 |          1.912 |    1279.23  |            0.769 |               0.955 |           2.02  |        4.716 |                0.734 |                4.341 |       0.565 |         1.542 |
|  20 | SENTINEL + state-aware trigger |  30 |          1.912 |    1279.23  |            0.769 |               0.955 |           2.02  |        4.716 |                0.734 |                4.341 |       0.565 |         1.542 |

## ue_sweep, disruption on

|   x | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   5 | AoII threshold (state-aware)   |  30 |          2.303 |     688.633 |            0.728 |               0.957 |           0.482 |        2.833 |                0.97  |              nan     |       0.808 |         1.867 |
|   5 | Nominal (non-robust) SENTINEL  |  30 |          3.523 |     977.9   |            0.843 |               0.223 |           1.923 |        4.975 |                0.855 |                4.84  |       1.618 |         1.544 |
|   5 | Random                         |  30 |          6.855 |     422.5   |            0.535 |               0.386 |           0.535 |        3.288 |                0.901 |              nan     |       0.357 |         6.808 |
|   5 | SENTINEL (robust)              |  30 |          2.744 |     809.3   |            0.848 |               0.223 |           1.927 |        4.659 |                0.789 |                4.47  |       1.219 |         1.351 |
|   5 | SENTINEL + rate-capped trigger |  30 |          2.865 |     837.4   |            0.727 |               0.957 |           0.482 |        4.433 |                0.761 |                4.47  |       1.289 |         1.318 |
|   5 | SENTINEL + state-aware trigger |  30 |          2.865 |     837.4   |            0.727 |               0.957 |           0.482 |        4.433 |                0.761 |                4.47  |       1.289 |         1.318 |
|  10 | AoII threshold (state-aware)   |  30 |          2.71  |    1214.37  |            0.714 |               0.956 |           0.996 |        2.883 |                0.976 |              nan     |       0.861 |         2.136 |
|  10 | Nominal (non-robust) SENTINEL  |  30 |          2.281 |     824.433 |            0.841 |               0.231 |           3.848 |        5.425 |                0.77  |                4.483 |       0.961 |         1.155 |
|  10 | Random                         |  30 |          6.724 |     426.167 |            0.55  |               0.386 |           1.101 |        3.359 |                0.877 |              nan     |       0.304 |         6.704 |
|  10 | SENTINEL (robust)              |  30 |          2.211 |     900.133 |            0.846 |               0.231 |           3.856 |        5.1   |                0.732 |                4.278 |       0.737 |         1.499 |
|  10 | SENTINEL + rate-capped trigger |  30 |          2.028 |     882.933 |            0.737 |               0.955 |           1.001 |        4.608 |                0.725 |                4.278 |       0.718 |         1.475 |
|  10 | SENTINEL + state-aware trigger |  30 |          2.028 |     882.933 |            0.737 |               0.955 |           1.001 |        4.608 |                0.725 |                4.278 |       0.718 |         1.475 |
|  15 | AoII threshold (state-aware)   |  30 |          2.903 |    1366.7   |            0.714 |               0.955 |           1.518 |        2.994 |                0.979 |              nan     |       1.061 |         2.392 |
|  15 | Nominal (non-robust) SENTINEL  |  30 |          2.786 |    1346.07  |            0.856 |               0.234 |           5.798 |        5.733 |                0.747 |                4.404 |       0.962 |         2.414 |
|  15 | Random                         |  30 |          6.835 |     501.6   |            0.551 |               0.389 |           1.653 |        3.359 |                0.874 |              nan     |       0.342 |         6.782 |
|  15 | SENTINEL (robust)              |  30 |          2.199 |    1249.83  |            0.87  |               0.234 |           5.821 |        5.407 |                0.722 |                4.256 |       0.856 |         1.56  |
|  15 | SENTINEL + rate-capped trigger |  30 |          2.043 |    1228.33  |            0.765 |               0.955 |           1.531 |        4.695 |                0.717 |                4.256 |       0.871 |         1.411 |
|  15 | SENTINEL + state-aware trigger |  30 |          2.043 |    1228.33  |            0.765 |               0.955 |           1.531 |        4.695 |                0.717 |                4.256 |       0.871 |         1.411 |
|  20 | AoII threshold (state-aware)   |  30 |          2.958 |    1792.17  |            0.704 |               0.955 |           2.001 |        3.066 |                0.979 |              nan     |       0.799 |         2.486 |
|  20 | Nominal (non-robust) SENTINEL  |  30 |          2.516 |    1285.1   |            0.85  |               0.232 |           7.721 |        6.197 |                0.765 |                4.466 |       0.82  |         1.895 |
|  20 | Random                         |  30 |          6.835 |     581.033 |            0.546 |               0.389 |           2.181 |        3.408 |                0.88  |              nan     |       0.199 |         6.751 |
|  20 | SENTINEL (robust)              |  30 |          2.143 |    1332.07  |            0.858 |               0.232 |           7.739 |        5.782 |                0.744 |                4.341 |       0.581 |         1.752 |
|  20 | SENTINEL + rate-capped trigger |  30 |          1.928 |    1279.23  |            0.751 |               0.955 |           2.014 |        4.754 |                0.733 |                4.341 |       0.565 |         1.553 |
|  20 | SENTINEL + state-aware trigger |  30 |          1.928 |    1279.23  |            0.751 |               0.955 |           2.014 |        4.754 |                0.733 |                4.341 |       0.565 |         1.553 |

## Validation against the exact ILP optimum of P3 (mean optimality gap %, fraction of instances solved to optimality)

### Experiment A

| label   |   Greedy |   Greedy+LS |   ILP exact |   SENTINEL (QAOA, Aer) |   SENTINEL (SA-XY, one-hot-preserving) |
|:--------|---------:|------------:|------------:|-----------------------:|---------------------------------------:|
| U=2     |        0 |           0 |           0 |                   0    |                                   0    |
| U=3     |        0 |           0 |           0 |                   0    |                                  76.06 |
| U=4     |        0 |           0 |           0 |                  34.22 |                                  34.22 |
| U=5     |        0 |           0 |           0 |                 225.93 |                                 233.7  |
| U=6     |        0 |           0 |           0 |                 265.64 |                                 321.07 |

Fraction optimal:

| label   |   Greedy |   Greedy+LS |   ILP exact |   SENTINEL (QAOA, Aer) |   SENTINEL (SA-XY, one-hot-preserving) |
|:--------|---------:|------------:|------------:|-----------------------:|---------------------------------------:|
| U=2     |        1 |           1 |           1 |                    1   |                                   1    |
| U=3     |        1 |           1 |           1 |                    1   |                                   0.6  |
| U=4     |        1 |           1 |           1 |                    0.5 |                                   0.5  |
| U=5     |        1 |           1 |           1 |                    0   |                                   0.25 |
| U=6     |        1 |           1 |           1 |                    0   |                                   0    |

Qubits / time / local feasibility:

| label   | solver                               |   qubits_max |   time_mean_s |   local_feasible |
|:--------|:-------------------------------------|-------------:|--------------:|-----------------:|
| U=2     | Greedy                               |            0 |         0     |              nan |
| U=2     | Greedy+LS                            |            0 |         0     |              nan |
| U=2     | ILP exact                            |            0 |         0.034 |              nan |
| U=2     | SENTINEL (QAOA, Aer)                 |           25 |       239.564 |                1 |
| U=2     | SENTINEL (SA-XY, one-hot-preserving) |           25 |         0.074 |                1 |
| U=3     | Greedy                               |            0 |         0     |              nan |
| U=3     | Greedy+LS                            |            0 |         0     |              nan |
| U=3     | ILP exact                            |            0 |         0.04  |              nan |
| U=3     | SENTINEL (QAOA, Aer)                 |           26 |       604.202 |                1 |
| U=3     | SENTINEL (SA-XY, one-hot-preserving) |           26 |         0.127 |                1 |
| U=4     | Greedy                               |            0 |         0     |              nan |
| U=4     | Greedy+LS                            |            0 |         0     |              nan |
| U=4     | ILP exact                            |            0 |         0.003 |              nan |
| U=4     | SENTINEL (QAOA, Aer)                 |           22 |       119.994 |                1 |
| U=4     | SENTINEL (SA-XY, one-hot-preserving) |           22 |         0.286 |                1 |
| U=5     | Greedy                               |            0 |         0     |              nan |
| U=5     | Greedy+LS                            |            0 |         0     |              nan |
| U=5     | ILP exact                            |            0 |         0.003 |              nan |
| U=5     | SENTINEL (QAOA, Aer)                 |           24 |       345.7   |                1 |
| U=5     | SENTINEL (SA-XY, one-hot-preserving) |           24 |         0.299 |                1 |
| U=6     | Greedy                               |            0 |         0     |              nan |
| U=6     | Greedy+LS                            |            0 |         0.001 |              nan |
| U=6     | ILP exact                            |            0 |         0.004 |              nan |
| U=6     | SENTINEL (QAOA, Aer)                 |           25 |       395.698 |                1 |
| U=6     | SENTINEL (SA-XY, one-hot-preserving) |           25 |         0.303 |                1 |

### Experiment B

| label   |   Greedy |   Greedy+LS |   ILP exact |   SA (monolithic QUBO) |   SENTINEL (SA on penalty QUBO) |   SENTINEL (SA-XY) + LS polish |   SENTINEL (SA-XY, one-hot-preserving) |
|:--------|---------:|------------:|------------:|-----------------------:|--------------------------------:|-------------------------------:|---------------------------------------:|
| U=10    |     0    |        0    |           0 |                   8    |                            1.43 |                           0    |                                   0.04 |
| U=100   |    20    |       11.47 |           0 |                 126.17 |                          167.41 |                          60.8  |                                 292.4  |
| U=25    |     0    |        0    |           0 |                  10.49 |                            2.93 |                           0    |                                   2.34 |
| U=50    |    18.23 |        5.95 |           0 |                  31.83 |                           33.22 |                           4.63 |                                  28.58 |
| U=75    |    15.82 |       14.38 |           0 |                 113.03 |                          132.83 |                          71.48 |                                 237.34 |

Fraction optimal:

| label   |   Greedy |   Greedy+LS |   ILP exact |   SA (monolithic QUBO) |   SENTINEL (SA on penalty QUBO) |   SENTINEL (SA-XY) + LS polish |   SENTINEL (SA-XY, one-hot-preserving) |
|:--------|---------:|------------:|------------:|-----------------------:|--------------------------------:|-------------------------------:|---------------------------------------:|
| U=10    |      1   |         1   |           1 |                    0.1 |                             0.6 |                            1   |                                    0.9 |
| U=100   |      0   |         0   |           1 |                    0   |                             0   |                            0   |                                    0   |
| U=25    |      1   |         1   |           1 |                    0   |                             0.1 |                            1   |                                    0   |
| U=50    |      0.3 |         0.3 |           1 |                    0   |                             0   |                            0.1 |                                    0   |
| U=75    |      0   |         0   |           1 |                    0   |                             0   |                            0   |                                    0   |

Qubits / time / local feasibility:

| label   | solver                               |   qubits_max |   time_mean_s |   local_feasible |
|:--------|:-------------------------------------|-------------:|--------------:|-----------------:|
| U=10    | Greedy                               |            0 |         0     |              nan |
| U=10    | Greedy+LS                            |            0 |         0.005 |              nan |
| U=10    | ILP exact                            |            0 |         0.008 |              nan |
| U=10    | SA (monolithic QUBO)                 |          276 |         0.577 |                0 |
| U=10    | SENTINEL (SA on penalty QUBO)        |          213 |         5.778 |                0 |
| U=10    | SENTINEL (SA-XY) + LS polish         |          213 |         1.295 |                1 |
| U=10    | SENTINEL (SA-XY, one-hot-preserving) |          213 |         1.315 |                1 |
| U=100   | Greedy                               |            0 |         0     |              nan |
| U=100   | Greedy+LS                            |            0 |         0.875 |              nan |
| U=100   | ILP exact                            |            0 |        30.119 |              nan |
| U=100   | SA (monolithic QUBO)                 |         5407 |        28.985 |                0 |
| U=100   | SENTINEL (SA on penalty QUBO)        |         3460 |       235.075 |                0 |
| U=100   | SENTINEL (SA-XY) + LS polish         |         3460 |        72.025 |                1 |
| U=100   | SENTINEL (SA-XY, one-hot-preserving) |         3460 |        71.62  |                1 |
| U=25    | Greedy                               |            0 |         0     |              nan |
| U=25    | Greedy+LS                            |            0 |         0.018 |              nan |
| U=25    | ILP exact                            |            0 |         0.017 |              nan |
| U=25    | SA (monolithic QUBO)                 |          549 |         1.028 |                0 |
| U=25    | SENTINEL (SA on penalty QUBO)        |          353 |        15.539 |                0 |
| U=25    | SENTINEL (SA-XY) + LS polish         |          353 |         1.108 |                1 |
| U=25    | SENTINEL (SA-XY, one-hot-preserving) |          353 |         1.064 |                1 |
| U=50    | Greedy                               |            0 |         0     |              nan |
| U=50    | Greedy+LS                            |            0 |         0.192 |              nan |
| U=50    | ILP exact                            |            0 |         0.13  |              nan |
| U=50    | SA (monolithic QUBO)                 |         1581 |         5.022 |                0 |
| U=50    | SENTINEL (SA on penalty QUBO)        |         1008 |        80.41  |                0 |
| U=50    | SENTINEL (SA-XY) + LS polish         |         1008 |         5.504 |                1 |
| U=50    | SENTINEL (SA-XY, one-hot-preserving) |         1008 |         4.402 |                1 |
| U=75    | Greedy                               |            0 |         0     |              nan |
| U=75    | Greedy+LS                            |            0 |         0.483 |              nan |
| U=75    | ILP exact                            |            0 |         0.155 |              nan |
| U=75    | SA (monolithic QUBO)                 |         3211 |        16.512 |                0 |
| U=75    | SENTINEL (SA on penalty QUBO)        |         1925 |       156.732 |                0 |
| U=75    | SENTINEL (SA-XY) + LS polish         |         1925 |        43.873 |                1 |
| U=75    | SENTINEL (SA-XY, one-hot-preserving) |         1925 |        44.99  |                1 |

### Experiment C

| label    |   Greedy |   Greedy+LS |   ILP exact |   SA (monolithic QUBO) |   SENTINEL (SA on penalty QUBO) |   SENTINEL (SA-XY) + LS polish |   SENTINEL (SA-XY, one-hot-preserving) |
|:---------|---------:|------------:|------------:|-----------------------:|--------------------------------:|-------------------------------:|---------------------------------------:|
| extreme  |        0 |           0 |           0 |                   0.51 |                            0.74 |                              0 |                                   0.15 |
| mild     |        0 |           0 |           0 |                  15.26 |                            2.89 |                              0 |                                   3.14 |
| moderate |        0 |           0 |           0 |                   7.63 |                            3.69 |                              0 |                                   1.13 |
| severe   |        0 |           0 |           0 |                   1.05 |                            0.67 |                              0 |                                   0.37 |

Fraction optimal:

| label    |   Greedy |   Greedy+LS |   ILP exact |   SA (monolithic QUBO) |   SENTINEL (SA on penalty QUBO) |   SENTINEL (SA-XY) + LS polish |   SENTINEL (SA-XY, one-hot-preserving) |
|:---------|---------:|------------:|------------:|-----------------------:|--------------------------------:|-------------------------------:|---------------------------------------:|
| extreme  |        1 |           1 |           1 |                    0.6 |                             0.5 |                              1 |                                    0.4 |
| mild     |        1 |           1 |           1 |                    0   |                             0.4 |                              1 |                                    0.1 |
| moderate |        1 |           1 |           1 |                    0   |                             0.1 |                              1 |                                    0.1 |
| severe   |        1 |           1 |           1 |                    0.3 |                             0.1 |                              1 |                                    0.4 |

Qubits / time / local feasibility:

| label    | solver                               |   qubits_max |   time_mean_s |   local_feasible |
|:---------|:-------------------------------------|-------------:|--------------:|-----------------:|
| extreme  | Greedy                               |            0 |         0     |              nan |
| extreme  | Greedy+LS                            |            0 |         0.001 |              nan |
| extreme  | ILP exact                            |            0 |         0.002 |              nan |
| extreme  | SA (monolithic QUBO)                 |          153 |         0.153 |                0 |
| extreme  | SENTINEL (SA on penalty QUBO)        |          111 |         0.404 |                0 |
| extreme  | SENTINEL (SA-XY) + LS polish         |          111 |         0.183 |                1 |
| extreme  | SENTINEL (SA-XY, one-hot-preserving) |          111 |         0.2   |                1 |
| mild     | Greedy                               |            0 |         0     |              nan |
| mild     | Greedy+LS                            |            0 |         0.008 |              nan |
| mild     | ILP exact                            |            0 |         0.006 |              nan |
| mild     | SA (monolithic QUBO)                 |          504 |         0.483 |                0 |
| mild     | SENTINEL (SA on penalty QUBO)        |          338 |         6.433 |                0 |
| mild     | SENTINEL (SA-XY) + LS polish         |          338 |         0.558 |                1 |
| mild     | SENTINEL (SA-XY, one-hot-preserving) |          338 |         0.54  |                1 |
| moderate | Greedy                               |            0 |         0     |              nan |
| moderate | Greedy+LS                            |            0 |         0.005 |              nan |
| moderate | ILP exact                            |            0 |         0.007 |              nan |
| moderate | SA (monolithic QUBO)                 |          443 |         0.433 |                0 |
| moderate | SENTINEL (SA on penalty QUBO)        |          284 |         5.824 |                0 |
| moderate | SENTINEL (SA-XY) + LS polish         |          284 |         0.621 |                1 |
| moderate | SENTINEL (SA-XY, one-hot-preserving) |          284 |         0.556 |                1 |
| severe   | Greedy                               |            0 |         0     |              nan |
| severe   | Greedy+LS                            |            0 |         0.001 |              nan |
| severe   | ILP exact                            |            0 |         0.003 |              nan |
| severe   | SA (monolithic QUBO)                 |          221 |         0.21  |                0 |
| severe   | SENTINEL (SA on penalty QUBO)        |          135 |         2.65  |                0 |
| severe   | SENTINEL (SA-XY) + LS polish         |          135 |         0.452 |                1 |
| severe   | SENTINEL (SA-XY, one-hot-preserving) |          135 |         0.433 |                1 |

### Experiment D

| label   |   Greedy |   Greedy+LS |   ILP exact |   SA (monolithic QUBO) |   SENTINEL (SA on penalty QUBO) |   SENTINEL (SA-XY) + LS polish |   SENTINEL (SA-XY, one-hot-preserving) |
|:--------|---------:|------------:|------------:|-----------------------:|--------------------------------:|-------------------------------:|---------------------------------------:|
| L=1     |     0    |        0    |           0 |                 606.69 |                          134.4  |                          -0    |                                  93.27 |
| L=3     |     0    |        0    |           0 |                 184.86 |                           12.51 |                           0    |                                  61.12 |
| L=5     |    17.78 |        1.13 |           0 |                  23.55 |                            4.66 |                           1.39 |                                   3.9  |
| L=6     |     0    |        0    |           0 |                   7.63 |                            3.69 |                           0    |                                   1.13 |

Fraction optimal:

| label   |   Greedy |   Greedy+LS |   ILP exact |   SA (monolithic QUBO) |   SENTINEL (SA on penalty QUBO) |   SENTINEL (SA-XY) + LS polish |   SENTINEL (SA-XY, one-hot-preserving) |
|:--------|---------:|------------:|------------:|-----------------------:|--------------------------------:|-------------------------------:|---------------------------------------:|
| L=1     |      1   |         1   |           1 |                      0 |                             0   |                            1   |                                    0   |
| L=3     |      1   |         1   |           1 |                      0 |                             0.3 |                            1   |                                    0.1 |
| L=5     |      0.6 |         0.6 |           1 |                      0 |                             0.1 |                            0.6 |                                    0.1 |
| L=6     |      1   |         1   |           1 |                      0 |                             0.1 |                            1   |                                    0.1 |

Qubits / time / local feasibility:

| label   | solver                               |   qubits_max |   time_mean_s |   local_feasible |
|:--------|:-------------------------------------|-------------:|--------------:|-----------------:|
| L=1     | Greedy                               |            0 |         0     |          nan     |
| L=1     | Greedy+LS                            |            0 |         0.005 |          nan     |
| L=1     | ILP exact                            |            0 |         0.005 |          nan     |
| L=1     | SA (monolithic QUBO)                 |          520 |         0.629 |            0     |
| L=1     | SENTINEL (SA on penalty QUBO)        |          333 |         7.324 |            0.047 |
| L=1     | SENTINEL (SA-XY) + LS polish         |          333 |         0.436 |            1     |
| L=1     | SENTINEL (SA-XY, one-hot-preserving) |          333 |         0.409 |            1     |
| L=3     | Greedy                               |            0 |         0     |          nan     |
| L=3     | Greedy+LS                            |            0 |         0.006 |          nan     |
| L=3     | ILP exact                            |            0 |         0.006 |          nan     |
| L=3     | SA (monolithic QUBO)                 |          476 |         0.44  |            0     |
| L=3     | SENTINEL (SA on penalty QUBO)        |          291 |         5.372 |            0     |
| L=3     | SENTINEL (SA-XY) + LS polish         |          291 |         1.019 |            1     |
| L=3     | SENTINEL (SA-XY, one-hot-preserving) |          291 |         1.024 |            1     |
| L=5     | Greedy                               |            0 |         0     |          nan     |
| L=5     | Greedy+LS                            |            0 |         0.009 |          nan     |
| L=5     | ILP exact                            |            0 |         0.024 |          nan     |
| L=5     | SA (monolithic QUBO)                 |          459 |         0.427 |            0     |
| L=5     | SENTINEL (SA on penalty QUBO)        |          295 |         6.324 |            0     |
| L=5     | SENTINEL (SA-XY) + LS polish         |          295 |         0.696 |            1     |
| L=5     | SENTINEL (SA-XY, one-hot-preserving) |          295 |         0.72  |            1     |
| L=6     | Greedy                               |            0 |         0     |          nan     |
| L=6     | Greedy+LS                            |            0 |         0.006 |          nan     |
| L=6     | ILP exact                            |            0 |         0.006 |          nan     |
| L=6     | SA (monolithic QUBO)                 |          443 |         0.432 |            0     |
| L=6     | SENTINEL (SA on penalty QUBO)        |          284 |         5.725 |            0     |
| L=6     | SENTINEL (SA-XY) + LS polish         |          284 |         0.567 |            1     |
| L=6     | SENTINEL (SA-XY, one-hot-preserving) |          284 |         0.552 |            1     |
