"""Depth-p QAOA on the Qiskit Aer simulator for a domain QUBO (paper Section V-B/V-C).

Cost Hamiltonian: H_C = sum_a h_a Z_a + sum_{a<a'} J_aa' Z_a Z_a' with h_a = -1/2 sum_a' Q_aa', J = Q/2.
Mixer: transverse field. Parameters optimized with COBYLA on the sampled energy; final bitstrings are
decoded classically. Returns the lowest-energy sample plus diagnostics (energy trace, sample statistics).
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
from scipy.optimize import minimize


@dataclass
class QAOAResult:
    best_w: np.ndarray
    best_energy: float
    energies: List[float] = field(default_factory=list)      # expectation trace during optimization
    samples: Optional[np.ndarray] = None                       # (n_samples, n) distinct samples sorted by energy
    sample_counts: Optional[np.ndarray] = None
    n_qubits: int = 0
    depth: int = 0
    shots: int = 0
    iterations: int = 0
    time_s: float = 0.0
    mean_energy_final: float = np.nan


def _build_hamiltonian(Q: np.ndarray):
    from qiskit.quantum_info import SparsePauliOp
    n = Q.shape[0]
    h = -0.5 * Q.sum(1)
    terms = []
    for a in range(n):
        if abs(h[a]) > 1e-12:
            label = ["I"] * n
            label[n - 1 - a] = "Z"
            terms.append(("".join(label), float(h[a])))
    for a in range(n):
        for b in range(a + 1, n):
            J = 0.5 * Q[a, b]
            if abs(J) > 1e-12:
                label = ["I"] * n
                label[n - 1 - a] = "Z"; label[n - 1 - b] = "Z"
                terms.append(("".join(label), float(J)))
    if not terms:
        terms = [("I" * n, 0.0)]
    return SparsePauliOp.from_list(terms)


def _counts_to_matrix(counts: dict, n: int):
    keys = list(counts.keys())
    W = np.array([[int(k[n - 1 - a]) for a in range(n)] for k in keys], dtype=float)   # qubit a = bit from the right
    c = np.array([counts[k] for k in keys], dtype=float)
    return W, c


def qaoa_qubo(Q: np.ndarray, depth: int = 2, shots: int = 1024, maxiter: int = 200,
              seed: int = 0, final_shots: int = 4096) -> QAOAResult:
    from qiskit import transpile
    from qiskit_aer import AerSimulator
    try:
        from qiskit.circuit.library import qaoa_ansatz as _qaoa
        make_ansatz = lambda H, p: _qaoa(H, reps=p)
    except Exception:  # older qiskit
        from qiskit.circuit.library import QAOAAnsatz
        make_ansatz = lambda H, p: QAOAAnsatz(cost_operator=H, reps=p)

    t0 = time.time()
    n = Q.shape[0]
    scale = float(np.max(np.abs(Q)) + 1e-12)        # normalize angles; Q/scale has the same minimizer
    H = _build_hamiltonian(Q / scale)
    ansatz = make_ansatz(H, depth)
    ansatz.measure_all()
    sim = AerSimulator(method="statevector", seed_simulator=seed)
    circ = transpile(ansatz, sim, optimization_level=1)
    params = list(circ.parameters)
    rng = np.random.default_rng(seed)
    Qs = Q / scale
    energies: List[float] = []

    def sampled_energy(theta, nshots):
        bound = circ.assign_parameters(dict(zip(params, theta)))
        counts = sim.run(bound, shots=nshots).result().get_counts()
        W, c = _counts_to_matrix(counts, n)
        E = np.einsum("ki,ij,kj->k", W, Qs, W)
        return float((E * c).sum() / c.sum()), W, c, E

    def objective(theta):
        e, *_ = sampled_energy(theta, shots)
        energies.append(e)
        return e

    x0 = np.concatenate([rng.uniform(0, np.pi, depth), rng.uniform(0, 2 * np.pi, depth)])[: len(params)]
    if len(x0) < len(params):
        x0 = rng.uniform(0, np.pi, len(params))
    res = minimize(objective, x0, method="COBYLA", options={"maxiter": maxiter, "rhobeg": 0.5})
    e_final, W, c, E = sampled_energy(res.x, final_shots)
    order = np.argsort(E)
    best = W[order[0]]
    out = QAOAResult(best_w=best, best_energy=float(best @ Q @ best), energies=[e * scale for e in energies],
                     samples=W[order], sample_counts=c[order], n_qubits=n, depth=depth, shots=shots,
                     iterations=int(res.nfev), time_s=time.time() - t0, mean_energy_final=e_final * scale)
    return out
