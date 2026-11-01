"""Builds the LaTeX device table of Section VI-E (paper/table_hardware.tex) from results/hardware/runs.csv.

One row per unmitigated device domain, greedy-start and W-state runs side by side where both exist: qubits, two-qubit
gates, feasible-shot fraction, probability that a shot is an optimal assignment, probability of the optimum given a
feasible shot, mean approximation ratio over feasible shots, and the same two quantities under uniform sampling of the
feasible one-hot set. The energy spread of the feasible set (max/opt - 1) is listed so that flat domains are visible.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def fmt(v, pct=False, nd=2):
    if v is None or pd.isna(v):
        return "--"
    return f"{100*v:.0f}\\%" if pct else f"{v:.{nd}f}"


def main():
    df = pd.read_csv(ROOT / "results" / "hardware" / "runs.csv")
    dev = df[(df["mode"] == "device") & (df["mitigation"].fillna("none") == "none")].copy()
    dev = dev[~dev["run"].str.endswith("_ctrl")]
    rows = []
    for (ues, seed, dom), g in dev.groupby(["ues", "seed", "domain"]):
        gr = g[g["init"] == "greedy"]
        wr = g[g["init"] == "w"]
        a = gr.iloc[0] if len(gr) else (wr.iloc[0] if len(wr) else None)
        if a is None:
            continue
        w_row = None
        if len(wr):
            same = wr[wr["backend"] == a["backend"]] if len(gr) else wr
            w_row = same.iloc[0] if len(same) else wr.iloc[0]
            print(f"W-state row for {ues} UEs seed {seed} domain {dom}: {w_row['backend']} (greedy on {a['backend']})")
        rows.append((ues, seed, dom, a, gr.iloc[0] if len(gr) else None, w_row))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    lines = [
        "\\begin{table}[!t]", "\\centering",
        "\\caption{Device Sampling Results on IBM Heron Processors (greedy start: \\texttt{ibm\\_kingston}, seeds 6 and 7 on \\texttt{ibm\\_fez}; $W$-state start: \\texttt{ibm\\_fez})}",
        "\\label{tab:hardware}", "\\scriptsize",
        "\\resizebox{\\columnwidth}{!}{%",
        "\\begin{tabular}{|l|c|c|c|cc|cc|cc|c|}", "\\hline",
        "\\textbf{Instance} & \\textbf{Qubits} & \\textbf{2q} & \\textbf{Spread} & \\multicolumn{2}{c|}{\\textbf{Feasible shots}} & "
        "\\multicolumn{2}{c|}{$P(\\text{opt. shot})$} & \\multicolumn{2}{c|}{$P(\\text{opt.}\\mid\\text{feas.})$} & \\textbf{Unif.} \\\\",
        " & & \\textbf{gates} & & greedy & $W$ & greedy & $W$ & greedy & $W$ & $P(\\text{opt.})$ \\\\",
        "\\hline",
    ]
    for ues, seed, dom, a, gr, wr in rows:
        name = f"{ues} UEs, s{seed}, d{dom}"
        spread = fmt(a.energy_spread_rel, pct=True)
        lines.append(
            f"{name} & {int(a.qubits)} & {int(a.two_qubit_gates)} & {spread} & "
            f"{fmt(gr.feasible_frac, pct=True) if gr is not None else '--'} & {fmt(wr.feasible_frac, pct=True) if wr is not None else '--'} & "
            f"{fmt(gr.p_optimal_shot) if gr is not None else '--'} & {fmt(wr.p_optimal_shot) if wr is not None else '--'} & "
            f"{fmt(gr.p_optimal_given_feasible) if gr is not None else '--'} & {fmt(wr.p_optimal_given_feasible) if wr is not None else '--'} & "
            f"{fmt(a.p_uniform_optimal, nd=3)} \\\\")
    lines += ["\\hline", "\\end{tabular}%", "}", "\\end{table}"]
    (ROOT / "paper" / "table_hardware.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
