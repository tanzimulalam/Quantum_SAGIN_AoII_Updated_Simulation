"""The five data figures of the manuscript (Figs. 2 to 6), drawn at the size at which the paper includes them so that
no scaling is applied: IEEE column width (3.5 in) for the three bar charts, 0.66 and 0.72 of it for the scatter plot
and the line plot. Times text at 7 to 8 pt, grayscale fills with hatching and distinct markers, so the figures print
in black and white. Reads the same summary and raw CSVs as make_figures.py (results/sweeps_tle_ntn_*.csv and
results/sweeps_tle_ntn_noack_summary.csv) and writes paper/figures/*.pdf, with PNG previews in figures/paper/.
"""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES, OUT, PREV = ROOT / "results", ROOT / "paper" / "figures", ROOT / "figures" / "paper"
COL = 3.5  # IEEE column width in inches

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "STIXGeneral", "DejaVu Serif"], "mathtext.fontset": "stix",
    "font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.8,
    "axes.linewidth": 0.6, "xtick.major.width": 0.5, "ytick.major.width": 0.5, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "ytick.minor.size": 1.5, "ytick.minor.width": 0.4, "xtick.minor.size": 1.5, "xtick.minor.width": 0.4,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": "0.82", "grid.linewidth": 0.4, "axes.axisbelow": True,
    "hatch.linewidth": 0.5, "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.dpi": 300,
    "legend.frameon": False, "legend.handlelength": 1.5, "legend.handleheight": 0.8, "legend.handletextpad": 0.5,
    "legend.columnspacing": 0.9, "legend.labelspacing": 0.25, "legend.borderaxespad": 0.2,
    "lines.linewidth": 0.9, "lines.markersize": 3.2,
})

POLICY_ORDER = ["random", "ppo", "whittle", "threshold", "nominal", "sentinel", "sentinel_triggered", "sentinel_capped_trigger"]
LABEL = {"random": "Random", "ppo": "PPO (trained)", "whittle": "Whittle index", "threshold": "AoII threshold",
         "nominal": "Nominal SENTINEL", "sentinel": "SENTINEL (robust)",
         "sentinel_triggered": "SENTINEL + state trigger", "sentinel_capped_trigger": "SENTINEL + capped trigger"}
# grayscale fills: baselines light, the SENTINEL family dark
FILL = {"random": dict(facecolor="white", hatch=""), "ppo": dict(facecolor="white", hatch="////"),
        "whittle": dict(facecolor="0.85", hatch=""), "threshold": dict(facecolor="0.85", hatch="\\\\\\\\"),
        "nominal": dict(facecolor="0.6", hatch=""), "sentinel": dict(facecolor="black", hatch=""),
        "sentinel_triggered": dict(facecolor="0.6", hatch="xxxx"), "sentinel_capped_trigger": dict(facecolor="white", hatch="++")}
TOPO_ORDER = ["Ground only (2 BS)", "Satellite only (2 SAT)", "Integrated (1 BS + 1 SAT)", "Integrated (2 BS + 2 SAT)",
              "Integrated (3 BS + 3 SAT)"]
TOPO_TICK = {"Ground only (2 BS)": "Ground only\n(2 BS)", "Satellite only (2 SAT)": "SAT only\n(2 SAT)",
             "Integrated (1 BS + 1 SAT)": "Integrated\n1 BS + 1 SAT", "Integrated (2 BS + 2 SAT)": "Integrated\n2 BS + 2 SAT",
             "Integrated (3 BS + 3 SAT)": "Integrated\n3 BS + 3 SAT"}
ERR = dict(ecolor="black", elinewidth=0.6, capsize=1.5, capthick=0.6)


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    PREV.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(PREV / f"{name}.png")
    plt.close(fig)
    print("written", OUT / f"{name}.pdf")


def median_iqr(sub, metric="average_aoii"):
    y = sub[f"{metric}_median"]
    yerr = np.vstack([y - sub[f"{metric}_q25"], sub[f"{metric}_q75"] - y]).clip(min=0)
    return y, yerr


def bar_chart(summ, sweep, name, xlabel, height, xtick=None, legend_rows=3):
    """Grouped bars of the median average AoII (IQR whiskers) per policy, log scale, legend below the axes."""
    d = summ[(summ.sweep == sweep) & (summ.disruption_mode == "on")].copy()
    if sweep == "ue_sweep":
        d["x_value"] = pd.to_numeric(d.x_value)
        xs = sorted(d.x_value.unique())
    else:
        xs = [x for x in TOPO_ORDER if x in set(d.x_value)]
    pols = [p for p in POLICY_ORDER if p in d.policy.unique()]
    fig, ax = plt.subplots(figsize=(COL, height), layout="constrained")
    w = 0.86 / len(pols)
    for i, p in enumerate(pols):
        sub = d[d.policy == p].set_index("x_value").reindex(xs)
        y, yerr = median_iqr(sub)
        ax.bar(np.arange(len(xs)) + (i - (len(pols) - 1) / 2) * w, y, w, yerr=yerr, error_kw=ERR,
               edgecolor="black", linewidth=0.5, label=LABEL[p], **FILL[p])
    ax.set_yscale("log")
    lo, hi = d["average_aoii_q25"].min(), d["average_aoii_q75"].max()
    ax.set_ylim(10 ** np.floor(np.log10(0.9 * lo)), 1.6 * hi)
    ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(base=10, numticks=6))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xticks(np.arange(len(xs)))
    ax.set_xticklabels([xtick[x] if xtick else str(x) for x in xs])
    ax.set_xlim(-0.55, len(xs) - 0.45)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Average AoII")
    ax.tick_params(axis="x", length=0)
    ncol = int(np.ceil(len(pols) / legend_rows))
    fig.legend(loc="outside lower center", ncol=ncol)
    save(fig, name)


def certificate_scatter(raw, name):
    """Certified worst case against realized average AoII per orchestration run, robust and nominal SENTINEL."""
    d = raw[(raw.sweep == "ue_sweep") & (raw.disruption_mode == "on") & raw.policy.isin(["sentinel", "nominal"])]
    fig, ax = plt.subplots(figsize=(0.66 * COL, 1.5), layout="constrained")
    ax.grid(True, axis="both")
    s = d[d.policy == "nominal"]
    ax.scatter(s.certified_eta_mean, s.average_aoii, s=10, facecolors="white", edgecolors="0.3", linewidths=0.5,
               label="Nominal SENTINEL", zorder=3)
    s = d[d.policy == "sentinel"]
    ax.scatter(s.certified_eta_mean, s.average_aoii, s=7, c="black", linewidths=0, label="SENTINEL (robust)", zorder=4)
    lim = max(d.certified_eta_mean.max(), d.average_aoii.max()) * 1.05
    ax.plot([0, lim], [0, lim], color="black", ls="--", lw=0.7, label="realized = certified")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_xlabel("Certified worst-case AoII")
    ax.set_ylabel("Realized average AoII")
    ax.legend(loc="upper left")
    save(fig, name)


def capacity_lines(summ, name):
    """Median average AoII at 20 UEs against the bandwidth per node, log-log, one line per per-slot policy."""
    d = summ[(summ.sweep == "capacity_limited") & (summ.disruption_mode == "on")].copy()
    d["x_value"] = pd.to_numeric(d.x_value)
    xs = sorted(d.x_value.unique())
    style = {"random": dict(color="0.55", marker="o", ls="-"), "whittle": dict(color="black", marker="s", ls="-"),
             "threshold": dict(color="black", marker="^", ls="--")}
    fig, ax = plt.subplots(figsize=(0.72 * COL, 1.5), layout="constrained")
    ax.grid(True, axis="both")
    for p in [p for p in POLICY_ORDER if p in d.policy.unique()]:
        sub = d[d.policy == p].set_index("x_value").reindex(xs)
        y, yerr = median_iqr(sub)
        ax.errorbar(xs, y, yerr=yerr, label=LABEL[p], markerfacecolor="white" if p == "threshold" else None,
                    **ERR, **style.get(p, {}))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(xs)
    ax.set_xticklabels([f"{x:g}" for x in xs])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Bandwidth per node (MHz), 20 UEs")
    ax.set_ylabel("Average AoII")
    ax.legend(loc="upper right")
    save(fig, name)


def main():
    summ = pd.read_csv(RES / "sweeps_tle_ntn_summary.csv")
    raw = pd.read_csv(RES / "sweeps_tle_ntn_raw.csv")
    noack = pd.read_csv(RES / "sweeps_tle_ntn_noack_summary.csv")
    bar_chart(summ, "ue_sweep", "ue_sweep_average_aoii_median_disruption_on", "Number of UEs", 1.5)          # Fig. 2
    certificate_scatter(raw, "certificate_vs_realized")                                                        # Fig. 3
    bar_chart(noack, "ue_sweep", "noack_ue_sweep_average_aoii_median", "Number of UEs", 1.5)                  # Fig. 4
    bar_chart(summ, "topology", "topology_average_aoii_median", "Deployment at 10 UEs", 1.65, xtick=TOPO_TICK)  # Fig. 5
    capacity_lines(summ, "capacity_average_aoii")                                                              # Fig. 6


if __name__ == "__main__":
    main()
