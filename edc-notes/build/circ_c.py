"""Circuits C: small-signal (re / hybrid) models, thyristors, UJT, special diodes."""
from ckt import *


def tb(c, x, y, s, **k):
    c.text(x, y, s, **k)


def shunt(c, kind, x, ytop, ybot, label, side="down"):
    if kind == "R":
        c.res((x, ytop), (x, ybot), label, side=side)
    elif kind == "I":
        c.isrc((x, ytop), (x, ybot), label, side=side, dependent=True)
    c.dot(x, ytop); c.dot(x, ybot)


def re_model_ce():
    c = Ckt(9, 4.8)
    top, bot = 3.7, 0.8
    c.term(0.4, top, "b", "left"); c.wire((0.4, top), (6.9, top)); c.term(6.9, top, "c", "right")
    c.term(0.4, bot, "e", "left"); c.wire((0.4, bot), (6.9, bot)); c.term(6.9, bot, "e", "right")
    shunt(c, "R", 1.9, top, bot, "$\\beta r_e$", side="down")
    shunt(c, "I", 3.9, top, bot, "$\\beta I_b$", side="down")
    shunt(c, "R", 5.7, top, bot, "$r_o$", side="down")
    c.arrow((0.9, 4.2), (1.5, 4.2), ms=9); c.text(1.2, 4.5, "$I_b$", size=10)
    c.arrow((6.35, 3.3), (6.35, 2.7), ms=9) if False else None
    c.save("c_re_model_ce")


def re_model_diode():
    c = Ckt(9, 4.8)
    top, bot = 3.7, 0.8
    c.term(0.4, top, "b", "left"); c.wire((0.4, top), (6.4, top)); c.term(6.4, top, "c", "right")
    c.term(0.4, bot, "e", "left"); c.wire((0.4, bot), (6.4, bot)); c.term(6.4, bot, "e", "right")
    c.diode((1.9, top), (1.9, bot), "$r_e$", side="down"); c.dot(1.9, top); c.dot(1.9, bot)
    c.isrc((4.2, top), (4.2, bot), "$\\beta I_b$", side="down", dependent=True); c.dot(4.2, top); c.dot(4.2, bot)
    c.arrow((0.8, 4.2), (1.5, 4.2), ms=9); c.text(1.15, 4.5, "$I_b$", size=10)
    c.arrow((2.6, 2.95), (2.6, 2.35), ms=9); c.text(3.0, 2.65, "$I_e$", size=10)
    c.save("c_re_model_diode")


def re_model_cb():
    c = Ckt(9, 4.8)
    top, bot = 3.7, 0.8
    c.term(0.4, top, "e", "left"); c.wire((0.4, top), (6.9, top)); c.term(6.9, top, "c", "right")
    c.term(0.4, bot, "b", "left"); c.wire((0.4, bot), (6.9, bot)); c.term(6.9, bot, "b", "right")
    shunt(c, "R", 1.9, top, bot, "$r_e$", side="down")
    c.isrc((3.9, bot), (3.9, top), "$\\alpha I_e$", side="down", dependent=True); c.dot(3.9, top); c.dot(3.9, bot)
    shunt(c, "R", 5.7, top, bot, "$r_o$", side="down")
    c.arrow((0.9, 4.2), (1.5, 4.2), ms=9); c.text(1.2, 4.5, "$I_e$", size=10)
    c.save("c_re_model_cb")


def ac_fixed():
    c = Ckt(12, 5.0)
    top, bot = 3.8, 0.8
    c.term(0.3, top, "$V_i$", "left"); c.wire((0.3, top), (10.2, top)); c.wire((0.3, bot), (10.2, bot)); c.term(0.3, bot, None)
    shunt(c, "R", 1.6, top, bot, "$R_B$"); shunt(c, "R", 3.1, top, bot, "$\\beta r_e$")
    shunt(c, "I", 5.0, top, bot, "$\\beta I_b$"); shunt(c, "R", 6.6, top, bot, "$r_o$"); shunt(c, "R", 8.2, top, bot, "$R_C$")
    c.term(10.2, top, "$V_o$", "right")
    c.arrow((0.8, 4.3), (1.3, 4.3), ms=9); c.text(1.05, 4.62, "$I_i$", size=10)
    c.arrow((2.5, 4.25), (3.0, 4.25), ms=9); c.text(2.75, 4.6, "$I_b$", size=10)
    c.line((2.2, 4.9), (2.2, 0.3), ls="--", lw=1.0, color="#7a86a0"); c.text(1.1, 0.25, "$Z_i$ →", size=10)
    c.line((9.2, 4.9), (9.2, 0.3), ls="--", lw=1.0, color="#7a86a0"); c.text(9.7, 0.25, "← $Z_o$", size=10)
    c.save("c_ac_fixed")


def ac_unbypassed():
    c = Ckt(11.5, 5.6)
    top, bot = 4.3, 0.6
    c.term(0.3, top, "$V_i$", "left"); c.wire((0.3, top), (10.0, top)); c.wire((0.3, bot), (10.0, bot)); c.term(0.3, bot, None)
    shunt(c, "R", 1.6, top, bot, "$R_B$")
    # beta*re from base node to E' ; RE from E' to ground
    c.res((3.4, top), (3.4, 2.5), "$\\beta r_e$", side="down"); c.dot(3.4, top); c.dot(3.4, 2.5)
    c.res((3.4, 2.5), (3.4, bot), "$R_E$", side="down"); c.dot(3.4, bot)
    # source from collector node down to E'
    c.isrc((5.6, top), (5.6, 2.5), "$\\beta I_b$", side="up", dependent=True); c.dot(5.6, top); c.wire((5.6, 2.5), (3.4, 2.5))
    shunt(c, "R", 8.0, top, bot, "$R_C$"); c.term(10.0, top, "$V_o$", "right")
    c.arrow((0.9, 4.75), (1.4, 4.75), ms=9); c.text(1.15, 5.05, "$I_i$", size=10)
    c.arrow((2.4, 4.75), (3.2, 4.75), ms=9); c.text(2.8, 5.05, "$I_b$", size=10)
    c.text(4.6, 1.95, "$I_e=(\\beta+1)I_b$", size=10, ha="left") if False else c.text(4.15, 1.7, "$I_e=(\\beta+1)I_b$\nflows through $R_E$", size=9.5, ha="left")
    c.save("c_ac_unbypassed")


def ac_follower():
    c = Ckt(11.5, 5.6)
    top, bot = 4.3, 0.6
    c.term(0.3, top, "$V_i$", "left"); c.wire((0.3, top), (3.6, top)); c.wire((0.3, bot), (9.0, bot)); c.term(0.3, bot, None)
    shunt(c, "R", 1.6, top, bot, "$R_B$")
    c.res((3.6, top), (3.6, 2.6), "$\\beta r_e$", side="down"); c.dot(3.6, top); c.dot(3.6, 2.6)
    c.res((3.6, 2.6), (3.6, bot), "$R_E$", side="down"); c.dot(3.6, bot)
    c.isrc((6.0, bot), (6.0, 2.6), "$\\beta I_b$", side="up", dependent=True); c.wire((6.0, 2.6), (3.6, 2.6)); c.dot(6.0, bot)
    c.wire((6.0, 2.6), (9.0, 2.6)); c.term(9.0, 2.6, "$V_o$", "right"); c.dot(6.0, 2.6)
    c.text(6.9, 3.6, "collector = ac ground\n(that is why it is called\nCOMMON collector)", size=9, ha="left")
    c.arrow((2.3, 4.75), (3.4, 4.75), ms=9); c.text(2.85, 5.05, "$I_b$", size=10)
    c.save("c_ac_follower")


def ac_collfb():
    c = Ckt(13, 5.2)
    top, bot = 3.8, 0.8
    c.term(0.3, top, "$V_i$", "left"); c.wire((0.3, top), (11.2, top)); c.wire((0.3, bot), (11.2, bot)); c.term(0.3, bot, None)
    shunt(c, "R", 1.6, top, bot, "$R_{F1}$"); shunt(c, "R", 3.3, top, bot, "$\\beta r_e$")
    shunt(c, "I", 5.2, top, bot, "$\\beta I_b$"); shunt(c, "R", 6.9, top, bot, "$r_o$")
    shunt(c, "R", 8.5, top, bot, "$R_{F2}$"); shunt(c, "R", 10.1, top, bot, "$R_C$")
    c.term(11.2, top, "$V_o$", "right")
    c.arrow((0.8, 4.3), (1.3, 4.3), ms=9); c.text(1.05, 4.62, "$I_i$", size=10)
    c.arrow((2.6, 4.25), (3.1, 4.25), ms=9); c.text(2.85, 4.6, "$I_b$", size=10)
    c.save("c_ac_collfb")


def hybrid():
    c = Ckt(10.5, 5.0)
    top, bot = 3.8, 0.8
    c.term(0.3, top, "$V_i$", "left"); c.term(0.3, bot, None)
    c.wire((0.3, top), (1.0, top)); c.res((1.0, top), (3.2, top), "$h_{ie}$", side="up"); c.wire((3.2, top), (3.6, top))
    c.dot(3.6, top); c.dot(3.6, bot)
    c.wire((0.3, bot), (9.4, bot))
    # dependent voltage source h_re V_o (vertical)
    pts = [(3.6, 2.9), (4.2, 2.3), (3.6, 1.7), (3.0, 2.3)]
    c.wire((3.6, top), (3.6, 2.9)); c.ax.add_patch(Polygon(pts, fc="white", ec=INK, lw=LW, zorder=4))
    c.text(3.6, 2.3, "+", size=10); c.wire((3.6, 1.7), (3.6, bot)) if False else c.wire((3.6, 1.7), (3.6, bot))
    c.text(2.75, 2.3, "$h_{re}V_o$", size=10, ha="right")
    c.wire((3.6, top), (9.4, top)); c.term(9.4, top, "$V_o$", "right"); c.term(9.4, bot, None)
    shunt(c, "I", 5.6, top, bot, "$h_{fe}I_i$"); shunt(c, "R", 7.6, top, bot, "$1/h_{oe}$")
    c.arrow((0.8, 4.3), (1.6, 4.3), ms=9); c.text(1.2, 4.62, "$I_i$", size=10)
    c.arrow((8.6, 4.3), (9.1, 4.3), ms=9) if False else None
    c.save("c_hybrid")


def scr_symbol():
    c = Ckt(6, 5.2)
    c.term(2.0, 4.9, "Anode (A)", "right") if False else None
    c.wire((2.0, 4.9), (2.0, 4.1)); c.term(2.0, 4.9, "A", "up")
    c.diode((2.0, 4.1), (2.0, 1.1), None)
    c.wire((2.0, 1.1), (2.0, 0.3)); c.term(2.0, 0.3, "K", "down")
    c.wire((0.4, 1.6), (1.2, 1.6)); c.line((1.2, 1.6), (2.0, 1.95)); c.term(0.4, 1.6, "G", "left")
    c.text(3.4, 4.1, "Anode", size=9.5, ha="left"); c.text(3.4, 0.3, "Cathode", size=9.5, ha="left")
    c.save("c_scr_symbol")


def scr_two_transistor():
    c = Ckt(9, 7.0)
    # PNP top (emitter = anode), NPN bottom
    p = c.bjt(3.6, 4.7, "pnp", label_b=None)
    n = c.bjt(3.6, 2.0, "npn")
    # Tr1 emitter is TOP for the pnp symbol we want: swap by mirroring - approximate by labels
    c.text(5.2, 4.7, "$Tr_1$ (PNP)", size=10, ha="left"); c.text(5.2, 2.0, "$Tr_2$ (NPN)", size=10, ha="left")
    c.save("c_scr_two_try")


def triac_diac():
    for nm, gate in (("c_triac_symbol", True), ("c_diac_symbol", False)):
        c = Ckt(6, 5.2)
        c.wire((2.6, 4.9), (2.6, 4.4)); c.term(2.6, 4.9, "$MT_2$", "up")
        c.wire((2.6, 0.3), (2.6, 0.8)); c.term(2.6, 0.3, "$MT_1$", "down")
        c.wire((1.9, 4.4), (3.3, 4.4)); c.wire((1.9, 0.8), (3.3, 0.8))
        c.diode((1.9, 4.4), (1.9, 0.8)); c.diode((3.3, 0.8), (3.3, 4.4))
        if gate:
            c.wire((0.4, 1.4), (1.1, 1.4)); c.line((1.1, 1.4), (1.9, 1.7)) if False else None
            c.wire((1.1, 1.4), (1.9, 1.4)); c.term(0.4, 1.4, "G", "left")
        c.save(nm)


def ujt_symbol():
    c = Ckt(5, 5)
    c.line((2.6, 1.2), (2.6, 3.8), lw=3.4)
    c.wire((2.6, 3.8), (2.6, 4.6)); c.term(2.6, 4.6, "$B_2$", "up")
    c.wire((2.6, 1.2), (2.6, 0.4)); c.term(2.6, 0.4, "$B_1$", "down")
    c.wire((0.4, 2.9), (1.6, 2.9)); c.line((1.6, 2.9), (2.55, 2.4)); c.term(0.4, 2.9, "E", "left")
    c.arrow((2.1, 2.61), (2.55, 2.4), ms=11)
    c.save("c_ujt_symbol")


def ujt_equiv():
    c = Ckt(7.5, 6.5)
    c.term(3.2, 6.1, "$B_2$  ($+V_{BB}$)", "right") if False else None
    c.wire((3.0, 6.1), (3.0, 5.6)); c.term(3.0, 6.1, "$B_2$", "up")
    c.res((3.0, 5.6), (3.0, 3.6), "$R_{B2}$", side="up")
    c.dot(3.0, 3.6); c.text(3.35, 3.6, "A", size=10, ha="left")
    c.res((3.0, 3.6), (3.0, 1.2), "$R_{B1}$", side="up")
    c.wire((3.0, 1.2), (3.0, 0.7)); c.term(3.0, 0.7, "$B_1$", "down")
    c.term(0.3, 3.6, "E", "left"); c.wire((0.3, 3.6), (0.8, 3.6)); c.diode((0.8, 3.6), (3.0, 3.6), "$V_D$", side="up")
    c.arrow((5.4, 3.5), (5.4, 1.2), style="<|-|>", ms=9, lw=1.2); c.text(5.6, 2.35, "$\\eta V_{BB}$", size=11, ha="left")
    c.arrow((4.6, 5.6), (4.6, 1.2), style="<|-|>", ms=9, lw=1.2); c.text(4.7, 4.9, "$V_{BB}$", size=11, ha="left")
    c.text(1.6, 3.0, "$I_E$", size=10)
    c.save("c_ujt_equiv")


def ujt_osc():
    c = Ckt(11, 7.6)
    Ry = 7.0
    c.wire((1.6, Ry), (4.6, Ry)); c.wire((3.2, Ry), (3.2, Ry + 0.45)); c.term(3.2, Ry + 0.45, "$+V_{BB}$", "up")
    # emitter branch
    c.res((1.6, Ry), (1.6, 5.0), "$R_E$", side="up")
    c.dot(1.6, 4.0); c.wire((1.6, 5.0), (1.6, 4.0))
    c.cap((1.6, 4.0), (1.6, 1.6), "$C_E$", side="up", polar=True); c.wire((1.6, 1.6), (1.6, 0.6)); c.ground(1.6, 0.6)
    c.wire((1.6, 4.0), (0.6, 4.0)); c.term(0.6, 4.0, "$V_E$", "left")
    # UJT
    bx = 4.6
    c.line((bx, 2.8), (bx, 4.6), lw=3.4)
    c.wire((1.6, 3.9), (3.6, 3.9)); c.line((3.6, 3.9), (bx - 0.05, 3.6)); c.arrow((4.1, 3.72), (bx - 0.05, 3.6), ms=11)
    c.res((bx, Ry), (bx, 5.6), "$R_2$", side="up"); c.wire((bx, 5.6), (bx, 4.6)); c.dot(bx, 5.2)
    c.wire((bx, 5.2), (6.2, 5.2)); c.term(6.2, 5.2, "$V_{B2}$", "right"); c.text(5.0, 4.85, "$B_2$", size=10, ha="left")
    c.wire((bx, 2.8), (bx, 2.2)); c.dot(bx, 2.2); c.wire((bx, 2.2), (6.2, 2.2)); c.term(6.2, 2.2, "$V_{B1}$", "right"); c.text(5.0, 2.55, "$B_1$", size=10, ha="left")
    c.res((bx, 2.2), (bx, 0.9), "$R_1$", side="up"); c.wire((bx, 0.9), (bx, 0.6)); c.ground(bx, 0.6)
    c.text(6.0, 6.3, "$R_E C_E$ sets the frequency", size=10, ha="left", color="#1f5fbf")
    c.save("c_ujt_osc")


def tunnel_eq():
    c = Ckt(11, 4.4)
    top, bot = 3.4, 0.7
    c.term(0.3, top, None); c.term(0.3, bot, None); c.wire((0.3, bot), (9.4, bot)); c.term(9.4, bot, None) if False else None
    c.wire((0.3, top), (0.9, top)); c.res((0.9, top), (3.0, top), "$R_S$ (1–5 Ω)")
    c.ind((3.0, top), (5.6, top), "$L_S$ (0.1–4 nH)")
    c.wire((5.6, top), (6.4, top)); c.dot(6.4, top); c.dot(6.4, bot)
    c.wire((6.4, top), (9.0, top)); c.dot(9.0, top); c.dot(9.0, bot)
    c.cap((6.4, top), (6.4, bot), "C\n0.35–100 pF", side="down")
    c.res((9.0, top), (9.0, bot), "$-R_n$", side="up")
    c.save("c_tunnel_eq")


def photodiode_circuit():
    c = Ckt(8, 5)
    c.battery((1, 0.7), (1, 3.7), label="$V_R$", side="down", plus_at_end=True)
    c.wire((1, 3.7), (1, 4.2), (2, 4.2)); c.res((2, 4.2), (4.4, 4.2), "$R_L$")
    c.wire((4.4, 4.2), (6.5, 4.2))
    c.photodiode((6.5, 0.7), (6.5, 4.2), None)
    c.text(7.6, 2.5, "photodiode", size=10, ha="left")
    c.wire((6.5, 0.7), (6.5, 0.2), (1, 0.2), (1, 0.7))
    c.text(4.2, 1.3, "reverse biased:\nlight → current", size=10)
    c.save("c_photodiode")


def special_symbols():
    items = [("c_sym_zener", "zener", "Zener"), ("c_sym_tunnel", "tunnel", "Tunnel"), ("c_sym_varactor", "varactor", "Varactor"),
             ("c_sym_led", "led", "LED"), ("c_sym_photo", "photo", "Photodiode"), ("c_sym_diode", "diode", "PN diode")]
    for nm, kind, lab in items:
        c = Ckt(5.6, 2.6, pad=0.2)
        c.term(0.3, 1.0, "A", "left"); c.term(5.3, 1.0, "K", "right")
        c.wire((0.3, 1.0), (1.2, 1.0)); c.wire((4.4, 1.0), (5.3, 1.0))
        getattr(c, "led" if kind == "led" else "photodiode" if kind == "photo" else kind if kind != "diode" else "diode")((1.2, 1.0), (4.4, 1.0), None)
        c.text(2.8, 2.1 if kind not in ("led", "photo") else 2.4, lab, size=10, weight="bold") if False else None
        c.save(nm)


def run_all():
    re_model_ce(); re_model_diode(); re_model_cb(); ac_fixed(); ac_unbypassed(); ac_follower(); ac_collfb(); hybrid()
    scr_symbol(); triac_diac(); ujt_symbol(); ujt_equiv(); ujt_osc(); tunnel_eq(); photodiode_circuit(); special_symbols()


if __name__ == "__main__":
    run_all(); print("ok")
