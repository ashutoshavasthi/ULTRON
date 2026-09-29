"""Circuits A: diodes, regulators, LED, rectifiers, filters."""
from ckt import *


def vdim(c, x, y1, y2, label, side="right", size=11):
    """vertical voltage dimension arrow with label"""
    c.arrow((x, y1), (x, y2), style="<|-|>", ms=9, lw=1.2)
    off = 0.32 if side == "right" else -0.32
    c.text(x + off, (y1 + y2) / 2, label, ha="left" if side == "right" else "right", size=size)


def diode_series():
    c = Ckt(8, 5)
    c.battery((1, 0.7), (1, 3.7), label="$V_S$", side="down", plus_at_end=True)
    c.wire((1, 3.7), (1, 4.2), (2, 4.2))
    c.res((2, 4.2), (5, 4.2), "$R$")
    c.wire((5, 4.2), (6.5, 4.2))
    c.diode((6.5, 4.2), (6.5, 0.7), "D", side="down")
    c.wire((6.5, 0.7), (6.5, 0.2), (1, 0.2), (1, 0.7))
    c.arrow((3.2, 3.55), (4.6, 3.55), ms=9)
    c.text(3.9, 3.2, "$I$", size=11)
    c.text(0.3, 2.2, "+", size=12); c.text(0.3, 1.3, "−", size=12)
    c.save("c_diode_series")


def diode_models():
    for nm, kind in (("c_diode_m1", 1), ("c_diode_m2", 2), ("c_diode_m3", 3)):
        c = Ckt(8, 2.0, pad=0.3)
        c.term(0.3, 1.0, "A", "left"); c.term(7.7, 1.0, "K", "right")
        if kind == 1:
            c.wire((0.3, 1.0), (1.4, 1.0)); c.battery((1.4, 1.0), (3.2, 1.0), label="$V_\\gamma$", side="up", plus_at_end=True)
            c.wire((3.2, 1.0), (3.8, 1.0)); c.res((3.8, 1.0), (6.4, 1.0), "$R_f$"); c.wire((6.4, 1.0), (7.7, 1.0))
        elif kind == 2:
            c.wire((0.3, 1.0), (2.4, 1.0)); c.battery((2.4, 1.0), (4.4, 1.0), label="$V_\\gamma$", side="up", plus_at_end=True)
            c.wire((4.4, 1.0), (7.7, 1.0))
        else:
            c.wire((0.3, 1.0), (7.7, 1.0)); c.text(4.0, 1.5, "ideal switch (closed)", size=10)
        c.save(nm)


def zener_reg(load=True):
    c = Ckt(9, 5.2)
    c.term(0.3, 4.2, "$V_{in}$", "left")
    c.wire((0.3, 4.2), (1.2, 4.2)); c.res((1.2, 4.2), (3.6, 4.2), "$R_S$"); c.wire((3.6, 4.2), (5.0, 4.2))
    c.dot(5.0, 4.2)
    c.zener((5.0, 0.9), (5.0, 4.2), "$V_Z$", side="down")   # anode at bottom, cathode at top
    c.wire((5.0, 0.9), (5.0, 0.4)); c.ground(5.0, 0.4)
    if load:
        c.wire((5.0, 4.2), (7.0, 4.2)); c.dot(7.0, 4.2)
        c.res((7.0, 4.2), (7.0, 0.9), "$R_L$", side="down")
        c.wire((7.0, 0.9), (7.0, 0.4)); c.ground(7.0, 0.4)
        c.wire((7.0, 4.2), (8.3, 4.2)); c.term(8.3, 4.2, "$V_{out}$", "right")
        c.arrow((5.9, 3.5), (5.9, 3.5))
    else:
        c.wire((5.0, 4.2), (8.3, 4.2)); c.term(8.3, 4.2, "$V_{out}$", "right")
    c.arrow((1.6, 3.6), (3.2, 3.6), ms=9); c.text(2.4, 3.3, "$I$", size=11)
    c.save("c_zener_reg_load" if load else "c_zener_reg")


def led_circuit():
    c = Ckt(8, 5)
    c.battery((1, 0.7), (1, 3.7), label="$V_S$", side="down", plus_at_end=True)
    c.wire((1, 3.7), (1, 4.2), (2, 4.2)); c.res((2, 4.2), (4.6, 4.2), "$R_S$")
    c.wire((4.6, 4.2), (6.5, 4.2))
    c.led((6.5, 4.2), (6.5, 0.7), "LED", side="down")
    c.wire((6.5, 0.7), (6.5, 0.2), (1, 0.2), (1, 0.7))
    c.text(3.3, 3.45, "$R_S=\\dfrac{V_S-V_F}{I_F}$", size=11)
    c.save("c_led")


def hwr():
    c = Ckt(10, 5.2)
    c.acsrc((1, 0.8), (1, 3.9), label="$V_i$", side="down")
    c.wire((1, 3.9), (1, 4.3), (2.4, 4.3)); c.diode((2.4, 4.3), (4.6, 4.3), "D", side="up")
    c.wire((4.6, 4.3), (6.6, 4.3)); c.dot(6.6, 4.3)
    c.res((6.6, 4.3), (6.6, 0.8), "$R_L$", side="down")
    c.wire((6.6, 0.8), (6.6, 0.3), (1, 0.3), (1, 0.8))
    c.wire((6.6, 4.3), (8.4, 4.3)); c.term(8.4, 4.3, "+", "right")
    c.wire((6.6, 0.3), (8.4, 0.3)); c.term(8.4, 0.3, "−", "right")
    vdim(c, 7.7, 0.5, 4.1, "$V_o$")
    c.arrow((3.2, 3.6), (4.2, 3.6), ms=9); c.text(3.7, 3.25, "$i$", size=11)
    c.save("c_hwr")


def ct_fwr():
    c = Ckt(11, 6)
    c.acsrc((0.7, 0.9), (0.7, 4.7), label="AC", side="down")
    c.wire((0.7, 4.7), (0.7, 5.1), (1.9, 5.1)); c.wire((0.7, 0.9), (0.7, 0.5), (1.9, 0.5))
    c.ind((1.9, 5.1), (1.9, 0.5), body=4.0)
    c.line((2.9, 0.9), (2.9, 4.7)); c.line((3.1, 0.9), (3.1, 4.7))
    c.ind((4.1, 5.1), (4.1, 0.5), body=4.0)
    # secondary arcs bulge to the right for direction of travel downward
    c.wire((4.1, 5.1), (4.9, 5.1)); c.diode((4.9, 5.1), (7.1, 5.1), "$D_1$", side="up"); c.wire((7.1, 5.1), (8.3, 5.1))
    c.wire((4.1, 0.5), (4.9, 0.5)); c.diode((4.9, 0.5), (7.1, 0.5), "$D_2$", side="down"); c.wire((7.1, 0.5), (8.3, 0.5))
    c.wire((8.3, 5.1), (8.3, 0.5)); c.dot(8.3, 2.8)
    c.wire((8.3, 2.8), (9.4, 2.8))
    c.res((9.4, 2.8), (9.4, 2.8))  # placeholder no-op
    c.save("c_ct_fwr_x")


def ct_fwr2():
    c = Ckt(11, 6.2)
    c.acsrc((0.7, 1.0), (0.7, 4.6), label="AC", side="down")
    c.wire((0.7, 4.6), (0.7, 5.0), (1.8, 5.0)); c.wire((0.7, 1.0), (0.7, 0.6), (1.8, 0.6))
    c.ind((1.8, 5.0), (1.8, 0.6), body=3.8)
    c.line((2.75, 0.9), (2.75, 4.7)); c.line((2.95, 0.9), (2.95, 4.7))
    c.ind((3.9, 5.0), (3.9, 0.6), body=3.8)
    c.wire((3.9, 5.0), (4.6, 5.0)); c.diode((4.6, 5.0), (6.8, 5.0), "$D_1$", side="up"); c.wire((6.8, 5.0), (8.2, 5.0))
    c.wire((3.9, 0.6), (4.6, 0.6)); c.diode((4.6, 0.6), (6.8, 0.6), "$D_2$", side="down"); c.wire((6.8, 0.6), (8.2, 0.6))
    c.wire((8.2, 5.0), (8.2, 0.6)); c.dot(8.2, 2.8)
    # load: from cathode rail (8.2, 2.8) horizontally to the centre tap
    c.wire((8.2, 2.8), (7.7, 2.8)); c.res((7.7, 2.8), (5.0, 2.8), "$R_L$", side="up"); c.wire((5.0, 2.8), (4.55, 2.8))
    c.dot(4.55, 2.8); c.wire((4.55, 2.8), (4.55, 2.35)); c.ground(4.55, 2.35)
    c.text(5.4, 2.15, "centre tap (0 V)", size=9.5)
    c.save("c_ct_fwr")


def bridge():
    c = Ckt(10, 6)
    c.acsrc((0.9, 1.0), (0.9, 4.6), label="AC", side="down")
    T, R, B, L = (4.6, 5.0), (7.2, 2.8), (4.6, 0.6), (2.0, 2.8)
    c.wire((0.9, 4.6), (0.9, 5.0), T); c.wire((0.9, 1.0), (0.9, 0.6), B)
    c.diode(T, R, "$D_1$", side="up"); c.diode(B, R, "$D_2$", side="down")
    c.diode(L, T, "$D_3$", side="up"); c.diode(L, B, "$D_4$", side="down")
    c.dot(*T); c.dot(*B); c.dot(*R); c.dot(*L)
    # load across the middle (R = +, L = -)
    c.wire(R, (6.2, 2.8)); c.res((6.2, 2.8), (3.0, 2.8), "$R_L$", side="up"); c.wire((3.0, 2.8), L)
    c.text(7.75, 3.15, "+", size=13, ha="left"); c.text(1.55, 3.15, "−", size=13, ha="right")
    c.save("c_bridge")


def filt(name, kind):
    c = Ckt(11, 4.3, pad=1.4)
    c.term(0.3, 3.4, "rectifier\noutput", "left", size=9.5)
    c.term(0.3, 0.5, None)
    x = 1.0
    c.wire((0.3, 3.4), (1.0, 3.4))
    if kind == "L":
        c.ind((1.0, 3.4), (4.2, 3.4), "L"); x = 4.2
    elif kind == "C":
        c.wire((1.0, 3.4), (2.0, 3.4)); c.dot(2.0, 3.4); c.cap((2.0, 3.4), (2.0, 0.5), "$C$", side="down"); c.dot(2.0, 0.5); x = 2.0
        c.wire((2.0, 3.4), (5.0, 3.4)); x = 5.0
    elif kind == "LC":
        c.ind((1.0, 3.4), (3.6, 3.4), "L"); c.dot(3.6, 3.4); c.cap((3.6, 3.4), (3.6, 0.5), "$C$", side="down"); c.dot(3.6, 0.5)
        c.wire((3.6, 3.4), (5.4, 3.4)); x = 5.4
    elif kind == "pi":
        c.wire((1.0, 3.4), (1.8, 3.4)); c.dot(1.8, 3.4); c.cap((1.8, 3.4), (1.8, 0.5), "$C_1$", side="down"); c.dot(1.8, 0.5)
        c.ind((1.8, 3.4), (4.6, 3.4), "L"); c.dot(4.6, 3.4); c.cap((4.6, 3.4), (4.6, 0.5), "$C_2$", side="down"); c.dot(4.6, 0.5)
        c.wire((4.6, 3.4), (6.2, 3.4)); x = 6.2
    c.dot(x, 3.4)
    c.res((x, 3.4), (x, 0.5), "$R_L$", side="down"); c.dot(x, 0.5)
    c.wire((x, 3.4), (x + 1.4, 3.4)); c.term(x + 1.4, 3.4, "+", "right")
    c.term(x + 1.4, 0.5, "−", "right"); c.wire((0.3, 0.5), (x + 1.4, 0.5))
    c.save(name)


def run_all():
    diode_series(); diode_models(); zener_reg(True); zener_reg(False); led_circuit(); hwr(); ct_fwr2(); bridge()
    filt("c_filter_l", "L"); filt("c_filter_c", "C"); filt("c_filter_lc", "LC"); filt("c_filter_pi", "pi")


if __name__ == "__main__":
    run_all()
    print("ok")
