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

    def test_214_captures_ascii_01(self):
        self.verify(
            "[x]",
            [(3, "TakeII"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test_214_captures_ascii_02_left(self):
        self.verify(
            "e2[x]",
            [
                (3, "TakeLI"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test_214_captures_ascii_03_right(self):
        self.verify(
            "[x]Qa4",
            [
                (3, "TakeIR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_214_captures_ascii_04_left_right(self):
        self.verify(
            "r[x]Qa4",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_214_captures_ascii_05_promote_01(self):
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

    def test_214_captures_ascii_05_promote_02(self):  # chessql accepts.
        self.verify("[x]=qa5", [], returncode=1)

    def test_214_captures_ascii_05_promote_03(self):  # chessql accepts.
        self.verify("[x]=check", [], returncode=1)

    def test_214_captures_ascii_06_left_promote_01(self):
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

    def test_214_captures_ascii_06_left_promote_02(self):  # chessql accepts.
        self.verify("e2[x]=bc6", [], returncode=1)

    def test_214_captures_ascii_06_left_promote_03(self):  # chessql accepts.
        self.verify("e2[x]=check", [], returncode=1)

    def test_214_captures_ascii_07_right_promote_01(self):  # chessql wrong.
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

    def test_214_captures_ascii_07_right_promote_02(self):
        self.verify("[x]Qa4=bc6", [], returncode=1)

    def test_214_captures_ascii_07_right_promote_03(self):
        self.verify("[x]Qa4=check", [], returncode=1)

    def test_214_captures_ascii_08_left_right_promote_01(self):  # wrong.
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

    def test_214_captures_ascii_08_left_right_promote_02(self):
        self.verify("r[x]Qa4=bc6", [], returncode=1)

    def test_214_captures_ascii_08_left_right_promote_03(self):
        self.verify("r[x]Qa4=check", [], returncode=1)

    def test_214_captures_ascii_09_target(self):  # chessql wrong.
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

    def test_214_captures_ascii_10_left_target(self):  # chessql wrong.
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

    def test_214_captures_ascii_11_right_target(self):  # chessql wrong.
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

    def test_214_captures_ascii_12_left_right_target(self):  # chessql wrong.
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

    def test_214_captures_ascii_13_promote_target(self):  # chessql wrong.
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

    def test_214_captures_ascii_14_promote_left_target(self):  # wrong.
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

    def test_214_captures_ascii_15_promote_right_target(self):  # wrong.
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

    def test_214_captures_ascii_16_promote_left_right_target(self):  # wrong.
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


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterCapturesASCII))
