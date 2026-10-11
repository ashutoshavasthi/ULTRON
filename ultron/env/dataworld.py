"""DataWorld: real measurements, served one row at a time as experiences.

Values are converted to SI units so every quantity carries a known dimension.
"""

import csv
import os

HERE = os.path.join(os.path.dirname(__file__), "data")


def _rows(name):
    with open(os.path.join(HERE, name)) as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def orbits(name="orbits.csv"):
    """Each orbiting body: r (m), T (s), and which body it circles."""
    out = []
    for row in _rows(name):
        out.append({"body": row["body"], "system": row["system"],
                    "r": float(row["r"]) * float(row["r_unit_km"]) * 1000.0,
                    "T": float(row["T_days"]) * 86400.0})
    return out


def boyle():
    """Boyle's air column: V (tube length, proportional to volume), P (inches of mercury)."""
    return [{"V": float(r["V"]), "P": float(r["P"])} for r in _rows("boyle.csv")]


def unseen_orbits():
    return orbits("orbits_unseen.csv")
