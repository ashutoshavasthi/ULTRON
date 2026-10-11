"""The Judge's checks of Stage 2's V4 (pendulum periods) and V6 (detection on par with a
lab tool) on the real lab films, by the rules fixed in docs/STAGE_2_PLAN.md before
anything was measured.

Ultron's side is its eyes and `senses/motion.py`: it gets the pictures, the frame rate in
the file and, for V4, the length the lab wrote. The Judge's side is here: the lab's own
hand marks from its Tracker files, the textbook period, and the verdicts.

Run: python -m ultron.judge.footage_checks   (needs a trained brain in brain/)
"""

import math

import numpy as np

from ..env import footage
from ..senses import motion
from .footage_reference import tracker_points

G_LAB = 9.80
PENDULUMS = ("pendulum_drag", "Pendulum")
MARKED = {"BallTossOut": "parabola", "Pendulum": "sine"}


def _track(eyes, name):
    pictures = footage.frames(name)
    label = footage.label(name)
    _, per, _, tracks = motion.watch(eyes, pictures, label["interlaced"])
    return motion.whole_mover(tracks), pictures, label


# ---------------------------------------------------------------- V4
def v4(eyes):
    """Each pendulum film: Ultron's period against T_ref = 2π√(L/g)(1 + θ₀²/16), with
    θ₀ the angle Ultron measured. Pass per film: within 2 errors, error at most 3%. The
    √length law needs three lengths; with two it is not judged and V4 stays open."""
    films = {}
    for name in PENDULUMS:
        track, _, label = _track(eyes, name)
        s = motion.swing(track, label["fps"]) if track else None
        if s is None:
            films[name] = {"measured": False, "passed": False}
            continue
        ref = 2 * math.pi * math.sqrt(label["length_m"] / G_LAB) * (1 + s["angle"] ** 2 / 16)
        within = abs(s["period"] - ref) <= 2 * s["error"]
        precise = s["error"] <= 0.03 * s["period"]
        films[name] = {"measured": True, "length_m": label["length_m"], "rate": label["fps"],
                       "period": s["period"], "error": s["error"], "reference": ref,
                       "angle_deg": math.degrees(s["angle"]), "half_swings": len(s["half_swings"]),
                       "off_by_errors": (s["period"] - ref) / s["error"],
                       "within": within, "precise": precise, "passed": within and precise}
    lengths = {f["length_m"] for f in films.values() if f["measured"]}
    return {"films": films, "lengths": len(lengths), "sqrt_law_judged": len(lengths) >= 3,
            "passed": all(f["passed"] for f in films.values()) and len(lengths) >= 3}


# ---------------------------------------------------------------- V6
def _smooth_scatter(ts, xs, ys, kind):
    """How far positions scatter about a smooth path: a parabola in x and in y (a thrown
    ball), or a swing (x a sine at the swing's frequency, y one at twice it, as a bob on
    a circle rises at both ends; the frequency is the best fit)."""
    if kind == "parabola":
        r = [v - np.polyval(np.polyfit(ts, v, 2), ts) for v in (xs, ys)]
        return float(np.sqrt(np.mean(np.concatenate(r) ** 2)))
    best = None
    for w in np.linspace(1.0, 6.0, 2001):
        e = 0.0
        for v, n in ((xs, 1), (ys, 2)):
            a = np.stack([np.sin(n * w * ts), np.cos(n * w * ts), np.ones_like(ts)], 1)
            c = np.linalg.lstsq(a, v, rcond=None)[0]
            e += float(np.sum((v - a @ c) ** 2))
        best = e if best is None else min(best, e)
    return float(np.sqrt(best / (2 * len(ts))))


def object_radius(pictures, points):
    """The object's size as the Judge measures it: in the change picture at each marked
    position, the area at least half as strong as its peak, as a disc's radius (median)."""
    diffs, _ = motion.changes(pictures)
    radii = []
    for f, x, y in points:
        d = np.abs(diffs[f])
        r, c = int(round(y)), int(round(x))
        win = d[max(0, r - 15):r + 16, max(0, c - 15):c + 16]
        if win.size:
            radii.append(math.sqrt((win >= 0.5 * win.max()).sum() / math.pi))
    return float(np.median(radii))


def v6(eyes):
    """Every film the lab marked by hand: Ultron finds the object in ≥ 90% of the marked
    pictures, its median distance to the lab's marks is at most the object's radius, and
    its positions scatter about a smooth path at most 1.5× as much as the lab's."""
    films = {}
    for name, kind in MARKED.items():
        track, pictures, label = _track(eyes, name)
        lab = tracker_points(footage.tracker_file(name))["points"]
        seen = [(f, x, y) for f, x, y in lab if track and f in track]
        dist = [math.hypot(track[f][0] - x, track[f][1] - y) for f, x, y in seen]
        radius = object_radius(pictures, lab)
        ts = np.array([f for f, _, _ in seen], float) / label["fps"]
        lab_s = _smooth_scatter(ts, np.array([x for _, x, _ in seen]),
                                np.array([y for _, _, y in seen]), kind)
        own_s = _smooth_scatter(ts, np.array([track[f][0] for f, _, _ in seen]),
                                np.array([track[f][1] for f, _, _ in seen]), kind)
        found = len(seen) / len(lab)
        median = float(np.median(dist)) if dist else float("inf")
        films[name] = {"marked": len(lab), "found": len(seen), "median_px": median,
                       "radius_px": radius, "scatter_lab_px": lab_s, "scatter_px": own_s,
                       "passed": found >= 0.9 and median <= radius and own_s <= 1.5 * lab_s}
    return {"films": films, "passed": all(f["passed"] for f in films.values())}


if __name__ == "__main__":
    import json
    from ..brain.brain import Brain
    eyes = Brain.load("brain/ultron_brain.json").eyes
    print(json.dumps({"V4": v4(eyes), "V6": v6(eyes)}, indent=1))
