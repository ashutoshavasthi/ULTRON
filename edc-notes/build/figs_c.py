"""Figures C: rectifiers, filters, BJT."""
from figs_common import *
from matplotlib.patches import Rectangle


def rect_waves():
    fig, axs = plt.subplots(3, 1, figsize=(7.6, 6.2), sharex=True)
    t = np.linspace(0, 4 * np.pi, 1600); v = np.sin(t)
    ax = axs[0]; ax.plot(t, v, color=GRAY); ax.set_ylabel("input $V_i$"); ax.axhline(0, color=INK, lw=.8); ax.set_title("AC input", fontsize=10)
    ax = axs[1]; o = np.where(v > 0, v, 0); ax.plot(t, o, color=BLUE); ax.fill_between(t, o, color="#cfe0ff"); ax.axhline(0, color=INK, lw=.8)
    ax.axhline(1 / np.pi, color=RED, ls="--", lw=1.2); ax.text(4 * np.pi, 1 / np.pi + .06, "$V_{dc}=V_m/\\pi$", ha="right", color=RED, fontsize=9.5); ax.set_ylabel("HWR output"); ax.set_title("Half-wave: only the positive half-cycles", fontsize=10)
    ax = axs[2]; o = np.abs(v); ax.plot(t, o, color=GREEN); ax.fill_between(t, o, color="#dff5ea"); ax.axhline(0, color=INK, lw=.8)
    ax.axhline(2 / np.pi, color=RED, ls="--", lw=1.2); ax.text(4 * np.pi, 2 / np.pi + .06, "$V_{dc}=2V_m/\\pi$", ha="right", color=RED, fontsize=9.5); ax.set_ylabel("FWR output"); ax.set_title("Full-wave: both half-cycles, flipped positive (ripple frequency = 2 × input)", fontsize=10)
    ax.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi]); ax.set_xticklabels(["0", "π", "2π", "3π", "4π"]); ax.set_xlabel("ωt")
    fig.tight_layout(); save(fig, "p_rect_waves")


def filter_waves():
    fig, axs = plt.subplots(2, 2, figsize=(9.4, 5.6), sharex=True)
    t = np.linspace(0, 4 * np.pi, 3000); r = np.abs(np.sin(t))
    # C filter
    def cfilt(RC):
        out = np.zeros_like(t); vc = 0.0; dt = t[1] - t[0]
        for i in range(len(t)):
            if r[i] > vc: vc = r[i]
            else: vc -= vc * dt / RC
            out[i] = vc
        return out
    ax = axs[0, 0]; ax.plot(t, r, color=GRAY, ls="--", lw=1); ax.plot(t, cfilt(6), color=BLUE); ax.set_title("Capacitor filter: charge fast, discharge slowly", fontsize=9.5); ax.set_ylabel("volts (peak = 1)")
    ax = axs[0, 1]; ax.plot(t, r, color=GRAY, ls="--", lw=1); ax.plot(t, cfilt(20), color=GREEN); ax.set_title("Bigger C (or bigger $R_L$): smaller ripple", fontsize=9.5)
    # L filter: current elongated, smoothed
    ax = axs[1, 0]; ax.plot(t, r, color=GRAY, ls="--", lw=1)
    avg = 2 / np.pi; sm = avg + (r - avg) * 0.35; ax.plot(t, sm, color=ORANGE); ax.axhline(avg, color=RED, ls=":", lw=1); ax.set_title("L filter: inductor opposes CHANGE in current", fontsize=9.5); ax.set_ylabel("volts / current")
    ax = axs[1, 1]; ax.plot(t, r, color=GRAY, ls="--", lw=1); c1 = cfilt(20); sm2 = np.mean(c1) + (c1 - np.mean(c1)) * 0.12; ax.plot(t, sm2, color=PURPLE); ax.set_title("π filter (C–L–C): almost flat DC", fontsize=9.5)
    for a in axs[1]: a.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi]); a.set_xticklabels(["0", "π", "2π", "3π", "4π"]); a.set_xlabel("ωt")
    for a in axs.ravel(): a.set_ylim(0, 1.15)
    fig.tight_layout(); save(fig, "p_filter_waves")


def bjt_struct():
    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.0))
    for ax, (kind, cols, lab) in zip(axs, (("NPN", ("#cfe0ff", "#ffe3b8", "#cfe0ff"), ("N", "P", "N")), ("PNP", ("#ffe3b8", "#cfe0ff", "#ffe3b8"), ("P", "N", "P")))):
        ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis("off"); ax.set_title(f"{kind} transistor", fontsize=11, weight="bold")
        xs = [0.6, 3.2, 4.2]; ws = [2.6, 1.0, 2.6]
        for x, w, c, l in zip(xs, ws, cols, lab): ax.add_patch(Rectangle((x, 1.2), w, 1.8, fc=c, ec=INK, lw=1.3)); ax.text(x + w / 2, 2.1, l, ha="center", va="center", fontsize=14, weight="bold")
        ax.text(1.9, 3.35, "Emitter\n(heavily doped)", ha="center", fontsize=8.5); ax.text(3.7, 3.35, "Base\n(thin, light)", ha="center", fontsize=8.5); ax.text(5.5, 3.35, "Collector\n(medium, big)", ha="center", fontsize=8.5)
        for x, t in ((1.9, "E"), (3.7, "B"), (5.5, "C")): ax.plot([x, x], [1.2, 0.5], color=INK, lw=2); ax.text(x, 0.25, t, ha="center", fontsize=11)
        ax.text(3.5, 1.05, "", fontsize=1)
        ax.text(7.3, 2.6, "$J_E$ (E–B junction)\n$J_C$ (C–B junction)", fontsize=9.5, va="center")
    fig.tight_layout(); save(fig, "p_bjt_struct")


def bjt_char():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.9))
    ax = axs[0]
    vbe = np.linspace(0, 0.85, 300)
    for vce, c in ((0.2, GRAY), (5, BLUE)):
        ib = 1e-14 * np.exp(vbe / 0.026) * 1e6 * (1 + (0.02 if vce > 1 else 0)); ax.plot(vbe, ib, color=c, label=f"$V_{{CE}}$ = {vce} V")
    ax.set_xlim(0, 0.85); ax.set_ylim(0, 60); ax.set_xlabel("$V_{BE}$ (V)"); ax.set_ylabel("$I_B$ (µA)"); ax.set_title("Input characteristic: just a diode", fontsize=10.5); ax.legend(loc="upper left"); ax.axvline(0.7, color=GRAY, ls=":", lw=1)
    ax = axs[1]
    vce = np.linspace(0, 12, 400)
    for k, ib in enumerate((10, 20, 30, 40, 50)):
        beta = 100; ic = beta * ib * 1e-3 * (1 - np.exp(-vce / 0.25)) * (1 + vce / 120); ax.plot(vce, ic, color=BLUE); ax.text(12.1, ic[-1], f"$I_B$={ib} µA", fontsize=8.5, va="center", color=BLUE)
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.5); ax.set_xlabel("$V_{CE}$ (V)"); ax.set_ylabel("$I_C$ (mA)"); ax.set_title("Output characteristic", fontsize=10.5)
    ax.axvspan(0, 0.4, color="#ffe9c9", alpha=.9); ax.text(0.2, 6.0, "saturation", rotation=90, ha="center", va="top", fontsize=8.8)
    ax.axhspan(0, 0.15, color="#e8e8e8"); ax.text(9, 0.28, "cut-off  ($I_B=0$)", fontsize=8.8, color=GRAY); ax.text(6, 5.6, "active (linear) region", ha="center", fontsize=9.5, color=GREEN)
    fig.subplots_adjust(right=0.86, wspace=0.28); save(fig, "p_bjt_char")


def loadline():
    fig, ax = new(6.6, 4.4)
    VCC, RC = 12, 2.2
    vce = np.linspace(0, 12.5, 400)
    for ib in (10, 20, 30, 40, 50, 60):
        ic = 100 * ib * 1e-3 * (1 - np.exp(-vce / 0.2)); ax.plot(vce, ic, color="#9db7e6", lw=1.4); ax.text(12.6, ic[-1], f"$I_{{B}}$={ib}µA", fontsize=8, va="center", color=GRAY)
    ax.plot([0, VCC], [VCC / RC, 0], color=RED, lw=2.2)
    ax.plot([6.82], [2.35], "o", color=GREEN, ms=8); ax.text(7.1, 2.55, "Q-point\n$(V_{CEQ},I_{CQ})$", color=GREEN, fontsize=9.5)
    ax.plot([0, 6.82], [2.35, 2.35], color=GREEN, ls=":", lw=1); ax.plot([6.82, 6.82], [0, 2.35], color=GREEN, ls=":", lw=1)
    ax.text(-0.15, 5.45, "$V_{CC}/R_C$\n(saturation end)", ha="right", va="center", fontsize=9, color=RED); ax.text(12, -0.45, "$V_{CC}$ (cut-off end)", ha="right", fontsize=9, color=RED)
    ax.text(3.3, 4.1, "DC load line:\n$V_{CE}=V_{CC}-I_CR_C$", color=RED, fontsize=9.5, rotation=-25)
    ax.set_xlim(0, 15.5); ax.set_ylim(0, 6.2); ax.set_xlabel("$V_{CE}$ (V)"); ax.set_ylabel("$I_C$ (mA)")
    fig.subplots_adjust(left=.12); save(fig, "p_loadline")


def loadline_effects():
    fig, axs = plt.subplots(1, 3, figsize=(10.4, 3.4), sharey=True)
    vce = np.linspace(0, 13, 300)
    def fam(ax):
        for ib in (10, 20, 30, 40, 50): ax.plot(vce, 100 * ib * 1e-3 * (1 - np.exp(-vce / 0.2)), color="#c5d4f0", lw=1.2)
        ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.set_xlabel("$V_{CE}$")
    ax = axs[0]; fam(ax); ax.plot([0, 12], [6, 0], color=RED); ax.set_title("$I_B$ increases → Q moves up the line", fontsize=9.5)
    for ib, col in ((20, GRAY), (30, ORANGE), (40, GREEN)): ic = 100 * ib * 1e-3; v = 12 - 2 * ic; ax.plot(v, ic, "o", color=col)
    ax.set_ylabel("$I_C$")
    ax = axs[1]; fam(ax); ax.plot([0, 12], [6, 0], color=RED, label="small $R_C$"); ax.plot([0, 12], [3, 0], color=ORANGE, label="larger $R_C$"); ax.plot([0, 12], [2, 0], color=PURPLE, label="even larger $R_C$"); ax.legend(loc="upper right", fontsize=8.5); ax.set_title("$R_C$ changes the SLOPE", fontsize=9.5)
    ax = axs[2]; fam(ax); ax.plot([0, 12], [6, 0], color=RED, label="$V_{CC}$ = 12"); ax.plot([0, 9], [4.5, 0], color=ORANGE, label="$V_{CC}$ = 9"); ax.plot([0, 6], [3, 0], color=PURPLE, label="$V_{CC}$ = 6"); ax.legend(loc="upper right", fontsize=8.5); ax.set_title("lower $V_{CC}$: line shifts, same slope", fontsize=9.5)
    fig.tight_layout(); save(fig, "p_loadline_effects")


def ac_phase():
    fig, ax = new(6.8, 3.2)
    t = np.linspace(0, 2, 500)
    ax.plot(t, 0.6 * np.sin(2 * np.pi * 2 * t), color=BLUE, label="input $v_i$ (small)"); ax.plot(t, -3.0 * np.sin(2 * np.pi * 2 * t) + 4, color=RED, label="output $v_o$ (big, INVERTED, riding on $V_{CEQ}$)")
    ax.axhline(4, color=GRAY, ls=":", lw=1); ax.text(2.02, 4, "$V_{CEQ}$", fontsize=9, va="center"); ax.axhline(0, color=INK, lw=.8)
    ax.set_xlabel("time"); ax.set_yticks([]); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=8.5, ncol=1); ax.set_title("Common-emitter amplifier: 180° phase shift", fontsize=10.5)
    save(fig, "p_ac_phase")


def freq_resp():
    fig, ax = new(6.4, 3.4)
    f = np.logspace(0, 8, 500); fl, fh = 30, 3e5
    A = 1 / np.sqrt(1 + (fl / f) ** 2) / np.sqrt(1 + (f / fh) ** 2)
    ax.semilogx(f, 20 * np.log10(A * 100), color=BLUE); ax.set_ylim(20, 44); ax.set_xlabel("frequency (Hz)"); ax.set_ylabel("voltage gain (dB)")
    ax.text(2e3, 41.5, "mid-band (flat)\ngain = $-R_C/r_e$ etc.", ha="center", fontsize=9, color=GREEN)
    ax.annotate("low-frequency roll-off\n(coupling & bypass\ncapacitors)", xy=(6, 24), xytext=(2, 33), fontsize=8.5, arrowprops=dict(arrowstyle="->"))
    ax.annotate("high-frequency roll-off\n(internal transistor\ncapacitances)", xy=(2e6, 25), xytext=(2e5, 34), fontsize=8.5, arrowprops=dict(arrowstyle="->"))
    save(fig, "p_freq_resp")


def early():
    fig, ax = new(6.4, 3.8)
    vce = np.linspace(-90, 14, 300); VA = 90
    for ib, ic0 in ((1, 1.0), (2, 2.0), (3, 3.0), (4, 4.0)):
        ax.plot(vce, ic0 * (1 + vce / VA), color=BLUE, lw=1.2, ls="--" if True else "-")
        v2 = np.linspace(0.5, 14, 100); ax.plot(v2, ic0 * (1 + v2 / VA), color=BLUE, lw=2)
    ax.axhline(0, color=INK, lw=.8); ax.axvline(0, color=INK, lw=.8)
    ax.set_xlim(-100, 15); ax.set_ylim(-0.5, 6); ax.set_xlabel("$V_{CE}$ (V)"); ax.set_ylabel("$I_C$ (mA)")
    ax.plot([-VA], [0], "o", color=RED); ax.text(-VA, -0.35, "$-V_A$  (Early voltage)", color=RED, ha="center", fontsize=9.5)
    ax.text(-45, 4.6, "all extended lines meet at $-V_A$\nslope of each line $=1/r_o$,   $r_o\\approx V_A/I_{CQ}$", fontsize=9.3, color=INK)
    save(fig, "p_early")


def run_all():
    rect_waves(); filter_waves(); bjt_struct(); bjt_char(); loadline(); loadline_effects(); ac_phase(); freq_resp(); early()


if __name__ == "__main__":
    run_all(); print("ok")
