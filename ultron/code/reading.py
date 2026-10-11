"""Reading Engc: Ultron finds what expressions mean by running programs (lesson 100, C1).

What Ultron is given (core knowledge, as `dsl.py` is): a program is words separated by
spaces; numbers are read with its own place-value law; a word between two values may
join them and a word before a value may act on it; marks may group words. What it
finds itself:

  * the frame every program has (here `PRINT ... .`), as the words that never change;
  * what each word means, as one of its own laws, found by its ordinary law search
    from runs it watched or designed (no table of meanings anywhere);
  * which of two printed symbols means "it holds" (a convention: both readings predict
    the same, so it takes the shorter description and says so);
  * how strongly each word groups and which way it chains, as the shortest grammar
    (fewest grouping levels) that reproduces every run, with experiments designed
    where rival grammars disagree;
  * what the marks `(` and `)` do, by trying the roles a mark can have.

Every meaning keeps the runs that decided it. Prediction never runs the program.
"""

import copy
import random

from ..brain import stepping
from ..brain.dsl import BOOL, INT, Law, Overflow, evaluate, show, size
from ..brain.language import read_number, speak_number
from ..brain.synth import synthesize

GRID = [(a, b) for a in range(13) for b in range(13)]       # what it tries itself
PROBE2 = [(0, 0), (1, 2), (2, 1), (3, 3), (5, 2), (2, 5), (7, 3), (4, 9), (9, 4), (6, 6)]
PROBE1 = [0, 1, 2, 3, 7]
BOOLS = [(False, False), (False, True), (True, False), (True, True)]
CONFIRM = 6          # fresh predictions in a row before a new meaning is trusted
CONFIRM_SYNONYM = 3  # ... when it is the meaning of a word already trusted
GRAMMAR_CONFIRM = 8  # longer programs in a row before a grammar is trusted
MAX_LEVELS = 10
SMALL = 10 ** 7      # outcomes it can imagine while searching (synth's limit)


class Unknown(Exception):
    """Something in the program Ultron doesn't understand yet."""


class _TooHard(Exception):
    pass


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _type_of(v):
    return BOOL if isinstance(v, bool) else INT


def _names(arity, types):
    """What it calls a phrase's inputs: x, y for numbers, p, q for truth values."""
    return ("x", "y")[:arity] if types and types[0] == INT else ("p", "q")[:arity]


class Reader:
    def __init__(self, brain, state=None):
        self.brain = brain
        st = state or {}
        self.frame = st.get("frame")                    # [words before], [words after]
        self.phrases = {k: dict(v) for k, v in st.get("phrases", {}).items()}
        self.symbols = list(st.get("symbols", []))      # [means "doesn't hold", "holds"]
        self.flipped = st.get("flipped", False)
        self.levels = dict(st.get("levels", {}))        # class -> grouping level
        self.assoc = {int(k): v for k, v in st.get("assoc", {}).items()}
        self.marks = dict(st.get("marks", {}))          # token -> open / close / ignore
        self.runs = [list(r) for r in st.get("runs", [])]   # [program, printed or None]
        self.laws = {k: Law.from_json(v) for k, v in st.get("laws", {}).items()}
        self.cycles = dict(st.get("cycles", {}))
        self.stats = dict(st.get("stats", {"trainer": 0, "own": 0}))
        self.aside = list(st.get("aside", []))      # runs it can't explain yet, kept apart
        self.library = copy.deepcopy(brain.library)
        for law in self.laws.values():
            if law.name.startswith("step:"):
                self.library.add(law)
        self.library.cycles.update(self.cycles)
        self.world = None       # set while a lesson runs: program text -> printed
        self._sigs = {}
        self._cache = {}
        self.rng = random.Random(st.get("seed", 0))

    def to_json(self):
        return {"frame": self.frame, "phrases": dict(sorted(self.phrases.items())),
                "symbols": self.symbols, "flipped": self.flipped,
                "levels": dict(sorted(self.levels.items())),
                "assoc": {str(k): v for k, v in sorted(self.assoc.items())},
                "marks": dict(sorted(self.marks.items())), "runs": self.runs,
                "laws": {k: v.to_json() for k, v in sorted(self.laws.items())},
                "cycles": dict(sorted(self.cycles.items())), "stats": self.stats,
                "aside": self.aside}

    def note(self, kind, text):
        self.brain.note(kind, text)

    # ------------------------------------------------------------ the world
    def run(self, program, who="own"):
        """Run a program in the sandbox (the Trainer's or one Ultron wrote)."""
        printed = self.world(program)
        self.runs.append([program, printed])
        self.stats[who] = self.stats.get(who, 0) + 1
        return printed

    def watch(self, program, printed):
        """A program the Trainer ran, and what it printed."""
        self.runs.append([program, printed])
        self.stats["trainer"] = self.stats.get("trainer", 0) + 1

    @property
    def total_runs(self):
        return self.stats.get("trainer", 0) + self.stats.get("own", 0)

    # ------------------------------------------------------------ perceiving
    def find_frame(self, programs):
        """The words at the start and end of every program carry no information."""
        toks = [p.split() for p in programs]
        before, after = [], []
        for i in range(min(len(t) for t in toks)):
            w = toks[0][i]
            if all(t[i] == w for t in toks) and read_number(self.brain, w)[0] is None:
                before.append(w)
            else:
                break
        for i in range(1, min(len(t) for t in toks) - len(before) + 1):
            w = toks[0][-i]
            if all(t[-i] == w for t in toks) and read_number(self.brain, w)[0] is None:
                after.insert(0, w)
            else:
                break
        self.frame = [before, after]
        self.note("code", f"every program starts with {' '.join(before)!r} and ends with "
                          f"{' '.join(after)!r}: those words never change what is printed")

    def number(self, tok):
        v, _ = read_number(self.brain, tok)
        return v

    def value_of(self, printed):
        """What a printed line means to Ultron: a number, or one of the two symbols."""
        if printed is None or len(printed) != 1:
            return None
        tok = printed[0]
        v = self.number(tok)
        if v is not None:
            return v
        if len(self.symbols) == 2 and tok in self.symbols:
            return self.symbols.index(tok) == 1
        return ("symbol", tok)

    def show_value(self, v):
        if isinstance(v, bool):
            return self.symbols[1 if v else 0] if len(self.symbols) == 2 else None
        if _is_int(v):
            return speak_number(self.brain, v)
        return None

    def _known_words(self):
        out = {tuple(p["words"]) for p in self.phrases.values()}
        out |= {(m,) for m in self.marks}
        return out

    def items(self, program):
        """The program as numbers and runs of words, with known phrases picked out."""
        key = (program, len(self.phrases), tuple(sorted(self.marks.items())))
        if key not in self._cache:
            try:
                self._cache[key] = self._items(program)
            except Unknown as e:
                self._cache[key] = e
        got = self._cache[key]
        if isinstance(got, Unknown):
            raise got
        return got

    def _items(self, program):
        toks = program.split()
        before, after = self.frame
        if toks[:len(before)] != before or (after and toks[-len(after):] != after):
            raise Unknown("not a program of the usual shape")
        toks = toks[len(before):len(toks) - len(after)]
        out, run = [], []
        for t in toks + [None]:
            v = self.number(t) if t is not None else None
            if t is None or v is not None:
                out += self._segment(run)
                run = []
                if t is not None:
                    out.append(("num", v))
            else:
                run.append(t)
        return out

    def _segment(self, run):
        """Letters make words; any other mark stands alone."""
        out, word = [], []
        for t in run:
            if t.isalpha():
                word.append(t)
            else:
                out += self._words(word) + [("w", (t,))]
                word = []
        return out + self._words(word)

    def _words(self, run):
        if not run:
            return []
        known = self._known_words()
        if not any(tuple(run[i:j]) in known for i in range(len(run))
                   for j in range(i + 1, len(run) + 1)):
            return [("w", tuple(run))]
        out, i = [], 0
        while i < len(run):
            for j in range(len(run), i, -1):
                if tuple(run[i:j]) in known:
                    out.append(("w", tuple(run[i:j])))
                    i = j
                    break
            else:
                out.append(("w", (run[i],)))
                i += 1
        return out

    def key(self, words, arity):
        return f"{' '.join(words)}/{arity}"

    def known(self, words, arity):
        return self.key(words, arity) in self.phrases

    # ------------------------------------------------------------ meanings
    def apply(self, key, args):
        p = self.phrases[key]
        if len(args) != len(p["types"]) or any(_type_of(a) != t for a, t in zip(args, p["types"])):
            raise Unknown(f"'{key}' doesn't take {args}")
        law = self.laws[p["law"]]
        env = dict(zip(_names(len(args), p["types"]), args))
        if p.get("fails") is not None:
            from ..brain.dsl import from_json
            if evaluate(from_json(p["fails"]), env, self.library):
                raise Unknown(f"'{key}' fails here")
        v = evaluate(law.expr, env, self.library)
        if v is None:
            raise Unknown("can't work it out")
        return v

    def _outputs(self, demos):
        """Demos' outcomes as values its laws can produce; None if they don't fit one type."""
        outs = [self.value_of(o) for _, o in demos]
        if all(_is_int(o) for o in outs):
            return outs, INT
        syms = sorted({o[1] for o in outs if isinstance(o, tuple)} |
                      {self.symbols[int(o)] for o in outs if isinstance(o, bool)})
        if all(isinstance(o, (tuple, bool)) for o in outs) and len(syms) <= 2:
            if len(self.symbols) < 2:
                # two symbols it has met: which one means "it holds" is a convention
                # decided later by the shorter description; first guess: sorted order
                self.symbols = sorted(set(self.symbols) | set(syms))
                if len(self.symbols) < 2:
                    return None, None
            return [self.value_of([o[1]]) if isinstance(o, tuple) else o for o in outs], BOOL
        return None, None

    def search(self, key, demos, rivals=10):
        """The shortest of its laws for these demos: (expr, rivals, steps)."""
        good = [(i, o) for i, o in demos if o is not None]
        outs, out_type = self._outputs(good)
        if outs is None or not good:
            return None, [], 0
        arity = len(good[0][0])
        names = _names(arity, [_type_of(v) for v in good[0][0]])
        types = {n: _type_of(v) for n, v in zip(names, good[0][0])}
        xs = [dict(zip(names, i)) for i, _ in good]
        return self._search(key, xs, outs, names, types, out_type, rivals)

    def _search(self, key, xs, outs, names, types, out_type, rivals):
        # a meaning it already found for another word, if it fits (a synonym)
        for name in sorted(self.laws):
            if name == f"engc:{key}" or name.startswith("step:"):
                continue
            law = self.laws[name]
            if law.params == sorted(names) and law.out_type == out_type and all(
                    _same(evaluate_safe(law.expr, x, self.library), y)
                    for x, y in zip(xs, outs)):
                return law.expr, [], 0
        # it imagines with small numbers; huge outcomes only check what it found
        small = [(x, y) for x, y in zip(xs, outs) if isinstance(y, bool) or abs(y) <= SMALL]
        if not small:
            return None, [], 0
        if all(t == BOOL for t in types.values()) and \
                len({tuple(sorted(x.items())) for x in xs}) == 2 ** len(types):
            rivals = 0      # it has seen every case there is: nothing left to disagree on
        # its own laws are the building blocks (a word's meaning, or a step it found for
        # one, is not one)
        res = synthesize([x for x, _ in small], [y for _, y in small], types, out_type,
                         self.brain.library, self.brain.constants(), rivals=rivals,
                         extra=self.brain.primitives())
        if res.expr is None or not all(_same(evaluate_safe(res.expr, x, self.library), y)
                                       for x, y in zip(xs, outs)):
            return None, [], res.steps
        return res.expr, res.rivals, res.steps

    def adopt(self, key, words, arity, demos, expr, types, out_type, how="search"):
        name = f"engc:{key}"
        names = _names(arity, types)
        law = Law(name, sorted(names), expr, out_type,
                  {"lesson": self.brain.lesson, "runs": len(demos), "size": size(expr),
                   "found_by": how})
        self.laws[name] = law      # words' meanings are not building blocks for laws
        old = self.phrases.get(key, {}).get("fails")
        self.phrases[key] = {"words": list(words), "arity": arity, "law": name,
                             "types": list(types), "out": out_type, "runs": len(demos),
                             "demos": [[list(i), o] for i, o in demos], "fails": old}
        self._learn_failures(key, names, demos)
        self._sigs = {}
        self._cache = {}

    def _learn_failures(self, key, names, demos):
        """Where a word makes the program fail (like dividing by nothing), as a law too."""
        p = self.phrases[key]
        before = p.pop("fails", None)
        if not any(o is None for _, o in demos):
            return
        xs = [dict(zip(names, i)) for i, _ in demos]
        ys = [o is None for _, o in demos]
        res = synthesize(xs, ys, {n: t for n, t in zip(names, p["types"])}, BOOL,
                         self.library, self.brain.constants(), extra=self.brain.primitives())
        if res.expr is not None:
            from ..brain.dsl import to_json
            p["fails"] = to_json(res.expr)
            if p["fails"] == before:
                return
            self.note("code", f"'{' '.join(p['words'])}' makes a program fail when "
                              f"{show(res.expr)}")

    def write(self, words, args):
        """Ultron writes a program: the frame around a phrase and its operands."""
        before, after = self.frame
        parts = []
        if len(args) == 1:
            parts = list(words) + self.operand_text(args[0])
        else:
            parts = self.operand_text(args[0]) + list(words) + self.operand_text(args[1])
        return " ".join(before + parts + after)

    def operand_text(self, v):
        if _is_int(v):
            s = speak_number(self.brain, v)
            if s is None:
                raise Unknown("can't write that number")
            return [s]
        # a truth value: it writes a comparison it knows, with numbers that make it so
        for key in sorted(self.phrases):
            p = self.phrases[key]
            if p["arity"] == 2 and p["types"] == [INT, INT] and p["out"] == BOOL:
                for a, b in GRID:
                    if self.apply(key, (a, b)) == v:
                        return [speak_number(self.brain, a)] + p["words"] + \
                               [speak_number(self.brain, b)]
        raise Unknown("can't write a truth value yet")

    def demo_from(self, program, printed):
        """If a run has exactly one phrase Ultron doesn't know, and splitting there leaves
        parts it can work out, the run is a demonstration of that phrase."""
        try:
            items = self.items(program)
        except Unknown:
            return None
        unknown = [i for i, it in enumerate(items) if it[0] == "w"
                   and not self.known(it[1], 1 if i == 0 else 2)
                   and it[1][0] not in self.marks]
        if len(unknown) != 1:
            return None
        i = unknown[0]
        words = items[i][1]
        flat = {"levels": {c: 0 for c in self.classes()}, "assoc": {}}
        try:
            if i == 0:
                right = self.value(items[1:], **flat)
                return words, 1, (right,), printed
            left, right = self.value(items[:i], **flat), self.value(items[i + 1:], **flat)
            return words, 2, (left, right), printed
        except Unknown:
            return None

    def study(self, words, arity, demos, budget, recheck=False):
        """Learn one phrase: search, design experiments where its rivals disagree, then
        confirm with fresh tries. Returns the runs it spent."""
        key = self.key(words, arity)
        spent, streak = 0, 0
        expr, rivals, out_type, synonym = None, [], None, False
        while spent < budget:
            good = [(i, o) for i, o in demos if o is not None]
            types = [_type_of(v) for v in good[0][0]] if good else None
            outs, out_type = self._outputs(good) if good else (None, None)
            if recheck and expr is None and key in self.phrases:
                expr = self.laws[self.phrases[key]["law"]].expr      # test what it holds
            if outs is not None and expr is not None and self._fits(key, demos):
                pass        # not surprised: keep the idea, keep testing it
            elif outs is not None:
                expr, rivals, _ = self.search(key, demos)
                synonym = expr is not None and any(
                    l.expr == expr for n, l in self.laws.items() if n != f"engc:{key}")
                if expr is None and arity == 2 and types == [INT, INT] and out_type == INT:
                    expr, used = self._by_stepping(key, words, demos)
                    spent += used
                if expr is None:
                    self.note("stuck", f"'{' '.join(words)}': none of my laws explains its "
                                       f"{len(good)} runs")
                    return spent
                self.adopt(key, words, arity, demos, expr, types, out_type)
            rivals = [r for r in rivals if self._rival_fits(key, r, demos)]
            # an experiment where my rival explanations disagree, else a fresh try
            probe = self._disagreement(key, expr, rivals, types, demos) if expr is not None else None
            fresh = probe is None
            if fresh:
                probe = self._fresh(types or [INT] * arity, demos)
            printed = self.run(self.write(words, probe))
            spent += 1
            demos.append((tuple(probe), printed))
            if expr is None:
                continue        # it hasn't seen enough kinds of outcome to say anything
            guess = self._try(key, probe)
            right = (printed is None and guess is None) or (
                printed is not None and guess is not None
                and self.show_value(guess) == printed[0])
            if not right:
                streak = 0
                self.note("code", f"'{' '.join(words)}' with {list(probe)}: I expected "
                                  f"{self.show_value(guess) if guess is not None else 'a failure'}"
                                  f", it printed {printed}; thinking again")
                continue
            if fresh:
                streak += 1
                if streak >= (CONFIRM_SYNONYM if synonym else CONFIRM):
                    self.adopt(key, words, arity, demos, expr, types, out_type)
                    self.note("code", f"'{' '.join(words)}' means {show(expr)} to me "
                                      f"({len(demos)} runs; {streak} fresh tries predicted"
                                      + ("; the same as a word I know" if synonym else "")
                                      + ")")
                    return spent
        return spent

    def _rival_fits(self, key, expr, demos):
        p = self.phrases.get(key)
        if p is None:
            return False
        names = _names(p["arity"], p["types"])
        for i, o in demos:
            if o is None:
                continue
            g = evaluate_safe(expr, dict(zip(names, i)), self.library)
            if g is None or self.show_value(g) != o[0]:
                return False
        return True

    def _fits(self, key, demos):
        if key not in self.phrases:
            return False
        for i, o in demos:
            g = self._try(key, i)
            if o is None:
                if g is not None:
                    return False        # it thought this would work, and it failed
                continue
            if g is None or self.show_value(g) != o[0]:
                return False
        return True

    def _try(self, key, args):
        try:
            return self.apply(key, args)
        except (Unknown, Overflow, KeyError, TypeError):
            return None

    def _disagreement(self, key, expr, rivals, types, demos):
        if not rivals:
            return None
        law = self.laws[self.phrases[key]["law"]]
        tried = {tuple(i) for i, _ in demos}
        for args in self._domain(types):
            if tuple(args) in tried:
                continue
            env = dict(zip(law.params, args))
            mine = evaluate_safe(expr, env, self.library)
            for r in rivals:
                if not _same(evaluate_safe(r, env, self.library), mine):
                    return args
        return None

    def _domain(self, types):
        if types == [INT, INT]:
            return GRID
        if types == [INT]:
            return [(a,) for a in range(13)]
        if types == [BOOL, BOOL]:
            return BOOLS
        return [(False,), (True,)]

    def _fresh(self, types, demos=()):
        """A fresh try: a kind of situation not seen yet (equal, zero, bigger, smaller...)
        if there is one, else any."""
        from ..brain.brain import Brain
        names = _names(len(types), types)
        seen = {Brain.kind_of(dict(zip(names, i))) for i, _ in demos}
        dom = list(self._domain(types))
        self.rng.shuffle(dom)
        for args in dom:
            if Brain.kind_of(dict(zip(names, args))) not in seen:
                return args
        return dom[0]

    def _by_stepping(self, key, words, demos):
        spent = 0
        known = {}
        for i, o in demos:
            if o is not None and len(i) == 2:
                known[tuple(i)] = self.value_of(o)

        def outcome(x, y):
            nonlocal spent
            printed = self.run(self.write(words, (x, y)))
            spent += 1
            demos.append(((x, y), printed))
            return self.value_of(printed)

        expr, step, story, _ = stepping.by_stepping(key, outcome, self.library,
                                                    self.brain.constants(),
                                                    self.brain.primitives(), known)
        if expr is None:
            return None, spent
        self.laws[step.name] = step
        if self.library.cycles.get(step.name) == "param":
            self.cycles[step.name] = "param"
        self.note("invent", f"'{' '.join(words)}': {story}")
        return expr, spent

    def decide_symbols(self):
        """Which printed symbol means 'it holds' is a convention: take the reading under
        which all its truth-valued words are described most shortly."""
        bool_keys = [k for k, p in self.phrases.items() if p["out"] == BOOL]
        if len(self.symbols) != 2 or not bool_keys:
            return
        now = sum(size(self.laws[self.phrases[k]["law"]].expr) for k in bool_keys)
        saved = (copy.deepcopy(self.phrases), dict(self.laws), list(self.symbols))
        self.symbols.reverse()
        flipped = 0
        for k in bool_keys:
            p = self.phrases[k]
            demos = [(tuple(i), o) for i, o in p["demos"]]
            expr, _, _ = self.search(k, demos, rivals=0)
            if expr is None:
                flipped = None
                break
            flipped += size(expr)
            self.adopt(k, p["words"], p["arity"], demos, expr, p["types"], BOOL)
        if flipped is None or flipped >= now:
            self.phrases, self.laws, self.symbols = saved
            self._sigs, self._cache = {}, {}
            self.note("code", f"I read '{self.symbols[1]}' as 'it holds' and "
                              f"'{self.symbols[0]}' as 'it doesn't': my truth-words take "
                              f"{now} pieces that way" + (
                                  f", {flipped} the other way round" if flipped else "")
                      + ("; both readings predict the same, so this is only a convention"
                         if flipped == now else ""))
        else:
            self.flipped = True
            self.note("code", f"I read '{self.symbols[1]}' as 'it holds': shorter "
                              f"({flipped} pieces against {now})")

    # ------------------------------------------------------------ grammar
    def cls(self, key):
        """Words with the same meaning are one kind of word (a synonym costs nothing)."""
        p = self.phrases[key]
        sig = (p["arity"], tuple(p["types"]), p["out"], self._signature(key))
        for k in sorted(self.phrases):
            q = self.phrases[k]
            if (q["arity"], tuple(q["types"]), q["out"], self._signature(k)) == sig:
                return k
        return key

    def _signature(self, key):
        p = self.phrases[key]
        if key in self._sigs:
            return self._sigs[key]
        if p["types"] == [INT, INT]:
            dom = PROBE2
        elif p["types"] == [INT]:
            dom = [(a,) for a in PROBE1]
        elif p["types"] == [BOOL, BOOL]:
            dom = BOOLS
        else:
            dom = [(False,), (True,)]
        sig = tuple(str(self._try(key, a)) for a in dom)
        self._sigs[key] = sig
        return sig

    def classes(self):
        return sorted({self.cls(k) for k in self.phrases})

    def parse(self, items, levels=None, assoc=None, marks=None):
        levels = self.levels if levels is None else levels
        assoc = self.assoc if assoc is None else assoc
        marks = self.marks if marks is None else marks
        pos = [0]
        items = [it for it in items if not (it[0] == "w" and len(it[1]) == 1
                                             and marks.get(it[1][0]) == "ignore")]

        def level(key):
            c = self.cls(key)
            if c not in levels:
                raise Unknown(f"I don't know how '{key}' groups")
            return levels[c]

        def operand():
            if pos[0] >= len(items):
                raise Unknown("ends too soon")
            it = items[pos[0]]
            if it[0] == "num":
                pos[0] += 1
                return ("val", it[1])
            words = it[1]
            if len(words) == 1 and marks.get(words[0]) == "open":
                pos[0] += 1
                e = expr(-1)
                if pos[0] >= len(items) or items[pos[0]] != ("w", (_closer(marks),)):
                    raise Unknown("a group that doesn't close")
                pos[0] += 1
                return e
            if self.known(words, 1):
                key = self.key(words, 1)
                pos[0] += 1
                return ("op", key, [expr(level(key) + 1)])
            raise Unknown(f"I don't know '{' '.join(words)}' here")

        def expr(minl):
            left = operand()
            while pos[0] < len(items):
                it = items[pos[0]]
                if it[0] != "w" or not self.known(it[1], 2):
                    break
                key = self.key(it[1], 2)
                lv = level(key)
                if lv < minl:
                    break
                pos[0] += 1
                nxt = lv + 1 if assoc.get(lv, "L") == "L" else lv
                left = ("op", key, [left, expr(nxt)])
            return left

        tree = expr(-1)
        if pos[0] != len(items):
            raise Unknown("words left over")
        return tree

    def evaluate(self, tree):
        if tree[0] == "val":
            return tree[1]
        args = [self.evaluate(t) for t in tree[2]]
        try:
            return self.apply(tree[1], args)
        except (Overflow, KeyError, TypeError) as e:
            raise Unknown("can't work it out") from e

    def value(self, items, **grammar):
        return self.evaluate(self.parse(items, **grammar))

    def predict(self, program, **grammar):
        """What the program will print, worked out without running it (None: don't know)."""
        try:
            return self.show_value(self.value(self.items(program), **grammar))
        except (Unknown, Overflow, RecursionError):
            return None

    def _explains(self, program, printed, **grammar):
        return printed is not None and len(printed) == 1 and \
            self.predict(program, **grammar) == printed[0]

    def grammar_runs(self):
        """Runs with more than one phrase or with marks: the evidence about grouping."""
        out = []
        for program, printed in self.runs:
            if printed is None or program in self.aside:
                continue
            try:
                items = self.items(program)
            except Unknown:
                continue
            ws = [it for it in items if it[0] == "w"]
            if len(ws) < 2:
                continue
            if any(not (self.known(w[1], 1) or self.known(w[1], 2)
                        or (len(w[1]) == 1 and w[1][0] in self.marks)) for w in ws):
                continue
            classes = set()
            for w in ws:
                for a in (1, 2):
                    if self.known(w[1], a):
                        classes.add(self.cls(self.key(w[1], a)))
            out.append((program, printed, classes))
        return out

    def readings(self, items, marks=None):
        """Every way of grouping a run that its laws can work out (any grouping at all,
        no grammar assumed), as (tree, value). Marks it knows group what they enclose."""
        marks = self.marks if marks is None else marks
        opener, closer = None, None
        for m, r in marks.items():
            if r == "open":
                opener = m
            elif r == "close":
                closer = m
        items = [it for it in items if not (it[0] == "w" and len(it[1]) == 1
                                             and marks.get(it[1][0]) == "ignore")]
        depth, match = [], {}
        for i, it in enumerate(items):
            if it == ("w", (opener,)):
                depth.append(i)
            elif it == ("w", (closer,)):
                if not depth:
                    return []
                match[depth.pop()] = i
        if depth:
            return []
        memo = {}

        def span(i, j):
            if (i, j) in memo:
                return memo[(i, j)]
            out = []
            if j - i == 1 and items[i][0] == "num":
                out.append((("val", items[i][1], i), items[i][1]))
            elif items[i] == ("w", (opener,)) and match.get(i) == j - 1:
                out += span(i + 1, j - 1)
            if j - i >= 2 and items[i][0] == "w" and self.known(items[i][1], 1):
                key = self.key(items[i][1], 1)
                for t, v in span(i + 1, j):
                    g = self._try(key, (v,))
                    if g is not None:
                        out.append((("op", key, [t], i), g))
            k = i
            while k < j:
                it = items[k]
                if it == ("w", (opener,)):
                    k = match[k] + 1
                    continue
                if k > i and it[0] == "w" and self.known(it[1], 2) and \
                        (items[k - 1][0] == "num" or items[k - 1] == ("w", (closer,))):
                    key = self.key(it[1], 2)
                    for lt, lvv in span(i, k):
                        for rt, rv in span(k + 1, j):
                            g = self._try(key, (lvv, rv))
                            if g is not None:
                                out.append((("op", key, [lt, rt], k), g))
                k += 1
            memo[(i, j)] = out
            return out

        return span(0, len(items)) if items else []

    def relations(self, program, printed):
        """What a run says about grouping, whatever the grammar: for two words in one
        bracket group where one sits inside the other's part, which one every reading
        that gives the printed answer works out first.
        Returns {('first' | 'second', A, B)} over kinds of word."""
        try:
            items = self.items(program)
        except Unknown:
            return None
        out = self.value_of(printed)
        if out is None or isinstance(out, tuple):
            return None
        good = [t for t, v in self.readings(items) if _same(v, out)]
        if not good:
            return None
        # which bracket group each word is in: only neighbours in one group are compared
        group, stack = {}, []
        for i, it in enumerate(items):
            if it[0] == "w" and len(it[1]) == 1 and self.marks.get(it[1][0]) == "open":
                stack.append(i)
            elif it[0] == "w" and len(it[1]) == 1 and self.marks.get(it[1][0]) == "close":
                stack.pop()
            group[i] = stack[-1] if stack else -1
        found = None
        for tree in good:
            rel = set()
            nodes = {}

            def walk(t, anc):
                if t[0] == "op":
                    nodes[t[3]] = (t[1], anc)
                    for c in t[2]:
                        walk(c, anc | {t[3]})
            walk(tree, frozenset())
            pos = sorted(nodes)
            for a, b in ((a, b) for i, a in enumerate(pos) for b in pos[i + 1:]):
                ka, kb = nodes[a][0], nodes[b][0]
                if group.get(a) != group.get(b):
                    continue
                if self.phrases[kb]["arity"] != 2:
                    continue
                if a in nodes[b][1]:        # b sits inside a: a waits for b
                    rel.add(("second", self.cls(ka), self.cls(kb)))
                elif b in nodes[a][1]:
                    rel.add(("first", self.cls(ka), self.cls(kb)))
            found = rel if found is None else found & rel
        return found

    def solve(self, extra=(), runs=None, marks=None, **_):
        """The grammar with the fewest grouping levels that explains every run: each
        run's relations become 'groups at least as tightly' or 'more tightly' between
        kinds of word; levels are the longest chains of 'more tightly'. Returns
        (levels, assoc) or None if no grammar of this shape explains the runs."""
        runs = self.grammar_runs() if runs is None else runs
        cons = set(extra) | self._typed_order()
        for program, printed, _ in runs:
            rel = self.relations(program, printed)
            if rel:
                cons |= rel
        classes = self.classes()
        binary = {c for c in classes if self.phrases[c]["arity"] == 2}
        side = {c: "L" for c in binary}           # chains from the left unless shown
        for kind, a, b in cons:
            if a == b and kind in ("second", "right"):
                side[a] = "R"
        for kind, a, b in cons:
            if a == b and kind in ("first", "left") and side[a] == "R":
                return None
        for flip in (None, "R above", "L above"):
            got = self._layers(classes, binary, side, cons, flip)
            if got is None:
                continue
            levels, assoc = got
            if all(self._explains(p, o, levels=levels, assoc=assoc, marks=marks)
                   for p, o, _ in runs):
                return levels, assoc
        return None

    def _typed_order(self):
        """Where only one grouping of 'x A y B z' (or 'A x B y') makes sense, as kinds of
        value go (a truth value can't be added), that grouping is the rule."""
        out = set()
        for a in self.classes():
            pa = self.phrases[a]
            for b in self.classes():
                pb = self.phrases[b]
                if pb["arity"] != 2:
                    continue
                a_first = pa["out"] == pb["types"][0]
                b_first = pb["out"] == pa["types"][-1]
                if a_first and not b_first:
                    out.add(("first", a, b))
                elif b_first and not a_first:
                    out.add(("second", a, b))
        return out

    def _layers(self, classes, binary, side, cons, flip):
        edges = []                               # (a, b, w): level[a] >= level[b] + w
        for kind, a, b in cons:
            if a == b:
                continue
            ua = self.phrases[a]["arity"] == 1
            same_l = side.get(a) == side.get(b) == "L"
            same_r = side.get(a) == side.get(b) == "R"
            if kind == "first":
                edges.append((a, b, 0) if ua else (a, b, 0 if same_l else 1))
            elif kind == "second":
                edges.append((b, a, 1) if ua else (b, a, 0 if same_r else 1))
            elif kind == "above":
                edges.append((a, b, 1))
            elif kind == "below":
                edges.append((b, a, 1))
            elif kind == "same":
                edges += [(a, b, 0), (b, a, 0)]
        if flip:
            rs = [c for c in binary if side[c] == "R"]
            ls = [c for c in binary if side[c] == "L"]
            for r in rs:
                for l_ in ls:
                    edges.append((r, l_, 1) if flip == "R above" else (l_, r, 1))
        level = {c: 0 for c in classes}
        for _ in range(len(classes) + 1):
            changed = False
            for a, b, w in edges:
                if level[a] < level[b] + w:
                    level[a] = level[b] + w
                    changed = True
            if not changed:
                break
        else:
            return None                          # a loop of 'more tightly': impossible
        if flip is None:
            for a in binary:
                for b in binary:
                    if a < b and level[a] == level[b] and side[a] != side[b]:
                        return None
        assoc = {}
        for c in binary:
            assoc[level[c]] = side[c]
        return level, assoc

    def learn_grammar(self, budget):
        """Find the grouping, then design experiments where rival grammars disagree, then
        confirm on longer programs it writes itself. Returns runs spent."""
        spent = 0
        streak = 0
        tried = set()
        while spent < budget:
            spent += self.doubt(budget - spent)
            best = self.solve()
            if best is None:
                self.note("stuck", "no grammar with few levels explains every run")
                return spent
            self.levels, self.assoc = best
            probe = self._grammar_experiment(best, tried)
            if probe is not None:
                printed = self.run(probe)
                spent += 1
                streak = 0
                continue
            program = self.imagine(self.rng.randint(3, 5))
            if program is None:
                return spent
            guess = self.predict(program)
            printed = self.run(program)
            spent += 1
            if printed is not None and guess == printed[0]:
                streak += 1
                if streak >= GRAMMAR_CONFIRM:
                    self.note("code", "my grammar: " + self.describe_grammar() +
                              f" ({GRAMMAR_CONFIRM} longer programs I wrote predicted in a "
                              f"row)")
                    return spent
            else:
                streak = 0
                self.note("code", f"{program!r}: I expected {guess}, it printed {printed}; "
                                  f"my grammar must change")
        return spent

    def doubt(self, budget):
        """A run that no grouping at all can explain means one of its words is not what
        Ultron thinks: it studies those words again. Returns runs spent."""
        spent = 0
        for program, printed, _ in self.grammar_runs():
            if spent >= budget:
                break
            try:
                items = self.items(program)
            except Unknown:
                continue
            out = self.value_of(printed)
            if any(_same(v, out) for _, v in self.readings(items)):
                continue
            suspects = []
            for i, it in enumerate(items):
                if it[0] == "w":
                    for a in (1, 2):
                        if self.known(it[1], a) and self.key(it[1], a) not in suspects:
                            suspects.append(self.key(it[1], a))
            self.note("doubt", f"{program!r} printed {printed}, and no way of grouping it "
                               f"gives that: one of {', '.join(suspects)} is not what I think")
            changed = False
            for key in suspects:
                p = self.phrases[key]
                before = p["law"], show(self.laws[p["law"]].expr)
                demos = [(tuple(i), o) for i, o in p["demos"]]
                spent += self.study(tuple(p["words"]), p["arity"], demos,
                                    min(CONFIRM + 2, budget - spent), recheck=True)
                q = self.phrases[key]
                changed |= (q["law"], show(self.laws[q["law"]].expr)) != before
            if not changed and not any(_same(v, out) for _, v in self.readings(items)):
                # every word held up when tested again: this run shows something it
                # has no idea for yet (say, a printed form it can't read); keep it apart
                self.aside.append(program)
                self.note("doubt", f"my words held up when I tested them again, so "
                                   f"{program!r} printing {printed} is something I can't "
                                   f"explain yet; I keep it apart and go on")
        return spent

    def _adjacent(self):
        """Ordered pairs of kinds of word it can put side by side in a program:
        'a A b B c' or 'A a B b', with plain numbers, or truth values it writes as
        comparisons, around them."""
        out = []
        for a in self.classes():
            pa = self.phrases[a]
            for b in self.classes():
                pb = self.phrases[b]
                if pb["arity"] != 2:
                    continue
                if pb["types"][1] == INT and pa["types"] in ([INT, INT], [INT]):
                    out.append((a, b))
                elif pa["out"] == pb["types"][0] and pb["out"] == pa["types"][-1]:
                    out.append((a, b))      # both groupings make sense: 'p AND q OR r'
        return out

    def _grammar_experiment(self, best, tried):
        """A program on which the best grammar and an equally simple rival disagree."""
        k = max(best[0].values()) + 1 if best[0] else 1
        for a, b in self._adjacent():
            if (a, b) in tried:
                continue
            first = self._holds_first(a, b, best)
            other = ("second" if first else "first", a, b)
            rival = self.solve(extra=[other], kmax=k, limit=20000)
            if rival is None:
                tried.add((a, b))
                continue
            program = self._pair_program(a, b, best, rival)
            tried.add((a, b))
            if program is not None:
                return program
        return None

    def _holds_first(self, a, b, best):
        lv, asc = best
        if self.phrases[a]["arity"] == 1:
            return lv[b] <= lv[a]
        return lv[a] > lv[b] or (lv[a] == lv[b] and asc.get(lv[a], "L") == "L")

    def _pair_program(self, a, b, g0, g1):
        """Operands for 'x A y B z' (or 'A x B y') where the two grammars disagree."""
        before, after = self.frame
        pa, pb = self.phrases[a], self.phrases[b]
        types = pa["types"] + pb["types"][1:]
        pools = [list(range(2, 9)) if t == INT else [True, False] for t in types]
        trials = [()]
        for pool in pools:
            trials = [t + (v,) for t in trials for v in pool]
        self.rng.shuffle(trials)
        for vals in trials[:150]:
            try:
                ops = [self.operand_text(v) for v in vals]
            except Unknown:
                return None
            if pa["arity"] == 1:
                body = pa["words"] + ops[0] + pb["words"] + ops[1]
            else:
                body = ops[0] + pa["words"] + ops[1] + pb["words"] + ops[2]
            program = " ".join(before + body + after)
            p0 = self.predict(program, levels=g0[0], assoc=g0[1])
            p1 = self.predict(program, levels=g1[0], assoc=g1[1])
            if p0 != p1:
                return program
        return None

    def imagine(self, n_ops, brackets=True):
        """A program Ultron writes itself: n_ops of its phrases, typed, small numbers."""
        rng = self.rng
        keys = sorted(self.phrases)
        ints = [k for k in keys if self.phrases[k]["out"] == INT]
        bools = [k for k in keys if self.phrases[k]["out"] == BOOL]
        opener = [m for m, r in sorted(self.marks.items()) if r == "open"]

        def build(want, n):
            if n == 0:
                if want == INT:
                    return [speak_number(self.brain, rng.randint(0, 12))]
                return None
            cands = ints if want == INT else bools
            rng_keys = list(cands)
            rng.shuffle(rng_keys)
            for key in rng_keys:
                p = self.phrases[key]
                if p["arity"] == 1:
                    sub = build(p["types"][0], n - 1)
                    if sub is not None:
                        return p["words"] + self._wrap(sub, opener, n - 1)
                    continue
                splits = list(range(n))
                rng.shuffle(splits)
                for left in splits:
                    a = build(p["types"][0], left)
                    b = build(p["types"][1], n - 1 - left)
                    if a is not None and b is not None:
                        return self._wrap(a, opener, left) + p["words"] + \
                            self._wrap(b, opener, n - 1 - left)
            return None

        before, after = self.frame
        for _ in range(50):
            want = INT if rng.random() < 0.6 or not bools else BOOL
            body = build(want, n_ops) or build(INT, n_ops)
            if body is None:
                return None
            program = " ".join(before + body + after)
            if self.predict(program) is not None:     # it writes what it can reason about
                return program
        return None

    def _wrap(self, toks, opener, n):
        if not opener or n == 0 or self.rng.random() > 0.3:
            return toks
        return [opener[0]] + toks + [_closer(self.marks)]

    def learn_marks(self):
        """What do marks it doesn't know do? It tries each role a mark can have (ignored,
        opening a group, closing one) and keeps the roles that explain every run."""
        unknown = set()
        for program, printed in self.runs:
            try:
                items = self.items(program)
            except Unknown:
                continue
            for it in items:
                if it[0] == "w" and not self.known(it[1], 1) and not self.known(it[1], 2):
                    if len(it[1]) == 1:
                        unknown.add(it[1][0])
        if not unknown:
            return None
        marks = sorted(unknown)
        roles = ["ignore", "open", "close"]
        import itertools
        best = None
        for combo in itertools.product(roles, repeat=len(marks)):
            trial = dict(self.marks)
            trial.update(zip(marks, combo))
            if list(trial.values()).count("open") > 1 or list(trial.values()).count("close") > 1:
                continue
            if ("open" in combo) != ("close" in combo):
                continue
            runs = [(p, o) for p, o in self.runs if o is not None
                    and any(m in p.split() for m in marks)]
            if runs and all(self._explains(p, o, marks=trial) for p, o in runs):
                cost = sum(r != "ignore" for r in combo)
                if best is None or cost < best[0]:
                    best = (cost, trial)
        if best is None:
            self.note("stuck", f"no role for {marks} explains the runs they appear in")
            return None
        self.marks = best[1]
        for m in marks:
            self.note("code", f"the mark '{m}' " + {
                "open": "opens a group: what follows, up to its partner, is worked out first",
                "close": "closes a group", "ignore": "changes nothing"}[self.marks[m]])
        return self.marks

    def describe_grammar(self):
        by = {}
        for c, lv in self.levels.items():
            by.setdefault(lv, []).append(" ".join(self.phrases[c]["words"]) +
                                         ("(before a value)" if self.phrases[c]["arity"] == 1
                                          else ""))
        parts = []
        for lv in sorted(by, reverse=True):
            chain = "" if not any(self.phrases[c]["arity"] == 2 for c in self.levels
                                  if self.levels[c] == lv) else \
                (", chaining from the left" if self.assoc.get(lv, "L") == "L"
                 else ", chaining from the right")
            parts.append("{" + ", ".join(sorted(by[lv])) + "}" + chain)
        return "tightest first: " + " > ".join(parts)


def _closer(marks):
    for m, r in marks.items():
        if r == "close":
            return m
    return None


def _same(a, b):
    return type(a) is type(b) and a == b


def evaluate_safe(expr, env, library):
    try:
        return evaluate(expr, env, library)
    except (Overflow, KeyError, TypeError, RecursionError, ZeroDivisionError):
        return None
