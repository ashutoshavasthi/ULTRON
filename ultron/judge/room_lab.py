"""The failure lab for Level 0 (WP3): attention and curiosity, each pushed until it
breaks.

These are the Judge's protocols. The Judge sets up the room as an experimenter would (it
may take things out, bring them in or hold its arms still, and it reads where things
really are), and only ever gives Ultron its senses. The seeds here are development seeds;
the Level 0 exams use seeds from 8001 on and are run at the gate.
"""

import numpy as np

from ..brain.explorer import BINS, Explorer, _posture_bin
from ..room.body import Senses
from ..room.world import GROUND, Room

SHOW, GAP, WARM = 60, 40, 300       # steps a toy is shown, taken away, and before it all
PLACE, SWING, PERIOD = (80.0, 50.0), 8.0, 20    # where a toy is dangled, how it swings
SEEDS = (11, 12, 13, 14, 15)


def _row(level, outcome, ok):
    return {"level": level, "outcome": outcome, "ok": bool(ok)}


def _experiment(name, question, dial, rows, note=""):
    bp = next((r["level"] for r in rows if not r["ok"]), None)
    return {"name": name, "question": question, "dial": dial, "rows": rows,
            "breakpoint": bp, "note": note}


# ------------------------------------------------------------------ attention

def _in_view(w, t):
    """Looking at it: the thing is in the middle of the view, the part it takes in."""
    return abs(t["x"] - w.gaze[0]) < 10 and abs(t["y"] - w.gaze[1]) < 10


def _run(w, mind, senses, steps, toy=None, dangle=None):
    """Live `steps` steps. toy: count the steps it is looked at. dangle: (x, y) where the
    experimenter holds the toy, swinging it gently side to side."""
    looked = 0
    for k in range(steps):
        if dangle is not None:
            w.bring(toy["id"], dangle[0] + SWING * np.sin(2 * np.pi * k / PERIOD), dangle[1],
                    pinned=True)
        w.act(mind.act(senses))
        w.step()
        senses = w.senses()
        if toy is not None and _in_view(w, toy):
            looked += 1
    return senses, looked


def showings(seed, noise_level=0.08, n=10):
    """Attention to the new: its arms are held still and one toy is dangled in front of it,
    swinging, n times; then a new toy. Returns the looking time (steps with the toy in the
    middle of its view) of each showing; the last is the new toy."""
    w = Room(seed, teacher="off", noise_level=noise_level)
    w.arms_still = True
    for t in w.things:
        w.put_away(t["id"])
    toys = [t for t in w.things if t["kind"] in ("ball", "block", "light")]
    old = toys[0]
    new = max(toys[1:], key=lambda t: float(np.abs(np.array(t["rgb"]) - old["rgb"]).sum()))
    mind = Explorer(seed)
    senses, _ = _run(w, mind, w.senses(), WARM)
    times = []
    for toy in [old] * n + [new]:
        senses, looked = _run(w, mind, senses, SHOW, toy, dangle=PLACE)
        times.append(looked)
        w.put_away(toy["id"])
        senses, _ = _run(w, mind, senses, GAP)
    return times


def habituated(times):
    """Looking falls to <= 50% of the first three showings within the familiar showings,
    and the new toy is looked at >= 2x the habituated level (the last three)."""
    first = np.mean(times[:3])
    familiar = times[:-1]
    fell = any(x <= 0.5 * first for x in familiar[3:])
    level = max(1.0, float(np.mean(familiar[-3:])))
    return bool(fell and times[-1] >= 2 * level)


def attention_stress(brain=None):
    rows = []
    for noise in (0.08, 0.16, 0.24, 0.32):
        runs = [showings(s, noise) for s in SEEDS]
        ok = sum(habituated(t) for t in runs)
        first = np.mean([np.mean(t[:3]) for t in runs])
        late = np.mean([np.mean(t[-4:-1]) for t in runs])
        novel = np.mean([t[-1] for t in runs])
        rows.append(_row(f"camera noise {noise}", f"{ok}/{len(runs)} habituated; looking "
                         f"{first:.0f} -> {late:.0f} steps, new toy {novel:.0f}",
                         ok >= len(runs) - 1))
    return _experiment(
        "Attention to the new (Level 0)", "One toy shown again and again, then a new one: "
        "does its looking fall, and come back for the new toy?", "camera noise", rows,
        "Development seeds; a row passes when at least 4 of 5 seeds habituate.")


# ------------------------------------------------------------------ curiosity

class _NoisyPalm:
    """A 'noisy TV': in some postures of the left arm, the palm feels random touches."""

    def __init__(self, mind, noisy, seed):
        self.mind, self.noisy = mind, set(noisy)
        self.rng = np.random.default_rng(seed + 31337)

    def act(self, senses):
        if _posture_bin(senses.joints, 0) in self.noisy:
            palms = list(senses.touch["palms"])
            palms[0] = (int(self.rng.random() < 0.5), palms[0][1])
            senses = Senses(senses.picture, senses.joints, senses.gaze,
                            {"palms": tuple(palms), "body": senses.touch["body"]},
                            senses.around)
        return self.mind.act(senses)


def noisy_share(seed, noisy, chooser, steps=4000):
    w = Room(seed, teacher="off")
    mind = _NoisyPalm(Explorer(seed, chooser=chooser), noisy, seed)
    senses, inside, counted = w.senses(), 0, 0
    for k in range(steps):
        w.act(mind.act(senses))
        w.step()
        senses = w.senses()
        if k >= steps // 2:
            counted += 1
            inside += _posture_bin(senses.joints, 0) in noisy
    return inside / counted


def curiosity_stress(brain=None):
    rows = []
    rng = np.random.default_rng(7)
    for n in (1, 3, 5):
        noisy = sorted(int(b) for b in rng.choice(BINS * BINS, size=n, replace=False))
        share = {c: np.mean([noisy_share(s, noisy, c) for s in SEEDS[:2]])
                 for c in ("progress", "random", "error")}
        rows.append(_row(f"{n} noisy postures of 9",
                         f"time there: learning progress {share['progress']:.0%}, random "
                         f"{share['random']:.0%}, error-chasing {share['error']:.0%}",
                         share["progress"] <= 1.25 * share["random"]))
    return _experiment(
        "Curiosity and the noisy TV (Level 0)", "In some arm postures the palm feels pure "
        "noise. Does curiosity by learning progress keep away, where chasing the biggest "
        "error gets stuck?", "noisy postures", rows,
        "A row passes when it spends at most 1.25x the time a random babbler does in the "
        "noisy postures (second half of 4,000 steps, 2 seeds).")


EXPERIMENTS = [attention_stress, curiosity_stress]

__all__ = ["EXPERIMENTS", "GROUND", "showings", "habituated", "noisy_share"]
