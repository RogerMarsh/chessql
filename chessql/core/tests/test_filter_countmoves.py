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

    def test_019_countmoves_01_plain_01_bare(self):
        self.verify("countmoves", [], returncode=1)

    def test_019_countmoves_01_plain_04_target_01_btm(self):
        self.verify(
            "countmoves --(btm)",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_019_countmoves_01_plain_04_target_02_o_o(self):
        self.verify(
            "countmoves --(o-o)",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
            ],
        )

    def test_019_countmoves_01_plain_04_target_03_o_o_o(self):
        self.verify(
            "countmoves --(o-o-o)",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OOO"),
            ],
        )

    def test_019_countmoves_01_plain_04_target_04_castle(self):
        self.verify(
            "countmoves --(castle)",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "Castle"),
            ],
        )

    def test_019_countmoves_01_plain_04_target_05_enpassant(self):
        self.verify(
            "countmoves --(enpassant)",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "EnPassant"),
            ],
        )

    def test_019_countmoves_01_plain_04_target_06_o_o_set(self):
        self.verify(
            "countmoves --(o-o to)",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (6, "To"),
            ],
        )

    def test_019_countmoves_01_plain_04_target_07_set_o_o(self):
        self.verify(
            "countmoves --(Rc4 o-o)",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "PieceDesignator"),
                (6, "OO"),
            ],
        )

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

    def test_019_countmoves_06_da_01_plain_06_rep_01_zero_up(self):
        self.verify("countmoves --*", [], returncode=1)

    def test_019_countmoves_06_da_01_plain_06_rep_02_one_up(self):
        self.verify("countmoves --+", [], returncode=1)

    def test_019_countmoves_06_da_01_plain_06_rep_03_optional(self):
        self.verify("countmoves --?", [], returncode=1)

    def test_019_countmoves_06_da_01_plain_06_rep_04_exact(self):
        self.verify("countmoves --{5}", [], returncode=1)

    def test_019_countmoves_06_da_01_plain_06_rep_05_range(self):
        self.verify("countmoves --{3,5}", [], returncode=1)

    def test_019_countmoves_06_da_01_plain_06_rep_06_up_to(self):
        self.verify("countmoves --{,5}", [], returncode=1)

    def test_019_countmoves_06_da_01_plain_06_rep_07_and_over(self):
        self.verify("countmoves --{3,}", [], returncode=1)

    def test_019_countmoves_06_da_01_plain_06_rep_08_force_zero_up(self):
        self.verify("countmoves --{*}", [], returncode=1)

    def test_019_countmoves_06_da_01_plain_06_rep_09_force_one_up(self):
        self.verify("countmoves --{+}", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_01_zero_up(self):
        self.verify("countmoves e2--*", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_02_one_up(self):
        self.verify("countmoves e2--+", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_03_optional(self):
        self.verify("countmoves e2--?", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_04_exact(self):
        self.verify("countmoves e2--{5}", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_05_range(self):
        self.verify("countmoves e2--{3,5}", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_06_up_to(self):
        self.verify("countmoves e2--{,5}", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_07_and_over(self):
        self.verify("countmoves e2--{3,}", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2--{*}", [], returncode=1)

    def test_019_countmoves_06_da_02_left_06_rep_09_force_one_up(self):
        self.verify("countmoves e2--{+}", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_01_zero_up(self):
        self.verify("countmoves --Qa4*", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_02_one_up(self):
        self.verify("countmoves --Qa4+", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_03_optional(self):
        self.verify("countmoves --Qa4?", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_04_exact(self):
        self.verify("countmoves --Qa4{5}", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_05_range(self):
        self.verify("countmoves --Qa4{3,5}", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_06_up_to(self):
        self.verify("countmoves --Qa4{,5}", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_07_and_over(self):
        self.verify("countmoves --Qa4{3,}", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_08_force_zero_up(self):
        self.verify("countmoves --Qa4{*}", [], returncode=1)

    def test_019_countmoves_06_da_03_right_06_rep_09_force_one_up(self):
        self.verify("countmoves --Qa4{+}", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_01_zero_up(self):
        self.verify("countmoves e2--Qa4*", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_02_one_up(self):
        self.verify("countmoves e2--Qa4+", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_03_optional(self):
        self.verify("countmoves e2--Qa4?", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_04_exact(self):
        self.verify("countmoves e2--Qa4{5}", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_05_range(self):
        self.verify("countmoves e2--Qa4{3,5}", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_06_up_to(self):
        self.verify("countmoves e2--Qa4{,5}", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_07_and_over(self):
        self.verify("countmoves e2--Qa4{3,}", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2--Qa4{*}", [], returncode=1)

    def test_019_countmoves_06_da_04_lr_06_rep_09_force_one_up(self):
        self.verify("countmoves e2--Qa4{+}", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_01_zero_up(self):
        self.verify("countmoves --=q*", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_02_one_up(self):
        self.verify("countmoves --=q+", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_03_optional(self):
        self.verify("countmoves --=q?", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_04_exact(self):
        self.verify("countmoves --=q{5}", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_05_range(self):
        self.verify("countmoves --=q{3,5}", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_06_up_to(self):
        self.verify("countmoves --=q{,5}", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_07_and_over(self):
        self.verify("countmoves --=q{3,}", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves --=q{*}", [], returncode=1)

    def test_019_countmoves_06_da_05_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves --=q{+}", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_01_zero_up(self):
        self.verify("countmoves e2--=q*", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_02_one_up(self):
        self.verify("countmoves e2--=q+", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_03_optional(self):
        self.verify("countmoves e2--=q?", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_04_exact(self):
        self.verify("countmoves e2--=q{5}", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_05_range(self):
        self.verify("countmoves e2--=q{3,5}", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_06_up_to(self):
        self.verify("countmoves e2--=q{,5}", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_07_and_over(self):
        self.verify("countmoves e2--=q{3,}", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2--=q{*}", [], returncode=1)

    def test_019_countmoves_06_da_06_left_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves e2--=q{+}", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_01_zero_up(self):
        self.verify("countmoves --Qa4=q*", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_02_one_up(self):
        self.verify("countmoves --Qa4=q+", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_03_optional(self):
        self.verify("countmoves --Qa4=q?", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_04_exact(self):
        self.verify("countmoves --Qa4=q{5}", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_05_range(self):
        self.verify("countmoves --Qa4=q{3,5}", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_06_up_to(self):
        self.verify("countmoves --Qa4=q{,5}", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_07_and_over(self):
        self.verify("countmoves --Qa4=q{3,}", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves --Qa4=q{*}", [], returncode=1)

    def test_019_countmoves_06_da_07_right_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves --Qa4=q{+}", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_01_zero_up(self):
        self.verify("countmoves e2--Qa4=q*", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_02_one_up(self):
        self.verify("countmoves e2--Qa4=q+", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_03_optional(self):
        self.verify("countmoves e2--Qa4=q?", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_04_exact(self):
        self.verify("countmoves e2--Qa4=q{5}", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_05_range(self):
        self.verify("countmoves e2--Qa4=q{3,5}", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_06_up_to(self):
        self.verify("countmoves e2--Qa4=q{,5}", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_07_and_over(self):
        self.verify("countmoves e2--Qa4=q{3,}", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2--Qa4=q{*}", [], returncode=1)

    def test_019_countmoves_06_da_08_lr_prom_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2--Qa4=q{+}", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_01_zero_up(self):
        self.verify("countmoves --(btm)*", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_02_one_up(self):
        self.verify("countmoves --(btm)+", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_03_optional(self):
        self.verify("countmoves --(btm)?", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_04_exact(self):
        self.verify("countmoves --(btm){5}", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_05_range(self):
        self.verify("countmoves --(btm){3,5}", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_06_up_to(self):
        self.verify("countmoves --(btm){,5}", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_07_and_over(self):
        self.verify("countmoves --(btm){3,}", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_08_force_zero_up(self):
        self.verify("countmoves --(btm){*}", [], returncode=1)

    def test_019_countmoves_06_da_09_target_06_rep_09_force_one_up(self):
        self.verify("countmoves --(btm){+}", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_01_zero_up(self):
        self.verify("countmoves e2--(btm)*", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_02_one_up(self):
        self.verify("countmoves e2--(btm)+", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_03_optional(self):
        self.verify("countmoves e2--(btm)?", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_04_exact(self):
        self.verify("countmoves e2--(btm){5}", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_05_range(self):
        self.verify("countmoves e2--(btm){3,5}", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_06_up_to(self):
        self.verify("countmoves e2--(btm){,5}", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_07_and_over(self):
        self.verify("countmoves e2--(btm){3,}", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2--(btm){*}", [], returncode=1)

    def test_019_countmoves_06_da_10_left_target_06_rep_09_force_one_up(self):
        self.verify("countmoves e2--(btm){+}", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_01_zero_up(self):
        self.verify("countmoves --Qa4(btm)*", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_02_one_up(self):
        self.verify("countmoves --Qa4(btm)+", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_03_optional(self):
        self.verify("countmoves --Qa4(btm)?", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_04_exact(self):
        self.verify("countmoves --Qa4(btm){5}", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_05_range(self):
        self.verify("countmoves --Qa4(btm){3,5}", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_06_up_to(self):
        self.verify("countmoves --Qa4(btm){,5}", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_07_and_over(self):
        self.verify("countmoves --Qa4(btm){3,}", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves --Qa4(btm){*}", [], returncode=1)

    def test_019_countmoves_06_da_11_right_target_06_rep_09_force_one_up(self):
        self.verify("countmoves --Qa4(btm){+}", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_01_zero_up(self):
        self.verify("countmoves e2--Qa4(btm)*", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_02_one_up(self):
        self.verify("countmoves e2--Qa4(btm)+", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_03_optional(self):
        self.verify("countmoves e2--Qa4(btm)?", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_04_exact(self):
        self.verify("countmoves e2--Qa4(btm){5}", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_05_range(self):
        self.verify("countmoves e2--Qa4(btm){3,5}", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_06_up_to(self):
        self.verify("countmoves e2--Qa4(btm){,5}", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_07_and_over(self):
        self.verify("countmoves e2--Qa4(btm){3,}", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2--Qa4(btm){*}", [], returncode=1)

    def test_019_countmoves_06_da_12_lr_target_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2--Qa4(btm){+}", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves --=q(btm)*", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves --=q(btm)+", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves --=q(btm)?", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves --=q(btm){5}", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_05_range(self):
        self.verify("countmoves --=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves --=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves --=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_08_force_zero_up(self):
        self.verify("countmoves --=q(btm){*}", [], returncode=1)

    def test_019_countmoves_06_da_13_prom_targ_06_rep_09_force_one_up(self):
        self.verify("countmoves --=q(btm){+}", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves e2--=q(btm)*", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves e2--=q(btm)+", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves e2--=q(btm)?", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves e2--=q(btm){5}", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_05_range(self):
        self.verify("countmoves e2--=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves e2--=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves e2--=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2--=q(btm){*}", [], returncode=1)

    def test_019_countmoves_06_da_14_l_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2--=q(btm){+}", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves --Qa4=q(btm)*", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves --Qa4=q(btm)+", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves --Qa4=q(btm)?", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves --Qa4=q(btm){5}", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_05_range(self):
        self.verify("countmoves --Qa4=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves --Qa4=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves --Qa4=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves --Qa4=q(btm){*}", [], returncode=1)

    def test_019_countmoves_06_da_15_r_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves --Qa4=q(btm){+}", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves e2--Qa4=q(btm)*", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves e2--Qa4=q(btm)+", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves e2--Qa4=q(btm)?", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves e2--Qa4=q(btm){5}", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_05_range(self):
        self.verify("countmoves e2--Qa4=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves e2--Qa4=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves e2--Qa4=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2--Qa4=q(btm){*}", [], returncode=1)

    def test_019_countmoves_06_da_16_lr_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2--Qa4=q(btm){+}", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_01_zero_up(self):
        self.verify("countmoves ――*", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_02_one_up(self):
        self.verify("countmoves ――+", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_03_optional(self):
        self.verify("countmoves ――?", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_04_exact(self):
        self.verify("countmoves ――{5}", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_05_range(self):
        self.verify("countmoves ――{3,5}", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_06_up_to(self):
        self.verify("countmoves ――{,5}", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_07_and_over(self):
        self.verify("countmoves ――{3,}", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_08_force_zero_up(self):
        self.verify("countmoves ――{*}", [], returncode=1)

    def test_019_countmoves_07_du_01_plain_06_rep_09_force_one_up(self):
        self.verify("countmoves ――{+}", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_01_zero_up(self):
        self.verify("countmoves e2――*", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_02_one_up(self):
        self.verify("countmoves e2――+", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_03_optional(self):
        self.verify("countmoves e2――?", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_04_exact(self):
        self.verify("countmoves e2――{5}", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_05_range(self):
        self.verify("countmoves e2――{3,5}", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_06_up_to(self):
        self.verify("countmoves e2――{,5}", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_07_and_over(self):
        self.verify("countmoves e2――{3,}", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2――{*}", [], returncode=1)

    def test_019_countmoves_07_du_02_left_06_rep_09_force_one_up(self):
        self.verify("countmoves e2――{+}", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_01_zero_up(self):
        self.verify("countmoves ――Qa4*", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_02_one_up(self):
        self.verify("countmoves ――Qa4+", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_03_optional(self):
        self.verify("countmoves ――Qa4?", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_04_exact(self):
        self.verify("countmoves ――Qa4{5}", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_05_range(self):
        self.verify("countmoves ――Qa4{3,5}", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_06_up_to(self):
        self.verify("countmoves ――Qa4{,5}", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_07_and_over(self):
        self.verify("countmoves ――Qa4{3,}", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_08_force_zero_up(self):
        self.verify("countmoves ――Qa4{*}", [], returncode=1)

    def test_019_countmoves_07_du_03_right_06_rep_09_force_one_up(self):
        self.verify("countmoves ――Qa4{+}", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_01_zero_up(self):
        self.verify("countmoves e2――Qa4*", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_02_one_up(self):
        self.verify("countmoves e2――Qa4+", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_03_optional(self):
        self.verify("countmoves e2――Qa4?", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_04_exact(self):
        self.verify("countmoves e2――Qa4{5}", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_05_range(self):
        self.verify("countmoves e2――Qa4{3,5}", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_06_up_to(self):
        self.verify("countmoves e2――Qa4{,5}", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_07_and_over(self):
        self.verify("countmoves e2――Qa4{3,}", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2――Qa4{*}", [], returncode=1)

    def test_019_countmoves_07_du_04_lr_06_rep_09_force_one_up(self):
        self.verify("countmoves e2――Qa4{+}", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_01_zero_up(self):
        self.verify("countmoves ――=q*", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_02_one_up(self):
        self.verify("countmoves ――=q+", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_03_optional(self):
        self.verify("countmoves ――=q?", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_04_exact(self):
        self.verify("countmoves ――=q{5}", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_05_range(self):
        self.verify("countmoves ――=q{3,5}", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_06_up_to(self):
        self.verify("countmoves ――=q{,5}", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_07_and_over(self):
        self.verify("countmoves ――=q{3,}", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves ――=q{*}", [], returncode=1)

    def test_019_countmoves_07_du_05_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves ――=q{+}", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_01_zero_up(self):
        self.verify("countmoves e2――=q*", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_02_one_up(self):
        self.verify("countmoves e2――=q+", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_03_optional(self):
        self.verify("countmoves e2――=q?", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_04_exact(self):
        self.verify("countmoves e2――=q{5}", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_05_range(self):
        self.verify("countmoves e2――=q{3,5}", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_06_up_to(self):
        self.verify("countmoves e2――=q{,5}", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_07_and_over(self):
        self.verify("countmoves e2――=q{3,}", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2――=q{*}", [], returncode=1)

    def test_019_countmoves_07_du_06_left_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves e2――=q{+}", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_01_zero_up(self):
        self.verify("countmoves ――Qa4=q*", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_02_one_up(self):
        self.verify("countmoves ――Qa4=q+", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_03_optional(self):
        self.verify("countmoves ――Qa4=q?", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_04_exact(self):
        self.verify("countmoves ――Qa4=q{5}", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_05_range(self):
        self.verify("countmoves ――Qa4=q{3,5}", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_06_up_to(self):
        self.verify("countmoves ――Qa4=q{,5}", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_07_and_over(self):
        self.verify("countmoves ――Qa4=q{3,}", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves ――Qa4=q{*}", [], returncode=1)

    def test_019_countmoves_07_du_07_right_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves ――Qa4=q{+}", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_01_zero_up(self):
        self.verify("countmoves e2――Qa4=q*", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_02_one_up(self):
        self.verify("countmoves e2――Qa4=q+", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_03_optional(self):
        self.verify("countmoves e2――Qa4=q?", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_04_exact(self):
        self.verify("countmoves e2――Qa4=q{5}", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_05_range(self):
        self.verify("countmoves e2――Qa4=q{3,5}", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_06_up_to(self):
        self.verify("countmoves e2――Qa4=q{,5}", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_07_and_over(self):
        self.verify("countmoves e2――Qa4=q{3,}", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2――Qa4=q{*}", [], returncode=1)

    def test_019_countmoves_07_du_08_lr_prom_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2――Qa4=q{+}", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_01_zero_up(self):
        self.verify("countmoves ――(btm)*", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_02_one_up(self):
        self.verify("countmoves ――(btm)+", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_03_optional(self):
        self.verify("countmoves ――(btm)?", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_04_exact(self):
        self.verify("countmoves ――(btm){5}", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_05_range(self):
        self.verify("countmoves ――(btm){3,5}", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_06_up_to(self):
        self.verify("countmoves ――(btm){,5}", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_07_and_over(self):
        self.verify("countmoves ――(btm){3,}", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_08_force_zero_up(self):
        self.verify("countmoves ――(btm){*}", [], returncode=1)

    def test_019_countmoves_07_du_09_target_06_rep_09_force_one_up(self):
        self.verify("countmoves ――(btm){+}", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_01_zero_up(self):
        self.verify("countmoves e2――(btm)*", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_02_one_up(self):
        self.verify("countmoves e2――(btm)+", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_03_optional(self):
        self.verify("countmoves e2――(btm)?", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_04_exact(self):
        self.verify("countmoves e2――(btm){5}", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_05_range(self):
        self.verify("countmoves e2――(btm){3,5}", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_06_up_to(self):
        self.verify("countmoves e2――(btm){,5}", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_07_and_over(self):
        self.verify("countmoves e2――(btm){3,}", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2――(btm){*}", [], returncode=1)

    def test_019_countmoves_07_du_10_left_target_06_rep_09_force_one_up(self):
        self.verify("countmoves e2――(btm){+}", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_01_zero_up(self):
        self.verify("countmoves ――Qa4(btm)*", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_02_one_up(self):
        self.verify("countmoves ――Qa4(btm)+", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_03_optional(self):
        self.verify("countmoves ――Qa4(btm)?", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_04_exact(self):
        self.verify("countmoves ――Qa4(btm){5}", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_05_range(self):
        self.verify("countmoves ――Qa4(btm){3,5}", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_06_up_to(self):
        self.verify("countmoves ――Qa4(btm){,5}", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_07_and_over(self):
        self.verify("countmoves ――Qa4(btm){3,}", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves ――Qa4(btm){*}", [], returncode=1)

    def test_019_countmoves_07_du_11_right_target_06_rep_09_force_one_up(self):
        self.verify("countmoves ――Qa4(btm){+}", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_01_zero_up(self):
        self.verify("countmoves e2――Qa4(btm)*", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_02_one_up(self):
        self.verify("countmoves e2――Qa4(btm)+", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_03_optional(self):
        self.verify("countmoves e2――Qa4(btm)?", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_04_exact(self):
        self.verify("countmoves e2――Qa4(btm){5}", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_05_range(self):
        self.verify("countmoves e2――Qa4(btm){3,5}", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_06_up_to(self):
        self.verify("countmoves e2――Qa4(btm){,5}", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_07_and_over(self):
        self.verify("countmoves e2――Qa4(btm){3,}", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2――Qa4(btm){*}", [], returncode=1)

    def test_019_countmoves_07_du_12_lr_target_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2――Qa4(btm){+}", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves ――=q(btm)*", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves ――=q(btm)+", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves ――=q(btm)?", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves ――=q(btm){5}", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_05_range(self):
        self.verify("countmoves ――=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves ――=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves ――=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_08_force_zero_up(self):
        self.verify("countmoves ――=q(btm){*}", [], returncode=1)

    def test_019_countmoves_07_du_13_prom_targ_06_rep_09_force_one_up(self):
        self.verify("countmoves ――=q(btm){+}", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves e2――=q(btm)*", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves e2――=q(btm)+", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves e2――=q(btm)?", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves e2――=q(btm){5}", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_05_range(self):
        self.verify("countmoves e2――=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves e2――=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves e2――=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2――=q(btm){*}", [], returncode=1)

    def test_019_countmoves_07_du_14_l_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2――=q(btm){+}", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves ――Qa4=q(btm)*", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves ――Qa4=q(btm)+", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves ――Qa4=q(btm)?", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves ――Qa4=q(btm){5}", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_05_range(self):
        self.verify("countmoves ――Qa4=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves ――Qa4=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves ――Qa4=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves ――Qa4=q(btm){*}", [], returncode=1)

    def test_019_countmoves_07_du_15_r_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves ――Qa4=q(btm){+}", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves e2――Qa4=q(btm)*", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves e2――Qa4=q(btm)+", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves e2――Qa4=q(btm)?", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves e2――Qa4=q(btm){5}", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_05_range(self):
        self.verify("countmoves e2――Qa4=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves e2――Qa4=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves e2――Qa4=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2――Qa4=q(btm){*}", [], returncode=1)

    def test_019_countmoves_07_du_16_lr_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2――Qa4=q(btm){+}", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_01_zero_up(self):
        self.verify("countmoves [x]*", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_02_one_up(self):
        self.verify("countmoves [x]+", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_03_optional(self):
        self.verify("countmoves [x]?", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_04_exact(self):
        self.verify("countmoves [x]{5}", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_05_range(self):
        self.verify("countmoves [x]{3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_06_up_to(self):
        self.verify("countmoves [x]{,5}", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_07_and_over(self):
        self.verify("countmoves [x]{3,}", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_08_force_zero_up(self):
        self.verify("countmoves [x]{*}", [], returncode=1)

    def test_019_countmoves_08_ta_01_plain_06_rep_09_force_one_up(self):
        self.verify("countmoves [x]{+}", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_01_zero_up(self):
        self.verify("countmoves e2[x]*", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_02_one_up(self):
        self.verify("countmoves e2[x]+", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_03_optional(self):
        self.verify("countmoves e2[x]?", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_04_exact(self):
        self.verify("countmoves e2[x]{5}", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_05_range(self):
        self.verify("countmoves e2[x]{3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_06_up_to(self):
        self.verify("countmoves e2[x]{,5}", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_07_and_over(self):
        self.verify("countmoves e2[x]{3,}", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2[x]{*}", [], returncode=1)

    def test_019_countmoves_08_ta_02_left_06_rep_09_force_one_up(self):
        self.verify("countmoves e2[x]{+}", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_01_zero_up(self):
        self.verify("countmoves [x]Qa4*", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_02_one_up(self):
        self.verify("countmoves [x]Qa4+", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_03_optional(self):
        self.verify("countmoves [x]Qa4?", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_04_exact(self):
        self.verify("countmoves [x]Qa4{5}", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_05_range(self):
        self.verify("countmoves [x]Qa4{3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_06_up_to(self):
        self.verify("countmoves [x]Qa4{,5}", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_07_and_over(self):
        self.verify("countmoves [x]Qa4{3,}", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_08_force_zero_up(self):
        self.verify("countmoves [x]Qa4{*}", [], returncode=1)

    def test_019_countmoves_08_ta_03_right_06_rep_09_force_one_up(self):
        self.verify("countmoves [x]Qa4{+}", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_01_zero_up(self):
        self.verify("countmoves e2[x]Qa4*", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_02_one_up(self):
        self.verify("countmoves e2[x]Qa4+", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_03_optional(self):
        self.verify("countmoves e2[x]Qa4?", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_04_exact(self):
        self.verify("countmoves e2[x]Qa4{5}", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_05_range(self):
        self.verify("countmoves e2[x]Qa4{3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_06_up_to(self):
        self.verify("countmoves e2[x]Qa4{,5}", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_07_and_over(self):
        self.verify("countmoves e2[x]Qa4{3,}", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2[x]Qa4{*}", [], returncode=1)

    def test_019_countmoves_08_ta_04_lr_06_rep_09_force_one_up(self):
        self.verify("countmoves e2[x]Qa4{+}", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_01_zero_up(self):
        self.verify("countmoves [x]=q*", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_02_one_up(self):
        self.verify("countmoves [x]=q+", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_03_optional(self):
        self.verify("countmoves [x]=q?", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_04_exact(self):
        self.verify("countmoves [x]=q{5}", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_05_range(self):
        self.verify("countmoves [x]=q{3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_06_up_to(self):
        self.verify("countmoves [x]=q{,5}", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_07_and_over(self):
        self.verify("countmoves [x]=q{3,}", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves [x]=q{*}", [], returncode=1)

    def test_019_countmoves_08_ta_05_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves [x]=q{+}", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_01_zero_up(self):
        self.verify("countmoves e2[x]=q*", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_02_one_up(self):
        self.verify("countmoves e2[x]=q+", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_03_optional(self):
        self.verify("countmoves e2[x]=q?", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_04_exact(self):
        self.verify("countmoves e2[x]=q{5}", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_05_range(self):
        self.verify("countmoves e2[x]=q{3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_06_up_to(self):
        self.verify("countmoves e2[x]=q{,5}", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_07_and_over(self):
        self.verify("countmoves e2[x]=q{3,}", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2[x]=q{*}", [], returncode=1)

    def test_019_countmoves_08_ta_06_left_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves e2[x]=q{+}", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_01_zero_up(self):
        self.verify("countmoves [x]Qa4=q*", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_02_one_up(self):
        self.verify("countmoves [x]Qa4=q+", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_03_optional(self):
        self.verify("countmoves [x]Qa4=q?", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_04_exact(self):
        self.verify("countmoves [x]Qa4=q{5}", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_05_range(self):
        self.verify("countmoves [x]Qa4=q{3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_06_up_to(self):
        self.verify("countmoves [x]Qa4=q{,5}", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_07_and_over(self):
        self.verify("countmoves [x]Qa4=q{3,}", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves [x]Qa4=q{*}", [], returncode=1)

    def test_019_countmoves_08_ta_07_right_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves [x]Qa4=q{+}", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_01_zero_up(self):
        self.verify("countmoves e2[x]Qa4=q*", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_02_one_up(self):
        self.verify("countmoves e2[x]Qa4=q+", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_03_optional(self):
        self.verify("countmoves e2[x]Qa4=q?", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_04_exact(self):
        self.verify("countmoves e2[x]Qa4=q{5}", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_05_range(self):
        self.verify("countmoves e2[x]Qa4=q{3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_06_up_to(self):
        self.verify("countmoves e2[x]Qa4=q{,5}", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_07_and_over(self):
        self.verify("countmoves e2[x]Qa4=q{3,}", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2[x]Qa4=q{*}", [], returncode=1)

    def test_019_countmoves_08_ta_08_lr_prom_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2[x]Qa4=q{+}", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_01_zero_up(self):
        self.verify("countmoves [x](btm)*", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_02_one_up(self):
        self.verify("countmoves [x](btm)+", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_03_optional(self):
        self.verify("countmoves [x](btm)?", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_04_exact(self):
        self.verify("countmoves [x](btm){5}", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_05_range(self):
        self.verify("countmoves [x](btm){3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_06_up_to(self):
        self.verify("countmoves [x](btm){,5}", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_07_and_over(self):
        self.verify("countmoves [x](btm){3,}", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_08_force_zero_up(self):
        self.verify("countmoves [x](btm){*}", [], returncode=1)

    def test_019_countmoves_08_ta_09_target_06_rep_09_force_one_up(self):
        self.verify("countmoves [x](btm){+}", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_01_zero_up(self):
        self.verify("countmoves e2[x](btm)*", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_02_one_up(self):
        self.verify("countmoves e2[x](btm)+", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_03_optional(self):
        self.verify("countmoves e2[x](btm)?", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_04_exact(self):
        self.verify("countmoves e2[x](btm){5}", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_05_range(self):
        self.verify("countmoves e2[x](btm){3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_06_up_to(self):
        self.verify("countmoves e2[x](btm){,5}", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_07_and_over(self):
        self.verify("countmoves e2[x](btm){3,}", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2[x](btm){*}", [], returncode=1)

    def test_019_countmoves_08_ta_10_left_target_06_rep_09_force_one_up(self):
        self.verify("countmoves e2[x](btm){+}", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_01_zero_up(self):
        self.verify("countmoves [x]Qa4(btm)*", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_02_one_up(self):
        self.verify("countmoves [x]Qa4(btm)+", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_03_optional(self):
        self.verify("countmoves [x]Qa4(btm)?", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_04_exact(self):
        self.verify("countmoves [x]Qa4(btm){5}", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_05_range(self):
        self.verify("countmoves [x]Qa4(btm){3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_06_up_to(self):
        self.verify("countmoves [x]Qa4(btm){,5}", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_07_and_over(self):
        self.verify("countmoves [x]Qa4(btm){3,}", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves [x]Qa4(btm){*}", [], returncode=1)

    def test_019_countmoves_08_ta_11_right_target_06_rep_09_force_one_up(self):
        self.verify("countmoves [x]Qa4(btm){+}", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_01_zero_up(self):
        self.verify("countmoves e2[x]Qa4(btm)*", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_02_one_up(self):
        self.verify("countmoves e2[x]Qa4(btm)+", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_03_optional(self):
        self.verify("countmoves e2[x]Qa4(btm)?", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_04_exact(self):
        self.verify("countmoves e2[x]Qa4(btm){5}", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_05_range(self):
        self.verify("countmoves e2[x]Qa4(btm){3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_06_up_to(self):
        self.verify("countmoves e2[x]Qa4(btm){,5}", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_07_and_over(self):
        self.verify("countmoves e2[x]Qa4(btm){3,}", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2[x]Qa4(btm){*}", [], returncode=1)

    def test_019_countmoves_08_ta_12_lr_target_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2[x]Qa4(btm){+}", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves [x]=q(btm)*", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves [x]=q(btm)+", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves [x]=q(btm)?", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves [x]=q(btm){5}", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_05_range(self):
        self.verify("countmoves [x]=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves [x]=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves [x]=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_08_force_zero_up(self):
        self.verify("countmoves [x]=q(btm){*}", [], returncode=1)

    def test_019_countmoves_08_ta_13_prom_targ_06_rep_09_force_one_up(self):
        self.verify("countmoves [x]=q(btm){+}", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves e2[x]=q(btm)*", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves e2[x]=q(btm)+", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves e2[x]=q(btm)?", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves e2[x]=q(btm){5}", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_05_range(self):
        self.verify("countmoves e2[x]=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves e2[x]=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves e2[x]=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2[x]=q(btm){*}", [], returncode=1)

    def test_019_countmoves_08_ta_14_l_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2[x]=q(btm){+}", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves [x]Qa4=q(btm)*", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves [x]Qa4=q(btm)+", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves [x]Qa4=q(btm)?", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves [x]Qa4=q(btm){5}", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_05_range(self):
        self.verify("countmoves [x]Qa4=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves [x]Qa4=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves [x]Qa4=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves [x]Qa4=q(btm){*}", [], returncode=1)

    def test_019_countmoves_08_ta_15_r_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves [x]Qa4=q(btm){+}", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves e2[x]Qa4=q(btm)*", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves e2[x]Qa4=q(btm)+", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves e2[x]Qa4=q(btm)?", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves e2[x]Qa4=q(btm){5}", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_05_range(self):
        self.verify("countmoves e2[x]Qa4=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves e2[x]Qa4=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves e2[x]Qa4=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2[x]Qa4=q(btm){*}", [], returncode=1)

    def test_019_countmoves_08_ta_16_lr_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2[x]Qa4=q(btm){+}", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_01_zero_up(self):
        self.verify("countmoves ×*", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_02_one_up(self):
        self.verify("countmoves ×+", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_03_optional(self):
        self.verify("countmoves ×?", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_04_exact(self):
        self.verify("countmoves ×{5}", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_05_range(self):
        self.verify("countmoves ×{3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_06_up_to(self):
        self.verify("countmoves ×{,5}", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_07_and_over(self):
        self.verify("countmoves ×{3,}", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_08_force_zero_up(self):
        self.verify("countmoves ×{*}", [], returncode=1)

    def test_019_countmoves_09_tu_01_plain_06_rep_09_force_one_up(self):
        self.verify("countmoves ×{+}", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_01_zero_up(self):
        self.verify("countmoves e2×*", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_02_one_up(self):
        self.verify("countmoves e2×+", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_03_optional(self):
        self.verify("countmoves e2×?", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_04_exact(self):
        self.verify("countmoves e2×{5}", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_05_range(self):
        self.verify("countmoves e2×{3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_06_up_to(self):
        self.verify("countmoves e2×{,5}", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_07_and_over(self):
        self.verify("countmoves e2×{3,}", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2×{*}", [], returncode=1)

    def test_019_countmoves_09_tu_02_left_06_rep_09_force_one_up(self):
        self.verify("countmoves e2×{+}", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_01_zero_up(self):
        self.verify("countmoves ×Qa4*", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_02_one_up(self):
        self.verify("countmoves ×Qa4+", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_03_optional(self):
        self.verify("countmoves ×Qa4?", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_04_exact(self):
        self.verify("countmoves ×Qa4{5}", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_05_range(self):
        self.verify("countmoves ×Qa4{3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_06_up_to(self):
        self.verify("countmoves ×Qa4{,5}", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_07_and_over(self):
        self.verify("countmoves ×Qa4{3,}", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_08_force_zero_up(self):
        self.verify("countmoves ×Qa4{*}", [], returncode=1)

    def test_019_countmoves_09_tu_03_right_06_rep_09_force_one_up(self):
        self.verify("countmoves ×Qa4{+}", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_01_zero_up(self):
        self.verify("countmoves e2×Qa4*", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_02_one_up(self):
        self.verify("countmoves e2×Qa4+", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_03_optional(self):
        self.verify("countmoves e2×Qa4?", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_04_exact(self):
        self.verify("countmoves e2×Qa4{5}", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_05_range(self):
        self.verify("countmoves e2×Qa4{3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_06_up_to(self):
        self.verify("countmoves e2×Qa4{,5}", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_07_and_over(self):
        self.verify("countmoves e2×Qa4{3,}", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2×Qa4{*}", [], returncode=1)

    def test_019_countmoves_09_tu_04_lr_06_rep_09_force_one_up(self):
        self.verify("countmoves e2×Qa4{+}", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_01_zero_up(self):
        self.verify("countmoves ×=q*", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_02_one_up(self):
        self.verify("countmoves ×=q+", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_03_optional(self):
        self.verify("countmoves ×=q?", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_04_exact(self):
        self.verify("countmoves ×=q{5}", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_05_range(self):
        self.verify("countmoves ×=q{3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_06_up_to(self):
        self.verify("countmoves ×=q{,5}", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_07_and_over(self):
        self.verify("countmoves ×=q{3,}", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves ×=q{*}", [], returncode=1)

    def test_019_countmoves_09_tu_05_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves ×=q{+}", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_01_zero_up(self):
        self.verify("countmoves e2×=q*", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_02_one_up(self):
        self.verify("countmoves e2×=q+", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_03_optional(self):
        self.verify("countmoves e2×=q?", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_04_exact(self):
        self.verify("countmoves e2×=q{5}", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_05_range(self):
        self.verify("countmoves e2×=q{3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_06_up_to(self):
        self.verify("countmoves e2×=q{,5}", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_07_and_over(self):
        self.verify("countmoves e2×=q{3,}", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2×=q{*}", [], returncode=1)

    def test_019_countmoves_09_tu_06_left_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves e2×=q{+}", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_01_zero_up(self):
        self.verify("countmoves ×Qa4=q*", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_02_one_up(self):
        self.verify("countmoves ×Qa4=q+", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_03_optional(self):
        self.verify("countmoves ×Qa4=q?", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_04_exact(self):
        self.verify("countmoves ×Qa4=q{5}", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_05_range(self):
        self.verify("countmoves ×Qa4=q{3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_06_up_to(self):
        self.verify("countmoves ×Qa4=q{,5}", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_07_and_over(self):
        self.verify("countmoves ×Qa4=q{3,}", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_08_force_zero_up(self):
        self.verify("countmoves ×Qa4=q{*}", [], returncode=1)

    def test_019_countmoves_09_tu_07_right_prom_06_rep_09_force_one_up(self):
        self.verify("countmoves ×Qa4=q{+}", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_01_zero_up(self):
        self.verify("countmoves e2×Qa4=q*", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_02_one_up(self):
        self.verify("countmoves e2×Qa4=q+", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_03_optional(self):
        self.verify("countmoves e2×Qa4=q?", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_04_exact(self):
        self.verify("countmoves e2×Qa4=q{5}", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_05_range(self):
        self.verify("countmoves e2×Qa4=q{3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_06_up_to(self):
        self.verify("countmoves e2×Qa4=q{,5}", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_07_and_over(self):
        self.verify("countmoves e2×Qa4=q{3,}", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2×Qa4=q{*}", [], returncode=1)

    def test_019_countmoves_09_tu_08_lr_prom_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2×Qa4=q{+}", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_01_zero_up(self):
        self.verify("countmoves ×(btm)*", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_02_one_up(self):
        self.verify("countmoves ×(btm)+", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_03_optional(self):
        self.verify("countmoves ×(btm)?", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_04_exact(self):
        self.verify("countmoves ×(btm){5}", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_05_range(self):
        self.verify("countmoves ×(btm){3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_06_up_to(self):
        self.verify("countmoves ×(btm){,5}", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_07_and_over(self):
        self.verify("countmoves ×(btm){3,}", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_08_force_zero_up(self):
        self.verify("countmoves ×(btm){*}", [], returncode=1)

    def test_019_countmoves_09_tu_09_target_06_rep_09_force_one_up(self):
        self.verify("countmoves ×(btm){+}", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_01_zero_up(self):
        self.verify("countmoves e2×(btm)*", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_02_one_up(self):
        self.verify("countmoves e2×(btm)+", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_03_optional(self):
        self.verify("countmoves e2×(btm)?", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_04_exact(self):
        self.verify("countmoves e2×(btm){5}", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_05_range(self):
        self.verify("countmoves e2×(btm){3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_06_up_to(self):
        self.verify("countmoves e2×(btm){,5}", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_07_and_over(self):
        self.verify("countmoves e2×(btm){3,}", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_08_force_zero_up(self):
        self.verify("countmoves e2×(btm){*}", [], returncode=1)

    def test_019_countmoves_09_tu_10_left_target_06_rep_09_force_one_up(self):
        self.verify("countmoves e2×(btm){+}", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_01_zero_up(self):
        self.verify("countmoves ×Qa4(btm)*", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_02_one_up(self):
        self.verify("countmoves ×Qa4(btm)+", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_03_optional(self):
        self.verify("countmoves ×Qa4(btm)?", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_04_exact(self):
        self.verify("countmoves ×Qa4(btm){5}", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_05_range(self):
        self.verify("countmoves ×Qa4(btm){3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_06_up_to(self):
        self.verify("countmoves ×Qa4(btm){,5}", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_07_and_over(self):
        self.verify("countmoves ×Qa4(btm){3,}", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves ×Qa4(btm){*}", [], returncode=1)

    def test_019_countmoves_09_tu_11_right_target_06_rep_09_force_one_up(self):
        self.verify("countmoves ×Qa4(btm){+}", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_01_zero_up(self):
        self.verify("countmoves e2×Qa4(btm)*", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_02_one_up(self):
        self.verify("countmoves e2×Qa4(btm)+", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_03_optional(self):
        self.verify("countmoves e2×Qa4(btm)?", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_04_exact(self):
        self.verify("countmoves e2×Qa4(btm){5}", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_05_range(self):
        self.verify("countmoves e2×Qa4(btm){3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_06_up_to(self):
        self.verify("countmoves e2×Qa4(btm){,5}", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_07_and_over(self):
        self.verify("countmoves e2×Qa4(btm){3,}", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2×Qa4(btm){*}", [], returncode=1)

    def test_019_countmoves_09_tu_12_lr_target_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2×Qa4(btm){+}", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves ×=q(btm)*", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves ×=q(btm)+", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves ×=q(btm)?", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves ×=q(btm){5}", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_05_range(self):
        self.verify("countmoves ×=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves ×=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves ×=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_08_force_zero_up(self):
        self.verify("countmoves ×=q(btm){*}", [], returncode=1)

    def test_019_countmoves_09_tu_13_prom_targ_06_rep_09_force_one_up(self):
        self.verify("countmoves ×=q(btm){+}", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves e2×=q(btm)*", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves e2×=q(btm)+", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves e2×=q(btm)?", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves e2×=q(btm){5}", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_05_range(self):
        self.verify("countmoves e2×=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves e2×=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves e2×=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2×=q(btm){*}", [], returncode=1)

    def test_019_countmoves_09_tu_14_l_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2×=q(btm){+}", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves ×Qa4=q(btm)*", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves ×Qa4=q(btm)+", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves ×Qa4=q(btm)?", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves ×Qa4=q(btm){5}", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_05_range(self):
        self.verify("countmoves ×Qa4=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves ×Qa4=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves ×Qa4=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves ×Qa4=q(btm){*}", [], returncode=1)

    def test_019_countmoves_09_tu_15_r_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves ×Qa4=q(btm){+}", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_01_zero_up(self):
        self.verify("countmoves e2×Qa4=q(btm)*", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_02_one_up(self):
        self.verify("countmoves e2×Qa4=q(btm)+", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_03_optional(self):
        self.verify("countmoves e2×Qa4=q(btm)?", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_04_exact(self):
        self.verify("countmoves e2×Qa4=q(btm){5}", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_05_range(self):
        self.verify("countmoves e2×Qa4=q(btm){3,5}", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_06_up_to(self):
        self.verify("countmoves e2×Qa4=q(btm){,5}", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_07_and_over(self):
        self.verify("countmoves e2×Qa4=q(btm){3,}", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("countmoves e2×Qa4=q(btm){*}", [], returncode=1)

    def test_019_countmoves_09_tu_16_lr_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("countmoves e2×Qa4=q(btm){+}", [], returncode=1)


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterCountMoves))
