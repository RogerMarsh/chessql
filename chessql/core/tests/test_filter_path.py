# test_filter_path.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'path' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterPath(verify.Verify):

    def test_087_path_01_01(self):  # chessql accepts this.
        self.verify("path", [], returncode=1)

    def test_087_path_01_02(self):
        self.verify(
            "path --",
            [
                (3, "Path"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_01_03(self):
        self.verify("path k", [(3, "Path"), (4, "PieceDesignator")])

    def test_087_path_01_04(self):
        self.verify(
            "path (--)",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "SingleMove"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_087_path_01_05(self):
        self.verify(
            "path (k)",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "PieceDesignator"),
            ],
        )

    def test_087_path_01_06_star(self):
        self.verify(
            "path -- *",
            [
                (3, "Path"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "StarRepeat"),
            ],
        )

    def test_087_path_01_07_star(self):  # chessql accepts this.
        self.verify("path k *", [], returncode=1)

    def test_087_path_01_08_star(self):
        self.verify(
            "path (--) *",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "SingleMove"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "StarRepeat"),
            ],
        )

    def test_087_path_01_09_star(self):
        self.verify(
            "path (k) *",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "PieceDesignator"),
                (4, "StarRepeat"),
            ],
        )

    def test_087_path_01_10_plus(self):
        self.verify(
            "path -- +",
            [
                (3, "Path"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PlusRepeat"),
            ],
        )

    def test_087_path_01_11_plus(self):  # chessql accepts this.
        self.verify("path k +", [], returncode=1)

    def test_087_path_01_12_plus(self):
        self.verify(
            "path (--) +",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "SingleMove"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "PlusRepeat"),
            ],
        )

    def test_087_path_01_13_plus(self):
        self.verify(
            "path (k) +",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "PieceDesignator"),
                (4, "PlusRepeat"),
            ],
        )

    def test_087_path_01_14_question(self):
        self.verify(
            "path -- ?",
            [
                (3, "Path"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RepeatZeroOrOne"),
            ],
        )

    def test_087_path_01_15_question(self):  # chessql accepts this.
        self.verify("path k ?", [], returncode=1)

    def test_087_path_01_16_question(self):
        self.verify(
            "path (--) ?",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "SingleMove"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "RepeatZeroOrOne"),
            ],
        )

    def test_087_path_01_17_question(self):
        self.verify(
            "path (k) ?",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "PieceDesignator"),
                (4, "RepeatZeroOrOne"),
            ],
        )

    def test_087_path_01_18_braced(self):  # chessql gets this wrong.
        self.verify(
            "path -- {1,3}",
            [
                (3, "Path"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (5, "RangeInteger"),
                (5, "RangeInteger"),
            ],
        )

    def test_087_path_01_19_braced(self):  # chessql accepts this.
        self.verify("path k {1,3}", [], returncode=1)

    def test_087_path_01_20_braced(self):  # chessql gets this wrong.
        self.verify(
            "path (--) {1,3}",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "SingleMove"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "RegexRepeat"),
                (5, "RangeInteger"),
                (5, "RangeInteger"),
            ],
        )

    def test_087_path_01_21_braced(self):  # chessql gets this wrong.
        self.verify(
            "path (k) {1,3}",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "PieceDesignator"),
                (4, "RegexRepeat"),
                (5, "RangeInteger"),
                (5, "RangeInteger"),
            ],
        )

    def ytest_087_path_01_nn(self):
        self.verify("path k+", [])

    def ytest_087_path_01_nn(self):
        self.verify("path k?", [])

    def ytest_087_path_01_nn(self):
        self.verify("path k{1,3}", [])

    def test_087_path_02(self):  # chessql accepts this.
        self.verify("path primary", [], returncode=1)

    def test_087_path_03(self):  # chessql accepts this.
        self.verify("path focus", [], returncode=1)

    def test_087_path_04(self):  # chessql accepts this.
        self.verify("path focus b", [], returncode=1)

    def test_087_path_05(self):  # chessql accepts this.
        self.verify("path focus capture", [], returncode=1)

    def test_087_path_06(self):  # chessql accepts this.
        self.verify("path focus capture r", [], returncode=1)

    def test_087_path_07(self):  # chessql accepts this.
        self.verify("path max", [], returncode=1)

    def test_087_path_08(self):  # chessql accepts this.
        self.verify("path max 4", [], returncode=1)

    def test_087_path_09(self):  # chessql accepts this.
        self.verify("path verbose", [], returncode=1)

    def test_087_path_10(self):  # chessql accepts this.
        self.verify("path keepallbest", [], returncode=1)

    def test_087_path_11(self):  # chessql accepts this.
        self.verify("path title", [], returncode=1)

    def test_087_path_12(self):  # chessql accepts this.
        self.verify('path title "Head"', [], returncode=1)

    def test_087_path_13(self):  # chessql accepts this.
        self.verify("path piecepath", [], returncode=1)

    def test_087_path_14(self):  # chessql accepts this.
        self.verify("path quiet", [], returncode=1)

    def test_087_path_15(self):  # chessql accepts this.
        self.verify("path nestban", [], returncode=1)

    def test_087_path_16(self):  # chessql accepts this.
        self.verify("path firstmatch", [], returncode=1)

    def test_087_path_17(self):  # chessql accepts this.
        self.verify("path lastposition", [], returncode=1)

    def test_189_plus_01_force_repeat(self):
        self.verify("{+}", [], returncode=1)

    def test_189_plus_12_repetition_path_01(self):  # wrong.
        self.verify(
            "path --(K)+",
            [
                (3, "Path"),
                (4, "SingleMoveR"),  # wrong.
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "PieceDesignator"),
                (4, "PlusRepeat"),
            ],
        )

    def test_189_plus_12_repetition_path_02(self):  # wrong.
        self.verify(
            "path --(K){+}",
            [
                (3, "Path"),
                (4, "SingleMoveR"),  # wrong.
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "PieceDesignator"),
                (4, "WildcardPlus"),
            ],
        )

    def test_189_plus_13_repetition_path_01(self):  # wrong.
        self.verify(
            "path -- K+",
            [
                (3, "Path"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),  # wrong.
                (4, "PlusRepeat"),
            ],
        )

    def test_189_plus_13_repetition_path_02(self):  # wrong.
        self.verify(
            "path -- K{+}",
            [
                (3, "Path"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),  # wrong.
                (4, "WildcardPlus"),
            ],
        )

    def test_190_star_01_force_repeat(self):
        self.verify("{*}", [], returncode=1)

    def test_190_star_11_repetition_path(self):  # wrong.
        self.verify(
            "path --(K)*",
            [
                (3, "Path"),
                (4, "SingleMoveR"),  # wrong.
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "PieceDesignator"),
                (4, "StarRepeat"),
            ],
        )

    def test_190_star_12_repetition_path(self):  # wrong.
        self.verify(
            "path -- K*",
            [
                (3, "Path"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),  # wrong.
                (4, "StarRepeat"),
            ],
        )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterPath))
