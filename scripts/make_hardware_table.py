"""Builds the LaTeX device table of Section VI-E (paper/table_hardware.tex) from results/hardware/runs.csv.

One row per unmitigated device domain, greedy-start and W-state runs side by side where both exist: qubits, the
two-qubit gate count of each circuit, the energy spread of the feasible set (max/opt - 1, so that flat domains are
visible), and per run the feasible-shot fraction, the probability of the optimum given a feasible shot, and the
probability of the optimum under uniform sampling of that run's feasible one-hot set. The product of the first two is
the probability that a single shot is an optimal assignment (p_optimal_shot in runs.csv). The uniform baseline is
listed per run because every run re-solves the scenario weights, so the optimal set of a domain can differ between its
greedy-start and W-state runs (it does on the two seed-2 domains).
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def fmt(v, pct=False, nd=2):
    if v is None or pd.isna(v):
        return "--"
    if pct:
        return f"{100*v:.0f}\\%"
    if nd == 2 and 0 < v < 0.0095:
        nd = 3
    return f"{v:.{nd}f}"


def cell(row, col, **kw):
    return fmt(row[col], **kw) if row is not None else "--"


def gates(row):
    return str(int(row["two_qubit_gates"])) if row is not None else "--"


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
        "\\caption{Device Sampling Results on IBM Heron Processors (greedy start: \\texttt{ibm\\_kingston}, seeds 6 and 7 on "
        "\\texttt{ibm\\_fez}; $W$-state start: \\texttt{ibm\\_fez}; U: number of UEs, s: seed, d: domain; uniform baseline "
        "per run)}",
        "\\label{tab:hardware}", "\\scriptsize",
        "\\setlength{\\tabcolsep}{2.5pt}",
        "\\resizebox{\\columnwidth}{!}{%",
        "\\begin{tabular}{|l|c|cc|c|cc|cc|cc|}", "\\hline",
        "\\textbf{Instance} & \\textbf{Qubits} & \\multicolumn{2}{c|}{\\textbf{2q gates}} & \\textbf{Spread} & "
        "\\multicolumn{2}{c|}{\\textbf{Feasible shots}} & "
        "\\multicolumn{2}{c|}{$P(\\text{opt.}\\mid\\text{feas.})$} & \\multicolumn{2}{c|}{\\textbf{Uniform} $P(\\text{opt.})$} \\\\",
        " & & greedy & $W$ & & greedy & $W$ & greedy & $W$ & greedy & $W$ \\\\",
        "\\hline",
    ]
    for ues, seed, dom, a, gr, wr in rows:
        name = f"U{ues} s{seed} d{dom}"
        lines.append(
            f"{name} & {int(a.qubits)} & {gates(gr)} & {gates(wr)} & {fmt(a.energy_spread_rel, pct=True)} & "
            f"{cell(gr, 'feasible_frac', pct=True)} & {cell(wr, 'feasible_frac', pct=True)} & "
            f"{cell(gr, 'p_optimal_given_feasible')} & {cell(wr, 'p_optimal_given_feasible')} & "
            f"{cell(gr, 'p_uniform_optimal', nd=3)} & {cell(wr, 'p_uniform_optimal', nd=3)} \\\\")
    lines += ["\\hline", "\\end{tabular}%", "}", "\\end{table}"]
    (ROOT / "paper" / "table_hardware.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
