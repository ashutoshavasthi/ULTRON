"""Ultron's built-in primitives ("core knowledge") and its program language.

A law about discrete things (objects, piles, cups) is a small program.
Programs are nested tuples so they are hashable, comparable and easy to
save as JSON:

    ("var", name)                 an input the brain perceived
    ("const", value)              a constant (0, 1, or a number it has a name for)
    ("succ", e)                   one more than e
    ("pred", e)                   one less than e (never below 0)
    ("not", e) ("and", a, b)      logic
    ("eq", a, b) ("lt", a, b)     "same as" and "fewer than"
    ("call", law, a, b)           use a law already in the library
    ("iter", F, n, x)             start at x and do F, n times
        F = ("succ",) | ("pred",) | ("call", law, t)   where ("call", law, t)
        means "acc -> law(acc, t)"

These primitives are the only thing designed by hand. Addition,
subtraction, multiplication and place value are not here: the brain has to
discover them as programs built from these pieces.
"""

INT, BOOL = "int", "bool"

import contextlib

MAX_ITER = 2_000_000    # refuse to count further than this in one step
MAX_VALUE = 10 ** 9     # refuse to hold numbers bigger than this


@contextlib.contextmanager
def limits(max_iter, max_value):
    """Tighter limits while imagining many candidate programs at once."""
    global MAX_ITER, MAX_VALUE
    saved = MAX_ITER, MAX_VALUE
    MAX_ITER, MAX_VALUE = max_iter, max_value
    try:
        yield
    finally:
        MAX_ITER, MAX_VALUE = saved


class Overflow(Exception):
    """A program tried to count further than the brain is willing to."""


def check(v):
    if isinstance(v, int) and not isinstance(v, bool) and v > MAX_VALUE:
        raise Overflow()
    return v


class Law:
    """A confirmed discrete law, usable as a building block by later searches."""

    def __init__(self, name, params, expr, out_type, provenance=None):
        self.name = name
        self.params = list(params)
        self.expr = expr
        self.out_type = out_type
        self.provenance = provenance or {}

    @property
    def is_binary_int(self):
        return self.out_type == INT and len(self.params) == 2

    def to_json(self):
        return {"name": self.name, "params": self.params, "expr": to_json(self.expr),
                "out_type": self.out_type, "provenance": self.provenance}

    @classmethod
    def from_json(cls, d):
        return cls(d["name"], d["params"], from_json(d["expr"]), d["out_type"], d.get("provenance"))


class Library:
    """Laws the brain has confirmed. Each one becomes a single building block."""

    def __init__(self):
        self.laws = {}

    def add(self, law):
        self.laws[law.name] = law

    def get(self, name):
        return self.laws.get(name)

    def binary_int_laws(self):
        return [self.laws[k] for k in sorted(self.laws) if self.laws[k].is_binary_int]

    def call(self, name, a, b):
        law = self.laws[name]
        return evaluate(law.expr, {law.params[0]: a, law.params[1]: b}, self)

    def __contains__(self, name):
        return name in self.laws

    def __len__(self):
        return len(self.laws)


def apply_step(F, acc, t, library):
    """One application of an iteration step F to an accumulator."""
    tag = F[0]
    if tag == "succ":
        return check(acc + 1)
    if tag == "pred":
        return acc - 1 if acc > 0 else 0
    return check(library.call(F[1], acc, t))


def iterate(F, n, x, t, library):
    if n > MAX_ITER:
        raise Overflow()
    acc = x
    for _ in range(n):
        acc = apply_step(F, acc, t, library)
    return acc


def evaluate(expr, env, library):
    tag = expr[0]
    if tag == "var":
        return env[expr[1]]
    if tag == "const":
        return expr[1]
    if tag == "succ":
        return check(evaluate(expr[1], env, library) + 1)
    if tag == "pred":
        v = evaluate(expr[1], env, library)
        return v - 1 if v > 0 else 0
    if tag == "not":
        return not evaluate(expr[1], env, library)
    if tag == "and":
        return evaluate(expr[1], env, library) and evaluate(expr[2], env, library)
    if tag == "eq":
        return evaluate(expr[1], env, library) == evaluate(expr[2], env, library)
    if tag == "lt":
        return evaluate(expr[1], env, library) < evaluate(expr[2], env, library)
    if tag == "call":
        return check(library.call(expr[1], evaluate(expr[2], env, library),
                                  evaluate(expr[3], env, library)))
    if tag == "iter":
        F = expr[1]
        t = evaluate(F[2], env, library) if F[0] == "call" else None
        return iterate(F, evaluate(expr[2], env, library), evaluate(expr[3], env, library), t, library)
    raise ValueError(f"unknown program node {tag!r}")


def safe_evaluate(expr, env, library):
    try:
        return evaluate(expr, env, library)
    except Overflow:
        return None


def size(expr):
    """Description length of a program: one unit per node (library laws cost 1)."""
    tag = expr[0]
    if tag in ("var", "const"):
        return 1
    if tag in ("succ", "pred", "not"):
        return 1 + size(expr[1])
    if tag in ("and", "eq", "lt"):
        return 1 + size(expr[1]) + size(expr[2])
    if tag == "call":
        return 1 + size(expr[2]) + size(expr[3])
    if tag == "iter":
        F = expr[1]
        f_cost = 1 + (size(F[2]) if F[0] == "call" else 0)
        return 1 + f_cost + size(expr[2]) + size(expr[3])
    raise ValueError(tag)


def show(expr):
    """Readable form of a program."""
    tag = expr[0]
    if tag == "var":
        return expr[1]
    if tag == "const":
        return str(expr[1]).lower() if isinstance(expr[1], bool) else str(expr[1])
    if tag in ("succ", "pred", "not"):
        return f"{tag}({show(expr[1])})"
    if tag in ("and", "eq", "lt"):
        return f"{tag}({show(expr[1])}, {show(expr[2])})"
    if tag == "call":
        return f"{expr[1]}({show(expr[2])}, {show(expr[3])})"
    if tag == "iter":
        F = expr[1]
        f = F[0] if F[0] != "call" else f"{F[1]}(·, {show(F[2])})"
        return f"repeat {show(expr[2])} times [{f}] starting from {show(expr[3])}"
    raise ValueError(tag)


def to_json(expr):
    return [to_json(e) if isinstance(e, tuple) else e for e in expr]


def from_json(data):
    return tuple(from_json(e) if isinstance(e, list) else e for e in data)
