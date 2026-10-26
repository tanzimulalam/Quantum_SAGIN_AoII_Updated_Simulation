"""Transpiled size of the XY-QAOA circuits on a Heron fake backend, before/after the W-state and one-hot changes."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import numpy as np
from qiskit import transpile
import qiskit_ibm_runtime.fake_provider as fp
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.compact import prune_candidates, build_compact_qubo, _shared_sats
from sentinel.solvers.qaoa_xy import build_xy_circuit
from run_validation import make_instance

backend = fp.FakeTorino()
for U in (6, 10, 16):
    cfg = configure(FullConfig(), net__num_ues=U, net__num_bs=2, net__num_sat=2, net__num_domains=2)
    inst = prune_candidates(make_instance(cfg, 1, 6), 4)
    shared = _shared_sats(inst)
    w = np.ones(6) / 6
    z = {int(j): inst.cap_units[j] / 2 for j in shared}; u = {int(j): 0.0 for j in shared}
    for k in range(2):
        for onehot in (True, False):
            dq = build_compact_qubo(inst, k, w, z, u, 0.0, shared, onehot_penalty=onehot)
            for init in ("w", "greedy"):
                qc, g, b, sc = build_xy_circuit(dq, depth=1, init=init, warm_start_sel=np.array([grp[0] for grp in dq.groups]))
                tqc = transpile(qc, backend, optimization_level=3, seed_transpiler=1)
                two_q = sum(1 for ins in tqc.data if ins.operation.num_qubits == 2)
                nz = int(np.count_nonzero(np.triu(dq.Q, 1)))
                print(f"U={U:>2} domain {k}: {dq.n:>2} qubits, {nz:>3} ZZ couplings, onehot_penalty={onehot!s:5}, init={init:6}: "
                      f"{two_q:>4} two-qubit gates, depth {tqc.depth():>4}", flush=True)
