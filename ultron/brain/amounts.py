"""Inventing amounts *between* numbers (fractions), and reasoning with them.

Ultron has two confirmed laws from the bakery:
  cake_balance: k pieces of a cake cut into n balance w whole cakes exactly when
                k = w groups of n
  recut:        cutting each piece of an n-cut into m gives pieces of an
                (n·m)-cut (it counts n·m of them per cake)

Reflecting, it imagines with those laws. One piece of a 3-cut balances no whole
number of cakes (not 0, not 1), yet 3 of them balance 1 cake exactly. So there are
amounts between its numbers. It decides to treat any pile of equal pieces
(count k, of a cake cut into n) as a number. Two piles are the same number when,
re-cut into the same kind of piece, they have the same count. Whole numbers are
just piles of pieces of a cake "cut into 1".

Everything below is worked out with Ultron's own laws: counts are combined with
its plus/minus/times laws (including its below-zero 'undo' rule), and kinds with
its recut law. No fraction arithmetic is built in.
"""

from .dsl import Overflow, evaluate
from .language import read_number, speak_number

KEY = "amounts:cake"


# ------------------------------------------------------------------ invention
def _balances(brain, pieces, cut, wholes):
    law = brain.library.get("cake_balance")
    try:
        return evaluate(law.expr, {"pieces": pieces, "cut": cut, "wholes": wholes},
                        brain.library)
    except Overflow:
        return None


def look_for_amounts(brain):
    if KEY in brain.inventions:
        return None
    if not brain.trusts("cake_balance") or not brain.trusts("recut"):
        return None
    # whole cakes are piles of "pieces of a cake cut into 1"
    if not all(_balances(brain, w, 1, w) for w in range(6)):
        return None
    for n in range(2, 7):
        no_whole = not any(_balances(brain, 1, n, w) for w in range(0, 4))
        if no_whole and _balances(brain, n, n, 1):
            story = (f"One piece of a cake cut into {n} balances no whole number of cakes: "
                     f"not 0, not 1. Yet {n} of them balance exactly 1 cake. So there are "
                     f"amounts *between* my numbers. I'll treat every pile of equal pieces "
                     f"(so many pieces of a cake cut into so many) as a number too. Two piles "
                     f"are the same number when, cut again into the same kind of piece, they "
                     f"have the same count. My whole numbers are piles of a cake 'cut into 1'.")
            inv = {"primitives": [], "lesson": brain.lesson, "story": story, "example": n}
            brain.inventions[KEY] = inv
            brain.note("invent", story)
            return inv
    return None


def invented(brain):
    return KEY in brain.inventions


# ------------------------------------------------------------ using its laws
def _law(brain, word):
    """The law Ultron bound to an operation word."""
    m = brain.vocab.get(word)
    return m[1] if m and m[0] == "op" else None


def _call(brain, law, a, b):
    return brain.library.call(law, a, b)


def _times(brain, a, b):
    return _call(brain, "groups", a, b)


def _recut(brain, n, m):
    return _call(brain, "recut", n, m)


def common(brain, x, y):
    """Re-cut two piles into the same kind of piece. Returns (count_x, count_y, kind)."""
    (k1, n1), (k2, n2) = x, y
    kind = _recut(brain, n1, n2)
    return _times(brain, k1, n2), _times(brain, k2, n1), kind


def same(brain, x, y):
    c1, c2, _ = common(brain, x, y)
    return c1 == c2


def simplest(brain, x):
    """The same amount written with the fewest pieces per cake."""
    k, n = x
    for d in range(1, n + 1):
        for c in range(0, abs(k) + 1):
            for cand in ((c, d), (-c, d)) if c else ((0, d),):
                if same(brain, cand, x):
                    return cand
    return x


def scale_compatible(brain, law):
    """Does this law work 'per kind of piece'? (law(x·d, y·d) == law(x, y)·d)"""
    try:
        return all(_call(brain, law, x * d, y * d) == _call(brain, law, x, y) * d
                   for x in range(0, 4) for y in range(0, 4) for d in range(1, 4))
    except Overflow:
        return False


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
    return None, f"my law '{law}' doesn't work piece by piece, so I can't use it on amounts"


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


def solve(brain, law, order, known, goal, unknown_first, max_cut=60):
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

    for d in range(1, max_cut + 1):
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
        # step out 1, 2, 4, 8... in the direction that closes the gap, until it is passed
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
