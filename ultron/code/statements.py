"""Reading Engc statements: what each line does to memory (lesson 101, C2).

Ultron watches programs run as films: before each line runs, which line it is, how
deep in routine calls, and the value of every name (sandbox.trace), plus what was
printed. From the films it builds its own picture of how a program runs, and then
predicts what new programs print without running them.

What it is given (core knowledge, stated plainly, as `dsl.py` is for numbers):

  * a program is lines of words; a line can change one name, print one value, choose
    which line runs next, or hand back a value and leave a routine;
  * some lines open a block of lines and some close one; a block can be run, skipped,
    run again, or run once for each thing in a row; a routine is a block that runs
    when it is called, with fresh memory holding what it was given;
  * the row-building pieces of its program language (an empty row, a row with one
    more at its end, counting from one number to another).

What it finds itself, from the films (nothing about Engc is written in here):

  * which mark opens a block, which word closes one, which line splits a block in
    two (the "otherwise" part);
  * for each kind of line (by its first word): what it does (changes a name, prints,
    hands back a value, tests and enters its block, repeats it, walks a row, or is a
    routine), which word is the name, which words are the value or the test;
  * what each new phrase means (`THE LENGTH OF`, a row written out, counting out
    numbers, a row with one more), as the shortest program in its own language;
  * how a call is written: the word that calls, the words before the inputs, the
    words between an input's name and its value, the mark between inputs;
  * how a row is printed.

The meanings of operators, how they group, and how numbers and truth values print
come from lesson 100 (C1).
"""

from ..brain.dsl import BOOL, INT, LIST, Overflow, evaluate, from_json, show, to_json
from ..brain.synth import synthesize
from .reading import Unknown, _is_int

MAX_STEPS = 400_000      # lines it is willing to work through for one program
MAX_DEPTH = 300          # calls inside calls


def _norm(v):
    """A value from a film as Ultron holds it (rows as tuples)."""
    if isinstance(v, list):
        return tuple(_norm(x) for x in v)
    return v


def _type(v):
    if isinstance(v, bool):
        return BOOL
    if isinstance(v, tuple):
        return LIST
    return INT


class _Return(Exception):
    def __init__(self, value):
        self.value = value


class Program:
    """A program's lines, as Ultron sees them."""

    def __init__(self, text):
        self.text = text
        self.lines = [ln.split() for ln in text.split("\n")]
        while self.lines and not self.lines[-1]:
            self.lines.pop()

    def __len__(self):
        return len(self.lines)

    def toks(self, n):          # lines are numbered from 1, as the films number them
        return self.lines[n - 1]


class Machine:
    def __init__(self, brain, reader, state=None):
        st = state or {}
        self.brain = brain
        self.reader = reader
        self.library = reader.library
        self.end = st.get("end")                  # the mark that ends a plain line
        self.blocks = st.get("blocks")            # {"open", "close", "middle": [...]}
        self.kinds = {k: dict(v) for k, v in st.get("kinds", {}).items()}
        self.phrases = {k: dict(v) for k, v in st.get("phrases", {}).items()}
        self.call = st.get("call")                # how a call is written
        self.rows = st.get("rows")                # how a row is printed: [open, sep, close]
        self.stats = dict(st.get("stats", {"trainer": 0, "own": 0}))
        self.seen = [list(r) for r in st.get("seen", [])]    # [program, what it printed]
        self.films = []                           # (Program, film) watched in this lesson
        self.wanting = {}                         # phrases it wants to try itself
        self.world = None                         # set in a lesson: program -> film
        self._ops = None

    def to_json(self):
        return {"end": self.end, "blocks": self.blocks,
                "kinds": dict(sorted(self.kinds.items())),
                "phrases": dict(sorted(self.phrases.items())), "call": self.call,
                "rows": self.rows, "stats": self.stats, "seen": self.seen}

    def note(self, kind, text):
        self.brain.note(kind, text)

    # ============================================================ watching
    def watch(self, text, film, who="trainer"):
        self.stats[who] = self.stats.get(who, 0) + 1
        self.seen.append([text, list(film["printed"]) if film["ok"] else None])
        steps = [{"line": s["line"], "depth": s["depth"], "printed": s["printed"],
                  "memory": {k: _norm(v) for k, v in s["memory"].items()}}
                 for s in film["steps"]]
        names = sorted({k for s in steps for k in s["memory"]})
        final = {k: _norm(v) for k, v in (film.get("final") or {}).items()}
        self.films.append((Program(text), {"ok": film["ok"], "printed": film["printed"],
                                           "steps": steps, "names": names,
                                           "final": final if film["ok"] else None}))

    @property
    def total_runs(self):
        return sum(self.stats.values())

    # ============================================================ reading values
    def _op_index(self):
        if self._ops is None:
            ops = {1: {}, 2: {}}
            for key, p in self.reader.phrases.items():
                ops[p["arity"]].setdefault(p["words"][0], []).append((len(p["words"]), key))
            for d in ops.values():
                for v in d.values():
                    v.sort(reverse=True)
            self._ops = ops
        return self._ops

    def _match_op(self, toks, i, arity):
        for n, key in self._op_index()[arity].get(toks[i], []):
            if toks[i:i + n] == self.reader.phrases[key]["words"]:
                return key, n
        return None

    def _match_phrase(self, toks, i, lead):
        best = None
        for head, p in self.phrases.items():
            if bool(p.get("lead")) != lead:
                continue
            words = p["head"]
            if toks[i:i + len(words)] == words and (best is None or len(words) > len(best[1])):
                best = (head, words)
        return best

    def _marks(self):
        m = self.reader.marks
        return ([k for k, r in m.items() if r == "open"], [k for k, r in m.items() if r == "close"])

    def _extent(self, toks, i, stops):
        """Where a value that starts at i ends: at a stop word or a closing mark outside
        any group it opened, or at the end."""
        opens, closes = self._marks()
        depth = 0
        while i < len(toks):
            t = toks[i]
            if depth == 0 and (t in stops or t in closes):
                return i
            if t in opens:
                depth += 1
            elif t in closes:
                depth -= 1
            i += 1
        return i

    def parse(self, toks):
        """A line's value words as a tree (Unknown if it can't read them)."""
        reader = self.reader
        levels, assoc = reader.levels, reader.assoc
        opens, closes = self._marks()
        top = max(levels.values()) + 1 if levels else 0
        pos = [0]

        def level(key):
            c = reader.cls(key)
            if c not in levels:
                raise Unknown(f"I don't know how '{key}' groups")
            return levels[c]

        def slot(stops):
            j = self._extent(toks, pos[0], stops)
            sub = toks[pos[0]:j]
            if not sub:
                raise Unknown("a phrase with nothing in it")
            pos[0] = j
            return self.parse(sub)

        def operand():
            if pos[0] >= len(toks):
                raise Unknown("ends too soon")
            t = toks[pos[0]]
            v = reader.number(t)
            if v is not None:
                pos[0] += 1
                return ("val", v)
            if t in opens:
                pos[0] += 1
                e = expr(-1)
                if pos[0] >= len(toks) or toks[pos[0]] not in closes:
                    raise Unknown("a group that doesn't close")
                pos[0] += 1
                return e
            if self.call and t == self.call["word"]:
                return call()
            ph = self._match_phrase(toks, pos[0], lead=False)
            if ph is not None:
                head, words = ph
                pos[0] += len(words)
                return ("phrase", head, tail(self.phrases[head]))
            un = self._match_op(toks, pos[0], 1)
            if un is not None:
                key, n = un
                pos[0] += n
                return ("op", key, [expr(level(key) + 1)])
            if t[0].isalpha():
                pos[0] += 1
                return ("name", t)
            raise Unknown(f"I don't know '{t}' here")

        def tail(p):
            args = []
            parts = p["tail"]
            for k, part in enumerate(parts):
                if part[0] == "fixed":
                    if pos[0] >= len(toks) or toks[pos[0]] != part[1]:
                        raise Unknown("not the phrase I know")
                    pos[0] += 1
                elif part[0] == "series":
                    j = self._extent(toks, pos[0], ())
                    items, start, depth = [], pos[0], 0
                    for q in range(pos[0], j + 1):
                        if q == j or (depth == 0 and toks[q] == part[1]):
                            if q == start:
                                raise Unknown("an empty place in a row")
                            items.append(self.parse(toks[start:q]))
                            start = q + 1
                        elif toks[q] in opens:
                            depth += 1
                        elif toks[q] in closes:
                            depth -= 1
                    pos[0] = j
                    args.append(("row", items))
                else:                               # one value
                    nxt = parts[k + 1] if k + 1 < len(parts) else None
                    if nxt is not None and nxt[0] == "fixed":
                        args.append(slot({nxt[1]}))
                    elif p.get("wide"):
                        args.append(slot(()))
                    else:
                        args.append(expr(top))      # just what comes next
            return args

        def call():
            c = self.call
            pos[0] += 1
            if pos[0] >= len(toks):
                raise Unknown("a call to nothing")
            routine = toks[pos[0]]
            pos[0] += 1
            for w in c["with"]:
                if pos[0] >= len(toks) or toks[pos[0]] != w:
                    return ("call", routine, [])
                pos[0] += 1
            binds = []
            while True:
                if pos[0] >= len(toks):
                    raise Unknown("a call with an input missing")
                name = toks[pos[0]]
                pos[0] += 1
                for w in c["bind"]:
                    if pos[0] >= len(toks) or toks[pos[0]] != w:
                        raise Unknown("not a call I can read")
                    pos[0] += 1
                binds.append((name, slot({c["sep"]} if c.get("sep") else ())))
                if c.get("sep") and pos[0] < len(toks) and toks[pos[0]] == c["sep"]:
                    pos[0] += 1
                    continue
                return ("call", routine, binds)

        def expr(minl):
            left = operand()
            while pos[0] < len(toks):
                t = toks[pos[0]]
                ph = self._match_phrase(toks, pos[0], lead=True)
                if ph is not None and minl <= -1:
                    head, words = ph
                    pos[0] += len(words)
                    left = ("phrase", head, [left] + tail(self.phrases[head]))
                    continue
                bi = self._match_op(toks, pos[0], 2)
                if bi is None:
                    break
                key, n = bi
                lv = level(key)
                if lv < minl:
                    break
                pos[0] += n
                nxt = lv + 1 if assoc.get(lv, "L") == "L" else lv
                left = ("op", key, [left, expr(nxt)])
            return left

        tree = expr(-1)
        if pos[0] != len(toks):
            raise Unknown(f"words left over: {' '.join(toks[pos[0]:])}")
        return tree

    def evaluate(self, tree, env, run=None):
        tag = tree[0]
        if tag == "val":
            return tree[1]
        if tag == "name":
            if tree[1] not in env:
                raise Unknown(f"'{tree[1]}' has no value")
            return env[tree[1]]
        if tag == "row":
            return tuple(self.evaluate(t, env, run) for t in tree[1])
        if tag == "op":
            args = [self.evaluate(t, env, run) for t in tree[2]]
            if any(isinstance(a, tuple) for a in args):
                raise Unknown("an operator on a row")
            try:
                return self.reader.apply(tree[1], args)
            except (Overflow, KeyError, TypeError, RecursionError) as e:
                raise Unknown("can't work it out") from e
        if tag == "phrase":
            p = self.phrases.get(tree[1])
            if p is None or p.get("law") is None:
                raise Unknown(f"I don't know what '{tree[1]}' means yet")
            args = [self.evaluate(t, env, run) for t in tree[2]]
            if [_type(a) for a in args] != p["types"]:
                raise Unknown(f"'{tree[1]}' doesn't take that")
            try:
                v = evaluate(from_json(p["law"]), dict(zip(p["names"], args)), self.library)
            except (Overflow, KeyError, TypeError, IndexError) as e:
                raise Unknown("can't work it out") from e
            if v is None:
                raise Unknown("can't work it out")
            return v
        if tag == "call":
            if run is None:
                raise Unknown("a call, while I'm only looking")
            return run.call(tree[1], {n: self.evaluate(t, env, run) for n, t in tree[2]})
        raise Unknown(tag)

    def value(self, toks, env, run=None):
        return self.evaluate(self.parse(toks), env, run)

    def show_value(self, v):
        if isinstance(v, tuple):
            if not self.rows:
                return None
            parts = [self.show_value(x) for x in v]
            if any(p is None for p in parts) or (len(parts) > 1 and self.rows[1] is None):
                return None
            return self.rows[0] + (self.rows[1] or "").join(parts) + self.rows[2]
        return self.reader.show_value(v)

    # ============================================================ structure
    def structure(self, prog, blocks=None):
        """For each line that opens a block: where its block closes and where it splits
        (the 'otherwise' line), by the marks it learned. Returns (headers, middles,
        closers, parent) or None if the marks don't pair up."""
        b = blocks or self.blocks
        if not b:
            return None
        heads, middles, closers, parent = {}, {}, set(), {}
        stack = []
        for n in range(1, len(prog) + 1):
            t = prog.toks(n)
            if not t:
                continue
            parent[n] = stack[-1] if stack else None
            if t[0] == b["close"]:
                if not stack:
                    return None
                h = stack.pop()
                heads[h]["end"] = n
                closers.add(n)
            elif t[-1] == b["open"] and t[0] in b["middle"]:
                if not stack:
                    return None
                heads[stack[-1]]["middle"] = n
                middles[n] = stack[-1]
            elif t[-1] == b["open"]:
                heads[n] = {"end": None, "middle": None}
                stack.append(n)
        if stack:
            return None
        return heads, middles, closers, parent

    # ============================================================ learning
    def _frame_next(self, steps, i):
        """The next step in the same routine call as step i: (index, ended_call).
        ended_call: the call ended after this line (or the program did)."""
        d = steps[i]["depth"]
        for j in range(i + 1, len(steps)):
            if steps[j]["depth"] < d:
                return None, True
            if steps[j]["depth"] == d:
                return j, False
        return None, True

    def learn_blocks(self):
        """Which mark opens a block and which word closes one: the pair that explains
        every jump in the films (a line followed by one that isn't the next)."""
        ran = {}
        lasts, firsts, words_ran = set(), set(), set()
        for prog, film in self.films:
            seen = {s["line"] for s in film["steps"]}
            for n in range(1, len(prog) + 1):
                t = prog.toks(n)
                if t:
                    lasts.add(t[-1])
                    if n in seen:
                        words_ran.add(t[0])
            ran[id(prog)] = seen
        for prog, film in self.films:
            for n in range(1, len(prog) + 1):
                t = prog.toks(n)
                if t and t[0] not in words_ran:
                    firsts.add(t[0])       # a kind of line that never runs itself
        best = None
        for o in sorted(lasts):
            for c in sorted(firsts):
                middle = set()
                for prog, film in self.films:
                    for n in range(1, len(prog) + 1):
                        t = prog.toks(n)
                        if t and t[-1] == o and t[0] != c and t[0] not in words_ran:
                            middle.add(t[0])
                cand = {"open": o, "close": c, "middle": sorted(middle)}
                score = self._explained(cand)
                if score is not None and (best is None or score > best[0]):
                    best = (score, cand)
        if best is None:
            self.note("stuck", "no marks explain where the programs jump")
            return False
        changed = best[1] != self.blocks
        self.blocks = best[1]
        if changed:
            mid = (f"; a line starting '{best[1]['middle'][0]}' splits a block in two"
                   if best[1]["middle"] else "")
            self.note("code", f"lines ending '{best[1]['open']}' open a block of lines, a "
                              f"line starting '{best[1]['close']}' closes it{mid} "
                              f"({best[0]} jumps explained)")
        return True

    def _explained(self, cand):
        jumps = 0
        for prog, film in self.films:
            st = self.structure(prog, cand)
            if st is None:
                return None
            heads, middles, closers, parent = st
            steps = film["steps"]
            for i, s in enumerate(steps):
                j, ended = self._frame_next(steps, i)
                if j is None:
                    continue
                a, b = s["line"], steps[j]["line"]
                if b == a + 1 and b not in closers and b not in middles:
                    continue
                ok = False
                if a in heads:
                    h = heads[a]
                    ok = b == a + 1 or (h["end"] is not None and b == h["end"] + 1) or \
                        (h["middle"] is not None and b == h["middle"] + 1)
                anc = parent.get(a)
                while not ok and anc is not None:
                    ok = b == anc or b == heads[anc]["end"] + 1
                    anc = parent.get(anc)
                if not ok and a in heads and heads[a]["end"] is not None:
                    # a block skipped inside another: on to where that one goes next
                    anc = parent.get(a)
                    while not ok and anc is not None:
                        ok = b == anc or b == heads[anc]["end"] + 1
                        anc = parent.get(anc)
                if not ok:
                    return None
                jumps += 1
        return jumps

    def _instances(self):
        """Every line that ran, with what it saw before and after (same routine call)."""
        out = []
        for prog, film in self.films:
            st = self.structure(prog)
            if st is None:
                continue
            heads = st[0]
            steps = film["steps"]
            for i, s in enumerate(steps):
                j, ended = self._frame_next(steps, i)
                deeper = i + 1 < len(steps) and steps[i + 1]["depth"] > s["depth"]
                nxt = steps[j] if j is not None else None
                printed_to = nxt["printed"] if nxt else (
                    steps[i + 1]["printed"] if i + 1 < len(steps) and not deeper
                    else len(film["printed"]) if ended and s["depth"] == 0 and
                    i == len(steps) - 1 else None)
                last = nxt is None and s["depth"] == 0 and not any(
                    t["depth"] == 0 for t in steps[i + 1:])
                out.append({"prog": prog, "film": film, "i": i, "line": s["line"],
                            "toks": prog.toks(s["line"]), "before": s["memory"],
                            "after": nxt["memory"] if nxt else
                            (film["final"] if last else None),
                            "next": nxt["line"] if nxt else None, "ended": ended,
                            "depth": s["depth"], "calls": deeper,
                            "said": film["printed"][s["printed"]:printed_to]
                            if printed_to is not None else None,
                            "header": s["line"] in heads, "heads": heads})
        return out

    def _shared(self, rows, names=()):
        """The words every instance has in the same place, from the start and from the
        end: a kind of line's fixed words (a name is never a fixed word, even when every
        instance happens to use the same one)."""
        n = min(len(r) for r in rows)
        names = set(names)

        def same(ws):
            return len(set(ws)) == 1 and not (set(ws) & names) and \
                self.reader.number(ws[0]) is None
        front = 0
        while front < n and same([r[front] for r in rows]):
            front += 1
        back = 0
        while back < n - front and same([r[len(r) - 1 - back] for r in rows]):
            back += 1
        return front, back

    def learn_kinds(self):
        """What each kind of line does, from every time one ran."""
        inst = self._instances()
        by = {}
        for x in inst:
            by.setdefault(x["toks"][0], []).append(x)
        plain_ends = {x["toks"][-1] for x in inst if not x["header"]}
        if len(plain_ends) == 1:
            self.end = next(iter(plain_ends))
        demos = []
        for word in sorted(by):
            xs = by[word]
            self._known = self.kinds.get(word)
            if xs[0]["header"]:
                law = self._learn_header(word, xs, demos)
            else:
                law = self._learn_plain(word, xs, demos)
            if law is not None:
                if self.kinds.get(word) != law:
                    self.kinds[word] = law
                    self.note("code", f"a line starting '{word}' {self.describe(word)}")
        return demos

    def _fewer(self, does, p, f2):
        """Keep the fewer fixed words it already settled on (see simplify)."""
        k = getattr(self, "_known", None)
        if k and k["does"] == does and k.get("name") == p:
            return min(f2, k["span"][0] - p - 1)
        return f2

    def _names(self, xs):
        return {n for x in xs for n in x["film"]["names"]}

    def _learn_plain(self, word, xs, demos):
        toks = [x["toks"] for x in xs]
        front, back = self._shared(toks, self._names(xs))
        # it hands back a value and the routine ends
        if all(x["ended"] and x["depth"] > 0 for x in xs):
            return {"does": "return", "span": [front, back], "fixed": toks[0][:front]}
        # it changes one name
        changed = []
        for x in xs:
            if x["after"] is None:
                continue
            ch = sorted(k for k in x["after"] if x["before"].get(k, "∅") != x["after"][k])
            changed.append((x, ch))
        if changed and all(len(ch) <= 1 for _, ch in changed) and any(ch for _, ch in changed):
            for p in range(front, min(len(t) for t in toks)):
                if all(not ch or x["toks"][p] == ch[0] for x, ch in changed):
                    rest = [t[p + 1:] for t in toks]
                    f2, _ = self._shared(rest, self._names(xs))
                    f2 = self._fewer("set", p, f2)
                    span = [p + 1 + f2, back]
                    law = {"does": "set", "name": p, "span": span,
                           "fixed": toks[0][:front] + ["·"] + toks[0][p + 1:p + 1 + f2]}
                    targets = [(x["toks"][span[0]:len(x["toks"]) - span[1]], x["before"],
                                x["after"][x["toks"][p]]) for x, _ in changed]
                    if self._check(targets, demos):
                        return law
        # it prints one line
        said = [x for x in xs if x["said"] is not None and not x["calls"]]
        if said and all(len(x["said"]) == 1 for x in said):
            law = {"does": "print", "span": [front, back], "fixed": toks[0][:front]}
            self._learn_rows(law, said)
            if all(self._fits_print(law, x) is not False for x in said):
                for x in said:
                    # what it printed is an example of words it can't read yet
                    if self._fits_print(law, x) is None:
                        v = self.reader.value_of(x["said"])
                        if isinstance(v, (int, bool)) and not isinstance(v, tuple):
                            t = x["toks"]
                            demos.append((t[law["span"][0]:len(t) - law["span"][1]],
                                          x["before"], v))
                return law
        self.note("stuck", f"I can't tell what a line starting '{word}' does")
        return None

    def _check(self, targets, demos):
        """Do these value words give these values? Words it can't read yet become
        examples of a new phrase; any wrong value rules the guess out."""
        for toks, env, want in targets:
            try:
                got = self.value(toks, env)
            except Unknown:
                demos.append((toks, env, want))
                continue
            if got != want:
                return False
        return True

    def _fits_print(self, law, x):
        t = x["toks"]
        try:
            v = self.value(t[law["span"][0]:len(t) - law["span"][1]], x["before"])
        except Unknown:
            return None
        shown = self.show_value(v)
        return None if shown is None else shown == x["said"][0]

    def _learn_rows(self, law, said):
        """How a row is printed: the marks around it and between its things."""
        if self.rows and self.rows[1] is not None:
            return
        for x in said:
            t = x["toks"]
            words = t[law["span"][0]:len(t) - law["span"][1]]
            if len(words) != 1 or not isinstance(x["before"].get(words[0]), tuple):
                continue
            row, text = x["before"][words[0]], x["said"][0]
            parts = [self.reader.show_value(v) for v in row]
            if not parts or any(p is None for p in parts):
                continue
            if len(parts) == 1:
                a = text.find(parts[0])
                if a >= 0 and not self.rows:
                    self.rows = [text[:a], None, text[a + len(parts[0]):]]
                continue
            a = text.find(parts[0])
            b = text.find(parts[1], a + len(parts[0]))
            if a < 0 or b < 0:
                continue
            guess = [text[:a], text[a + len(parts[0]):b], None]
            guess[2] = text[len(guess[0] + guess[1].join(parts)):]
            if guess[0] + guess[1].join(parts) + guess[2] == text:
                self.rows = guess
                self.note("code", f"a row prints as {guess[0]}one{guess[1]}two{guess[2]}")
                return

    def _learn_header(self, word, xs, demos):
        toks = [x["toks"] for x in xs]
        front, back = self._shared(toks, self._names(xs))
        heads = xs[0]["heads"]
        entered = [x["next"] == x["line"] + 1 for x in xs]
        back_to = False
        for x in xs:
            h = x["heads"][x["line"]]
            if h["end"] is None:
                continue
            for y in self._block_runs(x):
                if y == x["line"]:
                    back_to = True
        if not any(entered) and any(self._called_into(x) for x in xs):
            # never entered where it stands: its block runs only when called
            return {"does": "routine", "name": front, "fixed": toks[0][:front]}
        # a test: enter if the words between the fixed ones hold
        targets = [(x["toks"][front:len(x["toks"]) - back], x["before"], e)
                   for x, e in zip(xs, entered)]
        tests = []
        ok = True
        for t, env, e in targets:
            try:
                v = self.value(t, env)
            except Unknown:
                continue
            if not isinstance(v, bool) or v != e:
                ok = False
                break
            tests.append(v)
        if ok and tests:
            return {"does": "test", "again": back_to, "span": [front, back],
                    "fixed": toks[0][:front]}
        # a walk along a row: one name takes each thing in turn
        walk = self._learn_walk(xs, front, back, demos)
        if walk is not None:
            walk["fixed"] = toks[0][:front] + ["·"] * (walk["name"] - front + 1) + \
                walk.pop("after")
            return walk
        self.note("stuck", f"I can't tell what a line starting '{word}' does")
        return None

    def _block_runs(self, x):
        """Lines that ran right after this header's block, in the same call."""
        steps = x["film"]["steps"]
        h = x["heads"][x["line"]]
        out = []
        for i, s in enumerate(steps):
            if x["line"] < s["line"] < h["end"]:
                j, _ = self._frame_next(steps, i)
                if j is not None and not (x["line"] < steps[j]["line"] < h["end"]):
                    out.append(steps[j]["line"])
        return out

    def _called_into(self, x):
        steps = x["film"]["steps"]
        return any(s["line"] == x["line"] + 1 and s["depth"] > x["depth"] for s in steps)

    def _learn_walk(self, xs, front, back, demos):
        """Find the name that takes a new value each time the block is entered, and the
        words whose value is the row of those values."""
        by_film = {}
        for x in xs:
            by_film.setdefault(id(x["film"]), []).append(x)
        acts = []          # (toks, env at start, name position, [values])
        for group in by_film.values():
            cur = None
            for x in sorted(group, key=lambda x: x["i"]):
                steps = x["film"]["steps"]
                came_back = x["i"] > 0 and self._from_inside(x)
                if not came_back:
                    cur = {"x": x, "vals": [], "done": False}
                    acts.append(cur)
                if cur is None:
                    continue
                if x["next"] == x["line"] + 1:
                    cur["vals"].append(steps[self._frame_next(steps, x["i"])[0]]["memory"])
                else:
                    cur["done"] = True
        toks0 = xs[0]["toks"]
        for p in range(front, len(toks0) - back):
            if any(len(a["x"]["toks"]) <= p for a in acts):
                continue
            rows = []
            fine = True
            for a in acts:
                name = a["x"]["toks"][p]
                vals = [m.get(name, "∅") for m in a["vals"]]
                if "∅" in vals:
                    fine = False
                    break
                rows.append((a, tuple(vals)))
            if not fine or not rows:
                continue
            rest = [a["x"]["toks"][p + 1:] for a in acts]
            f2, _ = self._shared(rest, self._names(xs))
            f2 = self._fewer("walk", p, f2)
            span = [p + 1 + f2, back]
            targets = [(a["x"]["toks"][span[0]:len(a["x"]["toks"]) - span[1]],
                        a["x"]["before"], row) for a, row in rows if a["done"]]
            if targets and self._check(targets, demos):
                return {"does": "walk", "name": p, "span": span,
                        "after": toks0[p + 1:p + 1 + f2]}
        return None

    def _from_inside(self, x):
        steps = x["film"]["steps"]
        h = x["heads"][x["line"]]
        d = x["depth"]
        for k in range(x["i"] - 1, -1, -1):
            if steps[k]["depth"] < d:
                return False
            if steps[k]["depth"] == d:
                return h["end"] is not None and x["line"] < steps[k]["line"] < h["end"]
        return False

    # ------------------------------------------------------------ phrases
    def learn_phrases(self, demos):
        """New phrases: the words it couldn't read, with the values they turned out to
        have. Their shape (fixed words, places for values, a mark between many values)
        comes from lining examples up; their meaning is its ordinary law search."""
        groups = {}
        for toks, env, want in demos:
            if self.call and self.call["word"] in toks:
                continue
            shape = self._shape(toks, env)
            if shape is None:
                continue
            key, parts, lead, lead_val = shape
            g = groups.setdefault(key, {"lead": lead, "ex": []})
            g["ex"].append((parts, lead_val, want, env))
        for key, g in groups.items():
            # many values with one mark between them, in some example: a row of values
            sep = None
            for parts, _, _, _ in g["ex"]:
                marks = {parts[i][1] for i in range(1, len(parts), 2) if parts[i][0] == "fixed"}
                if len(parts) >= 5 and len(marks) == 1 and \
                        all(parts[i][0] == "slot" for i in range(0, len(parts), 2)):
                    sep = next(iter(marks))
            ex, tails = [], []
            for parts, lead_val, want, env in g["ex"]:
                if sep is not None:
                    if not all(parts[i][0] == "slot" for i in range(0, len(parts), 2)) or \
                            any(parts[i] != ("fixed", sep) for i in range(1, len(parts), 2)):
                        continue
                    args = [tuple(self._val(parts[i][1], env) for i in range(0, len(parts), 2))]
                    if any(v == "?" for v in args[0]):
                        continue
                    tail = (("series", sep),)
                else:
                    args = [self._val(p[1], env) for p in parts if p[0] == "slot"]
                    tail = tuple(("fixed", p[1]) if p[0] == "fixed" else ("slot",)
                                 for p in parts)
                    # what kind of value each place holds, from the first word in it
                    g.setdefault("kinds", []).append(
                        [_type(self._val(p[1][:1], env)) if self._val(p[1][:1], env) != "?"
                         else None for p in parts if p[0] == "slot"])
                if lead_val is not None:
                    args = [lead_val] + args
                tails.append(tail)
                ex.append((tail, args, want))
            if not ex:
                g["ex"], g["tail"] = [], None
                continue
            # the shape most examples have (others had more than this phrase in them)
            common = max(sorted(set(tails)), key=tails.count)
            g["ex"] = [(a, w) for t, a, w in ex if t == common]
            g["tail"] = [list(t) for t in common]
            g["kinds"] = [k for k in g.get("kinds", []) if len(k) == sum(
                1 for t in common if t[0] == "slot")]
        changed = False

        def inside(small, big):
            a, b = small.replace("· ", "").split(), big.replace("· ", "").split()
            return len(a) < len(b) and any(b[i:i + len(a)] == a for i in range(len(b)))
        for key in sorted(groups):
            g = groups[key]
            if key in self.phrases and self.phrases[key].get("law"):
                continue
            # a phrase with another one inside it waits until that one is known
            if any(inside(k, key) and len(groups[k]["ex"]) >= 3 and k not in self.phrases
                   for k in groups if k != key):
                continue
            if __import__("os").environ.get("DBG"):
                print("GROUP", key, g["tail"], len(g["ex"]), g.get("kinds", [])[:3])
            if g["tail"] is None:
                continue
            ex = [(a, w) for a, w in g["ex"] if all(not isinstance(v, str) for v in a)]
            if len(ex) < 3 and not g["lead"] and g.get("kinds"):
                # too few clean examples: it will try the phrase itself
                kinds = [k for k in g["kinds"] if None not in k]
                if kinds:
                    self.wanting[key] = {"tail": g["tail"], "types": kinds[0]}
            if len(ex) < 3 or len({len(a) for a, _ in ex}) != 1:
                continue
            self.wanting.pop(key, None)
            types = [_type(v) for v in ex[0][0]]
            if any([_type(v) for v in a] != types for a, _ in ex):
                continue
            out_t = _type(ex[0][1])
            names = [("a", "b", "c")[i] if t != LIST else ("row", "other")[i % 2]
                     for i, t in enumerate(types)]
            if len(set(names)) != len(names):
                names = [f"v{i}" for i in range(len(types))]
            res = synthesize([dict(zip(names, a)) for a, _ in ex], [w for _, w in ex],
                             dict(zip(names, types)), out_t, self.brain.library,
                             self.brain.constants(), max_size=5, max_bank=20000,
                             extra=self.brain.primitives() + ("rows",))
            if res.expr is None:
                self.note("stuck", f"I can't find what '{key}' means")
                continue
            self.phrases[key] = {"head": key.split(" ") if not g["lead"] else
                                 [key.split(" ", 1)[1].split(" ")[0]],
                                 "tail": g["tail"], "lead": g["lead"], "names": names,
                                 "types": types, "out": out_t, "law": to_json(res.expr),
                                 "runs": len(ex)}
            if g["lead"]:
                self.phrases[key]["head"] = key.split(" ")[1:2]
            changed = True
            self.note("code", f"'{key}' means {show(res.expr)} to me "
                              f"({len(ex)} examples)")
        return changed

    def _shape(self, toks, env):
        """Line up a phrase: its fixed words (those that are not values it can read)
        and the places in between that hold values. Returns (key, the parts after its
        first fixed words, whether a value comes first, that value)."""
        def readable(t):
            return self.reader.number(t) is not None or t in env or \
                self._match_op([t], 0, 2) is not None or self._match_op([t], 0, 1) is not None \
                or t in self.reader.marks
        parts = []
        k = 0
        while k < len(toks):
            if readable(toks[k]):
                j = k
                while j < len(toks) and readable(toks[j]):
                    j += 1
                parts.append(("slot", toks[k:j]))
                k = j
            else:
                parts.append(("fixed", toks[k]))
                k += 1
        if not any(p[0] == "fixed" for p in parts):
            return None
        lead = parts[0][0] == "slot"
        lead_val = self._val(parts[0][1], env) if lead else None
        if lead_val == "?":
            return None         # it can't tell where the phrase starts
        q = 1 if lead else 0
        head = []
        while q < len(parts) and parts[q][0] == "fixed":
            head.append(parts[q][1])
            q += 1
        key = ("· " if lead else "") + " ".join(head)
        return key, parts[q:], lead, lead_val

    def _val(self, toks, env):
        try:
            return self.value(toks, env)
        except Unknown:
            return "?"

    # ------------------------------------------------------------ calls
    def learn_calls(self):
        """How a call is written: in a line that sent the film one routine deeper, the
        routine's name, the word before it, and how each input is given its value."""
        found = []
        for prog, film in self.films:
            st = self.structure(prog)
            if st is None:
                continue
            steps = film["steps"]
            for i in range(len(steps) - 1):
                a, b = steps[i], steps[i + 1]
                if b["depth"] != a["depth"] + 1:
                    continue
                header = prog.toks(b["line"] - 1)
                k = self.kinds.get(header[0], {})
                if k.get("does") != "routine":
                    continue
                routine = header[k["name"]]
                line = prog.toks(a["line"])
                if routine not in line:
                    continue
                found.append((line, line.index(routine), a["memory"], b["memory"]))
        if not found:
            return False
        words = {line[q - 1] for line, q, _, _ in found if q > 0}
        if len(words) != 1:
            return False
        best = None
        for nbind in range(0, 4):
            for nwith in range(0, 3):
                cand = self._call_guess(found, nwith, nbind)
                if cand is not None and (best is None or (-cand["checked"], nbind + nwith)
                                         < best[0]):
                    best = ((-cand["checked"], nbind + nwith), cand)
        if best is None:
            self.note("stuck", "I can't tell how a call gives its inputs")
            return False
        cand = best[1]
        cand.pop("checked")
        cand["word"] = next(iter(words))
        if cand != self.call:
            self.call = cand
            self.note("code", f"a call is written '{cand['word']} <routine> "
                              f"{' '.join(cand['with'])} <input> {' '.join(cand['bind'])} "
                              f"<value>'" + (f", inputs split by '{cand['sep']}'"
                                             if cand.get("sep") else ""))
        return True

    def _call_guess(self, found, nwith, nbind):
        withs, binds, seps = set(), set(), set()
        checked = 0
        for line, q, mem, entry in found:
            w = tuple(line[q + 1:q + 1 + nwith])
            withs.add(w)
            p = q + 1 + nwith
            left = set(entry)
            while left:
                n = line[p] if p < len(line) else None
                if n not in left:
                    return None
                left.discard(n)
                bind = tuple(line[p + 1:p + 1 + nbind])
                binds.add(bind)
                p += 1 + nbind
                # the value runs to the end of the call, or to a mark followed by the
                # next input's name and the same binding words
                end = self._extent(line, p, {self.end} if self.end else ())
                if left:
                    j = next((j for j in range(p + 1, end - 1) if line[j + 1] in left
                              and tuple(line[j + 2:j + 2 + nbind]) == bind), None)
                    if j is None:
                        return None
                    seps.add(line[j])
                    end = j
                try:
                    v = self.value(line[p:end], mem)
                except Unknown:
                    p = end + 1
                    continue
                if v != entry[n]:
                    return None
                checked += 1
                p = end + 1
        if len(withs) != 1 or len(binds) != 1 or len(seps) > 1 or not checked:
            return None
        return {"with": list(next(iter(withs))), "bind": list(next(iter(binds))),
                "sep": next(iter(seps)) if seps else None, "checked": checked}

    # ------------------------------------------------------------ its own experiments
    def write_set(self, name, words):
        """A line that gives a name a value, written the way such lines are written."""
        k = next((k for k in self.kinds.values() if k["does"] == "set"), None)
        if k is None or self.end is None:
            raise Unknown("I can't write a line that sets a name yet")
        return " ".join([name if w == "·" else w for w in k["fixed"]] + list(words) +
                        [self.end])

    def write_value(self, v):
        """Words for a value: a number, or a row written out."""
        if isinstance(v, tuple):
            # the way of writing it saw most often
            for head, p in sorted(self.phrases.items(), key=lambda kv: (-kv[1]["runs"], kv[0])):
                law = p.get("law")
                if v and len(p["tail"]) == 1 and p["tail"][0][0] == "series" and \
                        law == ["var", p["names"][0]]:
                    out = list(p["head"])
                    for i, x in enumerate(v):
                        out += ([p["tail"][0][1]] if i else []) + self.write_value(x)
                    return out
                if not v and law == ["nil"] and not p["tail"]:
                    return list(p["head"])
            raise Unknown("I can't write that row")
        if isinstance(v, bool) or not _is_int(v) or v < 0:
            raise Unknown("I only write counting numbers here")
        from ..brain.language import speak_number
        return [speak_number(self.brain, v)]

    def experiment(self, budget):
        """Phrases it saw too seldom on their own: it writes programs that use them on
        values it chooses, runs them and watches. Returns runs spent."""
        spent = 0
        rows = [(3, 1, 4), (), (5,), (2, 7, 1, 8), (9, 9)]
        nums = [3, 0, 7, 12, 5]
        names = sorted({n for _, f in self.films for n in f["names"]})[:6]
        for key in sorted(self.wanting):
            want = self.wanting[key]
            if want["tail"] != [["slot"]] or len(names) < 3:
                continue
            for k in range(5):
                if spent >= budget:
                    return spent
                args = [rows[k] if t == LIST else nums[k] for t in want["types"]]
                try:
                    lines, words = [], list(key.split())
                    for i, a in enumerate(args):
                        if isinstance(a, tuple):
                            lines.append(self.write_set(names[i], self.write_value(a)))
                            words.append(names[i])
                        else:
                            words += self.write_value(a)
                    lines.append(self.write_set(names[-1], words))
                except Unknown:
                    break
                text = "\n".join(lines) + "\n"
                film = self.world(text)
                self.watch(text, film, who="own")
                spent += 1
            self.note("code", f"I wrote {k + 1} programs of my own to see what '{key}' does")
        self.wanting = {}
        return spent

    # ============================================================ running in its head
    def learn(self):
        """Everything from the films it has watched so far."""
        if not self.learn_blocks():
            return
        for _ in range(8):
            demos = self.learn_kinds()
            self.learn_calls()
            grew = self.learn_phrases(demos)
            if not self.simplify() and not grew:
                break

    def simplify(self):
        """A kind of line may have taken words that only happened to be the same every
        time (say 'IN THE' because every row it saw was written 'THE ...') as its own
        fixed words. With fewer fixed words the description is shorter; it keeps the
        fewest that still read every line it saw. Returns whether anything changed."""
        inst = self._instances()
        changed = False
        for word, k in sorted(self.kinds.items()):
            if k["does"] not in ("set", "walk", "test", "print", "return"):
                continue
            xs = [x for x in inst if x["toks"][0] == word]
            lo = k["name"] + 1 if "name" in k else 1
            for start in range(lo, k["span"][0]):
                reads = [self._reads(k, x, start) for x in xs]
                if False not in reads and True in reads:
                    cut = k["span"][0] - start
                    self.kinds[word] = dict(k, span=[start, k["span"][1]],
                                            fixed=k["fixed"][:len(k["fixed"]) - cut])
                    self.note("code", f"a line starting '{word}' has fewer fixed words "
                                      f"than I thought: "
                                      f"{' '.join(self.kinds[word]['fixed'])} <value>")
                    changed = True
                    break
        return changed

    def _reads(self, k, x, start):
        t = x["toks"]
        try:
            v = self.value(t[start:len(t) - k["span"][1]], x["before"])
        except Unknown:
            return None                 # words it can't read yet: no evidence either way
        d = k["does"]
        if d == "set":
            return x["after"] is None or x["after"].get(t[k["name"]]) == v
        if d == "walk":
            return isinstance(v, tuple)
        if d == "test":
            return isinstance(v, bool) and v == (x["next"] == x["line"] + 1)
        if d == "print":
            shown = self.show_value(v)
            return x["said"] is None or shown is None or x["said"][-1:] == [shown]
        return True

    def predict(self, text):
        """What the program prints, worked out in its head (None: it doesn't know)."""
        try:
            return _Run(self, Program(text)).go()
        except (Unknown, Overflow, RecursionError, _Return):
            return None

    def describe(self, word):
        k = self.kinds.get(word)
        if not k:
            return "does something I don't know"
        d = k["does"]
        fixed = " ".join(k.get("fixed", [])) or word
        if d == "set":
            return f"gives the name in place {k['name'] + 1} the value of the words after '{fixed}'"
        if d == "print":
            return "prints the value of the words after it"
        if d == "return":
            return "hands back the value of the words after it, and the routine ends"
        if d == "test":
            return ("runs its block again and again while the words after it hold"
                    if k["again"] else "runs its block only if the words after it hold "
                                       "(else the part after the split, if any)")
        if d == "walk":
            return (f"runs its block once for each thing in the row after it, with the "
                    f"name in place {k['name'] + 1} holding that thing")
        if d == "routine":
            return (f"names a routine (the word in place {k['name'] + 1}): its block runs "
                    f"only when called")
        return d


class _Run:
    """Ultron working a program through in its head, with its learned laws."""

    def __init__(self, m, prog):
        self.m = m
        self.prog = prog
        st = m.structure(prog)
        if st is None:
            raise Unknown("blocks that don't pair up")
        self.heads, self.middles, self.closers, _ = st
        self.out = []
        self.steps = 0
        self.depth = 0
        self.routines = {}
        for h in self.heads:
            k = m.kinds.get(prog.toks(h)[0])
            if k and k["does"] == "routine":
                self.routines[prog.toks(h)[k["name"]]] = h

    def go(self):
        env = {}
        self.block(1, len(self.prog) + 1, env)
        return self.out

    def span(self, k, toks):
        return toks[k["span"][0]:len(toks) - k["span"][1]]

    def block(self, a, b, env):
        m = self.m
        n = a
        while n < b:
            toks = self.prog.toks(n)
            if not toks or n in self.closers:
                n += 1
                continue
            self.steps += 1
            if self.steps > MAX_STEPS:
                raise Unknown("too long to work through in my head")
            k = m.kinds.get(toks[0])
            if k is None:
                raise Unknown(f"I don't know what '{toks[0]}' does")
            fixed = k.get("fixed", [])
            if len(toks) < len(fixed) or any(w != "·" and w != t for w, t in zip(fixed, toks)):
                raise Unknown(f"a '{toks[0]}' line of a shape I haven't seen")
            d = k["does"]
            if n in self.heads:
                h = self.heads[n]
                end = h["end"]
                if end is None:
                    raise Unknown("an open block")
                mid = h["middle"]
                if d == "routine":
                    n = end + 1
                    continue
                if d == "test" and not k["again"]:
                    if self.truth(k, toks, env):
                        self.block(n + 1, mid or end, env)
                    elif mid is not None:
                        self.block(mid + 1, end, env)
                    n = end + 1
                    continue
                if d == "test":
                    while self.truth(k, toks, env):
                        self.block(n + 1, end, env)
                        self.steps += 1
                        if self.steps > MAX_STEPS:
                            raise Unknown("too long to work through in my head")
                    n = end + 1
                    continue
                if d == "walk":
                    row = m.value(self.span(k, toks), env, self)
                    if not isinstance(row, tuple):
                        raise Unknown("a walk along something that isn't a row")
                    for item in row:
                        env[toks[k["name"]]] = item
                        self.block(n + 1, end, env)
                        self.steps += 1
                    n = end + 1
                    continue
                raise Unknown(f"I don't know how '{toks[0]}' runs its block")
            if d == "set":
                env[toks[k["name"]]] = m.value(self.span(k, toks), env, self)
            elif d == "print":
                text = m.show_value(m.value(self.span(k, toks), env, self))
                if text is None:
                    raise Unknown("I can't say how that prints")
                self.out.append(text)
            elif d == "return":
                raise _Return(m.value(self.span(k, toks), env, self))
            else:
                raise Unknown(f"I don't know what '{toks[0]}' does")
            n += 1

    def truth(self, k, toks, env):
        v = self.m.value(self.span(k, toks), env, self)
        if not isinstance(v, bool):
            raise Unknown("a test that isn't true or false")
        return v

    def call(self, routine, given):
        h = self.routines.get(routine)
        if h is None:
            raise Unknown(f"no routine called '{routine}'")
        self.depth += 1
        if self.depth > MAX_DEPTH:
            raise Unknown("calls too deep")
        try:
            self.block(h + 1, self.heads[h]["end"], dict(given))
        except _Return as r:
            return r.value
        finally:
            self.depth -= 1
        raise Unknown("a routine that hands nothing back")
