"""Stage 3 lessons: language (docs/STAGE_3_PLAN.md).

The Trainer speaks a little English about a tabletop Ultron sees through its camera.
The Trainer's way of speaking (which words, in which order, how much it says) lives
here, in the Trainer; Ultron never reads it. Ultron gets the sentence and the pictures.
"""

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
    number, title = 29, "Words by pointing"
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


def language_lessons(seed=0):
    return [WordsByPointing(seed + 29)]
