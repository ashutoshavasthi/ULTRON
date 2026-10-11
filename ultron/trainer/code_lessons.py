"""Code lessons (numbered from 100): programs are the world (docs/STAGE_CODE_PLAN.md).

Lesson 100 (C1): reading Engc expressions. The Trainer runs one-line programs and
Ultron watches what they print; then Ultron writes and runs programs of its own, to
pin down what each word means and how words group. It never sees Engc's compiler or
grammar. At most RUNS programs are run in all (the Trainer's and its own).
"""

import random

from ..code.reading import Reader
from . import engc_programs as P
from .lessons import Lesson

WORDS = ["PLUS", "MINUS", "TIMES", "MODULO", "RAISED TO", "IS GREATER THAN", "IS LESS THAN",
         "IS EQUAL TO", "IS AT LEAST", "IS AT MOST", "IS NOT"]
SYMBOLS = ["+", "-", "*", "%", "**", ">", "<", "==", ">=", "<=", "!="]
UNARY = ["MINUS", "-"]
LOGIC = [("AND", 2), ("OR", 2), ("NOT", 1)]


class ReadingEngc(Lesson):
    number, title = 100, "Reading Engc: what expressions mean"
    goal = ("The Trainer runs one-line Engc programs (PRINT <expression> .) and Ultron "
            "watches what they print. Can it find what each word and mark means, as one of "
            "its own laws, and how words group, from at most 400 runs, then say what "
            "expressions far longer than any it saw will print, without running them?")
    kind = "guided"
    RUNS = 400
    SHOWN = 3            # the Trainer's demonstrations of each word
    PER_WORD = 14        # runs Ultron may spend on one word (stepping may need more)
    TWO_OPS = 20         # the Trainer's two-operator programs
    BRACKETS = 6         # the Trainer's programs with brackets

    def __init__(self, seed=0):
        super().__init__(seed)
        self.rng = random.Random(seed)

    def teach(self, trainer):
        from ..code import sandbox
        brain = trainer.brain
        rng = self.rng
        reader = Reader(brain, {"seed": self.seed})
        reader.world = _world(sandbox)

        def show(text, printed):
            reader.watch(text, printed)

        trainer.say("These are programs in a language called Engc. I'll run some and you "
                    "watch what each one prints. Later you can write and run your own.")
        first = [P.one_op(rng, WORDS[0]) for _ in range(self.SHOWN)]
        reader.find_frame([t for t, _ in first])
        # words, then their symbol twins, then a word before a number
        for i, words in enumerate(WORDS + SYMBOLS):
            self._word(reader, rng, words, 2, trainer, first if i == 0 else None)
        for words in UNARY:
            self._word(reader, rng, words, 1, trainer)
        reader.decide_symbols()
        trainer.say("Now words that join whole statements.")
        for words, arity in LOGIC:
            self._word(reader, rng, words, arity, trainer)
        trainer.say("Now programs with two operators.")
        for _ in range(self.TWO_OPS):
            show(*P.program(rng, 2, 20))
        reader.learn_grammar(self._left(reader, 60))
        trainer.say("Now programs with brackets.")
        for _ in range(self.BRACKETS):
            show(*P.bracketed(rng))
        reader.learn_marks()
        reader.learn_grammar(self._left(reader, 0))
        brain.code = reader.to_json()
        trainer.say(f"That's all: {reader.total_runs} programs run "
                    f"({reader.stats.get('trainer', 0)} by me, {reader.stats.get('own', 0)} "
                    f"by you).")

    def _left(self, reader, keep):
        return max(0, self.RUNS - reader.total_runs - keep)

    def _word(self, reader, rng, words, arity, trainer, shown=None):
        demos = []
        for i in range(self.SHOWN):
            text, printed = shown[i] if shown else P.one_op(rng, words, unary=arity == 1)
            reader.watch(text, printed)
            got = reader.demo_from(text, printed)
            if got is not None:
                demos.append((got[2], got[3]))
        if not demos:
            reader.note("stuck", f"I couldn't tell what '{words}' joins")
            return
        budget = min(self.PER_WORD, self._left(reader, 120))
        reader.study(tuple(words.split()), arity, demos, budget)


def _world(sandbox):
    def run(text):
        out = sandbox.run(text)
        return out["printed"] if out["ok"] else None
    return run


def code_lessons(seed):
    """Code lessons need Engc in the sandbox; without it they are left out."""
    from ..code import sandbox
    if not sandbox.available():
        return []
    return [ReadingEngc(seed + 100)]
