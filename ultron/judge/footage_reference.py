"""The Trainer's and the Judge's work on the real lab films, done once, kept apart from
Ultron, and written into the manifest (ultron/env/data/real/footage.json).

* The scale label: where the metre stick in view has no calibration from the lab, the
  Trainer reads the stick's 10 cm marks (the dark bands between its white segments) on
  the film's median picture, the way a person reads a ruler. On BallTossOut, where the
  lab's own Tracker file calibrates the same stick (398.7 px per metre), the marks give
  400.0 px per metre, which confirms they are 10 cm apart.
* The lab tool's reference: the positions the lab marked in Tracker, and its scale and
  frame step, read from the Tracker file. Ultron never sees these.

Run: python -m ultron.judge.footage_reference   (prints what goes in the manifest)
"""

import re

import numpy as np


def stick_scale(pictures):
    """Pixels per metre from the stick's 10 cm marks on the median picture, and the
    marks' positions. The stick is the brightest column band; the marks are the dark
    minima along it."""
    med = np.median(np.array(pictures, dtype=float), axis=0)
    colmean = med.mean(axis=0)
    x0 = int(np.argmax(colmean))
    cols = [c for c in range(max(0, x0 - 6), min(med.shape[1], x0 + 7))
            if colmean[c] > 0.6 * colmean[x0]]
    prof = med[:, cols].mean(axis=1)
    rows = np.nonzero(prof > 0.5 * prof.max())[0]
    top, bot = int(rows[0]), int(rows[-1])
    level = 0.7 * np.median(prof[top:bot])
    mins = [y for y in range(top + 3, bot - 3)
            if prof[y] == prof[y - 3:y + 4].min() and prof[y] < level]
    groups = []
    for y in mins:
        if groups and y - groups[-1][-1] <= 3:
            groups[-1].append(y)
        else:
            groups.append([y])
    marks = [float(np.mean(g)) for g in groups]
    step = np.polyfit(np.arange(len(marks)), marks, 1)[0]
    return float(step / 0.10), marks


def _doubles(block, name):
    return [float(v) for v in re.findall(rf'name="{name}" type="double">([^<]+)', block)]


def tracker_points(xml):
    """The lab's hand-marked positions in a Tracker file: the clip (start frame, step),
    the scale (px per metre) and [(frame, x_px, y_px)] for the first point mass."""
    start = int(re.search(r'name="startframe" type="int">(\d+)', xml).group(1))
    step = int(re.search(r'name="stepsize" type="int">(\d+)', xml).group(1))
    scale = _doubles(xml, "xscale")[0]
    dt = _doubles(xml, "delta_t")[0] / 1000
    pm = xml[xml.index("tracker.PointMass"):]
    data = pm[pm.index('name="framedata"'):]
    pts = []
    for m in re.finditer(r'<property name="\[(\d+)\]" type="object">\s*<object class='
                         r'"org.opensourcephysics.cabrillo.tracker.PointMass\$FrameData">'
                         r'\s*<property name="x" type="double">([^<]+)</property>\s*'
                         r'<property name="y" type="double">([^<]+)</property>', data):
        pts.append((int(m.group(1)), float(m.group(2)), float(m.group(3))))
    return {"startframe": start, "stepsize": step, "pixels_per_metre": scale,
            "delta_t": dt, "points": pts}


if __name__ == "__main__":
    from ..env import footage
    for name in footage.manifest()["films"]:
        pics = footage.frames(name)
        print(name, len(pics), "pictures;", "stick: %.1f px per metre" % stick_scale(pics)[0])
        if footage.manifest()["films"][name].get("tracker"):
            t = tracker_points(footage.tracker_file(name))
            print("   Tracker:", {k: v for k, v in t.items() if k != "points"},
                  len(t["points"]), "points")
