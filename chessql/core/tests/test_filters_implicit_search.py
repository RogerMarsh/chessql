# test_filters_implicit_search.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for implicit search parameter filters.

The verification methods are provided by the Verify superclass.

Generally the test statements are the simplest which are accepted by CQL
for each filter.  Sometimes these will not make sense as queries to
evaluate.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FiltersImplicitSearch(verify.Verify):

    def test_024_date_01_plain(self):
        self.verify("date", [(3, "Date")])

    def test_024_date_02_piece(self):
        self.verify("date k", [(3, "Date"), (3, "PieceDesignator")])

    def test_024_date_03_implicit(self):
        self.verify_capture_cql_output(
            'date "2020-10-20"',
            [(3, "Date"), (4, "ImplicitSearchParameter")],
            "\n".join(
                (
                    " <StringInNode  isImplicit",
                    '   left: <StringLiteralNode "2020-10-20">',
                    "   right: <TagBuiltInNode Date>>",
                )
            ),
        )

    def test_024_date_04_value_match_01_ok(self):
        self.verify(
            'date ~~ "2019"',
            [(3, "RegexMatch"), (4, "Date"), (4, "String")],
        )

    def test_024_date_04_value_match_02_bad(self):
        self.verify('date "2019-10-21" ~~ "2019"', [], returncode=1)

    def test_024_date_05_string_01_str(self):
        self.verify_capture_cql_output(
            'str(date "2020-10-20")',
            [
                (3, "StrParentheses"),
                (4, "Date"),
                (4, "String"),
            ],
            "\n".join(
                (
                    " <StringConverter Nconverters: 2",
                    "   converter 0 of 2: <TagBuiltInNode Date>",
                    '   converter 1 of 2: <StringLiteralNode "2020-10-20">',
                )
            ),
        )

    def test_024_date_05_string_02_message(self):
        self.verify_capture_cql_output(
            'message(date "2020-10-20")',
            [
                (3, "MessageParentheses"),
                (4, "Date"),
                (4, "String"),
            ],
            "\n".join(
                (
                    " <StringConverter Nconverters: 2",
                    "    converter 0 of 2: <TagBuiltInNode Date>",
                    '    converter 1 of 2: <StringLiteralNode "2020-10-20">',
                )
            ),
        )

    def test_024_date_05_string_03_comment(self):
        self.verify_capture_cql_output(
            'comment(date "2020-10-20")',
            [
                (3, "CommentParentheses"),
                (4, "Date"),
                (4, "String"),
            ],
            "\n".join(
                (
                    " <StringConverter Nconverters: 2",
                    "    converter 0 of 2: <TagBuiltInNode Date>",
                    '    converter 1 of 2: <StringLiteralNode "2020-10-20">',
                )
            ),
        )

    def test_024_date_05_string_04_comment_symbol(self):
        self.verify_capture_cql_output(
            '/// date "2020-10-20"',
            [
                (3, "CommentSymbol"),
                (4, "Date"),
                (4, "String"),
            ],
            "\n".join(
                (
                    " <StringConverter Nconverters: 2",
                    "    converter 0 of 2: <TagBuiltInNode Date>",
                    '    converter 1 of 2: <StringLiteralNode "2020-10-20">',
                )
            ),
        )

    def test_024_date_06_implicit_01_str(self):
        self.verify_capture_cql_output(
            'str((date "2020-10-20"))',
            [
                (3, "StrParentheses"),
                (4, "ParenthesisLeft"),
                (5, "Date"),
                (6, "ImplicitSearchParameter"),
            ],
            "\n".join(
                (
                    " <StringConverter Nconverters: 1",
                    "   converter 0 of 1: <StringInNode  isImplicit",
                    '    left: <StringLiteralNode "2020-10-20">',
                    "    right: <TagBuiltInNode Date>>",
                )
            ),
        )

    def test_024_date_06_implicit_02_message(self):
        self.verify_capture_cql_output(
            'message((date "2020-10-20"))',
            [
                (3, "MessageParentheses"),
                (4, "ParenthesisLeft"),
                (5, "Date"),
                (6, "ImplicitSearchParameter"),
            ],
            "\n".join(
                (
                    " <StringConverter Nconverters: 1",
                    "    converter 0 of 1: <StringInNode  isImplicit",
                    '     left: <StringLiteralNode "2020-10-20">',
                    "     right: <TagBuiltInNode Date>>",
                )
            ),
        )

    def test_024_date_06_implicit_03_comment(self):
        self.verify_capture_cql_output(
            'comment((date "2020-10-20"))',
            [
                (3, "CommentParentheses"),
                (4, "ParenthesisLeft"),
                (5, "Date"),
                (6, "ImplicitSearchParameter"),
            ],
            "\n".join(
                (
                    " <StringConverter Nconverters: 1",
                    "    converter 0 of 1: <StringInNode  isImplicit",
                    '     left: <StringLiteralNode "2020-10-20">',
                    "     right: <TagBuiltInNode Date>>",
                )
            ),
        )

    def test_024_date_06_implicit_04_comment_symbol(self):
        self.verify_capture_cql_output(
            '/// (date "2020-10-20")',
            [
                (3, "CommentSymbol"),
                (4, "ParenthesisLeft"),
                (5, "Date"),
                (6, "ImplicitSearchParameter"),
            ],
            "\n".join(
                (
                    " <StringConverter Nconverters: 1",
                    "    converter 0 of 1: <StringInNode  isImplicit",
                    '     left: <StringLiteralNode "2020-10-20">',
                    "     right: <TagBuiltInNode Date>>",
                )
            ),
        )

    def test_031_eco_01_plain(self):
        self.verify("eco", [(3, "ECO")])

    def test_031_eco_02_piece(self):
        self.verify("eco k", [(3, "ECO"), (3, "PieceDesignator")])

    def test_031_eco_03_implicit(self):
        self.verify('eco "A50"', [(3, "ECO"), (4, "ImplicitSearchParameter")])

    def test_031_eco_04_value_match_01_ok(self):
        self.verify(
            'eco ~~ "A5"',
            [(3, "RegexMatch"), (4, "ECO"), (4, "String")],
        )

    def test_031_eco_04_value_match_02_bad(self):
        self.verify('eco "A50" ~~ "A5"', [], returncode=1)

    def test_033_event_01_plain(self):
        self.verify("event", [(3, "Event")])

    def test_033_event_02_piece(self):
        self.verify("event k", [(3, "Event"), (3, "PieceDesignator")])

    def test_033_event_03_implicit(self):
        self.verify(
            'event "London"', [(3, "Event"), (4, "ImplicitSearchParameter")]
        )

    def test_033_event_04_value_match_01_ok(self):
        self.verify(
            'event ~~ "Lon"',
            [(3, "RegexMatch"), (4, "Event"), (4, "String")],
        )

    def test_033_event_04_value_match_02_bad(self):
        self.verify('event "Event" ~~ "Lon"', [], returncode=1)

    def test_034_eventdate_01_plain(self):
        self.verify("eventdate", [(3, "EventDate")])

    def test_034_eventdate_02_piece(self):
        self.verify("eventdate k", [(3, "EventDate"), (3, "PieceDesignator")])

    def test_034_eventdate_03_implicit(self):
        self.verify(
            'eventdate "2020-10-20"',
            [(3, "EventDate"), (4, "ImplicitSearchParameter")],
        )

    def test_034_eventdate_04_value_match_01_ok(self):
        self.verify(
            'eventdate ~~ "2019"',
            [(3, "RegexMatch"), (4, "EventDate"), (4, "String")],
        )

    def test_034_eventdate_04_value_match_02_bad(self):
        self.verify('eventdate "2019-10-21" ~~ "2019"', [], returncode=1)

    def test_036_fen_plain(self):
        self.verify("fen", [(3, "FEN")])

    def test_036_fen_02_piece(self):
        self.verify("fen k", [(3, "FEN"), (3, "PieceDesignator")])

    def test_036_fen_03_implicit_01_obvious_non_fen_string(self):
        self.verify('fen "obvious non-fen"', [], returncode=1)

    def test_036_fen_03_implicit_02_pieces_01_invalid_01_extra_square(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/p8/8/8/8/PPPPPPPP/RNBQKBNR"',
            [],
            returncode=1,
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_02_extra_piece(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/p7/8/8/8/PPPPPPPP/RNBQKBNR"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_03_adjacent_kings(self):
        self.verify(
            'fen "rnbqkKnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQbBNR"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_04_missing_rank(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/PPPPPPPP/RNBQKBNR"',
            [],
            returncode=1,
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_05_extra_rank(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/8/PPPPPPPP/RNBQKBNR"',
            [],
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_06_extra_square_01(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/p8/8/8/8/PPPPPPPP/RNBQKBNR"',
            [],
            returncode=1,
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_06_extra_square_02(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/9/8/8/8/PPPPPPPP/RNBQKBNR"',
            [],
            returncode=1,
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_07_extra_digit_gap(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/71/8/8/8/PPPPPPPP/RNBQKBNR"',
            [],
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_08_fen_character(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/w7/8/PPPPPPPP/RNBQKBNR"',
            [],
            returncode=1,
        )

    def test_036_fen_03_implicit_02_pieces_01_invalid_08_empty_rank(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8//8/PPPPPPPP/RNBQKBNR"',
            [],
            returncode=1,
        )

    def test_036_fen_03_implicit_02_pieces_02_valid_01_standard_chars(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_02_pieces_02_valid_02_cql_chars(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/Aa._PPPP/RNBQKBNR"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_03_fen_01_too_many_fields(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 a"',
            [],
        )

    def test_036_fen_03_implicit_03_fen_02_six_01_full_move_valid(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_03_fen_02_six_01_full_move_bad(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 x"',
            [],
        )

    def test_036_fen_03_implicit_03_fen_03_five_01_half_move_clock_valid(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_03_fen_03_five_01_half_move_clock_bad(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - x"',
            [],
        )

    def test_036_fen_03_implicit_03_fen_04_four_01_no_ep(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_03_fen_04_four_02_ep_valid(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq b3"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_03_fen_04_four_03_ep_invalid(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq b4"',
            [],
        )

    def test_036_fen_03_implicit_03_fen_05_three_01_oo_valid(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_03_fen_05_three_02_oo_wrong_order(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KkQq"',
            [],
        )

    def test_036_fen_03_implicit_03_fen_05_three_03_oo_repeated(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KKQkq"',
            [],
        )

    def test_036_fen_03_implicit_03_fen_06_two_01_to_move_valid(self):
        self.verify(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"',
            [(3, "FEN"), (4, "ImplicitSearchParameter")],
        )

    def test_036_fen_03_implicit_03_fen_06_two_02_to_move_invalid(self):
        self.verify_tolerant(
            'fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR t"',
            [],
        )

    def test_036_fen_04_value_match_01_ok(self):
        self.verify(
            'fen ~~ "A5"',
            [(3, "RegexMatch"), (4, "FEN"), (4, "String")],
        )

    def test_036_fen_04_value_match_02_bad(self):
        self.verify('fen "A50" ~~ "A5"', [], returncode=1)

    def test_046_hascomment_01_plain(self):
        self.verify("hascomment", [(3, "OriginalComment")])

    def test_046_hascomment_02_piece(self):
        self.verify(
            "hascomment k",
            [(3, "OriginalComment"), (3, "PieceDesignator")],
        )

    def test_046_hascomment_03_implicit(self):
        self.verify(
            'hascomment "good"',
            [(3, "OriginalComment"), (4, "ImplicitSearchParameter")],
        )

    def test_046_hascomment_04_value_match_01_ok(self):
        self.verify(
            'hascomment ~~ "ood"',
            [(3, "RegexMatch"), (4, "OriginalComment"), (4, "String")],
        )

    def test_046_hascomment_04_value_match_02_bad(self):
        self.verify('hascomment "Good" ~~ "ood"', [], returncode=1)

    def test_084_originalcomment_01_plain(self):
        self.verify("originalcomment", [(3, "OriginalComment")])

    def test_084_originalcomment_02_piece(self):
        self.verify(
            "originalcomment k",
            [(3, "OriginalComment"), (3, "PieceDesignator")],
        )

    def test_084_originalcomment_03_implicit(self):
        self.verify(
            'originalcomment "good"',
            [(3, "OriginalComment"), (4, "ImplicitSearchParameter")],
        )

    def test_084_originalcomment_04_value_match_01_ok(self):
        self.verify(
            'originalcomment ~~ "ood"',
            [(3, "RegexMatch"), (4, "OriginalComment"), (4, "String")],
        )

    def test_084_originalcomment_04_value_match_02_bad(self):
        self.verify('originalcomment "Good" ~~ "ood"', [], returncode=1)

    def test_098_player_01_plain(self):
        self.verify("player", [(3, "Player")])

    def test_098_player_02_piece(self):
        self.verify("player k", [(3, "Player"), (3, "PieceDesignator")])

    def test_098_player_03_implicit(self):
        self.verify(
            'player "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_098_player_04_value_match_01_ok(self):
        self.verify(
            'player ~~ "aro"',
            [(3, "RegexMatch"), (4, "Player"), (4, "String")],
        )

    def test_098_player_04_value_match_02_bad(self):
        self.verify('player "Kasparov" ~~ "aro"', [], returncode=1)

    def test_099_player_white_01_plain(self):
        self.verify("player white", [(3, "Player")])

    def test_099_player_white_02_piece(self):
        self.verify("player white k", [(3, "Player"), (3, "PieceDesignator")])

    def test_099_player_white_03_implicit(self):
        self.verify(
            'player white "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_099_player_white_04_value_match_01_ok(self):
        self.verify(
            'player white ~~ "aro"',
            [(3, "RegexMatch"), (4, "Player"), (4, "String")],
        )

    def test_099_player_white_04_value_match_02_bad(self):
        self.verify('player white "Kasparov" ~~ "aro"', [], returncode=1)

    def test_100_player_black_01_plain(self):
        self.verify("player black", [(3, "Player")])

    def test_100_player_black_02_piece(self):
        self.verify("player black k", [(3, "Player"), (3, "PieceDesignator")])

    def test_100_player_black_03_implicit(self):
        self.verify(
            'player black "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_100_player_black_04_value_match_01_ok(self):
        self.verify(
            'player black ~~ "aro"',
            [(3, "RegexMatch"), (4, "Player"), (4, "String")],
        )

    def test_100_player_black_04_value_match_02_bad(self):
        self.verify('player black "Kasparov" ~~ "aro"', [], returncode=1)

    def test_124_site_01_plain(self):
        self.verify("site", [(3, "Site")])

    def test_124_site_02_piece(self):
        self.verify("site k", [(3, "Site"), (3, "PieceDesignator")])

    def test_124_site_03_implicit(self):
        self.verify(
            'site "Glasgow"', [(3, "Site"), (4, "ImplicitSearchParameter")]
        )

    def test_124_site_04_value_match_01_ok(self):
        self.verify(
            'site ~~ "off"',
            [(3, "RegexMatch"), (4, "Site"), (4, "String")],
        )

    def test_124_site_04_value_match_02_bad(self):
        self.verify('site "Lockerbie" ~~ "ker"', [], returncode=1)


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FiltersImplicitSearch))
