"""How often does SA on the penalty QUBO return an exactly feasible (one-hot, capacity-respecting) domain assignment?
Diagnostic for the write-up: sweeps vs one-hot fraction and local feasibility, on one 20-UE domain QUBO."""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.geometry import build_topology
from sentinel.sources import SourceSet
from sentinel.scenarios import build_scenarios
from sentinel.problem import build_instance
from sentinel.qubo import build_domain_qubo
from sentinel.solvers.sa import anneal_qubo
from sentinel.admm import _shared_sats

cfg = configure(FullConfig(), net__num_ues=20, net__num_bs=2, net__num_sat=2)
topo = build_topology(cfg.net, 1, 120, 1.0); src = SourceSet(20, cfg.src, 1)
k = int(np.argmax(topo.sat_visible.sum(axis=(0, 2))))
for L in (1, 6):
    inst = build_instance(cfg, topo, src, build_scenarios(cfg.dis, 2, L), k, 3)
    shared = _shared_sats(inst)
    z = {int(j): inst.cap_units[j] / 2 for j in shared}; u = {int(j): 0.0 for j in shared}
    dq = build_domain_qubo(inst, 0, z, u, 1.0, cfg.solver.eta_resolution, shared)
    print(f"L={L}: domain 0 has {len(dq.ue_list)} UEs, n_x={dq.n_x}, qubits={dq.n}, eta_bits={dq.eta_bits}, lambda={dq.lambdas[0]:.0f}")
    for sweeps in (400, 2000, 8000):
        t0 = time.time()
        feas, onehot, energies = [], [], []
        for r in range(5):
            w, e = anneal_qubo(dq.Q, sweeps=sweeps, restarts=1, rng=np.random.default_rng(r))
            xk = dq.decode(w)
            cnt = np.bincount(inst.var_ue[dq.x_vars], weights=xk, minlength=inst.num_ues)[dq.ue_list]
            onehot.append((cnt == 1).mean()); feas.append(dq.local_feasible(xk, inst)); energies.append(e + dq.const)
        print(f"   sweeps={sweeps:>5}: one-hot UEs {100*np.mean(onehot):5.1f}%  locally feasible {100*np.mean(feas):5.1f}%  "
              f"best energy {min(energies):8.1f}  mean energy {np.mean(energies):8.1f}  ({(time.time()-t0)/5:.1f}s per run)")
