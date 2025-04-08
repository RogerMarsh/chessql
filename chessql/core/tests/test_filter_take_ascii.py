# test_filter_take_ascii.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for '[x]' filter (called 'captures'?).

Equivalent to '×' ("\u00d7").

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes


class FilterTakeASCII(verify.Verify):

    def test_214_take_ascii_01_plain_01_bare(self):
        self.verify(
            "[x]",
            [(3, "TakeII"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test_214_take_ascii_01_plain_02_parentheses_01(self):
        self.verify(
            "([x])",
            [
                (3, "ParenthesisLeft"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_01_plain_02_parentheses_02(self):
        self.verify(
            "( [x])",
            [
                (3, "ParenthesisLeft"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_01_plain_02_parentheses_03(self):
        self.verify(
            "([x] )",
            [
                (3, "ParenthesisLeft"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_01_plain_02_parentheses_04(self):
        self.verify(
            "( [x] )",
            [
                (3, "ParenthesisLeft"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_01_plain_03_braces_01(self):
        self.verify(
            "{[x]}",
            [
                (3, "BraceLeft"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_01_plain_03_braces_02(self):
        self.verify(
            "{ [x]}",
            [
                (3, "BraceLeft"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_01_plain_03_braces_03(self):
        self.verify(
            "{[x] }",
            [
                (3, "BraceLeft"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_01_plain_03_braces_04(self):
        self.verify(
            "{ [x] }",
            [
                (3, "BraceLeft"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_01_plain_04_target_01_btm(self):
        self.verify(
            "[x](btm)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_01_plain_04_target_02_o_o(self):
        self.verify(
            "[x](o-o)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "OO"),
            ],
        )

    def test_214_take_ascii_01_plain_04_target_03_o_o_o(self):
        self.verify(
            "[x](o-o-o)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "OOO"),
            ],
        )

    def test_214_take_ascii_01_plain_04_target_04_castle(self):
        self.verify(
            "[x](castle)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "Castle"),
            ],
        )

    def test_214_take_ascii_01_plain_04_target_05_enpassant(self):
        self.verify(
            "[x](enpassant)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "EnPassant"),
            ],
        )

    def test_214_take_ascii_01_plain_04_target_06_o_o_set(self):
        self.verify(
            "[x](o-o to)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "OO"),
                (5, "To"),
            ],
        )

    def test_214_take_ascii_01_plain_04_target_07_set_o_o(self):
        self.verify(
            "[x](Rc4 o-o)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "PieceDesignator"),
                (5, "OO"),
            ],
        )

    def test_214_take_ascii_01_plain_05_brace_repeat_05_two_elements_03(self):
        self.verify("[x]{2 4}", [], returncode=1)

    def test_214_take_ascii_01_plain_05_brace_repeat_05_two_elements_04(self):
        self.verify(
            "[x] {2 4}",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (3, "BraceLeft"),
                (4, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_01_plain_06_repeat_01_zero_up(self):
        self.verify("[x]*", [], returncode=1)

    def test_214_take_ascii_01_plain_06_repeat_02_one_up(self):
        self.verify("[x]+", [], returncode=1)

    def test_214_take_ascii_01_plain_06_repeat_03_optional(self):
        self.verify("[x]?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_01_plain_06_repeat_04_exact(self):
        self.verify("[x]{5}", [], returncode=1)

    def test_214_take_ascii_01_plain_06_repeat_05_range(self):
        self.verify("[x]{3,5}", [], returncode=1)

    def test_214_take_ascii_01_plain_06_repeat_06_up_to(self):
        self.verify("[x]{,5}", [], returncode=1)

    def test_214_take_ascii_01_plain_06_repeat_07_and_over(self):
        self.verify("[x]{3,}", [], returncode=1)

    def test_214_take_ascii_01_plain_06_repeat_08_force_zero_up(self):
        self.verify("[x]{*}", [], returncode=1)

    def test_214_take_ascii_01_plain_06_repeat_09_force_one_up(self):
        self.verify("[x]{+}", [], returncode=1)

    def test_214_take_ascii_02_left_01_plain(self):
        self.verify(
            "e2[x]",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_214_take_ascii_02_left_02_compound_set(self):
        self.verify(
            "{2 e2}[x]",
            [
                (3, "TakeLI"),
                (4, "BraceLeft"),
                (5, "Integer"),
                (5, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_214_take_ascii_02_left_03_compound_not_set(self):
        self.verify("{e2 2}[x]", [], returncode=1)

    def test_214_take_ascii_02_left_06_repeat_01_zero_up(self):
        self.verify("e2[x]*", [], returncode=1)

    def test_214_take_ascii_02_left_06_repeat_02_one_up(self):
        self.verify("e2[x]+", [], returncode=1)

    def test_214_take_ascii_02_left_06_repeat_03_optional(self):
        self.verify("e2[x]?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_02_left_06_repeat_04_exact(self):
        self.verify("e2[x]{5}", [], returncode=1)

    def test_214_take_ascii_02_left_06_repeat_05_range(self):
        self.verify("e2[x]{3,5}", [], returncode=1)

    def test_214_take_ascii_02_left_06_repeat_06_up_to(self):
        self.verify("e2[x]{,5}", [], returncode=1)

    def test_214_take_ascii_02_left_06_repeat_07_and_over(self):
        self.verify("e2[x]{3,}", [], returncode=1)

    def test_214_take_ascii_02_left_06_repeat_08_force_zero_up(self):
        self.verify("e2[x]{*}", [], returncode=1)

    def test_214_take_ascii_02_left_06_repeat_09_force_one_up(self):
        self.verify("e2[x]{+}", [], returncode=1)

    def test_214_take_ascii_03_right_01_plain(self):
        self.verify(
            "[x]Qa4",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_03_right_02_compound_set(self):
        self.verify(
            "[x]{3 e4}",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "BraceLeft"),
                (5, "Integer"),
                (5, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_03_right_03_compound_not_set(self):
        self.verify("[x]{e4 3}", [], returncode=1)

    def test_214_take_ascii_03_right_06_repeat_01_zero_up(self):
        self.verify("[x]Qa4*", [], returncode=1)

    def test_214_take_ascii_03_right_06_repeat_02_one_up(self):
        self.verify("[x]Qa4+", [], returncode=1)

    def test_214_take_ascii_03_right_06_repeat_03_optional(self):
        self.verify("[x]Qa4?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_03_right_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "[x]Qa4{5}",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_03_right_06_repeat_05_range(self):
        self.verify("[x]Qa4{3,5}", [], returncode=1)

    def test_214_take_ascii_03_right_06_repeat_06_up_to(self):
        self.verify("[x]Qa4{,5}", [], returncode=1)

    def test_214_take_ascii_03_right_06_repeat_07_and_over(self):
        self.verify("[x]Qa4{3,}", [], returncode=1)

    def test_214_take_ascii_03_right_06_repeat_08_force_zero_up(self):
        self.verify("[x]Qa4{*}", [], returncode=1)

    def test_214_take_ascii_03_right_06_repeat_09_force_one_up(self):
        self.verify("[x]Qa4{+}", [], returncode=1)

    def test_214_take_ascii_04_left_right_01_plain(self):
        self.verify(
            "r[x]Qa4",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_04_left_right_02_compound_set(self):
        self.verify(
            "{2 e2}[x]{3 e4}",
            [
                (3, "TakeLR"),
                (4, "BraceLeft"),
                (5, "Integer"),
                (5, "PieceDesignator"),
                (4, "BraceLeft"),
                (5, "Integer"),
                (5, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_04_left_right_03_compound_not_set(self):
        self.verify("{e2 2}[x]{e4 3}", [], returncode=1)

    def test_214_take_ascii_04_left_right_06_repeat_01_zero_up(self):
        self.verify("e2[x]Qa4*", [], returncode=1)

    def test_214_take_ascii_04_left_right_06_repeat_02_one_up(self):
        self.verify("e2[x]Qa4+", [], returncode=1)

    def test_214_take_ascii_04_left_right_06_repeat_03_optional(self):
        self.verify("e2[x]Qa4?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_04_left_right_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2[x]Qa4{5}",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_04_left_right_06_repeat_05_range(self):
        self.verify("e2[x]Qa4{3,5}", [], returncode=1)

    def test_214_take_ascii_04_left_right_06_repeat_06_up_to(self):
        self.verify("e2[x]Qa4{,5}", [], returncode=1)

    def test_214_take_ascii_04_left_right_06_repeat_07_and_over(self):
        self.verify("e2[x]Qa4{3,}", [], returncode=1)

    def test_214_take_ascii_04_left_right_06_repeat_08_force_zero_up(self):
        self.verify("e2[x]Qa4{*}", [], returncode=1)

    def test_214_take_ascii_04_left_right_06_repeat_09_force_one_up(self):
        self.verify("e2[x]Qa4{+}", [], returncode=1)

    def test_214_take_ascii_05_promote_01(self):
        self.verify(
            "[x]=q",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_05_promote_02(self):
        self.verify("[x]=qa5", [], returncode=1)

    def test_214_take_ascii_05_promote_03(self):
        self.verify("[x]=check", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_01_plus(self):
        self.verify("2+[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_02_minus_01_no_space(self):
        self.verify("2[x]-=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_02_minus_02_space(self):
        self.verify("2- [x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_03_multiply(self):
        self.verify("2*[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_04_divide(self):
        self.verify("2/[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_05_modulus_01_no_space(self):
        self.verify("2%[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_05_modulus_02_space(self):
        self.verify("2% [x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_06_equals(self):
        self.verify("2==[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_07_gt(self):
        self.verify("2>[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_08_ge(self):
        self.verify("2>=[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_09_lt_01_no_space(self):
        self.verify("2<[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_09_lt_02_space(self):
        self.verify("2< [x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_10_le(self):
        self.verify("2<=[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_11_ne(self):
        self.verify("2!=[x]=q", [], returncode=1)

    def test_214_take_ascii_05_promote_04_lhs_12_and(self):
        self.verify(
            "2 and [x]=q",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_05_promote_04_lhs_13_or(self):
        self.verify(
            "2 or [x]=q",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_05_promote_05_rhs_01_plus(self):
        self.verify("[x]=q+2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_02_minus(self):
        self.verify(
            "[x]=q-2",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_05_promote_05_rhs_03_multiply(self):
        self.verify("[x]=q*2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_04_divide(self):
        self.verify("[x]=q/2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_05_modulus_01_no_space(self):
        self.verify("[x]=q%2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_05_modulus_02_space(self):
        self.verify("[x]=q %2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_06_equals(self):
        self.verify("[x]=q==2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_07_gt(self):
        self.verify("[x]=q>2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_08_ge(self):
        self.verify("[x]=q>=2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_09_lt_01_no_space(self):
        self.verify("[x]=q<2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_09_lt_02_space(self):
        self.verify("[x]=q <2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_10_le(self):
        self.verify("[x]=q<=2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_11_ne(self):
        self.verify("[x]=q!=2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_12_and_01_plain(self):
        self.verify("[x]=q and 2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "([x]=q) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_05_promote_05_rhs_13_or_01_plain(self):
        self.verify("[x]=q or 2", [], returncode=1)

    def test_214_take_ascii_05_promote_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "([x]=q) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_05_promote_06_repeat_01_zero_up(self):
        self.verify("[x]=q*", [], returncode=1)

    def test_214_take_ascii_05_promote_06_repeat_02_one_up(self):
        self.verify("[x]=q+", [], returncode=1)

    def test_214_take_ascii_05_promote_06_repeat_03_optional(self):
        self.verify("[x]=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_05_promote_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "[x]=q{5}",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_05_promote_06_repeat_05_range(self):
        self.verify("[x]=q{3,5}", [], returncode=1)

    def test_214_take_ascii_05_promote_06_repeat_06_up_to(self):
        self.verify("[x]=q{,5}", [], returncode=1)

    def test_214_take_ascii_05_promote_06_repeat_07_and_over(self):
        self.verify("[x]=q{3,}", [], returncode=1)

    def test_214_take_ascii_05_promote_06_repeat_08_force_zero_up(self):
        self.verify("[x]=q{*}", [], returncode=1)

    def test_214_take_ascii_05_promote_06_repeat_09_force_one_up(self):
        self.verify("[x]=q{+}", [], returncode=1)

    def test_214_take_ascii_06_left_promote_01(self):
        self.verify(
            "e2[x]=b",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_06_left_promote_02(self):
        self.verify("e2[x]=bc6", [], returncode=1)

    def test_214_take_ascii_06_left_promote_03(self):
        self.verify("e2[x]=check", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_01_plus(self):
        self.verify("2+e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_02_minus_01_no_space(self):
        self.verify("2-e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_02_minus_02_space(self):
        self.verify("2- e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_03_multiply(self):
        self.verify("2*e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_04_divide(self):
        self.verify("2/e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_05_mod_01_no_space(self):
        self.verify("2%e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_05_mod_02_space(self):
        self.verify("2% e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_06_equals(self):
        self.verify("2==e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_07_gt(self):
        self.verify("2>e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_08_ge(self):
        self.verify("2>=e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_09_lt_01_no_space(self):
        self.verify("2<e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_09_lt_02_space(self):
        self.verify("2< e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_10_le(self):
        self.verify("2<=e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_11_ne(self):
        self.verify("2!=e2[x]=q", [], returncode=1)

    def test_214_take_ascii_06_left_promote_04_lhs_12_and(self):
        self.verify(
            "2 and e2[x]=q",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_06_left_promote_04_lhs_13_or(self):
        self.verify(
            "2 or e2[x]=q",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_06_left_promote_05_rhs_01_plus(self):
        self.verify("e2[x]=q+2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_02_minus(self):
        self.verify(
            "e2[x]=q-2",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_06_left_promote_05_rhs_03_multiply(self):
        self.verify("e2[x]=q*2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_04_divide(self):
        self.verify("e2[x]=q/2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_05_mod_01_no_space(self):
        self.verify("e2[x]=q%2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_05_mod_02_space(self):
        self.verify("e2[x]=q %2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_06_equals(self):
        self.verify("e2[x]=q==2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_07_gt(self):
        self.verify("e2[x]=q>2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_08_ge(self):
        self.verify("e2[x]=q>=2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_09_lt_01_no_space(self):
        self.verify("e2[x]=q<2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_09_lt_02_space(self):
        self.verify("e2[x]=q <2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_10_le(self):
        self.verify("e2[x]=q<=2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_11_ne(self):
        self.verify("e2[x]=q!=2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_12_and_01_plain(self):
        self.verify("e2[x]=q and 2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "(e2[x]=q) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_06_left_promote_05_rhs_13_or_01_plain(self):
        self.verify("e2[x]=q or 2", [], returncode=1)

    def test_214_take_ascii_06_left_promote_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "(e2[x]=q) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_06_left_promote_06_repeat_01_zero_up(self):
        self.verify("e2[x]=q*", [], returncode=1)

    def test_214_take_ascii_06_left_promote_06_repeat_02_one_up(self):
        self.verify("e2[x]=q+", [], returncode=1)

    def test_214_take_ascii_06_left_promote_06_repeat_03_optional(self):
        self.verify("e2[x]=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_06_left_promote_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2[x]=q{5}",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_06_left_promote_06_repeat_05_range(self):
        self.verify("e2[x]=q{3,5}", [], returncode=1)

    def test_214_take_ascii_06_left_promote_06_repeat_06_up_to(self):
        self.verify("e2[x]=q{,5}", [], returncode=1)

    def test_214_take_ascii_06_left_promote_06_repeat_07_and_over(self):
        self.verify("e2[x]=q{3,}", [], returncode=1)

    def test_214_take_ascii_06_left_promote_06_repeat_08_force_zero_up(self):
        self.verify("e2[x]=q{*}", [], returncode=1)

    def test_214_take_ascii_06_left_promote_06_repeat_09_force_one_up(self):
        self.verify("e2[x]=q{+}", [], returncode=1)

    def test_214_take_ascii_07_right_promote_01(self):
        self.verify(
            "[x]Qa4=N",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_07_right_promote_02(self):
        self.verify("[x]Qa4=bc6", [], returncode=1)

    def test_214_take_ascii_07_right_promote_03(self):
        self.verify("[x]Qa4=check", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_01_plus(self):
        self.verify("2+[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_02_minus_01_no_space(self):
        self.verify("2[x]-Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_02_minus_02_space(self):
        self.verify("2- [x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_03_multiply(self):
        self.verify("2*[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_04_divide(self):
        self.verify("2/[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_05_mod_01_no_space(self):
        self.verify("2%[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_05_mod_02_space(self):
        self.verify("2% [x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_06_equals(self):
        self.verify("2==[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_07_gt(self):
        self.verify("2>[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_08_ge(self):
        self.verify("2>=[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_09_lt_01_no_space(self):
        self.verify("2<[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_09_lt_02_space(self):
        self.verify("2< [x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_10_le(self):
        self.verify("2<=[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_11_ne(self):
        self.verify("2!=[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_07_right_promote_04_lhs_12_and(self):
        self.verify(
            "2 and [x]Qa4=q",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_07_right_promote_04_lhs_13_or(self):
        self.verify(
            "2 or [x]Qa4=q",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_07_right_promote_05_rhs_01_plus(self):
        self.verify("[x]Qa4=q+2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_02_minus(self):
        self.verify(
            "[x]Qa4=q-2",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_07_right_promote_05_rhs_03_multiply(self):
        self.verify("[x]Qa4=q*2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_04_divide(self):
        self.verify("[x]Qa4=q/2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_05_mod_01_no_space(self):
        self.verify("[x]Qa4=q%2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_05_mod_02_space(self):
        self.verify("[x]Qa4=q %2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_06_equals(self):
        self.verify("[x]Qa4=q==2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_07_gt(self):
        self.verify("[x]Qa4=q>2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_08_ge(self):
        self.verify("[x]Qa4=q>=2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_09_lt_01_no_space(self):
        self.verify("[x]Qa4=q<2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_09_lt_02_space(self):
        self.verify("[x]Qa4=q <2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_10_le(self):
        self.verify("[x]Qa4=q<=2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_11_ne(self):
        self.verify("[x]Qa4=q!=2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_12_and_01_plain(self):
        self.verify("[x]Qa4=q and 2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "([x]Qa4=q) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_07_right_promote_05_rhs_13_or_01_plain(self):
        self.verify("[x]Qa4=q or 2", [], returncode=1)

    def test_214_take_ascii_07_right_promote_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "([x]Qa4=q) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_07_right_promote_06_repeat_01_zero_up(self):
        self.verify("[x]Qa4=q*", [], returncode=1)

    def test_214_take_ascii_07_right_promote_06_repeat_02_one_up(self):
        self.verify("[x]Qa4=q+", [], returncode=1)

    def test_214_take_ascii_07_right_promote_06_repeat_03_optional(self):
        self.verify("[x]Qa4=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_07_right_promote_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "[x]Qa4=q{5}",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_07_right_promote_06_repeat_05_range(self):
        self.verify("[x]Qa4=q{3,5}", [], returncode=1)

    def test_214_take_ascii_07_right_promote_06_repeat_06_up_to(self):
        self.verify("[x]Qa4=q{,5}", [], returncode=1)

    def test_214_take_ascii_07_right_promote_06_repeat_07_and_over(self):
        self.verify("[x]Qa4=q{3,}", [], returncode=1)

    def test_214_take_ascii_07_right_promote_06_repeat_08_force_zero_up(self):
        self.verify("[x]Qa4=q{*}", [], returncode=1)

    def test_214_take_ascii_07_right_promote_06_repeat_09_force_one_up(self):
        self.verify("[x]Qa4=q{+}", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_01(self):
        self.verify(
            "r[x]Qa4=R",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_08_left_right_promote_02(self):
        self.verify("r[x]Qa4=bc6", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_03(self):
        self.verify("r[x]Qa4=check", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_01_plus(self):
        self.verify("2+e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_02_minus_02_space(
        self,
    ):
        self.verify("2- e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_03_multiply(self):
        self.verify("2*e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_04_divide(self):
        self.verify("2/e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_05_mod_02_space(self):
        self.verify("2% e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_06_equals(self):
        self.verify("2==e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_07_gt(self):
        self.verify("2>e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_08_ge(self):
        self.verify("2>=e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_09_lt_01_no_space(
        self,
    ):
        self.verify("2<e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_09_lt_02_space(self):
        self.verify("2< e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_10_le(self):
        self.verify("2<=e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_11_ne(self):
        self.verify("2!=e2[x]Qa4=q", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_04_lhs_12_and(self):
        self.verify(
            "2 and e2[x]Qa4=q",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_08_left_right_promote_04_lhs_13_or(self):
        self.verify(
            "2 or e2[x]Qa4=q",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_08_left_right_promote_05_rhs_01_plus(self):
        self.verify("e2[x]Qa4=q+2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_02_minus(self):
        self.verify(
            "e2[x]Qa4=q-2",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_08_left_right_promote_05_rhs_03_multiply(self):
        self.verify("e2[x]Qa4=q*2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_04_divide(self):
        self.verify("e2[x]Qa4=q/2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("e2[x]Qa4=q%2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_05_mod_02_space(self):
        self.verify("e2[x]Qa4=q %2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_06_equals(self):
        self.verify("e2[x]Qa4=q==2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_07_gt(self):
        self.verify("e2[x]Qa4=q>2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_08_ge(self):
        self.verify("e2[x]Qa4=q>=2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_09_lt_01_no_space(
        self,
    ):
        self.verify("e2[x]Qa4=q<2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_09_lt_02_space(self):
        self.verify("e2[x]Qa4=q <2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_10_le(self):
        self.verify("e2[x]Qa4=q<=2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_11_ne(self):
        self.verify("e2[x]Qa4=q!=2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_12_and_01_plain(self):
        self.verify("e2[x]Qa4=q and 2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(e2[x]Qa4=q) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_08_left_right_promote_05_rhs_13_or_01_plain(self):
        self.verify("e2[x]Qa4=q or 2", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(e2[x]Qa4=q) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_08_left_right_promote_06_repeat_01_zero_up(self):
        self.verify("e2[x]Qa4=q*", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_06_repeat_02_one_up(self):
        self.verify("e2[x]Qa4=q+", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_06_repeat_03_optional(self):
        self.verify("e2[x]Qa4=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_08_left_right_promote_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2[x]Qa4=q{5}",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_08_left_right_promote_06_repeat_05_range(self):
        self.verify("e2[x]Qa4=q{3,5}", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_06_repeat_06_up_to(self):
        self.verify("e2[x]Qa4=q{,5}", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_06_repeat_07_and_over(self):
        self.verify("e2[x]Qa4=q{3,}", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("e2[x]Qa4=q{*}", [], returncode=1)

    def test_214_take_ascii_08_left_right_promote_06_repeat_09_force_one_up(
        self,
    ):
        self.verify("e2[x]Qa4=q{+}", [], returncode=1)

    def test_214_take_ascii_09_target_01_plain(self):
        self.verify(
            "[x](btm)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_09_target_04_lhs_01_plus(self):
        self.verify("2+[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_02_minus_01_no_space(self):
        self.verify("2-[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_02_minus_02_space(self):
        self.verify("2- [x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_03_multiply(self):
        self.verify("2*[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_04_divide(self):
        self.verify("2/[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_05_mod_01_no_space(self):
        self.verify("2%[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_05_mod_02_space(self):
        self.verify("2% [x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_06_equals(self):
        self.verify("2==[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_07_gt(self):
        self.verify("2>[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_08_ge(self):
        self.verify("2>=[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_09_lt_02_space(self):
        self.verify("2< [x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_10_le(self):
        self.verify("2<=[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_11_ne(self):
        self.verify("2!=[x](btm)", [], returncode=1)

    def test_214_take_ascii_09_target_04_lhs_12_and(self):
        self.verify(
            "2 and [x](btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_09_target_04_lhs_13_or(self):
        self.verify(
            "2 or [x](btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_09_target_05_rhs_01_plus(self):
        self.verify("[x](btm)+2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_02_minus(self):
        self.verify(
            "[x](btm)-2",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_09_target_05_rhs_03_multiply(self):
        self.verify("[x](btm)*2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_04_divide(self):
        self.verify("[x](btm)/2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_05_mod_01_no_space(self):
        self.verify("[x](btm)%2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_05_mod_02_space(self):
        self.verify("[x](btm) %2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_06_equals(self):
        self.verify("[x](btm)==2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_07_gt(self):
        self.verify("[x](btm)>2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_08_ge(self):
        self.verify("[x](btm)>=2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_09_lt_01_no_space(self):
        self.verify("[x](btm)<2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_09_lt_02_space(self):
        self.verify("[x](btm) <2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_10_le(self):
        self.verify("[x](btm)<=2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_11_ne(self):
        self.verify("[x](btm)!=2", [], returncode=1)

    def test_214_take_ascii_09_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "[x](btm) and 2",
            [
                (3, "And"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_09_target_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "([x](btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_09_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "[x](btm) or 2",
            [
                (3, "Or"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_09_target_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "([x](btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_09_target_06_repeat_01_zero_up(self):
        self.verify("[x](btm)*", [], returncode=1)

    def test_214_take_ascii_09_target_06_repeat_02_one_up(self):
        self.verify("[x](btm)+", [], returncode=1)

    def test_214_take_ascii_09_target_06_repeat_03_optional(self):
        self.verify("[x](btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_09_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "[x](btm){5}",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_09_target_06_repeat_05_range(self):
        self.verify("[x](btm){3,5}", [], returncode=1)

    def test_214_take_ascii_09_target_06_repeat_06_up_to(self):
        self.verify("[x](btm){,5}", [], returncode=1)

    def test_214_take_ascii_09_target_06_repeat_07_and_over(self):
        self.verify("[x](btm){3,}", [], returncode=1)

    def test_214_take_ascii_09_target_06_repeat_08_force_zero_up(self):
        self.verify("[x](btm){*}", [], returncode=1)

    def test_214_take_ascii_09_target_06_repeat_09_force_one_up(self):
        self.verify("[x](btm){+}", [], returncode=1)

    def test_214_take_ascii_10_left_target_01_plain(self):
        self.verify(
            "P[x](btm)",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_10_left_target_04_lhs_01_plus(self):
        self.verify("2+e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_02_minus_01_no_space(self):
        self.verify("2-e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_02_minus_02_space(self):
        self.verify("2- e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_03_multiply(self):
        self.verify("2*e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_04_divide(self):
        self.verify("2/e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_05_mod_01_no_space(self):
        self.verify("2%e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_05_mod_02_space(self):
        self.verify("2% e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_06_equals(self):
        self.verify("2==e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_07_gt(self):
        self.verify("2>e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_08_ge(self):
        self.verify("2>=e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_09_lt_02_space(self):
        self.verify("2< e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_10_le(self):
        self.verify("2<=e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_11_ne(self):
        self.verify("2!=e2[x](btm)", [], returncode=1)

    def test_214_take_ascii_10_left_target_04_lhs_12_and(self):
        self.verify(
            "2 and e2[x](btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_10_left_target_04_lhs_13_or(self):
        self.verify(
            "2 or e2[x](btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_10_left_target_05_rhs_01_plus(self):
        self.verify("e2[x](btm)+2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_02_minus(self):
        self.verify(
            "e2[x](btm)-2",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_10_left_target_05_rhs_03_multiply(self):
        self.verify("e2[x](btm)*2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_04_divide(self):
        self.verify("e2[x](btm)/2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_05_mod_01_no_space(self):
        self.verify("e2[x](btm)%2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_05_mod_02_space(self):
        self.verify("e2[x](btm) %2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_06_equals(self):
        self.verify("e2[x](btm)==2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_07_gt(self):
        self.verify("e2[x](btm)>2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_08_ge(self):
        self.verify("e2[x](btm)>=2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_09_lt_01_no_space(self):
        self.verify("e2[x](btm)<2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_09_lt_02_space(self):
        self.verify("e2[x](btm) <2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_10_le(self):
        self.verify("e2[x](btm)<=2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_11_ne(self):
        self.verify("e2[x](btm)!=2", [], returncode=1)

    def test_214_take_ascii_10_left_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "e2[x](btm) and 2",
            [
                (3, "And"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_10_left_target_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "(e2[x](btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_10_left_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "e2[x](btm) or 2",
            [
                (3, "Or"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_10_left_target_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "(e2[x](btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_10_left_target_06_repeat_01_zero_up(self):
        self.verify("e2[x](btm)*", [], returncode=1)

    def test_214_take_ascii_10_left_target_06_repeat_02_one_up(self):
        self.verify("e2[x](btm)+", [], returncode=1)

    def test_214_take_ascii_10_left_target_06_repeat_03_optional(self):
        self.verify("e2[x](btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_10_left_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2[x](btm){5}",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_10_left_target_06_repeat_05_range(self):
        self.verify("e2[x](btm){3,5}", [], returncode=1)

    def test_214_take_ascii_10_left_target_06_repeat_06_up_to(self):
        self.verify("e2[x](btm){,5}", [], returncode=1)

    def test_214_take_ascii_10_left_target_06_repeat_07_and_over(self):
        self.verify("e2[x](btm){3,}", [], returncode=1)

    def test_214_take_ascii_10_left_target_06_repeat_08_force_zero_up(self):
        self.verify("e2[x](btm){*}", [], returncode=1)

    def test_214_take_ascii_10_left_target_06_repeat_09_force_one_up(self):
        self.verify("e2[x](btm){+}", [], returncode=1)

    def test_214_take_ascii_11_right_target_01_plain(self):
        self.verify(
            "[x]N(btm)",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_11_right_target_04_lhs_01_plus(self):
        self.verify("2+[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_02_minus_01_no_space(self):
        self.verify("2-[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_02_minus_02_space(self):
        self.verify("2- [x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_03_multiply(self):
        self.verify("2*[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_04_divide(self):
        self.verify("2/[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_05_mod_01_no_space(self):
        self.verify("2%[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_05_mod_02_space(self):
        self.verify("2% [x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_06_equals(self):
        self.verify("2==[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_07_gt(self):
        self.verify("2>[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_08_ge(self):
        self.verify("2>=[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_09_lt_02_space(self):
        self.verify("2< [x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_10_le(self):
        self.verify("2<=[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_11_ne(self):
        self.verify("2!=[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_11_right_target_04_lhs_12_and(self):
        self.verify(
            "2 and [x]Qa4(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_11_right_target_04_lhs_13_or(self):
        self.verify(
            "2 or [x]Qa4(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_11_right_target_05_rhs_01_plus(self):
        self.verify("[x]Qa4(btm)+2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_02_minus(self):
        self.verify(
            "[x]Qa4(btm)-2",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_11_right_target_05_rhs_03_multiply(self):
        self.verify("[x]Qa4(btm)*2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_04_divide(self):
        self.verify("[x]Qa4(btm)/2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_05_mod_01_no_space(self):
        self.verify("[x]Qa4(btm)%2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_05_mod_02_space(self):
        self.verify("[x]Qa4(btm) %2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_06_equals(self):
        self.verify("[x]Qa4(btm)==2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_07_gt(self):
        self.verify("[x]Qa4(btm)>2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_08_ge(self):
        self.verify("[x]Qa4(btm)>=2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_09_lt_01_no_space(self):
        self.verify("[x]Qa4(btm)<2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_09_lt_02_space(self):
        self.verify("[x]Qa4(btm) <2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_10_le(self):
        self.verify("[x]Qa4(btm)<=2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_11_ne(self):
        self.verify("[x]Qa4(btm)!=2", [], returncode=1)

    def test_214_take_ascii_11_right_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "[x]Qa4(btm) and 2",
            [
                (3, "And"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_11_right_target_05_rhs_12_and_02_parentheses(self):
        self.verify(
            "([x]Qa4(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_11_right_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "[x]Qa4(btm) or 2",
            [
                (3, "Or"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_11_right_target_05_rhs_13_or_02_parentheses(self):
        self.verify(
            "([x]Qa4(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_11_right_target_06_repeat_01_zero_up(self):
        self.verify("[x]Qa4(btm)*", [], returncode=1)

    def test_214_take_ascii_11_right_target_06_repeat_02_one_up(self):
        self.verify("[x]Qa4(btm)+", [], returncode=1)

    def test_214_take_ascii_11_right_target_06_repeat_03_optional(self):
        self.verify("[x]Qa4(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_11_right_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "[x]Qa4(btm){5}",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_11_right_target_06_repeat_05_range(self):
        self.verify("[x]Qa4(btm){3,5}", [], returncode=1)

    def test_214_take_ascii_11_right_target_06_repeat_06_up_to(self):
        self.verify("[x]Qa4(btm){,5}", [], returncode=1)

    def test_214_take_ascii_11_right_target_06_repeat_07_and_over(self):
        self.verify("[x]Qa4(btm){3,}", [], returncode=1)

    def test_214_take_ascii_11_right_target_06_repeat_08_force_zero_up(self):
        self.verify("[x]Qa4(btm){*}", [], returncode=1)

    def test_214_take_ascii_11_right_target_06_repeat_09_force_one_up(self):
        self.verify("[x]Qa4(btm){+}", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_01_plain(self):
        self.verify(
            "r[x]N(btm)",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_04_lhs_01_plus(self):
        self.verify("2+e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_02_minus_02_space(
        self,
    ):
        self.verify("2- e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_03_multiply(self):
        self.verify("2*e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_04_divide(self):
        self.verify("2/e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_05_mod_02_space(self):
        self.verify("2% e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_06_equals(self):
        self.verify("2==e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_07_gt(self):
        self.verify("2>e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_08_ge(self):
        self.verify("2>=e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_09_lt_01_no_space(
        self,
    ):
        self.verify("2<e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_09_lt_02_space(self):
        self.verify("2< e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_10_le(self):
        self.verify("2<=e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_11_ne(self):
        self.verify("2!=e2[x]Qa4(btm)", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_04_lhs_12_and(self):
        self.verify(
            "2 and e2[x]Qa4(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_04_lhs_13_or(self):
        self.verify(
            "2 or e2[x]Qa4(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_05_rhs_01_plus(self):
        self.verify("e2[x]Qa4(btm)+2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_02_minus(self):
        self.verify(
            "e2[x]Qa4(btm)-2",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "UnaryMinus"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_05_rhs_03_multiply(self):
        self.verify("e2[x]Qa4(btm)*2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_04_divide(self):
        self.verify("e2[x]Qa4(btm)/2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("e2[x]Qa4(btm)%2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_05_mod_02_space(self):
        self.verify("e2[x]Qa4(btm) %2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_06_equals(self):
        self.verify("e2[x]Qa4(btm)==2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_07_gt(self):
        self.verify("e2[x]Qa4(btm)>2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_08_ge(self):
        self.verify("e2[x]Qa4(btm)>=2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_09_lt_01_no_space(
        self,
    ):
        self.verify("e2[x]Qa4(btm)<2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_09_lt_02_space(self):
        self.verify("e2[x]Qa4(btm) <2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_10_le(self):
        self.verify("e2[x]Qa4(btm)<=2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_11_ne(self):
        self.verify("e2[x]Qa4(btm)!=2", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "e2[x]Qa4(btm) and 2",
            [
                (3, "And"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(e2[x]Qa4(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "e2[x]Qa4(btm) or 2",
            [
                (3, "Or"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(e2[x]Qa4(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_06_repeat_01_zero_up(self):
        self.verify("e2[x]Qa4(btm)*", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_06_repeat_02_one_up(self):
        self.verify("e2[x]Qa4(btm)+", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_06_repeat_03_optional(self):
        self.verify("e2[x]Qa4(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_12_left_right_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2[x]Qa4(btm){5}",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_12_left_right_target_06_repeat_05_range(self):
        self.verify("e2[x]Qa4(btm){3,5}", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_06_repeat_06_up_to(self):
        self.verify("e2[x]Qa4(btm){,5}", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_06_repeat_07_and_over(self):
        self.verify("e2[x]Qa4(btm){3,}", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("e2[x]Qa4(btm){*}", [], returncode=1)

    def test_214_take_ascii_12_left_right_target_06_repeat_09_force_one_up(
        self,
    ):
        self.verify("e2[x]Qa4(btm){+}", [], returncode=1)

    def test_214_take_ascii_13_promote_target_01_plain(self):
        self.verify(
            "[x]=Q(btm)",
            [
                (3, "TakeII"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_13_promote_target_04_lhs_01_plus(self):
        self.verify("2+[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_02_minus_02_space(self):
        self.verify("2- [x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_03_multiply(self):
        self.verify("2*[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_04_divide(self):
        self.verify("2/[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_05_mod_01_no_space(self):
        self.verify("2%[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_05_mod_02_space(self):
        self.verify("2% [x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_06_equals(self):
        self.verify("2==[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_07_gt(self):
        self.verify("2>[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_08_ge(self):
        self.verify("2>=[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_09_lt_02_space(self):
        self.verify("2< [x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_10_le(self):
        self.verify("2<=[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_11_ne(self):
        self.verify("2!=[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_13_promote_target_04_lhs_12_and(self):
        self.verify(
            "2 and [x]=q(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_13_promote_target_04_lhs_13_or(self):
        self.verify(
            "2 or [x]=q(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_13_promote_target_05_rhs_01_plus(self):
        self.verify("[x]=q(btm)+2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_02_minus(self):
        self.verify(
            "[x]=q(btm)-2",
            [
                (3, "TakeII"),
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

    def test_214_take_ascii_13_promote_target_05_rhs_03_multiply(self):
        self.verify("[x]=q(btm)*2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_04_divide(self):
        self.verify("[x]=q(btm)/2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_05_mod_01_no_space(self):
        self.verify("[x]=q(btm)%2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_05_mod_02_space(self):
        self.verify("[x]=q(btm) %2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_06_equals(self):
        self.verify("[x]=q(btm)==2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_07_gt(self):
        self.verify("[x]=q(btm)>2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_08_ge(self):
        self.verify("[x]=q(btm)>=2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_09_lt_01_no_space(self):
        self.verify("[x]=q(btm)<2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_09_lt_02_space(self):
        self.verify("[x]=q(btm) <2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_10_le(self):
        self.verify("[x]=q(btm)<=2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_11_ne(self):
        self.verify("[x]=q(btm)!=2", [], returncode=1)

    def test_214_take_ascii_13_promote_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "[x]=q(btm) and 2",
            [
                (3, "And"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_13_promote_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "([x]=q(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_13_promote_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "[x]=q(btm) or 2",
            [
                (3, "Or"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_13_promote_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "([x]=q(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_13_promote_target_06_repeat_01_zero_up(self):
        self.verify("[x]=q(btm)*", [], returncode=1)

    def test_214_take_ascii_13_promote_target_06_repeat_02_one_up(self):
        self.verify("[x]=q(btm)+", [], returncode=1)

    def test_214_take_ascii_13_promote_target_06_repeat_03_optional(self):
        self.verify("[x]=q(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_13_promote_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "[x]=q(btm){5}",
            [
                (3, "TakeII"),
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

    def test_214_take_ascii_13_promote_target_06_repeat_05_range(self):
        self.verify("[x]=q(btm){3,5}", [], returncode=1)

    def test_214_take_ascii_13_promote_target_06_repeat_06_up_to(self):
        self.verify("[x]=q(btm){,5}", [], returncode=1)

    def test_214_take_ascii_13_promote_target_06_repeat_07_and_over(self):
        self.verify("[x]=q(btm){3,}", [], returncode=1)

    def test_214_take_ascii_13_promote_target_06_repeat_08_force_zero_up(self):
        self.verify("[x]=q(btm){*}", [], returncode=1)

    def test_214_take_ascii_13_promote_target_06_repeat_09_force_one_up(self):
        self.verify("[x]=q(btm){+}", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_01_plain(self):
        self.verify(
            "P[x]=Q(btm)",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_14_l_promote_target_04_lhs_01_plus(self):
        self.verify("2+e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_02_minus_02_space(self):
        self.verify("2- e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_03_multiply(self):
        self.verify("2*e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_04_divide(self):
        self.verify("2/e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_05_mod_02_space(self):
        self.verify("2% e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_06_equals(self):
        self.verify("2==e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_07_gt(self):
        self.verify("2>e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_08_ge(self):
        self.verify("2>=e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_09_lt_02_space(self):
        self.verify("2< e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_10_le(self):
        self.verify("2<=e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_11_ne(self):
        self.verify("2!=e2[x]=q(btm)", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_04_lhs_12_and(self):
        self.verify(
            "2 and e2[x]=q(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_14_l_promote_target_04_lhs_13_or(self):
        self.verify(
            "2 or e2[x]=q(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_14_l_promote_target_05_rhs_01_plus(self):
        self.verify("e2[x]=q(btm)+2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_02_minus(self):
        self.verify(
            "e2[x]=q(btm)-2",
            [
                (3, "TakeLI"),
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

    def test_214_take_ascii_14_l_promote_target_05_rhs_03_multiply(self):
        self.verify("e2[x]=q(btm)*2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_04_divide(self):
        self.verify("e2[x]=q(btm)/2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("e2[x]=q(btm)%2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_05_mod_02_space(self):
        self.verify("e2[x]=q(btm) %2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_06_equals(self):
        self.verify("e2[x]=q(btm)==2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_07_gt(self):
        self.verify("e2[x]=q(btm)>2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_08_ge(self):
        self.verify("e2[x]=q(btm)>=2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_09_lt_01_no_space(self):
        self.verify("e2[x]=q(btm)<2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_09_lt_02_space(self):
        self.verify("e2[x]=q(btm) <2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_10_le(self):
        self.verify("e2[x]=q(btm)<=2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_11_ne(self):
        self.verify("e2[x]=q(btm)!=2", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "e2[x]=q(btm) and 2",
            [
                (3, "And"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_14_l_promote_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(e2[x]=q(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_14_l_promote_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "e2[x]=q(btm) or 2",
            [
                (3, "Or"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_14_l_promote_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(e2[x]=q(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeLI"),
                (6, "PieceDesignator"),
                (6, "AnySquare"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_14_l_promote_target_06_repeat_01_zero_up(self):
        self.verify("e2[x]=q(btm)*", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_06_repeat_02_one_up(self):
        self.verify("e2[x]=q(btm)+", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_06_repeat_03_optional(self):
        self.verify("e2[x]=q(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_14_l_promote_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2[x]=q(btm){5}",
            [
                (3, "TakeLI"),
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

    def test_214_take_ascii_14_l_promote_target_06_repeat_05_range(self):
        self.verify("e2[x]=q(btm){3,5}", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_06_repeat_06_up_to(self):
        self.verify("e2[x]=q(btm){,5}", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_06_repeat_07_and_over(self):
        self.verify("e2[x]=q(btm){3,}", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("e2[x]=q(btm){*}", [], returncode=1)

    def test_214_take_ascii_14_l_promote_target_06_repeat_09_force_one_up(
        self,
    ):
        self.verify("e2[x]=q(btm){+}", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_01_plain(self):
        self.verify(
            "[x]N=Q(btm)",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_15_r_promote_target_04_lhs_01_plus(self):
        self.verify("2+[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_02_minus_02_space(self):
        self.verify("2- [x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_03_multiply(self):
        self.verify("2*[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_04_divide(self):
        self.verify("2/[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_05_mod_02_space(self):
        self.verify("2% [x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_06_equals(self):
        self.verify("2==[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_07_gt(self):
        self.verify("2>[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_08_ge(self):
        self.verify("2>=[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_09_lt_01_no_space(self):
        self.verify("2<[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_09_lt_02_space(self):
        self.verify("2< [x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_10_le(self):
        self.verify("2<=[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_11_ne(self):
        self.verify("2!=[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_04_lhs_12_and(self):
        self.verify(
            "2 and [x]Qa4=q(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_15_r_promote_target_04_lhs_13_or(self):
        self.verify(
            "2 or [x]Qa4=q(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_15_r_promote_target_05_rhs_01_plus(self):
        self.verify("[x]Qa4=q(btm)+2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_02_minus(self):
        self.verify(
            "[x]Qa4=q(btm)-2",
            [
                (3, "TakeIR"),
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

    def test_214_take_ascii_15_r_promote_target_05_rhs_03_multiply(self):
        self.verify("[x]Qa4=q(btm)*2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_04_divide(self):
        self.verify("[x]Qa4=q(btm)/2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("[x]Qa4=q(btm)%2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_05_mod_02_space(self):
        self.verify("[x]Qa4=q(btm) %2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_06_equals(self):
        self.verify("[x]Qa4=q(btm)==2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_07_gt(self):
        self.verify("[x]Qa4=q(btm)>2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_08_ge(self):
        self.verify("[x]Qa4=q(btm)>=2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_09_lt_01_no_space(self):
        self.verify("[x]Qa4=q(btm)<2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_09_lt_02_space(self):
        self.verify("[x]Qa4=q(btm) <2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_10_le(self):
        self.verify("[x]Qa4=q(btm)<=2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_11_ne(self):
        self.verify("[x]Qa4=q(btm)!=2", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "[x]Qa4=q(btm) and 2",
            [
                (3, "And"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_15_r_promote_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "([x]Qa4=q(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_15_r_promote_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "[x]Qa4=q(btm) or 2",
            [
                (3, "Or"),
                (4, "TakeIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_15_r_promote_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "([x]Qa4=q(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeIR"),
                (6, "AnySquare"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_15_r_promote_target_06_repeat_01_zero_up(self):
        self.verify("[x]Qa4=q(btm)*", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_06_repeat_02_one_up(self):
        self.verify("[x]Qa4=q(btm)+", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_06_repeat_03_optional(self):
        self.verify("[x]Qa4=q(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_15_r_promote_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "[x]Qa4=q(btm){5}",
            [
                (3, "TakeIR"),
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

    def test_214_take_ascii_15_r_promote_target_06_repeat_05_range(self):
        self.verify("[x]Qa4=q(btm){3,5}", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_06_repeat_06_up_to(self):
        self.verify("[x]Qa4=q(btm){,5}", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_06_repeat_07_and_over(self):
        self.verify("[x]Qa4=q(btm){3,}", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("[x]Qa4=q(btm){*}", [], returncode=1)

    def test_214_take_ascii_15_r_promote_target_06_repeat_09_force_one_up(
        self,
    ):
        self.verify("[x]Qa4=q(btm){+}", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_01_plain(self):
        self.verify(
            "r[x]N=Q(btm)",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test_214_take_ascii_16_lr_promote_target_04_lhs_01_plus(self):
        self.verify("2+e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_02_minus_01_no_space(
        self,
    ):
        self.verify("2-e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_02_minus_02_space(
        self,
    ):
        self.verify("2- e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_03_multiply(self):
        self.verify("2*e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_04_divide(self):
        self.verify("2/e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_05_mod_01_no_space(
        self,
    ):
        self.verify("2%e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_05_mod_02_space(self):
        self.verify("2% e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_06_equals(self):
        self.verify("2==e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_07_gt(self):
        self.verify("2>e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_08_ge(self):
        self.verify("2>=e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_09_lt_01_no_space(
        self,
    ):
        self.verify("2<e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_09_lt_02_space(self):
        self.verify("2< e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_10_le(self):
        self.verify("2<=e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_11_ne(self):
        self.verify("2!=e2[x]Qa4=q(btm)", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_04_lhs_12_and(self):
        self.verify(
            "2 and e2[x]Qa4=q(btm)",
            [
                (3, "And"),
                (4, "Integer"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_16_lr_promote_target_04_lhs_13_or(self):
        self.verify(
            "2 or e2[x]Qa4=q(btm)",
            [
                (3, "Or"),
                (4, "Integer"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
            ],
        )

    def test_214_take_ascii_16_lr_promote_target_05_rhs_01_plus(self):
        self.verify("e2[x]Qa4=q(btm)+2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_02_minus(self):
        self.verify(
            "e2[x]Qa4=q(btm)-2",
            [
                (3, "TakeLR"),
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

    def test_214_take_ascii_16_lr_promote_target_05_rhs_03_multiply(self):
        self.verify("e2[x]Qa4=q(btm)*2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_04_divide(self):
        self.verify("e2[x]Qa4=q(btm)/2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_05_mod_01_no_space(
        self,
    ):
        self.verify("e2[x]Qa4=q(btm)%2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_05_mod_02_space(self):
        self.verify("e2[x]Qa4=q(btm) %2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_06_equals(self):
        self.verify("e2[x]Qa4=q(btm)==2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_07_gt(self):
        self.verify("e2[x]Qa4=q(btm)>2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_08_ge(self):
        self.verify("e2[x]Qa4=q(btm)>=2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_09_lt_01_no_space(
        self,
    ):
        self.verify("e2[x]Qa4=q(btm)<2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_09_lt_02_space(self):
        self.verify("e2[x]Qa4=q(btm) <2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_10_le(self):
        self.verify("e2[x]Qa4=q(btm)<=2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_11_ne(self):
        self.verify("e2[x]Qa4=q(btm)!=2", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_05_rhs_12_and_01_plain(self):
        self.verify(
            "e2[x]Qa4=q(btm) and 2",
            [
                (3, "And"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_16_lr_promote_target_05_rhs_12_and_02_parentheses(
        self,
    ):
        self.verify(
            "(e2[x]Qa4=q(btm)) and 2",
            [
                (3, "And"),
                (4, "ParenthesisLeft"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_16_lr_promote_target_05_rhs_13_or_01_plain(self):
        self.verify(
            "e2[x]Qa4=q(btm) or 2",
            [
                (3, "Or"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_16_lr_promote_target_05_rhs_13_or_02_parentheses(
        self,
    ):
        self.verify(
            "(e2[x]Qa4=q(btm)) or 2",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "AssignPromotion"),
                (7, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "BTM"),
                (4, "Integer"),
            ],
        )

    def test_214_take_ascii_16_lr_promote_target_06_repeat_01_zero_up(self):
        self.verify("e2[x]Qa4=q(btm)*", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_06_repeat_02_one_up(self):
        self.verify("e2[x]Qa4=q(btm)+", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_06_repeat_03_optional(self):
        self.verify("e2[x]Qa4=q(btm)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_214_take_ascii_16_lr_promote_target_06_repeat_04_exact(self):
        self.verify_declare_fail(
            "e2[x]Qa4=q(btm){5}",
            [
                (3, "TakeLR"),
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

    def test_214_take_ascii_16_lr_promote_target_06_repeat_05_range(self):
        self.verify("e2[x]Qa4=q(btm){3,5}", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_06_repeat_06_up_to(self):
        self.verify("e2[x]Qa4=q(btm){,5}", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_06_repeat_07_and_over(self):
        self.verify("e2[x]Qa4=q(btm){3,}", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_06_repeat_08_force_zero_up(
        self,
    ):
        self.verify("e2[x]Qa4=q(btm){*}", [], returncode=1)

    def test_214_take_ascii_16_lr_promote_target_06_repeat_09_force_one_up(
        self,
    ):
        self.verify("e2[x]Qa4=q(btm){+}", [], returncode=1)

    def test_214_take_ascii_17_not_01_implicit_lhs(self):
        self.verify(
            "not [x]",
            [(3, "Not"), (4, "TakeII"), (5, "AnySquare"), (5, "AnySquare")],
        )

    def test_214_take_ascii_17_not_02_given_lhs(self):
        self.verify(
            "not q[x]",
            [
                (3, "Not"),
                (4, "TakeLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_18_or_01_implicit_lhs_01_space(self):
        self.verify("b| [x]", [], returncode=1)

    def test_214_take_ascii_18_or_01_implicit_lhs_02_nospace(self):
        self.verify("b|[x]", [], returncode=1)

    def test_214_take_ascii_18_or_02_given_lhs(self):
        self.verify(
            "b|q[x]",
            [
                (3, "TakeLI"),
                (4, "Union"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_214_take_ascii_19_colon_01_implicit_lhs_01_space(self):
        self.verify(
            "currentposition: [x]",
            [
                (3, "Colon"),
                (4, "CurrentPosition"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_19_colon_01_implicit_lhs_02_nospace(self):
        self.verify(
            "currentposition:[x]",
            [
                (3, "Colon"),
                (4, "CurrentPosition"),
                (4, "TakeII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_214_take_ascii_19_colon_02_given_lhs(self):
        self.verify(
            "currentposition:q[x]",
            [
                (3, "TakeLI"),
                (4, "Colon"),
                (5, "CurrentPosition"),
                (5, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_214_take_ascii_20_or_01_implicit_rhs_01_space(self):
        self.verify("[x] |b", [], returncode=1)

    def test_214_take_ascii_20_or_01_implicit_rhs_02_nospace(self):
        self.verify("[x]|b", [], returncode=1)

    def test_214_take_ascii_20_or_02_given_rhs(self):
        self.verify(
            "[x]q|b",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "Union"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_20_or_03_given_rhs_and_lhs(self):
        self.verify(
            "R[x]q|b",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "Union"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_20_or_04_implicit_rhs_given_lhs(self):
        self.verify("R[x] |b", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_01_implicit_01_dash_ascii(self):
        self.verify("[x]--", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_01_implicit_02_dash_utf8(self):
        self.verify("[x]――", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_01_implicit_03_take_ascii(self):
        self.verify("[x][x]", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_01_implicit_04_take_utf8(self):
        self.verify("[x]×", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_02_given_01_piecedesignator(self):
        self.verify("[x]k[x]", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_02_given_02_set(self):
        self.verify("[x]to[x]", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_02_given_03_compoundset(self):
        self.verify("[x]{1 k}[x]", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_02_given_04_parenthesizedset(self):
        self.verify("[x](k)[x]", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_02_given_05_parenthesizedset(self):
        self.verify("[x](k)[x]", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_02_given_06_and_01_no_spaces(self):
        self.verify("[x]and[x]", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_02_given_06_and_02_left_space(self):
        self.verify("[x] and[x]", [], returncode=1)

    def test_214_take_ascii_21_ambiguous_02_given_06_and_03_right_space(self):
        self.verify_tolerant("[x]and [x]", [])

    def test_214_take_ascii_22_target_filter_type_01_default(self):
        con = self.verify(
            "[x]",
            [(3, "TakeII"), (4, "AnySquare"), (4, "AnySquare")],
        )
        self.assertEqual(
            con.children[-1].children[-1].filter_type
            is cqltypes.FilterType.LOGICAL,
            True,
        )

    def test_214_take_ascii_22_target_filter_type_02_logical(self):
        con = self.verify(
            "[x](to btm)",
            [
                (3, "TakeII"),
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

    def test_214_take_ascii_22_target_filter_type_03_integer(self):
        con = self.verify(
            "[x](btm 4)",
            [
                (3, "TakeII"),
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

    def test_214_take_ascii_22_target_filter_type_04_string(self):
        con = self.verify(
            '[x](btm "hi")',
            [
                (3, "TakeII"),
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

    def test_214_take_ascii_22_target_filter_type_05_set(self):
        con = self.verify(
            "[x](btm to)",
            [
                (3, "TakeII"),
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

    def test_214_take_ascii_22_target_filter_type_06_position(self):
        con = self.verify(
            "[x](btm currentposition)",
            [
                (3, "TakeII"),
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
        runner().run(loader(FilterTakeASCII))
