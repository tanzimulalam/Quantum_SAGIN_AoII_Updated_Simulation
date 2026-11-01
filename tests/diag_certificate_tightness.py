"""Per-epoch certificate tightness and violation sizes for robust SENTINEL under TLE + NTN (paper Section VI-B).

For each network size and seed, plans the robust schedule (five-scenario set) and runs it; records every epoch's
realized average AoII against its certified worst case. Outputs results/certificate_tightness.csv (one row per epoch)
and prints the tightness ratio distribution, the violation rate, and the size of the violations.
"""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np, pandas as pd
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.simulator import make_episode, plan_schedule, run_policy

ROOT = pathlib.Path(__file__).resolve().parents[1]


def one(args):
    U, seed = args
    base = FullConfig(); base.net.sat_model = "tle"; base.dis.ntn_model = True; base.net.min_elevation_deg = 25.0
    base.solver.solver = "sa_xy"; base.dis.mild_scenario = False
    cfg = configure(base, net__num_ues=U, net__num_bs=2, net__num_sat=2, net__num_domains=2, dis__enabled=True)
    ep = make_episode(cfg, seed)
    plan = plan_schedule(ep, num_scenarios=5, solver_seed=seed)
    r = run_policy(ep, "sentinel", plan=plan, num_scenarios=5)
    d = r.epoch_detail
    return [{"num_ues": U, "seed": seed, "epoch": i, "realized": d["realized"][i], "certified": d["certified"][i], "weight": d["weight"][i]}
            for i in range(len(d["realized"]))]


if __name__ == "__main__":
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    tasks = [(U, s) for U in (5, 10, 15, 20) for s in range(1, 31)]
    rows = []; t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(one, t) for t in tasks]
        for i, f in enumerate(as_completed(futs), 1):
            rows += f.result()
            if i % 10 == 0: print(f"{i}/{len(tasks)} done, {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(rows); df.to_csv(ROOT / "results" / "certificate_tightness.csv", index=False)
    df["ratio"] = df.certified / df.realized.clip(lower=1e-9)
    df["viol"] = df.realized > df.certified + 1e-9
    df["excess"] = np.where(df.viol, df.realized - df.certified, np.nan)
    df["excess_rel"] = np.where(df.viol, df.realized / df.certified, np.nan)
    print("epochs:", len(df))
    for U, g in df.groupby("num_ues"):
        print(f"U={U}: ratio median {g.ratio.median():.1f} (IQR {g.ratio.quantile(.25):.1f}-{g.ratio.quantile(.75):.1f}); "
              f"violations {g.viol.mean()*100:.1f}% of epochs; excess median {g.excess.median():.2f} (max {g.excess.max():.2f}); "
              f"realized/certified when violated median {g.excess_rel.median():.2f} (max {g.excess_rel.max():.2f}); "
              f"certified mean {g.certified.mean():.2f}, realized mean {g.realized.mean():.3f}")
    print("all: violations %.2f%%, ratio median %.1f" % (df.viol.mean()*100, df.ratio.median()))
