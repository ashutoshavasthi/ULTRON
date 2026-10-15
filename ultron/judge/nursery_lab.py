"""The failure lab for the newborn (Age 0, WP3): habituation, curiosity and comfort,
each pushed until it breaks.

These are the Judge's protocols. The Judge sets up the nursery as an experimenter would
(it may take toys out and bring them in, and it reads where things really are), and
only ever gives the newborn its senses. The seeds here are development seeds; the
milestone exams (N1-N6) use seeds from 8001 on and are run at the Age 0 gate (WP5).
"""

import numpy as np

from ..brain.newborn import BINS, Newborn, _posture_bin
from ..nursery.body import Senses
from ..nursery.world import GROUND, Nursery

SHOW, GAP, WARM = 60, 40, 300       # steps a toy is shown, taken away, and before it all
PLACE, SWING, PERIOD = (80.0, 50.0), 8.0, 20    # where a toy is dangled, how it swings
SEEDS = (11, 12, 13, 14, 15)


def _row(level, outcome, ok):
    return {"level": level, "outcome": outcome, "ok": bool(ok)}


def _experiment(name, question, dial, rows, note=""):
    bp = next((r["level"] for r in rows if not r["ok"]), None)
    return {"name": name, "question": question, "dial": dial, "rows": rows,
            "breakpoint": bp, "note": note}


# ------------------------------------------------------------------ habituation

def _in_view(w, t):
    """Looking at it: the toy is in the middle of the view, the part the newborn takes in."""
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
    """Habituation as in infant looking-time studies: the baby sits in an infant seat
    (arms resting) and the experimenter dangles one toy in front of it, swinging gently,
    n times; then a new toy. Returns the looking time (steps with the toy in the middle of
    its view) of each showing; the last is the new toy."""
    w = Nursery(seed, caregiver="off", noise_level=noise_level)
    w.seated = True
    for t in w.things:
        w.put_away(t["id"])
    toys = [t for t in w.things if t["kind"] in ("ball", "block", "light")]
    old = toys[0]
    new = max(toys[1:], key=lambda t: float(np.abs(np.array(t["rgb"]) - old["rgb"]).sum()))
    mind = Newborn(seed)
    senses, _ = _run(w, mind, w.senses(), WARM)
    times = []
    for toy in [old] * n + [new]:
        senses, looked = _run(w, mind, senses, SHOW, toy, dangle=PLACE)
        times.append(looked)
        w.put_away(toy["id"])
        senses, _ = _run(w, mind, senses, GAP)
    return times


def habituated(times):
    """N1's rule: looking falls to <= 50% of the first three showings within the familiar
    showings, and the new toy is looked at >= 2x the habituated level (the last three)."""
    first = np.mean(times[:3])
    familiar = times[:-1]
    fell = any(x <= 0.5 * first for x in familiar[3:])
    level = max(1.0, float(np.mean(familiar[-3:])))
    return bool(fell and times[-1] >= 2 * level)


def habituation_stress(brain=None):
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
        "Habituation (newborn)", "One toy shown again and again, then a new one: does its "
        "looking fall, and come back for the new toy, as an infant's does?",
        "camera noise", rows,
        "Rule as N1 (docs/AGE_0_1_PLAN.md), on development seeds; a row passes when at "
        "least 4 of 5 seeds habituate.")


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
    w = Nursery(seed, caregiver="off")
    mind = _NoisyPalm(Newborn(seed, chooser=chooser), noisy, seed)
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
        "Curiosity and the noisy TV (newborn)", "In some arm postures the palm feels pure "
        "noise. Does curiosity by learning progress keep away, where chasing the biggest "
        "error gets stuck?", "noisy postures", rows,
        "A row passes when it spends at most 1.25x the time a random babbler does in the "
        "noisy postures (second half of 4,000 steps, 2 seeds).")


# ------------------------------------------------------------------ comfort

def comfort_run(seed, caregiver, steps=6000):
    w = Nursery(seed, caregiver=caregiver)
    mind = Newborn(seed)
    senses, levels = w.senses(), []
    for _ in range(steps):
        w.act(mind.act(senses))
        w.step()
        senses = w.senses()
        levels.append(mind.comfort)
    return w.stats["fussing"] / steps, float(np.mean(levels))


def caregiver_stress(brain=None):
    rows = []
    for mode in ("normal", "off"):
        runs = [comfort_run(s, mode) for s in SEEDS[:2]]
        fuss = np.mean([r[0] for r in runs])
        comfort = np.mean([r[1] for r in runs])
        rows.append(_row(f"caregiver {mode}", f"fussing {fuss:.0%} of the time, "
                         f"mean comfort {comfort:.2f}", fuss < 0.25))
    return _experiment(
        "Comfort without a caregiver (newborn)", "What happens to the newborn's comfort, "
        "and how much does it fuss, when nobody comes?", "caregiver", rows,
        "Nothing else is learned from the caregiver yet. The misleading-gaze row joins "
        "when gaze following is built (Age 1, WP6).")


EXPERIMENTS = [habituation_stress, curiosity_stress, caregiver_stress]

__all__ = ["EXPERIMENTS", "GROUND", "showings", "habituated", "noisy_share", "comfort_run"]
