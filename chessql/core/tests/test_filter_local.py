# test_filter_local.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'local dictionary' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FilterDictionaryLocal(verify.Verify):
    def test_063_local_01(self):
        self.verify("local", [], returncode=1)

    def test_063_local_02_local_dictionary(self):
        self.verify("local dictionary", [], returncode=1)

    def test_063_local_03_bad_name(self):
        self.verify("local dictionary k", [], returncode=1)

    def test_063_local_04_good_name(self):
        self.verify("local dictionary X", [(3, "Dictionary")])

    def test_063_local_05_string_string(self):
        self.verify(
            'local dictionary X["a"]="bc"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
            ],
        )

    def test_063_local_06_string_set_01_piecedesignator(self):
        self.verify(
            'local dictionary X["a"]=k',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_06_string_set_02_some_other_set(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "ConnectedPawns"),
            ],
        )

    def test_063_local_07_string_integer(self):
        self.verify(
            'local dictionary X["a"]=1',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "Integer"),
            ],
        )

    def test_063_local_08_local_string_position(self):
        self.verify(
            'local dictionary X["a"]=currentposition',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "CurrentPosition"),
            ],
        )

    def test_063_local_09_string_logical(self):
        self.verify('local dictionary X["a"]=false', [], returncode=1)

    def test_063_local_10_set_string(self):
        self.verify(
            'local dictionary X[to]="bc"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "String"),
            ],
        )

    def test_063_local_11_set_set_01_piece_designator(self):
        self.verify(
            "local dictionary X[to]=k",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_11_set_set_02_some_other_set(self):
        self.verify(
            "local dictionary X[to]=from",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "From"),
            ],
        )

    def test_063_local_12_set_integer(self):
        self.verify(
            "local dictionary X[to]=3",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "Integer"),
            ],
        )

    def test_063_local_13_local_set_position(self):
        self.verify(
            "local dictionary X[to]=currentposition",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "CurrentPosition"),
            ],
        )

    def test_063_local_14_string_logical(self):
        self.verify("local dictionary X[to]=false", [], returncode=1)

    def test_063_local_15_integer_string(self):
        self.verify(
            'local dictionary X[3]="bc"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
            ],
        )

    def test_063_local_16_integer_set_01_piece_designator(self):
        self.verify(
            "local dictionary X[3]=qa5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_16_integer_set_02_some_other_set(self):
        self.verify(
            "local dictionary X[3]=from",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "From"),
            ],
        )

    def test_063_local_17_integer_integer(self):
        self.verify(
            "local dictionary X[3]=3",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_063_local_18_integer_position(self):
        self.verify(
            "local dictionary X[3]=currentposition",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "CurrentPosition"),
            ],
        )

    def test_063_local_19_integer_logical(self):
        self.verify("local dictionary X[3]=false", [], returncode=1)

    def test_063_local_20_bad_piecedesignator_string(self):
        self.verify('local dictionary X[a5]="bc"', [], returncode=1)

    def test_063_local_21_bad_piecedesignator_set_01_piece_designator(self):
        self.verify("local dictionary X[a5]=h2", [], returncode=1)

    def test_063_local_21_bad_piecedesignator_set_02_some_other_set(self):
        self.verify("local dictionary X[a5]=from", [], returncode=1)

    def test_063_local_22_bad_piecedesignator_integer(self):
        self.verify("local dictionary X[a5]=3", [], returncode=1)

    def test_063_local_23_bad_piecedesignator_position(self):
        self.verify("local dictionary X[a5]=currentposition", [], returncode=1)

    def test_063_local_24_bad_piecedesignator_logical(self):
        self.verify("local dictionary X[a5]=false", [], returncode=1)

    def test_063_local_25_piecedesignator_string(self):
        self.verify(
            'local dictionary X[ a5 ]="bc"',  # chessql accepts '[ a5]' too.
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "String"),
            ],
        )

    def test_063_local_26_piecedesignator_set_01_piece_designator(self):
        self.verify(
            "local dictionary X[ a5 ]=d7",  # chessql accepts '[ a5]' too.
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_26_piecedesignator_set_02_some_other_set(self):
        self.verify(
            "local dictionary X[ a5 ]=from",  # chessql accepts '[ a5]' too.
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "From"),
            ],
        )

    def test_063_local_27_piecedesignator_integer(self):
        self.verify(
            "local dictionary X[ a5 ]=3",  # chessql accepts '[ a5]' too.
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_063_local_28_piecedesignator_position(self):
        self.verify(  # chessql accepts '[ a5]' too.
            "local dictionary X[ a5 ]=currentposition",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "CurrentPosition"),
            ],
        )

    def test_063_local_29_logical_string(self):
        self.verify('local dictionary X[true]="bc"', [], returncode=1)

    def test_063_local_30_logical_set_01_piece_designator(self):
        self.verify("local dictionary X[true]=k", [], returncode=1)

    def test_063_local_30_logical_set_02_some_other_set(self):
        self.verify("local dictionary X[true]=from", [], returncode=1)

    def test_063_local_31_logical_integer(self):
        self.verify("local dictionary X[true]=3", [], returncode=1)

    def test_063_local_32_logical_position(self):
        self.verify(
            "local dictionary X[true]=currentposition", [], returncode=1
        )

    def test_063_local_33_logical_logical(self):
        self.verify("local dictionary X[true]=false", [], returncode=1)

    def test_063_local_34_piecedesignator_logical(self):
        self.verify("local dictionary X[ a5 ]=false", [], returncode=1)

    def test_063_local_35_string_string_01(self):
        self.verify(
            'local dictionary X["a"]="bc" X["a"]="yz" X["b"]="ij"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
            ],
        )

    def test_063_local_35_string_string_02(self):
        self.verify(
            'local dictionary X["a"]="bc" X[to]="yz"', [], returncode=1
        )

    def test_063_local_35_string_string_03(self):
        self.verify(
            'local dictionary X["a"]="bc" X[ k ]="yz"', [], returncode=1
        )

    def test_063_local_35_string_string_04(self):
        self.verify('local dictionary X["a"]="bc" X[1]="yz"', [], returncode=1)

    def test_063_local_35_string_string_05(self):
        self.verify('local dictionary X["a"]="bc" X["a"]=to', [], returncode=1)

    def test_063_local_35_string_string_06(self):
        self.verify('local dictionary X["a"]="bc" X["a"]=k', [], returncode=1)

    def test_063_local_35_string_string_07(self):
        self.verify('local dictionary X["a"]="bc" X["a"]=1', [], returncode=1)

    def test_063_local_35_string_string_08(self):
        self.verify(
            'local dictionary X["a"]="bc" X[currentposition]=1',
            [],
            returncode=1,
        )

    def test_063_local_35_string_string_09(self):
        self.verify(
            'local dictionary X["a"]="bc" X["a"]=currentposition',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_01_piecedesignator_01(self):
        self.verify(
            'local dictionary X["a"]=k X["a"]=Pa6 X["b"]=R',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_36_string_set_01_piecedesignator_02(self):
        self.verify('local dictionary X["a"]=k X[to]=k', [], returncode=1)

    def test_063_local_36_string_set_01_piecedesignator_03(self):
        self.verify('local dictionary X["a"]=k X[ k ]=k', [], returncode=1)

    def test_063_local_36_string_set_01_piecedesignator_04(self):
        self.verify('local dictionary X["a"]=k X[1]=k', [], returncode=1)

    def test_063_local_36_string_set_01_piecedesignator_05(self):
        self.verify('local dictionary X["a"]=k X["a"]=1', [], returncode=1)

    def test_063_local_36_string_set_01_piecedesignator_06(self):
        self.verify('local dictionary X["a"]=k X["a"]="a"', [], returncode=1)

    def test_063_local_36_string_set_01_piecedesignator_07(self):
        self.verify(
            'local dictionary X["a"]=k X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_01_piecedesignator_08(self):
        self.verify(
            'local dictionary X["a"]=k X["a"]=currentposition',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_02_some_other_set_01(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns X["a"]=to X["b"]=from',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "ConnectedPawns"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "To"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "From"),
            ],
        )

    def test_063_local_36_string_set_02_some_other_set_02(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns X[1]=connectedpawns',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_02_some_other_set_03(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns X[ k ]=connectedpawns',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_02_some_other_set_04(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns X[to]=connectedpawns',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_02_some_other_set_05(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns X["a"]=1',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_02_some_other_set_06(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns X["a"]="a"',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_02_some_other_set_07(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_36_string_set_02_some_other_set_08(self):
        self.verify(
            'local dictionary X["a"]=connectedpawns X["a"]=currentposition',
            [],
            returncode=1,
        )

    def test_063_local_37_string_integer_01(self):
        self.verify(
            'local dictionary X["a"]=1 X["a"]=7 X["b"]=4',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "Integer"),
            ],
        )

    def test_063_local_37_string_integer_02(self):
        self.verify('local dictionary X["a"]=1 X[1]=1', [], returncode=1)

    def test_063_local_37_string_integer_03(self):
        self.verify('local dictionary X["a"]=1 X[ k ]=1', [], returncode=1)

    def test_063_local_37_string_integer_04(self):
        self.verify('local dictionary X["a"]=1 X[to]=1', [], returncode=1)

    def test_063_local_37_string_integer_05(self):
        self.verify('local dictionary X["a"]=1 X["a"]=k', [], returncode=1)

    def test_063_local_37_string_integer_06(self):
        self.verify('local dictionary X["a"]=1 X["a"]=to', [], returncode=1)

    def test_063_local_37_string_integer_07(self):
        self.verify('local dictionary X["a"]=1 X["a"]="a"', [], returncode=1)

    def test_063_local_37_string_integer_08(self):
        self.verify(
            'local dictionary X["a"]=1 X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_37_string_integer_09(self):
        self.verify(
            'local dictionary X["a"]=1 X["a"]=currentposition',
            [],
            returncode=1,
        )

    def test_063_local_38_set_string_01(self):
        self.verify(
            'local dictionary X[to]="bc" X[to]="yz" X[from]="mn" X[ Q ]="kh"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "From"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "String"),
            ],
        )

    def test_063_local_38_set_string_02(self):
        self.verify('local dictionary X[to]="bc" X[1]="bc"', [], returncode=1)

    def test_063_local_38_set_string_03(self):
        self.verify(
            'local dictionary X[to]="bc" X["a"]="bc"', [], returncode=1
        )

    def test_063_local_38_set_string_04(self):
        self.verify('local dictionary X[to]="bc" X[to]=1', [], returncode=1)

    def test_063_local_38_set_string_05(self):
        self.verify('local dictionary X[to]="bc" X[to]=k', [], returncode=1)

    def test_063_local_38_set_string_06(self):
        self.verify('local dictionary X[to]="bc" X[to]=from', [], returncode=1)

    def test_063_local_38_set_string_07(self):
        self.verify(
            'local dictionary X[to]="bc" X[currentposition]=from',
            [],
            returncode=1,
        )

    def test_063_local_38_set_string_08(self):
        self.verify(
            'local dictionary X[to]="bc" X[to]=currentposition',
            [],
            returncode=1,
        )

    def test_063_local_39_set_set_01_piecedesignator_01(self):
        self.verify(
            "local dictionary X[to]=k X[to]=R X[from]=Q "
            + "X[ a5 ]=connectedpawns",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "From"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "ConnectedPawns"),
            ],
        )

    def test_063_local_39_set_set_01_piecedesignator_02(self):
        self.verify("local dictionary X[to]=k X[1]=k", [], returncode=1)

    def test_063_local_39_set_set_01_piecedesignator_03(self):
        self.verify('local dictionary X[to]=k X["a"]=k', [], returncode=1)

    def test_063_local_39_set_set_01_piecedesignator_04(self):
        self.verify("local dictionary X[to]=k X[to]=1", [], returncode=1)

    def test_063_local_39_set_set_01_piecedesignator_05(self):
        self.verify('local dictionary X[to]=k X[to]="a"', [], returncode=1)

    def test_063_local_39_set_set_01_piecedesignator_06(self):
        self.verify("local dictionary X[to]=k X[1]=2", [], returncode=1)

    def test_063_local_39_set_set_01_piecedesignator_07(self):
        self.verify(
            "local dictionary X[to]=k X[currentposition]=2", [], returncode=1
        )

    def test_063_local_39_set_set_01_piecedesignator_08(self):
        self.verify(
            "local dictionary X[to]=k X[1]=currentposition", [], returncode=1
        )

    def test_063_local_39_set_set_02_some_other_set_01(self):
        self.verify(
            "local dictionary X[to]=from X[to]=to X[from]=to X[ b6 ]=c4",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "From"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "To"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "From"),
                (4, "To"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_39_set_set_02_some_other_set_02(self):
        self.verify("local dictionary X[to]=from X[1]=from", [], returncode=1)

    def test_063_local_39_set_set_02_some_other_set_03(self):
        self.verify(
            'local dictionary X[to]=from X["a"]=from', [], returncode=1
        )

    def test_063_local_39_set_set_02_some_other_set_04(self):
        self.verify("local dictionary X[to]=from X[to]=1", [], returncode=1)

    def test_063_local_39_set_set_02_some_other_set_05(self):
        self.verify('local dictionary X[to]=from X[to]="a"', [], returncode=1)

    def test_063_local_39_set_set_02_some_other_set_06(self):
        self.verify('local dictionary X[to]=from X[1]="a"', [], returncode=1)

    def test_063_local_39_set_set_02_some_other_set_07(self):
        self.verify(
            'local dictionary X[to]=from X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_39_set_set_02_some_other_set_08(self):
        self.verify(
            "local dictionary X[to]=from X[1]=currentposition",
            [],
            returncode=1,
        )

    def test_063_local_40_set_integer_01(self):
        self.verify(
            "local dictionary X[to]=3 X[to]=7 X[from]=4 X[ rh8 ]=1",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "From"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_063_local_40_set_integer_02(self):
        self.verify("local dictionary X[to]=3 X[1]=3", [], returncode=1)

    def test_063_local_40_set_integer_03(self):
        self.verify('local dictionary X[to]=3 X["a"]=3', [], returncode=1)

    def test_063_local_40_set_integer_04(self):
        self.verify("local dictionary X[to]=3 X[to]=k", [], returncode=1)

    def test_063_local_40_set_integer_05(self):
        self.verify("local dictionary X[to]=3 X[to]=from", [], returncode=1)

    def test_063_local_40_set_integer_06(self):
        self.verify('local dictionary X[to]=3 X[to]="a"', [], returncode=1)

    def test_063_local_40_set_integer_07(self):
        self.verify("local dictionary X[to]=3 X[1]=from", [], returncode=1)

    def test_063_local_40_set_integer_08(self):
        self.verify(
            "local dictionary X[to]=3 X[currentposition]=from",
            [],
            returncode=1,
        )

    def test_063_local_40_set_integer_09(self):
        self.verify(
            "local dictionary X[to]=3 X[1]=currentposition", [], returncode=1
        )

    def test_063_local_41_integer_string_01(self):
        self.verify(
            'local dictionary X[3]="bc" X[3]="xz" X[4]="mn"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
            ],
        )

    def test_063_local_41_integer_string_02(self):
        self.verify('local dictionary X[3]="bc" X["a"]="bc"', [], returncode=1)

    def test_063_local_41_integer_string_03(self):
        self.verify('local dictionary X[3]="bc" X[ k ]="bc"', [], returncode=1)

    def test_063_local_41_integer_string_04(self):
        self.verify('local dictionary X[3]="bc" X[to]="bc"', [], returncode=1)

    def test_063_local_41_integer_string_05(self):
        self.verify('local dictionary X[3]="bc" X[3]=1', [], returncode=1)

    def test_063_local_41_integer_string_06(self):
        self.verify('local dictionary X[3]="bc" X[3]=k', [], returncode=1)

    def test_063_local_41_integer_string_07(self):
        self.verify('local dictionary X[3]="bc" X[3]=from', [], returncode=1)

    def test_063_local_41_integer_string_08(self):
        self.verify(
            'local dictionary X[3]="bc" X[currentposition]=from',
            [],
            returncode=1,
        )

    def test_063_local_41_integer_string_09(self):
        self.verify(
            'local dictionary X[3]="bc" X[3]=currentposition', [], returncode=1
        )

    def test_063_local_42_integer_set_01_piecedesignator_01(self):
        self.verify(
            "local dictionary X[3]=qa5 X[3]=g2 X[4]=[KQ]a5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_42_integer_set_01_piecedesignator_02(self):
        self.verify('local dictionary X[3]=qa5 X["a"]=qa5', [], returncode=1)

    def test_063_local_42_integer_set_01_piecedesignator_03(self):
        self.verify("local dictionary X[3]=qa5 X[ k ]=qa5", [], returncode=1)

    def test_063_local_42_integer_set_01_piecedesignator_04(self):
        self.verify("local dictionary X[3]=qa5 X[from]=qa5", [], returncode=1)

    def test_063_local_42_integer_set_01_piecedesignator_05(self):
        self.verify("local dictionary X[3]=qa5 X[3]=1", [], returncode=1)

    def test_063_local_42_integer_set_01_piecedesignator_06(self):
        self.verify('local dictionary X[3]=qa5 X[3]="a"', [], returncode=1)

    def test_063_local_42_integer_set_01_piecedesignator_07(self):
        self.verify(
            'local dictionary X[3]=qa5 X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_42_integer_set_01_piecedesignator_08(self):
        self.verify(
            "local dictionary X[3]=qa5 X[3]=currentposition", [], returncode=1
        )

    def test_063_local_43_integer_set_02_some_other_set_01(self):
        self.verify(
            "local dictionary X[3]=from X[3]=to X[5]=connectedpawns",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "From"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "To"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "ConnectedPawns"),
            ],
        )

    def test_063_local_43_integer_set_02_some_other_set_02(self):
        self.verify('local dictionary X[3]=from X["a"]=from', [], returncode=1)

    def test_063_local_43_integer_set_02_some_other_set_03(self):
        self.verify("local dictionary X[3]=from X[ k ]=from", [], returncode=1)

    def test_063_local_43_integer_set_02_some_other_set_04(self):
        self.verify("local dictionary X[3]=from X[to]=from", [], returncode=1)

    def test_063_local_43_integer_set_02_some_other_set_05(self):
        self.verify("local dictionary X[3]=from X[3]=1", [], returncode=1)

    def test_063_local_43_integer_set_02_some_other_set_06(self):
        self.verify('local dictionary X[3]=from X[3]="a"', [], returncode=1)

    def test_063_local_43_integer_set_02_some_other_set_07(self):
        self.verify(
            'local dictionary X[3]=from X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_43_integer_set_02_some_other_set_08(self):
        self.verify(
            "local dictionary X[3]=from X[3]=currentposition", [], returncode=1
        )

    def test_063_local_44_integer_integer_01(self):
        self.verify(
            "local dictionary X[3]=3 X[3]=6 X[7]=4",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_063_local_44_integer_integer_02(self):
        self.verify('local dictionary X[3]=3 X["a"]=3', [], returncode=1)

    def test_063_local_44_integer_integer_03(self):
        self.verify("local dictionary X[3]=3 X[ k ]=3", [], returncode=1)

    def test_063_local_44_integer_integer_04(self):
        self.verify("local dictionary X[3]=3 X[to]=3", [], returncode=1)

    def test_063_local_44_integer_integer_05(self):
        self.verify('local dictionary X[3]=3 X[3]="a"', [], returncode=1)

    def test_063_local_44_integer_integer_06(self):
        self.verify("local dictionary X[3]=3 X[3]=k", [], returncode=1)

    def test_063_local_44_integer_integer_07(self):
        self.verify("local dictionary X[3]=3 X[3]=to", [], returncode=1)

    def test_063_local_44_integer_integer_08(self):
        self.verify(
            "local dictionary X[3]=3 X[currentposition]=to", [], returncode=1
        )

    def test_063_local_44_integer_integer_09(self):
        self.verify(
            "local dictionary X[3]=3 X[3]=currentposition", [], returncode=1
        )

    def test_063_local_45_piecedesignator_string_01(self):
        self.verify(  # chessql accepts '[ a5]' too.
            'local dictionary X[ a5 ]="bc" X[ a5 ]="xz" X[ R ]="mn" '
            + 'X[to]="bc"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "String"),
            ],
        )

    def test_063_local_45_piecedesignator_string_02(self):
        self.verify(
            'local dictionary X[ a5 ]="bc" X[1]="bc"', [], returncode=1
        )

    def test_063_local_45_piecedesignator_string_03(self):
        self.verify(
            'local dictionary X[ a5 ]="bc" X["a5"]="bc"', [], returncode=1
        )

    def test_063_local_45_piecedesignator_string_04(self):
        self.verify(
            'local dictionary X[ a5 ]="bc" X[ a5 ]=1', [], returncode=1
        )

    def test_063_local_45_piecedesignator_string_05(self):
        self.verify(
            'local dictionary X[ a5 ]="bc" X[ a5 ]=k', [], returncode=1
        )

    def test_063_local_45_piecedesignator_string_06(self):
        self.verify(
            'local dictionary X[ a5 ]="bc" X[ a5 ]=to', [], returncode=1
        )

    def test_063_local_45_piecedesignator_string_07(self):
        self.verify(
            'local dictionary X[ a5 ]="bc" X[currentposition]=to',
            [],
            returncode=1,
        )

    def test_063_local_45_piecedesignator_string_08(self):
        self.verify(
            'local dictionary X[ a5 ]="bc" X[ a5 ]=currentposition',
            [],
            returncode=1,
        )

    def test_063_local_46_piecedesignator_set_01_piecedesignator_01(self):
        self.verify(  # chessql accepts '[ a5]' too.
            "local dictionary X[ a5 ]=d7 X[ a5 ]=K X[ k ]=Q X[ to ]=h7",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_46_piecedesignator_set_01_piecedesignator_02(self):
        self.verify("local dictionary X[ a5 ]=d7 X[1]=d7", [], returncode=1)

    def test_063_local_46_piecedesignator_set_01_piecedesignator_03(self):
        self.verify('local dictionary X[ a5 ]=d7 X["a5"]=d7', [], returncode=1)

    def test_063_local_46_piecedesignator_set_01_piecedesignator_04(self):
        self.verify("local dictionary X[ a5 ]=d7 X[ a5 ]=1", [], returncode=1)

    def test_063_local_46_piecedesignator_set_01_piecedesignator_05(self):
        self.verify(
            'local dictionary X[ a5 ]=d7 X[ a5 ]="a"', [], returncode=1
        )

    def test_063_local_46_piecedesignator_set_01_piecedesignator_06(self):
        self.verify(
            'local dictionary X[ a5 ]=d7 X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_46_piecedesignator_set_01_piecedesignator_07(self):
        self.verify(
            "local dictionary X[ a5 ]=d7 X[ a5 ]=currentposition",
            [],
            returncode=1,
        )

    def test_063_local_46_piecedesignator_set_02_some_other_set_01(self):
        self.verify(  # chessql accepts '[ a5]' too.
            "local dictionary X[ a5 ]=from X[ a5 ]=to X[ h5 ]=connectedpawns "
            + "X[from]=to",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "From"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "To"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "ConnectedPawns"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "From"),
                (4, "To"),
            ],
        )

    def test_063_local_46_piecedesignator_set_02_some_other_set_02(self):
        self.verify(
            "local dictionary X[ a5 ]=from X[1]=from", [], returncode=1
        )

    def test_063_local_46_piecedesignator_set_02_some_other_set_03(self):
        self.verify(
            'local dictionary X[ a5 ]=from X["a5"]=from', [], returncode=1
        )

    def test_063_local_46_piecedesignator_set_02_some_other_set_04(self):
        self.verify(
            "local dictionary X[ a5 ]=from X[ a5 ]=1", [], returncode=1
        )

    def test_063_local_46_piecedesignator_set_02_some_other_set_05(self):
        self.verify(
            'local dictionary X[ a5 ]=from X[ a5 ]="a"', [], returncode=1
        )

    def test_063_local_46_piecedesignator_set_02_some_other_set_06(self):
        self.verify(
            'local dictionary X[ a5 ]=from X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_46_piecedesignator_set_02_some_other_set_07(self):
        self.verify(
            "local dictionary X[ a5 ]=from X[ a5 ]=currentposition",
            [],
            returncode=1,
        )

    def test_063_local_47_piecedesignator_integer_01(self):
        self.verify(  # chessql accepts '[ a5]' too.
            "local dictionary X[ a5 ]=3 X[ a5 ]=4 X[ h2 ]=3 X[to]=8",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "Integer"),
            ],
        )

    def test_063_local_47_piecedesignator_integer_02(self):
        self.verify("local dictionary X[ a5 ]=3 X[1]=3", [], returncode=1)

    def test_063_local_47_piecedesignator_integer_03(self):
        self.verify('local dictionary X[ a5 ]=3 X["a5"]=3', [], returncode=1)

    def test_063_local_47_piecedesignator_integer_04(self):
        self.verify("local dictionary X[ a5 ]=3 X[ a5 ]=k", [], returncode=1)

    def test_063_local_47_piecedesignator_integer_05(self):
        self.verify("local dictionary X[ a5 ]=3 X[ a5 ]=to", [], returncode=1)

    def test_063_local_47_piecedesignator_integer_06(self):
        self.verify('local dictionary X[ a5 ]=3 X[ a5 ]="a"', [], returncode=1)

    def test_063_local_47_piecedesignator_integer_07(self):
        self.verify(
            'local dictionary X[ a5 ]=3 X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_47_piecedesignator_integer_08(self):
        self.verify(
            "local dictionary X[ a5 ]=3 X[ a5 ]=currentposition",
            [],
            returncode=1,
        )

    def test_063_local_48_position_string_01(self):
        self.verify(
            'local dictionary X[currentposition]="a" '
            + 'X[currentposition]="b" '
            + 'X[initialposition]="c"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "String"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "String"),
            ],
        )

    def test_063_local_48_position_string_02(self):
        self.verify(
            'local dictionary X[currentposition]="a" ' + 'X[1]="b"',
            [],
            returncode=1,
        )

    def test_063_local_48_position_string_03(self):
        self.verify(
            'local dictionary X[currentposition]="a" ' + 'X["a"]="b"',
            [],
            returncode=1,
        )

    def test_063_local_48_position_string_04(self):
        self.verify(
            'local dictionary X[currentposition]="a" ' + 'X[ k ]="b"',
            [],
            returncode=1,
        )

    def test_063_local_48_position_string_05(self):
        self.verify(
            'local dictionary X[currentposition]="a" ' + 'X[to]="b"',
            [],
            returncode=1,
        )

    def test_063_local_48_position_string_06(self):
        self.verify(
            'local dictionary X[currentposition]="a" '
            + "X[currentposition]=1",
            [],
            returncode=1,
        )

    def test_063_local_48_position_string_07(self):
        self.verify(
            'local dictionary X[currentposition]="a" '
            + "X[currentposition]=k",
            [],
            returncode=1,
        )

    def test_063_local_48_position_string_08(self):
        self.verify(
            'local dictionary X[currentposition]="a" '
            + "X[currentposition]=to",
            [],
            returncode=1,
        )

    def test_063_local_48_position_string_09(self):
        self.verify(
            'local dictionary X[currentposition]="a" '
            + "X[currentposition]=initialposition",
            [],
            returncode=1,
        )

    def test_063_local_49_position_piecedesignator_01(self):
        self.verify(
            "local dictionary X[currentposition]=k "
            + "X[currentposition]=q "
            + "X[initialposition]=r "
            + "X[initialposition]=connectedpawns",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "ConnectedPawns"),
            ],
        )

    def test_063_local_49_position_piecedesignator_02(self):
        self.verify(
            "local dictionary X[currentposition]=k " + "X[1]=q",
            [],
            returncode=1,
        )

    def test_063_local_49_position_piecedesignator_03(self):
        self.verify(
            "local dictionary X[currentposition]=k " + 'X["a"]=q',
            [],
            returncode=1,
        )

    def test_063_local_49_position_piecedesignator_04(self):
        self.verify(
            "local dictionary X[currentposition]=k " + "X[ k ]=q",
            [],
            returncode=1,
        )

    def test_063_local_49_position_piecedesignator_05(self):
        self.verify(
            "local dictionary X[currentposition]=k " + "X[to]=q",
            [],
            returncode=1,
        )

    def test_063_local_49_position_piecedesignator_06(self):
        self.verify(
            "local dictionary X[currentposition]=k " + "X[currentposition]=1",
            [],
            returncode=1,
        )

    def test_063_local_49_position_piecedesignator_07(self):
        self.verify(
            "local dictionary X[currentposition]=k "
            + 'X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_49_position_piecedesignator_08(self):
        self.verify(
            "local dictionary X[currentposition]=k "
            + "X[currentposition]=initialposition",
            [],
            returncode=1,
        )

    def test_063_local_50_position_set_01(self):
        self.verify(
            "local dictionary X[currentposition]=from "
            + "X[currentposition]=to "
            + "X[initialposition]=connectedpawns "
            + "X[initialposition]=a5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "From"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "To"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "ConnectedPawns"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "PieceDesignator"),
            ],
        )

    def test_063_local_50_position_set_02(self):
        self.verify(
            "local dictionary X[currentposition]=from " + "X[1]=to",
            [],
            returncode=1,
        )

    def test_063_local_50_position_set_03(self):
        self.verify(
            "local dictionary X[currentposition]=from " + 'X["a"]=to',
            [],
            returncode=1,
        )

    def test_063_local_50_position_set_04(self):
        self.verify(
            "local dictionary X[currentposition]=from " + "X[ k ]=to",
            [],
            returncode=1,
        )

    def test_063_local_50_position_set_05(self):
        self.verify(
            "local dictionary X[currentposition]=from " + "X[to]=to",
            [],
            returncode=1,
        )

    def test_063_local_50_position_set_06(self):
        self.verify(
            "local dictionary X[currentposition]=from "
            + "X[currentposition]=1",
            [],
            returncode=1,
        )

    def test_063_local_50_position_set_07(self):
        self.verify(
            "local dictionary X[currentposition]=from "
            + 'X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_50_position_set_08(self):
        self.verify(
            "local dictionary X[currentposition]=from "
            + "X[currentposition]=initialposition",
            [],
            returncode=1,
        )

    def test_063_local_51_position_integer_01(self):
        self.verify(
            "local dictionary X[currentposition]=3 "
            + "X[currentposition]=4 "
            + "X[initialposition]=5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "Integer"),
            ],
        )

    def test_063_local_51_position_integer_02(self):
        self.verify(
            "local dictionary X[currentposition]=3 " + "X[1]=4",
            [],
            returncode=1,
        )

    def test_063_local_51_position_integer_03(self):
        self.verify(
            "local dictionary X[currentposition]=3 " + 'X["a"]=4',
            [],
            returncode=1,
        )

    def test_063_local_51_position_integer_04(self):
        self.verify(
            "local dictionary X[currentposition]=3 " + "X[ k ]=4",
            [],
            returncode=1,
        )

    def test_063_local_51_position_integer_05(self):
        self.verify(
            "local dictionary X[currentposition]=3 " + "X[to]=4",
            [],
            returncode=1,
        )

    def test_063_local_51_position_integer_06(self):
        self.verify(
            "local dictionary X[currentposition]=3 "
            + 'X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_51_position_integer_07(self):
        self.verify(
            "local dictionary X[currentposition]=3 " + "X[currentposition]=k",
            [],
            returncode=1,
        )

    def test_063_local_51_position_integer_08(self):
        self.verify(
            "local dictionary X[currentposition]=3 " + "X[currentposition]=to",
            [],
            returncode=1,
        )

    def test_063_local_51_position_integer_09(self):
        self.verify(
            "local dictionary X[currentposition]=3 "
            + "X[currentposition]=initialposition",
            [],
            returncode=1,
        )

    def test_063_local_52_position_position_01(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + "X[currentposition]=currentposition "
            + "X[initialposition]=currentposition",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "InitialPosition"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "CurrentPosition"),
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "CurrentPosition"),
            ],
        )

    def test_063_local_52_position_position_02(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + "X[1]=currentposition",
            [],
            returncode=1,
        )

    def test_063_local_52_position_position_03(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + 'X["a"]=currentposition',
            [],
            returncode=1,
        )

    def test_063_local_52_position_position_04(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + "X[ k ]=currentposition",
            [],
            returncode=1,
        )

    def test_063_local_52_position_position_05(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + "X[to]=currentposition",
            [],
            returncode=1,
        )

    def test_063_local_52_position_position_06(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + "X[currentposition]=1",
            [],
            returncode=1,
        )

    def test_063_local_52_position_position_07(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + 'X[currentposition]="a"',
            [],
            returncode=1,
        )

    def test_063_local_52_position_position_08(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + "X[currentposition]=k",
            [],
            returncode=1,
        )

    def test_063_local_52_position_position_09(self):
        self.verify(
            "local dictionary X[currentposition]=initialposition "
            + "X[currentposition]=to",
            [],
            returncode=1,
        )

    def test_063_local_53_variable_integer(self):
        self.verify("local X=1", [], returncode=1)

    def test_063_local_54_variable_string(self):
        self.verify('local X="a"', [], returncode=1)

    def test_063_local_55_variable_set(self):
        self.verify("local X=connectedpawns", [], returncode=1)

    def test_063_local_56_variable_piecedesignator(self):
        self.verify("local X=q", [], returncode=1)

    def test_063_local_57_variable_logical(self):
        self.verify("local X=true", [], returncode=1)

    def test_063_local_58_variable_position(self):
        self.verify("local X=currentposition", [], returncode=1)

    def test_063_local_80_no_value_01_integer_01_literal(self):
        con = self.verify(
            "local dictionary X X[1]",
            [
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "Integer"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_01_integer_02_filter(self):
        con = self.verify(
            "local dictionary X X[ply]",
            [
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "Ply"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_01_integer_03_variable(self):
        con = self.verify(
            "v=3 local dictionary X X[v]",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "Variable"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_02_string_01_literal(self):
        con = self.verify(
            'local dictionary X X["a"]',
            [
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "String"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_02_string_02_filter(self):
        con = self.verify(
            "local dictionary X X[fen]",
            [
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "FEN"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_02_string_03_variable(self):
        con = self.verify(
            'v="a" local dictionary X X[v]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "Variable"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_03_set_01_literal(self):
        # A piece designator.
        con = self.verify(
            "local dictionary X X[ a ]",
            [
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "PieceDesignator"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_03_set_02_filter(self):
        con = self.verify(
            "local dictionary X X[to]",
            [
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "To"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_03_set_03_variable(self):
        con = self.verify(
            "v=k local dictionary X X[v]",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "PieceDesignator"),
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "Variable"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_04_position_01_literal(self):
        # No position literals.
        # This implies an arbitrary single filter of allowed types is ok.
        con = self.verify(
            "local dictionary X X[position 0]",
            [
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "Position"),
                (5, "Integer"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_04_position_02_filter(self):
        con = self.verify(
            "local dictionary X X[currentposition]",
            [
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "CurrentPosition"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_04_position_03_variable(self):
        con = self.verify(
            "v=initialposition local dictionary X X[v]",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "InitialPosition"),
                (3, "Dictionary"),
                (3, "BracketLeft"),
                (4, "Dictionary"),
                (4, "Variable"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type
            is cqltypes.PersistenceType.LOCAL,
            True,
        )

    def test_063_local_80_no_value_05_logical_01_literal(self):
        # No logical literals.
        # This implies an arbitrary single filter of allowed types is ok.
        self.verify("local dictionary X X[1 and 2]", [], returncode=1)

    def test_063_local_80_no_value_05_logical_02_filter(self):
        self.verify("local dictionary X X[true]", [], returncode=1)

    def test_063_local_80_no_value_05_logical_03_variable(self):
        self.verify("v=false local dictionary X X[v]", [], returncode=1)


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterDictionaryLocal))
