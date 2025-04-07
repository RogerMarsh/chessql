# test_filters_iteration.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for iteration over filters.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FiltersIteration(verify.Verify):

    def test_169_square_ascii_01(self):
        self.verify("[element]", [], returncode=1)

    def test_169_square_ascii_02(self):
        self.verify("x[element]", [], returncode=1)

    def test_169_square_ascii_03(self):
        self.verify("x[element].", [], returncode=1)

    def test_169_square_ascii_04(self):
        self.verify("[element]. k", [], returncode=1)

    def test_169_square_ascii_05(self):
        self.verify("[element]. k", [], returncode=1)

    def test_169_square_ascii_06_set_01_set_01(self):
        self.verify(
            "x[element]. k",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_169_square_ascii_06_set_01_set_02(self):
        self.verify(
            "x [element] . k",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_169_square_ascii_06_set_02_integer(self):
        self.verify(
            "x[element]. 1",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_169_square_ascii_06_set_03_string(self):
        self.verify(
            'x[element]. "w"',
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_169_square_ascii_06_set_04_logical(self):
        self.verify(
            "x[element]. false",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_169_square_ascii_06_set_05_position(self):
        self.verify(
            "x[element]. currentposition",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_169_square_ascii_07_integer_set(self):
        self.verify("x [element] 1 k", [], returncode=1)

    def test_169_square_ascii_08_string_set(self):
        self.verify('x [element] "w" k', [], returncode=1)

    def test_169_square_ascii_09_logical_set(self):
        self.verify("x [element] true k", [], returncode=1)

    def test_169_square_ascii_10_position_set(self):
        self.verify("x [element] currentposition k", [], returncode=1)

    def test_170_square_utf8_01(self):
        self.verify("∊", [], returncode=1)

    def test_170_square_utf8_02(self):
        self.verify("x∊", [], returncode=1)

    def test_170_square_utf8_03(self):
        self.verify("x∊.", [], returncode=1)

    def test_170_square_utf8_04(self):
        self.verify("∊. k", [], returncode=1)

    def test_170_square_utf8_05(self):
        self.verify("∊. k", [], returncode=1)

    def test_170_square_utf8_06_set_01_set_01(self):
        self.verify(
            "x∊. k",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_170_square_utf8_06_set_01_set_02(self):
        self.verify(
            "x ∊ . k",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_170_square_utf8_06_set_02_integer(self):
        self.verify(
            "x∊. 1",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_170_square_utf8_06_set_03_string(self):
        self.verify(
            'x∊. "w"',
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_170_square_utf8_06_set_04_logical(self):
        self.verify(
            "x∊. false",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_170_square_utf8_06_set_05_position(self):
        self.verify(
            "x∊. currentposition",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_170_square_utf8_07_integer_set(self):
        self.verify("x ∊ 1 k", [], returncode=1)

    def test_170_square_utf8_08_string_set(self):
        self.verify('x ∊ "w" k', [], returncode=1)

    def test_170_square_utf8_09_logical_set(self):
        self.verify("x ∊ true k", [], returncode=1)

    def test_170_square_utf8_10_position_set(self):
        self.verify("x ∊ currentposition k", [], returncode=1)

    def test_171_universal_square_ascii_01_01(self):
        self.verify("[forall]", [], returncode=1)

    def test_171_universal_square_ascii_01_02(self):
        self.verify("[forall][element]", [], returncode=1)

    def test_171_universal_square_ascii_02(self):
        self.verify("[forall]x[element]", [], returncode=1)

    def test_171_universal_square_ascii_03(self):
        self.verify("[forall]x[element].", [], returncode=1)

    def test_171_universal_square_ascii_04(self):
        self.verify("[forall][element]. k", [], returncode=1)

    def test_171_universal_square_ascii_05(self):
        self.verify("[forall][element]. k", [], returncode=1)

    def test_171_universal_square_ascii_06(self):
        self.verify("[forall]. k", [], returncode=1)

    def test_171_universal_square_ascii_07_set_01_set_01_no_space(self):
        self.verify(
            "[forall]x[element].k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    # No 'all space' test because it is same as 'allowed space' test.
    def test_171_universal_square_ascii_07_set_01_set_03_allowed_space(self):
        self.verify(
            "[forall] x [element] . k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_171_universal_square_ascii_07_set_01_set_04_missing_space(self):
        self.verify("[forall]x[element]Qk", [], returncode=1)

    def test_171_universal_square_ascii_07_set_01_set_05_forced_space(self):
        self.verify(
            "[forall]x[element]Q k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_171_universal_square_ascii_07_set_02_integer(self):
        self.verify(
            "[forall]x[element]. 1",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_171_universal_square_ascii_07_set_03_string(self):
        self.verify(
            '[forall]x[element]. "w"',
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_171_universal_square_ascii_07_set_04_logical(self):
        self.verify(
            "[forall]x[element]. false",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_171_universal_square_ascii_07_set_05_position(self):
        self.verify(
            "[forall]x[element]. currentposition",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_172_universal_square_utf8_01_01(self):
        self.verify("∀", [], returncode=1)

    def test_172_universal_square_utf8_01_02(self):
        self.verify("∀∊", [], returncode=1)

    def test_172_universal_square_utf8_02(self):
        self.verify("∀x∊", [], returncode=1)

    def test_172_universal_square_utf8_03(self):
        self.verify("∀x∊.", [], returncode=1)

    def test_172_universal_square_utf8_04(self):
        self.verify("∀∊. k", [], returncode=1)

    def test_172_universal_square_utf8_05(self):
        self.verify("∀∊. k", [], returncode=1)

    def test_172_universal_square_utf8_06(self):
        self.verify("∀. k", [], returncode=1)

    def test_172_universal_square_utf8_07_set_01_set_01_no_space(self):
        self.verify(
            "∀x∊.k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    # No 'all space' test because it is same as 'allowed space' test.
    def test_172_universal_square_utf8_07_set_01_set_03_allowed_space(self):
        self.verify(
            "∀ x ∊ . k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_172_universal_square_utf8_07_set_01_set_04_missing_space(self):
        self.verify("∀x∊Qk", [], returncode=1)

    def test_172_universal_square_utf8_07_set_01_set_05_forced_space(self):
        self.verify(
            "∀x∊Q k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_172_universal_square_utf8_07_set_02_integer(self):
        self.verify(
            "∀x∊. 1",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_172_universal_square_utf8_07_set_03_string(self):
        self.verify(
            '∀x∊. "w"',
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_172_universal_square_utf8_07_set_04_logical(self):
        self.verify(
            "∀x∊. false",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_172_universal_square_utf8_07_set_05_position(self):
        self.verify(
            "∀x∊. currentposition",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_173_universal_square_utf8_01_01(self):
        self.verify("∀", [], returncode=1)

    def test_173_universal_square_utf8_01_02(self):
        self.verify("∀[element]", [], returncode=1)

    def test_173_universal_square_utf8_02(self):
        self.verify("∀x[element]", [], returncode=1)

    def test_173_universal_square_utf8_03(self):
        self.verify("∀x[element].", [], returncode=1)

    def test_173_universal_square_utf8_04(self):
        self.verify("∀[element]. k", [], returncode=1)

    def test_173_universal_square_utf8_05(self):
        self.verify("∀[element]. k", [], returncode=1)

    def test_173_universal_square_utf8_06(self):
        self.verify("∀. k", [], returncode=1)

    def test_173_universal_square_utf8_07_set_01_set_01(self):
        self.verify(
            "∀x[element]. k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_173_universal_square_utf8_07_set_01_set_02(self):
        self.verify(
            "∀ x [element] . k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_173_universal_square_utf8_07_set_02_integer(self):
        self.verify(
            "∀x[element]. 1",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_173_universal_square_utf8_07_set_03_string(self):
        self.verify(
            '∀x[element]. "w"',
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_173_universal_square_utf8_07_set_04_logical(self):
        self.verify(
            "∀x[element]. false",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_173_universal_square_utf8_07_set_05_position(self):
        self.verify(
            "∀x[element]. currentposition",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_174_universal_square_utf8_01_01(self):
        self.verify("∀", [], returncode=1)

    def test_174_universal_square_utf8_01_02(self):
        self.verify("∀∊", [], returncode=1)

    def test_174_universal_square_utf8_02(self):
        self.verify("∀x∊", [], returncode=1)

    def test_174_universal_square_utf8_03(self):
        self.verify("∀x∊.", [], returncode=1)

    def test_174_universal_square_utf8_04(self):
        self.verify("∀∊. k", [], returncode=1)

    def test_174_universal_square_utf8_05(self):
        self.verify("∀∊. k", [], returncode=1)

    def test_174_universal_square_utf8_06(self):
        self.verify("∀. k", [], returncode=1)

    def test_174_universal_square_utf8_07_set_01_set_01(self):
        self.verify(
            "∀x∊. k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_174_universal_square_utf8_07_set_01_set_02(self):
        self.verify(
            "∀ x ∊ . k",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_174_universal_square_utf8_07_set_02_integer(self):
        self.verify(
            "∀x∊. 1",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_174_universal_square_utf8_07_set_03_string(self):
        self.verify(
            '∀x∊. "w"',
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_174_universal_square_utf8_07_set_04_logical(self):
        self.verify(
            "∀x∊. false",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_174_universal_square_utf8_07_set_05_position(self):
        self.verify(
            "∀x∊. currentposition",
            [
                (3, "UniversalSquareIterator"),
                (4, "Element"),
                (5, "UniversalSquareVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_175_piece_ascii_01(self):
        self.verify("[Aa]", [(3, "PieceDesignator")])

    def test_175_piece_ascii_02(self):
        self.verify("[Aa]y", [], returncode=1)

    def test_175_piece_ascii_02(self):
        self.verify("[Aa] y", [], returncode=1)

    def test_175_piece_ascii_02(self):
        self.verify("[Aa]y[element]", [], returncode=1)

    def test_175_piece_ascii_03(self):
        self.verify("[Aa]y[element].", [], returncode=1)

    def test_175_piece_ascii_04(self):
        self.verify("[element]. k", [], returncode=1)

    def test_175_piece_ascii_05(self):
        self.verify("[Aa]y. k", [], returncode=1)

    def test_175_piece_ascii_06_set_01_set_01(self):
        self.verify(
            "[Aa]y[element]. k",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_175_piece_ascii_06_set_01_set_02(self):
        self.verify(
            "[Aa]y [element] . k",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_175_piece_ascii_06_set_01_set_03(self):
        self.verify(
            "[Aa] y [element] . k",
            [
                (3, "PieceDesignator"),
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_175_piece_ascii_06_set_02_integer(self):
        self.verify(
            "[Aa]y[element]. 1",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_175_piece_ascii_06_set_03_string(self):
        self.verify(
            '[Aa]y[element]. "w"',
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_175_piece_ascii_06_set_04_logical(self):
        self.verify(
            "[Aa]y[element]. false",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_175_piece_ascii_06_set_05_position(self):
        self.verify(
            "[Aa]y[element]. currentposition",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_175_piece_ascii_07_integer_set(self):
        self.verify("[Aa]y [element] 1 k", [], returncode=1)

    def test_175_piece_ascii_08_string_set(self):
        self.verify('[Aa]y [element] "w" k', [], returncode=1)

    def test_175_piece_ascii_09_logical_set(self):
        self.verify("[Aa]y [element] true k", [], returncode=1)

    def test_175_piece_ascii_10_position_set(self):
        self.verify("[Aa]y [element] currentposition k", [], returncode=1)

    def test_176_piece_utf8_01(self):
        self.verify("◭", [(3, "PieceDesignator")])

    def test_176_piece_utf8_02(self):
        self.verify("◭y", [], returncode=1)

    def test_176_piece_utf8_02(self):
        self.verify("◭ y", [], returncode=1)

    def test_176_piece_utf8_02(self):
        self.verify("◭y[element]", [], returncode=1)

    def test_176_piece_utf8_03(self):
        self.verify("◭y[element].", [], returncode=1)

    def test_176_piece_utf8_04(self):
        self.verify("[element]. k", [], returncode=1)

    def test_176_piece_utf8_05(self):  # chessql accepts.
        self.verify("◭y. k", [], returncode=1)

    def test_176_piece_utf8_06_set_01_set_01(self):
        self.verify(
            "◭y∊. k",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_176_piece_utf8_06_set_01_set_02(self):
        self.verify(
            "◭y ∊ . k",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_176_piece_utf8_06_set_01_set_03(self):
        self.verify(
            "◭ y ∊ . k",
            [
                (3, "PieceDesignator"),
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_176_piece_utf8_06_set_02_integer(self):
        self.verify(
            "◭y∊. 1",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_176_piece_utf8_06_set_03_string(self):
        self.verify(
            '◭y∊. "w"',
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_176_piece_utf8_06_set_04_logical(self):
        self.verify(
            "◭y∊. false",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_176_piece_utf8_06_set_05_position(self):
        self.verify(
            "◭y∊. currentposition",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_176_piece_utf8_07_integer_set(self):
        self.verify("◭y ∊ 1 k", [], returncode=1)

    def test_176_piece_utf8_08_string_set(self):
        self.verify('◭y ∊ "w" k', [], returncode=1)

    def test_176_piece_utf8_09_logical_set(self):
        self.verify("◭y ∊ true k", [], returncode=1)

    def test_176_piece_utf8_10_position_set(self):
        self.verify("◭y ∊ currentposition k", [], returncode=1)

    def test_177_piece_utf8_mix_01(self):
        self.verify("◭", [(3, "PieceDesignator")])

    def test_177_piece_utf8_mix_02(self):
        self.verify("◭y", [], returncode=1)

    def test_177_piece_utf8_mix_02(self):
        self.verify("◭ y", [], returncode=1)

    def test_177_piece_utf8_mix_02(self):
        self.verify("◭y[element]", [], returncode=1)

    def test_177_piece_utf8_mix_03(self):
        self.verify("◭y[element].", [], returncode=1)

    def test_177_piece_utf8_mix_04(self):
        self.verify("[element]. k", [], returncode=1)

    def test_177_piece_utf8_mix_05(self):
        self.verify("◭y. k", [], returncode=1)

    def test_177_piece_utf8_mix_06_set_01_set_01(self):
        self.verify(
            "◭y[element]. k",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_177_piece_utf8_mix_06_set_01_set_02(self):
        self.verify(
            "◭y [element] . k",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_177_piece_utf8_mix_06_set_01_set_03(self):
        self.verify(
            "◭ y [element] . k",
            [
                (3, "PieceDesignator"),
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_177_piece_utf8_mix_06_set_02_integer(self):
        self.verify(
            "◭y[element]. 1",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_177_piece_utf8_mix_06_set_03_string(self):
        self.verify(
            '◭y[element]. "w"',
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_177_piece_utf8_mix_06_set_04_logical(self):
        self.verify(
            "◭y[element]. false",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_177_piece_utf8_mix_06_set_05_position(self):
        self.verify(
            "◭y[element]. currentposition",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_177_piece_utf8_mix_07_integer_set(self):
        self.verify("◭y [element] 1 k", [], returncode=1)

    def test_177_piece_utf8_mix_08_string_set(self):
        self.verify('◭y [element] "w" k', [], returncode=1)

    def test_177_piece_utf8_mix_09_logical_set(self):
        self.verify("◭y [element] true k", [], returncode=1)

    def test_177_piece_utf8_mix_10_position_set(self):
        self.verify("◭y [element] currentposition k", [], returncode=1)

    def test_178_piece_ascii_mix_01(self):
        self.verify("[Aa]", [(3, "PieceDesignator")])

    def test_178_piece_ascii_mix_02(self):
        self.verify("[Aa]y", [], returncode=1)

    def test_178_piece_ascii_mix_02(self):
        self.verify("[Aa] y", [], returncode=1)

    def test_178_piece_ascii_mix_02(self):
        self.verify("[Aa]y∊", [], returncode=1)

    def test_178_piece_ascii_mix_03(self):
        self.verify("[Aa]y∊.", [], returncode=1)

    def test_178_piece_ascii_mix_04(self):
        self.verify("∊. k", [], returncode=1)

    def test_178_piece_ascii_mix_05(self):
        self.verify("[Aa]y. k", [], returncode=1)

    def test_178_piece_ascii_mix_06_set_01_set_01(self):
        self.verify(
            "[Aa]y∊. k",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_178_piece_ascii_mix_06_set_01_set_02(self):
        self.verify(
            "[Aa]y ∊ . k",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_178_piece_ascii_mix_06_set_01_set_03(self):
        self.verify(
            "[Aa] y ∊ . k",
            [
                (3, "PieceDesignator"),
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_178_piece_ascii_mix_06_set_02_integer(self):
        self.verify(
            "[Aa]y∊. 1",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_178_piece_ascii_mix_06_set_03_string(self):
        self.verify(
            '[Aa]y∊. "w"',
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_178_piece_ascii_mix_06_set_04_logical(self):
        self.verify(
            "[Aa]y∊. false",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_178_piece_ascii_mix_06_set_05_position(self):
        self.verify(
            "[Aa]y∊. currentposition",
            [
                (3, "ExistentialPieceIterator"),
                (4, "Element"),
                (5, "ExistentialPieceVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_178_piece_ascii_mix_07_integer_set(self):
        self.verify("[Aa]y ∊ 1 k", [], returncode=1)

    def test_178_piece_ascii_mix_08_string_set(self):
        self.verify('[Aa]y ∊ "w" k', [], returncode=1)

    def test_178_piece_ascii_mix_09_logical_set(self):
        self.verify("[Aa]y ∊ true k", [], returncode=1)

    def test_178_piece_ascii_mix_10_position_set(self):
        self.verify("[Aa]y ∊ currentposition k", [], returncode=1)

    def test_179_universal_piece_ascii_01_01(self):
        self.verify("[forall][Aa]", [], returncode=1)

    def test_179_universal_piece_ascii_01_02(self):
        self.verify("[forall][Aa][element]", [], returncode=1)

    def test_179_universal_piece_ascii_02(self):
        self.verify("[forall][Aa]x[element]", [], returncode=1)

    def test_179_universal_piece_ascii_03(self):
        self.verify("[forall][Aa]x[element].", [], returncode=1)

    def test_179_universal_piece_ascii_04(self):
        self.verify("[forall][Aa][element]. k", [], returncode=1)

    def test_179_universal_piece_ascii_05(self):
        self.verify("[forall][Aa][element]. k", [], returncode=1)

    def test_179_universal_piece_ascii_06(self):
        self.verify("[forall][Aa]. k", [], returncode=1)

    def test_179_universal_piece_ascii_07_set_01_set_01_no_space(self):
        self.verify(
            "[forall][Aa]x[element].k",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_179_universal_piece_ascii_07_set_01_set_02_all_space(self):
        self.verify("[forall] [Aa] x [element] . k", [], returncode=1)

    def test_179_universal_piece_ascii_07_set_01_set_03_allowed_space(self):
        self.verify(
            "[forall] [Aa]x [element] . k",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_179_universal_piece_ascii_07_set_01_set_04_missing_space(self):
        self.verify("[forall][Aa]x[element]Qk", [], returncode=1)

    def test_179_universal_piece_ascii_07_set_01_set_05_forced_space(self):
        self.verify(
            "[forall][Aa]x[element]Q k",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_179_universal_piece_ascii_07_set_02_integer(self):
        self.verify(
            "[forall][Aa]x[element]. 1",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_179_universal_piece_ascii_07_set_03_string(self):
        self.verify(
            '[forall][Aa]x[element]. "w"',
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_179_universal_piece_ascii_07_set_04_logical(self):
        self.verify(
            "[forall][Aa]x[element]. false",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_179_universal_piece_ascii_07_set_05_position(self):
        self.verify(
            "[forall][Aa]x[element]. currentposition",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )

    def test_180_universal_piece_utf8_01_01(self):
        self.verify("∀◭", [], returncode=1)

    def test_180_universal_piece_utf8_01_02(self):
        self.verify("∀◭∊", [], returncode=1)

    def test_180_universal_piece_utf8_02(self):
        self.verify("∀◭x∊", [], returncode=1)

    def test_180_universal_piece_utf8_03(self):
        self.verify("∀◭x∊.", [], returncode=1)

    def test_180_universal_piece_utf8_04(self):
        self.verify("∀◭∊. k", [], returncode=1)

    def test_180_universal_piece_utf8_05(self):
        self.verify("∀◭∊. k", [], returncode=1)

    def test_180_universal_piece_utf8_06(self):
        self.verify("∀◭. k", [], returncode=1)

    def test_180_universal_piece_utf8_07_set_01_set_01_no_space(self):
        self.verify(
            "∀◭x∊.k",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_180_universal_piece_utf8_07_set_01_set_02_all_space(self):
        self.verify("∀ ◭ x ∊ . k", [], returncode=1)

    def test_180_universal_piece_utf8_07_set_01_set_03_allowed_space(self):
        self.verify(
            "∀ ◭x ∊ . k",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_180_universal_piece_utf8_07_set_01_set_04_missing_space(self):
        self.verify("∀◭x∊Qk", [], returncode=1)

    def test_180_universal_piece_utf8_07_set_01_set_05_forced_space(self):
        self.verify(
            "∀◭x∊Q k",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_180_universal_piece_utf8_07_set_02_integer(self):
        self.verify(
            "∀◭x∊. 1",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "Integer"),
            ],
        )

    def test_180_universal_piece_utf8_07_set_03_string(self):
        self.verify(
            '∀◭x∊. "w"',
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "String"),
            ],
        )

    def test_180_universal_piece_utf8_07_set_04_logical(self):
        self.verify(
            "∀◭x∊. false",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "False_"),
            ],
        )

    def test_180_universal_piece_utf8_07_set_05_position(self):
        self.verify(
            "∀◭x∊. currentposition",
            [
                (3, "UniversalPieceIterator"),
                (4, "Element"),
                (5, "UniversalPieceVariable"),
                (5, "AnySquare"),
                (4, "CurrentPosition"),
            ],
        )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FiltersIteration))
