"""The Level 0 exams (docs/LEVEL_0_PLAN.md), as the Judge runs them in the room.

The Judge sets each scene up as an experimenter would and reads where things really are;
Ultron only ever gets pictures. Exam seeds start at 8001 and are run at the gate (WP6).
While a test is being built, the same protocol runs on development seeds (below 8001).
"""

import numpy as np

from ..brain.explorer import lumps
from ..room.world import MAT, Room
from ..senses.retina import channels, luminance

TOYS = ("ball", "block", "light")
LOOK_AT = (92.0, 66.0)          # where the scene is seen from (its own body is out of view)
SPAN = (64.0, 120.0)            # where toys are put (inside that view)
GLANCES = 5
NEAR = 1.5                      # pixels: "found" means a detection this close
EXAM_SEEDS = tuple(range(8001, 8026))
DEV_SEEDS = tuple(range(5101, 5126))


def scene(seed):
    """A still scene: 0-5 toys put down on the mat or floor in view, apart, nothing else
    there (no teacher, no screen, no cloth), its arms resting out of view."""
    rng = np.random.default_rng(seed)
    w = Room(seed, teacher="off")
    w.arms_still = True
    for t in w.things:
        w.put_away(t["id"])
    pool = [t for t in w.things if t["kind"] in TOYS]
    n = int(rng.integers(0, len(pool) + 1))
    toys = [pool[i] for i in sorted(rng.choice(len(pool), size=n, replace=False))]
    placed = []
    for t in toys:
        for _ in range(500):
            x = float(rng.uniform(SPAN[0] + t["hx"], SPAN[1] - t["hx"]))
            if all(abs(x - p["x"]) > t["hx"] + p["hx"] + 2.0 for p in placed):
                break
        top = MAT[1] if MAT[0] <= x <= MAT[2] else 90.0
        w.bring(t["id"], x, top - t["hy"] - 2.0)
        placed.append(t)
    for _ in range(40):                     # let them settle
        w.step()
    w.gaze = list(LOOK_AT)
    return w, toys


def glance(w, toys):
    """One picture of the scene, and where each toy really is in it (pixels)."""
    img = w.view(w.gaze)
    ox, oy = w.view_origin
    return luminance(img), [(t["x"] - ox, t["y"] - oy) for t in toys]


def _found(dets, truth):
    """Every toy has its own detection within NEAR pixels."""
    free = list(dets)
    for x, y in truth:
        best = min(free, key=lambda d: (d[0] - x) ** 2 + (d[1] - y) ** 2, default=None)
        if best is None or (best[0] - x) ** 2 + (best[1] - y) ** 2 > NEAR ** 2:
            return False
        free.remove(best)
    return True


def seeing(detect, seeds=DEV_SEEDS):
    """L0-1's protocol. detect(picture) -> [(x, y), ...]. In each scene: are all the toys
    found within NEAR pixels (first glance), and is the count right (the count most
    glances agree on)? Returns (scenes with every toy found, scenes counted right, scenes)."""
    found = counted = 0
    for seed in seeds:
        w, toys = scene(seed)
        counts = []
        for k in range(GLANCES):
            pic, truth = glance(w, toys)
            dets = detect(pic)
            if k == 0:
                found += _found(dets, truth)
            counts.append(len(dets))
        counted += max(set(counts), key=lambda c: (counts.count(c), -c)) == len(toys)
    return found, counted, len(seeds)


def by_eyes(eyes):
    """Its learned eyes, looking through the retina's ON channel (as they learned)."""
    return lambda pic: [(x, y) for x, y, _ in eyes.see(channels(pic)[0])]


def by_retina(pic):
    """The baseline: the untrained retina's lumps (ON centre-surround)."""
    return lumps(pic)
