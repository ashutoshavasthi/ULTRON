"""PhysicsSandbox: a deterministic 1-D mechanics world.

The world *behaves* physically; instruments report readings (scale, force
meter, ruler, accelerometer, speedometer). Springs have a hidden stiffness
that no instrument shows directly.
"""

import random


def _r(x):
    return float(f"{x:.12g}")


class PhysicsSandbox:
    def __init__(self, seed=0, n_springs=5, spring_prefix="S", precision=0.0):
        self.rng = random.Random(seed)
        self.precision = precision
        self._noise = random.Random(seed + 7919)
        self._stiffness = {f"{spring_prefix}{i + 1}": _r(self.rng.uniform(10, 100))
                           for i in range(n_springs)}

    def read(self, value):
        """An instrument reading: the true value, off by up to ±precision."""
        if not self.precision:
            return value
        return _r(value * (1 + self._noise.uniform(-self.precision, self.precision)))

    @property
    def springs(self):
        return sorted(self._stiffness)

    def add_spring(self, name):
        self._stiffness[name] = _r(self.rng.uniform(10, 100))

    # -- experiments
    def push(self, mass, force):
        """Push a ball of `mass` with a steady `force`; the accelerometer reads."""
        return _r(force / mass)

    def stretch(self, spring, extension):
        """Stretch a spring by `extension` metres; the force meter reads."""
        return _r(self._stiffness[spring] * extension)

    def collide(self, m1, v1, m2, v2, kind):
        """Two balls on a track. 'clay' balls stick together, 'steel' balls bounce."""
        if kind == "clay":
            v = (m1 * v1 + m2 * v2) / (m1 + m2)
            return _r(v), _r(v)
        u1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        u2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
        return _r(u1), _r(u2)

    def launch(self, spring, extension, mass):
        """A ball attached to a stretched spring is let go: its first acceleration."""
        return _r(self._stiffness[spring] * extension / mass)

    def secret_stiffness(self, spring):
        """Only the Judge may look at this, to grade answers."""
        return self._stiffness[spring]


class Track:
    """A frictionless roller-coaster track. A ball is let go from rest somewhere
    high; at points along its run, instruments read its height (m) and speed (m/s).
    The world obeys gravity; Ultron is told nothing about energy."""

    G = 9.81

    def __init__(self, seed=0, prefix="R"):
        self.rng = random.Random(seed)
        self.prefix = prefix
        self.run = 0
        self.release = None
        self.mass = None

    def new_run(self, height, mass):
        self.run += 1
        self.release, self.mass = height, mass
        return f"{self.prefix}{self.run}"

    def speed_at(self, height):
        """None if the ball can never get that high on this run."""
        drop = self.release - height
        return None if drop < 0 else _r((2 * self.G * drop) ** 0.5)


class SpringTrack(Track):
    """The same frictionless track, now with a spring bumper at the bottom. A ball rolls
    down, squashes the spring, stops, and is pushed back up. Instruments read its
    height, its speed and how far the spring is squashed. Nobody mentions that
    springs store anything."""

    STIFFNESS = 400.0   # N/m, hidden from Ultron
    MASS = 2.0          # kg, the same ball every time

    def speed(self, height, squash):
        left = 2 * self.G * (self.release - height) - self.STIFFNESS / self.MASS * squash ** 2
        return None if left < 0 else _r(left ** 0.5)

    def max_squash(self):
        return (2 * self.MASS * self.G * self.release / self.STIFFNESS) ** 0.5


class CoilShop:
    """Springs wound from the same wire, each with its own number of coils. Stretching a
    spring shows how hard it pulls; looking at it shows how many coils it has. Nothing
    says the two are connected (the world makes stiffness = 600 N/m / coils)."""

    WIRE = 600.0

    def __init__(self, seed=0, prefix="C"):
        self.rng = random.Random(seed)
        self.prefix = prefix
        self._coils = {}

    def new_spring(self, coils=None):
        name = f"{self.prefix}{len(self._coils) + 1}"
        self._coils[name] = coils if coils is not None else self.rng.randint(2, 12)
        return name

    @property
    def springs(self):
        return sorted(self._coils)

    def stretch(self, spring, extension):
        return _r(self.WIRE / self._coils[spring] * extension)

    def count_coils(self, spring):
        return list(range(self._coils[spring]))
