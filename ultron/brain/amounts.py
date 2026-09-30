"""Inventing amounts *between* numbers (fractions), and reasoning with them.

From the bakery Ultron has a law saying when k pieces of a cake cut into n
balance w whole cakes. Shape discovery (invention.py) finds that walking by pieces
is a *finer* walk than walking by wholes, which is the invention.

Reflecting, it imagines with that law. One piece of a 3-cut balances no whole
number of cakes (not 0, not 1), yet 3 of them balance 1 cake exactly. So there are
amounts between its numbers. It decides to treat any pile of equal pieces
(count k, of a cake cut into n) as a number. Two piles are the same number when,
re-cut into the same kind of piece, they have the same count. Whole numbers are
just piles of pieces of a cake "cut into 1".

Everything below is worked out with Ultron's own laws: counts are combined with
its plus/minus/times laws (including its below-zero 'undo' rule), and kinds are
re-cut in imagination with the law it checked scales count and kind together. No
fraction arithmetic is built in.
"""

from .dsl import Overflow, evaluate
from .language import read_number, speak_number

# ------------------------------------------------------------------ invention
# The invention itself is a shape ("a finer line"), found by invention.py's shape
# discovery. This module is how Ultron reasons with the numbers it invented.

def record(brain):
    return next((inv for inv in brain.inventions.values()
                 if inv.get("shape") == "finer line"), None)


def invented(brain):
    return record(brain) is not None


def look_for_amounts(brain):
    """Kept for callers: the finer line is found by shape discovery now."""
    from .invention import look_for_shapes
    return None if invented(brain) else look_for_shapes(brain)


# ------------------------------------------------------------ using its laws
def _law(brain, word):
    """The law Ultron bound to an operation word."""
    m = brain.vocab.get(word)
    return m[1] if m and m[0] == "op" else None


def _call(brain, law, a, b):
    return brain.library.call(law, a, b)


def _scale(brain):
    rec = record(brain)
    return rec["scale"] if rec else "groups"


def _times(brain, a, b):
    return _call(brain, _scale(brain), a, b)


def _recut(brain, n, m):
    """Cutting each piece of an n-cut into m: done in imagination with the law that
    Ultron checked scales count and kind together."""
    return _call(brain, _scale(brain), n, m)


def common(brain, x, y):
    """Re-cut two piles into the same kind of piece. Returns (count_x, count_y, kind)."""
    (k1, n1), (k2, n2) = x, y
    kind = _recut(brain, n1, n2)
    return _times(brain, k1, n2), _times(brain, k2, n1), kind


def same(brain, x, y):
    c1, c2, _ = common(brain, x, y)
    return c1 == c2


def _fits_evenly(brain, d, n):
    """Do some whole number q of d-pieces make exactly n? (q·d = n, found by halving)"""
    lo, hi = 1, n
    while lo <= hi:
        q = (lo + hi) // 2
        got = _times(brain, q, d)
        if got == n:
            return True
        if got < n:
            lo = q + 1
        else:
            hi = q - 1
    return False


def simplest(brain, x):
    """The same amount written with the fewest pieces per cake. Only kinds of piece
    that fit evenly into the n-cut can give the same amount; for each of those it asks
    whether some count c of them is the same as x (more pieces always weigh more, so
    it finds c by halving)."""
    k, n = x
    for d in range(1, n + 1):
        if d != n and not _fits_evenly(brain, d, n):
            continue
        target = _times(brain, k, d)
        lo, hi = -abs(k), abs(k)
        while lo <= hi:
            c = (lo + hi) // 2
            got = _times(brain, c, n)
            if got == target:
                return (c, d)
            if got < target:
                lo = c + 1
            else:
                hi = c - 1
    return x


def scale_compatible(brain, law):
    """Does this law work 'per kind of piece'? (law(x·d, y·d) == law(x, y)·d)"""
    try:
        return all(_call(brain, law, x * d, y * d) == _call(brain, law, x, y) * d
                   for x in range(0, 4) for y in range(0, 4) for d in range(1, 4))
    except Overflow:
        return False


MAX_REPEATS = 2000


def _plus_one(brain, acc, sign):
    law = "merge" if sign > 0 else "pay"
    if law not in brain.library:
        return None
    return apply_law(brain, law, acc, (1, 1)) if sign > 0 else apply_law(brain, law, (1, 1), acc)


def evaluate_amount(brain, expr, env):
    """Run one of Ultron's own programs with amounts instead of whole numbers.
    Repeating is only possible a whole number of times; repeating a step a
    below-zero number of times means undoing it (finding what the step turns into
    the current amount)."""
    tag = expr[0]
    if tag == "var":
        return env[expr[1]]
    if tag == "const" and isinstance(expr[1], int) and not isinstance(expr[1], bool):
        return (expr[1], 1)
    if tag == "call":
        a = evaluate_amount(brain, expr[2], env)
        b = evaluate_amount(brain, expr[3], env)
        return None if a is None or b is None else apply_law(brain, expr[1], a, b)
    if tag == "succ":
        v = evaluate_amount(brain, expr[1], env)
        return None if v is None else _plus_one(brain, v, 1)
    if tag == "down":
        v = evaluate_amount(brain, expr[1], env)
        return None if v is None else _plus_one(brain, v, -1)
    if tag == "iter":
        n = evaluate_amount(brain, expr[2], env)
        acc = evaluate_amount(brain, expr[3], env)
        if n is None or acc is None:
            return None
        n = simplest(brain, n)
        if n[1] != 1 or abs(n[0]) > MAX_REPEATS:
            return None             # I can only repeat something a whole number of times
        F = expr[1]
        t = evaluate_amount(brain, F[2], env) if F[0] == "call" else None
        for _ in range(abs(n[0])):
            if F[0] == "call" and n[0] > 0:
                acc = apply_law(brain, F[1], acc, t)
            elif F[0] == "call":
                acc = solve(brain, F[1], "xy", t, acc, unknown_first=True)   # undo one step
            elif F[0] in ("succ", "down"):
                up = (F[0] == "succ") == (n[0] > 0)
                acc = _plus_one(brain, acc, 1 if up else -1)
            else:
                return None
            if acc is None:
                return None
        return acc
    return None


def apply_law(brain, law, a, b):
    """law(a, b) on amounts, worked out with Ultron's own laws."""
    if law == "groups":
        (k1, n1), (k2, n2) = a, b
        return (_times(brain, k1, k2), _recut(brain, n1, n2))
    if scale_compatible(brain, law):
        c1, c2, kind = common(brain, a, b)
        return (_call(brain, law, c1, c2), kind)
    rule = brain.library.get(law)
    if rule is None or len(rule.params) != 2:
        return None
    return evaluate_amount(brain, rule.expr, {rule.params[0]: a, rule.params[1]: b})


def combine(brain, law, x, y, order):
    """Apply one of Ultron's laws to two amounts. Returns (amount, explanation)."""
    a, b = (x, y) if order == "xy" else (y, x)
    if law == "groups":
        # "a groups of b": cut b into a's n equal shares (recut), take a's k of them
        (k1, n1), (k2, n2) = a, b
        res = (_times(brain, k1, k2), _recut(brain, n1, n2))
        how = (f"{show(brain, a)} groups of {show(brain, b)}: I cut every piece of "
               f"{show(brain, b)} again into {n1} (my recut law) and take {k1} of each set")
        return res, how
    if scale_compatible(brain, law):
        c1, c2, kind = common(brain, a, b)
        res = (_call(brain, law, c1, c2), kind)
        how = (f"I cut both piles into pieces of a cake cut into {kind} (my recut law): "
               f"{c1} and {c2} such pieces, then use my law '{law}' on the counts")
        return res, how
    res = apply_law(brain, law, a, b)
    if res is None:
        return None, f"I can't run my law '{law}' on these amounts"
    return res, (f"I ran my law '{law}' step by step on amounts, using what I know about "
                 f"adding, taking away and multiplying pieces")


# --------------------------------------------------------------- reading/writing
def separator(brain):
    for k, m in brain.vocab.items():
        if k.startswith("infix:") and m[0] == "amount_sep":
            return k[len("infix:"):]
    return None


def bind_separator(brain, examples):
    """examples: [(what the Trainer wrote, (count, kind) Ultron sees)], e.g. ('2/3', (2, 3))."""
    found = None
    for said, (k, n) in examples:
        for i in range(1, len(said) - 1):
            left, sep, right = said[:i], said[i], said[i + 1:]
            if read_number(brain, left)[0] == k and read_number(brain, right)[0] == n:
                if found not in (None, sep):
                    return None
                found = sep
                break
        else:
            return None
    brain.bind("infix:" + found, ("amount_sep",))
    brain.note("word", f"'a{found}b' means a pieces of a cake cut into b")
    return found


def read_amount(brain, token):
    sep = separator(brain)
    if sep and sep in token and not token.startswith(sep):
        left, right = token.split(sep, 1)
        k, _ = read_number(brain, left)
        n, _ = read_number(brain, right)
        if k is None or n is None:
            return None, f"I can't read '{token}'"
        if n <= 0:
            return None, (f"'{token}' would mean cutting a cake into {n} pieces; I have never "
                          f"seen that and can't imagine it")
        return (k, n), f"'{token}' is {k} piece{'' if abs(k) == 1 else 's'} of a cake cut into {n}"
    v, why = read_number(brain, token)
    return ((v, 1), why) if v is not None else (None, why)


def show(brain, x):
    k, n = simplest(brain, x)
    if n == 1:
        return speak_number(brain, k) or str(k)
    sep = separator(brain) or "/"
    return f"{speak_number(brain, k) or k}{sep}{speak_number(brain, n) or n}"


# ------------------------------------------------------------ questions
def bind_division(brain, token, demos):
    """demos: [(a, b, share)] from sharing a cakes between b people. Find which of its
    operations, run backwards, the word means: b <op> share == a in every demo."""
    # prefer spoken words ('times') over marks ('×') when describing the meaning
    for word in sorted(brain.vocab, key=lambda w: (not w.isalpha(), w)):
        m = brain.vocab[word]
        if m[0] != "op":
            continue
        ok = True
        for a, b, share in demos:
            res, _ = combine(brain, m[1], (b, 1), share, m[2])
            if res is None or not same(brain, res, (a, 1)):
                ok = False
                break
        if ok:
            brain.bind(token, ("inv_op", m[1], m[2], word))
            brain.note("word", f"'{token}' asks: what, {word} the second number, gives the "
                               f"first? (checked on all {len(demos)} sharings)")
            return brain.vocab[token]
    return None


SOLVE_EFFORT = 1_500_000     # how much counting it will spend looking for a pile
LAST_CUT = [0]               # the finest cut the last search reached (for honest answers)


def solve(brain, law, order, known, goal, unknown_first, max_cut=None):
    """Find the simplest amount x with law(x, known) == goal (or law(known, x)).

    For each kind of piece (cut into 1, 2, 3, ...) it compares the result with the
    goal as a count of common pieces. It checks whether putting in more pieces
    changes the result at all: if not (e.g. zero groups), no amount of that kind can
    work. If it does, the right count is found by halving the range. Every answer
    is checked exactly before it is given."""
    def gap(x):
        pair = (x, known) if unknown_first else (known, x)
        res, _ = combine(brain, law, pair[0], pair[1], order)
        if res is None:
            return None
        c1, c2, _ = common(brain, res, goal)
        return c1 - c2

    from . import dsl
    if max_cut is None:
        # enough kinds of piece to hold any answer built from these two amounts
        max_cut = max(60, goal[1] * max(1, abs(known[0])) * known[1])
    start = dsl.STEPS[0]
    last = None
    for d in range(1, max_cut + 1):
        LAST_CUT[0] = d
        if dsl.STEPS[0] - start > SOLVE_EFFORT:
            break                   # looking further would cost more counting than it's worth
        try:
            g0, g1 = gap((0, d)), gap((1, d))
        except Overflow:
            continue
        if g0 is None or g1 is None:
            return None
        if g0 == 0:
            return (0, 1)
        if g1 == g0:
            continue            # more pieces change nothing: no count of this kind works
        up = g1 > g0
        lo = hi = None
        if last is not None:
            # the answer lay between two piles of the last kind of piece; for this kind
            # it must lie between the same two amounts, so only look there
            a, b_, e = last
            near, far = (a * d) // e - 1, -((-b_ * d) // e) + 1
            try:
                gn, gf = gap((near, d)), gap((far, d))
                if gn is not None and gf is not None and (gn <= 0 <= gf or gf <= 0 <= gn):
                    lo, hi = near, far
            except Overflow:
                pass
        if lo is None:
            # step out 1, 2, 4, 8... in the direction that closes the gap, until passed
            direction = 1 if (g0 < 0) == up else -1
            near, far = 0, direction
            try:
                while abs(far) <= 10 ** 6:
                    g = gap((far, d))
                    if g == 0 or (g > 0) != (g0 > 0):
                        break
                    near, far = far, far * 2
                else:
                    continue
            except Overflow:
                continue
            lo, hi = min(near, far), max(near, far)
        while lo <= hi:
            mid = (lo + hi) // 2
            try:
                g = gap((mid, d))
            except Overflow:
                break
            if g == 0:
                return simplest(brain, (mid, d))
            if (g < 0) == up:
                lo = mid + 1
            else:
                hi = mid - 1
        if hi < lo:
            last = (min(hi, lo), max(hi, lo), d)
    return None


def arithmetic(brain, tokens):
    """Questions whose numbers or answers may be amounts. Returns Answer-like tuple
    (value, text, steps) or None if the question isn't of this shape."""
    steps = []
    value, why = read_amount(brain, tokens[0])
    if value is None:
        return None, why, steps
    steps.append(why)
    i = 1
    while i < len(tokens):
        op = brain.vocab.get(tokens[i])
        if not op or op[0] not in ("op", "inv_op") or i + 1 >= len(tokens):
            return None, f"I don't know what '{tokens[i]}' means as an operation", steps
        right, why = read_amount(brain, tokens[i + 1])
        if right is None:
            return None, why, steps
        steps.append(why)
        if op[0] == "op":
            res, how = combine(brain, op[1], value, right, op[2])
            if res is None:
                return None, how, steps
            steps.append(f"'{tokens[i]}': {how}")
        else:
            res = solve(brain, op[1], op[2], right, value, unknown_first=False)
            if res is None:
                return None, (f"no amount, {op[3]} {show(brain, right)}, gives "
                              f"{show(brain, value)}"), steps
            steps.append(f"'{tokens[i]}' asks what, {op[3]} {show(brain, right)}, gives "
                         f"{show(brain, value)}; I looked through cakes cut into 1, 2, 3... "
                         f"pieces and found {show(brain, res)}")
        value = res
        i += 2
    return value, show(brain, value), steps
