# test_filters.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for individual filters.

See test_filter_captures for '[x]' filter tests.

See test_filter_dash for '--' filter tests.

See test_filter_path for 'path' filter tests.

See test_filters_iteration for square and piece '<iteration>' filter tests.

The verification methods are provided by the Verify superclass.

Generally the test statements are the simplest which are accepted by CQL
for each filter.  Sometimes these will not make sense as queries to
evaluate.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class Filters(verify.Verify):

    def test_000__error(self):
        self.verify("bt", [], returncode=1)

    def test_001_abs(self):
        self.verify("abs 1", [(3, "Abs"), (4, "Integer")])

    def test_002_ancestor(self):
        self.verify(
            "ancestor(position 1 position 2)",
            [
                (3, "Ancestor"),
                (4, "Position"),
                (5, "Integer"),
                (4, "Position"),
                (5, "Integer"),
            ],
        )

    def test_003_and(self):
        self.verify("1 and 2", [(3, "And"), (4, "Integer"), (4, "Integer")])

    def test_004_ascii_01(self):
        self.verify('ascii "A"', [(3, "ASCII"), (4, "String")])

    def test_004_ascii_02(self):
        self.verify("ascii 65", [(3, "ASCII"), (4, "Integer")])

    def test_005_assert(self):
        self.verify("assert 1", [(3, "Assert"), (4, "Integer")])

    def test_006_atomic_01_bare(self):
        self.verify("atomic", [], returncode=1)

    def test_006_atomic_02_name(self):
        self.verify("atomic X", [], returncode=1)

    def test_006_atomic_03_variable_integer(self):
        self.verify(
            "atomic X=1",
            [(3, "Assign"), (4, "Atomic"), (4, "Integer")],
        )

    def test_006_atomic_04_variable_string(self):
        self.verify(
            'atomic X="a"',
            [(3, "Assign"), (4, "Atomic"), (4, "String")],
        )

    def test_006_atomic_05_variable_set(self):
        self.verify(
            "atomic X=connectedpawns",
            [(3, "Assign"), (4, "Atomic"), (4, "ConnectedPawns")],
        )

    def test_006_atomic_06_variable_piecedesignator(self):
        self.verify(
            "atomic X=q",
            [(3, "Assign"), (4, "Atomic"), (4, "PieceDesignator")],
        )

    def test_006_atomic_07_variable_logical(self):
        self.verify("atomic X=false", [], returncode=1)

    def test_006_atomic_08_variable_position(self):
        self.verify(
            "atomic X=currentposition",
            [(3, "Assign"), (4, "Atomic"), (4, "CurrentPosition")],
        )

    def test_006_atomic_09_atomic_first(self):
        con = self.verify(
            "atomic X=1 X=2",
            [
                (3, "Assign"),
                (4, "Atomic"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type,
            cqltypes.PersistenceType.ATOMIC | cqltypes.PersistenceType.LOCAL,
        )

    def test_006_atomic_10_atomic_second(self):
        con = self.verify(
            "X=1 atomic X=2",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "Atomic"),
                (4, "Integer"),
            ],
        )
        self.assertEqual(
            con.definitions["X"].persistence_type,
            cqltypes.PersistenceType.LOCAL,
        )

    def test_006_atomic_11_atomic_persistent(self):
        self.verify("atomic X=1 persistent X=2", [], returncode=1)

    def test_006_atomic_12_variable_plus_equal(self):
        self.verify("atomic X+=1", [], returncode=1)

    def test_006_atomic_13_variable_minus_equal(self):
        self.verify("atomic X-=1", [], returncode=1)

    def test_006_atomic_14_variable_multiply_equal(self):
        self.verify("atomic X*=1", [], returncode=1)

    def test_006_atomic_15_variable_divide_equal(self):
        self.verify("atomic X/=1", [], returncode=1)

    def test_006_atomic_16_variable_modulus_equal(self):
        self.verify("atomic X%=1", [], returncode=1)

    def test_007_attackedby(self):
        self.verify(
            "_ attackedby k",
            [
                (3, "AttackedBy"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_008_attacks(self):
        self.verify(
            "A attacks k",
            [
                (3, "Attacks"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_009_between(self):
        self.verify(
            "between(R k)",
            [
                (3, "Between"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_010_black(self):
        self.verify("black", [(3, "Black")])

    def test_011_btm(self):
        self.verify("btm", [(3, "BTM")])

    def test_012_castle(self):
        self.verify("castle", [(3, "Castle")])

    def test_013_check(self):
        self.verify("check", [(3, "Check")])

    def test_014_child_01(self):
        self.verify(
            "check(3)",
            [(3, "Check"), (3, "ParenthesisLeft"), (4, "Integer")],
        )

    def test_014_child_02(self):
        self.verify("check", [(3, "Check")])

    def test_015_colortype(self):
        self.verify("colortype d4", [(3, "ColorType"), (4, "PieceDesignator")])

    def test_016_comment_01(self):
        self.verify(
            'comment("x is" A)',
            [(3, "CommentParentheses"), (4, "String"), (4, "PieceDesignator")],
        )

    def test_016_comment_02(self):
        self.verify(
            'comment "x is"',
            [(3, "Comment"), (4, "String")],
        )

    def test_016_comment_03(self):
        self.verify(
            "comment A",
            [(3, "Comment"), (4, "PieceDesignator")],
        )

    # Documentation for 'message' filter claims same syntax as 'comment'
    # filter.  The 'quiet' keyword is not mentioned for 'comment' filter.
    def test_016_comment_04(self):
        self.verify("comment quiet (A)", [], returncode=1)

    def test_017_connectedpawns(self):
        self.verify("connectedpawns", [(3, "ConnectedPawns")])

    def test_018_consecutivemoves_01(self):
        self.verify(
            "consecutivemoves(position 1 position 2)",
            [],
            returncode=1,
        )

    def test_018_consecutivemoves_02(self):
        self.verify(
            "p1=position 1 consecutivemoves(p1)",
            [],
            returncode=1,
        )

    def test_018_consecutivemoves_03(self):
        self.verify(
            "p1=position 1 p2=position 2 consecutivemoves(p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "ConsecutiveMoves"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_018_consecutivemoves_04(self):
        self.verify(
            "p1=position 1 p2=position 2 consecutivemoves quiet(p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "ConsecutiveMoves"),
                (4, "Quiet"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_018_consecutivemoves_05(self):
        self.verify(
            "p1=position 1 p2=position 2 consecutivemoves 1 2 (p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "ConsecutiveMoves"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_018_consecutivemoves_06(self):  # Fails.
        self.verify(
            "p1=position 1 p2=position 2 consecutivemoves 1 quiet (p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "ConsecutiveMoves"),
                (4, "Quiet"),
                (4, "RangeInteger"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_018_consecutivemoves_07(self):
        self.verify(
            "p1=position 1 p2=position 2 consecutivemoves quiet 1(p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "ConsecutiveMoves"),
                (4, "Quiet"),
                (4, "RangeInteger"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_018_consecutivemoves_08(self):
        self.verify(
            "p1=position 1 p2=position 2 consecutivemoves 1 rv(p1 p2)",
            [],
            returncode=1,
        )

    def test_018_consecutivemoves_09(self):
        self.verify(
            'rv="a" p1=position 1 p2=position 2 consecutivemoves 1 rv(p1 p2)',
            [],
            returncode=1,
        )

    def test_018_consecutivemoves_10(self):
        self.verify(
            "rv=1 p1=position 1 p2=position 2 consecutivemoves 1 rv(p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "ConsecutiveMoves"),
                (4, "RangeInteger"),
                (4, "RangeVariable"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_019_countmoves_01(self):
        self.verify("countmoves", [], returncode=1)

    def test_019_countmoves_02(self):
        self.verify("countmoves k", [], returncode=1)

    def test_019_countmoves_03_move(self):
        self.verify(
            "countmoves --",
            [
                (3, "CountMoves"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_019_countmoves_04_legal(self):
        self.verify(
            "countmoves legal --",
            [
                (3, "CountMoves"),
                (4, "Legal"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_019_countmoves_05_pseudolegal(self):
        self.verify(
            "countmoves pseudolegal --",
            [
                (3, "CountMoves"),
                (4, "Pseudolegal"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_020_currentmove_01(self):
        self.verify("currentmove", [], returncode=1)

    def test_020_currentmove_02(self):
        self.verify("currentmove k", [], returncode=1)

    def test_020_currentmove_03(self):
        self.verify(
            "currentmove --",
            [
                (3, "CurrentMove"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_021_currentposition_ascii(self):
        self.verify("currentposition", [(3, "CurrentPosition")])

    def test_021_currentposition_utf8(self):
        self.verify("∙", [(3, "CurrentPosition")])

    def test_022_currenttransform(self):
        self.verify("currenttransform", [(3, "CurrentTransform")])

    def test_023_dark(self):
        self.verify("dark B", [(3, "Dark"), (4, "PieceDesignator")])

    def test_024_date(self):
        self.verify("date", [(3, "Date")])

    def test_025_depth(self):
        self.verify("depth", [(3, "Depth")])

    def test_026_descendant_01(self):
        self.verify(
            "descendant(position 1 position 2)",
            [
                (3, "Descendant"),
                (4, "Position"),
                (5, "Integer"),
                (4, "Position"),
                (5, "Integer"),
            ],
        )

    def test_026_descendant_02(self):
        self.verify(
            "p1=position 1 p2=position 2 descendant(p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Descendant"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

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

    def test_028_distance_01(self):
        self.verify(
            "distance(position 1 position 2)",
            [
                (3, "Distance"),
                (4, "Position"),
                (5, "Integer"),
                (4, "Position"),
                (5, "Integer"),
            ],
        )

    def test_028_distance_02(self):
        self.verify(
            "p1=position 1 p2=position 2 distance(p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Distance"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_029_doubledpawns(self):
        self.verify("doubledpawns", [(3, "DoubledPawns")])

    def test_030_down_01(self):
        self.verify("down", [], returncode=1)

    def test_030_down_02(self):
        self.verify(
            "down P",
            [
                (3, "Down"),
                (4, "PieceDesignator"),
            ],
        )

    def test_030_down_03(self):
        self.verify(
            "down 1 4 P",
            [
                (3, "Down"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "PieceDesignator"),
            ],
        )

    def test_030_echo_01(self):
        self.verify("echo(R k)", [], returncode=1)

    def test_030_echo_02(self):
        self.verify("s=position 1 t=position 2 echo(s t)", [], returncode=1)

    def test_030_echo_03(self):
        self.verify(
            "s=position 1 t=position 2 echo(s t) k",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Echo"),
                (4, "Variable"),
                (4, "Variable"),
                (4, "PieceDesignator"),
            ],
        )

    def test_030_echo_04(self):
        self.verify(
            "s=position 1 t=position 2 echo quiet (s t) k",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Echo"),
                (4, "Quiet"),
                (4, "Variable"),
                (4, "Variable"),
                (4, "PieceDesignator"),
            ],
        )

    def test_030_echo_05(self):
        self.verify(
            "s=position 1 t=position 2 echo (s t) in all k",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Echo"),
                (4, "InAll"),
                (4, "Variable"),
                (4, "Variable"),
                (4, "PieceDesignator"),
            ],
        )

    def test_030_echo_06(self):
        self.verify(
            "s=position 1 t=position 2 echo quiet (s t) in all k",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Echo"),
                (4, "Quiet"),
                (4, "InAll"),
                (4, "Variable"),
                (4, "Variable"),
                (4, "PieceDesignator"),
            ],
        )

    def test_031_eco(self):
        self.verify("eco", [(3, "ECO")])

    def test_032_elo_01(self):
        self.verify("elo", [(3, "Elo")])

    def test_032_elo_02(self):
        self.verify("elo black", [(3, "Elo")])

    def test_032_elo_03(self):
        self.verify("elo white", [(3, "Elo")])

    def test_032_elo_04(self):
        self.verify("elo white k", [(3, "Elo"), (3, "PieceDesignator")])

    def test_033_event(self):
        self.verify("event", [(3, "Event")])

    def test_034_eventdate_01(self):
        self.verify("eventdate", [(3, "EventDate")])

    def test_035_false(self):
        self.verify("false", [(3, "False_")])

    def test_036_fen(self):
        self.verify("fen", [(3, "FEN")])

    def test_037_file_01(self):
        self.verify("file", [], returncode=1)

    def test_037_file_02(self):
        self.verify(
            "file P",
            [
                (3, "File"),
                (4, "PieceDesignator"),
            ],
        )

    def test_038_find_01(self):
        self.verify("find", [], returncode=1)

    def test_038_find_02(self):
        self.verify("find check", [(3, "Find"), (4, "Check")])

    def test_038_find_03(self):
        self.verify("find all check", [(3, "Find"), (4, "All"), (4, "Check")])

    def test_038_find_04(self):
        self.verify(
            "find quiet check",
            [(3, "Find"), (4, "Quiet"), (4, "Check")],
        )

    def test_038_find_05(self):
        self.verify(
            "find 3 check", [(3, "Find"), (4, "RangeInteger"), (4, "Check")]
        )

    def test_038_find_06(self):
        self.verify(
            "find 3 10 check",
            [
                (3, "Find"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "Check"),
            ],
        )

    def test_038_find_07(self):
        self.verify(
            "find <-- check", [(3, "Find"), (4, "FindBackward"), (4, "Check")]
        )

    def test_038_find_08(self):
        self.verify(
            "find quiet all check",
            [(3, "Find"), (4, "Quiet"), (4, "All"), (4, "Check")],
        )

    def test_038_find_09(self):
        self.verify(
            "find all quiet check",
            [(3, "Find"), (4, "All"), (4, "Quiet"), (4, "Check")],
        )

    def test_038_find_10(self):
        self.verify("find all 1 check", [], returncode=1)

    def test_038_find_11(self):
        self.verify("find 1 all check", [], returncode=1)

    def test_038_find_12(self):
        self.verify(
            "find quiet 2 4 check",
            [
                (3, "Find"),
                (4, "Quiet"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "Check"),
            ],
        )

    def test_038_find_13(self):
        self.verify(
            "find 2 4 quiet check",
            [
                (3, "Find"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "Quiet"),
                (4, "Check"),
            ],
        )

    def test_038_find_14(self):
        self.verify(
            "find <-- all check",
            [(3, "Find"), (4, "FindBackward"), (4, "All"), (4, "Check")],
        )

    def test_038_find_15(self):
        self.verify(
            "find all <-- check",
            [(3, "Find"), (4, "All"), (4, "FindBackward"), (4, "Check")],
        )

    def test_038_find_16(self):
        self.verify(
            "find <-- 4 check",
            [
                (3, "Find"),
                (4, "FindBackward"),
                (4, "RangeInteger"),
                (4, "Check"),
            ],
        )

    def test_038_find_17(self):
        self.verify(
            "find 4 <-- check",
            [
                (3, "Find"),
                (4, "RangeInteger"),
                (4, "FindBackward"),
                (4, "Check"),
            ],
        )

    def test_038_find_18(self):
        self.verify(
            "find <-- quiet check",
            [
                (3, "Find"),
                (4, "FindBackward"),
                (4, "Quiet"),
                (4, "Check"),
            ],
        )

    def test_038_find_19(self):
        self.verify(
            "find quiet <-- check",
            [
                (3, "Find"),
                (4, "Quiet"),
                (4, "FindBackward"),
                (4, "Check"),
            ],
        )

    def test_038_find_20(self):
        self.verify("v=2 find all v check", [], returncode=1)

    def test_038_find_21(self):
        self.verify("v=2 find v all check", [], returncode=1)

    def test_038_find_22(self):
        self.verify(
            "v=2 find quiet v <-- check",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Find"),
                (4, "Quiet"),
                (4, "RangeVariable"),
                (4, "FindBackward"),
                (4, "Check"),
            ],
        )

    def test_038_find_23(self):
        self.verify(
            "v=2 find quiet <-- v check",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Find"),
                (4, "Quiet"),
                (4, "FindBackward"),
                (4, "RangeVariable"),
                (4, "Check"),
            ],
        )

    def test_038_find_24(self):
        self.verify(
            "v=2 find v <-- quiet check",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Find"),
                (4, "RangeVariable"),
                (4, "FindBackward"),
                (4, "Quiet"),
                (4, "Check"),
            ],
        )

    def test_038_find_25(self):
        self.verify(
            "v=2 find v 5 <-- quiet check",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Find"),
                (4, "RangeVariable"),
                (4, "RangeInteger"),
                (4, "FindBackward"),
                (4, "Quiet"),
                (4, "Check"),
            ],
        )

    def test_038_find_26(self):
        self.verify(
            "v=2 find 1 v <-- quiet check",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Find"),
                (4, "RangeInteger"),
                (4, "RangeVariable"),
                (4, "FindBackward"),
                (4, "Quiet"),
                (4, "Check"),
            ],
        )

    def test_039_flip_01_ascii(self):
        self.verify("flip", [], returncode=1)

    def test_039_flip_01_utf8(self):
        self.verify("✵", [], returncode=1)

    def test_039_flip_02_ascii(self):
        self.verify("flip btm", [(3, "Flip"), (4, "BTM")])

    def test_039_flip_02_utf8(self):
        self.verify("✵ btm", [(3, "Flip"), (4, "BTM")])

    def test_039_flip_03_ascii(self):
        self.verify("flip count btm", [(3, "Flip"), (4, "Count"), (4, "BTM")])

    def test_039_flip_03_utf8(self):
        self.verify("✵ count btm", [(3, "Flip"), (4, "Count"), (4, "BTM")])

    def test_040_flipcolor_01_ascii(self):
        self.verify("flipcolor", [], returncode=1)

    def test_040_flipcolor_01_utf8(self):
        self.verify("⬓", [], returncode=1)

    def test_040_flipcolor_02_ascii(self):
        self.verify("flipcolor btm", [(3, "FlipColor"), (4, "BTM")])

    def test_040_flipcolor_02_utf8(self):
        self.verify("⬓ btm", [(3, "FlipColor"), (4, "BTM")])

    def test_040_flipcolor_03_ascii(self):
        self.verify(
            "flipcolor count btm",
            [(3, "FlipColor"), (4, "Count"), (4, "BTM")],
        )

    def test_040_flipcolor_03_utf8(self):
        self.verify(
            "⬓ count btm",
            [(3, "FlipColor"), (4, "Count"), (4, "BTM")],
        )

    def test_041_fliphorizontal_01(self):
        self.verify("fliphorizontal", [], returncode=1)

    def test_041_fliphorizontal_02(self):
        self.verify("fliphorizontal btm", [(3, "FlipHorizontal"), (4, "BTM")])

    def test_041_fliphorizontal_03(self):
        self.verify(
            "fliphorizontal count btm",
            [(3, "FlipHorizontal"), (4, "Count"), (4, "BTM")],
        )

    def test_042_flipvertical_01(self):
        self.verify("flipvertical", [], returncode=1)

    def test_042_flipvertical_02(self):
        self.verify("flipvertical btm", [(3, "FlipVertical"), (4, "BTM")])

    def test_042_flipvertical_03(self):
        self.verify(
            "flipvertical count btm",
            [(3, "FlipVertical"), (4, "Count"), (4, "BTM")],
        )

    def test_043_from(self):
        self.verify("from", [(3, "From")])

    def test_044_function_01_bare(self):
        self.verify("function", [], returncode=1)

    def test_044_function_02_name_bare(self):
        self.verify("function fn", [], returncode=1)

    def test_044_function_03_no_body(self):
        self.verify("function fn()", [], returncode=1)

    def test_044_function_04_body_named_filter(self):
        self.verify("function fn(){wtm}", [(3, "Function")])

    def test_044_function_05_body_named_filter_call(self):
        self.verify(
            "function fn(){wtm} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "WTM"),
            ],
        )

    def test_044_function_06_argument_body_named_filter_call(self):
        self.verify(
            "function fn(y){y==1} x=1 fn(x)",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Eq"),
                (7, "Variable"),
                (7, "Integer"),
            ],
        )

    def test_044_function_07_body_set_call(self):
        self.verify(
            "function fn(){k} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "PieceDesignator"),
            ],
        )

    def test_044_function_08_body_integer_call_01_bare(self):
        # Choose to allow this use of '{<digits>}' unlike CQL which
        # declares the construct invalid despite the CQL parser passing
        # the construct (actually the explicit statement of legality is
        # for 'fn(){2+3}' or any arithemic operation).
        self.verify_declare_fail(
            "function fn(){1} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Integer"),
            ],
        )

    def test_044_function_08_body_integer_call_02_parentheses(self):
        # If something like 'fn(){1}' really must be said to CQL it is done
        # by saying 'fn(){(1)}'.
        self.verify(
            "function fn(){(1)} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "ParenthesisLeft"),
                (7, "Integer"),
            ],
        )

    def test_044_function_08_body_integer_call_03_variable(self):
        self.verify(
            "v=1 function fn(){v} fn()",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Variable"),
            ],
        )

    def test_044_function_09_body_string_call(self):
        self.verify(
            'function fn(){"a"} fn()',
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "String"),
            ],
        )

    def test_044_function_10_body_logical_call(self):
        self.verify(
            "function fn(){true} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "True_"),
            ],
        )

    def test_044_function_11_body_position_call(self):
        self.verify(
            "function fn(){initialposition} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "InitialPosition"),
            ],
        )

    def test_044_function_12_body_integer_01_bare(self):
        self.verify_declare_fail("function fn(){1}", [(3, "Function")])

    def test_044_function_12_body_integer_02_parentheses(self):
        self.verify("function fn(){(1)}", [(3, "Function")])

    def test_044_function_12_body_integer_03_variable(self):
        self.verify(
            "v=1 function fn(){v}",
            [(3, "Assign"), (4, "Variable"), (4, "Integer"), (3, "Function")],
        )

    def test_044_function_13_body_string(self):
        self.verify('function fn(){"a"}', [(3, "Function")])

    def test_044_function_14_body_logical(self):
        self.verify("function fn(){true}", [(3, "Function")])

    def test_044_function_15_body_position(self):
        self.verify("function fn(){initialposition}", [(3, "Function")])

    # Tests for multiply like plus below are at 'test_190_star_12_function_*'.

    def test_044_function_16_plus_integer_01_base(self):
        self.verify(
            "I=3 I+I",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Plus"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_044_function_16_plus_integer_02_braced_base(self):
        self.verify(
            "{I=3 I+I}",
            [
                (3, "BraceLeft"),
                (4, "Assign"),
                (5, "Variable"),
                (5, "Integer"),
                (4, "Plus"),
                (5, "Variable"),
                (5, "Variable"),
            ],
        )

    def test_044_function_16_plus_integer_03_body_base(self):
        self.verify("function F(){I=3 I+I}", [(3, "Function")])

    def test_044_function_16_plus_integer_04_call_base(self):
        self.verify(
            "function F(){I=3 I+I}F()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Assign"),
                (7, "Variable"),
                (7, "Integer"),
                (6, "Plus"),
                (7, "Variable"),
                (7, "Variable"),
            ],
        )

    def test_044_function_16_plus_integer_05_body_base_invalid(self):
        self.verify("function F(){I=q I+I}", [(3, "Function")])

    def test_044_function_16_plus_06_integer_call_base_invalid(self):
        self.verify("function F(){I=q I+I}F()", [], returncode=1)

    def test_044_function_17_plus_string_01_base(self):
        self.verify(
            'I="v" I+I',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Plus"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_044_function_17_plus_string_02_braced_base(self):
        self.verify(
            '{I="v" I+I}',
            [
                (3, "BraceLeft"),
                (4, "Assign"),
                (5, "Variable"),
                (5, "String"),
                (4, "Plus"),
                (5, "Variable"),
                (5, "Variable"),
            ],
        )

    def test_044_function_17_plus_string_03_body_base(self):
        self.verify('function F(){I="v" I+I}', [(3, "Function")])

    def test_044_function_17_plus_string_04_call_base(self):
        self.verify(
            'function F(){I="v" I+I}F()',
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Assign"),
                (7, "Variable"),
                (7, "String"),
                (6, "Plus"),
                (7, "Variable"),
                (7, "Variable"),
            ],
        )

    def test_044_function_17_plus_string_05_body_base_invalid(self):
        self.verify("function F(){I=q I+I}", [(3, "Function")])

    def test_044_function_17_plus_string_06_call_base_invalid(self):
        self.verify("function F(){I=q I+I}F()", [], returncode=1)

    def test_044_function_18_minus_01_base(self):
        self.verify(
            "I=3 I-I",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Minus"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_044_function_18_minus_02_braced_base(self):
        self.verify(
            "{I=3 I-I}",
            [
                (3, "BraceLeft"),
                (4, "Assign"),
                (5, "Variable"),
                (5, "Integer"),
                (4, "Minus"),
                (5, "Variable"),
                (5, "Variable"),
            ],
        )

    def test_044_function_18_minus_03_body_base(self):
        self.verify("function F(){I=3 I-I}", [(3, "Function")])

    def test_044_function_18_minus_04_call_base(self):
        self.verify(
            "function F(){I=3 I-I}F()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Assign"),
                (7, "Variable"),
                (7, "Integer"),
                (6, "Minus"),
                (7, "Variable"),
                (7, "Variable"),
            ],
        )

    def test_044_function_18_minus_05_body_base_invalid(self):
        self.verify("function F(){I=q I-I}", [(3, "Function")])

    def test_044_function_18_minus_06_call_base_invalid(self):
        self.verify("function F(){I=q I-I}F()", [], returncode=1)

    def test_044_function_19_xray_01_body_base_no_variable(self):
        self.verify("function F(){xray(x k)}", [(3, "Function")])

    def test_044_function_19_xray_02_call_base_no_variable(self):
        self.verify("function F(){xray(x k)}F()", [], returncode=1)

    def test_044_function_19_xray_03_body_base_unassigned_parameter(self):
        self.verify("function F(x){xray(x k)}", [(3, "Function")])

    def test_044_function_19_xray_04_call_base_unassigned_parameter(self):
        self.verify("function F(x){xray(x k)}F(y)", [], returncode=1)

    def test_044_function_19_xray_05_call_base_set_variable(self):
        self.verify(
            "function F(x){xray(x k)}y=r F(y)",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "PieceDesignator"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "XRay"),
                (7, "Variable"),
                (7, "PieceDesignator"),
            ],
        )

    def test_044_function_19_xray_06_call_base_integer_variable(self):
        self.verify("function F(x){xray(x k)}y=3 F(y)", [], returncode=1)

    def test_044_function_19_xray_07_call_base_sring_variable(self):
        self.verify('function F(x){xray(x k)}y="w" F(y)', [], returncode=1)

    def test_044_function_19_xray_08_call_base_position_variable(self):
        self.verify(
            "function F(x){xray(x k)}y=currentposition F(y)", [], returncode=1
        )

    def test_045_gamenumber(self):
        self.verify("gamenumber", [(3, "GameNumber")])

    def test_046_hascomment_01(self):
        self.verify("hascomment", [(3, "OriginalComment")])

    def test_046_hascomment_02(self):
        self.verify(
            'hascomment "text"',
            [(3, "OriginalComment"), (4, "ImplicitSearchParameter")],
        )

    def test_047_idealmate(self):
        self.verify("idealmate", [(3, "IdealMate")])

    def test_048_idealstalemate(self):
        self.verify("idealstalemate", [(3, "IdealStaleMate")])

    def test_049_if_01(self):
        self.verify("if", [], returncode=1)

    def test_049_if_02(self):
        self.verify("if check", [], returncode=1)

    def test_049_if_03(self):
        self.verify(
            'if check "In check"', [(3, "If"), (4, "Check"), (4, "String")]
        )

    def test_049_if_04(self):
        self.verify(
            'if check "In check" else "Safe"',
            [
                (3, "If"),
                (4, "Check"),
                (4, "String"),
                (4, "Else"),
                (5, "String"),
            ],
        )

    def test_049_if_05(self):
        self.verify(
            'if check "In check" "Safe"',
            [
                (3, "If"),
                (4, "Check"),
                (4, "String"),
                (3, "String"),
            ],
        )

    def test_049_if_06(self):
        self.verify(
            'if check "In check" else "Safe" "Next"',
            [
                (3, "If"),
                (4, "Check"),
                (4, "String"),
                (4, "Else"),
                (5, "String"),
                (3, "String"),
            ],
        )

    def test_050_in_01(self):
        self.verify("in", [], returncode=1)

    def test_050_in_02(self):
        self.verify("R in", [], returncode=1)

    def test_050_in_03(self):
        self.verify('"Q" in', [], returncode=1)

    def test_050_in_04(self):  # chessql gets this wrong.
        self.verify('R in "Q"', [], returncode=1)

    def test_050_in_05(self):  # chessql gets this wrong.
        self.verify('"Q" in R', [], returncode=1)

    def test_050_in_06(self):
        self.verify(
            "R in A",
            [(3, "In"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_050_in_07(self):
        self.verify('"Q" in "s"', [(3, "In"), (4, "String"), (4, "String")])

    def test_051_indexof(self):
        self.verify(
            'indexof("sub" "some substring")',
            [
                (3, "IndexOf"),
                (4, "String"),
                (4, "String"),
            ],
        )

    def test_052_initial(self):
        self.verify("initial", [(3, "Initial")])

    def test_053_initialposition(self):
        self.verify("initialposition", [(3, "InitialPosition")])

    def test_054_int_01(self):
        self.verify("int", [], returncode=1)

    def test_054_int_02(self):
        self.verify('int "64"', [(3, "Int"), (4, "String")])

    def test_055_isbound_01(self):
        self.verify("isbound", [], returncode=1)

    def test_055_isbound_02(self):
        con = self.verify("isbound x", [(3, "IsBound"), (4, "BindName")])
        self.assertEqual("x" in con.definitions, False)

    def test_055_isbound_03(self):
        con = self.verify(
            "x=0 isbound x",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "IsBound"),
                (4, "Variable"),
            ],
        )
        self.assertEqual("x" in con.definitions, True)

    def test_055_isbound_04_key_no_dictionary(self):
        self.verify('isbound v["key"]', [], returncode=1)

    def test_055_isbound_05_dictionary(self):
        con = self.verify(
            "dictionary v isbound v",
            [
                (3, "Dictionary"),
                (3, "IsBound"),
                (4, "Dictionary"),
            ],
        )
        self.assertEqual("v" in con.definitions, True)

    def test_055_isbound_06_dictionary_key_absent(self):
        self.verify('dictionary v isbound v["key"]', [], returncode=1)

    def test_055_isbound_07_dictionary_key(self):
        self.verify(
            'dictionary v["key"]="value" isbound v["key"]', [], returncode=1
        )

    def test_055_isbound_08_dictionary_key_present(self):
        con = self.verify(
            'dictionary v["key"]="value" isbound v',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
                (3, "IsBound"),
                (4, "Dictionary"),
            ],
        )
        self.assertEqual("v" in con.definitions, True)

    def test_056_isolatedpwans(self):
        self.verify("isolatedpawns", [(3, "IsolatedPawns")])

    def test_057_isunbound_01(self):
        self.verify("isunbound", [], returncode=1)

    def test_057_isunbound_02(self):
        con = self.verify("isunbound x", [(3, "IsUnbound"), (4, "BindName")])
        self.assertEqual("x" in con.definitions, False)

    def test_057_isunbound_03(self):
        con = self.verify(
            "x=0 isunbound x",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "IsUnbound"),
                (4, "Variable"),
            ],
        )
        self.assertEqual("x" in con.definitions, True)

    def test_057_isunbound_04_key_no_dictionary(self):
        self.verify('isunbound v["key"]', [], returncode=1)

    def test_057_isunbound_05_dictionary(self):
        con = self.verify(
            "dictionary v isunbound v",
            [
                (3, "Dictionary"),
                (3, "IsUnbound"),
                (4, "Dictionary"),
            ],
        )
        self.assertEqual("v" in con.definitions, True)

    def test_057_isunbound_06_dictionary_key_absent(self):
        self.verify('dictionary v isunbound v["key"]', [], returncode=1)

    def test_057_isunbound_07_dictionary_key(self):
        self.verify(
            'dictionary v["key"]="value" isunbound v["key"]', [], returncode=1
        )

    def test_057_isunbound_08_dictionary_key_present(self):
        con = self.verify(
            'dictionary v["key"]="value" isunbound v',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
                (3, "IsUnbound"),
                (4, "Dictionary"),
            ],
        )
        self.assertEqual("v" in con.definitions, True)

    def test_058_lastgamenumber_01_bare(self):
        self.verify_run(
            "lastgamenumber", [(3, "LastGameNumber")], returncode=1
        )

    def test_058_lastgamenumber_02_used(self):
        self.verify_run(
            "lastgamenumber==2",
            [(3, "Eq"), (4, "LastGameNumber"), (4, "Integer")],
        )

    def test_059_lca_01(self):
        self.verify(
            "lca(position 1 position 2)",
            [
                (3, "LCA"),
                (4, "Position"),
                (5, "Integer"),
                (4, "Position"),
                (5, "Integer"),
            ],
        )

    def test_059_lca_02(self):
        self.verify(
            "p1=position 1 p2=position 2 lca(p1 p2)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Position"),
                (5, "Integer"),
                (3, "LCA"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_060_legal_01(self):
        self.verify("legal", [], returncode=1)

    def test_060_legal_02(self):
        self.verify("legal k", [], returncode=1)

    def test_060_legal_03(self):
        self.verify(
            "legal --",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_060_legal_04_capture(self):
        self.verify("legal [x]", [], returncode=1)

    def test_061_left_01(self):
        self.verify("left", [], returncode=1)

    def test_061_left_02(self):
        self.verify(
            "left P",
            [
                (3, "Left"),
                (4, "PieceDesignator"),
            ],
        )

    def test_061_left_03(self):
        self.verify(
            "left 1 4 P",
            [
                (3, "Left"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "PieceDesignator"),
            ],
        )

    def test_062_line_01(self):
        self.verify("line", [], returncode=1)

    def test_062_line_02(self):
        self.verify("line -->", [], returncode=1)

    def test_062_line_03(self):
        self.verify(
            "line --> check",
            [(3, "Line"), (4, "ArrowForward"), (5, "Check")],
        )

    def test_062_line_04(self):
        self.verify("line --> check -->", [], returncode=1)

    def test_062_line_05(self):
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

    def test_062_line_06(self):
        self.verify("line --> check <--", [], returncode=1)

    def test_062_line_07(self):
        self.verify("line --> check <-- check", [], returncode=1)

    def test_062_line_08(self):
        self.verify("line <--", [], returncode=1)

    def test_062_line_09(self):
        self.verify(
            "line <-- check",
            [(3, "Line"), (4, "ArrowBackward"), (5, "Check")],
        )

    def test_062_line_10(self):
        self.verify("line <-- check <--", [], returncode=1)

    def test_062_line_11(self):
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

    def test_062_line_12(self):
        self.verify("line <-- check -->", [], returncode=1)

    def test_062_line_13(self):
        self.verify("line <-- check --> check", [], returncode=1)

    def test_062_line_14(self):
        self.verify(
            "line --> .",
            [(3, "Line"), (4, "ArrowForward"), (5, "AnySquare")],
        )

    def test_062_line_15(self):
        self.verify(
            "line --> .*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "AnySquare"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_16(self):
        self.verify(
            "line --> check+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_17(self):
        self.verify(
            "line --> check?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_18_force_repeat_01_zero_or_more(self):
        self.verify(
            "line --> check{*}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "WildcardStar"),
            ],
        )

    def test_062_line_18_force_repeat_02_one_or_more(self):
        self.verify(
            "line --> check{+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "WildcardPlus"),
            ],
        )

    def test_062_line_19(self):
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

    def test_062_line_20(self):
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

    def test_062_line_21(self):
        self.verify(
            "line <-- .",
            [(3, "Line"), (4, "ArrowBackward"), (5, "AnySquare")],
        )

    def test_062_line_22(self):
        self.verify(
            "line <-- .*",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "AnySquare"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_23(self):
        self.verify(
            "line <-- check+",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_24(self):
        self.verify(
            "line <-- check?",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_25_repeat_01_closed_range(self):
        self.verify(
            "line <-- check{2,4}",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RegexRepeat"),
            ],
        )

    def test_062_line_25_repeat_02_closed_range_upper(self):
        self.verify(
            "line <-- check{,4}",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RegexRepeat"),
            ],
        )

    def test_062_line_25_repeat_03_closed_range_lower(self):
        self.verify(
            "line <-- check{2,}",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RegexRepeat"),
            ],
        )

    def test_062_line_26(self):
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

    def test_062_line_27(self):
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

    def test_062_line_28(self):
        self.verify("line --> (check <-- r)+", [], returncode=1)

    def test_062_line_29(self):
        self.verify("line <-- (check --> r)+", [], returncode=1)

    def test_062_line_30(self):
        self.verify("line primary secondary --> check", [], returncode=1)

    def test_062_line_31(self):
        self.verify(
            "line primary --> check",
            [
                (3, "Line"),
                (4, "PrimaryParameter"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_32(self):
        self.verify(
            "line secondary --> check",
            [
                (3, "Line"),
                (4, "SecondaryParameter"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_33(self):
        self.verify(
            "line firstmatch --> check",
            [
                (3, "Line"),
                (4, "FirstMatch"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_34(self):
        self.verify(
            "line lastposition --> check",
            [
                (3, "Line"),
                (4, "LastPosition"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_35(self):
        self.verify(
            "line singlecolor --> check",
            [
                (3, "Line"),
                (4, "SingleColor"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_36(self):
        self.verify(
            "line quiet --> check",
            [(3, "Line"), (4, "Quiet"), (4, "ArrowForward"), (5, "Check")],
        )

    def test_062_line_37(self):
        self.verify(
            "line nestban --> check",
            [(3, "Line"), (4, "NestBan"), (4, "ArrowForward"), (5, "Check")],
        )

    def test_062_line_38(self):
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

    def test_062_line_39(self):
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

    def test_062_line_40(self):
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

    def test_062_line_42(self):
        self.verify("line secondary primary --> check", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_01_zero_or_more(self):
        self.verify("check*", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_02_one_or_more(self):
        self.verify("check+", [], returncode=1)

    def test_062__line_43_regex_no_line_arrow_03_zero_or_one(self):
        self.verify("check?", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_04_zero_or_more(self):
        self.verify("check{*}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_05_one_or_more(self):
        self.verify("check{+}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_06_closed_range(self):
        self.verify("check{2,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_07_closed_range_high(self):
        self.verify("check{,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_08_closed_range_low(self):
        self.verify("check{2,}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_09_group_zero_or_more(self):
        self.verify("(check)*", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_10_group_one_or_more(self):
        self.verify("(check)+", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_11_group_zero_or_one(self):
        self.verify("(check)?", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_12_group_zero_or_more(self):
        self.verify("(check){*}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_13_group_one_or_more(self):
        self.verify("(check){+}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_14_group_closed_range(self):
        self.verify("(check){2,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_15_group_closed_range_high(self):
        self.verify("(check){,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_16_group_closed_range_low(self):
        self.verify("(check){2,}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_17_arrow_zero_or_more(self):
        self.verify("(check --> mate)*", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_18_arrow_one_or_more(self):
        self.verify("(check --> mate)+", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_19_arrow_zero_or_one(self):
        self.verify("(check --> mate)?", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_20_arrow_zero_or_more(self):
        self.verify("(check --> mate){*}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_21_arrow_one_or_more(self):
        self.verify("(check --> mate){+}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_22_arrow_closed_range(self):
        self.verify("(check --> mate){2,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_23_arrow_closed_range_high(self):
        self.verify("(check --> mate){,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_24_arrow_closed_range_low(self):
        self.verify("(check --> mate){2,}", [], returncode=1)

    def test_062_line_44_regex_line_arrow_01_arrow_zero_or_more(self):
        self.verify(
            "line --> (check --> mate)*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_44_regex_line_arrow_02_arrow_one_or_more(self):
        self.verify(
            "line --> (check --> mate)+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_44_regex_line_arrow_03_arrow_zero_or_one(self):
        self.verify(
            "line --> (check --> mate)?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_44_regex_line_arrow_04_arrow_zero_or_more(self):
        self.verify(
            "line --> (check --> mate){*}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "WildcardStar"),
            ],
        )

    def test_062_line_44_regex_line_arrow_05_arrow_one_or_more(self):
        self.verify(
            "line --> (check --> mate){+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "WildcardPlus"),
            ],
        )

    def test_062_line_44_regex_line_arrow_06_arrow_closed_range(self):
        self.verify_capture_cql_output(
            "line --> (check --> mate){2,4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "RegexRepeat"),
            ],
            "<RepeatConstituent \n    <VectorConstituent ",
        )

    def test_062_line_44_regex_line_arrow_07_arrow_closed_range_high(self):
        self.verify_capture_cql_output(
            "line --> (check --> mate){,4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "RegexRepeat"),
            ],
            "<RepeatConstituent \n    <VectorConstituent ",
        )

    def test_062_line_44_regex_line_arrow_08_arrow_closed_range_low(self):
        self.verify_capture_cql_output(
            "line --> (check --> mate){2,}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "RegexRepeat"),
            ],
            "<RepeatConstituent \n    <VectorConstituent ",
        )

    def test_062_line_45_regex_line_arrow_08_space_start_repeat_number(self):
        self.verify_capture_cql_output(
            "line --> check{ 2}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
            "<NumberNode:",
        )

    def test_062_line_45_regex_line_arrow_09_space_end_repeat_number(self):
        self.verify_capture_cql_output(
            "line --> check{2 }",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
            "<NumberNode:",
        )

    def test_062_line_45_regex_line_arrow_10_space_around_repeat_number(self):
        self.verify_capture_cql_output(
            "line --> check{ 2 }",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
            "<NumberNode:",
        )

    def test_062_line_45_regex_line_arrow_11_space_start_repeat_range(self):
        self.verify("line --> check{ 2,}", [], returncode=1)

    def test_062_line_45_regex_line_arrow_12_space_end_repeat_range(self):
        self.verify("line --> check{2, }", [], returncode=1)

    def test_062_line_45_regex_line_arrow_13_space_around_repeat_range(self):
        self.verify("line --> check{ 2, }", [], returncode=1)

    def test_062_line_45_regex_line_arrow_14_space_within_range_01(self):
        self.verify("line --> check{2 ,}", [], returncode=1)

    def test_062_line_45_regex_line_arrow_14_space_within_range_02(self):
        self.verify("line --> check{, 4}", [], returncode=1)

    def test_062_line_45_regex_line_arrow_14_space_within_range_03(self):
        self.verify("line --> check{2 , 4}", [], returncode=1)

    def test_062_line_46_integer_01_bare(self):
        self.verify_declare_fail(
            "line --> 3", [(3, "Line"), (4, "ArrowForward"), (5, "Integer")]
        )

    def test_062_line_46_integer_02_hide_in_parentheses(self):
        self.verify_declare_fail(
            "line --> (3)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
            ],
        )

    def test_062_line_46_integer_03_hide_in_braces(self):
        self.verify_declare_fail(
            "line --> {3}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Integer"),
            ],
        )

    def test_062_line_46_integer_04_bare_plus(self):  # '+' is add.
        self.verify_declare_fail(
            "line --> 3+4",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Plus"),
                (6, "Integer"),
                (6, "Integer"),
            ],
        )

    # '(3)+' is constituent of 'line'. '(4)' is new filter after 'line'.
    def xtest_062_line_46_integer_05_hide_in_parentheses_plus_01(self):
        self.verify_declare_fail(
            "line --> (3)+(4)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "PlusRepeat"),
                (3, "ParenthesisLeft"),
                (4, "Integer"),
            ],
        )

    def test_062_line_46_integer_05_hide_in_parentheses_plus_02(self):
        self.verify_declare_fail(
            "line --> (3+4)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Plus"),
                (7, "Integer"),
                (7, "Integer"),
            ],
        )

    # The constituent of '-->' is the '+' filter adding two compound filters.
    def test_062_line_46_integer_06_hide_in_braces_plus_01(self):
        self.verify_declare_fail(
            "line --> {3}+{4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Plus"),
                (6, "BraceLeft"),
                (7, "Integer"),
                (6, "BraceLeft"),
                (7, "Integer"),
            ],
        )

    def test_062_line_46_integer_06_hide_in_braces_plus_02(self):
        self.verify_declare_fail(
            "line --> {3+4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Plus"),
                (7, "Integer"),
                (7, "Integer"),
            ],
        )

    def test_062_line_46_integer_07_bare_star(self):  # '*' is multiply.
        self.verify_declare_fail(
            "line --> 3*4",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Star"),
                (6, "Integer"),
                (6, "Integer"),
            ],
        )

    # '(3)*' is constituent of 'line'. '(4)' is new filter after 'line'.
    def test_062_line_46_integer_08_hide_in_parentheses_star_01(self):
        self.verify_declare_fail(
            "line --> (3)*(4)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "StarRepeat"),
                (3, "ParenthesisLeft"),
                (4, "Integer"),
            ],
        )

    def test_062_line_46_integer_08_hide_in_parentheses_star_02(self):
        self.verify_declare_fail(
            "line --> (3*4)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Star"),
                (7, "Integer"),
                (7, "Integer"),
            ],
        )

    # The constituent of '-->' is the '*' filter multiplying two compound
    # filters.
    def test_062_line_46_integer_09_hide_in_braces_star_01(self):
        self.verify_declare_fail(
            "line --> {3}*{4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Star"),
                (6, "BraceLeft"),
                (7, "Integer"),
                (6, "BraceLeft"),
                (7, "Integer"),
            ],
        )

    def test_062_line_46_integer_09_hide_in_braces_star_02(self):
        self.verify_declare_fail(
            "line --> {3*4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Star"),
                (7, "Integer"),
                (7, "Integer"),
            ],
        )

    def test_062_line_46_integer_10_bare_plus_repeat(self):
        self.verify_declare_fail(
            "line --> 3+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Integer"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_46_integer_11_hide_in_parentheses_plus_repeat(self):
        self.verify_declare_fail(
            "line --> (3)+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_46_integer_12_hide_in_braces_plus_repeat(self):
        self.verify_declare_fail(
            "line --> {3}+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Integer"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_46_integer_13_bare_star_repeat(self):
        self.verify_declare_fail(
            "line --> 3*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Integer"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_46_integer_14_hide_in_parentheses_star_repeat(self):
        self.verify_declare_fail(
            "line --> (3)*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_46_integer_15_hide_in_braces_star_repeat(self):
        self.verify_declare_fail(
            "line --> {3}*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Integer"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_46_integer_16_bare_optional(self):
        self.verify_declare_fail(
            "line --> 3?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Integer"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_46_integer_17_hide_in_parentheses_optional(self):
        self.verify_declare_fail(
            "line --> (3)?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_46_integer_18_hide_in_braces_optional(self):
        self.verify_declare_fail(
            "line --> {3}?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Integer"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_46_string_01_bare(self):
        self.verify(
            'line --> "a"', [(3, "Line"), (4, "ArrowForward"), (5, "String")]
        )

    def test_062_line_46_string_02_hide_in_parentheses(self):
        self.verify(
            'line --> ("a")',
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "String"),
            ],
        )

    def test_062_line_47_string_03_hide_in_braces(self):
        self.verify(
            'line --> {"a"}',
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "String"),
            ],
        )

    def test_062_line_48_integer_variable_01_bare(self):
        self.verify_declare_fail(
            "v=3 line --> v",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Variable"),
            ],
        )

    def test_062_line_48_integer_variable_02_hide_in_parentheses(self):
        self.verify_declare_fail(
            "v=3 line --> (v)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Variable"),
            ],
        )

    def test_062_line_48_integer_variable_03_hide_in_braces(self):
        self.verify(
            "v=3 line --> {v}",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Variable"),
            ],
        )

    def test_062_line_49_string_variable_01_bare(self):
        self.verify(
            'v="a" line --> v',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Variable"),
            ],
        )

    def test_062_line_49_string_variable_02_hide_in_parentheses(self):
        self.verify(
            'v="a" line --> (v)',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Variable"),
            ],
        )

    def test_062_line_49_string_variable_03_hide_in_braces(self):
        self.verify(
            'v="a" line --> {v}',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Variable"),
            ],
        )

    def test_062_line_50_cql_6_1_examples_long_sacrifice_plus_01(self):
        self.verify(
            "{line-->7>=9+}",
            [
                (3, "BraceLeft"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "PlusRepeat"),
            ],
        )

    def test_062_line_50_cql_6_1_examples_long_sacrifice_plus_02(self):
        self.verify(
            "(line-->7>=9+)",
            [
                (3, "ParenthesisLeft"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "PlusRepeat"),
            ],
        )

    def test_062_line_50_cql_6_1_examples_long_sacrifice_plus_03(self):
        # The 'wildcard plus' test at *_062_*_50_*_04 is fine.
        self.verify_declare_fail(
            'v="s"v[line-->7>=9+]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "BracketLeft"),
                (4, "Variable"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "PlusRepeat"),
            ],
        )

    def test_062_line_50_cql_6_1_examples_long_sacrifice_plus_04(self):
        self.verify(
            'v="s"v[line-->7>=9{+}]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "BracketLeft"),
                (4, "Variable"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "WildcardPlus"),
            ],
        )

    def test_062_line_51_cql_6_1_examples_long_sacrifice_plus_01_star(self):
        self.verify(
            "{line-->7>=9*}",
            [
                (3, "BraceLeft"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "StarRepeat"),
            ],
        )

    def test_062_line_51_cql_6_1_examples_long_sacrifice_plus_02_star(self):
        self.verify(
            "(line-->7>=9*)",
            [
                (3, "ParenthesisLeft"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "StarRepeat"),
            ],
        )

    def test_062_line_51_cql_6_1_examples_long_sacrifice_plus_03_star(self):
        # The 'wildcard star' test at *_062_*_51_*_04_star is fine.
        self.verify_declare_fail(
            'v="s"v[line-->7>=9*]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "BracketLeft"),
                (4, "Variable"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "StarRepeat"),
            ],
        )

    def test_062_line_51_cql_6_1_examples_long_sacrifice_plus_04_star(self):
        self.verify(
            'v="s"v[line-->7>=9{*}]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "BracketLeft"),
                (4, "Variable"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "WildcardStar"),
            ],
        )

    def test_062_line_52_cql_6_1_examples_turton_01(self):
        self.verify(
            "line -->  move from k *",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (6, "FromParameter"),
                (7, "PieceDesignator"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_52_cql_6_1_examples_turton_02(self):
        self.verify(
            "line -->  move from k {*}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (6, "FromParameter"),
                (7, "PieceDesignator"),
                (5, "WildcardStar"),
            ],
        )

    def test_062_line_52_cql_6_1_examples_turton_03(self):
        self.verify(
            "line -->  move *",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_52_cql_6_1_examples_turton_04(self):
        self.verify(
            "line -->  move {*}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (5, "WildcardStar"),
            ],
        )

    def test_062_line_53_cql_6_1_examples_turton_01_plus(self):
        self.verify(
            "line -->  move from k +",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (6, "FromParameter"),
                (7, "PieceDesignator"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_53_cql_6_1_examples_turton_02_plus(self):
        self.verify(
            "line -->  move from k {+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (6, "FromParameter"),
                (7, "PieceDesignator"),
                (5, "WildcardPlus"),
            ],
        )

    def test_062_line_53_cql_6_1_examples_turton_03_plus(self):
        self.verify(
            "line -->  move +",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_53_cql_6_1_examples_turton_04_plus(self):
        self.verify(
            "line -->  move {+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (5, "WildcardPlus"),
            ],
        )

    def test_062_line_54_cql_6_1_examples_parallelpaths_simple(self):
        # Further simplification usually causes query to pass parsing
        # before fix applied.
        self.verify(
            "line-->x=?move to .-->y=?move to ~x from k-->z=?move to .",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "AssignIf"),
                (6, "Variable"),
                (6, "Move"),
                (7, "ToParameter"),
                (8, "AnySquare"),
                (4, "ArrowForward"),
                (5, "AssignIf"),
                (6, "Variable"),
                (6, "Move"),
                (7, "ToParameter"),
                (8, "Complement"),
                (9, "Variable"),
                (7, "FromParameter"),
                (8, "PieceDesignator"),
                (4, "ArrowForward"),
                (5, "AssignIf"),
                (6, "Variable"),
                (6, "Move"),
                (7, "ToParameter"),
                (8, "AnySquare"),
            ],
        )

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

    def test_064_loop_01(self):
        self.verify("loop", [], returncode=1)

    def test_064_loop_02(self):
        self.verify("loop K", [(3, "Loop"), (4, "PieceDesignator")])

    def test_065_lowercase_01(self):
        self.verify("lowercase", [], returncode=1)

    def test_065_lowercase_02(self):
        self.verify('lowercase "K"', [(3, "LowerCase"), (4, "String")])

    def test_066_mainline(self):
        self.verify("mainline", [(3, "MainLine")])

    def test_067_makesquare_01(self):
        self.verify("makesquare", [], returncode=1)

    def test_067_makesquare_02_argument_01_set(self):
        self.verify("makesquare k", [], returncode=1)

    def test_067_makesquare_02_argument_02_numeric(self):
        self.verify("makesquare 3", [], returncode=1)

    def test_067_makesquare_02_argument_03_logical(self):
        self.verify("makesquare false", [], returncode=1)

    def test_067_makesquare_02_argument_04_position(self):
        self.verify("makesquare currentposition", [], returncode=1)

    def test_067_makesquare_03(self):
        self.verify("makesquare(6)", [], returncode=1)

    def test_067_makesquare_04(self):
        self.verify('makesquare(6 "a")', [], returncode=1)

    def test_067_makesquare_05(self):
        self.verify(
            "makesquare(6 10)",
            [(3, "MakeSquareParentheses"), (4, "Integer"), (4, "Integer")],
        )

    def test_067_makesquare_06(self):
        self.verify(
            "makesquare(5 5)",
            [(3, "MakeSquareParentheses"), (4, "Integer"), (4, "Integer")],
        )

    def test_067_makesquare_07(self):
        self.verify('makesquare ""', [(3, "MakeSquareString"), (4, "String")])

    def test_067_makesquare_08(self):
        self.verify('makesquare "a"', [(3, "MakeSquareString"), (4, "String")])

    def test_067_makesquare_09(self):
        self.verify(
            'makesquare "ab"', [(3, "MakeSquareString"), (4, "String")]
        )

    def test_067_makesquare_10(self):
        self.verify('makesquare "2"', [(3, "MakeSquareString"), (4, "String")])

    def test_067_makesquare_11(self):
        self.verify(
            'makesquare "22"', [(3, "MakeSquareString"), (4, "String")]
        )

    def test_067_makesquare_12(self):
        self.verify(
            'makesquare "any"', [(3, "MakeSquareString"), (4, "String")]
        )

    def test_067_makesquare_13(self):
        self.verify(
            'makesquare "a2"', [(3, "MakeSquareString"), (4, "String")]
        )

    def test_067_makesquare_14(self):
        self.verify('makesquare "a" + 2', [], returncode=1)

    def test_067_makesquare_15(self):
        self.verify("makesquare 3 + 2", [], returncode=1)

    def test_067_makesquare_16(self):
        self.verify(
            'makesquare "a" + "2"',
            [
                (3, "MakeSquareString"),
                (4, "Plus"),
                (5, "String"),
                (5, "String"),
            ],
        )

    def test_068_mate(self):
        self.verify("mate", [(3, "Mate")])

    def test_069_max_01(self):
        self.verify("max", [], returncode=1)

    def test_069_max_02(self):
        self.verify("max()", [], returncode=1)

    def test_069_max_03(self):
        self.verify("max(2)", [], returncode=1)

    def test_069_max_04(self):
        self.verify("max(2 5)", [(3, "Max"), (4, "Integer"), (4, "Integer")])

    def test_069_max_05(self):
        self.verify('max(2 5 "k")', [], returncode=1)

    def test_069_max_06(self):
        self.verify(
            "max(2 5 1)",  # Any number of integers.
            [(3, "Max"), (4, "Integer"), (4, "Integer"), (4, "Integer")],
        )

    def test_069_max_07_compare_01_rhs(self):
        self.verify(
            "2==max(2 5)",
            [
                (3, "Eq"),
                (4, "Integer"),
                (4, "Max"),
                (5, "Integer"),
                (5, "Integer"),
            ],
        )

    def test_069_max_07_compare_02_lhs(self):
        self.verify(
            "max(2 5)==2",
            [
                (3, "Eq"),
                (4, "Max"),
                (5, "Integer"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_070_message_01(self):
        self.verify(
            'message("x is" A)',
            [(3, "MessageParentheses"), (4, "String"), (4, "PieceDesignator")],
        )

    def test_070_message_02(self):
        self.verify(
            'message "x is"',
            [(3, "Message"), (4, "String")],
        )

    def test_070_message_03(self):
        self.verify(
            "message A",
            [(3, "Message"), (4, "PieceDesignator")],
        )

    def test_070_message_04(self):
        self.verify(
            "message quiet (A)",
            [(3, "MessageParentheses"), (4, "PieceDesignator")],
        )

    def test_070_message_05(self):
        self.verify(
            "message quiet A", [(3, "Message"), (4, "PieceDesignator")]
        )

    def test_071_min_01(self):
        self.verify("min", [], returncode=1)

    def test_071_min_02(self):
        self.verify("min()", [], returncode=1)

    def test_071_min_03(self):
        self.verify("min(2)", [], returncode=1)

    def test_071_min_04(self):
        self.verify("min(2 5)", [(3, "Min"), (4, "Integer"), (4, "Integer")])

    def test_071_min_05(self):
        self.verify('min(2 5 "k")', [], returncode=1)

    def test_071_min_06(self):
        self.verify(
            "min(2 5 1)",  # Any number of integers.
            [(3, "Min"), (4, "Integer"), (4, "Integer"), (4, "Integer")],
        )

    def test_071_min_07_compare_01_rhs(self):
        self.verify(
            "2==min(2 5)",
            [
                (3, "Eq"),
                (4, "Integer"),
                (4, "Min"),
                (5, "Integer"),
                (5, "Integer"),
            ],
        )

    def test_071_min_07_compare_02_lhs(self):
        self.verify(
            "min(2 5)==2",
            [
                (3, "Eq"),
                (4, "Min"),
                (5, "Integer"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_072_modelmate(self):
        self.verify("modelmate", [(3, "ModelMate")])

    def test_073_modelstalemate(self):
        self.verify("modelstalemate", [(3, "ModelStalemate")])

    def test_074_move_01(self):
        con = self.verify("move", [(3, "Move")])
        move = con.children[0].children[0]
        self.assertEqual(move.__class__, filters.Move)
        self.assertEqual(move.filter_type, cqltypes.FilterType.LOGICAL)

    def test_074_move_02(self):
        self.verify("move capture", [], returncode=1)

    def test_074_move_03(self):
        con = self.verify("move castle", [(3, "Move"), (4, "CastleParameter")])
        move = con.children[0].children[0]
        self.assertEqual(move.__class__, filters.Move)
        self.assertEqual(move.filter_type, cqltypes.FilterType.LOGICAL)

    def test_074_move_04(self):
        self.verify("move comment", [], returncode=1)

    def test_074_move_05(self):
        self.verify("move count", [], returncode=1)

    def test_074_move_06(self):
        self.verify("move enpassant", [(3, "Move"), (4, "EnPassantParameter")])

    def test_074_move_07(self):
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
        con = self.verify(
            "move capture P",
            [(3, "Move"), (4, "Capture"), (5, "PieceDesignator")],
        )
        move = con.children[0].children[0]
        self.assertEqual(move.__class__, filters.Move)
        self.assertEqual(move.filter_type, cqltypes.FilterType.SET)

    def test_074_move_20(self):
        self.verify(
            'move comment ("Any move")',
            [(3, "Move"), (4, "CommentParenthesesParameter"), (5, "String")],
        )

    def test_074_move_21_comment_parameter_01_plain(self):
        self.verify(
            'move legal comment "Any move"',
            [
                (3, "Move"),
                (4, "LegalParameter"),
                (3, "Comment"),
                (4, "String"),
            ],
        )

    def test_074_move_21_comment_parameter_02_parentheses(self):
        self.verify(
            'move legal comment ("Any move")',
            [
                (3, "Move"),
                (4, "LegalParameter"),
                (3, "CommentParentheses"),
                (4, "String"),
            ],
        )

    def test_074_move_22_comment_parameter_01_plain(self):
        self.verify(
            'move pseudolegal comment "Any move"',
            [
                (3, "Move"),
                (4, "PseudolegalParameter"),
                (3, "Comment"),
                (4, "String"),
            ],
        )

    def test_074_move_22_comment_parameter_02_parentheses(self):
        self.verify(
            'move pseudolegal comment ("Any move")',
            [
                (3, "Move"),
                (4, "PseudolegalParameter"),
                (3, "CommentParentheses"),
                (4, "String"),
            ],
        )

    def test_074_move_23(self):
        con = self.verify(
            "move count legal",
            [(3, "Move"), (4, "Count"), (4, "LegalParameter")],
        )
        move = con.children[0].children[0]
        self.assertEqual(move.__class__, filters.Move)
        self.assertEqual(move.filter_type, cqltypes.FilterType.NUMERIC)

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

    def test_074_move_27(self):
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

    def test_074_move_31(self):
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

    def test_074_move_33(self):
        self.verify(
            'move castle comment ("Any move")',
            [
                (3, "Move"),
                (4, "CastleParameter"),
                (4, "CommentParenthesesParameter"),
                (5, "String"),
            ],
        )

    def test_074_move_34(self):
        self.verify(
            'move castle comment ("Any move") to r',
            [
                (3, "Move"),
                (4, "CastleParameter"),
                (4, "CommentParenthesesParameter"),
                (5, "String"),
                (3, "To"),
                (3, "PieceDesignator"),
            ],
        )

    def test_074_move_35(self):
        self.verify('move castle comment ("Any move") null', [], returncode=1)

    def test_074_move_36(self):
        self.verify(
            'move pseudolegal castle comment ("Any move")',
            [
                (3, "Move"),
                (4, "PseudolegalParameter"),
                (4, "CastleParameter"),
                (3, "CommentParentheses"),
                (4, "String"),
            ],
        )

    def test_074_move_37(self):
        self.verify("move primary secondary", [], returncode=1)

    def test_074_move_38(self):
        self.verify("move secondary primary", [], returncode=1)

    def test_075_movenumber(self):
        self.verify("movenumber", [(3, "MoveNumber")])

    def test_076_northeast_01(self):
        self.verify("northeast", [], returncode=1)

    def test_076_northeast_02(self):
        self.verify(
            "northeast P",
            [
                (3, "Northeast"),
                (4, "PieceDesignator"),
            ],
        )

    def test_076_northeast_03(self):
        self.verify(
            "northeast 1 4 P",
            [
                (3, "Northeast"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "PieceDesignator"),
            ],
        )

    def test_077_northwest_01(self):
        self.verify("northwest", [], returncode=1)

    def test_077_northwest_02(self):
        self.verify(
            "northwest P",
            [
                (3, "Northwest"),
                (4, "PieceDesignator"),
            ],
        )

    def test_077_northwest_03(self):
        self.verify(
            "northwest 1 4 P",
            [
                (3, "Northwest"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "PieceDesignator"),
            ],
        )

    def test_078_not_01(self):
        self.verify("not", [], returncode=1)

    def test_078_not_02(self):
        self.verify(
            "not P",
            [
                (3, "Not"),
                (4, "PieceDesignator"),
            ],
        )

    def test_079_notransform_01(self):
        self.verify("notransform", [], returncode=1)

    def test_079_notransform_02(self):
        self.verify(
            "notransform P",
            [
                (3, "NoTransform"),
                (4, "PieceDesignator"),
            ],
        )

    def test_080_nullmove(self):
        self.verify("nullmove", [(3, "NullMove")])

    def test_081_oo(self):
        self.verify("o-o", [(3, "OO")])

    def test_082_ooo(self):
        self.verify("o-o-o", [(3, "OOO")])

    def test_083_or_01(self):
        self.verify("or", [], returncode=1)

    def test_083_or_02(self):
        self.verify("A or", [], returncode=1)

    def test_083_or_03(self):
        self.verify(
            "A or k",
            [
                (3, "Or"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_084_originalcomment_01(self):
        self.verify("originalcomment", [(3, "OriginalComment")])

    def test_084_originalcomment_02(self):
        self.verify(
            'originalcomment "good"',
            [
                (3, "OriginalComment"),
                (4, "ImplicitSearchParameter"),
            ],
        )

    def test_085_parent(self):
        self.verify("parent", [(3, "Parent")])

    def test_086_passedpawns(self):
        self.verify("passedpawns", [(3, "PassedPawns")])

    def test_088_pathcount(self):
        self.verify("pathcount", [(3, "PathCount")])

    def test_089_pathcountunfocused(self):
        self.verify("pathcountunfocused", [(3, "PathCountUnfocused")])

    def test_090_pathlastposition(self):
        self.verify("pathlastposition", [(3, "PathLastPosition")])

    # Not 'pathstatus' as given in Table of Filters.
    def test_091_pathstart(self):
        self.verify("pathstart", [(3, "PathStart")])

    def test_092_persistent_01(self):
        self.verify("persistent", [], returncode=1)

    def test_092_persistent_02_quiet(self):
        self.verify("persistent quiet", [], returncode=1)

    def test_092_persistent_03_variable(self):
        self.verify("persistent x", [], returncode=1)

    def test_092_persistent_04_quiet_variable(self):
        self.verify("persistent quiet x", [], returncode=1)

    def test_092_persistent_05_variable_equal(self):
        self.verify("persistent x=", [], returncode=1)

    def test_092_persistent_06_quiet_variable_equal(self):
        self.verify("persistent quiet x=", [], returncode=1)

    def test_092_persistent_07_variable_equal_01_integer(self):
        self.verify(
            "persistent x=2",
            [(3, "Assign"), (4, "Persistent"), (4, "Integer")],
        )

    def test_092_persistent_07_variable_equal_02_string(self):
        self.verify(
            'persistent x="a"',
            [(3, "Assign"), (4, "Persistent"), (4, "String")],
        )

    def test_092_persistent_07_variable_equal_03_set(self):
        self.verify(
            "persistent x=connectedpawns",
            [(3, "Assign"), (4, "Persistent"), (4, "ConnectedPawns")],
        )

    def test_092_persistent_07_variable_equal_04_piecedesignator(self):
        self.verify(
            "persistent x=q",
            [(3, "Assign"), (4, "Persistent"), (4, "PieceDesignator")],
        )

    def test_092_persistent_07_variable_equal_05_logical(self):
        self.verify("persistent x=false", [], returncode=1)

    def test_092_persistent_07_variable_equal_06_position(self):
        self.verify("persistent x=currentposition", [], returncode=1)

    def test_092_persistent_08_quiet_variable_equal_01_integer(self):
        self.verify(
            "persistent quiet x=2",
            [(3, "Assign"), (4, "PersistentQuiet"), (4, "Integer")],
        )

    def test_092_persistent_08_quiet_variable_equal_02_string(self):
        self.verify(
            'persistent quiet x="a"',
            [(3, "Assign"), (4, "PersistentQuiet"), (4, "String")],
        )

    def test_092_persistent_08_quiet_variable_equal_03_set(self):
        self.verify(
            "persistent quiet x=connectedpawns",
            [(3, "Assign"), (4, "PersistentQuiet"), (4, "ConnectedPawns")],
        )

    def test_092_persistent_08_quiet_variable_equal_04_piecedesignator(self):
        self.verify(
            "persistent quiet x=q",
            [(3, "Assign"), (4, "PersistentQuiet"), (4, "PieceDesignator")],
        )

    def test_092_persistent_08_quiet_variable_equal_05_logical(self):
        self.verify("persistent quiet x=false", [], returncode=1)

    def test_092_persistent_08_quiet_variable_equal_06_position(self):
        self.verify("persistent quiet x=currentposition", [], returncode=1)

    def test_092_persistent_09_persistent_first(self):
        self.verify(
            "persistent X=1 X=2",
            [
                (3, "Assign"),
                (4, "Persistent"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
            ],
        )

    def test_092_persistent_10_persistent_second(self):
        self.verify("X=1 persistent X=2", [], returncode=1)

    def test_092_persistent_11_persistent_both(self):
        self.verify(
            "persistent X=1 persistent X=2",
            [
                (3, "Assign"),
                (4, "Persistent"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "Persistent"),
                (4, "Integer"),
            ],
        )

    def test_092_persistent_12_persistent_atomic(self):
        self.verify(
            "persistent X=1 atomic X=2",
            [
                (3, "Assign"),
                (4, "Persistent"),
                (4, "Integer"),
                (3, "Assign"),
                (4, "Atomic"),
                (4, "Integer"),
            ],
        )

    def test_093_piece_01(self):
        self.verify("piece", [], returncode=1)

    def test_093_piece_02_all(self):
        self.verify("piece all", [], returncode=1)

    def test_093_piece_03_variable(self):
        self.verify("piece x", [], returncode=1)

    # 'piece x =' is piece assignment: see test_095_piece_assignment.
    def test_093_piece_04_variable_y(self):  # not 'in'.
        self.verify("piece x y", [], returncode=1)

    def test_093_piece_05_all_variable(self):
        self.verify("piece all x", [], returncode=1)

    def test_093_piece_06_all_variable_y(self):  # not 'in'.
        self.verify("piece all x y", [], returncode=1)

    def test_093_piece_07_variable_in(self):
        self.verify("piece x in", [], returncode=1)

    def test_093_piece_08_all_variable_in(self):
        self.verify("piece all x in", [], returncode=1)

    def test_093_piece_09_variable_in_infilter(self):
        self.verify("piece x in A", [], returncode=1)

    def test_093_piece_10_all_variable_in_infilter(self):
        self.verify("piece all x in A", [], returncode=1)

    def test_093_piece_11_variable_in_infilter_body(self):
        self.verify(
            "piece x in A k",  # Normally body refers to 'x'.
            [(3, "Piece"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_093_piece_12_all_variable_in_infilter_body(self):
        self.verify(
            "piece all x in A k",  # Normally body refers to 'x'.
            [(3, "PieceAll"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_094_piecename_01(self):
        self.verify("piecename", [], returncode=1)

    def test_094_piecename_02_set(self):
        self.verify(
            "piecename k",  # Something like 'd4' is a more useful argument.
            [(3, "PieceName"), (4, "PieceDesignator")],
        )

    def test_095_piece_assignment_01(self):  # Repeats an 093 test.
        self.verify("piece", [], returncode=1)

    def test_095_piece_assignment_02_equals(self):
        self.verify("piece=", [], returncode=1)

    def test_095_piece_assignment_03_variable(self):  # Repeats an 093 test.
        self.verify("piece x", [], returncode=1)

    def test_095_piece_assignment_04_variable_equals(self):
        self.verify("piece x=", [], returncode=1)

    def test_095_piece_assignment_05_variable_equals_set(self):
        # More tests in "=" and "=?" tests.
        self.verify(
            "piece x=K",
            [(3, "Assign"), (4, "PieceVariable"), (4, "PieceDesignator")],
        )

    def test_096_pieceid_01(self):
        self.verify("pieceid", [], returncode=1)

    def test_096_pieceid_02_set(self):
        self.verify("pieceid q", [(3, "PieceId"), (4, "PieceDesignator")])

    def test_097_pin_01(self):
        self.verify("pin", [(3, "Pin")])

    def test_097_pin_02_from(self):
        self.verify("pin from", [], returncode=1)

    def test_097_pin_03_from_set(self):
        self.verify(
            "pin from Q",
            [(3, "Pin"), (4, "FromParameter"), (5, "PieceDesignator")],
        )

    def test_097_pin_04_from_set_to(self):
        self.verify("pin from Q to", [], returncode=1)

    def test_097_pin_05_from_set_to_set(self):
        self.verify(
            "pin from Q to k",
            [
                (3, "Pin"),
                (4, "FromParameter"),
                (5, "PieceDesignator"),
                (4, "ToParameter"),
                (5, "PieceDesignator"),
            ],
        )

    def test_097_pin_06_through(self):
        self.verify("pin through", [], returncode=1)

    def test_097_pin_07_through_set(self):
        self.verify(
            "pin through n",
            [(3, "Pin"), (4, "Through"), (5, "PieceDesignator")],
        )

    def test_097_pin_08_through_set_from(self):
        self.verify("pin through n from", [], returncode=1)

    def test_097_pin_09_through_set_from_set(self):
        self.verify(
            "pin through n from Q",
            [
                (3, "Pin"),
                (4, "Through"),
                (5, "PieceDesignator"),
                (4, "FromParameter"),
                (5, "PieceDesignator"),
            ],
        )

    def test_097_pin_10_to(self):
        self.verify("pin to", [], returncode=1)

    def test_097_pin_11_to_set(self):
        self.verify(
            "pin to k",
            [(3, "Pin"), (4, "ToParameter"), (5, "PieceDesignator")],
        )

    def test_097_pin_12_to_set_through(self):
        self.verify("pin to k through", [], returncode=1)

    def test_097_pin_13_to_set_through_set(self):
        self.verify(
            "pin to k through n",
            [
                (3, "Pin"),
                (4, "ToParameter"),
                (5, "PieceDesignator"),
                (4, "Through"),
                (5, "PieceDesignator"),
            ],
        )

    def test_097_pin_14_to_set_from_set_through(self):
        self.verify("pin to k from Q through", [], returncode=1)

    def test_097_pin_15_to_set_from_set_through_set(self):
        self.verify(
            "pin to k from Q through n",
            [
                (3, "Pin"),
                (4, "ToParameter"),
                (5, "PieceDesignator"),
                (4, "FromParameter"),
                (5, "PieceDesignator"),
                (4, "Through"),
                (5, "PieceDesignator"),
            ],
        )

    def test_097_pin_16_to_to(self):
        self.verify("pin to to", [(3, "Pin"), (4, "ToParameter"), (5, "To")])

    def test_097_pin_17_to_from(self):
        self.verify(
            "pin to from", [(3, "Pin"), (4, "ToParameter"), (5, "From")]
        )

    def test_097_pin_18_to_through(self):
        self.verify("pin to through", [], returncode=1)

    def test_097_pin_19_from_to(self):
        self.verify(
            "pin from to", [(3, "Pin"), (4, "FromParameter"), (5, "To")]
        )

    def test_097_pin_20_from_from(self):
        self.verify(
            "pin from from", [(3, "Pin"), (4, "FromParameter"), (5, "From")]
        )

    def test_097_pin_21_from_through(self):
        self.verify("pin from through", [], returncode=1)

    def test_097_pin_22_through_from(self):
        self.verify(
            "pin through from", [(3, "Pin"), (4, "Through"), (5, "From")]
        )

    def test_097_pin_23_through_to(self):
        self.verify("pin through to", [(3, "Pin"), (4, "Through"), (5, "To")])

    def test_097_pin_24_from_from_from(self):
        self.verify("pin from from from", [], returncode=1)

    def test_097_pin_25_to_from_from_from(self):
        self.verify(
            "pin to from from from",
            [
                (3, "Pin"),
                (4, "ToParameter"),
                (5, "From"),
                (4, "FromParameter"),
                (5, "From"),
            ],
        )

    def test_097_pin_26_to_to_to(self):
        self.verify("pin to to to", [], returncode=1)

    def test_097_pin_27_from_to_to_to(self):
        self.verify(
            "pin from to to to",
            [
                (3, "Pin"),
                (4, "FromParameter"),
                (5, "To"),
                (4, "ToParameter"),
                (5, "To"),
            ],
        )

    def test_098_player_01(self):
        self.verify("player", [(3, "Player")])

    def test_098_player_02(self):
        self.verify(
            'player "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_099_player_white_01(self):  # chessql gets this wrong.
        self.verify("player white", [(3, "Player")])

    def test_099_player_white_02(self):  # chessql gets this wrong.
        self.verify(
            'player white "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_100_player_black_01(self):  # chessql gets this wrong.
        self.verify("player black", [(3, "Player")])

    def test_100_player_black_02(self):  # chessql gets this wrong.
        self.verify(
            'player black "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_101_ply(self):
        self.verify("ply", [(3, "Ply")])

    def test_102_position_01(self):
        self.verify("position", [], returncode=1)

    def test_102_position_02_number(self):
        self.verify("position 1", [(3, "Position"), (4, "Integer")])

    def test_103_positionid(self):
        self.verify("positionid", [(3, "PositionId")])

    def test_104_power_01(self):
        self.verify("power", [], returncode=1)

    def test_104_power_02_set(self):
        self.verify("power A", [(3, "Power"), (4, "PieceDesignator")])

    def test_105_primary(self):  # chessql gets this wrong.
        self.verify("primary", [(3, "Primary")])

    def test_106_pseudolegal_01(self):
        self.verify("pseudolegal", [], returncode=1)

    def test_106_pseudolegal_02_dash(self):
        self.verify(
            "pseudolegal --",
            [
                (3, "Pseudolegal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_106_pseudolegal_02_captures(self):
        self.verify("pseudolegal [x]", [], returncode=1)

    def test_107_puremate(self):
        self.verify("puremate", [(3, "PureMate")])

    def test_108_purestalemate(self):
        self.verify("purestalemate", [(3, "PureStalemate")])

    def test_109_rank_01(self):
        self.verify("rank", [], returncode=1)

    def test_109_rank_02_set(self):
        self.verify("rank q", [(3, "Rank"), (4, "PieceDesignator")])

    def test_110_ray_01(self):
        self.verify("ray", [], returncode=1)

    def test_110_ray_02_direction(self):
        self.verify("ray up", [], returncode=1)

    def test_110_ray_03_set(self):
        self.verify("ray (Q)", [], returncode=1)

    def test_110_ray_04_direction_set(self):
        self.verify("ray up (Q)", [], returncode=1)

    def test_110_ray_05_set_set(self):
        self.verify(
            "ray (Q r)",
            [(3, "Ray"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_110_ray_06_direction_set_set(self):  # chessql not complete?.
        self.verify(
            "ray up (Q r)",
            [(3, "Ray"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_110_ray_07_direction_direction_set_set(self):
        self.verify(
            "ray up down (Q r)",
            [(3, "Ray"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_110_ray_08_all_directions_01_set_set(self):
        all_directions = " ".join(
            (
                "up",
                "down",
                "left",
                "right",
                "northeast",
                "northwest",
                "southeast",
                "southwest",
            )
        )
        self.verify(
            "ray " + all_directions + " (Q r)",
            [(3, "Ray"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_110_ray_08_all_directions_02_set_set(self):
        all_directions = " ".join(
            (
                "diagonal",
                "vertical",
                "horizontal",
            )
        )
        self.verify(
            "ray diagonal vertical horizontal (Q r)",
            [(3, "Ray"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_110_ray_09_any_direction_set_set(self):
        self.verify(
            "ray anydirection (Q r)",
            [(3, "Ray"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_110_ray_10_orthogonal_set_set(self):
        self.verify(
            "ray orthogonal (Q r)",
            [(3, "Ray"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_110_ray_11_direction_repeated_set_set(self):
        self.verify("ray up up (Q r)", [], returncode=1)

    def test_110_ray_12_direction_duplicate_set_set(self):
        self.verify("ray up vertical (Q r)", [], returncode=1)

    def test_111_readfile_01(self):
        self.verify("readfile", [], returncode=1)

    def test_111_readfile_01_name(self):
        self.verify('readfile "x.cql"', [(3, "ReadFile"), (4, "String")])

    def test_112_removecomment(self):
        self.verify("removecomment", [(3, "RemoveComment")])

    def test_113_result_01(self):
        self.verify("result", [], returncode=1)

    def test_113_result_01_name(self):
        self.verify('result "1-0"', [(3, "Result"), (4, "String")])

    def test_114_reversecolor_01(self):
        self.verify("reversecolor", [], returncode=1)

    def test_114_reversecolor_02(self):
        self.verify("reversecolor btm", [(3, "ReverseColor"), (4, "BTM")])

    def test_114_reversecolor_03(self):
        self.verify("reversecolor count btm", [], returncode=1)

    def test_115_right_01(self):
        self.verify("right", [], returncode=1)

    def test_115_right_02(self):
        self.verify(
            "right P",
            [
                (3, "Right"),
                (4, "PieceDesignator"),
            ],
        )

    def test_115_right_03(self):
        self.verify(
            "right 1 4 P",
            [
                (3, "Right"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "PieceDesignator"),
            ],
        )

    def test_116_rotate45_01(self):
        self.verify("rotate45", [], returncode=1)

    def test_116_rotate45_02(self):
        self.verify("rotate45 btm", [(3, "Rotate45"), (4, "BTM")])

    def test_116_rotate45_03(self):
        self.verify(
            "rotate45 count btm",
            [(3, "Rotate45"), (4, "Count"), (4, "BTM")],
        )

    def test_117_rotate90_01(self):
        self.verify("rotate90", [], returncode=1)

    def test_117_rotate90_02(self):
        self.verify("rotate90 btm", [(3, "Rotate90"), (4, "BTM")])

    def test_117_rotate90_03(self):
        self.verify(
            "rotate90 count btm",
            [(3, "Rotate90"), (4, "Count"), (4, "BTM")],
        )

    def test_118_secondary(self):  # chessql gets this wrong.
        self.verify("secondary", [(3, "Secondary")])

    def test_119_settag_01(self):
        self.verify("settag", [], returncode=1)

    def test_119_settag_02_string(self):
        self.verify('settag("MyTag")', [], returncode=1)

    def test_119_settag_03_string_string(self):
        self.verify(
            'settag("MyTag" "Value")',
            [(3, "SetTag"), (4, "String"), (4, "String")],
        )

    def test_119_settag_04_string_int_01(self):
        self.verify('settag("MyTag" 1)', [], returncode=1)

    def test_119_settag_04_string_int_02(self):
        self.verify(
            'settag("MyTag" "1")',
            [(3, "SetTag"), (4, "String"), (4, "String")],
        )

    def test_120_shift_01(self):
        self.verify("shift", [], returncode=1)

    def test_120_shift_02(self):
        self.verify("shift btm", [(3, "Shift"), (4, "BTM")])

    def test_120_shift_03(self):
        self.verify(
            "shift count btm",
            [(3, "Shift"), (4, "Count"), (4, "BTM")],
        )

    def test_121_shifthorizontal_01(self):
        self.verify("shifthorizontal", [], returncode=1)

    def test_121_shifthorizontal_02(self):
        self.verify(
            "shifthorizontal btm",
            [(3, "ShiftHorizontal"), (4, "BTM")],
        )

    def test_121_shifthorizontal_03(self):
        self.verify(
            "shifthorizontal count btm",
            [(3, "ShiftHorizontal"), (4, "Count"), (4, "BTM")],
        )

    def test_122_shiftvertical_01(self):
        self.verify("shiftvertical", [], returncode=1)

    def test_122_shiftvertical_02(self):
        self.verify("shiftvertical btm", [(3, "ShiftVertical"), (4, "BTM")])

    def test_122_shiftvertical_03(self):
        self.verify(
            "shiftvertical count btm",
            [(3, "ShiftVertical"), (4, "Count"), (4, "BTM")],
        )

    def test_123_sidetomove(self):
        self.verify("sidetomove", [(3, "SideToMove")])

    def test_124_site_01(self):
        self.verify("site", [(3, "Site")])

    def test_124_site_02_value(self):
        self.verify(
            'site "place"',
            [(3, "Site"), (4, "ImplicitSearchParameter")],
        )

    # Make sure all other implicit search parameter filters have this test.
    def test_124_site_03_value_match(self):
        self.verify(
            'site ~~ "place"',
            [(3, "RegexMatch"), (4, "Site"), (4, "String")],
        )

    def test_125_sort_01(self):
        self.verify("sort", [], returncode=1)

    def test_125_sort_02_int(self):
        self.verify_declare_fail("sort 1", [(3, "Sort"), (4, "Integer")])

    def test_125_sort_03_string(self):
        self.verify('sort "1"', [], returncode=1)

    def test_125_sort_04_filter_int_01(self):
        self.verify('sort int "1"', [(3, "Sort"), (4, "Int"), (5, "String")])

    def test_125_sort_04_filter_str_02(self):
        self.verify(
            'sort str("1")',
            [(3, "Sort"), (4, "StrParentheses"), (5, "String")],
        )

    def test_125_sort_05_doc_filter_int_01(self):
        self.verify(
            'sort "doc" int "1"',
            [(3, "Sort"), (4, "Documentation"), (4, "Int"), (5, "String")],
        )

    def test_125_sort_05_doc_filter_str_02(self):
        self.verify(
            'sort "doc" str("1")',
            [
                (3, "Sort"),
                (4, "Documentation"),
                (4, "StrParentheses"),
                (5, "String"),
            ],
        )

    def test_125_sort_05_min(self):
        self.verify("sort min", [], returncode=1)

    def test_125_sort_05_min_01_filter_int(self):
        self.verify_declare_fail(
            'sort min int "1"', [(3, "Sort"), (4, "Int"), (5, "String")]
        )

    def test_125_sort_05_min_02_filter_str(self):
        self.verify_declare_fail(
            'sort min str("1")',
            [(3, "Sort"), (4, "StrParentheses"), (5, "String")],
        )

    def test_125_sort_06_min_doc(self):
        self.verify('sort min "doc"', [], returncode=1)

    def test_125_sort_06_min_doc_01_filter_int(self):
        self.verify(
            'sort min "doc" int "1"',
            [(3, "Sort"), (4, "Documentation"), (4, "Int"), (5, "String")],
        )

    def test_125_sort_06_min_doc_02_filter_str(self):
        self.verify(
            'sort min "doc" str("1")',
            [
                (3, "Sort"),
                (4, "Documentation"),
                (4, "StrParentheses"),
                (5, "String"),
            ],
        )

    def test_126_sqrt_01(self):
        self.verify("sqrt", [], returncode=1)

    def test_126_sqrt_02_number(self):
        self.verify("sqrt 16", [(3, "Sqrt"), (4, "Integer")])

    def test_127_square_01(self):
        self.verify("square", [], returncode=1)

    def test_127_square_02_in(self):
        self.verify("square in", [], returncode=1)

    def test_127_square_03_variable(self):
        self.verify("square x", [], returncode=1)

    def test_127_square_04_variable_in_01(self):
        self.verify("square x in", [], returncode=1)

    def test_127_square_04_variable_in_02_filter(self):
        self.verify("square x in R", [], returncode=1)

    def test_127_square_04_variable_in_03_filter_body(self):  # chessql wrong.
        self.verify(
            "square x in R btm",
            [(3, "Square"), (4, "PieceDesignator"), (4, "BTM")],
        )

    def test_127_square_05_all(self):
        self.verify("square all", [], returncode=1)

    def test_127_square_06_all_variable(self):
        self.verify("square all x", [], returncode=1)

    def test_127_square_07_all_variable_in_01(self):
        self.verify("square all x in", [], returncode=1)

    def test_127_square_07_all_variable_in_02_filter(self):
        self.verify("square all x in R", [], returncode=1)

    def test_127_square_07_all_variable_in_03_filter_body(self):  # wrong.
        self.verify(
            "square all x in R btm",
            [(3, "SquareAll"), (4, "PieceDesignator"), (4, "BTM")],
        )

    def test_128_stalemate(self):
        self.verify("stalemate", [(3, "Stalemate")])

    def test_129_str_01(self):
        self.verify("str", [], returncode=1)

    def test_129_str_02_string_01(self):
        self.verify('str "string"', [(3, "Str"), (4, "String")])

    def test_129_str_02_string_02(self):
        self.verify('str("string")', [(3, "StrParentheses"), (4, "String")])

    def test_129_str_03_string_string_01(self):
        self.verify(
            'str "string" "string"',
            [(3, "Str"), (4, "String"), (3, "String")],
        )

    def test_129_str_03_string_string_02(self):
        self.verify(
            'str("string" "string")',
            [(3, "StrParentheses"), (4, "String"), (4, "String")],
        )

    def test_130_tag_01(self):
        self.verify("tag", [], returncode=1)

    def test_130_tag_02_string(self):
        self.verify('tag "MyTag"', [(3, "Tag"), (4, "String")])

    def test_131_terminal(self):
        self.verify("terminal", [(3, "Terminal")])

    def test_132_to(self):
        self.verify("to", [(3, "To")])

    def test_133_true(self):
        self.verify("true", [(3, "True_")])

    def test_134_try(self):
        self.verify("try", [(3, "Try")])

    def test_135_type_01(self):
        self.verify("type", [], returncode=1)

    def test_135_type_02_set(self):
        self.verify(
            "type d4",
            [(3, "Type"), (4, "PieceDesignator")],
        )

    def test_136_typename_01(self):
        self.verify("typename", [], returncode=1)

    def test_136_typename_02_set(self):
        self.verify(
            "typename d4",
            [(3, "TypeName"), (4, "PieceDesignator")],
        )

    def test_137_unbind_01(self):
        self.verify("unbind", [], returncode=1)

    def test_137_unbind_02_variable(self):
        self.verify("unbind x", [], returncode=1)

    def test_137_unbind_03_variable(self):
        con = self.verify(
            "x=1 unbind x",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Unbind"),
                (4, "Variable"),
            ],
        )
        self.assertEqual("x" in con.definitions, True)

    def test_137_unbind_04_dictionary(self):
        con = self.verify(
            "dictionary v unbind v",
            [
                (3, "Dictionary"),
                (3, "Unbind"),
                (4, "Dictionary"),
            ],
        )
        self.assertEqual("v" in con.definitions, True)

    def test_137_unbind_04_dictionary_key_01(self):
        self.verify('dictionary v unbind v["key"]', [], returncode=1)

    def test_137_unbind_04_dictionary_key_02(self):
        con = self.verify(
            'dictionary v["key"]="value" unbind v["key"]',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
                (3, "Unbind"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
            ],
        )
        self.assertEqual("v" in con.definitions, True)

    def test_137_unbind_04_dictionary_key_03(self):
        con = self.verify(
            'dictionary v["key"]="value" unbind v',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
                (3, "Unbind"),
                (4, "Dictionary"),
            ],
        )
        self.assertEqual("v" in con.definitions, True)

    def test_137_unbind_04_dictionary_key_04(self):
        self.verify('unbind v["key"]', [], returncode=1)

    def test_138_up_01(self):
        self.verify("up", [], returncode=1)

    def test_138_up_02(self):
        self.verify(
            "up P",
            [
                (3, "Up"),
                (4, "PieceDesignator"),
            ],
        )

    def test_138_up_03(self):
        self.verify(
            "up 1 4 P",
            [
                (3, "Up"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "PieceDesignator"),
            ],
        )

    def test_139_uppercase_01(self):
        self.verify("uppercase", [], returncode=1)

    def test_139_uppercase_02_string(self):
        self.verify('uppercase "MyTag"', [(3, "UpperCase"), (4, "String")])

    def test_140_variation(self):
        self.verify("variation", [(3, "Variation")])

    def test_141_virtualmainline(self):
        self.verify("virtualmainline", [(3, "VirtualMainLine")])

    def test_142_while_01(self):
        self.verify("while", [], returncode=1)

    def test_142_while_02_test_01(self):
        self.verify("while ()", [], returncode=1)

    def test_142_while_02_test_02(self):
        self.verify("while (k)", [], returncode=1)

    def test_142_while_02_test_03_body(self):
        self.verify(
            "while (k) q",
            [
                (3, "While"),
                (4, "ParenthesisLeft"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_142_while_02_test_04_body(self):
        self.verify(
            "while (k) {q}",
            [
                (3, "While"),
                (4, "ParenthesisLeft"),
                (5, "PieceDesignator"),
                (4, "BraceLeft"),
                (5, "PieceDesignator"),
            ],
        )

    def test_142_while_02_test_05_body(self):
        self.verify(
            'while (site~~".*") q',
            [
                (3, "While"),
                (4, "ParenthesisLeft"),
                (5, "RegexMatch"),
                (6, "Site"),
                (6, "String"),
                (4, "PieceDesignator"),
            ],
        )

    def test_142_while_02_test_06_body(self):
        self.verify(
            'while (site~~".*") {q}',
            [
                (3, "While"),
                (4, "ParenthesisLeft"),
                (5, "RegexMatch"),
                (6, "Site"),
                (6, "String"),
                (4, "BraceLeft"),
                (5, "PieceDesignator"),
            ],
        )

    def test_143_white(self):
        self.verify("white", [(3, "White")])

    def test_144_writefile_01(self):
        self.verify("writefile", [], returncode=1)

    def test_144_writefile_02(self):
        self.verify("writefile(", [], returncode=1)

    def test_144_writefile_03(self):
        self.verify("writefile()", [], returncode=1)

    def test_144_writefile_04_out_01(self):
        self.verify('writefile("outfile")', [], returncode=1)

    def test_144_writefile_04_out_02_text(self):
        self.verify(
            'writefile("outfile" "text")',
            [(3, "WriteFile"), (4, "String"), (4, "String")],
        )

    def test_144_writefile_04_out_03_text_more(self):
        self.verify('writefile("outfile" "text" K)', [], returncode=1)

    def test_145_xray_01(self):
        self.verify("xray", [], returncode=1)

    def test_145_xray_02_set(self):
        self.verify("xray (Q)", [], returncode=1)

    def test_145_xray_03_set_set(self):
        self.verify(
            "xray (Q r)",
            [(3, "XRay"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_145_xray_04_unassigned_variable(self):
        self.verify("xray (r v)", [], returncode=1)

    def test_145_xray_05_integer_variable(self):
        self.verify("v=3 xray (r v)", [], returncode=1)

    def test_145_xray_06_string_variable(self):
        self.verify('v="w" xray (r v)', [], returncode=1)

    def test_145_xray_07_position_variable(self):
        self.verify("v=currentposition xray (r v)", [], returncode=1)

    def test_146_year(self):
        self.verify("year", [(3, "Year")])

    def test_149_piecedsignator_01_K_ascii(self):
        self.verify("K", [(3, "PieceDesignator")])

    def test_149_piecedsignator_01_K_utf8(self):
        self.verify("♔", [(3, "PieceDesignator")])

    def test_149_piecedsignator_02_A_ascii(self):
        self.verify("A", [(3, "PieceDesignator")])

    def test_149_piecedsignator_02_A_utf8(self):
        self.verify("△", [(3, "PieceDesignator")])

    def test_149_piecedsignator_03_a_ascii(self):
        self.verify("a", [(3, "PieceDesignator")])

    def test_149_piecedsignator_03_a_utf8(self):
        self.verify("▲", [(3, "PieceDesignator")])

    def test_149_piecedsignator_04_Aa_ascii(self):
        self.verify("[Aa]", [(3, "PieceDesignator")])

    def test_149_piecedsignator_04_Aa_utf8(self):
        self.verify("◭", [(3, "PieceDesignator")])

    def test_149_piecedsignator_05_empty_ascii(self):
        self.verify("_", [(3, "PieceDesignator")])

    def test_149_piecedsignator_05_empty_utf8(self):
        self.verify("□", [(3, "PieceDesignator")])

    def test_149_piecedsignator_06_all_squares_ascii(self):
        self.verify("a-h1-8", [(3, "PieceDesignator")])

    # utf8 '▦' is textually equivalent to ascii '.' not ascii 'a-h1-8'.
    # '<piece>▦' is two set filters, not one like '<piece>a-h1-8'.
    def test_149_piecedsignator_06_all_squares_utf8(self):
        self.verify("▦", [(3, "AnySquare")])

    def test_149_piecedsignator_07_some_pieces_ascii(self):
        self.verify("[QrbNp]", [(3, "PieceDesignator")])

    def test_149_piecedsignator_07_some_pieces_utf8(self):
        self.verify("♕♜♝♘♟", [(3, "PieceDesignator")])

    def test_149_piecedsignator_08_some_pieces_some_squares_ascii_01(self):
        self.verify("[QrbNp]b-c4-5", [(3, "PieceDesignator")])

    def test_149_piecedsignator_08_some_pieces_some_squares_ascii_02(self):
        self.verify("[QrbNp][a5,b-c4-5,h1-2,e-g4]", [(3, "PieceDesignator")])

    def test_149_piecedsignator_08_some_pieces_some_squares_utf8_01(self):
        self.verify("♕♜♝♘♟b-c4-5", [(3, "PieceDesignator")])

    def test_149_piecedsignator_08_some_pieces_some_squares_utf8_02(self):
        self.verify("♕♜♝♘♟[a5,b-c4-5,h1-2,e-g4]", [(3, "PieceDesignator")])

    def test_149_piecedsignator_09_mix_ascii_utf8_pieces(self):
        self.verify("[♕♜B♘♟]", [], returncode=1)

    def test_150_attackarrow_01_ascii(self):
        self.verify("->", [], returncode=1)

    def test_150_attackarrow_01_utf8(self):
        self.verify("→", [], returncode=1)

    def test_150_attackarrow_02_single_ascii(self):  # Same as attacks?
        self.verify(
            "A -> k",
            [
                (3, "AttackArrow"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_150_attackarrow_02_single_utf8(self):  # Same as attacks?
        self.verify(
            "A → k",
            [
                (3, "AttackArrow"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_150_attackarrow_03_double_ascii(self):
        self.verify(
            "A -> P -> k",
            [
                (3, "AttackArrow"),
                (4, "PieceDesignator"),
                (4, "AttackArrow"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
            ],
        )

    def test_150_attackarrow_03_double_utf8(self):
        self.verify(
            "A → P → k",
            [
                (3, "AttackArrow"),
                (4, "PieceDesignator"),
                (4, "AttackArrow"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
            ],
        )

    def test_150_attackarrow_04_many_ascii(self):
        self.verify(
            "A -> P -> P -> k",
            [
                (3, "AttackArrow"),
                (4, "PieceDesignator"),
                (4, "AttackArrow"),
                (5, "PieceDesignator"),
                (5, "AttackArrow"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
            ],
        )

    def test_150_attackarrow_04_many_utf8(self):
        self.verify(
            "A → P → P → k",
            [
                (3, "AttackArrow"),
                (4, "PieceDesignator"),
                (4, "AttackArrow"),
                (5, "PieceDesignator"),
                (5, "AttackArrow"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
            ],
        )

    def test_151_attackedarrow_01_ascii(self):
        self.verify("<-", [], returncode=1)

    def test_151_attackedarrow_01_utf8(self):
        self.verify("←", [], returncode=1)

    def test_151_attackedarrow_02_single_ascii(self):  # Same as attackedby?
        self.verify(
            "A <- k",
            [
                (3, "AttackedArrow"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_151_attackedarrow_02_single_utf8(self):  # Same as attackedby?
        self.verify(
            "A ← k",
            [
                (3, "AttackedArrow"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_151_attackedarrow_03_double_ascii(self):
        self.verify(
            "A <- P <- k",
            [
                (3, "AttackedArrow"),
                (4, "PieceDesignator"),
                (4, "AttackedArrow"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
            ],
        )

    def test_151_attackedarrow_03_double_utf8(self):
        self.verify(
            "A ← P ← k",
            [
                (3, "AttackedArrow"),
                (4, "PieceDesignator"),
                (4, "AttackedArrow"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
            ],
        )

    def test_151_attackedarrow_04_many_ascii(self):
        self.verify(
            "A <- P <- P <- k",
            [
                (3, "AttackedArrow"),
                (4, "PieceDesignator"),
                (4, "AttackedArrow"),
                (5, "PieceDesignator"),
                (5, "AttackedArrow"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
            ],
        )

    def test_151_attackedarrow_04_many_utf8(self):
        self.verify(
            "A ← P ← P ← k",
            [
                (3, "AttackedArrow"),
                (4, "PieceDesignator"),
                (4, "AttackedArrow"),
                (5, "PieceDesignator"),
                (5, "AttackedArrow"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
            ],
        )

    def test_152_less_than_01(self):
        self.verify("<", [], returncode=1)

    def test_152_less_than_02(self):
        self.verify("A<", [], returncode=1)

    def test_152_less_than_03(self):
        self.verify("<A", [], returncode=1)

    def test_152_less_than_04_set_01_set(self):
        self.verify("a<A", [], returncode=1)

    def test_152_less_than_04_set_02_logical(self):
        self.verify("a<true", [], returncode=1)

    def test_152_less_than_04_set_03_numeric(self):
        self.verify(
            "a<1",
            [(3, "LT"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_152_less_than_04_set_04_string(self):
        self.verify('a<"t"', [], returncode=1)

    def test_152_less_than_04_set_05_position(self):
        self.verify("a<initialposition", [], returncode=1)

    def test_152_less_than_05_logical_01_set(self):
        self.verify("true<A", [], returncode=1)

    def test_152_less_than_05_logical_02_logical(self):
        self.verify("true<true", [], returncode=1)

    def test_152_less_than_05_logical_03_numeric(self):
        self.verify("true<1", [], returncode=1)

    def test_152_less_than_05_logical_04_string(self):
        self.verify('true<"t"', [], returncode=1)

    def test_152_less_than_05_logical_05_position(self):
        self.verify("true<initialposition", [], returncode=1)

    def test_152_less_than_06_numeric_01_set(self):
        self.verify(
            "1<A",
            [(3, "LT"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_152_less_than_06_numeric_02_logical(self):
        self.verify("1<true", [], returncode=1)

    def test_152_less_than_06_numeric_03_numeric(self):
        self.verify("1<2", [(3, "LT"), (4, "Integer"), (4, "Integer")])

    def test_152_less_than_06_numeric_04_string(self):
        self.verify('1<"t"', [], returncode=1)

    def test_152_less_than_06_numeric_05_position(self):
        self.verify("1<initialposition", [], returncode=1)

    def test_152_less_than_07_string_01_set(self):
        self.verify('"a"<A', [], returncode=1)

    def test_152_less_than_07_string_02_logical(self):
        self.verify('"a"<true', [], returncode=1)

    def test_152_less_than_07_string_03_numeric(self):
        self.verify('"a"<1', [], returncode=1)

    def test_152_less_than_07_string_04_string(self):
        self.verify('"a"<"b"', [(3, "LT"), (4, "String"), (4, "String")])

    def test_152_less_than_07_string_05_position(self):
        self.verify("a<initialposition", [], returncode=1)

    def test_152_less_than_08_position_01_set(self):
        self.verify("initialposition<A", [], returncode=1)

    def test_152_less_than_08_position_02_logical(self):
        self.verify("initialposition<true", [], returncode=1)

    def test_152_less_than_08_position_03_numeric(self):
        self.verify("initialposition<1", [], returncode=1)

    def test_152_less_than_08_position_04_string(self):
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

    def test_153_lt_eq_ascii_04_set_01_set(self):
        self.verify("a<=A", [], returncode=1)

    def test_153_lt_eq_ascii_04_set_02_logical(self):
        self.verify("a<=true", [], returncode=1)

    def test_153_lt_eq_ascii_04_set_03_numeric(self):
        self.verify(
            "a<=1",
            [(3, "LE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_153_lt_eq_ascii_04_set_04_string(self):
        self.verify('a<="t"', [], returncode=1)

    def test_153_lt_eq_ascii_04_set_05_position(self):
        self.verify("a<=initialposition", [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_01_set(self):
        self.verify("true<=A", [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_02_logical(self):
        self.verify("true<=true", [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_03_numeric(self):
        self.verify("true<=1", [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_04_string(self):
        self.verify('true<="t"', [], returncode=1)

    def test_153_lt_eq_ascii_05_logical_05_position(self):
        self.verify("true<=initialposition", [], returncode=1)

    def test_153_lt_eq_ascii_06_numeric_01_set(self):
        self.verify(
            "1<=A",
            [(3, "LE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_153_lt_eq_ascii_06_numeric_02_logical(self):
        self.verify("1<=true", [], returncode=1)

    def test_153_lt_eq_ascii_06_numeric_03_numeric(self):
        self.verify("1<=2", [(3, "LE"), (4, "Integer"), (4, "Integer")])

    def test_153_lt_eq_ascii_06_numeric_04_string(self):
        self.verify('1<="t"', [], returncode=1)

    def test_153_lt_eq_ascii_06_numeric_05_position(self):
        self.verify("1<=initialposition", [], returncode=1)

    def test_153_lt_eq_ascii_07_string_01_set(self):
        self.verify('"a"<=A', [], returncode=1)

    def test_153_lt_eq_ascii_07_string_02_logical(self):
        self.verify('"a"<=true', [], returncode=1)

    def test_153_lt_eq_ascii_07_string_03_numeric(self):
        self.verify('"a"<=1', [], returncode=1)

    def test_153_lt_eq_ascii_07_string_04_string(self):
        self.verify('"a"<="b"', [(3, "LE"), (4, "String"), (4, "String")])

    def test_153_lt_eq_ascii_07_string_05_position(self):
        self.verify("a<=initialposition", [], returncode=1)

    def test_153_lt_eq_ascii_08_position_01_set(self):
        self.verify("initialposition<=A", [], returncode=1)

    def test_153_lt_eq_ascii_08_position_02_logical(self):
        self.verify("initialposition<=true", [], returncode=1)

    def test_153_lt_eq_ascii_08_position_03_numeric(self):
        self.verify("initialposition<=1", [], returncode=1)

    def test_153_lt_eq_ascii_08_position_04_string(self):
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

    def test_154_lt_eq_utf8_04_set_01_set(self):
        self.verify("a≤A", [], returncode=1)

    def test_154_lt_eq_utf8_04_set_02_logical(self):
        self.verify("a≤true", [], returncode=1)

    def test_154_lt_eq_utf8_04_set_03_numeric(self):
        self.verify(
            "a≤1",
            [(3, "LE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_154_lt_eq_utf8_04_set_04_string(self):
        self.verify('a≤"t"', [], returncode=1)

    def test_154_lt_eq_utf8_04_set_05_position(self):
        self.verify("a≤initialposition", [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_01_set(self):
        self.verify("true≤A", [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_02_logical(self):
        self.verify("true≤true", [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_03_numeric(self):
        self.verify("true≤1", [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_04_string(self):
        self.verify('true≤"t"', [], returncode=1)

    def test_154_lt_eq_utf8_05_logical_05_position(self):
        self.verify("true≤initialposition", [], returncode=1)

    def test_154_lt_eq_utf8_06_numeric_01_set(self):
        self.verify(
            "1≤A",
            [(3, "LE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_154_lt_eq_utf8_06_numeric_02_logical(self):
        self.verify("1≤true", [], returncode=1)

    def test_154_lt_eq_utf8_06_numeric_03_numeric(self):
        self.verify("1≤2", [(3, "LE"), (4, "Integer"), (4, "Integer")])

    def test_154_lt_eq_utf8_06_numeric_04_string(self):
        self.verify('1≤"t"', [], returncode=1)

    def test_154_lt_eq_utf8_06_numeric_05_position(self):
        self.verify("1≤initialposition", [], returncode=1)

    def test_154_lt_eq_utf8_07_string_01_set(self):
        self.verify('"a"≤A', [], returncode=1)

    def test_154_lt_eq_utf8_07_string_02_logical(self):
        self.verify('"a"≤true', [], returncode=1)

    def test_154_lt_eq_utf8_07_string_03_numeric(self):
        self.verify('"a"≤1', [], returncode=1)

    def test_154_lt_eq_utf8_07_string_04_string(self):
        self.verify('"a"≤"b"', [(3, "LE"), (4, "String"), (4, "String")])

    def test_154_lt_eq_utf8_07_string_05_position(self):
        self.verify("a≤initialposition", [], returncode=1)

    def test_154_lt_eq_utf8_08_position_01_set(self):
        self.verify("initialposition≤A", [], returncode=1)

    def test_154_lt_eq_utf8_08_position_02_logical(self):
        self.verify("initialposition≤true", [], returncode=1)

    def test_154_lt_eq_utf8_08_position_03_numeric(self):
        self.verify("initialposition≤1", [], returncode=1)

    def test_154_lt_eq_utf8_08_position_04_string(self):
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

    def test_155_gt_eq_ascii_04_set_01_set(self):
        self.verify("a>=A", [], returncode=1)

    def test_155_gt_eq_ascii_04_set_02_logical(self):
        self.verify("a>=true", [], returncode=1)

    def test_155_gt_eq_ascii_04_set_03_numeric(self):
        self.verify(
            "a>=1",
            [(3, "GE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_155_gt_eq_ascii_04_set_04_string(self):
        self.verify('a>="t"', [], returncode=1)

    def test_155_gt_eq_ascii_04_set_05_position(self):
        self.verify("a>=initialposition", [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_01_set(self):
        self.verify("true>=A", [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_02_logical(self):
        self.verify("true>=true", [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_03_numeric(self):
        self.verify("true>=1", [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_04_string(self):
        self.verify('true>="t"', [], returncode=1)

    def test_155_gt_eq_ascii_05_logical_05_position(self):
        self.verify("true>=initialposition", [], returncode=1)

    def test_155_gt_eq_ascii_06_numeric_01_set(self):
        self.verify(
            "1>=A",
            [(3, "GE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_155_gt_eq_ascii_06_numeric_02_logical(self):
        self.verify("1>=true", [], returncode=1)

    def test_155_gt_eq_ascii_06_numeric_03_numeric(self):
        self.verify("1>=2", [(3, "GE"), (4, "Integer"), (4, "Integer")])

    def test_155_gt_eq_ascii_06_numeric_04_string(self):
        self.verify('1>="t"', [], returncode=1)

    def test_155_gt_eq_ascii_06_numeric_05_position(self):
        self.verify("1>=initialposition", [], returncode=1)

    def test_155_gt_eq_ascii_07_string_01_set(self):
        self.verify('"a">=A', [], returncode=1)

    def test_155_gt_eq_ascii_07_string_02_logical(self):
        self.verify('"a">=true', [], returncode=1)

    def test_155_gt_eq_ascii_07_string_03_numeric(self):
        self.verify('"a">=1', [], returncode=1)

    def test_155_gt_eq_ascii_07_string_04_string(self):
        self.verify('"a">="b"', [(3, "GE"), (4, "String"), (4, "String")])

    def test_155_gt_eq_ascii_07_string_05_position(self):
        self.verify("a>=initialposition", [], returncode=1)

    def test_155_gt_eq_ascii_08_position_01_set(self):
        self.verify("initialposition>=A", [], returncode=1)

    def test_155_gt_eq_ascii_08_position_02_logical(self):
        self.verify("initialposition>=true", [], returncode=1)

    def test_155_gt_eq_ascii_08_position_03_numeric(self):
        self.verify("initialposition>=1", [], returncode=1)

    def test_155_gt_eq_ascii_08_position_04_string(self):
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

    def test_156_gt_eq_utf8_04_set_01_set(self):
        self.verify("a≥A", [], returncode=1)

    def test_156_gt_eq_utf8_04_set_02_logical(self):
        self.verify("a≥true", [], returncode=1)

    def test_156_gt_eq_utf8_04_set_03_numeric(self):
        self.verify(
            "a≥1",
            [(3, "GE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_156_gt_eq_utf8_04_set_04_string(self):
        self.verify('a≥"t"', [], returncode=1)

    def test_156_gt_eq_utf8_04_set_05_position(self):
        self.verify("a≥initialposition", [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_01_set(self):
        self.verify("true≥A", [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_02_logical(self):
        self.verify("true≥true", [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_03_numeric(self):
        self.verify("true≥1", [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_04_string(self):
        self.verify('true≥"t"', [], returncode=1)

    def test_156_gt_eq_utf8_05_logical_05_position(self):
        self.verify("true≥initialposition", [], returncode=1)

    def test_156_gt_eq_utf8_06_numeric_01_set(self):
        self.verify(
            "1≥A",
            [(3, "GE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_156_gt_eq_utf8_06_numeric_02_logical(self):
        self.verify("1≥true", [], returncode=1)

    def test_156_gt_eq_utf8_06_numeric_03_numeric(self):
        self.verify("1≥2", [(3, "GE"), (4, "Integer"), (4, "Integer")])

    def test_156_gt_eq_utf8_06_numeric_04_string(self):
        self.verify('1≥"t"', [], returncode=1)

    def test_156_gt_eq_utf8_06_numeric_05_position(self):
        self.verify("1≥initialposition", [], returncode=1)

    def test_156_gt_eq_utf8_07_string_01_set(self):
        self.verify('"a"≥A', [], returncode=1)

    def test_156_gt_eq_utf8_07_string_02_logical(self):
        self.verify('"a"≥true', [], returncode=1)

    def test_156_gt_eq_utf8_07_string_03_numeric(self):
        self.verify('"a"≥1', [], returncode=1)

    def test_156_gt_eq_utf8_07_string_04_string(self):
        self.verify('"a"≥"b"', [(3, "GE"), (4, "String"), (4, "String")])

    def test_156_gt_eq_utf8_07_string_05_position(self):
        self.verify("a≥initialposition", [], returncode=1)

    def test_156_gt_eq_utf8_08_position_01_set(self):
        self.verify("initialposition≥A", [], returncode=1)

    def test_156_gt_eq_utf8_08_position_02_logical(self):
        self.verify("initialposition≥true", [], returncode=1)

    def test_156_gt_eq_utf8_08_position_03_numeric(self):
        self.verify("initialposition≥1", [], returncode=1)

    def test_156_gt_eq_utf8_08_position_04_string(self):
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

    def test_157_gt_04_set_01_set(self):
        self.verify("a>A", [], returncode=1)

    def test_157_gt_04_set_02_logical(self):
        self.verify("a>true", [], returncode=1)

    def test_157_gt_04_set_03_numeric(self):
        self.verify(
            "a>1",
            [(3, "GT"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_157_gt_04_set_04_string(self):
        self.verify('a>"t"', [], returncode=1)

    def test_157_gt_04_set_05_position(self):
        self.verify("a>initialposition", [], returncode=1)

    def test_157_gt_05_logical_01_set(self):
        self.verify("true>A", [], returncode=1)

    def test_157_gt_05_logical_02_logical(self):
        self.verify("true>true", [], returncode=1)

    def test_157_gt_05_logical_03_numeric(self):
        self.verify("true>1", [], returncode=1)

    def test_157_gt_05_logical_04_string(self):
        self.verify('true>"t"', [], returncode=1)

    def test_157_gt_05_logical_05_position(self):
        self.verify("true>initialposition", [], returncode=1)

    def test_157_gt_06_numeric_01_set(self):
        self.verify(
            "1>A",
            [(3, "GT"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_157_gt_06_numeric_02_logical(self):
        self.verify("1>true", [], returncode=1)

    def test_157_gt_06_numeric_03_numeric(self):
        self.verify("1>2", [(3, "GT"), (4, "Integer"), (4, "Integer")])

    def test_157_gt_06_numeric_04_string(self):
        self.verify('1>"t"', [], returncode=1)

    def test_157_gt_06_numeric_05_position(self):
        self.verify("1>initialposition", [], returncode=1)

    def test_157_gt_07_string_01_set(self):
        self.verify('"a">A', [], returncode=1)

    def test_157_gt_07_string_02_logical(self):
        self.verify('"a">true', [], returncode=1)

    def test_157_gt_07_string_03_numeric(self):
        self.verify('"a">1', [], returncode=1)

    def test_157_gt_07_string_04_string(self):
        self.verify('"a">"b"', [(3, "GT"), (4, "String"), (4, "String")])

    def test_157_gt_07_string_05_position(self):
        self.verify("a>initialposition", [], returncode=1)

    def test_157_gt_08_position_01_set(self):
        self.verify("initialposition>A", [], returncode=1)

    def test_157_gt_08_position_02_logical(self):
        self.verify("initialposition>true", [], returncode=1)

    def test_157_gt_08_position_03_numeric(self):
        self.verify("initialposition>1", [], returncode=1)

    def test_157_gt_08_position_04_string(self):
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

    def test_158_ne_ascii_04_set_01_set(self):
        self.verify(
            "a!=A",
            [(3, "NE"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_158_ne_ascii_04_set_02_logical(self):
        self.verify("a!=true", [], returncode=1)

    def test_158_ne_ascii_04_set_03_numeric(self):
        self.verify(
            "a!=1",
            [(3, "NE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_158_ne_ascii_04_set_04_string(self):
        self.verify('a!="t"', [], returncode=1)

    def test_158_ne_ascii_04_set_05_position(self):
        self.verify("a!=initialposition", [], returncode=1)

    def test_158_ne_ascii_05_logical_01_set(self):
        self.verify("true!=A", [], returncode=1)

    def test_158_ne_ascii_05_logical_02_logical(self):
        self.verify("true!=true", [], returncode=1)

    def test_158_ne_ascii_05_logical_03_numeric(self):
        self.verify("true!=1", [], returncode=1)

    def test_158_ne_ascii_05_logical_04_string(self):
        self.verify('true!="t"', [], returncode=1)

    def test_158_ne_ascii_05_logical_05_position(self):
        self.verify("true!=initialposition", [], returncode=1)

    def test_158_ne_ascii_06_numeric_01_set(self):
        self.verify(
            "1!=A",
            [(3, "NE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_158_ne_ascii_06_numeric_02_logical(self):
        self.verify("1!=true", [], returncode=1)

    def test_158_ne_ascii_06_numeric_03_numeric(self):
        self.verify("1!=2", [(3, "NE"), (4, "Integer"), (4, "Integer")])

    def test_158_ne_ascii_06_numeric_04_string(self):
        self.verify('1!="t"', [], returncode=1)

    def test_158_ne_ascii_06_numeric_05_position(self):
        self.verify("1!=initialposition", [], returncode=1)

    def test_158_ne_ascii_07_string_01_set(self):
        self.verify('"a"!=A', [], returncode=1)

    def test_158_ne_ascii_07_string_02_logical(self):
        self.verify('"a"!=true', [], returncode=1)

    def test_158_ne_ascii_07_string_03_numeric(self):
        self.verify('"a"!=1', [], returncode=1)

    def test_158_ne_ascii_07_string_04_string(self):
        self.verify('"a"!="b"', [(3, "NE"), (4, "String"), (4, "String")])

    def test_158_ne_ascii_07_string_05_position(self):
        self.verify("a!=initialposition", [], returncode=1)

    def test_158_ne_ascii_08_position_01_set(self):
        self.verify("initialposition!=A", [], returncode=1)

    def test_158_ne_ascii_08_position_02_logical(self):
        self.verify("initialposition!=true", [], returncode=1)

    def test_158_ne_ascii_08_position_03_numeric(self):
        self.verify("initialposition!=1", [], returncode=1)

    def test_158_ne_ascii_08_position_04_string(self):
        self.verify('initialposition!="t"', [], returncode=1)

    def test_158_ne_ascii_08_position_05_position(self):
        self.verify("initialposition!=currentposition", [], returncode=1)

    def test_159_ne_utf8_01(self):
        self.verify("≠", [], returncode=1)

    def test_159_ne_utf8_02(self):
        self.verify("A≠", [], returncode=1)

    def test_159_ne_utf8_03(self):
        self.verify("≠A", [], returncode=1)

    def test_159_ne_utf8_04_set_01_set(self):
        self.verify(
            "a≠A",
            [(3, "NE"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_159_ne_utf8_04_set_02_logical(self):
        self.verify("a≠true", [], returncode=1)

    def test_159_ne_utf8_04_set_03_numeric(self):
        self.verify(
            "a≠1",
            [(3, "NE"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_159_ne_utf8_04_set_04_string(self):
        self.verify('a≠"t"', [], returncode=1)

    def test_159_ne_utf8_04_set_05_position(self):
        self.verify("a≠initialposition", [], returncode=1)

    def test_159_ne_utf8_05_logical_01_set(self):
        self.verify("true≠A", [], returncode=1)

    def test_159_ne_utf8_05_logical_02_logical(self):
        self.verify("true≠true", [], returncode=1)

    def test_159_ne_utf8_05_logical_03_numeric(self):
        self.verify("true≠1", [], returncode=1)

    def test_159_ne_utf8_05_logical_04_string(self):
        self.verify('true≠"t"', [], returncode=1)

    def test_159_ne_utf8_05_logical_05_position(self):
        self.verify("true≠initialposition", [], returncode=1)

    def test_159_ne_utf8_06_numeric_01_set(self):
        self.verify(
            "1≠A",
            [(3, "NE"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_159_ne_utf8_06_numeric_02_logical(self):
        self.verify("1≠true", [], returncode=1)

    def test_159_ne_utf8_06_numeric_03_numeric(self):
        self.verify("1≠2", [(3, "NE"), (4, "Integer"), (4, "Integer")])

    def test_159_ne_utf8_06_numeric_04_string(self):
        self.verify('1≠"t"', [], returncode=1)

    def test_159_ne_utf8_06_numeric_05_position(self):
        self.verify("1≠initialposition", [], returncode=1)

    def test_159_ne_utf8_07_string_01_set(self):
        self.verify('"a"≠A', [], returncode=1)

    def test_159_ne_utf8_07_string_02_logical(self):
        self.verify('"a"≠true', [], returncode=1)

    def test_159_ne_utf8_07_string_03_numeric(self):
        self.verify('"a"≠1', [], returncode=1)

    def test_159_ne_utf8_07_string_04_string(self):
        self.verify('"a"≠"b"', [(3, "NE"), (4, "String"), (4, "String")])

    def test_159_ne_utf8_07_string_05_position(self):
        self.verify("a≠initialposition", [], returncode=1)

    def test_159_ne_utf8_08_position_01_set(self):
        self.verify("initialposition≠A", [], returncode=1)

    def test_159_ne_utf8_08_position_02_logical(self):
        self.verify("initialposition≠true", [], returncode=1)

    def test_159_ne_utf8_08_position_03_numeric(self):
        self.verify("initialposition≠1", [], returncode=1)

    def test_159_ne_utf8_08_position_04_string(self):
        self.verify('initialposition≠"t"', [], returncode=1)

    def test_159_ne_utf8_08_position_05_position(self):
        self.verify("initialposition≠currentposition", [], returncode=1)

    def test_160_ancestor_ascii_01(self):
        self.verify("[<]", [], returncode=1)

    def test_160_ancestor_ascii_02(self):
        self.verify("A[<]", [], returncode=1)

    def test_160_ancestor_ascii_03(self):
        self.verify("[<]A", [], returncode=1)

    def test_160_ancestor_ascii_04_set_01_set(self):
        self.verify("a[<]A", [], returncode=1)

    def test_160_ancestor_ascii_04_set_02_logical(self):
        self.verify("a[<]true", [], returncode=1)

    def test_160_ancestor_ascii_04_set_03_numeric(self):
        self.verify("a[<]1", [], returncode=1)

    def test_160_ancestor_ascii_04_set_04_string(self):
        self.verify('a[<]"t"', [], returncode=1)

    def test_160_ancestor_ascii_04_set_05_position(self):
        self.verify("a[<]initialposition", [], returncode=1)

    def test_160_ancestor_ascii_05_logical_01_set(self):
        self.verify("true[<]A", [], returncode=1)

    def test_160_ancestor_ascii_05_logical_02_logical(self):
        self.verify("true[<]true", [], returncode=1)

    def test_160_ancestor_ascii_05_logical_03_numeric(self):
        self.verify("true[<]1", [], returncode=1)

    def test_160_ancestor_ascii_05_logical_04_string(self):
        self.verify('true[<]"t"', [], returncode=1)

    def test_160_ancestor_ascii_05_logical_05_position(self):
        self.verify("true[<]initialposition", [], returncode=1)

    def test_160_ancestor_ascii_06_numeric_01_set(self):
        self.verify_run_fail("1[<]A")

    def test_160_ancestor_ascii_06_numeric_02_logical(self):
        self.verify("1[<]true", [], returncode=1)

    def test_160_ancestor_ascii_06_numeric_03_numeric(self):
        self.verify_run_fail("1[<]2")

    def test_160_ancestor_ascii_06_numeric_04_string(self):
        self.verify('1[<]"t"', [], returncode=1)

    def test_160_ancestor_ascii_06_numeric_05_position(self):
        self.verify("1[<]initialposition", [], returncode=1)

    def test_160_ancestor_ascii_07_string_01_set(self):
        self.verify('"a"[<]A', [], returncode=1)

    def test_160_ancestor_ascii_07_string_02_logical(self):
        self.verify('"a"[<]true', [], returncode=1)

    def test_160_ancestor_ascii_07_string_03_numeric(self):
        self.verify('"a"[<]1', [], returncode=1)

    def test_160_ancestor_ascii_07_string_04_string(self):
        self.verify_run_fail('"a"[<]"b"')

    def test_160_ancestor_ascii_07_string_05_position(self):
        self.verify("a[<]initialposition", [], returncode=1)

    def test_160_ancestor_ascii_08_position_01_set(self):
        self.verify("initialposition[<]A", [], returncode=1)

    def test_160_ancestor_ascii_08_position_02_logical(self):
        self.verify("initialposition[<]true", [], returncode=1)

    def test_160_ancestor_ascii_08_position_03_numeric(self):
        self.verify("initialposition[<]1", [], returncode=1)

    def test_160_ancestor_ascii_08_position_04_string(self):
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

    def test_161_ancestor_utf8_04_set_01_set(self):
        self.verify("a≺A", [], returncode=1)

    def test_161_ancestor_utf8_04_set_02_logical(self):
        self.verify("a≺true", [], returncode=1)

    def test_161_ancestor_utf8_04_set_03_numeric(self):
        self.verify_run_fail("a≺1")

    def test_161_ancestor_utf8_04_set_04_string(self):
        self.verify('a≺"t"', [], returncode=1)

    def test_161_ancestor_utf8_04_set_05_position(self):
        self.verify("a≺initialposition", [], returncode=1)

    def test_161_ancestor_utf8_05_logical_01_set(self):
        self.verify("true≺A", [], returncode=1)

    def test_161_ancestor_utf8_05_logical_02_logical(self):
        self.verify("true≺true", [], returncode=1)

    def test_161_ancestor_utf8_05_logical_03_numeric(self):
        self.verify("true≺1", [], returncode=1)

    def test_161_ancestor_utf8_05_logical_04_string(self):
        self.verify('true≺"t"', [], returncode=1)

    def test_161_ancestor_utf8_05_logical_05_position(self):
        self.verify("true≺initialposition", [], returncode=1)

    def test_161_ancestor_utf8_06_numeric_01_set(self):
        self.verify_run_fail("1≺A")

    def test_161_ancestor_utf8_06_numeric_02_logical(self):
        self.verify("1≺true", [], returncode=1)

    def test_161_ancestor_utf8_06_numeric_03_numeric(self):
        self.verify_run_fail("1≺2")

    def test_161_ancestor_utf8_06_numeric_04_string(self):
        self.verify('1≺"t"', [], returncode=1)

    def test_161_ancestor_utf8_06_numeric_05_position(self):
        self.verify("1≺initialposition", [], returncode=1)

    def test_161_ancestor_utf8_07_string_01_set(self):
        self.verify('"a"≺A', [], returncode=1)

    def test_161_ancestor_utf8_07_string_02_logical(self):
        self.verify('"a"≺true', [], returncode=1)

    def test_161_ancestor_utf8_07_string_03_numeric(self):
        self.verify('"a"≺1', [], returncode=1)

    def test_161_ancestor_utf8_07_string_04_string(self):
        self.verify_run_fail('"a"≺"b"')

    def test_161_ancestor_utf8_07_string_05_position(self):
        self.verify("a≺initialposition", [], returncode=1)

    def test_161_ancestor_utf8_08_position_01_set(self):
        self.verify("initialposition≺A", [], returncode=1)

    def test_161_ancestor_utf8_08_position_02_logical(self):
        self.verify("initialposition≺true", [], returncode=1)

    def test_161_ancestor_utf8_08_position_03_numeric(self):
        self.verify("initialposition≺1", [], returncode=1)

    def test_161_ancestor_utf8_08_position_04_string(self):
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

    def test_162_descendant_ascii_04_set_01_set(self):
        self.verify("a[>]A", [], returncode=1)

    def test_162_descendant_ascii_04_set_02_logical(self):
        self.verify("a[>]true", [], returncode=1)

    def test_162_descendant_ascii_04_set_03_numeric(self):
        self.verify("a[>]1", [], returncode=1)

    def test_162_descendant_ascii_04_set_04_string(self):
        self.verify('a[>]"t"', [], returncode=1)

    def test_162_descendant_ascii_04_set_05_position(self):
        self.verify("a[>]initialposition", [], returncode=1)

    def test_162_descendant_ascii_05_logical_01_set(self):
        self.verify("true[>]A", [], returncode=1)

    def test_162_descendant_ascii_05_logical_02_logical(self):
        self.verify("true[>]true", [], returncode=1)

    def test_162_descendant_ascii_05_logical_03_numeric(self):
        self.verify("true[>]1", [], returncode=1)

    def test_162_descendant_ascii_05_logical_04_string(self):
        self.verify('true[>]"t"', [], returncode=1)

    def test_162_descendant_ascii_05_logical_05_position(self):
        self.verify("true[>]initialposition", [], returncode=1)

    def test_162_descendant_ascii_06_numeric_01_set(self):
        self.verify_run_fail("1[>]A")

    def test_162_descendant_ascii_06_numeric_02_logical(self):
        self.verify("1[>]true", [], returncode=1)

    def test_162_descendant_ascii_06_numeric_03_numeric(self):
        self.verify_run_fail("1[>]2")

    def test_162_descendant_ascii_06_numeric_04_string(self):
        self.verify('1[>]"t"', [], returncode=1)

    def test_162_descendant_ascii_06_numeric_05_position(self):
        self.verify("1[>]initialposition", [], returncode=1)

    def test_162_descendant_ascii_07_string_01_set(self):
        self.verify('"a"[>]A', [], returncode=1)

    def test_162_descendant_ascii_07_string_02_logical(self):
        self.verify('"a"[>]true', [], returncode=1)

    def test_162_descendant_ascii_07_string_03_numeric(self):
        self.verify('"a"[>]1', [], returncode=1)

    def test_162_descendant_ascii_07_string_04_string(self):
        self.verify_run_fail('"a"[>]"b"')

    def test_162_descendant_ascii_07_string_05_position(self):
        self.verify("a[>]initialposition", [], returncode=1)

    def test_162_descendant_ascii_08_position_01_set(self):
        self.verify("initialposition[>]A", [], returncode=1)

    def test_162_descendant_ascii_08_position_02_logical(self):
        self.verify("initialposition[>]true", [], returncode=1)

    def test_162_descendant_ascii_08_position_03_numeric(self):
        self.verify("initialposition[>]1", [], returncode=1)

    def test_162_descendant_ascii_08_position_04_string(self):
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

    def test_163_descendant_utf8_04_set_01_set(self):
        self.verify("a≻A", [], returncode=1)

    def test_163_descendant_utf8_04_set_02_logical(self):
        self.verify("a≻true", [], returncode=1)

    def test_163_descendant_utf8_04_set_03_numeric(self):
        self.verify_run_fail("a≻1")

    def test_163_descendant_utf8_04_set_04_string(self):
        self.verify('a≻"t"', [], returncode=1)

    def test_163_descendant_utf8_04_set_05_position(self):
        self.verify("a≻initialposition", [], returncode=1)

    def test_163_descendant_utf8_05_logical_01_set(self):
        self.verify("true≻A", [], returncode=1)

    def test_163_descendant_utf8_05_logical_02_logical(self):
        self.verify("true≻true", [], returncode=1)

    def test_163_descendant_utf8_05_logical_03_numeric(self):
        self.verify("true≻1", [], returncode=1)

    def test_163_descendant_utf8_05_logical_04_string(self):
        self.verify('true≻"t"', [], returncode=1)

    def test_163_descendant_utf8_05_logical_05_position(self):
        self.verify("true≻initialposition", [], returncode=1)

    def test_163_descendant_utf8_06_numeric_01_set(self):
        self.verify_run_fail("1≻A")

    def test_163_descendant_utf8_06_numeric_02_logical(self):
        self.verify("1≻true", [], returncode=1)

    def test_163_descendant_utf8_06_numeric_03_numeric(self):
        self.verify_run_fail("1≻2")

    def test_163_descendant_utf8_06_numeric_04_string(self):
        self.verify('1≻"t"', [], returncode=1)

    def test_163_descendant_utf8_06_numeric_05_position(self):
        self.verify("1≻initialposition", [], returncode=1)

    def test_163_descendant_utf8_07_string_01_set(self):
        self.verify('"a"≻A', [], returncode=1)

    def test_163_descendant_utf8_07_string_02_logical(self):
        self.verify('"a"≻true', [], returncode=1)

    def test_163_descendant_utf8_07_string_03_numeric(self):
        self.verify('"a"≻1', [], returncode=1)

    def test_163_descendant_utf8_07_string_04_string(self):
        self.verify_run_fail('"a"≻"b"')

    def test_163_descendant_utf8_07_string_05_position(self):
        self.verify("a≻initialposition", [], returncode=1)

    def test_163_descendant_utf8_08_position_01_set(self):
        self.verify("initialposition≻A", [], returncode=1)

    def test_163_descendant_utf8_08_position_02_logical(self):
        self.verify("initialposition≻true", [], returncode=1)

    def test_163_descendant_utf8_08_position_03_numeric(self):
        self.verify("initialposition≻1", [], returncode=1)

    def test_163_descendant_utf8_08_position_04_string(self):
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

    def test_164_ancestor_eq_ascii_04_set_01_set(self):
        self.verify("a[<=]A", [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_02_logical(self):
        self.verify("a[<=]true", [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_03_numeric(self):
        self.verify("a[<=]1", [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_04_string(self):
        self.verify('a[<=]"t"', [], returncode=1)

    def test_164_ancestor_eq_ascii_04_set_05_position(self):
        self.verify("a[<=]initialposition", [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_01_set(self):
        self.verify("true[<=]A", [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_02_logical(self):
        self.verify("true[<=]true", [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_03_numeric(self):
        self.verify("true[<=]1", [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_04_string(self):
        self.verify('true[<=]"t"', [], returncode=1)

    def test_164_ancestor_eq_ascii_05_logical_05_position(self):
        self.verify("true[<=]initialposition", [], returncode=1)

    def test_164_ancestor_eq_ascii_06_numeric_01_set(self):
        self.verify_run_fail("1[<=]A")

    def test_164_ancestor_eq_ascii_06_numeric_02_logical(self):
        self.verify("1[<=]true", [], returncode=1)

    def test_164_ancestor_eq_ascii_06_numeric_03_numeric(self):
        self.verify_run_fail("1[<=]2")

    def test_164_ancestor_eq_ascii_06_numeric_04_string(self):
        self.verify('1[<=]"t"', [], returncode=1)

    def test_164_ancestor_eq_ascii_06_numeric_05_position(self):
        self.verify("1[<=]initialposition", [], returncode=1)

    def test_164_ancestor_eq_ascii_07_string_01_set(self):
        self.verify('"a"[<=]A', [], returncode=1)

    def test_164_ancestor_eq_ascii_07_string_02_logical(self):
        self.verify('"a"[<=]true', [], returncode=1)

    def test_164_ancestor_eq_ascii_07_string_03_numeric(self):
        self.verify('"a"[<=]1', [], returncode=1)

    def test_164_ancestor_eq_ascii_07_string_04_string(self):
        self.verify_run_fail('"a"[<=]"b"')

    def test_164_ancestor_eq_ascii_07_string_05_position(self):
        self.verify("a[<=]initialposition", [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_01_set(self):
        self.verify("initialposition[<=]A", [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_02_logical(self):
        self.verify("initialposition[<=]true", [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_03_numeric(self):
        self.verify("initialposition[<=]1", [], returncode=1)

    def test_164_ancestor_eq_ascii_08_position_04_string(self):
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

    def test_165_ancestor_eq_utf8_04_set_01_set(self):
        self.verify("a≼A", [], returncode=1)

    def test_165_ancestor_eq_utf8_04_set_02_logical(self):
        self.verify("a≼true", [], returncode=1)

    def test_165_ancestor_eq_utf8_04_set_03_numeric(self):
        self.verify_run_fail("a≼1")

    def test_165_ancestor_eq_utf8_04_set_04_string(self):
        self.verify('a≼"t"', [], returncode=1)

    def test_165_ancestor_eq_utf8_04_set_05_position(self):
        self.verify("a≼initialposition", [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_01_set(self):
        self.verify("true≼A", [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_02_logical(self):
        self.verify("true≼true", [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_03_numeric(self):
        self.verify("true≼1", [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_04_string(self):
        self.verify('true≼"t"', [], returncode=1)

    def test_165_ancestor_eq_utf8_05_logical_05_position(self):
        self.verify("true≼initialposition", [], returncode=1)

    def test_165_ancestor_eq_utf8_06_numeric_01_set(self):
        self.verify_run_fail("1≼A")

    def test_165_ancestor_eq_utf8_06_numeric_02_logical(self):
        self.verify("1≼true", [], returncode=1)

    def test_165_ancestor_eq_utf8_06_numeric_03_numeric(self):
        self.verify_run_fail("1≼2")

    def test_165_ancestor_eq_utf8_06_numeric_04_string(self):
        self.verify('1≼"t"', [], returncode=1)

    def test_165_ancestor_eq_utf8_06_numeric_05_position(self):
        self.verify("1≼initialposition", [], returncode=1)

    def test_165_ancestor_eq_utf8_07_string_01_set(self):
        self.verify('"a"≼A', [], returncode=1)

    def test_165_ancestor_eq_utf8_07_string_02_logical(self):
        self.verify('"a"≼true', [], returncode=1)

    def test_165_ancestor_eq_utf8_07_string_03_numeric(self):
        self.verify('"a"≼1', [], returncode=1)

    def test_165_ancestor_eq_utf8_07_string_04_string(self):
        self.verify_run_fail('"a"≼"b"')

    def test_165_ancestor_eq_utf8_07_string_05_position(self):
        self.verify("a≼initialposition", [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_01_set(self):
        self.verify("initialposition≼A", [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_02_logical(self):
        self.verify("initialposition≼true", [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_03_numeric(self):
        self.verify("initialposition≼1", [], returncode=1)

    def test_165_ancestor_eq_utf8_08_position_04_string(self):
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

    def test_166_descendant_eq_ascii_04_set_01_set(self):
        self.verify("a[>=]A", [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_02_logical(self):
        self.verify("a[>=]true", [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_03_numeric(self):  # accepts.
        self.verify("a[>=]1", [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_04_string(self):
        self.verify('a[>=]"t"', [], returncode=1)

    def test_166_descendant_eq_ascii_04_set_05_position(self):
        self.verify("a[>=]initialposition", [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_01_set(self):
        self.verify("true[>=]A", [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_02_logical(self):
        self.verify("true[>=]true", [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_03_numeric(self):
        self.verify("true[>=]1", [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_04_string(self):
        self.verify('true[>=]"t"', [], returncode=1)

    def test_166_descendant_eq_ascii_05_logical_05_position(self):
        self.verify("true[>=]initialposition", [], returncode=1)

    def test_166_descendant_eq_ascii_06_numeric_01_set(self):
        self.verify_run_fail("1[>=]A")

    def test_166_descendant_eq_ascii_06_numeric_02_logical(self):
        self.verify("1[>=]true", [], returncode=1)

    def test_166_descendant_eq_ascii_06_numeric_03_numeric(self):
        self.verify_run_fail("1[>=]2")

    def test_166_descendant_eq_ascii_06_numeric_04_string(self):
        self.verify('1[>=]"t"', [], returncode=1)

    def test_166_descendant_eq_ascii_06_numeric_05_position(self):
        self.verify("1[>=]initialposition", [], returncode=1)

    def test_166_descendant_eq_ascii_07_string_01_set(self):
        self.verify('"a"[>=]A', [], returncode=1)

    def test_166_descendant_eq_ascii_07_string_02_logical(self):
        self.verify('"a"[>=]true', [], returncode=1)

    def test_166_descendant_eq_ascii_07_string_03_numeric(self):
        self.verify('"a"[>=]1', [], returncode=1)

    def test_166_descendant_eq_ascii_07_string_04_string(self):
        self.verify_run_fail('"a"[>=]"b"')

    def test_166_descendant_eq_ascii_07_string_05_position(self):
        self.verify("a[>=]initialposition", [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_01_set(self):
        self.verify("initialposition[>=]A", [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_02_logical(self):
        self.verify("initialposition[>=]true", [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_03_numeric(self):
        self.verify("initialposition[>=]1", [], returncode=1)

    def test_166_descendant_eq_ascii_08_position_04_string(self):
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

    def test_167_descendant_eq_utf8_04_set_01_set(self):
        self.verify("a≽A", [], returncode=1)

    def test_167_descendant_eq_utf8_04_set_02_logical(self):
        self.verify("a≽true", [], returncode=1)

    def test_167_descendant_eq_utf8_04_set_03_numeric(self):
        self.verify_run_fail("a≽1")

    def test_167_descendant_eq_utf8_04_set_04_string(self):
        self.verify('a≽"t"', [], returncode=1)

    def test_167_descendant_eq_utf8_04_set_05_position(self):
        self.verify("a≽initialposition", [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_01_set(self):
        self.verify("true≽A", [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_02_logical(self):
        self.verify("true≽true", [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_03_numeric(self):
        self.verify("true≽1", [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_04_string(self):
        self.verify('true≽"t"', [], returncode=1)

    def test_167_descendant_eq_utf8_05_logical_05_position(self):
        self.verify("true≽initialposition", [], returncode=1)

    def test_167_descendant_eq_utf8_06_numeric_01_set(self):
        self.verify_run_fail("1≽A")

    def test_167_descendant_eq_utf8_06_numeric_02_logical(self):
        self.verify("1≽true", [], returncode=1)

    def test_167_descendant_eq_utf8_06_numeric_03_numeric(self):
        self.verify_run_fail("1≽2")

    def test_167_descendant_eq_utf8_06_numeric_04_string(self):
        self.verify('1≽"t"', [], returncode=1)

    def test_167_descendant_eq_utf8_06_numeric_05_position(self):
        self.verify("1≽initialposition", [], returncode=1)

    def test_167_descendant_eq_utf8_07_string_01_set(self):
        self.verify('"a"≽A', [], returncode=1)

    def test_167_descendant_eq_utf8_07_string_02_logical(self):
        self.verify('"a"≽true', [], returncode=1)

    def test_167_descendant_eq_utf8_07_string_03_numeric(self):
        self.verify('"a"≽1', [], returncode=1)

    def test_167_descendant_eq_utf8_07_string_04_string(self):
        self.verify_run_fail('"a"≽"b"')

    def test_167_descendant_eq_utf8_07_string_05_position(self):
        self.verify("a≽initialposition", [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_01_set(self):
        self.verify("initialposition≽A", [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_02_logical(self):
        self.verify("initialposition≽true", [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_03_numeric(self):
        self.verify("initialposition≽1", [], returncode=1)

    def test_167_descendant_eq_utf8_08_position_04_string(self):
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

    def test_168_eq_04_set_01_set(self):
        self.verify(
            "a==A",
            [(3, "Eq"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_168_eq_04_set_02_logical(self):
        self.verify("a==true", [], returncode=1)

    def test_168_eq_04_set_03_numeric(self):
        self.verify(
            "a==1",
            [(3, "Eq"), (4, "PieceDesignator"), (4, "Integer")],
        )

    def test_168_eq_04_set_04_string(self):
        self.verify('a=="t"', [], returncode=1)

    def test_168_eq_04_set_05_position(self):
        self.verify("a==initialposition", [], returncode=1)

    def test_168_eq_05_logical_01_set(self):
        self.verify("true==A", [], returncode=1)

    def test_168_eq_05_logical_02_logical(self):
        self.verify("true==true", [], returncode=1)

    def test_168_eq_05_logical_03_numeric(self):
        self.verify("true==1", [], returncode=1)

    def test_168_eq_05_logical_04_string(self):
        self.verify('true=="t"', [], returncode=1)

    def test_168_eq_05_logical_05_position(self):
        self.verify("true==initialposition", [], returncode=1)

    def test_168_eq_06_numeric_01_set(self):
        self.verify(
            "1==A",
            [(3, "Eq"), (4, "Integer"), (4, "PieceDesignator")],
        )

    def test_168_eq_06_numeric_02_logical(self):
        self.verify("1==true", [], returncode=1)

    def test_168_eq_06_numeric_03_numeric(self):
        self.verify("1==2", [(3, "Eq"), (4, "Integer"), (4, "Integer")])

    def test_168_eq_06_numeric_04_string(self):
        self.verify('1=="t"', [], returncode=1)

    def test_168_eq_06_numeric_05_position(self):
        self.verify("1==initialposition", [], returncode=1)

    def test_168_eq_07_string_01_set(self):
        self.verify('"a"==A', [], returncode=1)

    def test_168_eq_07_string_02_logical(self):
        self.verify('"a"==true', [], returncode=1)

    def test_168_eq_07_string_03_numeric(self):
        self.verify('"a"==1', [], returncode=1)

    def test_168_eq_07_string_04_string(self):
        self.verify('"a"=="b"', [(3, "Eq"), (4, "String"), (4, "String")])

    def test_168_eq_07_string_05_position(self):
        self.verify('"a"==initialposition', [], returncode=1)

    def test_168_eq_08_position_01_set(self):
        self.verify("initialposition==A", [], returncode=1)

    def test_168_eq_08_position_02_logical(self):
        self.verify("initialposition==true", [], returncode=1)

    def test_168_eq_08_position_03_numeric(self):
        self.verify("initialposition==1", [], returncode=1)

    def test_168_eq_08_position_04_string(self):
        self.verify('initialposition=="t"', [], returncode=1)

    def test_168_eq_08_position_05_position(self):
        self.verify(
            "initialposition==currentposition",
            [(3, "Eq"), (4, "InitialPosition"), (4, "CurrentPosition")],
        )

    def test_181_union_ascii_01(self):
        self.verify("|", [], returncode=1)

    def test_181_union_ascii_02_set_01(self):
        self.verify("k|", [], returncode=1)

    def test_181_union_ascii_02_set_02(self):
        self.verify("|K", [], returncode=1)

    def test_181_union_ascii_03_set_set_01(self):
        self.verify(
            "k|K",
            [(3, "Union"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_181_union_ascii_03_set_set_02(self):
        self.verify(
            "k | K",
            [(3, "Union"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_181_union_ascii_04_set_integer(self):
        self.verify("k|1", [], returncode=1)

    def test_181_union_ascii_05_set_string(self):
        self.verify('k|"w"', [], returncode=1)

    def test_181_union_ascii_06_set_logical(self):
        self.verify("k|false", [], returncode=1)

    def test_181_union_ascii_07_set_position(self):
        self.verify("k|currentposition", [], returncode=1)

    def test_181_union_ascii_08_integer_set(self):
        self.verify("1|K", [], returncode=1)

    def test_181_union_ascii_09_string_set(self):
        self.verify('"w"|K', [], returncode=1)

    def test_181_union_ascii_10_logical_set(self):
        self.verify("false|K", [], returncode=1)

    def test_181_union_ascii_11_position_set(self):
        self.verify("currentposition|K", [], returncode=1)

    def test_182_union_utf8_01(self):
        self.verify("∪", [], returncode=1)

    def test_182_union_utf8_02_set_01(self):
        self.verify("k∪", [], returncode=1)

    def test_182_union_utf8_02_set_02(self):
        self.verify("∪K", [], returncode=1)

    def test_182_union_utf8_03_set_set_01(self):
        self.verify(
            "k∪K",
            [(3, "Union"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_182_union_utf8_03_set_set_02(self):
        self.verify(
            "k ∪ K",
            [(3, "Union"), (4, "PieceDesignator"), (4, "PieceDesignator")],
        )

    def test_182_union_utf8_04_set_integer(self):
        self.verify("k∪1", [], returncode=1)

    def test_182_union_utf8_05_set_string(self):
        self.verify('k∪"w"', [], returncode=1)

    def test_182_union_utf8_06_set_logical(self):
        self.verify("k∪false", [], returncode=1)

    def test_182_union_utf8_07_set_position(self):
        self.verify("k∪currentposition", [], returncode=1)

    def test_182_union_utf8_08_integer_set(self):
        self.verify("1∪K", [], returncode=1)

    def test_182_union_utf8_09_string_set(self):
        self.verify('"w"∪K', [], returncode=1)

    def test_182_union_utf8_10_logical_set(self):
        self.verify("false∪K", [], returncode=1)

    def test_182_union_utf8_11_position_set(self):
        self.verify("currentposition∪K", [], returncode=1)

    def test_183_intersection_ascii_01(self):
        self.verify("&", [], returncode=1)

    def test_183_intersection_ascii_02_set_01(self):
        self.verify("k&", [], returncode=1)

    def test_183_intersection_ascii_02_set_02(self):
        self.verify("&K", [], returncode=1)

    def test_183_intersection_ascii_03_set_set_01(self):
        self.verify(
            "k&K",
            [
                (3, "Intersection"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_183_intersection_ascii_03_set_set_02(self):
        self.verify(
            "k & K",
            [
                (3, "Intersection"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_183_intersection_ascii_03_position_position_03(self):
        self.verify(
            "initialposition&currentposition",
            [
                (3, "Intersection"),
                (4, "InitialPosition"),
                (4, "CurrentPosition"),
            ],
        )

    def test_183_intersection_ascii_03_position_position_04(self):
        self.verify(
            "initialposition & currentposition",
            [
                (3, "Intersection"),
                (4, "InitialPosition"),
                (4, "CurrentPosition"),
            ],
        )

    def test_183_intersection_ascii_04_set_integer(self):
        self.verify("k&1", [], returncode=1)

    def test_183_intersection_ascii_05_set_string(self):
        self.verify('k&"w"', [], returncode=1)

    def test_183_intersection_ascii_06_set_logical(self):
        self.verify("k&false", [], returncode=1)

    def test_183_intersection_ascii_07_set_position(self):
        self.verify("k&currentposition", [], returncode=1)

    def test_183_intersection_ascii_08_integer_set(self):
        self.verify("1&K", [], returncode=1)

    def test_183_intersection_ascii_09_string_set(self):
        self.verify('"w"&K', [], returncode=1)

    def test_183_intersection_ascii_10_logical_set(self):
        self.verify("false&K", [], returncode=1)

    def test_183_intersection_ascii_11_position_set(self):
        self.verify("currentposition&K", [], returncode=1)

    def test_184_intersection_utf8_01(self):
        self.verify("∩", [], returncode=1)

    def test_184_intersection_utf8_02_set_01(self):
        self.verify("k∩", [], returncode=1)

    def test_184_intersection_utf8_02_set_02(self):
        self.verify("∩K", [], returncode=1)

    def test_184_intersection_utf8_03_set_set_01(self):
        self.verify(
            "k∩K",
            [
                (3, "Intersection"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_184_intersection_utf8_03_set_set_02(self):
        self.verify(
            "k ∩ K",
            [
                (3, "Intersection"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_184_intersection_utf8_03_position_position_03(self):
        self.verify(
            "initialposition∩currentposition",
            [
                (3, "Intersection"),
                (4, "InitialPosition"),
                (4, "CurrentPosition"),
            ],
        )

    def test_184_intersection_utf8_03_position_position_04(self):
        self.verify(
            "initialposition ∩ currentposition",
            [
                (3, "Intersection"),
                (4, "InitialPosition"),
                (4, "CurrentPosition"),
            ],
        )

    def test_184_intersection_utf8_04_set_integer(self):
        self.verify("k∩1", [], returncode=1)

    def test_184_intersection_utf8_05_set_string(self):
        self.verify('k∩"w"', [], returncode=1)

    def test_184_intersection_utf8_06_set_logical(self):
        self.verify("k∩false", [], returncode=1)

    def test_184_intersection_utf8_07_set_position(self):
        self.verify("k∩currentposition", [], returncode=1)

    def test_184_intersection_utf8_08_integer_set(self):
        self.verify("1∩K", [], returncode=1)

    def test_184_intersection_utf8_09_string_set(self):
        self.verify('"w"∩K', [], returncode=1)

    def test_184_intersection_utf8_10_logical_set(self):
        self.verify("false∩K", [], returncode=1)

    def test_184_intersection_utf8_11_position_set(self):
        self.verify("currentposition&K", [], returncode=1)

    def test_185_all_squares_01_ascii_01(self):
        self.verify(".", [(3, "AnySquare")])

    def test_185_all_squares_01_ascii_02_piece(self):
        self.verify("k.", [(3, "PieceDesignator"), (3, "AnySquare")])

    def test_185_all_squares_01_ascii_03_piece_squares(self):
        self.verify("ka-h1-8.", [(3, "PieceDesignator"), (3, "AnySquare")])

    def test_185_all_squares_01_ascii_03_missing(self):
        self.verify("ka-h1-8", [(3, "PieceDesignator")])

    def test_185_all_squares_02_utf8_01_all_squares(self):
        self.verify("▦", [(3, "AnySquare")])

    def test_185_all_squares_02_utf8_02_piece_all_squares(self):
        self.verify("k▦", [(3, "PieceDesignator"), (3, "AnySquare")])

    def test_185_all_squares_02_utf8_03_piece_squares_all_squares(self):
        self.verify("ka-h1-8▦", [(3, "PieceDesignator"), (3, "AnySquare")])

    def test_185_all_squares_02_utf8_04_piece_all_squares_squares(self):
        self.verify(
            "k▦a-h1-8",
            [
                (3, "PieceDesignator"),
                (3, "AnySquare"),
                (3, "PieceDesignator"),
            ],
        )

    def test_186_pattern_match_01(self):
        self.verify("~~", [], returncode=1)

    def test_186_pattern_match_02(self):
        self.verify('"king"~~', [], returncode=1)

    def test_186_pattern_match_02(self):
        self.verify('~~"d"', [], returncode=1)

    def test_186_pattern_match_03_01(self):
        self.verify(
            '"king"~~"d"', [(3, "RegexMatch"), (4, "String"), (4, "String")]
        )

    def test_186_pattern_match_03_02(self):
        self.verify(
            '"king" ~~ "d"', [(3, "RegexMatch"), (4, "String"), (4, "String")]
        )

    def test_186_pattern_match_04_01(self):
        self.verify(
            '"king"~~"i"', [(3, "RegexMatch"), (4, "String"), (4, "String")]
        )

    def test_186_pattern_match_04_02(self):
        self.verify(
            '"king" ~~ "i"', [(3, "RegexMatch"), (4, "String"), (4, "String")]
        )

    def test_186_pattern_match_05_set(self):
        self.verify('k~~"d"', [], returncode=1)

    def test_186_pattern_match_06_set(self):
        self.verify('"king"~~k', [], returncode=1)

    def test_186_pattern_match_07_numeric(self):
        self.verify('1~~"d"', [], returncode=1)

    def test_186_pattern_match_08_numeric(self):
        self.verify('"king"~~1', [], returncode=1)

    def test_186_pattern_match_09_logigal(self):
        self.verify('false~~"d"', [], returncode=1)

    def test_186_pattern_match_10_logical(self):
        self.verify('"king"~~false', [], returncode=1)

    def test_186_pattern_match_11_position(self):
        self.verify('currentposition~~"d"', [], returncode=1)

    def test_186_pattern_match_12_position(self):
        self.verify('"king"~~currentposition', [], returncode=1)

    def xtest_187_backslash_string_01_backslash(self):  # wrong.
        self.verify(r"\\", [])

    def xtest_187_backslash_string_02_newline(self):  # wrong.
        self.verify(r"\n", [])

    def xtest_187_backslash_string_03_quote(self):  # wrong.
        self.verify(r"\n", [])

    def xtest_187_backslash_string_04_tab(self):  # wrong.
        self.verify(r"\t", [])

    def xtest_187_backslash_string_05_return(self):  # wrong.
        self.verify(r"\r", [])

    def test_187_backslash_string_06_digit(self):
        self.verify(r"\1", [(3, "RegexCapturedGroup")])

    def test_187_backslash_string_07_index(self):
        self.verify(r"\-1", [(3, "RegexCapturedGroupIndex")])

    def test_187_backslash_string_08_other(self):
        self.verify(r"\a", [], returncode=1)

    def test_187_backslash_string_09_quoted(self):
        self.verify(r'"\a"', [(3, "String")])

    def test_188_colon_01_bare(self):
        self.verify(":", [], returncode=1)

    def test_188_colon_02_set_01(self):
        self.verify("A:", [], returncode=1)

    def test_188_colon_02_set_02(self):
        self.verify(":A", [], returncode=1)

    def test_188_colon_03_integer_01(self):
        self.verify("4:", [], returncode=1)

    def test_188_colon_03_integer_02(self):
        self.verify(":4", [], returncode=1)

    def test_188_colon_04_string_01(self):
        self.verify('"y":', [], returncode=1)

    def test_188_colon_04_string_02(self):
        self.verify(':"y"', [], returncode=1)

    def test_188_colon_05_logical_01(self):
        self.verify("true:", [], returncode=1)

    def test_188_colon_05_logical_02(self):
        self.verify(":true", [], returncode=1)

    def test_188_colon_06_position_01(self):
        self.verify("currentposition:", [], returncode=1)

    def test_188_colon_06_position_02(self):
        self.verify(":currentposition", [], returncode=1)

    def test_188_colon_07_position_01_set(self):
        self.verify(
            "currentposition:k",
            [(3, "Colon"), (4, "CurrentPosition"), (4, "PieceDesignator")],
        )

    def test_188_colon_07_position_02_integer(self):
        self.verify(
            "currentposition:3",
            [(3, "Colon"), (4, "CurrentPosition"), (4, "Integer")],
        )

    def test_188_colon_07_position_03_string(self):
        self.verify(
            'currentposition:"y"',
            [(3, "Colon"), (4, "CurrentPosition"), (4, "String")],
        )

    def test_188_colon_07_position_04_logical(self):
        self.verify(
            "currentposition:true",
            [(3, "Colon"), (4, "CurrentPosition"), (4, "True_")],
        )

    def test_188_colon_07_position_05_position(self):
        self.verify(
            "currentposition:initialposition",
            [(3, "Colon"), (4, "CurrentPosition"), (4, "InitialPosition")],
        )

    def test_189_plus_01_bare(self):
        self.verify("+", [], returncode=1)

    def test_189_plus_02_integer_01(self):
        self.verify("3+", [], returncode=1)

    def test_189_plus_02_integer_02(self):
        self.verify("+3", [], returncode=1)

    def test_189_plus_03_integer(self):
        con = self.verify("2+3", [(3, "Plus"), (4, "Integer"), (4, "Integer")])
        plus = con.children[0].children[0]
        self.assertEqual(isinstance(plus, filters.Plus), True)
        self.assertEqual(plus.filter_type is cqltypes.FilterType.NUMERIC, True)

    def test_189_plus_04_string_01(self):
        self.verify('"x"+', [], returncode=1)

    def test_189_plus_04_string_02(self):
        self.verify('+"y"', [], returncode=1)

    def test_189_plus_05_string(self):
        con = self.verify(
            '"x"+"y"', [(3, "Plus"), (4, "String"), (4, "String")]
        )
        plus = con.children[0].children[0]
        self.assertEqual(isinstance(plus, filters.Plus), True)
        self.assertEqual(plus.filter_type is cqltypes.FilterType.STRING, True)

    def test_189_plus_06_integer_string(self):
        self.verify('2+"y"', [], returncode=1)

    def test_189_plus_07_set_set(self):
        self.verify("K+Q", [], returncode=1)

    def test_189_plus_08_logical_logical(self):
        self.verify("true+false", [], returncode=1)

    def test_189_plus_09_position_position(self):
        self.verify("initialposition+currentposition", [], returncode=1)

    def test_189_plus_10_repetition(self):
        self.verify("K+", [], returncode=1)

    def test_189_plus_11_repetition_line_01(self):
        self.verify(
            "line --> K+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "PieceDesignator"),
                (5, "PlusRepeat"),
            ],
        )

    def test_189_plus_11_repetition_line_02(self):
        self.verify(
            "line --> K{+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "PieceDesignator"),
                (5, "WildcardPlus"),
            ],
        )

    def test_190_star_01_bare(self):
        self.verify("*", [], returncode=1)

    def test_190_star_02_integer_01(self):
        self.verify("3*", [], returncode=1)

    def test_190_star_02_integer_02(self):
        self.verify("*3", [], returncode=1)

    def test_190_star_03_integer(self):
        self.verify("2*3", [(3, "Star"), (4, "Integer"), (4, "Integer")])

    def test_190_star_04_string_01(self):
        self.verify('"x"*', [], returncode=1)

    def test_190_star_04_string_02(self):
        self.verify('*"y"', [], returncode=1)

    def test_190_star_04_string_03(self):
        self.verify('"x"*"y"', [], returncode=1)

    def test_190_star_05_integer_string(self):
        self.verify('2*"y"', [], returncode=1)

    def test_190_star_06_set_set(self):
        self.verify("K*Q", [], returncode=1)

    def test_190_star_07_logical_logical(self):
        self.verify("true*false", [], returncode=1)

    def test_190_star_08_position_position(self):
        self.verify("initialposition*currentposition", [], returncode=1)

    def test_190_star_09_repetition(self):
        self.verify("K*", [], returncode=1)

    def test_190_star_10_repetition_line(self):
        self.verify(
            "line --> K*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "PieceDesignator"),
                (5, "StarRepeat"),
            ],
        )

    def test_190_star_11_function_01_base(self):
        self.verify(
            "I=3 I*I",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Star"),
                (4, "Variable"),
                (4, "Variable"),
            ],
        )

    def test_190_star_11_function_02_braced_base(self):
        self.verify(
            "{I=3 I*I}",
            [
                (3, "BraceLeft"),
                (4, "Assign"),
                (5, "Variable"),
                (5, "Integer"),
                (4, "Star"),
                (5, "Variable"),
                (5, "Variable"),
            ],
        )

    def test_190_star_12_function_03_body_base(self):
        self.verify("function F(){I=3 I*I}", [(3, "Function")])

    def test_190_star_12_function_04_call_base(self):
        self.verify(
            "function F(){I=3 I*I}F()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Assign"),
                (7, "Variable"),
                (7, "Integer"),
                (6, "Star"),
                (7, "Variable"),
                (7, "Variable"),
            ],
        )

    def test_190_star_12_function_05_body_base_invalid(self):
        self.verify("function F(){I=q I*I}", [(3, "Function")])

    def test_190_star_12_function_06_call_base_invalid(self):
        self.verify("function F(){I=q I*I}F()", [], returncode=1)

    def test_191_modulus_01_bare(self):
        self.verify("%", [], returncode=1)

    def test_191_modulus_02_integer_01(self):
        self.verify("3%", [], returncode=1)

    def test_191_modulus_02_integer_02(self):
        self.verify("%3", [], returncode=1)

    def test_191_modulus_03_integer(self):
        self.verify("2%3", [(3, "Modulus"), (4, "Integer"), (4, "Integer")])

    def test_191_modulus_04_integer_01_set(self):
        self.verify("K%3", [], returncode=1)

    def test_191_modulus_04_integer_02_set(self):
        self.verify("2%K", [], returncode=1)

    def test_191_modulus_05_integer_01_string(self):
        self.verify('"v"%3', [], returncode=1)

    def test_191_modulus_05_integer_02_string(self):
        self.verify('2%"v"', [], returncode=1)

    def test_191_modulus_06_integer_01_logical(self):
        self.verify("true%3", [], returncode=1)

    def test_191_modulus_06_integer_02_logical(self):
        self.verify("2%true", [], returncode=1)

    def test_191_modulus_07_integer_01_position(self):
        self.verify("initialposition%3", [], returncode=1)

    def test_191_modulus_07_integer_02_position(self):
        self.verify("2%initialposition", [], returncode=1)

    def test_192_divide_01_bare(self):
        self.verify("/", [], returncode=1)

    def test_192_divide_02_integer_01(self):
        self.verify("3/", [], returncode=1)

    def test_192_divide_02_integer_02(self):
        self.verify("/3", [], returncode=1)

    def test_192_divide_03_integer(self):
        self.verify("2/3", [(3, "Divide"), (4, "Integer"), (4, "Integer")])

    def test_192_divide_04_integer_01_set(self):
        self.verify("K/3", [], returncode=1)

    def test_192_divide_04_integer_02_set(self):
        self.verify("2/K", [], returncode=1)

    def test_192_divide_05_integer_01_string(self):
        self.verify('"v"/3', [], returncode=1)

    def test_192_divide_05_integer_02_string(self):
        self.verify('2/"v"', [], returncode=1)

    def test_192_divide_06_integer_01_logical(self):
        self.verify("true/3", [], returncode=1)

    def test_192_divide_06_integer_02_logical(self):
        self.verify("2/true", [], returncode=1)

    def test_192_divide_07_integer_01_position(self):
        self.verify("initialposition/3", [], returncode=1)

    def test_192_divide_07_integer_02_position(self):
        self.verify("2/initialposition", [], returncode=1)

    def test_193_comment_eol_01_bare(self):
        self.verify("//", [], returncode=1)

    def test_193_comment_eol_02(self):  # wromg.
        self.verify("K//\n", [(3, "PieceDesignator")])

    def test_194_comment_symbol_01_bare(self):
        self.verify("///", [], returncode=1)

    def test_194_comment_symbol_01(self):
        self.verify("///K", [(3, "CommentSymbol"), (4, "PieceDesignator")])

    def test_195_block_comment_01_bare(self):
        self.verify("/*", [], returncode=1)

    def test_195_block_comment_02_bare(self):
        self.verify("*/", [], returncode=1)

    def test_195_block_comment_03(self):
        self.verify("/**/", [], returncode=1)

    def test_195_block_comment_04(self):
        self.verify("/**/k", [(3, "PieceDesignator")])

    def test_196_minus_01_bare(self):
        self.verify("-", [], returncode=1)

    def test_196_minus_02_integer_01(self):
        self.verify("3-", [], returncode=1)

    def test_196_minus_02_integer_02_unary(self):
        self.verify("-3", [(3, "UnaryMinus"), (4, "Integer")])

    def test_196_minus_03_integer_01(self):
        self.verify("2-3", [(3, "Minus"), (4, "Integer"), (4, "Integer")])

    def test_196_minus_03_integer_02(self):
        self.verify(
            "y=1 2-y",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Minus"),
                (4, "Integer"),
                (4, "Variable"),
            ],
        )

    def test_196_minus_04_integer_01_set(self):
        self.verify(
            "K-3",
            [(3, "PieceDesignator"), (3, "UnaryMinus"), (4, "Integer")],
        )

    def test_196_minus_04_integer_02_set(self):
        self.verify("2-K", [], returncode=1)

    def test_196_minus_05_integer_01_string(self):
        self.verify(
            '"v"-3',
            [(3, "String"), (3, "UnaryMinus"), (4, "Integer")],
        )

    def test_196_minus_05_integer_02_string(self):
        self.verify('2-"v"', [], returncode=1)

    def test_196_minus_06_integer_01_logical(self):
        self.verify(
            "true-2",
            [(3, "True_"), (3, "UnaryMinus"), (4, "Integer")],
        )

    def test_196_minus_06_integer_02_logical(self):
        self.verify("2-true", [], returncode=1)

    def test_196_minus_07_integer_01_position(self):
        self.verify(
            "initialposition-3",
            [(3, "InitialPosition"), (3, "UnaryMinus"), (4, "Integer")],
        )

    def test_196_minus_07_integer_02_position(self):
        self.verify("2-initialposition", [], returncode=1)

    def test_196_minus_08_parenthesized_piecedesignator_integer(self):
        self.verify("(q-2)", [], returncode=1)

    def test_196_minus_09_parenthesized_rank_integer(self):
        self.verify(
            "(rank q-2)",
            [
                (3, "ParenthesisLeft"),
                (4, "Minus"),
                (5, "Rank"),
                (6, "PieceDesignator"),
                (5, "Integer"),
            ],
        )

    def test_196_minus_10_parenthesized_unary(self):
        self.verify(
            "(-2)",
            [
                (3, "ParenthesisLeft"),
                (4, "UnaryMinus"),
                (5, "Integer"),
            ],
        )

    def test_196_minus_11_braced_piecedesignator_integer(self):
        self.verify(
            "{q-2}",
            [
                (3, "BraceLeft"),
                (4, "PieceDesignator"),
                (4, "UnaryMinus"),
                (5, "Integer"),
            ],
        )

    def test_196_minus_12_braced_rank_integer(self):
        self.verify(
            "{rank q-2}",
            [
                (3, "BraceLeft"),
                (4, "Minus"),
                (5, "Rank"),
                (6, "PieceDesignator"),
                (5, "Integer"),
            ],
        )

    def test_196_minus_13_braced_unary(self):
        self.verify(
            "{-2}",
            [
                (3, "BraceLeft"),
                (4, "UnaryMinus"),
                (5, "Integer"),
            ],
        )

    def test_196_minus_14_unary_non_integer_01_set(self):
        self.verify("-to", [], returncode=1)

    def test_196_minus_14_unary_non_integer_02_piecedesignator(self):
        self.verify("-qa5", [], returncode=1)

    def test_196_minus_14_unary_non_integer_03_string(self):
        self.verify('-"v"', [], returncode=1)

    def test_196_minus_14_unary_non_integer_04_logical(self):
        self.verify("-true", [], returncode=1)

    def test_196_minus_14_unary_non_integer_05_position(self):
        self.verify("-currentposition", [], returncode=1)

    def test_196_minus_15_unary_compare_01_equal_integer(self):
        self.verify(
            "2==-1",
            [(3, "Eq"), (4, "Integer"), (4, "UnaryMinus"), (5, "Integer")],
        )

    def test_196_minus_15_unary_compare_02_equal_colortype(self):
        self.verify(
            "2==-colortype a5",
            [
                (3, "Eq"),
                (4, "Integer"),
                (4, "UnaryMinus"),
                (5, "ColorType"),
                (6, "PieceDesignator"),
            ],
        )

    def test_197_complement_01_bare(self):
        self.verify("~", [], returncode=1)

    def test_197_complement_02_set(self):
        self.verify("k~", [], returncode=1)

    def test_197_complement_03_set(self):
        self.verify("~k", [(3, "Complement"), (4, "PieceDesignator")])

    def test_197_complement_04_integer(self):
        self.verify("~3", [], returncode=1)

    def test_197_complement_05_string(self):
        self.verify('~"y"', [], returncode=1)

    def test_197_complement_06_logical(self):
        self.verify("~true", [], returncode=1)

    def test_197_complement_07_position(self):
        self.verify("~currentposition", [], returncode=1)

    def test_198_compound_01_bare_01(self):
        self.verify("{", [], returncode=1)

    def test_198_compound_01_bare_02(self):
        self.verify("}", [], returncode=1)

    def test_198_compound_02_empty(self):
        self.verify("{}", [], returncode=1)

    def test_198_compound_03(self):
        self.verify("{k}", [(3, "BraceLeft"), (4, "PieceDesignator")])

    def test_199_assign_01_bare(self):
        self.verify("=", [], returncode=1)

    def test_199_assign_02_name(self):
        self.verify("y=", [], returncode=1)

    def test_199_assign_03_set_01_set_variable(self):
        self.verify_assign(
            "y=k",
            [(3, "Assign"), (4, "Variable"), (4, "PieceDesignator")],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_03_set_02_piece_variable(self):
        self.verify_assign(
            "piece y=k",
            [(3, "Assign"), (4, "PieceVariable"), (4, "PieceDesignator")],
            "y",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_04_integer(self):
        self.verify_assign(
            "y=3",
            [(3, "Assign"), (4, "Variable"), (4, "Integer")],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_199_assign_05_string(self):
        self.verify_assign(
            'y="str"',
            [(3, "Assign"), (4, "Variable"), (4, "String")],
            "y",
            cqltypes.VariableType.STRING,
            cqltypes.FilterType.STRING,
        )

    def test_199_assign_06_logical(self):
        self.verify("y=true", [], returncode=1)

    def test_199_assign_07_position(self):
        self.verify_assign(
            "y=currentposition",
            [(3, "Assign"), (4, "Variable"), (4, "CurrentPosition")],
            "y",
            cqltypes.VariableType.POSITION,
            cqltypes.FilterType.POSITION,
        )

    def test_199_assign_08_function_set_01_set_variable(self):
        self.verify_assign(
            "function x(){k} y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_08_function_set_02_piece_variable(self):
        self.verify_assign(
            "function x(){k} piece y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_09_function_integer_01(self):
        self.verify_assign(
            "function x(){(7)} y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "ParenthesisLeft"),
                (8, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_199_assign_09_function_integer_02(self):
        self.verify_assign(
            "function x(){k 7} y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "PieceDesignator"),
                (7, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_199_assign_10_function_string(self):
        self.verify_assign(
            'function x(){"a"} y=x()',
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "String"),
            ],
            "y",
            cqltypes.VariableType.STRING,
            cqltypes.FilterType.STRING,
        )

    def test_199_assign_11_function_logical(self):
        self.verify("function x(){true} y=x()", [], returncode=1)

    def test_199_assign_12_function_position(self):
        self.verify_assign(
            "function x(){currentposition} y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "CurrentPosition"),
            ],
            "y",
            cqltypes.VariableType.POSITION,
            cqltypes.FilterType.POSITION,
        )

    def test_199_assign_13_set_01_integer(self):
        self.verify("y=k y=7", [], returncode=1)

    def test_199_assign_13_set_02_string(self):
        self.verify('y=k y="a"', [], returncode=1)

    def test_199_assign_13_set_03_position(self):
        self.verify("y=k y=currentposition", [], returncode=1)

    def test_199_assign_13_set_04_piece(self):
        self.verify("y=k piece y=q", [], returncode=1)

    def test_199_assign_13_set_05_piece(self):
        self.verify_assign(
            "y=k piece x=y",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "Variable"),
            ],
            "x",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_13_set_06_piece(self):
        self.verify_assign(
            "piece x=q y=k piece x=y",
            [
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "Variable"),
            ],
            "x",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_13_set_07_piece(self):
        self.verify_assign(
            "piece x=q piece y=k piece y=x",
            [
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceVariable"),
            ],
            "y",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_13_set_08_piece(self):
        self.verify("piece x=q piece y=k y=x", [], returncode=1)

    def test_199_assign_14_integer_01_set(self):
        self.verify("y=7 y=k", [], returncode=1)

    def test_199_assign_14_integer_02_string(self):
        self.verify('y=7 y="a"', [], returncode=1)

    def test_199_assign_14_integer_03_position(self):
        self.verify("y=7 y=currentposition", [], returncode=1)

    def test_199_assign_14_integer_04_piece(self):
        self.verify("y=7 piece y=q", [], returncode=1)

    def test_199_assign_15_string_01_set(self):
        self.verify('y="a" y=k', [], returncode=1)

    def test_199_assign_15_string_02_integer(self):
        self.verify('y="a" y=7', [], returncode=1)

    def test_199_assign_15_string_03_position(self):
        self.verify('y="a" y=currentposition', [], returncode=1)

    def test_199_assign_15_string_04_piece(self):
        self.verify('y="a" piece y=q', [], returncode=1)

    def test_199_assign_16_position_01_set(self):
        self.verify("y=currentposition y=k", [], returncode=1)

    def test_199_assign_16_position_02_integer(self):
        self.verify("y=currentposition y=7", [], returncode=1)

    def test_199_assign_16_position_03_string(self):
        self.verify('y=currentposition y="a"', [], returncode=1)

    def test_199_assign_16_position_04_piece(self):
        self.verify("y=currentposition piece y=q", [], returncode=1)

    def test_199_assign_17_piece_01_set(self):
        self.verify("piece y=q y=k", [], returncode=1)

    def test_199_assign_17_piece_02_integer(self):
        self.verify("piece y=q y=7", [], returncode=1)

    def test_199_assign_17_piece_03_string(self):
        self.verify('piece y=q y="a"', [], returncode=1)

    def test_199_assign_17_piece_04_position(self):
        self.verify("piece y=q y=currentposition", [], returncode=1)

    def test_199_assign_17_piece_05_piece(self):
        self.verify_assign(
            "piece y=q piece y=q",
            [
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_18_variable_01_variable(self):
        self.verify("y=x", [], returncode=1)

    def test_199_assign_18_variable_02_piece_variable(self):
        self.verify("piece y=x", [], returncode=1)

    def test_199_assign_19_name_integer(self):
        self.verify("y[3]", [], returncode=1)

    def test_199_assign_20_name_integer_assign(self):
        self.verify("y[3]=", [], returncode=1)

    def test_199_assign_21_name_integer_integer(self):
        self.verify("y[3]=4", [], returncode=1)

    def test_199_assign_22_name_integer_string(self):
        self.verify('y[3]="a"', [], returncode=1)

    def test_199_assign_23_name_integer_piecedesignator(self):
        self.verify("y[3]=r", [], returncode=1)

    def test_199_assign_24_name_integer_other_set(self):
        self.verify("y[3]=from", [], returncode=1)

    def test_199_assign_25_name_integer_position(self):
        self.verify("y[3]=currentposition", [], returncode=1)

    def test_199_assign_26_name_integer_logical(self):
        self.verify("y[3]=true", [], returncode=1)

    def test_199_assign_27_name_string_integer(self):
        self.verify('y["here"]=4', [], returncode=1)

    def test_199_assign_28_name_string_string(self):
        self.verify('y["here"]="a"', [], returncode=1)

    def test_199_assign_29_name_string_piecedesignator(self):
        self.verify('y["here"]=r', [], returncode=1)

    def test_199_assign_30_name_string_other_set(self):
        self.verify('y["here"]=from', [], returncode=1)

    def test_199_assign_31_name_string_position(self):
        self.verify('y["here"]=currentposition', [], returncode=1)

    def test_199_assign_32_name_string_logical(self):
        self.verify('y["here"]=true', [], returncode=1)

    def test_199_assign_33_name_bad_piecedesignator_integer(self):
        self.verify("y[rc4]=4", [], returncode=1)

    def test_199_assign_34_name_bad_piecedesignator_string(self):
        self.verify('y[rc4]="a"', [], returncode=1)

    def test_199_assign_35_name_bad_piecedesignator_piecedesignator(self):
        self.verify("y[rc4]=r", [], returncode=1)

    def test_199_assign_36_name_bad_piecedesignator_other_set(self):
        self.verify("y[rc4]=from", [], returncode=1)

    def test_199_assign_37_name_bad_piecedesignator_position(self):
        self.verify("y[rc4]=currentposition", [], returncode=1)

    def test_199_assign_38_name_bad_piecedesignator_logical(self):
        self.verify("y[rc4]=true", [], returncode=1)

    def test_199_assign_39_name_piecedesignator_integer(self):
        self.verify("y[ rc4 ]=4", [], returncode=1)

    def test_199_assign_40_name_piecedesignator_string(self):
        self.verify('y[ rc4 ]="a"', [], returncode=1)

    def test_199_assign_41_name_piecedesignator_piecedesignator(self):
        self.verify("y[ rc4 ]=r", [], returncode=1)

    def test_199_assign_42_name_piecedesignator_other_set(self):
        self.verify("y[ rc4 ]=from", [], returncode=1)

    def test_199_assign_43_name_piecedesignator_position(self):
        self.verify("y[ rc4 ]=currentposition", [], returncode=1)

    def test_199_assign_44_name_piecedesignator_logical(self):
        self.verify("y[ rc4 ]=true", [], returncode=1)

    def test_199_assign_45_name_position_integer(self):
        self.verify("y[currentposition]=4", [], returncode=1)

    def test_199_assign_46_name_position_string(self):
        self.verify('y[currentposition]="a"', [], returncode=1)

    def test_199_assign_47_name_position_piecedesignator(self):
        self.verify("y[currentposition]=r", [], returncode=1)

    def test_199_assign_48_name_position_other_set(self):
        self.verify("y[currentposition]=from", [], returncode=1)

    def test_199_assign_49_name_position_position(self):
        self.verify("y[currentposition]=currentposition", [], returncode=1)

    def test_199_assign_50_name_position_logical(self):
        self.verify("y[currentposition]=true", [], returncode=1)

    def test_199_assign_51_name_logical_integer(self):
        self.verify("y[false]=4", [], returncode=1)

    def test_199_assign_52_name_logical_string(self):
        self.verify('y[false]="a"', [], returncode=1)

    def test_199_assign_53_name_logical_piecedesignator(self):
        self.verify("y[false]=r", [], returncode=1)

    def test_199_assign_54_name_logical_other_set(self):
        self.verify("y[false]=from", [], returncode=1)

    def test_199_assign_55_name_logical_position(self):
        self.verify("y[false]=currentposition", [], returncode=1)

    def test_199_assign_56_name_logical_logical(self):
        self.verify("y[false]=true", [], returncode=1)

    def test_200_assignif_01_bare(self):
        self.verify("=?", [], returncode=1)

    def test_200_assignif_02_name(self):
        self.verify("y=?", [], returncode=1)

    def test_200_assignif_03_set(self):
        self.verify_assign(
            "y=?k",
            [(3, "AssignIf"), (4, "Variable"), (4, "PieceDesignator")],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_200_assignif_04_piece(self):
        self.verify("piece y=?3", [], returncode=1)

    def test_200_assignif_05_integer(self):
        self.verify("y=?3", [], returncode=1)

    def test_200_assignif_06_string(self):
        self.verify('y=?"str"', [], returncode=1)

    def test_200_assignif_07_logical(self):
        self.verify("y=?true", [], returncode=1)

    def test_200_assignif_08_position(self):
        self.verify("y=?currentposition", [], returncode=1)

    def test_200_assignif_09_function_set(self):
        self.verify_assign(
            "function x(){k} y=?x()",
            [
                (3, "Function"),
                (3, "AssignIf"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_200_assignif_10_function_piece(self):
        self.verify("function x(){k} piece y=?x()", [], returncode=1)

    def test_200_assignif_11_function_integer_01(self):
        self.verify("function x(){(7)} y=?x()", [], returncode=1)

    def test_200_assignif_11_function_integer_02(self):
        self.verify("function x(){k 7} y=?x()", [], returncode=1)

    def test_200_assignif_12_function_string(self):
        self.verify('function x(){"a"} y=?x()', [], returncode=1)

    def test_200_assignif_13_function_logical(self):
        self.verify("function x(){true} y=?x()", [], returncode=1)

    def test_200_assignif_14_function_position(self):
        self.verify("function x(){currentposition} y=?x()", [], returncode=1)

    def test_200_assignif_15_set_01_set(self):
        self.verify_assign(
            "y=k y=?q",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "PieceDesignator"),
                (3, "AssignIf"),
                (4, "Variable"),
                (4, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_200_assignif_15_set_02_piece(self):
        self.verify("piece y=k y=?q", [], returncode=1)

    def test_200_assignif_15_set_03_integer(self):
        self.verify("y=7 y=?q", [], returncode=1)

    def test_200_assignif_15_set_04_string(self):
        self.verify('y="a" y=?q', [], returncode=1)

    def test_200_assignif_15_set_05_position(self):
        self.verify("y=currentposition y=?q", [], returncode=1)

    def test_201_count_01_bare(self):
        self.verify("#", [], returncode=1)

    def test_201_count_02_set(self):
        self.verify("#k", [(3, "CountFilter"), (4, "PieceDesignator")])

    def test_201_count_03_integer(self):
        self.verify("#3", [], returncode=1)

    def test_201_count_04_string(self):
        self.verify('#"str"', [(3, "CountFilter"), (4, "String")])

    def test_201_count_05_logical(self):
        self.verify("#false", [], returncode=1)

    def test_201_count_06_position(self):
        self.verify("#currentposition", [], returncode=1)

    def test_202_assign_plus_01_bare_01(self):
        self.verify("+=", [], returncode=1)

    def test_202_assign_plus_01_bare_02(self):
        self.verify("y=k +=", [], returncode=1)

    def test_202_assign_plus_01_bare_03(self):
        self.verify("y=k y+=", [], returncode=1)

    def test_202_assign_plus_02_undefined_01_set(self):
        self.verify("y+=k", [], returncode=1)

    def test_202_assign_plus_02_undefined_02_integer(self):
        self.verify("y+=7", [], returncode=1)

    def test_202_assign_plus_02_undefined_03_string(self):
        self.verify('y+="a"', [], returncode=1)

    def test_202_assign_plus_02_undefined_04_logical(self):
        self.verify("y+=true", [], returncode=1)

    def test_202_assign_plus_02_undefined_05_position(self):
        self.verify("y+=currentposition", [], returncode=1)

    def test_202_assign_plus_03_set(self):
        self.verify("y=k y+=q", [], returncode=1)

    def test_202_assign_plus_04_integer(self):
        self.verify_assign(
            "y=3 y+=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignPlus"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_202_assign_plus_05_string(self):
        self.verify_assign(
            'y="3" y+="4"',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "AssignPlus"),
                (4, "Variable"),
                (4, "String"),
            ],
            "y",
            cqltypes.VariableType.STRING,
            cqltypes.FilterType.STRING,
        )

    def test_202_assign_plus_06_logical(self):
        self.verify("y=true y+=false", [], returncode=1)

    def test_202_assign_plus_07_position(self):
        self.verify("y=initialposition y+=currentposition", [], returncode=1)

    def test_203_assign_minus_01_bare_01(self):
        self.verify("-=", [], returncode=1)

    def test_203_assign_minus_01_bare_02(self):
        self.verify("y=k -=", [], returncode=1)

    def test_203_assign_minus_01_bare_03(self):
        self.verify("y=k y-=", [], returncode=1)

    def test_203_assign_minus_02_undefined_01_set(self):
        self.verify("y-=k", [], returncode=1)

    def test_203_assign_minus_02_undefined_02_integer(self):
        self.verify("y-=7", [], returncode=1)

    def test_203_assign_minus_02_undefined_03_string(self):
        self.verify('y-="a"', [], returncode=1)

    def test_203_assign_minus_02_undefined_04_logical(self):
        self.verify("y-=true", [], returncode=1)

    def test_203_assign_minus_02_undefined_05_position(self):
        self.verify("y-=currentposition", [], returncode=1)

    def test_203_assign_minus_03_set(self):
        self.verify("y=k y-=q", [], returncode=1)

    def test_203_assign_minus_04_integer(self):
        self.verify_assign(
            "y=3 y-=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignMinus"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_203_assign_minus_05_string(self):
        self.verify('y="3" y-="4"', [], returncode=1)

    def test_203_assign_minus_06_logical(self):
        self.verify("y=true y-=false", [], returncode=1)

    def test_203_assign_minus_07_position(self):
        self.verify("y=initialposition y-=currentposition", [], returncode=1)

    def test_204_assign_divide_01_bare_01(self):
        self.verify("/=", [], returncode=1)

    def test_204_assign_divide_01_bare_02(self):
        self.verify("y=k /=", [], returncode=1)

    def test_204_assign_divide_01_bare_03(self):
        self.verify("y=k y/=", [], returncode=1)

    def test_204_assign_divide_02_undefined_01_set(self):
        self.verify("y/=k", [], returncode=1)

    def test_204_assign_divide_02_undefined_02_integer(self):
        self.verify("y/=7", [], returncode=1)

    def test_204_assign_divide_02_undefined_03_string(self):
        self.verify('y/="a"', [], returncode=1)

    def test_204_assign_divide_02_undefined_04_logical(self):
        self.verify("y/=true", [], returncode=1)

    def test_204_assign_divide_02_undefined_05_position(self):
        self.verify("y/=currentposition", [], returncode=1)

    def test_204_assign_divide_03_set(self):
        self.verify("y=k y/=q", [], returncode=1)

    def test_204_assign_divide_04_integer(self):
        self.verify_assign(
            "y=3 y/=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignDivide"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_204_assign_divide_05_string(self):
        self.verify('y="3" y/="4"', [], returncode=1)

    def test_204_assign_divide_06_logical(self):
        self.verify("y=true y/=false", [], returncode=1)

    def test_204_assign_divide_07_position(self):
        self.verify("y=initialposition y/=currentposition", [], returncode=1)

    def test_205_assign_multiply_01_bare_01(self):
        self.verify("*=", [], returncode=1)

    def test_205_assign_multiply_01_bare_02(self):
        self.verify("y=k *=", [], returncode=1)

    def test_205_assign_multiply_01_bare_03(self):
        self.verify("y=k y*=", [], returncode=1)

    def test_205_assign_multiply_02_undefined_01_set(self):
        self.verify("y*=k", [], returncode=1)

    def test_205_assign_multiply_02_undefined_02_integer(self):
        self.verify("y*=7", [], returncode=1)

    def test_205_assign_multiply_02_undefined_03_string(self):
        self.verify('y*="a"', [], returncode=1)

    def test_205_assign_multiply_02_undefined_04_logical(self):
        self.verify("y*=true", [], returncode=1)

    def test_205_assign_multiply_02_undefined_05_position(self):
        self.verify("y*=currentposition", [], returncode=1)

    def test_205_assign_multiply_03_set(self):
        self.verify("y=k y*=q", [], returncode=1)

    def test_205_assign_multiply_04_integer(self):
        self.verify_assign(
            "y=3 y*=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignMultiply"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_205_assign_multiply_05_string(self):
        self.verify('y="3" y*="4"', [], returncode=1)

    def test_205_assign_multiply_06_logical(self):
        self.verify("y=true y*=false", [], returncode=1)

    def test_205_assign_multiply_07_position(self):
        self.verify("y=initialposition y*=currentposition", [], returncode=1)

    def test_206_assign_modulus_01_bare_01(self):
        self.verify("%=", [], returncode=1)

    def test_206_assign_modulus_01_bare_02(self):
        self.verify("y=k %=", [], returncode=1)

    def test_206_assign_modulus_01_bare_03(self):
        self.verify("y=k y%=", [], returncode=1)

    def test_206_assign_modulus_02_undefined_01_set(self):
        self.verify("y%=k", [], returncode=1)

    def test_206_assign_modulus_02_undefined_02_integer(self):
        self.verify("y%=7", [], returncode=1)

    def test_206_assign_modulus_02_undefined_03_string(self):
        self.verify('y%="a"', [], returncode=1)

    def test_206_assign_modulus_02_undefined_04_logical(self):
        self.verify("y%=true", [], returncode=1)

    def test_206_assign_modulus_02_undefined_05_position(self):
        self.verify("y%=currentposition", [], returncode=1)

    def test_206_assign_modulus_03_set(self):
        self.verify("y=k y%=q", [], returncode=1)

    def test_206_assign_modulus_04_integer(self):
        self.verify_assign(
            "y=3 y%=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignModulus"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_206_assign_modulus_05_string(self):
        self.verify('y="3" y%="4"', [], returncode=1)

    def test_206_assign_modulus_06_logical(self):
        self.verify("y=true y%=false", [], returncode=1)

    def test_206_assign_modulus_07_position(self):
        self.verify("y=initialposition y%=currentposition", [], returncode=1)

    def test_207_brackets_01_bare_01(self):
        self.verify("[", [], returncode=1)

    def test_207_brackets_01_bare_02(self):
        self.verify("]", [], returncode=1)

    def test_207_brackets_02_empty(self):
        self.verify("[]", [(3, "EmptySquares")])

    def test_207_brackets_03_assign_empty(self):
        self.verify(
            "y=[]", [(3, "Assign"), (4, "Variable"), (4, "EmptySquares")]
        )

    def test_207_brackets_04_index(self):
        self.verify(
            '"mate"[3]', [(3, "BracketLeft"), (4, "String"), (4, "Integer")]
        )

    def test_207_brackets_05_range(self):
        self.verify(
            '"mate"[1:2]',
            [
                (3, "BracketLeft"),
                (4, "String"),
                (4, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_208_white(self):  # Original name 'test_144_white' is confusing.
        self.verify("wtm", [(3, "WTM")])

    def test_209_pseudolegal_01(self):  # Original name 'test_062_' confusing.
        self.verify("pseudolegal", [], returncode=1)

    def test_209_pseudolegal_02(self):  # Original name 'test_062_' confusing.
        self.verify("pseudolegal k", [], returncode=1)

    def test_209_pseudolegal_03_move(self):  # Original 'test_062_' confusing.
        self.verify(
            "pseudolegal --",
            [
                (3, "Pseudolegal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_209_pseudolegal_04_capture(self):  # Original '_062_' confusing.
        self.verify("pseudolegal [x]", [], returncode=1)

    def test_210_light_01(self):  # Original name 'test_061_' confusing.
        self.verify("light", [], returncode=1)

    def test_210_light_02(self):  # Original name 'test_061_' confusing.
        self.verify(
            "light P",
            [
                (3, "Light"),
                (4, "PieceDesignator"),
            ],
        )

    def test_211_persistent_assign_01_plus_01_bare(self):
        self.verify("persistent y+=", [], returncode=1)

    def test_211_persistent_assign_01_plus_02_integer(self):
        self.verify(
            "persistent y+=2",
            [(3, "AssignPlus"), (4, "Persistent"), (4, "Integer")],
        )

    def test_211_persistent_assign_01_plus_03_move_count(self):
        self.verify(
            "persistent y+=move from . count legal",
            [
                (3, "AssignPlus"),
                (4, "Persistent"),
                (4, "Move"),
                (5, "FromParameter"),
                (6, "AnySquare"),
                (5, "Count"),
                (5, "LegalParameter"),
            ],
        )

    def test_211_persistent_assign_01_plus_04_string(self):
        self.verify(
            'persistent y+="a"',
            [(3, "AssignPlus"), (4, "Persistent"), (4, "String")],
        )

    def test_211_persistent_assign_02_star_01_bare(self):
        self.verify("persistent y*=", [], returncode=1)

    def test_211_persistent_assign_02_star_02_integer(self):
        self.verify(
            "persistent y*=2",
            [(3, "AssignMultiply"), (4, "Persistent"), (4, "Integer")],
        )

    def test_211_persistent_assign_02_star_03_move_count(self):
        self.verify(
            "persistent y*=move from . count legal",
            [
                (3, "AssignMultiply"),
                (4, "Persistent"),
                (4, "Move"),
                (5, "FromParameter"),
                (6, "AnySquare"),
                (5, "Count"),
                (5, "LegalParameter"),
            ],
        )

    def test_211_persistent_assign_02_star_04_string(self):
        self.verify('persistent y*="a"', [], returncode=1)

    def test_211_persistent_assign_03_divide_01_bare(self):
        self.verify("persistent y/=", [], returncode=1)

    def test_211_persistent_assign_03_divide_02_integer(self):
        self.verify(
            "persistent y/=2",
            [(3, "AssignDivide"), (4, "Persistent"), (4, "Integer")],
        )

    def test_211_persistent_assign_03_divide_03_move_count(self):
        self.verify(
            "persistent y/=move from . count legal",
            [
                (3, "AssignDivide"),
                (4, "Persistent"),
                (4, "Move"),
                (5, "FromParameter"),
                (6, "AnySquare"),
                (5, "Count"),
                (5, "LegalParameter"),
            ],
        )

    def test_211_persistent_assign_03_divide_04_string(self):
        self.verify('persistent y/="a"', [], returncode=1)

    def test_211_persistent_assign_04_minus_01_bare(self):
        self.verify("persistent y-=", [], returncode=1)

    def test_211_persistent_assign_04_minus_02_integer(self):
        self.verify(
            "persistent y-=2",
            [(3, "AssignMinus"), (4, "Persistent"), (4, "Integer")],
        )

    def test_211_persistent_assign_04_minus_03_move_count(self):
        self.verify(
            "persistent y-=move from . count legal",
            [
                (3, "AssignMinus"),
                (4, "Persistent"),
                (4, "Move"),
                (5, "FromParameter"),
                (6, "AnySquare"),
                (5, "Count"),
                (5, "LegalParameter"),
            ],
        )

    def test_211_persistent_assign_04_minus_04_string(self):
        self.verify('persistent y-="a"', [], returncode=1)

    def test_211_persistent_assign_05_modulus_01_bare(self):
        self.verify("persistent y%=", [], returncode=1)

    def test_211_persistent_assign_05_modulus_02_integer(self):
        self.verify(
            "persistent y%=2",
            [(3, "AssignModulus"), (4, "Persistent"), (4, "Integer")],
        )

    def test_211_persistent_assign_05_modulus_03_move_count(self):
        self.verify(
            "persistent y%=move from . count legal",
            [
                (3, "AssignModulus"),
                (4, "Persistent"),
                (4, "Move"),
                (5, "FromParameter"),
                (6, "AnySquare"),
                (5, "Count"),
                (5, "LegalParameter"),
            ],
        )

    def test_211_persistent_assign_05_modulus_04_string(self):
        self.verify('persistent y%="a"', [], returncode=1)

    def test_212_hhdb_01_not_implemented_yet(self):
        self.verify("hddb", [], returncode=1)

    def test_213_compare_lhs_filter_type_01_ASCII_01_numeric(self):
        self.verify(
            'ascii 4=="a"',
            [
                (3, "Eq"),
                (4, "ASCII"),
                (5, "Integer"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_01_ASCII_02_string(self):
        self.verify(
            'ascii "a"==3',
            [
                (3, "Eq"),
                (4, "ASCII"),
                (5, "String"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_02_element_01_set(self):
        self.verify(
            "x∊._==3",
            [
                (3, "ExistentialSquareIterator"),
                (4, "Element"),
                (5, "ExistentialSquareVariable"),
                (5, "AnySquare"),
                (4, "Eq"),
                (5, "PieceDesignator"),
                (5, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_03_sort_01_numeric_01(self):
        self.verify(
            "sort 3==4",
            [
                (3, "Sort"),
                (4, "Eq"),
                (5, "Integer"),
                (5, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_03_sort_01_numeric_02(self):
        self.verify(
            'sort "e" 3==4',
            [
                (3, "Sort"),
                (4, "Documentation"),
                (4, "Eq"),
                (5, "Integer"),
                (5, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_03_sort_02_string_01(self):
        self.verify(
            'sort player=="w"',
            [
                (3, "Sort"),
                (4, "Eq"),
                (5, "Player"),
                (5, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_03_sort_02_string_02(self):
        self.verify('sort "e"=="w"', [], returncode=1)

    def test_213_compare_lhs_filter_type_03_sort_02_string_03(self):
        self.verify(
            'sort "e" "f"=="w"',
            [
                (3, "Sort"),
                (4, "Documentation"),
                (4, "Eq"),
                (5, "String"),
                (5, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_04_colon_01_numeric(self):
        self.verify(
            "currentposition:1==3",
            [
                (3, "Eq"),
                (4, "Colon"),
                (5, "CurrentPosition"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_04_colon_02_string(self):
        self.verify(
            'currentposition:"alpha"=="w"',
            [
                (3, "Eq"),
                (4, "Colon"),
                (5, "CurrentPosition"),
                (5, "String"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_04_colon_03_logical(self):
        self.verify("currentposition:true==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_04_colon_04_set(self):
        self.verify(
            "currentposition:k==3",
            [
                (3, "Eq"),
                (4, "Colon"),
                (5, "CurrentPosition"),
                (5, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_04_colon_05_position(self):
        self.verify("currentposition:initialposition==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_05_plus_01_numeric(self):
        self.verify(
            "7+3==4",
            [
                (3, "Eq"),
                (4, "Plus"),
                (5, "Integer"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_05_plus_02_string(self):
        self.verify(
            '"x"+"y"=="z"',
            [
                (3, "Eq"),
                (4, "Plus"),
                (5, "String"),
                (5, "String"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_06_move_01_logical(self):
        self.verify("move==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_06_move_02_no_legal(self):
        self.verify("move count==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_06_move_03_logical(self):
        self.verify("move legal==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_06_move_04_numeric(self):
        self.verify(
            "move legal count==3",
            [
                (3, "Eq"),
                (4, "Move"),
                (5, "LegalParameter"),
                (5, "Count"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_06_move_05_set(self):
        self.verify(
            "move to k==3",
            [
                (3, "Eq"),
                (4, "Move"),
                (5, "ToParameter"),
                (6, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_06_move_06_numeric(self):
        self.verify(
            "move to k count pseudolegal==3",
            [
                (3, "Eq"),
                (4, "Move"),
                (5, "ToParameter"),
                (6, "PieceDesignator"),
                (5, "Count"),
                (5, "PseudolegalParameter"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_07_compound_01_numeric(self):
        self.verify(
            "{k 1}==3",
            [
                (3, "Eq"),
                (4, "BraceLeft"),
                (5, "PieceDesignator"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_07_compound_02_string(self):
        self.verify(
            '{k "a"}=="w"',
            [
                (3, "Eq"),
                (4, "BraceLeft"),
                (5, "PieceDesignator"),
                (5, "String"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_07_compound_03_set(self):
        self.verify(
            "{k q}==3",
            [
                (3, "Eq"),
                (4, "BraceLeft"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_07_compound_04_logical(self):
        self.verify("[k true}==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_07_compound_05_position(self):
        self.verify("{k currentposition}==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_08_parentheses_01_numeric(self):
        self.verify(
            "(1)==3",
            [
                (3, "Eq"),
                (4, "ParenthesisLeft"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_08_parentheses_02_string(self):
        self.verify(
            '("a")=="w"',
            [
                (3, "Eq"),
                (4, "ParenthesisLeft"),
                (5, "String"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_08_parentheses_03_set(self):
        self.verify(
            "(q)==3",
            [
                (3, "Eq"),
                (4, "ParenthesisLeft"),
                (5, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_08_parentheses_04_logical(self):
        self.verify("(true)==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_08_parentheses_05_position(self):
        self.verify("(currentposition)==3", [], returncode=1)

    def test_213_compare_lhs_filter_type_09_brackets_01_numeric(self):
        self.verify(
            'v="a" v[1]=="w"',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Variable"),
                (5, "Integer"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_09_brackets_02_string_01_index(self):
        self.verify('v="a" v["b"]=="w"', [], returncode=1)

    def test_213_compare_lhs_filter_type_09_brackets_02_string_02_slice(self):
        self.verify('v="a" v[2:"b"]=="w"', [], returncode=1)

    def test_213_compare_lhs_filter_type_09_brackets_02_string_03_slice(self):
        self.verify(
            'v="a" v[2:4]=="w"',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Variable"),
                (5, "Integer"),
                (5, "Integer"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_09_brackets_03_set_01(self):
        self.verify(
            'v="a" v[q]==3',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Variable"),
                (3, "Eq"),
                (4, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_09_brackets_03_set_02(self):
        self.verify('v="a" v[qa5]==3', [], returncode=1)

    def test_213_compare_lhs_filter_type_09_brackets_04_logical(self):
        self.verify('v="a" v[true]==3', [], returncode=1)

    def test_213_compare_lhs_filter_type_09_brackets_05_position(self):
        self.verify('v="a" v[currentposition]==3', [], returncode=1)

    def test_213_compare_lhs_filter_type_10_dict_01_numeric_01_numeric(self):
        self.verify(
            "dictionary v[3]=4 v[2]==5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_01_numeric_02_string(self):
        self.verify(
            'dictionary v[3]="u" v[2]=="w"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_02_string_01_numeric(self):
        self.verify(
            "dictionary v[3]=4 v[2]==5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_02_string_02_string(self):
        self.verify(
            'dictionary v[3]="u" v[2]=="w"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "Integer"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_03_set_01_numeric(self):
        self.verify(
            "dictionary v[to]=4 v[from]==5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "Integer"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "From"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_03_set_02_string(self):
        self.verify(
            'dictionary v[to]="u" v[from]=="w"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "To"),
                (4, "String"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "From"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_04_pd_01_numeric(self):
        self.verify(
            "dictionary v[ a3 ]=4 v[ a4 ]==5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "Integer"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_04_pd_02_string(self):
        self.verify(
            'dictionary v[ a3 ]="u" v[ a4 ]=="w"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "String"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "PieceDesignator"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_05_position_01_numeric(self):
        self.verify(
            "local dictionary v[currentposition]=4 v[initialposition]==5",
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "Integer"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "Integer"),
            ],
        )

    def test_213_compare_lhs_filter_type_10_dict_05_position_02_string(self):
        self.verify(
            'local dictionary v[currentposition]="u" v[initialposition]=="w"',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "CurrentPosition"),
                (4, "String"),
                (3, "Eq"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "InitialPosition"),
                (4, "String"),
            ],
        )

    def test_213_compare_lhs_filter_type_11_lca(self):
        self.verify(
            "lca(currentposition initialposition)==initialposition",
            [
                (3, "Eq"),
                (4, "LCA"),
                (5, "CurrentPosition"),
                (5, "InitialPosition"),
                (4, "InitialPosition"),
            ],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Filters))
