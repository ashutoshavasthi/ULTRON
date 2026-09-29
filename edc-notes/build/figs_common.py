import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BLUE = "#1f5fbf"; ORANGE = "#d9822b"; GREEN = "#2f9e6b"; RED = "#d64545"; PURPLE = "#7b5cd6"
GRAY = "#6b7385"; INK = "#14213d"; TEAL = "#1996a3"

plt.rcParams.update({
    "svg.fonttype": "path", "font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
    "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 1.2,
    "axes.titlesize": 11, "axes.labelsize": 10.5, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.frameon": False, "legend.fontsize": 9, "figure.facecolor": "white", "axes.facecolor": "white",
    "lines.linewidth": 2.0,
})


def new(w=6.0, h=3.6, **kw):
    fig, ax = plt.subplots(figsize=(w, h), **kw)
    return fig, ax


def axes_cross(ax, xlabel="", ylabel="", origin=True):
    """textbook style: axes crossing at origin with arrows"""
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.set_xlabel(""); ax.set_ylabel("")
    xl = ax.get_xlim(); yl = ax.get_ylim()
    ax.annotate("", xy=(xl[1], 0), xytext=(xl[1] - 1e-9, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(xl[1], 0, "  " + xlabel, va="center", ha="left", fontsize=10.5, color=INK, clip_on=False)
    ax.text(0, yl[1], ylabel, va="bottom", ha="center", fontsize=10.5, color=INK, clip_on=False)


def save(fig, name, out="../figs/"):
    fig.savefig(f"{out}{name}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)
