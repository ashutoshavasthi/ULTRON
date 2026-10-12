"""The Trainer's Engc programs with statements: lesson 101 (C2) and the Judge's exam.

The Trainer knows Engc; Ultron does not. Programs are written by a random builder that
keeps track of which names hold numbers and which hold lists, so every program it
hands out is well formed; each one is then run in the sandbox, and any that fails,
runs too long or prints huge numbers is thrown away. What a program prints always
comes from the sandbox, never from the builder.

    lesson programs   3-14 lines, loops of at most 6 turns, blocks nested at most 1
                      deep, recursion at most 4 calls deep, numbers 0-9
    exam programs     5-40 lines, loops of up to 1,000 turns, blocks nested up to 3
                      deep, recursion up to 12 calls deep, numbers 0-99

The exam (seeds 70xx) is never used while developing; development uses 75xx.
"""

import random

from ..code import sandbox

NAMES = ["a", "b", "c", "d", "k", "m", "n2", "t", "u", "v", "w", "x", "y", "z", "total",
         "count", "best", "acc", "s", "r"]
LISTS = ["xs", "ys", "seen", "row", "picks"]
LOOPS = ["i", "j", "q"]
ITEMS = ["e", "item", "p"]
ROUTINES = ["f", "g", "h", "step", "grow", "fold"]
PARAMS = ["n", "m"]
INT_WORDS = ["PLUS", "MINUS", "TIMES"]
SYMS = {"PLUS": "+", "MINUS": "-", "TIMES": "*", "MODULO": "%"}
COMPARE = ["IS GREATER THAN", "IS LESS THAN", "IS EQUAL TO", "IS AT LEAST", "IS AT MOST",
           "IS NOT"]
BIG = 10 ** 12

LESSON = {"lines": (3, 14), "turns": (1, 6), "nest": 1, "depth": 4, "top": 9,
          "routines": 1}
EXAM = {"lines": (5, 40), "turns": (1, 1000), "nest": 3, "depth": 12, "top": 99,
        "routines": 2}


class _Builder:
    def __init__(self, rng, spec, features):
        self.rng = rng
        self.spec = spec
        self.features = set(features)
        self.ints = []           # names holding numbers (in scope)
        self.lists = []          # names holding lists
        self.busy = set()        # loop counters and loop lists not to be changed
        self.routines = []       # (name, params)
        self.lines = []
        self.indent = 0

    # --- values ---
    def num(self):
        return str(self.rng.randint(0, self.spec["top"]))

    def atom(self):
        rng = self.rng
        if self.ints and rng.random() < 0.6:
            return rng.choice(self.ints)
        if self.lists and "lists" in self.features and rng.random() < 0.25:
            return f"THE {rng.choice(['LENGTH', 'SUM'])} OF {rng.choice(self.lists)}"
        return self.num()

    def int_expr(self, ops=None):
        rng = self.rng
        ops = rng.randint(0, 2) if ops is None else ops
        out = [self.atom()]
        for _ in range(ops):
            op = rng.choice(INT_WORDS + ["MODULO"])
            word = op if rng.random() < 0.7 else SYMS[op]
            if op == "MODULO":
                out += [word, str(rng.randint(2, 9))]
            else:
                out += [word, self.atom()]
        return " ".join(out)

    def cond(self):
        rng = self.rng
        c = f"{self.int_expr(rng.randint(0, 1))} {rng.choice(COMPARE)} {self.int_expr(0)}"
        if rng.random() < 0.2:
            c = f"NOT {c}"
        if rng.random() < 0.2:
            c += f" {rng.choice(['AND', 'OR'])} {self.int_expr(0)} " \
                 f"{rng.choice(COMPARE)} {self.int_expr(0)}"
        return c

    def call(self):
        name, params, recursive = self.rng.choice(self.routines)
        first = str(self.rng.randint(0, self.spec["depth"])) if recursive else \
            self.int_expr(self.rng.randint(0, 1))
        args = " , ".join(f"{p} EQUAL TO {first if i == 0 else self.int_expr(0)}"
                          for i, p in enumerate(params))
        return f"CALL {name} WITH {args}"

    # --- statements ---
    def emit(self, text):
        self.lines.append("    " * self.indent + text)

    def fresh(self, pool):
        free = [n for n in pool if n not in self.ints and n not in self.lists
                and n not in self.busy]
        return self.rng.choice(free) if free else None

    def statement(self, nest, budget):
        rng = self.rng
        kinds = ["set", "set", "print", "print"]
        if nest < self.spec["nest"]:
            kinds += ["if", "while"] + (["for"] if "lists" in self.features else [])
        if "lists" in self.features:
            kinds += ["list"]
        if self.routines:
            kinds += ["callset"]
        kind = rng.choice(kinds)
        if kind == "set" or (kind == "print" and not self.ints and rng.random() < 0.5):
            free = [n for n in self.ints if n not in self.busy]
            name = rng.choice(free) if free and rng.random() < 0.5 else self.fresh(NAMES)
            if name is None:
                return 0
            self.emit(f"SET {name} TO {self.int_expr()} .")
            if name not in self.ints:
                self.ints.append(name)
            return 1
        if kind == "print":
            r = rng.random()
            if r < 0.15 and self.lists:
                self.emit(f"PRINT {rng.choice(self.lists)} .")
            elif r < 0.3:
                self.emit(f"PRINT {self.cond()} .")
            else:
                self.emit(f"PRINT {self.int_expr()} .")
            return 1
        if kind == "callset":
            name = self.fresh(NAMES)
            if name is None:
                return 0
            self.emit(f"SET {name} TO {self.call()} .")
            self.ints.append(name)
            return 1
        if kind == "list":
            if self.lists and rng.random() < 0.6:
                xs = rng.choice([x for x in self.lists if x not in self.busy] or [None])
                if xs is None:
                    return 0
                self.emit(f"SET {xs} TO {xs} WITH {self.int_expr(rng.randint(0, 1))} ADDED .")
                return 1
            xs = self.fresh(LISTS)
            if xs is None:
                return 0
            if rng.random() < 0.3:
                self.emit(f"SET {xs} TO THE EMPTY LIST .")
            else:
                items = " , ".join(self.int_expr(0) for _ in range(rng.randint(1, 4)))
                self.emit(f"SET {xs} TO THE LIST {items} .")
            self.lists.append(xs)
            return 1
        if budget < 3:
            return 0
        if kind == "if":
            self.emit(f"IF {self.cond()} THEN :")
            used = self.block(nest + 1, budget - 2)
            if rng.random() < 0.5 and budget - used >= 3:
                self.emit("ELSE :")
                used += 1 + self.block(nest + 1, budget - used - 3)
            self.emit("END IF .")
            return used + 2
        if kind == "while":
            counter = next((c for c in LOOPS if c not in self.busy and c not in self.ints), None)
            if counter is None or budget < 5:
                return 0
            lo, hi = self.spec["turns"]
            turns = rng.randint(lo, hi if nest == 0 else min(hi, 12))
            self.emit(f"SET {counter} TO 0 .")
            self.emit(f"WHILE {counter} IS LESS THAN {turns} DO :")
            self.busy.add(counter)
            self.ints.append(counter)
            used = self.block(nest + 1, budget - 4)
            self.indent += 1
            self.emit(f"SET {counter} TO {counter} PLUS 1 .")
            self.indent -= 1
            self.emit("END WHILE .")
            self.busy.discard(counter)
            return used + 4
        if kind == "for":
            item = next((c for c in ITEMS if c not in self.busy and c not in self.ints), None)
            if item is None:
                return 0
            r = rng.random()
            if r < 0.4 and self.lists:
                over = rng.choice(self.lists)
                self.busy.add(over)
            elif r < 0.7:
                lo, hi = self.spec["turns"]
                hi = hi if nest == 0 else min(hi, 12)
                a = rng.randint(0, 3)
                over = f"THE NUMBERS {a} TO {a + rng.randint(lo, hi) - 1}"
            else:
                over = "THE LIST " + " , ".join(self.int_expr(0)
                                                for _ in range(rng.randint(1, 5)))
            self.emit(f"FOR EACH {item} IN {over} :")
            self.busy.add(item)
            self.ints.append(item)
            used = self.block(nest + 1, budget - 2)
            self.emit("END FOR .")
            self.busy.discard(item)
            if over in self.lists:
                self.busy.discard(over)
            return used + 2
        return 0

    def block(self, nest, budget):
        """Statements inside a block; names first set inside stay usable after it
        only if the block surely ran, so they are forgotten when it closes."""
        self.indent += 1
        ints, lists = list(self.ints), list(self.lists)
        used, tries = 0, 0
        want = self.rng.randint(1, max(1, min(4, budget)))
        while used < want and tries < 20:
            used += self.statement(nest, budget - used)
            tries += 1
        if used == 0:
            self.emit(f"PRINT {self.num()} .")
            used = 1
        self.ints = [n for n in self.ints if n in ints]
        self.lists = [n for n in self.lists if n in lists]
        self.indent -= 1
        return used

    def routine(self):
        rng = self.rng
        name = rng.choice([r for r in ROUTINES if r not in [x[0] for x in self.routines]])
        params = PARAMS[:rng.randint(1, 2)]
        sig = " , ".join(f"{p} AS NUMBER" for p in params)
        self.emit(f"DEFINE ROUTINE {name} WITH {sig} :")
        self.indent += 1
        saved = self.ints, self.lists
        self.ints, self.lists = list(params), []
        n = params[0]
        recursive = rng.random() < 0.6
        if recursive:
            # recursion on the first parameter, with a base case
            others = " , ".join(f"{p} EQUAL TO {p}" for p in params[1:])
            rest = f" , {others}" if others else ""
            self.emit(f"IF {n} IS LESS THAN {rng.randint(1, 2)} THEN :")
            self.indent += 1
            self.emit(f"RETURN {self.int_expr(rng.randint(0, 1))} .")
            self.indent -= 1
            self.emit("END IF .")
            op = rng.choice(["PLUS", "TIMES", "MINUS"])
            self.emit(f"RETURN {self.int_expr(0)} {op} ( CALL {name} WITH {n} EQUAL TO "
                      f"{n} MINUS 1{rest} ) .")
        else:
            if rng.random() < 0.5:
                self.emit(f"IF {self.cond()} THEN :")
                self.indent += 1
                self.emit(f"RETURN {self.int_expr()} .")
                self.indent -= 1
                self.emit("END IF .")
            self.emit(f"RETURN {self.int_expr()} .")
        self.ints, self.lists = saved
        self.indent -= 1
        self.emit("END ROUTINE .")
        self.routines.append((name, params, recursive))

    def build(self):
        rng = self.rng
        lo, hi = self.spec["lines"]
        target = rng.randint(lo, hi)
        if "routines" in self.features:
            for _ in range(rng.randint(1, self.spec["routines"])):
                if len(self.lines) < target - 3:
                    self.routine()
        tries = 0
        while len(self.lines) < target - 1 and tries < 60:
            self.statement(0, target - 1 - len(self.lines))
            tries += 1
        if self.ints:
            self.emit(f"PRINT {rng.choice(self.ints)} .")
        else:
            self.emit(f"PRINT {self.num()} .")
        return "\n".join(self.lines) + "\n"


FEATURES = ("lists", "routines")


def program(rng, spec=LESSON, features=FEATURES, tries=200):
    """One well-formed program and what the sandbox printed for it."""
    for _ in range(tries):
        b = _Builder(rng, spec, features)
        text = b.build()
        n = len(text.splitlines())
        if not spec["lines"][0] <= n <= spec["lines"][1]:
            continue
        out = sandbox.run(text, seconds=5)
        if not out["ok"] or not out["printed"] or len(out["printed"]) > 2000:
            continue
        if any(_huge(p) for p in out["printed"]):
            continue
        return text, out["printed"]
    raise RuntimeError("couldn't write a program")


def _huge(line):
    for tok in line.replace("[", " ").replace("]", " ").replace(",", " ").split():
        try:
            if abs(int(tok)) > BIG:
                return True
        except ValueError:
            pass
    return False


def exam_programs(seed, n=200):
    """The C2 exam: n held-out programs, 5-40 lines, loops up to 1,000 turns, blocks
    nested up to 3 deep. Recursion goes deeper than the lesson's because exam programs
    call their routines with bigger numbers."""
    rng = random.Random(seed)
    return [program(rng, EXAM) for _ in range(n)]


def first_programs(rng):
    """Short programs the Trainer shows first, each one making one thing plain (as a
    teacher shows each word on its own before mixing them): giving names values,
    printing, a test with an 'otherwise', a loop, walking a row, rows built, measured
    and added to, and routines that call themselves."""
    def n():
        return rng.randint(0, 9)

    def row(k):
        return " , ".join(str(n()) for _ in range(k))
    a, b = rng.sample(NAMES[:10], 2)
    xs = rng.choice(LISTS)
    f = rng.choice(ROUTINES)
    texts = [
        f"SET {a} TO {n()} .\nSET {b} TO {a} PLUS {n()} .\nPRINT {b} .\n",
        f"SET {a} TO {n()} .\nIF {a} IS GREATER THAN 4 THEN :\n    PRINT {n()} .\n"
        f"ELSE :\n    PRINT {n()} .\nEND IF .\n",
        f"SET i TO 0 .\nSET {a} TO 0 .\nWHILE i IS LESS THAN {rng.randint(2, 5)} DO :\n"
        f"    SET {a} TO {a} PLUS i .\n    SET i TO i PLUS 1 .\nEND WHILE .\nPRINT {a} .\n",
        f"SET {xs} TO THE LIST {row(rng.randint(2, 4))} .\nPRINT {xs} .\n",
        f"SET {xs} TO THE EMPTY LIST .\nSET {xs} TO {xs} WITH {n()} ADDED .\n"
        f"SET {xs} TO {xs} WITH {n()} ADDED .\nPRINT {xs} .\n",
        f"SET {xs} TO THE LIST {row(rng.randint(1, 4))} .\nSET {a} TO THE LENGTH OF {xs} .\n"
        f"SET {b} TO THE SUM OF {xs} .\nPRINT {a} .\nPRINT {b} .\n",
        f"SET {a} TO 0 .\nFOR EACH e IN THE NUMBERS {rng.randint(0, 2)} TO {rng.randint(3, 5)} :\n"
        f"    SET {a} TO {a} PLUS e .\nEND FOR .\nPRINT {a} .\n",
        f"SET {xs} TO THE LIST {row(3)} .\nFOR EACH e IN {xs} :\n    PRINT e .\nEND FOR .\n",
        f"FOR EACH e IN THE LIST {row(rng.randint(1, 3))} :\n    PRINT e TIMES 2 .\nEND FOR .\n",
        f"DEFINE ROUTINE {f} WITH n AS NUMBER , m AS NUMBER :\n    RETURN n TIMES m .\n"
        f"END ROUTINE .\nSET {a} TO CALL {f} WITH n EQUAL TO {n()} , m EQUAL TO {n()} .\n"
        f"PRINT {a} .\n",
        f"DEFINE ROUTINE {f} WITH n AS NUMBER :\n    IF n IS LESS THAN 1 THEN :\n"
        f"        RETURN 0 .\n    END IF .\n    RETURN n PLUS ( CALL {f} WITH n EQUAL TO n "
        f"MINUS 1 ) .\nEND ROUTINE .\nPRINT CALL {f} WITH n EQUAL TO {rng.randint(2, 4)} .\n",
    ]
    out = []
    for text in texts:
        res = sandbox.run(text)
        if res["ok"]:
            out.append((text, res["printed"]))
    return out
