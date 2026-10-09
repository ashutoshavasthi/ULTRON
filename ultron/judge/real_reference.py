"""The Judge's reference for the real microscope video: trackpy, the scientists' own
tool, run exactly as in its walkthrough notebook. Ultron never sees this.

Not imported by Ultron. Regenerate with (trackpy in its own environment):
    python ultron/judge/real_reference.py data/real/bulk_water \
        ultron/env/data/real/bulk_water_trackpy.json
"""
import glob, json, sys
import numpy as np, pandas as pd, trackpy as tp
from PIL import Image
src = sys.argv[1]
files = sorted(glob.glob(src + "/bulk_water_*.png"))
frames = [np.array(Image.open(f).convert("RGB"))[:, :, 0].astype(float) for f in files]
tp.quiet()
f = tp.batch(frames, 11, invert=True, minmass=20, processes=1)
t = tp.link(f, 5, memory=3)
t1 = tp.filter_stubs(t, 25)
d = tp.compute_drift(t1)
tm = tp.subtract_drift(t1.copy(), d)
em = tp.emsd(tm, 100 / 285., 24)
fit = tp.utils.fit_powerlaw(em, plot=False)
out = {"frames": len(frames), "tracks": int(tm["particle"].nunique()),
       "emsd_lag_s": [float(x) for x in em.index[:40]], "emsd_um2": [float(x) for x in em.values[:40]],
       "n": float(fit["n"].iloc[0]), "A": float(fit["A"].iloc[0]),
       "detections": {str(i): f[f.frame == i][["x", "y"]].round(2).values.tolist()
                      for i in range(0, len(frames), 25)}}
json.dump(out, open(sys.argv[2], "w"))
print(out["frames"], out["tracks"], "n", round(out["n"], 3), "A", round(out["A"], 3), "D=A/4", round(out["A"] / 4, 3))
print("detections per frame", [len(v) for v in out["detections"].values()])
