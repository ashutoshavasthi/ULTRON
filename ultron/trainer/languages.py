"""Second languages for C3 (lessons 102 and 103): the Trainer's own translations.

Ultron never sees anything here. The Trainer writes every lesson program and exam
program in Engc with the same generators as lessons 100 and 101, then translates it:

  * the invented language: every Engc word and mark gets a fresh word or mark of its
    own (numbers and names stay as they are), chosen once from a fixed seed;
  * a Python subset: Python's own words and marks, blocks shown only by indentation,
    `f ( n = 3 )` for calls, `[ 1 , 2 ]` for rows, `len`, `sum`, `range`.

Programs in the invented language are run by translating them back to Engc; Python
programs are run as Python. What a program prints always comes from running it.
"""

import contextlib
import io
import random
import signal
import sys

from ..code import sandbox

ENGC_WORDS = ["PRINT", "SET", "TO", "IF", "THEN", "ELSE", "END", "WHILE", "DO", "FOR",
              "EACH", "IN", "DEFINE", "ROUTINE", "WITH", "AS", "NUMBER", "RETURN", "CALL",
              "EQUAL", "THE", "LIST", "NUMBERS", "EMPTY", "LENGTH", "OF", "SUM", "ADDED",
              "PLUS", "MINUS", "TIMES", "MODULO", "RAISED", "IS", "GREATER", "THAN", "LESS",
              "AT", "LEAST", "MOST", "NOT", "AND", "OR"]
ENGC_MARKS = ["+", "-", "*", "%", "**", ">", "<", "==", ">=", "<=", "!=", "(", ")", ",",
              ":", "."]
FRESH_MARKS = ["@", "#", "$", "&", "~", "|", "^", "?", "!", "<<", ">>", "=>", "{", "}",
               ";", "!!"]


def _fresh_words(seed):
    rng = random.Random(seed)
    cons, vows = "BDFGKLMNPRSTVZ", "AEIOU"
    out, used = [], set(ENGC_WORDS)
    while len(out) < len(ENGC_WORDS):
        w = "".join(rng.choice(cons) + rng.choice(vows) for _ in range(rng.randint(2, 3)))
        if w not in used:
            used.add(w)
            out.append(w)
    return out


class Invented:
    """Engc with every word and mark replaced by a fresh one (seed 102 fixes them)."""

    def __init__(self, seed=102):
        words = _fresh_words(seed)
        marks = list(FRESH_MARKS)
        random.Random(seed).shuffle(marks)
        self.out = dict(zip(ENGC_WORDS, words))
        self.out.update(zip(ENGC_MARKS, marks))
        self.back = {v: k for k, v in self.out.items()}

    def from_engc(self, text):
        return "\n".join(self._line(ln, self.out) for ln in text.split("\n"))

    def to_engc(self, text):
        return "\n".join(self._line(ln, self.back) for ln in text.split("\n"))

    @staticmethod
    def _line(ln, table):
        indent = ln[:len(ln) - len(ln.lstrip(" "))]
        return indent + " ".join(table.get(t, t) for t in ln.split())

    def run(self, text):
        return sandbox.run(self.to_engc(text))

    def trace(self, text):
        return sandbox.trace(self.to_engc(text))


# ---------------------------------------------------------------- Python
PY_OPS = {("IS", "GREATER", "THAN"): ">", ("IS", "LESS", "THAN"): "<",
          ("IS", "EQUAL", "TO"): "==", ("IS", "AT", "LEAST"): ">=", ("IS", "AT", "MOST"): "<=",
          ("RAISED", "TO"): "**", ("IS", "NOT"): "!=", ("PLUS",): "+", ("MINUS",): "-",
          ("TIMES",): "*", ("MODULO",): "%", ("AND",): "and", ("OR",): "or", ("NOT",): "not"}


def _py_expr(toks):
    """An Engc value (as the generators write them) in Python, token by token."""
    out, i = [], 0
    while i < len(toks):
        t = toks[i]
        if toks[i:i + 3] in (["THE", "LENGTH", "OF"], ["THE", "SUM", "OF"]):
            out += ["len" if toks[i + 1] == "LENGTH" else "sum", "(", toks[i + 3], ")"]
            i += 4
            continue
        if toks[i:i + 3] == ["THE", "EMPTY", "LIST"]:
            out += ["[", "]"]
            i += 3
            continue
        if toks[i:i + 2] == ["THE", "LIST"]:
            j = _group_end(toks, i + 2)
            out += ["["] + _py_expr(toks[i + 2:j]) + ["]"]
            i = j
            continue
        if toks[i:i + 2] == ["THE", "NUMBERS"]:
            a, b = toks[i + 2], toks[i + 4]
            out += ["range", "(", a, ",", str(int(b) + 1), ")"]
            i += 5
            continue
        if t == "CALL":
            j = _group_end(toks, i + 1)
            name = toks[i + 1]
            args, k = [], i + 3
            parts = []
            while k < j:
                p = toks[k]
                m = k + 3           # after 'p EQUAL TO'
                e = m
                depth = 0
                while e < j:
                    if toks[e] == "(":
                        depth += 1
                    elif toks[e] == ")":
                        depth -= 1
                    elif depth == 0 and toks[e] == "," and e + 2 < j and \
                            toks[e + 2:e + 4] == ["EQUAL", "TO"]:
                        break
                    e += 1
                parts.append([p, "="] + _py_expr(toks[m:e]))
                k = e + 1
            for n, p in enumerate(parts):
                args += ([","] if n else []) + p
            out += [name, "("] + args + [")"]
            i = j
            continue
        hit = next(((k, v) for k, v in sorted(PY_OPS.items(), key=lambda kv: -len(kv[0]))
                    if tuple(toks[i:i + len(k)]) == k), None)
        if hit:
            out.append(hit[1])
            i += len(hit[0])
            continue
        out.append(t)
        i += 1
    return out


def _group_end(toks, i):
    depth = 0
    while i < len(toks):
        if toks[i] == "(":
            depth += 1
        elif toks[i] == ")":
            if depth == 0:
                return i
            depth -= 1
        i += 1
    return i


def to_python(text):
    """An Engc program from the generators, in the Python subset."""
    out = []
    for ln in text.split("\n"):
        if not ln.strip():
            continue
        indent = ln[:len(ln) - len(ln.lstrip(" "))]
        t = ln.split()
        if t[0] == "END":
            continue
        if t[0] == "SET":
            body = [t[1], "="] + _py_expr(t[3:-1])
        elif t[0] == "PRINT":
            body = ["print", "("] + _py_expr(t[1:-1]) + [")"]
        elif t[0] == "RETURN":
            body = ["return"] + _py_expr(t[1:-1])
        elif t[0] == "IF":
            body = ["if"] + _py_expr(t[1:-2]) + [":"]
        elif t[0] == "ELSE":
            body = ["else", ":"]
        elif t[0] == "WHILE":
            body = ["while"] + _py_expr(t[1:-2]) + [":"]
        elif t[0] == "FOR":
            body = ["for", t[2], "in"] + _py_expr(t[4:-1]) + [":"]
        elif t[0] == "DEFINE":
            params = [t[k] for k in range(4, len(t)) if t[k - 1] in ("WITH", ",")]
            ps = []
            for n, p in enumerate(params):
                ps += ([","] if n else []) + [p]
            body = ["def", t[2], "("] + ps + [")", ":"]
        else:
            raise ValueError(f"no Python for {ln!r}")
        out.append(indent + " ".join(body))
    return "\n".join(out) + "\n"


PY_BUILTINS = {"print": print, "len": len, "sum": sum, "range": range, "True": True,
               "False": False}


def _plain_env(d):
    out = {}
    for k, v in d.items():
        if k.startswith("_") or k in PY_BUILTINS:
            continue
        p = sandbox._plain(v)
        if p is not None or v is None:
            out[k] = p
    return out


def py_trace(source, seconds=5, max_steps=20000, film=True):
    """Run a Python-subset program and film it, as sandbox.trace films Engc."""
    try:
        code = compile(source, "<py>", "exec")
    except SyntaxError:
        return {"ok": False, "printed": [], "error": "does not compile", "steps": [],
                "final": None}
    out = io.StringIO()
    env = {"__builtins__": dict(PY_BUILTINS)}
    steps, final = [], {}

    class _TooLong(Exception):
        pass

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<py>":
            return None
        if event == "return" and frame.f_code.co_name == "<module>":
            final.update(_plain_env(frame.f_locals))
        if event == "line":
            if len(steps) >= max_steps:
                raise _TooLong()
            depth, f = 0, frame.f_back
            while f is not None:
                depth += f.f_code.co_filename == "<py>"
                f = f.f_back
            steps.append({"line": frame.f_lineno, "depth": depth,
                          "memory": _plain_env(frame.f_locals),
                          "printed": out.getvalue().count("\n")})
        return tracer

    old = None
    try:
        old = signal.signal(signal.SIGALRM, sandbox._alarm)
        signal.setitimer(signal.ITIMER_REAL, seconds)
    except (ValueError, AttributeError):
        old = None
    before = sys.gettrace()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            if film:
                sys.settrace(tracer)
            try:
                exec(code, env)  # noqa: S102 - the sandbox world, with only four builtins
            finally:
                sys.settrace(before)
        ok, error = True, None
    except (sandbox._Timeout, _TooLong):
        ok, error = False, "ran too long"
    except Exception:  # noqa: BLE001
        ok, error = False, "failed"
    finally:
        if old is not None:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)
    printed = out.getvalue().splitlines()
    return {"ok": ok, "printed": printed if ok else [], "error": error, "steps": steps,
            "final": final if ok else None}


def py_run(source, seconds=5):
    r = py_trace(source, seconds, film=False)
    return {"ok": r["ok"], "printed": r["printed"], "error": r["error"]}


class Python:
    def from_engc(self, text):
        return to_python(text)

    def run(self, text):
        return py_run(text)

    def trace(self, text):
        return py_trace(text)
