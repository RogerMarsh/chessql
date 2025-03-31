# test_filter_captures_ascii.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for '[x]' filter (called 'captures'?).

Equivalent to '×' ("\u00d7").

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterCapturesASCII(verify.Verify):

    def test_214_take_ascii_01(self):
        self.verify(
            "[x]",
            [(3, "TakeII"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test_214_take_ascii_02_left(self):
        self.verify(
            "e2[x]",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_214_take_ascii_03_right(self):
        self.verify(
            "[x]Qa4",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_214_take_ascii_04_left_right(self):
        self.verify(
            "r[x]Qa4",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

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

    def test_214_take_ascii_09_target(self):
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

    def test_214_take_ascii_10_left_target(self):
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

    def test_214_take_ascii_11_right_target(self):
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

    def test_214_take_ascii_12_left_right_target(self):
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

    def test_214_take_ascii_13_promote_target(self):
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

    def test_214_take_ascii_14_promote_left_target(self):
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

    def test_214_take_ascii_15_promote_right_target(self):
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

    def test_214_take_ascii_16_promote_left_right_target(self):
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


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterCapturesASCII))
