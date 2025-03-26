# test_elements.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Unittests for chessql.core.elements module.

Verify the values of constant attributes defined in ..elements module.
Changes in ..elements not done here too will be highlighted.
"""

import unittest

from .. import elements


class PatternAttributes(unittest.TestCase):
    def test_attributes(self):
        self.assertEqual(
            [a for a in sorted(dir(elements)) if a.isupper()],
            [
                "ABS",
                "AFTER_EQ",
                "AFTER_NE",
                "ALL",
                "ANCESTOR",
                "AND",
                "ANYDIRECTION",
                "ANYTHING_ELSE",
                "ANY_SQUARE",
                "ARROW_BACKWARD",
                "ARROW_FORWARD",
                "ASCII",
                "ASSERT",
                "ASSIGN",
                "ASSIGN_DIVIDE",
                "ASSIGN_IF",
                "ASSIGN_MINUS",
                "ASSIGN_MODULUS",
                "ASSIGN_MULTIPLY",
                "ASSIGN_PLUS",
                "ATOMIC",
                "ATTACKEDBY",
                "ATTACKED_ARROW",
                "ATTACKS",
                "ATTACK_ARROW",
                "BACKSLASH",
                "BEFORE_EQ",
                "BEFORE_NE",
                "BETWEEN",
                "BLACK",
                "BLOCK_COMMENT",
                "BRACE_LEFT",
                "BRACE_RIGHT",
                "BRACKET_LEFT",
                "BRACKET_RIGHT",
                "BTM",
                "CAPTURE",
                "CASTLE",
                "CHECK",
                "CHILD",
                "CHILD_PARENTHESES",
                "COLON",
                "COLORTYPE",
                "COMMENT",
                "COMMENT_PARENTHESES",
                "COMMENT_SYMBOL",
                "COMPLEMENT",
                "CONNECTEDPAWNS",
                "CONSECUTIVEMOVES",
                "COUNT",
                "COUNTMOVES",
                "COUNT_FILTER",
                "CQL",
                "CURRENTMOVE",
                "CURRENTPOSITION",
                "CURRENTTRANSFORM",
                "DARK",
                "DASH_II",
                "DASH_IR",
                "DASH_LI",
                "DASH_LR",
                "DATE",
                "DEPTH",
                "DESCENDANT",
                "DIAGONAL",
                "DICTIONARY",
                "DISTANCE",
                "DIVIDE",
                "DOUBLEDPAWNS",
                "DOWN",
                "ECHO",
                "ECO",
                "ELEMENT",
                "ELO",
                "ELSE",
                "EMPTY_SQUARE",
                "EMPTY_SQUARES",
                "END_OF_LINE",
                "END_OF_STREAM",
                "ENPASSANT",
                "ENPASSANTSQUARE",
                "EQ",
                "EVENT",
                "EVENTDATE",
                "EXISTENTIAL_PIECE_VARIABLE",
                "EXISTENTIAL_SQUARE_VARIABLE",
                "FALSE",
                "FEN",
                "FILE",
                "FIND",
                "FIRSTMATCH",
                "FLIP",
                "FLIPCOLOR",
                "FLIPHORIZONTAL",
                "FLIPVERTICAL",
                "FOCUS",
                "FOCUS_CAPTURE",
                "FORALL",
                "FROM",
                "FUNCTION",
                "FUNCTION_CALL",
                "GAMENUMBER",
                "GE",
                "GT",
                "HASCOMMENT",
                "HORIZONTAL",
                "IDEALMATE",
                "IDEALSTALEMATE",
                "IF",
                "IN",
                "INDEXOF",
                "INITIAL",
                "INITIALPOSITION",
                "INT",
                "INTEGER",
                "INTERSECTION",
                "IN_ALL",
                "ISBOUND",
                "ISOLATEDPAWNS",
                "ISUNBOUND",
                "KEEPALLBEST",
                "KEYWORD_ANYTHING_ELSE",
                "LASTGAMENUMBER",
                "LASTPOSITION",
                "LCA",
                "LE",
                "LEFT",
                "LEGAL",
                "LIGHT",
                "LINE",
                "LINE_COMMENT",
                "LOCAL",
                "LOOP",
                "LOWERCASE",
                "LT",
                "MAINDIAGONAL",
                "MAINLINE",
                "MAKESQUARE_PARENTHESES",
                "MAKESQUARE_STRING",
                "MATE",
                "MAX",
                "MAX_PARAMETER",
                "MESSAGE",
                "MESSAGE_PARENTHESES",
                "MIN",
                "MINUS",
                "MODELMATE",
                "MODELSTALEMATE",
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
                "NULLMOVE",
                "OFFDIAGONAL",
                "OO",
                "OOO",
                "OR",
                "ORIGINALCOMMENT",
                "ORTHOGONAL",
                "PARENT",
                "PARENTHESIS_LEFT",
                "PARENTHESIS_RIGHT",
                "PASSEDPAWNS",
                "PATH",
                "PATHCOUNT",
                "PATHCOUNTUNFOCUSED",
                "PATHLASTPOSITION",
                "PATHSTART",
                "PERSISTENT",
                "PERSISTENT_QUIET",
                "PIECE",
                "PIECEID",
                "PIECENAME",
                "PIECEPATH",
                "PIECE_DESIGNATOR",
                "PIECE_OPTIONS",
                "PIECE_VARIABLE",
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
                "PUREMATE",
                "PURESTALEMATE",
                "QUIET",
                "RANK",
                "RAY",
                "READFILE",
                "REGEX_CAPTURED_GROUP",
                "REGEX_CAPTURED_GROUP_INDEX",
                "REGEX_MATCH",
                "REGEX_REPEAT",
                "REMOVECOMMENT",
                "REPEAT_0_OR_1",
                "RESULT",
                "RESULT_ARGUMENT",
                "REVERSECOLOR",
                "RIGHT",
                "ROTATE45",
                "ROTATE90",
                "SECONDARY",
                "SETTAG",
                "SHIFT",
                "SHIFTHORIZONTAL",
                "SHIFTVERTICAL",
                "SIDETOMOVE",
                "SINGLECOLOR",
                "SITE",
                "SORT",
                "SOUTHEAST",
                "SOUTHWEST",
                "SQRT",
                "SQUARE",
                "SQUARE_SEPARATOR",
                "STALEMATE",
                "STAR",
                "STR",
                "STRING",
                "STR_PARENTHESES",
                "TAG",
                "TAKE_II",
                "TAKE_IR",
                "TAKE_LI",
                "TAKE_LR",
                "TERMINAL",
                "THEN",
                "THROUGH",
                "TITLE",
                "TO",
                "TRUE",
                "TRY",
                "TYPE",
                "TYPENAME",
                "UNBIND",
                "UNION",
                "UNIVERSAL_PIECE_VARIABLE",
                "UNIVERSAL_SQUARE_VARIABLE",
                "UP",
                "UPPERCASE",
                "VARIABLE",
                "VARIABLE_ASSIGN",
                "VARIATION",
                "VERBOSE",
                "VERTICAL",
                "VIRTUALMAINLINE",
                "WHILE",
                "WHITE",
                "WHITESPACE",
                "WILDCARD_PLUS",
                "WILDCARD_STAR",
                "WRITEFILE",
                "WTM",
                "XRAY",
                "YEAR",
                "_ALL_PIECES",
                "_COMPOUND_PIECE",
                "_COMPOUND_SQUARE",
                "_PIECE_CHARS",
                "_SIMPLE_PIECE",
                "_SIMPLE_SQUARE",
                "_SQUARE_OPTIONS",
                "_UNICODE_PIECES",
                "_UNICODE_PIECE_CHARS",
            ],
        )


class PatternElement(unittest.TestCase):
    def test_block_comment(self):
        self.assertEqual(
            elements.BLOCK_COMMENT,
            r"(?P<block_comment>)/\*(?:[^*]|(?:\*(?!/)))*\*/",
        )

    def test_line_comment(self):
        self.assertEqual(
            elements.LINE_COMMENT,
            r"(?P<line_comment>)(?:////|//(?!/))[^\n]*\n+",
        )

    def test_string(self):
        self.assertEqual(
            elements.STRING, r'(?P<string>)"[^\\"]*(?:\\.[^\\"]*)*"'
        )

    def test_whitespace(self):
        self.assertEqual(elements.WHITESPACE, r"(?P<whitespace>)\s+")

    def test_regex_repeat(self):
        self.assertEqual(
            elements.REGEX_REPEAT,
            r"(?P<regex_repeat>)\{(?:(?:\d+(?:,(?:\d+)?)?)|(?:,(?:\d+)))\}",
        )

    def test_brace_left(self):
        self.assertEqual(elements.BRACE_LEFT, r"(?P<brace_left>){")

    def test_brace_right(self):
        self.assertEqual(elements.BRACE_RIGHT, r"(?P<brace_right>)}")

    def test_parenthesis_left(self):
        self.assertEqual(
            elements.PARENTHESIS_LEFT, r"(?P<parenthesis_left>)\("
        )

    def test_parenthesis_right(self):
        self.assertEqual(
            elements.PARENTHESIS_RIGHT, r"(?P<parenthesis_right>)\)"
        )

    def test_anything_else(self):
        self.assertEqual(
            elements.ANYTHING_ELSE, r"(?P<anything_else>)[^/\s{}()]+"
        )

    def test_keyword_anything_else(self):
        self.assertEqual(
            elements.KEYWORD_ANYTHING_ELSE,
            r"".join(
                (
                    r"(?P<keyword_anything_else>)(?:",
                    r"|".join(
                        (
                            r"ancestor",
                            r"between",
                            r"child",
                            r"comment",
                            r"consecutivemoves",
                            r"cql",
                            r"descendant",
                            r"distance",
                            r"echo",
                            r"function",
                            r"indexof",
                            r"lca",
                            r"makesquare",
                            r"max",
                            r"message",
                            r"min",
                            r"ray",
                            r"settag",
                            r"str",
                            r"while",
                            r"writefile",
                            r"xray",
                        )
                    ),
                    r")(?![\w$])",
                )
            ),
        )

    def test_end_of_stream(self):
        self.assertEqual(elements.END_OF_STREAM, r"(?P<end_of_stream>)$")

    def test_after_eq(self):
        self.assertEqual(elements.AFTER_EQ, r"(?P<after_eq>)(?:\[>=\]|\u227d)")

    def test_before_eq(self):
        self.assertEqual(
            elements.BEFORE_EQ, r"(?P<before_eq>)(?:\[<=\]|\u227c)"
        )

    def test_arrow_backward(self):
        self.assertEqual(elements.ARROW_BACKWARD, r"(?P<arrow_backward>)<--")

    def test_arrow_forward(self):
        self.assertEqual(elements.ARROW_FORWARD, r"(?P<arrow_forward>)-->")

    def test_wildcard_plus(self):
        self.assertEqual(elements.WILDCARD_PLUS, r"(?P<wildcard_plus>){\+}")

    def test_wildcard_star(self):
        self.assertEqual(elements.WILDCARD_STAR, r"(?P<wildcard_star>){\*}")

    def test_after_ne(self):
        self.assertEqual(elements.AFTER_NE, r"(?P<after_ne>)(?:\[>\]|\u227b)")

    def test_before_ne(self):
        self.assertEqual(
            elements.BEFORE_NE, r"(?P<before_ne>)(?:\[<\]|\u227a)"
        )

    def test_comment_symbol(self):
        self.assertEqual(
            elements.COMMENT_SYMBOL, r"(?P<comment_symbol>)///(?!/)"
        )

    def test_end_of_line(self):
        self.assertEqual(elements.END_OF_LINE, r"(?P<end_of_line>)(?:\s*)\n+")

    def test_le(self):
        self.assertEqual(elements.LE, r"(?P<le>)(?:<=|\u2264)")

    def test_ge(self):
        self.assertEqual(elements.GE, r"(?P<ge>)(?:>=|\u2265)")

    def test_eq(self):
        self.assertEqual(elements.EQ, r"(?P<eq>)==")

    def test_ne(self):
        self.assertEqual(elements.NE, r"(?P<ne>)(?:!=|\u2260)")

    def test_assign_if(self):
        self.assertEqual(elements.ASSIGN_IF, r"(?P<assign_if>)=\?")

    def test_assign_plus(self):
        self.assertEqual(elements.ASSIGN_PLUS, r"(?P<assign_plus>)\+=")

    def test_assign_minus(self):
        self.assertEqual(elements.ASSIGN_MINUS, r"(?P<assign_minus>)-=")

    def test_assign_divide(self):
        self.assertEqual(elements.ASSIGN_DIVIDE, r"(?P<assign_divide>)/=")

    def test_assign_multiply(self):
        self.assertEqual(elements.ASSIGN_MULTIPLY, r"(?P<assign_multiply>)\*=")

    def test_assign_modulus(self):
        self.assertEqual(elements.ASSIGN_MODULUS, r"(?P<assign_modulus>)%=")

    def test_regex_match(self):
        self.assertEqual(elements.REGEX_MATCH, r"(?P<regex_match>)~~")

    def test_regex_captured_group(self):
        self.assertEqual(
            elements.REGEX_CAPTURED_GROUP, r"(?P<regex_captured_group>)\\\d+"
        )

    def test_regex_captured_group_index(self):
        self.assertEqual(
            elements.REGEX_CAPTURED_GROUP_INDEX,
            r"(?P<regex_captured_group_index>)\\-\d+",
        )

    def test_empty_squares(self):
        self.assertEqual(elements.EMPTY_SQUARES, r"(?P<empty_squares>)\[\]")

    def test_attack_arrow(self):
        self.assertEqual(
            elements.ATTACK_ARROW, r"(?P<attack_arrow>)(?:->|\u2192)"
        )

    def test_attacked_arrow(self):
        self.assertEqual(
            elements.ATTACKED_ARROW, r"(?P<attacked_arrow>)(?:<-|\u2190)"
        )

    def test_dash_ii(self):
        self.assertEqual(elements.DASH_II, r"(?P<dash_ii>)(?:--|\u2015\u2015)")

    def test_dash_li(self):
        self.assertEqual(
            elements.DASH_LI,
            r"(?P<dash_li>)(?<=\S)(?:--|\u2015\u2015)",
        )

    def test_dash_ir(self):
        self.assertEqual(
            elements.DASH_IR,
            r"(?P<dash_ir>)(?:--|\u2015\u2015)(?=\S)",
        )

    def test_dash_lr(self):
        self.assertEqual(
            elements.DASH_LR,
            r"(?P<dash_lr>)(?<=\S)(?:--|\u2015\u2015)(?=\S)",
        )

    def test_take_ii(self):
        self.assertEqual(elements.TAKE_II, r"(?P<take_ii>)(?:\[x\]|\u00d7)")

    def test_take_li(self):
        self.assertEqual(
            elements.TAKE_LI,
            r"(?P<take_li>)(?<=\S)(?:\[x\]|\u00d7)",
        )

    def test_take_ir(self):
        self.assertEqual(
            elements.TAKE_IR,
            r"(?P<take_ir>)(?:\[x\]|\u00d7)(?=\S)",
        )

    def test_take_lr(self):
        self.assertEqual(
            elements.TAKE_LR,
            r"(?P<take_lr>)(?<=\S)(?:\[x\]|\u00d7)(?=\S)",
        )

    def test_any_square(self):
        self.assertEqual(elements.ANY_SQUARE, r"(?P<any_square>)(?:\.|\u25a6)")

    def test_empty_square(self):
        self.assertEqual(
            elements.EMPTY_SQUARE, r"(?P<empty_square>)(?:_|\u25a1)"
        )

    def test_colon(self):
        self.assertEqual(elements.COLON, r"(?P<colon>):")

    def test_intersection(self):
        self.assertEqual(
            elements.INTERSECTION, r"(?P<intersection>)(?:&|\u2229)"
        )

    def test_lt(self):
        self.assertEqual(elements.LT, r"(?P<lt>)<")

    def test_gt(self):
        self.assertEqual(elements.GT, r"(?P<gt>)>")

    def test_plus(self):
        self.assertEqual(elements.PLUS, r"(?P<plus>)\+")

    def test_star(self):
        self.assertEqual(elements.STAR, r"(?P<star>)\*")

    def test_modulus(self):
        self.assertEqual(elements.MODULUS, r"(?P<modulus>)%")

    def test_divide(self):
        self.assertEqual(elements.DIVIDE, r"(?P<divide>)/")

    def test_minus(self):
        self.assertEqual(elements.MINUS, r"(?P<minus>)-")

    def test_complement(self):
        self.assertEqual(elements.COMPLEMENT, r"(?P<complement>)~")

    def test_union(self):
        self.assertEqual(elements.UNION, r"(?P<union>)(?:\||\u222a)")

    def test_assign(self):
        self.assertEqual(elements.ASSIGN, r"(?P<assign>)=")

    def test_repeat_0_or_1(self):
        self.assertEqual(elements.REPEAT_0_OR_1, r"(?P<repeat_0_or_1>)\?")

    def test_count_flter(self):
        self.assertEqual(elements.COUNT_FILTER, r"(?P<count_filter>)#")

    def test_square_separator(self):
        self.assertEqual(elements.SQUARE_SEPARATOR, r"(?P<square_separator>),")

    def test_backslash(self):
        self.assertEqual(elements.BACKSLASH, r"(?P<backslash>)\\")

    def test_bracket_left(self):
        self.assertEqual(elements.BRACKET_LEFT, r"(?P<bracket_left>)\[")

    def test_bracket_right(self):
        self.assertEqual(elements.BRACKET_RIGHT, r"(?P<bracket_right>)\]")

    def test_abs(self):
        self.assertEqual(elements.ABS, r"(?P<abs>)abs(?![\w$])")

    def test_all(self):
        self.assertEqual(elements.ALL, r"(?P<all>)all(?![\w$])")

    def test_ancestor(self):
        self.assertEqual(elements.ANCESTOR, r"(?P<ancestor>)ancestor\s*\(")

    def test_and(self):
        self.assertEqual(elements.AND, r"(?P<and>)and(?![\w$])")

    def test_anydirection(self):
        self.assertEqual(
            elements.ANYDIRECTION, r"(?P<anydirection>)anydirection(?![\w$])"
        )

    def test_attackedby(self):
        self.assertEqual(
            elements.ATTACKEDBY, r"(?P<attackedby>)attackedby(?![\w$])"
        )

    def test_attacks(self):
        self.assertEqual(elements.ATTACKS, r"(?P<attacks>)attacks(?![\w$])")

    def test_between(self):
        self.assertEqual(elements.BETWEEN, r"(?P<between>)between\s*\(")

    def test_black(self):
        self.assertEqual(elements.BLACK, r"(?P<black>)black(?![\w$])")

    def test_btm(self):
        self.assertEqual(elements.BTM, r"(?P<btm>)btm(?![\w$])")

    def test_capture(self):
        self.assertEqual(elements.CAPTURE, r"(?P<capture>)capture(?![\w$])")

    def test_castle(self):
        self.assertEqual(elements.CASTLE, r"(?P<castle>)castle(?![\w$])")

    def test_check(self):
        self.assertEqual(elements.CHECK, r"(?P<check>)check(?![\w$])")

    def test_child_parentheses(self):
        self.assertEqual(
            elements.CHILD_PARENTHESES, r"(?P<child_parentheses>)child\s*\("
        )

    def test_child(self):
        self.assertEqual(elements.CHILD, r"(?P<child>)child(?![\w$])")

    def test_colortype(self):
        self.assertEqual(
            elements.COLORTYPE, r"(?P<colortype>)colortype(?![\w$])"
        )

    def test_comment(self):
        self.assertEqual(elements.COMMENT, r"(?P<comment>)comment(?![\w$])")

    def test_comment_parentheses(self):
        self.assertEqual(
            elements.COMMENT_PARENTHESES,
            r"(?P<comment_parentheses>)comment\s*\(",
        )

    def test_connectedpawns(self):
        self.assertEqual(
            elements.CONNECTEDPAWNS,
            r"(?P<connectedpawns>)connectedpawns(?![\w$])",
        )

    def test_consecutivemoves(self):
        self.assertEqual(
            elements.CONSECUTIVEMOVES,
            r"".join(
                (
                    r"(?P<consecutivemoves>)consecutivemoves",
                    r"(?:\s+quiet(?:\s+(?:\d+|[a-zA-Z0-9_$]+)",
                    r"(?:\s+(?:\d+|[a-zA-Z0-9_$]+))?)?",
                    r"|\s+(?:\d+|[a-zA-Z0-9_$]+)",
                    r"(?:\s+(?:\d+|[a-zA-Z0-9_$]+))?(?:\s+quiet)?)?\s*\(",
                )
            ),
        )

    def test_count(self):
        self.assertEqual(elements.COUNT, r"(?P<count>)count(?![\w$])")

    def test_cql(self):
        self.assertEqual(
            elements.CQL,
            r'cql\s*\((?P<cql>(?:(?:"[^\\"]*(?:\\.[^\\"]*)*")|[^)])*)\)',
        )

    def test_currentposition(self):
        self.assertEqual(
            elements.CURRENTPOSITION,
            r"(?P<currentposition>)(?:currentposition(?![\w$])|\u2219)",
        )

    def test_currenttransform(self):
        self.assertEqual(
            elements.CURRENTTRANSFORM,
            r"(?P<currenttransform>)currenttransform(?![\w$])",
        )

    def test_dark(self):
        self.assertEqual(elements.DARK, r"(?P<dark>)dark(?![\w$])")

    def test_depth(self):
        self.assertEqual(elements.DEPTH, r"(?P<depth>)depth(?![\w$])")

    def test_descendant(self):
        self.assertEqual(
            elements.DESCENDANT, r"(?P<descendant>)descendant\s*\("
        )

    def test_diagonal(self):
        self.assertEqual(elements.DIAGONAL, r"(?P<diagonal>)diagonal(?![\w$])")

    def test_distance(self):
        self.assertEqual(elements.DISTANCE, r"(?P<distance>)distance\s*\(")

    def test_doubledpawns(self):
        self.assertEqual(
            elements.DOUBLEDPAWNS, r"(?P<doubledpawns>)doubledpawns(?![\w$])"
        )

    def test_down(self):
        self.assertEqual(elements.DOWN, r"(?P<down>)down(?![\w$])")

    def test_echo(self):
        self.assertEqual(
            elements.ECHO,
            r"".join(
                (
                    r"(?P<echo>)echo(?:\s+quiet)?\s*\(\s*\w+\s+\w+\s*\)",
                    r"(?:\s*in\s+all(?![\w$]))?\s*",
                )
            ),
        )

    def test_elo(self):
        self.assertEqual(
            elements.ELO, r"(?P<elo>)elo(?:\s+(?:black|white))?(?![\w$])"
        )

    def test_else(self):
        self.assertEqual(elements.ELSE, r"(?P<else>)else(?![\w$])")

    def test_enpassant(self):
        self.assertEqual(
            elements.ENPASSANT, r"(?P<enpassant>)enpassant(?![\w$])"
        )

    def test_enpassantsquare(self):
        self.assertEqual(
            elements.ENPASSANTSQUARE,
            r"(?P<enpassantsquare>)enpassantsquare(?![\w$])",
        )

    def test_event(self):
        self.assertEqual(elements.EVENT, r"(?P<event>)event(?![\w$])")

    def test_false(self):
        self.assertEqual(elements.FALSE, r"(?P<false>)false(?![\w$])")

    def test_fen(self):
        self.assertEqual(elements.FEN, r"(?P<fen>)fen(?![\w$])")

    def test_file(self):
        self.assertEqual(elements.FILE, r"(?P<file>)file(?![\w$])")

    def test_find(self):
        self.assertEqual(elements.FIND, r"(?P<find>)find(?![\w$])")

    def test_firstmatch(self):
        self.assertEqual(
            elements.FIRSTMATCH, r"(?P<firstmatch>)firstmatch(?![\w$])"
        )

    def test_flip(self):
        self.assertEqual(elements.FLIP, r"(?P<flip>)(?:flip(?![\w$])|\u2735)")

    def test_flipcolor(self):
        self.assertEqual(
            elements.FLIPCOLOR, r"(?P<flipcolor>)(?:flipcolor(?![\w$])|\u2b13)"
        )

    def test_fliphorizontal(self):
        self.assertEqual(
            elements.FLIPHORIZONTAL,
            r"(?P<fliphorizontal>)fliphorizontal(?![\w$])",
        )

    def test_flipvertical(self):
        self.assertEqual(
            elements.FLIPVERTICAL, r"(?P<flipvertical>)flipvertical(?![\w$])"
        )

    def test_from(self):
        self.assertEqual(elements.FROM, r"(?P<from>)from(?![\w$])")

    def test_function(self):
        self.assertEqual(
            elements.FUNCTION,
            r"function\s+(?P<function>[\w$]+)\s*\([^)]*\)\s*(?=\{)",
        )

    def test_function_call(self):
        self.assertEqual(
            elements.FUNCTION_CALL, r"(?P<function_call>[a-zA-Z0-9_$]+)\s*\("
        )

    def test_gamenumber(self):
        self.assertEqual(
            elements.GAMENUMBER, r"(?P<gamenumber>)gamenumber(?![\w$])"
        )

    def test_hascomment(self):
        self.assertEqual(
            elements.HASCOMMENT, r"(?P<hascomment>)hascomment(?![\w$])"
        )

    def test_horizontal(self):
        self.assertEqual(
            elements.HORIZONTAL, r"(?P<horizontal>)horizontal(?![\w$])"
        )

    def test_if(self):
        self.assertEqual(elements.IF, r"(?P<if>)if(?![\w$])")

    def test_in_all(self):
        self.assertEqual(elements.IN_ALL, r"(?P<in_all>)in\s+all(?![\w$])")

    def test_in(self):
        self.assertEqual(elements.IN, r"(?P<in>)in(?![\w$])")

    def test_initial(self):
        self.assertEqual(elements.INITIAL, r"(?P<initial>)initial(?![\w$])")

    def test_isolatedpawns(self):
        self.assertEqual(
            elements.ISOLATEDPAWNS,
            r"(?P<isolatedpawns>)isolatedpawns(?![\w$])",
        )

    def test_lastposition(self):
        self.assertEqual(
            elements.LASTPOSITION, r"(?P<lastposition>)lastposition(?![\w$])"
        )

    def test_lca(self):
        self.assertEqual(elements.LCA, r"(?P<lca>)lca\s*\(")

    def test_left(self):
        self.assertEqual(elements.LEFT, r"(?P<left>)left(?![\w$])")

    def test_legal(self):
        self.assertEqual(elements.LEGAL, r"(?P<legal>)legal(?![\w$])")

    def test_light(self):
        self.assertEqual(elements.LIGHT, r"(?P<light>)light(?![\w$])")

    def test_line(self):
        self.assertEqual(elements.LINE, r"(?P<line>)line(?![\w$])")

    def test_loop(self):
        self.assertEqual(elements.LOOP, r"(?P<loop>)loop(?![\w$])")

    def test_maindiagonal(self):
        self.assertEqual(
            elements.MAINDIAGONAL, r"(?P<maindiagonal>)maindiagonal(?![\w$])"
        )

    def test_mainline(self):
        self.assertEqual(elements.MAINLINE, r"(?P<mainline>)mainline(?![\w$])")

    def test_makesquare_parentheses(self):
        self.assertEqual(
            elements.MAKESQUARE_PARENTHESES,
            r"(?P<makesquare_parentheses>)makesquare\s*\(",
        )

    def test_makesquare_string(self):
        self.assertEqual(
            elements.MAKESQUARE_STRING,
            r'(?P<makesquare_string>)makesquare(?=\s*")',
        )

    def test_mate(self):
        self.assertEqual(elements.MATE, r"(?P<mate>)mate(?![\w$])")

    def test_max(self):
        self.assertEqual(elements.MAX, r"(?P<max>)max\s*\(")

    def test_max_parameter(self):
        self.assertEqual(
            elements.MAX_PARAMETER, r"(?P<max_parameter>)max(?![\w$])"
        )

    def test_message(self):
        self.assertEqual(
            elements.MESSAGE, r"(?P<message>)message(?:\s+quiet)?(?![\w$])"
        )

    def test_message_parentheses(self):
        self.assertEqual(
            elements.MESSAGE_PARENTHESES,
            r"(?P<message_parentheses>)message(?:\s+quiet)?\s*\(",
        )

    def test_min(self):
        self.assertEqual(elements.MIN, r"(?P<min>)min\s*\(")

    def test_move(self):
        self.assertEqual(elements.MOVE, r"(?P<move>)move(?![\w$])")

    def test_movenumber(self):
        self.assertEqual(
            elements.MOVENUMBER, r"(?P<movenumber>)movenumber(?![\w$])"
        )

    def test_nestban(self):
        self.assertEqual(elements.NESTBAN, r"(?P<nestban>)nestban(?![\w$])")

    def test_northeast(self):
        self.assertEqual(
            elements.NORTHEAST, r"(?P<northeast>)northeast(?![\w$])"
        )

    def test_northwest(self):
        self.assertEqual(
            elements.NORTHWEST, r"(?P<northwest>)northwest(?![\w$])"
        )

    def test_not(self):
        self.assertEqual(elements.NOT, r"(?P<not>)not(?![\w$])")

    def test_notransform(self):
        self.assertEqual(
            elements.NOTRANSFORM, r"(?P<notransform>)notransform(?![\w$])"
        )

    def test_null(self):
        self.assertEqual(elements.NULL, r"(?P<null>)null(?![\w$])")

    def test_oo(self):
        self.assertEqual(elements.OO, r"(?P<oo>)o-o(?![\w$])")

    def test_ooo(self):
        self.assertEqual(elements.OOO, r"(?P<ooo>)o-o-o(?![\w$])")

    def test_offdiagonal(self):
        self.assertEqual(
            elements.OFFDIAGONAL, r"(?P<offdiagonal>)offdiagonal(?![\w$])"
        )

    def test_orthogonal(self):
        self.assertEqual(
            elements.ORTHOGONAL, r"(?P<orthogonal>)orthogonal(?![\w$])"
        )

    def test_or(self):
        self.assertEqual(elements.OR, r"(?P<or>)or(?![\w$])")

    def test_parent(self):
        self.assertEqual(elements.PARENT, r"(?P<parent>)parent(?![\w$])")

    def test_passedpawns(self):
        self.assertEqual(
            elements.PASSEDPAWNS, r"(?P<passedpawns>)passedpawns(?![\w$])"
        )

    def test_persistent_quiet(self):
        self.assertEqual(
            elements.PERSISTENT_QUIET,
            r"".join(
                (
                    r"persistent\s+quiet\s+(?P<persistent_quiet>",
                    r"[a-zA-Z0-9_$]+)(?=\s*(?:=|\+=|-=|\*=|/=|%=))",
                )
            ),
        )

    def test_persistent(self):
        self.assertEqual(
            elements.PERSISTENT,
            r"".join(
                (
                    r"persistent\s+(?P<persistent>[a-zA-Z0-9_$]+)",
                    r"(?=\s*(?:=|\+=|-=|\*=|/=|%=))",
                )
            ),
        )

    def test_piece(self):
        self.assertEqual(
            elements.PIECE,
            r"?:piece\s+(?:all\s+)?(?P<piece>[a-zA-Z0-9_$]+)\s+in(?![\w$])",
        )

    def test_piece_assignment(self):
        self.assertEqual(
            elements.PIECE_VARIABLE,
            r"(?:piece\s+|\u25ed|\[Aa\])(?P<piece_variable>[\w$]+)\s*(?==)",
        )

    def test_pieceid(self):
        self.assertEqual(elements.PIECEID, r"(?P<pieceid>)pieceid(?![\w$])")

    def test_pin(self):
        self.assertEqual(elements.PIN, r"(?P<pin>)pin(?![\w$])")

    def test_player(self):
        self.assertEqual(
            elements.PLAYER,
            r"(?P<player>)player(?:\s+(?:black|white))?(?![\w$])",
        )

    def test_ply(self):
        self.assertEqual(elements.PLY, r"(?P<ply>)ply(?![\w$])")

    def test_position(self):
        self.assertEqual(elements.POSITION, r"(?P<position>)position(?![\w$])")

    def test_positionid(self):
        self.assertEqual(
            elements.POSITIONID, r"(?P<positionid>)positionid(?![\w$])"
        )

    def test_power(self):
        self.assertEqual(elements.POWER, r"(?P<power>)power(?![\w$])")

    def test_previous(self):
        self.assertEqual(elements.PREVIOUS, r"(?P<previous>)previous(?![\w$])")

    def test_primary(self):
        self.assertEqual(elements.PRIMARY, r"(?P<primary>)primary(?![\w$])")

    def test_promote(self):
        self.assertEqual(elements.PROMOTE, r"(?P<promote>)promote(?![\w$])")

    def test_pseudolegal(self):
        self.assertEqual(
            elements.PSEUDOLEGAL, r"(?P<pseudolegal>)pseudolegal(?![\w$])"
        )

    def test_quiet(self):
        self.assertEqual(elements.QUIET, r"(?P<quiet>)quiet(?![\w$])")

    def test_rank(self):
        self.assertEqual(elements.RANK, r"(?P<rank>)rank(?![\w$])")

    def test_ray(self):
        self.assertEqual(
            elements.RAY,
            r"".join(
                (
                    r"(?P<ray>)ray",
                    r"(?:\s+(?:",
                    r"up|down|right|left|northeast|northwest",
                    r"|southwest|southeast",
                    r"|diagonal|orthogonal|vertical|horizontal|anydirection",
                    r"))*\s*\(",
                )
            ),
        )

    def test_removecomment(self):
        self.assertEqual(
            elements.REMOVECOMMENT,
            r"(?P<removecomment>)removecomment(?![\w$])",
        )

    def test_result(self):
        self.assertEqual(elements.RESULT, r"(?P<result>)result(?![\w$])")

    def test_reversecolor(self):
        self.assertEqual(
            elements.REVERSECOLOR, r"(?P<reversecolor>)reversecolor(?![\w$])"
        )

    def test_right(self):
        self.assertEqual(elements.RIGHT, r"(?P<right>)right(?![\w$])")

    def test_rotate45(self):
        self.assertEqual(elements.ROTATE45, r"(?P<rotate45>)rotate45(?![\w$])")

    def test_rotate90(self):
        self.assertEqual(elements.ROTATE90, r"(?P<rotate90>)rotate90(?![\w$])")

    def test_secondary(self):
        self.assertEqual(
            elements.SECONDARY, r"(?P<secondary>)secondary(?![\w$])"
        )

    def test_shift(self):
        self.assertEqual(elements.SHIFT, r"(?P<shift>)shift(?![\w$])")

    def test_shifthorizontal(self):
        self.assertEqual(
            elements.SHIFTHORIZONTAL,
            r"(?P<shifthorizontal>)shifthorizontal(?![\w$])",
        )

    def test_shiftvertical(self):
        self.assertEqual(
            elements.SHIFTVERTICAL,
            r"(?P<shiftvertical>)shiftvertical(?![\w$])",
        )

    def test_sidetomove(self):
        self.assertEqual(
            elements.SIDETOMOVE, r"(?P<sidetomove>)sidetomove(?![\w$])"
        )

    def test_singlecolor(self):
        self.assertEqual(
            elements.SINGLECOLOR, r"(?P<singlecolor>)singlecolor(?![\w$])"
        )

    def test_site(self):
        self.assertEqual(elements.SITE, r"(?P<site>)site(?![\w$])")

    def test_sort(self):
        self.assertEqual(elements.SORT, r"(?P<sort>)sort(?:\s+min)?(?![\w$])")

    def test_southeast(self):
        self.assertEqual(
            elements.SOUTHEAST, r"(?P<southeast>)southeast(?![\w$])"
        )

    def test_southwest(self):
        self.assertEqual(
            elements.SOUTHWEST, r"(?P<southwest>)southwest(?![\w$])"
        )

    def test_sqrt(self):
        self.assertEqual(elements.SQRT, r"(?P<sqrt>)sqrt(?![\w$])")

    def test_square(self):
        self.assertEqual(
            elements.SQUARE,
            r"?:square\s+(?:all\s+)?(?P<square>[a-zA-Z0-9_$]+)\s+in(?![\w$])",
        )

    def test_stalemate(self):
        self.assertEqual(
            elements.STALEMATE, r"(?P<stalemate>)stalemate(?![\w$])"
        )

    def test_terminal(self):
        self.assertEqual(elements.TERMINAL, r"(?P<terminal>)terminal(?![\w$])")

    def test_then(self):
        self.assertEqual(elements.THEN, r"(?P<then>)then(?![\w$])")

    def test_through(self):
        self.assertEqual(elements.THROUGH, r"(?P<through>)through(?![\w$])")

    def test_to(self):
        self.assertEqual(elements.TO, r"(?P<to>)to(?![\w$])")

    def test_true(self):
        self.assertEqual(elements.TRUE, r"(?P<true>)true(?![\w$])")

    def test_type(self):
        self.assertEqual(elements.TYPE, r"(?P<type>)type(?![\w$])")

    def test_up(self):
        self.assertEqual(elements.UP, r"(?P<up>)up(?![\w$])")

    def test_variation(self):
        self.assertEqual(
            elements.VARIATION, r"(?P<variation>)variation(?![\w$])"
        )

    def test_vertical(self):
        self.assertEqual(elements.VERTICAL, r"(?P<vertical>)vertical(?![\w$])")

    def test_virtualmainline(self):
        self.assertEqual(
            elements.VIRTUALMAINLINE,
            r"(?P<virtualmainline>)virtualmainline(?![\w$])",
        )

    def test_white(self):
        self.assertEqual(elements.WHITE, r"(?P<white>)white(?![\w$])")

    def test_wtm(self):
        self.assertEqual(elements.WTM, r"(?P<wtm>)wtm(?![\w$])")

    def test_xray(self):
        self.assertEqual(elements.XRAY, r"(?P<xray>)xray\s*\(")

    def test_year(self):
        self.assertEqual(elements.YEAR, r"(?P<year>)year(?![\w$])")

    def test_ascii(self):
        self.assertEqual(elements.ASCII, r"(?P<ascii>)ascii(?![\w$])")

    def test_assert(self):
        self.assertEqual(elements.ASSERT, r"(?P<assert>)assert(?![\w$])")

    def test_date(self):
        self.assertEqual(elements.DATE, r"(?P<date>)date(?![\w$])")

    def test_dictionary(self):
        self.assertEqual(
            elements.DICTIONARY,
            r"(?:local\s+)?dictionary\s+(?P<dictionary>[a-zA-Z0-9_$]+)",
        )

    def test_eco(self):
        self.assertEqual(elements.ECO, r"(?P<eco>)eco(?![\w$])")

    def test_eventdate(self):
        self.assertEqual(
            elements.EVENTDATE, r"(?P<eventdate>)eventdate(?![\w$])"
        )

    def test_indexof(self):
        self.assertEqual(elements.INDEXOF, r"(?P<indexof>)indexof\s*\(")

    def test_initialposition(self):
        self.assertEqual(
            elements.INITIALPOSITION,
            r"(?P<initialposition>)initialposition(?![\w$])",
        )

    def test_int(self):
        self.assertEqual(elements.INT, r"(?P<int>)int(?![\w$])")

    def test_isbound(self):
        self.assertEqual(elements.ISBOUND, r"(?P<isbound>)isbound(?![\w$])")

    def test_isunbound(self):
        self.assertEqual(
            elements.ISUNBOUND, r"(?P<isunbound>)isunbound(?![\w$])"
        )

    def test_lowercase(self):
        self.assertEqual(
            elements.LOWERCASE, r"(?P<lowercase>)lowercase(?![\w$])"
        )

    def test_originalcomment(self):
        self.assertEqual(
            elements.ORIGINALCOMMENT,
            r"(?P<originalcomment>)originalcomment(?![\w$])",
        )

    def test_readfile(self):
        self.assertEqual(elements.READFILE, r"(?P<readfile>)readfile(?![\w$])")

    def test_settag(self):
        self.assertEqual(elements.SETTAG, r"(?P<settag>)settag\s*\(")

    def test_str_parentheses(self):
        self.assertEqual(
            elements.STR_PARENTHESES, r"(?P<str_parentheses>)str\s*\("
        )

    def test_str(self):
        self.assertEqual(elements.STR, r"(?P<str>)str(?![\w$])")

    def test_tag(self):
        self.assertEqual(elements.TAG, r"(?P<tag>)tag(?![\w$])")

    def test_unbind(self):
        self.assertEqual(elements.UNBIND, r"(?P<unbind>)unbind(?![\w$])")

    def test_uppercase(self):
        self.assertEqual(
            elements.UPPERCASE, r"(?P<uppercase>)uppercase(?![\w$])"
        )

    def test_while(self):
        self.assertEqual(elements.WHILE, r"(?P<while>)while(?=\s*\()")

    def test_writefile(self):
        self.assertEqual(elements.WRITEFILE, r"(?P<writefile>)writefile\s*\(")

    def test_atomic(self):
        self.assertEqual(
            elements.ATOMIC,
            r"".join(
                (
                    r"atomic\s+(?P<atomic>[a-zA-Z0-9_$]+)",
                    r"(?=\s*(?:=))",
                )
            ),
        )

    def test_countmoves(self):
        self.assertEqual(
            elements.COUNTMOVES, r"(?P<countmoves>)countmoves(?![\w$])"
        )

    def test_currentmove(self):
        self.assertEqual(
            elements.CURRENTMOVE, r"(?P<currentmove>)currentmove(?![\w$])"
        )

    def test_element(self):
        self.assertEqual(
            elements.ELEMENT, r"(?P<element>)(?:\[element\]|\u220a)"
        )

    def test_focus_capture(self):
        self.assertEqual(
            elements.FOCUS_CAPTURE,
            r"(?P<focus_capture>)(?:focus\s+|\u25ce\s*)capture(?![\w$])",
        )

    def test_focus(self):
        self.assertEqual(
            elements.FOCUS, r"(?P<focus>)(?:focus(?![\w$])|\u25ce)"
        )

    def test_forall(self):
        self.assertEqual(elements.FORALL, r"(?P<forall>)(?:\[forall\]|\u2200)")

    def test_idealmate(self):
        self.assertEqual(
            elements.IDEALMATE, r"(?P<idealmate>)idealmate(?![\w$])"
        )

    def test_idealstalemate(self):
        self.assertEqual(
            elements.IDEALSTALEMATE,
            r"(?P<idealstalemate>)idealstalemate(?![\w$])",
        )

    def test_keepallbest(self):
        self.assertEqual(
            elements.KEEPALLBEST, r"(?P<keepallbest>)keepallbest(?![\w$])"
        )

    def test_lastgamenumber(self):
        self.assertEqual(
            elements.LASTGAMENUMBER,
            r"(?P<lastgamenumber>)lastgamenumber(?![\w$])",
        )

    def test_local(self):
        self.assertEqual(elements.LOCAL, r"(?P<local>)local(?![\w$])")

    def test_modelmate(self):
        self.assertEqual(
            elements.MODELMATE, r"(?P<modelmate>)modelmate(?![\w$])"
        )

    def test_modelstalemate(self):
        self.assertEqual(
            elements.MODELSTALEMATE,
            r"(?P<modelstalemate>)modelstalemate(?![\w$])",
        )

    def test_nullmove(self):
        self.assertEqual(elements.NULLMOVE, r"(?P<nullmove>)nullmove(?![\w$])")

    def test_path(self):
        self.assertEqual(elements.PATH, r"(?P<path>)(?:path(?![\w$])|\u22a2)")

    def test_pathcount(self):
        self.assertEqual(
            elements.PATHCOUNT, r"(?P<pathcount>)pathcount(?![\w$])"
        )

    def test_pathcountunfocused(self):
        self.assertEqual(
            elements.PATHCOUNTUNFOCUSED,
            r"(?P<pathcountunfocused>)pathcountunfocused(?![\w$])",
        )

    def test_pathlastposition(self):
        self.assertEqual(
            elements.PATHLASTPOSITION,
            r"(?P<pathlastposition>)pathlastposition(?![\w$])",
        )

    def test_pathstart(self):
        self.assertEqual(
            elements.PATHSTART, r"(?P<pathstart>)pathstart(?![\w$])"
        )

    def test_piecename(self):
        self.assertEqual(
            elements.PIECENAME, r"(?P<piecename>)piecename(?![\w$])"
        )

    def test_piecepath(self):
        self.assertEqual(
            elements.PIECEPATH, r"(?P<piecepath>)piecepath(?![\w$])"
        )

    def test_puremate(self):
        self.assertEqual(elements.PUREMATE, r"(?P<puremate>)puremate(?![\w$])")

    def test_purestalemate(self):
        self.assertEqual(
            elements.PURESTALEMATE,
            r"(?P<purestalemate>)purestalemate(?![\w$])",
        )

    def test_title(self):
        self.assertEqual(elements.TITLE, r"(?P<title>)title(?![\w$])")

    def test_try(self):
        self.assertEqual(elements.TRY, r"(?P<try>)try(?![\w$])")

    def test_typename(self):
        self.assertEqual(elements.TYPENAME, r"(?P<typename>)typename(?![\w$])")

    def test_verbose(self):
        self.assertEqual(elements.VERBOSE, r"(?P<verbose>)verbose(?![\w$])")

    def test__simple_square(self):
        self.assertEqual(
            elements._SIMPLE_SQUARE, r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?"
        )

    def test__compound_square(self):
        self.assertEqual(
            elements._COMPOUND_SQUARE,
            "".join(
                (
                    r"\[",
                    r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r"(?:,",
                    r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r")*\]",
                )
            ),
        )

    def test__piece_chars(self):
        self.assertEqual(elements._PIECE_CHARS, r"[QBRNKPAqbrnkpa_]")

    def test__simple_piece(self):
        self.assertEqual(elements._SIMPLE_PIECE, r"[QBRNKPAqbrnkpa_](?![\w$])")

    def test__compound_piece(self):
        self.assertEqual(
            elements._COMPOUND_PIECE,
            r"".join(
                (
                    r"\[",
                    r"[QBRNKPAqbrnkpa_]",
                    r"(?:",
                    r"[QBRNKPAqbrnkpa_]",
                    r")*\]",
                )
            ),
        )

    def test__unicode_piece_chars(self):
        self.assertEqual(
            elements._UNICODE_PIECE_CHARS,
            r"".join(
                (
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                )
            ),
        )

    def test__unicode_pieces(self):
        self.assertEqual(
            elements._UNICODE_PIECES,
            r"".join(
                (
                    r"(?:[",
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                    r"]+)|\[(?:[",
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                    r"]+)\]",
                )
            ),
        )

    def test__all_pieces(self):
        self.assertEqual(elements._ALL_PIECES, r"\u25ed")

    def test__square_options(self):
        self.assertEqual(
            elements._SQUARE_OPTIONS,
            "".join(
                (
                    r"\[",
                    r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r"(?:,",
                    r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r")*\]",
                    r"|",
                    r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                )
            ),
        )

    def test__piece_options(self):
        self.assertEqual(
            elements.PIECE_OPTIONS,
            r"".join(
                (
                    r"\[",
                    r"[QBRNKPAqbrnkpa_]",
                    r"(?:",
                    r"[QBRNKPAqbrnkpa_]",
                    r")*\]",
                    r"|",
                    r"[QBRNKPAqbrnkpa_]",
                    r"|",
                    r"(?:[",
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                    r"]+)|\[(?:[",
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                    r"]+)\]",
                    r"|",
                    r"\u25ed",
                )
            ),
        )

    def test_piece_designator(self):
        self.assertEqual(
            elements.PIECE_DESIGNATOR,
            "".join(
                (
                    r"(?P<piece_designator>)",
                    r"(?:",
                    r"(?:",
                    r"(?:",
                    r"\[",
                    r"[QBRNKPAqbrnkpa_]",
                    r"(?:",
                    r"[QBRNKPAqbrnkpa_]",
                    r")*\]",
                    r"|",
                    r"[QBRNKPAqbrnkpa_]",
                    r"|",
                    r"(?:[",
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                    r"]+)|\[(?:[",
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                    r"]+)\]",
                    r"|",
                    r"\u25ed",
                    ")?",
                    "(?:",
                    r"\[",
                    r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r"(?:,",
                    r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    r")*\]",
                    r"|",
                    r"[a-h](?:-[a-h])?[1-8](?:-[1-8])?",
                    ")",
                    r")|(?:",
                    r"\[",
                    r"[QBRNKPAqbrnkpa_]",
                    r"(?:",
                    r"[QBRNKPAqbrnkpa_]",
                    r")*\]",
                    r"|",
                    r"[QBRNKPAqbrnkpa_](?![\w$])",
                    r"|",
                    r"(?:[",
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                    r"]+)|\[(?:[",
                    r"\u25b3",
                    r"\u2654",
                    r"\u2655",
                    r"\u2656",
                    r"\u2657",
                    r"\u2658",
                    r"\u2659",
                    r"\u25b2",
                    r"\u265a",
                    r"\u265b",
                    r"\u265c",
                    r"\u265d",
                    r"\u265e",
                    r"\u265f",
                    r"\u25a1",
                    r"]+)\]",
                    r"|",
                    r"\u25ed",
                    r")",
                    r")",
                )
            ),
        )

    def test_variable(self):
        self.assertEqual(elements.VARIABLE, r"(?P<variable>[a-zA-Z0-9_$]+)")

    def test_variable_assign(self):
        self.assertEqual(
            elements.VARIABLE_ASSIGN,
            r"(?P<variable_assign>[a-zA-Z0-9_$]+)(?=\s*=[^=])",
        )

    def test_existential_square_variable(self):
        self.assertEqual(
            elements.EXISTENTIAL_SQUARE_VARIABLE,
            "".join(
                (
                    r"(?:)",
                    r"(?P<existential_square_variable>",
                    r"[a-zA-Z0-9_$]",
                    r"+)(?=\s*(?:\[element\]|\u220a))",
                )
            ),
        )

    def test_existential_piece_variable(self):
        self.assertEqual(
            elements.EXISTENTIAL_PIECE_VARIABLE,
            "".join(
                (
                    r"(?:\[Aa\]|\u25ed)",
                    r"(?P<existential_piece_variable>",
                    r"[a-zA-Z0-9_$]",
                    r"+)(?=\s*(?:\[element\]|\u220a))",
                )
            ),
        )

    def test_universal_square_variable(self):
        self.assertEqual(
            elements.UNIVERSAL_SQUARE_VARIABLE,
            "".join(
                (
                    r"(?:\[forall\]|\u2200)",
                    r"(?P<universal_square_variable>",
                    r"[a-zA-Z0-9_$]",
                    r"+)(?=\s*(?:\[element\]|\u220a))",
                )
            ),
        )

    def test_universal_piece_variable(self):
        self.assertEqual(
            elements.UNIVERSAL_PIECE_VARIABLE,
            "".join(
                (
                    r"(?:\[forall\]|\u2200)",
                    r"(?:\[Aa\]|\u25ed)",
                    r"(?P<universal_piece_variable>",
                    r"[a-zA-Z0-9_$]",
                    r"+)(?=\s*(?:\[element\]|\u220a))",
                )
            ),
        )

    def test_result_argument(self):
        self.assertEqual(
            elements.RESULT_ARGUMENT,
            r"(?P<result_argument>)(?:1-0|1/2-1/2|0-1)",
        )

    def test_integer(self):
        self.assertEqual(elements.INTEGER, r"(?P<integer>)\d+")


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(PatternAttributes))
    runner().run(loader(PatternElement))
