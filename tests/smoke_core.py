"""Smoke test of the optimization core on a small instance (no time-domain simulation)."""
import sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sentinel.config import FullConfig
from sentinel.geometry import build_topology
from sentinel.sources import SourceSet, psi_table, birth_death_matrix, distortion_matrix
from sentinel.scenarios import build_scenarios
from sentinel.problem import build_instance
from sentinel.qubo import build_domain_qubo
from sentinel.solvers.ilp import solve_p3_exact
from sentinel.solvers.sa import anneal_qubo
from sentinel.solvers.exact import brute_force_qubo
from sentinel.solvers.greedy import greedy_assign, local_search
from sentinel.admm import sentinel_solve, _shared_sats
from sentinel.channel import nominal_rate_table

cfg = FullConfig()
cfg.net.num_ues = 6
cfg.net.num_bs = 2
cfg.net.num_sat = 2
n_int = 600
topo = build_topology(cfg.net, seed=1, num_intervals=n_int, interval_s=1.0)
print("UE domains:", topo.domain_of_ue)
vis_frac = topo.sat_visible.mean(axis=(1, 2))
print("satellite visibility fraction over the run per SAT slot:", np.round(vis_frac, 3))
print("elevation range (deg) where visible:", np.round(topo.sat_elev_deg[topo.sat_visible].min(), 1), "-",
      np.round(topo.sat_elev_deg[topo.sat_visible].max(), 1))
rates, vis = nominal_rate_table(topo, 0, cfg.radio)
print("nominal rates at interval 0 (Mbps), level 2.5 MHz, rows=UE, cols=[BS0,BS1,SAT0,SAT1]:")
print(np.round(rates[:, :, 0] / 1e6, 2))
print("need >= %.1f Mbps" % (cfg.src.packet_bits / (cfg.src.slot_ms * 1e-3) / 1e6))

src = SourceSet(cfg.net.num_ues, cfg.src, seed=1)
print("p_stay:", np.round(src.p_stay, 3))
print("Psi(Y)/Y for Y=5,10,20,50 (UE0):", [round(float(src.psi[0, Y] / Y), 3) for Y in (5, 10, 20, 50)])

scen = build_scenarios(cfg.dis, cfg.net.num_sat, 6)
inst = build_instance(cfg, topo, src, scen, interval=0, horizon_intervals=5)
print("instance: vars =", inst.num_vars, " forced fallbacks =", int(inst.forced_fallback.sum()))
for i in range(inst.num_ues):
    idx = inst.vars_of_ue(i)
    print(f"  UE{i}: {len(idx)} admissible combos; nodes {sorted(set(inst.var_node[idx].tolist()))}; min worst cost {inst.cost[idx].max(1).min():.3f}")

t0 = time.time(); ilp = solve_p3_exact(inst); print(f"ILP exact: eta={ilp['eta']:.4f} scen={ilp['scenario']} status={ilp['status']} time={ilp['time_s']:.2f}s")
g = greedy_assign(inst); print("greedy: eta=%.4f feasible=%s" % (inst.worst_case(g)[0], inst.is_feasible(g)))
gl = local_search(inst, g); print("greedy+LS: eta=%.4f feasible=%s" % (inst.worst_case(gl)[0], inst.is_feasible(gl)))

shared = _shared_sats(inst); print("shared SATs:", shared)
z = {int(j): inst.cap_units[j] / 2 for j in shared}; u = {int(j): 0.0 for j in shared}
for k in range(2):
    dq = build_domain_qubo(inst, k, z, u, 1.0, cfg.solver.eta_resolution, shared)
    print(f"domain {k}: n_x={dq.n_x}, qubits={dq.n}, eta_bits={dq.eta_bits}, lambda={dq.lambdas[0]:.1f}, layout={dq.layout}")
    t0 = time.time(); w_sa, e_sa = anneal_qubo(dq.Q, sweeps=200, restarts=2, rng=np.random.default_rng(0)); t_sa = time.time() - t0
    xk = dq.decode(w_sa)
    print(f"   SA: energy={e_sa + dq.const:.2f} locally feasible={dq.local_feasible(xk, inst)} time={t_sa:.2f}s")
    if dq.n <= 20:
        w_bf, e_bf = brute_force_qubo(dq.Q)
        print(f"   brute force: energy={e_bf + dq.const:.2f}  (SA gap {e_sa - e_bf:.2f})")

cfg.solver.solver = "sa"
t0 = time.time(); res = sentinel_solve(inst, cfg.solver, seed=0); print(f"SENTINEL(SA): eta={res.eta:.4f} feasible={res.feasible} rounds={res.rounds} qubits={res.qubits_per_domain} time={res.time_s:.1f}s  gap to ILP={100*(res.eta/ilp['eta']-1):.2f}%")

# tiny QAOA check on a reduced instance: 2 UEs per domain, 2 levels, 2 periods, L=2
cfg2 = FullConfig(); cfg2.net.num_ues = 4; cfg2.net.num_bs = 2; cfg2.net.num_sat = 1
cfg2.radio.bandwidth_levels_mhz = (5.0,); cfg2.src.update_periods_slots = (5, 20); cfg2.solver.eta_resolution = 0.25
topo2 = build_topology(cfg2.net, seed=3, num_intervals=600, interval_s=1.0)
src2 = SourceSet(4, cfg2.src, seed=3)
scen2 = build_scenarios(cfg2.dis, 1, 3)[:2]
k0 = int(np.argmax(topo2.sat_visible[0].all(axis=1)))   # an interval where the SAT sees everyone
inst2 = build_instance(cfg2, topo2, src2, scen2, interval=k0, horizon_intervals=3)
print("\nQAOA test instance: vars =", inst2.num_vars, "domains:", topo2.domain_of_ue, "interval", k0)
ilp2 = solve_p3_exact(inst2); print(f"  ILP exact eta={ilp2['eta']:.4f}")
cfg2.solver.solver = "qaoa"; cfg2.solver.max_qaoa_qubits = 22; cfg2.solver.qaoa_maxiter = 60; cfg2.solver.qaoa_shots = 512
t0 = time.time()
res2 = sentinel_solve(inst2, cfg2.solver, seed=0, check_exact=True)
print(f"  SENTINEL(QAOA): eta={res2.eta:.4f} feasible={res2.feasible} rounds={res2.rounds} qubits={res2.qubits_per_domain} "
      f"time={time.time()-t0:.1f}s local QUBO gaps to brute force={np.round(res2.local_gap_to_exact, 2)} gap to ILP={100*(res2.eta/ilp2['eta']-1):.2f}%")
if res2.qaoa_traces:
    tr = res2.qaoa_traces[0]; print(f"  QAOA energy trace (first domain): start {tr[0]:.1f} -> end {tr[-1]:.1f} over {len(tr)} evals")
print("SMOKE OK")
