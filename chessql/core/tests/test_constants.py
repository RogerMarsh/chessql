# constants.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""constants tests for cql"""

import unittest
import re

try:
    import pgn_read.core.constants as pgn_read_constants
except ImportError:  # Not ModuleNotFoundError for Pythons earlier than 3.6
    pgn_read_constants = None
from .. import constants


class CQLConstants(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test____assumptions(self):
        ae = self.assertEqual
        ae(constants.FNR, "a-h")
        ae(constants.RNR, "1-8")
        ae(constants.WKING, "K")
        ae(constants.WQUEEN, "Q")
        ae(constants.WROOK, "R")
        ae(constants.WBISHOP, "B")
        ae(constants.WKNIGHT, "N")
        ae(constants.WPAWN, "P")
        ae(constants.BKING, "k")
        ae(constants.BQUEEN, "q")
        ae(constants.BROOK, "r")
        ae(constants.BBISHOP, "b")
        ae(constants.BKNIGHT, "n")
        ae(constants.BPAWN, "p")
        if pgn_read_constants is None:
            ae(constants.WHITE_WIN, "1-0")
            ae(constants.BLACK_WIN, "0-1")
            ae(constants.DRAW, "1/2-1/2")
        ae(constants.EMPTY_SQUARE_NAME, r"_")
        ae(constants.FILE_NAMES, "abcdefgh")
        ae(constants.RANK_NAMES, "12345678")
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
        if pgn_read_constants is None:
            ae(len([c for c in dir(constants) if not c.startswith("__")]), 39)
        else:
            ae(len([c for c in dir(constants) if not c.startswith("__")]), 35)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(CQLConstants))
