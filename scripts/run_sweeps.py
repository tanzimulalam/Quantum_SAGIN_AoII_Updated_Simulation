"""Run the UE sweep and the topology sweep with N seeds in parallel. Writes results/*.csv."""
import sys, pathlib, time, argparse, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from sentinel.config import FullConfig
from sentinel.experiments import configure, run_seed, summarize

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = ROOT / "results"


def build_tasks(seeds, which, formulation="compact", sat_model="synthetic", ntn=False, no_ack=False, policies=None,
                no_mild=False):
    base = FullConfig()
    base.dis.mild_scenario = not no_mild
    base.solver.formulation = formulation
    base.net.sat_model = sat_model
    base.dis.ntn_model = ntn
    if no_ack:
        # ablation: no ACK-based link-failure handling for any policy (no blocking, no reactive re-solve)
        base.sim.failure_window_slots = 10**9
        base.sim.reactive_resolve = False
    if sat_model == "tle":
        base.net.min_elevation_deg = 25.0        # typical NTN user-terminal mask for a dense LEO constellation
    base.solver.solver = "sa_xy"           # one-hot-preserving annealer; formulation set by --formulation
    policies = policies or ["random", "threshold", "nominal", "sentinel", "sentinel_triggered", "sentinel_capped_trigger"]
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
    if which in ("scen", "all"):
        # sensitivity of the robust schedule to the scenario-set size L (nominal, +mild, +severe, +handover of each
        # satellite, +joint outage); 10 UEs, 2 BS + 2 SAT, robust SENTINEL only, disruption on
        cfg = configure(base, net__num_ues=10, net__num_bs=2, net__num_sat=2, net__num_domains=2)
        for L in (1, 2, 3, 4, 5, 6):
            for s in seeds:
                tasks.append({"cfg": cfg, "seed": s, "policies": ["sentinel"], "sweep": "scenario_set",
                              "x_label": "Scenario-set size L", "x_value": L, "num_scenarios": L,
                              "disruption_modes": ["on"]})
    if which in ("cap", "all"):
        # capacity-limited stress test for the per-slot state-aware policies: the bandwidth per node is swept down
        # from the default (20 MHz BS / 50 MHz SAT) to 2 MHz, where a node delivers only 4 to 6 equal sharers per slot
        for bw in (2.0, 5.0, 10.0, 20.0):
            cfg = configure(base, net__num_ues=20, net__num_bs=2, net__num_sat=2, net__num_domains=2,
                            radio__sat_bandwidth_mhz=bw, radio__bs_bandwidth_mhz=bw)
            for s in seeds:
                tasks.append({"cfg": cfg, "seed": s, "policies": ["random", "threshold", "whittle"],
                              "sweep": "capacity_limited", "x_label": "Bandwidth per node (MHz), 20 UEs", "x_value": bw,
                              "disruption_modes": ["on"]})
    return tasks


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30, help="last seed (seeds run from --seed-start to this value)")
    ap.add_argument("--seed-start", type=int, default=1)
    ap.add_argument("--workers", type=int, default=20)
    ap.add_argument("--which", default="all", choices=["ue", "topo", "scen", "cap", "all"])
    ap.add_argument("--tag", default="")
    ap.add_argument("--x-filter", default=None, help="only run tasks whose x_value equals this string")
    ap.add_argument("--append", action="store_true", help="merge new rows into results/sweeps_raw.csv and re-summarize")
    ap.add_argument("--formulation", default="compact", choices=["compact", "epigraph"])
    ap.add_argument("--sat-model", default="synthetic", choices=["synthetic", "tle"])
    ap.add_argument("--ntn", action="store_true", help="enable the TR 38.811 large-scale NTN channel model")
    ap.add_argument("--no-ack", action="store_true", help="ablation: disable ACK-based link-failure handling for all policies")
    ap.add_argument("--policies", default=None, help="comma-separated subset of policies (default: all six)")
    ap.add_argument("--no-mild", action="store_true", help="drop the mild-shadowing scenario from the robust scenario set (L = 5)")
    ap.add_argument("--out-prefix", default="sweeps", help="prefix of the output CSV files")
    args = ap.parse_args()
    seeds = list(range(args.seed_start, args.seeds + 1))
    tasks = build_tasks(seeds, args.which, args.formulation, args.sat_model, args.ntn, args.no_ack,
                        args.policies.split(",") if args.policies else None, args.no_mild)
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
    if args.append and (RES / f"{args.out_prefix}_raw.csv").exists():
        old = pd.read_csv(RES / f"{args.out_prefix}_raw.csv")
        key = ["sweep", "x_value", "policy", "seed", "disruption_mode"]
        new_keys = set(map(tuple, raw[key].astype(str).values.tolist()))
        old = old[[tuple(k) not in new_keys for k in old[key].astype(str).values.tolist()]]   # replace only the rows re-run
        raw = pd.concat([old, raw], ignore_index=True)
        rows = raw.to_dict("records")
        tag = ""
    raw.to_csv(RES / f"{args.out_prefix}_raw{tag}.csv", index=False)
    pd.DataFrame(summarize(rows)).to_csv(RES / f"{args.out_prefix}_summary{tag}.csv", index=False)
    cfg_dump = FullConfig(); cfg_dump.solver.formulation = args.formulation; cfg_dump.net.sat_model = args.sat_model; cfg_dump.dis.ntn_model = args.ntn
    with open(RES / f"{args.out_prefix}_config{tag}.json", "w") as fh:
        json.dump(cfg_dump.to_dict(), fh, indent=2, default=str)
    print(f"done in {time.time()-t0:.0f}s; {len(raw)} rows", flush=True)
