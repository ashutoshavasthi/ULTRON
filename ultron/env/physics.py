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
