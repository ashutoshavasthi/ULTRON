# Ultron on Kaggle (ARC Prize)

ARC Prize's official competition runs offline on Kaggle: no internet, a fixed CPU/GPU
budget. Ultron needs neither a GPU nor a network, only Python 3 and numpy.

## Submitting (done by a person; Ultron cannot reach Kaggle)

1. Make a Kaggle **dataset** from this repository (zip the `ultron/` folder and the
   `brain/arc_library.json` file, keeping their paths).
2. Create a notebook in the ARC Prize competition, add the dataset and the competition
   data, turn the internet **off**, and run one cell:

   ```python
   import sys, shutil
   shutil.copytree("/kaggle/input/ultron/ultron", "/kaggle/working/ultron")
   shutil.copytree("/kaggle/input/ultron/brain", "/kaggle/working/brain")
   sys.path.insert(0, "/kaggle/working")
   from ultron.arc.kaggle import submit
   import glob
   challenges = glob.glob("/kaggle/input/arc-prize-*/arc-agi_test_challenges.json")[0]
   submit.main([challenges, "/kaggle/working/submission.json", "--workers", "4"])
   ```

3. Submit `submission.json`. `submission_programs.json` beside it lists, for every task,
   the program Ultron used: every answer can be read and checked.

## Checking it locally first

```
python -m ultron.arc.kaggle.check
```

builds a challenges file in the competition's format from the public **training** split,
runs `submit.py` on it, and scores the result with the official rule, so the package is
tested end to end without touching the evaluation split.

The same seeds, the same budget (counted in operations, not seconds) and the same
answers on any machine: the Kaggle score for a given task set is reproducible here.
