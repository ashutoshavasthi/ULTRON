"""Ultron's built-in primitives ("core knowledge") and its program language.

A law about discrete things (objects, piles, cups) is a small program.
Programs are nested tuples so they are hashable, comparable and easy to
save as JSON:

    ("var", name)                 an input the brain perceived
    ("const", value)              a constant (0, 1, or a number it has a name for)
    ("succ", e)                   one more than e
    ("pred", e)                   one less than e (never below 0)
    ("down", e)                   one step lower, with no floor (an *invented*
                                  primitive: only available once the brain has
                                  discovered a line that goes below zero)
    ("not", e) ("and", a, b)      logic
    ("eq", a, b) ("lt", a, b)     "same as" and "fewer than"
    ("call", law, a, b)           use a law already in the library
    ("call1", law, a)             use a one-input law (e.g. "tick" on a wheel)
    ("ite", c, a, b)              if c then a else b
    ("iter", F, n, x)             start at x and do F, n times
        F = ("succ",) | ("pred",) | ("down",) | ("call1", law) | ("call", law, t)
        where ("call", law, t)
        means "acc -> law(acc, t)"

These primitives are the only thing designed by hand. Addition,
subtraction, multiplication and place value are not here: the brain has to
discover them as programs built from these pieces.
"""

INT, BOOL = "int", "bool"

import contextlib

MAX_ITER = 2_000_000    # refuse to count further than this in one step
MAX_VALUE = 10 ** 9     # refuse to hold numbers bigger than this
_DEFAULT_LIMITS = (MAX_ITER, MAX_VALUE)


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
        # which step undoes which, as Ultron worked out by imagining with its laws:
        # "succ" -> ["down"], "merge" -> ["pay", "t_first"] (pay(t, acc) undoes merge(acc, t))
        self.inverses = {}
        self._memo = {}     # laws are pure functions: remember results already worked out
        # steps that come back to where they started after k repeats (found by reflection)
        self.cycles = {}

    def inverse_of(self, F):
        """The step that undoes F, if Ultron knows one."""
        if F[0] in ("succ", "down"):
            inv = self.inverses.get(F[0])
            return (inv[0],) if inv else None
        if F[0] == "call" and F[1] in self.inverses:
            law, order = self.inverses[F[1]]
            return ("call" if order == "acc_first" else "callr", law, F[2])
        return None

    def add(self, law):
        self.laws[law.name] = law
        self._memo = {}     # a replaced law may give different answers

    def get(self, name):
        return self.laws.get(name)

    def binary_int_laws(self):
        return [self.laws[k] for k in sorted(self.laws) if self.laws[k].is_binary_int]

    def unary_int_laws(self):
        return [self.laws[k] for k in sorted(self.laws)
                if self.laws[k].out_type == INT and len(self.laws[k].params) == 1]

    def call1(self, name, a):
        key = (name, a, len(self.inverses), len(self.cycles))
        if key in self._memo:
            return self._memo[key]
        law = self.laws[name]
        v = evaluate(law.expr, {law.params[0]: a}, self)
        self._memo[key] = v
        return v

    def call(self, name, a, b):
        key = (name, a, b, len(self.inverses))
        if key in self._memo:
            hit = self._memo[key]
            if hit is Overflow:
                raise Overflow()
            return hit
        law = self.laws[name]
        try:
            v = evaluate(law.expr, {law.params[0]: a, law.params[1]: b}, self)
        except Overflow:
            if MAX_ITER == _DEFAULT_LIMITS[0]:
                self._memo[key] = Overflow
            raise
        if MAX_ITER == _DEFAULT_LIMITS[0] or v is not None:
            self._memo[key] = v
        return v

    def __deepcopy__(self, memo):
        import copy
        new = Library()
        new.laws = copy.deepcopy(self.laws, memo)
        new.inverses = copy.deepcopy(self.inverses, memo)
        new.cycles = copy.deepcopy(self.cycles, memo)
        return new

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
    if tag == "down":
        return acc - 1
    if tag == "callr":
        return check(library.call(F[1], t, acc))
    if tag == "call1":
        return check(library.call1(F[1], acc))
    return check(library.call(F[1], acc, t))


def iterate(F, n, x, t, library):
    if F[0] == "call1" and F[1] in library.cycles:
        # on a cycle, k repeats change nothing, and going back = going on round
        n = n % library.cycles[F[1]]
    if n < 0:
        # doing something a below-zero number of times = undoing it that many times
        G = library.inverse_of(F)
        if G is None:
            raise Overflow()
        F, n = G, -n
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
    if tag == "down":
        return evaluate(expr[1], env, library) - 1
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
    if tag == "call1":
        return check(library.call1(expr[1], evaluate(expr[2], env, library)))
    if tag == "ite":
        return (evaluate(expr[2], env, library) if evaluate(expr[1], env, library)
                else evaluate(expr[3], env, library))
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
    if tag in ("succ", "pred", "down", "not"):
        return 1 + size(expr[1])
    if tag in ("and", "eq", "lt"):
        return 1 + size(expr[1]) + size(expr[2])
    if tag == "call":
        return 1 + size(expr[2]) + size(expr[3])
    if tag == "call1":
        return 1 + size(expr[2])
    if tag == "ite":
        return 1 + size(expr[1]) + size(expr[2]) + size(expr[3])
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
    if tag in ("succ", "pred", "down", "not"):
        return f"{tag}({show(expr[1])})"
    if tag in ("and", "eq", "lt"):
        return f"{tag}({show(expr[1])}, {show(expr[2])})"
    if tag == "call":
        return f"{expr[1]}({show(expr[2])}, {show(expr[3])})"
    if tag == "call1":
        return f"{expr[1]}({show(expr[2])})"
    if tag == "ite":
        return f"if {show(expr[1])} then {show(expr[2])} else {show(expr[3])}"
    if tag == "iter":
        F = expr[1]
        f = (f"{F[1]}(·, {show(F[2])})" if F[0] == "call"
             else F[1] if F[0] == "call1" else F[0])
        return f"repeat {show(expr[2])} times [{f}] starting from {show(expr[3])}"
    raise ValueError(tag)


def to_json(expr):
    return [to_json(e) if isinstance(e, tuple) else e for e in expr]


def from_json(data):
    return tuple(from_json(e) if isinstance(e, list) else e for e in data)
