"""Checks on the XY-QAOA circuit: W-state preparation is exact, and every sampled state is one-hot per UE group."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.compact import prune_candidates, build_compact_qubo, _shared_sats
from sentinel.solvers.qaoa_xy import _prepare_w_state, build_xy_circuit, decode_xy_counts
from run_validation import make_instance

# 1) W-state preparation
for m in (2, 3, 4, 5, 6):
    qc = QuantumCircuit(m); _prepare_w_state(qc, list(range(m)))
    sv = Statevector(qc).data
    probs = np.abs(sv) ** 2
    onehot_idx = [1 << j for j in range(m)]
    assert abs(probs[onehot_idx].sum() - 1.0) < 1e-9, f"W state leaks outside one-hot subspace for m={m}"
    assert np.allclose(probs[onehot_idx], 1.0 / m, atol=1e-9), f"W state not uniform for m={m}: {probs[onehot_idx]}"
print("W-state preparation exact for m = 2..6")

# 2) one-hot invariance of the full circuit under random angles, for both initial states
cfg = configure(FullConfig(), net__num_ues=6, net__num_bs=2, net__num_sat=2, net__num_domains=2)
inst = prune_candidates(make_instance(cfg, 1, 6), 4)
shared = _shared_sats(inst)
w = np.ones(6) / 6
z = {int(j): inst.cap_units[j] / 2 for j in shared}; u = {int(j): 0.0 for j in shared}
sim = AerSimulator(seed_simulator=3)
rng = np.random.default_rng(0)
for k in range(2):
    dq = build_compact_qubo(inst, k, w, z, u, 0.0, shared, onehot_penalty=False)
    greedy = np.array([g[0] for g in dq.groups])
    for init in ("w", "greedy"):
        for depth in (1, 2):
            qc, gammas, betas, _ = build_xy_circuit(dq, depth=depth, init=init, warm_start_sel=greedy)
            vals = {p: rng.uniform(0, 2 * np.pi) for p in qc.parameters}
            tqc = transpile(qc.assign_parameters(vals), sim)
            counts = sim.run(tqc, shots=2000).result().get_counts()
            best_sel, best_e, e_mean, onehot_frac, feas_frac = decode_xy_counts(dq, inst, counts)
            assert onehot_frac == 1.0, f"one-hot violated: domain {k} init {init} depth {depth}: {onehot_frac}"
            print(f"domain {k}: {dq.n} qubits, init={init}, depth={depth}: one-hot fraction {onehot_frac:.3f}, capacity-feasible fraction {feas_frac:.3f}")
print("PASS: XY-mixer circuits keep every UE group exactly one-hot")
