"""The room (Level 0, WP1 and WP2): the world, the body, the teacher, a day of life."""

import ast
import hashlib
import os
import re

import numpy as np
import pytest

from ultron.brain.reflexes import Reflexes
from ultron.room import body, png, teacher as teacher_module
from ultron.room.body import Action, Senses
from ultron.room.life import EXAM_SEEDS, Life
from ultron.room.world import GROUND, Room

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _live(world, steps, seed=0):
    mind = Reflexes(seed)
    senses = world.senses()
    for _ in range(steps):
        world.act(mind.act(senses))
        world.step()
        senses = world.senses()
    return senses


def _free_solids(world):
    held = {v[0] for v in world.held.values()}
    return [t for t in world.things if t["kind"] not in ("screen",) and t["id"] not in held]


def test_same_seed_same_life():
    a, b = Room(3), Room(3)
    sa, sb = _live(a, 300), _live(b, 300)
    assert sa.picture.tobytes() == sb.picture.tobytes()
    assert a.truth() == b.truth()


def test_a_dropped_ball_comes_to_rest_on_the_mat():
    w = Room(0, teacher="off")
    ball = w.thing("ball")[0]
    ball["x"], ball["y"], ball["vy"] = 70.0, 20.0, 0.0
    for _ in range(120):
        w.step()
    assert ball["y"] + ball["hy"] == pytest.approx(GROUND[1][2], abs=0.05)
    assert abs(ball["vy"]) < 1e-6


def test_a_block_on_the_cloth_moves_when_the_cloth_is_dragged():
    w = Room(0, teacher="off")
    cloth = w.thing("cloth")[0]
    block = w.thing("block")[0]
    block["x"], block["y"] = cloth["x"], cloth["y"] - cloth["hy"] - block["hy"] - 2.0
    for _ in range(40):
        w.step()
    assert block["on"] == cloth["id"]
    start = block["x"]
    # a hand (the teacher's, scripted here) holds the cloth and drags it 10 units right
    w.teacher = None
    hand = [cloth["x"] + cloth["hx"] - 1.0, cloth["y"]]       # holding its far end
    w.held["cg_left"] = (cloth["id"], cloth["x"] - hand[0], 0.0)
    for _ in range(10):
        hand[0] += 1.0
        w._cg = {"present": True, "hands": [tuple(hand), (200.0, 60.0)], "grip": (True, False)}
        w.step()
    assert block["x"] - start == pytest.approx(10.0, abs=1.0)


def test_solid_things_never_stay_inside_each_other_or_the_ground():
    for seed in (0, 1):
        w = Room(seed)
        mind = Reflexes(seed)
        senses = w.senses()
        for step in range(600):
            w.act(mind.act(senses))
            w.step()
            senses = w.senses()
            if step % 50:
                continue
            things = _free_solids(w)
            for t in things:
                for x0, x1, top in GROUND:
                    if t["x"] + t["hx"] > x0 + 0.01 and t["x"] - t["hx"] < x1 - 0.01:
                        assert t["y"] + t["hy"] <= top + 0.1
            for i, a in enumerate(things):
                for b in things[i + 1:]:
                    ox = a["hx"] + b["hx"] - abs(a["x"] - b["x"])
                    oy = a["hy"] + b["hy"] - abs(a["y"] - b["y"])
                    assert ox <= 1.0 or oy <= 1.0


def test_the_screen_hides_what_is_behind_it():
    w = Room(0, teacher="off", noise=False)
    screen = w.thing("screen")[0]
    block = w.thing("block")[0]
    block["x"], block["y"] = screen["x"], screen["y"] + screen["hy"] - block["hy"]
    centre = (screen["x"], screen["y"])
    with_block = w.view(centre, noise=False)
    block["x"] = 150.0
    without = w.view(centre, noise=False)
    assert np.array_equal(with_block, without)
    block["x"] = screen["x"] - 30.0                 # out from behind the screen: seen
    assert not np.array_equal(w.view((block["x"], block["y"]), noise=False),
                              w.view((block["x"] + 40, block["y"]), noise=False))


def test_senses_hold_no_hidden_truth():
    s = Room(0).senses()
    assert set(Senses.__slots__) == {"picture", "joints", "gaze", "touch", "around"}
    assert s.picture.shape == (48, 64, 3) and s.around.shape == (48, 80, 3)
    assert len(s.joints) == 4 and len(s.gaze) == 2
    assert set(s.touch) == {"palms", "body"}


def test_teacher_never_looks_inside_ultron_and_its_script_is_recorded():
    path = teacher_module.__file__
    tree = ast.parse(open(path).read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] + [getattr(node, "module", "") or ""]
            assert not any("brain" in n or "judge" in n for n in names)
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    plan = open(os.path.join(ROOT, "docs", "LEVEL_0_PLAN.md")).read()
    recorded = re.search(r"teacher\.py` SHA-256: `([0-9a-f]{64})`", plan)
    assert recorded, "the teacher script's hash must be recorded in the plan"
    assert recorded.group(1) == digest, "the teacher script changed: record its new hash"


def test_teacher_off_never_comes():
    w = Room(2, teacher="off")
    _live(w, 1500)
    assert w.teacher.log == []
    assert not w.teacher.present


def test_misleading_gaze_looks_at_another_toy():
    w = Room(2, teacher="misleading_gaze")
    _live(w, 3000)
    acts = [e for e in w.teacher.log if e["toy"] is not None]
    assert acts
    assert all(e["gaze_toy"] != e["toy"] for e in acts)
    normal = Room(2)
    _live(normal, 3000)
    assert all(e["gaze_toy"] == e["toy"] for e in normal.teacher.log if e["toy"] is not None)


def test_a_life_to_learn_refuses_exam_seeds():
    with pytest.raises(ValueError):
        Life(Room(EXAM_SEEDS), Reflexes(0))
    Life(Room(EXAM_SEEDS), Reflexes(0), exam=True)


def test_a_palm_touch_closes_the_hand():
    r = Reflexes(0)
    pic = np.zeros((48, 64, 3))
    s = Senses(pic, body.START, (0, 0), {"palms": ((1, 0.0), (0, 0.0)), "body": 0})
    a = r.act(s)
    assert a.grip == (True, False)


def test_hands_can_not_go_into_the_mat():
    w = Room(0, teacher="off")
    for _ in range(300):
        w.act(Action(turn=(0.08, -0.08, 0.08, -0.08)))
        w.step()
    for hx, hy in w.hands:
        for x0, x1, top in GROUND[1:]:
            if x0 < hx < x1:
                assert hy + body.HAND_R <= top + 1e-6


def test_a_short_day():
    w = Room(0)
    life = Life(w, Reflexes(0))
    log = life.day(steps=1500)
    assert life.days == 1 and log["to"] == 1500
    assert log["stats"]["palm_contacts"] > 0
    assert log["teacher"], "the teacher came during the day"


def test_png_is_a_png():
    data = png.encode(np.zeros((4, 5, 3)))
    assert data.startswith(b"\x89PNG\r\n\x1a\n") and b"IEND" in data
