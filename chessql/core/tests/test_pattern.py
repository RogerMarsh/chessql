# test_pattern.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Unittests for chessql.core.pattern module.

Verify the values of constant attributes defined in ..pattern module.
Changes in ..pattern not done here too will be highlighted.
"""

import unittest

from .. import pattern


class PatternAttributes(unittest.TestCase):
    def test_attributes(self):
        self.assertEqual(
            [a for a in sorted(dir(pattern)) if a.isupper()],
            [
                "CQL_TOKENS",
            ],
        )


class Pattern(unittest.TestCase):
    def test_cql_tokens(self):
        self.assertEqual(
            pattern.CQL_TOKENS,
            r"".join(
                (
                    r"("
                    # BLOCK_COMMENT
                    r"(?P<block_comment>)/\*(?:[^*]|(?:\*(?!/)))*\*/",
                    r")|(",
                    # LINE_COMMENT
                    r"(?P<line_comment>)(?:////|//(?!/))[^\n]*\n+",
                    r")|(",
                    r'(?P<string>)"[^\\"]*(?:\\.[^\\"]*)*"',  # STRING
                    r")|(",
                    r"(?P<end_of_line>)(?:\s*)\n+",  # END_OF_LINE
                    r")|(",
                    r"(?P<whitespace>)\s+",  # WHITESPACE
                    r")|(",
                    r"(?P<brace_right>)}",  # BRACE_RIGHT
                    r")|(",
                    r"(?P<wildcard_plus>){\+}",  # WILDCARD_PLUS
                    r")|(",
                    r"(?P<wildcard_star>){\*}",  # WILDCARD_STAR
                    r")|(",
                    # REGEX_REPEAT
                    r"(?P<regex_repeat>)",
                    r"\{(?:\d+(?:,(?:\d+)?)?)\}|(?:,(?:\d+))\}",
                    r")|(",
                    r"(?P<brace_left>){",  # BRACE_LEFT
                    r")|(",
                    r"(?P<parenthesis_left>)\(",  # PARENTHESIS_LEFT
                    r")|(",
                    r"(?P<parenthesis_right>)\)",  # PARENTHESIS_RIGHT
                    r")|(",
                    r"(?P<arrow_backward>)<--",  # ARROW_BACKWARD
                    r")|(",
                    r"(?P<arrow_forward>)-->",  # ARROW_FORWARD
                    r")|(",
                    r"(?P<after_eq>)(?:\[>=\]|\u227d)",  # AFTER_EQ
                    r")|(",
                    r"(?P<after_ne>)(?:\[>\]|\u227b)",  # AFTER_NE
                    r")|(",
                    r"(?P<before_eq>)(?:\[<=\]|\u227c)",  # BEFORE_EQ
                    r")|(",
                    r"(?P<before_ne>)(?:\[<\]|\u227a)",  # BEFORE_NE
                    r")|(",
                    # CAPTURES_PBPE
                    r"(?P<captures_pbpe>)(?:(?<=\()\[x\]|\u00d7)(?=\))",
                    r")|(",
                    # CAPTURES_PBR
                    r"(?P<captures_pbr>)(?:(?<=\()\[x\]|\u00d7)(?=[^\s(=])",
                    r")|(",
                    r"(?P<captures_pb>)(?:(?<=\()\[x\]|\u00d7)",  # CAPTURES_PB
                    r")|(",
                    # CAPTURES_PE
                    r"(?P<captures_pe>)(?:\[x\]|\u00d7)(?=\))",
                    r")|(",
                    # CAPTURES_LPE
                    r"(?P<captures_lpe>)(?:(?<=\S)\[x\]|\u00d7)(?=\))",
                    r")|(",
                    # CAPTURES_LR
                    r"(?P<captures_lr>)(?:(?<=\S)\[x\]|\u00d7)(?=[^\s(=])",
                    r")|(",
                    r"(?P<captures_l>)(?:(?<=\S)\[x\]|\u00d7)",  # CAPTURES_L
                    r")|(",
                    # CAPTURES_R
                    r"(?P<captures_r>)(?:\[x\]|\u00d7)(?=[^\s(=])",
                    r")|(",
                    r"(?P<captures>)(?:\[x\]|\u00d7)",  # CAPTURES
                    r")|(",
                    r"(?P<comment_symbol>)///(?!/)",  # COMMENT_SYMBOL
                    r")|(",
                    r"(?P<attack_arrow>)(?:->|\u2192)",  # ATTACK_ARROW
                    r")|(",
                    r"(?P<attacked_arrow>)(?:<-|\u2190)",  # ATTACKED_ARROW
                    r")|(",
                    # SINGLE_MOVE_PBPE
                    r"(?P<single_move_pbpe>)(?:(?<=\()--|\u2015\u2015)",
                    r"(?=[\)\*\+=])",
                    r")|(",
                    # SINGLE_MOVE_PBR
                    r"(?P<single_move_pbr>)(?:(?<=\()--|\u2015\u2015)",
                    r"(?=\S)",
                    r")|(",
                    # SINGLE_MOVE_PB
                    r"(?P<single_move_pb>)(?:(?<=\()--|\u2015\u2015)",
                    r")|(",
                    # SINGLE_MOVE_PE
                    r"(?P<single_move_pe>)(?:--|\u2015\u2015)(?=[\)\*\+=])",
                    r")|(",
                    # SINGLE_MOVE_LPE
                    r"(?P<single_move_lpe>)(?:(?<=\S)--|\u2015\u2015)",
                    r"(?=[\)\*\+=])",
                    r")|(",
                    # SINGLE_MOVE_LR
                    r"(?P<single_move_lr>)(?:(?<=\S)--|\u2015\u2015)",
                    r"(?=\S)",
                    r")|(",
                    # SINGLE_MOVE_L
                    r"(?P<single_move_l>)(?:(?<=\S)--|\u2015\u2015)",
                    r")|(",
                    # SINGLE_MOVE_R
                    r"(?P<single_move_r>)(?:--|\u2015\u2015)(?=\S)",
                    r")|(",
                    r"(?P<single_move>)(?:--|\u2015\u2015)",  # SINGLE_MOVE
                    r")|(",
                    r"(?P<regex_match>)~~",  # REGEX_MATCH
                    r")|(",
                    r"(?P<regex_captured_group>)\\\d+",  # REGEX_CAPTURED_GROUP
                    r")|(",
                    # REGEX_CAPTURED_GROUP_INDEX
                    r"(?P<regex_captured_group_index>)\\-\d+",
                    r")|(",
                    r"(?P<empty_squares>)\[\]",  # EMPTY_SQUARES
                    r")|(",
                    r"(?P<le>)(?:<=|\u2264)",  # LE
                    r")|(",
                    r"(?P<ge>)(?:>=|\u2265)",  # GE
                    r")|(",
                    r"(?P<eq>)==",  # EQ
                    r")|(",
                    r"(?P<ne>)(?:!=|\u2260)",  # NE
                    r")|(",
                    r"(?P<assign_if>)=\?",  # ASSIGN_IF
                    r")|(",
                    r"(?P<assign_plus>)\+=",  # ASSIGN_PLUS
                    r")|(",
                    r"(?P<assign_minus>)-=",  # ASSIGN_MINUS
                    r")|(",
                    r"(?P<assign_divide>)/=",  # ASSIGN_DIVIDE
                    r")|(",
                    r"(?P<assign_multiply>)\*=",  # ASSIGN_MULTIPLY
                    r")|(",
                    r"(?P<assign_modulus>)%=",  # ASSIGN_MODULUS
                    r")|(",
                    r"(?P<abs>)abs(?![\w$])",  # ABS
                    r")|(",
                    r"(?P<all>)all(?![\w$])",  # ALL
                    r")|(",
                    r"(?P<ancestor>)ancestor\s*\(",  # ANCESTOR
                    r")|(",
                    r"(?P<and>)and(?![\w$])",  # AND
                    r")|(",
                    r"(?P<anydirection>)anydirection(?![\w$])",  # ANYDIRECTION
                    r")|(",
                    r"(?P<ascii>)ascii(?![\w$])",  # ASCII
                    r")|(",
                    r"(?P<assert>)assert(?![\w$])",  # ASSERT
                    r")|(",
                    # ATOMIC
                    r"atomic\s+(?P<atomic>[a-zA-Z0-9_$]+)",
                    r"(?=\s*(?:=|\+=|-=|\*=|/=|%=))",
                    r")|(",
                    r"(?P<attackedby>)attackedby(?![\w$])",  # ATTACKEDBY
                    r")|(",
                    r"(?P<attacks>)attacks(?![\w$])",  # ATTACKS
                    r")|(",
                    r"(?P<between>)between\s*\(",  # BETWEEN
                    r")|(",
                    r"(?P<black>)black(?![\w$])",  # BLACK
                    r")|(",
                    r"(?P<btm>)btm(?![\w$])",  # BTM
                    r")|(",
                    r"(?P<capture>)capture(?![\w$])",  # CAPTURE
                    r")|(",
                    r"(?P<castle>)castle(?![\w$])",  # CASTLE
                    r")|(",
                    r"(?P<check>)check(?![\w$])",  # CHECK
                    r")|(",
                    r"(?P<child_parentheses>)child\s*\(",  # CHILD_PARENTHESES
                    r")|(",
                    r"(?P<child>)child(?![\w$])",  # CHILD
                    r")|(",
                    r"(?P<colortype>)colortype(?![\w$])",  # COLORTYPE
                    r")|(",
                    # COMMENT_PARENTHESES
                    r"(?P<comment_parentheses>)comment\s*\(",
                    r")|(",
                    r"(?P<comment>)comment(?![\w$])",  # COMMENT
                    r")|(",
                    # CONNECTEDPAWNS
                    r"(?P<connectedpawns>)connectedpawns(?![\w$])",
                    r")|(",
                    # CONSECUTIVEMOVES
                    r"(?P<consecutivemoves>)consecutivemoves",
                    r"(?:\s+quiet(?:\s+(?:\d+|[a-zA-Z0-9_$]+)",
                    r"(?:\s+(?:\d+|[a-zA-Z0-9_$]+))?)?",
                    r"|\s+(?:\d+|[a-zA-Z0-9_$]+)",
                    r"(?:\s+(?:\d+|[a-zA-Z0-9_$]+))?(?:\s+quiet)?)?\s*\(",
                    r")|(",
                    r"(?P<count>)count(?![\w$])",  # COUNT
                    r")|(",
                    r"(?P<countmoves>)countmoves(?![\w$])",  # COUNTMOVES
                    # CQL
                    r")|(",
                    r'cql\s*\((?P<cql>(?:(?:"[^\\"]*(?:\\.[^\\"]*)*")',
                    r"|[^)])*)\)",
                    r")|(",
                    r"(?P<currentmove>)currentmove(?![\w$])",  # CURRENTMOVE
                    r")|(",
                    # CURRENTPOSITION
                    r"(?P<currentposition>)",
                    r"(?:currentposition(?![\w$])|\u2219)",
                    r")|(",
                    # CURRENTTRANSFORM
                    r"(?P<currenttransform>)currenttransform(?![\w$])",
                    r")|(",
                    r"(?P<dark>)dark(?![\w$])",  # DARK
                    r")|(",
                    r"(?P<date>)date(?![\w$])",  # DATE
                    r")|(",
                    r"(?P<depth>)depth(?![\w$])",  # DEPTH
                    r")|(",
                    r"(?P<descendant>)descendant\s*\(",  # DESCENDANT
                    r")|(",
                    r"(?P<diagonal>)diagonal(?![\w$])",  # DIAGONAL
                    r")|(",
                    # DICTIONARY
                    r"(?:local\s+)?dictionary\s+",
                    r"(?P<dictionary>[a-zA-Z0-9_$]+)",
                    r")|(",
                    r"(?P<distance>)distance\s*\(",  # DISTANCE
                    r")|(",
                    r"(?P<doubledpawns>)doubledpawns(?![\w$])",  # DOUBLEDPAWNS
                    r")|(",
                    r"(?P<down>)down(?![\w$])",  # DOWN
                    r")|(",
                    # ECHO
                    r"(?P<echo>)echo(?:\s+quiet)?\s*\(\s*\w+\s+\w+\s*\)",
                    r"(?:\s*in\s+all(?![\w$]))?\s*",
                    r")|(",
                    r"(?P<eco>)eco(?![\w$])",  # ECO
                    r")|(",
                    r"(?P<element>)(?:\[element\]|\u220a)",  # ELEMENT
                    r")|(",
                    r"(?P<elo>)elo(?:\s+(?:black|white))?(?![\w$])",  # ELO
                    r")|(",
                    r"(?P<else>)else(?![\w$])",  # ELSE
                    r")|(",
                    r"(?P<enpassant>)enpassant(?![\w$])",  # ENPASSANT
                    r")|(",
                    # ENPASSANTSQUARE
                    r"(?P<enpassantsquare>)enpassantsquare(?![\w$])",
                    r")|(",
                    r"(?P<eventdate>)eventdate(?![\w$])",  # EVENTDATE
                    r")|(",
                    r"(?P<event>)event(?![\w$])",  # EVENT
                    r")|(",
                    r"(?P<false>)false(?![\w$])",  # FALSE
                    r")|(",
                    r"(?P<fen>)fen(?![\w$])",  # FEN
                    r")|(",
                    r"(?P<file>)file(?![\w$])",  # FILE
                    r")|(",
                    r"(?P<find>)find(?![\w$])",  # FIND
                    r")|(",
                    r"(?P<firstmatch>)firstmatch(?![\w$])",  # FIRSTMATCH
                    r")|(",
                    # FLIPCOLOR
                    r"(?P<flipcolor>)(?:flipcolor(?![\w$])|\u2b13)",
                    r")|(",
                    # FLIPHORIZONTAL
                    r"(?P<fliphorizontal>)fliphorizontal(?![\w$])",
                    r")|(",
                    r"(?P<flipvertical>)flipvertical(?![\w$])",  # FLIPVERTICAL
                    r")|(",
                    r"(?P<flip>)(?:flip(?![\w$])|\u2735)",  # FLIP
                    r")|(",
                    # FOCUS_CAPTURE
                    r"(?P<focus_capture>)",
                    r"(?:focus\s+|\u25ce\s*)capture(?![\w$])",
                    r")|(",
                    r"(?P<focus>)(?:focus(?![\w$])|\u25ce)",  # FOCUS
                    r")|(",
                    r"(?P<from>)from(?![\w$])",  # FROM
                    r")|(",
                    # FUNCTION
                    r"function\s+(?P<function>[\w$]+)\s*\([^)]*\)\s*(?=\{)",
                    r")|(",
                    r"(?P<gamenumber>)gamenumber(?![\w$])",  # GAMENUMBER
                    r")|(",
                    r"(?P<hascomment>)hascomment(?![\w$])",  # HASCOMMENT
                    r")|(",
                    r"(?P<hhdb>)hhdb(?![\w$])",  # HHDB
                    r")|(",
                    r"(?P<horizontal>)horizontal(?![\w$])",  # HORIZONTAL
                    r")|(",
                    r"(?P<idealmate>)idealmate(?![\w$])",  # IDEALMATE
                    r")|(",
                    # IDEALSTALEMATE
                    r"(?P<idealstalemate>)idealstalemate(?![\w$])",
                    r")|(",
                    r"(?P<if>)if(?![\w$])",  # IF
                    r")|(",
                    r"(?P<indexof>)indexof\s*\(",  # INDEXOF
                    r")|(",
                    # INITIALPOSITION
                    r"(?P<initialposition>)initialposition(?![\w$])",
                    r")|(",
                    r"(?P<initial>)initial(?![\w$])",  # INITIAL
                    r")|(",
                    r"(?P<int>)int(?![\w$])",  # INT
                    r")|(",
                    r"(?P<in_all>)in\s+all(?![\w$])",  # IN_ALL
                    r")|(",
                    r"(?P<in>)in(?![\w$])",  # IN
                    r")|(",
                    r"(?P<isbound>)isbound(?![\w$])",  # ISBOUND
                    r")|(",
                    # ISOLATEDPAWNS
                    r"(?P<isolatedpawns>)isolatedpawns(?![\w$])",
                    r")|(",
                    r"(?P<isunbound>)isunbound(?![\w$])",  # ISUNBOUND
                    r")|(",
                    r"(?P<keepallbest>)keepallbest(?![\w$])",  # KEEPALLBEST
                    r")|(",
                    # LASTGAMENUMBER
                    r"(?P<lastgamenumber>)lastgamenumber(?![\w$])",
                    r")|(",
                    r"(?P<lastposition>)lastposition(?![\w$])",  # LASTPOSITION
                    r")|(",
                    r"(?P<lca>)lca\s*\(",  # LCA
                    r")|(",
                    r"(?P<left>)left(?![\w$])",  # LEFT
                    r")|(",
                    r"(?P<legal>)legal(?![\w$])",  # LEGAL
                    r")|(",
                    r"(?P<light>)light(?![\w$])",  # LIGHT
                    r")|(",
                    r"(?P<line>)line(?![\w$])",  # LINE
                    r")|(",
                    r"(?P<local>)local(?![\w$])",  # LOCAL
                    r")|(",
                    r"(?P<loop>)loop(?![\w$])",  # LOOP
                    r")|(",
                    r"(?P<lowercase>)lowercase(?![\w$])",  # LOWERCASE
                    r")|(",
                    r"(?P<maindiagonal>)maindiagonal(?![\w$])",  # MAINDIAGONAL
                    r")|(",
                    r"(?P<mainline>)mainline(?![\w$])",  # MAINLINE
                    r")|(",
                    # MAKESQUARE_PARENTHESES
                    r"(?P<makesquare_parentheses>)makesquare\s*\(",
                    r")|(",
                    # MAKESQUARE_STRING
                    r'(?P<makesquare_string>)makesquare(?=\s*")',
                    r")|(",
                    r"(?P<mate>)mate(?![\w$])",  # MATE
                    r")|(",
                    r"(?P<max>)max\s*\(",  # MAX
                    r")|(",
                    r"(?P<max_parameter>)max(?![\w$])",  # MAX_PARAMETER
                    r")|(",
                    r"(?P<message>)message(?=(?:\s+quiet)?\s*\()",  # MESSAGE
                    r")|(",
                    r"(?P<min>)min\s*\(",  # MIN
                    r")|(",
                    r"(?P<modelmate>)modelmate(?![\w$])",  # MODELMATE
                    r")|(",
                    # MODELSTALEMATE
                    r"(?P<modelstalemate>)modelstalemate(?![\w$])",
                    r")|(",
                    r"(?P<movenumber>)movenumber(?![\w$])",  # MOVENUMBER
                    r")|(",
                    r"(?P<move>)move(?![\w$])",  # MOVE
                    r")|(",
                    r"(?P<nestban>)nestban(?![\w$])",  # NESTBAN
                    r")|(",
                    r"(?P<northeast>)northeast(?![\w$])",  # NORTHEAST
                    r")|(",
                    r"(?P<northwest>)northwest(?![\w$])",  # NORTHWEST
                    r")|(",
                    r"(?P<notransform>)notransform(?![\w$])",  # NOTRANSFORM
                    r")|(",
                    r"(?P<not>)not(?![\w$])",  # NOT
                    r")|(",
                    r"(?P<nullmove>)nullmove(?![\w$])",  # NULLMOVE
                    r")|(",
                    r"(?P<null>)null(?![\w$])",  # NULL
                    r")|(",
                    r"(?P<offdiagonal>)offdiagonal(?![\w$])",  # OFFDIAGONAL
                    r")|(",
                    r"(?P<ooo>)o-o-o(?![\w$])",  # OOO
                    r")|(",
                    r"(?P<oo>)o-o(?![\w$])",  # OO
                    r")|(",
                    # ORIGINALCOMMENT
                    r"(?P<originalcomment>)originalcomment(?![\w$])",
                    r")|(",
                    r"(?P<orthogonal>)orthogonal(?![\w$])",  # ORTHOGONAL
                    r")|(",
                    r"(?P<or>)or(?![\w$])",  # OR
                    r")|(",
                    r"(?P<parent>)parent(?![\w$])",  # PARENT
                    r")|(",
                    r"(?P<passedpawns>)passedpawns(?![\w$])",  # PASSEDPAWNS
                    r")|(",
                    # PATHCOUNTUNFOCUSED
                    r"(?P<pathcountunfocused>)pathcountunfocused(?![\w$])",
                    r")|(",
                    r"(?P<pathcount>)pathcount(?![\w$])",  # PATHCOUNT
                    r")|(",
                    # PATHLASTPOSITION
                    r"(?P<pathlastposition>)pathlastposition(?![\w$])",
                    r")|(",
                    r"(?P<pathstart>)pathstart(?![\w$])",  # PATHSTART
                    r")|(",
                    r"(?P<path>)(?:path(?![\w$])|\u22a2)",  # PATH
                    r")|(",
                    # PERSISTENT_QUIET
                    r"persistent\s+quiet\s+(?P<persistent_quiet>\w+)",
                    r"(?=\s*(?:=|\+=|-=|\*=|/=|%=))",
                    r")|(",
                    # PERSISTENT
                    r"persistent\s+(?P<persistent>\w+)",
                    r"(?=\s*(?:=|\+=|-=|\*=|/=|%=))",
                    r")|(",
                    r"(?P<pieceid>)pieceid(?![\w$])",  # PIECEID
                    r")|(",
                    r"(?P<piecename>)piecename(?![\w$])",  # PIECENAME
                    r")|(",
                    r"(?P<piecepath>)piecepath(?![\w$])",  # PIECEPATH
                    r")|(",
                    # PIECE_VARIABLE
                    r"(?:piece\s+|\u25ed|\[Aa\])",
                    r"(?P<piece_variable>[\w$]+)\s*(?==)",
                    r")|(",
                    # PIECE
                    r"?:piece\s+(?:all\s+)?(?P<piece>",
                    r"[a-zA-Z0-9_$]+)\s+in(?![\w$])",
                    r")|(",
                    r"(?P<pin>)pin(?![\w$])",  # PIN
                    r")|(",
                    # PLAYER
                    r"(?P<player>)player(?:\s+(?:black|white))?(?![\w$])",
                    r")|(",
                    r"(?P<ply>)ply(?![\w$])",  # PLY
                    r")|(",
                    r"(?P<positionid>)positionid(?![\w$])",  # POSITIONID
                    r")|(",
                    r"(?P<position>)position(?![\w$])",  # POSITION
                    r")|(",
                    r"(?P<power>)power(?![\w$])",  # POWER
                    r")|(",
                    r"(?P<previous>)previous(?![\w$])",  # PREVIOUS
                    r")|(",
                    r"(?P<primary>)primary(?![\w$])",  # PRIMARY
                    r")|(",
                    r"(?P<promote>)promote(?![\w$])",  # PROMOTE
                    r")|(",
                    r"(?P<pseudolegal>)pseudolegal(?![\w$])",  # PSEUDOLEGAL
                    r")|(",
                    r"(?P<puremate>)puremate(?![\w$])",  # PUREMATE
                    r")|(",
                    # PURESTALEMATE
                    r"(?P<purestalemate>)purestalemate(?![\w$])",
                    r")|(",
                    r"(?P<quiet>)quiet(?![\w$])",  # QUIET
                    r")|(",
                    r"(?P<rank>)rank(?![\w$])",  # RANK
                    r")|(",
                    # RAY
                    r"(?P<ray>)ray",
                    r"(?:\s+(?:",
                    r"up|down|right|left|northeast|northwest",
                    r"|southwest|southeast|diagonal|orthogonal",
                    r"|vertical|horizontal|anydirection",
                    r"))*\s*\(",
                    r")|(",
                    r"(?P<readfile>)readfile(?![\w$])",  # READFILE
                    r")|(",
                    # REMOVECOMMENT
                    r"(?P<removecomment>)removecomment(?![\w$])",
                    r")|(",
                    r"(?P<result>)result(?![\w$])",  # RESULT
                    r")|(",
                    r"(?P<reversecolor>)reversecolor(?![\w$])",  # REVERSECOLOR
                    r")|(",
                    r"(?P<right>)right(?![\w$])",  # RIGHT
                    r")|(",
                    r"(?P<rotate45>)rotate45(?![\w$])",  # ROTATE45
                    r")|(",
                    r"(?P<rotate90>)rotate90(?![\w$])",  # ROTATE90
                    r")|(",
                    r"(?P<secondary>)secondary(?![\w$])",  # SECONDARY
                    r")|(",
                    r"(?P<settag>)settag\s*\(",  # SETTAG
                    r")|(",
                    # SHIFTHORIZONTAL
                    r"(?P<shifthorizontal>)shifthorizontal(?![\w$])",
                    r")|(",
                    # SHIFTVERTICAL
                    r"(?P<shiftvertical>)shiftvertical(?![\w$])",
                    r")|(",
                    r"(?P<shift>)shift(?![\w$])",  # SHIFT
                    r")|(",
                    r"(?P<sidetomove>)sidetomove(?![\w$])",  # SIDETOMOVE
                    r")|(",
                    r"(?P<singlecolor>)singlecolor(?![\w$])",  # SINGLECOLOR
                    r")|(",
                    r"(?P<site>)site(?![\w$])",  # SITE
                    r")|(",
                    r"(?P<sort>)sort(?:\s+min)?(?![\w$])",  # SORT
                    r")|(",
                    r"(?P<southeast>)southeast(?![\w$])",  # SOUTHEAST
                    r")|(",
                    r"(?P<southwest>)southwest(?![\w$])",  # SOUTHWEST
                    r")|(",
                    r"(?P<sqrt>)sqrt(?![\w$])",  # SQRT
                    r")|(",
                    # SQUARE
                    r"?:square\s+(?:all\s+)?(?P<square>",
                    r"[a-zA-Z0-9_$]+)\s+in(?![\w$])",
                    r")|(",
                    r"(?P<stalemate>)stalemate(?![\w$])",  # STALEMATE
                    r")|(",
                    r"(?P<str_parentheses>)str\s*\(",  # STR_PARENTHESES
                    r")|(",
                    r"(?P<str>)str(?![\w$])",  # STR
                    r")|(",
                    r"(?P<tag>)tag(?![\w$])",  # TAG
                    r")|(",
                    r"(?P<terminal>)terminal(?![\w$])",  # TERMINAL
                    r")|(",
                    r"(?P<then>)then(?![\w$])",  # THEN
                    r")|(",
                    r"(?P<through>)through(?![\w$])",  # THROUGH
                    r")|(",
                    r"(?P<title>)title(?![\w$])",  # TITLE
                    r")|(",
                    r"(?P<to>)to(?![\w$])",  # TO
                    r")|(",
                    r"(?P<true>)true(?![\w$])",  # TRUE
                    r")|(",
                    r"(?P<try>)try(?![\w$])",  # TRY
                    r")|(",
                    r"(?P<typename>)typename(?![\w$])",  # TYPENAME
                    r")|(",
                    r"(?P<type>)type(?![\w$])",  # TYPE
                    r")|(",
                    r"(?P<unbind>)unbind(?![\w$])",  # UNBIND
                    r")|(",
                    r"(?P<uppercase>)uppercase(?![\w$])",  # UPPERCASE
                    r")|(",
                    r"(?P<up>)up(?![\w$])",  # UP
                    r")|(",
                    r"(?P<variation>)variation(?![\w$])",  # VARIATION
                    r")|(",
                    r"(?P<verbose>)verbose(?![\w$])",  # VERBOSE
                    r")|(",
                    r"(?P<vertical>)vertical(?![\w$])",  # VERTICAL
                    r")|(",
                    # VIRTUALMAINLINE
                    r"(?P<virtualmainline>)virtualmainline(?![\w$])",
                    r")|(",
                    r"(?P<while>)while(?=\s*\()",  # WHILE
                    r")|(",
                    r"(?P<white>)white(?![\w$])",  # WHITE
                    r")|(",
                    r"(?P<writefile>)writefile\s*\(",  # WRITEFILE
                    r")|(",
                    r"(?P<wtm>)wtm(?![\w$])",  # WTM
                    r")|(",
                    r"(?P<xray>)xray\s*\(",  # XRAY
                    r")|(",
                    r"(?P<year>)year(?![\w$])",  # YEAR
                    r")|(",
                    # EXISTENTIAL_SQUARE_VARIABLE
                    r"(?:)",
                    r"(?P<existential_square_variable>",
                    r"[a-zA-Z0-9_$]",
                    r"+)(?=\s*(?:\[element\]|\u220a))",
                    r")|(",
                    # EXISTENTIAL_PIECE_VARIABLE
                    r"(?:\[Aa\]|\u25ed)",
                    r"(?P<existential_piece_variable>",
                    r"[a-zA-Z0-9_$]",
                    r"+)(?=\s*(?:\[element\]|\u220a))",
                    r")|(",
                    # UNIVERSAL_SQUARE_VARIABLE
                    r"(?:\[forall\]|\u2200)",
                    r"(?P<universal_square_variable>",
                    r"[a-zA-Z0-9_$]",
                    r"+)(?=\s*(?:\[element\]|\u220a))",
                    r")|(",
                    # UNIVERSAL_PIECE_VARIABLE
                    r"(?:\[forall\]|\u2200)",
                    r"(?:\[Aa\]|\u25ed)",
                    r"(?P<universal_piece_variable>",
                    r"[a-zA-Z0-9_$]",
                    r"+)(?=\s*(?:\[element\]|\u220a))",
                    r")|(",
                    # PIECE_DESIGNATOR
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
                    r"|",
                    r"\u25a6",
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
                    r")|(",
                    # RESULT_ARGUMENT
                    r"(?P<result_argument>)(?:1-0|1/2-1/2|0-1)",
                    r")|(",
                    r"(?P<integer>)-?\d+",  # INTEGER
                    r")|(",
                    # KEYWORD_ANYTHING_ELSE
                    r"(?P<keyword_anything_else>)(?:",
                    r"ancestor",
                    r"|between",
                    r"|child",
                    r"|comment",
                    r"|consecutivemoves",
                    r"|cql",
                    r"|descendant",
                    r"|distance",
                    r"|echo",
                    r"|function",
                    r"|indexof",
                    r"|lca",
                    r"|makesquare",
                    r"|max",
                    r"|message",
                    r"|min",
                    r"|ray",
                    r"|settag",
                    r"|str",
                    r"|while",
                    r"|writefile",
                    r"|xray",
                    r")(?![\w$])",
                    r")|(",
                    r"(?P<function_call>[a-zA-Z0-9_$]+)\s*\(",  # FUNCTION_CALL
                    r")|(",
                    # VARIABLE_ASSIGN
                    r"(?P<variable_assign>[a-zA-Z0-9_$]+)(?=\s*=[^=])",
                    r")|(",
                    r"(?P<variable>[a-zA-Z0-9_$]+)",  # VARIABLE
                    r")|(",
                    r"(?P<backslash>)\\",  # BACKSLASH
                    r")|(",
                    r"(?P<any_square>)\.",  # ANY_SQUARE
                    r")|(",
                    r"(?P<bracket_left>)\[",  # BRACKET_LEFT
                    r")|(",
                    r"(?P<bracket_right>)\]",  # BRACKET_RIGHT
                    r")|(",
                    r"(?P<colon>):",  # COLON
                    r")|(",
                    r"(?P<intersection>)(?:&|\u2229)",  # INTERSECTION
                    r")|(",
                    r"(?P<lt>)<",  # LT
                    r")|(",
                    r"(?P<gt>)>",  # GT
                    r")|(",
                    r"(?P<plus>)\+",  # PLUS
                    r")|(",
                    r"(?P<star>)\*",  # STAR
                    r")|(",
                    r"(?P<modulus>)%",  # MODULUS
                    r")|(",
                    r"(?P<divide>)/",  # DIVIDE
                    r")|(",
                    r"(?P<minus>)-",  # MINUS
                    r")|(",
                    r"(?P<complement>)~",  # COMPLEMENT
                    r")|(",
                    r"(?P<union>)(?:\||\u222a)",  # UNION
                    r")|(",
                    r"(?P<assign>)=",  # ASSIGN
                    r")|(",
                    r"(?P<repeat_0_or_1>)\?",  # REPEAT_0_OR_1
                    r")|(",
                    r"(?P<count_filter>)#",  # COUNT_FILTER
                    r")|(",
                    r"(?P<anything_else>)[^/\s{}()]+",  # ANYTHING_ELSE
                    r")|(",
                    r"(?P<end_of_stream>)$",  # END_OF_STREAM
                    r")",
                )
            ),
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(PatternAttributes))
    runner().run(loader(Pattern))
