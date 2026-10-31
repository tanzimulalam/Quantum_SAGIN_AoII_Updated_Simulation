"""Figure: probability that an XY-QAOA sample is an optimal assignment versus shots, depth and initial state.

Reads results/qaoa_depth_shots.csv (scale_mode 'max'), averages over seeds, domains and restarts, and writes
figures/qaoa_depth_shots.pdf/.png with clean log-x ticks at the shot counts actually used.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import NullFormatter

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 150})


def main():
    d = pd.read_csv(ROOT / "results" / "qaoa_depth_shots.csv")
    d = d[d.scale_mode == "max"]
    shots = sorted(d.shots.unique())
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    styles = {("greedy", 1): ("#1f77b4", "o", "-"), ("greedy", 2): ("#ff7f0e", "s", "-"),
              ("w", 1): ("#2ca02c", "o", "--"), ("w", 2): ("#d62728", "s", "--")}
    for (init, depth), (c, m, ls) in styles.items():
        s = d[(d.init == init) & (d.depth == depth)].groupby("shots").p_optimal_sample
        ax.errorbar(shots, s.mean().reindex(shots), yerr=s.sem().reindex(shots), color=c, marker=m, ls=ls, ms=4, capsize=2,
                    label=f"{'greedy start' if init == 'greedy' else '$W$-state start'}, depth {depth}")
    ax.axhline(d.p_uniform.mean(), color="k", ls=":", lw=1, label="uniform over one-hot subspace")
    ax.set_xscale("log"); ax.set_xticks(shots); ax.set_xticklabels([str(x) for x in shots]); ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Shots per optimizer evaluation"); ax.set_ylabel("P(sample is an optimal assignment)")
    ax.set_ylim(0, 1.05); ax.legend(fontsize=7, loc="center right", frameon=False)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "qaoa_depth_shots.pdf"); fig.savefig(ROOT / "figures" / "qaoa_depth_shots.png")
    print("written")


if __name__ == "__main__":
    main()
