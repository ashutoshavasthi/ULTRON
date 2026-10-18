"""Ultron's body in the room: two arms, two hands, a gaze; and the two things that
cross between Ultron and the world each step, Senses and Action.

It sits on the floor at the left of the room, facing right. Each arm has a shoulder and
an elbow. Ultron feels its joint angles, never where its hands are in the room: where a
hand ends up for given angles is a law of its own body it has to learn (milestone N3).
"""

import math

import numpy as np

SHOULDERS = ((19.0, 60.0), (22.0, 61.0))    # left arm, right arm (room units, y down)
UPPER, FORE = 20.0, 18.0                    # arm lengths
HAND_R = 3.0
LIMITS = ((-1.5, 1.4), (-0.3, 2.6))         # shoulder, elbow (radians; + turns down)
START = (0.9, 2.5, 0.8, 2.4)                # left shoulder, left elbow, right ...
MAX_TURN = 0.08                             # most a joint can turn in one step
MAX_GAZE = 30.0                             # most the gaze can move in one step (units):
                                            # a saccade takes a step or two, as real ones do
TORSO = (8.0, 58.0, 24.0, 90.0)             # x0, y0, x1, y1
HEAD = (16.0, 50.0, 7.0)                    # x, y, radius


def hand_at(joints, arm):
    """Where a hand is for these joint angles (the world's knowledge, not Ultron's)."""
    sx, sy = SHOULDERS[arm]
    a, b = joints[2 * arm], joints[2 * arm + 1]
    ex, ey = sx + UPPER * math.cos(a), sy + UPPER * math.sin(a)
    return ex + FORE * math.cos(a + b), ey + FORE * math.sin(a + b), (ex, ey)


def clip_joints(joints):
    out = []
    for i, j in enumerate(joints):
        lo, hi = LIMITS[i % 2]
        out.append(min(hi, max(lo, float(j))))
    return out


class Action:
    """What Ultron does in one step: turn its joints a little, move its gaze a little,
    close or open each hand."""

    __slots__ = ("turn", "look", "grip")

    def __init__(self, turn=(0.0, 0.0, 0.0, 0.0), look=(0.0, 0.0), grip=(False, False)):
        self.turn = tuple(float(t) for t in turn)
        self.look = tuple(float(v) for v in look)
        self.grip = tuple(bool(g) for g in grip)


class Senses:
    """Everything Ultron gets in one step, and nothing else.

    picture: the view around where it is looking (48 x 64 x 3, brightness 0-1), sharp in
             the middle and blurred toward the edges, with camera noise and shake;
    around:  the blurry wide view (48 x 80 x 3, four room units a pixel), centred where
             it looks and wide enough to hold the whole room, as eyes see coarsely
             almost everywhere;
    joints:  its four joint angles (left shoulder, left elbow, right shoulder, right elbow);
    gaze:    where its eyes point (pan, tilt), each from -1 to 1;
    touch:   'palms': for each hand, (contact 0/1, weight held); 'body': being touched.
    """

    __slots__ = ("picture", "joints", "gaze", "touch", "around")

    def __init__(self, picture, joints, gaze, touch, around=None):
        self.picture = picture
        self.around = around
        self.joints = tuple(joints)
        self.gaze = tuple(gaze)
        self.touch = touch


def clip_look(look):
    dx, dy = look
    n = math.hypot(dx, dy)
    if n > MAX_GAZE:
        dx, dy = dx * MAX_GAZE / n, dy * MAX_GAZE / n
    return dx, dy


def clip_turn(turn):
    return [float(np.clip(t, -MAX_TURN, MAX_TURN)) for t in turn]
