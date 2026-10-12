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


class ReadingStatements(Lesson):
    number, title = 101, "Reading Engc: what statements do"
    goal = ("The Trainer runs Engc programs with statements (names, tests, loops, rows, "
            "routines that call themselves) and Ultron watches each one run line by line. "
            "Can it find what every kind of line does to memory, from at most 1,000 runs, "
            "then say what longer, more deeply nested programs print, without running them?")
    kind = "guided"
    RUNS = 1000
    ROUNDS = 2           # rounds of the Trainer's short first programs
    MIXED = 60           # then programs mixing everything
    OWN = 40             # runs Ultron may spend on its own experiments at a time
    CONFIRM = 10         # fresh programs predicted right in a row before it is trusted

    def __init__(self, seed=0):
        super().__init__(seed)
        self.rng = random.Random(seed)

    def teach(self, trainer):
        from ..code import sandbox
        from ..code.reading import Reader
        from ..code.statements import Machine
        from . import engc_statements as S
        brain = trainer.brain
        rng = self.rng
        reader = Reader(brain, brain.code)
        m = Machine(brain, reader, (brain.code or {}).get("statements"))
        m.world = sandbox.trace

        def show(text):
            m.watch(text, sandbox.trace(text))

        trainer.say("Now programs with many lines. I'll run each one and you can watch it "
                    "line by line: which line runs next, and what every name holds.")
        for _ in range(self.ROUNDS):
            for text, _ in S.first_programs(rng):
                show(text)
        for _ in range(self.MIXED):
            show(S.program(rng, S.LESSON)[0])
        m.learn()
        m.experiment(self.OWN)
        m.learn()
        trainer.say("Now tell me what each new program prints before I run it.")
        streak = 0
        while streak < self.CONFIRM and m.total_runs < self.RUNS:
            text, printed = S.program(rng, S.LESSON)
            guess = m.predict(text)
            show(text)
            if guess == printed:
                streak += 1
                continue
            streak = 0
            m.note("code", "I didn't know what that program prints" if guess is None else
                           f"I expected {guess[:4]}, it printed {printed[:4]}: I think again")
            m.learn()
            if m.wanting:
                m.experiment(min(self.OWN, self.RUNS - m.total_runs))
                m.learn()
        if streak >= self.CONFIRM:
            m.note("code", f"{self.CONFIRM} new programs in a row predicted right")
        code = dict(brain.code or {})
        code["statements"] = m.to_json()
        brain.code = code
        trainer.say(f"That's all: {m.total_runs} programs run "
                    f"({m.stats.get('trainer', 0)} by me, {m.stats.get('own', 0)} by you).")


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
    return [ReadingEngc(seed + 100), ReadingStatements(seed + 101)]
