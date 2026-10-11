"""Stage 3, L3: how words combine (lesson 33; numbered 31 when its exam was fixed).

The Trainer talks about tables of the same coloured things in longer sentences: "the red
ball left of the big box", "the ball that is above the box right of the ball", "the green
box and the small ball". Its way of speaking (its grammar) lives here; Ultron never reads
it. Ultron gets the sentence and the pictures.
"""

import math

from ..senses.tabletop import COLOURS, SHAPES, SIZE, SIZES, Tabletop, reach
from .lessons import Lesson

# The Trainer's grammar. A noun phrase is "the [size] [colour] shape", maybe followed by a
# relation and another noun phrase; noun phrases are joined by "and". Every noun phrase
# picks out exactly one thing, and it says a relation only when the thing can't be told
# apart without it.
RELATION_WORDS = {"left": ("left", "of"), "right": ("right", "of"), "above": ("above",),
                  "below": ("below",)}
THAT = 0.25         # how often it says "that is left of" instead of "left of"
TIE = 2.5           # pixels: no two things are placed closer than this across or up-down,
                    # so left, right, above and below are always plain to see
MOST_THINGS = 10
# Held out of teaching (fixed 2026-10-11, before any measurement): "bar" is said only
# alone ("the bar"), and "below" only between two bare shapes ("the box below the ball").
# Teaching nests at most 2 noun phrases and joins at most 2.
TAUGHT_SHAPES = ("ball", "box")
TAUGHT_RELATIONS = ("left", "right", "above")
TEACHING = (("alone", 0.15), ("bar", 0.05), ("related", 0.40), ("below", 0.10),
            ("joined", 0.30))
EXAM = (("deeper nesting", 70), ("more joined phrases", 60), ("words in new places", 70))


def related(a, b, rel):
    """The Trainer's meaning of a relation between two true things."""
    if rel == "left":
        return a["x"] < b["x"]
    if rel == "right":
        return a["x"] > b["x"]
    if rel == "above":
        return a["y"] < b["y"]
    return a["y"] > b["y"]


def phrase_words(np_):
    """The words of a noun phrase {"look": {attr: value}, "rel": (word, phrase) or None,
    "that": bool}."""
    ws = ["the"] + [np_["look"][a] for a in ("size", "colour") if a in np_["look"]]
    ws.append(np_["look"]["shape"])
    if np_.get("rel"):
        word, inner = np_["rel"]
        ws += (["that", "is"] if np_.get("that") else []) + list(RELATION_WORDS[word])
        ws += phrase_words(inner)
    return ws


def sentence_words(phrases):
    out = []
    for k, np_ in enumerate(phrases):
        out += (["and"] if k else []) + phrase_words(np_)
    return out


def depth_of(np_):
    return 1 + (depth_of(np_["rel"][1]) if np_.get("rel") else 0)


def readings(words, things):
    """Every way the Trainer's own grammar can put the words together, as the sets of
    things they pick out ('the' keeps the one thing; sizes and colours keep things;
    shapes name them; relation words and 'and' take a phrase on each side). The Trainer
    uses it to avoid saying anything with two readings, and the Judge to grade."""
    toks = []
    for w in words:
        if w in ("of", "that", "is"):
            continue
        if w == "the":
            toks.append(("mod", ("the",)))
        elif w in COLOURS or w in SIZES:
            toks.append(("mod", ("attr", w)))
        elif w in SHAPES:
            toks.append(("set", frozenset(i for i, t in enumerate(things) if t["shape"] == w)))
        elif w in RELATION_WORDS:
            toks.append(("two", ("rel", w)))
        elif w == "and":
            toks.append(("two", ("and",)))
        else:
            raise ValueError(w)
    n = len(toks)
    chart = [[set() for _ in range(n + 1)] for _ in range(n)]
    for i, t in enumerate(toks):
        chart[i][i + 1].add(t)

    def mod(f, s):
        if f[0] == "the":
            return s if len(s) == 1 else None
        if f[0] == "attr":
            return frozenset(i for i in s if f[1] in (things[i]["colour"], things[i]["size"]))
        if f[0] == "rel":
            return frozenset(i for i in s if any(j != i and related(things[i], things[j], f[1])
                                                 for j in f[2]))
        return s | f[1]

    for span in range(2, n + 1):
        for i in range(n - span + 1):
            for k in range(i + 1, i + span):
                for a in chart[i][k]:
                    for b in chart[k][i + span]:
                        if a[0] == "mod" and b[0] == "set":
                            got = mod(a[1], b[1])
                            if got is not None:
                                chart[i][i + span].add(("set", got))
                        elif a[0] == "two" and b[0] == "set":
                            chart[i][i + span].add(("after", a[1] + (b[1],)))
                        elif a[0] == "set" and b[0] == "after":
                            f = b[1] if b[1][0] == "rel" else ("and", b[1][1])
                            got = mod(f, a[1])
                            if got is not None:
                                chart[i][i + span].add(("set", got))
    return {v for kind, v in chart[0][n] if kind == "set" and v}


def meant_by(np_, things):
    """The thing a noun phrase picks out (the Trainer's meaning), or None."""
    fit = [i for i, t in enumerate(things) if all(t[a] == v for a, v in np_["look"].items())]
    if np_.get("rel"):
        word, inner = np_["rel"]
        j = meant_by(inner, things)
        if j is None:
            return None
        fit = [i for i in fit if i != j and related(things[i], things[j], word)]
    return fit[0] if len(fit) == 1 else None


def _needed(np_, things):
    """Every relation said is needed: without it the phrase wouldn't pick out one thing."""
    if not np_.get("rel"):
        return True
    return meant_by({"look": np_["look"]}, things) is None and _needed(np_["rel"][1], things)


def held_out_use(words):
    """Does the sentence use 'bar' or 'below' in a way teaching never does?"""
    if "bar" in words and words != ["the", "bar"]:
        return True
    if "below" in words:
        bare = (len(words) == 5 and words[0] == "the" and words[1] in SHAPES
                and words[2] == "below" and words[3] == "the" and words[4] in SHAPES)
        return not bare
    return False


class HowWordsCombine(Lesson):
    number, title = 33, "How words combine"
    goal = ("Tables of the same coloured things. The Trainer now says longer things: 'the "
            "red ball left of the big box', 'the ball that is above the box right of the "
            "ball', 'the green box and the small ball'. It never says how the words go "
            "together, nor which things it means. Can Ultron find a grammar (what each word "
            "does and how it combines with its neighbours) as the shortest account of what "
            "it heard, and understand sentences nested deeper, with more phrases joined, and "
            "with words in places it never heard them?")
    kind = "guided"
    TALKS = 300

    def __init__(self, seed=0):
        super().__init__(seed)
        self.table = Tabletop(seed)
        self.rng = self.table.rng

    def _pick(self, options):
        return options[int(self.rng.integers(0, len(options)))]

    # -------------------------------------------------------- tables
    def _thing_like(self, look):
        return self.table.thing(look.get("colour") or self._pick(sorted(COLOURS)),
                                look.get("size") or self._pick(sorted(SIZES)),
                                look["shape"])

    def _look(self, shapes):
        look = {"shape": self._pick(shapes)}
        for a, values in (("size", SIZES), ("colour", COLOURS)):
            if self.rng.random() < 0.5:
                look[a] = self._pick(sorted(values))
        return look

    def _phrase(self, depth, shapes, rels):
        """A noun phrase with `depth` noun phrases nested in one another."""
        np_ = {"look": self._look(shapes), "rel": None}
        if depth > 1:
            np_["rel"] = (self._pick(rels), self._phrase(depth - 1, shapes, rels))
            np_["that"] = bool(self.rng.random() < THAT)
        return np_

    def _things_for(self, np_):
        """The things a phrase is about: the one it means, a lookalike when it says a
        relation (so the relation is needed), and those of the phrase inside it."""
        out = [self._thing_like(np_["look"])]
        if np_.get("rel"):
            out.append(self._thing_like(np_["look"]))
            out += self._things_for(np_["rel"][1])
        return out

    def _place(self, things, tries=80):
        """Put things down one at a time, never touching, never nearly level with another
        across or up-down. False if they don't fit."""
        rng = self.rng
        for k, t in enumerate(things):
            m = 4 + reach(t)
            for _ in range(tries):
                x, y = (float(v) for v in rng.uniform(m, SIZE - m, size=2))
                if all(math.hypot(x - o["x"], y - o["y"]) >= reach(t) + reach(o) + 3.0
                       and abs(x - o["x"]) >= TIE and abs(y - o["y"]) >= TIE
                       for o in things[:k]):
                    t["x"], t["y"] = x, y
                    break
            else:
                return False
        return True

    def scene(self, phrases, tries=60):
        """A table on which each phrase picks out one thing, every relation said is
        needed, and the sentence has one reading only: (things, [thing each phrase
        means]), or None."""
        rng = self.rng
        for _ in range(tries):
            things = []
            for np_ in phrases:
                things += self._things_for(np_)
            things += self.random_things(int(rng.integers(0, 3)))
            if len(things) > MOST_THINGS:
                things = things[:MOST_THINGS]
            things = [things[i] for i in rng.permutation(len(things))]
            if not self._place(things):
                continue
            meant = [meant_by(np_, things) for np_ in phrases]
            if any(m is None for m in meant) or len(set(meant)) != len(meant):
                continue
            if not all(_needed(np_, things) for np_ in phrases):
                continue
            if readings(sentence_words(phrases), things) != {frozenset(meant)}:
                continue
            return things, meant
        return None

    def random_things(self, n):
        return [self.table.thing(self._pick(sorted(COLOURS)), self._pick(sorted(SIZES)),
                                 self._pick(SHAPES)) for _ in range(n)]

    # -------------------------------------------------------- what the Trainer says
    def phrases(self, kind):
        rng = self.rng
        if kind == "alone":
            return [self._phrase(1, TAUGHT_SHAPES, TAUGHT_RELATIONS)]
        if kind == "bar":
            return [{"look": {"shape": "bar"}, "rel": None}]
        if kind == "related":
            return [self._phrase(2, TAUGHT_SHAPES, TAUGHT_RELATIONS)]
        if kind == "below":
            return [{"look": {"shape": self._pick(TAUGHT_SHAPES)}, "rel": (
                "below", {"look": {"shape": self._pick(TAUGHT_SHAPES)}, "rel": None})}]
        if kind == "joined":
            return [self._phrase(int(rng.integers(1, 3)), TAUGHT_SHAPES, TAUGHT_RELATIONS)
                    for _ in range(2)]
        rels = tuple(RELATION_WORDS)
        if kind == "deeper nesting":
            return [self._phrase(int(rng.integers(3, 5)), SHAPES, rels)]
        if kind == "more joined phrases":
            return [self._phrase(int(rng.integers(1, 3)), SHAPES, rels)
                    for _ in range(int(rng.integers(3, 5)))]
        if kind == "words in new places":
            while True:
                ps = [self._phrase(int(rng.integers(1, 3)), SHAPES, rels)
                      for _ in range(int(rng.integers(1, 3)))]
                if held_out_use(sentence_words(ps)):
                    return ps
        raise ValueError(kind)

    def _taught(self, words):
        """Teaching never uses a held-out way of speaking."""
        return not held_out_use(words)

    def talks(self, n=None, kinds=None):
        """(sentence, a way of looking, the things, [the thing each phrase means], kind).
        kinds: [(kind, share)] for teaching, or the exam's kinds with counts."""
        rng = self.rng
        if kinds is None:
            names = [k for k, _ in TEACHING]
            shares = [p for _, p in TEACHING]
            plan = [names[int(rng.choice(len(names), p=shares))] for _ in range(n or self.TALKS)]
        else:
            plan = [k for k, count in kinds for _ in range(count)]
        for kind in plan:
            while True:
                ps = self.phrases(kind)
                words = sentence_words(ps)
                if kinds is None and not self._taught(words):
                    continue
                got = self.scene(ps)
                if got is None:
                    continue
                things, meant = got
                yield " ".join(words), self.table.look(things), things, meant, kind
                break
