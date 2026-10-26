"""Train the PPO baseline, one model per network size, on seeds disjoint from the evaluation seeds (1..30)."""
import sys, pathlib, argparse, time, os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
os.environ.setdefault("OMP_NUM_THREADS", "2")
from concurrent.futures import ProcessPoolExecutor
from sentinel.config import FullConfig
from sentinel.experiments import configure
from sentinel.rl import train_ppo, model_path

ROOT = pathlib.Path(__file__).resolve().parents[1]


def train_one(args_tuple):
    U, sat_model, ntn, episodes, train_slots, seeds = args_tuple
    cfg = configure(FullConfig(), net__num_ues=U, net__num_bs=2, net__num_sat=2, net__sat_model=sat_model, dis__ntn_model=ntn,
                    net__min_elevation_deg=25.0 if sat_model == "tle" else 10.0)
    path = model_path(U, sat_model, ntn)
    print(f"[U={U}] training {episodes} episodes x {train_slots} slots on seeds {seeds[0]}..{seeds[-1]} -> {path.name}", flush=True)
    t0 = time.time()
    _, hist = train_ppo(cfg, seeds, episodes=episodes, train_slots=train_slots, seed=U, save=path, threads=2)
    print(f"[U={U}] done in {time.time()-t0:.0f}s; last-20 avg AoII {sum(h['avg_aoii'] for h in hist[-20:])/20:.3f}", flush=True)
    return U, hist[-1]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ues", default="5,10,15,20"); ap.add_argument("--episodes", type=int, default=300)
    ap.add_argument("--train-slots", type=int, default=6000); ap.add_argument("--sat-model", default="tle"); ap.add_argument("--ntn", action="store_true")
    ap.add_argument("--train-seeds", default="101-130"); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    lo, hi = [int(v) for v in a.train_seeds.split("-")]; seeds = list(range(lo, hi + 1))
    tasks = [(int(u), a.sat_model, a.ntn, a.episodes, a.train_slots, seeds) for u in a.ues.split(",")]
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for U, last in ex.map(train_one, tasks):
            print(f"U={U}: final episode {last}", flush=True)
