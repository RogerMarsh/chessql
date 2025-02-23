# test_filter_dash.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for '--' filter (called 'dash').

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterDash(verify.Verify):

    def test__147_dash_01_ascii(self):
        self.verify(
            "--",
            [(3, "SingleMove"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test__147_dash_01_utf8(self):
        self.verify(
            "――",
            [(3, "SingleMove"), (4, "AnySquare"), (4, "AnySquare")],
        )

    def test__147_dash_02_left_ascii(self):
        self.verify(
            "e2--",
            [
                (3, "SingleMoveL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test__147_dash_02_left_utf8(self):
        self.verify(
            "e2――",
            [
                (3, "SingleMoveL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
            ],
        )

    def test__147_dash_03_right_ascii(self):
        self.verify(
            "--Qa4",
            [
                (3, "SingleMoveR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test__147_dash_03_right_utf8(self):
        self.verify(
            "――Qa4",
            [
                (3, "SingleMoveR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test__147_dash_04_left_right_ascii(self):
        self.verify(
            "r--Qa4",
            [
                (3, "SingleMoveLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test__147_dash_04_left_right_utf8(self):
        self.verify(
            "r――Qa4",
            [
                (3, "SingleMoveLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test__147_dash_05_promote_ascii_01(self):
        self.verify(
            "--=q",
            [
                (3, "SingleMove"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__147_dash_05_promote_ascii_02(self):  # chessql accepts.
        self.verify("--=qa5", [], returncode=1)

    def test__147_dash_05_promote_ascii_03(self):  # chessql accepts.
        self.verify("--=check", [], returncode=1)

    def test__147_dash_05_promote_utf8_01(self):
        self.verify(
            "――=q",
            [
                (3, "SingleMove"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__147_dash_05_promote_utf8_02(self):  # chessql accepts.
        self.verify("――=qa5", [], returncode=1)

    def test__147_dash_05_promote_utf8_03(self):  # chessql accepts.
        self.verify("――=check", [], returncode=1)

    def test__147_dash_06_left_promote_ascii_01(self):
        self.verify(
            "e2--=b",
            [
                (3, "SingleMoveL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__147_dash_06_left_promote_ascii_02(self):  # chessql accepts.
        self.verify("e2--=bc6", [], returncode=1)

    def test__147_dash_06_left_promote_ascii_03(self):  # chessql accepts.
        self.verify("e2--=check", [], returncode=1)

    def test__147_dash_06_left_promote_utf8_01(self):
        self.verify(
            "e2――=b",
            [
                (3, "SingleMoveL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__147_dash_06_left_promote_utf8_02(self):  # chessql accepts.
        self.verify("e2--=bc6", [], returncode=1)

    def test__147_dash_06_left_promote_utf8_03(self):  # chessql accepts.
        self.verify("e2--=check", [], returncode=1)

    def test__147_dash_07_right_promote_ascii_01(self):  # chessql wrong.
        self.verify(
            "--Qa4=N",
            [
                (3, "SingleMoveR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__147_dash_07_right_promote_ascii_02(self):
        self.verify("--Qa4=bc6", [], returncode=1)

    def test__147_dash_07_right_promote_ascii_03(self):
        self.verify("--Qa4=check", [], returncode=1)

    def test__147_dash_07_right_promote_utf8_01(self):  # chessql wrong.
        self.verify(
            "――Qa4=N",
            [
                (3, "SingleMoveR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__147_dash_07_right_promote_utf8_02(self):
        self.verify("――Qa4=bc6", [], returncode=1)

    def test__147_dash_07_right_promote_utf8_03(self):
        self.verify("――Qa4=check", [], returncode=1)

    def test__147_dash_08_left_right_promote_ascii_01(self):  # chessql wrong.
        self.verify(
            "r--Qa4=R",
            [
                (3, "SingleMoveLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__147_dash_08_left_right_promote_ascii_02(self):
        self.verify("r--Qa4=bc6", [], returncode=1)

    def test__147_dash_08_left_right_promote_ascii_03(self):
        self.verify("r--Qa4=check", [], returncode=1)

    def test__147_dash_08_left_right_promote_utf8_01(self):  # chessql wrong.
        self.verify(
            "r――Qa4=R",
            [
                (3, "SingleMoveLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
            ],
        )

    def test__147_dash_08_left_right_promote_utf8_02(self):
        self.verify("r――Qa4=bc6", [], returncode=1)

    def test__147_dash_08_left_right_promote_utf8_03(self):
        self.verify("r――Qa4=check", [], returncode=1)

    def test__147_dash_09_target_ascii(self):  # chessql wrong.
        self.verify(
            "--(btm)",
            [
                (3, "SingleMove"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_09_target_utf8(self):  # chessql wrong.
        self.verify(
            "――(btm)",
            [
                (3, "SingleMove"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_10_left_target_ascii(self):  # chessql wrong.
        self.verify(
            "P--(btm)",
            [
                (3, "SingleMoveL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_10_left_target_utf8(self):  # chessql wrong.
        self.verify(
            "P――(btm)",
            [
                (3, "SingleMoveL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_11_right_target_ascii(self):  # chessql wrong.
        self.verify(
            "--N(btm)",
            [
                (3, "SingleMoveR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_11_right_target_utf8(self):  # chessql wrong.
        self.verify(
            "――N(btm)",
            [
                (3, "SingleMoveR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_12_left_right_target_ascii(self):  # chessql wrong.
        self.verify(
            "r--N(btm)",
            [
                (3, "SingleMoveLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_12_left_right_target_utf8(self):  # chessql wrong.
        self.verify(
            "r――N(btm)",
            [
                (3, "SingleMoveLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_13_promote_target_ascii(self):  # chessql wrong.
        self.verify(
            "--=Q(btm)",
            [
                (3, "SingleMove"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_13_promote_target_utf8(self):  # chessql wrong.
        self.verify(
            "――=Q(btm)",
            [
                (3, "SingleMove"),
                (4, "AnySquare"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_14_promote_left_target_ascii(self):  # chessql wrong.
        self.verify(
            "P--=Q(btm)",
            [
                (3, "SingleMoveL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_14_promote_left_target_utf8(self):  # chessql wrong.
        self.verify(
            "P――=Q(btm)",
            [
                (3, "SingleMoveL"),
                (4, "PieceDesignator"),
                (4, "AnySquare"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_15_promote_right_target_ascii(self):  # chessql wrong.
        self.verify(
            "--N=Q(btm)",
            [
                (3, "SingleMoveR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_15_promote_right_target_utf8(self):  # chessql wrong.
        self.verify(
            "――N=Q(btm)",
            [
                (3, "SingleMoveR"),
                (4, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_16_promote_left_right_target_ascii(
        self,
    ):  # chessql wrong.
        self.verify(
            "r--N=Q(btm)",
            [
                (3, "SingleMoveLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "AssignPromotion"),
                (5, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "BTM"),
            ],
        )

    def test__147_dash_16_promote_left_right_target_utf8(
        self,
    ):  # chessql wrong.
        self.verify(
            "r――N=Q(btm)",
            [
                (3, "SingleMoveLR"),
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
    runner().run(loader(FilterDash))
