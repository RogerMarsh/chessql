# test_filter_captures.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for '[x]' filter (called 'captures'?).

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterCaptures(verify.Verify):

    def test_148_captures_01_ascii(self):
        self.verify(
            "[x]",
            [(3, "Captures"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test_148_captures_01_utf8(self):
        self.verify(
            "×",
            [(3, "Captures"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test__148_captures_02_left_ascii(self):
        self.verify(
            "e2[x]",
            [
                (3, "CapturesL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test__148_captures_02_left_utf8(self):
        self.verify(
            "e2×",
            [
                (3, "CapturesL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test__148_captures_03_right_ascii(self):
        self.verify(
            "[x]Qa4",
            [
                (3, "CapturesR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test__148_captures_03_right_utf8(self):
        self.verify(
            "×Qa4",
            [
                (3, "CapturesR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test__148_captures_04_left_right_ascii(self):
        self.verify(
            "r[x]Qa4",
            [
                (3, "CapturesLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test__148_captures_04_left_right_utf8(self):
        self.verify(
            "r×Qa4",
            [
                (3, "CapturesLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test__148_captures_05_promote_ascii_01(self):
        self.verify(
            "[x]=q",
            [
                (3, "Captures"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__148_captures_05_promote_ascii_02(self):  # chessql accepts.
        self.verify("[x]=qa5", [], returncode=1)

    def test__148_captures_05_promote_ascii_03(self):  # chessql accepts.
        self.verify("[x]=check", [], returncode=1)

    def test__148_captures_05_promote_utf8_01(self):
        self.verify(
            "×=q",
            [
                (3, "Captures"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__148_captures_05_promote_utf8_02(self):  # chessql accepts.
        self.verify("×=qa5", [], returncode=1)

    def test__148_captures_05_promote_utf8_03(self):  # chessql accepts.
        self.verify("×=check", [], returncode=1)

    def test__148_captures_06_left_promote_ascii_01(self):
        self.verify(
            "e2[x]=b",
            [
                (3, "CapturesL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__148_captures_06_left_promote_ascii_02(self):  # chessql accepts.
        self.verify("e2[x]=bc6", [], returncode=1)

    def test__148_captures_06_left_promote_ascii_03(self):  # chessql accepts.
        self.verify("e2[x]=check", [], returncode=1)

    def test__148_captures_06_left_promote_utf8_01(self):
        self.verify(
            "e2×=b",
            [
                (3, "CapturesL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__148_captures_06_left_promote_utf8_02(self):  # chessql accepts.
        self.verify("e2[x]=bc6", [], returncode=1)

    def test__148_captures_06_left_promote_utf8_03(self):  # chessql accepts.
        self.verify("e2[x]=check", [], returncode=1)

    def test__148_captures_07_right_promote_ascii_01(self):  # chessql wrong.
        self.verify(
            "[x]Qa4=N",
            [
                (3, "CapturesR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__148_captures_07_right_promote_ascii_02(self):
        self.verify("[x]Qa4=bc6", [], returncode=1)

    def test__148_captures_07_right_promote_ascii_03(self):
        self.verify("[x]Qa4=check", [], returncode=1)

    def test__148_captures_07_right_promote_utf8_01(self):  # chessql wrong.
        self.verify(
            "×Qa4=N",
            [
                (3, "CapturesR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__148_captures_07_right_promote_utf8_02(self):
        self.verify("×Qa4=bc6", [], returncode=1)

    def test__148_captures_07_right_promote_utf8_03(self):
        self.verify("×Qa4=check", [], returncode=1)

    def test__148_captures_08_left_right_promote_ascii_01(self):  # wrong.
        self.verify(
            "r[x]Qa4=R",
            [
                (3, "CapturesLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__148_captures_08_left_right_promote_ascii_02(self):
        self.verify("r[x]Qa4=bc6", [], returncode=1)

    def test__148_captures_08_left_right_promote_ascii_03(self):
        self.verify("r[x]Qa4=check", [], returncode=1)

    def test__148_captures_08_left_right_promote_utf8_01(self):  # wrong.
        self.verify(
            "r×Qa4=R",
            [
                (3, "CapturesLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__148_captures_08_left_right_promote_utf8_02(self):
        self.verify("r×Qa4=bc6", [], returncode=1)

    def test__148_captures_08_left_right_promote_utf8_03(self):
        self.verify("r×Qa4=check", [], returncode=1)

    def test__148_captures_09_target_ascii(self):  # chessql wrong.
        self.verify(
            "[x](btm)",
            [
                (3, "Captures"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_09_target_utf8(self):  # chessql wrong.
        self.verify(
            "×(btm)",
            [
                (3, "Captures"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_10_left_target_ascii(self):  # chessql wrong.
        self.verify(
            "P[x](btm)",
            [
                (3, "CapturesL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_10_left_target_utf8(self):  # chessql wrong.
        self.verify(
            "P×(btm)",
            [
                (3, "CapturesL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_11_right_target_ascii(self):  # chessql wrong.
        self.verify(
            "[x]N(btm)",
            [
                (3, "CapturesR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_11_right_target_utf8(self):  # chessql wrong.
        self.verify(
            "×N(btm)",
            [
                (3, "CapturesR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_12_left_right_target_ascii(self):  # chessql wrong.
        self.verify(
            "r[x]N(btm)",
            [
                (3, "CapturesLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_12_left_right_target_utf8(self):  # chessql wrong.
        self.verify(
            "r×N(btm)",
            [
                (3, "CapturesLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_13_promote_target_ascii(self):  # chessql wrong.
        self.verify(
            "[x]=Q(btm)",
            [
                (3, "Captures"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_13_promote_target_utf8(self):  # chessql wrong.
        self.verify(
            "×=Q(btm)",
            [
                (3, "Captures"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_14_promote_left_target_ascii(self):  # wrong.
        self.verify(
            "P[x]=Q(btm)",
            [
                (3, "CapturesL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_14_promote_left_target_utf8(self):  # chessql wrong.
        self.verify(
            "P×=Q(btm)",
            [
                (3, "CapturesL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_15_promote_right_target_ascii(self):  # wrong.
        self.verify(
            "[x]N=Q(btm)",
            [
                (3, "CapturesR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_15_promote_right_target_utf8(self):  # wrong.
        self.verify(
            "×N=Q(btm)",
            [
                (3, "CapturesR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_16_promote_left_right_target_ascii(self):  # wrong.
        self.verify(
            "r[x]N=Q(btm)",
            [
                (3, "CapturesLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__148_captures_16_promote_left_right_target_utf8(self):  # wrong.
        self.verify(
            "r×N=Q(btm)",
            [
                (3, "CapturesLR"),
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
    runner().run(loader(FilterCaptures))
