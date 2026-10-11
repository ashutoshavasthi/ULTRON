"""Dimensional analysis. A dimension is (M, L, T): powers of mass, length, time."""

NAMES = {
    (0, 0, 0): "dimensionless",
    (1, 0, 0): "kg",
    (0, 1, 0): "m",
    (0, 0, 1): "s",
    (0, 1, -1): "m/s",
    (0, 1, -2): "m/s²",
    (1, 1, -2): "N",
    (1, 0, -2): "N/m",
    (1, 1, -1): "kg·m/s",
    (1, 2, -2): "J",
    (1, 2, -3): "W",
    (1, -1, -2): "Pa",
    (0, 3, 0): "m³",
}


def of_monomial(powers, units):
    """Dimension of product(var ** power), or None if a unit is unknown."""
    total = [0, 0, 0]
    for var, p in powers.items():
        if var not in units:
            return None
        for i, d in enumerate(units[var]):
            total[i] += p * d
    return tuple(total)


def name(dims):
    if dims is None:
        return "the data's own units"
    if dims in NAMES:
        return NAMES[dims]
    parts = []
    for sym, p in zip(("kg", "m", "s"), dims):
        if p:
            parts.append(sym if p == 1 else f"{sym}^{p}")
    return "·".join(parts)
