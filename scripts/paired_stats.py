"""Paired statistical comparisons between policies across seeds (common random numbers).

For each sweep point and each (policy A, policy B) pair of interest, the 30 seeds give 30 paired differences of
average AoII. Reported: median paired ratio A/B, fraction of seeds with A < B, two-sided Wilcoxon signed-rank p-value,
two-sided paired t-test p-value, and the Hodges-Lehmann estimate of the median difference with a bootstrap 95% CI.
Holm correction is applied within each sweep over all tests. Also reports the certificate-validity rate per policy
and a Wilcoxon test of certified eta (robust vs nominal).

Usage:
    .venv/Scripts/python.exe scripts/paired_stats.py --prefix sweeps_tle_ntn --metric average_aoii
Outputs results/<prefix>_paired_stats.csv and results/<prefix>_paired_stats.md
"""
import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [
    ("sentinel", "nominal"),
    ("sentinel", "threshold"),
    ("sentinel_capped_trigger", "threshold"),
    ("sentinel_triggered", "threshold"),
    ("sentinel", "ppo"),
    ("nominal", "ppo"),
    ("sentinel", "random"),
    ("whittle", "threshold"),
    ("sentinel_capped_trigger", "whittle"),
]


def holm(pvals):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, p[idx] * (m - rank))
        adj[idx] = min(1.0, running)
    return adj


def hodges_lehmann(d, rng, n_boot=2000):
    d = np.asarray(d, float)
    n = len(d)
    walsh = np.array([(d[i] + d[j]) / 2 for i in range(n) for j in range(i, n)])
    est = float(np.median(walsh))
    boots = []
    for _ in range(n_boot):
        s = rng.choice(d, n, replace=True)
        boots.append(np.median([(s[i] + s[j]) / 2 for i in range(n) for j in range(i, n)]))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return est, float(lo), float(hi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="sweeps_tle_ntn")
    ap.add_argument("--metric", default="average_aoii")
    ap.add_argument("--disruption-mode", default="on")
    args = ap.parse_args()
    raw = pd.read_csv(ROOT / "results" / f"{args.prefix}_raw.csv")
    raw = raw[raw["disruption_mode"] == args.disruption_mode]
    rng = np.random.default_rng(0)
    rows = []
    for (sweep, xv), g in raw.groupby(["sweep", "x_value"]):
        piv = g.pivot_table(index="seed", columns="policy", values=args.metric)
        for a, b in PAIRS:
            if a not in piv.columns or b not in piv.columns:
                continue
            both = piv[[a, b]].dropna()
            if len(both) < 6:
                continue
            da, db = both[a].to_numpy(), both[b].to_numpy()
            diff = da - db
            if np.allclose(diff, 0):
                w_p = 1.0
            else:
                w_p = float(stats.wilcoxon(da, db, zero_method="wilcox", alternative="two-sided").pvalue)
            t_p = float(stats.ttest_rel(da, db).pvalue)
            hl, lo, hi = hodges_lehmann(diff, rng)
            rows.append({
                "sweep": sweep, "x_value": xv, "policy_a": a, "policy_b": b, "n_seeds": len(both),
                "median_a": float(np.median(da)), "median_b": float(np.median(db)),
                "median_paired_ratio": float(np.median(da / db)),
                "frac_a_lower": float(np.mean(da < db)),
                "hl_median_diff": hl, "hl_ci_lo": lo, "hl_ci_hi": hi,
                "wilcoxon_p": w_p, "ttest_p": t_p,
            })
    out = pd.DataFrame(rows)
    if out.empty:
        raise SystemExit("no comparable pairs found")
    out["wilcoxon_p_holm"] = np.nan
    for sweep, idx in out.groupby("sweep").groups.items():
        out.loc[idx, "wilcoxon_p_holm"] = holm(out.loc[idx, "wilcoxon_p"].to_numpy())
    out = out.sort_values(["sweep", "x_value", "policy_a", "policy_b"]).reset_index(drop=True)
    csv_path = ROOT / "results" / f"{args.prefix}_paired_stats.csv"
    out.to_csv(csv_path, index=False)

    # certificate validity and certified-eta comparison
    cert_lines = []
    cert = raw[raw["policy"].isin(["sentinel", "nominal"]) & raw["certificate_holds"].notna()]
    if len(cert):
        c = cert.groupby("policy")["certificate_holds"].mean()
        cert_lines.append("Certificate holds (fraction of epochs, all sweep points): " +
                          ", ".join(f"{k} {v:.3f}" for k, v in c.items()))
        for (sweep, xv), g in cert.groupby(["sweep", "x_value"]):
            piv = g.pivot_table(index="seed", columns="policy", values="certified_eta_mean").dropna()
            if {"sentinel", "nominal"} <= set(piv.columns) and len(piv) >= 6:
                r = piv["sentinel"] / piv["nominal"]
                p = stats.wilcoxon(piv["sentinel"], piv["nominal"]).pvalue if not np.allclose(r, 1) else 1.0
                cert_lines.append(f"{sweep} x={xv}: certified eta robust/nominal median {r.median():.3f}, "
                                  f"robust lower in {np.mean(piv['sentinel'] < piv['nominal']):.2f} of seeds, Wilcoxon p={p:.2e}")

    md = [f"# Paired comparisons, `{args.prefix}`, metric `{args.metric}`, disruption {args.disruption_mode}", "",
          "Each row: 30 paired seeds (common random numbers). HL = Hodges-Lehmann median of the paired differences with a",
          "bootstrap 95% CI; Wilcoxon p is two-sided signed-rank, Holm-corrected within the sweep.", "",
          "| sweep | x | A | B | median A | median B | median A/B | A lower in | HL diff [95% CI] | Wilcoxon p (Holm) | paired t p |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in out.iterrows():
        md.append(f"| {r.sweep} | {r.x_value} | {r.policy_a} | {r.policy_b} | {r.median_a:.3f} | {r.median_b:.3f} | "
                  f"{r.median_paired_ratio:.2f} | {r.frac_a_lower:.2f} | {r.hl_median_diff:+.3f} [{r.hl_ci_lo:+.3f}, {r.hl_ci_hi:+.3f}] | "
                  f"{r.wilcoxon_p:.1e} ({r.wilcoxon_p_holm:.1e}) | {r.ttest_p:.1e} |")
    if cert_lines:
        md += ["", "## Certificates", ""] + [f"- {l}" for l in cert_lines]
    (ROOT / "results" / f"{args.prefix}_paired_stats.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
