"""Run the UE sweep and the topology sweep with N seeds in parallel. Writes results/*.csv."""
import sys, pathlib, time, argparse, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from sentinel.config import FullConfig
from sentinel.experiments import configure, run_seed, summarize

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def build_tasks(seeds, which):
    base = FullConfig()
    base.solver.solver = "sa_xy"           # one-hot-preserving annealer on the domain objective (domains far exceed Aer's reach)
    policies = ["random", "threshold", "nominal", "sentinel", "sentinel_triggered"]
    tasks = []
    if which in ("ue", "all"):
        for U in (5, 10, 15, 20):
            cfg = configure(base, net__num_ues=U, net__num_bs=2, net__num_sat=2)
            for s in seeds:
                tasks.append({"cfg": cfg, "seed": s, "policies": policies, "sweep": "ue_sweep",
                              "x_label": "Number of UEs", "x_value": U})
    if which in ("topo", "all"):
        topo_cfgs = [("Ground only (2 BS)", 2, 0), ("Satellite only (2 SAT)", 0, 2), ("Integrated (1 BS + 1 SAT)", 1, 1),
                     ("Integrated (2 BS + 2 SAT)", 2, 2), ("Integrated (3 BS + 3 SAT)", 3, 3)]
        for name, B, S in topo_cfgs:
            cfg = configure(base, net__num_ues=10, net__num_bs=B, net__num_sat=S, net__num_domains=2)
            for s in seeds:
                tasks.append({"cfg": cfg, "seed": s, "policies": policies, "sweep": "topology",
                              "x_label": "Topology", "x_value": name, "disruption_modes": ["on"]})
    return tasks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--which", default="all", choices=["ue", "topo", "all"])
    ap.add_argument("--tag", default="")
    ap.add_argument("--x-filter", default=None, help="only run tasks whose x_value equals this string")
    ap.add_argument("--append", action="store_true", help="merge new rows into results/sweeps_raw.csv and re-summarize")
    args = ap.parse_args()
    seeds = list(range(1, args.seeds + 1))
    tasks = build_tasks(seeds, args.which)
    if args.x_filter is not None:
        tasks = [t for t in tasks if str(t["x_value"]) == args.x_filter]
    print(f"{len(tasks)} tasks on {args.workers} workers", flush=True)
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_seed, t): (t["sweep"], t["x_value"], t["seed"]) for t in tasks}
        done = 0
        for f in as_completed(futs):
            done += 1
            try:
                rows.extend(f.result())
            except Exception as e:  # keep going, report
                print("FAILED", futs[f], repr(e), flush=True)
            if done % 10 == 0 or done == len(tasks):
                print(f"  {done}/{len(tasks)} tasks done, {time.time()-t0:.0f}s elapsed", flush=True)
    raw = pd.DataFrame(rows)
    tag = f"_{args.tag}" if args.tag else ""
    if args.append and (RES / "sweeps_raw.csv").exists():
        old = pd.read_csv(RES / "sweeps_raw.csv")
        old = old[~((old.sweep.isin(raw.sweep.unique())) & (old.x_value.astype(str).isin(raw.x_value.astype(str).unique())))]
        raw = pd.concat([old, raw], ignore_index=True)
        rows = raw.to_dict("records")
        tag = ""
    raw.to_csv(RES / f"sweeps_raw{tag}.csv", index=False)
    pd.DataFrame(summarize(rows)).to_csv(RES / f"sweeps_summary{tag}.csv", index=False)
    with open(RES / f"sweeps_config{tag}.json", "w") as fh:
        json.dump(FullConfig().to_dict(), fh, indent=2, default=str)
    print(f"done in {time.time()-t0:.0f}s; {len(raw)} rows", flush=True)
