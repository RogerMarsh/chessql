# test_filter_dictionary.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'dictionary' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FilterDictionary(verify.Verify):

    def test_027_dictionary_01_bare(self):
        self.verify("dictionary", [], returncode=1)

    def test_027_dictionary_02_bad_name(self):
        self.verify(" dictionary k", [], returncode=1)

    def test_027_dictionary_03_good_name(self):
        self.verify(" dictionary X", [(3, "Dictionary")])

    def test_027_dictionary_04_string_string(self):
        self.verify(
            'dictionary X["a"]="bc"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
            ],
        )

    def test_027_dictionary_05_string_set_01_piecedesignator(self):
        self.verify(
            'dictionary X["a"]=k',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "PieceDesignator"),
            ],
        )

    def test_027_dictionary_05_string_set_02_some_other_set(self):
        self.verify(
            'dictionary X["a"]=connectedpawns',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "ConnectedPawns"),
            ],
        )

    def test_027_dictionary_06_string_integer(self):
        self.verify(
            'dictionary X["a"]=1',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "Integer"),
            ],
        )

    def test_027_dictionary_07_string_position(self):
        self.verify('dictionary X["a"]=currentposition', [], returncode=1)

    def test_027_dictionary_08_string_logical(self):
        self.verify('dictionary X["a"]=false', [], returncode=1)

    def test_027_dictionary_09_set_string(self):
        self.verify(
            'dictionary X[to]="bc"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "String"),
            ],
        )

    def test_027_dictionary_10_set_set_01_piece_designator(self):
        self.verify(
            "dictionary X[to]=k",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "PieceDesignator"),
            ],
        )

    def test_027_dictionary_10_set_set_02_some_other_set(self):
        self.verify(
            "dictionary X[to]=from",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "From"),
            ],
        )

    def test_027_dictionary_11_set_integer(self):
        self.verify(
            "dictionary X[to]=3",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "Integer"),
            ],
        )

    def test_027_dictionary_12_set_position(self):
        self.verify("dictionary X[to]=currentposition", [], returncode=1)

    def test_027_dictionary_13_string_logical(self):
        self.verify("dictionary X[to]=false", [], returncode=1)

    def test_027_dictionary_14_integer_string(self):
        self.verify(
            'dictionary X[3]="bc"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
            ],
        )

    def test_027_dictionary_15_integer_set_01_piece_designator(self):
        self.verify(
            "dictionary X[3]=qa5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "PieceDesignator"),
            ],
        )

    def test_027_dictionary_15_integer_set_02_some_other_set(self):
        self.verify(
            "dictionary X[3]=from",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "From"),
            ],
        )

    def test_027_dictionary_16_integer_integer(self):
        self.verify(
            "dictionary X[3]=3",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_027_dictionary_17_integer_position(self):
        self.verify("dictionary X[3]=currentposition", [], returncode=1)

    def test_027_dictionary_18_integer_logical(self):
        self.verify("dictionary X[3]=false", [], returncode=1)

    def test_027_dictionary_19_bad_piecedesignator_string(self):
        self.verify('dictionary X[a5]="bc"', [], returncode=1)

    def test_027_dictionary_20_bad_piecedesignator_set_01_piece_designator(
        self,
    ):
        self.verify("dictionary X[a5]=h2", [], returncode=1)

    def test_027_dictionary_20_bad_piecedesignator_set_02_some_other_set(self):
        self.verify("dictionary X[a5]=from", [], returncode=1)

    def test_027_dictionary_21_bad_piecedesignator_integer(self):
        self.verify("dictionary X[a5]=3", [], returncode=1)

    def test_027_dictionary_22_bad_piecedesignator_position(self):
        self.verify("dictionary X[a5]=currentposition", [], returncode=1)

    def test_027_dictionary_23_bad_piecedesignator_logical(self):
        self.verify("dictionary X[a5]=false", [], returncode=1)

    def test_027_dictionary_24_piecedesignator_string(self):
        self.verify(
            'dictionary X[ a5 ]="bc"',  # chessql accepts '[ a5]' too.
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "String"),
            ],
        )

    def test_027_dictionary_25_piecedesignator_set_01_piece_designator(self):
        self.verify(
            "dictionary X[ a5 ]=d7",  # chessql accepts '[ a5]' too.
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_027_dictionary_25_piecedesignator_set_02_some_other_set(self):
        self.verify(
            "dictionary X[ a5 ]=from",  # chessql accepts '[ a5]' too.
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "From"),
            ],
        )

    def test_027_dictionary_26_piecedesignator_integer(self):
        self.verify(
            "dictionary X[ a5 ]=3",  # chessql accepts '[ a5]' too.
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_027_dictionary_27_piecedesignator_position(self):
        self.verify("dictionary X[ a5 ]=currentposition", [], returncode=1)

    def test_027_dictionary_28_logical_string(self):
        self.verify('dictionary X[true]="bc"', [], returncode=1)

    def test_027_dictionary_29_logical_set_01_piece_designator(self):
        self.verify("dictionary X[true]=k", [], returncode=1)

    def test_027_dictionary_29_logical_set_02_some_other_set(self):
        self.verify("dictionary X[true]=from", [], returncode=1)

    def test_027_dictionary_30_logical_integer(self):
        self.verify("dictionary X[true]=3", [], returncode=1)

    def test_027_dictionary_31_logical_position(self):
        self.verify("dictionary X[true]=currentposition", [], returncode=1)

    def test_027_dictionary_32_logical_logical(self):
        self.verify("dictionary X[true]=false", [], returncode=1)

    def test_027_dictionary_33_piecedesignator_logical(self):
        self.verify("dictionary X[ a5 ]=false", [], returncode=1)

    def test_027_dictionary_34_string_string_01(self):
        self.verify(
            'dictionary X["a"]="bc" X["a"]="yz" X["b"]="ij"',
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

    def test_027_dictionary_34_string_string_02(self):
        self.verify('dictionary X["a"]="bc" X[to]="yz"', [], returncode=1)

    def test_027_dictionary_34_string_string_03(self):
        self.verify('dictionary X["a"]="bc" X[ k ]="yz"', [], returncode=1)

    def test_027_dictionary_34_string_string_04(self):
        self.verify('dictionary X["a"]="bc" X[1]="yz"', [], returncode=1)

    def test_027_dictionary_34_string_string_05(self):
        self.verify('dictionary X["a"]="bc" X["a"]=to', [], returncode=1)

    def test_027_dictionary_34_string_string_06(self):
        self.verify('dictionary X["a"]="bc" X["a"]=k', [], returncode=1)

    def test_027_dictionary_34_string_string_07(self):
        self.verify('dictionary X["a"]="bc" X["a"]=1', [], returncode=1)

    def test_027_dictionary_35_string_set_01_piecedesignator_01(self):
        self.verify(
            'dictionary X["a"]=k X["a"]=Pa6 X["b"]=R',
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

    def test_027_dictionary_35_string_set_01_piecedesignator_02(self):
        self.verify('dictionary X["a"]=k X[to]=k', [], returncode=1)

    def test_027_dictionary_35_string_set_01_piecedesignator_03(self):
        self.verify('dictionary X["a"]=k X[ k ]=k', [], returncode=1)

    def test_027_dictionary_35_string_set_01_piecedesignator_04(self):
        self.verify('dictionary X["a"]=k X[1]=k', [], returncode=1)

    def test_027_dictionary_35_string_set_01_piecedesignator_05(self):
        self.verify('dictionary X["a"]=k X["a"]=1', [], returncode=1)

    def test_027_dictionary_35_string_set_01_piecedesignator_06(self):
        self.verify('dictionary X["a"]=k X["a"]="a"', [], returncode=1)

    def test_027_dictionary_35_string_set_02_some_other_set_01(self):
        self.verify(
            'dictionary X["a"]=connectedpawns X["a"]=to X["b"]=from',
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

    def test_027_dictionary_35_string_set_02_some_other_set_02(self):
        self.verify(
            'dictionary X["a"]=connectedpawns X[1]=connectedpawns',
            [],
            returncode=1,
        )

    def test_027_dictionary_35_string_set_02_some_other_set_03(self):
        self.verify(
            'dictionary X["a"]=connectedpawns X[ k ]=connectedpawns',
            [],
            returncode=1,
        )

    def test_027_dictionary_35_string_set_02_some_other_set_04(self):
        self.verify(
            'dictionary X["a"]=connectedpawns X[to]=connectedpawns',
            [],
            returncode=1,
        )

    def test_027_dictionary_35_string_set_02_some_other_set_05(self):
        self.verify(
            'dictionary X["a"]=connectedpawns X["a"]=1',
            [],
            returncode=1,
        )

    def test_027_dictionary_35_string_set_02_some_other_set_06(self):
        self.verify(
            'dictionary X["a"]=connectedpawns X["a"]="a"',
            [],
            returncode=1,
        )

    def test_027_dictionary_36_string_integer_01(self):
        self.verify(
            'dictionary X["a"]=1 X["a"]=7 X["b"]=4',
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

    def test_027_dictionary_36_string_integer_02(self):
        self.verify('dictionary X["a"]=1 X[1]=1', [], returncode=1)

    def test_027_dictionary_36_string_integer_03(self):
        self.verify('dictionary X["a"]=1 X[ k ]=1', [], returncode=1)

    def test_027_dictionary_36_string_integer_04(self):
        self.verify('dictionary X["a"]=1 X[to]=1', [], returncode=1)

    def test_027_dictionary_36_string_integer_05(self):
        self.verify('dictionary X["a"]=1 X["a"]=k', [], returncode=1)

    def test_027_dictionary_36_string_integer_06(self):
        self.verify('dictionary X["a"]=1 X["a"]=to', [], returncode=1)

    def test_027_dictionary_36_string_integer_07(self):
        self.verify('dictionary X["a"]=1 X["a"]="a"', [], returncode=1)

    def test_027_dictionary_37_set_string_01(self):
        self.verify(
            'dictionary X[to]="bc" X[to]="yz" X[from]="mn" X[ Q ]="kh"',
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

    def test_027_dictionary_37_set_string_02(self):
        self.verify('dictionary X[to]="bc" X[1]="bc"', [], returncode=1)

    def test_027_dictionary_37_set_string_03(self):
        self.verify('dictionary X[to]="bc" X["a"]="bc"', [], returncode=1)

    def test_027_dictionary_37_set_string_04(self):
        self.verify('dictionary X[to]="bc" X[to]=1', [], returncode=1)

    def test_027_dictionary_37_set_string_05(self):
        self.verify('dictionary X[to]="bc" X[to]=k', [], returncode=1)

    def test_027_dictionary_37_set_string_06(self):
        self.verify('dictionary X[to]="bc" X[to]=from', [], returncode=1)

    def test_027_dictionary_38_set_set_01_piecedesignator_01(self):
        self.verify(
            "dictionary X[to]=k X[to]=R X[from]=Q X[ a5 ]=connectedpawns",
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

    def test_027_dictionary_38_set_set_01_piecedesignator_02(self):
        self.verify("dictionary X[to]=k X[1]=k", [], returncode=1)

    def test_027_dictionary_38_set_set_01_piecedesignator_03(self):
        self.verify('dictionary X[to]=k X["a"]=k', [], returncode=1)

    def test_027_dictionary_38_set_set_01_piecedesignator_04(self):
        self.verify("dictionary X[to]=k X[to]=1", [], returncode=1)

    def test_027_dictionary_38_set_set_01_piecedesignator_05(self):
        self.verify('dictionary X[to]=k X[to]="a"', [], returncode=1)

    def test_027_dictionary_38_set_set_01_piecedesignator_06(self):
        self.verify("dictionary X[to]=k X[1]=2", [], returncode=1)

    def test_027_dictionary_38_set_set_02_some_other_set_01(self):
        self.verify(
            "dictionary X[to]=from X[to]=to X[from]=to X[ b6 ]=c4",
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

    def test_027_dictionary_38_set_set_02_some_other_set_02(self):
        self.verify("dictionary X[to]=from X[1]=from", [], returncode=1)

    def test_027_dictionary_38_set_set_02_some_other_set_03(self):
        self.verify('dictionary X[to]=from X["a"]=from', [], returncode=1)

    def test_027_dictionary_38_set_set_02_some_other_set_04(self):
        self.verify("dictionary X[to]=from X[to]=1", [], returncode=1)

    def test_027_dictionary_38_set_set_02_some_other_set_05(self):
        self.verify('dictionary X[to]=from X[to]="a"', [], returncode=1)

    def test_027_dictionary_38_set_set_02_some_other_set_06(self):
        self.verify('dictionary X[to]=from X[1]="a"', [], returncode=1)

    def test_027_dictionary_39_set_integer_01(self):
        self.verify(
            "dictionary X[to]=3 X[to]=7 X[from]=4 X[ rh8 ]=1",
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

    def test_027_dictionary_39_set_integer_02(self):
        self.verify("dictionary X[to]=3 X[1]=3", [], returncode=1)

    def test_027_dictionary_39_set_integer_03(self):
        self.verify('dictionary X[to]=3 X["a"]=3', [], returncode=1)

    def test_027_dictionary_39_set_integer_04(self):
        self.verify("dictionary X[to]=3 X[to]=k", [], returncode=1)

    def test_027_dictionary_39_set_integer_05(self):
        self.verify("dictionary X[to]=3 X[to]=from", [], returncode=1)

    def test_027_dictionary_39_set_integer_06(self):
        self.verify('dictionary X[to]=3 X[to]="a"', [], returncode=1)

    def test_027_dictionary_39_set_integer_07(self):
        self.verify("dictionary X[to]=3 X[1]=from", [], returncode=1)

    def test_027_dictionary_40_integer_string_01(self):
        self.verify(
            'dictionary X[3]="bc" X[3]="xz" X[4]="mn"',
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

    def test_027_dictionary_40_integer_string_02(self):
        self.verify('dictionary X[3]="bc" X["a"]="bc"', [], returncode=1)

    def test_027_dictionary_40_integer_string_03(self):
        self.verify('dictionary X[3]="bc" X[ k ]="bc"', [], returncode=1)

    def test_027_dictionary_40_integer_string_04(self):
        self.verify('dictionary X[3]="bc" X[to]="bc"', [], returncode=1)

    def test_027_dictionary_40_integer_string_05(self):
        self.verify('dictionary X[3]="bc" X[3]=1', [], returncode=1)

    def test_027_dictionary_40_integer_string_06(self):
        self.verify('dictionary X[3]="bc" X[3]=k', [], returncode=1)

    def test_027_dictionary_40_integer_string_07(self):
        self.verify('dictionary X[3]="bc" X[3]=from', [], returncode=1)

    def test_027_dictionary_41_integer_set_01_piecedesignator_01(self):
        self.verify(
            "dictionary X[3]=qa5 X[3]=g2 X[4]=[KQ]a5",
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

    def test_027_dictionary_41_integer_set_01_piecedesignator_02(self):
        self.verify('dictionary X[3]=qa5 X["a"]=qa5', [], returncode=1)

    def test_027_dictionary_41_integer_set_01_piecedesignator_03(self):
        self.verify("dictionary X[3]=qa5 X[ k ]=qa5", [], returncode=1)

    def test_027_dictionary_41_integer_set_01_piecedesignator_04(self):
        self.verify("dictionary X[3]=qa5 X[from]=qa5", [], returncode=1)

    def test_027_dictionary_41_integer_set_01_piecedesignator_05(self):
        self.verify("dictionary X[3]=qa5 X[3]=1", [], returncode=1)

    def test_027_dictionary_41_integer_set_01_piecedesignator_06(self):
        self.verify('dictionary X[3]=qa5 X[3]="a"', [], returncode=1)

    def test_027_dictionary_42_integer_set_02_some_other_set_01(self):
        self.verify(
            "dictionary X[3]=from X[3]=to X[5]=connectedpawns",
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

    def test_027_dictionary_42_integer_set_02_some_other_set_02(self):
        self.verify('dictionary X[3]=from X["a"]=from', [], returncode=1)

    def test_027_dictionary_42_integer_set_02_some_other_set_03(self):
        self.verify("dictionary X[3]=from X[ k ]=from", [], returncode=1)

    def test_027_dictionary_42_integer_set_02_some_other_set_04(self):
        self.verify("dictionary X[3]=from X[to]=from", [], returncode=1)

    def test_027_dictionary_42_integer_set_02_some_other_set_05(self):
        self.verify("dictionary X[3]=from X[3]=1", [], returncode=1)

    def test_027_dictionary_42_integer_set_02_some_other_set_06(self):
        self.verify('dictionary X[3]=from X[3]="a"', [], returncode=1)

    def test_027_dictionary_43_integer_integer_01(self):
        self.verify(
            "dictionary X[3]=3 X[3]=6 X[7]=4",
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

    def test_027_dictionary_43_integer_integer_02(self):
        self.verify('dictionary X[3]=3 X["a"]=3', [], returncode=1)

    def test_027_dictionary_43_integer_integer_03(self):
        self.verify("dictionary X[3]=3 X[ k ]=3", [], returncode=1)

    def test_027_dictionary_43_integer_integer_04(self):
        self.verify("dictionary X[3]=3 X[to]=3", [], returncode=1)

    def test_027_dictionary_43_integer_integer_05(self):
        self.verify('dictionary X[3]=3 X[3]="a"', [], returncode=1)

    def test_027_dictionary_43_integer_integer_06(self):
        self.verify("dictionary X[3]=3 X[3]=k", [], returncode=1)

    def test_027_dictionary_43_integer_integer_07(self):
        self.verify("dictionary X[3]=3 X[3]=to", [], returncode=1)

    def test_027_dictionary_44_piecedesignator_string_01(self):
        self.verify(  # chessql accepts '[ a5]' too.
            'dictionary X[ a5 ]="bc" X[ a5 ]="xz" X[ R ]="mn" X[to]="bc"',
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

    def test_027_dictionary_44_piecedesignator_string_02(self):
        self.verify('dictionary X[ a5 ]="bc" X[1]="bc"', [], returncode=1)

    def test_027_dictionary_44_piecedesignator_string_03(self):
        self.verify('dictionary X[ a5 ]="bc" X["a5"]="bc"', [], returncode=1)

    def test_027_dictionary_44_piecedesignator_string_04(self):
        self.verify('dictionary X[ a5 ]="bc" X[ a5 ]=1', [], returncode=1)

    def test_027_dictionary_44_piecedesignator_string_05(self):
        self.verify('dictionary X[ a5 ]="bc" X[ a5 ]=k', [], returncode=1)

    def test_027_dictionary_44_piecedesignator_string_06(self):
        self.verify('dictionary X[ a5 ]="bc" X[ a5 ]=to', [], returncode=1)

    def test_027_dictionary_45_piecedesignator_set_01_piecedesignator_01(self):
        self.verify(  # chessql accepts '[ a5]' too.
            "dictionary X[ a5 ]=d7 X[ a5 ]=K X[ k ]=Q X[ to ]=h7",
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

    def test_027_dictionary_45_piecedesignator_set_01_piecedesignator_02(self):
        self.verify("dictionary X[ a5 ]=d7 X[1]=d7", [], returncode=1)

    def test_027_dictionary_45_piecedesignator_set_01_piecedesignator_03(self):
        self.verify('dictionary X[ a5 ]=d7 X["a5"]=d7', [], returncode=1)

    def test_027_dictionary_45_piecedesignator_set_01_piecedesignator_04(self):
        self.verify("dictionary X[ a5 ]=d7 X[ a5 ]=1", [], returncode=1)

    def test_027_dictionary_45_piecedesignator_set_01_piecedesignator_05(self):
        self.verify('dictionary X[ a5 ]=d7 X[ a5 ]="a"', [], returncode=1)

    def test_027_dictionary_45_piecedesignator_set_02_some_other_set_01(self):
        self.verify(  # chessql accepts '[ a5]' too.
            "dictionary X[ a5 ]=from X[ a5 ]=to X[ h5 ]=connectedpawns "
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

    def test_027_dictionary_45_piecedesignator_set_02_some_other_set_02(self):
        self.verify("dictionary X[ a5 ]=from X[1]=from", [], returncode=1)

    def test_027_dictionary_45_piecedesignator_set_02_some_other_set_03(self):
        self.verify('dictionary X[ a5 ]=from X["a5"]=from', [], returncode=1)

    def test_027_dictionary_45_piecedesignator_set_02_some_other_set_04(self):
        self.verify("dictionary X[ a5 ]=from X[ a5 ]=1", [], returncode=1)

    def test_027_dictionary_45_piecedesignator_set_02_some_other_set_05(self):
        self.verify('dictionary X[ a5 ]=from X[ a5 ]="a"', [], returncode=1)

    def test_027_dictionary_46_piecedesignator_integer_01(self):
        self.verify(  # chessql accepts '[ a5]' too.
            "dictionary X[ a5 ]=3 X[ a5 ]=4 X[ h2 ]=3 X[to]=8",
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

    def test_027_dictionary_46_piecedesignator_integer_02(self):
        self.verify("dictionary X[ a5 ]=3 X[1]=3", [], returncode=1)

    def test_027_dictionary_46_piecedesignator_integer_03(self):
        self.verify('dictionary X[ a5 ]=3 X["a5"]=3', [], returncode=1)

    def test_027_dictionary_46_piecedesignator_integer_04(self):
        self.verify("dictionary X[ a5 ]=3 X[ a5 ]=k", [], returncode=1)

    def test_027_dictionary_46_piecedesignator_integer_05(self):
        self.verify("dictionary X[ a5 ]=3 X[ a5 ]=to", [], returncode=1)

    def test_027_dictionary_46_piecedesignator_integer_06(self):
        self.verify('dictionary X[ a5 ]=3 X[ a5 ]="a"', [], returncode=1)


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterDictionary))
