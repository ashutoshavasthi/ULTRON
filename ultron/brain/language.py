"""Grounded language: words are attached to concepts Ultron already has.

  * a number word or mark is bound to a quantity it can count;
  * an operation word is bound to whichever of *its own* laws reproduces every
    demonstration the Trainer gave (and in which argument order);
  * a relation word is bound to an innate relation ("same", "fewer");
  * a word heard about things on a table is bound to a kind of thing it found itself
    (stage 3: words by pointing, below).

A word nobody demonstrated stays meaningless to it.
"""

import math

from .dsl import Overflow

NUMERAL_LAW = "numeral"     # the place-value law Ultron discovers in lesson 4


def bind_number(brain, token, pile_count):
    known = brain.vocab.get(token)
    if known and known != ("number", pile_count):
        brain.note("conflict", f"'{token}' was shown for {known[1]} and for {pile_count}")
    brain.bind(token, ("number", pile_count))


def bind_operation(brain, token, demos):
    """demos: [(x, y, result)] as Ultron perceived them. Returns the binding or None."""
    for law in brain.library.binary_int_laws():
        for order in ("xy", "yx"):
            ok = True
            for x, y, r in demos:
                a, b = (x, y) if order == "xy" else (y, x)
                try:
                    if brain.library.call(law.name, a, b) != r:
                        ok = False
                        break
                except Overflow:
                    ok = False
                    break
            if ok:
                brain.bind(token, ("op", law.name, order))
                # a demonstration the Trainer acted out is an experience too
                if law.name in brain.memory.episodes:
                    for x, y, r in demos:
                        a, b = (x, y) if order == "xy" else (y, x)
                        ep = {"inputs": {law.params[0]: a, law.params[1]: b}, "outcome": r}
                        if ep not in brain.memory.of(law.name):
                            brain.memory.store(law.name, ep)
                brain.note("word", f"'{token}' behaves exactly like my law '{law.name}' "
                                   f"(arguments {order}) in all {len(demos)} demonstrations")
                return brain.vocab[token]
    brain.note("word", f"'{token}': none of my laws matches the demonstrations")
    return None


def bind_relation(brain, token, demos):
    """demos: [(left, right)] pairs the Trainer said this word joins."""
    relations = {"same": lambda a, b: a == b, "fewer": lambda a, b: a < b}
    for name, rel in relations.items():
        if all(rel(a, b) for a, b in demos):
            brain.bind(token, ("relation", name))
            brain.note("word", f"'{token}' joins things that are the {name} amount")
            return brain.vocab[token]
    return None


def bind_prefix(brain, examples):
    """examples: [(what the Trainer said, position Ultron perceives)], e.g. ('-3', -3)
    or ('negative three', -3). Ultron finds the part that is the same in every example,
    checks the rest reads as the distance below zero, and learns that prefix."""
    found = set()
    for said, pos in examples:
        if pos is None or pos >= 0:
            return None
        for i in range(1, len(said)):
            prefix, rest = said[:i].strip(), said[i:].strip()
            value, _ = read_number(brain, rest)
            if value == -pos and prefix:
                found.add(prefix)
                break
        else:
            return None
    for prefix in sorted(found):
        brain.bind("prefix:" + prefix, ("prefix", "below zero"))
        brain.note("word", f"'{prefix}' in front of a number means that far below zero")
    return found


def prefixes(brain):
    return [k[len("prefix:"):] for k, m in sorted(brain.vocab.items())
            if k.startswith("prefix:") and m[0] == "prefix"]


def is_numeral(brain, token):
    return bool(token) and all(brain.vocab.get(ch, ("",))[0] == "number" and len(ch) == 1
                               for ch in token)


def read_number(brain, token):
    """Returns (value, explanation) or (None, reason)."""
    meaning = brain.vocab.get(token)
    if meaning and meaning[0] == "number":
        things = "thing" if meaning[1] == 1 else "things"
        return meaning[1], f"'{token}' is a word I was shown with {meaning[1]} {things}"
    for p in prefixes(brain):
        rest = token[len(p):].strip()
        if token.startswith(p) and rest and (not p.isalpha() or token[len(p)] == " "):
            value, _ = read_number(brain, rest)
            if value is not None and value > 0:
                return -value, f"'{token}' is {value} below zero on my purse line"
    if not is_numeral(brain, token):
        return None, f"I don't know the word '{token}'"
    law = brain.library.get(NUMERAL_LAW)
    if law is None:
        return None, "I can't read numerals with more than one mark yet"
    value = brain.vocab[token[0]][1]
    for ch in token[1:]:
        value = brain.library.call(NUMERAL_LAW, value, brain.vocab[ch][1])
    return value, (f"I read '{token}' mark by mark with my place-value law "
                   f"(value so far, next mark) -> {NUMERAL_LAW}")


def speak_number(brain, n):
    """Write a quantity as marks by inverting the place-value law."""
    if n < 0:
        marks = [p for p in prefixes(brain) if not p.isalpha()]
        rest = speak_number(brain, -n)
        return None if not marks or rest is None else marks[0] + rest
    marks = {m[1]: tok for tok, m in brain.vocab.items()
             if m[0] == "number" and len(tok) == 1}
    if n in marks:
        return marks[n]
    if brain.library.get(NUMERAL_LAW) is None:
        return None
    cols = getattr(brain.library, "_columns", None)
    if cols is not None and all(d in marks for d in range(10)):
        # with column arithmetic, a count is already held as its column marks
        return "".join(marks[d] for d in reversed(cols.digits(n)))
    for last in sorted(marks):
        lo, hi = 1, n
        while lo <= hi:     # the law grows with its first argument: search by halving
            mid = (lo + hi) // 2
            try:
                v = brain.library.call(NUMERAL_LAW, mid, last)
            except Overflow:
                return None
            if v == n:
                prefix = speak_number(brain, mid)
                return None if prefix is None else prefix + marks[last]
            if v < n:
                lo = mid + 1
            else:
                hi = mid - 1
    return None


# ------------------------------------------------------------ words by pointing (stage 3)
# The Trainer talks about one thing on a table ("the big red ball") and never says which
# word means what, or even which thing it means. A word's meaning is a description of a
# thing in Ultron's own kinds (brain/categories.py): one group of one measure, two groups
# of two measures together, or nothing at all (a word like "the" that picks out nothing).
#
# The lexicon kept is the shortest account of everything heard (MDL):
#   + the bits to state each word's meaning;
#   + for each sentence, the bits still needed to say which thing was meant (none when
#     exactly one thing fits every word); a sentence that fits nothing is an exception
#     and costs most;
#   - a coincidence it no longer has to explain: each time a word was said about a thing
#     of a kind that is rare, a lexicon where the word means that kind expects it; one
#     where the word means nothing would call it chance (-log2 of how common the kind is).
#     This is how a word that was never *needed* ("the blue ball" with one ball on the
#     table) is still learned. It counts one measure per word: a word is about one thing
#     about things, unless picking things out needs two (as "box" does: not long, and
#     filling its outline).
# Lexicons nearly as short as the best are kept as rivals: when they would pick different
# things, Ultron is not sure yet and doesn't answer.

ANYTHING = ()
NOT_EXPLAINED = 8.0     # bits for a sentence the lexicon can't explain (fits nothing)
AMBIGUOUS = 4.0         # extra bits when a sentence would fit more than one thing: the
                        # Trainer speaks to be understood, so an account in which it often
                        # wasn't (more than 1 time in 16) is an unlikely one
RIVAL_BITS = 3.0        # an account this close to the best (under 8 times less likely)
                        # is a live rival


def meanings(categories):
    """Every meaning a word could have, shortest first."""
    singles = [(m, g) for m in sorted(categories)
               for g in range(len(categories[m]["groups"])) if len(categories[m]["groups"]) > 1]
    pairs = [(a, b) for i, a in enumerate(singles) for b in singles[i + 1:] if a[0] != b[0]]
    return [ANYTHING] + [(s,) for s in singles] + pairs


def fits(meaning, kinds):
    return all(kinds.get(m) == g for m, g in meaning)


class _Account:
    """The description length of what was heard under a lexicon, quick to evaluate
    (numpy: every sentence's things at once). A lexicon is one option index per word."""

    def __init__(self, heard, categories):
        import numpy as np
        self.np = np
        self.options = meanings(categories)
        n_singles = sum(1 for o in self.options if len(o) == 1)
        self.meaning_bits = np.array([len(o) * math.log2(max(n_singles, 2))
                                      for o in self.options])
        self.words = sorted({w for ws, _ in heard for w in ws})
        index = {w: i for i, w in enumerate(self.words)}
        things = [(s, k) for s, (_, ks) in enumerate(heard) for k in ks]
        self.sent = np.array([s for s, _ in things], dtype=int)
        self.n_sent = len(heard)
        # fit[o, t]: does option o fit thing t
        self.fit = np.array([[fits(o, k) for _, k in things] for o in self.options],
                            dtype=bool)
        share = {o[0]: max(float(self.fit[i].mean()), 1e-9)
                 for i, o in enumerate(self.options) if len(o) == 1}
        self.coincidence = np.array([max((-math.log2(share[p]) for p in o), default=0.0)
                                     for o in self.options])
        # said_in[w, s]: is word w said in sentence s
        self.said_in = np.zeros((len(self.words), self.n_sent), dtype=bool)
        for s, (ws, _) in enumerate(heard):
            for w in ws:
                self.said_in[index[w], s] = True
        self.uses = self.said_in[:, self.sent]
        self.n_things = np.bincount(self.sent, minlength=self.n_sent)

    def bits(self, choice):
        np = self.np
        fitting = (self.fit[choice] | ~self.uses).all(axis=0)
        how_many = np.bincount(self.sent, weights=fitting, minlength=self.n_sent)
        explained = how_many > 0
        sentence = np.where(explained, np.log2(np.maximum(how_many, 1))
                            + AMBIGUOUS * (how_many > 1), NOT_EXPLAINED + np.log2(self.n_things))
        expected = (self.said_in & explained).sum(axis=1) * self.coincidence[choice]
        return float(sentence.sum() + self.meaning_bits[choice].sum() - expected.sum())

    def descend(self, choice, frozen=(), sweeps=20):
        """Change one word's meaning at a time while the account gets shorter."""
        choice = list(choice)
        for _ in range(sweeps):
            changed = False
            for i in range(len(self.words)):
                if i in frozen:
                    continue
                costs = []
                for o in range(len(self.options)):
                    trial = choice[:i] + [o] + choice[i + 1:]
                    costs.append((round(self.bits(trial), 9), len(self.options[o]), o))
                best = min(costs)[2]
                if best != choice[i]:
                    choice[i], changed = best, True
            if not changed:
                break
        return choice

    def lexicon(self, choice):
        return {w: self.options[c] for w, c in zip(self.words, choice)}


def learn_lexicon(heard, categories, rivals=False, tries=2, known=None):
    """heard: [(words, [kinds of each thing])]. Returns {word: meaning}. With rivals=True,
    (lexicon, [other lexicons nearly as short]).

    The search changes one word's meaning at a time while the account gets shorter. Words
    are tied together (what "the" means changes what "bar" must mean), so that can stop
    short of the best account. It is run again from each start where one word means one
    kind and the rest nothing; then, around the best found, with each word held to each of
    its next best meanings while the others settle. Every account found that is nearly as
    short as the best is a rival.

    known: {word: meaning} for words it already has; they keep their meanings."""
    if not heard:
        return ({}, []) if rivals else {}
    acc = _Account(heard, categories)
    n = len(acc.words)
    known = {w: tuple(tuple(p) for p in m) for w, m in (known or {}).items()}
    fixed = {i: acc.options.index(known[w]) for i, w in enumerate(acc.words) if w in known}
    frozen = tuple(sorted(fixed))
    found = {}

    def start(i=None, o=None):
        c = [fixed.get(k, 0) for k in range(n)]
        if i is not None:
            c[i] = o
        return c

    def keep(choice):
        found.setdefault(tuple(choice), acc.bits(choice))

    keep(acc.descend(start(), frozen=frozen))
    singles = [o for o, opt in enumerate(acc.options) if len(opt) == 1]
    for i in range(n):
        if i in fixed:
            continue
        for o in singles:
            keep(acc.descend(start(i, o), frozen=frozen))
    best = min(found, key=lambda c: (found[c], c))
    if rivals:
        for i in range(n):
            if i in fixed:
                continue
            ranked = sorted((acc.bits(list(best[:i]) + [o] + list(best[i + 1:])), o)
                            for o in range(len(acc.options)) if o != best[i])
            for _, o in ranked[:tries]:
                held = acc.descend(list(best[:i]) + [o] + list(best[i + 1:]),
                                   frozen=frozen + (i,))
                keep(held)
                keep(acc.descend(held, frozen=frozen))
        best = min(found, key=lambda c: (found[c], c))
    lexicon = acc.lexicon(list(best))
    if not rivals:
        return lexicon
    close = [acc.lexicon(list(c)) for c in sorted(found, key=lambda c: (found[c], c))
             if c != best and found[c] - found[best] < RIVAL_BITS]
    return lexicon, close


def lexicon_bits(heard, categories, lexicon):
    acc = _Account(heard, categories)
    return acc.bits([acc.options.index(lexicon[w]) for w in acc.words])


def refer(brain, said, things):
    """Which thing is meant? Returns (index, explanation); index None when Ultron can't
    tell: a word it was never taught, a word whose meaning it isn't sure of yet (a rival
    account of what it heard would pick a different thing), nothing that fits, or more
    than one thing that fits."""
    from .categories import kinds_of
    words = said.split()
    for w in words:
        m = brain.vocab.get(w)
        if m is None or m[0] != "look":
            return None, f"I don't know the word '{w}'"
    kinds = [kinds_of(brain.categories, t) for t in things]
    as_tuple = lambda m: tuple(tuple(p) for p in m)

    def pick(lexicon):
        return [i for i, k in enumerate(kinds) if all(fits(lexicon[w], k) for w in words)]

    lexicon = {w: as_tuple(brain.vocab[w][1]) for w in words}
    hits = pick(lexicon)
    for rival in brain.rival_lexicons:
        other = {w: as_tuple(rival.get(w, brain.vocab[w][1])) for w in words}
        if pick(other) != hits:
            unsure = sorted(w for w in words if other[w] != lexicon[w])
            return None, f"I'm not sure yet what '{unsure[0]}' means"
    if len(hits) == 1:
        return hits[0], "the only thing that fits every word"
    if not hits:
        return None, "nothing here fits what you said"
    return None, f"{len(hits)} things here fit what you said; I can't tell which"


def settled_after(heard, categories, every=20, known=None):
    """For each word: how many sentences using it Ultron had heard when its meaning
    became the one it keeps. The lexicon is relearned after every `every` sentences, so
    this is an upper bound. known: words it already had (left out)."""
    final = learn_lexicon(heard, categories, known=known)
    final = {w: m for w, m in final.items() if w not in (known or {})}
    points = sorted(set(range(every, len(heard), every)) | {len(heard)})
    settle = {w: None for w in final}
    for n in points:
        lex = learn_lexicon(heard[:n], categories, known=known)
        for w in final:
            if lex.get(w) == final[w]:
                if settle[w] is None:
                    settle[w] = n
            else:
                settle[w] = None
    return {w: sum(1 for ws, _ in heard[:settle[w]] if w in ws) for w in sorted(final)}


def heard_as_kinds(brain):
    """What Ultron heard, with each thing it saw as the kinds it is in."""
    from .categories import kinds_of
    return [(h["said"].split(), [kinds_of(brain.categories, t) for t in h["things"]])
            for h in brain.heard]


def describe_meaning(brain, meaning):
    """A meaning in Ultron's own terms, for its log."""
    if not meaning:
        return "nothing: it fits every thing"
    parts = []
    for m, g in meaning:
        lo, hi = brain.categories[m]["groups"][g]
        turn = brain.categories[m].get("turn", 0.0)
        if turn:
            lo, hi = (lo + turn) % 360, (hi + turn) % 360
        parts.append(f"{m} is in my group {g + 1} ({lo:.3g} to {hi:.3g})")
    return "things whose " + " and ".join(parts)


# ------------------------------------------------------------------ stage 3: what happens
# Words for events and for comparing (L2). A film is the things in it, each with what it
# looks like and what it did, in Ultron's own kinds (brain/events.py).
#
# An event word ("falls") is learned like a word for a look: its meaning is the kind of
# motion present every time the word is said about a thing, found as the shortest account
# of what was heard, with the words it already knows ("the", "red", "ball") keeping their
# meanings. It says which thing a sentence is about with those words.
#
# A comparing word joins two things, or two kinds of thing, named in the sentence: the
# words before it name one, the words after it the other (the innate part, stated
# plainly; grammar is L3). Its meaning is a quantity it measures and which way round:
# "the first has more of it" or "the first has less of it". It is the shortest account
# again: the bits to say which quantity, the sentences it leaves unexplained, minus the
# coincidences it explains (a word said only when the first thing started earlier, if it
# meant nothing, would be chance). A word it heard in every kind of comparing sentence
# ("than") means nothing.

def _known_look(brain, w):
    m = brain.vocab.get(w)
    return m is not None and m[0] == "look"


def runs(brain, words):
    """The sentence split into runs of words that describe things ([(start, words)]) and
    the other words, in order."""
    out, cur = [], []
    others = []
    for i, w in enumerate(words):
        if _known_look(brain, w):
            cur.append(w)
        else:
            if cur:
                out.append(cur)
                cur = []
            others.append(w)
    if cur:
        out.append(cur)
    return out, others


def picked(brain, film, words):
    """The things in a film that fit every word (indices)."""
    from .events import kinds_of_thing
    as_tuple = lambda m: tuple(tuple(p) for p in m)
    meaning = [as_tuple(brain.vocab[w][1]) for w in words]
    return [i for i, t in enumerate(film["things"])
            if all(fits(m, kinds_of_thing(brain, t)) for m in meaning)]


def relation_options():
    from .events import QUANTITIES
    return [None] + [(q, d) for q in QUANTITIES for d in (">", "<")]


def _holds(film, a, b, option):
    from .events import compare
    if option is None:
        return True
    if not a or not b or set(a) & set(b):
        return None             # it can't find one of the things named, or both name the
                                # same thing: it can't compare
    c = compare(film, a, b, option[0])
    if c is None:
        return None
    return c if option[1] == ">" else not c


def comparing(brain, said, film):
    """(the words that may compare, the first group, the second group) or None when the
    sentence doesn't name two groups."""
    words = said.split()
    rs, others = runs(brain, words)
    if len(rs) != 2 or not others:
        return None
    return others, picked(brain, film, rs[0]), picked(brain, film, rs[1])


def learn_relations(heard, rivals=False):
    """heard: [(words that may compare, film, first, second)]. Returns {word: option}
    (option None: it means nothing), and with rivals=True also the accounts nearly as
    short."""
    options = relation_options()
    words = sorted({w for ws, _, _, _ in heard for w in ws})
    status = {}                 # (sentence, option) -> True / False / None
    for s, (_, film, a, b) in enumerate(heard):
        for o in options:
            status[(s, o)] = _holds(film, a, b, o)
    n = len(heard)
    share = {o: max(sum(status[(s, o)] is True for s in range(n)) / n, 1e-9)
             for o in options if o is not None}
    meaning_bits = math.log2(len(options) - 1)

    def bits(choice):
        total = sum(meaning_bits for o in choice.values() if o is not None)
        for s, (ws, _, _, _) in enumerate(heard):
            ok = all(status[(s, choice[w])] is True for w in ws)
            if not ok:
                total += NOT_EXPLAINED
            else:
                total -= sum(-math.log2(share[choice[w]]) for w in ws
                             if choice[w] is not None)
        return total

    def descend(choice, frozen=()):
        choice = dict(choice)
        for _ in range(20):
            changed = False
            for w in words:
                if w in frozen:
                    continue
                costs = sorted((round(bits({**choice, w: o}), 9), o is not None, str(o), o)
                               for o in options)
                if costs[0][3] != choice[w]:
                    choice[w], changed = costs[0][3], True
            if not changed:
                break
        return choice

    found = {}

    def keep(c):
        found.setdefault(tuple(sorted((w, str(o)) for w, o in c.items())), (bits(c), c))

    keep(descend({w: None for w in words}))
    for w in words:
        for o in options[1:]:
            keep(descend({**{v: None for v in words}, w: o}))
    best_key = min(found, key=lambda k: (found[k][0], k))
    best = found[best_key][1]
    if not rivals:
        return best
    for w in words:
        for o in options:
            if o != best[w]:
                held = descend({**best, w: o}, frozen=(w,))
                keep(held)
                keep(descend(held))
    best_bits = found[best_key][0]
    close = [c for k, (b, c) in sorted(found.items(), key=lambda kv: (kv[1][0], kv[0]))
             if k != best_key and b - best_bits < RIVAL_BITS]
    return best, close


def relation_of(brain, w):
    """What a comparing word means to it: (quantity, way) or None; 'unknown' if never
    taught. A word it already had another meaning for (lesson 4's 'after') keeps that
    meaning; the comparing one is its second sense."""
    m = brain.vocab.get(w)
    if m is not None and m[0] == "order":
        return tuple(m[1]) if m[1] else None
    if w in brain.senses:
        sense = brain.senses[w]
        return tuple(sense[1]) if sense[1] else None
    return "unknown"


def relate_with(meanings, rivals, film, a, b):
    """The comparing words to say of the first group and the second: every one whose
    meaning it can check holds here, and about which no rival account disagrees.
    meanings: {word: (quantity, way) or None}."""
    out = []
    for w in sorted(meanings):
        o = meanings[w]
        if o is None or _holds(film, a, b, tuple(o)) is not True:
            continue
        if any(_holds(film, a, b, tuple(r[w]) if r[w] else None) is not True
               for r in rivals if w in r):
            continue
        out.append(w)
    return out


def relate(brain, film, a, b):
    """The comparing words it would say of the first group and the second."""
    words = sorted({w for w, m in brain.vocab.items() if m[0] == "order"} | set(brain.senses))
    meanings = {w: relation_of(brain, w) for w in words}
    meanings = {w: o for w, o in meanings.items() if o != "unknown"}
    return relate_with(meanings, brain.rival_relations, film, a, b)


def specificity(meaning, seen):
    """How rare things that fit this meaning are among all it watched (bits): saying
    the rarest word that fits tells the listener most."""
    share = sum(fits(meaning, k) for k in seen) / max(len(seen), 1)
    return -math.log2(max(share, 1e-9))


def name_with(lexicon, rivals, kinds, seen):
    """The event word for a thing of these kinds: of the words whose meaning fits, the
    one that fits fewest of the things it has watched. (None, why) when it didn't see the
    thing move (words for what happens are said of things that do something), none fits, a
    rival account would say another word, or it heard a word for what things do whose
    meaning it hasn't found (that word might be the one for this)."""
    if not any(kinds.get(m) for m in ("across", "updown", "turns back")):
        return None, "I didn't see it do anything"
    unsure = sorted(w for w, m in lexicon.items() if not m)
    if unsure:
        return None, f"I don't know yet what '{unsure[0]}' means: it might be the word for this"
    same = sorted(w for w, m in lexicon.items()
                  if any(v != w and tuple(map(tuple, n)) == tuple(map(tuple, m))
                         for v, n in lexicon.items()))
    if same:
        return None, f"'{same[0]}' and '{same[1]}' seem to mean the same: I can't tell which to say"
    rarity = {w: specificity(m, seen) for w, m in lexicon.items() if m}

    def best(lex):
        fitting = [(rarity.get(w, specificity(lex[w], seen)), w) for w in lex
                   if lex[w] and fits(lex[w], kinds)]
        return max(fitting)[1] if fitting else None

    word = best(lexicon)
    for rival in rivals:
        other = {w: tuple(tuple(p) for p in rival.get(w, lexicon[w])) for w in lexicon}
        if best(other) != word:
            return None, "I'm not sure yet which word says what it did"
    if word is None:
        return None, "I have no word for what it did"
    return word, f"it fits '{word}', and nothing rarer fits"


def name_event(brain, film, i):
    """The word for what thing i did in the film, or (None, why)."""
    from .events import kinds_of_thing
    as_tuple = lambda m: tuple(tuple(p) for p in m)
    lexicon = {w: as_tuple(brain.vocab[w][1]) for w in brain.event_words}
    seen = [kinds_of_thing(brain, t) for f in brain.films for t in f["things"]]
    return name_with(lexicon, brain.rival_lexicons, kinds_of_thing(brain, film["things"][i]),
                     seen)
