"""C4: Ultron's own code (docs/STAGE_CODE_PLAN.md, "C4 in detail").

The Trainer's side only: which of Ultron's own functions it studies (the fixed list, by
the rule in the plan), what inputs it may run them on, and the held-out inputs of the
exam. The truth is what each function returns when run with the trained brain. Ultron
never sees this file.
"""

import random

# (module, function, what each input is): "n" a number, "amount" a (count, kind) pair
FUNCTIONS = [
    ("dsl", "check", ("n",)),
    ("amounts", "_times", ("n", "n")),
    ("amounts", "_recut", ("n", "n")),
    ("amounts", "common", ("amount", "amount")),
    ("amounts", "same", ("amount", "amount")),
    ("amounts", "_fits_evenly", ("n", "n")),
    ("amounts", "_kinds_that_fit", ("n",)),
    ("amounts", "simplest", ("amount",)),
    ("amounts", "_simplest", ("n", "n")),
    ("amounts", "_plus_one", ("amount", "n")),
]
PER_FUNCTION = 50       # held-out inputs for each
RUNS = 20               # runs Ultron may make of each


def name(f):
    return f"{f[0]}.{f[1]}"


def function(f):
    """The real function, taking a brain first when it needs one."""
    from ..brain import amounts, dsl
    mod = {"dsl": dsl, "amounts": amounts}[f[0]]
    fn = getattr(mod, f[1])
    if f[0] == "dsl":
        return lambda brain, *args: fn(*args)
    return fn


def run(brain, f, args):
    """What the function returns (rows as tuples), or ("fails",) if it fails."""
    try:
        out = function(f)(brain, *args)
    except Exception:  # noqa: BLE001 - a failure is an outcome too
        return ("fails",)
    return tuple(out) if isinstance(out, list) else out


def lesson_range(f, rng):
    """One input of the kind Ultron may choose while running f (lesson ranges)."""
    fn = f[1]
    if fn == "_fits_evenly":
        return (rng.randint(1, 12), rng.randint(1, 30))
    if fn == "_kinds_that_fit":
        return (rng.randint(1, 30),)
    if fn == "_plus_one":
        return ((rng.randint(0, 12), rng.randint(1, 12)), rng.choice((-1, 0, 1)))
    if fn in ("check", "_times", "_recut"):
        return tuple(rng.randint(0, 12) for _ in f[2])
    if fn == "_simplest":
        return (rng.randint(0, 12), rng.randint(1, 12))
    return tuple((rng.randint(0, 12), rng.randint(1, 12)) for _ in f[2])


def _held_out_one(f, rng, i):
    fn = f[1]
    r = rng.randint
    if fn == "check":
        return (r(21, 10 ** 6),)
    if fn in ("_times", "_recut"):
        return (r(13, 300), r(13, 300))
    if fn == "common":
        return ((r(13, 99), r(13, 99)), (r(13, 99), r(13, 99)))
    if fn == "same":
        x = (r(13, 99), r(13, 99))
        if i % 2 == 0:
            k = r(2, 9)
            return (x, (x[0] * k, x[1] * k))
        return (x, (r(13, 99), r(13, 99)))
    if fn == "_fits_evenly":
        d = r(2, 50)
        if i % 2 == 0:
            return (d, d * r(-(-50 // d), 2000 // d))
        return (d, r(50, 2000))
    if fn == "_kinds_that_fit":
        return (r(31, 500),)
    if fn in ("simplest", "_simplest"):
        k = r(2, 9)
        x = (r(13, 99) * k, r(13, 99) * k)
        return (x,) if fn == "simplest" else x
    if fn == "_plus_one":
        return ((r(13, 99), r(13, 99)), rng.choice((-1, 0, 1)))
    raise ValueError(fn)


def held_out(seed):
    """{function name: [inputs, ...]} for the exam (seed 7007), PER_FUNCTION each."""
    rng = random.Random(seed)
    return {name(f): [_held_out_one(f, rng, i) for i in range(PER_FUNCTION)]
            for f in FUNCTIONS}


def source():
    """The Python source Ultron is given to read in C4 (b): the three files, as text."""
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[1] / "brain"
    return {f: (root / f).read_text() for f in ("dsl.py", "amounts.py", "columns.py")}
