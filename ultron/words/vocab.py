"""The words of the language: hand-written ones (run by code) and free ones (learned).

A word is an operation name plus one argument (None, a colour, a direction, ...). The
interpreter sees a word as the sum of two learned vectors, one for the operation and one
for the argument. Arguments are shared between words, so a learned word can take a colour
the same way a hand-written one does.
"""

from typing import NamedTuple

from ..arc import ops

COLOURS = tuple(range(10))
DIRECTIONS = ("down", "up", "left", "right")

# every argument a word can take, as (kind, value); the kind keeps the colour 1 apart
# from the number 1
ARGS = ([("none", None)] + [("colour", c) for c in COLOURS] + [("side", d) for d in DIRECTIONS]
        + [("axis", a) for a in ("h", "v", "both", "rot")]
        + [("lines", a) for a in ("rows", "cols", "diagonals", "all")]
        + [("number", n) for n in (1, 2)])
ARG_KIND = {"remove_colour": "colour", "keep_colour": "colour", "recolour_all": "colour",
            "fill_enclosed": "colour", "outline": "colour", "frame_things": "colour",
            "gravity": "side", "slide_things": "side", "symmetrize": "axis",
            "connect": "lines", "remove_specks": "number"}


class Word(NamedTuple):
    op: str
    param: object = None

    def __str__(self):
        return self.op if self.param is None else f"{self.op}({self.param})"


def family(name, params=(None,)):
    return [Word(name, p) for p in params]


# G0 (docs/MECHANISM.md): the words the interpreter is taught, and five families it is
# never shown, to be rediscovered as free words from puzzles alone.
KNOWN_G0 = (family("rot180") + family("transpose") + family("antitranspose")
            + family("remove_colour", COLOURS) + family("keep_colour", COLOURS)
            + family("slide_things", DIRECTIONS) + family("frame_things", COLOURS[1:])
            + family("remove_specks", (1, 2)) + family("crop_content")
            + family("hollow_things") + family("connect", ("rows", "cols", "diagonals", "all"))
            + family("symmetrize", ("h", "v", "both", "rot")))
HIDDEN_G0 = {"flip_h": family("flip_h"),
             "recolour_all": family("recolour_all", COLOURS[1:]),
             "gravity": family("gravity", DIRECTIONS),
             "fill_enclosed": family("fill_enclosed", COLOURS[1:]),
             "outline": family("outline", COLOURS[1:])}

_FN = {name: getattr(ops, name) for name in ops.FROZEN}


def run(word, g):
    """A hand-written word carried out by its code (None when it doesn't apply)."""
    try:
        return _FN[word.op](g, word.param)
    except (ValueError, IndexError):
        return None


def changes(word, g):
    """The word's result on g when it applies and changes the picture, else None."""
    out = run(word, g)
    if out is None or (out.shape == g.shape and (out == g).all()):
        return None
    return out


class Vocab:
    """Numbers for operations and arguments. Free operations are named new0, new1, ..."""

    def __init__(self, known, n_free=0):
        self.known = list(known)
        self.ops = sorted({w.op for w in known}) + [f"new{i}" for i in range(n_free)]
        self.op_id = {n: i for i, n in enumerate(self.ops)}
        self.arg_id = {a: i for i, a in enumerate(ARGS)}
        self.n_free = n_free

    def free(self, i, colour=None):
        return Word(f"new{i}", colour)

    def is_free(self, word):
        return word.op.startswith("new")

    def ids(self, word):
        kind = "none" if word.param is None else ARG_KIND.get(word.op, "colour")
        return self.op_id[word.op], self.arg_id[(kind, word.param)]
