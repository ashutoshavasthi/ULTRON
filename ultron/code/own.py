"""C4 (a): Ultron's own code, watched from outside (lesson 104).

Ultron runs one of its own functions on inputs it chooses (at most 20 runs) and finds a
law in its own program language for what comes back. Nothing about any particular
function is written here; what it brings:

  * an input that is a pair (an amount: count and kind) is two places, one number each;
    an answer that is a short row of the same length every time is one law per place,
    and a place it has found can help explain the others;
  * its ordinary law search, with undoing a law ("the number q with law(q, a) = b, or
    nothing") and asking whether there is something at all;
  * when the answer is one of a row of numbers counted out (1, 2, ... up to an input):
    which ones are kept, or which one comes first, is a test it finds by the same search;
  * when one input takes only a few values and no single law fits: a law for each value,
    and a test that tells them apart;
  * every law it settles on becomes a building block for the next function (in its own
    copy of the library, so lessons before this one never see them).
"""

import copy
import random

from ..brain.dsl import BOOL, INT, LIST, MAYBE, Law, Overflow, evaluate, from_json, show, \
    to_json
from ..brain.synth import synthesize

RUNS = 20
CONFIRM = 3             # test runs its law must predict right before it trusts it
RIVALS = 4              # other laws that fit about as well, kept to choose experiments
MAX_PLACES = 4          # a row this short, always the same length, is a few places
NAMES = "abcdefgh"


def _flat(args):
    """The places of the inputs: a number is one place, a pair two."""
    out = []
    for a in args:
        out += list(a) if isinstance(a, tuple) else [a]
    return out


def _shape(args):
    return [len(a) if isinstance(a, tuple) else 0 for a in args]


def _typ(v):
    if v is None:
        return MAYBE
    if isinstance(v, bool):
        return BOOL
    if isinstance(v, tuple):
        return LIST
    return INT


def _subst(expr, name, by):
    if not isinstance(expr, tuple):
        return expr
    if expr == ("var", name):
        return by
    return tuple(_subst(e, name, by) for e in expr)


class OwnCode:
    def __init__(self, brain, state=None):
        st = state or {}
        self.brain = brain
        self.found = {k: dict(v) for k, v in st.get("found", {}).items()}
        self.runs = {k: [list(r) for r in v] for k, v in st.get("runs", {}).items()}
        self.order = list(st.get("order", []))
        self.library = copy.deepcopy(brain.library)
        for name in self.order:
            self._add_laws(name)

    def to_json(self):
        return {"found": dict(sorted(self.found.items())), "runs": self.runs,
                "order": self.order}

    def note(self, kind, text):
        self.brain.note(kind, text)

    # ------------------------------------------------------------ studying one function
    def study(self, name, run, choose, allowed, seed, budget=RUNS):
        """run(args) -> what the function returns (("fails",) if it fails); choose(rng)
        -> inputs it may try, at random; allowed(args): may it try these?

        It runs the function on inputs picked at random first, then puts the law it has
        to the test where the law says something it has seldom seen. A law it trusts has
        predicted at least CONFIRM test runs right since it last changed; otherwise it
        says it isn't sure. Returns the law it found, or None."""
        rng = random.Random(seed)
        seen, tried, fruitful, uses = [], set(), [], {}

        def ask(args):
            tried.add(repr(args))
            seen.append((args, run(args)))
        for _ in range(budget * 5):
            if len(seen) >= budget * 3 // 5:
                break
            args = choose(rng)
            if repr(args) not in tried:
                ask(args)
        if name not in self.order:
            self.order.append(name)
        law = self._learn(name, [(a, o) for a, o in seen if o != ("fails",)])
        confirmed = 0
        while len(seen) < budget:
            got = self._test_input(law, seen, choose, allowed, rng, tried, fruitful, uses)
            if got is None:
                # nothing left it could find to try: the law fits every input it may run
                confirmed = CONFIRM if law is not None else 0
                break
            args, probe = got
            kind = probe[0] if probe else None
            uses[kind] = uses.get(kind, 0) + 1
            ask(args)
            o = seen[-1][1]
            before = sum(1 for _, x in seen[:-1] if repr(x) == repr(o))
            if probe is not None and before <= 1 and probe not in fruitful:
                fruitful.append(probe)      # this way of changing inputs finds rare answers
            if law is not None and self._guess(law, args) == (True, o):
                confirmed += 1
                continue
            law = self._learn(name, [(a, o) for a, o in seen if o != ("fails",)])
            confirmed = 0
        self.runs[name] = [[_jsonable(a), _jsonable(o)] for a, o in seen]
        if law is not None and confirmed < CONFIRM:
            self.note("doubt", f"{name}: {self.describe_law(law)} fits all {len(seen)} runs, "
                               f"but only {confirmed} came after I found it: I'm not sure")
            law = None
        if law is None:
            self.found.pop(name, None)
            self.note("stuck", f"I ran {name} {len(seen)} times and found no law I trust")
            return None
        self.found[name] = law
        self._add_laws(name)
        self.note("code", f"{name}: {self.describe(name)} ({len(seen)} runs)")
        return law

    def _test_input(self, law, seen, choose, allowed, rng, tried, fruitful=(), uses=None):
        """Inputs where its law says what it has seen least often (a law built on rare
        cases is the one most likely to be wrong there); at random if it has none. Beside
        inputs at random it tries ones made from what gave a rare answer: one input given
        twice, one input with everything in it twice as big, or one place a step up or
        down; and a way of changing inputs that found a
        rare answer before is tried on everything it ran. Each way of making inputs takes
        its turn, so no one way decides alone. Returns (inputs, how made)."""
        uses = uses or {}
        counts = {}
        for _, o in seen:
            counts[repr(o)] = counts.get(repr(o), 0) + 1

        def made(args, probe):
            flat, shape = _flat(args), _shape(args)
            if probe[0] == "copy":
                i, j = probe[1:]
                if max(i, j) >= len(args) or shape[i] != shape[j]:
                    return None
                return tuple(args[i] if k == j else a for k, a in enumerate(args))
            if probe[0] == "twice":
                i = probe[1]
                if i >= len(args):
                    return None
                big = tuple(2 * v for v in args[i]) if shape[i] else 2 * args[i]
                return tuple(big if k == i else a for k, a in enumerate(args))
            i, d = probe[1:]
            if i >= len(flat):
                return None
            return _unflat(flat[:i] + [flat[i] + d] + flat[i + 1:], shape)
        pool = [(made(args, p), p) for p in fruitful for args, _ in seen]
        copies, steps = [], []      # made from rare answers: on a tie they come first
        for args, o in seen:
            # what gave a rare answer; or anything, while every answer was the same
            if counts[repr(o)] > 2 and len(counts) > 1:
                continue
            n = len(_flat(args))
            copies += [(made(args, ("copy", i, j)), ("copy", i, j))
                       for i in range(len(args)) for j in range(len(args)) if i != j]
            copies += [(made(args, ("twice", i)), ("twice", i)) for i in range(len(args))]
            steps += [(made(args, ("step", i, d)), ("step", i, d))
                      for i in range(n) for d in (1, -1)]
        pool += copies + steps + [(choose(rng), None) for _ in range(200)]
        best = None
        for args, probe in pool:
            if args is None or repr(args) in tried or not allowed(args):
                continue
            turn = uses.get(probe[0] if probe else None, 0)
            if law is None:
                score = (turn,)
            else:
                ok, v = self._guess(law, args)
                # where laws that fit as well say different things, a run tells most
                said = {repr(v)} | {repr(self._eval(from_json(r), dict(zip(
                    law["params"], _flat(args))))) for r in law.get("rivals", [])}
                score = (-len(said), turn, counts.get(repr(v), 0) if ok else -1)
            if best is None or score < best[0]:
                best = (score, (args, probe))
        return best[1] if best else None

    def _guess(self, law, args):
        if _shape(args) != law["shape"]:
            return False, None
        env = dict(zip(law["params"], _flat(args)))
        if law["out"] == "places":
            vals = [self._eval(from_json(e), env) for e in law["laws"]]
            return (False, None) if "?" in vals else (True, tuple(vals))
        v = self._eval(from_json(law["law"]), env)
        return (False, None) if v == "?" else (True, v)

    def _learn(self, name, ok):
        if not ok:
            return None
        shapes = {tuple(_shape(a)) for a, _ in ok}
        if len(shapes) != 1:
            return None
        shape = list(shapes.pop())
        xs = [_flat(a) for a, _ in ok]
        params = list(NAMES[:len(xs[0])])
        env = [dict(zip(params, x)) for x in xs]
        outs = [o for _, o in ok]
        kinds = {_typ(o) for o in outs}
        law = {"shape": shape, "params": params}
        if kinds == {BOOL} and min(outs.count(True), outs.count(False)) < 3:
            return None         # too few of one answer to say when it comes
        if kinds <= {INT, MAYBE} or kinds == {BOOL}:
            t = BOOL if kinds == {BOOL} else MAYBE if MAYBE in kinds else INT
            self.rivals = []
            e = self._value(env, outs, t, params, rivals=RIVALS)
            if e is None:
                return None
            return dict(law, out="value", type=t, law=to_json(e),
                        rivals=[to_json(r) for r in self.rivals])
        if kinds != {LIST}:
            return None
        lens = {len(o) for o in outs}
        if len(lens) == 1 and next(iter(lens)) <= MAX_PLACES:
            places = self._places(env, outs, params)
            if places is None:
                return None
            return dict(law, out="places", laws=[to_json(e) for e in places])
        e = self._row(env, outs, params)
        if e is None:
            return None
        return dict(law, out="row", law=to_json(e))

    def _search(self, env, ys, t, names, size=7, rivals=0):
        """Its ordinary search: first with only 0 and 1 (a wider search for the same
        effort), then with every number it has a name for. With rivals, the other laws
        about as short that fit too are kept in self.rivals."""
        types = {n: INT for n in names}
        xs = [{n: x[n] for n in names} for x in env]
        for consts, bank in (((0, 1), 100000), (self.brain.constants(), 20000)):
            res = synthesize(xs, list(ys), types, t, self.library, consts, max_size=size,
                             max_bank=bank, rivals=rivals,
                             extra=self.brain.primitives() + ("rows", "code"))
            if res.expr is not None:
                if rivals:
                    self.rivals = list(res.rivals)[:rivals]
                return res.expr
        return None

    def _value(self, env, ys, t, names, split=True, rivals=0):
        e = self._search(env, ys, t, names, rivals=rivals)
        if e is not None:
            return e
        if t == INT:
            e = self._first(env, ys, names)
            if e is not None:
                return e
        if split:
            return self._split(env, ys, t, names)
        return None

    def _counted(self, env, names):
        """Rows counted out that an answer might be taken from: 0 or 1 up to an input."""
        for v in names:
            for lo in (1, 0):
                yield ("upto", ("const", lo), ("var", v))

    def _first(self, env, ys, names):
        """The answer is the first of a counted-out row for which some test holds."""
        for R in self._counted(env, names):
            rows = [self._eval(R, x) for x in env]
            if any(r is None or y not in r for r, y in zip(rows, ys)):
                continue
            tenv, labels = [], []
            for x, r, y in zip(env, rows, ys):
                for it in r[:r.index(y) + 1]:
                    tenv.append(dict(x, it=it))
                    labels.append(it == y)
            P = self._search(tenv, labels, BOOL, names + ["it"])
            if P is not None:
                e = ("first", P, R)
                if all(self._eval(e, x) == y for x, y in zip(env, ys)):
                    return e
        return None

    def _row(self, env, ys, names):
        e = self._search(env, ys, LIST, names, size=6)
        if e is not None:
            return e
        for R in self._counted(env, names):
            rows = [self._eval(R, x) for x in env]
            if any(r is None or not set(y) <= set(r) or list(y) != [v for v in r if v in y]
                   for r, y in zip(rows, ys)):
                continue
            tenv, labels = [], []
            for x, r, y in zip(env, rows, ys):
                for it in r:
                    tenv.append(dict(x, it=it))
                    labels.append(it in y)
            P = self._search(tenv, labels, BOOL, names + ["it"])
            if P is not None:
                e = ("keep", P, R)
                if all(self._eval(e, x) == y for x, y in zip(env, ys)):
                    return e
        return None

    def _places(self, env, outs, names):
        """One law per place; a place found can help find the others."""
        n = len(outs[0])
        laws = [None] * n
        progress = True
        while progress and None in laws:
            progress = False
            known = [i for i in range(n) if laws[i] is not None]
            for i in range(n):
                if laws[i] is not None:
                    continue
                ys = [o[i] for o in outs]
                t = {_typ(y) for y in ys}
                if not t <= {INT}:
                    return None
                penv = [dict(x, **{f"p{k}": o[k] for k in known}) for x, o in zip(env, outs)]
                e = self._value(penv, ys, INT, names + [f"p{k}" for k in known])
                if e is not None:
                    for k in known:
                        e = _subst(e, f"p{k}", laws[k])
                    laws[i] = e
                    progress = True
                    break
        return None if None in laws else laws

    def _split(self, env, ys, t, names):
        """One input takes only a few values: a law for each, and a test between them."""
        for v in names:
            vals = sorted({x[v] for x in env})
            if not 2 <= len(vals) <= 3:
                continue
            groups = []         # [values, law]
            for val in vals:
                idx = [i for i, x in enumerate(env) if x[v] == val]
                genv, gys = [env[i] for i in idx], [ys[i] for i in idx]
                hit = next((g for g in groups if all(
                    self._eval(g[1], x) == y for x, y in zip(genv, gys))), None)
                if hit is not None:
                    hit[0].append(val)
                    continue
                e = self._value(genv, gys, t, names, split=False)
                if e is None:
                    break
                groups.append([[val], e])
            else:
                if len(groups) != 2:
                    continue
                test = self._search([{v: val} for val in vals],
                                    [val in groups[0][0] for val in vals], BOOL, [v], size=4)
                if test is None:
                    continue
                e = ("ite", test, groups[0][1], groups[1][1])
                if all(self._eval(e, x) == y for x, y in zip(env, ys)):
                    return e
        return None

    def _eval(self, e, env):
        try:
            v = evaluate(e, env, self.library)
        except (Overflow, KeyError, TypeError, ValueError, RecursionError):
            return "?"
        return tuple(v) if isinstance(v, list) else v

    # ------------------------------------------------------------ using what it found
    def _add_laws(self, name):
        """A law for a number from at most two places becomes a building block."""
        f = self.found.get(name)
        if not f or len(f["params"]) > 2 or len(f["params"]) == 0:
            return
        exprs = [f["law"]] if f["out"] == "value" and f["type"] == INT else \
            f["laws"] if f["out"] == "places" else []
        for i, e in enumerate(exprs):
            key = f"{name}#{i}" if f["out"] == "places" else name
            self.library.add(Law(key, f["params"], ("sure", from_json(e)), INT,
                                 {"own": True, **({"list_params": False})}))

    def predict(self, name, args):
        """(True, what it will return) or (False, None) if it has no law."""
        f = self.found.get(name)
        return (False, None) if f is None else self._guess(f, args)

    def describe(self, name):
        return self.describe_law(self.found.get(name))

    def describe_law(self, f):
        if not f:
            return "I don't know"
        ps = ", ".join(f["params"])
        if f["out"] == "places":
            return f"({ps}) -> (" + "; ".join(show(from_json(e)) for e in f["laws"]) + ")"
        return f"({ps}) -> {show(from_json(f['law']))}"


def _unflat(flat, shape):
    out, i = [], 0
    for n in shape:
        out.append(tuple(flat[i:i + n]) if n else flat[i])
        i += n or 1
    return tuple(out)


def _jsonable(v):
    if isinstance(v, tuple):
        return [_jsonable(x) for x in v]
    return v
