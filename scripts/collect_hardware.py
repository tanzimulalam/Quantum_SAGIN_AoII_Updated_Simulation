"""Collect every run under results/hardware/ into one table (results/hardware/runs.csv and runs.md).

One row per (run, domain): backend, instance (UEs, seed), qubits, two-qubit gates, depth, shots, fraction of samples
that decode to one-hot and capacity-feasible assignments, whether the best sample equals the noiseless optimum, the
decoded network schedule's eta against the exact ILP, and the QPU seconds reported by the service.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
HW = ROOT / "results" / "hardware"


def main():
    rows = []
    for d in sorted(HW.iterdir()):
        f = d / "summary.json"
        if not d.is_dir() or not f.exists():
            continue
        s = json.loads(f.read_text(encoding="utf-8"))
        seed = int(d.name.split("_s")[-1].split("_")[0]) if "_s" in d.name else None
        for dom in s["domains"]:
            if "hw_feasible_sample_fraction" not in dom:
                continue
            rows.append({
                "run": d.name, "mode": s["mode"], "backend": s["backend"], "ues": s["ues"], "seed": seed,
                "domain": dom["domain"], "qubits": dom["n_qubits"], "two_qubit_gates": dom["two_qubit_gates"],
                "depth": dom["transpiled_depth"], "shots": s["shots"],
                "feasible_frac": dom["hw_feasible_sample_fraction"],
                "best_matches_noiseless": bool(dom.get("hw_matches_sim_best", False)),
                "hw_best_energy": dom["hw_best_energy"], "sim_best_energy": dom["sim_best_energy"],
                "hw_mean_energy": dom.get("hw_mean_qubo_energy"),
                "ilp_eta": s["ilp_eta"], "hw_schedule_eta": s.get("hw_schedule_eta"),
                "gap_pct": s.get("hw_gap_pct_vs_ilp"), "feasible_schedule": s.get("hw_schedule_feasible"),
                "job_id": s.get("job_id"), "qpu_s": s.get("usage_s"),
            })
    df = pd.DataFrame(rows).sort_values(["mode", "ues", "seed", "domain", "backend"]).reset_index(drop=True)
    df.to_csv(HW / "runs.csv", index=False)
    dev = df[df["mode"] == "device"]
    md = ["# Hardware runs", "", "## Real device", "",
          "| run | backend | UEs | seed | domain | qubits | 2q gates | depth | shots | feasible shots | best = noiseless opt | schedule gap vs ILP | QPU s | job |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in dev.iterrows():
        gap = f"{r.gap_pct:+.2f}%" if pd.notna(r.gap_pct) else "n/a"
        md.append(f"| {r.run} | {r.backend} | {r.ues} | {r.seed} | {r.domain} | {r.qubits} | {r.two_qubit_gates} | {r.depth} | {r.shots} | "
                  f"{100*r.feasible_frac:.1f}% | {'yes' if r.best_matches_noiseless else 'no'} | {gap} | {r.qpu_s} | {r.job_id} |")
    if len(dev):
        md += ["", f"Device domains sampled: {len(dev)}; best sample equals the noiseless optimum in "
               f"{int(dev.best_matches_noiseless.sum())} of {len(dev)}; total QPU time {dev.drop_duplicates('job_id').qpu_s.fillna(0).sum():.0f} s over {dev.job_id.nunique()} jobs; "
               f"feasible-shot fraction {100*dev.feasible_frac.min():.1f}% to {100*dev.feasible_frac.max():.1f}%."]
    fake = df[df["mode"] == "fake"]
    md += ["", "## Noise models (offline)", "",
           "| run | backend | UEs | seed | domain | qubits | 2q gates | depth | shots | feasible shots | best = noiseless opt | schedule gap vs ILP |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in fake.iterrows():
        gap = f"{r.gap_pct:+.2f}%" if pd.notna(r.gap_pct) else "n/a"
        md.append(f"| {r.run} | {r.backend} | {r.ues} | {r.seed} | {r.domain} | {r.qubits} | {r.two_qubit_gates} | {r.depth} | {r.shots} | "
                  f"{100*r.feasible_frac:.1f}% | {'yes' if r.best_matches_noiseless else 'no'} | {gap} |")
    (HW / "runs.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
