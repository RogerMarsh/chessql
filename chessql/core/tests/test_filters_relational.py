# test_filters_relational.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for relational filters.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FiltersRelational(verify.Verify):

    def test_152_less_than_01(self):
        self.verify("<", [], returncode=1)

    def test_152_less_than_02(self):
        self.verify("A<", [], returncode=1)

    def test_152_less_than_03(self):
        self.verify("<A", [], returncode=1)

    def test_152_less_than_04_set_01_set(self):  # chessql accepts.
        self.verify("a<A", [], returncode=1)

    def test_152_less_than_04_set_02_logical(self):  # chessql accepts.
        self.verify("a<true", [], returncode=1)

    def test_152_less_than_04_set_03_numeric(self):
        self.verify(
            "a<1",
            [(3, "LT"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_152_less_than_04_set_04_string(self):  # chessql accepts.
        self.verify('a<"t"', [], returncode=1)

    def test_152_less_than_04_set_05_position(self):  # chessql accepts.
        self.verify("a<initialposition", [], returncode=1)

    def test_152_less_than_05_logical_01_set(self):  # chessql accepts.
        self.verify("true<A", [], returncode=1)

    def test_152_less_than_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true<true", [], returncode=1)

    def test_152_less_than_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true<1", [], returncode=1)

    def test_152_less_than_05_logical_04_string(self):  # chessql accepts.
        self.verify('true<"t"', [], returncode=1)

    def test_152_less_than_05_logical_05_position(self):  # chessql accepts.
        self.verify("true<initialposition", [], returncode=1)

    def test_152_less_than_06_numeric_01_set(self):
        self.verify(
            "1<A",
            [(3, "LT"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_152_less_than_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1<true", [], returncode=1)

    def test_152_less_than_06_numeric_03_numeric(self):
        self.verify("1<2", [(3, "LT"), (4, "Integer"), (4, "Integer")])

    def test_152_less_than_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1<"t"', [], returncode=1)

    def test_152_less_than_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1<initialposition", [], returncode=1)

    def test_152_less_than_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"<A', [], returncode=1)

    def test_152_less_than_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"<true', [], returncode=1)

    def test_152_less_than_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"<1', [], returncode=1)

    def test_152_less_than_07_string_04_string(self):
        self.verify('"a"<"b"', [(3, "LT"), (4, "String"), (4, "String")])

    def test_152_less_than_07_string_05_position(self):  # chessql accepts.
        self.verify("a<initialposition", [], returncode=1)

    def test_152_less_than_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition<A", [], returncode=1)

    def test_152_less_than_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition<true", [], returncode=1)

    def test_152_less_than_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition<1", [], returncode=1)

    def test_152_less_than_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition<"t"', [], returncode=1)

    def test_152_less_than_08_position_05_position(self):
        self.verify(
            "initialposition<currentposition",
            [(3, "LT"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_153_lt_eq_ascii_01(self):
        self.verify("<=", [], returncode=1)

    def test_153_lt_eq_ascii_02(self):
        self.verify("A<=", [], returncode=1)

    def test_153_lt_eq_ascii_03(self):
        self.verify("<=A", [], returncode=1)

    def test_153_lt_eq_ascii_04_set_01_set(self):  # chessql accepts.
        self.verify("a<=A", [], returncode=1)

    def test_153_lt_eq_ascii_04_set_02_logical(self):  # chessql accepts.
        self.verify("a<=true", [], returncode=1)

    def test_153_lt_eq_ascii_04_set_03_numeric(self):
        self.verify(
            "a<=1",
            [(3, "LE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_153_lt_eq_ascii_04_set_04_string(self):  # chessql accepts.
        self.verify('a<="t"', [], returncode=1)

    def test_153_lt_eq_ascii_04_set_05_position(self):  # chessql accepts.
        self.verify("a<=initialposition", [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_01_set(self):  # chessql accepts.
        self.verify("true<=A", [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true<=true", [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true<=1", [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_04_string(self):  # chessql accepts.
        self.verify('true<="t"', [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_05_position(self):  # chessql accepts.
        self.verify("true<=initialposition", [], returncode=1)

    def test_153_lt_eq_ascii_06_numeric_01_set(self):
        self.verify(
            "1<=A",
            [(3, "LE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_153_lt_eq_ascii_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1<=true", [], returncode=1)

    def test_153_lt_eq_ascii_06_numeric_03_numeric(self):
        self.verify("1<=2", [(3, "LE"), (4, "Integer"), (4, "Integer")])

    def test_153_lt_eq_ascii_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1<="t"', [], returncode=1)

    def test_153_lt_eq_ascii_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1<=initialposition", [], returncode=1)

    def test_153_lt_eq_ascii_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"<=A', [], returncode=1)

    def test_153_lt_eq_ascii_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"<=true', [], returncode=1)

    def test_153_lt_eq_ascii_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"<=1', [], returncode=1)

    def test_153_lt_eq_ascii_07_string_04_string(self):
        self.verify('"a"<="b"', [(3, "LE"), (4, "String"), (4, "String")])

    def test_153_lt_eq_ascii_07_string_05_position(self):  # chessql accepts.
        self.verify("a<=initialposition", [], returncode=1)

    def test_153_lt_eq_ascii_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition<=A", [], returncode=1)

    def test_153_lt_eq_ascii_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition<=true", [], returncode=1)

    def test_153_lt_eq_ascii_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition<=1", [], returncode=1)

    def test_153_lt_eq_ascii_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition<="t"', [], returncode=1)

    def test_153_lt_eq_ascii_08_position_05_position(self):
        self.verify(
            "initialposition<=currentposition",
            [(3, "LE"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_154_lt_eq_utf8_01(self):
        self.verify("≤", [], returncode=1)

    def test_154_lt_eq_utf8_02(self):
        self.verify("A≤", [], returncode=1)

    def test_154_lt_eq_utf8_03(self):
        self.verify("≤A", [], returncode=1)

    def test_154_lt_eq_utf8_04_set_01_set(self):  # chessql accepts.
        self.verify("a≤A", [], returncode=1)

    def test_154_lt_eq_utf8_04_set_02_logical(self):  # chessql accepts.
        self.verify("a≤true", [], returncode=1)

    def test_154_lt_eq_utf8_04_set_03_numeric(self):
        self.verify(
            "a≤1",
            [(3, "LE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_154_lt_eq_utf8_04_set_04_string(self):  # chessql accepts.
        self.verify('a≤"t"', [], returncode=1)

    def test_154_lt_eq_utf8_04_set_05_position(self):  # chessql accepts.
        self.verify("a≤initialposition", [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_01_set(self):  # chessql accepts.
        self.verify("true≤A", [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true≤true", [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true≤1", [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_04_string(self):  # chessql accepts.
        self.verify('true≤"t"', [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_05_position(self):  # chessql accepts.
        self.verify("true≤initialposition", [], returncode=1)

    def test_154_lt_eq_utf8_06_numeric_01_set(self):
        self.verify(
            "1≤A",
            [(3, "LE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_154_lt_eq_utf8_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1≤true", [], returncode=1)

    def test_154_lt_eq_utf8_06_numeric_03_numeric(self):
        self.verify("1≤2", [(3, "LE"), (4, "Integer"), (4, "Integer")])

    def test_154_lt_eq_utf8_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1≤"t"', [], returncode=1)

    def test_154_lt_eq_utf8_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1≤initialposition", [], returncode=1)

    def test_154_lt_eq_utf8_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"≤A', [], returncode=1)

    def test_154_lt_eq_utf8_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"≤true', [], returncode=1)

    def test_154_lt_eq_utf8_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"≤1', [], returncode=1)

    def test_154_lt_eq_utf8_07_string_04_string(self):
        self.verify('"a"≤"b"', [(3, "LE"), (4, "String"), (4, "String")])

    def test_154_lt_eq_utf8_07_string_05_position(self):  # chessql accepts.
        self.verify("a≤initialposition", [], returncode=1)

    def test_154_lt_eq_utf8_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition≤A", [], returncode=1)

    def test_154_lt_eq_utf8_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition≤true", [], returncode=1)

    def test_154_lt_eq_utf8_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition≤1", [], returncode=1)

    def test_154_lt_eq_utf8_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition≤"t"', [], returncode=1)

    def test_154_lt_eq_utf8_08_position_05_position(self):
        self.verify(
            "initialposition≤currentposition",
            [(3, "LE"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_155_gt_eq_ascii_01(self):
        self.verify(">=", [], returncode=1)

    def test_155_gt_eq_ascii_02(self):
        self.verify("A>=", [], returncode=1)

    def test_155_gt_eq_ascii_03(self):
        self.verify(">=A", [], returncode=1)

    def test_155_gt_eq_ascii_04_set_01_set(self):  # chessql accepts.
        self.verify("a>=A", [], returncode=1)

    def test_155_gt_eq_ascii_04_set_02_logical(self):  # chessql accepts.
        self.verify("a>=true", [], returncode=1)

    def test_155_gt_eq_ascii_04_set_03_numeric(self):
        self.verify(
            "a>=1",
            [(3, "GE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_155_gt_eq_ascii_04_set_04_string(self):  # chessql accepts.
        self.verify('a>="t"', [], returncode=1)

    def test_155_gt_eq_ascii_04_set_05_position(self):  # chessql accepts.
        self.verify("a>=initialposition", [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_01_set(self):  # chessql accepts.
        self.verify("true>=A", [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true>=true", [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true>=1", [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_04_string(self):  # chessql accepts.
        self.verify('true>="t"', [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_05_position(self):  # chessql accepts.
        self.verify("true>=initialposition", [], returncode=1)

    def test_155_gt_eq_ascii_06_numeric_01_set(self):
        self.verify(
            "1>=A",
            [(3, "GE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_155_gt_eq_ascii_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1>=true", [], returncode=1)

    def test_155_gt_eq_ascii_06_numeric_03_numeric(self):
        self.verify("1>=2", [(3, "GE"), (4, "Integer"), (4, "Integer")])

    def test_155_gt_eq_ascii_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1>="t"', [], returncode=1)

    def test_155_gt_eq_ascii_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1>=initialposition", [], returncode=1)

    def test_155_gt_eq_ascii_07_string_01_set(self):  # chessql accepts.
        self.verify('"a">=A', [], returncode=1)

    def test_155_gt_eq_ascii_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a">=true', [], returncode=1)

    def test_155_gt_eq_ascii_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a">=1', [], returncode=1)

    def test_155_gt_eq_ascii_07_string_04_string(self):
        self.verify('"a">="b"', [(3, "GE"), (4, "String"), (4, "String")])

    def test_155_gt_eq_ascii_07_string_05_position(self):  # chessql accepts.
        self.verify("a>=initialposition", [], returncode=1)

    def test_155_gt_eq_ascii_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition>=A", [], returncode=1)

    def test_155_gt_eq_ascii_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition>=true", [], returncode=1)

    def test_155_gt_eq_ascii_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition>=1", [], returncode=1)

    def test_155_gt_eq_ascii_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition>="t"', [], returncode=1)

    def test_155_gt_eq_ascii_08_position_05_position(self):
        self.verify(
            "initialposition>=currentposition",
            [(3, "GE"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_156_gt_eq_utf8_01(self):
        self.verify("≥", [], returncode=1)

    def test_156_gt_eq_utf8_02(self):
        self.verify("A≥", [], returncode=1)

    def test_156_gt_eq_utf8_03(self):
        self.verify("≥A", [], returncode=1)

    def test_156_gt_eq_utf8_04_set_01_set(self):  # chessql accepts.
        self.verify("a≥A", [], returncode=1)

    def test_156_gt_eq_utf8_04_set_02_logical(self):  # chessql accepts.
        self.verify("a≥true", [], returncode=1)

    def test_156_gt_eq_utf8_04_set_03_numeric(self):
        self.verify(
            "a≥1",
            [(3, "GE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_156_gt_eq_utf8_04_set_04_string(self):  # chessql accepts.
        self.verify('a≥"t"', [], returncode=1)

    def test_156_gt_eq_utf8_04_set_05_position(self):  # chessql accepts.
        self.verify("a≥initialposition", [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_01_set(self):  # chessql accepts.
        self.verify("true≥A", [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true≥true", [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true≥1", [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_04_string(self):  # chessql accepts.
        self.verify('true≥"t"', [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_05_position(self):  # chessql accepts.
        self.verify("true≥initialposition", [], returncode=1)

    def test_156_gt_eq_utf8_06_numeric_01_set(self):
        self.verify(
            "1≥A",
            [(3, "GE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_156_gt_eq_utf8_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1≥true", [], returncode=1)

    def test_156_gt_eq_utf8_06_numeric_03_numeric(self):
        self.verify("1≥2", [(3, "GE"), (4, "Integer"), (4, "Integer")])

    def test_156_gt_eq_utf8_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1≥"t"', [], returncode=1)

    def test_156_gt_eq_utf8_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1≥initialposition", [], returncode=1)

    def test_156_gt_eq_utf8_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"≥A', [], returncode=1)

    def test_156_gt_eq_utf8_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"≥true', [], returncode=1)

    def test_156_gt_eq_utf8_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"≥1', [], returncode=1)

    def test_156_gt_eq_utf8_07_string_04_string(self):
        self.verify('"a"≥"b"', [(3, "GE"), (4, "String"), (4, "String")])

    def test_156_gt_eq_utf8_07_string_05_position(self):  # chessql accepts.
        self.verify("a≥initialposition", [], returncode=1)

    def test_156_gt_eq_utf8_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition≥A", [], returncode=1)

    def test_156_gt_eq_utf8_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition≥true", [], returncode=1)

    def test_156_gt_eq_utf8_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition≥1", [], returncode=1)

    def test_156_gt_eq_utf8_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition≥"t"', [], returncode=1)

    def test_156_gt_eq_utf8_08_position_05_position(self):
        self.verify(
            "initialposition≥currentposition",
            [(3, "GE"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_157_gt_01(self):
        self.verify(">", [], returncode=1)

    def test_157_gt_02(self):
        self.verify("A>", [], returncode=1)

    def test_157_gt_03(self):
        self.verify(">A", [], returncode=1)

    def test_157_gt_04_set_01_set(self):  # chessql accepts.
        self.verify("a>A", [], returncode=1)

    def test_157_gt_04_set_02_logical(self):  # chessql accepts.
        self.verify("a>true", [], returncode=1)

    def test_157_gt_04_set_03_numeric(self):
        self.verify(
            "a>1",
            [(3, "GT"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_157_gt_04_set_04_string(self):  # chessql accepts.
        self.verify('a>"t"', [], returncode=1)

    def test_157_gt_04_set_05_position(self):  # chessql accepts.
        self.verify("a>initialposition", [], returncode=1)

    def test_157_gt_05_logical_01_set(self):  # chessql accepts.
        self.verify("true>A", [], returncode=1)

    def test_157_gt_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true>true", [], returncode=1)

    def test_157_gt_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true>1", [], returncode=1)

    def test_157_gt_05_logical_04_string(self):  # chessql accepts.
        self.verify('true>"t"', [], returncode=1)

    def test_157_gt_05_logical_05_position(self):  # chessql accepts.
        self.verify("true>initialposition", [], returncode=1)

    def test_157_gt_06_numeric_01_set(self):
        self.verify(
            "1>A",
            [(3, "GT"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_157_gt_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1>true", [], returncode=1)

    def test_157_gt_06_numeric_03_numeric(self):
        self.verify("1>2", [(3, "GT"), (4, "Integer"), (4, "Integer")])

    def test_157_gt_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1>"t"', [], returncode=1)

    def test_157_gt_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1>initialposition", [], returncode=1)

    def test_157_gt_07_string_01_set(self):  # chessql accepts.
        self.verify('"a">A', [], returncode=1)

    def test_157_gt_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a">true', [], returncode=1)

    def test_157_gt_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a">1', [], returncode=1)

    def test_157_gt_07_string_04_string(self):
        self.verify('"a">"b"', [(3, "GT"), (4, "String"), (4, "String")])

    def test_157_gt_07_string_05_position(self):  # chessql accepts.
        self.verify("a>initialposition", [], returncode=1)

    def test_157_gt_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition>A", [], returncode=1)

    def test_157_gt_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition>true", [], returncode=1)

    def test_157_gt_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition>1", [], returncode=1)

    def test_157_gt_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition>"t"', [], returncode=1)

    def test_157_gt_08_position_05_position(self):
        self.verify(
            "initialposition>currentposition",
            [(3, "GT"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_158_ne_ascii_01(self):
        self.verify("!=", [], returncode=1)

    def test_158_ne_ascii_02(self):
        self.verify("A!=", [], returncode=1)

    def test_158_ne_ascii_03(self):
        self.verify("!=A", [], returncode=1)

    def test_158_ne_ascii_04_set_01_set(self):  # chessql accepts.
        self.verify("a!=A", [], returncode=1)

    def test_158_ne_ascii_04_set_02_logical(self):  # chessql accepts.
        self.verify("a!=true", [], returncode=1)

    def test_158_ne_ascii_04_set_03_numeric(self):
        self.verify(
            "a!=1",
            [(3, "NE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_158_ne_ascii_04_set_04_string(self):  # chessql accepts.
        self.verify('a!="t"', [], returncode=1)

    def test_158_ne_ascii_04_set_05_position(self):  # chessql accepts.
        self.verify("a!=initialposition", [], returncode=1)

    def test_158_ne_ascii_05_logical_01_set(self):  # chessql accepts.
        self.verify("true!=A", [], returncode=1)

    def test_158_ne_ascii_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true!=true", [], returncode=1)

    def test_158_ne_ascii_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true!=1", [], returncode=1)

    def test_158_ne_ascii_05_logical_04_string(self):  # chessql accepts.
        self.verify('true!="t"', [], returncode=1)

    def test_158_ne_ascii_05_logical_05_position(self):  # chessql accepts.
        self.verify("true!=initialposition", [], returncode=1)

    def test_158_ne_ascii_06_numeric_01_set(self):
        self.verify(
            "1!=A",
            [(3, "NE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_158_ne_ascii_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1!=true", [], returncode=1)

    def test_158_ne_ascii_06_numeric_03_numeric(self):
        self.verify("1!=2", [(3, "NE"), (4, "Integer"), (4, "Integer")])

    def test_158_ne_ascii_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1!="t"', [], returncode=1)

    def test_158_ne_ascii_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1!=initialposition", [], returncode=1)

    def test_158_ne_ascii_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"!=A', [], returncode=1)

    def test_158_ne_ascii_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"!=true', [], returncode=1)

    def test_158_ne_ascii_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"!=1', [], returncode=1)

    def test_158_ne_ascii_07_string_04_string(self):
        self.verify('"a"!="b"', [(3, "NE"), (4, "String"), (4, "String")])

    def test_158_ne_ascii_07_string_05_position(self):  # chessql accepts.
        self.verify("a!=initialposition", [], returncode=1)

    def test_158_ne_ascii_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition!=A", [], returncode=1)

    def test_158_ne_ascii_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition!=true", [], returncode=1)

    def test_158_ne_ascii_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition!=1", [], returncode=1)

    def test_158_ne_ascii_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition!="t"', [], returncode=1)

    def test_158_ne_ascii_08_position_05_position(self):
        self.verify("initialposition!=currentposition", [], returncode=1)

    def test_159_ne_utf8_01(self):
        self.verify("≠", [], returncode=1)

    def test_159_ne_utf8_02(self):
        self.verify("A≠", [], returncode=1)

    def test_159_ne_utf8_03(self):
        self.verify("≠A", [], returncode=1)

    def test_159_ne_utf8_04_set_01_set(self):  # chessql accepts.
        self.verify("a≠A", [], returncode=1)

    def test_159_ne_utf8_04_set_02_logical(self):  # chessql accepts.
        self.verify("a≠true", [], returncode=1)

    def test_159_ne_utf8_04_set_03_numeric(self):
        self.verify(
            "a≠1",
            [(3, "NE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_159_ne_utf8_04_set_04_string(self):  # chessql accepts.
        self.verify('a≠"t"', [], returncode=1)

    def test_159_ne_utf8_04_set_05_position(self):  # chessql accepts.
        self.verify("a≠initialposition", [], returncode=1)

    def test_159_ne_utf8_05_logical_01_set(self):  # chessql accepts.
        self.verify("true≠A", [], returncode=1)

    def test_159_ne_utf8_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true≠true", [], returncode=1)

    def test_159_ne_utf8_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true≠1", [], returncode=1)

    def test_159_ne_utf8_05_logical_04_string(self):  # chessql accepts.
        self.verify('true≠"t"', [], returncode=1)

    def test_159_ne_utf8_05_logical_05_position(self):  # chessql accepts.
        self.verify("true≠initialposition", [], returncode=1)

    def test_159_ne_utf8_06_numeric_01_set(self):
        self.verify(
            "1≠A",
            [(3, "NE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_159_ne_utf8_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1≠true", [], returncode=1)

    def test_159_ne_utf8_06_numeric_03_numeric(self):
        self.verify("1≠2", [(3, "NE"), (4, "Integer"), (4, "Integer")])

    def test_159_ne_utf8_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1≠"t"', [], returncode=1)

    def test_159_ne_utf8_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1≠initialposition", [], returncode=1)

    def test_159_ne_utf8_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"≠A', [], returncode=1)

    def test_159_ne_utf8_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"≠true', [], returncode=1)

    def test_159_ne_utf8_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"≠1', [], returncode=1)

    def test_159_ne_utf8_07_string_04_string(self):
        self.verify('"a"≠"b"', [(3, "NE"), (4, "String"), (4, "String")])

    def test_159_ne_utf8_07_string_05_position(self):  # chessql accepts.
        self.verify("a≠initialposition", [], returncode=1)

    def test_159_ne_utf8_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition≠A", [], returncode=1)

    def test_159_ne_utf8_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition≠true", [], returncode=1)

    def test_159_ne_utf8_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition≠1", [], returncode=1)

    def test_159_ne_utf8_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition≠"t"', [], returncode=1)

    def test_159_ne_utf8_08_position_05_position(self):
        self.verify("initialposition≠currentposition", [], returncode=1)

    def test_160_ancestor_ascii_01(self):
        self.verify("[<]", [], returncode=1)

    def test_160_ancestor_ascii_02(self):
        self.verify("A[<]", [], returncode=1)

    def test_160_ancestor_ascii_03(self):
        self.verify("[<]A", [], returncode=1)

    def test_160_ancestor_ascii_04_set_01_set(self):  # chessql accepts.
        self.verify("a[<]A", [], returncode=1)

    def test_160_ancestor_ascii_04_set_02_logical(self):  # chessql accepts.
        self.verify("a[<]true", [], returncode=1)

    def test_160_ancestor_ascii_04_set_03_numeric(self):
        self.verify("a[<]1", [], returncode=1)

    def test_160_ancestor_ascii_04_set_04_string(self):  # chessql accepts.
        self.verify('a[<]"t"', [], returncode=1)

    def test_160_ancestor_ascii_04_set_05_position(self):  # chessql accepts.
        self.verify("a[<]initialposition", [], returncode=1)

    def test_160_ancestor_ascii_05_logical_01_set(self):  # chessql accepts.
        self.verify("true[<]A", [], returncode=1)

    def test_160_ancestor_ascii_05_logical_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("true[<]true", [], returncode=1)

    def test_160_ancestor_ascii_05_logical_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("true[<]1", [], returncode=1)

    def test_160_ancestor_ascii_05_logical_04_string(self):  # chessql accepts.
        self.verify('true[<]"t"', [], returncode=1)

    def test_160_ancestor_ascii_05_logical_05_position(
        self,
    ):  # chessql accepts.
        self.verify("true[<]initialposition", [], returncode=1)

    def test_160_ancestor_ascii_06_numeric_01_set(self):
        self.verify(
            "1[<]A",
            [(3, "BeforeNE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_160_ancestor_ascii_06_numeric_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("1[<]true", [], returncode=1)

    def test_160_ancestor_ascii_06_numeric_03_numeric(self):
        self.verify("1[<]2", [(3, "BeforeNE"), (4, "Integer"), (4, "Integer")])

    def test_160_ancestor_ascii_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1[<]"t"', [], returncode=1)

    def test_160_ancestor_ascii_06_numeric_05_position(
        self,
    ):  # chessql accepts.
        self.verify("1[<]initialposition", [], returncode=1)

    def test_160_ancestor_ascii_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"[<]A', [], returncode=1)

    def test_160_ancestor_ascii_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"[<]true', [], returncode=1)

    def test_160_ancestor_ascii_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"[<]1', [], returncode=1)

    def test_160_ancestor_ascii_07_string_04_string(self):
        self.verify(
            '"a"[<]"b"', [(3, "BeforeNE"), (4, "String"), (4, "String")]
        )

    def test_160_ancestor_ascii_07_string_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a[<]initialposition", [], returncode=1)

    def test_160_ancestor_ascii_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition[<]A", [], returncode=1)

    def test_160_ancestor_ascii_08_position_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[<]true", [], returncode=1)

    def test_160_ancestor_ascii_08_position_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[<]1", [], returncode=1)

    def test_160_ancestor_ascii_08_position_04_string(
        self,
    ):  # chessql accepts.
        self.verify('initialposition[<]"t"', [], returncode=1)

    def test_160_ancestor_ascii_08_position_05_position(self):
        self.verify(
            "initialposition[<]currentposition",
            [(3, "BeforeNE"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_161_ancestor_utf8_01(self):
        self.verify("≺", [], returncode=1)

    def test_161_ancestor_utf8_02(self):
        self.verify("A≺", [], returncode=1)

    def test_161_ancestor_utf8_03(self):
        self.verify("≺A", [], returncode=1)

    def test_161_ancestor_utf8_04_set_01_set(self):  # chessql accepts.
        self.verify("a≺A", [], returncode=1)

    def test_161_ancestor_utf8_04_set_02_logical(self):  # chessql accepts.
        self.verify("a≺true", [], returncode=1)

    def test_161_ancestor_utf8_04_set_03_numeric(self):
        self.verify(
            "a≺1",
            [(3, "BeforeNE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_161_ancestor_utf8_04_set_04_string(self):  # chessql accepts.
        self.verify('a≺"t"', [], returncode=1)

    def test_161_ancestor_utf8_04_set_05_position(self):  # chessql accepts.
        self.verify("a≺initialposition", [], returncode=1)

    def test_161_ancestor_utf8_05_logical_01_set(self):  # chessql accepts.
        self.verify("true≺A", [], returncode=1)

    def test_161_ancestor_utf8_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true≺true", [], returncode=1)

    def test_161_ancestor_utf8_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true≺1", [], returncode=1)

    def test_161_ancestor_utf8_05_logical_04_string(self):  # chessql accepts.
        self.verify('true≺"t"', [], returncode=1)

    def test_161_ancestor_utf8_05_logical_05_position(
        self,
    ):  # chessql accepts.
        self.verify("true≺initialposition", [], returncode=1)

    def test_161_ancestor_utf8_06_numeric_01_set(self):
        self.verify(
            "1≺A",
            [(3, "BeforeNE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_161_ancestor_utf8_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1≺true", [], returncode=1)

    def test_161_ancestor_utf8_06_numeric_03_numeric(self):
        self.verify("1≺2", [(3, "BeforeNE"), (4, "Integer"), (4, "Integer")])

    def test_161_ancestor_utf8_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1≺"t"', [], returncode=1)

    def test_161_ancestor_utf8_06_numeric_05_position(
        self,
    ):  # chessql accepts.
        self.verify("1≺initialposition", [], returncode=1)

    def test_161_ancestor_utf8_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"≺A', [], returncode=1)

    def test_161_ancestor_utf8_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"≺true', [], returncode=1)

    def test_161_ancestor_utf8_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"≺1', [], returncode=1)

    def test_161_ancestor_utf8_07_string_04_string(self):
        self.verify('"a"≺"b"', [(3, "BeforeNE"), (4, "String"), (4, "String")])

    def test_161_ancestor_utf8_07_string_05_position(self):  # chessql accepts.
        self.verify("a≺initialposition", [], returncode=1)

    def test_161_ancestor_utf8_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition≺A", [], returncode=1)

    def test_161_ancestor_utf8_08_position_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≺true", [], returncode=1)

    def test_161_ancestor_utf8_08_position_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≺1", [], returncode=1)

    def test_161_ancestor_utf8_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition≺"t"', [], returncode=1)

    def test_161_ancestor_utf8_08_position_05_position(self):
        self.verify(
            "initialposition≺currentposition",
            [(3, "BeforeNE"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_162_descendant_ascii_01(self):
        self.verify("[>]", [], returncode=1)

    def test_162_descendant_ascii_02(self):
        self.verify("A[>]", [], returncode=1)

    def test_162_descendant_ascii_03(self):
        self.verify("[>]A", [], returncode=1)

    def test_162_descendant_ascii_04_set_01_set(self):  # chessql accepts.
        self.verify("a[>]A", [], returncode=1)

    def test_162_descendant_ascii_04_set_02_logical(self):  # chessql accepts.
        self.verify("a[>]true", [], returncode=1)

    def test_162_descendant_ascii_04_set_03_numeric(self):
        self.verify("a[>]1", [], returncode=1)

    def test_162_descendant_ascii_04_set_04_string(self):  # chessql accepts.
        self.verify('a[>]"t"', [], returncode=1)

    def test_162_descendant_ascii_04_set_05_position(self):  # chessql accepts.
        self.verify("a[>]initialposition", [], returncode=1)

    def test_162_descendant_ascii_05_logical_01_set(self):  # chessql accepts.
        self.verify("true[>]A", [], returncode=1)

    def test_162_descendant_ascii_05_logical_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("true[>]true", [], returncode=1)

    def test_162_descendant_ascii_05_logical_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("true[>]1", [], returncode=1)

    def test_162_descendant_ascii_05_logical_04_string(
        self,
    ):  # chessql accepts.
        self.verify('true[>]"t"', [], returncode=1)

    def test_162_descendant_ascii_05_logical_05_position(
        self,
    ):  # chessql accepts.
        self.verify("true[>]initialposition", [], returncode=1)

    def test_162_descendant_ascii_06_numeric_01_set(self):
        self.verify(
            "1[>]A",
            [(3, "AfterNE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_162_descendant_ascii_06_numeric_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("1[>]true", [], returncode=1)

    def test_162_descendant_ascii_06_numeric_03_numeric(self):
        self.verify("1[>]2", [(3, "AfterNE"), (4, "Integer"), (4, "Integer")])

    def test_162_descendant_ascii_06_numeric_04_string(
        self,
    ):  # chessql accepts.
        self.verify('1[>]"t"', [], returncode=1)

    def test_162_descendant_ascii_06_numeric_05_position(
        self,
    ):  # chessql accepts.
        self.verify("1[>]initialposition", [], returncode=1)

    def test_162_descendant_ascii_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"[>]A', [], returncode=1)

    def test_162_descendant_ascii_07_string_02_logical(
        self,
    ):  # chessql accepts.
        self.verify('"a"[>]true', [], returncode=1)

    def test_162_descendant_ascii_07_string_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify('"a"[>]1', [], returncode=1)

    def test_162_descendant_ascii_07_string_04_string(self):
        self.verify(
            '"a"[>]"b"', [(3, "AfterNE"), (4, "String"), (4, "String")]
        )

    def test_162_descendant_ascii_07_string_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a[>]initialposition", [], returncode=1)

    def test_162_descendant_ascii_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition[>]A", [], returncode=1)

    def test_162_descendant_ascii_08_position_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[>]true", [], returncode=1)

    def test_162_descendant_ascii_08_position_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[>]1", [], returncode=1)

    def test_162_descendant_ascii_08_position_04_string(
        self,
    ):  # chessql accepts.
        self.verify('initialposition[>]"t"', [], returncode=1)

    def test_162_descendant_ascii_08_position_05_position(self):
        self.verify(
            "initialposition[>]currentposition",
            [(3, "AfterNE"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_163_descendant_utf8_01(self):
        self.verify("≻", [], returncode=1)

    def test_163_descendant_utf8_02(self):
        self.verify("A≻", [], returncode=1)

    def test_163_descendant_utf8_03(self):
        self.verify("≻A", [], returncode=1)

    def test_163_descendant_utf8_04_set_01_set(self):  # chessql accepts.
        self.verify("a≻A", [], returncode=1)

    def test_163_descendant_utf8_04_set_02_logical(self):  # chessql accepts.
        self.verify("a≻true", [], returncode=1)

    def test_163_descendant_utf8_04_set_03_numeric(self):
        self.verify(
            "a≻1",
            [(3, "AfterNE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_163_descendant_utf8_04_set_04_string(self):  # chessql accepts.
        self.verify('a≻"t"', [], returncode=1)

    def test_163_descendant_utf8_04_set_05_position(self):  # chessql accepts.
        self.verify("a≻initialposition", [], returncode=1)

    def test_163_descendant_utf8_05_logical_01_set(self):  # chessql accepts.
        self.verify("true≻A", [], returncode=1)

    def test_163_descendant_utf8_05_logical_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("true≻true", [], returncode=1)

    def test_163_descendant_utf8_05_logical_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("true≻1", [], returncode=1)

    def test_163_descendant_utf8_05_logical_04_string(
        self,
    ):  # chessql accepts.
        self.verify('true≻"t"', [], returncode=1)

    def test_163_descendant_utf8_05_logical_05_position(
        self,
    ):  # chessql accepts.
        self.verify("true≻initialposition", [], returncode=1)

    def test_163_descendant_utf8_06_numeric_01_set(self):
        self.verify(
            "1≻A",
            [(3, "AfterNE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_163_descendant_utf8_06_numeric_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("1≻true", [], returncode=1)

    def test_163_descendant_utf8_06_numeric_03_numeric(self):
        self.verify("1≻2", [(3, "AfterNE"), (4, "Integer"), (4, "Integer")])

    def test_163_descendant_utf8_06_numeric_04_string(
        self,
    ):  # chessql accepts.
        self.verify('1≻"t"', [], returncode=1)

    def test_163_descendant_utf8_06_numeric_05_position(
        self,
    ):  # chessql accepts.
        self.verify("1≻initialposition", [], returncode=1)

    def test_163_descendant_utf8_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"≻A', [], returncode=1)

    def test_163_descendant_utf8_07_string_02_logical(
        self,
    ):  # chessql accepts.
        self.verify('"a"≻true', [], returncode=1)

    def test_163_descendant_utf8_07_string_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify('"a"≻1', [], returncode=1)

    def test_163_descendant_utf8_07_string_04_string(self):
        self.verify('"a"≻"b"', [(3, "AfterNE"), (4, "String"), (4, "String")])

    def test_163_descendant_utf8_07_string_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a≻initialposition", [], returncode=1)

    def test_163_descendant_utf8_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition≻A", [], returncode=1)

    def test_163_descendant_utf8_08_position_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≻true", [], returncode=1)

    def test_163_descendant_utf8_08_position_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≻1", [], returncode=1)

    def test_163_descendant_utf8_08_position_04_string(
        self,
    ):  # chessql accepts.
        self.verify('initialposition≻"t"', [], returncode=1)

    def test_163_descendant_utf8_08_position_05_position(self):
        self.verify(
            "initialposition≻currentposition",
            [(3, "AfterNE"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_164_ancestor_eq_ascii_01(self):
        self.verify("[<=]", [], returncode=1)

    def test_164_ancestor_eq_ascii_02(self):
        self.verify("A[<=]", [], returncode=1)

    def test_164_ancestor_eq_ascii_03(self):
        self.verify("[<=]A", [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_01_set(self):  # chessql accepts.
        self.verify("a[<=]A", [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_02_logical(self):  # chessql accepts.
        self.verify("a[<=]true", [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_03_numeric(self):
        self.verify("a[<=]1", [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_04_string(self):  # chessql accepts.
        self.verify('a[<=]"t"', [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a[<=]initialposition", [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_01_set(self):  # chessql accepts.
        self.verify("true[<=]A", [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("true[<=]true", [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("true[<=]1", [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_04_string(
        self,
    ):  # chessql accepts.
        self.verify('true[<=]"t"', [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_05_position(
        self,
    ):  # chessql accepts.
        self.verify("true[<=]initialposition", [], returncode=1)

    def test_164_ancestor_eq_ascii_06_numeric_01_set(self):
        self.verify(
            "1[<=]A",
            [(3, "BeforeEq"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_164_ancestor_eq_ascii_06_numeric_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("1[<=]true", [], returncode=1)

    def test_164_ancestor_eq_ascii_06_numeric_03_numeric(self):
        self.verify(
            "1[<=]2", [(3, "BeforeEq"), (4, "Integer"), (4, "Integer")]
        )

    def test_164_ancestor_eq_ascii_06_numeric_04_string(
        self,
    ):  # chessql accepts.
        self.verify('1[<=]"t"', [], returncode=1)

    def test_164_ancestor_eq_ascii_06_numeric_05_position(
        self,
    ):  # chessql accepts.
        self.verify("1[<=]initialposition", [], returncode=1)

    def test_164_ancestor_eq_ascii_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"[<=]A', [], returncode=1)

    def test_164_ancestor_eq_ascii_07_string_02_logical(
        self,
    ):  # chessql accepts.
        self.verify('"a"[<=]true', [], returncode=1)

    def test_164_ancestor_eq_ascii_07_string_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify('"a"[<=]1', [], returncode=1)

    def test_164_ancestor_eq_ascii_07_string_04_string(self):
        self.verify(
            '"a"[<=]"b"', [(3, "BeforeEq"), (4, "String"), (4, "String")]
        )

    def test_164_ancestor_eq_ascii_07_string_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a[<=]initialposition", [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_01_set(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[<=]A", [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[<=]true", [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[<=]1", [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_04_string(
        self,
    ):  # chessql accepts.
        self.verify('initialposition[<=]"t"', [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_05_position(self):
        self.verify(
            "initialposition[<=]currentposition",
            [(3, "BeforeEq"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_165_ancestor_eq_utf8_01(self):
        self.verify("≼", [], returncode=1)

    def test_165_ancestor_eq_utf8_02(self):
        self.verify("A≼", [], returncode=1)

    def test_165_ancestor_eq_utf8_03(self):
        self.verify("≼A", [], returncode=1)

    def test_165_ancestor_eq_utf8_04_set_01_set(self):  # chessql accepts.
        self.verify("a≼A", [], returncode=1)

    def test_165_ancestor_eq_utf8_04_set_02_logical(self):  # chessql accepts.
        self.verify("a≼true", [], returncode=1)

    def test_165_ancestor_eq_utf8_04_set_03_numeric(self):
        self.verify(
            "a≼1",
            [(3, "BeforeEq"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_165_ancestor_eq_utf8_04_set_04_string(self):  # chessql accepts.
        self.verify('a≼"t"', [], returncode=1)

    def test_165_ancestor_eq_utf8_04_set_05_position(self):  # chessql accepts.
        self.verify("a≼initialposition", [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_01_set(self):  # chessql accepts.
        self.verify("true≼A", [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("true≼true", [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("true≼1", [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_04_string(
        self,
    ):  # chessql accepts.
        self.verify('true≼"t"', [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_05_position(
        self,
    ):  # chessql accepts.
        self.verify("true≼initialposition", [], returncode=1)

    def test_165_ancestor_eq_utf8_06_numeric_01_set(self):
        self.verify(
            "1≼A",
            [(3, "BeforeEq"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_165_ancestor_eq_utf8_06_numeric_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("1≼true", [], returncode=1)

    def test_165_ancestor_eq_utf8_06_numeric_03_numeric(self):
        self.verify("1≼2", [(3, "BeforeEq"), (4, "Integer"), (4, "Integer")])

    def test_165_ancestor_eq_utf8_06_numeric_04_string(
        self,
    ):  # chessql accepts.
        self.verify('1≼"t"', [], returncode=1)

    def test_165_ancestor_eq_utf8_06_numeric_05_position(
        self,
    ):  # chessql accepts.
        self.verify("1≼initialposition", [], returncode=1)

    def test_165_ancestor_eq_utf8_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"≼A', [], returncode=1)

    def test_165_ancestor_eq_utf8_07_string_02_logical(
        self,
    ):  # chessql accepts.
        self.verify('"a"≼true', [], returncode=1)

    def test_165_ancestor_eq_utf8_07_string_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify('"a"≼1', [], returncode=1)

    def test_165_ancestor_eq_utf8_07_string_04_string(self):
        self.verify('"a"≼"b"', [(3, "BeforeEq"), (4, "String"), (4, "String")])

    def test_165_ancestor_eq_utf8_07_string_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a≼initialposition", [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition≼A", [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≼true", [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≼1", [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_04_string(
        self,
    ):  # chessql accepts.
        self.verify('initialposition≼"t"', [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_05_position(self):
        self.verify(
            "initialposition≼currentposition",
            [(3, "BeforeEq"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_166_descendant_eq_ascii_01(self):
        self.verify("[>=]", [], returncode=1)

    def test_166_descendant_eq_ascii_02(self):
        self.verify("A[>=]", [], returncode=1)

    def test_166_descendant_eq_ascii_03(self):
        self.verify("[>=]A", [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_01_set(self):  # chessql accepts.
        self.verify("a[>=]A", [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("a[>=]true", [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_03_numeric(self):  # accepts.
        self.verify("a[>=]1", [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_04_string(
        self,
    ):  # chessql accepts.
        self.verify('a[>=]"t"', [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a[>=]initialposition", [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_01_set(
        self,
    ):  # chessql accepts.
        self.verify("true[>=]A", [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("true[>=]true", [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("true[>=]1", [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_04_string(
        self,
    ):  # chessql accepts.
        self.verify('true[>=]"t"', [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_05_position(
        self,
    ):  # chessql accepts.
        self.verify("true[>=]initialposition", [], returncode=1)

    def test_166_descendant_eq_ascii_06_numeric_01_set(self):
        self.verify(
            "1[>=]A",
            [(3, "AfterEq"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_166_descendant_eq_ascii_06_numeric_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("1[>=]true", [], returncode=1)

    def test_166_descendant_eq_ascii_06_numeric_03_numeric(self):
        self.verify("1[>=]2", [(3, "AfterEq"), (4, "Integer"), (4, "Integer")])

    def test_166_descendant_eq_ascii_06_numeric_04_string(
        self,
    ):  # chessql accepts.
        self.verify('1[>=]"t"', [], returncode=1)

    def test_166_descendant_eq_ascii_06_numeric_05_position(
        self,
    ):  # chessql accepts.
        self.verify("1[>=]initialposition", [], returncode=1)

    def test_166_descendant_eq_ascii_07_string_01_set(
        self,
    ):  # chessql accepts.
        self.verify('"a"[>=]A', [], returncode=1)

    def test_166_descendant_eq_ascii_07_string_02_logical(
        self,
    ):  # chessql accepts.
        self.verify('"a"[>=]true', [], returncode=1)

    def test_166_descendant_eq_ascii_07_string_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify('"a"[>=]1', [], returncode=1)

    def test_166_descendant_eq_ascii_07_string_04_string(self):
        self.verify(
            '"a"[>=]"b"', [(3, "AfterEq"), (4, "String"), (4, "String")]
        )

    def test_166_descendant_eq_ascii_07_string_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a[>=]initialposition", [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_01_set(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[>=]A", [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[>=]true", [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("initialposition[>=]1", [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_04_string(
        self,
    ):  # chessql accepts.
        self.verify('initialposition[>=]"t"', [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_05_position(self):
        self.verify(
            "initialposition[>=]currentposition",
            [(3, "AfterEq"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_167_descendant_eq_utf8_01(self):
        self.verify("≽", [], returncode=1)

    def test_167_descendant_eq_utf8_02(self):
        self.verify("A≽", [], returncode=1)

    def test_167_descendant_eq_utf8_03(self):
        self.verify("≽A", [], returncode=1)

    def test_167_descendant_eq_utf8_04_set_01_set(self):  # chessql accepts.
        self.verify("a≽A", [], returncode=1)

    def test_167_descendant_eq_utf8_04_set_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("a≽true", [], returncode=1)

    def test_167_descendant_eq_utf8_04_set_03_numeric(self):
        self.verify(
            "a≽1",
            [(3, "AfterEq"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_167_descendant_eq_utf8_04_set_04_string(self):  # chessql accepts.
        self.verify('a≽"t"', [], returncode=1)

    def test_167_descendant_eq_utf8_04_set_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a≽initialposition", [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_01_set(
        self,
    ):  # chessql accepts.
        self.verify("true≽A", [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("true≽true", [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("true≽1", [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_04_string(
        self,
    ):  # chessql accepts.
        self.verify('true≽"t"', [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_05_position(
        self,
    ):  # chessql accepts.
        self.verify("true≽initialposition", [], returncode=1)

    def test_167_descendant_eq_utf8_06_numeric_01_set(self):
        self.verify(
            "1≽A",
            [(3, "AfterEq"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_167_descendant_eq_utf8_06_numeric_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("1≽true", [], returncode=1)

    def test_167_descendant_eq_utf8_06_numeric_03_numeric(self):
        self.verify("1≽2", [(3, "AfterEq"), (4, "Integer"), (4, "Integer")])

    def test_167_descendant_eq_utf8_06_numeric_04_string(
        self,
    ):  # chessql accepts.
        self.verify('1≽"t"', [], returncode=1)

    def test_167_descendant_eq_utf8_06_numeric_05_position(
        self,
    ):  # chessql accepts.
        self.verify("1≽initialposition", [], returncode=1)

    def test_167_descendant_eq_utf8_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"≽A', [], returncode=1)

    def test_167_descendant_eq_utf8_07_string_02_logical(
        self,
    ):  # chessql accepts.
        self.verify('"a"≽true', [], returncode=1)

    def test_167_descendant_eq_utf8_07_string_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify('"a"≽1', [], returncode=1)

    def test_167_descendant_eq_utf8_07_string_04_string(self):
        self.verify('"a"≽"b"', [(3, "AfterEq"), (4, "String"), (4, "String")])

    def test_167_descendant_eq_utf8_07_string_05_position(
        self,
    ):  # chessql accepts.
        self.verify("a≽initialposition", [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_01_set(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≽A", [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_02_logical(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≽true", [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_03_numeric(
        self,
    ):  # chessql accepts.
        self.verify("initialposition≽1", [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_04_string(
        self,
    ):  # chessql accepts.
        self.verify('initialposition≽"t"', [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_05_position(self):
        self.verify(
            "initialposition≽currentposition",
            [(3, "AfterEq"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_168_eq_01(self):
        self.verify("==", [], returncode=1)

    def test_168_eq_02(self):
        self.verify("A==", [], returncode=1)

    def test_168_eq_03(self):
        self.verify("==A", [], returncode=1)

    def test_168_eq_04_set_01_set(self):  # chessql accepts.
        self.verify("a==A", [], returncode=1)

    def test_168_eq_04_set_02_logical(self):  # chessql accepts.
        self.verify("a==true", [], returncode=1)

    def test_168_eq_04_set_03_numeric(self):
        self.verify(
            "a==1",
            [(3, "Eq"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_168_eq_04_set_04_string(self):  # chessql accepts.
        self.verify('a=="t"', [], returncode=1)

    def test_168_eq_04_set_05_position(self):  # chessql accepts.
        self.verify("a==initialposition", [], returncode=1)

    def test_168_eq_05_logical_01_set(self):  # chessql accepts.
        self.verify("true==A", [], returncode=1)

    def test_168_eq_05_logical_02_logical(self):  # chessql accepts.
        self.verify("true==true", [], returncode=1)

    def test_168_eq_05_logical_03_numeric(self):  # chessql accepts.
        self.verify("true==1", [], returncode=1)

    def test_168_eq_05_logical_04_string(self):  # chessql accepts.
        self.verify('true=="t"', [], returncode=1)

    def test_168_eq_05_logical_05_position(self):  # chessql accepts.
        self.verify("true==initialposition", [], returncode=1)

    def test_168_eq_06_numeric_01_set(self):
        self.verify(
            "1==A",
            [(3, "Eq"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_168_eq_06_numeric_02_logical(self):  # chessql accepts.
        self.verify("1==true", [], returncode=1)

    def test_168_eq_06_numeric_03_numeric(self):
        self.verify("1==2", [(3, "Eq"), (4, "Integer"), (4, "Integer")])

    def test_168_eq_06_numeric_04_string(self):  # chessql accepts.
        self.verify('1=="t"', [], returncode=1)

    def test_168_eq_06_numeric_05_position(self):  # chessql accepts.
        self.verify("1==initialposition", [], returncode=1)

    def test_168_eq_07_string_01_set(self):  # chessql accepts.
        self.verify('"a"==A', [], returncode=1)

    def test_168_eq_07_string_02_logical(self):  # chessql accepts.
        self.verify('"a"==true', [], returncode=1)

    def test_168_eq_07_string_03_numeric(self):  # chessql accepts.
        self.verify('"a"==1', [], returncode=1)

    def test_168_eq_07_string_04_string(self):
        self.verify('"a"=="b"', [(3, "Eq"), (4, "String"), (4, "String")])

    def test_168_eq_07_string_05_position(self):  # chessql accepts.
        self.verify("a==initialposition", [], returncode=1)

    def test_168_eq_08_position_01_set(self):  # chessql accepts.
        self.verify("initialposition==A", [], returncode=1)

    def test_168_eq_08_position_02_logical(self):  # chessql accepts.
        self.verify("initialposition==true", [], returncode=1)

    def test_168_eq_08_position_03_numeric(self):  # chessql accepts.
        self.verify("initialposition==1", [], returncode=1)

    def test_168_eq_08_position_04_string(self):  # chessql accepts.
        self.verify('initialposition=="t"', [], returncode=1)

    def test_168_eq_08_position_05_position(self):
        self.verify(
            "initialposition==currentposition",
            [(3, "Eq"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FiltersRelational))
