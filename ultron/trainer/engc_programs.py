"""The Trainer's Engc programs: expressions it writes for lesson 100 and the Judge's exam.

The Trainer knows Engc (it is the teacher, and the Judge is the examiner); Ultron does
not: it only ever sees a program's text and what the sandbox printed. The tables below
never reach the brain.
"""

import random

from ..code import sandbox

# what each operator does and how tightly it groups, in Engc (the teacher's knowledge)
BINARY = {
    "PLUS": ("+", 5), "MINUS": ("-", 5), "TIMES": ("*", 6), "MODULO": ("%", 6),
    "RAISED TO": ("**", 8),
    "IS GREATER THAN": (">", 4), "IS LESS THAN": ("<", 4), "IS EQUAL TO": ("==", 4),
    "IS AT LEAST": (">=", 4), "IS AT MOST": ("<=", 4), "IS NOT": ("!=", 4),
    "AND": (None, 2), "OR": (None, 1),
}
UNARY = {"MINUS": ("-", 7), "NOT": (None, 3)}
RIGHT = {8}                                     # the levels that chain from the right
INT_OPS = ["PLUS", "MINUS", "TIMES", "MODULO", "RAISED TO"]
COMPARE = ["IS GREATER THAN", "IS LESS THAN", "IS EQUAL TO", "IS AT LEAST", "IS AT MOST",
           "IS NOT"]
PY = {"PLUS": "+", "MINUS": "-", "TIMES": "*", "MODULO": "%", "RAISED TO": "**",
      "IS GREATER THAN": ">", "IS LESS THAN": "<", "IS EQUAL TO": "==", "IS AT LEAST": ">=",
      "IS AT MOST": "<=", "IS NOT": "!=", "AND": "and", "OR": "or"}
BIG = 10 ** 12


class Reject(Exception):
    pass


def value(tree):
    """The teacher's own working-out, with the exam's rules about operands."""
    kind = tree[0]
    if kind == "num":
        return tree[1]
    if kind == "un":
        v = value(tree[2])
        return -v if tree[1] == "MINUS" else (not v)
    a, b = value(tree[2]), value(tree[3])
    op = tree[1]
    if op == "MODULO" and (a < 0 or b < 1):
        raise Reject()
    if op == "RAISED TO" and (not 0 <= b <= 3 or abs(a) > 30):
        raise Reject()
    v = eval(f"a {PY[op]} b", {"a": a, "b": b})     # noqa: S307 - the teacher's own arithmetic
    if isinstance(v, int) and not isinstance(v, bool) and abs(v) > BIG:
        raise Reject()
    return v


def level(tree):
    if tree[0] == "num":
        return 99
    return (UNARY if tree[0] == "un" else BINARY)[tree[1]][1]


def gen(rng, want, n, top):
    """A random typed expression tree with n operators and numbers up to top."""
    if n == 0:
        if want != "int":
            raise Reject()
        return ("num", rng.randint(0, top))
    if want == "int":
        op = rng.choice(INT_OPS + ["NEG"])
        if op == "NEG":
            return ("un", "MINUS", gen(rng, "int", n - 1, top))
        if op == "RAISED TO":
            return ("bin", op, gen(rng, "int", n - 1, min(top, 30)), ("num", rng.randint(0, 3)))
        left = rng.randint(0, n - 1)
        return ("bin", op, gen(rng, "int", left, top), gen(rng, "int", n - 1 - left, top))
    choices = ["CMP"] * 3 + (["NOT"] if n >= 2 else []) + (["AND", "OR"] if n >= 3 else [])
    op = rng.choice(choices)
    if op == "NOT":
        return ("un", "NOT", gen(rng, "bool", n - 1, top))
    if op == "CMP":
        left = rng.randint(0, n - 1)
        return ("bin", rng.choice(COMPARE), gen(rng, "int", left, top),
                gen(rng, "int", n - 1 - left, top))
    left = rng.randint(1, n - 2)
    return ("bin", op, gen(rng, "bool", left, top), gen(rng, "bool", n - 1 - left, top))


def render(tree, rng, symbols=0.5, extra=0.0):
    """The program's words. Brackets wherever the grouping needs them, sometimes more."""
    def spell(op, unary):
        sym = (UNARY if unary else BINARY)[op][0]
        return [sym] if sym and rng.random() < symbols else op.split()

    def wrap(child, toks, need, root=False):
        if child[0] != "num" and (need or (not root and rng.random() < extra)):
            return ["("] + toks + [")"]
        return toks

    def go(t, root=False):
        if t[0] == "num":
            return [str(t[1])]
        if t[0] == "un":
            lu = UNARY[t[1]][1]
            c = t[2]
            return spell(t[1], True) + wrap(c, go(c), level(c) <= lu)
        lp = BINARY[t[1]][1]
        left, right = t[2], t[3]
        need_l = level(left) < lp or (level(left) == lp and lp in RIGHT)
        need_r = level(right) < lp or (level(right) == lp and lp not in RIGHT)
        return wrap(left, go(left), need_l) + spell(t[1], False) + wrap(right, go(right), need_r)

    return ["PRINT"] + go(tree, root=True) + ["."]


def program(rng, n_ops, top, want=None, symbols=0.5, extra=0.0, tries=500):
    """(program text, printed): a random program whose printed answer the sandbox and the
    teacher's own working-out agree on."""
    for _ in range(tries):
        w = want or ("int" if rng.random() < 0.6 else "bool")
        try:
            tree = gen(rng, w, n_ops, top)
            v = value(tree)
        except (Reject, ZeroDivisionError, OverflowError):
            continue
        text = " ".join(render(tree, rng, symbols, extra))
        out = sandbox.run(text)
        if out["ok"] and out["printed"] == [str(v)]:
            return text, out["printed"]
    raise RuntimeError("could not write a program")


def one_op(rng, words, unary=False, top=20):
    """A one-operator program for a phrase (word or symbol), as the Trainer shows it."""
    for _ in range(200):
        if unary:
            if words in ("NOT",):
                cmp_ = rng.choice(COMPARE)
                a, b = rng.randint(0, top), rng.randint(0, top)
                text = f"PRINT NOT {a} {cmp_} {b} ."
            else:
                text = f"PRINT {words} {rng.randint(0, top)} ."
        elif words in ("AND", "OR"):
            parts = []
            for _ in range(2):
                parts.append(f"{rng.randint(0, top)} {rng.choice(COMPARE)} {rng.randint(0, top)}")
            text = f"PRINT {parts[0]} {words} {parts[1]} ."
        else:
            a, b = rng.randint(0, top), rng.randint(0, top)
            if words in ("MODULO", "%"):
                b = rng.randint(1, top)
            if words in ("RAISED TO", "**"):
                a, b = rng.randint(0, 10), rng.randint(0, 3)
            text = f"PRINT {a} {words} {b} ."
        out = sandbox.run(text)
        if out["ok"]:
            return text, out["printed"]
    raise RuntimeError("could not write a program")


def bracketed(rng, top=20):
    """A program whose brackets change the answer: (a P b) Q c or a P (b Q c)."""
    ops = ["PLUS", "MINUS", "TIMES"]
    for _ in range(200):
        p, q = rng.choice(ops), rng.choice(ops)
        a, b, c = (rng.randint(0, top) for _ in range(3))
        if rng.random() < 0.5:
            text = f"PRINT ( {a} {p} {b} ) {q} {c} ."
            other = f"PRINT {a} {p} {b} {q} {c} ."
        else:
            text = f"PRINT {a} {p} ( {b} {q} {c} ) ."
            other = f"PRINT {a} {p} {b} {q} {c} ."
        out, plain = sandbox.run(text), sandbox.run(other)
        if out["ok"] and plain["ok"] and out["printed"] != plain["printed"]:
            return text, out["printed"]
    raise RuntimeError("could not write a program")


def exam_programs(seed, n=200, ops=(3, 6), top=999):
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        text, printed = program(rng, rng.randint(*ops), top, extra=0.15)
        if all(text != t for t, _ in out):
            out.append((text, printed))
    return out
