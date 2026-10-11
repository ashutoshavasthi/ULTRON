"""The Judge's checks of Stage 2's V4 (pendulum periods), V5 (restitution) and V6
(detection on par with a lab tool) on the real lab films, by the rules fixed in docs/STAGE_2_PLAN.md before
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
PENDULUMS = ("Pendulum50cm", "pendulum_drag", "Pendulum")
BOUNCING = ("GBDrop", "BallBounceCorridor")
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
    law = sqrt_law({n: f for n, f in films.items() if f["measured"]})
    return {"films": films, "sqrt_law": law,
            "passed": all(f["passed"] for f in films.values()) and law["passed"]}


def sqrt_law(films):
    """The √length law over pendulum films ({name: {length_m, period, error}}), by the
    rule in docs/STAGE_2_PLAN.md: the power of log T against log L, weighted by Ultron's
    errors, within 2 errors of 0.5; the constant T/√L within 2 errors of 2π/√g, its error
    at most 3%. Each error is from Ultron's own errors, or from the scatter if larger."""
    if len({f["length_m"] for f in films.values()}) < 3:
        return {"judged": False, "passed": False}
    L = np.array([f["length_m"] for f in films.values()])
    T = np.array([f["period"] for f in films.values()])
    e = np.array([f["error"] for f in films.values()])
    x, y, w = np.log(L), np.log(T), (T / e) ** 2
    xm = np.sum(w * x) / np.sum(w)
    sxx = np.sum(w * (x - xm) ** 2)
    power = float(np.sum(w * (x - xm) * (y - np.sum(w * y) / np.sum(w))) / sxx)
    fit = np.sum(w * y) / np.sum(w) + power * (x - xm)
    chi = float(np.sum(w * (y - fit) ** 2) / (len(L) - 2))
    power_err = float(math.sqrt(max(1.0, chi) / sxx))
    c, ce = T / np.sqrt(L), e / np.sqrt(L)
    cw = 1 / ce ** 2
    const = float(np.sum(cw * c) / np.sum(cw))
    cchi = float(np.sum(cw * (c - const) ** 2) / (len(L) - 1))
    const_err = float(math.sqrt(max(1.0, cchi) / np.sum(cw)))
    ref = 2 * math.pi / math.sqrt(G_LAB)
    power_ok = abs(power - 0.5) <= 2 * power_err
    const_ok = abs(const - ref) <= 2 * const_err and const_err <= 0.03 * const
    return {"judged": True, "power": power, "power_error": power_err,
            "power_off_by_errors": (power - 0.5) / power_err,
            "constant": const, "constant_error": const_err, "constant_reference": ref,
            "constant_off_by_errors": (const - ref) / const_err,
            "power_passed": power_ok, "constant_passed": const_ok,
            "passed": power_ok and const_ok}


# ---------------------------------------------------------------- V5
def v5(eyes):
    """Each bouncing-ball film: Ultron's coefficient of restitution against the lab's
    hand marks measured the same way, over the bounces both saw (a bounce matches if
    its lowest picture is within 3 of the lab's). Pass per film: at least 2 bounces,
    within 2 combined errors, Ultron's error at most 5%."""
    def mean_se(v):
        m = float(np.mean(v))
        return m, (float(np.std(v, ddof=1) / math.sqrt(len(v))) if len(v) > 1 else float("inf"))
    films = {}
    for name in BOUNCING:
        track, _, _ = _track(eyes, name)
        lab = {f: (x, y) for f, x, y in tracker_points(footage.tracker_file(name))["points"]}
        own = motion.bounces(track) if track else []
        ref = motion.bounces(lab)
        pairs = []
        for f, e in ref:
            near = [(abs(g - f), k) for g, k in own if abs(g - f) <= 3]
            if near:
                pairs.append((f, min(near)[1], e))
        if len(pairs) < 2:
            films[name] = {"bounces_lab": len(ref), "bounces": len(pairs), "passed": False,
                           "pairs": pairs}
            continue
        e, err = mean_se([p[1] for p in pairs])
        e_lab, err_lab = mean_se([p[2] for p in pairs])
        combined = math.sqrt(err ** 2 + err_lab ** 2)
        within = abs(e - e_lab) <= 2 * combined
        precise = err <= 0.05 * e
        films[name] = {"bounces_lab": len(ref), "bounces": len(pairs), "pairs": pairs,
                       "e": e, "error": err, "e_lab": e_lab, "error_lab": err_lab,
                       "off_by_errors": (e - e_lab) / combined, "within": within,
                       "precise": precise, "passed": within and precise}
    return {"films": films, "passed": all(f["passed"] for f in films.values())}


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
    print(json.dumps({"V4": v4(eyes), "V5": v5(eyes), "V6": v6(eyes)}, indent=1))
