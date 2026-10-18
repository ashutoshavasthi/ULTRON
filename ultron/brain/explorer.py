"""The explorer (Level 0, WP3): attention, curiosity, memory of its days, and sleep.

Everything here is in the starting kit (docs/LEVEL_0_PLAN.md):

  * attention (habituation): what is in the middle of its view is interesting while it is new; the
    longer it looks, the less interesting it gets, and something new catches it again.
    A spot it has just left can't pull its eyes straight back (inhibition of return);
  * curiosity by learning progress (brain/curiosity.py): its babbling drifts toward the
    postures where its guess "will my palm touch something here?" is getting better,
    and leaves both the mastered ones and the hopeless (pure noise) ones;
  * episodic memory: every fixation is kept (when, where it looked, what it saw, how long,
    how surprising);
  * sleep: at night the day is consolidated. One record per familiar thing (where and when
    it was last seen, how often) and the most vivid episodes are kept; the rest is
    forgotten, and the day's short-term habituation is reset;
  * its eyes (WP4) learn at night from glimpses kept during the day: the bounded lumps that
    lasted from glimpse to glimpse are taken as real things (as in lesson 26's
    self-teaching), and a small network (senses/eyes.py) is trained to light up there.

It sees only Senses (room/body.py).
"""

import math

import numpy as np

from ..room.body import Action, LIMITS
from ..room.world import COARSE
from ..senses import track
from ..senses.eyes import Eyes
from ..senses.retina import _box, luminance
from ..senses.things import _regions
from .curiosity import Curiosity

# habituation
TAU = 30.0              # steps of looking for interest to fall to 1/e
FORGET = 0.995          # short-term habituation decays this much each step
FAMILIAR = 50.0         # fixations after which a thing is half as interesting
LEAVE = 0.5             # it looks away when interest falls below this
MATCH = 0.06            # rms difference within which two sights are the same thing
LUMP = 4.0              # how far (in noise) a pixel must stand out from its surround
SURROUND = 15           # the surround it is compared with (pixels), as the retina's
CHANGE = 0.3            # how much a patch of the wide view must change (in all three
                        # colours together) to catch its eye
WIDE_OUT = 0.15         # how far from the background a patch of the wide view stands out
WANDER = 0.05           # chance each idle step of looking at something that stands out
PAN, TILT = 48.0, 24.0  # how far its eyes turn (room units) per unit of its gaze sense
RETURN = 60             # steps a spot it left can't pull its eyes back
NEAR = 12.0             # view pixels: what counts as the same spot
# curiosity
BINS = 3                # posture bins per joint
GOAL_EVERY = 40         # steps between choosing where to babble toward
PULL = 0.04             # how hard it babbles toward the chosen posture
LEARN = 0.1             # how fast its touch guesses follow what happens
# sleep
VIVID = 10              # episodes kept from each day
# eyes (WP4)
GLIMPSE_EVERY = 4       # while its eyes are still, a glimpse is kept every this many steps
GLIMPSES = 2500         # at most this many glimpses a day
LASTS = 8               # a lump seen in this many glimpses (along one path) is a real thing
TEACH = 300             # glimpses the eyes learn from each night
SMALLEST, LARGEST = 6, 200  # a lump's size in pixels (smaller is noise, bigger is a surface)


def _descriptor(picture):
    """The thing in the middle of the view, wherever in it it sits: the lump nearest the
    middle that stands out from its surroundings (the retina's centre-surround, so a wide
    even mat or wall is not a thing), described by its colour, how much of the middle it
    fills, and how stretched it is. None when no lump is there. (Seeing bounded lumps is
    in the starting kit.)"""
    lum = luminance(picture)
    diff = _box(lum, 3) - _box(lum, SURROUND)
    noise = 1.4826 * float(np.median(np.abs(diff - np.median(diff)))) or 1e-9
    h, w = lum.shape
    z = diff[h // 2 - 12:h // 2 + 12, w // 2 - 12:w // 2 + 12] / noise
    best = None
    for sign in (1, -1):
        labels, n = _regions(sign * z > LUMP)
        for k in range(1, n + 1):
            yy, xx = np.nonzero(labels == k)
            if len(yy) < 4:
                continue
            d = float(np.min((yy - 11.5) ** 2 + (xx - 11.5) ** 2))
            if best is None or d < best[0]:
                best = (d, yy, xx)
    if best is None or best[0] > 8.0 ** 2:
        return None
    _, yy, xx = best
    patch = picture[h // 2 - 12:h // 2 + 12, w // 2 - 12:w // 2 + 12]
    rgb = patch[yy, xx].mean(axis=0)
    sx, sy = float(xx.std()), float(yy.std())
    return np.array([*rgb, math.sqrt(len(yy) / 576.0), sx / (sx + sy + 1e-9)])


def lumps(lum):
    """The bounded lumps in a picture that stand out from their surroundings (the retina's
    centre-surround): their middles [(x, y)], weighted by how strongly they stand out.
    Long thin ones are edges, not lumps; two middles within 3 pixels are one lump (a thing
    and the halo around it)."""
    diff = _box(lum, 3) - _box(lum, SURROUND)
    noise = 1.4826 * float(np.median(np.abs(diff - np.median(diff)))) or 1e-9
    z = diff / noise
    out = []
    for sign in (1, -1):
        labels, n = _regions(sign * z > LUMP)
        for k in range(1, n + 1):
            yy, xx = np.nonzero(labels == k)
            if not SMALLEST <= len(yy) <= LARGEST:
                continue
            wide, tall = int(np.ptp(xx)) + 1, int(np.ptp(yy)) + 1
            if wide > 3 * tall or tall > 3 * wide:
                continue
            wgt = np.abs(z[yy, xx])
            p = (float((xx * wgt).sum() / wgt.sum()), float((yy * wgt).sum() / wgt.sum()))
            if all(math.dist(p, q) > 3.0 for q in out):
                out.append(p)
    return out


def _room(gaze):
    """Where its eyes point, from its sense of its own eyes (in the starting kit, like the
    oculomotor map that lets an animal turn its eyes toward something it glimpsed)."""
    return (gaze[0] * PAN, gaze[1] * TILT)


def _posture_bin(joints, arm):
    out = []
    for k in (0, 1):
        lo, hi = LIMITS[k]
        f = (joints[2 * arm + k] - lo) / (hi - lo)
        out.append(min(BINS - 1, max(0, int(f * BINS))))
    return out[0] * BINS + out[1]


class Explorer:
    def __init__(self, seed=0, chooser="progress"):
        self.rng = np.random.default_rng(seed)
        # where to babble: "progress" (its own way), or for comparison in the failure lab,
        # "error" (chase the biggest recent error) and "random"
        self.chooser = chooser
        self.t = 0
        self.day = 0
        # habituation and familiarity: one prototype per thing it has looked at
        self.protos = []                    # {"what", "seen", "habit", "where", "last"}
        self.fix = None                     # the fixation going on now
        self.inhibit = []                   # (where it looked, until t)
        self.last_wide = None
        self.last_here = None
        self.target = None                  # where a saccade under way is going
        self.flight = 0
        self.step_len = 0.0
        # memory
        self.episodes = []
        self.vivid = []
        # curiosity over postures
        self.curiosity = Curiosity()
        self.guess = {}                     # posture bin -> how likely a touch is
        self.pending = {}                   # posture bin -> errors since the last record
        self.goal = None
        self.turning = np.zeros(4)
        # grasping
        self.holding = [0, 0]
        # eyes (WP4): none until it has slept on what it saw
        self.seed = seed
        self.eyes = None
        self.glimpses = []

    # ------------------------------------------------------------ one step

    def act(self, senses):
        self.t += 1
        look = self._look(senses)
        if (self.step_len < 0.25 and self.t % GLIMPSE_EVERY == 0
                and len(self.glimpses) < GLIMPSES):
            self.glimpses.append((luminance(senses.picture).astype(np.float32),
                                  _room(senses.gaze)))
        turn = self._babble(senses)
        grip = self._grasp(senses)
        self._feel(senses)
        return Action(turn=turn, look=look, grip=grip)

    # ---- eyes: habituation

    def _match(self, what):
        """The thing it knows that looks like this, or None."""
        if not self.protos:
            return None
        a = np.array([p["what"] for p in self.protos])
        d = np.sqrt(((a - what) ** 2).mean(axis=1))
        i = int(np.argmin(d))
        return self.protos[i] if d[i] < MATCH else None

    def _proto(self, what):
        p = self._match(what)
        if p is None:
            p = {"what": what.copy(), "seen": 0, "habit": 0.0, "where": None, "last": None}
            self.protos.append(p)
        return p

    def interest(self, p):
        return math.exp(-p["habit"] / TAU) / (1.0 + p["seen"] / FAMILIAR)

    def _look(self, senses):
        pic = senses.picture
        here = _room(senses.gaze)
        self.step_len = 0.0 if self.last_here is None else math.dist(here, self.last_here)
        moved = self.step_len > 0.25
        wide = np.asarray(senses.around, dtype=float)
        # what changes in the wide view is only noticed while the eyes are still
        # (saccadic suppression): while they move, everything seems to change
        change = None
        if self.last_wide is not None and not moved:
            change = np.abs(wide - self.last_wide).sum(axis=2)
        self.last_wide, self.last_here = wide, here
        for p in self.protos:
            p["habit"] *= FORGET
        self.inhibit = [(g, u) for g, u in self.inhibit if u > self.t]
        if self.target is not None:                 # a saccade on its way
            step = self._toward(here)
            if step is not None:
                return step
        # a sudden change elsewhere breaks off whatever it is looking at (orienting)
        if change is not None and change.max() >= 2 * CHANGE:
            jump = self._choose_target(change, wide, here, strong=True)
            if jump is not None:
                self._end_fixation(here)
                self.target = jump
                return self._toward(here) or (0.0, 0.0)
        what = _descriptor(pic)
        if what is not None:
            p = None
            if self.fix is not None:        # still the same thing? (a little leeway)
                q = self.fix["proto"]
                if math.sqrt(((q["what"] - what) ** 2).mean()) < 1.5 * MATCH:
                    p = q
            p = p or self._proto(what)
            if self.fix is None or self.fix["proto"] is not p:
                self._end_fixation(here)
                self.fix = {"proto": p, "start": self.t, "where": here,
                            "surprise": self.interest(p), "sum": np.zeros_like(what), "n": 0}
            p["habit"] += 1.0
            self.fix["sum"] += what
            self.fix["n"] += 1
            if self.interest(p) > LEAVE:
                return self._track(_box(luminance(pic), 5))
            self._end_fixation(here, leaving=True)
            self.target = self._choose_target(change, wide, here, away=True)
        else:
            self._end_fixation(here)
            self.target = self._choose_target(change, wide, here)
        if self.target is not None:
            step = self._toward(here)
            if step is not None:
                return step
        return tuple(float(v) for v in self.rng.normal(0.0, 0.3, size=2))

    def _toward(self, here):
        """One step of the saccade under way; None when it has arrived (or can't go on)."""
        tx, ty = self.target
        dx, dy = tx - here[0], ty - here[1]
        self.flight += 1
        stuck = self.flight > 2 and self.step_len < 0.3     # its eyes can't turn further
        if math.hypot(dx, dy) <= 1.5 or self.flight > 40 or stuck:
            self.target, self.flight = None, 0
            return None
        return (dx, dy)

    def _track(self, lum):
        """Keep what it is looking at in the middle: look toward where it stands out."""
        h, w = lum.shape
        c = lum[h // 2 - 12:h // 2 + 12, w // 2 - 12:w // 2 + 12]
        e = np.abs(c - np.median(lum))
        if e.sum() <= 1e-9:
            return (0.0, 0.0)
        yy, xx = np.mgrid[0:24, 0:24]
        return (0.5 * float((e * xx).sum() / e.sum() - 11.5),
                0.5 * float((e * yy).sum() / e.sum() - 11.5))

    def _inhibited(self, spot):
        return any(math.dist(spot, g) < NEAR for g, _ in self.inhibit)

    def _choose_target(self, change, wide, here, strong=False, away=False):
        """Where to look next: what just changed anywhere in view (strongest first), or
        now and then something that stands out; never a spot it has just left."""
        h, w = wide.shape[:2]

        def spot(k):
            r, c = divmod(int(k), w)
            return (here[0] + (c + 0.5 - w / 2) * COARSE, here[1] + (r + 0.5 - h / 2) * COARSE)

        if change is not None:
            for k in np.argsort(change, axis=None)[::-1][:20]:
                if change.flat[k] < (2 * CHANGE if strong else CHANGE):
                    break
                s = spot(k)
                if math.dist(s, here) > NEAR and not self._inhibited(s):
                    self.flight = 0
                    return s
        if strong:
            return None
        if away or self.rng.random() < WANDER:
            out = np.abs(wide - np.median(wide, axis=(0, 1))).sum(axis=2).ravel()
            weights = np.where(out > WIDE_OUT, out, 0.0)
            if weights.sum() > 0:
                for k in self.rng.choice(len(weights), size=5, p=weights / weights.sum()):
                    s = spot(k)
                    if math.dist(s, here) > NEAR and not self._inhibited(s):
                        self.flight = 0
                        return s
        if away:                        # nothing else to see: look somewhere else anyway
            a = self.rng.uniform(0, 2 * math.pi)
            r = self.rng.uniform(2 * NEAR, 4 * NEAR)
            self.flight = 0
            return (here[0] + r * math.cos(a), here[1] + r * math.sin(a))
        return None

    def _end_fixation(self, here, leaving=False):
        f = self.fix
        if f is None:
            return
        self.fix = None
        if leaving:
            self.inhibit.append((here, self.t + RETURN))
        if f["n"] == 0:
            return
        p = f["proto"]
        p["seen"] += 1
        p["where"], p["last"] = tuple(f["where"]), self.t
        self.episodes.append({"day": self.day, "t": f["start"], "where": tuple(f["where"]),
                              "what": (f["sum"] / f["n"]).round(3).tolist(),
                              "dwell": f["n"], "surprise": round(f["surprise"], 4)})

    # ---- arms: curiosity by learning progress

    def _babble(self, senses):
        rng = self.rng
        joints = np.array(senses.joints)
        if self.t % GOAL_EVERY == 1 or self.goal is None:
            # one record per posture visited in the last stretch of babbling: how wrong its
            # touch guesses were there on average (single steps are too noisy to compare)
            for key in sorted(self.pending):
                self.curiosity.record(key, float(np.mean(self.pending[key])))
            # a posture it aimed for and never reached is a try with nothing learned:
            # after a fair number of such tries it stops straining for it
            if self.goal is not None:
                aim = f"{self.goal[0]}:{_posture_bin(list(self.goal[1]) * 2, 0)}"
                if aim not in self.pending:
                    self.curiosity.record(aim, 1.0)
            self.pending = {}
            options = [f"{arm}:{b}" for arm in (0, 1) for b in range(BINS * BINS)]
            choice = None
            if self.chooser == "progress":
                choice = self.curiosity.choose(options)
            elif self.chooser == "error":
                choice = max(options, key=lambda o: (self.curiosity.recent_error(o), o))
            if choice is None:
                choice = options[int(rng.integers(len(options)))]
            arm, b = (int(v) for v in choice.split(":"))
            target = []
            for k, i in enumerate(divmod(b, BINS)):
                lo, hi = LIMITS[k]
                target.append(lo + (i + rng.random()) * (hi - lo) / BINS)
            self.goal = (arm, target)
        arm, target = self.goal
        self.turning = 0.9 * self.turning + rng.normal(0.0, 0.012, size=4)
        pull = np.zeros(4)
        pull[2 * arm:2 * arm + 2] = PULL * (np.array(target) - joints[2 * arm:2 * arm + 2])
        return tuple(self.turning + pull)

    def _feel(self, senses):
        for arm in (0, 1):
            key = f"{arm}:{_posture_bin(senses.joints, arm)}"
            touched = float(senses.touch["palms"][arm][0])
            guess = self.guess.get(key, 0.5)
            self.pending.setdefault(key, []).append(abs(touched - guess))
            self.guess[key] = guess + LEARN * (touched - guess)

    def _grasp(self, senses):
        grip = []
        for k, (contact, _weight) in enumerate(senses.touch["palms"]):
            if self.holding[k] > 0:
                self.holding[k] -= 1
            elif contact:
                self.holding[k] = int(self.rng.integers(20, 100))
            grip.append(self.holding[k] > 0)
        return grip

    # ------------------------------------------------------------ memory

    def where_last(self, what):
        """Where it last saw something like this (its gaze then), and when; None if never."""
        p = self._match(np.asarray(what, dtype=float))
        if p is None or p["where"] is None:
            return None
        return p["where"], p["last"]

    def stored(self):
        """How much of its experience it is keeping: the episodes of its days, the vivid
        ones kept from earlier days, and one record per thing it knows. (Curiosity's few
        recent errors per posture are working state, not experiences.)"""
        return len(self.episodes) + len(self.vivid) + len(self.protos)

    # ------------------------------------------------------------ sleep

    def sleep(self, log=None):
        """Consolidate the day: keep a record per familiar thing (met more than once, or
        once vividly) and the most vivid episodes, forget the rest, and wake without the
        day's short-term habituation."""
        before = self.stored()
        self._end_fixation(self.fix["where"] if self.fix else (0.0, 0.0))
        day = self.episodes
        self.vivid += sorted(day, key=lambda e: (-e["surprise"], e["t"]))[:VIVID]
        self.episodes = []
        merged = []
        vivid = {tuple(e["where"]) for e in self.vivid}
        for p in sorted(self.protos, key=lambda q: (-q["seen"], q["last"] or 0)):
            # a thing glimpsed once is forgotten, unless that glimpse was a vivid one
            if p["seen"] == 0 or (p["seen"] == 1 and tuple(p["where"]) not in vivid):
                continue
            twin = next((m for m in merged
                         if math.sqrt(((m["what"] - p["what"]) ** 2).mean()) < MATCH / 2), None)
            if twin is None:
                merged.append(p)
                continue
            twin["seen"] += p["seen"]
            if (p["last"] or 0) > (twin["last"] or 0):
                twin["where"], twin["last"] = p["where"], p["last"]
        for p in merged:
            p["habit"] = 0.0
        self.protos = merged
        for key in self.curiosity.errors:
            self.curiosity.errors[key] = self.curiosity.errors[key][-16:]
        self.inhibit = []
        eyes = self._teach_eyes()
        self.day += 1
        return {"before": before, "after": self.stored(), "things": len(self.protos),
                "eyes": eyes}

    def _teach_eyes(self):
        """Train its eyes on the day's glimpses: what lasted is a real thing, the rest is
        nothing. Glimpses are forgotten afterwards."""
        glimpses, self.glimpses = self.glimpses, []
        if len(glimpses) < 50:
            return None
        h, w = glimpses[0][0].shape
        offsets = [(here[0] - w / 2, here[1] - h / 2) for _, here in glimpses]
        dets = [[(x + ox, y + oy) for x, y in lumps(lum)]
                for (lum, _), (ox, oy) in zip(glimpses, offsets)]
        lasting = track.lasting(track.link(dets, max_step=3.0), LASTS)
        rng = np.random.default_rng(self.seed * 1000 + self.day)
        pick = sorted(int(i) for i in rng.choice(len(glimpses), size=min(TEACH, len(glimpses)),
                                                replace=False))
        imgs = [glimpses[i][0].astype(float) for i in pick]
        touches = [[(t[i][0] - offsets[i][0], t[i][1] - offsets[i][1]) for t in lasting if i in t]
                   for i in pick]
        if not any(touches):
            return {"glimpses": len(glimpses), "lasted": len(lasting), "learned": 0}
        if self.eyes is None:
            self.eyes = Eyes(seed=self.seed)
        self.eyes.learn(imgs, touches, seed=self.seed + self.day, epochs=8)
        return {"glimpses": len(glimpses), "lasted": len(lasting), "learned": len(imgs)}
