# Regenerated results tables

## Certificate validity (fraction of epochs with realized avg AoII <= certified worst case)

| policy   |   certificate_holds |
|:---------|--------------------:|
| nominal  |            0.985035 |
| sentinel |            0.987012 |

## capacity_limited, disruption on

|   x | policy                       |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-----------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   2 | AoII threshold (state-aware) |  30 |         38.011 |    3509.1   |            0.155 |               0.956 |           1.292 |        6.492 |                0.781 |                  nan |       9.903 |        33.454 |
|   2 | Random                       |  30 |          6.438 |     599.933 |            0.571 |               0.382 |           2.284 |        6.436 |                0.914 |                  nan |       0.227 |         6.311 |
|   2 | Whittle index (state-aware)  |  30 |          0.331 |     323.4   |            0.945 |               0.955 |           2.051 |        7.121 |                0.979 |                  nan |       0.184 |         0.161 |
|   5 | AoII threshold (state-aware) |  30 |          0.516 |     493.467 |            0.866 |               0.955 |           2.045 |        4.554 |                0.978 |                  nan |       0.237 |         0.239 |
|   5 | Random                       |  30 |          6.247 |     535.267 |            0.585 |               0.379 |           2.338 |        4.535 |                0.896 |                  nan |       0.266 |         6.108 |
|   5 | Whittle index (state-aware)  |  30 |          0.322 |     322.8   |            0.937 |               0.955 |           2.056 |        4.558 |                0.979 |                  nan |       0.184 |         0.152 |
|  10 | AoII threshold (state-aware) |  30 |          0.316 |     299.6   |            0.918 |               0.955 |           2.056 |        3.728 |                0.979 |                  nan |       0.22  |         0.152 |
|  10 | Random                       |  30 |          6.161 |     576.567 |            0.589 |               0.378 |           2.354 |        3.917 |                0.89  |                  nan |       0.223 |         6.102 |
|  10 | Whittle index (state-aware)  |  30 |          0.312 |     274.5   |            0.937 |               0.955 |           2.056 |        3.721 |                0.979 |                  nan |       0.184 |         0.148 |
|  20 | AoII threshold (state-aware) |  30 |          0.272 |     271.967 |            0.92  |               0.955 |           2.056 |        3.307 |                0.979 |                  nan |       0.146 |         0.152 |
|  20 | Random                       |  30 |          6.114 |     533.9   |            0.59  |               0.377 |           2.361 |        3.597 |                0.886 |                  nan |       0.198 |         6.052 |
|  20 | Whittle index (state-aware)  |  30 |          0.311 |     275.767 |            0.938 |               0.955 |           2.057 |        3.303 |                0.979 |                  nan |       0.184 |         0.145 |

## scenario_set, disruption on

|   x | policy            |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   1 | SENTINEL (robust) |  30 |          0.306 |     170.6   |            0.925 |               0.232 |           3.935 |        5.4   |                0.772 |                4.483 |       0.05  |         0.27  |
|   2 | SENTINEL (robust) |  30 |          0.306 |     170.6   |            0.925 |               0.232 |           3.935 |        5.4   |                0.772 |                4.483 |       0.05  |         0.27  |
|   3 | SENTINEL (robust) |  30 |          0.305 |     175.3   |            0.927 |               0.232 |           3.937 |        5.214 |                0.777 |                4.508 |       0.051 |         0.265 |
|   4 | SENTINEL (robust) |  30 |          0.305 |     177.133 |            0.929 |               0.232 |           3.939 |        5.196 |                0.794 |                4.573 |       0.05  |         0.278 |
|   5 | SENTINEL (robust) |  30 |          0.303 |     166.4   |            0.924 |               0.232 |           3.934 |        5.044 |                0.736 |                4.278 |       0.051 |         0.266 |
|   6 | SENTINEL (robust) |  30 |          0.307 |     179.367 |            0.924 |               0.232 |           3.934 |        5.112 |                0.736 |                4.278 |       0.05  |         0.269 |

## topology, disruption on

| x                         | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|:--------------------------|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
| Ground only (2 BS)        | AoII threshold (state-aware)   |  30 |         77.873 |    3768.13  |            0.042 |               0.962 |           0.349 |        6.117 |                0     |              nan     |      18.779 |        62.669 |
| Ground only (2 BS)        | Nominal (non-robust) SENTINEL  |  30 |         88.27  |    4177.3   |            0.079 |               0.265 |           1.095 |        6.209 |                0     |                0.212 |      19.17  |        73.092 |
| Ground only (2 BS)        | Random                         |  30 |         87.5   |    3898.6   |            0.178 |               0.399 |           0.355 |        5.305 |                0     |              nan     |      19.63  |        70.682 |
| Ground only (2 BS)        | SENTINEL (robust)              |  30 |         88.27  |    4177.3   |            0.079 |               0.265 |           1.095 |        6.209 |                0     |                0.212 |      19.17  |        73.092 |
| Ground only (2 BS)        | SENTINEL + rate-capped trigger |  30 |         87.016 |    4103.37  |            0.033 |               0.962 |           0.298 |        6.229 |                0     |                0.212 |      18.876 |        71.426 |
| Ground only (2 BS)        | SENTINEL + state-aware trigger |  30 |         87.016 |    4103.37  |            0.033 |               0.962 |           0.298 |        6.229 |                0     |                0.212 |      18.876 |        71.426 |
| Ground only (2 BS)        | Whittle index (state-aware)    |  30 |         94.739 |    4307.7   |            0.813 |               0.864 |           0.294 |        4.522 |                0     |              nan     |      19.718 |        81.278 |
| Integrated (1 BS + 1 SAT) | AoII threshold (state-aware)   |  30 |          2.494 |     956     |            0.719 |               0.955 |           0.998 |        3.288 |                0.978 |              nan     |       1.181 |         0.898 |
| Integrated (1 BS + 1 SAT) | Nominal (non-robust) SENTINEL  |  30 |          3.919 |    1174.6   |            0.818 |               0.231 |           3.82  |        5.726 |                0.894 |                5.17  |       1.745 |         1.912 |
| Integrated (1 BS + 1 SAT) | Random                         |  30 |          7.419 |     877.667 |            0.65  |               0.351 |           1.301 |        3.457 |                0.904 |              nan     |       0.82  |         6.829 |
| Integrated (1 BS + 1 SAT) | SENTINEL (robust)              |  30 |          3.786 |    1142.57  |            0.822 |               0.231 |           3.825 |        5.595 |                0.879 |                5.077 |       1.751 |         1.559 |
| Integrated (1 BS + 1 SAT) | SENTINEL + rate-capped trigger |  30 |          7.496 |    1917.27  |            0.561 |               0.955 |           0.972 |        4.763 |                0.871 |                5.077 |       3.095 |         5.375 |
| Integrated (1 BS + 1 SAT) | SENTINEL + state-aware trigger |  30 |          7.496 |    1917.27  |            0.561 |               0.955 |           0.972 |        4.763 |                0.871 |                5.077 |       3.095 |         5.375 |
| Integrated (1 BS + 1 SAT) | Whittle index (state-aware)    |  30 |          2.908 |    1000.77  |            0.943 |               0.955 |           0.999 |        3.265 |                0.98  |              nan     |       1.486 |         0.866 |
| Integrated (2 BS + 2 SAT) | AoII threshold (state-aware)   |  30 |          0.176 |     141.767 |            0.927 |               0.955 |           1.025 |        2.876 |                0.976 |              nan     |       0.048 |         0.142 |
| Integrated (2 BS + 2 SAT) | Nominal (non-robust) SENTINEL  |  30 |          0.306 |     170.6   |            0.925 |               0.232 |           3.935 |        5.4   |                0.772 |                4.483 |       0.05  |         0.27  |
| Integrated (2 BS + 2 SAT) | Random                         |  30 |          5.953 |     381.867 |            0.594 |               0.375 |           1.189 |        3.343 |                0.883 |              nan     |       0.242 |         6.056 |
| Integrated (2 BS + 2 SAT) | SENTINEL (robust)              |  30 |          0.307 |     179.367 |            0.924 |               0.232 |           3.934 |        5.112 |                0.736 |                4.278 |       0.05  |         0.269 |
| Integrated (2 BS + 2 SAT) | SENTINEL + rate-capped trigger |  30 |          0.208 |     198.733 |            0.906 |               0.956 |           1.023 |        4.647 |                0.73  |                4.278 |       0.059 |         0.168 |
| Integrated (2 BS + 2 SAT) | SENTINEL + state-aware trigger |  30 |          0.208 |     198.733 |            0.906 |               0.956 |           1.023 |        4.647 |                0.73  |                4.278 |       0.059 |         0.168 |
| Integrated (2 BS + 2 SAT) | Whittle index (state-aware)    |  30 |          0.175 |     138.9   |            0.938 |               0.955 |           1.025 |        2.875 |                0.976 |              nan     |       0.048 |         0.141 |
| Integrated (3 BS + 3 SAT) | AoII threshold (state-aware)   |  30 |          0.141 |     103.433 |            0.936 |               0.955 |           1.026 |        2.648 |                0.979 |              nan     |       0.008 |         0.143 |
| Integrated (3 BS + 3 SAT) | Nominal (non-robust) SENTINEL  |  30 |          0.275 |     181.5   |            0.917 |               0.232 |           3.928 |        5.365 |                0.709 |                2.612 |       0.015 |         0.273 |
| Integrated (3 BS + 3 SAT) | Random                         |  30 |          6.057 |     375.4   |            0.572 |               0.381 |           1.144 |        3.313 |                0.888 |              nan     |       0.188 |         6.035 |
| Integrated (3 BS + 3 SAT) | SENTINEL (robust)              |  30 |          0.266 |     164.567 |            0.92  |               0.232 |           3.93  |        4.913 |                0.644 |                1.727 |       0.013 |         0.263 |
| Integrated (3 BS + 3 SAT) | SENTINEL + rate-capped trigger |  30 |          0.163 |     190.367 |            0.904 |               0.955 |           1.022 |        4.706 |                0.648 |                1.727 |       0.01  |         0.16  |
| Integrated (3 BS + 3 SAT) | SENTINEL + state-aware trigger |  30 |          0.163 |     190.367 |            0.904 |               0.955 |           1.022 |        4.706 |                0.648 |                1.727 |       0.01  |         0.16  |
| Integrated (3 BS + 3 SAT) | Whittle index (state-aware)    |  30 |          0.141 |     103.433 |            0.936 |               0.955 |           1.026 |        2.648 |                0.979 |              nan     |       0.008 |         0.143 |
| Satellite only (2 SAT)    | AoII threshold (state-aware)   |  30 |          0.176 |     139.167 |            0.926 |               0.955 |           1.025 |        2.947 |                1     |              nan     |       0.047 |         0.141 |
| Satellite only (2 SAT)    | Nominal (non-robust) SENTINEL  |  30 |          0.32  |     187.7   |            0.941 |               0.231 |           3.95  |        5.773 |                1     |                5.771 |       0.05  |         0.278 |
| Satellite only (2 SAT)    | Random                         |  30 |          2.749 |     237.767 |            0.985 |               0.3   |           1.971 |        3.256 |                1     |              nan     |       0.11  |         2.72  |
| Satellite only (2 SAT)    | SENTINEL (robust)              |  30 |          0.318 |     195.633 |            0.942 |               0.231 |           3.951 |        5.447 |                1     |                5.771 |       0.05  |         0.278 |
| Satellite only (2 SAT)    | SENTINEL + rate-capped trigger |  30 |          0.281 |     258.967 |            0.909 |               0.955 |           1.023 |        4.563 |                1     |                5.771 |       0.128 |         0.184 |
| Satellite only (2 SAT)    | SENTINEL + state-aware trigger |  30 |          0.281 |     258.967 |            0.909 |               0.955 |           1.023 |        4.563 |                1     |                5.771 |       0.128 |         0.184 |
| Satellite only (2 SAT)    | Whittle index (state-aware)    |  30 |          0.176 |     139.167 |            0.927 |               0.955 |           1.025 |        2.947 |                1     |              nan     |       0.047 |         0.141 |

## ue_sweep, disruption off

|   x | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   5 | AoII threshold (state-aware)   |  30 |          0.15  |     100.533 |            0.96  |               0.957 |           0.496 |        2.801 |                0.971 |              nan     |       0.06  |         0.113 |
|   5 | Nominal (non-robust) SENTINEL  |  30 |          0.316 |     163.733 |            0.962 |               0.223 |           1.984 |        4.936 |                0.858 |                4.84  |       0.138 |         0.237 |
|   5 | PPO (AoII reward, trained)     |  30 |          0.33  |     145.633 |            0.97  |               0.223 |           1.975 |        4.05  |                1     |              nan     |       0.084 |         0.253 |
|   5 | Random                         |  30 |          5.85  |     326.533 |            0.587 |               0.372 |           0.587 |        3.24  |                0.908 |              nan     |       0.288 |         5.773 |
|   5 | SENTINEL (robust)              |  30 |          0.32  |     164     |            0.961 |               0.223 |           1.983 |        4.667 |                0.795 |                4.47  |       0.138 |         0.238 |
|   5 | SENTINEL + rate-capped trigger |  30 |          0.257 |     186.133 |            0.939 |               0.957 |           0.495 |        4.424 |                0.767 |                4.47  |       0.204 |         0.143 |
|   5 | SENTINEL + state-aware trigger |  30 |          0.257 |     186.133 |            0.939 |               0.957 |           0.495 |        4.424 |                0.767 |                4.47  |       0.204 |         0.143 |
|   5 | Whittle index (state-aware)    |  30 |          0.142 |      96.267 |            0.969 |               0.957 |           0.496 |        2.801 |                0.971 |              nan     |       0.042 |         0.113 |
|  10 | AoII threshold (state-aware)   |  30 |          0.156 |     138.233 |            0.965 |               0.955 |           1.029 |        2.829 |                0.976 |              nan     |       0.047 |         0.121 |
|  10 | Nominal (non-robust) SENTINEL  |  30 |          0.285 |     165.433 |            0.949 |               0.231 |           3.957 |        5.424 |                0.773 |                4.483 |       0.049 |         0.246 |
|  10 | PPO (AoII reward, trained)     |  30 |          0.406 |     229.9   |            0.96  |               0.237 |           3.8   |        4.221 |                1     |              nan     |       0.058 |         0.344 |
|  10 | Random                         |  30 |          5.878 |     367.6   |            0.598 |               0.375 |           1.197 |        3.309 |                0.884 |              nan     |       0.235 |         5.96  |
|  10 | SENTINEL (robust)              |  30 |          0.294 |     177.9   |            0.946 |               0.231 |           3.954 |        5.122 |                0.737 |                4.278 |       0.06  |         0.251 |
|  10 | SENTINEL + rate-capped trigger |  30 |          0.193 |     196.5   |            0.933 |               0.955 |           1.026 |        4.61  |                0.731 |                4.278 |       0.058 |         0.153 |
|  10 | SENTINEL + state-aware trigger |  30 |          0.193 |     196.5   |            0.933 |               0.955 |           1.026 |        4.61  |                0.731 |                4.278 |       0.058 |         0.153 |
|  10 | Whittle index (state-aware)    |  30 |          0.155 |     135.367 |            0.977 |               0.955 |           1.029 |        2.829 |                0.976 |              nan     |       0.047 |         0.121 |
|  15 | AoII threshold (state-aware)   |  30 |          0.214 |     159.467 |            0.967 |               0.955 |           1.567 |        2.933 |                0.978 |              nan     |       0.173 |         0.123 |
|  15 | Nominal (non-robust) SENTINEL  |  30 |          0.343 |     235.667 |            0.958 |               0.234 |           5.947 |        5.774 |                0.752 |                4.404 |       0.176 |         0.25  |
|  15 | PPO (AoII reward, trained)     |  30 |          0.483 |     284.7   |            0.959 |               0.239 |           5.702 |        4.648 |                1     |              nan     |       0.189 |         0.383 |
|  15 | Random                         |  30 |          5.962 |     396.867 |            0.599 |               0.377 |           1.794 |        3.313 |                0.881 |              nan     |       0.276 |         5.828 |
|  15 | SENTINEL (robust)              |  30 |          0.341 |     224.533 |            0.957 |               0.234 |           5.945 |        5.433 |                0.727 |                4.256 |       0.175 |         0.249 |
|  15 | SENTINEL + rate-capped trigger |  30 |          0.492 |     367.633 |            0.924 |               0.955 |           1.56  |        4.698 |                0.722 |                4.256 |       0.393 |         0.14  |
|  15 | SENTINEL + state-aware trigger |  30 |          0.492 |     367.633 |            0.924 |               0.955 |           1.56  |        4.698 |                0.722 |                4.256 |       0.393 |         0.14  |
|  15 | Whittle index (state-aware)    |  30 |          0.212 |     153.5   |            0.974 |               0.955 |           1.567 |        2.932 |                0.978 |              nan     |       0.173 |         0.123 |
|  20 | AoII threshold (state-aware)   |  30 |          0.256 |     270.9   |            0.954 |               0.955 |           2.063 |        2.995 |                0.979 |              nan     |       0.147 |         0.131 |
|  20 | Nominal (non-robust) SENTINEL  |  30 |          0.442 |     342.4   |            0.947 |               0.232 |           7.91  |        6.257 |                0.768 |                4.466 |       0.189 |         0.254 |
|  20 | PPO (AoII reward, trained)     |  30 |          0.5   |     401.633 |            0.954 |               0.235 |           7.693 |        5.582 |                0.999 |              nan     |       0.106 |         0.424 |
|  20 | Random                         |  30 |          6.024 |     507.533 |            0.595 |               0.377 |           2.377 |        3.365 |                0.887 |              nan     |       0.202 |         5.99  |
|  20 | SENTINEL (robust)              |  30 |          0.37  |     311.7   |            0.947 |               0.232 |           7.909 |        5.83  |                0.75  |                4.341 |       0.163 |         0.26  |
|  20 | SENTINEL + rate-capped trigger |  30 |          0.332 |     399.067 |            0.914 |               0.955 |           2.055 |        4.761 |                0.739 |                4.341 |       0.178 |         0.161 |
|  20 | SENTINEL + state-aware trigger |  30 |          0.332 |     399.067 |            0.914 |               0.955 |           2.055 |        4.761 |                0.739 |                4.341 |       0.178 |         0.161 |
|  20 | Whittle index (state-aware)    |  30 |          0.293 |     271.267 |            0.973 |               0.955 |           2.064 |        2.993 |                0.979 |              nan     |       0.185 |         0.127 |

## ue_sweep, disruption on

|   x | policy                         |   n |   average_aoii |   peak_aoii |   delivery_ratio |   informative_ratio |   sum_rate_mbps |   latency_ms |   sat_delivery_share |   certified_eta_mean |   aoii_ci95 |   aoii_median |
|----:|:-------------------------------|----:|---------------:|------------:|-----------------:|--------------------:|----------------:|-------------:|---------------------:|---------------------:|------------:|--------------:|
|   5 | AoII threshold (state-aware)   |  30 |          0.168 |     103.4   |            0.924 |               0.957 |           0.494 |        2.844 |                0.97  |              nan     |       0.06  |         0.134 |
|   5 | Nominal (non-robust) SENTINEL  |  30 |          0.339 |     168.333 |            0.934 |               0.223 |           1.971 |        4.958 |                0.858 |                4.84  |       0.138 |         0.253 |
|   5 | PPO (AoII reward, trained)     |  30 |          0.354 |     151.067 |            0.939 |               0.223 |           1.962 |        4.04  |                1     |              nan     |       0.083 |         0.28  |
|   5 | Random                         |  30 |          5.99  |     368.467 |            0.582 |               0.373 |           0.582 |        3.276 |                0.907 |              nan     |       0.298 |         5.936 |
|   5 | SENTINEL (robust)              |  30 |          0.337 |     158.4   |            0.937 |               0.223 |           1.973 |        4.678 |                0.794 |                4.47  |       0.137 |         0.265 |
|   5 | SENTINEL + rate-capped trigger |  30 |          0.31  |     189.567 |            0.907 |               0.957 |           0.493 |        4.461 |                0.766 |                4.47  |       0.276 |         0.155 |
|   5 | SENTINEL + state-aware trigger |  30 |          0.31  |     189.567 |            0.907 |               0.957 |           0.493 |        4.461 |                0.766 |                4.47  |       0.276 |         0.155 |
|   5 | Whittle index (state-aware)    |  30 |          0.16  |      99.133 |            0.932 |               0.957 |           0.494 |        2.843 |                0.971 |              nan     |       0.042 |         0.134 |
|  10 | AoII threshold (state-aware)   |  30 |          0.176 |     141.767 |            0.927 |               0.955 |           1.025 |        2.876 |                0.976 |              nan     |       0.048 |         0.142 |
|  10 | Nominal (non-robust) SENTINEL  |  30 |          0.306 |     170.6   |            0.925 |               0.232 |           3.935 |        5.4   |                0.772 |                4.483 |       0.05  |         0.27  |
|  10 | PPO (AoII reward, trained)     |  30 |          0.435 |     236.5   |            0.928 |               0.238 |           3.772 |        4.219 |                1     |              nan     |       0.058 |         0.372 |
|  10 | Random                         |  30 |          5.953 |     381.867 |            0.594 |               0.375 |           1.189 |        3.343 |                0.883 |              nan     |       0.242 |         6.056 |
|  10 | SENTINEL (robust)              |  30 |          0.307 |     179.367 |            0.924 |               0.232 |           3.934 |        5.112 |                0.736 |                4.278 |       0.05  |         0.269 |
|  10 | SENTINEL + rate-capped trigger |  30 |          0.208 |     198.733 |            0.906 |               0.956 |           1.023 |        4.647 |                0.73  |                4.278 |       0.059 |         0.168 |
|  10 | SENTINEL + state-aware trigger |  30 |          0.208 |     198.733 |            0.906 |               0.956 |           1.023 |        4.647 |                0.73  |                4.278 |       0.059 |         0.168 |
|  10 | Whittle index (state-aware)    |  30 |          0.175 |     138.9   |            0.938 |               0.955 |           1.025 |        2.875 |                0.976 |              nan     |       0.048 |         0.141 |
|  15 | AoII threshold (state-aware)   |  30 |          0.234 |     160.467 |            0.929 |               0.955 |           1.561 |        2.98  |                0.978 |              nan     |       0.173 |         0.142 |
|  15 | Nominal (non-robust) SENTINEL  |  30 |          0.363 |     242.6   |            0.935 |               0.235 |           5.917 |        5.692 |                0.75  |                4.404 |       0.177 |         0.269 |
|  15 | PPO (AoII reward, trained)     |  30 |          0.51  |     286.167 |            0.928 |               0.24  |           5.661 |        4.618 |                1     |              nan     |       0.188 |         0.413 |
|  15 | Random                         |  30 |          6.012 |     402.7   |            0.595 |               0.378 |           1.783 |        3.351 |                0.88  |              nan     |       0.281 |         5.873 |
|  15 | SENTINEL (robust)              |  30 |          0.36  |     227.733 |            0.936 |               0.235 |           5.917 |        5.398 |                0.726 |                4.256 |       0.176 |         0.264 |
|  15 | SENTINEL + rate-capped trigger |  30 |          0.507 |     368.767 |            0.898 |               0.955 |           1.555 |        4.735 |                0.722 |                4.256 |       0.393 |         0.155 |
|  15 | SENTINEL + state-aware trigger |  30 |          0.507 |     368.767 |            0.898 |               0.955 |           1.555 |        4.735 |                0.722 |                4.256 |       0.393 |         0.155 |
|  15 | Whittle index (state-aware)    |  30 |          0.231 |     154.5   |            0.936 |               0.955 |           1.561 |        2.979 |                0.978 |              nan     |       0.173 |         0.142 |
|  20 | AoII threshold (state-aware)   |  30 |          0.274 |     271.4   |            0.92  |               0.955 |           2.056 |        3.043 |                0.979 |              nan     |       0.146 |         0.149 |
|  20 | Nominal (non-robust) SENTINEL  |  30 |          0.462 |     342.8   |            0.923 |               0.232 |           7.868 |        6.135 |                0.766 |                4.466 |       0.189 |         0.276 |
|  20 | PPO (AoII reward, trained)     |  30 |          0.525 |     403.933 |            0.925 |               0.236 |           7.644 |        5.453 |                0.999 |              nan     |       0.107 |         0.446 |
|  20 | Random                         |  30 |          6.107 |     543.133 |            0.591 |               0.377 |           2.362 |        3.401 |                0.886 |              nan     |       0.198 |         6.051 |
|  20 | SENTINEL (robust)              |  30 |          0.389 |     315.033 |            0.925 |               0.232 |           7.872 |        5.763 |                0.749 |                4.341 |       0.163 |         0.278 |
|  20 | SENTINEL + rate-capped trigger |  30 |          0.346 |     399.067 |            0.888 |               0.955 |           2.049 |        4.799 |                0.738 |                4.341 |       0.177 |         0.175 |
|  20 | SENTINEL + state-aware trigger |  30 |          0.346 |     399.067 |            0.888 |               0.955 |           2.049 |        4.799 |                0.738 |                4.341 |       0.177 |         0.175 |
|  20 | Whittle index (state-aware)    |  30 |          0.311 |     271.767 |            0.938 |               0.955 |           2.057 |        3.041 |                0.979 |              nan     |       0.184 |         0.146 |

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
