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

Device domains sampled: 6; best sample equals the noiseless optimum in 6 of 6; total QPU time 14 s over 4 jobs; feasible-shot fraction 34.8% to 73.5%.

## Noise models (offline)

| run | backend | UEs | seed | domain | qubits | 2q gates | depth | shots | feasible shots | best = noiseless opt | schedule gap vs ILP |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fake_U6_k4_p1_s1_greedy | fake_fez | 6 | 1 | 0 | 18 | 139 | 188 | 2048 | 69.6% | yes | +0.00% |
| fake_U6_k4_p1_s1_greedy_torino | fake_torino | 6 | 1 | 0 | 18 | 137 | 169 | 2048 | 52.1% | yes | +0.00% |
| fake_U6_k4_p1_s1_greedy | fake_fez | 6 | 1 | 1 | 20 | 301 | 436 | 2048 | 47.6% | no | +0.00% |
| fake_U6_k4_p1_s1_greedy_torino | fake_torino | 6 | 1 | 1 | 20 | 279 | 355 | 2048 | 33.1% | yes | +0.00% |
