"""Figures B: thyristors, UJT, PN junction."""
from figs_common import *
from matplotlib.patches import Rectangle, Polygon, Circle


def layers(ax, x0, y0, w, h, labels, colors, fs=10):
    y = y0 + h * len(labels)
    for lab, col in zip(labels, colors):
        y -= h
        ax.add_patch(Rectangle((x0, y), w, h, fc=col, ec=INK, lw=1.3)); ax.text(x0 + w / 2, y + h / 2, lab, ha="center", va="center", fontsize=fs, weight="bold")


def scr_struct():
    fig, ax = plt.subplots(figsize=(7.4, 3.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    P = "#ffe3b8"; N = "#cfe0ff"
    layers(ax, 1.4, 0.9, 2.6, 1.0, ["P$_1$", "N$_1$", "P$_2$", "N$_2$"], [P, N, P, N], 12)
    ax.plot([2.7, 2.7], [4.9, 5.5], color=INK, lw=2); ax.text(2.7, 5.7, "Anode (A)", ha="center", fontsize=10)
    ax.plot([2.7, 2.7], [0.9, 0.3], color=INK, lw=2); ax.text(2.7, 0.05, "Cathode (K)", ha="center", fontsize=10)
    ax.plot([1.4, 0.5], [2.4, 2.4], color=INK, lw=2); ax.text(0.5, 2.7, "Gate (G)", ha="left", fontsize=10)
    for y, t in ((3.9, "$J_1$"), (2.9, "$J_2$"), (1.9, "$J_3$")):
        ax.text(4.15, y, t, fontsize=10, color=RED, va="center"); ax.plot([4.0, 4.1], [y, y], color=RED)
    ax.text(5.0, 4.6, "Four layers P-N-P-N,\nthree junctions $J_1,J_2,J_3$", fontsize=10, va="top")
    ax.text(5.0, 3.2, "Gate is attached to the\nP layer next to the cathode ($P_2$)", fontsize=10, va="top", color=GREEN)
    ax.text(5.0, 1.7, "Made of silicon (small leakage,\nhigh temperature capability)", fontsize=10, va="top", color=GRAY)
    save(fig, "p_scr_struct")


def scr_iv():
    fig, ax = new(7.0, 4.3)
    x = np.linspace(0, 1, 100)
    ax.plot([-6.0, 0, 6.0], [-0.15, 0, 0.35], color=BLUE)  # forward blocking
    ax.plot([6.0, 5.2], [0.35, 0.6], color=BLUE, ls="--"); ax.annotate("", xy=(4.2, 4.2), xytext=(6.0, 0.4), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6, ls="--"))
    ax.plot([4.2, 4.6, 5.6], [4.2, 5.0, 8.2], color=BLUE)  # on-state
    ax.plot([-6, -7.0, -7.4], [-0.15, -0.6, -6.5], color=BLUE)  # reverse breakdown
    ax.set_xlim(-8, 8); ax.set_ylim(-4, 9); axes_cross(ax, "$V_{AK}$", "$I_A$")
    ax.text(3.2, 0.9, "forward blocking\n(OFF)", fontsize=9, color=INK); ax.text(4.9, 6.2, "forward conducting\n(ON)", fontsize=9, color=GREEN)
    ax.text(-7.6, 1.0, "reverse blocking", fontsize=9, color=INK); ax.text(6.05, -0.9, "$V_{BO}$", color=RED, fontsize=10, ha="center")
    ax.plot([6.0], [0.35], "o", color=RED, ms=4); ax.plot([4.2], [0.02], "o", color=GRAY, ms=1)
    ax.plot([4.1, 4.9], [1.3, 1.3], color=ORANGE, lw=0)
    ax.text(0.5, 8.2, "$I_H$ = holding current:\nbelow it the SCR turns OFF", fontsize=8.8, color=PURPLE)
    ax.plot([-0.3, 4.2], [3.0, 3.0], color=PURPLE, ls=":", lw=1.2); ax.text(-0.5, 3.0, "$I_H$", color=PURPLE, ha="right", va="center", fontsize=10)
    ax.text(-7.9, -3.5, "reverse breakdown (avoid!)", fontsize=8.6, color=GRAY)
    save(fig, "p_scr_iv")


def scr_family():
    fig, ax = new(6.2, 3.8)
    for ig, vbo, c in ((0, 8.5, GRAY), (1, 6.0, TEAL), (2, 3.6, BLUE), (3, 1.4, PURPLE)):
        ax.plot([0, vbo], [0, 0.4], color=c); ax.plot([vbo, vbo * 0.55 + .6, 0.6 + vbo * 0.6 + 0.4], [0.4, 3, 9], color=c, lw=1.6)
        ax.text(vbo + 0.1, 0.9, f"$I_G$={ig}" if ig else "$I_G$=0", fontsize=8.8, color=c)
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 9.5); ax.set_xlabel("$V_{AK}$"); ax.set_ylabel("$I_A$"); ax.set_title("More gate current → SCR turns on at a LOWER forward voltage")
    save(fig, "p_scr_family")


def scr_two_tr():
    from ckt import Ckt
    c = Ckt(10.5, 8.0, pad=1.3)
    t1 = c.bjt(3.6, 5.6, "pnp", flip=True, mirror=True)      # emitter top-left, collector bottom-left, base right
    t2 = c.bjt(3.6, 2.2, "npn")                               # base left, collector top-right, emitter bottom-right
    c.wire(t1["E"], (t1["E"][0], 7.6)); c.term(t1["E"][0], 7.6, "Anode (A)", "up")
    c.wire(t2["E"], (t2["E"][0], 0.3)); c.term(t2["E"][0], 0.3, "Cathode (K)", "down")
    c.wire(t1["C"], (t1["C"][0], 4.3), (1.9, 4.3), (1.9, 2.2), t2["B"])       # Tr1 collector -> Tr2 base
    c.wire(t2["C"], (t2["C"][0], 3.3), (5.7, 3.3), (5.7, 5.6), t1["B"])       # Tr2 collector -> Tr1 base
    c.dot(1.9, 2.2); c.wire((1.9, 2.2), (0.7, 2.2)); c.term(0.7, 2.2, "Gate (G)", "left")
    c.text(7.0, 5.6, "$Tr_1$ : PNP\n(layers $P_1N_1P_2$)", ha="left", size=10, color=BLUE)
    c.text(5.0, 1.0, "$Tr_2$ : NPN\n(layers $N_1P_2N_2$)", ha="left", size=10, color=GREEN)
    c.text(7.4, 3.3, "each collector feeds the\nother's base → a positive-\nfeedback (regenerative) loop", ha="left", size=9.5, color=RED)
    c.save("p_scr_two_tr")


def triac_struct():
    fig, ax = plt.subplots(figsize=(7.4, 3.8)); ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
    P = "#ffe3b8"; N = "#cfe0ff"
    ax.add_patch(Rectangle((1, 4.4), 3.6, 1.0, fc=P, ec=INK)); ax.text(2.8, 4.9, "P$_1$", ha="center", va="center", weight="bold", fontsize=11)
    ax.add_patch(Rectangle((1, 3.4), 3.6, 1.0, fc=N, ec=INK)); ax.text(2.8, 3.9, "N$_1$", ha="center", va="center", weight="bold", fontsize=11)
    ax.add_patch(Rectangle((1, 2.4), 3.6, 1.0, fc=P, ec=INK)); ax.text(2.8, 2.9, "P$_2$", ha="center", va="center", weight="bold", fontsize=11)
    ax.add_patch(Rectangle((1, 5.4), 1.4, 0.6, fc=N, ec=INK)); ax.text(1.7, 5.7, "N$_4$", ha="center", va="center", fontsize=10, weight="bold")
    ax.add_patch(Rectangle((1, 1.8), 1.3, 0.6, fc=N, ec=INK)); ax.text(1.65, 2.1, "N$_3$", ha="center", va="center", fontsize=10, weight="bold")
    ax.add_patch(Rectangle((3.3, 1.8), 1.3, 0.6, fc=N, ec=INK)); ax.text(3.95, 2.1, "N$_2$", ha="center", va="center", fontsize=10, weight="bold")
    ax.plot([2.8, 2.8], [6.0, 6.0]); ax.text(2.8, 6.15, "$MT_2$", ha="center", fontsize=10.5)
    ax.plot([1.7, 1.7], [1.8, 1.2], color=INK, lw=2); ax.text(1.7, 0.85, "Gate", ha="center", fontsize=10.5)
    ax.plot([3.95, 3.95], [1.8, 1.2], color=INK, lw=2); ax.text(3.95, 0.85, "$MT_1$", ha="center", fontsize=10.5)
    ax.plot([1.3, 1.3], [1.8, 1.8], color=INK)
    ax.text(5.4, 5.3, "Five layers, three terminals.", fontsize=10.5, va="center"); ax.text(5.4, 4.3, "≡ two SCRs in inverse-parallel\n   (anode of each = cathode of the other,\n    one shared gate)", fontsize=10, va="center", color=BLUE)
    ax.text(5.4, 2.5, "$P_1N_1P_2N_2$ : conducts when $MT_2$ is +\n$P_2N_1P_1N_4$ : conducts when $MT_2$ is −", fontsize=10, va="center", color=GREEN)
    save(fig, "p_triac_struct")


def triac_iv():
    fig, ax = new(6.6, 4.4)
    ax.plot([-6, 0, 6], [0.3, 0, -0.3], color=BLUE)
    ax.plot([6, 6.0, 4.8, 4.4], [0.35, 0.35, 3.3, 8.0], color=BLUE, lw=0); ax.plot([4.2, 5.2, 5.8], [3.0, 5.5, 8.3], color=BLUE)
    ax.annotate("", xy=(4.25, 3.0), xytext=(6.0, 0.4), arrowprops=dict(arrowstyle="-|>", color=RED, ls="--", lw=1.4))
    ax.plot([0, 6.0], [0, 0.4], color=BLUE)
    ax.plot([0, -6.0], [0, -0.4], color=BLUE); ax.annotate("", xy=(-4.25, -3.0), xytext=(-6.0, -0.4), arrowprops=dict(arrowstyle="-|>", color=RED, ls="--", lw=1.4))
    ax.plot([-4.2, -5.2, -5.8], [-3.0, -5.5, -8.3], color=BLUE)
    ax.set_xlim(-8.5, 8.5); ax.set_ylim(-9.5, 9.5); axes_cross(ax, "$V_{MT2-MT1}$", "$I$")
    ax.text(5.4, -1.2, "$V_{DRM}$", color=RED, ha="center", fontsize=10); ax.text(-5.4, 1.2, "$V_{RRM}$", color=RED, ha="center", fontsize=10)
    ax.text(2.4, 6.7, "on-state\n($V_{TM}$)", fontsize=9, color=GREEN, ha="center"); ax.text(-2.4, -6.7, "on-state", fontsize=9, color=GREEN, ha="center")
    ax.text(1.4, 1.25, "off-state ($I_{DRM}$)", fontsize=8.6, color=GRAY); ax.text(-1.5, -1.6, "off-state ($I_{RRM}$)", fontsize=8.6, color=GRAY, ha="right")
    ax.text(4.2, 8.6, "$I_H$", color=PURPLE, fontsize=10)
    ax.text(1.0, -8.6, "same shape in quadrant I and quadrant III", fontsize=9.5, color=INK)
    save(fig, "p_triac_iv")


def diac_iv():
    fig, ax = new(6.4, 4.2)
    v = np.linspace(-1, 1, 400)
    I = np.where(np.abs(v) < 0.55, 0.1 * v / 0.55, 0)
    xs = np.array([0, 0.25, 0.5, 0.58, 0.55, 0.42, 0.34, 0.4, 0.7, 1.0])
    ys = np.array([0, 0.08, 0.15, 0.18, 0.4, 1.0, 1.7, 2.3, 4.0, 6.0])
    xs2 = np.concatenate([xs[::-1] * -1, xs]); ys2 = np.concatenate([ys[::-1] * -1, ys])
    ax.plot(xs2 * 30, ys2, color=BLUE)
    ax.set_xlim(-38, 38); ax.set_ylim(-7.5, 7.5); axes_cross(ax, "V (volts)", "I")
    ax.text(17.5, -2.4, "$V_{BO1}\\approx 30$ V", color=RED, ha="center", fontsize=10); ax.text(-17, 1.1, "$V_{BO2}$", color=RED, ha="center", fontsize=10)
    ax.text(3, 0.9, "blocking\n(small leakage)", fontsize=9, color=GRAY); ax.text(20, 4.2, "conducting", fontsize=9.5, color=GREEN); ax.text(-30, -4.2, "conducting\n(−ve half-cycle)", fontsize=9.5, color=GREEN)
    ax.plot([17.4, 17.4], [0, 0], "o", color=RED)
    save(fig, "p_diac_iv")


def phase_control():
    fig, axs = plt.subplots(2, 1, figsize=(7.6, 4.8), sharex=True)
    t = np.linspace(0, 4 * np.pi, 1500); v = np.sin(t); a = np.pi / 3
    ax = axs[0]; ax.plot(t, v, color=GRAY, lw=1.2, ls="--"); on = ((t % (2 * np.pi)) > a) & ((t % (2 * np.pi)) < np.pi)
    ax.plot(t, np.where(on, v, np.nan), color=BLUE, lw=2.2); ax.fill_between(t, np.where(on, v, 0), color="#cfe0ff", alpha=.6)
    ax.set_title("SCR (half-wave control): gate fires at angle α = 60°", fontsize=10); ax.set_ylabel("load voltage"); ax.axhline(0, color=INK, lw=.8)
    ax.annotate("α", xy=(a, 0), xytext=(a / 2 - .05, -0.35), color=RED, fontsize=11)
    ax = axs[1]; ax.plot(t, v, color=GRAY, lw=1.2, ls="--")
    on2 = ((t % np.pi) > a)
    ax.plot(t, np.where(on2, v, np.nan), color=GREEN, lw=2.2); ax.fill_between(t, np.where(on2, v, 0), color="#dff5ea", alpha=.7)
    ax.set_title("TRIAC (full-wave control): fires at α in BOTH half-cycles", fontsize=10); ax.set_ylabel("load voltage"); ax.axhline(0, color=INK, lw=.8); ax.set_xlabel("ωt")
    ax.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi]); ax.set_xticklabels(["0", "π", "2π", "3π", "4π"])
    fig.tight_layout(); save(fig, "p_phase")


def ujt_struct():
    fig, ax = plt.subplots(figsize=(7.6, 3.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(Rectangle((2.5, 1.2), 2.2, 3.6, fc="#cfe0ff", ec=INK, lw=1.4)); ax.text(3.6, 4.35, "N-type silicon bar\n(lightly doped)", ha="center", va="center", fontsize=9.5)
    ax.add_patch(Rectangle((1.6, 2.5), 1.0, 0.9, fc="#ffe3b8", ec=INK, lw=1.4)); ax.text(2.1, 2.95, "P", ha="center", va="center", weight="bold")
    ax.plot([1.6, 0.6], [2.95, 2.95], color=INK, lw=2); ax.text(0.5, 3.2, "Emitter (E)", ha="left", fontsize=10)
    ax.plot([3.6, 3.6], [4.8, 5.5], color=INK, lw=2); ax.text(3.6, 5.65, "Base 2 ($B_2$)", ha="center", fontsize=10)
    ax.plot([3.6, 3.6], [1.2, 0.5], color=INK, lw=2); ax.text(3.6, 0.15, "Base 1 ($B_1$)", ha="center", fontsize=10)
    ax.annotate("", xy=(4.95, 2.95), xytext=(4.95, 4.75), arrowprops=dict(arrowstyle="<|-|>", color=RED)); ax.text(5.05, 3.85, "$R_{B2}$", color=RED, fontsize=11, va="center")
    ax.annotate("", xy=(4.95, 1.25), xytext=(4.95, 2.95), arrowprops=dict(arrowstyle="<|-|>", color=GREEN)); ax.text(5.05, 2.1, "$R_{B1}$", color=GREEN, fontsize=11, va="center")
    ax.text(6.4, 4.2, "ONE PN junction only\n(that is why 'uni-junction')", fontsize=10.5, va="center")
    ax.text(6.4, 2.7, "$R_{BB}=R_{B1}+R_{B2}$\ntypically 5–10 kΩ (E open)", fontsize=10.5, va="center", color=BLUE)
    ax.text(6.4, 1.2, "P region is heavily doped;\nthe emitter joint sits closer to $B_2$", fontsize=9.5, va="center", color=GRAY)
    save(fig, "p_ujt_struct")


def ujt_iv():
    fig, ax = new(6.6, 4.2)
    ie = np.array([0, 1, 3, 6, 10, 14, 18, 22, 26, 30, 36, 44, 55, 70]); ve = np.array([7.2, 8.0, 8.6, 8.85, 8.7, 7.5, 6.0, 4.6, 3.4, 2.5, 2.0, 1.85, 2.2, 2.9])
    from scipy.interpolate import PchipInterpolator as P
    ii = np.linspace(0, 70, 300); ax.plot(ii, P(ie, ve)(ii), color=BLUE)
    ax.set_xlim(0, 75); ax.set_ylim(0, 11); ax.set_xlabel("emitter current $I_E$ (mA)  [µA at the start]"); ax.set_ylabel("emitter voltage $V_E$ (V)")
    ax.plot([6], [8.85], "o", color=RED); ax.text(7, 9.3, "peak point $(I_P,V_P)$", color=RED, fontsize=9.5)
    ax.plot([44], [1.85], "o", color=GREEN); ax.text(41, 0.6, "valley point $(I_V,V_V)$", color=GREEN, fontsize=9.5, ha="center")
    ax.axvspan(0, 6, color="#eeeeee", alpha=.8); ax.text(3, 5, "cut-off", rotation=90, ha="center", fontsize=9.5)
    ax.axvspan(6, 44, color="#fff0d0", alpha=.7); ax.text(30, 8.2, "negative-resistance\nregion", ha="center", fontsize=9.5, color=ORANGE)
    ax.axvspan(44, 75, color="#e2f5ea", alpha=.7); ax.text(60, 7.0, "saturation\n(positive R again)", ha="center", fontsize=9.5, color=GREEN)
    ax.axhline(7.2, color=GRAY, lw=.8, ls=":"); ax.text(74, 7.35, "$\\eta V_{BB}$", ha="right", fontsize=9.5, color=GRAY)
    save(fig, "p_ujt_iv")


def ujt_wave():
    # exact simulation: RE=100k, CE=1nF... use eta=0.5, VBB=40 so VP=20 V; valley ~2 V ; fast discharge
    RE, CE, VBB, VP, VV = 100e3, 1e-9, 40.0, 20.0, 2.0
    tau = RE * CE; dt = tau / 400; t = 0; vc = VV; T = []; VC = []; state = "charge"; tdis = 0.06 * tau
    ts = np.arange(0, 5.2 * tau, dt); out = []
    vc = 0.0
    for tt in ts:
        out.append(vc)
        if state == "charge":
            vc += (VBB - vc) * dt / tau
            if vc >= VP: state = "dis"
        else:
            vc += (VV - vc) * dt / (0.04 * tau)
            if vc <= VV + 0.6: state = "charge"
    out = np.array(out)
    fig, axs = plt.subplots(3, 1, figsize=(7.2, 5.4), sharex=True)
    axs[0].plot(ts / tau, out, color=BLUE); axs[0].axhline(VP, color=RED, ls=":", lw=1); axs[0].text(5.15, VP + 1, "$V_P$", color=RED); axs[0].axhline(VV, color=GREEN, ls=":", lw=1); axs[0].text(5.15, VV + 1, "$V_V$", color=GREEN)
    axs[0].set_ylabel("$V_E$ = capacitor\nvoltage (V)"); axs[0].set_title("UJT relaxation oscillator (RE·CE = 1 → time in units of the time constant)", fontsize=10)
    # B1 positive spikes, B2 negative spikes when discharging
    dis = np.gradient(out) < -1e-3 * VBB
    b1 = np.where(dis, 1.0, 0.0); b2 = np.where(dis, -1.0, 0.0)
    axs[1].plot(ts / tau, b1, color=GREEN); axs[1].set_ylabel("$V_{B1}$\n(positive spikes)"); axs[1].set_yticks([])
    axs[2].plot(ts / tau, b2, color=ORANGE); axs[2].set_ylabel("$V_{B2}$\n(negative spikes)"); axs[2].set_yticks([]); axs[2].set_xlabel("time / (RE·CE)")
    fig.tight_layout(); save(fig, "p_ujt_wave")


def pn_formation():
    fig, axs = plt.subplots(5, 1, figsize=(7.4, 11.2), gridspec_kw={"height_ratios": [1.0, 1.15, 1.1, 1.0, 1.0]})
    x = np.linspace(-3, 3, 600); x1, x2 = -1.0, 1.0
    ax = axs[0]; ax.set_xlim(-3, 3); ax.set_ylim(0, 3); ax.axis("off")
    ax.add_patch(Rectangle((-3, 0.4), 2, 2, fc="#ffe3b8", ec=INK)); ax.add_patch(Rectangle((-1, 0.4), 1, 2, fc="#f1d6f5", ec=INK, hatch="--", alpha=.9)); ax.add_patch(Rectangle((0, 0.4), 1, 2, fc="#d6e4ff", ec=INK, hatch="++")); ax.add_patch(Rectangle((1, 0.4), 2, 2, fc="#cfe0ff", ec=INK))
    ax.text(-2, 1.4, "P", fontsize=16, ha="center", weight="bold"); ax.text(2, 1.4, "N", fontsize=16, ha="center", weight="bold")
    ax.text(-0.5, 1.4, "−\n−\n−", ha="center", va="center", fontsize=11, color=RED); ax.text(0.5, 1.4, "+\n+\n+", ha="center", va="center", fontsize=11, color=BLUE)
    ax.text(-0.5, 2.7, "exposed ionized\nacceptors", ha="center", fontsize=8.5); ax.text(0.5, 2.7, "exposed ionized\ndonors", ha="center", fontsize=8.5); ax.annotate("", xy=(-0.7, 0.2), xytext=(0.7, 0.2), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8)); ax.text(0, -0.05, "E (field points P ← N... from + to −)", ha="center", fontsize=8.5, color=GREEN)
    ax.set_title("(a) PN junction, space-charge region between $x_1$ and $x_2$", fontsize=10)
    ax = axs[1]
    p = np.where(x < x1, 1.0, np.where(x < x2, 10 ** (-3 * (x - x1) / (x2 - x1)), 1e-3)); n = p[::-1]
    ax.semilogy(x, np.maximum(p, 1e-4) * 1e17, color=ORANGE, label="holes"); ax.semilogy(x, np.maximum(n, 1e-4) * 1e17, color=BLUE, label="electrons")
    ax.axvspan(x1, x2, color="#f0f0f0"); ax.set_ylim(1e12, 3e17); ax.set_ylabel("carrier\nconcentration"); ax.legend(loc="center right", fontsize=8.5); ax.set_title("(b) charge concentration", fontsize=10); ax.set_xticks([])
    ax = axs[2]; rho = np.where((x > x1) & (x < 0), -1, np.where((x >= 0) & (x < x2), 1, 0)); ax.fill_between(x, rho, step="mid", color="#ddd", alpha=.9); ax.plot(x, rho, color=INK, drawstyle="steps-mid")
    ax.fill_between(x, rho, where=rho > 0, color="#cfe0ff", step="mid"); ax.fill_between(x, rho, where=rho < 0, color="#ffd7d7", step="mid")
    ax.axhline(0, color=INK, lw=.8); ax.set_ylim(-1.6, 1.6); ax.set_ylabel("space-charge\ndensity ρ"); ax.set_xticks([]); ax.set_title("(c) abrupt (alloy) junction:  ρ = −qN$_A$ for x$_1$<x<0,  ρ = +qN$_D$ for 0<x<x$_2$", fontsize=9.5)
    ax.text((x1) / 2, -1.25, "−qN$_A$", ha="center", color=RED); ax.text(x2 / 2, 1.2, "+qN$_D$", ha="center", color=BLUE)
    ax = axs[3]; E = np.where((x > x1) & (x < 0), (x - x1), np.where((x >= 0) & (x < x2), (x2 - x), 0)); ax.plot(x, -E, color=GREEN); ax.fill_between(x, -E, color="#dff5ea")
    ax.axhline(0, color=INK, lw=.8); ax.set_ylabel("electric\nfield E"); ax.set_xticks([]); ax.set_title("(d) field is a triangle: it is largest at the junction (x = 0)", fontsize=10)
    ax = axs[4]
    V = np.where(x < x1, 0, np.where(x < 0, (x - x1) ** 2 / 2, np.where(x < x2, 0.5 + (0.5 - (x2 - x) ** 2 / 2), 1.0)))
    ax.plot(x, V, color=PURPLE); ax.axhline(0, color=GRAY, lw=.8, ls=":"); ax.axhline(1, color=GRAY, lw=.8, ls=":"); ax.set_ylabel("potential V"); ax.set_xticks([x1, 0, x2]); ax.set_xticklabels(["$x_1$", "x = 0", "$x_2$"])
    ax.annotate("", xy=(2.4, 1), xytext=(2.4, 0), arrowprops=dict(arrowstyle="<|-|>", color=RED)); ax.text(2.45, 0.5, "$V_0$", color=RED, va="center", fontsize=11); ax.set_title("(e) potential rises by the contact (built-in) potential $V_0$", fontsize=10)
    ax.text(-2.6, 0.06, "$V_1$", fontsize=10); ax.text(1.6, 1.05, "$V_2$", fontsize=10)
    fig.tight_layout(); save(fig, "p_pn_formation")


def pn_bands():
    fig, ax = plt.subplots(figsize=(7.8, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(-0.6, 6.4); ax.axis("off")
    xs = np.array([0, 3.4, 4.2, 5.0, 5.8, 6.6, 10])
    def curve(y_l, y_r):
        xx = np.linspace(3.4, 6.6, 100); s = (xx - 3.4) / 3.2; ss = 3 * s ** 2 - 2 * s ** 3
        return np.concatenate([[0, 3.4], xx, [6.6, 10]]), np.concatenate([[y_l, y_l], y_l + (y_r - y_l) * ss, [y_r, y_r]])
    Eg = 2.6; Ecp = 5.1; Ecn = Ecp - 1.4
    for (yl, yr, c, lab, ls) in ((Ecp, Ecn, INK, "$E_{cp}$ → $E_{cn}$", "-"), (Ecp - Eg, Ecn - Eg, INK, "", "-")):
        x, y = curve(yl, yr); ax.plot(x, y, color=c, lw=2.4)
    ax.fill_between([0, 3.4], [Ecp, Ecp], [6.2, 6.2], color="#cfe0ff", alpha=.6); ax.fill_between([6.6, 10], [Ecn, Ecn], [6.2, 6.2], color="#cfe0ff", alpha=.6)
    ax.fill_between([0, 3.4], [Ecp - Eg, Ecp - Eg], [-0.5, -0.5], color="#ffe3b8", alpha=.7); ax.fill_between([6.6, 10], [Ecn - Eg, Ecn - Eg], [-0.5, -0.5], color="#ffe3b8", alpha=.7)
    EFp = Ecp - Eg * 0.5 - 0.7; ax.plot([0, 10], [EFp, EFp], color=RED, ls="--", lw=1.6); ax.text(10.05, EFp, "$E_F$ (same\nall through)", color=RED, va="center", fontsize=9.5)
    ax.text(0.1, 5.75, "P-region", fontsize=11, weight="bold"); ax.text(9.9, 5.75, "N-region", fontsize=11, weight="bold", ha="right"); ax.text(5.0, 6.15, "space-charge\nregion", ha="center", fontsize=9.5)
    ax.text(1.7, 5.45, "conduction band", ha="center", fontsize=9); ax.text(8.3, 4.65, "conduction band", ha="center", fontsize=9); ax.text(1.7, 0.1, "valence band", ha="center", fontsize=9); ax.text(8.3, -0.3, "valence band", ha="center", fontsize=9)
    ax.annotate("", xy=(5.0, Ecp), xytext=(5.0, Ecn), arrowprops=dict(arrowstyle="<|-|>", color=PURPLE, lw=1.6)); ax.text(5.15, (Ecp + Ecn) / 2 + .2, "$E_0=qV_0$", color=PURPLE, fontsize=11)
    ax.annotate("", xy=(0.4, Ecp), xytext=(0.4, Ecp - Eg), arrowprops=dict(arrowstyle="<|-|>", color=GRAY)); ax.text(0.5, Ecp - Eg / 2 + .55, "$E_G$", color=GRAY, fontsize=10)
    ax.plot([3.4, 3.4], [-0.5, 6.2], color=GRAY, lw=.8, ls=":"); ax.plot([6.6, 6.6], [-0.5, 6.2], color=GRAY, lw=.8, ls=":")
    ax.text(3.35, -0.55, "$x_1$", ha="right", fontsize=9); ax.text(6.65, -0.55, "$x_2$", fontsize=9)
    save(fig, "p_pn_bands")


def pn_bias():
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.3))
    for ax, (t, wid, bar, col) in zip(axs, (("Unbiased", 1.2, 1.0, "#f0f0f0"), ("Forward bias\nbarrier lowered, W shrinks", 0.55, 0.45, "#dff5ea"), ("Reverse bias\nbarrier raised, W grows", 2.1, 1.7, "#ffe1e1"))):
        ax.set_xlim(-4, 4); ax.set_ylim(-0.4, 2.4); ax.axis("off"); ax.set_title(t, fontsize=10)
        ax.add_patch(Rectangle((-4, 0.2), 4 - wid / 2, 0.9, fc="#ffe3b8", ec=INK)); ax.add_patch(Rectangle((wid / 2, 0.2), 4 - wid / 2, 0.9, fc="#cfe0ff", ec=INK)); ax.add_patch(Rectangle((-wid / 2, 0.2), wid, 0.9, fc=col, ec=INK, hatch="///"))
        ax.text(-2.5, 0.65, "P", ha="center", va="center", weight="bold", fontsize=12); ax.text(2.5, 0.65, "N", ha="center", va="center", weight="bold", fontsize=12)
        ax.annotate("", xy=(wid / 2, 1.6), xytext=(-wid / 2, 1.6), arrowprops=dict(arrowstyle="<|-|>", color=INK)); ax.text(0, 1.75, "W", ha="center", fontsize=10)
        ax.text(0, 2.15, f"barrier ∝ {'V₀' if t=='Unbiased' else ('V₀ − V' if 'Forward' in t else 'V₀ + V')}", ha="center", fontsize=9, color=PURPLE)
        ax.text(0, -0.15, "", ha="center")
    axs[0].text(0, -0.25, "diffusion = drift → net I = 0", ha="center", fontsize=8.8); axs[1].text(0, -0.25, "diffusion ≫ drift → big I (mA)", ha="center", fontsize=8.8, color=GREEN); axs[2].text(0, -0.25, "only minority carriers → tiny $I_0$", ha="center", fontsize=8.8, color=RED)
    fig.tight_layout(); save(fig, "p_pn_bias")


def run_all():
    scr_struct(); scr_iv(); scr_family(); scr_two_tr(); triac_struct(); triac_iv(); diac_iv(); phase_control(); ujt_struct(); ujt_iv(); ujt_wave(); pn_formation(); pn_bands(); pn_bias()


if __name__ == "__main__":
    run_all(); print("ok")
