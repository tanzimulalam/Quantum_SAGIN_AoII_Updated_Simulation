"""Figures and tables from results/*.csv -> figures/*.pdf|png and results/tables.md"""
import sys, pathlib, json, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES, FIG = ROOT / "results", ROOT / "figures"
FIG.mkdir(exist_ok=True)

POLICY_ORDER = ["random", "ppo", "whittle", "threshold", "nominal", "sentinel", "sentinel_triggered", "sentinel_capped_trigger"]
TOPO_ORDER = ["Ground only (2 BS)", "Satellite only (2 SAT)", "Integrated (1 BS + 1 SAT)", "Integrated (2 BS + 2 SAT)", "Integrated (3 BS + 3 SAT)"]
POLICY_LABEL = {"random": "Random", "ppo": "PPO (AoII reward, trained)", "whittle": "Whittle index (state-aware)", "threshold": "AoII threshold (state-aware)", "nominal": "Nominal (non-robust) SENTINEL",
                "sentinel": "SENTINEL (robust)", "sentinel_triggered": "SENTINEL + state-aware trigger",
                "sentinel_capped_trigger": "SENTINEL + rate-capped trigger"}
COLORS = {"random": "#7f7f7f", "ppo": "#bcbd22", "whittle": "#8c564b", "threshold": "#1f77b4", "nominal": "#ff7f0e", "sentinel": "#d62728", "sentinel_triggered": "#9467bd",
          "sentinel_capped_trigger": "#17becf"}
METRICS = [("average_aoii", "Average AoII"), ("peak_aoii", "Peak AoII"), ("delivery_ratio", "Delivery ratio"),
           ("informative_ratio", "Informative update ratio"), ("sum_rate_mbps", "Delivered goodput (Mbps)"),
           ("latency_ms", "E2E latency of delivered updates (ms)"), ("sat_delivery_share", "Satellite delivery share"),
           ("budget_violation_fraction", "Fraction of UEs over AoII budget")]

plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 150})


def _order_labels(labels):
    """Sort 'U=10'-style or 'L=3'-style labels numerically; keep other labels in first-seen order."""
    def key(l):
        m = re.match(r"^[A-Za-z]+=(\d+(\.\d+)?)$", str(l))
        return (0, float(m.group(1))) if m else (1, 0.0)
    labels = list(dict.fromkeys(labels))
    if all(re.match(r"^[A-Za-z]+=(\d+(\.\d+)?)$", str(l)) for l in labels):
        return sorted(labels, key=key)
    return labels


def bar_sweep(summ, sweep, metric, ylabel, dis_mode, fname, log=False, stat="mean"):
    d = summ[(summ.sweep == sweep) & (summ.disruption_mode == dis_mode)].copy()
    if sweep == "ue_sweep":
        d["x_value"] = pd.to_numeric(d.x_value)
        xs = sorted(d.x_value.unique())
    else:
        xs = [x for x in TOPO_ORDER if x in set(d.x_value)] + sorted(set(d.x_value) - set(TOPO_ORDER))
    pols = [p for p in POLICY_ORDER if p in d.policy.unique()]
    fig, ax = plt.subplots(figsize=(6.0, 3.9))
    w = 0.8 / len(pols)
    for pi, p in enumerate(pols):
        sub = d[d.policy == p].set_index("x_value").reindex(xs)
        if stat == "median":
            y = sub[f"{metric}_median"]
            yerr = np.vstack([y - sub[f"{metric}_q25"], sub[f"{metric}_q75"] - y]).clip(min=0)
        else:
            y, yerr = sub[f"{metric}_mean"], sub[f"{metric}_ci95"]
        ax.bar(np.arange(len(xs)) + (pi - (len(pols) - 1) / 2) * w, y, w,
               yerr=yerr, capsize=2, label=POLICY_LABEL[p], color=COLORS[p])
    ax.set_xticks(np.arange(len(xs))); ax.set_xticklabels([str(x) for x in xs], rotation=0 if sweep == "ue_sweep" else 15, ha="center" if sweep == "ue_sweep" else "right")
    ax.set_xlabel({"ue_sweep": "Number of UEs", "topology": "Topology"}.get(sweep, ""))
    ax.set_ylabel(ylabel + (" (median, IQR)" if stat == "median" else " (mean, 95% CI)"))
    if log:
        ax.set_yscale("log")
    ax.legend(fontsize=7, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.28 if sweep == "ue_sweep" else -0.55), frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / f"{fname}.pdf"); fig.savefig(FIG / f"{fname}.png"); plt.close(fig)


def line_sweep(summ, sweep, metric, ylabel, dis_mode, fname, xlabel, log=False, stat="median", logx=False):
    """Line plot over a numeric x for the sensitivity sweeps (scenario-set size, bandwidth per node)."""
    d = summ[(summ.sweep == sweep) & (summ.disruption_mode == dis_mode)].copy()
    if d.empty or f"{metric}_mean" not in d.columns:
        return
    d["x_value"] = pd.to_numeric(d.x_value)
    xs = sorted(d.x_value.unique())
    pols = [p for p in POLICY_ORDER if p in d.policy.unique()]
    fig, ax = plt.subplots(figsize=(4.6, 3.3))
    for p in pols:
        sub = d[d.policy == p].set_index("x_value").reindex(xs)
        if stat == "median" and f"{metric}_median" in sub.columns:
            y = sub[f"{metric}_median"]
            yerr = np.vstack([y - sub[f"{metric}_q25"], sub[f"{metric}_q75"] - y]).clip(min=0)
        else:
            y, yerr = sub[f"{metric}_mean"], sub[f"{metric}_ci95"]
        ax.errorbar(xs, y, yerr=yerr, marker="o", ms=4, capsize=2, label=POLICY_LABEL.get(p, p), color=COLORS.get(p))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel + (" (median, IQR)" if stat == "median" else " (mean, 95% CI)"))
    ax.set_xticks(xs)
    if log:
        ax.set_yscale("log")
    if logx:
        from matplotlib.ticker import NullFormatter
        ax.set_xscale("log"); ax.set_xticks(xs); ax.set_xticklabels([f"{x:g}" for x in xs]); ax.xaxis.set_minor_formatter(NullFormatter())
    if len(pols) > 1:
        ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / f"{fname}.pdf"); fig.savefig(FIG / f"{fname}.png"); plt.close(fig)


def main(prefix="sweeps", fig_prefix=""):
    global FIG
    if fig_prefix:
        FIG = ROOT / "figures" / fig_prefix
        FIG.mkdir(parents=True, exist_ok=True)
    summ = pd.read_csv(RES / f"{prefix}_summary.csv")
    raw = pd.read_csv(RES / f"{prefix}_raw.csv")
    lines = ["# Regenerated results tables\n"]
    # UE sweep figures, disruption on and off
    for mode in ("on", "off"):
        for metric, ylabel in METRICS:
            bar_sweep(summ, "ue_sweep", metric, ylabel, mode, f"ue_sweep_{metric}_disruption_{mode}", log=(metric in ("average_aoii", "peak_aoii")))
        bar_sweep(summ, "ue_sweep", "average_aoii", "Average AoII", mode, f"ue_sweep_average_aoii_median_disruption_{mode}", log=True, stat="median")
    if (summ.sweep == "topology").any():
        bar_sweep(summ, "topology", "average_aoii", "Average AoII", "on", "topology_average_aoii_median", log=True, stat="median")
    if (summ.sweep == "topology").any():
        for metric, ylabel in METRICS:
            bar_sweep(summ, "topology", metric, ylabel, "on", f"topology_{metric}", log=(metric in ("average_aoii", "peak_aoii")))
    # sensitivity sweeps (present only in some runs)
    if (summ.sweep == "scenario_set").any():
        xl = "Scenario-set size L"
        line_sweep(summ, "scenario_set", "average_aoii", "Average AoII", "on", "scenario_set_average_aoii", xl)
        line_sweep(summ, "scenario_set", "certified_eta_mean", "Certified worst-case AoII", "on", "scenario_set_certified_eta", xl, stat="mean")
        line_sweep(summ, "scenario_set", "certificate_holds", "Certificate validity (fraction of epochs)", "on", "scenario_set_certificate_holds", xl, stat="mean")
        line_sweep(summ, "scenario_set", "sat_delivery_share", "Satellite delivery share", "on", "scenario_set_sat_share", xl, stat="mean")
        line_sweep(summ, "scenario_set", "solve_time_s", "Solver time per run (s)", "on", "scenario_set_solve_time", xl, stat="mean")
    if (summ.sweep == "capacity_limited").any():
        xl = "Bandwidth per node (MHz), 20 UEs"
        line_sweep(summ, "capacity_limited", "average_aoii", "Average AoII", "on", "capacity_average_aoii", xl, log=True, logx=True)
        line_sweep(summ, "capacity_limited", "delivery_ratio", "Delivery ratio", "on", "capacity_delivery_ratio", xl, stat="mean", logx=True)
        line_sweep(summ, "capacity_limited", "peak_aoii", "Peak AoII", "on", "capacity_peak_aoii", xl, log=True, logx=True)
    # certificate figure: certified worst case vs realized average AoII for SENTINEL and nominal
    d = raw[(raw.sweep == "ue_sweep") & (raw.disruption_mode == "on") & raw.policy.isin(["sentinel", "nominal"])]
    if len(d):
        fig, ax = plt.subplots(figsize=(4.2, 3.4))
        for p in ("nominal", "sentinel"):
            s = d[d.policy == p]
            ax.scatter(s.certified_eta_mean, s.average_aoii, s=14, alpha=0.7, label=POLICY_LABEL[p], color=COLORS[p])
        lim = max(d.certified_eta_mean.max(), d.average_aoii.max()) * 1.05
        ax.plot([0, lim], [0, lim], "k--", lw=0.8, label="realized = certified")
        ax.set_xlabel("Certified worst-case AoII (time-weighted)"); ax.set_ylabel("Realized average AoII")
        ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(FIG / "certificate_vs_realized.pdf"); fig.savefig(FIG / "certificate_vs_realized.png"); plt.close(fig)
        holds = d.groupby("policy").certificate_holds.mean()
        lines.append("## Certificate validity (fraction of epochs with realized avg AoII <= certified worst case)\n")
        lines.append(holds.to_frame().to_markdown() + "\n")
    # summary tables
    cols = ["average_aoii", "peak_aoii", "delivery_ratio", "informative_ratio", "sum_rate_mbps", "latency_ms", "sat_delivery_share", "certified_eta_mean"]
    for sweep in summ.sweep.unique():
        for mode in summ[summ.sweep == sweep].disruption_mode.unique():
            d = summ[(summ.sweep == sweep) & (summ.disruption_mode == mode)].copy()
            d["policy"] = d.policy.map(POLICY_LABEL)
            if sweep in ("ue_sweep", "scenario_set", "capacity_limited"):
                d["x_value"] = pd.to_numeric(d.x_value)
            tab = d[["x_value", "policy", "n"] + [f"{c}_mean" for c in cols] + ["average_aoii_ci95", "average_aoii_median"]].sort_values(["x_value", "policy"])
            tab.columns = ["x", "policy", "n"] + cols + ["aoii_ci95", "aoii_median"]
            lines.append(f"## {sweep}, disruption {mode}\n")
            lines.append(tab.round(3).to_markdown(index=False) + "\n")
    # validation
    vfile = RES / "validation_summary.csv"
    if vfile.exists():
        v = pd.read_csv(vfile)
        lines.append("## Validation against the exact ILP optimum of P3 (mean optimality gap %, fraction of instances solved to optimality)\n")
        for exp in sorted(v.exp.unique()):
            lines.append(f"### Experiment {exp}\n")
            piv = v[v.exp == exp].pivot_table(index="label", columns="solver", values="gap_mean")
            lines.append(piv.round(2).to_markdown() + "\n")
            piv2 = v[v.exp == exp].pivot_table(index="label", columns="solver", values="optimal_frac")
            lines.append("Fraction optimal:\n\n" + piv2.round(2).to_markdown() + "\n")
            q = v[(v.exp == exp)][["label", "solver", "qubits_max", "time_mean_s", "local_feasible"]]
            lines.append("Qubits / time / local feasibility:\n\n" + q.round(3).to_markdown(index=False) + "\n")
        # gap figure per experiment
        for exp in sorted(v.exp.unique()):
            d = v[v.exp == exp]
            fig, ax = plt.subplots(figsize=(5.2, 3.2))
            labels = _order_labels(d.label)
            for solver in d.solver.unique():
                s = d[d.solver == solver].set_index("label").reindex(labels)
                ax.plot(range(len(labels)), s.gap_mean, marker="o", label=solver)
            ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels)
            ax.set_ylabel("Mean optimality gap vs exact ILP (%)"); ax.legend(fontsize=7)
            fig.tight_layout(); fig.savefig(FIG / f"validation_{exp}_gap.pdf"); fig.savefig(FIG / f"validation_{exp}_gap.png"); plt.close(fig)
        # QAOA energy trace (first available)
        vr = pd.read_csv(RES / "validation_raw.csv")
        tr = vr[(vr.exp == "A") & vr.qaoa_trace.notna() & (vr.qaoa_trace != "")]
        if len(tr):
            fig, ax = plt.subplots(figsize=(4.2, 3.0))
            for _, row in tr.head(5).iterrows():
                e = json.loads(row.qaoa_trace)
                ax.plot(e, lw=0.8, label=f"{row.label}, seed {row.seed}, {row.qubits} qubits")
            ax.set_xlabel("COBYLA evaluation"); ax.set_ylabel("Sampled QAOA energy  <H_C>"); ax.legend(fontsize=6)
            fig.tight_layout(); fig.savefig(FIG / "qaoa_energy_trace.pdf"); fig.savefig(FIG / "qaoa_energy_trace.png"); plt.close(fig)
    # compact-formulation validation (separate CSV)
    vc = RES / "validation_compact_summary.csv"
    if vc.exists() and prefix == "sweeps":
        v = pd.read_csv(vc)
        lines.append("## Compact formulation: optimality gap vs the exact ILP of P3 (mean %, feasible solutions)\n")
        for exp in sorted(v.exp.unique()):
            d = v[v.exp == exp]
            lines.append(f"### Experiment {exp}\n")
            lines.append(d.pivot_table(index="label", columns="solver", values="gap_mean").round(2).to_markdown() + "\n")
            lines.append("Qubits per domain (max):\n\n" + d.pivot_table(index="label", columns="solver", values="qubits_max").round(0).to_markdown() + "\n")
            fig, ax = plt.subplots(figsize=(5.6, 3.6))
            labels = _order_labels(d.label)
            for solver in [s_ for s_ in d.solver.unique() if "ILP on pruned" not in s_ and s_ != "ILP exact"]:
                sub = d[d.solver == solver].set_index("label").reindex(labels)
                ax.plot(range(len(labels)), sub.gap_mean, marker="o", label=solver)
            ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels)
            ax.set_ylabel("Mean gap vs exact ILP (%)")
            ax.legend(fontsize=6, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False)
            fig.tight_layout(); fig.savefig(ROOT / "figures" / f"validation_compact_{exp}_gap.pdf"); fig.savefig(ROOT / "figures" / f"validation_compact_{exp}_gap.png"); plt.close(fig)
        d = v[(v.exp == "B") & v.solver.isin(["Compact dual + SA-XY ADMM", "Epigraph QUBO + SA-XY ADMM"])]
        if len(d):
            fig, ax = plt.subplots(figsize=(4.6, 3.2))
            labels = _order_labels(d.label)
            for solver, lab in (("Epigraph QUBO + SA-XY ADMM", "Epigraph encoding (Section V)"), ("Compact dual + SA-XY ADMM", "Compact dual encoding")):
                sub = d[d.solver == solver].set_index("label").reindex(labels)
                ax.plot(range(len(labels)), sub.qubits_max, marker="o", label=lab)
            ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels); ax.set_yscale("log")
            ax.set_ylabel("Qubits per domain (max)"); ax.legend(fontsize=7)
            fig.tight_layout(); fig.savefig(ROOT / "figures" / "qubits_compact_vs_epigraph.pdf"); fig.savefig(ROOT / "figures" / "qubits_compact_vs_epigraph.png"); plt.close(fig)
    (RES / (f"tables_{prefix}.md" if prefix != "sweeps" else "tables.md")).write_text("\n".join(lines), encoding="utf-8")
    print("figures written to", FIG)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--prefix", default="sweeps"); ap.add_argument("--fig-prefix", default="")
    a = ap.parse_args(); main(a.prefix, a.fig_prefix)
