"""Ultron's life in the nursery: days of waking steps, each followed by a night.

A day is DAY_STEPS waking steps (docs/AGE_0_1_PLAN.md). Each step the mind gets its
senses and gives an action; at night the mind may sleep on its day (if it can). Days
are counted, so every milestone can be reported in simulated days next to children's.

Seeds from EXAM_SEEDS on are for held-out exams only: a life lived to learn refuses them.
"""

import time

DAY_STEPS = 10_000
EXAM_SEEDS = 8001


class Life:
    def __init__(self, world, mind, exam=False):
        if world.seed >= EXAM_SEEDS and not exam:
            raise ValueError(f"seed {world.seed} is an exam seed (>= {EXAM_SEEDS}); "
                             "a life lived to learn may not use it")
        self.world, self.mind = world, mind
        self.days = 0
        self.seconds = 0.0
        self.steps = 0

    def day(self, steps=DAY_STEPS, watch=None):
        """Live one day of `steps` waking steps, then a night. watch(t, senses) is called
        each step (for people looking at the nursery; it can't change anything)."""
        w, mind = self.world, self.mind
        start_t = w.t
        clock = time.perf_counter()
        senses = w.senses()
        for _ in range(steps):
            w.act(mind.act(senses))
            w.step()
            senses = w.senses()
            if watch is not None:
                watch(w.t, senses)
        self.seconds += time.perf_counter() - clock
        self.steps += steps
        log = {"day": self.days, "from": start_t, "to": w.t, "stats": dict(w.stats),
               "caregiver": [e for e in (w.caregiver.log if w.caregiver else [])
                             if start_t <= e["t"] < w.t]}
        if hasattr(mind, "sleep"):
            mind.sleep(log)
        self.days += 1
        return log

    def per_step(self):
        return self.seconds / self.steps if self.steps else 0.0
