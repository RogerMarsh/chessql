# constants.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""constants tests for cql"""

import unittest
import re

from .. import constants


class CQLConstants(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test____assumptions(self):
        ae = self.assertEqual
        ae(constants.EMPTY_SQUARE_NAME, r"_")
        ae(constants.FILE_NAMES, "abcdefgh")
        ae(constants.CQL_RANK_NAMES, "12345678")
        ae(constants.ANY_WHITE_PIECE_NAME, r"A")
        ae(constants.ANY_BLACK_PIECE_NAME, r"a")
        ae(
            constants.SIMPLE_SQUARE_DESIGNATOR,
            r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
        )
        ae(
            constants.COMPOUND_SQUARE_DESIGNATOR,
            r"".join(
                (
                    r"\[[a-h](?:-[a-h])?[1-8](?:-[1-8])?(?:,[a-h]",
                    r"(?:-[a-h])?[1-8](?:-[1-8])?)*]",
                )
            ),
        )
        ae(constants.WHITE_PIECE_NAMES, r"KQRBNP")
        ae(constants.BLACK_PIECE_NAMES, r"kqrbnp")
        ae(constants.ALL_GAMES_MATCH_PIECE_DESIGNATORS, r"AaKk_")
        ae(constants.ALL_PIECES, r"KQRBNPkqrbnp_")
        ae(constants.PIECE_NAMES, r"KQRBNPkqrbnpAa_")
        ae(constants.WHITE_WIN, "1-0")
        ae(constants.BLACK_WIN, "0-1")
        ae(constants.DRAW, "1/2-1/2")
        ae(constants.RANGE_SEPARATOR, r"-")
        ae(constants.COMPOUND_DESIGNATOR_START, r"\[")
        ae(constants.COMPOUND_DESIGNATOR_END, r"\]")
        ae(constants.FILE_DESIGNATOR, r"[a-h]")
        ae(constants.RANK_DESIGNATOR, r"[1-8]")
        ae(constants.SQUARE_DESIGNATOR_SEPARATOR, r",")
        ae(constants.FILE_RANGE, r"[a-h]-[a-h]")
        ae(constants.RANK_RANGE, r"[1-8]-[1-8]")
        ae(
            constants.PIECE_DESIGNATOR,
            r"".join(
                (
                    r"(?:(?:[a-h](?:-[a-h])?[1-8](?:-[1-8])?|\[[a-h]",
                    r"(?:-[a-h])?[1-8](?:-[1-8])?(?:,[a-h](?:-[a-h])?[1-8]",
                    r"(?:-[1-8])?)*])|(?:(?:[KQRBNPkqrbnpAa_]|\[",
                    "(?:[KQRBNPkqrbnpAa_]+)])(?:[a-h](?:-[a-h])?[1-8]",
                    r"(?:-[1-8])?|\[[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r"(?:,[a-h](?:-[a-h])?[1-8](?:-[1-8])?)*]))|\[",
                    r"(?:[KQRBNPkqrbnpAa_]+)])(?![a-zA-Z0-9_[\]])|",
                    r"[KQRBNPkqrbnpAa_]\b",
                )
            ),
        )
        ae(constants.UP, "up")
        ae(constants.DOWN, "down")
        ae(constants.RIGHT, "right")
        ae(constants.LEFT, "left")
        ae(constants.NORTHEAST, "northeast")
        ae(constants.NORTHWEST, "northwest")
        ae(constants.SOUTHEAST, "southeast")
        ae(constants.SOUTHWEST, "southwest")
        ae(constants.DIAGONAL, "diagonal")
        ae(constants.ORTHOGONAL, "orthogonal")
        ae(constants.VERTICAL, "vertical")
        ae(constants.HORIZONTAL, "horizontal")
        ae(constants.ANYDIRECTION, "anydirection")
        ae(constants.ANY_WHITE_PIECE_NAME, r"A")
        ae(constants.ANY_BLACK_PIECE_NAME, r"a")
        ae(
            constants.SIMPLE_SQUARE_DESIGNATOR,
            r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
        )
        ae(
            constants.COMPOUND_SQUARE_DESIGNATOR,
            "".join(
                (
                    r"\[[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r"(?:,[a-h](?:-[a-h])?[1-8](?:-[1-8])?)*]",
                )
            ),
        )
        ae(constants.CQL_RANK_NAMES, "12345678")
        ae(len([c for c in dir(constants) if not c.startswith("__")]), 37)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(CQLConstants))
