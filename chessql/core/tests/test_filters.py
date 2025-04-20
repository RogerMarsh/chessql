# test_filters.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for filters without own test module.

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

    def test_094_piecename_03_compare(self):
        self.verify(
            "piecename d4 == piecename d5",
            [
                (3, "Eq"),
                (4, "PieceName"),
                (5, "PieceDesignator"),
                (4, "PieceName"),
                (5, "PieceDesignator"),
            ],
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

    def test_105_primary(self):
        self.verify("primary", [(3, "Primary")])

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

    def test_110_ray_06_direction_set_set(self):
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

    def test_118_secondary(self):
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

    def test_136_typename_03_compare(self):
        self.verify(
            "typename d4 == typename d5",
            [
                (3, "Eq"),
                (4, "TypeName"),
                (5, "PieceDesignator"),
                (4, "TypeName"),
                (5, "PieceDesignator"),
            ],
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
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(Filters))
