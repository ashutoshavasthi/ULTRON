"""Reflexes: what Ultron does before it has learned anything.

All three are in its starting kit (docs/LEVEL_0_PLAN.md), as they are in animals:
  * motor babbling: its arms wander smoothly at random;
  * orienting: its eyes turn toward what just changed in the picture (motion, a light);
  * grasping: a hand closes when something touches its palm, and lets go after a while.

They learn nothing; the explorer (brain/explorer.py) builds on them.
"""

import numpy as np

from ..room.body import Action
from ..senses.retina import _box, luminance

MOMENTUM = 0.9
WANDER = 0.012          # how hard babbling pushes a joint each step (radians)
CHANGE = 0.08           # how much a patch must change to catch its eye (brightness)
HOLD = (20, 100)        # steps a grasp lasts


class Reflexes:
    def __init__(self, seed=0):
        self.rng = np.random.default_rng(seed)
        self.turning = np.zeros(4)
        self.last = None
        self.holding = [0, 0]           # steps left in each hand's grasp

    def act(self, senses):
        rng = self.rng
        self.turning = MOMENTUM * self.turning + rng.normal(0.0, WANDER, size=4)
        look = self._orient(senses)
        grip = []
        for k, (contact, _weight) in enumerate(senses.touch["palms"]):
            if self.holding[k] > 0:
                self.holding[k] -= 1
            elif contact:
                self.holding[k] = int(rng.integers(*HOLD))
            grip.append(self.holding[k] > 0)
        return Action(turn=self.turning, look=look, grip=grip)

    def _orient(self, senses):
        now = _box(luminance(senses.picture), 5)
        last, self.last = self.last, now
        if last is None:
            return (0.0, 0.0)
        change = np.abs(now - last)
        r, c = np.unravel_index(int(np.argmax(change)), change.shape)
        if change[r, c] < CHANGE:
            return tuple(self.rng.normal(0.0, 0.3, size=2))
        h, w = change.shape
        return (0.5 * (c - w / 2), 0.5 * (r - h / 2))
