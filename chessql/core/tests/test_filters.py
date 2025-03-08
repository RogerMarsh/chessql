# test_filters.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for individual filters.

See test_filter_captures for '[x]' filter tests.

See test_filter_dash for '--' filter tests.

See test_filters_atomic_dict for 'atomic' filter tests.

See test_filters_atomic_dict for 'dictionary' filter tests.

See test_filter_find for 'find' filter tests.

See test_filters_for_bind for 'isunbound' filter tests.

See test_filter_function for 'function' filter tests.

See test_filter_line for 'line' filter tests.

See test_filter_move for 'move' filter tests.

See test_filter_path for 'path' filter tests.

See test_filter_pin for 'pin' filter tests.

See test_filters_for_bind for 'unbind' filter tests.

The verification methods are provided by the Verify superclass.

Generally the test statements are the simplest which are accepted by CQL
for each filter.  Sometimes these will not make sense as queries to
evaluate.
"""

import unittest

from . import verify
from .. import cqltypes


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
                (4, "SingleMove"),
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
                (5, "SingleMove"),
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
                (5, "SingleMove"),
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
                (4, "SingleMove"),
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

    def test_056_isolatedpwans(self):
        self.verify("isolatedpawns", [(3, "IsolatedPawns")])

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
                (4, "SingleMove"),
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

    def test_062_pseudolegal_01(self):
        self.verify("pseudolegal", [], returncode=1)

    def test_062_pseudolegal_02(self):
        self.verify("pseudolegal k", [], returncode=1)

    def test_062_pseudolegal_03_move(self):
        self.verify(
            "pseudolegal --",
            [
                (3, "Pseudolegal"),
                (4, "SingleMove"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_062_pseudolegal_04_capture(self):
        self.verify("pseudolegal [x]", [], returncode=1)

    def test_061_light_01(self):
        self.verify("light", [], returncode=1)

    def test_061_light_02(self):
        self.verify(
            "light P",
            [
                (3, "Light"),
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

    def test_072_modelmate(self):
        self.verify("modelmate", [(3, "ModelMate")])

    def test_073_modelstalemate(self):
        self.verify("modelstalemate", [(3, "ModelStalemate")])

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

    def test_092_persistent_07_variable_equal_2(self):
        self.verify(
            "persistent x=1",
            [(3, "Assign"), (4, "Persistent"), (4, "Integer")],
        )

    def test_092_persistent_08_quiet_variable_equal_2(self):
        self.verify(
            "persistent quiet x=1",
            [(3, "Assign"), (4, "PersistentQuiet"), (4, "Integer")],
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
                (4, "SingleMove"),
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
        self.verify("2+3", [(3, "Plus"), (4, "Integer"), (4, "Integer")])

    def test_189_plus_04_string_01(self):
        self.verify('"x"+', [], returncode=1)

    def test_189_plus_04_string_02(self):
        self.verify('+"y"', [], returncode=1)

    def test_189_plus_05_string(self):
        self.verify('"x"+"y"', [(3, "Plus"), (4, "String"), (4, "String")])

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
        self.verify_run_fail('#"str"')

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


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Filters))
