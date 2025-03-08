# test_filter_move.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'move' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterMove(verify.Verify):

    def test_074_move_01(self):
        self.verify("move", [(3, "Move")])

    def test_074_move_02(self):
        self.verify("move capture", [], returncode=1)

    def test_074_move_03(self):
        self.verify("move castle", [(3, "Move"), (4, "CastleParameter")])

    def test_074_move_04(self):
        self.verify("move comment", [], returncode=1)

    def test_074_move_05(self):  # chessql accepts this.
        self.verify("move count", [], returncode=1)

    def test_074_move_06(self):
        self.verify("move enpassant", [(3, "Move"), (4, "EnPassantParameter")])

    def test_074_move_07(self):  # chessql accepts this.
        self.verify("move enpassantsquare", [], returncode=1)

    def test_074_move_08(self):
        self.verify("move from", [], returncode=1)

    def test_074_move_09(self):
        self.verify("move legal", [(3, "Move"), (4, "LegalParameter")])

    def test_074_move_10(self):
        self.verify("move null", [(3, "Move"), (4, "Null")])

    def test_074_move_11(self):
        self.verify("move o-o", [(3, "Move"), (4, "OOParameter")])

    def test_074_move_12(self):
        self.verify("move o-o-o", [(3, "Move"), (4, "OOOParameter")])

    def test_074_move_13(self):
        self.verify("move previous", [(3, "Move"), (4, "Previous")])

    def test_074_move_14(self):
        self.verify("move primary", [(3, "Move"), (4, "PrimaryParameter")])

    def test_074_move_15(self):
        self.verify("move promote", [], returncode=1)

    def test_074_move_16(self):
        self.verify(
            "move pseudolegal", [(3, "Move"), (4, "PseudolegalParameter")]
        )

    def test_074_move_17(self):
        self.verify("move secondary", [(3, "Move"), (4, "SecondaryParameter")])

    def test_074_move_18(self):
        self.verify("move to", [], returncode=1)

    def test_074_move_19(self):
        self.verify(
            "move capture P",
            [(3, "Move"), (4, "Capture"), (5, "PieceDesignator")],
        )

    def test_074_move_20(self):
        self.verify(
            'move comment ("Any move")',
            [(3, "Move"), (4, "CommentParenthesesParameter"), (5, "String")],
        )

    def test_074_move_21(self):  # chessql gets this wrong. (I think.)
        self.verify(
            'move legal comment ("Any move")',
            [
                (3, "Move"),
                (4, "LegalParameter"),
                (3, "CommentParenthesesParameter"),
                (4, "String"),
            ],
        )

    def test_074_move_22(self):  # chessql gets this wrong. (I think.)
        self.verify(
            'move pseudolegal comment ("Any move")',
            [
                (3, "Move"),
                (4, "PseudolegalParameter"),
                (3, "CommentParenthesesParameter"),
                (4, "String"),
            ],
        )

    def test_074_move_23(self):
        self.verify(
            "move count legal",
            [(3, "Move"), (4, "Count"), (4, "LegalParameter")],
        )

    def test_074_move_24(self):
        self.verify(
            "move count pseudolegal",
            [(3, "Move"), (4, "Count"), (4, "PseudolegalParameter")],
        )

    def test_074_move_25(self):
        self.verify(
            "move legal count",
            [(3, "Move"), (4, "LegalParameter"), (4, "Count")],
        )

    def test_074_move_26(self):
        self.verify(
            "move pseudolegal count",
            [(3, "Move"), (4, "PseudolegalParameter"), (4, "Count")],
        )

    def test_074_move_27(self):  # chessql gets this wrong.
        self.verify(
            "move enpassantsquare d5",
            [
                (3, "Move"),
                (4, "EnPassantSquareParameter"),
                (5, "PieceDesignator"),
            ],
        )

    def test_074_move_28(self):
        self.verify(
            "move from R",
            [(3, "Move"), (4, "FromParameter"), (5, "PieceDesignator")],
        )

    def test_074_move_29(self):
        self.verify(
            "move promote B",
            [(3, "Move"), (4, "Promote"), (5, "PieceDesignator")],
        )

    def test_074_move_30(self):
        self.verify(
            "move to Q",
            [(3, "Move"), (4, "ToParameter"), (5, "PieceDesignator")],
        )

    def test_074_move_31(self):  # wrong after 'pin' changes.
        self.verify(
            "move capture a5 from r to Q",
            [
                (3, "Move"),
                (4, "Capture"),
                (5, "PieceDesignator"),
                (4, "FromParameter"),
                (5, "PieceDesignator"),
                (4, "ToParameter"),
                (5, "PieceDesignator"),
            ],
        )

    def test_074_move_32(self):
        self.verify(
            "move to Q from r capture a5",
            [
                (3, "Move"),
                (4, "ToParameter"),
                (5, "PieceDesignator"),
                (4, "FromParameter"),
                (5, "PieceDesignator"),
                (4, "Capture"),
                (5, "PieceDesignator"),
            ],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterMove))
