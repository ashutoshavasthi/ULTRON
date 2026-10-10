"""Worlds that change step by step, where none of Ultron's innate kinds of
explanation works. Each keeps its true settings hidden; the Judge may read them.

Readings are rounded to the instrument's precision (like any real instrument).
"""

import random


def _r(x, digits=3):
    return round(x, digits)


class _Objects:
    """Objects with hidden settings, named with a prefix."""

    def __init__(self, seed, prefix):
        self.rng = random.Random(seed)
        self.prefix = prefix
        self.hidden = {}

    def _new(self, settings):
        name = f"{self.prefix}{len(self.hidden) + 1}"
        self.hidden[name] = settings
        return name

    @property
    def names(self):
        return list(self.hidden)


class CoolingCups(_Objects):
    """Hot cups on a table; a thermometer in each, read once a minute. Each cup loses
    the same fraction of its excess heat each minute (Newton's cooling); the room's
    temperature and each cup's rate are hidden."""

    def __init__(self, seed=0, prefix="Cup"):
        super().__init__(seed, prefix)

    def new_cup(self):
        rng = self.rng
        return self._new({"room": rng.uniform(12, 26), "start": rng.uniform(60, 95),
                          "keep": rng.uniform(0.78, 0.93)})

    def read(self, cup, t):
        h = self.hidden[cup]
        return _r(h["room"] + (h["start"] - h["room"]) * h["keep"] ** t)

    def room(self, cup):
        return self.hidden[cup]["room"]


class BouncingBalls(_Objects):
    """Balls dropped on a hard floor; the height of each bounce is measured. Each ball
    keeps the same fraction of its height each bounce (hidden)."""

    def __init__(self, seed=0, prefix="Ball"):
        super().__init__(seed, prefix)

    def new_ball(self):
        rng = self.rng
        return self._new({"drop": rng.uniform(1, 4), "keep": rng.uniform(0.45, 0.8)})

    def read(self, ball, k):
        h = self.hidden[ball]
        return _r(h["drop"] * h["keep"] ** k, 4)


class Batteries(_Objects):
    """Batteries on a charger; the charge meter is read every minute. Each fills up
    toward its own capacity, a fixed fraction of what is missing each minute."""

    def __init__(self, seed=0, prefix="Battery"):
        super().__init__(seed, prefix)

    def new_battery(self):
        rng = self.rng
        return self._new({"full": rng.uniform(50, 120), "keep": rng.uniform(0.7, 0.9)})

    def read(self, battery, t):
        h = self.hidden[battery]
        return _r(h["full"] * (1 - h["keep"] ** t))


class HangingSprings(_Objects):
    """Springs hung from a hook; weights (in newtons) are hung on them and a ruler reads
    the spring's whole LENGTH, not how far it stretched. Each spring has its own
    unstretched length and stiffness (hidden)."""

    def __init__(self, seed=0, prefix="Coil"):
        super().__init__(seed, prefix)

    def new_spring(self):
        rng = self.rng
        return self._new({"rest": rng.uniform(0.1, 0.4), "k": rng.uniform(40, 200)})

    def read(self, spring, F):
        h = self.hidden[spring]
        return _r(h["rest"] + F / h["k"], 5)


class Candles(_Objects):
    """Candles burning; a ruler reads each candle's height now and then (whenever
    someone looks: not at equal times). Each burns down at its own steady rate from
    its own starting height (hidden)."""

    def __init__(self, seed=0, prefix="Candle"):
        super().__init__(seed, prefix)

    def new_candle(self):
        rng = self.rng
        return self._new({"tall": rng.uniform(15, 30), "rate": rng.uniform(0.2, 0.8)})

    def read(self, candle, t):
        h = self.hidden[candle]
        return _r(h["tall"] - h["rate"] * t)


class Wanderers(_Objects):
    """A marker nudged left or right by random gusts: there is nothing to find."""

    def __init__(self, seed=0, prefix="Walker"):
        super().__init__(seed, prefix)
        self.path = {}

    def new_walker(self):
        name = self._new({})
        x, path = self.rng.uniform(-5, 5), []
        for _ in range(40):
            path.append(_r(x))
            x += self.rng.gauss(0, 1)
        self.path[name] = path
        return name

    def read(self, walker, t):
        return self.path[walker][t]


class DrainingTanks(_Objects):
    """Water tanks with a small hole near the bottom, above a drain; a gauge reads the
    water's height every minute. Each loses the same fraction of what is above the
    hole each minute (hidden)."""

    def __init__(self, seed=0, prefix="Tank"):
        super().__init__(seed, prefix)

    def new_tank(self):
        rng = self.rng
        return self._new({"hole": rng.uniform(0.05, 0.3), "start": rng.uniform(1.5, 3.0),
                          "keep": rng.uniform(0.75, 0.92)})

    def read(self, tank, t):
        h = self.hidden[tank]
        return _r(h["hole"] + (h["start"] - h["hole"]) * h["keep"] ** t, 4)


class Pendulums(_Objects):
    """Pendulums swinging freely; a camera reads each one's angle (degrees) every tenth of
    a second. Each has its own swing and period (hidden)."""

    DT = 0.1

    def __init__(self, seed=0, prefix="Pendulum"):
        super().__init__(seed, prefix)

    def new_pendulum(self):
        rng = self.rng
        return self._new({"amp": rng.uniform(5, 20), "period": rng.uniform(1.0, 2.5),
                          "phase": rng.uniform(0, 6.283)})

    def read(self, p, t):
        import math
        h = self.hidden[p]
        return _r(h["amp"] * math.cos(2 * math.pi * t * self.DT / h["period"] + h["phase"]))

    def period(self, p):
        return self.hidden[p]["period"]


class ShockAbsorbers(_Objects):
    """A car's spring and shock absorber after a bump: the body's height above its resting
    point (cm), read every tenth of a second. It swings, and each swing is smaller by the
    same fraction (hidden)."""

    def __init__(self, seed=0, prefix="Car"):
        super().__init__(seed, prefix)

    def new_car(self):
        rng = self.rng
        return self._new({"amp": rng.uniform(3, 10), "keep": rng.uniform(0.8, 0.95),
                          "step": rng.uniform(0.4, 0.9), "phase": rng.uniform(0, 6.283)})

    def read(self, car, t):
        import math
        h = self.hidden[car]
        return _r(h["amp"] * h["keep"] ** t * math.cos(h["step"] * t + h["phase"]))

    def keep(self, car):
        return self.hidden[car]["keep"]


class YeastJars(_Objects):
    """Yeast growing in jars of sugar water; the cells are counted (thousands) every hour.
    They multiply, then crowd each other out: each jar has its own capacity (hidden)."""

    def __init__(self, seed=0, prefix="Jar"):
        super().__init__(seed, prefix)

    def new_jar(self):
        rng = self.rng
        return self._new({"cap": rng.uniform(500, 2000), "start": rng.uniform(5, 50),
                          "rate": rng.uniform(0.3, 0.9)})

    def read(self, jar, t):
        import math
        h = self.hidden[jar]
        return _r(h["cap"] / (1 + (h["cap"] / h["start"] - 1) * math.exp(-h["rate"] * t)), 2)

    def capacity(self, jar):
        return self.hidden[jar]["cap"]


class Funnels(_Objects):
    """Funnels of water emptying through a small hole at the bottom; the water's height
    (cm) is read every 10 seconds. Water runs out faster when it stands higher (Torricelli);
    each funnel's start and hole are hidden."""

    def __init__(self, seed=0, prefix="Funnel"):
        super().__init__(seed, prefix)

    def new_funnel(self):
        rng = self.rng
        return self._new({"start": rng.uniform(20, 60), "drop": rng.uniform(0.25, 0.45)})

    def read(self, f, t):
        h = self.hidden[f]
        return _r(max(h["start"] ** 0.5 - h["drop"] * t, 0) ** 2)

    def empty_at(self, f):
        h = self.hidden[f]
        return h["start"] ** 0.5 / h["drop"]
