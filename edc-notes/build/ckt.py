"""Tiny circuit-drawing library on top of matplotlib (exact coordinates, consistent style)."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyArrowPatch

INK = "#14213d"
LW = 1.7
plt.rcParams["svg.fonttype"] = "path"
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["mathtext.fontset"] = "dejavusans"


class Ckt:
    def __init__(self, w=8, h=5, pad=0.4):
        self.fig, self.ax = plt.subplots(figsize=(w * 0.62, h * 0.62))
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.ax.set_xlim(-pad, w + pad)
        self.ax.set_ylim(-pad, h + pad)
        self.fig.subplots_adjust(0, 0, 1, 1)

    # ---------- basics ----------
    def line(self, *pts, lw=LW, color=INK, ls="-"):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round", solid_joinstyle="round", zorder=4)

    def wire(self, *pts):
        self.line(*pts)

    def dot(self, x, y, r=0.07, open=False):
        self.ax.add_patch(Circle((x, y), r if not open else 0.09, fc="white" if open else INK, ec=INK, lw=1.3, zorder=6))

    def text(self, x, y, s, size=11, ha="center", va="center", color=INK, weight="normal", rot=0, style="normal"):
        self.ax.text(x, y, s, fontsize=size * 1.22, ha=ha, va=va, color=color, fontweight=weight, rotation=rot,
                     fontstyle=style, zorder=6)

    def ground(self, x, y):
        self.line((x, y), (x, y - 0.15))
        for i, wd in enumerate([0.32, 0.20, 0.08]):
            yy = y - 0.15 - i * 0.09
            self.line((x - wd, yy), (x + wd, yy), lw=1.5)

    def arrow(self, p, q, color=INK, lw=1.4, ms=10, style="-|>"):
        self.ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, zorder=6,
                                          shrinkA=0, shrinkB=0))

    # ---------- two-terminal elements ----------
    def _frame(self, p, q):
        p = np.array(p, float); q = np.array(q, float)
        L = np.linalg.norm(q - p)
        u = (q - p) / L
        n = np.array([-u[1], u[0]])
        return p, q, L, u, n

    def _g(self, p, u, n, s, t):
        return (p[0] + s * u[0] + t * n[0], p[1] + s * u[1] + t * n[1])

    def _leads(self, p, q, L, u, n, body):
        s0 = (L - body) / 2
        self.line(tuple(p), self._g(p, u, n, s0, 0))
        self.line(self._g(p, u, n, s0 + body, 0), tuple(q))
        return s0

    def _label(self, p, u, n, L, label, side, off=0.42, size=11):
        if not label:
            return
        t = off if side == "up" or side == "left" else -off
        # 'up' = normal direction (left of travel direction) ; 'down' opposite
        self.text(*self._g(p, u, n, L / 2, t), label, size=size)

    def res(self, p, q, label=None, side="up", body=1.1):
        p, q, L, u, n = self._frame(p, q)
        s0 = self._leads(p, q, L, u, n, body)
        pts = [self._g(p, u, n, s0, 0)]
        k = 6
        for i in range(k):
            s = s0 + body * (i + 0.5) / k
            pts.append(self._g(p, u, n, s, 0.17 * (1 if i % 2 == 0 else -1)))
        pts.append(self._g(p, u, n, s0 + body, 0))
        self.line(*pts)
        self._label(p, u, n, L, label, side)

    def ind(self, p, q, label=None, side="up", body=1.3):
        p, q, L, u, n = self._frame(p, q)
        s0 = self._leads(p, q, L, u, n, body)
        k = 4
        for i in range(k):
            c = self._g(p, u, n, s0 + body * (i + 0.5) / k, 0)
            th = np.linspace(0, math.pi, 30)
            r = body / (2 * k)
            xs = [c[0] + r * math.cos(t) * u[0] + r * math.sin(t) * n[0] for t in th]
            ys = [c[1] + r * math.cos(t) * u[1] + r * math.sin(t) * n[1] for t in th]
            self.ax.plot(xs, ys, color=INK, lw=LW)
        self._label(p, u, n, L, label, side, off=0.5)

    def cap(self, p, q, label=None, side="up", gap=0.22, plate=0.55, polar=False):
        p, q, L, u, n = self._frame(p, q)
        s0 = self._leads(p, q, L, u, n, gap)
        a = self._g(p, u, n, s0, -plate / 2), self._g(p, u, n, s0, plate / 2)
        b = self._g(p, u, n, s0 + gap, -plate / 2), self._g(p, u, n, s0 + gap, plate / 2)
        self.line(*a, lw=2.2); self.line(*b, lw=2.2)
        if polar:
            x, y = self._g(p, u, n, s0 - 0.18, plate / 2 + 0.12)
            self.text(x, y, "+", size=10)
        self._label(p, u, n, L, label, side, off=0.5)

    def battery(self, p, q, label=None, side="up", cells=1, plus_at_end=True):
        p, q, L, u, n = self._frame(p, q)
        body = 0.32 * cells + 0.12
        s0 = self._leads(p, q, L, u, n, body)
        for i in range(cells):
            s = s0 + i * 0.32
            # long (+) plate first if plus_at_start else last
            longp = (s, 0.34); shortp = (s + 0.16, 0.2)
            if plus_at_end:
                longp, shortp = (s + 0.16, 0.34), (s, 0.2)
            self.line(self._g(p, u, n, longp[0], -longp[1]), self._g(p, u, n, longp[0], longp[1]), lw=2.4)
            self.line(self._g(p, u, n, shortp[0], -shortp[1]), self._g(p, u, n, shortp[0], shortp[1]), lw=3.6)
        self._label(p, u, n, L, label, side, off=0.55)

    def acsrc(self, p, q, label=None, side="up", r=0.42):
        p, q, L, u, n = self._frame(p, q)
        self._leads(p, q, L, u, n, 2 * r)
        c = self._g(p, u, n, L / 2, 0)
        self.ax.add_patch(Circle(c, r, fc="white", ec=INK, lw=LW, zorder=4))
        th = np.linspace(-math.pi, math.pi, 60)
        xs = [c[0] + 0.6 * r * (t / math.pi) for t in th]
        ys = [c[1] + 0.3 * r * math.sin(t) for t in th]
        if abs(u[0]) < 0.5:  # vertical: rotate sine 90deg -> keep horizontal sine, fine
            pass
        self.ax.plot(xs, ys, color=INK, lw=1.5, zorder=5)
        self._label(p, u, n, L, label, side, off=0.7)

    def dcsrc(self, p, q, label=None, side="up", r=0.42):
        p, q, L, u, n = self._frame(p, q)
        self._leads(p, q, L, u, n, 2 * r)
        c = self._g(p, u, n, L / 2, 0)
        self.ax.add_patch(Circle(c, r, fc="white", ec=INK, lw=LW, zorder=4))
        self.text(*self._g(p, u, n, L / 2 + 0.22, 0), "+", size=11)
        self.text(*self._g(p, u, n, L / 2 - 0.2, 0), "−", size=11)
        self._label(p, u, n, L, label, side, off=0.7)

    def isrc(self, p, q, label=None, side="up", r=0.42, dependent=False):
        """current source, arrow points p->q"""
        p, q, L, u, n = self._frame(p, q)
        self._leads(p, q, L, u, n, 2 * r)
        c = self._g(p, u, n, L / 2, 0)
        if dependent:
            pts = [self._g(p, u, n, L / 2, r), self._g(p, u, n, L / 2 + r, 0), self._g(p, u, n, L / 2, -r),
                   self._g(p, u, n, L / 2 - r, 0)]
            self.ax.add_patch(Polygon(pts, fc="white", ec=INK, lw=LW, zorder=4))
        else:
            self.ax.add_patch(Circle(c, r, fc="white", ec=INK, lw=LW, zorder=4))
        self.arrow(self._g(p, u, n, L / 2 - r * 0.6, 0), self._g(p, u, n, L / 2 + r * 0.6, 0), ms=9)
        self._label(p, u, n, L, label, side, off=0.72)

    # ---------- diodes (anode at p, cathode at q) ----------
    def _diode_base(self, p, q, kind="plain", label=None, side="up"):
        p, q, L, u, n = self._frame(p, q)
        w, h = 0.5, 0.5
        s0 = self._leads(p, q, L, u, n, w)
        tri = [self._g(p, u, n, s0, h / 2), self._g(p, u, n, s0, -h / 2), self._g(p, u, n, s0 + w, 0)]
        self.ax.add_patch(Polygon(tri, fc="white", ec=INK, lw=LW, zorder=4))
        bar_a, bar_b = self._g(p, u, n, s0 + w, h / 2), self._g(p, u, n, s0 + w, -h / 2)
        if kind == "zener":
            self.line(self._g(p, u, n, s0 + w + 0.12, h / 2 + 0.0), bar_a, bar_b,
                      self._g(p, u, n, s0 + w - 0.12, -h / 2))
        elif kind == "tunnel":
            self.line(self._g(p, u, n, s0 + w + 0.14, h / 2), bar_a, bar_b, self._g(p, u, n, s0 + w + 0.14, -h / 2))
        elif kind == "varactor":
            self.line(bar_a, bar_b)
            self.line(self._g(p, u, n, s0 + w + 0.16, h / 2), self._g(p, u, n, s0 + w + 0.16, -h / 2))
        else:
            self.line(bar_a, bar_b)
        if kind in ("led", "photo"):
            for k in (0.08, 0.32):
                if kind == "led":
                    a = self._g(p, u, n, s0 + w * 0.35 + k * 0.6, h / 2 + 0.08)
                    b = self._g(p, u, n, s0 + w * 0.35 + k * 0.6 + 0.28, h / 2 + 0.55)
                else:
                    b = self._g(p, u, n, s0 + w * 0.35 + k * 0.6, h / 2 + 0.08)
                    a = self._g(p, u, n, s0 + w * 0.35 + k * 0.6 + 0.28, h / 2 + 0.55)
                self.arrow(a, b, ms=8, lw=1.3)
        self._label(p, u, n, L, label, side, off=0.65 if kind in ("led", "photo") else 0.5)

    def diode(self, p, q, label=None, side="up"):
        self._diode_base(p, q, "plain", label, side)

    def zener(self, p, q, label=None, side="up"):
        self._diode_base(p, q, "zener", label, side)

    def led(self, p, q, label=None, side="down"):
        self._diode_base(p, q, "led", label, side)

    def photodiode(self, p, q, label=None, side="down"):
        self._diode_base(p, q, "photo", label, side)

    def tunnel(self, p, q, label=None, side="up"):
        self._diode_base(p, q, "tunnel", label, side)

    def varactor(self, p, q, label=None, side="up"):
        self._diode_base(p, q, "varactor", label, side)

    # ---------- terminals ----------
    def term(self, x, y, label=None, side="right", size=11):
        self.dot(x, y, open=True)
        if label:
            dx, dy = {"right": (0.28, 0), "left": (-0.28, 0), "up": (0, 0.3), "down": (0, -0.3)}[side]
            ha = {"right": "left", "left": "right", "up": "center", "down": "center"}[side]
            self.text(x + dx, y + dy, label, ha=ha, size=size)

    # ---------- transistor ----------
    def bjt(self, cx, cy, kind="npn", circle=True, label_b=None, label_c=None, label_e=None, flip=False, mirror=False):
        """Symbol centred at (cx,cy). Default terminals: B=(cx-0.9,cy), C=(cx+0.25,cy+1.0), E=(cx+0.25,cy-1.0).
        flip=True swaps top/bottom (emitter on top); mirror=True puts the base on the right."""
        m = -1 if mirror else 1
        f = -1 if flip else 1
        X = lambda dx: cx + m * dx
        Y = lambda dy: cy + f * dy
        r = 0.62
        if circle:
            self.ax.add_patch(Circle((cx, cy), r, fc="white", ec=INK, lw=LW, zorder=3))
        self.line((X(-0.9), cy), (X(-0.22), cy))
        self.line((X(-0.22), Y(0.36)), (X(-0.22), Y(-0.36)), lw=3.2)
        self.line((X(-0.22), Y(0.16)), (X(0.25), Y(0.5)), (X(0.25), Y(1.0)))
        self.line((X(-0.22), Y(-0.16)), (X(0.25), Y(-0.5)), (X(0.25), Y(-1.0)))
        if kind == "npn":
            self.arrow((X(-0.02), Y(-0.32)), (X(0.2), Y(-0.47)), ms=11)
        else:
            self.arrow((X(0.22), Y(-0.47)), (X(-0.02), Y(-0.32)), ms=11)
        if label_b: self.text(X(-1.05), cy + 0.18, label_b, ha="right" if not mirror else "left", size=10.5)
        if label_c: self.text(X(0.42), Y(1.0), label_c, ha="left" if not mirror else "right", size=10.5)
        if label_e: self.text(X(0.42), Y(-1.0), label_e, ha="left" if not mirror else "right", size=10.5)
        return {"B": (X(-0.9), cy), "C": (X(0.25), Y(1.0)), "E": (X(0.25), Y(-1.0))}

    def save(self, name, out="../figs/"):
        self.fig.savefig(f"{out}{name}.svg", transparent=False, facecolor="white")
        plt.close(self.fig)
