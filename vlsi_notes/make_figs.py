"""Generates every diagram used in the VLSI notes PDF (matplotlib, saved to figs/)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)

BLUE, RED, GREEN, ORANGE, GREY, PURPLE = "#1f5fa8", "#c0392b", "#1e8449", "#d68910", "#7f8c8d", "#6c3483"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "DejaVu Sans", "figure.dpi": 150})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), bbox_inches="tight", dpi=170, facecolor="white")
    plt.close(fig)


def arrow(ax, x0, y0, x1, y1, color="k", lw=1.5, style="-|>"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=12, color=color, lw=lw))


# ---------------------------------------------------------------- 1. metals / insulators / semiconductors
def fig_bands3():
    fig, axs = plt.subplots(1, 3, figsize=(9, 3.2))
    titles = ["Metal", "Semiconductor", "Insulator"]
    gaps = [None, 1.1, 5.5]
    for ax, t, g in zip(axs, titles, gaps):
        ax.set_xlim(0, 4); ax.set_ylim(0, 8); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(t, fontweight="bold")
        ax.set_ylabel("Energy")
        if g is None:
            ax.add_patch(Rectangle((1, 2.5), 2, 3.2, fc="#f5b7b1", ec="k"))
            ax.add_patch(Rectangle((1, 4.7), 2, 3, fc="#d6eaf8", ec="k", alpha=.8))
            ax.text(2, 5.2, "CB and VB\noverlap", ha="center", fontsize=9)
            ax.text(3.15, 7.2, "CB", fontsize=8); ax.text(3.15, 3, "VB", fontsize=8)
        else:
            top = 2.6
            ax.add_patch(Rectangle((1, 0.3), 2, top - 0.3, fc="#f5b7b1", ec="k", hatch="///"))
            ax.add_patch(Rectangle((1, top + g * 0.9), 2, 7.7 - top - g * 0.9, fc="#d6eaf8", ec="k"))
            ax.annotate("", xy=(2, top), xytext=(2, top + g * 0.9), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2))
            ax.text(2.1, top + g * 0.45 - .1, "$E_g$", color=GREEN, fontweight="bold", fontsize=11)
            ax.text(3.15, 7.2, "CB\n(empty)", fontsize=8); ax.text(3.15, 1, "VB\n(full)", fontsize=8)
    axs[1].text(2, 7.9, "small gap ≈ 1 eV", ha="center", fontsize=8)
    axs[2].text(2, 7.9, "huge gap > 5 eV", ha="center", fontsize=8)
    save(fig, "bands3")


# ---------------------------------------------------------------- 2. band formation from N atoms
def fig_band_formation():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    x = np.linspace(0, 1, 400)          # 0 = atoms far apart, 1 = atoms at crystal spacing
    mid, xm = 2.9, 0.55
    t = np.minimum(x / xm, 1)
    gap = np.where(x > xm, 1.5 * ((x - xm) / (1 - xm)) ** 0.8, 0)
    s_lo = 1.8 - 1.1 * x ** 1.3
    p_hi = 4.0 + 1.3 * x ** 1.3
    s_hi = np.where(x < xm, 1.8 + (mid - 1.8) * t ** 1.4, mid - gap / 2)
    p_lo = np.where(x < xm, 4.0 - (4.0 - mid) * t ** 1.4, mid + gap / 2)
    ax.fill_between(x, s_lo, s_hi, color="#f5b7b1", alpha=.9); ax.fill_between(x, p_lo, p_hi, color="#d6eaf8", alpha=.9)
    for y in (s_lo, s_hi, p_lo, p_hi): ax.plot(x, y, color=BLUE, lw=1.2)
    ax.plot([0, .08], [4, 4], color=BLUE, lw=3); ax.plot([0, .08], [1.8, 1.8], color=BLUE, lw=3)
    ax.axvline(1.0, color=GREY, ls="--", lw=1)
    ax.text(0.01, 4.3, "2p level\n(6N states, 2N e⁻)", fontsize=8, color=BLUE)
    ax.text(0.01, 1.05, "2s level\n(2N states, 2N e⁻)", fontsize=8, color=BLUE)
    ax.text(1.02, 4.2, "CB\n4N states\nempty", fontsize=8, va="center")
    ax.text(1.02, 1.5, "VB\n4N states\n4N e⁻ (full)", fontsize=8, va="center")
    ax.annotate("", xy=(1.0, mid - .75), xytext=(1.0, mid + .75), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2))
    ax.text(1.02, mid, "$E_g$", color=GREEN, fontsize=12, fontweight="bold", va="center")
    ax.text(xm, mid, "s and p bands\nmerge (8N states)", fontsize=7, ha="center", va="center", color=RED, bbox=dict(fc="white", ec="none", alpha=.8))
    ax.set_xlim(0, 1.25); ax.set_ylim(0, 6)
    ax.set_xlabel("←  atoms far apart                     spacing shrinks (r ↓)  →"); ax.set_ylabel("Energy")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Discrete levels widen into bands as atoms approach", fontsize=10)
    save(fig, "band_formation")


# ---------------------------------------------------------------- 3. E-k free vs crystal
def fig_ek():
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.4))
    k = np.linspace(-2.2, 2.2, 400)
    ax = axs[0]
    ax.plot(k, k ** 2, color=BLUE, lw=2)
    ax.set_title("Free electron: $E=\\hbar^2k^2/2m$"); ax.set_xlabel("k"); ax.set_ylabel("E")
    ax.set_xticks([]); ax.set_yticks([])
    ax = axs[1]
    # nearly-free-electron picture: parabola broken at k = ±pi/a, ±2pi/a with a gap each time
    g = 0.5
    k1 = np.linspace(-1, 1, 200); ax.plot(k1, k1 ** 2 - 0.0 * k1 - 0.15 * np.sin(np.pi * np.abs(k1) / 2) ** 6, color=BLUE, lw=2)
    for s_ in (-1, 1):
        k2 = np.linspace(1, 2, 200); ax.plot(s_ * k2, k2 ** 2 + g - 0.6 * (k2 - 1) * (2 - k2) * 0, color=BLUE, lw=2)
        k3 = np.linspace(2, 2.4, 100); ax.plot(s_ * k3, k3 ** 2 + 2 * g, color=BLUE, lw=2)
    for x in (-2, -1, 1, 2):
        ax.axvline(x, color=GREY, ls=":", lw=1)
    ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_xticklabels(["-2π/a", "-π/a", "0", "π/a", "2π/a"]); ax.set_yticks([])
    ax.annotate("forbidden gap\n(no states)", xy=(1, 1.25), xytext=(-0.4, 4.2), arrowprops=dict(arrowstyle="->", color=RED), color=RED, fontsize=9)
    ax.set_title("Crystal lattice: gaps open at ±nπ/a"); ax.set_xlabel("k"); ax.set_ylabel("E"); ax.set_ylim(-.3, 7)
    save(fig, "ek_free_crystal")


# ---------------------------------------------------------------- 4. direct vs indirect
def fig_direct_indirect():
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    k = np.linspace(-1, 1, 300)
    for ax, kind in zip(axs, ["direct", "indirect"]):
        vb = -0.5 - 1.6 * k ** 2
        if kind == "direct":
            cb = 1.5 + 2.2 * k ** 2
            ax.plot(k, cb, color=BLUE, lw=2); ax.plot(k, vb, color=RED, lw=2)
            ax.annotate("", xy=(0, 1.5), xytext=(0, -0.5), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2))
            ax.text(0.06, 0.5, "photon:\nvertical jump\n(k unchanged)", color=GREEN, fontsize=8)
            ax.set_title("Direct gap (GaAs, GaN)", fontweight="bold")
            ax.plot([0], [1.5], "o", color=BLUE); ax.plot([0], [-0.5], "o", color=RED)
        else:
            cb = 1.5 + 2.2 * (np.abs(k) - 0.65) ** 2 * 1.6 * 0 + 2.5 * np.minimum((np.abs(k) - 0.65) ** 2, 0.5) + 0.0
            cb = np.minimum(1.5 + 2.2 * k ** 2 + 0.6, 1.5 + 4 * (np.abs(k) - 0.7) ** 2)
            ax.plot(k, cb, color=BLUE, lw=2); ax.plot(k, vb, color=RED, lw=2)
            ax.plot([0], [-0.5], "o", color=RED); ax.plot([0.7], [1.5], "o", color=BLUE)
            arrow(ax, 0, -0.5, 0.7, 1.5, color=GREEN, lw=2)
            ax.text(-0.95, 0.55, "needs a PHONON\n(heat) to change k\nas well as energy", color=GREEN, fontsize=8)
            ax.set_title("Indirect gap (Si, Ge)", fontweight="bold")
        ax.axhline(1.5, color=GREY, lw=.6, ls=":"); ax.axhline(-0.5, color=GREY, lw=.6, ls=":")
        ax.text(-0.98, 1.65 if kind == "direct" else 1.3, "$E_c$", fontsize=9); ax.text(-0.98, -0.35, "$E_v$", fontsize=9)
        ax.set_xlabel("k"); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-1.5, 3.4)
    axs[0].set_ylabel("E")
    save(fig, "direct_indirect")


# ---------------------------------------------------------------- 5. Fermi function
def fig_fermi():
    E = np.linspace(-0.3, 0.3, 600)
    fig, ax = plt.subplots(figsize=(6, 3.6))
    kB = 8.617e-5
    ax.step([-0.3, 0, 0.3], [1, 0, 0], where="post", color="k", lw=2, label="T = 0 K")
    ax.plot([0, 0], [0, 1], color="k", lw=2)
    for T, c in [(200, GREEN), (300, BLUE), (600, RED)]:
        ax.plot(E, 1 / (1 + np.exp(E / (kB * T))), color=c, lw=1.8, label=f"T = {T} K")
    ax.axhline(.5, color=GREY, ls=":", lw=1); ax.axvline(0, color=GREY, ls=":", lw=1)
    ax.set_xlabel("E − E$_F$  (eV)"); ax.set_ylabel("f(E)  =  probability state is filled")
    ax.legend(frameon=False, fontsize=9); ax.set_title("Fermi–Dirac function")
    ax.text(0.01, 0.53, "f = ½ at E = E$_F$", fontsize=8)
    save(fig, "fermi")


# ---------------------------------------------------------------- 6. Ef position
def fig_ef_positions():
    fig, axs = plt.subplots(1, 3, figsize=(9.5, 3.3))
    data = [("Intrinsic\n n = p", 0.5, None), ("n-type\n n > p", 0.85, "Ed"), ("p-type\n p > n", 0.15, "Ea")]
    for ax, (t, pos, lvl) in zip(axs, data):
        ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(t, fontweight="bold")
        ax.plot([0.3, 3.7], [3, 3], color=BLUE, lw=3); ax.plot([0.3, 3.7], [1, 1], color=RED, lw=3)
        ax.text(3.75, 3, "$E_c$", va="center"); ax.text(3.75, 1, "$E_v$", va="center")
        y = 1 + 2 * pos
        ax.plot([0.3, 3.7], [y, y], color="k", ls="--", lw=1.6); ax.text(3.75, y, "$E_F$", va="center", fontweight="bold")
        if lvl == "Ed":
            ax.plot([1, 3], [2.8, 2.8], color=ORANGE, ls=":", lw=2); ax.text(1.2, 2.55, "$E_d$ (donors)", fontsize=8, color=ORANGE)
            ax.plot([1.6], [3.15], "o", color=BLUE, ms=5); ax.plot([2.2], [3.25], "o", color=BLUE, ms=5)
        if lvl == "Ea":
            ax.plot([1, 3], [1.2, 1.2], color=ORANGE, ls=":", lw=2); ax.text(1.2, 1.35, "$E_a$ (acceptors)", fontsize=8, color=ORANGE)
            ax.plot([1.6], [0.8], "o", mfc="white", mec=RED, ms=6); ax.plot([2.2], [0.7], "o", mfc="white", mec=RED, ms=6)
    axs[0].set_ylabel("Energy")
    save(fig, "ef_positions")


# ---------------------------------------------------------------- 7. doping lattices
def fig_doping():
    fig, axs = plt.subplots(1, 2, figsize=(8.5, 3.4))
    for ax, kind in zip(axs, ["n", "p"]):
        ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.set_aspect("equal"); ax.axis("off")
        for i in range(1, 5):
            for j in range(1, 5):
                x, y = i, j
                is_dopant = (i, j) == (2, 3) or (i, j) == (3, 3) and False
                if (i, j) == (3, 3):
                    ax.add_patch(Circle((x, y), .33, fc="#fad7a0", ec=ORANGE, lw=2))
                    ax.text(x, y, "P" if kind == "n" else "B", ha="center", va="center", fontweight="bold")
                else:
                    ax.add_patch(Circle((x, y), .33, fc="#d6eaf8", ec=BLUE))
                    ax.text(x, y, "Si", ha="center", va="center", fontsize=8)
                if i < 4: ax.plot([x + .33, x + .67], [y, y], color=GREY, lw=1.2)
                if j < 4: ax.plot([x, x], [y + .33, y + .67], color=GREY, lw=1.2)
        if kind == "n":
            ax.plot([3.55], [3.55], "o", color=BLUE, ms=8); ax.annotate("free electron\n(5th electron of P)", xy=(3.55, 3.55), xytext=(3.6, 4.5), fontsize=8, arrowprops=dict(arrowstyle="->"))
            ax.set_title("n-type: P (5 valence e⁻) → P⁺ fixed + free e⁻", fontsize=9, fontweight="bold")
        else:
            ax.plot([3.55], [3.55], "o", mfc="white", mec=RED, ms=9, mew=2); ax.annotate("hole\n(missing bond electron)", xy=(3.55, 3.55), xytext=(3.4, 4.5), fontsize=8, arrowprops=dict(arrowstyle="->"))
            ax.set_title("p-type: B (3 valence e⁻) → B⁻ fixed + free hole", fontsize=9, fontweight="bold")
    save(fig, "doping")


# ---------------------------------------------------------------- 8. mobility vs T
def fig_mobility_T():
    T = np.linspace(50, 600, 300)
    mu_ph = 1.0 * (T / 300) ** -1.5 * 1500
    mu_ii = 1.0 * (T / 300) ** 1.5 * 900
    tot = 1 / (1 / mu_ph + 1 / mu_ii)
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.plot(T, mu_ph, color=RED, ls="--", label="μ (phonon scattering) ↓ with T")
    ax.plot(T, mu_ii, color=GREEN, ls="--", label="μ (ionised impurity) ↑ with T")
    ax.plot(T, tot, color="k", lw=2.5, label="μ total  (1/μ = 1/μ$_{ph}$ + 1/μ$_{II}$)")
    ax.set_ylim(0, 2500); ax.set_xlabel("Temperature"); ax.set_ylabel("Mobility μ")
    ax.set_xticks([]); ax.set_yticks([]); ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_title("Mobility vs temperature: the hill")
    save(fig, "mobility_T")


# ---------------------------------------------------------------- 9. drift velocity vs E
def fig_vd_E():
    E = np.linspace(0, 10, 300)
    v = 1 / (1 / (1.0 * E + 1e-9) + 1 / 6)
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.plot(E, v, color=BLUE, lw=2.5)
    ax.axhline(6, color=RED, ls="--", lw=1); ax.text(6.2, 6.25, "saturation velocity $v_{sat}$", color=RED, fontsize=9)
    ax.text(0.5, 1.7, "low-E:\n$v_d=\\mu E$\n(slope = μ)", fontsize=9, color=BLUE)
    ax.set_xlabel("Electric field E"); ax.set_ylabel("Drift velocity $v_d$"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_ylim(0, 7.5)
    save(fig, "vd_E")


# ---------------------------------------------------------------- 10. drift & diffusion picture
def fig_drift_diffusion():
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.2))
    ax = axs[0]
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    ax.add_patch(Rectangle((0.5, 0.8), 9, 2.4, fc="#eaf2f8", ec="k"))
    xs = [0.9, 2.0, 3.4, 4.5, 5.7, 6.6, 7.8, 8.9]
    pts = [(xs[i], 1.2 + 1.6 * abs(np.sin(i * 1.7))) for i in range(len(xs))]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=BLUE, lw=1.5, marker="o", ms=4)
    ax.text(5, 3.55, "Drift: zig-zag path with a net push opposite to E", ha="center", fontsize=9, fontweight="bold")
    arrow(ax, 8.6, 0.4, 3.4, 0.4, color=RED, lw=2); ax.text(6, 0.05, "E field", ha="center", color=RED)
    ax.text(0.7, 2.4, "e⁻ →", color=BLUE, fontsize=10)
    ax = axs[1]
    x = np.linspace(0, 5, 100)
    ax.plot(x, 8 * np.exp(-x / 1.4), color=BLUE, lw=2.5)
    ax.set_title("Diffusion: from crowded to empty", fontsize=9, fontweight="bold")
    ax.set_xlabel("x"); ax.set_ylabel("n(x)"); ax.set_xticks([]); ax.set_yticks([])
    arrow(ax, 1, 6.5, 3.2, 6.5, color=GREEN, lw=2); ax.text(1.0, 7.1, "particles move →", color=GREEN, fontsize=9)
    arrow(ax, 3.2, 3.2, 1.0, 3.2, color=RED, lw=2); ax.text(1.0, 2.5, "electron current ←", color=RED, fontsize=9)
    ax.text(2.9, 1.0, "dn/dx < 0", fontsize=9)
    save(fig, "drift_diffusion")


# ---------------------------------------------------------------- 11. SRH
def fig_srh():
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    ax.set_xlim(0, 6); ax.set_ylim(0, 6); ax.axis("off")
    ax.plot([0.5, 5.5], [5, 5], color=BLUE, lw=3); ax.text(5.6, 5, "CB", va="center")
    ax.plot([0.5, 5.5], [1, 1], color=RED, lw=3); ax.text(5.6, 1, "VB", va="center")
    ax.plot([1.5, 4.5], [3, 3], color=ORANGE, ls="--", lw=2); ax.text(4.6, 3.15, "trap level\n(defect)", fontsize=8, color=ORANGE)
    ax.plot([2], [5.2], "o", color=BLUE)
    arrow(ax, 2, 4.9, 2, 3.2, color=BLUE, lw=2); ax.text(2.15, 4.0, "① e⁻ captured", fontsize=8, color=BLUE)
    arrow(ax, 3.2, 2.9, 3.2, 1.15, color=RED, lw=2); ax.text(3.35, 2.0, "② hole captured\n(e⁻ drops to VB)", fontsize=8, color=RED)
    ax.set_title("SRH recombination via a mid-gap trap", fontsize=10, fontweight="bold")
    save(fig, "srh")


# ---------------------------------------------------------------- 12. PN junction picture
def fig_pn_structure():
    fig, axs = plt.subplots(3, 1, figsize=(7, 6.6), sharex=True, gridspec_kw={"height_ratios": [1.5, 1, 1]})
    ax = axs[0]
    ax.set_xlim(-5, 5); ax.set_ylim(0, 3); ax.axis("off")
    ax.add_patch(Rectangle((-5, 0.5), 10, 2, fc="white", ec="k"))
    ax.add_patch(Rectangle((-1.2, 0.5), 2.2, 2, fc="#fdebd0", ec="none"))
    rng = np.random.RandomState(3)
    for i in range(14):
        x = rng.uniform(-4.8, -1.4); y = rng.uniform(0.7, 2.3)
        ax.plot(x, y, "o", mfc="white", mec=RED, ms=6)
        ax.plot(x + .25, y - .15, "s", color=BLUE, ms=3)
    for i in range(14):
        x = rng.uniform(1.4, 4.8); y = rng.uniform(0.7, 2.3)
        ax.plot(x, y, "o", color=BLUE, ms=6)
        ax.plot(x + .25, y - .15, "P", color=RED, ms=5)
    for y in (0.9, 1.5, 2.1):
        ax.text(-0.8, y, "−", color=BLUE, fontsize=12, ha="center", fontweight="bold"); ax.text(0.7, y, "+", color=RED, fontsize=12, ha="center", fontweight="bold")
    ax.text(-3, 2.75, "p-type (holes ○ + fixed acceptors ▪−)", ha="center", fontsize=8)
    ax.text(3, 2.75, "n-type (electrons ● + fixed donors +)", ha="center", fontsize=8)
    ax.text(0, 0.15, "depletion region  W = x$_p$ + x$_n$", ha="center", fontsize=9, color=ORANGE, fontweight="bold")
    ax.set_title("p–n junction at equilibrium", fontweight="bold")
    ax = axs[1]
    x = np.array([-5, -1.0, -1.0, 1.0, 1.0, 5])
    y = np.array([0, 0, -1, -1 + 0, 0, 0])
    ax.fill_between([-1.2, 0], [-1, -1], color="#aed6f1"); ax.fill_between([0, 1.0], [1, 1], color="#f5b7b1")
    ax.axhline(0, color="k", lw=.8)
    ax.text(-0.6, -1.5, "charge  −qN$_A$", ha="center", fontsize=8); ax.text(0.5, 1.25, "+qN$_D$", ha="center", fontsize=8)
    ax.set_ylim(-2, 2); ax.set_ylabel("charge ρ"); ax.set_yticks([])
    ax = axs[2]
    xx = np.linspace(-1.2, 1.0, 100)
    ax.plot([-5, -1.2], [0, 0], color=GREEN, lw=2); ax.plot([1, 5], [0, 0], color=GREEN, lw=2)
    ax.plot([-1.2, 0, 1.0], [0, -1.5, 0], color=GREEN, lw=2)
    ax.set_ylabel("E-field"); ax.set_yticks([]); ax.set_ylim(-2, 0.6)
    ax.text(0.1, -1.8, "peak at the metallurgical junction", fontsize=8, color=GREEN)
    ax.set_xticks([])
    save(fig, "pn_structure")


# ---------------------------------------------------------------- 13. band diagram pn
def fig_pn_bands():
    fig, ax = plt.subplots(figsize=(7, 3.6))
    x = np.linspace(-5, 5, 400)
    s = 1 / (1 + np.exp(-x * 2.2))
    Ec = 3 - 1.6 * s
    Ev = Ec - 1.5
    ax.plot(x, Ec, color=BLUE, lw=2.5); ax.plot(x, Ev, color=RED, lw=2.5)
    ax.axhline(2.0 - 0.1, xmin=0, xmax=1, color="k", ls="--", lw=1.4)
    ax.text(5.05, 1.9, "$E_F$ (flat)", va="center", fontsize=9)
    ax.text(5.05, Ec[-1], "$E_c$", va="center"); ax.text(5.05, Ev[-1], "$E_v$", va="center")
    ax.annotate("", xy=(-6.3, 3), xytext=(-6.3, 1.4), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2))
    ax.text(-6.1, 2.2, "$qV_0$", color=GREEN, fontsize=12, fontweight="bold")
    ax.text(-3.5, 3.4, "p-side", fontsize=10, fontweight="bold"); ax.text(2.5, 1.85, "n-side", fontsize=10, fontweight="bold")
    ax.axvspan(-1.0, 1.0, color="#fdebd0", alpha=.7); ax.text(0, .3, "depletion\nregion", ha="center", fontsize=8)
    ax.set_xlim(-7, 6.2); ax.set_ylim(0, 4); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Band diagram at equilibrium: flat E$_F$ = zero net current, tilted bands = built-in field")
    save(fig, "pn_bands")


# ---------------------------------------------------------------- 14. bias
def fig_pn_bias():
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    x = np.linspace(-5, 5, 300)
    s = 1 / (1 + np.exp(-x * 2.2))
    for ax, (t, drop, w) in zip(axs, [("Forward bias\nbarrier V₀−V$_F$ (smaller)", 0.8, .55), ("Equilibrium\nbarrier V₀", 1.6, 1.0), ("Reverse bias\nbarrier V₀+V$_R$ (bigger)", 2.6, 1.6)]):
        s = 1 / (1 + np.exp(-x * 2.2 / w))
        Ec = 3 - drop * s
        ax.plot(x, Ec, color=BLUE, lw=2.5); ax.plot(x, Ec - 1.5, color=RED, lw=2.5)
        ax.axvspan(-w, w, color="#fdebd0", alpha=.6)
        ax.set_title(t, fontsize=9, fontweight="bold"); ax.set_xticks([]); ax.set_yticks([])
        ax.text(0, 0.05, f"W ↔", ha="center", fontsize=8)
        ax.set_xlim(-5, 5); ax.set_ylim(-1, 4)
    axs[0].text(-4.8, 3.5, "W ↓ narrow", fontsize=8); axs[2].text(-4.8, 3.5, "W ↑ wide", fontsize=8)
    save(fig, "pn_bias")


# ---------------------------------------------------------------- 15. diode IV
def fig_diode_iv():
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    V = np.linspace(-1.0, 0.75, 500)
    Is = 0.02; VT = 0.0259 * 4
    I = Is * (np.exp(V / VT) - 1)
    # breakdown
    I = np.where(V < -0.85, -Is - 40 * (np.exp((-V - 0.85) / .04) - 1) * 0.05, I)
    ax.plot(V, np.clip(I, -6, 6), color=BLUE, lw=2.5)
    ax.axhline(0, color="k", lw=.8); ax.axvline(0, color="k", lw=.8)
    ax.text(-0.98, 0.5, "$V_{BR}$", color=RED, fontsize=10); ax.text(-0.5, -0.9, "$-I_s$ (tiny)", color=GREEN, fontsize=9)
    ax.text(0.15, 3.5, "forward:\nexponential", color=BLUE); ax.text(-0.95, -4.8, "breakdown\n(Zener / avalanche)", color=RED, fontsize=8)
    ax.set_ylim(-6, 6); ax.set_xlabel("V"); ax.set_ylabel("$I_D$"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Ideal diode I–V:  $I=I_s(e^{V/V_T}-1)$")
    save(fig, "diode_iv")


# ---------------------------------------------------------------- 16. excess minority carriers
def fig_excess_carriers():
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    xn = np.linspace(0, 5, 100); xp = -xn
    ax.plot(xn + .6, 1 + 6 * np.exp(-xn / 1.2), color=BLUE, lw=2.5)
    ax.plot(xp - .6, 1 + 4 * np.exp(-xn / 0.9), color=RED, lw=2.5)
    ax.axhline(1, color=GREY, ls=":", lw=1)
    ax.text(3.5, 1.25, "$p_{n0}$ (equilibrium)", fontsize=8); ax.text(-5.5, 1.25, "$n_{p0}$", fontsize=8)
    ax.text(0.7, 7.3, "$p_{n0}e^{V/V_T}$", color=BLUE, fontsize=9); ax.text(-3.2, 5.3, "$n_{p0}e^{V/V_T}$", color=RED, fontsize=9)
    ax.axvline(0.6, color=GREY, lw=.8); ax.axvline(-.6, color=GREY, lw=.8)
    ax.text(0, 8.3, "junction", ha="center", fontsize=8); ax.text(-.6, -0.2, "−x$_p$", ha="center", fontsize=8); ax.text(.6, -0.2, "x$_n$", ha="center", fontsize=8)
    ax.text(2.6, 4.3, "excess holes decay\nwith diffusion length $L_p$\n(they recombine)", fontsize=8, color=BLUE)
    ax.set_ylim(-.5, 8.8); ax.set_xticks([]); ax.set_yticks([])
    ax.set_ylabel("minority carrier concentration"); ax.set_title("Forward bias: minority-carrier injection")
    save(fig, "excess_carriers")


# ---------------------------------------------------------------- 17. BJT structure & flows
def fig_bjt():
    fig, ax = plt.subplots(figsize=(8, 3.9))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(Rectangle((1, 2), 3.2, 2, fc="#d6eaf8", ec="k")); ax.text(2.6, 3, "n⁺\nEmitter\n(heavy)", ha="center", va="center")
    ax.add_patch(Rectangle((4.2, 2), 1.4, 2, fc="#fadbd8", ec="k")); ax.text(4.9, 3, "p\nBase\n(thin,\nlight)", ha="center", va="center", fontsize=8)
    ax.add_patch(Rectangle((5.6, 2), 3.6, 2, fc="#d6eaf8", ec="k", alpha=.7)); ax.text(7.4, 3, "n\nCollector", ha="center", va="center")
    ax.text(4.2, 4.15, "EBJ", ha="center", fontsize=8, color=GREEN); ax.text(5.6, 4.15, "CBJ", ha="center", fontsize=8, color=GREEN)
    ax.plot([1, .3], [3, 3], color="k"); ax.text(.1, 3.25, "E", fontweight="bold")
    ax.plot([9.2, 9.9], [3, 3], color="k"); ax.text(9.95, 3.25, "C", fontweight="bold")
    ax.plot([4.9, 4.9], [2, 1.2], color="k"); ax.text(5.0, .85, "B", fontweight="bold")
    arrow(ax, 3.9, 3.4, 6.6, 3.4, color=BLUE, lw=3); ax.text(4.3, 3.65, "I$_{En}$ → I$_{Cn}$ (most electrons)", fontsize=8, color=BLUE)
    arrow(ax, 4.1, 2.5, 2.2, 2.5, color=RED, lw=2); ax.text(1.4, 2.15, "I$_{Ep}$ (wasted holes)", fontsize=8, color=RED)
    arrow(ax, 4.9, 2.9, 4.9, 1.5, color=PURPLE, lw=1.5); ax.text(5.1, 1.55, "I$_B$ (few recombine)", fontsize=8, color=PURPLE)
    ax.text(6, 5.3, "Active mode:  EBJ forward-biased (V$_{BE}$),  CBJ reverse-biased (V$_{CB}$)", ha="center", fontweight="bold", fontsize=9)
    save(fig, "bjt")


# ---------------------------------------------------------------- 18. BJT output + early
def fig_bjt_curves():
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.4))
    V = np.linspace(0, 6, 200)
    for ax, early in zip(axs, [False, True]):
        for k, Ib in enumerate([1, 2, 3]):
            ic = Ib * 2 * (1 - np.exp(-V / 0.4))
            if early:
                ic = ic * (1 + V / 8)
            ax.plot(V, ic, color=BLUE)
            ax.text(6.05, ic[-1], f"I$_B${'′' * k}", fontsize=8)
        ax.set_xlabel("V$_{CB}$ (or V$_{CE}$)"); ax.set_ylabel("I$_C$"); ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(-0.2, 6.6)
    axs[0].set_title("Ideal: flat in active region"); axs[1].set_title("Practical: slopes up (Early effect)")
    # extrapolate
    Vx = np.linspace(-8, 6, 50)
    ic = 6 * (1 + Vx / 8) * 1
    axs[1].set_xlim(-8.6, 6.6)
    axs[1].plot(Vx, ic, color=RED, ls="--", lw=1)
    axs[1].plot([-8], [0], "o", color=RED); axs[1].text(-8, 0.6, "−V$_A$\n(Early V)", color=RED, fontsize=8, ha="center")
    axs[1].set_ylim(-.5, 13)
    save(fig, "bjt_curves")


# ---------------------------------------------------------------- 19. BJT band diagram npn
def fig_bjt_bands():
    fig, ax = plt.subplots(figsize=(7.3, 3.3))
    x = np.linspace(0, 10, 500)
    def sm(x0, w): return 1 / (1 + np.exp(-(x - x0) / w))
    Ec = 1.0 + 1.6 * sm(3, .18) - 1.6 * sm(6.5, .18)
    Ev = Ec - 1.6
    ax.plot(x, Ec, color=BLUE, lw=2.5); ax.plot(x, Ev, color=RED, lw=2.5)
    ax.axhline(0.35, color="k", ls="--", lw=1.3); ax.text(10.1, .35, "$E_F$", va="center")
    for xx, l in [(1.5, "n (Emitter)"), (4.7, "p (Base)"), (8.3, "n (Collector)")]:
        ax.text(xx, 3.4, l, ha="center", fontweight="bold")
    ax.axvline(3, color=GREY, ls=":"); ax.axvline(6.5, color=GREY, ls=":")
    ax.text(3, -1.5, "EBJ", ha="center", fontsize=8); ax.text(6.5, -1.5, "CBJ", ha="center", fontsize=8)
    ax.set_ylim(-1.8, 3.8); ax.set_xlim(0, 10.6); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("npn at equilibrium: two barriers, one flat E$_F$")
    save(fig, "bjt_bands")


# ---------------------------------------------------------------- 20. MOS capacitor
def fig_mos_states():
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.7))
    cfg = [("Accumulation\nV$_G$ negative", "-", "holes ○ pile up", 0),
           ("Depletion\nV$_G$ small +", "+", "holes pushed away;\nfixed B⁻ ions exposed", 1),
           ("Inversion\nV$_G$ > V$_{th}$", "+", "electrons ● gather\n(p-substrate → n-layer)", 2)]
    for ax, (t, sign, cap, mode) in zip(axs, cfg):
        ax.set_xlim(0, 6); ax.set_ylim(-1.2, 7); ax.axis("off")
        ax.add_patch(Rectangle((1, 5.4), 4, .5, fc="#d5d8dc", ec="k")); ax.text(3, 6.15, "Gate (metal)", ha="center", fontsize=8)
        ax.add_patch(Rectangle((1, 4.9), 4, .5, fc="#f9e79f", ec="k")); ax.text(5.05, 5.1, "SiO₂", fontsize=7)
        ax.add_patch(Rectangle((1, 0.5), 4, 4.4, fc="#eaf2f8", ec="k")); ax.text(3, 0.7, "p-type Si", ha="center", fontsize=8)
        for i in range(5):
            ax.text(1.4 + i * .8, 5.65, sign if mode else "−", color=RED if mode else BLUE, ha="center", va="center", fontweight="bold", fontsize=9)
        rng = np.random.RandomState(mode + 4)
        if mode == 0:
            for i in range(9):
                ax.plot(1.3 + i * .42, 4.6 - (i % 2) * .25, "o", mfc="white", mec=RED, ms=6)
            for i in range(5): ax.plot(rng.uniform(1.3, 4.7), rng.uniform(1, 3.6), "o", mfc="white", mec=RED, ms=6)
        if mode >= 1:
            wd = 1.5 if mode == 1 else 2.2
            ax.add_patch(Rectangle((1, 4.9 - wd), 4, wd, fc="#fdebd0", ec="none", alpha=.9));
            for i in range(6): ax.text(1.5 + i * .65, 4.9 - wd / 2 - 0.15, "▪⁻", color=BLUE, fontsize=8, ha="center")
            ax.annotate("", xy=(5.4, 4.9 - wd), xytext=(5.4, 4.9), arrowprops=dict(arrowstyle="<->", color=ORANGE)); ax.text(5.45, 4.9 - wd / 2, "w", color=ORANGE, fontsize=9)
            for i in range(4): ax.plot(rng.uniform(1.3, 4.7), rng.uniform(0.9, 4.9 - wd - .3), "o", mfc="white", mec=RED, ms=6)
        if mode == 2:
            for i in range(8): ax.plot(1.3 + i * .45, 4.75, "o", color=BLUE, ms=6)
            ax.text(3, 5.02, "", fontsize=1)
        ax.set_title(t, fontsize=9, fontweight="bold"); ax.text(3, -.2, cap, ha="center", fontsize=8, va="top")
    save(fig, "mos_states")


def fig_mos_cv():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    V = np.linspace(-3, 3, 400)
    C = np.where(V < -0.3, 1.0, np.maximum(0.3, 1 - 0.7 * ((V + .3) / 1.3)))
    C = np.where(V < -0.3, 1, np.where(V < 1.0, 1 - 0.7 * ((V + .3) / 1.3), .3))
    ax.plot(V[V < 1], C[V < 1], color=BLUE, lw=2.5)
    ax.plot(V[V >= 1], C[V >= 1], color=BLUE, lw=2.5, label="high frequency")
    ax.plot(V[V >= 1], .3 + .7 * (1 - np.exp(-(V[V >= 1] - 1) * 1.6)), color=GREEN, ls="--", lw=2, label="low frequency")
    ax.axvline(1, color=GREY, ls=":"); ax.text(1.05, .05, "V$_{th}$\n(w = w$_m$)", fontsize=8)
    ax.text(-2.8, 1.04, "accumulation: C = C$_{ox}$", fontsize=8)
    ax.text(-.3, .55, "depletion:\nC$_{dep}$ ↓ as w ↑", fontsize=8, color=RED)
    ax.text(1.2, .22, "C$_{min}$", fontsize=8); ax.text(2.0, .75, "inversion", fontsize=8)
    ax.set_ylim(0, 1.2); ax.set_xlabel("Gate voltage V$_G$  →"); ax.set_ylabel("C / C$_{ox}$"); ax.set_xticks([]); ax.set_yticks([0.3, 1]); ax.set_yticklabels(["", "1"])
    ax.legend(frameon=False, fontsize=8, loc="center right"); ax.set_title("MOS capacitor C–V curve (p-type substrate)")
    save(fig, "mos_cv")


# ---------------------------------------------------------------- 21. MOSFET structure & operation
def fig_nmos():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.9))
    ax = axs[0]
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(Rectangle((0.3, 0.5), 11.4, 3.3, fc="#fdebd0", ec="k")); ax.text(6, 0.9, "p-type substrate (Body / Bulk)", ha="center", fontsize=9)
    ax.add_patch(Rectangle((1.7, 2.8), 2.6, 1.0, fc="#aed6f1", ec="k")); ax.text(3, 3.3, "n⁺", ha="center")
    ax.add_patch(Rectangle((7.7, 2.8), 2.6, 1.0, fc="#aed6f1", ec="k")); ax.text(9, 3.3, "n⁺", ha="center")
    ax.add_patch(Rectangle((4.3, 3.8), 3.4, .35, fc="#f9e79f", ec="k")); ax.text(6, 3.9, "SiO₂", ha="center", fontsize=7)
    ax.add_patch(Rectangle((4.3, 4.15), 3.4, .45, fc="#aab7b8", ec="k")); ax.text(6, 4.25, "Gate", ha="center", fontsize=8)
    ax.add_patch(Rectangle((.6, 3.3), .9, .5, fc="#f5cba7", ec="k")); ax.text(1.05, 3.4, "p⁺", ha="center", fontsize=7)
    for x, y, l in [(3, 3.8, "S"), (9, 3.8, "D"), (6, 4.6, "G"), (1.05, 3.8, "B")]:
        ax.plot([x, x], [y, y + .9 if l != "G" else y + .7], color="k"); ax.text(x, y + (1.05 if l != "G" else .85), l, ha="center", fontweight="bold")
    ax.annotate("", xy=(7.7, 2.6), xytext=(4.3, 2.6), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.8)); ax.text(6, 2.1, "L (channel length)", ha="center", fontsize=8, color=GREEN)
    ax.set_title("nMOS structure", fontweight="bold")
    ax = axs[1]
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(Rectangle((0.3, 0.5), 11.4, 3.3, fc="#fdebd0", ec="k"))
    ax.add_patch(Rectangle((1.7, 2.8), 2.6, 1.0, fc="#aed6f1", ec="k")); ax.text(3, 3.3, "n⁺ S", ha="center")
    ax.add_patch(Rectangle((7.7, 2.8), 2.6, 1.0, fc="#aed6f1", ec="k")); ax.text(9, 3.3, "n⁺ D", ha="center")
    ax.add_patch(Rectangle((4.3, 3.8), 3.4, .35, fc="#f9e79f", ec="k"))
    ax.add_patch(Rectangle((4.3, 4.15), 3.4, .45, fc="#aab7b8", ec="k")); ax.text(6, 4.25, "V$_{GS}$ > V$_{th}$", ha="center", fontsize=8)
    ax.add_patch(Rectangle((4.3, 3.45), 3.4, .35, fc="#5dade2", ec="none")); ax.text(6, 3.0, "inversion channel of e⁻", ha="center", fontsize=8, color=BLUE)
    for i in range(6): ax.plot(4.6 + i * .6, 3.62, "o", color=BLUE, ms=4)
    arrow(ax, 4.0, 3.2, 8.3, 3.2, color=BLUE, lw=0)  # invisible
    ax.text(6, 1.6, "electrons flow S → D\nconventional current D → S", ha="center", fontsize=9, color=RED)
    ax.set_title("Channel formed (ON)", fontweight="bold")
    save(fig, "nmos")


def fig_nwell():
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(Rectangle((0.3, 0.4), 13.4, 3.6, fc="#fdebd0", ec="k")); ax.text(2, 0.7, "p-substrate", fontsize=9)
    ax.add_patch(Rectangle((7, 1.2), 6.2, 2.8, fc="#d6eaf8", ec="k")); ax.text(10.1, 1.5, "n-well", ha="center", fontsize=9)
    def blk(x, w, t, c): ax.add_patch(Rectangle((x, 3.1), w, .9, fc=c, ec="k")); ax.text(x + w / 2, 3.45, t, ha="center", fontsize=8)
    blk(.5, .8, "p⁺", "#f5cba7"); blk(1.6, 1.8, "n⁺", "#aed6f1"); blk(4.6, 1.8, "n⁺", "#aed6f1")
    ax.add_patch(Rectangle((3.4, 4.0), 1.2, .35, fc="#aab7b8", ec="k")); ax.text(4.0, 4.5, "G", ha="center")
    blk(7.3, .8, "n⁺", "#aed6f1"); blk(8.4, 1.8, "p⁺", "#f5cba7"); blk(11.2, 1.8, "p⁺", "#f5cba7")
    ax.add_patch(Rectangle((10.2, 4.0), 1.0, .35, fc="#aab7b8", ec="k")); ax.text(10.7, 4.5, "G", ha="center")
    ax.text(3.3, 5.3, "nMOS", ha="center", fontweight="bold"); ax.text(10.1, 5.3, "pMOS", ha="center", fontweight="bold")
    ax.set_title("CMOS n-well process: both transistor types on one chip", fontsize=10)
    save(fig, "nwell")


def fig_mos_iv():
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.5))
    V = np.linspace(0, 5, 300); Vt = 1.0
    ax = axs[0]
    for Vg, c in [(2, GREEN), (3, BLUE), (4, RED)]:
        Vov = Vg - Vt
        I = np.where(V < Vov, (Vov * V - V ** 2 / 2), Vov ** 2 / 2)
        ax.plot(V, I, color=c, lw=2); ax.text(5.05, I[-1], f"V$_{{GS}}$={Vg}V", fontsize=8, color=c)
    vv = np.linspace(0, 3, 100); ax.plot(vv, vv * 0 + 0, alpha=0)
    Vo = np.linspace(0, 3, 100); ax.plot(Vo, Vo ** 2 / 2, ls="--", color=GREY); ax.text(1.5, 5.2, "V$_{DS}$ = V$_{GS}$−V$_{th}$\n(pinch-off edge)", fontsize=8, color=GREY)
    ax.set_xlabel("V$_{DS}$"); ax.set_ylabel("I$_D$"); ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 6.3)
    ax.set_title("Output characteristics", fontsize=10)
    ax.text(.1, 0.3, "triode\n(linear)", fontsize=8); ax.text(3.5, 5.5, "saturation", fontsize=8)
    ax = axs[1]
    Vg = np.linspace(0, 4, 300)
    I = np.where(Vg > Vt, (Vg - Vt) ** 2, 0)
    ax.plot(Vg, I, color=BLUE, lw=2.5); ax.axvline(Vt, color=GREY, ls=":"); ax.text(Vt + .05, 6, "V$_{th}$", fontsize=9)
    ax.text(.2, .6, "cutoff\n(OFF)", fontsize=8); ax.set_xlabel("V$_{GS}$"); ax.set_ylabel("I$_D$ (saturation)"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Transfer characteristic: I$_D$ ∝ (V$_{GS}$−V$_{th}$)²", fontsize=10)
    save(fig, "mos_iv")


def fig_pinchoff():
    fig, axs = plt.subplots(1, 3, figsize=(10, 2.9))
    labels = ["Small V$_{DS}$: uniform channel\n(resistor-like, TRIODE)", "V$_{DS}$ = V$_{GS}$−V$_{th}$:\nchannel just pinches at drain", "V$_{DS}$ larger: pinch-off point\nmoves toward source (SATURATION)"]
    for ax, l, i in zip(axs, labels, range(3)):
        ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
        ax.add_patch(Rectangle((0, 0.3), 10, 2.2, fc="#fdebd0", ec="k"))
        ax.add_patch(Rectangle((0.3, 1.8), 1.8, .7, fc="#aed6f1", ec="k")); ax.add_patch(Rectangle((7.9, 1.8), 1.8, .7, fc="#aed6f1", ec="k"))
        ax.add_patch(Rectangle((2.1, 2.5), 5.8, .3, fc="#f9e79f", ec="k")); ax.add_patch(Rectangle((2.1, 2.8), 5.8, .4, fc="#aab7b8", ec="k"))
        if i == 0:
            xs = [2.1, 7.9, 7.9, 2.1]; ys = [2.5, 2.5, 2.0, 2.0]
        elif i == 1:
            xs = [2.1, 7.9, 7.9, 2.1]; ys = [2.5, 2.5, 2.48, 1.85]
        else:
            xs = [2.1, 6.6, 7.9, 2.1]; ys = [2.5, 2.5, 2.5, 1.85]
        if i == 0: ax.fill([2.1, 7.9, 7.9, 2.1], [2.5, 2.5, 1.9, 1.75], color="#5dade2")
        if i == 1: ax.fill([2.1, 7.9, 7.9, 2.1], [2.5, 2.5, 2.48, 1.75], color="#5dade2")
        if i == 2: ax.fill([2.1, 6.9, 2.1], [2.5, 2.5, 1.75], color="#5dade2"); ax.plot([6.9], [2.5], "o", color=RED)
        ax.text(5, 3.9, l, ha="center", fontsize=8, va="center")
        ax.text(1.0, 2.1, "S", ha="center", fontsize=8); ax.text(8.8, 2.1, "D", ha="center", fontsize=8)
    save(fig, "pinchoff")


def fig_inverter():
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.4))
    ax = axs[0]; ax.set_xlim(0, 8); ax.set_ylim(0, 8); ax.axis("off")
    ax.plot([4, 4], [7.3, 6.3], color="k"); ax.text(4.2, 7.4, "V$_{DD}$", fontsize=9)
    ax.add_patch(Rectangle((3.4, 4.6), 1.2, 1.7, fc="#fadbd8", ec="k")); ax.text(4, 5.45, "pMOS", ha="center", fontsize=9)
    ax.add_patch(Rectangle((3.4, 1.8), 1.2, 1.7, fc="#d6eaf8", ec="k")); ax.text(4, 2.65, "nMOS", ha="center", fontsize=9)
    ax.plot([4, 4], [4.6, 3.5], color="k"); ax.plot([4, 6.6], [4.05, 4.05], color="k"); ax.text(6.7, 4.0, "V$_{out}$", va="center", fontsize=9)
    ax.plot([4, 4], [1.8, 1.0], color="k"); ax.text(4.2, .5, "GND", fontsize=9)
    ax.plot([1.2, 2.6, 2.6], [4.05, 4.05, 2.65], color="k"); ax.plot([2.6, 3.4], [5.45, 5.45], color="k"); ax.plot([2.6, 2.6], [5.45, 2.65], color="k"); ax.plot([2.6, 3.4], [2.65, 2.65], color="k")
    ax.text(.1, 4.0, "V$_{in}$", va="center", fontsize=9)
    ax.set_title("CMOS inverter", fontweight="bold")
    ax = axs[1]
    vin = np.linspace(0, 5, 300)
    vout = 5 / (1 + np.exp((vin - 2.5) * 4))
    ax.plot(vin, vout, color=BLUE, lw=2.5); ax.plot([0, 5], [0, 5], color=GREY, ls=":")
    ax.text(.3, 5.2, "V$_{in}$ = 0 → V$_{out}$ = V$_{DD}$ (1)", fontsize=8); ax.text(2.6, .5, "V$_{in}$ = V$_{DD}$ → V$_{out}$ = 0", fontsize=8)
    ax.set_xlabel("V$_{in}$"); ax.set_ylabel("V$_{out}$"); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-.3, 6)
    ax.set_title("Voltage transfer curve", fontweight="bold")
    save(fig, "inverter")


def fig_ic_scale():
    fig, ax = plt.subplots(figsize=(7, 2.8))
    names = ["SSI\n< 10 gates", "MSI\n10–100", "LSI\n100–10⁴", "VLSI\n10⁴–10⁶", "ULSI / today\n> 10⁶ (billions)"]
    for i, n in enumerate(names):
        ax.add_patch(Rectangle((i * 1.9, 0.5 + 0.35 * i), 1.7, 0.6 + .35 * i, fc=plt.cm.Blues(0.25 + 0.15 * i), ec="k"))
        ax.text(i * 1.9 + .85, 0.15, n, ha="center", fontsize=8, va="top")
    ax.set_xlim(-.2, 9.6); ax.set_ylim(-.9, 3.3); ax.axis("off"); ax.set_title("Integration levels: more transistors on one chip", fontweight="bold")
    save(fig, "ic_scale")


def fig_capacitors():
    fig, axs = plt.subplots(1, 2, figsize=(8, 2.9))
    ax = axs[0]; ax.set_xlim(0, 6); ax.set_ylim(0, 5); ax.axis("off")
    ax.add_patch(Rectangle((1, 3), 4, .4, fc="#aab7b8", ec="k")); ax.add_patch(Rectangle((1, 2.4), 4, .6, fc="#f9e79f", ec="k")); ax.add_patch(Rectangle((1, 2), 4, .4, fc="#aab7b8", ec="k"))
    ax.text(3, 1.3, "MIM: metal–insulator–metal\nC = ε A / d  (constant)", ha="center", fontsize=9)
    ax.set_title("Ordinary capacitor", fontweight="bold")
    ax = axs[1]; ax.set_xlim(0, 6); ax.set_ylim(0, 5); ax.axis("off")
    ax.add_patch(Rectangle((1, 3.4), 4, .4, fc="#aab7b8", ec="k")); ax.add_patch(Rectangle((1, 2.8), 4, .6, fc="#f9e79f", ec="k")); ax.add_patch(Rectangle((1, 1.8), 4, 1.0, fc="#eaf2f8", ec="k"))
    ax.text(3, 1.0, "MOS / MIS: metal–oxide–semiconductor\nC changes with V$_G$", ha="center", fontsize=9)
    ax.set_title("MOS capacitor", fontweight="bold")
    save(fig, "capacitors")


ALL = [fig_bands3, fig_band_formation, fig_ek, fig_direct_indirect, fig_fermi, fig_ef_positions, fig_doping,
       fig_mobility_T, fig_vd_E, fig_drift_diffusion, fig_srh, fig_pn_structure, fig_pn_bands, fig_pn_bias,
       fig_diode_iv, fig_excess_carriers, fig_bjt, fig_bjt_curves, fig_bjt_bands, fig_mos_states, fig_mos_cv,
       fig_nmos, fig_nwell, fig_mos_iv, fig_pinchoff, fig_inverter, fig_ic_scale, fig_capacitors]

if __name__ == "__main__":
    for f in ALL:
        f()
        print("ok", f.__name__)
