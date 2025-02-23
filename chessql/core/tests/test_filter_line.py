# test_filter_line.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'line' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterLine(verify.Verify):

    def test__062_line_01(self):  # chessql accepts this.
        self.verify("line", [], returncode=1)

    def test__062_line_02(self):
        self.verify("line -->", [], returncode=1)

    def test__062_line_03(self):
        self.verify(
            "line --> check",
            [(3, "Line"), (4, "ArrowForward"), (5, "Check")],
        )

    def test__062_line_04(self):
        self.verify("line --> check -->", [], returncode=1)

    def test__062_line_05(self):
        self.verify(
            "line --> check --> check",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test__062_line_06(self):
        self.verify("line --> check <--", [], returncode=1)

    def test__062_line_07(self):
        self.verify("line --> check <-- check", [], returncode=1)

    def test__062_line_08(self):
        self.verify("line <--", [], returncode=1)

    def test__062_line_09(self):
        self.verify(
            "line <-- check",
            [(3, "Line"), (4, "ArrowBackward"), (5, "Check")],
        )

    def test__062_line_10(self):
        self.verify("line <-- check <--", [], returncode=1)

    def test__062_line_11(self):
        self.verify(
            "line <-- check <-- check",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (4, "ArrowBackward"),
                (5, "Check"),
            ],
        )

    def test__062_line_12(self):
        self.verify("line <-- check -->", [], returncode=1)

    def test__062_line_13(self):
        self.verify("line <-- check --> check", [], returncode=1)

    def test__062_line_14(self):
        self.verify(
            "line --> .",
            [(3, "Line"), (4, "ArrowForward"), (5, "AnySquare")],
        )

    def test__062_line_15(self):
        self.verify(
            "line --> .*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "AnySquare"),
                (5, "StarRepeat"),
            ],
        )

    def test__062_line_16(self):
        self.verify(
            "line --> check+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "PlusRepeat"),
            ],
        )

    def test__062_line_17(self):
        self.verify(
            "line --> check?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test__062_line_18(self):  # chessql gets this wrong.
        self.verify(
            "line --> check{2,4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "RegexRepeat"),
                (6, "Integer"),  # Missing.
                (6, "Integer"),  # Missing.
            ],
        )

    def test__062_line_19(self):
        self.verify(
            "line --> (check --> r)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "PieceDesignator"),
            ],
        )

    def test__062_line_20(self):
        self.verify(
            "line --> (check --> r)+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "PieceDesignator"),
                (5, "PlusRepeat"),
            ],
        )

    def test__062_line_21(self):
        self.verify(
            "line <-- .",
            [(3, "Line"), (4, "ArrowBackward"), (5, "AnySquare")],
        )

    def test__062_line_22(self):
        self.verify(
            "line <-- .*",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "AnySquare"),
                (5, "StarRepeat"),
            ],
        )

    def test__062_line_23(self):
        self.verify(
            "line <-- check+",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "PlusRepeat"),
            ],
        )

    def test__062_line_24(self):
        self.verify(
            "line <-- check?",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test__062_line_25(self):  # chessql gets this wrong.
        self.verify(
            "line <-- check{2,4}",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RegexRepeat"),
                (6, "Integer"),  # Missing.
                (6, "Integer"),  # Missing.
            ],
        )

    def test__062_line_26(self):
        self.verify(
            "line <-- (check <-- r)",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowBackward"),
                (7, "PieceDesignator"),
            ],
        )

    def test__062_line_27(self):
        self.verify(
            "line <-- (check <-- r)+",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowBackward"),
                (7, "PieceDesignator"),
                (5, "PlusRepeat"),
            ],
        )

    def test__062_line_28(self):  # chessql gets this wrong.
        self.verify("line --> (check <-- r)+", [], returncode=1)

    def test__062_line_29(self):  # chessql gets this wrong.
        self.verify("line <-- (check --> r)+", [], returncode=1)

    def test__062_line_30(self):  # chessql gives wrong Exception.
        self.verify("line primary secondary --> check", [], returncode=1)

    def test__062_line_31(self):  # chessql gets this wrong.
        self.verify(
            "line primary --> check",
            [(3, "Line"), (4, "Primary"), (4, "ArrowForward"), (5, "Check")],
        )

    def test__062_line_32(self):  # chessql gets this wrong.
        self.verify(
            "line secondary --> check",
            [(3, "Line"), (4, "Secondary"), (4, "ArrowForward"), (5, "Check")],
        )

    def test__062_line_33(self):
        self.verify(
            "line firstmatch --> check",
            [
                (3, "Line"),
                (4, "FirstMatch"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test__062_line_34(self):
        self.verify(
            "line lastposition --> check",
            [
                (3, "Line"),
                (4, "LastPosition"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test__062_line_35(self):
        self.verify(
            "line singlecolor --> check",
            [
                (3, "Line"),
                (4, "SingleColor"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test__062_line_36(self):
        self.verify(
            "line quiet --> check",
            [(3, "Line"), (4, "Quiet"), (4, "ArrowForward"), (5, "Check")],
        )

    def test__062_line_37(self):
        self.verify(
            "line nestban --> check",
            [(3, "Line"), (4, "NestBan"), (4, "ArrowForward"), (5, "Check")],
        )

    def test__062_line_38(self):
        self.verify(
            "line singlecolor nestban quiet lastposition --> check",
            [
                (3, "Line"),
                (4, "SingleColor"),
                (4, "NestBan"),
                (4, "Quiet"),
                (4, "LastPosition"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test__062_line_39(self):
        self.verify(
            "line 1 3 --> check",
            [
                (3, "Line"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test__062_line_40(self):
        self.verify(
            "line quiet 1 3 firstmatch --> check",
            [
                (3, "Line"),
                (4, "Quiet"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "FirstMatch"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_41(self):
        self.verify(
            "line quiet 1 3 firstmatch <-- check",
            [
                (3, "Line"),
                (4, "Quiet"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "FirstMatch"),
                (4, "ArrowBackward"),
                (5, "Check"),
            ],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterLine))
