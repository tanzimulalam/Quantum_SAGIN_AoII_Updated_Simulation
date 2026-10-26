# Regenerated results tables

## Certificate validity (fraction of epochs with realized avg AoII <= certified worst case)

| policy   |   certificate_holds |
|:---------|--------------------:|
| nominal  |            0.980915 |
| sentinel |            0.980425 |

## topology, disruption on

| x                         | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|:--------------------------|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
| Ground only (2 BS)        | AoII threshold (state-aware)   |  30 |         77.223 |    3722.27  |            0.042 |               0.962 |           0.351 |        6.133 |                0     |              nan     |      18.754 |        60.606 |
| Ground only (2 BS)        | Nominal (non-robust) SENTINEL  |  30 |         89.264 |    4257.57  |            0.078 |               0.244 |           1.081 |        6.076 |                0     |                0.212 |      18.671 |        78.003 |
| Ground only (2 BS)        | Random                         |  30 |         87.605 |    3989.07  |            0.139 |               0.448 |           0.278 |        5.306 |                0     |              nan     |      19.328 |        68.758 |
| Ground only (2 BS)        | SENTINEL (robust)              |  30 |         89.264 |    4257.57  |            0.078 |               0.244 |           1.081 |        6.076 |                0     |                0.212 |      18.671 |        78.003 |
| Ground only (2 BS)        | SENTINEL + rate-capped trigger |  30 |         89.223 |    4257.57  |            0.033 |               0.931 |           0.294 |        6.084 |                0     |                0.212 |      18.674 |        77.96  |
| Ground only (2 BS)        | SENTINEL + state-aware trigger |  30 |         89.223 |    4257.57  |            0.033 |               0.931 |           0.294 |        6.084 |                0     |                0.212 |      18.674 |        77.96  |
| Integrated (1 BS + 1 SAT) | AoII threshold (state-aware)   |  30 |          4.299 |    1591.4   |            0.627 |               0.955 |           0.984 |        5.229 |                0.969 |              nan     |       1.004 |         3.851 |
| Integrated (1 BS + 1 SAT) | Nominal (non-robust) SENTINEL  |  30 |          4.529 |    1596.97  |            0.78  |               0.232 |           3.779 |        7.58  |                0.895 |                4.958 |       1.154 |         4.102 |
| Integrated (1 BS + 1 SAT) | Random                         |  30 |         11.297 |    1973.93  |            0.538 |               0.384 |           1.076 |        5.296 |                0.885 |              nan     |       1.835 |        10.119 |
| Integrated (1 BS + 1 SAT) | SENTINEL (robust)              |  30 |          4.496 |    1596.97  |            0.781 |               0.232 |           3.779 |        7.358 |                0.877 |                4.864 |       1.11  |         4.101 |
| Integrated (1 BS + 1 SAT) | SENTINEL + rate-capped trigger |  30 |          4.279 |    1587     |            0.618 |               0.955 |           0.982 |        6.547 |                0.872 |                4.864 |       0.987 |         3.832 |
| Integrated (1 BS + 1 SAT) | SENTINEL + state-aware trigger |  30 |          4.279 |    1587     |            0.618 |               0.955 |           0.982 |        6.547 |                0.872 |                4.864 |       0.987 |         3.832 |
| Integrated (2 BS + 2 SAT) | AoII threshold (state-aware)   |  30 |          0.689 |     324.833 |            0.919 |               0.955 |           1.024 |        4.432 |                0.944 |              nan     |       0.946 |         0.141 |
| Integrated (2 BS + 2 SAT) | Nominal (non-robust) SENTINEL  |  30 |          0.511 |     221.9   |            0.912 |               0.232 |           3.923 |        7.235 |                0.781 |                4.517 |       0.364 |         0.282 |
| Integrated (2 BS + 2 SAT) | Random                         |  30 |          7.221 |     640.4   |            0.549 |               0.387 |           1.097 |        5.278 |                0.873 |              nan     |       0.962 |         6.813 |
| Integrated (2 BS + 2 SAT) | SENTINEL (robust)              |  30 |          0.502 |     219.067 |            0.918 |               0.232 |           3.928 |        6.49  |                0.735 |                4.265 |       0.365 |         0.265 |
| Integrated (2 BS + 2 SAT) | SENTINEL + rate-capped trigger |  30 |          0.703 |     324.167 |            0.897 |               0.956 |           1.022 |        5.971 |                0.728 |                4.265 |       0.962 |         0.145 |
| Integrated (2 BS + 2 SAT) | SENTINEL + state-aware trigger |  30 |          0.703 |     324.167 |            0.897 |               0.956 |           1.022 |        5.971 |                0.728 |                4.265 |       0.962 |         0.145 |
| Integrated (3 BS + 3 SAT) | AoII threshold (state-aware)   |  30 |          0.136 |      71.5   |            0.941 |               0.956 |           1.027 |        3.957 |                0.952 |              nan     |       0.008 |         0.139 |
| Integrated (3 BS + 3 SAT) | Nominal (non-robust) SENTINEL  |  30 |          0.266 |      82.067 |            0.91  |               0.232 |           3.921 |        6.997 |                0.71  |                3.735 |       0.012 |         0.261 |
| Integrated (3 BS + 3 SAT) | Random                         |  30 |          6.549 |     421.3   |            0.542 |               0.389 |           1.084 |        5.248 |                0.881 |              nan     |       0.211 |         6.532 |
| Integrated (3 BS + 3 SAT) | SENTINEL (robust)              |  30 |          0.253 |      74.933 |            0.919 |               0.232 |           3.929 |        5.894 |                0.644 |                2.926 |       0.012 |         0.251 |
| Integrated (3 BS + 3 SAT) | SENTINEL + rate-capped trigger |  30 |          0.14  |      71.733 |            0.906 |               0.955 |           1.022 |        5.634 |                0.647 |                2.926 |       0.008 |         0.142 |
| Integrated (3 BS + 3 SAT) | SENTINEL + state-aware trigger |  30 |          0.14  |      71.733 |            0.906 |               0.955 |           1.022 |        5.634 |                0.647 |                2.926 |       0.008 |         0.142 |
| Satellite only (2 SAT)    | AoII threshold (state-aware)   |  30 |          0.236 |     149.633 |            0.918 |               0.956 |           1.024 |        4.656 |                1     |              nan     |       0.113 |         0.154 |
| Satellite only (2 SAT)    | Nominal (non-robust) SENTINEL  |  30 |          0.356 |     151.9   |            0.93  |               0.231 |           3.94  |        7.95  |                1     |                5.771 |       0.092 |         0.289 |
| Satellite only (2 SAT)    | Random                         |  30 |          2.781 |     263.2   |            0.985 |               0.3   |           1.971 |        5.443 |                1     |              nan     |       0.121 |         2.786 |
| Satellite only (2 SAT)    | SENTINEL (robust)              |  30 |          0.348 |     147.867 |            0.937 |               0.231 |           3.946 |        7.226 |                1     |                5.771 |       0.092 |         0.28  |
| Satellite only (2 SAT)    | SENTINEL + rate-capped trigger |  30 |          0.245 |     152.2   |            0.906 |               0.956 |           1.023 |        6.331 |                1     |                5.771 |       0.114 |         0.16  |
| Satellite only (2 SAT)    | SENTINEL + state-aware trigger |  30 |          0.245 |     152.2   |            0.906 |               0.956 |           1.023 |        6.331 |                1     |                5.771 |       0.114 |         0.16  |

## ue_sweep, disruption off

|   x | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   5 | AoII threshold (state-aware)   |  30 |          0.357 |     153.8   |            0.969 |               0.957 |           0.496 |        4.38  |                0.942 |              nan     |       0.326 |         0.103 |
|   5 | Nominal (non-robust) SENTINEL  |  30 |          0.588 |     167.567 |            0.969 |               0.223 |           1.986 |        6.948 |                0.856 |                4.795 |       0.5   |         0.215 |
|   5 | Random                         |  30 |          7.025 |     464.767 |            0.539 |               0.386 |           0.539 |        5.223 |                0.899 |              nan     |       0.627 |         6.767 |
|   5 | SENTINEL (robust)              |  30 |          0.588 |     168.1   |            0.968 |               0.223 |           1.986 |        6.248 |                0.795 |                4.449 |       0.5   |         0.215 |
|   5 | SENTINEL + rate-capped trigger |  30 |          0.481 |     164.533 |            0.95  |               0.957 |           0.495 |        5.876 |                0.767 |                4.449 |       0.5   |         0.106 |
|   5 | SENTINEL + state-aware trigger |  30 |          0.481 |     164.533 |            0.95  |               0.957 |           0.495 |        5.876 |                0.767 |                4.449 |       0.5   |         0.106 |
|  10 | AoII threshold (state-aware)   |  30 |          0.652 |     270.933 |            0.982 |               0.955 |           1.031 |        4.381 |                0.944 |              nan     |       0.946 |         0.103 |
|  10 | Nominal (non-robust) SENTINEL  |  30 |          0.458 |     162     |            0.962 |               0.231 |           3.967 |        7.378 |                0.783 |                4.517 |       0.365 |         0.214 |
|  10 | Random                         |  30 |          7.087 |     621.433 |            0.555 |               0.386 |           1.111 |        5.252 |                0.874 |              nan     |       0.965 |         6.657 |
|  10 | SENTINEL (robust)              |  30 |          0.459 |     161.667 |            0.959 |               0.231 |           3.964 |        6.635 |                0.737 |                4.265 |       0.365 |         0.214 |
|  10 | SENTINEL + rate-capped trigger |  30 |          0.667 |     271.933 |            0.952 |               0.955 |           1.028 |        5.942 |                0.729 |                4.265 |       0.963 |         0.107 |
|  10 | SENTINEL + state-aware trigger |  30 |          0.667 |     271.933 |            0.952 |               0.955 |           1.028 |        5.942 |                0.729 |                4.265 |       0.963 |         0.107 |
|  15 | AoII threshold (state-aware)   |  30 |          0.57  |     363.767 |            0.962 |               0.955 |           1.566 |        4.512 |                0.955 |              nan     |       0.465 |         0.108 |
|  15 | Nominal (non-robust) SENTINEL  |  30 |          0.715 |     368.933 |            0.957 |               0.234 |           5.945 |        7.651 |                0.754 |                4.393 |       0.481 |         0.225 |
|  15 | Random                         |  30 |          6.983 |     684.633 |            0.555 |               0.389 |           1.664 |        5.243 |                0.87  |              nan     |       0.443 |         6.655 |
|  15 | SENTINEL (robust)              |  30 |          0.715 |     368.8   |            0.957 |               0.234 |           5.944 |        7.014 |                0.727 |                4.234 |       0.481 |         0.225 |
|  15 | SENTINEL + rate-capped trigger |  30 |          0.601 |     366.467 |            0.931 |               0.955 |           1.561 |        6.05  |                0.721 |                4.234 |       0.482 |         0.115 |
|  15 | SENTINEL + state-aware trigger |  30 |          0.601 |     366.467 |            0.931 |               0.955 |           1.561 |        6.05  |                0.721 |                4.234 |       0.482 |         0.115 |
|  20 | AoII threshold (state-aware)   |  30 |          0.499 |     266.767 |            0.958 |               0.955 |           2.064 |        4.529 |                0.949 |              nan     |       0.411 |         0.109 |
|  20 | Nominal (non-robust) SENTINEL  |  30 |          0.663 |     335.6   |            0.953 |               0.232 |           7.917 |        8.26  |                0.77  |                4.44  |       0.432 |         0.225 |
|  20 | Random                         |  30 |          7.094 |     766.967 |            0.549 |               0.389 |           2.194 |        5.323 |                0.876 |              nan     |       0.483 |         6.682 |
|  20 | SENTINEL (robust)              |  30 |          0.663 |     335.667 |            0.952 |               0.232 |           7.916 |        7.505 |                0.75  |                4.316 |       0.432 |         0.225 |
|  20 | SENTINEL + rate-capped trigger |  30 |          0.581 |     335.133 |            0.926 |               0.955 |           2.056 |        6.107 |                0.738 |                4.316 |       0.464 |         0.117 |
|  20 | SENTINEL + state-aware trigger |  30 |          0.581 |     335.133 |            0.926 |               0.955 |           2.056 |        6.107 |                0.738 |                4.316 |       0.464 |         0.117 |

## ue_sweep, disruption on

|   x | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   5 | AoII threshold (state-aware)   |  30 |          0.394 |     195.333 |            0.906 |               0.957 |           0.493 |        4.429 |                0.941 |              nan     |       0.327 |         0.138 |
|   5 | Nominal (non-robust) SENTINEL  |  30 |          0.645 |     220.8   |            0.916 |               0.223 |           1.963 |        6.911 |                0.854 |                4.795 |       0.499 |         0.279 |
|   5 | Random                         |  30 |          7.163 |     473.967 |            0.532 |               0.387 |           0.532 |        5.252 |                0.898 |              nan     |       0.635 |         6.932 |
|   5 | SENTINEL (robust)              |  30 |          0.637 |     214.933 |            0.923 |               0.223 |           1.966 |        6.203 |                0.793 |                4.449 |       0.5   |         0.268 |
|   5 | SENTINEL + rate-capped trigger |  30 |          0.52  |     205.8   |            0.89  |               0.957 |           0.492 |        5.906 |                0.766 |                4.449 |       0.5   |         0.149 |
|   5 | SENTINEL + state-aware trigger |  30 |          0.52  |     205.8   |            0.89  |               0.957 |           0.492 |        5.906 |                0.766 |                4.449 |       0.5   |         0.149 |
|  10 | AoII threshold (state-aware)   |  30 |          0.689 |     324.833 |            0.919 |               0.955 |           1.024 |        4.432 |                0.944 |              nan     |       0.946 |         0.141 |
|  10 | Nominal (non-robust) SENTINEL  |  30 |          0.511 |     221.9   |            0.912 |               0.232 |           3.923 |        7.235 |                0.781 |                4.517 |       0.364 |         0.282 |
|  10 | Random                         |  30 |          7.221 |     640.4   |            0.549 |               0.387 |           1.097 |        5.278 |                0.873 |              nan     |       0.962 |         6.813 |
|  10 | SENTINEL (robust)              |  30 |          0.502 |     219.067 |            0.918 |               0.232 |           3.928 |        6.49  |                0.735 |                4.265 |       0.365 |         0.265 |
|  10 | SENTINEL + rate-capped trigger |  30 |          0.703 |     324.167 |            0.897 |               0.956 |           1.022 |        5.971 |                0.728 |                4.265 |       0.962 |         0.145 |
|  10 | SENTINEL + state-aware trigger |  30 |          0.703 |     324.167 |            0.897 |               0.956 |           1.022 |        5.971 |                0.728 |                4.265 |       0.962 |         0.145 |
|  15 | AoII threshold (state-aware)   |  30 |          0.608 |     415.633 |            0.901 |               0.955 |           1.557 |        4.566 |                0.955 |              nan     |       0.467 |         0.145 |
|  15 | Nominal (non-robust) SENTINEL  |  30 |          0.764 |     425.933 |            0.913 |               0.235 |           5.886 |        7.381 |                0.752 |                4.393 |       0.482 |         0.27  |
|  15 | Random                         |  30 |          7.112 |     685.133 |            0.549 |               0.39  |           1.645 |        5.27  |                0.869 |              nan     |       0.445 |         6.797 |
|  15 | SENTINEL (robust)              |  30 |          0.758 |     420.9   |            0.918 |               0.235 |           5.892 |        6.753 |                0.725 |                4.234 |       0.483 |         0.261 |
|  15 | SENTINEL + rate-capped trigger |  30 |          0.638 |     418.833 |            0.879 |               0.955 |           1.552 |        6.078 |                0.72  |                4.234 |       0.484 |         0.147 |
|  15 | SENTINEL + state-aware trigger |  30 |          0.638 |     418.833 |            0.879 |               0.955 |           1.552 |        6.078 |                0.72  |                4.234 |       0.484 |         0.147 |
|  20 | AoII threshold (state-aware)   |  30 |          0.535 |     318.4   |            0.899 |               0.955 |           2.051 |        4.585 |                0.948 |              nan     |       0.412 |         0.145 |
|  20 | Nominal (non-robust) SENTINEL  |  30 |          0.709 |     394.867 |            0.907 |               0.232 |           7.835 |        7.863 |                0.768 |                4.44  |       0.43  |         0.269 |
|  20 | Random                         |  30 |          7.23  |     761.167 |            0.542 |               0.39  |           2.169 |        5.349 |                0.875 |              nan     |       0.485 |         6.804 |
|  20 | SENTINEL (robust)              |  30 |          0.702 |     389.867 |            0.912 |               0.232 |           7.844 |        7.147 |                0.747 |                4.316 |       0.431 |         0.265 |
|  20 | SENTINEL + rate-capped trigger |  30 |          0.618 |     385.033 |            0.873 |               0.955 |           2.044 |        6.137 |                0.736 |                4.316 |       0.467 |         0.149 |
|  20 | SENTINEL + state-aware trigger |  30 |          0.618 |     385.033 |            0.873 |               0.955 |           2.044 |        6.137 |                0.736 |                4.316 |       0.467 |         0.149 |

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
