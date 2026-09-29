"""Circuits B: BJT DC bias configurations and the BJT lab set-ups."""
from ckt import *


def rail(c, x1, x2, y, label="$V_{CC}$", term_x=None):
    c.wire((x1, y), (x2, y))
    tx = term_x if term_x is not None else (x1 + x2) / 2
    c.wire((tx, y), (tx, y + 0.45))
    c.term(tx, y + 0.45, label, "up")


def couple_in(c, x_from, y, x_to, label="$C_1$"):
    c.term(x_from, y, "$V_i$", "left")
    c.wire((x_from, y), (x_from + 0.7, y))
    c.cap((x_from + 0.7, y), (x_from + 1.9, y), label, side="up", polar=True)
    c.wire((x_from + 1.9, y), (x_to, y))


def out_tap(c, x, y, x_end=None, label="$C_2$"):
    x_end = x_end or x + 3.6
    c.dot(x, y)
    c.wire((x, y), (x + 0.8, y))
    c.cap((x + 0.8, y), (x + 2.0, y), label, side="up", polar=True)
    c.wire((x + 2.0, y), (x_end, y))
    c.term(x_end, y, "$V_o$", "right")


def fixed_bias(with_re=False, name="c_fixed_bias"):
    c = Ckt(10.5, 7.2)
    cx, cy = 6.0, 2.8
    t = c.bjt(cx, cy, "npn", label_b=None)
    Ry = 6.3
    rail(c, 4.2, cx + 0.25, Ry)
    c.dot(4.2, Ry) if False else None
    # RB
    c.res((4.2, Ry), (4.2, cy), "$R_B$", side="down" if False else "up")
    c.wire((4.2, cy), t["B"])
    c.dot(4.2, cy)
    couple_in(c, 0.3, cy, 4.2)
    # RC
    c.res((cx + 0.25, Ry), (cx + 0.25, t["C"][1]), "$R_C$", side="down")
    out_tap(c, cx + 0.25, 3.5) if False else None
    c.dot(cx + 0.25, 3.5)
    c.wire((cx + 0.25, 3.5), (cx + 1.0, 3.5)); c.cap((cx + 1.0, 3.5), (cx + 2.2, 3.5), "$C_2$", side="up", polar=True)
    c.wire((cx + 2.2, 3.5), (cx + 3.2, 3.5)); c.term(cx + 3.2, 3.5, "$V_o$", "right")
    if with_re:
        c.res(t["E"], (cx + 0.25, 0.5), "$R_E$", side="down")
        c.ground(cx + 0.25, 0.5)
    else:
        c.wire(t["E"], (cx + 0.25, 1.4)); c.ground(cx + 0.25, 1.4)
    c.text(3.55, 4.6, "$I_B$", size=10.5); c.arrow((3.85, 4.9), (3.85, 4.2), ms=8)
    c.text(6.85, 4.9, "$I_C$", size=10.5); c.arrow((7.05, 5.2), (7.05, 4.5), ms=8)
    c.save(name)


def voltage_divider():
    c = Ckt(10.5, 7.4)
    cx, cy = 6.4, 3.2
    t = c.bjt(cx, cy, "npn")
    Ry = 6.6
    rail(c, 4.3, cx + 0.25, Ry)
    c.res((4.3, Ry), (4.3, cy + 0.6), "$R_1$", side="down"); c.dot(4.3, cy)
    c.wire((4.3, cy + 0.6), (4.3, cy)); c.wire((4.3, cy), t["B"])
    c.res((4.3, cy), (4.3, 0.9), "$R_2$", side="down"); c.ground(4.3, 0.9) if False else None
    c.wire((4.3, 0.9), (4.3, 0.5)); c.ground(4.3, 0.5)
    couple_in(c, 0.3, cy, 4.3)
    c.res((cx + 0.25, Ry), (cx + 0.25, t["C"][1]), "$R_C$", side="down")
    c.dot(cx + 0.25, 3.9)
    c.wire((cx + 0.25, 3.9), (cx + 1.0, 3.9)); c.cap((cx + 1.0, 3.9), (cx + 2.2, 3.9), "$C_2$", side="up", polar=True)
    c.wire((cx + 2.2, 3.9), (cx + 3.2, 3.9)); c.term(cx + 3.2, 3.9, "$V_o$", "right")
    c.res(t["E"], (cx + 0.25, 0.9), "$R_E$", side="down"); c.wire((cx + 0.25, 0.9), (cx + 0.25, 0.5)); c.ground(cx + 0.25, 0.5)
    c.text(4.85, 5.0, "$I_1$", size=10.5); c.text(4.85, 1.9, "$I_2$", size=10.5)
    c.save("c_vdiv")


def thevenin():
    c = Ckt(9.5, 5.6)
    # left: the divider being reduced
    c.text(1.8, 5.3, "Step 1: the divider", size=9.5, weight="bold")
    c.term(0.6, 4.4, "$V_{CC}$", "up"); c.wire((0.6, 4.4), (0.6, 3.9))
    c.res((0.6, 3.9), (0.6, 2.5), "$R_1$", side="down")
    c.dot(0.6, 2.5)
    c.wire((0.6, 2.5), (2.6, 2.5)); c.term(2.6, 2.5, "B", "right")
    c.res((0.6, 2.5), (0.6, 0.9), "$R_2$", side="down"); c.wire((0.6, 0.9), (0.6, 0.5)); c.ground(0.6, 0.5)
    # right: Thevenin equivalent driving the base
    c.text(6.4, 5.3, "Step 2: $E_{Th}$ and $R_{Th}$", size=9.5, weight="bold")
    c.wire((5.0, 2.5), (5.4, 2.5)); c.res((5.0, 2.5), (6.9, 2.5), "$R_{Th}$", side="up")
    c.wire((5.0, 2.5), (5.0, 2.5))
    c.battery((4.3, 0.9), (4.3, 2.5), label="$E_{Th}$", side="up", plus_at_end=True)
    c.wire((4.3, 2.5), (5.0, 2.5)); c.wire((4.3, 0.9), (4.3, 0.5)); c.ground(4.3, 0.5)
    c.wire((6.9, 2.5), (7.6, 2.5)); c.term(7.6, 2.5, "B", "right")
    c.save("c_thevenin")


def collector_feedback():
    c = Ckt(10.5, 7.4)
    cx, cy = 6.4, 2.6
    t = c.bjt(cx, cy, "npn")
    Ry = 6.8
    rail(c, cx + 0.25, cx + 0.25, Ry)
    c.res((cx + 0.25, Ry), (cx + 0.25, 4.6), "$R_C$", side="down")
    c.dot(cx + 0.25, 4.3); c.wire((cx + 0.25, 4.6), (cx + 0.25, t["C"][1]))
    c.wire((cx + 0.25, 4.3), (4.2, 4.3)); c.res((4.2, 4.3), (4.2, cy), "$R_F$", side="up")
    c.dot(4.2, cy); c.wire((4.2, cy), t["B"])
    couple_in(c, 0.3, cy, 4.2)
    c.dot(cx + 0.25, 3.7) if False else None
    c.wire((cx + 0.25, 4.3), (cx + 1.0, 4.3)); c.cap((cx + 1.0, 4.3), (cx + 2.2, 4.3), "$C_2$", side="up", polar=True)
    c.wire((cx + 2.2, 4.3), (cx + 3.2, 4.3)); c.term(cx + 3.2, 4.3, "$V_o$", "right")
    c.res(t["E"], (cx + 0.25, 0.4), "$R_E$", side="down") if False else None
    c.wire(t["E"], (cx + 0.25, 1.2)); c.res((cx + 0.25, 1.6), (cx + 0.25, 0.6), "$R_E$", side="down") if False else None
    c.res(t["E"], (cx + 0.25, 0.6), "$R_E$", side="down"); c.ground(cx + 0.25, 0.6)
    c.text(5.2, 4.65, "$I_C'$", size=10.5)
    c.save("c_coll_fb")


def emitter_follower():
    c = Ckt(10.5, 7.0)
    cx, cy = 6.0, 3.6
    t = c.bjt(cx, cy, "npn")
    c.wire(t["C"], (cx + 0.25, 5.8)); c.term(cx + 0.25, 5.8, "0 V (ground)", "up") if False else None
    c.wire(t["C"], (cx + 0.25, 5.3)); c.ground(cx + 0.25, 5.3) if False else None
    c.text(cx + 0.9, 5.2, "collector at 0 V", size=9.5, ha="left")
    c.ground(cx + 0.25, 5.4) if False else None
    # ground at collector: draw a ground symbol above (inverted)
    c.wire((cx + 0.25, 4.6), (cx + 0.25, 5.4))
    for i, wd in enumerate([0.32, 0.2, 0.08]):
        c.line((cx + 0.25 - wd, 5.4 + i * 0.09), (cx + 0.25 + wd, 5.4 + i * 0.09), lw=1.5)
    # RB to ground
    c.wire(t["B"], (4.0, cy)); c.dot(4.0, cy)
    c.res((4.0, cy), (4.0, 1.6), "$R_B$", side="down"); c.wire((4.0, 1.6), (4.0, 1.2)); c.ground(4.0, 1.2)
    couple_in(c, 0.3, cy, 4.0)
    # emitter
    c.dot(cx + 0.25, 2.2)
    c.res((cx + 0.25, 2.6), (cx + 0.25, 0.9), "$R_E$", side="down") if False else None
    c.wire(t["E"], (cx + 0.25, 2.6))
    c.wire((cx + 0.25, 2.6), (cx + 0.25, 2.3)) if False else None
    c.res((cx + 0.25, 2.6), (cx + 0.25, 0.9), "$R_E$", side="down")
    c.wire((cx + 0.25, 0.9), (cx + 0.25, 0.4)); c.term(cx + 0.25, 0.4, "$-V_{EE}$", "down")
    c.dot(cx + 0.25, 2.6)
    c.wire((cx + 0.25, 2.6), (cx + 1.0, 2.6)); c.cap((cx + 1.0, 2.6), (cx + 2.2, 2.6), "$C_2$", side="up", polar=True)
    c.wire((cx + 2.2, 2.6), (cx + 3.2, 2.6)); c.term(cx + 3.2, 2.6, "$V_o$", "right")
    c.save("c_emitter_follower")


def common_base():
    c = Ckt(11.5, 7.2)
    cx, cy = 5.4, 3.4
    t = c.bjt(cx, cy, "npn")
    # base grounded
    c.wire(t["B"], (t["B"][0] - 0.4, cy)); c.wire((t["B"][0] - 0.4, cy), (t["B"][0] - 0.4, cy - 0.5)); c.ground(t["B"][0] - 0.4, cy - 0.5)
    # emitter
    c.wire(t["E"], (cx + 0.25, 1.9)); c.dot(cx + 0.25, 1.9)
    c.res((cx + 0.25, 1.9), (cx + 0.25, 0.7), "$R_E$", side="down") if False else None
    c.res((cx + 0.25, 1.9), (cx + 0.25, 0.7), "$R_E$", side="down")
    c.wire((cx + 0.25, 0.7), (cx + 0.25, 0.3)); c.wire((cx + 0.25, 0.3), (3.4, 0.3))
    c.battery((3.4, 0.3), (1.8, 0.3), label="$V_{EE}$", side="down", plus_at_end=True)
    c.wire((1.8, 0.3), (1.4, 0.3)); c.wire((1.4, 0.3), (1.4, 0.0)); c.ground(1.4, 0.0) if False else None
    c.ground(1.4, 0.3)
    # input coupling to emitter
    c.term(0.3, 1.9, "$V_i$", "left"); c.wire((0.3, 1.9), (0.9, 1.9)); c.cap((0.9, 1.9), (2.1, 1.9), "$C_1$", side="up", polar=True)
    c.wire((2.1, 1.9), (cx + 0.25, 1.9))
    # collector
    c.res((cx + 0.25, 6.2), (cx + 0.25, t["C"][1]), "$R_C$", side="down")
    c.wire((cx + 0.25, 6.2), (9.6, 6.2)); c.battery((9.6, 6.2), (9.6, 4.6), label="$V_{CC}$", side="up", plus_at_end=False)
    c.wire((9.6, 4.6), (9.6, 4.2)); c.ground(9.6, 4.2)
    c.dot(cx + 0.25, 4.7); c.wire((cx + 0.25, 4.7), (cx + 1.0, 4.7)); c.cap((cx + 1.0, 4.7), (cx + 2.2, 4.7), "$C_2$", side="up", polar=True)
    c.wire((cx + 2.2, 4.7), (cx + 2.9, 4.7)); c.term(cx + 2.9, 4.7, "$V_o$", "right")
    c.save("c_common_base")


def lab_ce_bc547():
    """Input/output characteristics test bench (your two lab figures)."""
    c = Ckt(12.5, 7.4)
    cx, cy = 6.8, 3.4
    t = c.bjt(cx, cy, "npn")
    c.text(cx - 0.3, cy - 1.45, "BC547", size=10, color="#1f5fbf", ha="center")
    # input loop: VBB - RB - uA - base ; emitter to ground
    c.battery((0.9, 1.0), (0.9, 3.6), label="$V_{BB}$", side="down", plus_at_end=True)
    c.wire((0.9, 3.6), (0.9, cy)); c.wire((0.9, cy), (1.4, cy))
    c.res((1.4, cy), (3.0, cy), "$R_B$=100 k", side="up")
    c.wire((3.0, cy), (3.6, cy))
    # microammeter
    c.ax.add_patch(Circle((4.3, cy), 0.55, fc="white", ec=INK, lw=LW, zorder=4)); c.text(4.3, cy, "µA", size=10)
    c.wire((3.6, cy), (3.75, cy)); c.wire((4.85, cy), t["B"])
    c.dot(5.45, cy)
    # VBE voltmeter between base node and ground
    c.wire((5.45, cy), (5.45, 1.9)); c.ax.add_patch(Circle((5.45, 1.35), 0.5, fc="white", ec=INK, lw=LW, zorder=4)); c.text(5.45, 1.35, "V", size=11)
    c.wire((5.45, 0.85), (5.45, 0.4))
    c.text(4.75, 1.4, "$V_{BE}$", size=10, ha="right")
    # ground rail
    c.wire((0.9, 1.0), (0.9, 0.4), (11.2, 0.4)); c.wire(t["E"], (cx + 0.25, 0.4)); c.dot(cx + 0.25, 0.4); c.dot(5.45, 0.4)
    # collector loop: mA meter, RC, VCC
    c.wire(t["C"], (cx + 0.25, 5.6)); c.ax.add_patch(Circle((cx + 0.25 + 1.0, 5.6), 0.0)) if False else None
    c.wire((cx + 0.25, 5.6), (7.9, 5.6)); c.ax.add_patch(Circle((8.5, 5.6), 0.55, fc="white", ec=INK, lw=LW, zorder=4)); c.text(8.5, 5.6, "mA", size=10)
    c.wire((9.05, 5.6), (9.4, 5.6)); c.res((9.4, 5.6), (10.9, 5.6), "$R_C$=1 k", side="up"); c.wire((10.9, 5.6), (11.2, 5.6))
    c.battery((11.2, 0.4), (11.2, 5.6), label="$V_{CC}$", side="up", plus_at_end=True) if False else None
    c.wire((11.2, 5.6), (11.2, 4.2)); c.battery((11.2, 4.2), (11.2, 1.8), label="$V_{CC}$", side="up", plus_at_end=False)
    c.wire((11.2, 1.8), (11.2, 0.4))
    # VCE voltmeter from collector node to ground
    c.dot(cx + 0.25, 4.7); c.wire((cx + 0.25, 4.7), (8.9, 4.7)); c.wire((8.9, 4.7), (8.9, 3.9)); c.ax.add_patch(Circle((8.9, 3.3), 0.5, fc="white", ec=INK, lw=LW, zorder=4)); c.text(8.9, 3.3, "V", size=11)
    c.wire((8.9, 2.8), (8.9, 0.4)); c.dot(8.9, 0.4)
    c.text(9.55, 3.3, "$V_{CE}$", size=10, ha="left")
    c.save("c_lab_bc547")


def run_all():
    fixed_bias(False, "c_fixed_bias"); fixed_bias(True, "c_emitter_bias"); voltage_divider(); thevenin()
    collector_feedback(); emitter_follower(); common_base(); lab_ce_bc547()


if __name__ == "__main__":
    run_all(); print("ok")
