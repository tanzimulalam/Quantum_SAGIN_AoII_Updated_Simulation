# Hardware runs

## Real device

| run | backend | UEs | seed | domain | qubits | 2q gates | depth | shots | feasible shots | best = noiseless opt | schedule gap vs ILP | QPU s | job |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| device_U6_k4_p1_s1_greedy | ibm_kingston | 6 | 1 | 0 | 18 | 139 | 187 | 4096 | 63.3% | yes | +0.00% | 3.0 | dbgjgr9t9uhs73c8act0 |
| device_U6_k4_p1_s1_greedy_d1 | ibm_kingston | 6 | 1 | 1 | 20 | 301 | 428 | 4096 | 42.7% | yes | +0.00% | 3.0 | dbgjjopq260s73btdpl0 |
| device_U6_k4_p1_s2_greedy | ibm_kingston | 6 | 2 | 0 | 18 | 139 | 187 | 4096 | 60.9% | yes | +0.00% | 4.0 | dbgjk11q260s73btdqa0 |
| device_U6_k4_p1_s2_greedy | ibm_kingston | 6 | 2 | 1 | 12 | 58 | 76 | 4096 | 73.5% | yes | +0.00% | 4.0 | dbgjk11q260s73btdqa0 |
| device_U6_k4_p1_s3_greedy | ibm_kingston | 6 | 3 | 0 | 24 | 305 | 387 | 4096 | 34.8% | yes | +0.00% | 4.0 | dbgjnmht9uhs73c8asrg |
| device_U6_k4_p1_s3_greedy | ibm_kingston | 6 | 3 | 1 | 14 | 120 | 187 | 4096 | 69.6% | yes | +0.00% | 4.0 | dbgjnmht9uhs73c8asrg |
| device_U6_k4_p1_s5_greedy | ibm_kingston | 6 | 5 | 0 | 12 | 58 | 74 | 4096 | 75.9% | yes | +0.00% | 4.0 | dbglprcdgr2s73crp4sg |
| device_U6_k4_p1_s5_greedy | ibm_kingston | 6 | 5 | 1 | 12 | 58 | 74 | 4096 | 76.4% | yes | +0.00% | 4.0 | dbglprcdgr2s73crp4sg |
| device_U6_k4_p1_s6_greedy | ibm_fez | 6 | 6 | 0 | 8 | 38 | 77 | 4096 | 86.5% | yes | +0.00% | 4.0 | dbgls5kdgr2s73crp820 |
| device_U6_k4_p1_s6_greedy | ibm_fez | 6 | 6 | 1 | 16 | 79 | 77 | 4096 | 61.8% | yes | +0.00% | 4.0 | dbgls5kdgr2s73crp820 |
| device_U6_k4_p1_s7_greedy | ibm_fez | 6 | 7 | 0 | 12 | 58 | 76 | 4096 | 71.9% | yes | +0.00% | 4.0 | dbglse8te5oc738ieka0 |
| device_U6_k4_p1_s7_greedy | ibm_fez | 6 | 7 | 1 | 18 | 142 | 171 | 4096 | 59.4% | yes | +0.00% | 4.0 | dbglse8te5oc738ieka0 |
| device_U10_k4_p1_s1_greedy | ibm_kingston | 10 | 1 | 0 | 38 | 606 | 626 | 4096 | 2.6% | yes | +0.00% | 3.0 | dbgls09q260s73btht2g |

Device domains sampled: 13; best sample equals the noiseless optimum in 13 of 13; total QPU time 29 s over 8 jobs; feasible-shot fraction 2.6% to 86.5%.

## Noise models (offline)

| run | backend | UEs | seed | domain | qubits | 2q gates | depth | shots | feasible shots | best = noiseless opt | schedule gap vs ILP |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fake_U6_k4_p1_s1_greedy | fake_fez | 6 | 1 | 0 | 18 | 139 | 188 | 2048 | 69.6% | yes | +0.00% |
| fake_U6_k4_p1_s1_greedy_torino | fake_torino | 6 | 1 | 0 | 18 | 137 | 169 | 2048 | 52.1% | yes | +0.00% |
| fake_U6_k4_p1_s1_greedy | fake_fez | 6 | 1 | 1 | 20 | 301 | 436 | 2048 | 47.6% | no | +0.00% |
| fake_U6_k4_p1_s1_greedy_torino | fake_torino | 6 | 1 | 1 | 20 | 279 | 355 | 2048 | 33.1% | yes | +0.00% |
