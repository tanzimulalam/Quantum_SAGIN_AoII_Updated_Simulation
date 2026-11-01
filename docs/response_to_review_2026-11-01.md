# Response to the review comments of 31 October 2026

Point-by-point record of what was changed in the manuscript (`paper/`) and what was run to support it. Numbers quoted
here come from `RESULTS.md`, `results/hardware/runs.md`, `results/certificate_tightness.csv` and
`results/sweeps_tle_ntn_noack_paired_stats.md`.

## 1. Quantum framing and terminology

- **Hybrid.** The abstract, the introduction (new paragraph after the SENTINEL description), the start of Section V,
  and Section VI-A now say explicitly that the procedure is hybrid at three levels (classical angle optimizer; classical
  scenario weights, ADMM, repair and certificate; classical annealer for domains beyond the sampler) and that every
  network-level result of Section VI was produced with the annealer as the inner solver, because the domains of 5 to
  20 UEs span 12 to 76 qubits and are re-solved hundreds of times per run. XY-QAOA is validated against the annealer
  and the exact optimum on domains up to 24 qubits (VI-D) and run on hardware (VI-E). This is stated, not implied.
- **"Distributed quantum computing."** The phrase did not occur in the revised draft; the text speaks of domains
  coordinated classically by ADMM.
- **SAGIN.** Replaced by "satellite-ground integrated network (SGIN)" throughout, with a defining sentence in the
  introduction stating that there is no aerial layer. The title keeps "Satellite-Ground", which the acronym now
  matches. (STIN would also be accurate; SGIN was chosen to match the title wording.)

## 2. Major issues

- **Hardware result close to trivial.** Agreed. Three things were done. (i) Every saved device run was re-analysed
  against the enumerated optimal set of its domain (`sentinel/sample_stats.py`, `hardware_run.py --reanalyze`): the
  probability that a shot is an optimal assignment, the probability of the optimum given a feasible shot, the mean
  approximation ratio over feasible shots, and the same quantities under uniform sampling of the feasible one-hot
  set. (ii) The energy spread of each domain's feasible set is reported, because several hardware-sized domains turned
  out to be nearly flat (all feasible assignments within 2% of the optimum), which the earlier text did not reveal.
  (iii) W-state (no warm start) runs of the same domains on the same device were added. Section VI-E and the device
  table now report these per-shot statistics side by side. With the greedy start, P(optimal shot) is 0.32 to 0.85 on
  the 6-UE domains against 0.016 to 0.25 for uniform feasible sampling, and 0.006 at 38 qubits, equal to the uniform
  baseline. The text says plainly that the greedy-start result is retention of an already-optimal warm start under
  noise, not a search. From the W state (no warm start; run on the same processor as the greedy start), the device behaves as a uniform sampler of the feasible set: P(optimal | feasible) is 0.03 to 0.33 against the uniform 0.06 to 0.25 of the same run (each run re-solves the scenario weights, and on the two seed-2 domains this changes the optimal set, so the table lists the uniform baseline per run), between 0.52 and 2.04 times the uniform value on every 6-UE domain, and the approximation ratio of feasible shots exceeds the uniform value by at most 0.07; at 38 qubits no feasible shot was optimal. The paper now says that the 1.3-fold concentration of one noiseless layer is lost to hardware noise and that the schedule-level optimum is reached only because the decoder keeps the best of thousands of shots over small feasible sets. All 13 domains were run from the W state on both ibm_fez and ibm_kingston, and the two processors agree (ibm_fez: P(optimal | feasible) 0.04 to 0.33, approximation ratio within +0.05 of uniform; ibm_kingston: 0.03 to 0.37 and within +0.07). On the same processor the W-state circuits have the same feasible-shot fraction as the greedy-start circuits despite 13 to 113 more two-qubit gates, so the lower ibm_fez yields are a device effect, not a depth effect. The device table pairs each greedy-start run with the W-state run on the same processor, and VI-E quotes the ranges of that pairing.
- **"Exact through 25 UEs" versus Table V.** The claim was overstated. Validation D (20 UEs, scenario-count instances)
  has the compact pipeline at 3.2% (L = 3) and 6.9% (L = 5), optimal on 90% and 60% of those instances. The abstract,
  introduction, Section V-F, Section VI-D and the conclusion now say: exact on all 10- and 25-UE instances and on the
  20-UE severity instances, within 3 to 7% on the 20-UE scenario-count instances, within 12% at 50 UEs.
- **Qubit-reduction factor.** Unified to "four to six times" everywhere (10 to 100 UEs: compact 44/78/50-59/87-161/
  156-171 qubits per domain against epigraph 213/353/248-261/417-842/1038). Section V-C now states that the 22/34/
  46/58 counts are the time-domain instances, the 44 and 78 counts are the validation instances with other
  topologies and candidate sets, and that the ratio is larger below 10 UEs where the epigraph's fixed registers
  dominate (Table V's 8 to 24 against 133 to 193). The introduction's "three to four auxiliary qubits per decision
  qubit" was wrong and is replaced by a description of what the epigraph encoding adds.
- **"+ trigger" and the certificate.** Option 2 adopted. Section VI-B states that the certificate is proved for the
  periodic schedule, that the triggered variant's deliveries are state-dependent so the renewal argument does not
  cover it, and that it is checked empirically: its realized average stayed within the certificate of the schedule it
  runs on in 97.9 to 98.7% of epochs.
- **Certificate looseness.** A per-epoch diagnostic was run (`tests/diag_certificate_tightness.py`, 120 runs, 3975
  epochs). Section VI-B now reports the tightness ratio (median 17, IQR 13 to 23), the violation rate (1.3% of epochs),
  the size of violations (realized/certified median 1.2 to 2.1, maximum 5.4), and the cause of the looseness (each
  scenario applies its outage to every inter-delivery interval of the epoch, a persistent disruption, whereas realized
  disruptions are intermittent).
- **Whittle in the no-feedback comparison.** The Whittle policy was run on the 60-seed no-feedback sweep. It
  coincides with the threshold policy there as well (identical decisions), so the "25 to 30% better than the best
  per-slot heuristic" statement holds against both; Section VI-B names both policies and gives the Holm-corrected p
  values against each (0.023/0.029 threshold, 0.034/0.043 Whittle at 15/20 UEs). Fig. 4 now includes Whittle.
- **Solver per result.** Section VI-A opens with the statement that all network-level results used the annealer, and
  why; the validation table says which rows are QAOA.
- **Abstract length.** Rewritten to about 240 words (number-dense middle removed).
- **Greedy association.** Defined in Section V-C ("Greedy assignment" paragraph) where it is first used: UEs in
  decreasing order of candidate-cost spread, each takes its cheapest candidate whose node still has capacity. The
  warm-start reference now points to that paragraph (`\ref`), not to V-E.

## 3. Captions

All suggested captions adopted (Fig. 2, 3, 4, 5, 6 and Tables II, III, V). Findings moved to the text; the hardware
table's parameters ($\varkappa=4$, depth 1, greedy start, 4096 shots, optimization level 3) moved into the first
sentence of VI-E. Fig. 3's caption now says "per orchestration run" and the text distinguishes the per-run plot from
the per-epoch 98.7% statistic.

## 4. Smaller items

- Notation: pruning size $\kappa \to \varkappa$ (delivery index keeps $\kappa$); weight-update step $\sigma \to \mu$
  (Pauli $\sigma^{x,z}$ and $\sigma_{\mathrm{sf}}$ unchanged); ADMM dual $u_{jk} \to \upsilon_{jk}$ (and
  $\boldsymbol{\upsilon}_k$); ADMM penalty $\varrho \to \lambda_{\mathrm{c}}$; weighted cost $a_v \to \bar\psi_v$;
  AoII lag $a \to \iota$ in (6). Table I updated. The qubit index $a$ no longer clashes with anything.
- VANGUARD expansion: "Volatility-Aware Network-wide Generation, Update, Association, and Resource orchestration under
  Disruption" (every letter contributes; no VoI). SENTINEL expanded at first use: "Satellite-ground Edge Network
  orchestration for Trustworthy Information via Node-level Estimation Limits".
- Conclusion: "fail for minutes at a time" replaced by "for a fraction of a second at each handover and for a whole pass
  under blockage".
- PPO: "is close to the nominal schedule at 5 UEs (0.280 against 0.253, 11% worse)". One sentence added to the
  baselines paragraph justifying the once-per-interval, equal-sharing, source-blind design (it isolates the decision
  rule; the per-slot source-observing role is filled by the threshold and Whittle policies).
- Section references: all internal references now use `\ref` with labels on every section and subsection.
- "Fig." at the beginning of a sentence: replaced by "Figure" in the five places it occurred.
- Fig. 1 redrawn (`scripts/draw_system_model.py`): two domains, base stations with edge servers, shared LEO
  satellites with a handover, monitored Markov sources, a blocked NLOS pass, and the classical coordinator.

## Verified as correct by the reviewer and left unchanged

Ising coefficients, the taboo-matrix AoII expression, and the proof of Proposition 1.
