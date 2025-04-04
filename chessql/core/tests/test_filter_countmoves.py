# test_filter_countmoves.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'countmoves' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FilterCountMoves(verify.Verify):

    def test_019_countmoves_01(self):
        self.verify("countmoves", [], returncode=1)

    def test_019_countmoves_02(self):
        self.verify("countmoves k", [], returncode=1)

    def test_019_countmoves_03_move_01_dash_ascii(self):
        self.verify(
            "countmoves --",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_019_countmoves_03_move_02_dash_utf8(self):
        self.verify(
            "countmoves ――",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_019_countmoves_03_move_03_take_ascii(self):
        self.verify(
            "countmoves [x]",
            [
                (3, "CountMoves"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_019_countmoves_03_move_04_take_utf8(self):
        self.verify(
            "countmoves ×",
            [
                (3, "CountMoves"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_01_plus_01(self):
        self.verify(
            "countmoves ×+2",
            [
                (3, "Plus"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_02_minus_01_ascii(self):
        self.verify_declare_fail(
            "countmoves ×-2",
            [
                (3, "Minus"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_02_minus_02_utf8(self):
        self.verify_declare_fail(
            "countmoves ×-2",
            [
                (3, "Minus"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_03_multiply_01(self):
        self.verify(
            "countmoves ×*2",
            [
                (3, "Star"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_04_divide_01(self):
        self.verify(
            "countmoves ×/2",
            [
                (3, "Divide"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_05_modulus_01(self):
        self.verify(
            "countmoves ×%2",
            [
                (3, "Modulus"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    # Is it '--' '>' or '-->'? not relevant here.
    def test_019_countmoves_03_move_05_take_utf8_06_gt_01(self):
        self.verify(
            "countmoves ×>2",
            [
                (3, "GT"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_06_gt_02(self):
        self.verify(
            "countmoves × >2",
            [
                (3, "GT"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    # Is it '--' '>' or '-->'? not relevant here.
    def test_019_countmoves_03_move_05_take_utf8_07_ge_01(self):
        self.verify(
            "countmoves ×>=2",
            [
                (3, "GE"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_07_ge_02(self):
        self.verify(
            "countmoves × >=2",
            [
                (3, "GE"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_08_lt_01(self):
        self.verify(
            "countmoves ×<2",
            [
                (3, "LT"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_09_le_01(self):
        self.verify(
            "countmoves ×<=2",
            [
                (3, "LE"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_10_eq_01(self):
        self.verify(
            "countmoves ×==2",
            [
                (3, "Eq"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_03_move_05_take_utf8_11_ne_01(self):
        self.verify(
            "countmoves ×!=2",
            [
                (3, "NE"),
                (4, "CountMoves"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_01_dash_ascii(self):
        self.verify(
            "countmoves legal --",
            [
                (3, "CountMoves"),
                (4, "Legal"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_019_countmoves_04_legal_02_dash_utf8(self):
        self.verify(
            "countmoves legal ――",
            [
                (3, "CountMoves"),
                (4, "Legal"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_019_countmoves_04_legal_03_take_ascii(self):
        self.verify("countmoves legal [x]", [], returncode=1)

    def test_019_countmoves_04_legal_04_take_utf8(self):
        self.verify("countmoves legal ×", [], returncode=1)

    def test_019_countmoves_04_legal_05_dash_ascii_01_plus_01(self):
        self.verify(
            "countmoves legal --+2",
            [
                (3, "Plus"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_02_minus_01_ascii(self):
        self.verify_declare_fail(
            "countmoves legal ---2",
            [
                (3, "Minus"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_02_minus_02_utf8(self):
        self.verify_declare_fail(
            "countmoves legal ――-2",
            [
                (3, "Minus"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_03_multiply_01(self):
        self.verify(
            "countmoves legal --*2",
            [
                (3, "Star"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_04_divide_01(self):
        self.verify(
            "countmoves legal --/2",
            [
                (3, "Divide"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_05_modulus_01(self):
        self.verify(
            "countmoves legal --%2",
            [
                (3, "Modulus"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    # Is it '--' '>' or '-->'?
    def test_019_countmoves_04_legal_05_dash_ascii_06_gt_01(self):
        self.verify("countmoves legal -->2", [], returncode=1)

    def test_019_countmoves_04_legal_05_dash_ascii_06_gt_02(self):
        self.verify(
            "countmoves legal -- >2",
            [
                (3, "GT"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    # Is it '--' '>' or '-->'?
    def test_019_countmoves_04_legal_05_dash_ascii_07_ge_01(self):
        self.verify("countmoves legal -->=2", [], returncode=1)

    def test_019_countmoves_04_legal_05_dash_ascii_07_ge_02(self):
        self.verify(
            "countmoves legal -- >=2",
            [
                (3, "GE"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_08_lt_01(self):
        self.verify(
            "countmoves legal --<2",
            [
                (3, "LT"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_09_le_01(self):
        self.verify(
            "countmoves legal --<=2",
            [
                (3, "LE"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_10_eq_01(self):
        self.verify(
            "countmoves legal --==2",
            [
                (3, "Eq"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_04_legal_05_dash_ascii_11_ne_01(self):
        self.verify(
            "countmoves legal --!=2",
            [
                (3, "NE"),
                (4, "CountMoves"),
                (5, "Legal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_01_dash_ascii(self):
        self.verify(
            "countmoves pseudolegal --",
            [
                (3, "CountMoves"),
                (4, "Pseudolegal"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_02_dash_utf8(self):
        self.verify(
            "countmoves pseudolegal ――",
            [
                (3, "CountMoves"),
                (4, "Pseudolegal"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_03_take_ascii(self):
        self.verify("countmoves pseudolegal [x]", [], returncode=1)

    def test_019_countmoves_05_pseudolegal_04_take_utf8(self):
        self.verify("countmoves pseudolegal ×", [], returncode=1)

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_01_plus_01(self):
        self.verify(
            "countmoves pseudolegal ――+2",
            [
                (3, "Plus"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_02_minus_01_ascii(
        self,
    ):
        self.verify_declare_fail(
            "countmoves pseudolegal ――-2",
            [
                (3, "Minus"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_02_minus_02_utf8(self):
        self.verify_declare_fail(
            "countmoves pseudolegal ――-2",
            [
                (3, "Minus"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_03_multiply_01(self):
        self.verify(
            "countmoves pseudolegal ――*2",
            [
                (3, "Star"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_04_divide_01(self):
        self.verify(
            "countmoves pseudolegal ――/2",
            [
                (3, "Divide"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_05_modulus_01(self):
        self.verify(
            "countmoves pseudolegal ――%2",
            [
                (3, "Modulus"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    # Is it '--' '>' or '-->'? not relevant here.
    def test_019_countmoves_05_pseudolegal_05_dash_utf8_06_gt_01(self):
        self.verify(
            "countmoves pseudolegal ――>2",
            [
                (3, "GT"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_06_gt_02(self):
        self.verify(
            "countmoves pseudolegal ―― >2",
            [
                (3, "GT"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    # Is it '--' '>' or '-->'? not relevant here.
    def test_019_countmoves_05_pseudolegal_05_dash_utf8_07_ge_01(self):
        self.verify(
            "countmoves pseudolegal ――>=2",
            [
                (3, "GE"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_07_ge_02(self):
        self.verify(
            "countmoves pseudolegal ―― >=2",
            [
                (3, "GE"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_08_lt_01(self):
        self.verify(
            "countmoves pseudolegal ――<2",
            [
                (3, "LT"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_09_le_01(self):
        self.verify(
            "countmoves pseudolegal ――<=2",
            [
                (3, "LE"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_10_eq_01(self):
        self.verify(
            "countmoves pseudolegal ――==2",
            [
                (3, "Eq"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_019_countmoves_05_pseudolegal_05_dash_utf8_11_ne_01(self):
        self.verify(
            "countmoves pseudolegal ――!=2",
            [
                (3, "NE"),
                (4, "CountMoves"),
                (5, "Pseudolegal"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (4, "Integer"),
            ],
        )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterCountMoves))
