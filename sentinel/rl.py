"""Learning baseline: PPO at the orchestration level.

Every orchestration interval (100 slots) the agent picks, for each UE, a serving node and an update-period level.
UEs on the same node share its bandwidth equally (as the other heuristic baselines do), so capacity is respected by
construction. The reward is minus the mean AoII over the interval plus a small delivery bonus. Training uses short
episodes (60 intervals) on seeds disjoint from the evaluation seeds; evaluation runs the trained policy
deterministically on the same 10-minute episodes as every other policy (common random numbers).
"""
from __future__ import annotations

import os, time, pathlib
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from .config import FullConfig, C_LIGHT
from .channel import bs_rate_bps, sat_rate_bps, nominal_rate_table
from .simulator import Episode, make_episode, RunResult

MODELS = pathlib.Path(__file__).resolve().parents[1] / "models"


class OrchestrationEnv:
    """Interval-level environment on top of an Episode."""

    def __init__(self, ep: Episode):
        self.ep = ep
        cfg = ep.cfg
        self.U, self.B, self.S = ep.topology.num_ues, ep.topology.num_bs, ep.topology.num_sat
        self.M = self.B + self.S
        self.H = len(cfg.src.update_periods_slots)
        self.periods = np.array(cfg.src.update_periods_slots)
        self.I = cfg.sim.orchestration_interval_slots
        self.T = ep.num_slots
        self.T_s = cfg.src.slot_ms * 1e-3
        self.D = cfg.src.packet_bits
        self.rc = cfg.radio
        self.d_bs = ep.topology.ue_bs_distance_m() if self.B else np.zeros((self.U, 0))
        self.full_bw = np.where(np.arange(self.M) < self.B, self.rc.bs_bandwidth_mhz * 1e6, self.rc.sat_bandwidth_mhz * 1e6)
        # per-interval nominal rates and visibility (features)
        self.rates_int = np.zeros((ep.num_intervals, self.U, self.M)); self.vis_int = np.zeros((ep.num_intervals, self.U, self.M), dtype=bool)
        for k in range(ep.num_intervals):
            r, v = nominal_rate_table(ep.topology, k, self.rc)
            self.rates_int[k] = r[:, :, -1] * v; self.vis_int[k] = v
        self.rate_norm = max(self.rates_int.max(), 1.0)
        self.cap_bs = cfg.sim.bs_compute_gcycles_s * 1e9; self.cap_sat = cfg.sim.sat_compute_gcycles_s * 1e9
        self.obs_dim = self.U * (4 + 2 * self.M) + self.M + 1
        self.reset()

    def reset(self):
        X = self.ep.X
        self.t = 1; self.k = 0
        self.est = X[0].copy(); self.last_correct = np.zeros(self.U, dtype=int); self.last_delivery = np.zeros(self.U, dtype=int)
        self.aoii = np.zeros(self.U); self.aoii_sum = np.zeros(self.U); self.aoii_peak = 0.0
        self.attempts = 0; self.deliveries = 0; self.informative = 0; self.bits = 0.0
        self.lat_sum = 0.0; self.lat_bs = 0.0; self.lat_sat = 0.0; self.n_bs = 0; self.n_sat = 0; self.sat_sched = 0
        self.last_succ = np.zeros(self.U); self.last_load = np.zeros(self.M)
        self.fail_since = np.full(self.U, -1, dtype=int); self.blocked_until = np.zeros((self.U, self.M), dtype=int)
        return self.observe()

    def allowed(self):
        """Visible nodes not currently blocked by ACK feedback (same 60-slot / 600-slot rule as the other policies)."""
        k = min(self.k, self.ep.num_intervals - 1)
        a = self.vis_int[k] & ~(self.blocked_until > self.t)
        none = ~a.any(axis=1)
        a[none] = self.vis_int[k][none]
        return a

    def observe(self):
        k = min(self.k, self.ep.num_intervals - 1)
        per_ue = np.concatenate([
            np.log1p(np.minimum(self.aoii, 100.0))[:, None] / 5.0,
            np.minimum(self.t - self.last_delivery, 1000) [:, None] / 1000.0,
            self.last_succ[:, None],
            (self.ep.X[min(self.t, self.T - 1)] != self.est)[:, None].astype(float),
            self.rates_int[k] / self.rate_norm,
            self.allowed().astype(float),
        ], axis=1)
        glob = np.concatenate([self.last_load / max(self.U, 1), [self.k / self.ep.num_intervals]])
        return np.concatenate([per_ue.ravel(), glob]).astype(np.float32)

    def step(self, node_action: np.ndarray, period_action: np.ndarray):
        """Simulate one orchestration interval. Returns (obs, reward, done, info)."""
        X = self.ep.X; U, B, M = self.U, self.B, self.M
        k = min(self.k, self.ep.num_intervals - 1)
        node = node_action.astype(int); period = self.periods[period_action.astype(int)]
        # invisible or blocked choice -> fall back to the best allowed node
        allowed = self.allowed()
        bad = ~allowed[np.arange(U), node]
        if bad.any():
            node[bad] = np.argmax(np.where(allowed[bad], self.rates_int[k][bad], -1.0), axis=1)
        cfg_sim = self.ep.cfg.sim
        counts = np.bincount(node, minlength=M)
        bw_ue = self.full_bw[node] / np.maximum(counts[node], 1)
        succ = np.zeros(U); att = np.zeros(U)
        aoii_acc = 0.0
        t_end = min(self.t + self.I, self.T)
        for t in range(self.t, t_end):
            tx = (t - self.last_delivery) >= period
            idx = np.flatnonzero(tx)
            if len(idx):
                n_i = node[idx]; bw_i = bw_ue[idx]
                rate = np.zeros(len(idx)); dist = np.zeros(len(idx)); is_bs = n_i < B
                if is_bs.any():
                    dd = self.d_bs[idx[is_bs], n_i[is_bs]]
                    rate[is_bs] = bs_rate_bps(dd, bw_i[is_bs], self.rc, fading_db=self.ep.fading_db[t, idx[is_bs]]); dist[is_bs] = dd
                if (~is_bs).any():
                    j = n_i[~is_bs] - B; ii = idx[~is_bs]
                    rg = self.ep.topology.sat_range_m[j, k, ii]; vis = self.ep.topology.sat_visible[j, k, ii]
                    r = sat_rate_bps(rg, bw_i[~is_bs], self.rc, extra_loss_db=self.ep.disruption.loss_db[t, j, ii], fading_db=self.ep.fading_db[t, ii])
                    rate[~is_bs] = np.where(vis, r, 0.0); dist[~is_bs] = np.where(np.isfinite(rg), rg, 0.0)
                    self.sat_sched += int((~is_bs).sum())
                ok = rate * self.T_s >= self.D
                self.attempts += len(idx); att[idx] += 1
                # ACK feedback: block a node after failure_window_slots of consecutive failures
                self.fail_since[idx[ok]] = -1
                failed = idx[~ok]
                if len(failed):
                    fresh = self.fail_since[failed] < 0
                    self.fail_since[failed[fresh]] = t
                    persistent = (t - self.fail_since[failed]) >= cfg_sim.failure_window_slots
                    for i_u, m_u in zip(failed[persistent], n_i[~ok][persistent]):
                        self.blocked_until[i_u, m_u] = t + cfg_sim.failure_block_slots
                    self.fail_since[failed[persistent]] = -1
                if ok.any():
                    good = idx[ok]; succ[good] += 1
                    self.deliveries += len(good); self.informative += int((X[t, good] != self.est[good]).sum())
                    self.est[good] = X[t, good]; self.last_delivery[good] = t; self.bits += self.D * len(good)
                    gn = n_i[ok]; served = np.bincount(gn, minlength=M)
                    comp = np.where(gn < B, self.cap_bs, self.cap_sat) / served[gn]
                    lat = self.D / rate[ok] + dist[ok] / C_LIGHT + self.D * self.ep.cfg.sim.cycles_per_bit / comp
                    self.lat_sum += lat.sum(); bsm = gn < B
                    self.lat_bs += lat[bsm].sum(); self.n_bs += int(bsm.sum()); self.lat_sat += lat[~bsm].sum(); self.n_sat += int((~bsm).sum())
            correct = X[t] == self.est
            self.last_correct[correct] = t
            self.aoii = np.where(correct, 0.0, (t - self.last_correct) * np.abs(X[t] - self.est))
            self.aoii_sum += self.aoii; aoii_acc += self.aoii.mean()
            self.aoii_peak = max(self.aoii_peak, float(self.aoii.max()))
        n_slots = t_end - self.t
        self.t = t_end; self.k += 1
        self.last_succ = np.where(att > 0, succ / np.maximum(att, 1), self.last_succ); self.last_load = counts.astype(float)
        mean_aoii = aoii_acc / max(n_slots, 1)
        reward = -min(mean_aoii, 20.0) / 5.0 + 0.01 * succ.sum() / U
        done = self.t >= self.T
        return self.observe(), float(reward), done, {"mean_aoii": mean_aoii}

    def result(self, policy_name: str = "ppo") -> RunResult:
        T = self.T; avg = self.aoii_sum / (T - 1)
        return RunResult(policy=policy_name, seed=self.ep.seed, num_ues=self.U, num_bs=self.B, num_sat=self.S, disruption=self.ep.cfg.dis.enabled,
                         average_aoii=float(avg.mean()), peak_aoii=float(self.aoii_peak),
                         delivery_ratio=self.deliveries / self.attempts if self.attempts else 0.0,
                         informative_ratio=self.informative / self.deliveries if self.deliveries else 0.0,
                         sum_rate_mbps=self.bits / ((T - 1) * self.T_s) / 1e6,
                         latency_ms=1e3 * self.lat_sum / self.deliveries if self.deliveries else np.nan,
                         bs_latency_ms=1e3 * self.lat_bs / self.n_bs if self.n_bs else np.nan,
                         sat_latency_ms=1e3 * self.lat_sat / self.n_sat if self.n_sat else np.nan,
                         sat_delivery_share=self.n_sat / self.deliveries if self.deliveries else 0.0,
                         sat_scheduling_share=self.sat_sched / self.attempts if self.attempts else 0.0,
                         attempts=self.attempts, deliveries=self.deliveries,
                         budget_violation_fraction=float((avg > self.ep.cfg.src.aoii_budget).mean()), solver="ppo")


# ----------------------------------------------------------------------------------------------
# PPO
# ----------------------------------------------------------------------------------------------
def _make_model(obs_dim, U, M, H, hidden=256):
    import torch, torch.nn as nn

    class ActorCritic(nn.Module):
        def __init__(self):
            super().__init__()
            self.body = nn.Sequential(nn.Linear(obs_dim, hidden), nn.Tanh(), nn.Linear(hidden, hidden), nn.Tanh())
            self.node_head = nn.Linear(hidden, U * M); self.period_head = nn.Linear(hidden, U * H); self.value = nn.Linear(hidden, 1)
            self.U, self.M, self.H = U, M, H

        def forward(self, obs):
            z = self.body(obs)
            return self.node_head(z).view(-1, self.U, self.M), self.period_head(z).view(-1, self.U, self.H), self.value(z).squeeze(-1)
    return ActorCritic()


def model_path(num_ues: int, sat_model: str, ntn: bool) -> pathlib.Path:
    return MODELS / f"ppo_U{num_ues}_{sat_model}_{'ntn' if ntn else 'plain'}.pt"


def train_ppo(cfg: FullConfig, train_seeds: List[int], episodes: int = 300, train_slots: int = 6000, lr: float = 3e-4,
              gamma: float = 0.98, lam: float = 0.95, clip: float = 0.2, epochs: int = 4, minibatch: int = 256,
              entropy: float = 0.01, seed: int = 0, log_every: int = 20, threads: int = 2, save: Optional[pathlib.Path] = None):
    import torch, torch.nn.functional as F
    from torch.distributions import Categorical
    torch.set_num_threads(threads); torch.manual_seed(seed); rng = np.random.default_rng(seed)
    import copy
    tcfg = copy.deepcopy(cfg); tcfg.sim.duration_slots = train_slots
    eps = [make_episode(tcfg, s) for s in train_seeds]            # training episodes, built once and reused
    env0 = OrchestrationEnv(eps[0]); U, M, H = env0.U, env0.M, env0.H
    model = _make_model(env0.obs_dim, U, M, H); opt = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    best_score, best_state = -np.inf, None
    t0 = time.time()
    for ep_i in range(episodes):
        env = OrchestrationEnv(eps[ep_i % len(eps)])
        obs = env.reset(); done = False
        O, A_n, A_p, LP, V, R, Dn = [], [], [], [], [], [], []
        while not done:
            ot = torch.as_tensor(obs).unsqueeze(0)
            with torch.no_grad():
                ln, lp, v = model(ot)
                # mask invisible nodes
                vis = torch.as_tensor(env.allowed()).unsqueeze(0)
                ln = ln.masked_fill(~vis, -1e9)
                dn, dp = Categorical(logits=ln), Categorical(logits=lp)
                an, ap = dn.sample(), dp.sample()
                logp = (dn.log_prob(an) + dp.log_prob(ap)).sum(-1)
            obs2, r, done, info = env.step(an.squeeze(0).numpy(), ap.squeeze(0).numpy())
            O.append(obs); A_n.append(an.squeeze(0).numpy()); A_p.append(ap.squeeze(0).numpy()); LP.append(float(logp)); V.append(float(v)); R.append(r); Dn.append(done)
            obs = obs2
        # GAE
        adv = np.zeros(len(R)); last = 0.0; next_v = 0.0
        for t in reversed(range(len(R))):
            nonterm = 0.0 if Dn[t] else 1.0
            delta = R[t] + gamma * next_v * nonterm - V[t]
            last = delta + gamma * lam * nonterm * last; adv[t] = last; next_v = V[t]
        ret = adv + np.array(V)
        adv = (adv - adv.mean()) / (adv.std() + 1e-8)
        O_t = torch.as_tensor(np.array(O)); An_t = torch.as_tensor(np.array(A_n)); Ap_t = torch.as_tensor(np.array(A_p))
        LP_t = torch.as_tensor(np.array(LP), dtype=torch.float32); ret_t = torch.as_tensor(ret, dtype=torch.float32); adv_t = torch.as_tensor(adv, dtype=torch.float32)
        n = len(R)
        for _ in range(epochs):
            perm = torch.randperm(n)
            for s in range(0, n, minibatch):
                b = perm[s:s + minibatch]
                ln, lp, v = model(O_t[b])
                dn, dp = Categorical(logits=ln), Categorical(logits=lp)
                logp = (dn.log_prob(An_t[b]) + dp.log_prob(Ap_t[b])).sum(-1)
                ratio = torch.exp(logp - LP_t[b])
                pg = -torch.min(ratio * adv_t[b], torch.clamp(ratio, 1 - clip, 1 + clip) * adv_t[b]).mean()
                vl = F.mse_loss(v, ret_t[b]); ent = (dn.entropy().sum(-1) + dp.entropy().sum(-1)).mean()
                loss = pg + 0.5 * vl - entropy * ent
                opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5); opt.step()
        res = env.result()
        history.append({"episode": ep_i, "return": float(np.sum(R)), "avg_aoii": res.average_aoii, "delivery": res.delivery_ratio, "time_s": time.time() - t0})
        if ep_i >= 50:
            score = -float(np.mean([h["avg_aoii"] for h in history[-50:]]))      # trailing mean AoII over 50 episodes
            if score > best_score:
                best_score, best_state = score, {k_: v_.detach().clone() for k_, v_ in model.state_dict().items()}
        if (ep_i + 1) % log_every == 0:
            h = history[-log_every:]
            print(f"  ep {ep_i+1}/{episodes}: return {np.mean([x['return'] for x in h]):.3f}  avg AoII {np.mean([x['avg_aoii'] for x in h]):.3f}  delivery {np.mean([x['delivery'] for x in h]):.3f}  {time.time()-t0:.0f}s", flush=True)
    if best_state is not None:
        model.load_state_dict(best_state)                      # keep the checkpoint with the best trailing-average AoII
    if save is not None:
        save.parent.mkdir(parents=True, exist_ok=True)
        torch.save({"state_dict": model.state_dict(), "obs_dim": env0.obs_dim, "U": U, "M": M, "H": H, "history": history, "best_trailing_aoii": -best_score,
                    "train_seeds": list(train_seeds), "episodes": episodes, "train_slots": train_slots}, save)
    return model, history


def run_ppo_policy(ep: Episode, path: pathlib.Path) -> RunResult:
    """Deterministic (argmax) evaluation of a trained model on a full episode."""
    import torch
    ck = torch.load(path, map_location="cpu")
    env = OrchestrationEnv(ep)
    assert (ck["U"], ck["M"], ck["H"]) == (env.U, env.M, env.H), "model/topology mismatch"
    model = _make_model(ck["obs_dim"], ck["U"], ck["M"], ck["H"]); model.load_state_dict(ck["state_dict"]); model.eval()
    obs = env.reset(); done = False; t0 = time.time()
    while not done:
        with torch.no_grad():
            ln, lp, _ = model(torch.as_tensor(obs).unsqueeze(0))
            vis = torch.as_tensor(env.allowed()).unsqueeze(0)
            ln = ln.masked_fill(~vis, -1e9)
            an = ln.argmax(-1).squeeze(0).numpy(); ap = lp.argmax(-1).squeeze(0).numpy()
        obs, _, done, _ = env.step(an, ap)
    res = env.result("ppo"); res.wall_time_s = time.time() - t0
    return res
