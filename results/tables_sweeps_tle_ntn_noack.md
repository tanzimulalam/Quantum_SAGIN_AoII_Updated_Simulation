# Regenerated results tables

## Certificate validity (fraction of epochs with realized avg AoII <= certified worst case)

| policy   |   certificate_holds |
|:---------|--------------------:|
| nominal  |            0.880993 |
| sentinel |            0.890043 |

## scenario_set, disruption on

|   x | policy            |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   1 | SENTINEL (robust) |  30 |          2.281 |     824.433 |            0.841 |               0.231 |           3.848 |        5.425 |                0.77  |                4.483 |       0.961 |         1.155 |
|   2 | SENTINEL (robust) |  30 |          2.281 |     824.433 |            0.841 |               0.231 |           3.848 |        5.425 |                0.77  |                4.483 |       0.961 |         1.155 |
|   3 | SENTINEL (robust) |  30 |          2.243 |     958.933 |            0.843 |               0.231 |           3.852 |        5.183 |                0.775 |                4.508 |       0.754 |         1.882 |
|   4 | SENTINEL (robust) |  30 |          2.634 |    1088.57  |            0.848 |               0.231 |           3.856 |        5.196 |                0.787 |                4.573 |       0.813 |         2.29  |
|   5 | SENTINEL (robust) |  30 |          2.065 |     837.367 |            0.842 |               0.231 |           3.851 |        5.028 |                0.732 |                4.278 |       0.733 |         1.474 |
|   6 | SENTINEL (robust) |  30 |          2.211 |     900.133 |            0.846 |               0.231 |           3.856 |        5.1   |                0.732 |                4.278 |       0.737 |         1.499 |

## ue_sweep, disruption off

|   x | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   5 | AoII threshold (state-aware)   |  60 |          2.466 |     679.15  |            0.777 |               0.957 |           0.496 |        2.761 |                0.982 |              nan     |       0.947 |         0.947 |
|   5 | Nominal (non-robust) SENTINEL  |  60 |          2.732 |     819.583 |            0.884 |               0.228 |           1.945 |        4.993 |                0.821 |                4.723 |       0.951 |         1.155 |
|   5 | Random                         |  60 |          6.636 |     397.283 |            0.55  |               0.386 |           0.55  |        3.272 |                0.888 |              nan     |       0.244 |         6.579 |
|   5 | SENTINEL (robust)              |  60 |          2.698 |     752.45  |            0.883 |               0.228 |           1.945 |        4.712 |                0.748 |                4.318 |       1.127 |         0.986 |
|   5 | SENTINEL + rate-capped trigger |  60 |          2.703 |     766     |            0.78  |               0.957 |           0.497 |        4.487 |                0.73  |                4.318 |       1.147 |         0.89  |
|   5 | SENTINEL + state-aware trigger |  60 |          2.703 |     766     |            0.78  |               0.957 |           0.497 |        4.487 |                0.73  |                4.318 |       1.147 |         0.89  |
|  10 | AoII threshold (state-aware)   |  60 |          2.504 |    1140.22  |            0.755 |               0.956 |           0.999 |        2.827 |                0.984 |              nan     |       0.602 |         1.701 |
|  10 | Nominal (non-robust) SENTINEL  |  60 |          2.338 |     965.283 |            0.867 |               0.23  |           3.875 |        5.507 |                0.776 |                4.507 |       0.686 |         1.006 |
|  10 | Random                         |  60 |          6.672 |     437.633 |            0.552 |               0.386 |           1.104 |        3.32  |                0.881 |              nan     |       0.188 |         6.669 |
|  10 | SENTINEL (robust)              |  60 |          2.324 |    1104.97  |            0.87  |               0.23  |           3.88  |        5.164 |                0.738 |                4.3   |       0.56  |         1.674 |
|  10 | SENTINEL + rate-capped trigger |  60 |          2.201 |    1115.52  |            0.762 |               0.956 |           1     |        4.612 |                0.731 |                4.3   |       0.562 |         1.559 |
|  10 | SENTINEL + state-aware trigger |  60 |          2.201 |    1115.52  |            0.762 |               0.956 |           1     |        4.612 |                0.731 |                4.3   |       0.562 |         1.559 |
|  15 | AoII threshold (state-aware)   |  60 |          3.159 |    1552.33  |            0.736 |               0.955 |           1.504 |        2.905 |                0.984 |              nan     |       0.852 |         2.442 |
|  15 | Nominal (non-robust) SENTINEL  |  60 |          2.581 |    1304.5   |            0.869 |               0.231 |           5.818 |        5.963 |                0.756 |                4.409 |       0.595 |         2.097 |
|  15 | Random                         |  60 |          6.715 |     486.2   |            0.553 |               0.387 |           1.657 |        3.357 |                0.878 |              nan     |       0.186 |         6.697 |
|  15 | SENTINEL (robust)              |  60 |          2.242 |    1298.4   |            0.876 |               0.231 |           5.831 |        5.559 |                0.731 |                4.261 |       0.565 |         1.569 |
|  15 | SENTINEL + rate-capped trigger |  60 |          2.098 |    1287.78  |            0.77  |               0.955 |           1.509 |        4.728 |                0.726 |                4.261 |       0.572 |         1.417 |
|  15 | SENTINEL + state-aware trigger |  60 |          2.098 |    1287.78  |            0.77  |               0.955 |           1.509 |        4.728 |                0.726 |                4.261 |       0.572 |         1.417 |
|  20 | AoII threshold (state-aware)   |  60 |          2.816 |    1786.27  |            0.729 |               0.955 |           2     |        2.97  |                0.981 |              nan     |       0.483 |         2.504 |
|  20 | Nominal (non-robust) SENTINEL  |  60 |          2.452 |    1495.68  |            0.878 |               0.23  |           7.777 |        6.404 |                0.765 |                4.461 |       0.538 |         1.877 |
|  20 | Random                         |  60 |          6.681 |     542.95  |            0.55  |               0.387 |           2.202 |        3.372 |                0.88  |              nan     |       0.127 |         6.647 |
|  20 | SENTINEL (robust)              |  60 |          2.393 |    1700.93  |            0.878 |               0.231 |           7.779 |        5.921 |                0.743 |                4.332 |       0.558 |         1.712 |
|  20 | SENTINEL + rate-capped trigger |  60 |          2.23  |    1668.28  |            0.771 |               0.955 |           2.01  |        4.725 |                0.737 |                4.332 |       0.551 |         1.597 |
|  20 | SENTINEL + state-aware trigger |  60 |          2.23  |    1668.28  |            0.771 |               0.955 |           2.01  |        4.725 |                0.737 |                4.332 |       0.551 |         1.597 |

## ue_sweep, disruption on

|   x | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   5 | AoII threshold (state-aware)   |  60 |          2.485 |     681.2   |            0.75  |               0.957 |           0.494 |        2.802 |                0.981 |              nan     |       0.947 |         0.967 |
|   5 | Nominal (non-robust) SENTINEL  |  60 |          2.775 |     827.917 |            0.861 |               0.228 |           1.934 |        4.999 |                0.82  |                4.723 |       0.951 |         1.182 |
|   5 | Random                         |  60 |          6.709 |     400.533 |            0.546 |               0.387 |           0.546 |        3.312 |                0.887 |              nan     |       0.246 |         6.654 |
|   5 | SENTINEL (robust)              |  60 |          2.699 |     744.8   |            0.864 |               0.228 |           1.935 |        4.716 |                0.747 |                4.318 |       1.127 |         1.013 |
|   5 | SENTINEL + rate-capped trigger |  60 |          2.701 |     757.033 |            0.76  |               0.957 |           0.495 |        4.523 |                0.729 |                4.318 |       1.148 |         0.904 |
|   5 | SENTINEL + state-aware trigger |  60 |          2.701 |     757.033 |            0.76  |               0.957 |           0.495 |        4.523 |                0.729 |                4.318 |       1.148 |         0.904 |
|  10 | AoII threshold (state-aware)   |  60 |          2.523 |    1141.47  |            0.731 |               0.956 |           0.995 |        2.872 |                0.984 |              nan     |       0.602 |         1.721 |
|  10 | Nominal (non-robust) SENTINEL  |  60 |          2.33  |     966.883 |            0.846 |               0.23  |           3.854 |        5.451 |                0.775 |                4.507 |       0.672 |         1.119 |
|  10 | Random                         |  60 |          6.741 |     441.15  |            0.548 |               0.387 |           1.097 |        3.36  |                0.88  |              nan     |       0.19  |         6.704 |
|  10 | SENTINEL (robust)              |  60 |          2.343 |    1107.03  |            0.852 |               0.231 |           3.861 |        5.133 |                0.737 |                4.3   |       0.56  |         1.687 |
|  10 | SENTINEL + rate-capped trigger |  60 |          2.216 |    1116.98  |            0.743 |               0.956 |           0.998 |        4.649 |                0.73  |                4.3   |       0.563 |         1.571 |
|  10 | SENTINEL + state-aware trigger |  60 |          2.216 |    1116.98  |            0.743 |               0.956 |           0.998 |        4.649 |                0.73  |                4.3   |       0.563 |         1.571 |
|  15 | AoII threshold (state-aware)   |  60 |          3.178 |    1552.58  |            0.713 |               0.955 |           1.498 |        2.951 |                0.984 |              nan     |       0.852 |         2.465 |
|  15 | Nominal (non-robust) SENTINEL  |  60 |          2.627 |    1312.37  |            0.849 |               0.231 |           5.788 |        5.837 |                0.755 |                4.409 |       0.593 |         2.172 |
|  15 | Random                         |  60 |          6.785 |     486.3   |            0.549 |               0.387 |           1.647 |        3.398 |                0.878 |              nan     |       0.188 |         6.766 |
|  15 | SENTINEL (robust)              |  60 |          2.26  |    1298.95  |            0.858 |               0.231 |           5.803 |        5.49  |                0.73  |                4.261 |       0.566 |         1.583 |
|  15 | SENTINEL + rate-capped trigger |  60 |          2.112 |    1288.1   |            0.752 |               0.956 |           1.505 |        4.765 |                0.725 |                4.261 |       0.572 |         1.432 |
|  15 | SENTINEL + state-aware trigger |  60 |          2.112 |    1288.1   |            0.752 |               0.956 |           1.505 |        4.765 |                0.725 |                4.261 |       0.572 |         1.432 |
|  20 | AoII threshold (state-aware)   |  60 |          2.834 |    1786.27  |            0.708 |               0.955 |           1.992 |        3.017 |                0.981 |              nan     |       0.483 |         2.525 |
|  20 | Nominal (non-robust) SENTINEL  |  60 |          2.479 |    1499.45  |            0.857 |               0.231 |           7.735 |        6.207 |                0.763 |                4.461 |       0.539 |         1.895 |
|  20 | Random                         |  60 |          6.747 |     545.367 |            0.547 |               0.388 |           2.189 |        3.411 |                0.879 |              nan     |       0.128 |         6.725 |
|  20 | SENTINEL (robust)              |  60 |          2.413 |    1700.93  |            0.859 |               0.231 |           7.742 |        5.808 |                0.742 |                4.332 |       0.559 |         1.728 |
|  20 | SENTINEL + rate-capped trigger |  60 |          2.246 |    1668.28  |            0.752 |               0.955 |           2.004 |        4.763 |                0.737 |                4.332 |       0.551 |         1.612 |
|  20 | SENTINEL + state-aware trigger |  60 |          2.246 |    1668.28  |            0.752 |               0.955 |           2.004 |        4.763 |                0.737 |                4.332 |       0.551 |         1.612 |

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
