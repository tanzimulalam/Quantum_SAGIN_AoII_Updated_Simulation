# Running the SENTINEL domain QUBOs on an IBM Quantum device

This is the only step of the evaluation that needs an author's own account. Everything else (scenario weights, ADMM
targets, QAOA angles) is optimized on the local simulator; the device is used once per domain for the final sampling,
which costs a few seconds of QPU time under the Open Plan's 10 minutes per 28 days.

## 1. One-time account setup (your own Python session, never in a script in this repository)

1. Create a free account at quantum.cloud.ibm.com (IBM Quantum Platform) and copy your API token from the dashboard.
2. In a Python session using this repository's environment:

   ```python
   from qiskit_ibm_runtime import QiskitRuntimeService
   QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token="PASTE-YOUR-TOKEN", overwrite=True)
   ```

   The token is stored in your user profile (`~/.qiskit/qiskit-ibm.json`), outside the repository. Do not paste it
   into any file that is committed.
3. Check the remaining budget on the platform's usage page before and after each run.

## 2. Dry runs (no account, no QPU time)

```bash
.venv/Scripts/python.exe scripts/hardware_run.py --mode estimate --fake FakeTorino --ues 6 --init greedy
.venv/Scripts/python.exe scripts/hardware_run.py --mode fake --fake FakeTorino --ues 6 --init greedy --shots 2048
```

`estimate` prints qubits, two-qubit gates, depth and an upper bound on QPU seconds per domain. `fake` runs the identical
circuits on the device's noise model and produces the same summary files as a device run, so the write-up can compare
noiseless, noisy-model and device results side by side.

## 3. Device run

```bash
.venv/Scripts/python.exe scripts/hardware_run.py --mode device --ues 6 --init greedy --shots 4096 --domains 0
```

- With no `--backend`, the least busy operational device of your instance is used; add `--backend ibm_torino` (or
  another name shown on the platform) to choose one.
- `--domains 0` samples only the 18-qubit domain (about 140 two-qubit gates); omit it to sample both domains.
- Expect minutes to hours of queue time and 2 to 5 seconds of QPU time per 4096-shot job. The job id and the usage
  reported by the service are written to `results/hardware/<tag>/summary.json`.
- Outputs per run: `summary.json`, `summary.md`, and `counts_domain<k>.json` (raw device counts), all safe to commit.

## 4. What to report in the paper

Per domain: qubits, two-qubit gates after transpilation, depth, the fraction of device shots that decode to one-hot
and capacity-feasible assignments, the best decoded energy against the noiseless optimum, and the worst-case AoII of
the device-decoded network schedule against the exact ILP. Report the noisy-model run of the same circuits next to it.
State the device name, calibration date (from the platform), shots, and the QPU seconds consumed.

## 5. Budget plan

| Item | QPU time |
|---|---|
| One 4096-shot sampling job on an 18 to 20 qubit domain | about 3 to 5 s |
| Both domains of a 6-UE instance | about 10 s |
| Five instances (seeds 1 to 5), both domains | about 50 s |
| Repeating the five instances with 3 shot counts for a shot-noise study | about 150 s |

Even the full plan uses a quarter of one month's allowance, leaving room for a second device for comparison.
