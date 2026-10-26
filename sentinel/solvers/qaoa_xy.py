"""XY-mixer QAOA for the compact (slack-free) domain QUBO of sentinel.compact.

Each UE's decision qubits form a one-hot group. The mixer on a group is the ring XY Hamiltonian
sum_(a,b adjacent) (X_a X_b + Y_a Y_b)/2, which conserves Hamming weight, so a state that starts one-hot stays one-hot
exactly (every XY term conserves weight individually, so Trotterization does not break it). Capacity-slack qubits use
the usual X mixer. The initial state is either the W state of each group (uniform superposition of its one-hot
states) or a warm start in the greedy assignment's basis state.

Parameters are optimized on a simulator with COBYLA on the sampled QUBO energy; sampled bitstrings are decoded
classically. The same circuit builder is used by scripts/hardware_run.py, which sends only the final sampling to an
IBM Quantum device.
"""
from __future__ import annotations

import time
from typing import Optional

import numpy as np
from scipy.optimize import minimize

from .qaoa import _build_hamiltonian


def _xy_ring_op(positions, n):
    from qiskit.quantum_info import SparsePauliOp
    m = len(positions)
    pairs = [(positions[i], positions[(i + 1) % m]) for i in range(m)] if m > 2 else [(positions[0], positions[1])]
    terms = []
    for a, b in pairs:
        for p in ("X", "Y"):
            label = ["I"] * n
            label[n - 1 - a] = p
            label[n - 1 - b] = p
            terms.append(("".join(label), 0.5))
    return SparsePauliOp.from_list(terms).simplify()


def _prepare_w_state(qc, qubits):
    """Linear-depth W-state preparation: |100..0> then a ladder of controlled-RY and CX (2 two-qubit gates per qubit)."""
    m = len(qubits)
    qc.x(qubits[0])
    for j in range(1, m):
        theta = 2.0 * np.arccos(np.sqrt(1.0 / (m - j + 1)))
        qc.cry(theta, qubits[j - 1], qubits[j])
        qc.cx(qubits[j], qubits[j - 1])


def build_xy_circuit(dq, depth: int = 1, init: str = "w", warm_start_sel=None, scale: Optional[float] = None):
    """Return (parameterized circuit with measurements, gamma parameters, beta parameters, cost scale)."""
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter
    from qiskit.circuit.library import PauliEvolutionGate
    n = dq.n
    scale = float(np.max(np.abs(dq.Q)) + 1e-12) if scale is None else scale
    H_C = _build_hamiltonian(dq.Q / scale)
    slack = list(range(dq.n_x, n))
    qc = QuantumCircuit(n)
    for g in dq.groups:
        g = [int(v) for v in g]
        if init == "greedy" and warm_start_sel is not None:
            chosen = [int(v) for v in warm_start_sel if int(v) in g]
            qc.x(chosen[0] if chosen else g[0])
        elif len(g) == 1:
            qc.x(g[0])
        else:
            _prepare_w_state(qc, g)
    for q in slack:
        qc.h(q)
    gammas = [Parameter(f"g{l}") for l in range(depth)]
    betas = [Parameter(f"b{l}") for l in range(depth)]
    mixers = [_xy_ring_op([int(v) for v in g], n) for g in dq.groups if len(g) >= 2]
    for l in range(depth):
        qc.append(PauliEvolutionGate(H_C, time=gammas[l]), range(n))
        for op in mixers:
            qc.append(PauliEvolutionGate(op, time=betas[l]), range(n))
        for q in slack:
            qc.rx(2 * betas[l], q)
    qc.measure_all()
    return qc, gammas, betas, scale


def decode_xy_counts(dq, inst, counts: dict, objective: str = "implied"):
    """Classical decoding. Returns (best_sel, best_assignment_energy, mean_energy, onehot_frac, feasible_frac).

    mean_energy is the quantity the classical optimizer minimizes: with objective="implied" it is the mean over
    one-hot samples of the assignment energy with slack bits set optimally (non-one-hot samples count as the worst
    one-hot energy seen plus one penalty unit); with objective="qubo" it is the raw QUBO energy of the full bitstring.
    """
    n = dq.n
    total = sum(counts.values())
    e_sum = 0.0
    onehot = 0
    feasible = 0
    best_sel, best_e = None, np.inf
    worst_seen = 0.0
    bad = 0
    for key, c in counts.items():
        w = np.array([int(key[n - 1 - a]) for a in range(n)], dtype=float)
        xk = w[: dq.n_x]
        if objective == "qubo":
            e_sum += c * (w @ dq.Q @ w + dq.const)
        if dq.is_onehot(xk):
            onehot += c
            sel = dq.sel_from_x(xk)
            e = dq.assignment_energy(sel, inst)
            if objective != "qubo":
                e_sum += c * e
            worst_seen = max(worst_seen, e)
            if dq.local_feasible(xk, inst):
                feasible += c
                if e < best_e:
                    best_sel, best_e = sel, e
        else:
            bad += c
    if objective != "qubo":
        e_sum += bad * (worst_seen + dq.lam_cap)
    return best_sel, float(best_e), e_sum / total, onehot / total, feasible / total


def qaoa_xy(dq, inst, depth: int = 1, shots: int = 512, maxiter: int = 60, seed: int = 0, init_params=None,
            warm_start_sel=None, init: str = "w", final_shots: int = 4096, backend=None):
    """Optimize XY-QAOA parameters on a simulator and decode the best sample of a final, larger shot batch."""
    from qiskit import transpile
    from qiskit_aer import AerSimulator
    t0 = time.time()
    qc, gammas, betas, scale = build_xy_circuit(dq, depth=depth, init=init, warm_start_sel=warm_start_sel)
    n = dq.n
    if backend is None:
        method = "statevector" if n <= 28 else "matrix_product_state"
        backend = AerSimulator(method=method, seed_simulator=seed)
    tqc = transpile(qc, backend, optimization_level=1)
    params = list(tqc.parameters)
    order = [p.name for p in params]
    rng = np.random.default_rng(seed)
    energies = []

    def run(theta, nshots):
        bound = tqc.assign_parameters(dict(zip(params, theta)))
        return backend.run(bound, shots=nshots).result().get_counts()

    def objective(theta):
        counts = run(theta, shots)
        _, _, e_mean, _, _ = decode_xy_counts(dq, inst, counts)
        energies.append(e_mean)
        return e_mean

    if init_params is not None and len(init_params) == len(params):
        x0 = np.asarray(init_params, dtype=float)
    else:
        x0 = rng.uniform(0.1, 0.8, size=len(params))
    res = minimize(objective, x0, method="COBYLA", options={"maxiter": maxiter, "rhobeg": 0.3})
    counts = run(res.x, final_shots)
    best_sel, best_e, e_mean, onehot_frac, feas_frac = decode_xy_counts(dq, inst, counts)
    two_q = sum(1 for ins in tqc.data if ins.operation.num_qubits == 2)
    return {"best_sel": best_sel, "best_energy": best_e, "energies": energies, "params": list(res.x), "param_names": order,
            "n_qubits": n, "depth": depth, "time_s": time.time() - t0, "onehot_sample_fraction": onehot_frac,
            "feasible_sample_fraction": feas_frac, "mean_energy_final": e_mean,
            "method": f"qaoa_xy_{getattr(backend.options, 'method', 'sim')}",
            "circuit_depth_transpiled": tqc.depth(), "two_qubit_gates": two_q, "scale": scale}
