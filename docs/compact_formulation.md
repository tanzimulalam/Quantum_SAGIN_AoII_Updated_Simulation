# Compact (slack-free) robust formulation and the quantum-ready pipeline

This note gives the mathematics behind `sentinel/compact.py` and `sentinel/solvers/qaoa_xy.py`, in the notation of
the manuscript, so that Section V can be rewritten around it. It replaces the epigraph-and-slack QUBO of the current
Section V-A while keeping the problem P2, the robust pre-elimination, the ADMM coordination, and the exact worst-case
certificate unchanged.

## 1. Why the epigraph encoding cannot run on a quantum device

The current QUBO carries, per domain, M_eta epigraph bits plus L x M_eta scenario-slack bits plus capacity-slack
bits. With L = 6 and Delta_eta = 0.05 this is about 50 auxiliary qubits before a single decision qubit, and the
equality-with-slack penalties produce an energy landscape in which single-flip search never reaches an exactly
feasible state (0 of 50 solves in the validation). Reducing Delta_eta to fit a qubit budget destroys solution quality
(226 to 266 percent gaps at 5 to 6 UEs). The problem is structural.

## 2. Scenario-weight dualization of the minimax

P2 minimizes max_l c_l(x) with c_l(x) = (1/|U|) sum_i sum_(m,q,h) psi_imqh^(l) x_imqh linear in x. For any weight
vector w in the probability simplex Delta_L,

    max_l c_l(x) = max_{w in Delta_L} sum_l w_l c_l(x),

so P2 equals min_x max_w w^T c(x). Exchanging the order gives the dual lower bound max_w min_x w^T c(x), and the
standard subgradient / exponentiated-gradient scheme on w recovers the minimax value to within the duality gap, which
for this finite problem we close by keeping the best certified primal iterate:

    for t = 1..T:
        x_t  <- argmin_x  sum_l w_l^(t) c_l(x)      s.t. D1 (one-hot), D2-D3 (capacity)        [inner problem]
        eta_t <- max_l c_l(x_t)                                                                   [exact certificate]
        w^(t+1) <- w^(t) * exp(step * c(x_t) / eta_t), renormalized                              [push weight to the worst scenarios]
    return the x_t with the smallest eta_t

The inner problem has a **linear** objective over the decision variables. No epigraph variable, no scenario slacks.
Every x_t is certified exactly by eta_t, so the returned schedule's worst-case guarantee is identical in nature to the
one the manuscript already claims; only the way the solver searches for it changes. In the validation (T = 8,
step = 2) the dual loop reached the exact ILP optimum at 10, 20 and 50 UEs.

## 3. Candidate pruning

The robust pre-elimination of Section IV-A removes infeasible combinations; we additionally keep only the k_cand
admissible combinations of each UE with the smallest worst-case cost, plus one combination per distinct node so that
the capacity coupling is preserved. With k_cand = 4 the exact optimum of the pruned instance equalled the exact
optimum of the full instance on every tested instance (10 to 100 UEs), while the decision-qubit count per UE drops
from Q x H x |M| = 36 to at most 4 to 6. The paper should report this as part of the pre-elimination.

## 4. The compact domain QUBO

For domain k with scenario weights w and ADMM targets (z, u), the inner problem is the QUBO over
w_k = (x_k, nu_k) with

    F_k = sum_v a_v x_v                                        a_v = (1/|U|) sum_l w_l psi_v^(l)           (weighted cost)
        + lambda_cap sum_{m in own nodes} (b_m(x_k) + nu_m - B_m)^2                                       (capacity, binary slack nu_m)
        + (rho/2) sum_{j shared} (b_j(x_k) - z_jk + u_jk)^2                                                (ADMM coordination)

The one-hot constraint D1 is **not** penalized: it is enforced by the mixer (Section 5). Because x_v x_v' = 0 for two
candidates of the same UE on the one-hot subspace, their couplings carry no energy and are dropped from Q, which
removes a large share of the ZZ terms. Qubits per domain: sum_i |A_i^k| (at most k_cand + nodes per UE) plus
ceil(log2(B_m + 1)) slack bits per own node (4 bits for a 20 MHz BS at 2.5 MHz resolution). The 5 to 20 UE sweeps
need 30 to 60 qubits per domain with K = 2, versus 120 to 260 with the epigraph encoding.

The penalty weight follows Proposition 1 with the ADMM term bounded over one-hot assignments (each UE selects one
candidate), not over the whole hypercube; the proof only needs the bound at a feasible point and the hypercube bound
inflates lambda by about 50x.

## 5. XY mixers and warm start

The mixer on the decision qubits of UE i is the ring XY Hamiltonian

    H_M^(i) = sum_{(a,b) adjacent in the ring of A_i} (X_a X_b + Y_a Y_b) / 2,

which commutes with the Hamming weight of the group; every term conserves it individually, so the Lie-Trotter
synthesis of exp(-i beta H_M^(i)) keeps one-hot states one-hot exactly. Capacity-slack qubits use the usual
transverse-field mixer. Two initial states are supported: the W state of each group (uniform superposition of its
one-hot states, prepared with a linear-depth ladder of CRY and CX gates) or the greedy assignment's basis state
(warm start, zero preparation cost). The QAOA angles are optimized on a simulator with COBYLA on the sampled energy
and reused across outer iterations; sampled bitstrings are decoded classically and the best capacity-feasible sample
is taken. In the validation 100 percent of samples were one-hot and capacity-feasible, and the compact QAOA matched
the exact optimum on every 4 to 6 UE instance (8 to 20 qubits per domain).

## 6. ADMM coordination (two fixes to Algorithm 1)

1. **Warm start.** Round 0 solves the domains uncoupled (rho = 0) and initializes the targets z_jk from the resulting
   loads projected onto capacity. Initializing z_jk = B_j / K_j and penalizing deviation in both directions, as
   Algorithm 1 does, pulls every domain toward using exactly its equal share of every shared satellite and produced
   schedules 60 to 560 percent above the optimum at 50 to 100 UEs.
2. **Scaled rho.** rho is set to rho_0 times the mean per-UE spread of the weighted costs, so one bandwidth unit of
   deviation at a shared satellite costs about one typical per-UE cost difference; residual balancing adapts it from
   there. With rho = 1 in cost units of about 0.01 to 0.1 the quadratic term dominated the objective completely.

With both fixes the compact pipeline matched the exact ILP at 20 and 50 UEs for K = 2 and K = 4; at 100 UEs with
K = 8 it remains about 30 percent above the optimum after 20 rounds per outer iteration, which is the scale limit to
report.

## 7. Hardware protocol (IBM Quantum Open Plan, 10 min QPU per 28 days)

All optimization (weights, targets, angles) runs on the simulator. For each domain a single sampling job with the
optimized angles (4096 shots, a few seconds of QPU time) is submitted; the device counts are decoded with the same
classical decoder, the network schedule is assembled, and its worst case is evaluated exactly. Report, per domain:
qubits, two-qubit gates after transpilation, depth, the fraction of one-hot and capacity-feasible device samples, and
the worst-case AoII of the device-decoded schedule against the simulator and the exact ILP. A noisy-simulator run on
the device's fake backend (noise model) is reported alongside as the expected baseline.
