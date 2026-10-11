"""Stage 3 lessons: language (docs/STAGE_3_PLAN.md).

The Trainer speaks a little English about a tabletop Ultron sees through its camera.
The Trainer's way of speaking (which words, in which order, how much it says) lives
here, in the Trainer; Ultron never reads it. Ultron gets the sentence and the pictures.
"""

import math

from ..senses import floor as fl
from ..senses.tabletop import COLOURS, SHAPES, SIZES, Tabletop
from .lessons import Lesson

ATTRIBUTES = ("size", "colour")         # spoken in this order, before the noun
REDUNDANT = 0.2                         # how often the Trainer says more than it needs to

# Word pairs the Trainer never says together while teaching (fixed 2026-10-11, before any
# measurement). The exam's sentences each hold at least one of them.
HELD_OUT = (("red", "ball"), ("green", "box"), ("blue", "bar"), ("yellow", "ball"),
            ("small", "bar"), ("big", "box"), ("big", "yellow"))


def holds_out(words):
    return any(a in words and b in words for a, b in HELD_OUT)


def matches(thing, attrs):
    return all(thing[a] == v for a, v in attrs.items())


def describe(target, things, rng, must=()):
    """What the Trainer says to pick out `target`: the noun, and the fewest adjectives
    that leave no other thing fitting (sometimes one more than needed, as people do).
    `must`: attributes it has to mention. None if nothing it can say picks it out."""
    needed = {a for a in must if a in ATTRIBUTES}      # the noun is always said
    options = []
    for k in range(len(ATTRIBUTES) + 1):
        for chosen in _subsets(ATTRIBUTES, k):
            if not needed <= set(chosen):
                continue
            attrs = {a: target[a] for a in chosen}
            attrs["shape"] = target["shape"]
            if sum(1 for t in things if matches(t, attrs)) == 1:
                options.append(chosen)
        if options:
            break
    if not options:
        return None
    chosen = list(options[int(rng.integers(0, len(options)))])
    rest = [a for a in ATTRIBUTES if a not in chosen]
    if rest and rng.random() < REDUNDANT:
        chosen.append(rest[int(rng.integers(0, len(rest)))])
    words = ["the"] + [target[a] for a in ATTRIBUTES if a in chosen] + [target["shape"]]
    return " ".join(words)


def _subsets(items, k):
    if k == 0:
        yield ()
        return
    for i, x in enumerate(items):
        for rest in _subsets(items[i + 1:], k - 1):
            yield (x,) + rest


class WordsByPointing(Lesson):
    number, title = 31, "Words by pointing"
    goal = ("Things of several colours, sizes and shapes on a table, seen through the "
            "camera. First Ultron only looks: does it find, from what it measures itself, "
            "that things come in kinds (colours, sizes, shapes), and that where they lie "
            "doesn't group? Then the Trainer talks about one thing at a time ('the big red "
            "ball') and never says which word means what. Can Ultron work out each word's "
            "meaning, and pick out the thing meant when it hears words in combinations it "
            "never heard, while saying so when a word is new to it?")
    kind = "guided"
    MEASURES = ("hue", "size", "elongation", "fill", "x", "y")
    LOOKS = 60          # tables it only looks at
    TALKS = 120         # tables the Trainer talks about

    def __init__(self, seed=0):
        super().__init__(seed)
        self.table = Tabletop(seed)
        self.rng = self.table.rng

    def random_things(self, n):
        rng = self.rng
        colours, sizes = sorted(COLOURS), sorted(SIZES)
        return [self.table.thing(colours[int(rng.integers(0, len(colours)))],
                                 sizes[int(rng.integers(0, len(sizes)))],
                                 SHAPES[int(rng.integers(0, len(SHAPES)))])
                for _ in range(n)]

    def tables(self, n=None):
        """Tables to look at, with nothing said."""
        for _ in range(n or self.LOOKS):
            things = self.table.place(self.random_things(int(self.rng.integers(2, 5))))
            yield self.table.look(things)

    def talks(self, n=None, held_out=False):
        """(sentence, a way of looking, the things, which one was meant). Teaching never
        says a held-out pair; held_out=True gives only sentences that say one."""
        rng = self.rng
        made = 0
        while made < (n or self.TALKS):
            if held_out:
                pair = HELD_OUT[int(rng.integers(0, len(HELD_OUT)))]
                target, others = self._scene_needing(pair)
                things = [target] + others
                order = rng.permutation(len(things))
                things = [things[i] for i in order]
                said = describe(target, things, rng, must=self._attrs_of(pair))
                if said is None or not holds_out(said.split()):
                    continue
            else:
                things = self.random_things(int(rng.integers(2, 5)))
                target = things[int(rng.integers(0, len(things)))]
                said = describe(target, things, rng)
                if said is None or holds_out(said.split()):
                    continue
            self.table.place(things)
            made += 1
            yield said, self.table.look(things), things, things.index(target)

    @staticmethod
    def _attrs_of(pair):
        out = []
        for w in pair:
            if w in COLOURS:
                out.append("colour")
            elif w in SIZES:
                out.append("size")
            else:
                out.append("shape")
        return tuple(out)

    def _scene_needing(self, pair):
        """A target with both words of the pair, and other things that make the Trainer
        say both: one that differs only in the first, one only in the second."""
        rng = self.rng
        attrs = dict(zip(self._attrs_of(pair), pair))
        base = self.random_things(1)[0]
        target = self.table.thing(attrs.get("colour", base["colour"]),
                                  attrs.get("size", base["size"]),
                                  attrs.get("shape", base["shape"]))
        others = []
        for a in attrs:
            choices = sorted({"colour": COLOURS, "size": SIZES, "shape": SHAPES}[a])
            other = [v for v in choices if v != target[a]]
            kw = {k: target[k] for k in ("colour", "size", "shape")}
            kw[a] = other[int(rng.integers(0, len(other)))]
            others.append(self.table.thing(kw["colour"], kw["size"], kw["shape"]))
        others += self.random_things(int(rng.integers(0, 2)))
        return target, others

    def strange_word(self):
        """A sentence with a word the Trainer never taught, about a table."""
        rng = self.rng
        things = self.random_things(int(rng.integers(2, 5)))
        target = things[int(rng.integers(0, len(things)))]
        new = ("purple", "orange", "cup", "tiny", "shiny", "ring")
        word = new[int(rng.integers(0, len(new)))]
        said = f"the {word} {target['shape']}" if word not in SHAPES else f"the {word}"
        if word in ("cup", "ring"):
            said = f"the {target['colour']} {word}"
        self.table.place(things)
        return said, self.table.look(things)


# ---------------------------------------------------------------- lesson 32
VERBS = fl.EVENTS                                   # falls, bounces, rolls, stops
RELATIONS = ("faster", "heavier", "before", "after", "more", "fewer")
# Word pairs the Trainer never says together while teaching lesson 32 (numbered 30 then; fixed 2026-10-11,
# before any measurement). Things of these kinds never do these things while it
# teaches; the exam's films are all about them.
EVENT_HELD_OUT = (("box", "bounces"), ("bar", "rolls"), ("ball", "stops"),
                  ("green", "falls"), ("yellow", "bounces"), ("big", "rolls"))
RELATION_HELD_OUT = (("bar", "faster"), ("box", "heavier"), ("yellow", "before"),
                     ("red", "after"), ("green", "more"), ("blue", "fewer"))
GAP = 5.0           # things never come closer than this (pixels), except when they collide:
                    # a pixel more than the closest two things ever stand on the table
# The Trainer only says what anyone watching would notice: before or after when the
# starts are at least 3 pictures apart, faster when one goes at least 1.3 times as fast,
# heavier when one is at least 1.6 times as heavy.
APART, FASTER_BY, HEAVIER_BY = 3, 1.3, 1.6


def held_out_in(words, pairs):
    return any(a in words and b in words for a, b in pairs)


def _boxes_apart(a, b, n, gap):
    return (abs(a["xs"][n] - b["xs"][n]) >= fl.half_width(a) + fl.half_width(b) + gap or
            abs(a["ys"][n] - b["ys"][n]) >= fl.half_height(a) + fl.half_height(b) + gap)


def _inside(t):
    w, h = fl.half_width(t), fl.half_height(t)
    return all(w + 1 <= x <= fl.SIZE - 1 - w for x in t["xs"]) and \
        all(h + 1 <= y <= fl.FLOOR - h + 1e-6 for y in t["ys"])


def true_motion(t):
    """What the thing really did (for the Trainer and the Judge): when it started and
    stopped moving, and how fast it went meanwhile (pixels per picture)."""
    steps = [math.hypot(t["xs"][n + 1] - t["xs"][n], t["ys"][n + 1] - t["ys"][n])
             for n in range(len(t["xs"]) - 1)]
    moving = [n for n, s in enumerate(steps) if s > 0.05]
    if not moving:
        return {"start": None, "end": None, "speed": 0.0}
    a, b = moving[0], moving[-1] + 1
    return {"start": a + 1, "end": b, "speed": sum(steps[a:b]) / (b - a)}


def truth(word, a, b):
    """Is 'a <word> b' true of the film? a and b are lists of things (one thing, or all
    the things of a colour). The Trainer's own meaning of its words."""
    if word in ("more", "fewer"):
        return len(a) > len(b) if word == "more" else len(a) < len(b)
    if len(a) != 1 or len(b) != 1:
        return False
    ma, mb = true_motion(a[0]), true_motion(b[0])
    if word == "faster":
        return ma["speed"] > mb["speed"]
    if word == "heavier":
        return a[0]["mass"] > b[0]["mass"]
    if ma["start"] is None or mb["start"] is None:
        return False
    return ma["start"] < mb["start"] if word == "before" else ma["start"] > mb["start"]


class WordsForWhatHappens(Lesson):
    number, title = 32, "Words for what happens"
    goal = ("Films of the same coloured things, seen from the side: they fall, bounce, roll, "
            "slide to a stop and knock into each other. Ultron follows each thing and "
            "describes how it moved with its own kinds of law. The Trainer says what "
            "happened ('the red ball bounces', 'the blue box rolls faster than the green "
            "ball', 'the red ball is heavier than the yellow bar', 'there are more red than "
            "blue') and never says which word means what. Can Ultron bind the words for "
            "events to kinds of law, and the words for comparing to quantities it can "
            "measure (the heavier one by its momentum law), then name what happens in new "
            "films, about things it never saw doing that?")
    kind = "guided"
    EVENT_TALKS = 100
    RELATION_TALKS = 120

    def __init__(self, seed=0, noise=None):
        super().__init__(seed)
        self.floor = fl.Floor(seed) if noise is None else fl.Floor(seed, noise)
        self.rng = self.floor.rng

    # -------------------------------------------------------- making films
    def _pick(self, options):
        return options[int(self.rng.integers(0, len(options)))]

    def random_thing(self, colour=None, size=None, shape=None):
        return self.floor.thing(colour or self._pick(sorted(COLOURS)),
                                size or self._pick(sorted(SIZES)),
                                shape or self._pick(SHAPES))

    def _move(self, t, event, start=None):
        """Set the thing's path for this event (random place, speed, start)."""
        rng = self.rng
        t0 = int(rng.integers(0, 9)) if start is None else start
        t["event"] = event
        rest = fl.resting(t)
        w = fl.half_width(t)
        if event in ("falls", "bounces"):
            h = fl.half_height(t)
            drop = float(rng.uniform(22.0, min(48.0, rest - h - 2.0)))
            e = 0.0 if event == "falls" else float(rng.uniform(0.55, 0.8))
            t["ys"] = fl.fall(t0, rest - drop, rest, e)
            t["xs"] = [float(rng.uniform(w + 2, fl.SIZE - w - 2))] * fl.FRAMES
        elif event in ("rolls", "stops"):
            t["ys"] = [rest] * fl.FRAMES
            x0 = float(rng.uniform(w + 2, fl.SIZE - w - 2))
            if event == "rolls":
                v = float(rng.uniform(0.9, 2.0)) * (1 if rng.random() < 0.5 else -1)
                t["xs"] = fl.roll(t0, x0, v)
            else:
                v = float(rng.uniform(1.8, 3.2)) * (1 if rng.random() < 0.5 else -1)
                t["xs"] = fl.slide(t0, x0, v, float(rng.uniform(0.72, 0.88)))
        else:
            t["event"] = None
            h = fl.half_height(t)
            x = float(rng.uniform(w + 2, fl.SIZE - w - 2))
            y = float(rng.uniform(h + 2, rest))
            t["xs"], t["ys"] = [x] * fl.FRAMES, [y] * fl.FRAMES
        return t

    def _fits(self, things, allowed=()):
        if not all(_inside(t) for t in things):
            return False
        for i, a in enumerate(things):
            for j in range(i + 1, len(things)):
                if (i, j) in allowed:
                    continue
                if not all(_boxes_apart(a, things[j], n, GAP) for n in range(fl.FRAMES)):
                    return False
        return True

    def film_of(self, things, events, starts=None, tries=400):
        """Give each thing its event (None: it stays still), placed so that nothing ever
        touches anything else. None if no such film was found."""
        for _ in range(tries):
            for k, (t, e) in enumerate(zip(things, events)):
                self._move(t, e, None if starts is None else starts[k])
            if self._fits(things):
                return things
        return None

    def collision(self, a, b, tries=400):
        """a rolls into b (which may be rolling toward it); they knock and move on."""
        rng = self.rng
        for _ in range(tries):
            ra, rb = fl.resting(a), fl.resting(b)
            wa, wb = fl.half_width(a), fl.half_width(b)
            va = float(rng.uniform(1.0, 2.2))
            # the other waits for it, or comes to meet it at a speed anyone would notice
            vb = 0.0 if rng.random() < 0.5 else -float(rng.uniform(0.5, 1.4))
            xa = float(rng.uniform(wa + 2, 30.0))
            xb = float(rng.uniform(40.0, fl.SIZE - wb - 2))
            if rng.random() < 0.5:
                ratio = float(rng.uniform(HEAVIER_BY, 3.0))
            else:
                ratio = 1.0 / float(rng.uniform(HEAVIER_BY, 3.0))
            b["mass"] = a["mass"] / ratio
            xs_a, xs_b, met = fl.collide(xa, va, xb, vb, a["mass"], b["mass"],
                                         float(rng.uniform(0.7, 1.0)), wa + wb)
            if met is None or not 8 <= met <= 20:
                continue
            a["xs"], b["xs"] = xs_a, xs_b
            a["ys"], b["ys"] = [ra] * fl.FRAMES, [rb] * fl.FRAMES
            a["event"] = b["event"] = "collides"
            if _inside(a) and _inside(b):
                return a, b
        return None

    def add_still(self, things, n, protect=None):
        """Put n still things where nothing will run into them."""
        out = list(things)
        for _ in range(n):
            for _ in range(200):
                t = self._move(self.random_thing(), None)
                trial = out + [t]
                allowed = {protect} if protect else ()
                if self._fits(trial, allowed=allowed):
                    out = trial
                    break
        return out

    # -------------------------------------------------------- what the Trainer says
    def _words_of(self, t):
        return (t["colour"], t["size"], t["shape"])

    def _event_ok(self, things, held_out):
        """Teaching: no thing does a held-out thing. (The exam's target does.)"""
        for t in things:
            if t.get("event") in VERBS and not held_out:
                if any((w, t["event"]) in EVENT_HELD_OUT for w in self._words_of(t)):
                    return False
        return True

    def event_talks(self, n=None, held_out=False):
        """Films where one thing does something and the Trainer says what: (sentence,
        a way of watching, the things, which one it is about)."""
        rng = self.rng
        made = 0
        while made < (n or self.EVENT_TALKS):
            if held_out:
                word, verb = self._pick(EVENT_HELD_OUT)
                attr = {"colour": word if word in COLOURS else None,
                        "size": word if word in SIZES else None,
                        "shape": word if word in SHAPES else None}
                target = self.random_thing(**attr)
            else:
                verb = self._pick(VERBS)
                target = self.random_thing()
            others = [self.random_thing() for _ in range(int(rng.integers(0, 2)))]
            movers = [target] + others
            events = [verb] + [self._pick(VERBS) for _ in others]
            things = self.film_of(movers, events)
            if things is None or not self._event_ok(things, held_out):
                continue
            things = self.add_still(things, int(rng.integers(1, 3)))
            order = rng.permutation(len(things))
            things = [things[i] for i in order]
            said = describe(target, things, rng)
            if said is None:
                continue
            said = f"{said} {verb}"
            if held_out_in(said.split(), EVENT_HELD_OUT) and not held_out:
                continue
            made += 1
            yield said, self.floor.film(things), things, things.index(target)

    def relation_talks(self, n=None, held_out=False):
        """Films the Trainer compares two things (or two colours) in: (sentence, a way of
        watching, the things, its word, the first group, the second group)."""
        made = 0
        while made < (n or self.RELATION_TALKS):
            word = self._pick(RELATIONS)
            must = None
            if held_out:
                must = self._pick([p for p in RELATION_HELD_OUT if p[1] == word])[0]
            while True:             # every word as often as any other
                got = self._relation_film(word, must)
                if got is not None and \
                        held_out_in(got[0].split(), RELATION_HELD_OUT) == held_out:
                    break
            said, things, first, second = got
            made += 1
            yield said, self.floor.film(things), things, word, first, second

    def _relation_film(self, word, must):
        rng = self.rng
        need = {k: (must if must in v else None) for k, v in
                (("colour", COLOURS), ("size", SIZES), ("shape", SHAPES))}
        if word in ("more", "fewer"):
            colours = sorted(COLOURS)
            ca = must if must in COLOURS else self._pick(colours)
            cb = self._pick([c for c in colours if c != ca])
            na = int(rng.integers(1, 4))
            nb = self._pick([k for k in range(1, 4) if k != na])
            if (na > nb) != (word == "more"):
                na, nb = nb, na
            rest = [c for c in colours if c not in (ca, cb)]
            things = [self.random_thing(colour=ca) for _ in range(na)] + \
                     [self.random_thing(colour=cb) for _ in range(nb)] + \
                     [self.random_thing(colour=self._pick(rest))
                      for _ in range(int(rng.integers(0, 2)))]
            placed = self.film_of(things, [None] * len(things))
            if placed is None:
                return None
            first = [t for t in placed if t["colour"] == ca]
            second = [t for t in placed if t["colour"] == cb]
            return f"there are {word} {ca} than {cb}", placed, first, second
        if word == "heavier":
            a = self.random_thing(**need) if must else self.random_thing()
            b = self.random_thing()
            got = self.collision(a, b)
            if got is None:
                return None
            heavy, light = (a, b) if a["mass"] > b["mass"] else (b, a)
            things = self.add_still([a, b], int(rng.integers(0, 2)), protect=(0, 1))
            first, second = heavy, light
            verb = "is"
        elif word == "faster":
            a = self.random_thing(**need) if must else self.random_thing()
            b = self.random_thing()
            things = self.film_of([a, b], ["rolls", "rolls"])
            if things is None:
                return None
            sa, sb = true_motion(a)["speed"], true_motion(b)["speed"]
            if max(sa, sb) < FASTER_BY * min(sa, sb):
                return None
            first, second = (a, b) if sa > sb else (b, a)
            things = self.add_still(things, int(rng.integers(0, 2)))
            verb = self._pick(["rolls", "is"])
        else:
            a = self.random_thing(**need) if must else self.random_thing()
            b = self.random_thing()
            sa, sb = int(rng.integers(0, 12)), int(rng.integers(0, 12))
            if abs(sa - sb) < APART:
                return None
            things = self.film_of([a, b], [self._pick(VERBS), self._pick(VERBS)],
                                  starts=[sa, sb])
            if things is None:
                return None
            early, late = (a, b) if sa < sb else (b, a)
            first, second = (early, late) if word == "before" else (late, early)
            things = self.add_still(things, int(rng.integers(0, 2)))
            verb = first["event"]
        order = rng.permutation(len(things))
        things = [things[i] for i in order]
        da, db = describe(first, things, rng), describe(second, things, rng)
        if da is None or db is None:
            return None
        if not truth(word, [first], [second]):
            return None
        tail = "than " if word in ("faster", "heavier") else ""
        return f"{da} {verb} {word} {tail}{db}", things, [first], [second]



def language_lessons(seed=0):
    # Numbered 29 and 30 when their exams were fixed; renumbered 31 and 32 when Stage 2's
    # lessons took 29 (falling) and 30 (swinging). The seeds keep their first offsets, so teaching and exams see
    # exactly the worlds fixed in advance.
    return [WordsByPointing(seed + 29), WordsForWhatHappens(seed + 30)]
