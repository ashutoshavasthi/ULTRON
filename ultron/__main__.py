"""Trainer console.

    python -m ultron train            train from scratch through every lesson, save, report
    python -m ultron exam             re-run every held-out exam on the saved brain
    python -m ultron ask "what is 12 times 11?"
    python -m ultron ask "find a given F=21 m=7"
    python -m ultron ask "find a given spring=S2 x=0.3 m=4"
    python -m ultron why "3 + 2"      a checked Peano proof from Ultron's own laws
    python -m ultron show             what Ultron knows
    python -m ultron blind FILE       score Ultron on questions someone else wrote
    python -m ultron experiment       designing experiments vs watching (slow, ~4 min)
"""

import argparse
import json
import os
import sys

from .brain import reasoner
from .brain.brain import Brain
from .brain.dsl import show
from .brain.language import read_number
from .judge.exams import EXAMS
from .judge.report import write_all
from .logic import peano
from .trainer.trainer import Trainer

BRAIN = os.path.join("brain", "ultron_brain.json")


def cmd_train(args):
    brain = Brain()
    trainer = Trainer(brain, seed=args.seed)
    for n in range(args.upto + 1):
        r = trainer.run(n)
        status = "passed" if r["passed"] else "FAILED"
        print(f"lesson {n}: {status} (attempt {r['attempt']})")
    os.makedirs(os.path.dirname(args.brain), exist_ok=True)
    brain.save(args.brain)
    write_all(brain, trainer.results)
    print(f"saved brain to {args.brain}; reports in reports/")


def cmd_exam(args):
    brain = Brain.load(args.brain)
    for n, exam in EXAMS.items():
        r = exam(brain)
        for item in r["items"]:
            s = item["scores"]
            print(f"lesson {n} | {item['name']}: ultron {s['ultron'][0]}/{s['ultron'][1]}  "
                  f"lookup {s['lookup'][0]}/{s['lookup'][1]}  "
                  f"nearest {s['nearest'][0]}/{s['nearest'][1]}")


def cmd_ask(args):
    brain = Brain.load(args.brain)
    q = " ".join(args.question)
    if q.strip().startswith("find"):
        target, knowns, objects = reasoner.parse_physics(q)
        print(reasoner.physics(brain, target, knowns, objects))
    else:
        print(reasoner.arithmetic(brain, q))


def cmd_why(args):
    brain = Brain.load(args.brain)
    tokens = " ".join(args.question).replace("?", "").split()
    if len(tokens) != 3:
        sys.exit('ask like: why "3 + 2"')
    x, _ = read_number(brain, tokens[0])
    y, _ = read_number(brain, tokens[2])
    op = brain.vocab.get(tokens[1])
    if x is None or y is None or not op or op[0] != "op":
        sys.exit("I don't understand that question")
    a, b = (x, y) if op[2] == "xy" else (y, x)
    if not peano.rules_from_law(brain.library.get(op[1])) or min(a, b) < 0:
        print(f"My law '{op[1]}' works with numbers below zero, which Peano arithmetic "
              f"(numbers from zero upward) cannot express, so I can't give a formal proof. "
              f"My reasoning instead:")
        print(reasoner.arithmetic(brain, " ".join(tokens)))
        return
    rules = peano.all_rules(brain.library)
    print("Rules I derived from my own laws:")
    for name, lhs, rhs in rules:
        print(f"  {name}: {peano.show(lhs)} -> {peano.show(rhs)}")
    lhs = (op[1], peano.numeral(a), peano.numeral(b))
    steps = peano.prove(lhs, rules)
    print(f"\nProof of {peano.show(lhs)}:")
    for i, st in enumerate(steps, 1):
        if len(steps) > 40 and 20 < i <= len(steps) - 10:
            if i == 21:
                print(f"  ... {len(steps) - 30} more steps ...")
            continue
        print(f"  {i:3}. {peano.show(st['after']):40}  by {st['rule']}")
    value = peano.value(steps[-1]["after"]) if steps else peano.value(lhs)
    ok, msg = peano.check(lhs, value, steps, rules)
    print(f"\nResult: {value}.  Checker: {msg if ok else 'REJECTED - ' + msg}")


def cmd_blind(args):
    """Score Ultron on a question file (see blind/README.md)."""
    brain = Brain.load(args.brain)
    right = total = 0
    rows = []
    with open(args.file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line:
                continue
            q, expected = (x.strip() for x in line.rsplit("|", 1))
            if q.startswith("find"):
                target, knowns, objects = reasoner.parse_physics(q)
                ans = reasoner.physics(brain, target, knowns, objects)
                got = ans.value
            else:
                ans = reasoner.arithmetic(brain, q)
                got = None if ans.value is None else ans.text
            if expected.lower() == "refuse":
                ok = got is None
            elif expected.startswith("~"):
                want = float(expected[1:])
                v = ans.value
                if isinstance(v, tuple) and v and v[0] == "between":
                    ok = v[1][0] / v[1][1] <= want <= v[2][0] / v[2][1]
                else:
                    ok = isinstance(v, (int, float)) and abs(v - want) <= 0.02 * abs(want)
            elif got is None:
                ok = False
            elif isinstance(got, float):
                ok = abs(got - float(expected)) <= 0.02 * abs(float(expected))
            else:
                ok = got == expected
            right += ok
            total += 1
            shown = ans.text if got is None else (f"{got:.6g}" if isinstance(got, float) else got)
            rows.append(f"{'PASS' if ok else 'FAIL'}  {q}  ->  {shown}   (expected {expected})")
    print("\n".join(rows))
    print(f"\nScore: {right}/{total}")


def cmd_experiment(args):
    """Does designing its own experiments help? Three conditions (a few minutes)."""
    from .judge.exams import active_vs_passive, biased_teacher, compression_benefit
    r = {"curated": active_vs_passive(curated=True),
         "uncurated": active_vs_passive(curated=False),
         "biased": biased_teacher(),
         "compression": compression_benefit()}
    os.makedirs("reports", exist_ok=True)
    with open(os.path.join("reports", "active_vs_passive.json"), "w") as f:
        json.dump(r, f, indent=1, sort_keys=True)
        f.write("\n")
    for cond in ("curated", "uncurated"):
        a = sum(v for v in r[cond]["active"].values() if v)
        p = sum(v for v in r[cond]["passive"].values() if v)
        print(f"{cond:10} experiences to find all laws: active {a}, passive {p}")
    for mode, c in r["compression"].items():
        print(f"growing    {mode:16} programs searched {c['programs_searched']}, "
              f"found after {c['found_after']} experiences, passed={c['passed']}")
    for mode in ("active", "passive"):
        b = r["biased"][mode]
        print(f"biased     {mode:8} lesson 1 passed={b['1']['passed']}  lesson 8 "
              f"passed={b['8']['passed']}  invented below zero={b['invented_below_zero']}")


def cmd_show(args):
    brain = Brain.load(args.brain)
    print("Laws about things:")
    for name, law in brain.library.laws.items():
        print(f"  {name}({', '.join(law.params)}) = {show(law.expr)}"
              f"   [{brain.names.get(name, 'unnamed')}]")
    print("Laws about measurements:")
    for name, law in brain.qlaws.items():
        c = f"{law.constant:.6g}" if law.kind == "global" else f"a property of each {law.group_by}"
        print(f"  {name}: {law.formula()} = {c}   [{brain.names.get(name, 'unnamed')}]")
    for name, laws in brain.claws.items():
        for law in laws:
            print(f"  {name}: total {law.formula()} conserved "
                  f"({'always' if law.scope == 'all' else 'only ' + '/'.join(law.scope)})")
    print("Words:", " ".join(sorted(brain.vocab)))


def main(argv=None):
    p = argparse.ArgumentParser(prog="ultron")
    p.add_argument("--brain", default=BRAIN)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("train")
    t.add_argument("--upto", type=int, default=16)
    t.add_argument("--seed", type=int, default=0)
    sub.add_parser("exam")
    a = sub.add_parser("ask")
    a.add_argument("question", nargs="+")
    w = sub.add_parser("why")
    w.add_argument("question", nargs="+")
    sub.add_parser("show")
    bl = sub.add_parser("blind")
    bl.add_argument("file")
    sub.add_parser("experiment")
    args = p.parse_args(argv)
    {"train": cmd_train, "exam": cmd_exam, "ask": cmd_ask, "why": cmd_why,
     "show": cmd_show, "blind": cmd_blind, "experiment": cmd_experiment}[args.cmd](args)


if __name__ == "__main__":
    main()
