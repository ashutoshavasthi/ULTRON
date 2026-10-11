"""How words combine (stage 3, L3): a grammar found by MDL.

Ultron hears sentences about tables ("the red ball left of the box above the bar and the
yellow box") and is never told how the words go together, which word means what, or
which things were meant. A grammar here is a lexicon of a particular kind: for every
word, what it means and how it combines with its neighbours. It is found the way the
words of L1 were found: the grammar kept is the shortest account of everything heard.

What is given (the assumptions, as in L1):
- A phrase means a set of things on the table.
- A word combines with the phrase just before or just after it, by taking it as an
  argument (forward or backward application, as in a categorial grammar). A word that
  takes one phrase changes a set into a set; a word that takes two joins them. What a
  word does when it takes its argument is one of a few things Ultron can already do:
  keep the things of one of its kinds (L1), keep the one thing that is there if there is
  exactly one (else the phrase picks out nothing), keep the things that stand in one of
  its measured orderings (L2) to some thing of another set, put two sets together, or
  keep what two sets share. A word can also mean nothing.
- The Trainer speaks to be understood: an account in which its sentences had several
  readings, or picked out nothing, is an unlikely one.

What is found: every word's meaning and the way it combines (its category), and so the
order of words, which phrase goes inside which, and how deep they nest. Nothing in the
search is about English: a category is a direction and a number of arguments.
"""

import math

from .language import ANYTHING, AMBIGUOUS, NOT_EXPLAINED, RIVAL_BITS, fits, meanings

# categories: "N" is a set of things; (slash, result, argument)
N = "N"
MOD_AFTER = ("/", N, N)                         # takes the phrase after it
MOD_BEFORE = ("\\", N, N)                       # takes the phrase before it
ONE_PLACE = (MOD_AFTER, MOD_BEFORE)
TWO_PLACE = (("/", MOD_BEFORE, N), ("/", MOD_AFTER, N),
             ("\\", MOD_BEFORE, N), ("\\", MOD_AFTER, N))
DOES = ("nothing", "kind", "the one", "order", "together", "shared")
QUANTITIES = ("place", "height", "size")        # what it measures on a table, and compares
SURE = 0.5                                      # pixels: how sure it is where a thing is


def options(categories):
    """Everything a word could be: (what it does, its content, its category)."""
    out = [("nothing", None, None)]
    for m in meanings(categories):
        if m == ANYTHING:
            continue
        for c in (N,) + ONE_PLACE:
            out.append(("kind", m, c))
    for c in ONE_PLACE:
        out.append(("the one", None, c))
    for q in QUANTITIES:
        for d in (">", "<"):
            for c in TWO_PLACE:
                out.append(("order", (q, d), c))
    for does in ("together", "shared"):
        for c in TWO_PLACE:
            out.append((does, None, c))
    return out


def option_bits(option, n_singles):
    """How many bits it takes to say what a word does (how it combines is counted for
    all the words together: grammar_bits)."""
    does, content, cat = option
    bits = math.log2(len(DOES))
    if does == "kind":
        bits += len(content) * math.log2(max(n_singles, 2))
    elif does == "order":
        bits += math.log2(2 * len(QUANTITIES))
    return bits


CATEGORIES = {"kind": (N,) + ONE_PLACE, "the one": ONE_PLACE, "order": TWO_PLACE,
              "together": TWO_PLACE, "shared": TWO_PLACE}


def category_bits(opts):
    """How the words combine, said once for each thing a word can do: the categories
    the words that do it use (each named from those it could be), then for each word
    which of those it is. Words that do the same thing and combine the same way cost
    nothing more: a word combines like the others of its kind unless it pays to say
    otherwise."""
    used = {}
    for does, _, cat in opts:
        if does != "nothing":
            used.setdefault(does, set()).add(cat)
    bits = sum(len(cats) * math.log2(len(CATEGORIES[d])) for d, cats in used.items())
    bits += sum(math.log2(len(used[does])) for does, _, _ in opts if does != "nothing")
    return bits


# ---------------------------------------------------------------- understanding
def _holds(table, i, j, order):
    """Does thing i stand in this ordering to thing j (clearly, given how sure it is)?"""
    q, d = order
    a, b = table[i]["q"][q], table[j]["q"][q]
    diff = a[0] - b[0]
    if abs(diff) <= 2 * math.hypot(a[1], b[1]):
        return False
    return diff > 0 if d == ">" else diff < 0


def _apply(f, x, table, kinds):
    """A functor's value applied to an argument (a set: (frozenset, definite) or a
    partly applied two-place word). None when the phrase picks out nothing."""
    tag = f[0]
    if tag in ("kind", "the one", "around", "with", "both"):
        s, definite = x
        if tag == "kind":
            return frozenset(i for i in s if fits(f[1], kinds[i])), False
        if tag == "the one":
            return (s, True) if len(s) == 1 else None
        if tag == "around":
            ref = f[2]
            return frozenset(i for i in s if any(j != i and _holds(table, i, j, f[1])
                                                 for j in ref)), False
        if tag == "with":
            return f[1][0] | s, f[1][1] and definite
        return f[1][0] & s, False
    s = x
    if tag == "order":
        return ("around", f[1], s[0])
    if tag == "together":
        return ("with", s)
    return ("both", s)


def _lexical(option, table, kinds):
    does, content, cat = option
    if does == "kind":
        if cat == N:
            return frozenset(i for i in range(len(table)) if fits(content, kinds[i])), False
        return ("kind", content)
    if does == "the one":
        return ("the one",)
    return (does, content)


def parse(words, lexicon, table, kinds):
    """Every reading of the sentence: {(frozenset of things, definite)} for the whole
    sentence taken as a set of things that isn't empty."""
    toks = [lexicon[w] for w in words if lexicon[w][0] != "nothing"]
    n = len(toks)
    if n == 0:
        return set()
    chart = [[set() for _ in range(n + 1)] for _ in range(n)]
    for i, o in enumerate(toks):
        v = _lexical(o, table, kinds)
        if v is not None:
            chart[i][i + 1].add((o[2], v))
    for span in range(2, n + 1):
        for i in range(n - span + 1):
            k_end = i + span
            cell = chart[i][k_end]
            for k in range(i + 1, k_end):
                for cl, vl in chart[i][k]:
                    for cr, vr in chart[k][k_end]:
                        # forward: X/Y Y -> X ; backward: Y X\Y -> X
                        if cl != N and cl[0] == "/" and cl[2] == cr:
                            got = _apply(vl, vr, table, kinds)
                            if got is not None:
                                cell.add((cl[1], got))
                        if cr != N and cr[0] == "\\" and cr[2] == cl:
                            got = _apply(vr, vl, table, kinds)
                            if got is not None:
                                cell.add((cr[1], got))
    return {v for c, v in chart[0][n] if c == N and v[0]}


def sentence_bits(readings, n_things):
    """Bits still needed to know what the Trainer meant, given the readings."""
    if not readings:
        return NOT_EXPLAINED + math.log2(max(n_things, 1))
    sets = {}
    for s, definite in readings:
        sets[s] = sets.get(s, False) or definite
    k = len(sets)
    each = min(0.0 if d else math.log2(len(s)) + AMBIGUOUS * (len(s) > 1)
               for s, d in sets.items())
    return math.log2(k) + AMBIGUOUS * (k > 1) + each


# ---------------------------------------------------------------- learning
class _Account:
    """The description length of everything heard under a grammar (one option per word),
    worked out sentence by sentence and remembered."""

    def __init__(self, heard, categories):
        self.heard = heard                    # [(words, table, kinds)]
        self.options = options(categories)
        n_singles = sum(1 for m in meanings(categories) if len(m) == 1)
        self.bits_of = [option_bits(o, n_singles) for o in self.options]
        self.words = sorted({w for ws, _, _ in heard for w in ws})
        self.index = {w: i for i, w in enumerate(self.words)}
        self.uses = [[] for _ in self.words]
        for s, (ws, _, _) in enumerate(heard):
            for w in sorted(set(ws)):
                self.uses[self.index[w]].append(s)
        self.memo = {}

    def sentence(self, s, choice):
        ws, table, kinds = self.heard[s]
        key = (s,) + tuple(choice[self.index[w]] for w in ws)
        got = self.memo.get(key)
        if got is None:
            lexicon = {w: self.options[choice[self.index[w]]] for w in ws}
            got = sentence_bits(parse(ws, lexicon, table, kinds), len(table))
            self.memo[key] = got
        return got

    def grammar_bits(self, choice):
        return (sum(self.bits_of[c] for c in choice)
                + category_bits([self.options[c] for c in choice]))

    def bits(self, choice):
        return (sum(self.sentence(s, choice) for s in range(len(self.heard)))
                + self.grammar_bits(choice))

    def descend(self, choice, frozen=(), sweeps=30):
        """Change one word at a time while the account gets shorter."""
        choice = list(choice)
        for _ in range(sweeps):
            changed = False
            for i in range(len(self.words)):
                if i in frozen:
                    continue
                best = None
                for o in self.shortlist(i, choice):
                    trial = choice[:i] + [o] + choice[i + 1:]
                    cost = (sum(self.sentence(s, trial) for s in self.uses[i])
                            + self.grammar_bits(trial))
                    key = (round(cost, 9), self.bits_of[o], o)
                    if best is None or key < best:
                        best = key
                if best[2] != choice[i]:
                    choice[i], changed = best[2], True
            if not changed:
                break
        return choice

    SCREEN = 24     # sentences a word is first tried on
    KEEP = 8        # meanings tried on all its sentences

    def shortlist(self, i, choice):
        """The meanings worth trying for word i on everything heard: those that do best
        on the first few sentences that use it (and the one it has). Only a way to search
        faster; what is kept is still the shortest account found."""
        allowed = list(self.allowed(i))
        some = self.uses[i][:self.SCREEN]
        if len(allowed) <= self.KEEP or len(some) == len(self.uses[i]):
            return allowed
        scored = []
        for o in allowed:
            trial = choice[:i] + [o] + choice[i + 1:]
            scored.append((round(sum(self.sentence(s, trial) for s in some)
                                 + self.bits_of[o], 9), o))
        keep = [o for _, o in sorted(scored)[:self.KEEP]]
        return keep + ([choice[i]] if choice[i] not in keep else [])

    def allowed(self, i):
        return self.fixed_options.get(i, range(len(self.options)))

    def lexicon(self, choice):
        return {w: self.options[c] for w, c in zip(self.words, choice)}


def learn_grammar(heard, categories, known=None, rivals=False, tries=2):
    """heard: [(words, table, kinds)], a table being [{"q": {quantity: [value, se]}}]
    and kinds what each thing is ({measure: group}). known: {word: meaning} for words
    whose meaning it already has (it keeps it, and finds only how the word combines; a
    word that meant nothing may come to mean something). Returns {word: option}, and with
    rivals=True also the other grammars nearly as short."""
    acc = _Account(heard, categories)
    known = {w: tuple(tuple(p) for p in m) for w, m in (known or {}).items()}
    acc.fixed_options = {}
    for w, m in known.items():
        if w in acc.index and m != ANYTHING:
            acc.fixed_options[acc.index[w]] = [o for o, opt in enumerate(acc.options)
                                               if opt[0] == "kind" and opt[1] == m]
    start = []
    for i, w in enumerate(acc.words):
        if i in acc.fixed_options:
            start.append(acc.fixed_options[i][0])            # its kind, taken alone
        else:
            start.append(0)                                   # nothing
    found = {}

    def keep(c):
        found.setdefault(tuple(c), acc.bits(c))

    keep(acc.descend(start))
    best = min(found, key=lambda c: (found[c], c))
    # words are tied together ("that" and "is" only make sense as a pair), so changing
    # one at a time can stop short: hold each word at each of its next best meanings, and
    # at meaning nothing, while the others settle; then let it go. Again from the best
    # found, until nothing shorter turns up.
    tried = set()
    while best not in tried:
        tried.add(best)
        for i in range(len(acc.words)):
            ranked = sorted((acc.bits(list(best[:i]) + [o] + list(best[i + 1:])), o)
                            for o in acc.allowed(i) if o != best[i])
            holds = [o for _, o in ranked[:tries]]
            if 0 in acc.allowed(i) and best[i] != 0 and 0 not in holds:
                holds.append(0)
            for o in holds:
                held = acc.descend(list(best[:i]) + [o] + list(best[i + 1:]),
                                   frozen=(i,))
                keep(held)
                keep(acc.descend(held))
        best = min(found, key=lambda c: (found[c], c))
    lexicon = acc.lexicon(list(best))
    if not rivals:
        return lexicon
    close = [acc.lexicon(list(c)) for c in sorted(found, key=lambda c: (found[c], c))
             if c != best and found[c] - found[best] < RIVAL_BITS]
    return lexicon, close


SURPRISE = 1e-3     # a word whose sentences go unexplained this unusually often is doubted


def doubtful_words(heard, lexicon):
    """Words the grammar fits badly: the sentences that use the word go unexplained far
    more often than sentences do in general (chance below SURPRISE). A word said with two
    meanings, or never pinned down, shows up this way; it then says it isn't sure."""
    failed = []
    for ws, table, kinds in heard:
        failed.append(not parse(ws, {w: lexicon[w] for w in ws}, table, kinds))
    p = sum(failed) / max(len(failed), 1)
    out = []
    for w in sorted(lexicon):
        uses = [f for (ws, _, _), f in zip(heard, failed) if w in ws]
        n, k = len(uses), sum(uses)
        if n and k / n > p and _tail(n, k, p) < SURPRISE:
            out.append(w)
    return out


def unsteady_words(heard, categories, known=None):
    """Words whose meaning or way of combining it would find differently from either half
    of what it heard (every other sentence). A meaning it would have found from either
    half is one it can rely on; one that depends on which half it heard is not."""
    a = learn_grammar(heard[0::2], categories, known=known)
    b = learn_grammar(heard[1::2], categories, known=known)
    return sorted(w for w in a if w in b and a[w] != b[w])


def _tail(n, k, p):
    """Chance of k or more failures in n tries, each failing with chance p."""
    if p <= 0:
        return 0.0 if k else 1.0
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def understand(lexicon, rivals, words, table, kinds, doubtful=()):
    """Which things the sentence means: (sorted list, why) or (None, why)."""
    for w in words:
        if w not in lexicon:
            return None, f"I don't know the word '{w}'"
    for w in words:
        if w in doubtful:
            return None, f"I'm not sure what '{w}' does: what I heard with it fits no one meaning"

    def meaning(lex):
        rs = parse(words, lex, table, kinds)
        sets = {}
        for s, d in rs:
            sets[s] = sets.get(s, False) or d
        if len(sets) != 1:
            return None, len(sets)
        s, d = next(iter(sets.items()))
        if not d and len(s) > 1:
            return None, -len(s)
        return s, 1

    got, k = meaning(lexicon)
    for rival in rivals:
        other = dict(lexicon)
        other.update({w: rival[w] for w in words if w in rival})
        if meaning(other)[0] != got:
            return None, "I'm not sure yet how these words go together"
    if got is None:
        if k == 0:
            return None, "no way of putting these words together picks out anything here"
        if k < 0:
            return None, f"{-k} things here fit what you said; I can't tell which"
        return None, f"the words can be put together in {k} ways that mean different things"
    return sorted(got), "the one way of putting the words together that picks out something"


def describe_option(option, kinds_words=None):
    """A word's meaning and how it combines, in plain words."""
    does, content, cat = option
    if does == "nothing":
        return "means nothing by itself"
    side = {MOD_AFTER: "the phrase after it", MOD_BEFORE: "the phrase before it"}
    if does == "kind":
        what = (kinds_words or {}).get(content, str(content))
        if cat == N:
            return f"names things ({what})"
        return f"keeps the things of {side[cat]} that are {what}"
    if does == "the one":
        return f"picks out the one thing {side[cat]} names (or nothing, if it names several)"
    arg = "after" if cat[0] == "/" else "before"
    head = "before" if cat[1] == MOD_BEFORE else "after"
    if does == "order":
        q, d = content
        rel = {"place": ("further right", "further left"), "height": ("higher", "lower"),
               "size": ("bigger", "smaller")}[q][0 if d == ">" else 1]
        return (f"takes the phrase {arg} it and keeps the things of the phrase {head} it "
                f"that are {rel} than one of them")
    if does == "together":
        return f"puts the things of the phrase {arg} it together with those of the phrase {head} it"
    return f"keeps what the phrase {arg} it shares with the phrase {head} it"


# ---------------------------------------------------------------- with a brain
def tup(x):
    """An option read back from the brain's file (lists) as it is used (tuples)."""
    return tuple(tup(i) for i in x) if isinstance(x, list) else x


def to_json(option):
    def lst(x):
        return [lst(i) for i in x] if isinstance(x, tuple) else x
    return lst(option)


def see_table(brain, look):
    """What it sees on a table: each thing's measures (as in L1) and where it is."""
    from ..senses.things import look_at_table
    return look_at_table(brain.eyes, look)


def table_of(seen):
    """The quantities it compares, for each thing it sees on a table."""
    return [{"q": {"place": [t["x"], SURE], "height": [-t["y"], SURE],
                   "size": [t["size"], 2.0]}} for t in seen]


def heard_as(brain, said, seen):
    from .categories import kinds_of
    return (said.split(), table_of(seen), [kinds_of(brain.categories, t) for t in seen])


def known_kinds(brain):
    """The words it has for kinds of thing (L1): they keep their meanings."""
    return {w: m[1] for w, m in brain.vocab.items()
            if m[0] == "look" and w not in brain.event_words}


def kind_names(brain):
    return {tuple(tuple(p) for p in m): w for w, m in known_kinds(brain).items() if m}


def brain_grammar(brain):
    lexicon = {w: tup(o) for w, o in brain.grammar.items()}
    return (lexicon, [dict(lexicon, **{w: tup(o) for w, o in r.items()})
                      for r in brain.rival_grammars])


def understand_table(brain, said, seen):
    """Which of the things seen the sentence means: (indices, why) or (None, why)."""
    lexicon, rivals = brain_grammar(brain)
    words, table, kinds = heard_as(brain, said, seen)
    return understand(lexicon, rivals, words, table, kinds, brain.grammar_doubts)
