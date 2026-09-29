"""Figures A: bands, semiconductors, diodes, special diodes."""
from figs_common import *
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch


def bands():
    fig, axs = plt.subplots(1, 3, figsize=(9.2, 3.5))
    titles = ["Metal (conductor)", "Semiconductor", "Insulator"]
    for ax, t in zip(axs, titles):
        ax.set_xlim(0, 4); ax.set_ylim(0, 10); ax.axis("off"); ax.set_title(t, fontsize=11, color=INK, weight="bold")
    # metal: overlapping bands
    ax = axs[0]
    ax.add_patch(Rectangle((0.6, 4.6), 2.8, 4.4, fc="#cfe0ff", ec=INK)); ax.text(2, 8.4, "Conduction band", ha="center", fontsize=9)
    ax.add_patch(Rectangle((0.6, 1.0), 2.8, 4.6, fc="#ffe3b8", ec=INK)); ax.text(2, 1.5, "Valence band", ha="center", fontsize=9)
    ax.add_patch(Rectangle((0.6, 4.6), 2.8, 1.0, fc="#e6d5ff", ec=None, alpha=.9)); ax.text(2, 5.1, "overlap", ha="center", fontsize=8.5)
    ax.text(2, 3.0, "no gap: electrons\nfree to move", ha="center", fontsize=9, color=RED)
    # semiconductor
    ax = axs[1]
    ax.add_patch(Rectangle((0.6, 6.0), 2.8, 3.0, fc="#cfe0ff", ec=INK)); ax.text(2, 8.2, "Conduction band", ha="center", fontsize=9)
    ax.add_patch(Rectangle((0.6, 1.0), 2.8, 3.4, fc="#ffe3b8", ec=INK)); ax.text(2, 1.6, "Valence band", ha="center", fontsize=9)
    ax.annotate("", xy=(3.75, 6.0), xytext=(3.75, 4.4), arrowprops=dict(arrowstyle="<|-|>", color=INK))
    ax.text(2, 5.15, "small gap $E_g$\n1.1 eV (Si), 0.74 eV (Ge)", ha="center", va="center", fontsize=8.4, color=GREEN)
    for x, y in [(1.0, 3.3), (1.6, 3.0), (2.2, 3.4), (2.8, 3.1)]:
        ax.plot(x, y, "o", color=BLUE, ms=5)
    ax.plot(1.8, 6.5, "o", color=BLUE, ms=5); ax.plot(2.6, 7.0, "o", color=BLUE, ms=5)
    ax.plot(1.2, 3.9, "o", mfc="white", mec=RED, ms=6); ax.text(2.0, 0.35, "● electron   ○ hole (empty seat)", ha="center", fontsize=8)
    # insulator
    ax = axs[2]
    ax.add_patch(Rectangle((0.6, 7.6), 2.8, 1.5, fc="#cfe0ff", ec=INK)); ax.text(2, 8.3, "Conduction band", ha="center", fontsize=9)
    ax.add_patch(Rectangle((0.6, 0.8), 2.8, 3.0, fc="#ffe3b8", ec=INK)); ax.text(2, 1.4, "Valence band", ha="center", fontsize=9)
    ax.annotate("", xy=(3.75, 7.6), xytext=(3.75, 3.8), arrowprops=dict(arrowstyle="<|-|>", color=INK))
    ax.text(2, 5.7, "huge gap\n$E_g$ ≈ 6–7 eV\n(diamond 7 eV)", ha="center", fontsize=8.8, color=RED)
    fig.subplots_adjust(wspace=0.05)
    save(fig, "p_bands")


def fermi_dirac():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.7), gridspec_kw={"width_ratios": [1, 1.3]})
    ax = axs[0]
    E = np.linspace(-0.4, 0.4, 500); kT = 0.0259
    for T, c in ((0.0001, GRAY), (300, BLUE), (600, ORANGE)):
        kt = 8.617e-5 * max(T, 1)
        f = 1 / (1 + np.exp(np.clip(E / kt, -60, 60))); ax.plot(f, E, color=c, label=f"T = {int(T) if T>1 else 0} K")
    ax.axhline(0, color=GRAY, ls="--", lw=1); ax.text(0.98, 0.012, "$E_F$", ha="right", fontsize=10)
    ax.set_xlabel("probability f(E)"); ax.set_ylabel("$E-E_F$ (eV)"); ax.legend(loc="upper right"); ax.set_title("Fermi–Dirac function")
    ax = axs[1]
    ax.set_xlim(0, 3); ax.set_ylim(0, 10); ax.axis("off")
    def band(x0, title, ef, extra):
        ax.add_patch(Rectangle((x0, 7.5), 0.9, 1.6, fc="#cfe0ff", ec=INK)); ax.add_patch(Rectangle((x0, 0.9), 0.9, 1.6, fc="#ffe3b8", ec=INK))
        ax.text(x0 + .45, 9.4, title, ha="center", fontsize=9.5, weight="bold")
        ax.plot([x0, x0 + .9], [ef, ef], color=RED, lw=2); ax.text(x0 + .95, ef, "$E_F$", va="center", fontsize=10, color=RED)
        for y, s in extra:
            ax.plot([x0, x0 + .9], [y, y], color=GRAY, ls="--", lw=1); ax.text(x0 + .95, y, s, va="center", fontsize=9, color=GRAY)
        ax.text(x0 - 0.05, 8.3, "$E_c$", ha="right", fontsize=9); ax.text(x0 - 0.05, 1.7, "$E_v$", ha="right", fontsize=9)
    band(0.15, "N-type", 6.7, [(7.2, "$E_D$")]); band(1.15, "Intrinsic", 5.0, []); band(2.15, "P-type", 3.3, [(2.9, "$E_A$")])
    ax.text(1.5, 0.15, "Fermi level: N-type just below $E_c$, P-type just above $E_v$", ha="center", fontsize=9)
    save(fig, "p_fermi")


def diode_iv():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.6), gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axs[0]
    V = np.linspace(0, 1.0, 400)
    Ige = 1e-8 * (np.exp(V / 0.02585) - 1) * 1e3; Isi = 1e-13 * (np.exp(V / (1.2 * 0.02585)) - 1) * 1e3
    ax.plot(V, Ige, color=ORANGE, label="Ge  (knee ≈ 0.3 V)"); ax.plot(V, Isi, color=BLUE, label="Si  (knee ≈ 0.7 V)")
    ax.set_ylim(0, 30); ax.set_xlim(0, 1.0); ax.set_xlabel("forward voltage $V_F$ (V)"); ax.set_ylabel("forward current $I_F$ (mA)")
    ax.axvline(0.3, color=ORANGE, ls=":", lw=1); ax.axvline(0.7, color=BLUE, ls=":", lw=1); ax.legend(loc="upper left"); ax.set_title("Forward bias")
    ax = axs[1]
    ax.plot([0, 50], [2, 2], color=ORANGE, label="Ge  (a few µA)")
    ax.plot([0, 50], [0.05, 0.05], color=BLUE, label="Si  (nA: almost zero)")
    yb = np.linspace(2, 40, 100); ax.plot(50 + 0.5 * (1 - np.exp(-(yb - 2) / 12)), yb, color=RED, lw=2, label="breakdown")
    ax.set_xlim(0, 60); ax.set_ylim(-1, 42)
    ax.set_xlabel("reverse voltage $|V_R|$ (V)"); ax.set_ylabel("reverse current $|I_R|$ ($\\mu$A)")
    ax.set_title("Reverse bias (not to scale)"); ax.legend(loc="upper left")
    ax.annotate("$V_{BR}$", xy=(50.2, 22), xytext=(53, 22), color=RED, va="center", fontsize=11, arrowprops=dict(arrowstyle="->", color=RED))
    fig.tight_layout(); save(fig, "p_diode_iv")


def diode_temp():
    fig, ax = new(6.2, 3.6)
    V = np.linspace(0, 0.9, 400)
    for T, c, l in ((300, BLUE, "25 °C"), (350, ORANGE, "75 °C"), (400, RED, "125 °C")):
        vt = T / 11600
        # I0 doubles every 10 C -> scale
        I0 = 1e-13 * 2 ** ((T - 300) / 10)
        ax.plot(V, I0 * (np.exp(V / (1.2 * vt)) - 1) * 1e3, color=c, label=l)
    ax.set_ylim(0, 15); ax.set_xlim(0, 0.9); ax.set_xlabel("$V_F$ (V)"); ax.set_ylabel("$I_F$ (mA)")
    ax.annotate("curve shifts LEFT as T rises\n(cut-in voltage falls)", xy=(0.74, 6), xytext=(0.12, 9.5), arrowprops=dict(arrowstyle="->", color=INK), fontsize=9.5)
    ax.legend(loc="lower right"); ax.set_title("Forward characteristic vs temperature")
    save(fig, "p_diode_temp")


def diode_models():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.0), sharey=True)
    V = np.linspace(-0.2, 1.0, 400); real = 1e-13 * (np.exp(V / (1.2 * 0.02585)) - 1) * 1e3
    titles = ["1) Piecewise linear\n$V_\\gamma$ and $R_f$", "2) Constant drop\n$V_\\gamma$ only ($R_f=0$)", "3) Ideal diode\n(switch)"]
    for ax, t in zip(axs, titles):
        ax.plot(V, real, color=GRAY, lw=1.2, ls="--", label="real curve"); ax.set_xlim(-0.2, 1.0); ax.set_ylim(-1, 12); ax.set_title(t, fontsize=9.5)
        ax.axhline(0, color=INK, lw=.8); ax.axvline(0, color=INK, lw=.8); ax.set_xlabel("V (V)")
    axs[0].set_ylabel("I (mA)")
    x = np.array([0.7, 0.9]); axs[0].plot([-0.2, 0.7, 0.9], [0, 0, 4], color=BLUE); axs[0].annotate("slope = 1/$R_f$", xy=(0.82, 2.4), xytext=(0.2, 6), arrowprops=dict(arrowstyle="->"), fontsize=9)
    axs[0].text(0.7, -0.8, "$V_\\gamma$", ha="center", color=BLUE)
    axs[1].plot([-0.2, 0.7, 0.7], [0, 0, 12], color=BLUE); axs[1].text(0.7, -0.8, "$V_\\gamma$", ha="center", color=BLUE)
    axs[2].plot([-0.2, 0, 0], [0, 0, 12], color=BLUE)
    fig.tight_layout(); save(fig, "p_diode_models")


def diode_res():
    fig, ax = new(5.6, 3.6)
    V = np.linspace(0, 0.85, 400); I = 1e-13 * (np.exp(V / (1.2 * 0.02585)) - 1) * 1e3
    ax.plot(V, I, color=BLUE); ax.set_xlim(0, 0.85); ax.set_ylim(0, 14)
    Vq = 0.72; Iq = 1e-13 * (np.exp(Vq / (1.2 * 0.02585)) - 1) * 1e3
    ax.plot(Vq, Iq, "o", color=RED, ms=7); ax.plot([0, Vq], [0, Iq], color=ORANGE, ls="--"); ax.text(0.2, Iq * 0.35, "static (dc) resistance\n$R_{dc}=V/I$ : slope of\nline to origin", color=ORANGE, fontsize=9)
    sl = (1e-13 / (1.2 * 0.02585)) * np.exp(Vq / (1.2 * 0.02585)) * 1e3
    xs = np.array([Vq - 0.09, Vq + 0.07]); ax.plot(xs, Iq + sl * (xs - Vq), color=GREEN, lw=2)
    ax.text(0.47, 11.6, "dynamic (ac) resistance\n$r_d=\\Delta V/\\Delta I$ : slope of\ntangent at Q", color=GREEN, fontsize=9)
    ax.text(Vq + .015, Iq - 1.3, "Q", color=RED, fontsize=11)
    ax.set_xlabel("$V_D$ (V)"); ax.set_ylabel("$I_D$ (mA)")
    save(fig, "p_diode_res")


def zener_iv():
    fig, ax = new(6.4, 4.2)
    Vz = 5.6; rz = 0.07
    Vf = np.linspace(0, 0.85, 200); ax.plot(Vf, 4.5 * (np.exp(Vf / 0.09) - 1) / (np.exp(0.85 / 0.09) - 1) * 4, color=BLUE)
    Vr = np.linspace(0, -Vz, 100); ax.plot(Vr, -0.15 * (Vr / -Vz) ** 3, color=BLUE)
    Ir = np.linspace(0, 24, 100); ax.plot(-Vz - rz * Ir - 0.25 * (1 - np.exp(-Ir / 0.8)), -Ir, color=BLUE)
    ax.set_xlim(-9.5, 1.5); ax.set_ylim(-28, 7); axes_cross(ax, "V", "I")
    ax.plot([-9.3, -6.05], [-2.2, -2.2], color=GRAY, lw=.9, ls=":"); ax.text(-9.4, -1.6, "$I_{ZK}$ (knee)", fontsize=8.8, color=GRAY)
    ax.plot([-9.3, -7.4], [-22, -22], color=GRAY, lw=.9, ls=":"); ax.text(-9.4, -23.4, "$I_{ZM}$ (max)", fontsize=8.8, color=GRAY)
    ax.annotate("", xy=(-6.3, -3), xytext=(-6.3, -21), arrowprops=dict(arrowstyle="<->", color=GREEN)); ax.text(-8.9, -12, "regulating\nregion", ha="left", va="center", color=GREEN, fontsize=9.5)
    ax.plot(-Vz, 0, "o", color=RED, ms=5); ax.text(-Vz, 1.4, "$V_Z$", ha="center", fontsize=11, color=RED)
    ax.text(0.3, 4.3, "forward: like an\nordinary diode", fontsize=8.8, color=GRAY)
    ax.text(-9.4, -27, "slight tilt = zener resistance $r_Z$", fontsize=8.6, color=GRAY)
    save(fig, "p_zener_iv")


def tunnel_iv():
    fig, ax = new(6.6, 4.0)
    V = np.linspace(-0.15, 0.6, 700)
    tun = 6.0 * (V / 0.09) * np.exp(1 - V / 0.09) * (V > 0)
    thermal = 0.02 * (np.exp(np.clip(V, 0, None) / 0.07) - 1) * (V > 0)
    Ir = -1.0 * (np.abs(V) / 0.12) * (V < 0) * 6
    I = tun + thermal + Ir + 0.4 * (V > 0) * (V < 0.35) * (1 - np.exp(-V / 0.05)) * 0
    ax.plot(V, I, color=BLUE); ax.set_xlim(-0.18, 0.62); ax.set_ylim(-4.2, 9.5); axes_cross(ax, "$V_F$ (V)", "$I_F$ (mA)")
    vp = 0.09; ip = 6.0
    iv = I[(V > 0.2) & (V < 0.4)].min(); vv = V[(V > 0.2) & (V < 0.4)][np.argmin(I[(V > 0.2) & (V < 0.4)])]
    ax.plot([vp], [ip], "o", color=RED); ax.text(vp + .01, ip + .35, "A  peak $(V_P, I_P)$", color=RED, fontsize=9.5)
    ax.plot([vv], [iv], "o", color=GREEN); ax.text(vv + .015, iv - 0.7, "B  valley $(V_V, I_V)$", color=GREEN, fontsize=9.5)
    ax.annotate("", xy=(0.19, 3.4), xytext=(0.13, 5.0), arrowprops=dict(arrowstyle="->", color=PURPLE, lw=0))
    ax.fill_between([vp, vv], [-4.2, -4.2], [9.5, 9.5], color="#ffe9b8", alpha=.45)
    ax.text((vp + vv) / 2, 8.5, "negative-\nresistance\nregion", ha="center", fontsize=9, color=ORANGE)
    ax.text(0.5, 3.2, "C  normal diode\nregion", fontsize=9, color=GRAY, ha="center")
    ax.text(-0.10, -3.4, "reverse: current grows\n(back diode)", fontsize=8.5, color=GRAY, ha="center")
    save(fig, "p_tunnel_iv")


def varactor_cv():
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.4))
    ax = axs[0]
    V = np.linspace(0.05, 20, 300); C = 161.2 / np.sqrt(0.6 + V)
    ax.plot(V, C, color=BLUE); ax.set_xlabel("reverse voltage $V_R$ (V)"); ax.set_ylabel("junction capacitance $C_T$ (pF)"); ax.set_title("$C_T$ falls as reverse bias rises")
    ax.set_ylim(0, 200)
    ax = axs[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    for x0, wd, tt, w2 in ((0.4, 1.4, "small $V_R$", 1.0), (5.6, 4.0, "large $V_R$", 3.0)):
        pass
    ax.add_patch(Rectangle((0.3, 3.6), 1.7, 1.6, fc="#ffe3b8", ec=INK)); ax.add_patch(Rectangle((2.0, 3.6), 0.9, 1.6, fc="#eeeeee", ec=INK, hatch="//")); ax.add_patch(Rectangle((2.9, 3.6), 1.7, 1.6, fc="#cfe0ff", ec=INK))
    ax.text(1.15, 4.4, "P", ha="center", fontsize=12); ax.text(3.75, 4.4, "N", ha="center", fontsize=12); ax.text(2.45, 5.5, "narrow\ndepletion", ha="center", fontsize=8.5)
    ax.text(2.45, 3.2, "small $V_R$ → thin gap → BIG C", ha="center", fontsize=9, color=GREEN)
    ax.add_patch(Rectangle((5.4, 0.9), 1.0, 1.6, fc="#ffe3b8", ec=INK)); ax.add_patch(Rectangle((6.4, 0.9), 2.2, 1.6, fc="#eeeeee", ec=INK, hatch="//")); ax.add_patch(Rectangle((8.6, 0.9), 1.0, 1.6, fc="#cfe0ff", ec=INK))
    ax.text(5.9, 1.7, "P", ha="center", fontsize=12); ax.text(9.1, 1.7, "N", ha="center", fontsize=12); ax.text(7.5, 2.8, "wide depletion", ha="center", fontsize=8.5)
    ax.text(7.5, 0.35, "large $V_R$ → thick gap → small C", ha="center", fontsize=9, color=RED)
    fig.tight_layout(); save(fig, "p_varactor")


def led_colors():
    fig, ax = new(9, 2.4)
    lam = np.linspace(380, 800, 800)
    def rgb(l):
        if l < 440: r, g, b = -(l - 440) / 60, 0, 1
        elif l < 490: r, g, b = 0, (l - 440) / 50, 1
        elif l < 510: r, g, b = 0, 1, -(l - 510) / 20
        elif l < 580: r, g, b = (l - 510) / 70, 1, 0
        elif l < 645: r, g, b = 1, -(l - 645) / 65, 0
        else: r, g, b = 1, 0, 0
        f = 0.3 + 0.7 * min(1, (800 - l) / 60 if l > 700 else (l - 380) / 40 if l < 420 else 1)
        return (r * f, g * f, b * f)
    for l in lam: ax.axvspan(l, l + 0.6, color=rgb(l), lw=0)
    ax.set_xlim(380, 900); ax.set_ylim(0, 1); ax.set_yticks([])
    ax.axvspan(800, 900, color="#3a2020", alpha=.9); ax.text(850, 0.5, "infrared\n(invisible)", color="white", ha="center", va="center", fontsize=9)
    ax.set_xlabel("wavelength (nm)")
    for x, t in ((425, "violet\n400–450"), (535, "green\n500–570"), (685, "red\n610–760")):
        ax.text(x, 0.5, t, ha="center", va="center", fontsize=8.5, color="white" if x != 535 else INK, weight="bold")
    ax.spines["left"].set_visible(False)
    save(fig, "p_led_colors")


def photodiode_iv():
    fig, ax = new(6.4, 4.0)
    V = np.linspace(-6, 0.65, 400)
    for P, c in ((0, GRAY), (1, TEAL), (2, BLUE), (3, PURPLE)):
        I = 0.02 * (np.exp(V / 0.06) - 1) - P * 1.2
        ax.plot(V, I, color=c, label=f"light level {P}" if P else "dark")
    ax.set_xlim(-6, 1.0); ax.set_ylim(-5.4, 2.2); axes_cross(ax, "V", "I")
    ax.text(-3.0, -4.95, "reverse-biased\n(photoconductive mode)", fontsize=9, color=INK, ha="center")
    ax.text(0.5, -4.2, "no bias\n(solar-cell\nmode)", fontsize=9, color=INK, ha="center")
    ax.legend(loc="upper left", fontsize=8.5, bbox_to_anchor=(0.0, 1.0)); save(fig, "p_photodiode_iv")


def cond_temp():
    fig, ax = new(5.6, 3.4)
    T = np.linspace(250, 500, 200); k = 8.617e-5
    ni2 = T ** 3 * np.exp(-1.12 / (k * T)); ax.semilogy(T, ni2 / ni2[0] * 1, color=BLUE, label="intrinsic $n_i^2$")
    nn = np.ones_like(T) * 1e6; ax.semilogy(T, nn, color=ORANGE, label="N-type free-electron conc.\n(≈ $N_D$: almost flat)")
    ax.set_xlabel("temperature T (K)"); ax.set_ylabel("carrier concentration (relative)"); ax.legend(loc="upper left", fontsize=8.5)
    ax.set_title("Intrinsic concentration explodes with T")
    save(fig, "p_ni_temp")


def drift_diff():
    fig, axs = plt.subplots(1, 2, figsize=(9.3, 3.2))
    ax = axs[0]; ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off"); ax.set_title("Drift: electric field pushes", fontsize=10.5)
    ax.add_patch(Rectangle((1, 1.2), 7.5, 2.2, fc="#f3f6ff", ec=INK))
    rng = np.random.default_rng(3)
    xs = rng.uniform(1.3, 8.2, 14); ys = rng.uniform(1.5, 3.1, 14); ax.plot(xs, ys, "o", color=BLUE, ms=6)
    for x, y in zip(xs[:9], ys[:9]): ax.annotate("", xy=(x - 0.5, y), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1))
    ax.annotate("", xy=(8.3, 4.2), xytext=(1.5, 4.2), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2)); ax.text(5, 4.5, "electric field $E$  →   electrons drift ←", ha="center", fontsize=9.5, color=RED)
    ax.text(5, 0.5, "$v_d=\\mu E$,   $J = nq\\mu E=\\sigma E$", ha="center", fontsize=10)
    ax = axs[1]
    x = np.linspace(0, 4, 200); ax.plot(x, np.exp(-x / 1.2), color=GREEN); ax.fill_between(x, np.exp(-x / 1.2), color="#dff5ea")
    ax.set_xlabel("distance x"); ax.set_ylabel("carrier concentration"); ax.set_title("Diffusion: crowd spreads out", fontsize=10.5)
    ax.annotate("", xy=(1.9, 0.5), xytext=(0.7, 0.5), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2)); ax.text(1.3, 0.56, "carriers move\nfrom crowded to empty", ha="center", fontsize=8.8, color=RED)
    ax.text(2.9, 0.75, "$J_p=-qD_p\\,\\dfrac{dp}{dx}$", fontsize=10)
    fig.tight_layout(); save(fig, "p_drift_diff")


def run_all():
    bands(); fermi_dirac(); diode_iv(); diode_temp(); diode_models(); diode_res(); zener_iv(); tunnel_iv(); varactor_cv()
    led_colors(); photodiode_iv(); cond_temp(); drift_diff()


if __name__ == "__main__":
    run_all(); print("ok")
