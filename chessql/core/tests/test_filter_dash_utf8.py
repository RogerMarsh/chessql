# test_filter_dash_utf8.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for '――' filter (called 'dash').

This is "\u2015\u2015" and is equivalent to '――'.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes


class FilterDashUTF8(verify.Verify):

    def test_148_dash_utf8_01_plain_01_bare(self):
        self.verify(
            "――",
            [(3, "DashII"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test_148_dash_utf8_01_plain_02_parentheses_01(self):
        self.verify(
            "(――)",
            [
                (3, "ParenthesisLeft"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_01_plain_02_parentheses_02(self):
        self.verify(
            "( ――)",
            [
                (3, "ParenthesisLeft"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_01_plain_02_parentheses_03(self):
        self.verify(
            "(―― )",
            [
                (3, "ParenthesisLeft"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_01_plain_02_parentheses_04(self):
        self.verify(
            "( ―― )",
            [
                (3, "ParenthesisLeft"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_01_plain_03_braces_01(self):
        self.verify(
            "{――}",
            [
                (3, "BraceLeft"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_01_plain_03_braces_02(self):
        self.verify(
            "{ ――}",
            [
                (3, "BraceLeft"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_01_plain_03_braces_03(self):
        self.verify(
            "{―― }",
            [
                (3, "BraceLeft"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_01_plain_03_braces_04(self):
        self.verify(
            "{ ―― }",
            [
                (3, "BraceLeft"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_01_plain_04_target_01_btm(self):
        self.verify(
            "――(btm)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_01_plain_04_target_02_o_o(self):
        self.verify(
            "――(o-o)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "OO"),
            ],
        )

    def test_148_dash_utf8_01_plain_04_target_03_o_o_o(self):
        self.verify(
            "――(o-o-o)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "OOO"),
            ],
        )

    def test_148_dash_utf8_01_plain_04_target_04_castle(self):
        self.verify(
            "――(castle)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "Castle"),
            ],
        )

    def test_148_dash_utf8_01_plain_04_target_05_enpassant(self):
        self.verify(
            "――(enpassant)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "EnPassant"),
            ],
        )

    def test_148_dash_utf8_01_plain_04_target_06_o_o_set(self):
        self.verify(
            "――(o-o to)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "OO"),
                (5, "To"),
            ],
        )

    def test_148_dash_utf8_01_plain_04_target_07_set_o_o(self):
        self.verify(
            "――(Rc4 o-o)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "PieceDesignator"),
                (5, "OO"),
            ],
        )

    def test_148_dash_utf8_01_plain_05_brace_repeat_05_two_elements_03(self):
        self.verify("――{2 4}", [], returncode=1)

    def test_148_dash_utf8_01_plain_05_brace_repeat_05_two_elements_04(self):
        self.verify(
            "―― {2 4}",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (3, "BraceLeft"),
                (4, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_01_plain_06_repeat_01_zero_up(self):
        self.verify("――*", [], returncode=1)

    def test_148_dash_utf8_01_plain_06_repeat_02_one_up(self):
        self.verify("――+", [], returncode=1)

    def test_148_dash_utf8_01_plain_06_repeat_03_optional(self):
        self.verify("――?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_01_plain_06_repeat_04_exact(self):
        self.verify("――{5}", [], returncode=1)

    def test_148_dash_utf8_01_plain_06_repeat_05_range(self):
        self.verify("――{3,5}", [], returncode=1)

    def test_148_dash_utf8_01_plain_06_repeat_06_up_to(self):
        self.verify("――{,5}", [], returncode=1)

    def test_148_dash_utf8_01_plain_06_repeat_07_and_over(self):
        self.verify("――{3,}", [], returncode=1)

    def test_148_dash_utf8_01_plain_06_repeat_08_force_zero_up(self):
        self.verify("――{*}", [], returncode=1)

    def test_148_dash_utf8_01_plain_06_repeat_09_force_one_up(self):
        self.verify("――{+}", [], returncode=1)

    def test_148_dash_utf8_02_left_01_plain(self):
        self.verify(
            "e2――",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_02_left_02_compound_set(self):
        self.verify(
            "{2 e2}――",
            [
                (3, "DashLI"),
                (4, "BraceLeft"),
                (5, "Integer"),
                (5, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_02_left_03_compound_not_set(self):
        self.verify("{e2 2}――", [], returncode=1)

    def test_148_dash_utf8_02_left_06_repeat_01_zero_up(self):
        self.verify("e2――*", [], returncode=1)

    def test_148_dash_utf8_02_left_06_repeat_02_one_up(self):
        self.verify("e2――+", [], returncode=1)

    def test_148_dash_utf8_02_left_06_repeat_03_optional(self):
        self.verify("e2――?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_02_left_06_repeat_04_exact(self):
        self.verify("e2――{5}", [], returncode=1)

    def test_148_dash_utf8_02_left_06_repeat_05_range(self):
        self.verify("e2――{3,5}", [], returncode=1)

    def test_148_dash_utf8_02_left_06_repeat_06_up_to(self):
        self.verify("e2――{,5}", [], returncode=1)

    def test_148_dash_utf8_02_left_06_repeat_07_and_over(self):
        self.verify("e2――{3,}", [], returncode=1)

    def test_148_dash_utf8_02_left_06_repeat_08_force_zero_up(self):
        self.verify("e2――{*}", [], returncode=1)

    def test_148_dash_utf8_02_left_06_repeat_09_force_one_up(self):
        self.verify("e2――{+}", [], returncode=1)

    def test_148_dash_utf8_03_right_01_plain(self):
        self.verify(
            "――Qa4",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_03_right_02_compound_set(self):
        self.verify(
            "――{3 e4}",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "BraceLeft"),
                (5, "Integer"),
                (5, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_03_right_03_compound_not_set(self):
        self.verify("――{e4 3}", [], returncode=1)

    def test_148_dash_utf8_03_right_06_repeat_01_zero_up(self):
        self.verify("――Qa4*", [], returncode=1)

    def test_148_dash_utf8_03_right_06_repeat_02_one_up(self):
        self.verify("――Qa4+", [], returncode=1)

    def test_148_dash_utf8_03_right_06_repeat_03_optional(self):
        self.verify("――Qa4?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_03_right_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "――Qa4{5}",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_03_right_06_repeat_05_range(self):
        self.verify("――Qa4{3,5}", [], returncode=1)

    def test_148_dash_utf8_03_right_06_repeat_06_up_to(self):
        self.verify("――Qa4{,5}", [], returncode=1)

    def test_148_dash_utf8_03_right_06_repeat_07_and_over(self):
        self.verify("――Qa4{3,}", [], returncode=1)

    def test_148_dash_utf8_03_right_06_repeat_08_force_zero_up(self):
        self.verify("――Qa4{*}", [], returncode=1)

    def test_148_dash_utf8_03_right_06_repeat_09_force_one_up(self):
        self.verify("――Qa4{+}", [], returncode=1)

    def test_148_dash_utf8_04_left_right_01_plain(self):
        self.verify(
            "r――Qa4",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_04_left_right_02_compound_set(self):
        self.verify(
            "{2 e2}――{3 e4}",
            [
                (3, "DashLR"),
                (4, "BraceLeft"),
                (5, "Integer"),
                (5, "PieceDesignator"),
                (4, "BraceLeft"),
                (5, "Integer"),
                (5, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_04_left_right_03_compound_not_set(self):
        self.verify("{e2 2}――{e4 3}", [], returncode=1)

    def test_148_dash_utf8_04_left_right_06_repeat_01_zero_up(self):
        self.verify("e2――Qa4*", [], returncode=1)

    def test_148_dash_utf8_04_left_right_06_repeat_02_one_up(self):
        self.verify("e2――Qa4+", [], returncode=1)

    def test_148_dash_utf8_04_left_right_06_repeat_03_optional(self):
        self.verify("e2――Qa4?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_04_left_right_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2――Qa4{5}",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_04_left_right_06_repeat_05_range(self):
        self.verify("e2――Qa4{3,5}", [], returncode=1)

    def test_148_dash_utf8_04_left_right_06_repeat_06_up_to(self):
        self.verify("e2――Qa4{,5}", [], returncode=1)

    def test_148_dash_utf8_04_left_right_06_repeat_07_and_over(self):
        self.verify("e2――Qa4{3,}", [], returncode=1)

    def test_148_dash_utf8_04_left_right_06_repeat_08_force_zero_up(self):
        self.verify("e2――Qa4{*}", [], returncode=1)

    def test_148_dash_utf8_04_left_right_06_repeat_09_force_one_up(self):
        self.verify("e2――Qa4{+}", [], returncode=1)

    def test_148_dash_utf8_05_promote_01(self):
        self.verify(
            "――=q",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_05_promote_02(self):
        self.verify("――=qa5", [], returncode=1)

    def test_148_dash_utf8_05_promote_03(self):
        self.verify("――=check", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_01_plus(self):
        self.verify("2+――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_02_minus_01_no_space(self):
        self.verify("2――-=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_02_minus_02_space(self):
        self.verify("2- ――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_03_multiply(self):
        self.verify("2*――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_04_divide(self):
        self.verify("2/――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_05_modulus_01_no_space(self):
        self.verify("2%――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_05_modulus_02_space(self):
        self.verify("2% ――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_06_equals(self):
        self.verify("2==――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_07_gt(self):
        self.verify("2>――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_08_ge(self):
        self.verify("2>=――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_09_lt_01_no_space(self):
        self.verify("2<――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_09_lt_02_space(self):
        self.verify("2< ――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_10_le(self):
        self.verify("2<=――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_11_ne(self):
        self.verify("2!=――=q", [], returncode=1)

    def test_148_dash_utf8_05_promote_04_lhs_12_and(self):
        self.verify(
            "2 and ――=q",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_05_promote_04_lhs_13_or(self):
        self.verify(
            "2 or ――=q",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_05_promote_05_rhs_01_plus(self):
        self.verify("――=q+2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_02_minus(self):
        self.verify(
            "――=q-2",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_05_promote_05_rhs_03_multiply(self):
        self.verify("――=q*2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_04_divide(self):
        self.verify("――=q/2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_05_modulus_01_no_space(self):
        self.verify("――=q%2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_05_modulus_02_space(self):
        self.verify("――=q %2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_06_equals(self):
        self.verify("――=q==2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_07_gt(self):
        self.verify("――=q>2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_08_ge(self):
        self.verify("――=q>=2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_09_lt_01_no_space(self):
        self.verify("――=q<2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_09_lt_02_space(self):
        self.verify("――=q <2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_10_le(self):
        self.verify("――=q<=2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_11_ne(self):
        self.verify("――=q!=2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_12_and_01_plain(self):
        self.verify("――=q and 2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "(――=q) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_05_promote_05_rhs_13_or_01_plain(self):
        self.verify("――=q or 2", [], returncode=1)

    def test_148_dash_utf8_05_promote_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "(――=q) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_05_promote_06_repeat_01_zero_up(self):
        self.verify("――=q*", [], returncode=1)

    def test_148_dash_utf8_05_promote_06_repeat_02_one_up(self):
        self.verify("――=q+", [], returncode=1)

    def test_148_dash_utf8_05_promote_06_repeat_03_optional(self):
        self.verify("――=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_05_promote_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "――=q{5}",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_05_promote_06_repeat_05_range(self):
        self.verify("――=q{3,5}", [], returncode=1)

    def test_148_dash_utf8_05_promote_06_repeat_06_up_to(self):
        self.verify("――=q{,5}", [], returncode=1)

    def test_148_dash_utf8_05_promote_06_repeat_07_and_over(self):
        self.verify("――=q{3,}", [], returncode=1)

    def test_148_dash_utf8_05_promote_06_repeat_08_force_zero_up(self):
        self.verify("――=q{*}", [], returncode=1)

    def test_148_dash_utf8_05_promote_06_repeat_09_force_one_up(self):
        self.verify("――=q{+}", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_01(self):
        self.verify(
            "e2――=b",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_06_left_promote_02(self):
        self.verify("e2――=bc6", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_03(self):
        self.verify("e2――=check", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_01_plus(self):
        self.verify("2+e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_02_minus_01_no_space(self):
        self.verify("2-e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_02_minus_02_space(self):
        self.verify("2- e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_03_multiply(self):
        self.verify("2*e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_04_divide(self):
        self.verify("2/e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_05_mod_01_no_space(self):
        self.verify("2%e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_05_mod_02_space(self):
        self.verify("2% e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_06_equals(self):
        self.verify("2==e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_07_gt(self):
        self.verify("2>e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_08_ge(self):
        self.verify("2>=e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_09_lt_01_no_space(self):
        self.verify("2<e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_09_lt_02_space(self):
        self.verify("2< e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_10_le(self):
        self.verify("2<=e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_11_ne(self):
        self.verify("2!=e2――=q", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_04_lhs_12_and(self):
        self.verify(
            "2 and e2――=q",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_06_left_promote_04_lhs_13_or(self):
        self.verify(
            "2 or e2――=q",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_06_left_promote_05_rhs_01_plus(self):
        self.verify("e2――=q+2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_02_minus(self):
        self.verify(
            "e2――=q-2",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_06_left_promote_05_rhs_03_multiply(self):
        self.verify("e2――=q*2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_04_divide(self):
        self.verify("e2――=q/2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_05_mod_01_no_space(self):
        self.verify("e2――=q%2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_05_mod_02_space(self):
        self.verify("e2――=q %2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_06_equals(self):
        self.verify("e2――=q==2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_07_gt(self):
        self.verify("e2――=q>2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_08_ge(self):
        self.verify("e2――=q>=2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_09_lt_01_no_space(self):
        self.verify("e2――=q<2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_09_lt_02_space(self):
        self.verify("e2――=q <2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_10_le(self):
        self.verify("e2――=q<=2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_11_ne(self):
        self.verify("e2――=q!=2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_12_and_01_plain(self):
        self.verify("e2――=q and 2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "(e2――=q) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_06_left_promote_05_rhs_13_or_01_plain(self):
        self.verify("e2――=q or 2", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "(e2――=q) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_06_left_promote_06_repeat_01_zero_up(self):
        self.verify("e2――=q*", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_06_repeat_02_one_up(self):
        self.verify("e2――=q+", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_06_repeat_03_optional(self):
        self.verify("e2――=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_06_left_promote_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2――=q{5}",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_06_left_promote_06_repeat_05_range(self):
        self.verify("e2――=q{3,5}", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_06_repeat_06_up_to(self):
        self.verify("e2――=q{,5}", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_06_repeat_07_and_over(self):
        self.verify("e2――=q{3,}", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_06_repeat_08_force_zero_up(self):
        self.verify("e2――=q{*}", [], returncode=1)

    def test_148_dash_utf8_06_left_promote_06_repeat_09_force_one_up(self):
        self.verify("e2――=q{+}", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_01(self):
        self.verify(
            "――Qa4=N",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_07_right_promote_02(self):
        self.verify("――Qa4=bc6", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_03(self):
        self.verify("――Qa4=check", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_01_plus(self):
        self.verify("2+――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_02_minus_01_no_space(self):
        self.verify("2――-Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_02_minus_02_space(self):
        self.verify("2- ――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_03_multiply(self):
        self.verify("2*――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_04_divide(self):
        self.verify("2/――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_05_mod_01_no_space(self):
        self.verify("2%――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_05_mod_02_space(self):
        self.verify("2% ――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_06_equals(self):
        self.verify("2==――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_07_gt(self):
        self.verify("2>――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_08_ge(self):
        self.verify("2>=――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_09_lt_01_no_space(self):
        self.verify("2<――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_09_lt_02_space(self):
        self.verify("2< ――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_10_le(self):
        self.verify("2<=――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_11_ne(self):
        self.verify("2!=――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_04_lhs_12_and(self):
        self.verify(
            "2 and ――Qa4=q",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_07_right_promote_04_lhs_13_or(self):
        self.verify(
            "2 or ――Qa4=q",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_07_right_promote_05_rhs_01_plus(self):
        self.verify("――Qa4=q+2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_02_minus(self):
        self.verify(
            "――Qa4=q-2",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_07_right_promote_05_rhs_03_multiply(self):
        self.verify("――Qa4=q*2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_04_divide(self):
        self.verify("――Qa4=q/2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_05_mod_01_no_space(self):
        self.verify("――Qa4=q%2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_05_mod_02_space(self):
        self.verify("――Qa4=q %2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_06_equals(self):
        self.verify("――Qa4=q==2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_07_gt(self):
        self.verify("――Qa4=q>2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_08_ge(self):
        self.verify("――Qa4=q>=2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_09_lt_01_no_space(self):
        self.verify("――Qa4=q<2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_09_lt_02_space(self):
        self.verify("――Qa4=q <2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_10_le(self):
        self.verify("――Qa4=q<=2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_11_ne(self):
        self.verify("――Qa4=q!=2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_12_and_01_plain(self):
        self.verify("――Qa4=q and 2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "(――Qa4=q) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_07_right_promote_05_rhs_13_or_01_plain(self):
        self.verify("――Qa4=q or 2", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "(――Qa4=q) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_07_right_promote_06_repeat_01_zero_up(self):
        self.verify("――Qa4=q*", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_06_repeat_02_one_up(self):
        self.verify("――Qa4=q+", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_06_repeat_03_optional(self):
        self.verify("――Qa4=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_07_right_promote_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "――Qa4=q{5}",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_07_right_promote_06_repeat_05_range(self):
        self.verify("――Qa4=q{3,5}", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_06_repeat_06_up_to(self):
        self.verify("――Qa4=q{,5}", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_06_repeat_07_and_over(self):
        self.verify("――Qa4=q{3,}", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_06_repeat_08_force_zero_up(self):
        self.verify("――Qa4=q{*}", [], returncode=1)

    def test_148_dash_utf8_07_right_promote_06_repeat_09_force_one_up(self):
        self.verify("――Qa4=q{+}", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_01(self):
        self.verify(
            "r――Qa4=R",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_08_left_right_promote_02(self):
        self.verify("r――Qa4=bc6", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_03(self):
        self.verify("r――Qa4=check", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_01_plus(self):
        self.verify("2+e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_02_minus_02_space(
        self,
    ):
        self.verify("2- e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_03_multiply(self):
        self.verify("2*e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_04_divide(self):
        self.verify("2/e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_05_mod_02_space(self):
        self.verify("2% e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_06_equals(self):
        self.verify("2==e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_07_gt(self):
        self.verify("2>e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_08_ge(self):
        self.verify("2>=e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_09_lt_01_no_space(
        self,
    ):
        self.verify("2<e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_09_lt_02_space(self):
        self.verify("2< e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_10_le(self):
        self.verify("2<=e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_11_ne(self):
        self.verify("2!=e2――Qa4=q", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_04_lhs_12_and(self):
        self.verify(
            "2 and e2――Qa4=q",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_08_left_right_promote_04_lhs_13_or(self):
        self.verify(
            "2 or e2――Qa4=q",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_08_left_right_promote_05_rhs_01_plus(self):
        self.verify("e2――Qa4=q+2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_02_minus(self):
        self.verify(
            "e2――Qa4=q-2",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_08_left_right_promote_05_rhs_03_multiply(self):
        self.verify("e2――Qa4=q*2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_04_divide(self):
        self.verify("e2――Qa4=q/2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("e2――Qa4=q%2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_05_mod_02_space(self):
        self.verify("e2――Qa4=q %2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_06_equals(self):
        self.verify("e2――Qa4=q==2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_07_gt(self):
        self.verify("e2――Qa4=q>2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_08_ge(self):
        self.verify("e2――Qa4=q>=2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_09_lt_01_no_space(
        self,
    ):
        self.verify("e2――Qa4=q<2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_09_lt_02_space(self):
        self.verify("e2――Qa4=q <2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_10_le(self):
        self.verify("e2――Qa4=q<=2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_11_ne(self):
        self.verify("e2――Qa4=q!=2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_12_and_01_plain(self):
        self.verify("e2――Qa4=q and 2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(e2――Qa4=q) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_08_left_right_promote_05_rhs_13_or_01_plain(self):
        self.verify("e2――Qa4=q or 2", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(e2――Qa4=q) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_08_left_right_promote_06_repeat_01_zero_up(self):
        self.verify("e2――Qa4=q*", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_06_repeat_02_one_up(self):
        self.verify("e2――Qa4=q+", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_06_repeat_03_optional(self):
        self.verify("e2――Qa4=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_08_left_right_promote_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2――Qa4=q{5}",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_08_left_right_promote_06_repeat_05_range(self):
        self.verify("e2――Qa4=q{3,5}", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_06_repeat_06_up_to(self):
        self.verify("e2――Qa4=q{,5}", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_06_repeat_07_and_over(self):
        self.verify("e2――Qa4=q{3,}", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("e2――Qa4=q{*}", [], returncode=1)

    def test_148_dash_utf8_08_left_right_promote_06_repeat_09_force_one_up(
        self,
    ):
        self.verify("e2――Qa4=q{+}", [], returncode=1)

    def test_148_dash_utf8_09_target_01_plain(self):
        self.verify(
            "――(btm)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_09_target_04_lhs_01_plus(self):
        self.verify("2+――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_02_minus_01_no_space(self):
        self.verify("2――-(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_02_minus_02_space(self):
        self.verify("2- ――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_03_multiply(self):
        self.verify("2*――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_04_divide(self):
        self.verify("2/――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_05_mod_01_no_space(self):
        self.verify("2%――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_05_mod_02_space(self):
        self.verify("2% ――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_06_equals(self):
        self.verify("2==――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_07_gt(self):
        self.verify("2>――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_08_ge(self):
        self.verify("2>=――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_09_lt_02_space(self):
        self.verify("2< ――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_10_le(self):
        self.verify("2<=――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_11_ne(self):
        self.verify("2!=――(btm)", [], returncode=1)

    def test_148_dash_utf8_09_target_04_lhs_12_and(self):
        self.verify(
            "2 and ――(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_09_target_04_lhs_13_or(self):
        self.verify(
            "2 or ――(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_09_target_05_rhs_01_plus(self):
        self.verify("――(btm)+2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_02_minus(self):
        self.verify(
            "――(btm)-2",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_09_target_05_rhs_03_multiply(self):
        self.verify("――(btm)*2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_04_divide(self):
        self.verify("――(btm)/2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_05_mod_01_no_space(self):
        self.verify("――(btm)%2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_05_mod_02_space(self):
        self.verify("――(btm) %2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_06_equals(self):
        self.verify("――(btm)==2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_07_gt(self):
        self.verify("――(btm)>2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_08_ge(self):
        self.verify("――(btm)>=2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_09_lt_01_no_space(self):
        self.verify("――(btm)<2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_09_lt_02_space(self):
        self.verify("――(btm) <2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_10_le(self):
        self.verify("――(btm)<=2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_11_ne(self):
        self.verify("――(btm)!=2", [], returncode=1)

    def test_148_dash_utf8_09_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "――(btm) and 2",
            [
                (3, "And"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_09_target_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "(――(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_09_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "――(btm) or 2",
            [
                (3, "Or"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_09_target_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "(――(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_09_target_06_repeat_01_zero_up(self):
        self.verify("――(btm)*", [], returncode=1)

    def test_148_dash_utf8_09_target_06_repeat_02_one_up(self):
        self.verify("――(btm)+", [], returncode=1)

    def test_148_dash_utf8_09_target_06_repeat_03_optional(self):
        self.verify("――(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_09_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "――(btm){5}",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_09_target_06_repeat_05_range(self):
        self.verify("――(btm){3,5}", [], returncode=1)

    def test_148_dash_utf8_09_target_06_repeat_06_up_to(self):
        self.verify("――(btm){,5}", [], returncode=1)

    def test_148_dash_utf8_09_target_06_repeat_07_and_over(self):
        self.verify("――(btm){3,}", [], returncode=1)

    def test_148_dash_utf8_09_target_06_repeat_08_force_zero_up(self):
        self.verify("――(btm){*}", [], returncode=1)

    def test_148_dash_utf8_09_target_06_repeat_09_force_one_up(self):
        self.verify("――(btm){+}", [], returncode=1)

    def test_148_dash_utf8_10_left_target_01_plain(self):
        self.verify(
            "P――(btm)",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_10_left_target_04_lhs_01_plus(self):
        self.verify("2+e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_02_minus_01_no_space(self):
        self.verify("2-e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_02_minus_02_space(self):
        self.verify("2- e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_03_multiply(self):
        self.verify("2*e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_04_divide(self):
        self.verify("2/e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_05_mod_01_no_space(self):
        self.verify("2%e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_05_mod_02_space(self):
        self.verify("2% e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_06_equals(self):
        self.verify("2==e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_07_gt(self):
        self.verify("2>e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_08_ge(self):
        self.verify("2>=e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_09_lt_02_space(self):
        self.verify("2< e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_10_le(self):
        self.verify("2<=e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_11_ne(self):
        self.verify("2!=e2――(btm)", [], returncode=1)

    def test_148_dash_utf8_10_left_target_04_lhs_12_and(self):
        self.verify(
            "2 and e2――(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_10_left_target_04_lhs_13_or(self):
        self.verify(
            "2 or e2――(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_10_left_target_05_rhs_01_plus(self):
        self.verify("e2――(btm)+2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_02_minus(self):
        self.verify(
            "e2――(btm)-2",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_10_left_target_05_rhs_03_multiply(self):
        self.verify("e2――(btm)*2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_04_divide(self):
        self.verify("e2――(btm)/2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_05_mod_01_no_space(self):
        self.verify("e2――(btm)%2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_05_mod_02_space(self):
        self.verify("e2――(btm) %2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_06_equals(self):
        self.verify("e2――(btm)==2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_07_gt(self):
        self.verify("e2――(btm)>2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_08_ge(self):
        self.verify("e2――(btm)>=2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_09_lt_01_no_space(self):
        self.verify("e2――(btm)<2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_09_lt_02_space(self):
        self.verify("e2――(btm) <2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_10_le(self):
        self.verify("e2――(btm)<=2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_11_ne(self):
        self.verify("e2――(btm)!=2", [], returncode=1)

    def test_148_dash_utf8_10_left_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "e2――(btm) and 2",
            [
                (3, "And"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_10_left_target_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "(e2――(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_10_left_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "e2――(btm) or 2",
            [
                (3, "Or"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_10_left_target_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "(e2――(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_10_left_target_06_repeat_01_zero_up(self):
        self.verify("e2――(btm)*", [], returncode=1)

    def test_148_dash_utf8_10_left_target_06_repeat_02_one_up(self):
        self.verify("e2――(btm)+", [], returncode=1)

    def test_148_dash_utf8_10_left_target_06_repeat_03_optional(self):
        self.verify("e2――(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_10_left_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2――(btm){5}",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_10_left_target_06_repeat_05_range(self):
        self.verify("e2――(btm){3,5}", [], returncode=1)

    def test_148_dash_utf8_10_left_target_06_repeat_06_up_to(self):
        self.verify("e2――(btm){,5}", [], returncode=1)

    def test_148_dash_utf8_10_left_target_06_repeat_07_and_over(self):
        self.verify("e2――(btm){3,}", [], returncode=1)

    def test_148_dash_utf8_10_left_target_06_repeat_08_force_zero_up(self):
        self.verify("e2――(btm){*}", [], returncode=1)

    def test_148_dash_utf8_10_left_target_06_repeat_09_force_one_up(self):
        self.verify("e2――(btm){+}", [], returncode=1)

    def test_148_dash_utf8_11_right_target_01_plain(self):
        self.verify(
            "――N(btm)",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_11_right_target_04_lhs_01_plus(self):
        self.verify("2+――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_02_minus_01_no_space(self):
        self.verify("2――-Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_02_minus_02_space(self):
        self.verify("2- ――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_03_multiply(self):
        self.verify("2*――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_04_divide(self):
        self.verify("2/――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_05_mod_01_no_space(self):
        self.verify("2%――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_05_mod_02_space(self):
        self.verify("2% ――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_06_equals(self):
        self.verify("2==――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_07_gt(self):
        self.verify("2>――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_08_ge(self):
        self.verify("2>=――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_09_lt_02_space(self):
        self.verify("2< ――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_10_le(self):
        self.verify("2<=――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_11_ne(self):
        self.verify("2!=――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_11_right_target_04_lhs_12_and(self):
        self.verify(
            "2 and ――Qa4(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_11_right_target_04_lhs_13_or(self):
        self.verify(
            "2 or ――Qa4(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_11_right_target_05_rhs_01_plus(self):
        self.verify("――Qa4(btm)+2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_02_minus(self):
        self.verify(
            "――Qa4(btm)-2",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_11_right_target_05_rhs_03_multiply(self):
        self.verify("――Qa4(btm)*2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_04_divide(self):
        self.verify("――Qa4(btm)/2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_05_mod_01_no_space(self):
        self.verify("――Qa4(btm)%2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_05_mod_02_space(self):
        self.verify("――Qa4(btm) %2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_06_equals(self):
        self.verify("――Qa4(btm)==2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_07_gt(self):
        self.verify("――Qa4(btm)>2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_08_ge(self):
        self.verify("――Qa4(btm)>=2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_09_lt_01_no_space(self):
        self.verify("――Qa4(btm)<2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_09_lt_02_space(self):
        self.verify("――Qa4(btm) <2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_10_le(self):
        self.verify("――Qa4(btm)<=2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_11_ne(self):
        self.verify("――Qa4(btm)!=2", [], returncode=1)

    def test_148_dash_utf8_11_right_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "――Qa4(btm) and 2",
            [
                (3, "And"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_11_right_target_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "(――Qa4(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_11_right_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "――Qa4(btm) or 2",
            [
                (3, "Or"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_11_right_target_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "(――Qa4(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_11_right_target_06_repeat_01_zero_up(self):
        self.verify("――Qa4(btm)*", [], returncode=1)

    def test_148_dash_utf8_11_right_target_06_repeat_02_one_up(self):
        self.verify("――Qa4(btm)+", [], returncode=1)

    def test_148_dash_utf8_11_right_target_06_repeat_03_optional(self):
        self.verify("――Qa4(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_11_right_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "――Qa4(btm){5}",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_11_right_target_06_repeat_05_range(self):
        self.verify("――Qa4(btm){3,5}", [], returncode=1)

    def test_148_dash_utf8_11_right_target_06_repeat_06_up_to(self):
        self.verify("――Qa4(btm){,5}", [], returncode=1)

    def test_148_dash_utf8_11_right_target_06_repeat_07_and_over(self):
        self.verify("――Qa4(btm){3,}", [], returncode=1)

    def test_148_dash_utf8_11_right_target_06_repeat_08_force_zero_up(self):
        self.verify("――Qa4(btm){*}", [], returncode=1)

    def test_148_dash_utf8_11_right_target_06_repeat_09_force_one_up(self):
        self.verify("――Qa4(btm){+}", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_01_plain(self):
        self.verify(
            "r――N(btm)",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_04_lhs_01_plus(self):
        self.verify("2+e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_02_minus_02_space(
        self,
    ):
        self.verify("2- e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_03_multiply(self):
        self.verify("2*e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_04_divide(self):
        self.verify("2/e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_05_mod_02_space(self):
        self.verify("2% e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_06_equals(self):
        self.verify("2==e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_07_gt(self):
        self.verify("2>e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_08_ge(self):
        self.verify("2>=e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_09_lt_01_no_space(
        self,
    ):
        self.verify("2<e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_09_lt_02_space(self):
        self.verify("2< e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_10_le(self):
        self.verify("2<=e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_11_ne(self):
        self.verify("2!=e2――Qa4(btm)", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_04_lhs_12_and(self):
        self.verify(
            "2 and e2――Qa4(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_04_lhs_13_or(self):
        self.verify(
            "2 or e2――Qa4(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_05_rhs_01_plus(self):
        self.verify("e2――Qa4(btm)+2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_02_minus(self):
        self.verify(
            "e2――Qa4(btm)-2",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_05_rhs_03_multiply(self):
        self.verify("e2――Qa4(btm)*2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_04_divide(self):
        self.verify("e2――Qa4(btm)/2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("e2――Qa4(btm)%2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_05_mod_02_space(self):
        self.verify("e2――Qa4(btm) %2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_06_equals(self):
        self.verify("e2――Qa4(btm)==2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_07_gt(self):
        self.verify("e2――Qa4(btm)>2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_08_ge(self):
        self.verify("e2――Qa4(btm)>=2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_09_lt_01_no_space(
        self,
    ):
        self.verify("e2――Qa4(btm)<2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_09_lt_02_space(self):
        self.verify("e2――Qa4(btm) <2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_10_le(self):
        self.verify("e2――Qa4(btm)<=2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_11_ne(self):
        self.verify("e2――Qa4(btm)!=2", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "e2――Qa4(btm) and 2",
            [
                (3, "And"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(e2――Qa4(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "e2――Qa4(btm) or 2",
            [
                (3, "Or"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(e2――Qa4(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_06_repeat_01_zero_up(self):
        self.verify("e2――Qa4(btm)*", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_06_repeat_02_one_up(self):
        self.verify("e2――Qa4(btm)+", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_06_repeat_03_optional(self):
        self.verify("e2――Qa4(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_12_left_right_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2――Qa4(btm){5}",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_12_left_right_target_06_repeat_05_range(self):
        self.verify("e2――Qa4(btm){3,5}", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_06_repeat_06_up_to(self):
        self.verify("e2――Qa4(btm){,5}", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_06_repeat_07_and_over(self):
        self.verify("e2――Qa4(btm){3,}", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("e2――Qa4(btm){*}", [], returncode=1)

    def test_148_dash_utf8_12_left_right_target_06_repeat_09_force_one_up(
        self,
    ):
        self.verify("e2――Qa4(btm){+}", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_01_plain(self):
        self.verify(
            "――=Q(btm)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_04_lhs_01_plus(self):
        self.verify("2+――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2――-=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_02_minus_02_space(self):
        self.verify("2- ――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_03_multiply(self):
        self.verify("2*――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_04_divide(self):
        self.verify("2/――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_05_mod_01_no_space(self):
        self.verify("2%――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_05_mod_02_space(self):
        self.verify("2% ――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_06_equals(self):
        self.verify("2==――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_07_gt(self):
        self.verify("2>――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_08_ge(self):
        self.verify("2>=――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_09_lt_02_space(self):
        self.verify("2< ――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_10_le(self):
        self.verify("2<=――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_11_ne(self):
        self.verify("2!=――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_04_lhs_12_and(self):
        self.verify(
            "2 and ――=q(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_04_lhs_13_or(self):
        self.verify(
            "2 or ――=q(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_05_rhs_01_plus(self):
        self.verify("――=q(btm)+2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_02_minus(self):
        self.verify(
            "――=q(btm)-2",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_05_rhs_03_multiply(self):
        self.verify("――=q(btm)*2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_04_divide(self):
        self.verify("――=q(btm)/2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_05_mod_01_no_space(self):
        self.verify("――=q(btm)%2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_05_mod_02_space(self):
        self.verify("――=q(btm) %2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_06_equals(self):
        self.verify("――=q(btm)==2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_07_gt(self):
        self.verify("――=q(btm)>2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_08_ge(self):
        self.verify("――=q(btm)>=2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_09_lt_01_no_space(self):
        self.verify("――=q(btm)<2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_09_lt_02_space(self):
        self.verify("――=q(btm) <2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_10_le(self):
        self.verify("――=q(btm)<=2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_11_ne(self):
        self.verify("――=q(btm)!=2", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "――=q(btm) and 2",
            [
                (3, "And"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(――=q(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "――=q(btm) or 2",
            [
                (3, "Or"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(――=q(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_06_repeat_01_zero_up(self):
        self.verify("――=q(btm)*", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_06_repeat_02_one_up(self):
        self.verify("――=q(btm)+", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_06_repeat_03_optional(self):
        self.verify("――=q(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_13_promote_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "――=q(btm){5}",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_13_promote_target_06_repeat_05_range(self):
        self.verify("――=q(btm){3,5}", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_06_repeat_06_up_to(self):
        self.verify("――=q(btm){,5}", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_06_repeat_07_and_over(self):
        self.verify("――=q(btm){3,}", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_06_repeat_08_force_zero_up(self):
        self.verify("――=q(btm){*}", [], returncode=1)

    def test_148_dash_utf8_13_promote_target_06_repeat_09_force_one_up(self):
        self.verify("――=q(btm){+}", [], returncode=1)

    def test_148_dash_utf8_14_promote_left_target_01_plain(self):
        self.verify(
            "P――=Q(btm)",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_04_lhs_01_plus(self):
        self.verify("2+e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_02_minus_02_space(self):
        self.verify("2- e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_03_multiply(self):
        self.verify("2*e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_04_divide(self):
        self.verify("2/e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_05_mod_02_space(self):
        self.verify("2% e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_06_equals(self):
        self.verify("2==e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_07_gt(self):
        self.verify("2>e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_08_ge(self):
        self.verify("2>=e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_09_lt_02_space(self):
        self.verify("2< e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_10_le(self):
        self.verify("2<=e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_11_ne(self):
        self.verify("2!=e2――=q(btm)", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_04_lhs_12_and(self):
        self.verify(
            "2 and e2――=q(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_04_lhs_13_or(self):
        self.verify(
            "2 or e2――=q(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_05_rhs_01_plus(self):
        self.verify("e2――=q(btm)+2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_02_minus(self):
        self.verify(
            "e2――=q(btm)-2",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_05_rhs_03_multiply(self):
        self.verify("e2――=q(btm)*2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_04_divide(self):
        self.verify("e2――=q(btm)/2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("e2――=q(btm)%2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_05_mod_02_space(self):
        self.verify("e2――=q(btm) %2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_06_equals(self):
        self.verify("e2――=q(btm)==2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_07_gt(self):
        self.verify("e2――=q(btm)>2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_08_ge(self):
        self.verify("e2――=q(btm)>=2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_09_lt_01_no_space(self):
        self.verify("e2――=q(btm)<2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_09_lt_02_space(self):
        self.verify("e2――=q(btm) <2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_10_le(self):
        self.verify("e2――=q(btm)<=2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_11_ne(self):
        self.verify("e2――=q(btm)!=2", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "e2――=q(btm) and 2",
            [
                (3, "And"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(e2――=q(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "e2――=q(btm) or 2",
            [
                (3, "Or"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(e2――=q(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_06_repeat_01_zero_up(self):
        self.verify("e2――=q(btm)*", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_06_repeat_02_one_up(self):
        self.verify("e2――=q(btm)+", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_06_repeat_03_optional(self):
        self.verify("e2――=q(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_14_l_promote_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2――=q(btm){5}",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_14_l_promote_target_06_repeat_05_range(self):
        self.verify("e2――=q(btm){3,5}", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_06_repeat_06_up_to(self):
        self.verify("e2――=q(btm){,5}", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_06_repeat_07_and_over(self):
        self.verify("e2――=q(btm){3,}", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("e2――=q(btm){*}", [], returncode=1)

    def test_148_dash_utf8_14_l_promote_target_06_repeat_09_force_one_up(self):
        self.verify("e2――=q(btm){+}", [], returncode=1)

    def test_148_dash_utf8_15_promote_right_target_01_plain(self):
        self.verify(
            "――N=Q(btm)",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_04_lhs_01_plus(self):
        self.verify("2+――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2――-Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_02_minus_02_space(self):
        self.verify("2- ――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_03_multiply(self):
        self.verify("2*――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_04_divide(self):
        self.verify("2/――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_05_mod_02_space(self):
        self.verify("2% ――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_06_equals(self):
        self.verify("2==――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_07_gt(self):
        self.verify("2>――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_08_ge(self):
        self.verify("2>=――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_09_lt_02_space(self):
        self.verify("2< ――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_10_le(self):
        self.verify("2<=――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_11_ne(self):
        self.verify("2!=――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_04_lhs_12_and(self):
        self.verify(
            "2 and ――Qa4=q(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_04_lhs_13_or(self):
        self.verify(
            "2 or ――Qa4=q(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_05_rhs_01_plus(self):
        self.verify("――Qa4=q(btm)+2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_02_minus(self):
        self.verify(
            "――Qa4=q(btm)-2",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_05_rhs_03_multiply(self):
        self.verify("――Qa4=q(btm)*2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_04_divide(self):
        self.verify("――Qa4=q(btm)/2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("――Qa4=q(btm)%2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_05_mod_02_space(self):
        self.verify("――Qa4=q(btm) %2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_06_equals(self):
        self.verify("――Qa4=q(btm)==2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_07_gt(self):
        self.verify("――Qa4=q(btm)>2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_08_ge(self):
        self.verify("――Qa4=q(btm)>=2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_09_lt_01_no_space(self):
        self.verify("――Qa4=q(btm)<2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_09_lt_02_space(self):
        self.verify("――Qa4=q(btm) <2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_10_le(self):
        self.verify("――Qa4=q(btm)<=2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_11_ne(self):
        self.verify("――Qa4=q(btm)!=2", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "――Qa4=q(btm) and 2",
            [
                (3, "And"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(――Qa4=q(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "――Qa4=q(btm) or 2",
            [
                (3, "Or"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(――Qa4=q(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_06_repeat_01_zero_up(self):
        self.verify("――Qa4=q(btm)*", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_06_repeat_02_one_up(self):
        self.verify("――Qa4=q(btm)+", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_06_repeat_03_optional(self):
        self.verify("――Qa4=q(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_15_r_promote_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "――Qa4=q(btm){5}",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_15_r_promote_target_06_repeat_05_range(self):
        self.verify("――Qa4=q(btm){3,5}", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_06_repeat_06_up_to(self):
        self.verify("――Qa4=q(btm){,5}", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_06_repeat_07_and_over(self):
        self.verify("――Qa4=q(btm){3,}", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("――Qa4=q(btm){*}", [], returncode=1)

    def test_148_dash_utf8_15_r_promote_target_06_repeat_09_force_one_up(self):
        self.verify("――Qa4=q(btm){+}", [], returncode=1)

    def test_148_dash_utf8_16_promote_left_right_target_01_plain(self):
        self.verify(
            "r――N=Q(btm)",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_01_plus(self):
        self.verify("2+e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_02_minus_02_space(
        self,
    ):
        self.verify("2- e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_03_multiply(self):
        self.verify("2*e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_04_divide(self):
        self.verify("2/e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_05_mod_02_space(self):
        self.verify("2% e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_06_equals(self):
        self.verify("2==e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_07_gt(self):
        self.verify("2>e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_08_ge(self):
        self.verify("2>=e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_09_lt_01_no_space(
        self,
    ):
        self.verify("2<e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_09_lt_02_space(self):
        self.verify("2< e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_10_le(self):
        self.verify("2<=e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_11_ne(self):
        self.verify("2!=e2――Qa4=q(btm)", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_12_and(self):
        self.verify(
            "2 and e2――Qa4=q(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_04_lhs_13_or(self):
        self.verify(
            "2 or e2――Qa4=q(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_01_plus(self):
        self.verify("e2――Qa4=q(btm)+2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_02_minus(self):
        self.verify(
            "e2――Qa4=q(btm)-2",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_03_multiply(self):
        self.verify("e2――Qa4=q(btm)*2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_04_divide(self):
        self.verify("e2――Qa4=q(btm)/2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("e2――Qa4=q(btm)%2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_05_mod_02_space(self):
        self.verify("e2――Qa4=q(btm) %2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_06_equals(self):
        self.verify("e2――Qa4=q(btm)==2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_07_gt(self):
        self.verify("e2――Qa4=q(btm)>2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_08_ge(self):
        self.verify("e2――Qa4=q(btm)>=2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_09_lt_01_no_space(
        self,
    ):
        self.verify("e2――Qa4=q(btm)<2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_09_lt_02_space(self):
        self.verify("e2――Qa4=q(btm) <2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_10_le(self):
        self.verify("e2――Qa4=q(btm)<=2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_11_ne(self):
        self.verify("e2――Qa4=q(btm)!=2", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "e2――Qa4=q(btm) and 2",
            [
                (3, "And"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(e2――Qa4=q(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "DashLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "e2――Qa4=q(btm) or 2",
            [
                (3, "Or"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(e2――Qa4=q(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "DashLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_06_repeat_01_zero_up(self):
        self.verify("e2――Qa4=q(btm)*", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_06_repeat_02_one_up(self):
        self.verify("e2――Qa4=q(btm)+", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_06_repeat_03_optional(self):
        self.verify("e2――Qa4=q(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_148_dash_utf8_16_lr_promote_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2――Qa4=q(btm){5}",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_148_dash_utf8_16_lr_promote_target_06_repeat_05_range(self):
        self.verify("e2――Qa4=q(btm){3,5}", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_06_repeat_06_up_to(self):
        self.verify("e2――Qa4=q(btm){,5}", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_06_repeat_07_and_over(self):
        self.verify("e2――Qa4=q(btm){3,}", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("e2――Qa4=q(btm){*}", [], returncode=1)

    def test_148_dash_utf8_16_lr_promote_target_06_repeat_09_force_one_up(
        self,
    ):
        self.verify("e2――Qa4=q(btm){+}", [], returncode=1)

    def test_148_dash_utf8_17_not_01_implicit_lhs(self):
        self.verify(
            "not ――",
            [(3, "Not"), (4, "DashII"), (5, "AnySquare"), (5, "AnySquare")],
        )

    def test_148_dash_utf8_17_not_02_given_lhs(self):
        self.verify(
            "not q――",
            [
                (3, "Not"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_18_or_01_implicit_lhs_01_space(self):
        self.verify("b| ――", [], returncode=1)

    def test_148_dash_utf8_18_or_01_implicit_lhs_02_nospace(self):
        self.verify("b|――", [], returncode=1)

    def test_148_dash_utf8_18_or_02_given_lhs(self):
        self.verify(
            "b|q――",
            [
                (3, "DashLI"),
                (4, "Union"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_19_colon_01_implicit_lhs_01_space(self):
        self.verify(
            "currentposition: ――",
            [
                (3, "Colon"),
                (4, "CurrentPosition"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_19_colon_01_implicit_lhs_02_nospace(self):
        self.verify(
            "currentposition:――",
            [
                (3, "Colon"),
                (4, "CurrentPosition"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_19_colon_02_given_lhs(self):
        self.verify(
            "currentposition:q――",
            [
                (3, "DashLI"),
                (4, "Colon"),
                (5, "CurrentPosition"),
                (5, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_20_or_01_implicit_rhs_01_space(self):
        self.verify("―― |b", [], returncode=1)

    def test_148_dash_utf8_20_or_01_implicit_rhs_02_nospace(self):
        self.verify("――|b", [], returncode=1)

    def test_148_dash_utf8_20_or_02_given_rhs(self):
        self.verify(
            "――q|b",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "Union"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_20_or_03_given_rhs_and_lhs(self):
        self.verify(
            "R――q|b",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "Union"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_20_or_04_implicit_rhs_given_lhs(self):
        self.verify("R―― |b", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_01_implicit_01_dash_ascii(self):
        self.verify("――--", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_01_implicit_02_dash_utf8(self):
        self.verify("――――", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_01_implicit_03_take_ascii(self):
        self.verify("――[x]", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_01_implicit_04_take_utf8(self):
        self.verify("――×", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_02_given_01_piecedesignator(self):
        self.verify("――k――", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_02_given_02_set(self):
        self.verify("――to――", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_02_given_03_compoundset(self):
        self.verify("――{1 k}――", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_02_given_04_parenthesizedset(self):
        self.verify("――(k)――", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_02_given_05_parenthesizedset(self):
        self.verify("――(k)――", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_02_given_06_and_01_no_spaces(self):
        self.verify("――and――", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_02_given_06_and_02_left_space(self):
        self.verify("―― and――", [], returncode=1)

    def test_148_dash_utf8_21_ambiguous_02_given_06_and_03_right_space(self):
        self.verify_tolerant("――and ――", [])

    def test_148_dash_utf8_22_target_filter_type_01_default(self):
        con = self.verify(
            "――",
            [(3, "DashII"), (4, "AnySquare"), (4, "AnySquare")],
        )
        self.assertEqual(
            con.children[-1].children[-1].filter_type
            is cqltypes.FilterType.LOGICAL,
            True,
        )

    def test_148_dash_utf8_22_target_filter_type_02_logical(self):
        con = self.verify(
            "――(to btm)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "To"),
                (5, "BTM"),
            ],
        )
        self.assertEqual(
            con.children[-1].children[-1].filter_type
            is cqltypes.FilterType.LOGICAL,
            True,
        )

    def test_148_dash_utf8_22_target_filter_type_03_integer(self):
        con = self.verify(
            "――(btm 4)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (5, "Integer"),
            ],
        )
        self.assertEqual(
            con.children[-1].children[-1].filter_type
            is cqltypes.FilterType.NUMERIC,
            True,
        )

    def test_148_dash_utf8_22_target_filter_type_04_string(self):
        con = self.verify(
            '――(btm "hi")',
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (5, "String"),
            ],
        )
        self.assertEqual(
            con.children[-1].children[-1].filter_type
            is cqltypes.FilterType.STRING,
            True,
        )

    def test_148_dash_utf8_22_target_filter_type_05_set(self):
        con = self.verify(
            "――(btm to)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (5, "To"),
            ],
        )
        self.assertEqual(
            con.children[-1].children[-1].filter_type
            is cqltypes.FilterType.SET,
            True,
        )

    def test_148_dash_utf8_22_target_filter_type_06_position(self):
        con = self.verify(
            "――(btm currentposition)",
            [
                (3, "DashII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (5, "CurrentPosition"),
            ],
        )
        self.assertEqual(
            con.children[-1].children[-1].filter_type
            is cqltypes.FilterType.POSITION,
            True,
        )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterDashUTF8))
