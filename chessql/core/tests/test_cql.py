# cql.py
# Copyright 2020 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""constants tests for cql"""
# No definition for CQL.FUNCTION, the 'function' filter.

import unittest
import re

from .. import constants
from .. import cql


class TokenDefinition(unittest.TestCase):
    def test_01_token(self):
        ae = self.assertEqual
        t = cql.TokenDefinition(*[None] * 6)
        ae(len(t), 7)
        ae(t.name, None)
        ae(t.flags, None)
        ae(t.precedence, None)
        ae(t.pattern, None)
        ae(t.returntype, None)
        ae(t.arguments, None)
        ae(t.variant_name, None)


class Flags(unittest.TestCase):
    def test_01_Flags(self):
        ae = self.assertEqual
        ae(len([a for a in dir(cql.Flags) if not a.startswith("__")]), 17)
        ae(
            sorted([a for a in dir(cql.Flags) if not a.startswith("__")]),
            [
                "ACCEPT_RANGE",
                "ALLOWED_TOP_STACK_AT_END",
                "ALLOWED_UNARY_MINUS",
                "ASSIGN_TO_VARIABLE",
                "CLOSE_BRACE_OR_PARENTHESIS",
                "END_FILTER_NON_PARAMETER",
                "HALT_POP_CHAINED_FILTERS",
                "HALT_POP_NO_BODY_FILTER",
                "IF_FRAME",
                "INCOMPLETE_IF_ON_STACK",
                "INHIBIT_ENCLOSING_TRANSFORMS",
                "LINE_FRAME",
                "NAMED_COMPOUND_FILTER",
                "NO_ARITHMETIC_FILTERS",
                "PARAMETER_TAKES_ARGUMENT",
                "PARENTHESIZED_ARGUMENTS",
                "STATEMENT_FRAME",
            ],
        )

    def test_02_HALT_POP_CHAINED_FILTERS(self):
        self.assertEqual(
            cql.Flags.HALT_POP_CHAINED_FILTERS.value,
            "halt_pop_chained_filters",
        )

    def test_03_CLOSE_BRACE_OR_PARENTHESIS(self):
        self.assertEqual(
            cql.Flags.CLOSE_BRACE_OR_PARENTHESIS.value,
            "close_brace_or_parenthesis",
        )

    def test_04_NAMED_COMPOUND_FILTER(self):
        self.assertEqual(
            cql.Flags.NAMED_COMPOUND_FILTER.value, "named_compound_filter"
        )

    def test_05_INHIBIT_ENCLOSING_TRANSFORMS(self):
        self.assertEqual(
            cql.Flags.INHIBIT_ENCLOSING_TRANSFORMS.value,
            "inhibit_enclosing_transforms",
        )

    def test_06_ASSIGN_TO_VARIABLE(self):
        self.assertEqual(
            cql.Flags.ASSIGN_TO_VARIABLE.value, "assign_to_variable"
        )

    def test_07_INCOMPLETE_IF_ON_STACK(self):
        self.assertEqual(
            cql.Flags.INCOMPLETE_IF_ON_STACK.value, "incomplete_if_on_stack"
        )

    def test_08_PARAMETER_TAKES_ARGUMENT(self):
        self.assertEqual(
            cql.Flags.PARAMETER_TAKES_ARGUMENT.value,
            "parameter_takes_argument",
        )

    def test_09_PARENTHESIZED_ARGUMENTS(self):
        self.assertEqual(
            cql.Flags.PARENTHESIZED_ARGUMENTS.value, "parenthesized_arguments"
        )

    def test_10_HALT_POP_NO_BODY_FILTER(self):
        self.assertEqual(
            cql.Flags.HALT_POP_NO_BODY_FILTER.value, "halt_pop_no_body_filter"
        )

    def test_11_ACCEPT_RANGE(self):
        self.assertEqual(cql.Flags.ACCEPT_RANGE.value, "accept_range")

    def test_12_END_FILTER_NON_PARAMETER(self):
        self.assertEqual(
            cql.Flags.END_FILTER_NON_PARAMETER.value,
            "end_filter_non_parameter",
        )

    def test_13_ALLOWED_UNARY_MINUS(self):
        self.assertEqual(
            cql.Flags.ALLOWED_UNARY_MINUS.value, "allowed_unary_minus"
        )

    def test_14_NO_ARITHMETIC_FILTERS(self):
        self.assertEqual(
            cql.Flags.NO_ARITHMETIC_FILTERS.value, "no_arithmetic_filters"
        )

    def test_15_STATEMENT_FRAME(self):
        self.assertEqual(cql.Flags.STATEMENT_FRAME.value, "statement_frame")

    def test_16_LINE_FRAME(self):
        self.assertEqual(cql.Flags.LINE_FRAME.value, "line_frame")

    def test_17_IF_FRAME(self):
        self.assertEqual(cql.Flags.IF_FRAME.value, "if_frame")


class TokenTypes(unittest.TestCase):
    def test_01_Type(self):
        ae = self.assertEqual
        ae(len([a for a in dir(cql.TokenTypes) if not a.startswith("__")]), 23)
        ae(
            sorted([a for a in dir(cql.TokenTypes) if not a.startswith("__")]),
            [
                "CONSECUTIVEMOVES_PARAMETER",
                "ELSE_PARAMETER",
                "FIND_PARAMETER",
                "FUNCTION_CALL",
                "FUNCTION_NAME",
                "LINE_LEFTARROW_PARAMETER",
                "LINE_PARAMETER",
                "LINE_RE_SYMBOLS",
                "LINE_RIGHTARROW_PARAMETER",
                "LOGICAL_FILTER",
                "MOVE_PARAMETER",
                "NUMERAL",
                "NUMERIC_FILTER",
                "NUMERIC_VARIABLE",
                "PERSISTENT_NUMERIC_VARIABLE",
                "PIECE_VARIABLE",
                "PIN_PARAMETER",
                "POSITION_FILTER",
                "POSITION_VARIABLE",
                "SET_FILTER",
                "SET_VARIABLE",
                "THEN_PARAMETER",
                "UNSET_VARIABLE",
            ],
        )

    def test_03_NUMERIC_FILTER(self):
        self.assertEqual(cql.TokenTypes.NUMERIC_FILTER.value, "numeric")

    def test_04_POSITION_FILTER(self):
        self.assertEqual(cql.TokenTypes.POSITION_FILTER.value, "position")

    def test_06_SET_FILTER(self):
        self.assertEqual(cql.TokenTypes.SET_FILTER.value, "set")

    def test_07_NUMERAL_CONSTANT(self):
        self.assertEqual(cql.TokenTypes.NUMERAL.value, "numeral")

    def test_09_FUNCTION_CALL(self):
        self.assertEqual(cql.TokenTypes.FUNCTION_CALL.value, "function call")

    def test_10_FUNCTION_NAME(self):
        self.assertEqual(cql.TokenTypes.FUNCTION_NAME.value, "function name")

    def test_12_POSITION_VARIABLE(self):
        self.assertEqual(
            cql.TokenTypes.POSITION_VARIABLE.value, "position variable"
        )

    def test_14_LINE_RE_SYMBOLS(self):
        self.assertEqual(
            cql.TokenTypes.LINE_RE_SYMBOLS.value, "line re symbols"
        )

    def test_15_LOGICAL_FILTER(self):
        self.assertEqual(cql.TokenTypes.LOGICAL_FILTER.value, "logical")

    def test_24_UNSET_VARIABLE(self):
        self.assertEqual(cql.TokenTypes.UNSET_VARIABLE.value, "unset variable")

    def test_25_NUMERIC_VARIABLE(self):
        self.assertEqual(
            cql.TokenTypes.NUMERIC_VARIABLE.value, "numeric variable"
        )

    def test_26_SET_VARIABLE(self):
        self.assertEqual(cql.TokenTypes.SET_VARIABLE.value, "set variable")

    def test_27_PIECE_VARIABLE(self):
        self.assertEqual(cql.TokenTypes.PIECE_VARIABLE.value, "piece variable")

    def test_28_PERSISTENT_NUMERIC_VARIABLE(self):
        self.assertEqual(
            cql.TokenTypes.PERSISTENT_NUMERIC_VARIABLE.value,
            "persistent numeric variable",
        )

    def test_30_MOVE_PARAMETER(self):
        self.assertEqual(cql.TokenTypes.MOVE_PARAMETER.value, "move parameter")

    def test_31_PIN_PARAMETER(self):
        self.assertEqual(cql.TokenTypes.PIN_PARAMETER.value, "pin parameter")

    def test_32_THEN_PARAMETER(self):
        self.assertEqual(cql.TokenTypes.THEN_PARAMETER.value, "then parameter")

    def test_33_ELSE_PARAMETER(self):
        self.assertEqual(cql.TokenTypes.ELSE_PARAMETER.value, "else parameter")


class Token(unittest.TestCase):
    # Confirm the regular expressions for each token can be compiled.
    # Confirm token attributes have not been changed without repeating it here.
    # Failure in these tests means something was definitely changed without
    # being tested.

    def test_001_token_existence(self):
        ae = self.assertEqual
        ae(len([a for a in dir(cql.Token) if not a.startswith("__")]), 177)
        ae(
            sorted([a for a in dir(cql.Token) if not a.startswith("__")]),
            [
                "ABS",
                "ALL",
                "ANCESTOR",
                "AND",
                "ANYDIRECTION",
                "ASSIGN",
                "ATTACKEDBY",
                "ATTACKS",
                "BADTOKEN",
                "BETWEEN",
                "BLACK",
                "BLOCKCOMMENT",
                "BTM",
                "CAPTURE",
                "CASTLE",
                "CHECK",
                "CHILD",
                "COLON",
                "COLORTYPE",
                "COMMENT",
                "CONNECTEDPAWNS",
                "CONSECUTIVEMOVES",
                "COUNT",
                "CQL",
                "CURRENTPOSITION",
                "DARK",
                "DEPTH",
                "DESCENDANT",
                "DIAGONAL",
                "DISTANCE",
                "DIVIDE",
                "DOT",
                "DOUBLEDPAWNS",
                "DOWN",
                "ECHO",
                "ELO",
                "ELSE",
                "ENPASSANT",
                "ENPASSANT_SQUARE",
                "EOLCOMMENT",
                "EQ",
                "EVENT",
                "FALSE",
                "FEN",
                "FILE",
                "FIND",
                "FIRSTMATCH",
                "FLIP",
                "FLIPCOLOR",
                "FLIPHORIZONTAL",
                "FLIPVERTICAL",
                "FROM",
                "FUNCTION",
                "GAMENUMBER",
                "GE",
                "GT",
                "HASCOMMENT",
                "HASH",
                "HORIZONTAL",
                "IF",
                "IN",
                "INITIAL",
                "INPUT",
                "INTERSECTION",
                "IPDIVIDE",
                "IPMINUS",
                "IPMODULUS",
                "IPMULTIPLY",
                "IPPLUS",
                "ISOLATEDPAWNS",
                "LASTPOSITION",
                "LCA",
                "LE",
                "LEFT",
                "LEFTARROW",
                "LEFTBRACE",
                "LEFTPARENTHESIS",
                "LEGAL",
                "LIGHT",
                "LINE",
                "LOOP",
                "LT",
                "MAINLINE",
                "MAKESQUARE",
                "MATCHCOUNT",
                "MATCHSTRING",
                "MATE",
                "MAX",
                "MESSAGE",
                "MIN",
                "MINUS",
                "MODULUS",
                "MOVE",
                "MOVENUMBER",
                "NE",
                "NESTBAN",
                "NORTHEAST",
                "NORTHWEST",
                "NOT",
                "NOTRANSFORM",
                "NULL",
                "NUMBER",
                "OO",
                "OOO",
                "OR",
                "ORTHOGONAL",
                "OUTPUT",
                "PARENT",
                "PASSEDPAWNS",
                "PERSISTENT",
                "PIECE",
                "PIECEID",
                "PIECE_ALL_IN",
                "PIECE_ASSIGNMENT",
                "PIECE_DESIGNATOR",
                "PIECE_IN",
                "PIN",
                "PLAYER",
                "PLUS",
                "PLY",
                "POSITION",
                "POSITIONID",
                "POWER",
                "PREVIOUS",
                "PRIMARY",
                "PROMOTE",
                "PSEUDOLEGAL",
                "QUERY",
                "QUIET",
                "RANK",
                "RAY",
                "REPEATPLUS",
                "REPEATRANGE",
                "REPEATSTAR",
                "RESULT",
                "REVERSECOLOR",
                "RIGHT",
                "RIGHTARROW",
                "RIGHTBRACE",
                "RIGHTPARENTHESIS",
                "ROTATE45",
                "ROTATE90",
                "SECONDARY",
                "SHIFT",
                "SHIFTHORIZONTAL",
                "SHIFTVERTICAL",
                "SIDETOMOVE",
                "SILENT",
                "SINGLECOLOR",
                "SITE",
                "SORT",
                "SOUTHEAST",
                "SOUTHWEST",
                "SQRT",
                "SQUARE",
                "SQUARE_ALL_IN",
                "SQUARE_IN",
                "STALEMATE",
                "STAR",
                "TERMINAL",
                "THEN",
                "THROUGH",
                "TILDE",
                "TO",
                "TRUE",
                "TYPE",
                "UNION",
                "UP",
                "VARIABLE",
                "VARIATION",
                "VARIATIONS",
                "VERTICAL",
                "VIRTUALMAINLINE",
                "WHITE",
                "WTM",
                "XRAY",
                "YEAR",
            ],
        )

    def test_001_token_returntype(self):
        ae = self.assertEqual
        for a in dir(cql.Token):
            if a.startswith("__"):
                continue
            t = getattr(cql.Token, a)
            if len(t.returntype) != 1:
                pass  # print(len(t.returntype), a)

    def test_002_token_varint_name(self):
        ae = self.assertEqual
        for a in dir(cql.Token):
            if a.startswith("__"):
                continue
            t = getattr(cql.Token, a)
            ae(t.variant_name, None)

    def test_100_(self):
        ae = self.assertEqual
        t = cql.Token.ABS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "abs")
        ae({v.value for v in t[1]}, {"allowed_unary_minus"})
        ae(t[2], 100)
        ae(t[3], r"abs\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeral", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_101_(self):
        ae = self.assertEqual
        t = cql.Token.ANCESTOR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ancestor")
        ae(
            {v.value for v in t[1]},
            {"halt_pop_chained_filters", "parenthesized_arguments"},
        )
        ae(t[2], 40)
        ae(t[3], r"ancestor\s*\(")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_102_(self):
        ae = self.assertEqual
        t = cql.Token.AND
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "and_")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 60)
        ae(t[3], r"and\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set", "logical", "position", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_103_(self):
        ae = self.assertEqual
        t = cql.Token.ANYDIRECTION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "anydirection")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"anydirection\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_104_(self):
        ae = self.assertEqual
        t = cql.Token.ATTACKEDBY
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "attackedby")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 180)
        ae(t[3], r"attackedby\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_105_(self):
        ae = self.assertEqual
        t = cql.Token.ATTACKS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "attacks")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 180)
        ae(t[3], r"attacks\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_106_(self):
        ae = self.assertEqual
        t = cql.Token.BETWEEN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "between")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 140)
        ae(t[3], r"between\s*\(")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_107_(self):
        ae = self.assertEqual
        t = cql.Token.BLACK
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "black")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"black\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_108_(self):
        ae = self.assertEqual
        t = cql.Token.BTM
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "btm")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"btm\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_109_(self):
        ae = self.assertEqual
        t = cql.Token.CHECK
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "check")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"check\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_110_(self):
        ae = self.assertEqual
        t = cql.Token.CHILD
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "child")
        ae(
            {v.value for v in t[1]},
            {"halt_pop_chained_filters", "parenthesized_arguments"},
        )
        ae(t[2], 0)
        ae(t[3], r"child(?:\s*\()?")
        ae({v.value for v in t[4]}, {"position"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_111_(self):
        ae = self.assertEqual
        t = cql.Token.COLORTYPE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "colortype")
        ae(t[1], frozenset())
        ae(t[2], 140)
        ae(t[3], r"colortype\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_112_(self):
        ae = self.assertEqual
        t = cql.Token.COMMENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "comment")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 0)
        ae(t[3], r"comment(?:\s*\()?")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_113_(self):
        ae = self.assertEqual
        t = cql.Token.CONNECTEDPAWNS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "connectedpawns")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"connectedpawns\b")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_114_(self):
        ae = self.assertEqual
        t = cql.Token.CONSECUTIVEMOVES
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "consecutivemoves")
        ae({v.value for v in t[1]}, {"incomplete_if_on_stack", "accept_range"})
        ae(t[2], 0)
        ae(t[3], r"consecutivemoves\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"consecutivemoves parameter"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_115_(self):
        ae = self.assertEqual
        t = cql.Token.CQL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "cql")
        ae(
            {v.value for v in t[1]},
            {"halt_pop_chained_filters", "statement_frame"},
        )
        ae(t[2], 0)
        ae(
            t[3],
            r"".join(
                (
                    r"cql(?:\s*\(\s*(?:(?:",
                    r"(?:output|input)\s+\S+\.pgn|",
                    r"(?:sort\s+)?matchcount(?:\s+[0-9]+){,2}|",
                    r"gamenumber(?:\s+[0-9]+){,2}|",
                    r"result\s+(?:1-0|1/2-1/2|0-1)|",
                    r"silent|",
                    r"quiet|",
                    r"variations|",
                    r'matchstring\s+"(?:[^\\"]|\\.)*")\s+',
                    r")*\)\s*)?",
                )
            ),
        )
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_116_(self):
        ae = self.assertEqual
        t = cql.Token.CURRENTPOSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "currentposition")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"currentposition\b")
        ae({v.value for v in t[4]}, {"position"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_117_(self):
        ae = self.assertEqual
        t = cql.Token.DARK
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "dark")
        ae(t[1], frozenset())
        ae(t[2], 200)
        ae(t[3], r"dark\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_118_(self):
        ae = self.assertEqual
        t = cql.Token.DEPTH
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "depth")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"depth\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_119_(self):
        ae = self.assertEqual
        t = cql.Token.DESCENDANT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "descendant")
        ae(
            {v.value for v in t[1]},
            {"halt_pop_chained_filters", "parenthesized_arguments"},
        )
        ae(t[2], 40)
        ae(t[3], r"descendant\s*\(")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_120_(self):
        ae = self.assertEqual
        t = cql.Token.DIAGONAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "diagonal")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"diagonal\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_121_(self):
        ae = self.assertEqual
        t = cql.Token.DISTANCE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "distance")
        ae(
            {v.value for v in t[1]},
            {
                "parenthesized_arguments",
                "halt_pop_chained_filters",
                "allowed_unary_minus",
            },
        )
        ae(t[2], 40)
        ae(t[3], r"distance\s*\(")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_122_(self):
        ae = self.assertEqual
        t = cql.Token.DOUBLEDPAWNS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "doubledpawns")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"doubledpawns\b")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_123_(self):
        ae = self.assertEqual
        t = cql.Token.DOWN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "down")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"down\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_124_(self):
        ae = self.assertEqual
        t = cql.Token.ECHO
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "echo")
        ae(
            {v.value for v in t[1]},
            {"incomplete_if_on_stack", "halt_pop_no_body_filter"},
        )
        ae(t[2], 0)
        ae(
            t[3],
            r"".join(
                (
                    r"echo\s+\(\s*[$A-Z_a-z][$0-9A-Z_a-z]*",
                    r"\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s*\)\s*(?:in\s+all\b)?",
                )
            ),
        )
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_125_(self):
        ae = self.assertEqual
        t = cql.Token.ELO
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "elo")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"elo(?:\s+(?:black|white))?\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_126_(self):
        ae = self.assertEqual
        t = cql.Token.EVENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "event")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r'event\s+(?:"((?:[^\\"]|\\.)*)")')
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_127_(self):
        ae = self.assertEqual
        t = cql.Token.FALSE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "false")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"false\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_128_(self):
        ae = self.assertEqual
        t = cql.Token.FEN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "fen")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r'fen\s+"[^"]*"')
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_129_(self):
        ae = self.assertEqual
        t = cql.Token.FILE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "file")
        ae(
            {v.value for v in t[1]},
            frozenset({"inhibit_enclosing_transforms"}),
        )
        ae(t[2], 140)
        ae(t[3], r"file\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_130_(self):
        ae = self.assertEqual
        t = cql.Token.FIND
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "find")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"find\b")
        ae({v.value for v in t[4]}, {"position"})
        ae({v.value for v in t[5]}, {"set", "logical", "position", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_131_(self):
        ae = self.assertEqual
        t = cql.Token.FLIP
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "flip")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"flip(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_132_(self):
        ae = self.assertEqual
        t = cql.Token.FLIPCOLOR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "flipcolor")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"flipcolor(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_133_(self):
        ae = self.assertEqual
        t = cql.Token.FLIPHORIZONTAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "fliphorizontal")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"fliphorizontal(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_134_(self):
        ae = self.assertEqual
        t = cql.Token.FLIPVERTICAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "flipvertical")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"flipvertical(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_135_(self):
        ae = self.assertEqual
        t = cql.Token.FUNCTION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "function")
        ae(
            {v.value for v in t[1]},
            {"halt_pop_chained_filters", "parenthesized_arguments"},
        )
        ae(t[2], 0)
        ae(
            t[3],
            r"".join(
                (
                    r"function\s+([$A-Z_a-z][$0-9A-Z_a-z]*)\s*",
                    r"\(\s*([$A-Z_a-z][$0-9A-Z_a-z]*",
                    r"(?:\s[$A-Z_a-z][$0-9A-Z_a-z]*)*)\s*\)",
                    r"\s*{",
                )
            ),
        )
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_136_(self):
        ae = self.assertEqual
        t = cql.Token.GAMENUMBER
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "gamenumber")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "allowed_unary_minus"},
        )
        ae(t[2], 0)
        ae(t[3], r"gamenumber\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_137_(self):
        ae = self.assertEqual
        t = cql.Token.HASCOMMENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "hascomment")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r'hascomment\s+(?:"((?:[^\\"]|\\.)*)")')
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_138_(self):
        ae = self.assertEqual
        t = cql.Token.HORIZONTAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "horizontal")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"horizontal\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_139_(self):
        ae = self.assertEqual
        t = cql.Token.IF
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "if_")
        ae({v.value for v in t[1]}, {"incomplete_if_on_stack", "if_frame"})
        ae(t[2], 40)
        ae(t[3], r"if\b")
        ae({v.value for v in t[4]}, {"logical", "set", "numeric", "position"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_140_(self):
        ae = self.assertEqual
        t = cql.Token.THEN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "then")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"then\b")
        ae({v.value for v in t[4]}, {"then parameter"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_141_(self):
        ae = self.assertEqual
        t = cql.Token.ELSE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "else_")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"else\b")
        ae({v.value for v in t[4]}, {"else parameter"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_142_(self):
        ae = self.assertEqual
        t = cql.Token.IN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "in_")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 80)
        ae(t[3], r"in\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_143_(self):
        ae = self.assertEqual
        t = cql.Token.INITIAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "initial")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"initial\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_144_(self):
        ae = self.assertEqual
        t = cql.Token.ISOLATEDPAWNS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "isolatedpawns")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"isolatedpawns\b")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_145_(self):
        ae = self.assertEqual
        t = cql.Token.LCA
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "lca")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 40)
        ae(t[3], r"lca\s*\(")
        ae({v.value for v in t[4]}, {"position"})
        ae({v.value for v in t[5]}, {"position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_146_(self):
        ae = self.assertEqual
        t = cql.Token.LEFT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "left")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"left\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_147_(self):
        ae = self.assertEqual
        t = cql.Token.LIGHT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "light")
        ae(t[1], frozenset())
        ae(t[2], 200)
        ae(t[3], r"light\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_148_(self):
        ae = self.assertEqual
        t = cql.Token.LINE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "line")
        ae(
            {v.value for v in t[1]},
            {"accept_range", "halt_pop_chained_filters", "line_frame"},
        )
        ae(t[2], 0)
        ae(t[3], r"line\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"line parameter"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_149_(self):
        ae = self.assertEqual
        t = cql.Token.LOOP
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "loop")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"loop\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_150_(self):
        ae = self.assertEqual
        t = cql.Token.MAINLINE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "mainline")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"mainline\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_151_(self):
        ae = self.assertEqual
        t = cql.Token.MAKESQUARE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "makesquare")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 100)
        ae(t[3], r"makesquare\s*\(")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"numeral", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_152_(self):
        ae = self.assertEqual
        t = cql.Token.MATE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "mate")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"mate\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_153_(self):
        ae = self.assertEqual
        t = cql.Token.MAX
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "max")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 0)
        ae(t[3], r"max\s*\(")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeral", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_154_(self):
        ae = self.assertEqual
        t = cql.Token.MESSAGE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "message")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 0)
        ae(t[3], r"message(?:\s*\()?")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_155_(self):
        ae = self.assertEqual
        t = cql.Token.MIN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "min")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 0)
        ae(t[3], r"min\s*\(")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeral", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_156_(self):
        ae = self.assertEqual
        t = cql.Token.MOVE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "move")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "end_filter_non_parameter"},
        )
        ae(t[2], 0)
        ae(t[3], r"move\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"move parameter"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_157_(self):
        ae = self.assertEqual
        t = cql.Token.MOVENUMBER
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "movenumber")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "allowed_unary_minus"},
        )
        ae(t[2], 0)
        ae(t[3], r"movenumber\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_158_(self):
        ae = self.assertEqual
        t = cql.Token.NORTHEAST
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "northeast")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"northeast\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_159_(self):
        ae = self.assertEqual
        t = cql.Token.NORTHWEST
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "northwest")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"northwest\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_160_(self):
        ae = self.assertEqual
        t = cql.Token.NOTRANSFORM
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "notransform")
        ae(
            {v.value for v in t[1]},
            frozenset({"inhibit_enclosing_transforms"}),
        )
        ae(t[2], 200)
        ae(t[3], r"notransform\b")
        ae({v.value for v in t[4]}, {"logical", "set", "numeric", "position"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_161_(self):
        ae = self.assertEqual
        t = cql.Token.NOT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "not_")
        ae(t[1], frozenset())
        ae(t[2], 70)
        ae(t[3], r"not\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_162_(self):
        ae = self.assertEqual
        t = cql.Token.ORTHOGONAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "orthogonal")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"orthogonal\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_163_(self):
        ae = self.assertEqual
        t = cql.Token.OR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "or_")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 50)
        ae(t[3], r"or\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"logical", "numeric", "set", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_164_(self):
        ae = self.assertEqual
        t = cql.Token.PARENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "parent")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"parent\b")
        ae({v.value for v in t[4]}, {"position"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_165_(self):
        ae = self.assertEqual
        t = cql.Token.PASSEDPAWNS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "passedpawns")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"passedpawns\b")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_166_(self):
        ae = self.assertEqual
        t = cql.Token.PERSISTENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "persistent")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 100)
        ae(t[3], r"persistent\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_167_(self):
        ae = self.assertEqual
        t = cql.Token.PIECE_IN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "piecein")
        ae(
            {v.value for v in t[1]},
            frozenset({"incomplete_if_on_stack", "halt_pop_no_body_filter"}),
        )
        ae(t[2], 0)
        ae(t[3], r"piece\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_168_(self):
        ae = self.assertEqual
        t = cql.Token.PIECE_ASSIGNMENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "pieceassignment")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"piece\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+=")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_169_(self):
        ae = self.assertEqual
        t = cql.Token.PIECE_DESIGNATOR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "piecedesignator")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(
            t[3],
            r"".join(
                (
                    r"(?:(?:[a-h](?:-[a-h])?[1-8](?:-[1-8])?|\[[a-h]",
                    r"(?:-[a-h])?[1-8](?:-[1-8])?(?:,[a-h](?:-[a-h])?[1-8]",
                    r"(?:-[1-8])?)*])|(?:(?:[KQRBNPkqrbnpAa_]|\[",
                    "(?:[KQRBNPkqrbnpAa_]+)])(?:[a-h](?:-[a-h])?[1-8]",
                    r"(?:-[1-8])?|\[[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r"(?:,[a-h](?:-[a-h])?[1-8](?:-[1-8])?)*]))|\[",
                    r"(?:[KQRBNPkqrbnpAa_]+)])(?![a-zA-Z0-9_[\]])|",
                    r"[KQRBNPkqrbnpAa_]\b",
                )
            ),
        )
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_170_(self):
        ae = self.assertEqual
        t = cql.Token.PIECEID
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "pieceid")
        ae(t[1], frozenset())
        ae(t[2], 140)
        ae(t[3], r"pieceid\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_171_(self):
        ae = self.assertEqual
        t = cql.Token.PIN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "pin")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "end_filter_non_parameter"},
        )
        ae(t[2], 0)
        ae(t[3], r"pin\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"pin parameter"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_172_(self):
        ae = self.assertEqual
        t = cql.Token.PLAYER
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "player")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r'player\s+(?:(?:black|white)\s+)?(?:"((?:[^\\"]|\\.)*)")')
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_173_(self):
        ae = self.assertEqual
        t = cql.Token.PLY
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ply")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "allowed_unary_minus"},
        )
        ae(t[2], 0)
        ae(t[3], r"ply\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_174_(self):
        ae = self.assertEqual
        t = cql.Token.POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "position")
        ae(t[1], frozenset())
        ae(t[2], 100)
        ae(t[3], r"position\b")
        ae({v.value for v in t[4]}, {"position"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_175_(self):
        ae = self.assertEqual
        t = cql.Token.POSITIONID
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "positionid")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "allowed_unary_minus"},
        )
        ae(t[2], 0)
        ae(t[3], r"positionid\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_176_(self):
        ae = self.assertEqual
        t = cql.Token.POWER
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "power")
        ae({v.value for v in t[1]}, {"allowed_unary_minus"})
        ae(t[2], 140)
        ae(t[3], r"power\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_177_(self):
        ae = self.assertEqual
        t = cql.Token.RANK
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "rank")
        ae(
            {v.value for v in t[1]},
            frozenset({"inhibit_enclosing_transforms"}),
        )
        ae(t[2], 140)
        ae(t[3], r"rank\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_178_(self):
        ae = self.assertEqual
        t = cql.Token.RAY
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ray")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 0)
        ae(
            t[3],
            r"".join(
                (
                    r"ray(?:\s+(?:",
                    r"up|down|right|left|northeast|northwest|southeast|southwest|",
                    r"diagonal|orthogonal|vertical|horizontal|anydirection",
                    r"))*\s*\(",
                )
            ),
        )
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_179_(self):
        ae = self.assertEqual
        t = cql.Token.RESULT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "result")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r'result(?:\s+(?:(?:1-0|0-1|1/2-1/2)|"(?:1-0|0-1|1/2-1/2)"))')
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_180_(self):
        ae = self.assertEqual
        t = cql.Token.REVERSECOLOR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "reversecolor")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"reversecolor\b")
        ae({v.value for v in t[4]}, {"logical", "set", "numeric", "position"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_181_(self):
        ae = self.assertEqual
        t = cql.Token.RIGHT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "right")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"right\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_182_(self):
        ae = self.assertEqual
        t = cql.Token.ROTATE45
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "rotate45")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"rotate45(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_183_(self):
        ae = self.assertEqual
        t = cql.Token.ROTATE90
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "rotate90")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"rotate90(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_184_(self):
        ae = self.assertEqual
        t = cql.Token.SHIFT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "shift")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"shift(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_185_(self):
        ae = self.assertEqual
        t = cql.Token.SHIFTHORIZONTAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "shifthorizontal")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"shifthorizontal(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_186_(self):
        ae = self.assertEqual
        t = cql.Token.SHIFTVERTICAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "shiftvertical")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"shiftvertical(?:\s+count)?\b")
        ae({v.value for v in t[4]}, {"position", "numeric", "set", "logical"})
        ae({v.value for v in t[5]}, {"position", "numeric", "set", "logical"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_187_(self):
        ae = self.assertEqual
        t = cql.Token.SIDETOMOVE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "sidetomove")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"sidetomove\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_188_(self):
        ae = self.assertEqual
        t = cql.Token.SITE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "site")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r'site\s+(?:"((?:[^\\"]|\\.)*)")')
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_189_(self):
        ae = self.assertEqual
        t = cql.Token.SORT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "sort")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r'sort(?:\s+min)?(?:\s+"((?:[^\\"]|\\.)*)")?')
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_190_(self):
        ae = self.assertEqual
        t = cql.Token.SOUTHEAST
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "southeast")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"southeast\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_191_(self):
        ae = self.assertEqual
        t = cql.Token.SOUTHWEST
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "southwest")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"southwest\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_192_(self):
        ae = self.assertEqual
        t = cql.Token.SQRT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "sqrt")
        ae(t[1], frozenset())
        ae(t[2], 100)
        ae(t[3], r"sqrt\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_193_(self):
        ae = self.assertEqual
        t = cql.Token.SQUARE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "square")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"square\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_194_(self):
        ae = self.assertEqual
        t = cql.Token.STALEMATE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "stalemate")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"stalemate\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_195_(self):
        ae = self.assertEqual
        t = cql.Token.TERMINAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "terminal")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"terminal\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_196_(self):
        ae = self.assertEqual
        t = cql.Token.TRUE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "true")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"true\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_197_(self):
        ae = self.assertEqual
        t = cql.Token.TYPE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "type")
        ae(t[1], frozenset())
        ae(t[2], 140)
        ae(t[3], r"type\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_198_(self):
        ae = self.assertEqual
        t = cql.Token.UP
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "up")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"up\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_199_(self):
        ae = self.assertEqual
        t = cql.Token.VARIATION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "variation")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"variation\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_200_(self):
        ae = self.assertEqual
        t = cql.Token.VERTICAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "vertical")
        ae({v.value for v in t[1]}, {"accept_range"})
        ae(t[2], 200)
        ae(t[3], r"vertical\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_201_(self):
        ae = self.assertEqual
        t = cql.Token.VIRTUALMAINLINE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "virtualmainline")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"virtualmainline\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_202_(self):
        ae = self.assertEqual
        t = cql.Token.WHITE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "white")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"white\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_203_(self):
        ae = self.assertEqual
        t = cql.Token.WTM
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "wtm")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"wtm\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_204_(self):
        ae = self.assertEqual
        t = cql.Token.XRAY
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "xray")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 140)
        ae(t[3], r"xray\s*\(")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_205_(self):
        ae = self.assertEqual
        t = cql.Token.YEAR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "year")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"year\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_206_(self):
        ae = self.assertEqual
        t = cql.Token.TILDE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "tilde")
        ae(t[1], frozenset())
        ae(t[2], 170)
        ae(t[3], r"~")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_207_(self):
        ae = self.assertEqual
        t = cql.Token.HASH
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "hash")
        ae({v.value for v in t[1]}, {"allowed_unary_minus"})
        ae(t[2], 140)
        ae(t[3], r"#")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_208_(self):
        ae = self.assertEqual
        t = cql.Token.COLON
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "colon")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 210)
        ae(t[3], r":")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set", "logical", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_209_(self):
        ae = self.assertEqual
        t = cql.Token.DOT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "dot")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"\.")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_210_(self):
        ae = self.assertEqual
        t = cql.Token.STAR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "star")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 130)
        ae(t[3], r"\*")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_211_(self):
        ae = self.assertEqual
        t = cql.Token.REPEATSTAR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "repeatstar")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 20)
        ae(t[3], r"{\*}")
        ae({v.value for v in t[4]}, {"line re symbols"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_212_(self):
        ae = self.assertEqual
        t = cql.Token.LEFTBRACE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftbrace")
        ae(
            {v.value for v in t[1]},
            {
                "halt_pop_chained_filters",
                "allowed_unary_minus",
                "parenthesized_arguments",
                "incomplete_if_on_stack",
            },
        )
        ae(t[2], 0)
        ae(t[3], r"{")
        ae({v.value for v in t[4]}, {"position", "logical", "numeric", "set"})
        ae({v.value for v in t[5]}, {"position", "logical", "numeric", "set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_213_(self):
        ae = self.assertEqual
        t = cql.Token.RIGHTBRACE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "rightbrace")
        ae({v.value for v in t[1]}, {"close_brace_or_parenthesis"})
        ae(t[2], 0)
        ae(t[3], r"}")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_214_(self):
        ae = self.assertEqual
        t = cql.Token.LEFTPARENTHESIS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftparenthesis")
        ae(
            {v.value for v in t[1]},
            {
                "halt_pop_chained_filters",
                "parenthesized_arguments",
                "allowed_unary_minus",
            },
        )
        ae(t[2], 0)
        ae(t[3], r"\(")
        ae({v.value for v in t[4]}, {"logical", "set", "numeric", "position"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_215_(self):
        ae = self.assertEqual
        t = cql.Token.RIGHTPARENTHESIS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "rightparenthesis")
        ae({v.value for v in t[1]}, {"close_brace_or_parenthesis"})
        ae(t[2], 0)
        ae(t[3], r"\)")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_216_(self):
        ae = self.assertEqual
        t = cql.Token.INTERSECTION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "intersection")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 160)
        ae(t[3], r"&")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"position", "set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_217_(self):
        ae = self.assertEqual
        t = cql.Token.LT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "lt")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"<")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_218_(self):
        ae = self.assertEqual
        t = cql.Token.LE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "le")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"<=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_219_(self):
        ae = self.assertEqual
        t = cql.Token.GT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "gt")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r">")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_220_(self):
        ae = self.assertEqual
        t = cql.Token.GE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ge")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r">=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_221_(self):
        ae = self.assertEqual
        t = cql.Token.ASSIGN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "assign")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 40)
        ae(t[3], r"=\??")
        ae({v.value for v in t[4]}, {"set", "numeric", "position"})
        ae({v.value for v in t[5]}, {"set", "numeric", "position"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_222_(self):
        ae = self.assertEqual
        t = cql.Token.EQ
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "eq")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"==")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_223_(self):
        ae = self.assertEqual
        t = cql.Token.NE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ne")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"!=")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_224_(self):
        ae = self.assertEqual
        t = cql.Token.PLUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "plus")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 110)
        ae(t[3], r"\+")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_225_(self):
        ae = self.assertEqual
        t = cql.Token.REPEATPLUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "repeatplus")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 20)
        ae(t[3], r"{\+}")
        ae({v.value for v in t[4]}, {"line re symbols"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_226_(self):
        ae = self.assertEqual
        t = cql.Token.MINUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "minus")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 110)
        ae(t[3], r"-")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_227_(self):
        ae = self.assertEqual
        t = cql.Token.MODULUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "modulus")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 130)
        ae(t[3], r"%")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_228_(self):
        ae = self.assertEqual
        t = cql.Token.DIVIDE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "divide")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 130)
        ae(t[3], r"/")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_229_(self):
        ae = self.assertEqual
        t = cql.Token.UNION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "union")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 150)
        ae(t[3], r"\|")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_230_(self):
        ae = self.assertEqual
        t = cql.Token.IPPLUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ipplus")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 100)
        ae(t[3], r"\+=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_231_(self):
        ae = self.assertEqual
        t = cql.Token.IPMINUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ipminus")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 100)
        ae(t[3], r"-=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_232_(self):
        ae = self.assertEqual
        t = cql.Token.IPMULTIPLY
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ipmultiply")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 100)
        ae(t[3], r"\*=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_233_(self):
        ae = self.assertEqual
        t = cql.Token.IPDIVIDE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ipdivide")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 100)
        ae(t[3], r"/=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_234_(self):
        ae = self.assertEqual
        t = cql.Token.IPMODULUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ipmodulus")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 100)
        ae(t[3], r"%=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_235_(self):
        ae = self.assertEqual
        t = cql.Token.LEFTARROW
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftarrow")
        ae({v.value for v in t[1]}, {"no_arithmetic_filters"})
        ae(t[2], 10)
        ae(t[3], r"<--")
        ae({v.value for v in t[4]}, {"line parameter"})
        ae(
            {v.value for v in t[5]},
            {"line re symbols", "numeric", "logical", "set", "position"},
        )
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_236_(self):
        ae = self.assertEqual
        t = cql.Token.RIGHTARROW
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "rightarrow")
        ae({v.value for v in t[1]}, {"no_arithmetic_filters"})
        ae(t[2], 10)
        ae(t[3], r"-->")
        ae({v.value for v in t[4]}, {"line parameter"})
        ae(
            {v.value for v in t[5]},
            {"line re symbols", "numeric", "logical", "set", "position"},
        )
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_237_(self):
        ae = self.assertEqual
        t = cql.Token.EOLCOMMENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "eolcomment")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"//.*(?:\n|\Z)")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_238_(self):
        ae = self.assertEqual
        t = cql.Token.BLOCKCOMMENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "blockcomment")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"/\*[\S|\s]*\*/")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_239_(self):
        ae = self.assertEqual
        t = cql.Token.NUMBER
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "x")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "allowed_unary_minus"},
        )
        ae(t[2], 0)
        ae(t[3], r"[0-9]+")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_240_(self):
        ae = self.assertEqual
        t = cql.Token.VARIABLE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "y")
        ae(
            {v.value for v in t[1]},
            {
                "allowed_top_stack_at_end",
                "assign_to_variable",
                "allowed_unary_minus",
            },
        )
        ae(t[2], 0)
        ae(t[3], r"[$A-Z_a-z][$0-9A-Z_a-z]*\b")
        ae({v.value for v in t[4]}, {"unset variable"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_241_(self):
        ae = self.assertEqual
        t = cql.Token.BADTOKEN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "z")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"\S+")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_242_(self):
        ae = self.assertEqual
        t = cql.Token.FIRSTMATCH
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "firstmatch")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"firstmatch\b")
        ae({v.value for v in t[4]}, {"line parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_243_(self):
        ae = self.assertEqual
        t = cql.Token.LASTPOSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "lastposition")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"lastposition\b")
        ae({v.value for v in t[4]}, {"line parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_244_(self):
        ae = self.assertEqual
        t = cql.Token.SINGLECOLOR
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "singlecolor")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"singlecolor\b")
        ae({v.value for v in t[4]}, {"line parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_245_(self):
        ae = self.assertEqual
        t = cql.Token.NESTBAN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "nestban")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"nestban\b")
        ae({v.value for v in t[4]}, {"line parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_246_(self):
        ae = self.assertEqual
        t = cql.Token.PRIMARY
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "primary")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"primary\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_247_(self):
        ae = self.assertEqual
        t = cql.Token.SECONDARY
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "secondary")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"secondary\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_248_(self):
        ae = self.assertEqual
        t = cql.Token.OUTPUT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "output")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"output\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_249_(self):
        ae = self.assertEqual
        t = cql.Token.INPUT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "input_")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"input\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_250_(self):
        ae = self.assertEqual
        t = cql.Token.MATCHCOUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "matchcount")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"matchcount\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_251_(self):
        ae = self.assertEqual
        t = cql.Token.SILENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "silent")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"silent\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_252_(self):
        ae = self.assertEqual
        t = cql.Token.VARIATIONS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "variations")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"variations\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_253_(self):
        ae = self.assertEqual
        t = cql.Token.MATCHSTRING
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "matchstring")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"matchstring\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_254_(self):
        ae = self.assertEqual
        t = cql.Token.COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "count")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"count\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_255_(self):
        ae = self.assertEqual
        t = cql.Token.ALL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "all")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"all\b")
        ae({v.value for v in t[4]}, {"find parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_256_(self):
        ae = self.assertEqual
        t = cql.Token.PIECE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "piece")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"piece\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_257_(self):
        ae = self.assertEqual
        t = cql.Token.PIECE_ALL_IN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "pieceallin")
        ae(
            {v.value for v in t[1]},
            {"incomplete_if_on_stack", "halt_pop_no_body_filter"},
        )
        ae(t[2], 0)
        ae(t[3], r"piece\s+all\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_258_(self):
        ae = self.assertEqual
        t = cql.Token.SQUARE_ALL_IN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "squareallin")
        ae(
            {v.value for v in t[1]},
            {"incomplete_if_on_stack", "halt_pop_no_body_filter"},
        )
        ae(t[2], 0)
        ae(t[3], r"square\s+all\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_259_(self):
        ae = self.assertEqual
        t = cql.Token.SQUARE_IN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "squarein")
        ae(
            {v.value for v in t[1]},
            {"incomplete_if_on_stack", "halt_pop_no_body_filter"},
        )
        ae(t[2], 0)
        ae(t[3], r"square\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_260_(self):
        ae = self.assertEqual
        t = cql.Token.QUIET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "quiet")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"quiet\b")
        ae({v.value for v in t[4]}, {"consecutivemoves parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_261_(self):
        ae = self.assertEqual
        t = cql.Token.CAPTURE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "capture")
        ae({v.value for v in t[1]}, {"parameter_takes_argument"})
        ae(t[2], 190)
        ae(t[3], r"capture\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_262_(self):
        ae = self.assertEqual
        t = cql.Token.CASTLE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "castle")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"castle\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_263_(self):
        ae = self.assertEqual
        t = cql.Token.ENPASSANT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "enpassant")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"enpassant\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_264_(self):
        ae = self.assertEqual
        t = cql.Token.ENPASSANT_SQUARE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "enpassantsquare")
        ae({v.value for v in t[1]}, {"parameter_takes_argument"})
        ae(t[2], 190)
        ae(t[3], r"enpassantsquare\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_265_(self):
        ae = self.assertEqual
        t = cql.Token.FROM
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "from_")
        ae({v.value for v in t[1]}, {"parameter_takes_argument"})
        ae(t[2], 190)
        ae(t[3], r"from\b")
        ae({v.value for v in t[4]}, {"move parameter", "pin parameter"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_266_(self):
        ae = self.assertEqual
        t = cql.Token.LEGAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "legal")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"legal\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_267_(self):
        ae = self.assertEqual
        t = cql.Token.NULL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "null")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"null\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_268_(self):
        ae = self.assertEqual
        t = cql.Token.OO
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "oo")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"o-o\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_269_(self):
        ae = self.assertEqual
        t = cql.Token.OOO
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ooo")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"o-o-o\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_270_(self):
        ae = self.assertEqual
        t = cql.Token.PREVIOUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "previous")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"previous\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_271_(self):
        ae = self.assertEqual
        t = cql.Token.PROMOTE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "promote")
        ae({v.value for v in t[1]}, {"parameter_takes_argument"})
        ae(t[2], 0)
        ae(t[3], r"promote\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_272_(self):
        ae = self.assertEqual
        t = cql.Token.PSEUDOLEGAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "pseudolegal")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"pseudolegal\b")
        ae({v.value for v in t[4]}, {"move parameter"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_273_(self):
        ae = self.assertEqual
        t = cql.Token.THROUGH
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "through")
        ae({v.value for v in t[1]}, {"parameter_takes_argument"})
        ae(t[2], 190)
        ae(t[3], r"through\b")
        ae({v.value for v in t[4]}, {"pin parameter"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_274_(self):
        ae = self.assertEqual
        t = cql.Token.TO
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "to")
        ae({v.value for v in t[1]}, {"parameter_takes_argument"})
        ae(t[2], 190)
        ae(t[3], r"to\b")
        ae({v.value for v in t[4]}, {"move parameter", "pin parameter"})
        ae({v.value for v in t[5]}, {"set"})
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_275_(self):
        ae = self.assertEqual
        t = cql.Token.REPEATRANGE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "repeatrange")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 20)
        ae(t[3], r"\s*{\s*[1-9][0-9]*(?:\s+[1-9][0-9]*)?\s*}")
        ae({v.value for v in t[4]}, {"line re symbols"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)


class CQL_PATTERN(unittest.TestCase):
    def test_01_cql_pattern(self):
        ae = self.assertEqual
        ae(
            cql.CQL_PATTERN,
            r"".join(
                (
                    r"(?:(?P<consecutivemoves>consecutivemoves\b)|",
                    r"(?P<rightparenthesis>\))|",
                    r"(?P<currentposition>currentposition\b)|",
                    r"(?P<enpassantsquare>enpassantsquare\b)|",
                    r"(?P<leftparenthesis>\()|",
                    r"(?P<pieceassignment>piece\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+=)|",
                    r"(?P<piecedesignator>",
                    r"(?:(?:[a-h](?:-[a-h])?[1-8](?:-[1-8])?|\[[a-h]",
                    r"(?:-[a-h])?[1-8](?:-[1-8])?(?:,[a-h](?:-[a-h])?[1-8]",
                    r"(?:-[1-8])?)*])|(?:(?:[KQRBNPkqrbnpAa_]|\[",
                    "(?:[KQRBNPkqrbnpAa_]+)])(?:[a-h](?:-[a-h])?[1-8]",
                    r"(?:-[1-8])?|\[[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r"(?:,[a-h](?:-[a-h])?[1-8](?:-[1-8])?)*]))|\[",
                    r"(?:[KQRBNPkqrbnpAa_]+)])(?![a-zA-Z0-9_[\]])|",
                    r"[KQRBNPkqrbnpAa_]\b)",
                    r"|",
                    r"(?P<shifthorizontal>shifthorizontal(?:\s+count)?\b)|",
                    r"(?P<virtualmainline>virtualmainline\b)|",
                    r"(?P<connectedpawns>connectedpawns\b)|",
                    r"(?P<fliphorizontal>fliphorizontal(?:\s+count)?\b)|",
                    r"(?P<isolatedpawns>isolatedpawns\b)|",
                    r"(?P<shiftvertical>shiftvertical(?:\s+count)?\b)|",
                    r"(?P<anydirection>anydirection\b)|",
                    r"(?P<blockcomment>/\*[\S|\s]*\*/)|",
                    r"(?P<doubledpawns>doubledpawns\b)|",
                    r"(?P<flipvertical>flipvertical(?:\s+count)?\b)|",
                    r"(?P<intersection>&)|",
                    r"(?P<lastposition>lastposition\b)|",
                    r"(?P<reversecolor>reversecolor\b)|",
                    r"(?P<matchstring>matchstring\b)|",
                    r"(?P<notransform>notransform\b)|",
                    r"(?P<passedpawns>passedpawns\b)|",
                    r"(?P<pseudolegal>pseudolegal\b)|",
                    r"(?P<repeatrange>\s*{\s*[1-9][0-9]*(?:\s+[1-9][0-9]*)?\s*})|",
                    r"(?P<singlecolor>singlecolor\b)|",
                    r"(?P<squareallin>",
                    r"square\s+all\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b)|",
                    r"(?P<attackedby>attackedby\b)|",
                    r"(?P<descendant>descendant\s*\()|",
                    r"(?P<eolcomment>//.*(?:\n|\Z))|",
                    r"(?P<firstmatch>firstmatch\b)|",
                    r"(?P<gamenumber>gamenumber\b)|",
                    r'(?P<hascomment>hascomment\s+(?:"((?:[^\\"]|\\.)*)"))|',
                    r"(?P<horizontal>horizontal\b)|",
                    r"(?P<ipmultiply>\*=)|",
                    r"(?P<makesquare>makesquare\s*\()|",
                    r"(?P<matchcount>matchcount\b)|",
                    r"(?P<movenumber>movenumber\b)|",
                    r"(?P<orthogonal>orthogonal\b)|",
                    r"(?P<persistent>persistent\b)|",
                    r"(?P<pieceallin>",
                    r"piece\s+all\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b)|",
                    r"(?P<positionid>positionid\b)|",
                    r"(?P<repeatplus>{\+})|",
                    r"(?P<repeatstar>{\*})|",
                    r"(?P<rightarrow>-->)|",
                    r"(?P<rightbrace>})|",
                    r"(?P<sidetomove>sidetomove\b)|",
                    r"(?P<variations>variations\b)|",
                    r"(?P<colortype>colortype\b)|",
                    r"(?P<enpassant>enpassant\b)|",
                    r"(?P<flipcolor>flipcolor(?:\s+count)?\b)|",
                    r"(?P<ipmodulus>%=)|",
                    r"(?P<leftarrow><--)|",
                    r"(?P<leftbrace>{)|",
                    r"(?P<northeast>northeast\b)|",
                    r"(?P<northwest>northwest\b)|",
                    r"(?P<secondary>secondary\b)|",
                    r"(?P<southeast>southeast\b)|",
                    r"(?P<southwest>southwest\b)|",
                    r"(?P<stalemate>stalemate\b)|",
                    r"(?P<variation>variation\b)|",
                    r"(?P<ancestor>ancestor\s*\()|",
                    r"(?P<diagonal>diagonal\b)|",
                    r"(?P<distance>distance\s*\()|",
                    r"(?P<function>function\s+([$A-Z_a-z][$0-9A-Z_a-z]*)\s*\(",
                    r"\s*([$A-Z_a-z][$0-9A-Z_a-z]*",
                    r"(?:\s[$A-Z_a-z][$0-9A-Z_a-z]*)*)\s*\)\s*{)|",
                    r"(?P<ipdivide>/=)|",
                    r"(?P<mainline>mainline\b)|",
                    r"(?P<position>position\b)|",
                    r"(?P<previous>previous\b)|",
                    r"(?P<rotate45>rotate45(?:\s+count)?\b)|",
                    r"(?P<rotate90>rotate90(?:\s+count)?\b)|",
                    r"(?P<squarein>square\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b)|",
                    r"(?P<terminal>terminal\b)|",
                    r"(?P<vertical>vertical\b)|",
                    r"(?P<attacks>attacks\b)|",
                    r"(?P<between>between\s*\()|",
                    r"(?P<capture>capture\b)|",
                    r"(?P<comment>comment(?:\s*\()?)|",
                    r"(?P<initial>initial\b)|",
                    r"(?P<ipminus>-=)|",
                    r"(?P<message>message(?:\s*\()?)|",
                    r"(?P<modulus>%)|",
                    r"(?P<nestban>nestban\b)|",
                    r"(?P<pieceid>pieceid\b)|",
                    r"(?P<piecein>piece\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b)|",
                    r"(?P<primary>primary\b)|",
                    r"(?P<promote>promote\b)|",
                    r"(?P<through>through\b)|",
                    r"(?P<assign>=\??)|",
                    r"(?P<castle>castle\b)|",
                    r"(?P<divide>/)|",
                    r"(?P<input_>input\b)|",
                    r"(?P<ipplus>\+=)|",
                    r"(?P<output>output\b)|",
                    r"(?P<parent>parent\b)|",
                    r"(?P<player>player\s+(?:(?:black|white)\s+)?",
                    r'(?:"((?:[^\\"]|\\.)*)"))|',
                    r"(?P<result>result(?:\s+",
                    r'(?:(?:1-0|0-1|1/2-1/2)|"(?:1-0|0-1|1/2-1/2)")))|',
                    r"(?P<silent>silent\b)|",
                    r"(?P<square>square\b)|",
                    r"(?P<black>black\b)|",
                    r"(?P<check>check\b)|",
                    r"(?P<child>child(?:\s*\()?)|",
                    r"(?P<colon>:)|",
                    r"(?P<count>count\b)|",
                    r"(?P<depth>depth\b)|",
                    r"(?P<else_>else\b)|",
                    r'(?P<event>event\s+(?:"((?:[^\\"]|\\.)*)"))|',
                    r"(?P<false>false\b)|",
                    r"(?P<from_>from\b)|",
                    r"(?P<legal>legal\b)|",
                    r"(?P<light>light\b)|",
                    r"(?P<minus>-)|",
                    r"(?P<piece>piece\b)|",
                    r"(?P<power>power\b)|",
                    r"(?P<query>\?)|",
                    r"(?P<quiet>quiet\b)|",
                    r"(?P<right>right\b)|",
                    r"(?P<shift>shift(?:\s+count)?\b)|",
                    r"(?P<tilde>~)|",
                    r"(?P<union>\|)|",
                    r"(?P<white>white\b)|",
                    r"(?P<and_>and\b)|",
                    r"(?P<dark>dark\b)|",
                    r"(?P<down>down\b)|",
                    r"(?P<echo>echo\s+\(\s*[$A-Z_a-z][$0-9A-Z_a-z]*",
                    r"\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s*\)\s*(?:in\s+all\b)?)|",
                    r"(?P<file>file\b)|",
                    r"(?P<find>find\b)|",
                    r"(?P<flip>flip(?:\s+count)?\b)|",
                    r"(?P<hash>#)|",
                    r"(?P<left>left\b)|",
                    r"(?P<line>line\b)|",
                    r"(?P<loop>loop\b)|",
                    r"(?P<mate>mate\b)|",
                    r"(?P<move>move\b)|",
                    r"(?P<not_>not\b)|",
                    r"(?P<null>null\b)|",
                    r"(?P<plus>\+)|",
                    r"(?P<rank>rank\b)|",
                    r'(?P<site>site\s+(?:"((?:[^\\"]|\\.)*)"))|',
                    r'(?P<sort>sort(?:\s+min)?(?:\s+"((?:[^\\"]|\\.)*)")?)|',
                    r"(?P<sqrt>sqrt\b)|",
                    r"(?P<star>\*)|",
                    r"(?P<then>then\b)|",
                    r"(?P<true>true\b)|",
                    r"(?P<type>type\b)|",
                    r"(?P<xray>xray\s*\()|",
                    r"(?P<year>year\b)|",
                    r"(?P<abs>abs\b)|",
                    r"(?P<all>all\b)|",
                    r"(?P<btm>btm\b)|",
                    r"(?P<cql>cql(?:\s*\(\s*(?:(?:(?:output|input)\s+\S+\.pgn|(?:",
                    r"sort\s+)?matchcount(?:\s+[0-9]+){,2}|gamenumber(?:",
                    r"\s+[0-9]+){,2}|result\s+(?:1-0|1/2-1/2|0-1",
                    r')|silent|quiet|variations|matchstring\s+"(?:',
                    r'[^\\"]|\\.)*")\s+)*\)\s*)?)|',
                    r"(?P<dot>\.)|",
                    r"(?P<elo>elo(?:\s+(?:black|white))?\b)|",
                    r'(?P<fen>fen\s+"[^"]*")|',
                    r"(?P<if_>if\b)|",
                    r"(?P<in_>in\b)|",
                    r"(?P<lca>lca\s*\()|",
                    r"(?P<max>max\s*\()|",
                    r"(?P<min>min\s*\()|",
                    r"(?P<ooo>o-o-o\b)|",
                    r"(?P<or_>or\b)|",
                    r"(?P<pin>pin\b)|",
                    r"(?P<ply>ply\b)|",
                    r"(?P<ray>ray(?:\s+(?:up|down|right|left|northeast|north",
                    r"west|southeast|southwest|diagonal|orthogonal|vert",
                    r"ical|horizontal|anydirection))*\s*\()|",
                    r"(?P<wtm>wtm\b)|",
                    r"(?P<eq>==)|",
                    r"(?P<ge>>=)|",
                    r"(?P<gt>>)|",
                    r"(?P<le><=)|",
                    r"(?P<lt><)|",
                    r"(?P<ne>!=)|",
                    r"(?P<oo>o-o\b)|",
                    r"(?P<to>to\b)|",
                    r"(?P<up>up\b)|",
                    r"(?P<x>[0-9]+)|",
                    r"(?P<y>[$A-Z_a-z][$0-9A-Z_a-z]*\b)|",
                    r"(?P<z>\S+))",
                    r"(?:\s*|\Z)",
                )
            ),
        )

    def test_02_cql_pattern(self):
        ae = self.assertEqual
        ae(isinstance(re.compile(cql.CQL_PATTERN), re.Pattern), True)


class ModuleConstants(unittest.TestCase):
    def test_01_(self):
        ae = self.assertEqual
        ae(len([a for a in dir(cql) if not a.startswith("__")]), 76)
        ae(
            sorted([a for a in dir(cql) if not a.startswith("__")]),
            [
                "ASSIGNMENT_VARIABLE_TYPES",
                "CHILD_NO_ARGUMENT",
                "CONSECUTIVEMOVES_LEFTPARENTHESIS",
                "CQL_DIRECTIONS",
                "CQL_PATTERN",
                "CQL_RESERVED_VARIABLE_NAME_PREFIX",
                "CQL_TOKENS",
                "ECHO_IN_ALL",
                "ELO_BLACK",
                "ELO_WHITE",
                "EQ_BOTH_SETS",
                "EQ_POSITION",
                "EQ_SET",
                "Enum",
                "FIND_NUMERIC",
                "FLIPCOLOR_COUNT",
                "FLIPHORIZONTAL_COUNT",
                "FLIPVERTICAL_COUNT",
                "FLIP_COUNT",
                "FUNCTION_CALL",
                "FUNCTION_NAME",
                "Flags",
                "GE_POSITION",
                "GE_SET",
                "GT_POSITION",
                "GT_SET",
                "IF_LOGICAL",
                "IF_NUMERIC",
                "IF_POSITION",
                "IF_SET",
                "INTERSECTION_POSITION",
                "INTERSECTION_SET",
                "LEFTBRACE_LOGICAL",
                "LEFTBRACE_NUMBER",
                "LEFTBRACE_POSITION",
                "LEFTBRACE_SET",
                "LEFTPARENTHESIS_LOGICAL",
                "LEFTPARENTHESIS_NUMBER",
                "LEFTPARENTHESIS_POSITION",
                "LEFTPARENTHESIS_SET",
                "LE_POSITION",
                "LE_SET",
                "LINE_LEFTARROW",
                "LINE_RIGHTARROW",
                "LT_POSITION",
                "LT_SET",
                "MOVE_SET",
                "NE_BOTH_SETS",
                "NE_POSITION",
                "NE_SET",
                "NUMERIC_VARIABLE",
                "PIECE_VARIABLE",
                "PLAYER_BLACK",
                "PLAYER_WHITE",
                "POSITION_VARIABLE",
                "QUOTED_STRING",
                "RANGE",
                "ROTATE45_COUNT",
                "ROTATE90_COUNT",
                "SET_VARIABLE",
                "SHIFTHORIZONTAL_COUNT",
                "SHIFTVERTICAL_COUNT",
                "SHIFT_COUNT",
                "SINGLE_COMMENT_ARGUMENT",
                "SINGLE_MESSAGE_ARGUMENT",
                "SORT_MIN",
                "Token",
                "TokenDefinition",
                "TokenTypes",
                "UNARY_MINUS",
                "constants",
                "map_filter_assign_to_variable",
                "map_filter_to_leftparenthesis",
                "map_filter_type_to_leftbrace_type",
                "map_filter_type_to_leftparenthesis_type",
                "namedtuple",
            ],
        )
        ae(cql.CQL_RESERVED_VARIABLE_NAME_PREFIX, "__CQL")

    def test_02_(self):
        ae = self.assertEqual
        t = cql.ECHO_IN_ALL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "echo_in_all")
        ae(
            {v.value for v in t[1]},
            {"incomplete_if_on_stack", "halt_pop_no_body_filter"},
        )
        ae(t[2], 0)
        ae(t[3], r"in\s+all\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_03_(self):
        ae = self.assertEqual
        t = cql.FLIP_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "flip_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_04_(self):
        ae = self.assertEqual
        t = cql.FLIPCOLOR_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "flipcolor_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_05_(self):
        ae = self.assertEqual
        t = cql.FLIPHORIZONTAL_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "fliphorizontal_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_06_(self):
        ae = self.assertEqual
        t = cql.FLIPVERTICAL_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "flipvertical_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_07_(self):
        ae = self.assertEqual
        t = cql.ROTATE45_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "rotate45_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_08_(self):
        ae = self.assertEqual
        t = cql.ROTATE90_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "rotate90_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_09_(self):
        ae = self.assertEqual
        t = cql.SHIFT_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "shift_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_10_(self):
        ae = self.assertEqual
        t = cql.SHIFTHORIZONTAL_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "shifthorizontal_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_11_(self):
        ae = self.assertEqual
        t = cql.SHIFTVERTICAL_COUNT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "shiftvertical_count")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"\s+count\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_14_(self):
        ae = self.assertEqual
        t = cql.RANGE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "range_")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"(?:\s+[0-9]+){,2}")
        ae(t[4], None)
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_16_(self):
        ae = self.assertEqual
        ae(
            {v for v in cql.ASSIGNMENT_VARIABLE_TYPES},
            {
                cql.SET_VARIABLE,
                cql.POSITION_VARIABLE,
                cql.NUMERIC_VARIABLE,
                cql.PIECE_VARIABLE,
            },
        )

    def test_18_(self):
        ae = self.assertEqual
        ae(
            [v for v in sorted(cql.map_filter_assign_to_variable.items())],
            [
                (
                    frozenset((cql.TokenTypes.NUMERIC_FILTER,)),
                    cql.NUMERIC_VARIABLE,
                ),
                (
                    frozenset((cql.TokenTypes.POSITION_FILTER,)),
                    cql.POSITION_VARIABLE,
                ),
                (frozenset((cql.TokenTypes.SET_FILTER,)), cql.SET_VARIABLE),
            ],
        )

    def test_21_(self):
        ae = self.assertEqual
        t = cql.FUNCTION_CALL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "function_call")
        ae(
            {v.value for v in t[1]},
            {"parenthesized_arguments", "halt_pop_chained_filters"},
        )
        ae(t[2], 0)
        ae(t[3], r"[$A-Z_a-z][$0-9A-Z_a-z]*\b")
        ae(t[4], frozenset())
        ae({v.value for v in t[5]}, {"set", "position", "numeric", "logical"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_22_(self):
        ae = self.assertEqual
        t = cql.FUNCTION_NAME
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "function_name")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"[$A-Z_a-z][$0-9A-Z_a-z]*\b")
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_23_(self):
        ae = self.assertEqual
        t = cql.NUMERIC_VARIABLE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "y")
        ae(
            {v.value for v in t[1]},
            {
                "allowed_top_stack_at_end",
                "assign_to_variable",
                "allowed_unary_minus",
            },
        )
        ae(t[2], 0)
        ae(t[3], r"[$A-Z_a-z][$0-9A-Z_a-z]*\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(t[6], "numeric_variable")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_24_(self):
        ae = self.assertEqual
        t = cql.PIECE_VARIABLE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "y")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "assign_to_variable"},
        )
        ae(t[2], 0)
        ae(t[3], r"[$A-Z_a-z][$0-9A-Z_a-z]*\b")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(t[6], "piece_variable")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_25_(self):
        ae = self.assertEqual
        t = cql.POSITION_VARIABLE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "y")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "assign_to_variable"},
        )
        ae(t[2], 0)
        ae(t[3], r"[$A-Z_a-z][$0-9A-Z_a-z]*\b")
        ae({v.value for v in t[4]}, {"position"})
        ae(t[5], frozenset())
        ae(t[6], "position_variable")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_26_(self):
        ae = self.assertEqual
        t = cql.SET_VARIABLE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "y")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "assign_to_variable"},
        )
        ae(t[2], 0)
        ae(t[3], r"[$A-Z_a-z][$0-9A-Z_a-z]*\b")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(t[6], "set_variable")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_29_(self):
        ae = self.assertEqual
        t = cql.ELO_BLACK
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "elo_black")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"black\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_30_(self):
        ae = self.assertEqual
        t = cql.ELO_WHITE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "elo_white")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"white\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_31_(self):
        ae = self.assertEqual
        t = cql.PLAYER_BLACK
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "player_black")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"black\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_32_(self):
        ae = self.assertEqual
        t = cql.PLAYER_WHITE
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "player_white")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"white\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_33_(self):
        ae = self.assertEqual
        t = cql.SORT_MIN
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "sort_min")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"min\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_34_(self):
        ae = self.assertEqual
        t = cql.QUOTED_STRING
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "string")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r'(sort)(\s+min)?(\s+"(?:[^\\"]|\\.)*")?')
        ae(t[4], frozenset())
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_37_(self):
        ae = self.assertEqual
        t = cql.FIND_NUMERIC
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "find_numeric")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"find\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "logical", "position", "numeric"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_38_(self):
        ae = self.assertEqual
        t = cql.MOVE_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "move_set")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "end_filter_non_parameter"},
        )
        ae(t[2], 0)
        ae(t[3], r"move\b")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"move parameter"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_39_(self):
        ae = self.assertEqual
        t = cql.CHILD_NO_ARGUMENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "child_no_argument")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"child(?:\s*\()?")
        ae({v.value for v in t[4]}, {"position"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_40_(self):
        ae = self.assertEqual
        t = cql.SINGLE_MESSAGE_ARGUMENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "single_message_argument")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"message(?:\s*\()?")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_41_(self):
        ae = self.assertEqual
        t = cql.SINGLE_COMMENT_ARGUMENT
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "single_comment_argument")
        ae(t[1], frozenset())
        ae(t[2], 0)
        ae(t[3], r"comment(?:\s*\()?")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"logical", "set", "numeric", "position"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_42_(self):
        ae = self.assertEqual
        ae(
            cql.CQL_DIRECTIONS,
            {
                cql.Token.UP: {cql.Token.UP},
                cql.Token.DOWN: {cql.Token.DOWN},
                cql.Token.RIGHT: {cql.Token.RIGHT},
                cql.Token.LEFT: {cql.Token.LEFT},
                cql.Token.NORTHEAST: {cql.Token.NORTHEAST},
                cql.Token.NORTHWEST: {cql.Token.NORTHWEST},
                cql.Token.SOUTHEAST: {cql.Token.SOUTHEAST},
                cql.Token.SOUTHWEST: {cql.Token.SOUTHWEST},
                cql.Token.DIAGONAL: {
                    cql.Token.NORTHEAST,
                    cql.Token.NORTHWEST,
                    cql.Token.SOUTHEAST,
                    cql.Token.SOUTHWEST,
                },
                cql.Token.ORTHOGONAL: {
                    cql.Token.UP,
                    cql.Token.DOWN,
                    cql.Token.RIGHT,
                    cql.Token.LEFT,
                },
                cql.Token.VERTICAL: {cql.Token.UP, cql.Token.DOWN},
                cql.Token.HORIZONTAL: {cql.Token.RIGHT, cql.Token.LEFT},
                cql.Token.ANYDIRECTION: {
                    cql.Token.UP,
                    cql.Token.DOWN,
                    cql.Token.RIGHT,
                    cql.Token.LEFT,
                    cql.Token.NORTHEAST,
                    cql.Token.NORTHWEST,
                    cql.Token.SOUTHEAST,
                    cql.Token.SOUTHWEST,
                },
            },
        )

    def test_43_(self):
        ae = self.assertEqual
        t = cql.LINE_LEFTARROW
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "line_leftarrow")
        ae({v.value for v in t[1]}, {"halt_pop_chained_filters", "line_frame"})
        ae(t[2], 0)
        ae(t[3], r"line\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"line leftarrow parameter"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_44_(self):
        ae = self.assertEqual
        t = cql.LINE_RIGHTARROW
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "line_rightarrow")
        ae({v.value for v in t[1]}, {"halt_pop_chained_filters", "line_frame"})
        ae(t[2], 0)
        ae(t[3], r"line\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"line rightarrow parameter"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_45_(self):
        ae = self.assertEqual
        t = cql.CONSECUTIVEMOVES_LEFTPARENTHESIS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "consecutivemoves_leftparenthesis")
        ae(
            {v.value for v in t[1]},
            {"halt_pop_chained_filters", "parenthesized_arguments"},
        )
        ae(t[2], 0)
        ae(t[3], r"consecutivemoves\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position variable"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_46_(self):
        ae = self.assertEqual
        t = cql.INTERSECTION_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "intersection_position")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 160)
        ae(t[3], r"&")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"position"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_47_(self):
        ae = self.assertEqual
        t = cql.INTERSECTION_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "intersection_set")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 160)
        ae(t[3], r"&")
        ae({v.value for v in t[4]}, {"set"})
        ae({v.value for v in t[5]}, {"set"})
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_48_(self):
        ae = self.assertEqual
        t = cql.UNARY_MINUS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "minus")
        ae(t[1], frozenset())
        ae(t[2], 120)
        ae(t[3], r"-")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric", "numeral"})
        ae(t[6], "unary_minus")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_50_(self):
        ae = self.assertEqual
        t = cql.LEFTBRACE_NUMBER
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftbrace_number")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "allowed_unary_minus"},
        )
        ae(t[2], 0)
        ae(t[3], r"{")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_51_(self):
        ae = self.assertEqual
        t = cql.LEFTBRACE_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftbrace_position")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"{")
        ae({v.value for v in t[4]}, {"position"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_52_(self):
        ae = self.assertEqual
        t = cql.LEFTBRACE_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftbrace_set")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"{")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_53_(self):
        ae = self.assertEqual
        t = cql.LEFTBRACE_LOGICAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftbrace_logical")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"{")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_60_(self):
        ae = self.assertEqual
        t = cql.LEFTPARENTHESIS_NUMBER
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftparenthesis_number")
        ae(
            {v.value for v in t[1]},
            {"allowed_top_stack_at_end", "allowed_unary_minus"},
        )
        ae(t[2], 0)
        ae(t[3], r"\(")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_61_(self):
        ae = self.assertEqual
        t = cql.LEFTPARENTHESIS_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftparenthesis_position")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"\(")
        ae({v.value for v in t[4]}, {"position"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_62_(self):
        ae = self.assertEqual
        t = cql.LEFTPARENTHESIS_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftparenthesis_set")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"\(")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_63_(self):
        ae = self.assertEqual
        t = cql.LEFTPARENTHESIS_LOGICAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "leftparenthesis_logical")
        ae({v.value for v in t[1]}, {"allowed_top_stack_at_end"})
        ae(t[2], 0)
        ae(t[3], r"\(")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_70_(self):
        ae = self.assertEqual
        t = cql.LT_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "lt")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"<")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric"})
        ae(t[6], "lt_set")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_71_(self):
        ae = self.assertEqual
        t = cql.LE_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "le")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"<=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric"})
        ae(t[6], "le_set")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_72_(self):
        ae = self.assertEqual
        t = cql.GT_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "gt")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r">")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric"})
        ae(t[6], "gt_set")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_73_(self):
        ae = self.assertEqual
        t = cql.GE_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ge")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r">=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"numeric"})
        ae(t[6], "ge_set")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_74_(self):
        ae = self.assertEqual
        t = cql.EQ_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "eq")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"==")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"set", "numeric"})
        ae(t[6], "eq_set")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_75_(self):
        ae = self.assertEqual
        t = cql.EQ_BOTH_SETS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "eq_both_sets")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"==")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_76_(self):
        ae = self.assertEqual
        t = cql.NE_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ne")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"!=")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"set", "numeric"})
        ae(t[6], "ne_set")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_77_(self):
        ae = self.assertEqual
        t = cql.NE_BOTH_SETS
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ne_both_sets")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"!=")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(t[6], None)
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_80_(self):
        ae = self.assertEqual
        t = cql.LT_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "lt")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"<")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position"})
        ae(t[6], "lt_position")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_81_(self):
        ae = self.assertEqual
        t = cql.LE_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "le")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"<=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position"})
        ae(t[6], "le_position")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_82_(self):
        ae = self.assertEqual
        t = cql.GT_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "gt")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r">")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position"})
        ae(t[6], "gt_position")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_83_(self):
        ae = self.assertEqual
        t = cql.GE_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ge")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r">=")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position"})
        ae(t[6], "ge_position")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_84_(self):
        ae = self.assertEqual
        t = cql.EQ_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "eq")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"==")
        ae({v.value for v in t[4]}, {"numeric"})
        ae({v.value for v in t[5]}, {"position"})
        ae(t[6], "eq_position")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_85_(self):
        ae = self.assertEqual
        t = cql.NE_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "ne")
        ae({v.value for v in t[1]}, {"named_compound_filter"})
        ae(t[2], 90)
        ae(t[3], r"!=")
        ae({v.value for v in t[4]}, {"logical"})
        ae({v.value for v in t[5]}, {"position"})
        ae(t[6], "ne_position")
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_92_(self):
        ae = self.assertEqual
        t = cql.IF_LOGICAL
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "if_logical")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"if\b")
        ae({v.value for v in t[4]}, {"logical"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_93_(self):
        ae = self.assertEqual
        t = cql.IF_NUMERIC
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "if_numeric")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"if\b")
        ae({v.value for v in t[4]}, {"numeric"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_94_(self):
        ae = self.assertEqual
        t = cql.IF_POSITION
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "if_position")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"if\b")
        ae({v.value for v in t[4]}, {"position"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)

    def test_95_(self):
        ae = self.assertEqual
        t = cql.IF_SET
        ae(isinstance(t, cql.TokenDefinition), True)
        ae(len(t), 7)
        ae(t[0], "if_set")
        ae(t[1], frozenset())
        ae(t[2], 40)
        ae(t[3], r"if\b")
        ae({v.value for v in t[4]}, {"set"})
        ae(t[5], frozenset())
        ae(isinstance(re.compile(t[3]), re.Pattern), True)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(TokenDefinition))
    runner().run(loader(Flags))
    runner().run(loader(TokenTypes))
    runner().run(loader(Token))
    runner().run(loader(CQL_PATTERN))
    runner().run(loader(ModuleConstants))
