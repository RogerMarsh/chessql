# rays.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Define rays in terms of the pgn_read *_ATTACKS dicts.

There are eight basic ray directions, and five compound ray directions.

"""
from pgn_read.core.constants import (
    FILE_ATTACKS,
    RANK_ATTACKS,
    LRD_DIAGONAL_ATTACKS,
    RLD_DIAGONAL_ATTACKS,
)

from .constants import (
    UP,
    DOWN,
    RIGHT,
    LEFT,
    NORTHEAST,
    NORTHWEST,
    SOUTHEAST,
    SOUTHWEST,
    DIAGONAL,
    ORTHOGONAL,
    VERTICAL,
    HORIZONTAL,
    ANYDIRECTION,
)


def _build(direction1, direction2, source):
    """Populate direction1 and direction2 sets from source.

    The two directions are opposite directions in the same line.

    """
    for start, sqr_list in source.items():
        base, line = sqr_list
        for end in line:
            offset = line.index(end)
            if offset > base:
                direction1.add((start, end))
            elif offset < base:
                direction2.add((start, end))


_up = set()
_down = set()
_build(_up, _down, FILE_ATTACKS)
_up = frozenset(_up)
_down = frozenset(_down)

_right = set()
_left = set()
_build(_right, _left, RANK_ATTACKS)
_right = frozenset(_right)
_left = frozenset(_left)

_northwest = set()
_southeast = set()
_build(_northwest, _southeast, LRD_DIAGONAL_ATTACKS)
_northwest = frozenset(_northwest)
_southeast = frozenset(_southeast)

_northeast = set()
_southwest = set()
_build(_northeast, _southwest, RLD_DIAGONAL_ATTACKS)
_northeast = frozenset(_northeast)
_southwest = frozenset(_southwest)

del _build

_ray = {}
_ray[_up] = FILE_ATTACKS
_ray[_down] = FILE_ATTACKS
_ray[_right] = RANK_ATTACKS
_ray[_left] = RANK_ATTACKS
_ray[_northwest] = LRD_DIAGONAL_ATTACKS
_ray[_southeast] = LRD_DIAGONAL_ATTACKS
_ray[_northeast] = RLD_DIAGONAL_ATTACKS
_ray[_southwest] = RLD_DIAGONAL_ATTACKS

_directions = {}
_directions[UP] = (_up,)
_directions[DOWN] = (_down,)
_directions[RIGHT] = (_right,)
_directions[LEFT] = (_left,)
_directions[NORTHEAST] = (_northeast,)
_directions[NORTHWEST] = (_northwest,)
_directions[SOUTHEAST] = (_southeast,)
_directions[SOUTHWEST] = (_southwest,)
_directions[DIAGONAL] = (_northwest, _southeast, _northeast, _southwest)
_directions[ORTHOGONAL] = (_up, _down, _right, _left)
_directions[VERTICAL] = (_up, _down)
_directions[HORIZONTAL] = (_right, _left)
_directions[ANYDIRECTION] = (
    _up,
    _down,
    _right,
    _left,
    _northwest,
    _southeast,
    _northeast,
    _southwest,
)


def get_ray(*args, direction_name=ANYDIRECTION):
    """Return ray squares for args in direction, or None.

    args must contain exactly two square names, ("c1", "h5") for example,
    where the first name is the start of the ray and the second name is the
    end of the ray.  The two squares in ("c2", "a5") are not on the same
    diagonal, file, or rank, so None is returned.

    direction_name must be one of the eight basic directions or five
    compound directions.  Default is ANYDIRECTION.

    """
    for direction in _directions[direction_name]:
        if args in direction:
            start, end = args
            start_index, vector = _ray[direction][start]
            end_index = vector.index(end)
            if end_index > start_index:
                return vector[start_index : end_index + 1]
            return list(reversed(vector[end_index : start_index + 1]))
    return None


del FILE_ATTACKS, RANK_ATTACKS, LRD_DIAGONAL_ATTACKS, RLD_DIAGONAL_ATTACKS
del UP
del DOWN
del RIGHT
del LEFT
del NORTHEAST
del NORTHWEST
del SOUTHEAST
del SOUTHWEST
del DIAGONAL
del ORTHOGONAL
del VERTICAL
del HORIZONTAL
del ANYDIRECTION
del _up
del _down
del _right
del _left
del _northwest
del _southeast
del _northeast
del _southwest
