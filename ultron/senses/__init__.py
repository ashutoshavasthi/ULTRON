"""Ultron's senses (Phase 3): a camera that gives only pixels, and eyes it learns.

numpy is imported only here, so lessons 0-18 still run without it. One thread keeps
every sum in the same order, so training the eyes is deterministic.
"""

import os

for _var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_var, "1")
