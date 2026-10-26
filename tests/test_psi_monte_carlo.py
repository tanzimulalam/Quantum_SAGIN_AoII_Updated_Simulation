"""Monte-Carlo validation of the renewal-interval AoII formula implemented in sentinel.sources.psi_table."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from sentinel.sources import birth_death_matrix, distortion_matrix, psi_table, stationary_distribution


def mc_time_average_aoii(P, Y, slots=1_500_000, seed=1):
    rng = np.random.default_rng(seed)
    n = P.shape[0]
    pi = stationary_distribution(P)
    x = rng.choice(n, p=pi)
    cum = np.cumsum(P, axis=1)
    est, last_correct, acc = x, 0, 0.0
    u = rng.random(slots)
    for t in range(slots):
        if t % Y == 0:
            est = x
        if x == est:
            last_correct = t
        acc += (t - last_correct) * abs(x - est)
        x = int(np.searchsorted(cum[x], u[t]))
        x = min(x, n - 1)
    return acc / slots


if __name__ == "__main__":
    f = distortion_matrix(4)
    worst = 0.0
    for p_stay in (0.90, 0.95, 0.99):
        P = birth_death_matrix(4, p_stay)
        psi = psi_table(P, f, 100)
        for Y in (5, 10, 20, 50):
            cf = psi[Y] / Y
            mc = mc_time_average_aoii(P, Y)
            rel = abs(cf - mc) / mc
            worst = max(worst, rel)
            print(f"p_stay={p_stay} Y={Y:>2}: closed form {cf:.4f}  Monte Carlo {mc:.4f}  rel.err {100*rel:.2f}%")
    assert worst < 0.03, f"closed form disagrees with Monte Carlo: {worst:.3f}"
    print("PASS: Psi(Y)/Y matches Monte Carlo within 3% on all cases")
