# test_filter_dash_utf8.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for '――' filter (called 'dash').

This is "\u2015\u2015" and is equivalent to '――'.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterDashUTF8(verify.Verify):

    def test_148_dash_utf8_01(self):
        self.verify(
            "――",
            [(3, "DashII"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test_148_dash_utf8_02_left(self):
        self.verify(
            "e2――",
            [
                (3, "DashLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_148_dash_utf8_03_right(self):
        self.verify(
            "――Qa4",
            [
                (3, "DashIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_148_dash_utf8_04_left_right(self):
        self.verify(
            "r――Qa4",
            [
                (3, "DashLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

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

    def test_148_dash_utf8_09_target(self):
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

    def test_148_dash_utf8_10_left_target(self):
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

    def test_148_dash_utf8_11_right_target(self):
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

    def test_148_dash_utf8_12_left_right_target(self):
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

    def test_148_dash_utf8_13_promote_target(self):
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

    def test_148_dash_utf8_14_promote_left_target(self):
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

    def test_148_dash_utf8_15_promote_right_target(self):
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

    def test_148_dash_utf8_16_promote_left_right_target(self):
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

    def test_148_dash_utf8_18_or_01_implicit_lhs(self):
        self.verify("b| ――", [], returncode=1)

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

    def test_148_dash_utf8_19_colon_01_implicit_lhs(self):
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

    def test_148_dash_utf8_20_or_01_implicit_rhs(self):
        self.verify("―― |b", [], returncode=1)

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


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterDashUTF8))
