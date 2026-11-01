"""Figure 1: the system model, drawn to match the paper (two satellite-ground domains, shared LEO satellites,
base stations with edge servers, monitored sources, a non-line-of-sight pass, a handover, and the classical
coordinator). Writes figures/system_model.pdf and .png.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Ellipse, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
C_SAT, C_BS, C_UE, C_DOM, C_COORD, C_NLOS = "#1f4e79", "#2e7d32", "#b23a3a", "#9e9e9e", "#6a1b9a", "#8d6e63"


def satellite(ax, x, y, label):
    ax.add_patch(Rectangle((x - 0.22, y - 0.14), 0.44, 0.28, fc=C_SAT, ec="none"))
    for sx in (-0.7, 0.7):
        ax.add_patch(Rectangle((x + sx - 0.42, y - 0.09), 0.84, 0.18, fc="#5b8dd9", ec=C_SAT, lw=0.6))
    ax.plot([x - 0.28, x - 0.22], [y, y], color=C_SAT, lw=1); ax.plot([x + 0.22, x + 0.28], [y, y], color=C_SAT, lw=1)
    ax.text(x, y + 0.42, label, ha="center", va="bottom", fontsize=8, color=C_SAT)
    ax.text(x, y - 0.46, "edge server", ha="center", va="top", fontsize=6.5, color=C_SAT, style="italic")


def base_station(ax, x, y, label):
    ax.add_patch(Polygon([[x - 0.16, y], [x + 0.16, y], [x, y + 1.1]], closed=True, fc=C_BS, ec="none"))
    for h in (0.35, 0.65):
        ax.plot([x - 0.12, x + 0.12], [y + h, y + h], color=C_BS, lw=1.2)
    ax.add_patch(FancyBboxPatch((x - 0.32, y - 0.42), 0.64, 0.3, boxstyle="round,pad=0.02", fc="white", ec=C_BS, lw=0.9))
    ax.text(x, y - 0.27, "edge server", ha="center", va="center", fontsize=6.5, color=C_BS)
    ax.text(x, y + 1.22, label, ha="center", va="bottom", fontsize=8, color=C_BS)


def ue(ax, x, y, label):
    ax.add_patch(Circle((x, y), 0.17, fc=C_UE, ec="none"))
    ax.add_patch(Circle((x, y), 0.07, fc="white", ec="none"))
    ax.text(x, y - 0.3, label, ha="center", va="top", fontsize=6.5, color=C_UE)


def source(ax, x, y):
    """A small three-state Markov chain beside a UE: the monitored process."""
    for dx in (-0.26, 0.0, 0.26):
        ax.add_patch(Circle((x + dx, y), 0.075, fc="white", ec="#444", lw=0.7))
    ax.annotate("", xy=(x - 0.075, y + 0.03), xytext=(x - 0.185, y + 0.03), arrowprops=dict(arrowstyle="->", lw=0.6, color="#444"))
    ax.annotate("", xy=(x + 0.185, y - 0.03), xytext=(x + 0.075, y - 0.03), arrowprops=dict(arrowstyle="->", lw=0.6, color="#444"))
    ax.text(x, y + 0.13, "$X_i(t)$", ha="center", va="bottom", fontsize=6.5, color="#444")


def link(ax, p, q, color, ls="-", lw=1.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=7, color=color, lw=lw, ls=ls, shrinkA=6, shrinkB=10))


def main():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(-0.2, 12.2); ax.set_ylim(-1.15, 7.0); ax.set_aspect("equal"); ax.axis("off")

    # domains: controller label top-left, domain name top-right
    for x0, name in ((0.1, "Domain $\\mathcal{D}_1$"), (6.3, "Domain $\\mathcal{D}_2$")):
        ax.add_patch(FancyBboxPatch((x0, -1.0), 5.7, 3.4, boxstyle="round,pad=0.05", fc="#f6f6f6", ec=C_DOM, lw=0.9, ls="--"))
        ax.text(x0 + 5.55, 2.3, name, fontsize=8, color="#555", ha="right", va="top")
        ax.text(x0 + 0.2, 2.3, "domain controller\n(compact QUBO, XY-QAOA)", fontsize=6.5, color=C_COORD, ha="left", va="top")

    # satellites (shared between the domains), their motion and the handover
    satellite(ax, 3.6, 5.7, "LEO satellite $s_1$ (setting)")
    satellite(ax, 8.6, 6.0, "LEO satellite $s_2$ (rising)")
    ax.annotate("", xy=(1.4, 5.7), xytext=(2.6, 5.7), arrowprops=dict(arrowstyle="->", lw=0.8, color=C_SAT, ls=":"))
    ax.annotate("", xy=(10.9, 6.0), xytext=(9.7, 6.0), arrowprops=dict(arrowstyle="->", lw=0.8, color=C_SAT, ls=":"))
    ax.annotate("", xy=(7.5, 5.9), xytext=(4.7, 5.8), arrowprops=dict(arrowstyle="<->", lw=0.8, color=C_SAT))
    ax.text(6.1, 5.95, "handover", fontsize=7, color=C_SAT, ha="center", va="bottom")

    # base stations with edge servers
    base_station(ax, 1.3, 0.1, "BS $b_1$")
    base_station(ax, 7.5, 0.1, "BS $b_2$")

    # UEs (sources drawn to the right of each UE)
    ue(ax, 3.0, 0.5, "$u_1$"); source(ax, 3.75, 0.55)
    ue(ax, 5.0, -0.5, "$u_2$"); source(ax, 5.8, -0.45)
    ue(ax, 9.3, 0.5, "$u_3$"); source(ax, 10.05, 0.55)
    ue(ax, 11.2, -0.5, "$u_4$"); source(ax, 10.4, -0.45)

    # links: BS (green, with acknowledgement), satellite (blue), blocked non-line-of-sight pass (brown, dashed)
    link(ax, (3.0, 0.5), (1.5, 0.5), C_BS)
    ax.annotate("", xy=(2.85, 0.32), xytext=(1.7, 0.32), arrowprops=dict(arrowstyle="->", lw=0.6, color=C_BS, ls=":"))
    ax.text(2.25, 0.2, "ACK", fontsize=6, color=C_BS, ha="center", va="top")
    link(ax, (5.0, -0.5), (3.6, 5.4), C_SAT)
    link(ax, (9.3, 0.5), (8.6, 5.7), C_SAT)
    link(ax, (11.2, -0.5), (8.6, 5.7), C_NLOS, ls="--")
    ax.add_patch(Ellipse((9.85, 3.35), 0.9, 1.25, fc="#c8e6c9", ec=C_NLOS, lw=0.8))
    ax.add_patch(Rectangle((9.76, 2.55), 0.18, 0.35, fc=C_NLOS, ec="none"))
    ax.text(10.95, 3.65, "NLOS pass\n(blocked)", fontsize=6.5, color=C_NLOS, ha="center", va="bottom")

    # classical coordinator between the satellites and the domains
    ax.add_patch(FancyBboxPatch((4.3, 3.4), 3.4, 1.05, boxstyle="round,pad=0.05", fc="#f3e5f5", ec=C_COORD, lw=1.0))
    ax.text(6.0, 4.15, "Classical coordinator", ha="center", va="center", fontsize=8, color=C_COORD)
    ax.text(6.0, 3.7, "scenario weights $\\mathbf{w}$, ADMM targets $z_{jk}$,\ncertificate $\\eta$", ha="center", va="center", fontsize=6.5, color=C_COORD)
    ax.annotate("", xy=(2.3, 2.45), xytext=(4.5, 3.4), arrowprops=dict(arrowstyle="<->", lw=0.8, color=C_COORD))
    ax.annotate("", xy=(8.5, 2.45), xytext=(7.5, 3.4), arrowprops=dict(arrowstyle="<->", lw=0.8, color=C_COORD))

    fig.tight_layout(pad=0.2)
    fig.savefig(ROOT / "figures" / "system_model.pdf"); fig.savefig(ROOT / "figures" / "system_model.png", dpi=200)
    print("written")


if __name__ == "__main__":
    main()
