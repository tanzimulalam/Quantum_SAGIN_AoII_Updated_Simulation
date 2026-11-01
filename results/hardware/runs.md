# Hardware runs

## Real device

| run | backend | init | mitigation | UEs | seed | domain | qubits | 2q gates | feasible shots | P(opt shot) | P(opt given feasible) | approx ratio | uniform P(opt) | uniform ratio | spread | best = opt | schedule gap vs ILP | QPU s | job |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| device_U6_k4_p1_s1_w_fez | ibm_fez | w | none | 6 | 1 | 0 | 18 | 179 | 40.1% | 0.063 | 0.158 | 0.908 | 0.125 | 0.894 | 42.7% | yes | +0.00% | 4.0 | dbjfspt6p51s73ckoagg |
| device_U6_k4_p1_s1_greedy | ibm_kingston | greedy | none | 6 | 1 | 0 | 18 | 139 | 63.3% | 0.603 | 0.953 | 0.996 | 0.125 | 0.894 | 42.8% | yes | +0.00% | 3.0 | dbgjgr9t9uhs73c8act0 |
| device_U6_k4_p1_s1_w | ibm_kingston | w | none | 6 | 1 | 0 | 18 | 179 | 61.6% | 0.105 | 0.171 | 0.917 | 0.125 | 0.894 | 42.7% | yes | +0.00% | 4.0 | dbjcjbhkdqps7390bch0 |
| device_U6_k4_p1_s1_w_fez | ibm_fez | w | none | 6 | 1 | 1 | 20 | 314 | 16.1% | 0.028 | 0.173 | 0.665 | 0.125 | 0.623 | 307.1% | yes | +0.00% | 4.0 | dbjfspt6p51s73ckoagg |
| device_U6_k4_p1_s1_greedy_d1 | ibm_kingston | greedy | none | 6 | 1 | 1 | 20 | 301 | 42.7% | 0.396 | 0.928 | 0.979 | 0.125 | 0.623 | 307.3% | yes | +0.00% | 3.0 | dbgjjopq260s73btdpl0 |
| device_U6_k4_p1_s1_w | ibm_kingston | w | none | 6 | 1 | 1 | 20 | 314 | 36.2% | 0.055 | 0.152 | 0.693 | 0.125 | 0.623 | 307.1% | yes | +0.00% | 4.0 | dbjcjbhkdqps7390bch0 |
| device_U6_k4_p1_s2_w_fez | ibm_fez | w | none | 6 | 2 | 0 | 18 | 179 | 40.2% | 0.036 | 0.089 | 0.927 | 0.125 | 0.909 | 34.6% | yes | +0.00% | 0.0 | dbjfst1kdqps7390h29g |
| device_U6_k4_p1_s2_greedy | ibm_kingston | greedy | none | 6 | 2 | 0 | 18 | 139 | 60.9% | 0.580 | 0.952 | 0.997 | 0.031 | 0.909 | 34.7% | yes | +0.00% | 4.0 | dbgjk11q260s73btdqa0 |
| device_U6_k4_p1_s2_w | ibm_kingston | w | none | 6 | 2 | 0 | 18 | 179 | 62.1% | 0.055 | 0.088 | 0.925 | 0.125 | 0.909 | 34.6% | yes | +0.00% | 0.0 | dbjeag0nceqs73ajs610 |
| device_U6_k4_p1_s2_w_fez | ibm_fez | w | none | 6 | 2 | 1 | 12 | 78 | 57.4% | 0.081 | 0.141 | 0.999 | 0.125 | 0.999 | 0.2% | yes | +0.00% | 0.0 | dbjfst1kdqps7390h29g |
| device_U6_k4_p1_s2_greedy | ibm_kingston | greedy | none | 6 | 2 | 1 | 12 | 58 | 73.5% | 0.695 | 0.945 | 1.000 | 0.016 | 0.998 | 0.3% | yes | +0.00% | 4.0 | dbgjk11q260s73btdqa0 |
| device_U6_k4_p1_s2_w | ibm_kingston | w | none | 6 | 2 | 1 | 12 | 78 | 73.6% | 0.087 | 0.118 | 0.999 | 0.125 | 0.999 | 0.2% | yes | +0.00% | 0.0 | dbjeag0nceqs73ajs610 |
| device_U6_k4_p1_s3_w_fez | ibm_fez | w | none | 6 | 3 | 0 | 24 | 333 | 16.3% | 0.006 | 0.036 | 0.779 | 0.062 | 0.765 | 114.8% | yes | +0.00% | 0.0 | dbjft1onceqs73ajuglg |
| device_U6_k4_p1_s3_greedy | ibm_kingston | greedy | none | 6 | 3 | 0 | 24 | 305 | 34.8% | 0.315 | 0.906 | 0.991 | 0.062 | 0.765 | 114.8% | yes | +0.00% | 4.0 | dbgjnmht9uhs73c8asrg |
| device_U6_k4_p1_s3_greedy_ctrl | ibm_kingston | greedy | none | 6 | 3 | 0 | 24 | 305 | 25.0% | 0.219 | 0.875 | 0.985 | 0.062 | 0.765 | 114.8% | yes | +0.00% | 3.0 | dbgnj9cdgr2s73crsme0 |
| device_U6_k4_p1_s3_greedy_dd | ibm_kingston | greedy | dd | 6 | 3 | 0 | 24 | 305 | 21.1% | 0.182 | 0.863 | 0.973 | 0.062 | 0.765 | 114.8% | yes | +0.00% | 3.0 | dbgndlht9uhs73c8hsn0 |
| device_U6_k4_p1_s3_greedy_ddtwirl | ibm_kingston | greedy | dd_twirl | 6 | 3 | 0 | 24 | 305 | 13.8% | 0.119 | 0.860 | 0.974 | 0.062 | 0.765 | 114.8% | yes | +0.00% | 3.0 | dbgnev1q260s73btl0ig |
| device_U6_k4_p1_s3_w | ibm_kingston | w | none | 6 | 3 | 0 | 24 | 333 | 33.8% | 0.011 | 0.032 | 0.802 | 0.062 | 0.765 | 114.8% | yes | +0.00% | 0.0 | dbjeam8nceqs73ajs6ag |
| device_U6_k4_p1_s3_w_fez | ibm_fez | w | none | 6 | 3 | 1 | 14 | 154 | 46.6% | 0.085 | 0.182 | 0.720 | 0.250 | 0.718 | 263.1% | yes | +0.00% | 0.0 | dbjft1onceqs73ajuglg |
| device_U6_k4_p1_s3_greedy | ibm_kingston | greedy | none | 6 | 3 | 1 | 14 | 120 | 69.6% | 0.667 | 0.958 | 0.988 | 0.250 | 0.718 | 263.1% | yes | +0.00% | 4.0 | dbgjnmht9uhs73c8asrg |
| device_U6_k4_p1_s3_w | ibm_kingston | w | none | 6 | 3 | 1 | 14 | 154 | 73.7% | 0.147 | 0.200 | 0.739 | 0.250 | 0.718 | 263.1% | yes | +0.00% | 0.0 | dbjeam8nceqs73ajs6ag |
| device_U6_k4_p1_s5_w_fez | ibm_fez | w | none | 6 | 5 | 0 | 12 | 82 | 55.7% | 0.086 | 0.154 | 1.000 | 0.125 | 0.999 | 0.1% | yes | +0.00% | 0.0 | dbjfsppffo6c73b9j8n0 |
| device_U6_k4_p1_s5_greedy | ibm_kingston | greedy | none | 6 | 5 | 0 | 12 | 58 | 75.9% | 0.744 | 0.980 | 1.000 | 0.125 | 1.000 | 0.0% | yes | +0.00% | 4.0 | dbglprcdgr2s73crp4sg |
| device_U6_k4_p1_s5_w | ibm_kingston | w | none | 6 | 5 | 0 | 12 | 82 | 72.9% | 0.096 | 0.132 | 0.999 | 0.125 | 0.999 | 0.1% | yes | +0.00% | 0.0 | dbjead1kdqps7390erqg |
| device_U6_k4_p1_s5_w_fez | ibm_fez | w | none | 6 | 5 | 1 | 12 | 82 | 54.5% | 0.059 | 0.108 | 0.999 | 0.125 | 0.999 | 0.1% | yes | +0.00% | 0.0 | dbjfsppffo6c73b9j8n0 |
| device_U6_k4_p1_s5_greedy | ibm_kingston | greedy | none | 6 | 5 | 1 | 12 | 58 | 76.4% | 0.748 | 0.979 | 1.000 | 0.125 | 1.000 | 0.0% | yes | +0.00% | 4.0 | dbglprcdgr2s73crp4sg |
| device_U6_k4_p1_s5_w | ibm_kingston | w | none | 6 | 5 | 1 | 12 | 82 | 73.8% | 0.086 | 0.117 | 0.999 | 0.125 | 0.999 | 0.1% | yes | +0.00% | 0.0 | dbjead1kdqps7390erqg |
| device_U6_k4_p1_s6_greedy | ibm_fez | greedy | none | 6 | 6 | 0 | 8 | 38 | 86.5% | 0.854 | 0.988 | 1.000 | 0.250 | 0.993 | 1.4% | yes | +0.00% | 4.0 | dbgls5kdgr2s73crp820 |
| device_U6_k4_p1_s6_w_fez | ibm_fez | w | none | 6 | 6 | 0 | 8 | 52 | 65.5% | 0.216 | 0.329 | 0.994 | 0.250 | 0.993 | 1.4% | yes | +0.00% | 0.0 | dbjft61ffo6c73b9j950 |
| device_U6_k4_p1_s6_w | ibm_kingston | w | none | 6 | 6 | 0 | 8 | 52 | 81.0% | 0.299 | 0.369 | 0.994 | 0.250 | 0.993 | 1.4% | yes | +0.00% | 0.0 | dbjeart6p51s73ckm3dg |
| device_U6_k4_p1_s6_greedy | ibm_fez | greedy | none | 6 | 6 | 1 | 16 | 79 | 61.8% | 0.588 | 0.953 | 1.000 | 0.062 | 0.993 | 1.4% | yes | +0.00% | 4.0 | dbgls5kdgr2s73crp820 |
| device_U6_k4_p1_s6_w_fez | ibm_fez | w | none | 6 | 6 | 1 | 16 | 108 | 43.8% | 0.056 | 0.128 | 0.994 | 0.062 | 0.993 | 1.4% | yes | +0.00% | 0.0 | dbjft61ffo6c73b9j950 |
| device_U6_k4_p1_s6_w | ibm_kingston | w | none | 6 | 6 | 1 | 16 | 108 | 69.0% | 0.096 | 0.140 | 0.995 | 0.062 | 0.993 | 1.4% | yes | +0.00% | 0.0 | dbjeart6p51s73ckm3dg |
| device_U6_k4_p1_s7_greedy | ibm_fez | greedy | none | 6 | 7 | 0 | 12 | 58 | 71.9% | 0.699 | 0.973 | 1.000 | 0.125 | 0.992 | 1.5% | yes | +0.00% | 4.0 | dbglse8te5oc738ieka0 |
| device_U6_k4_p1_s7_w_fez | ibm_fez | w | none | 6 | 7 | 0 | 12 | 80 | 59.4% | 0.073 | 0.123 | 0.992 | 0.125 | 0.992 | 1.5% | yes | +0.00% | 4.0 | dbjfst1kdqps7390h290 |
| device_U6_k4_p1_s7_w | ibm_kingston | w | none | 6 | 7 | 0 | 12 | 80 | 74.1% | 0.088 | 0.118 | 0.992 | 0.125 | 0.992 | 1.5% | yes | +0.00% | 4.0 | dbjeaggnceqs73ajs620 |
| device_U6_k4_p1_s7_greedy | ibm_fez | greedy | none | 6 | 7 | 1 | 18 | 142 | 59.4% | 0.554 | 0.933 | 0.994 | 0.125 | 0.858 | 62.7% | yes | +0.00% | 4.0 | dbglse8te5oc738ieka0 |
| device_U6_k4_p1_s7_w_fez | ibm_fez | w | none | 6 | 7 | 1 | 18 | 185 | 49.0% | 0.032 | 0.066 | 0.874 | 0.125 | 0.858 | 62.7% | yes | +0.00% | 4.0 | dbjfst1kdqps7390h290 |
| device_U6_k4_p1_s7_w | ibm_kingston | w | none | 6 | 7 | 1 | 18 | 185 | 52.7% | 0.035 | 0.066 | 0.875 | 0.125 | 0.858 | 62.7% | yes | +0.00% | 4.0 | dbjeaggnceqs73ajs620 |
| device_U10_k4_p1_s1_w_fez | ibm_fez | w | none | 10 | 1 | 0 | 38 | 719 | 1.4% | 0.000 | 0.000 | 0.802 | 0.006 | 0.790 | 82.0% | no | +0.00% | 0.0 | dbjft4l6p51s73ckoatg |
| device_U10_k4_p1_s1_greedy | ibm_kingston | greedy | none | 10 | 1 | 0 | 38 | 606 | 2.6% | 0.006 | 0.243 | 0.858 | 0.006 | 0.790 | 82.0% | yes | +0.00% | 3.0 | dbgls09q260s73btht2g |
| device_U10_k4_p1_s1_greedy_ctrl | ibm_kingston | greedy | none | 10 | 1 | 0 | 38 | 606 | 2.4% | 0.007 | 0.309 | 0.866 | 0.006 | 0.790 | 82.0% | yes | +0.00% | 3.0 | dbgo21gte5oc738ij3h0 |
| device_U10_k4_p1_s1_greedy_dd | ibm_kingston | greedy | dd | 10 | 1 | 0 | 38 | 606 | 0.7% | 0.002 | 0.370 | 0.869 | 0.006 | 0.790 | 82.0% | yes | +0.00% | 3.0 | dbgnee1t9uhs73c8hud0 |
| device_U10_k4_p1_s1_greedy_ddtwirl | ibm_kingston | greedy | dd_twirl | 10 | 1 | 0 | 38 | 606 | 0.2% | 0.000 | 0.100 | 0.873 | 0.006 | 0.790 | 82.0% | yes | +0.00% | 3.0 | dbgnfp0te5oc738ihpg0 |
| device_U10_k4_p1_s1_w | ibm_kingston | w | none | 10 | 1 | 0 | 38 | 719 | 3.5% | 0.000 | 0.000 | 0.821 | 0.006 | 0.790 | 82.0% | no | +0.00% | 0.0 | dbjeaod6p51s73ckm38g |

Device domains sampled: 45; best sample equals the noiseless optimum in 43 of 45; total QPU time 63 s over 28 jobs; feasible-shot fraction 0.2% to 86.5%.

## Noise models (offline)

| run | backend | UEs | seed | domain | qubits | 2q gates | depth | shots | feasible shots | best = noiseless opt | schedule gap vs ILP |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fake_U6_k4_p1_s1_greedy | fake_fez | 6 | 1 | 0 | 18 | 139 | 188 | 2048 | 69.6% | yes | +0.00% |
| fake_U6_k4_p1_s1_greedy_torino | fake_torino | 6 | 1 | 0 | 18 | 137 | 169 | 2048 | 52.1% | yes | +0.00% |
| fake_U6_k4_p1_s1_greedy | fake_fez | 6 | 1 | 1 | 20 | 301 | 436 | 2048 | 47.6% | no | +0.00% |
| fake_U6_k4_p1_s1_greedy_torino | fake_torino | 6 | 1 | 1 | 20 | 279 | 355 | 2048 | 33.1% | yes | +0.00% |
