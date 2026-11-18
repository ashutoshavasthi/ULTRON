"""Diagrams for Chapters 11-16 (added 2026-11-18). Same style and helpers as make_figs.py."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
from make_figs import save, arrow, BLUE, RED, GREEN, ORANGE, GREY, PURPLE


# ================================================================ schematic helpers
def wire(ax, pts, color="k", lw=1.4):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round")


def mosfet(ax, x, y, kind="n", label=None, gate_label=None, h=1.0):
    """Vertical MOSFET. Channel at x, from y-h/2 (bottom) to y+h/2 (top). Gate on the left.
    Returns (top, bottom, gate) terminal points."""
    top, bot = (x, y + h / 2), (x, y - h / 2)
    wire(ax, [(x, y + h / 2), (x, y + h * .25), (x - .25, y + h * .25), (x - .25, y - h * .25), (x, y - h * .25), (x, y - h / 2)])
    gx = x - .38
    wire(ax, [(gx, y + h * .25), (gx, y - h * .25)], lw=2)
    if kind == "p":
        ax.add_patch(Circle((gx - .08, y), .08, fill=False, lw=1.3))
        g = (gx - .16, y)
    else:
        g = (gx, y)
    wire(ax, [g, (g[0] - .45, y)])
    if label:
        ax.text(x + .08, y, label, fontsize=8, va="center", color=GREY)
    if gate_label:
        ax.text(g[0] - .5, y, gate_label, fontsize=10, ha="right", va="center", fontweight="bold")
    return top, bot, (g[0] - .45, y)


def vdd(ax, x, y, text="V$_{DD}$"):
    wire(ax, [(x - .3, y), (x + .3, y)], lw=2)
    ax.text(x, y + .12, text, ha="center", fontsize=9)


def gnd(ax, x, y):
    for i, w in enumerate((.3, .2, .1)):
        wire(ax, [(x - w, y - i * .08), (x + w, y - i * .08)])


def cap(ax, x, y):  # capacitor to ground hanging at (x, y)
    wire(ax, [(x, y), (x, y - .25)])
    wire(ax, [(x - .2, y - .25), (x + .2, y - .25)], lw=2)
    wire(ax, [(x - .2, y - .35), (x + .2, y - .35)], lw=2)
    wire(ax, [(x, y - .35), (x, y - .55)])
    gnd(ax, x, y - .55)


def resistor(ax, x0, y0, x1, y1, n=6, amp=.1, color="k"):
    t = np.linspace(0, 1, 2 * n + 1)
    dx, dy = x1 - x0, y1 - y0
    L = np.hypot(dx, dy); ux, uy = dx / L, dy / L; px, py = -uy, ux
    off = np.array([0] + [amp * (1 if i % 2 else -1) for i in range(1, 2 * n)] + [0])
    xs = x0 + t * dx + off * px; ys = y0 + t * dy + off * py
    ax.plot(xs, ys, color=color, lw=1.4)


def dot(ax, x, y):
    ax.add_patch(Circle((x, y), .05, color="k"))


# ================================================================ Ch11: regions of operation
def fig_mos_regions():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    ax = axs[0]
    k, vt = 1.0, 1.0
    vds = np.linspace(0, 5, 400)
    for vgs, c in ((2, GREY), (3, BLUE)):
        vov = vgs - vt
        i = np.where(vds < vov, k * (vov * vds - vds ** 2 / 2), k * vov ** 2 / 2)
        ax.plot(vds, i, color=c, lw=2)
        ax.text(5.05, k * vov ** 2 / 2, f"V$_{{GS}}$ = {vgs} V", va="center", fontsize=8, color=c)
    vov = 2
    ax.axvspan(0, .35, color="#d6eaf8", alpha=.8); ax.axvspan(.35, 1.0, color="#d5f5e3", alpha=.8)
    ax.axvspan(1.0, vov, color="#fdebd0", alpha=.8); ax.axvspan(vov, 5, color="#f5eef8", alpha=.8)
    for x, y, t in ((.17, 2.5, "①"), (.67, 2.5, "②"), (1.5, 2.5, "③ non-\nlinear"), (3.5, 2.5, "④ saturation\n(pinch-off)")):
        ax.text(x, y, t, ha="center", va="top", fontsize=8)
    ax.text(.05, 1.15, "① deep triode\n② linear", fontsize=7.5, bbox=dict(fc="white", ec=GREY, alpha=.9))
    ax.plot([vov, vov], [0, 2], ls="--", color=RED, lw=1); ax.text(vov + .08, 1.0, "V$_{DS,sat}$ =\nV$_{GS}$ − V$_{th}$", fontsize=8, color=RED)
    v2 = np.linspace(0, 5, 50); ax.plot(v2, v2 ** 2 / 2 * k, ls=":", color=RED, lw=1)
    ax.set_ylim(0, 2.6); ax.set_xlim(0, 6.2); ax.set_xlabel("V$_{DS}$ (V)"); ax.set_ylabel("I$_D$ (mA)")
    ax.set_title("Output characteristic: the four on-regions", fontsize=10)
    ax = axs[1]
    vg = np.linspace(0, 2, 400); vt = .7; n = 1.3; vT = .0259
    i = 1e-4 * (2 * n * vT) ** 2 * np.log1p(np.exp((vg - vt) / (2 * n * vT))) ** 2
    ax.semilogy(vg, i, color=BLUE, lw=2)
    ax.axvline(vt, color=GREY, ls="--", lw=1); ax.text(vt + .03, 1e-12, "V$_{th}$", color=GREY)
    ax.axvspan(0, vt, color="#fdebd0", alpha=.6)
    ax.text(.08, 3e-5, "sub-threshold\n(weak inversion)\nI$_D$ ∝ e$^{(V_{GS}-V_{th})/nV_T}$", fontsize=8)
    ax.text(1.05, 1e-9, "strong inversion\nI$_D$ ∝ (V$_{GS}$ − V$_{th}$)$^2$", fontsize=8)
    ax.annotate("slope S ≈ 60–100 mV\nper decade", xy=(.45, 1e-4 * (2 * n * vT) ** 2 * np.log1p(np.exp((.45 - vt) / (2 * n * vT))) ** 2), xytext=(.05, 1e-10),
                fontsize=8, arrowprops=dict(arrowstyle="->"))
    ax.set_ylim(1e-13, 1e-3); ax.set_xlabel("V$_{GS}$ (V)"); ax.set_ylabel("I$_D$ (A, log scale)")
    ax.set_title("Transfer characteristic on a log scale", fontsize=10)
    save(fig, "mos_regions")


def fig_mos_sce():
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.3))
    ax = axs[0]; lam = .08
    vds = np.linspace(0, 6, 300)
    for vov, c in ((1, GREY), (1.5, BLUE), (2, PURPLE)):
        i = np.where(vds < vov, vov * vds - vds ** 2 / 2, vov ** 2 / 2 * (1 + lam * (vds - vov)))
        i = np.where(vds < vov, i * (1 + lam * 0), i)
        ax.plot(vds, i, color=c, lw=2)
        ax.plot([-1 / lam, vov], [0, vov ** 2 / 2], ls=":", color=c, lw=.9)
    ax.set_xlim(-13.5, 6.5); ax.set_ylim(0, 3); ax.axvline(0, color="k", lw=.8)
    ax.text(-1 / lam + .5, .25, "−V$_A$ = −1/λ", ha="center", fontsize=8, color=RED); ax.plot(-1 / lam, 0, "o", color=RED)
    ax.set_xlabel("V$_{DS}$"); ax.set_ylabel("I$_D$"); ax.set_title("Channel-length modulation", fontsize=10)
    ax = axs[1]
    E = np.linspace(0, 10, 300); Ec = 2.0; mu = 1
    ax.plot(E, mu * E, ls="--", color=GREY, lw=1.2, label="v = μE (ideal)")
    ax.plot(E, mu * E / (1 + E / Ec), color=BLUE, lw=2, label="v = μE/(1 + E/E$_c$)")
    ax.axhline(mu * Ec, color=RED, ls=":", lw=1); ax.text(6, mu * Ec + .15, "→ v$_{sat}$ = μE$_c$", color=RED, fontsize=8)
    ax.set_ylim(0, 5); ax.set_xlabel("lateral field E"); ax.set_ylabel("drift velocity v$_d$")
    ax.legend(fontsize=7, loc="upper left", frameon=False); ax.set_title("Velocity saturation", fontsize=10)
    ax = axs[2]
    x = np.linspace(0, 1, 300)
    def barrier(drop, L):
        return .9 * np.exp(-((x - .5) / L) ** 2 * 3) - drop * x ** 4
    ax.plot(x, barrier(0, .5), color=BLUE, lw=2, label="long channel, any V$_{DS}$")
    ax.plot(x, .55 * np.exp(-((x - .45) / .22) ** 2 * 3) - 1.2 * x ** 3, color=RED, lw=2, label="short channel, high V$_{DS}$")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["source", "drain"]); ax.set_yticks([])
    ax.set_ylabel("electron energy (barrier)"); ax.legend(fontsize=7, frameon=False, loc="lower left")
    ax.set_title("DIBL: the drain pulls the source barrier down", fontsize=10)
    save(fig, "mos_sce")


# ================================================================ Ch12: CMOS inverter
def inverter_schematic(ax, x=2.5, ytop=4.4, label_in="V$_{in}$"):
    vdd(ax, x, ytop)
    t, b, g1 = mosfet(ax, x, ytop - .9, "p", "M2 (pMOS)")
    wire(ax, [(x, ytop), t])
    t2, b2, g2 = mosfet(ax, x, ytop - 2.5, "n", "M1 (nMOS)")
    wire(ax, [b, t2]); wire(ax, [b2, (x, ytop - 3.25)]); gnd(ax, x, ytop - 3.25)
    wire(ax, [g1, (g1[0] - .2, g1[1]), (g1[0] - .2, g2[1]), g2])
    mid = (x, ytop - 1.7); dot(ax, *mid); dot(ax, g1[0] - .2, ytop - 1.7)
    wire(ax, [(g1[0] - .2, ytop - 1.7), (g1[0] - .8, ytop - 1.7)])
    ax.text(g1[0] - .85, ytop - 1.7, label_in, ha="right", va="center", fontsize=10)
    wire(ax, [mid, (x + 1.3, mid[1])]); cap(ax, x + 1.0, mid[1]); ax.text(x + 1.25, mid[1] - .35, "C$_L$", fontsize=9)
    ax.text(x + 1.35, mid[1], "V$_{out}$", va="center", fontsize=10)


def fig_cmos_switch():
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.8))
    ax = axs[0]; ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.axis("off")
    inverter_schematic(ax); ax.set_title("CMOS inverter", fontweight="bold", fontsize=10)
    for k, (ax, vin) in enumerate(zip(axs[1:], ("0", "V$_{DD}$"))):
        ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.axis("off")
        x = 2.5; vdd(ax, x, 4.4)
        if k == 0:
            resistor(ax, x, 4.4, x, 3.2, color=BLUE); ax.text(x + .2, 3.8, "R$_p$ (pMOS ON)", color=BLUE, fontsize=9)
            wire(ax, [(x, 3.2), (x, 2.7)])
            wire(ax, [(x, 2.7), (x, 2.3)]); wire(ax, [(x, 2.3), (x + .35, 1.7)]); wire(ax, [(x, 1.5), (x, 1.0)])
            ax.text(x - 1.5, 1.8, "nMOS OFF\n(open)", fontsize=8, color=GREY)
            arrow(ax, x + 1.6, 2.2, x + 1.6, 2.65, color=GREEN); ax.text(x + 1.7, 2.3, "charges\nto V$_{DD}$", fontsize=8, color=GREEN)
            res = "V$_{out}$ = V$_{DD}$  (logic 1)"; tau = "τ = R$_p$C$_L$"
        else:
            wire(ax, [(x, 4.4), (x, 3.9)]); wire(ax, [(x, 3.9), (x + .35, 3.3)]); wire(ax, [(x, 3.1), (x, 2.7)])
            ax.text(x - 1.5, 3.4, "pMOS OFF\n(open)", fontsize=8, color=GREY)
            resistor(ax, x, 2.7, x, 1.0, color=RED); ax.text(x + .2, 1.6, "R$_n$ (nMOS ON)", color=RED, fontsize=9)
            arrow(ax, x + 1.6, 2.65, x + 1.6, 2.2, color=RED); ax.text(x + 1.7, 2.3, "discharges\nto 0", fontsize=8, color=RED)
            res = "V$_{out}$ = 0  (logic 0)"; tau = "τ = R$_n$C$_L$"
        dot(ax, x, 2.7); wire(ax, [(x, 2.7), (x + 1.0, 2.7)]); cap(ax, x + 1.0, 2.7)
        ax.text(x + 1.1, 2.85, "V$_{out}$", fontsize=9)
        gnd(ax, x, 1.0)
        ax.set_title(f"Switch model, V$_{{in}}$ = {vin}", fontweight="bold", fontsize=10)
        ax.text(2.5, .2, res + "\n" + tau, ha="center", fontsize=9)
    save(fig, "cmos_switch")


def fig_cmos_vtc():
    VDD, Vt, r = 2.5, 0.5, 1.0   # symmetric inverter, kn = kp
    vin = np.linspace(0, VDD, 1201)
    vout = []
    from math import sqrt
    for v in vin:
        lo, hi = 0.0, VDD
        def i_n(vo):
            vov = v - Vt
            if vov <= 0: return 0
            return vov * vo - vo ** 2 / 2 if vo < vov else vov ** 2 / 2
        def i_p(vo):
            vov = VDD - v - Vt
            if vov <= 0: return 0
            vsd = VDD - vo
            return r * (vov * vsd - vsd ** 2 / 2 if vsd < vov else vov ** 2 / 2)
        for _ in range(60):
            m = (lo + hi) / 2
            if i_n(m) - i_p(m) > 0: hi = m
            else: lo = m
        vout.append((lo + hi) / 2)
    vout = np.array(vout)
    g = np.gradient(vout, vin)
    il = vin[np.where(g < -1)[0][0]]; ih = vin[np.where(g < -1)[0][-1]]
    vol = np.interp(ih, vin, vout); voh = np.interp(il, vin, vout)
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    ax = axs[0]
    ax.plot(vin, vout, color=BLUE, lw=2.2); ax.plot([0, VDD], [0, VDD], ls="--", color=GREY, lw=1)
    vm = VDD / 2; ax.plot(vm, vm, "o", color=RED); ax.annotate("V$_M$ (switching threshold)\nV$_{out}$ = V$_{in}$", xy=(vm, vm), xytext=(1.45, 1.75), fontsize=8, arrowprops=dict(arrowstyle="->", color=RED), color=RED)
    for x, t in ((il, "V$_{IL}$"), (ih, "V$_{IH}$")):
        ax.axvline(x, ls=":", color=GREEN, lw=1); ax.text(x, -.22, t, ha="center", fontsize=8, color=GREEN)
    ax.text(.05, 2.25, "V$_{OH}$ = V$_{DD}$", fontsize=8, color=ORANGE); ax.text(1.9, .1, "V$_{OL}$ = 0", fontsize=8, color=ORANGE)
    ax.text(.15, .9, "slope = −1 at\nV$_{IL}$ and V$_{IH}$", fontsize=8, color=GREEN)
    for x0, x1, lab in ((0, Vt, "A"), (Vt, il + .12, "B"), (vm - .05, vm + .05, "C"), (ih - .12, VDD - Vt, "D"), (VDD - Vt, VDD, "E")):
        ax.text((x0 + x1) / 2, 2.62, lab, ha="center", fontweight="bold", fontsize=9)
    ax.set_xlim(0, VDD + .25); ax.set_ylim(-.3, 2.8); ax.set_xlabel("V$_{in}$ (V)"); ax.set_ylabel("V$_{out}$ (V)")
    ax.set_title(f"VTC (V$_{{DD}}$ = {VDD} V, V$_{{tn}}$ = |V$_{{tp}}$| = {Vt} V, matched)", fontsize=10)
    ax = axs[1]
    idd = []
    for v, vo in zip(vin, vout):
        vov = v - Vt
        idd.append(0 if vov <= 0 else (vov * vo - vo ** 2 / 2 if vo < vov else vov ** 2 / 2))
    ax.plot(vin, idd, color=RED, lw=2)
    ax.set_xlabel("V$_{in}$ (V)"); ax.set_ylabel("I$_{DD}$ (relative)")
    ax.set_title("Current from V$_{DD}$ to ground: only during switching", fontsize=10)
    ax.text(.05, max(idd) * .8, "static: I ≈ 0\n(one device OFF)", fontsize=8); ax.text(1.75, max(idd) * .8, "static: I ≈ 0", fontsize=8)
    save(fig, "cmos_vtc")
    return il, ih, vol, voh


def fig_cmos_gates():
    fig, axs = plt.subplots(1, 4, figsize=(13, 5.2))
    for ax in axs:
        ax.set_xlim(0, 6); ax.set_ylim(-.6, 7.2); ax.axis("off")
    # NAND: pMOS parallel, nMOS series
    ax = axs[0]; ax.set_title("2-input NAND  Y = (AB)′", fontweight="bold", fontsize=10)
    vdd(ax, 3, 6.6); wire(ax, [(2, 6.6), (4, 6.6)])
    for x, lab, m in ((2.2, "A", "M1"), (4.2, "B", "M2")):
        t, b, g = mosfet(ax, x, 5.7, "p", m, lab); wire(ax, [t, (x, 6.6)]); wire(ax, [b, (x, 4.9)])
    wire(ax, [(2.2, 4.9), (4.2, 4.9)]); dot(ax, 3.2, 4.9); wire(ax, [(3.2, 4.9), (3.2, 4.4)])
    wire(ax, [(4.2, 4.9), (5.3, 4.9)]); ax.text(5.35, 4.9, "Y", va="center", fontweight="bold")
    t, b, g = mosfet(ax, 3.2, 3.9, "n", "M3", "A"); t2, b2, g2 = mosfet(ax, 3.2, 2.6, "n", "M4", "B"); wire(ax, [b, t2]); wire(ax, [b2, (3.2, 1.8)]); gnd(ax, 3.2, 1.8)
    ax.text(3, .7, "PUN: pMOS in PARALLEL\nPDN: nMOS in SERIES", ha="center", fontsize=8)
    # NOR
    ax = axs[1]; ax.set_title("2-input NOR  Y = (A+B)′", fontweight="bold", fontsize=10)
    vdd(ax, 3.2, 6.8)
    t, b, g = mosfet(ax, 3.2, 6.1, "p", "M1", "A"); wire(ax, [t, (3.2, 6.8)])
    t2, b2, g2 = mosfet(ax, 3.2, 4.8, "p", "M2", "B"); wire(ax, [b, t2])
    wire(ax, [b2, (3.2, 3.9)]); dot(ax, 3.2, 3.9); wire(ax, [(3.2, 3.9), (5.3, 3.9)]); ax.text(5.35, 3.9, "Y", va="center", fontweight="bold")
    wire(ax, [(2.2, 3.9), (4.2, 3.9)])
    for x, lab, m in ((2.2, "A", "M3"), (4.2, "B", "M4")):
        t, b, g = mosfet(ax, x, 3.0, "n", m, lab); wire(ax, [(x, 3.9), t]); wire(ax, [b, (x, 2.2)])
    wire(ax, [(2.2, 2.2), (4.2, 2.2)]); wire(ax, [(3.2, 2.2), (3.2, 1.9)]); gnd(ax, 3.2, 1.9)
    ax.text(3, .7, "PUN: pMOS in SERIES\nPDN: nMOS in PARALLEL", ha="center", fontsize=8)
    # Complex gate Y = (AB + CD)'
    ax = axs[2]; ax.set_title("Y = (AB + CD)′", fontweight="bold", fontsize=10)
    vdd(ax, 3.2, 7.0); wire(ax, [(2.2, 7.0), (4.2, 7.0)])
    for x, lab in ((2.2, "A"), (4.2, "B")):
        t, b, g = mosfet(ax, x, 6.35, "p", None, lab); wire(ax, [t, (x, 7.0)]); wire(ax, [b, (x, 5.7)])
    wire(ax, [(2.2, 5.7), (4.2, 5.7)]); wire(ax, [(3.2, 5.7), (3.2, 5.45)])
    wire(ax, [(2.2, 5.45), (4.2, 5.45)])
    for x, lab in ((2.2, "C"), (4.2, "D")):
        t, b, g = mosfet(ax, x, 4.8, "p", None, lab); wire(ax, [t, (x, 5.45)]); wire(ax, [b, (x, 4.15)])
    wire(ax, [(2.2, 4.15), (4.2, 4.15)]); dot(ax, 3.2, 4.15); wire(ax, [(3.2, 4.15), (3.2, 3.9)])
    wire(ax, [(4.2, 4.15), (5.3, 4.15)]); ax.text(5.35, 4.15, "Y", va="center", fontweight="bold")
    wire(ax, [(2.2, 3.9), (4.2, 3.9)])
    for x, l1, l2 in ((2.2, "A", "B"), (4.2, "C", "D")):
        t, b, g = mosfet(ax, x, 3.35, "n", None, l1); t2, b2, g2 = mosfet(ax, x, 2.3, "n", None, l2)
        wire(ax, [(x, 3.9), t]); wire(ax, [b, t2]); wire(ax, [b2, (x, 1.6)])
    wire(ax, [(2.2, 1.6), (4.2, 1.6)]); wire(ax, [(3.2, 1.6), (3.2, 1.4)]); gnd(ax, 3.2, 1.4)
    ax.text(3, .2, "PDN: (A series B) ∥ (C series D)\nPUN: (A ∥ B) series (C ∥ D)", ha="center", fontsize=8)
    # pseudo-nMOS NOR
    ax = axs[3]; ax.set_title("Pseudo-nMOS NOR", fontweight="bold", fontsize=10)
    vdd(ax, 3.2, 6.6); t, b, g = mosfet(ax, 3.2, 5.7, "p", "always ON"); wire(ax, [t, (3.2, 6.6)])
    wire(ax, [g, (g[0], 5.2)]); gnd(ax, g[0], 5.2)
    wire(ax, [b, (3.2, 4.4)]); dot(ax, 3.2, 4.4); wire(ax, [(3.2, 4.4), (5.3, 4.4)]); ax.text(5.35, 4.4, "Y", va="center", fontweight="bold")
    wire(ax, [(2.2, 4.4), (4.2, 4.4)])
    for x, lab in ((2.2, "A"), (4.2, "B")):
        t, b, g = mosfet(ax, x, 3.5, "n", None, lab); wire(ax, [(x, 4.4), t]); wire(ax, [b, (x, 2.7)])
    wire(ax, [(2.2, 2.7), (4.2, 2.7)]); wire(ax, [(3.2, 2.7), (3.2, 2.4)]); gnd(ax, 3.2, 2.4)
    ax.text(3, .7, "N + 1 transistors (not 2N)\nbut static current when Y = 0\n(ratioed: V$_{OL}$ > 0)", ha="center", fontsize=8)
    save(fig, "cmos_gates")


# ================================================================ Ch13: Unit I extras
def fig_dos_carriers():
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.6), sharey=True)
    E = np.linspace(-1.2, 1.2, 600); Ec, Ev, Ef = .55, -.55, .3; kT = .06
    gc = np.where(E > Ec, np.sqrt(np.clip(E - Ec, 0, None)), 0); gv = np.where(E < Ev, np.sqrt(np.clip(Ev - E, 0, None)), 0)
    f = 1 / (1 + np.exp((E - Ef) / kT))
    axs[0].plot(gc, E, color=BLUE, lw=2); axs[0].plot(gv, E, color=RED, lw=2)
    axs[0].set_title("density of states g(E)", fontsize=10); axs[0].set_ylabel("Energy")
    axs[1].plot(f, E, color=GREEN, lw=2); axs[1].plot(1 - f, E, color=ORANGE, lw=1.2, ls="--")
    axs[1].set_title("f(E) (solid), 1 − f(E) (dashed)", fontsize=10)
    n = gc * f; p = gv * (1 - f)
    sc = 1 / max(n.max(), p.max()); axs[2].fill_betweenx(E, 0, n * sc, color=BLUE, alpha=.6); axs[2].fill_betweenx(E, 0, p * sc, color=RED, alpha=.6)
    axs[2].set_title("n(E) = g$_c$f   and   p(E) = g$_v$(1 − f)", fontsize=10)
    for ax in axs:
        for y, lab, c in ((Ec, "E$_c$", "k"), (Ev, "E$_v$", "k"), (Ef, "E$_F$", GREEN)):
            ax.axhline(y, color=c, lw=.8, ls="-" if lab != "E$_F$" else "--")
        ax.set_xticks([])
    axs[0].set_yticks([Ev, Ef, Ec]); axs[0].set_yticklabels(["E$_v$", "E$_F$", "E$_c$"])
    axs[2].text(.35, .75, "electrons (area = n)", fontsize=8, color=BLUE); axs[2].text(.05, -.75, "holes (area = p)", fontsize=8, color=RED); axs[2].set_xlim(0, 1.05)
    fig.suptitle("n-type example: E$_F$ above mid-gap ⇒ more electrons than holes", fontsize=10)
    save(fig, "dos_carriers")


def fig_n_vs_T():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    T = np.linspace(15, 900, 900); ND = 1e15; Nc300, Nv300 = 2.8e19, 1.04e19; Eg = 1.12; Ed = .045; k = 8.617e-5
    Nc = Nc300 * (T / 300) ** 1.5; Nv = Nv300 * (T / 300) ** 1.5
    ni = np.sqrt(Nc * Nv) * np.exp(-Eg / (2 * k * T))
    nd_ion = []
    for t, nc, nI in zip(T, Nc, ni):
        lo, hi = 1, 1e20
        for _ in range(200):
            n = np.sqrt(lo * hi)
            ef_ec = k * t * np.log(n / nc)                  # E_F - E_c
            ndp = ND / (1 + 2 * np.exp((ef_ec + Ed) / (k * t)))
            p = nI ** 2 / n
            if n > ndp + p: hi = n
            else: lo = n
        nd_ion.append(n)
    n = np.array(nd_ion)
    ax.plot(T, n / ND, color=BLUE, lw=2.2); ax.plot(T, ni / ND, ls="--", color=GREY, lw=1, label="n$_i$/N$_D$")
    ax.set_yscale("log"); ax.set_ylim(1e-2, 1e2); ax.set_xlim(0, 900)
    ax.axhline(1, color=GREEN, ls=":", lw=1)
    ax.axvspan(0, 100, color="#d6eaf8", alpha=.6); ax.axvspan(100, 520, color="#d5f5e3", alpha=.5); ax.axvspan(520, 900, color="#fadbd8", alpha=.5)
    ax.text(50, 30, "freeze-out", ha="center", fontsize=9); ax.text(310, 30, "extrinsic: n ≈ N$_D$\n(where chips work)", ha="center", fontsize=9)
    ax.text(710, 30, "intrinsic:\nn ≈ n$_i$ ≫ N$_D$", ha="center", fontsize=9)
    ax.axvline(300, color="k", lw=.6); ax.text(305, .015, "300 K", fontsize=8)
    ax.set_xlabel("Temperature T (K)"); ax.set_ylabel("n / N$_D$"); ax.legend(fontsize=8, loc="lower right", frameon=False)
    ax.set_title("Si, N$_D$ = 10$^{15}$ cm$^{-3}$ (P, E$_c$ − E$_D$ = 45 meV)", fontsize=10)
    save(fig, "n_vs_T")


def fig_continuity():
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.2))
    t = np.linspace(-1, 4, 400)
    ax = axs[0]; ax.plot(t, np.where(t < 0, 1, np.exp(-t)), color=BLUE, lw=2)
    ax.axvline(0, color=GREY, ls="--", lw=1); ax.text(.05, 1.03, "light OFF at t = 0", fontsize=8)
    ax.plot([0, 1], [1, 0], ls=":", color=RED); ax.text(1.02, .03, "τ", color=RED, fontsize=11)
    ax.set_xlabel("time t (units of τ)"); ax.set_ylabel("Δn / (G$_L$τ)"); ax.set_title("Δn(t) = G$_L$τ e$^{-t/τ}$", fontsize=10); ax.set_ylim(0, 1.15)
    ax = axs[1]; x = np.linspace(0, 4, 400); ax.plot(x, np.exp(-x), color=GREEN, lw=2)
    ax.plot([0, 1], [1, 0], ls=":", color=RED); ax.text(1.02, .03, "L$_n$ = √(D$_n$τ)", color=RED, fontsize=9)
    ax.set_xlabel("distance x from the injection point (units of L$_n$)"); ax.set_ylabel("Δn(x) / Δn(0)")
    ax.set_title("Steady state: Δn(x) = Δn(0) e$^{-x/L_n}$", fontsize=10)
    save(fig, "continuity")


def fig_diode_gr():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
    V = np.linspace(0, .8, 400); VT = .0259
    J0 = 1e-15; Jr0 = 1e-10
    Jd = J0 * (np.exp(V / VT) - 1); Jr = Jr0 * (np.exp(V / (2 * VT)) - 1)
    ax = axs[0]
    ax.semilogy(V, Jd + Jr, color=BLUE, lw=2.2, label="total")
    ax.semilogy(V, Jd + 1e-30, ls="--", color=GREEN, lw=1, label="ideal diffusion, η = 1")
    ax.semilogy(V, Jr + 1e-30, ls="--", color=RED, lw=1, label="recombination, η = 2")
    ax.set_ylim(1e-12, 1e-1); ax.set_xlabel("forward voltage V$_a$ (V)"); ax.set_ylabel("J (log scale)")
    ax.legend(fontsize=8, frameon=False, loc="upper left"); ax.set_title("Forward: two slopes (ideality factor)", fontsize=10)
    ax.text(.08, 1e-11, "low V: G-R wins\nslope 1/(2V$_T$)", fontsize=8, color=RED); ax.text(.5, 1e-6, "high V: diffusion wins\nslope 1/V$_T$", fontsize=8, color=GREEN)
    ax = axs[1]; VR = np.linspace(0, 10, 300)
    ax.plot(VR, np.ones_like(VR), ls="--", color=GREEN, lw=1.2, label="J$_0$ alone (flat)")
    ax.plot(VR, 1 + 2 * np.sqrt(.7 + VR), color=BLUE, lw=2, label="J$_0$ + J$_{gen}$ (∝ W ∝ √(V$_{bi}$ + V$_R$))")
    ax.set_xlabel("reverse voltage V$_R$ (V)"); ax.set_ylabel("|J$_{rev}$| (relative)"); ax.legend(fontsize=8, frameon=False)
    ax.set_title("Reverse: current creeps up with V$_R$", fontsize=10)
    save(fig, "diode_gr")


def fig_diode_quadrants():
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    V = np.linspace(-2, .75, 500); VT = .0259; I0 = 1e-9
    I = I0 * (np.exp(V / VT) - 1); I = I / 1e-3
    IL = 2.0
    ax.plot(V, np.clip(I, -5, 5), color=BLUE, lw=2, label="dark")
    ax.plot(V, np.clip(I - IL, -5, 5), color=ORANGE, lw=2, label="illuminated (shifted down by I$_{ph}$)")
    ax.axhline(0, color="k", lw=.8); ax.axvline(0, color="k", lw=.8)
    ax.text(.35, 3.5, "Q1: forward\nLED", fontsize=9, ha="center"); ax.text(-1.2, 3.5, "Q2: not used", fontsize=9, ha="center")
    ax.text(-1.2, -3.3, "Q3: reverse + light\nphotodetector", fontsize=9, ha="center"); ax.text(.42, -3.6, "Q4: solar cell\n(power out)", fontsize=9, ha="center")
    ax.plot(0, -IL, "o", color=RED); ax.text(.03, -IL - .45, "I$_{SC}$", color=RED, fontsize=9)
    voc = VT * np.log(IL * 1e-3 / I0 + 1); ax.plot(voc, 0, "o", color=RED); ax.text(voc - .05, .3, "V$_{OC}$", color=RED, fontsize=9)
    ax.set_xlim(-2, .8); ax.set_ylim(-5, 5); ax.set_xlabel("V"); ax.set_ylabel("I (mA)"); ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_title("One junction, four jobs", fontsize=10)
    save(fig, "diode_quadrants")


def fig_cv_profiling():
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    Vbi = .8; V = np.linspace(-5, .7, 100); y = (Vbi - V)
    ax.plot(V, y, color=BLUE, lw=2); ax.plot([.7, Vbi], [Vbi - .7, 0], ls=":", color=BLUE)
    ax.plot(Vbi, 0, "o", color=RED); ax.text(Vbi - .2, .35, "intercept\n= V$_{bi}$", color=RED, fontsize=8, ha="right")
    ax.annotate("slope = −2 / (q ε$_s$ N$_D$)\n⇒ gives N$_D$", xy=(-2.5, 3.3), xytext=(-4.8, 1.0), fontsize=9, arrowprops=dict(arrowstyle="->"))
    ax.axhline(0, color="k", lw=.8); ax.set_xlabel("applied voltage V$_A$ (reverse is negative)"); ax.set_ylabel("1 / C² (per area²)")
    ax.set_title("C–V profiling of a one-sided p⁺n junction", fontsize=10); ax.set_yticks([])
    save(fig, "cv_profiling")


def fig_mos_bands():
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.6))
    x = np.linspace(0, 1, 200); Eg = 1.0; phiF = .3
    for ax, (bend, title) in zip(axs, ((-.15, "Accumulation (V$_G$ < 0)"), (.2, "Depletion (small V$_G$ > 0)"), (2 * phiF, "Strong inversion (ψ$_s$ = 2φ$_F$)"))):
        prof = bend * np.exp(-x / .3)
        Ei = 0 - prof; Ec = Ei + Eg / 2; Ev = Ei - Eg / 2; EF = -phiF * np.ones_like(x)
        ax.plot(x, Ec, color=BLUE, lw=2); ax.plot(x, Ev, color=RED, lw=2); ax.plot(x, Ei, color=GREY, ls=":", lw=1.2); ax.plot(x, EF, color=GREEN, ls="--", lw=1.4)
        ax.axvline(0, color="k", lw=2); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-1.05, .95)
        ax.text(1.01, Ec[-1], "E$_c$", va="center", fontsize=8); ax.text(1.01, Ev[-1], "E$_v$", va="center", fontsize=8)
        ax.text(1.01, Ei[-1], "E$_i$", va="center", fontsize=8); ax.text(1.01, EF[-1] - .05, "E$_F$", va="center", fontsize=8, color=GREEN)
        ax.set_title(title, fontsize=9); ax.set_xlabel("oxide | ← depth into p-Si →")
    ax = axs[0]; ax.annotate("", xy=(.95, -phiF), xytext=(.95, 0), arrowprops=dict(arrowstyle="<->", color=PURPLE)); ax.text(.8, -.17, "qφ$_F$", color=PURPLE, fontsize=9)
    ax = axs[2]; ax.text(.04, -.5, "surface: E$_i$ below E$_F$\n⇒ surface is n-type", fontsize=8, color=PURPLE)
    save(fig, "mos_bands")


def fig_bjt_profile():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.axvspan(-1, 0, color="#d6eaf8"); ax.axvspan(0, 1, color="#fadbd8"); ax.axvspan(1, 2, color="#d6eaf8")
    ax.text(-.5, 1.05, "n⁺ emitter", ha="center"); ax.text(.5, 1.05, "p base (W$_{Bn}$)", ha="center"); ax.text(1.5, 1.05, "n collector", ha="center")
    xb = np.linspace(0, 1, 50); ax.plot(xb, 1 - xb, color=BLUE, lw=2.2); ax.plot(xb, (np.sinh((1 - xb) * 1.5) / np.sinh(1.5)), ls="--", color=GREY, lw=1)
    ax.text(.25, .8, "n$_b$(0) = (n$_i$²/N$_{AB}$) e$^{qV_{BE}/kT}$", fontsize=8, color=BLUE)
    ax.text(1.03, .05, "n$_b$(W) ≈ 0", fontsize=8, color=BLUE)
    xe = np.linspace(-1, 0, 50); ax.plot(xe, .12 * np.exp(xe * 4), color=RED, lw=1.6); ax.text(-.95, .2, "holes back-injected\n(I$_{Ep}$, small)", fontsize=8, color=RED)
    ax.set_ylim(0, 1.15); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylabel("minority carriers")
    ax.set_title("Forward active: electrons in a short base decay almost linearly", fontsize=10)
    save(fig, "bjt_profile")


# ================================================================ Ch14: manufacturing
def fig_cz():
    fig, ax = plt.subplots(figsize=(5.2, 5.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.axis("off")
    ax.add_patch(Rectangle((1, .5), 8, 9.8, fill=False, lw=1.4, ls="--", ec=GREY)); ax.text(1.1, 9.9, "chamber: vacuum, then argon", fontsize=8, color=GREY)
    ax.add_patch(Rectangle((2.2, 1.6), 5.6, 3.2, fc="#5d6d7e", ec="k")); ax.text(5, 1.15, "graphite susceptor + heater (RF / resistance)", ha="center", fontsize=8)
    ax.add_patch(Rectangle((2.6, 2.0), 4.8, 2.8, fc="#fdfefe", ec="k", lw=1.5)); ax.text(7.5, 4.4, "silica (quartz)\ncrucible", fontsize=8)
    ax.add_patch(Rectangle((2.65, 2.05), 4.7, 1.9, fc="#f5b041", ec="none")); ax.text(5, 2.6, "molten Si ≈ 1412–1417 °C", ha="center", fontsize=8)
    ax.add_patch(Polygon([(4.3, 3.95), (5.7, 3.95), (5.6, 4.6), (5.6, 7.6), (4.4, 7.6), (4.4, 4.6)], fc="#aed6f1", ec="k")); ax.text(5, 6.0, "single-\ncrystal\ningot", ha="center", fontsize=8)
    ax.add_patch(Rectangle((4.8, 7.6), .4, .4, fc="#1f618d", ec="k")); ax.text(5.35, 7.7, "seed ⟨100⟩/⟨111⟩", fontsize=8)
    wire(ax, [(5, 8), (5, 10.6)], lw=2); arrow(ax, 6.0, 8.6, 6.0, 9.6, color=BLUE); ax.text(6.15, 9.0, "pull slowly\n(mm/min)", fontsize=8, color=BLUE)
    ax.text(3.0, 9.0, "↺ seed shaft\nanticlockwise", fontsize=8, ha="center", color=PURPLE)
    wire(ax, [(5, 1.6), (5, .2)], lw=2); ax.text(6.4, .6, "↻ crucible shaft clockwise", fontsize=8, ha="center", color=PURPLE)
    ax.set_title("Czochralski (CZ) crystal puller", fontweight="bold", fontsize=10)
    save(fig, "cz")


def fig_deal_grove():
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    A, B = .165, .0117   # um, um^2/h  (dry O2 ~1100 C, illustrative)
    t = np.linspace(0, 10, 300); x = (-A + np.sqrt(A ** 2 + 4 * B * t)) / 2
    ax.plot(t, x, color=BLUE, lw=2.2, label="Deal–Grove: x² + Ax = B t")
    ax.plot(t, (B / A) * t, ls="--", color=GREEN, lw=1.2, label="thin: x ≈ (B/A) t  (reaction-limited)")
    ax.plot(t, np.sqrt(B * t), ls="--", color=RED, lw=1.2, label="thick: x ≈ √(B t)  (diffusion-limited)")
    ax.set_ylim(0, .4); ax.set_xlabel("oxidation time t (h)"); ax.set_ylabel("oxide thickness x (μm)")
    ax.legend(fontsize=8, frameon=False); ax.set_title("Thermal oxidation: linear, then parabolic", fontsize=10)
    save(fig, "deal_grove")


def fig_diffusion_profiles():
    from math import erfc
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    x = np.linspace(0, 3, 300); ax = axs[0]
    for Dt, c in ((.05, GREY), (.15, BLUE), (.4, PURPLE)):
        ax.plot(x, [erfc(xx / (2 * np.sqrt(Dt))) for xx in x], color=c, lw=2, label=f"√(Dt) = {np.sqrt(Dt):.2f}")
    ax.set_title("Pre-deposition: constant surface C$_s$ ⇒ erfc", fontsize=10); ax.set_xlabel("depth x"); ax.set_ylabel("C / C$_s$"); ax.legend(fontsize=8, frameon=False)
    ax = axs[1]; Q = .3
    for Dt, c in ((.05, GREY), (.15, BLUE), (.4, PURPLE)):
        ax.plot(x, Q / np.sqrt(np.pi * Dt) * np.exp(-x ** 2 / (4 * Dt)), color=c, lw=2, label=f"√(Dt) = {np.sqrt(Dt):.2f}")
    ax.set_title("Drive-in: fixed dose Q ⇒ Gaussian (surface C falls)", fontsize=10); ax.set_xlabel("depth x"); ax.set_ylabel("C (same dose Q under each curve)"); ax.legend(fontsize=8, frameon=False)
    save(fig, "diffusion_profiles")


def fig_implant():
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    x = np.linspace(0, .8, 400)
    for name, Rp, dR, c in (("B", .53, .093, RED), ("P", .25, .073, BLUE), ("As", .12, .036, GREEN), ("Sb", .09, .025, PURPLE)):
        y = np.exp(-(x - Rp) ** 2 / (2 * dR ** 2)) / (np.sqrt(2 * np.pi) * dR)
        ax.plot(x, y, color=c, lw=2); ax.text(Rp, y.max() * 1.03, name, color=c, ha="center", fontweight="bold")
    ax.set_xlabel("depth (μm)"); ax.set_ylabel("concentration (same dose)"); ax.set_yticks([])
    ax.set_title("Ion implantation at 200 keV: C(x) = C$_p$ exp[−(x − R$_p$)²/2ΔR$_p$²]", fontsize=9)
    ax.text(.45, ax.get_ylim()[1] * .55, "light ion (B): deeper, broader\nheavy ion (Sb): shallow, narrow", fontsize=8)
    save(fig, "implant")


def fig_litho_resist():
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.6))
    for ax, kind in zip(axs, ("positive", "negative")):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
        ax.set_title(f"{kind.capitalize()} resist", fontweight="bold", fontsize=10)
        ax.add_patch(Rectangle((1, 8.6), 8, .3, fc="#d5d8dc", ec="k")); ax.add_patch(Rectangle((4, 8.6), 2, .3, fc="k"))
        ax.text(9.2, 8.6, "mask", fontsize=8)
        for xx in (1.5, 2.5, 3.5, 6.5, 7.5, 8.5): arrow(ax, xx, 9.7, xx, 9.05, color=PURPLE, lw=1)
        ax.text(.1, 9.4, "UV", color=PURPLE, fontsize=8)
        ax.add_patch(Rectangle((1, 6.0), 8, .6, fc="#aab7b8", ec="k")); ax.add_patch(Rectangle((1, 6.6), 8, .5, fc="#f9e79f", ec="k"))
        ax.add_patch(Rectangle((1, 6.6), 3, .5, fc="#e59866", ec="k")); ax.add_patch(Rectangle((6, 6.6), 3, .5, fc="#e59866", ec="k"))
        ax.text(9.2, 6.75, "resist", fontsize=8); ax.text(9.2, 6.1, "film", fontsize=8); ax.text(5, 7.35, "exposed regions shaded orange", ha="center", fontsize=7)
        ax.text(5, 5.3, "after developing ↓", ha="center", fontsize=8)
        ax.add_patch(Rectangle((1, 3.6), 8, .6, fc="#aab7b8", ec="k"))
        if kind == "positive":
            ax.add_patch(Rectangle((4, 4.2), 2, .5, fc="#f9e79f", ec="k")); txt = "exposed part dissolves ⇒ pattern = mask"
        else:
            ax.add_patch(Rectangle((1, 4.2), 3, .5, fc="#e59866", ec="k")); ax.add_patch(Rectangle((6, 4.2), 3, .5, fc="#e59866", ec="k")); txt = "exposed part cross-links ⇒ pattern = inverse"
        ax.text(5, 2.6, txt, ha="center", fontsize=8)
        ax.text(5, 1.4, "higher resolution, better CD control" if kind == "positive" else "tougher etch resistance, lower resolution", ha="center", fontsize=8, color=GREY)
    save(fig, "litho_resist")


def fig_nmos_flow():
    steps = ["1. p-Si substrate", "2. grow thick SiO₂", "3–7. resist, mask 1, UV,\ndevelop, HF etch: S/D windows",
             "8–9. strip resist (piranha);\ndiffuse/implant n⁺ S/D", "10–13. regrow oxide; mask 2 opens gate;\ngrow THIN gate oxide",
             "14–16. mask 3 opens contacts;\ndeposit Al; mask 4 patterns S, G, D"]
    fig, axs = plt.subplots(2, 3, figsize=(11, 5.2))
    for i, (ax, s) in enumerate(zip(axs.flat, steps)):
        ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off"); ax.set_title(s, fontsize=8.5)
        ax.add_patch(Rectangle((.5, .5), 9, 2.8, fc="#fadbd8", ec="k")); ax.text(9.3, .8, "p", ha="right", fontsize=9)
        if i >= 3:
            for x in (1.8, 6.4): ax.add_patch(Rectangle((x, 2.3), 1.8, 1.0, fc="#aed6f1", ec="k")); ax.text(x + .9, 2.7, "n⁺", ha="center", fontsize=9)
        if i == 1:
            ax.add_patch(Rectangle((.5, 3.3), 9, .8, fc="#f9e79f", ec="k"))
        if i in (2, 3):
            ax.add_patch(Rectangle((.5, 3.3), 1.3, .8, fc="#f9e79f", ec="k")); ax.add_patch(Rectangle((3.6, 3.3), 2.8, .8, fc="#f9e79f", ec="k")); ax.add_patch(Rectangle((8.2, 3.3), 1.3, .8, fc="#f9e79f", ec="k"))
            if i == 2:
                for x0, w in ((.5, 1.3), (3.6, 2.8), (8.2, 1.3)): ax.add_patch(Rectangle((x0, 4.1), w, .5, fc="#e59866", ec="k"))
                ax.text(5, 5.0, "resist", ha="center", fontsize=8)
        if i == 4:
            ax.add_patch(Rectangle((.5, 3.3), 3.6, .8, fc="#f9e79f", ec="k")); ax.add_patch(Rectangle((5.9, 3.3), 3.6, .8, fc="#f9e79f", ec="k"))
            ax.add_patch(Rectangle((4.1, 3.3), 1.8, .2, fc="#f4d03f", ec="k")); ax.text(5, 3.8, "thin\nt$_{ox}$", ha="center", fontsize=7)
        if i == 5:
            ax.add_patch(Rectangle((.5, 3.3), 1.6, .8, fc="#f9e79f", ec="k")); ax.add_patch(Rectangle((3.4, 3.3), .7, .8, fc="#f9e79f", ec="k"))
            ax.add_patch(Rectangle((5.9, 3.3), .7, .8, fc="#f9e79f", ec="k")); ax.add_patch(Rectangle((7.9, 3.3), 1.6, .8, fc="#f9e79f", ec="k"))
            ax.add_patch(Rectangle((4.1, 3.3), 1.8, .2, fc="#f4d03f", ec="k"))
            for x0, w, lab in ((2.1, 1.3, "S"), (4.1, 1.8, "G"), (6.6, 1.3, "D")):
                ax.add_patch(Rectangle((x0, 3.5 if lab == "G" else 3.3), w, 1.1 if lab != "G" else .9, fc="#aab7b8", ec="k")); ax.text(x0 + w / 2, 4.7, lab, ha="center", fontweight="bold")
    fig.suptitle("Metal-gate NMOS process flow (four masks)", fontsize=10)
    save(fig, "nmos_flow")


# ================================================================ Ch15: SPICE equivalent circuit
def fig_spice_eqckt():
    fig, ax = plt.subplots(figsize=(6.4, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    D, S, G, B = (5, 9.6), (5, .4), (.6, 5), (9.4, 5)
    for p, lab in ((D, "D"), (S, "S"), (G, "G"), (B, "B")):
        ax.add_patch(Circle(p, .18, fc="white", ec="k", lw=1.5)); ax.text(p[0] + (.35 if lab != "G" else -.45), p[1], lab, fontweight="bold", va="center")
    resistor(ax, 5, 9.4, 5, 8.0); ax.text(5.2, 8.7, "R$_D$", fontsize=9)
    resistor(ax, 5, 2.0, 5, .6); ax.text(5.2, 1.3, "R$_S$", fontsize=9)
    wire(ax, [(5, 8.0), (5, 7.4)]); dot(ax, 5, 7.4); ax.text(4.6, 7.55, "D′", fontsize=8)
    wire(ax, [(5, 2.6), (5, 2.0)]); dot(ax, 5, 2.6); ax.text(4.55, 2.4, "S′", fontsize=8)
    ax.add_patch(Circle((5, 5), .6, fill=False, lw=1.5)); arrow(ax, 5, 4.6, 5, 5.4); wire(ax, [(5, 7.4), (5, 5.6)]); wire(ax, [(5, 4.4), (5, 2.6)])
    ax.text(6.0, 4.4, "I$_D$ (Level-1 equation)", fontsize=8, va="center")
    def c(x0, y0, x1, y1, lab, lx, ly):
        wire(ax, [(x0, y0), (x1, y1)], color=BLUE, lw=1); ax.text(lx, ly, lab, fontsize=8, color=BLUE)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2; ax.plot(mx, my, marker="$\\|\\|$", ms=12, color=BLUE)
    c(.8, 5, 4.9, 7.3, "C$_{gd}$", 2.3, 6.6); c(.8, 5, 4.9, 2.7, "C$_{gs}$", 2.3, 3.2)
    wire(ax, [(.8, 5), (2.0, 5)]); c(2.0, 5, 4.2, 5, "C$_{gb}$", 2.9, 5.25)
    wire(ax, [(4.2, 5), (4.2, 6.2), (5.8, 6.2), (5.8, 5), (9.2, 5)], color=BLUE, lw=1)
    for (y, lab) in ((7.4, "D-B diode + C$_{db}$"), (2.6, "S-B diode + C$_{sb}$")):
        wire(ax, [(5, y), (8.0, y)], color=RED, lw=1); ax.plot(7.0, y, marker=">", ms=9, color=RED); wire(ax, [(8.0, y), (8.0, 5), (9.2, 5)], color=RED, lw=1)
        ax.text(6.3, y + .25, lab, fontsize=8, color=RED)
    ax.set_title("SPICE MOSFET model: an ideal current source plus parasitics", fontsize=10)
    save(fig, "spice_eqckt")


# ================================================================ Ch16: memories
def fig_mem_array():
    fig, ax = plt.subplots(figsize=(6.6, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")
    ax.add_patch(FancyBboxPatch((.3, 2.0), 1.6, 4.6, boxstyle="round,pad=.05", fc="#d6eaf8", ec="k")); ax.text(1.1, 4.3, "row\ndecoder\n\nN address\nbits →\n2$^N$ word\nlines", ha="center", va="center", fontsize=8)
    for i in range(6):
        y = 2.4 + i * .75; wire(ax, [(1.9, y), (8.6, y)], color=BLUE, lw=1.2)
    for j in range(7):
        x = 2.6 + j * .9; wire(ax, [(x, 1.6), (x, 6.8)], color=RED, lw=1.2)
        for i in range(6): ax.add_patch(Rectangle((x - .14, 2.4 + i * .75 - .14), .28, .28, fc="white", ec="k", lw=.8))
    ax.add_patch(Rectangle((2.6 + 3 * .9 - .14, 2.4 + 3 * .75 - .14), .28, .28, fc=ORANGE, ec="k"))
    ax.text(5.6, 4.9, "selected cell", fontsize=8, color=ORANGE)
    ax.add_patch(FancyBboxPatch((.3, .3), 9.4, 1.0, boxstyle="round,pad=.05", fc="#fadbd8", ec="k")); ax.text(5.3, .8, "sense amplifiers + column decoder (M address bits → picks from 2$^M$ bit lines)", ha="center", fontsize=8)
    ax.text(8.7, 6.2, "word lines\n(rows)", color=BLUE, fontsize=8); ax.text(7.6, 7.1, "bit lines (columns)", color=RED, fontsize=8)
    ax.set_title("Memory array: 2$^N$ × 2$^M$ cells, one bit at each crossing", fontsize=10)
    save(fig, "mem_array")


def fig_nor_rom():
    fig, ax = plt.subplots(figsize=(7.4, 5.6)); ax.set_xlim(-.5, 10.5); ax.set_ylim(-.8, 10.4); ax.axis("off")
    cols = [3.0, 4.8, 6.6, 8.4]; rows = [7.2, 5.6, 4.0, 2.4]
    tx = {0: (0, 2), 1: (0, 1), 2: (1, 2), 3: (0, 3)}   # row -> columns with a transistor (from the board)
    wire(ax, [(2.2, 9.8), (9.4, 9.8)], lw=2); ax.text(9.5, 9.8, "V$_{DD}$", va="center")
    for j, x in enumerate(cols):
        t, b, g = mosfet(ax, x, 9.1, "p", h=.9)
        wire(ax, [t, (x, 9.8)]); wire(ax, [g, (g[0], 8.45)]); gnd(ax, g[0], 8.45)
        wire(ax, [b, (x, 1.2)], color=RED, lw=1.6); ax.text(x, .75, f"C{j + 1}", ha="center", color=RED, fontweight="bold")
    for i, y in enumerate(rows):
        wire(ax, [(1.0, y), (9.2, y)], color=BLUE, lw=1.6); ax.text(.95, y, f"R{i + 1}", ha="right", va="center", color=BLUE, fontweight="bold")
        for j in tx[i]:
            x = cols[j] - .45
            wire(ax, [(cols[j], y - .15), (x + .3, y - .15)])
            wire(ax, [(x + .3, y - .15), (x + .3, y - .75)], lw=1.2)
            wire(ax, [(x + .3, y - .75), (x + .3, y - .95)]); gnd(ax, x + .3, y - .95)
            wire(ax, [(x + .18, y - .2), (x + .18, y - .7)], lw=2); wire(ax, [(x + .18, y - .45), (x - .05, y - .45), (x - .05, y)])
            dot(ax, x - .05, y)
    ax.text(5.5, -.6, "nMOS at (Ri, Cj): Ri = 1 pulls Cj to 0.  No nMOS: Cj stays 1 (pMOS pull-up).", ha="center", fontsize=8)
    ax.set_title("4 × 4 NOR ROM from your board notes", fontsize=10)
    save(fig, "nor_rom")


def fig_sram_dram():
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.4))
    ax = axs[0]; ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off"); ax.set_title("6T SRAM cell", fontweight="bold", fontsize=10)
    wire(ax, [(.8, 1.9), (.8, 7.4)], color=RED, lw=1.6); ax.text(.8, 7.6, "BL", ha="center", color=RED)
    wire(ax, [(9.2, 1.9), (9.2, 7.4)], color=RED, lw=1.6); ax.text(9.2, 7.6, "BL̄", ha="center", color=RED)
    wire(ax, [(.8, 6.8), (9.2, 6.8)], color=BLUE, lw=1.2); ax.text(5, 7.0, "WL (word line)", ha="center", color=BLUE, fontsize=8)
    # inverter 1 (top): Q -> Qbar ; inverter 2 (bottom): Qbar -> Q
    ax.add_patch(Polygon([(4.4, 5.0), (4.4, 3.8), (5.5, 4.4)], fill=False, lw=1.5)); ax.add_patch(Circle((5.58, 4.4), .08, fill=False))
    ax.add_patch(Polygon([(5.6, 3.2), (5.6, 2.0), (4.5, 2.6)], fill=False, lw=1.5)); ax.add_patch(Circle((4.42, 2.6), .08, fill=False))
    wire(ax, [(2.2, 3.4), (2.2, 4.4), (4.4, 4.4)]); wire(ax, [(5.66, 4.4), (7.8, 4.4), (7.8, 3.4)])
    wire(ax, [(7.8, 3.4), (7.8, 2.6), (5.6, 2.6)]); wire(ax, [(4.34, 2.6), (2.2, 2.6), (2.2, 3.4)])
    dot(ax, 2.2, 3.8); dot(ax, 7.8, 3.8)
    ax.text(2.0, 4.05, "Q", fontsize=9, fontweight="bold"); ax.text(7.85, 4.05, "Q̄", fontsize=9, fontweight="bold")
    wire(ax, [(.8, 3.8), (1.5, 3.8)]); wire(ax, [(1.5, 3.8), (2.2, 3.8)], lw=2.5, color=GREEN); ax.text(1.2, 3.2, "access\nnMOS", fontsize=7, color=GREEN)
    wire(ax, [(1.85, 3.8), (1.85, 6.8)], color=GREEN, lw=1)
    wire(ax, [(9.2, 3.8), (8.5, 3.8)]); wire(ax, [(8.5, 3.8), (7.8, 3.8)], lw=2.5, color=GREEN); wire(ax, [(8.15, 3.8), (8.15, 6.8)], color=GREEN, lw=1)
    ax.text(5, 1.2, "two cross-coupled inverters (4 T) hold the bit while power is on;\n2 access transistors connect it to the bit lines when WL = 1", ha="center", fontsize=8)
    ax = axs[1]; ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off"); ax.set_title("1T1C DRAM cell", fontweight="bold", fontsize=10)
    wire(ax, [(2, 2.2), (2, 7.4)], color=RED, lw=1.6); ax.text(2, 7.6, "BL", ha="center", color=RED)
    wire(ax, [(1, 6.2), (8, 6.2)], color=BLUE, lw=1.2); ax.text(7.2, 6.4, "WL", color=BLUE)
    wire(ax, [(2, 4.0), (4.3, 4.0)]); wire(ax, [(4.3, 4.0), (4.3, 4.6), (5.3, 4.6), (5.3, 4.0)], lw=1.4); wire(ax, [(4.4, 4.75), (5.2, 4.75)], lw=2)
    wire(ax, [(4.8, 4.75), (4.8, 6.2)]); dot(ax, 4.8, 6.2)
    wire(ax, [(5.3, 4.0), (6.5, 4.0), (6.5, 3.3)]); wire(ax, [(6.1, 3.3), (6.9, 3.3)], lw=2); wire(ax, [(6.1, 3.1), (6.9, 3.1)], lw=2); wire(ax, [(6.5, 3.1), (6.5, 2.4)]); gnd(ax, 6.5, 2.4)
    ax.text(7.1, 3.15, "C$_S$ (stores\ncharge = bit)", fontsize=8)
    ax.text(5, 1.0, "1 transistor + 1 capacitor ⇒ densest RAM;\ncharge leaks away ⇒ must be REFRESHED every few ms;\nreading is destructive (charge shared with C$_{BL}$)", ha="center", fontsize=8)
    save(fig, "sram_dram")


ALL2 = [fig_mos_regions, fig_mos_sce, fig_cmos_switch, fig_cmos_vtc, fig_cmos_gates, fig_dos_carriers, fig_n_vs_T,
        fig_continuity, fig_diode_gr, fig_diode_quadrants, fig_cv_profiling, fig_mos_bands, fig_bjt_profile, fig_cz,
        fig_deal_grove, fig_diffusion_profiles, fig_implant, fig_litho_resist, fig_nmos_flow, fig_spice_eqckt,
        fig_mem_array, fig_nor_rom, fig_sram_dram]

if __name__ == "__main__":
    for f in ALL2:
        r = f()
        print("ok", f.__name__, r if r is not None else "")
