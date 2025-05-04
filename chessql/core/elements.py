# elements.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Elements for pattern to parse Chess Query Language (CQL) statements.

The initial definition is for CQL-6.0.4 with additions for later versions.

Definitions exist for each token in the CQL language, and these are
combined to form the pattern for the regular expression applied to the
text of a CQL statement.

In '#' comments '6.0.4 index of symbols' and '6.1 index of symbols' mean
'6.2 ascii symbols' too because the reference changes it's name with the
introduction of 'unicode symbols'.

"""
from . import constants

# 6.0.4 overview of comments.  Ignore text in *.cql file.
BLOCK_COMMENT = r"(?P<block_comment>)/\*(?:[^*]|(?:\*(?!/)))*\*/"
LINE_COMMENT = r"(?P<line_comment>)(?:////|//(?!/))[^\n]*\n+"

# Quoted strings are used but do not have a reference.
# For example go to sort filter page from 6.0.4 table of filters.
STRING = r"(?P<string>)" + constants.QUOTED_STRING

# Ignore whitespace in *.cql file.
# At 6.2 a line of whitespace is needed to terminate a path filter,
# but end of file will do.
WHITESPACE = r"(?P<whitespace>)\s+"

# 6.0.4 table of filters: line '{range}' parameter.
# The 6.0 syntax option '{2 3}' is not supported because it would allow
# '{2 3}' at 6.1 and later. '{2,3}' is supported at 6.0 but the examples
# use the '{2 3}' option.
# The line filter is deprecated at 6.2.
REGEX_REPEAT = r"(?P<regex_repeat>)\{(?:(?:\d+(?:,(?:\d+)?)?)|(?:,(?:\d+)))\}"

# 6.0.4 table of filters: symbolic filters: {}.
BRACE_LEFT = r"(?P<brace_left>){"  # Start compound filter.
BRACE_RIGHT = r"(?P<brace_right>)}"  # End compound filter.

# 6.0.4 precedence.
# Some filters take arguments enclosed in '()'.  The precedence reference
# does not cover this.
PARENTHESIS_LEFT = r"(?P<parenthesis_left>)\("  # Start parenthesis block.
PARENTHESIS_RIGHT = r"(?P<parenthesis_right>)\)"  # End parenthesis block.

# Anything which does not start something.
# This will be last clause of pattern.CQL_TOKENS except for END_OF_STREAM.
# Bug?  Should '[', ']', and '"', be in this pattern too?
ANYTHING_ELSE = r"(?P<anything_else>)[^/\s{}()]+"

# Keywords not caught by '(?![\w$])' pattern suffix because their relation to
# a '(' is established by a pattern suffix.
# This clause exists to prevent interpreting these keywords as variable
# names if the expected '(' is missing.
KEYWORD_ANYTHING_ELSE = r"".join(
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
)

END_OF_STREAM = r"(?P<end_of_stream>)$"  # Final match in input.

AFTER_EQ = r"(?P<after_eq>)(?:\[>=\]|\u227d)"  # 6.2 unicode symbols, '[>=]'.
BEFORE_EQ = r"(?P<before_eq>)(?:\[<=\]|\u227c)"  # 6.2 unicode symbols, '[<=]'.

ARROW_BACKWARD = r"(?P<arrow_backward>)<--"  # find and line parameter, '<--'.
ARROW_FORWARD = r"(?P<arrow_forward>)-->"  # line parameter '>--'.

WILDCARD_PLUS = r"(?P<wildcard_plus>){\+}"  # line parameter, '{+}'.
WILDCARD_STAR = r"(?P<wildcard_star>){\*}"  # line parameter, '{*}'.

AFTER_NE = r"(?P<after_ne>)(?:\[>\]|\u227b)"  # 6.2 unicode symbols, '[>]'.
BEFORE_NE = r"(?P<before_ne>)(?:\[<\]|\u227a)"  # 6.2 unicode symbols, '[<]'.

# 6.2 table of filters, '///' described with comment filter.
COMMENT_SYMBOL = r"(?P<comment_symbol>)///(?!/)"

# 6.2 '///' filter needs to catch next '\n'.
END_OF_LINE = r"(?P<end_of_line>)(?:\s*)\n+"

LE = r"(?P<le>)(?:<=|\u2264)"  # 6.0.4 index of symbols, 6.2 unicode symbols.
GE = r"(?P<ge>)(?:>=|\u2265)"  # 6.0.4 index of symbols, 6.2 unicode symbols.
EQ = r"(?P<eq>)=="  # 6.0.4 index of symbols, '=='.
NE = r"(?P<ne>)(?:!=|\u2260)"  # 6.0.4 index of symbols, 6.2 unicode symbols.

ASSIGN_IF = r"(?P<assign_if>)=\?"  # 6.0.4 index of symbols, '=?'.
ASSIGN_PLUS = r"(?P<assign_plus>)\+="  # 6.0.4 index of symbols, '+='.
ASSIGN_MINUS = r"(?P<assign_minus>)-="  # 6.0.4 index of symbols '-='.
ASSIGN_DIVIDE = r"(?P<assign_divide>)/="  # 6.0.4 index of symbols, '/='.
ASSIGN_MULTIPLY = r"(?P<assign_multiply>)\*="  # 6.0.4 index of symbols, '*='.
ASSIGN_MODULUS = r"(?P<assign_modulus>)%="  # 6.0.4 index of symbols, '\='.

REGEX_MATCH = r"(?P<regex_match>)~~"  # 6.1 index of symbols, '~~'.

# 6.1 strings and regular expressions, '\<any number of digits>' eg '\1'.
REGEX_CAPTURED_GROUP = r"(?P<regex_captured_group>)\\\d+"

# 6.1 strings and regular expressions, '\-<any number of digits>' eg '\-1'.
REGEX_CAPTURED_GROUP_INDEX = r"(?P<regex_captured_group_index>)\\-\d+"

EMPTY_SQUARES = r"(?P<empty_squares>)\[\]"  # 6.1 index of symbols, '[]'.
ATTACK_ARROW = r"(?P<attack_arrow>)(?:->|\u2192)"  # 6.2 unicode symbols, '->'.

# 6.2 unicode symbols, '<-'.
ATTACKED_ARROW = r"(?P<attacked_arrow>)(?:<-|\u2190)"

# 6.2 unicode symbols, '--'.  Dash filters (any move).
# F and G must be set filters when attached to '--'.
# F--G, F --G, F-- G, and F -- G, are different: a ' ' attached to '--'
# means the left or right filter, as appropriate, is 'a-h1-8' (all squares).
# '--r=b' is like 'F --G=Q' and is accepted.
# '(--)' and '{--}' are like 'F -- G'.  Must be distinguished from 'F--G'.
# 'V="d" V[--]' and 'V="d" V[ -- ]' are not accepted.
# '--(r q B)' is like parenthesized arguments to the '--' filter,
# but '-- (r q B)' is not accepted, unlike 'ray (r q B)'.
# Also 'ray/* text */(r q B)' is accepted but not '--/* text */(r q B)'.
# '{r b}--{N Q} is F--G with both being compound filters, and the
# expression '{r b}--{N Q}=b(r q B)' is legal but will never match since
# F is not asking for a black pawn move promoting to bishop.
DASH_II = r"(?P<dash_ii>)(?:--|\u2015\u2015)"
DASH_LI = r"(?P<dash_li>)(?<=\S)(?:--|\u2015\u2015)"
DASH_IR = r"(?P<dash_ir>)(?:--|\u2015\u2015)(?=\S)"
DASH_LR = r"(?P<dash_lr>)(?<=\S)(?:--|\u2015\u2015)(?=\S)"

# 6.2 unicode symbols, '[x]'.  Similar to the dash filters.
# Take filters (dash filters for captures only).  (unicode given as U+D7)
# F[x]G, F [x]G, F[x] G, and F [x] G, are different: a ' ' attached to '[x]'
# means the left or right filter, as appropriate, is 'a-h1-8' (all squares).
TAKE_II = r"(?P<take_ii>)(?:\[x\]|\u00d7)"
TAKE_LI = r"(?P<take_li>)(?<=\S)(?:\[x\]|\u00d7)"
TAKE_IR = r"(?P<take_ir>)(?:\[x\]|\u00d7)(?=\S)"
TAKE_LR = r"(?P<take_lr>)(?<=\S)(?:\[x\]|\u00d7)(?=\S)"

# 6.0.4 index of symbols, '.'.  6.2 unicode symbols (equivalent to 'a-h1-8').
ANY_SQUARE = r"(?P<any_square>)(?:\.|\u25a6)"

# 6.0.4 index of symbols, '_'.  6.2 unicode symbols.
EMPTY_SQUARE = r"(?P<empty_square>)(?:_|\u25a1)"

COLON = r"(?P<colon>):"  # 6.0.4 index of symbols, ':'.

# 6.0.4 index of symbols, '&'.  6.2 unicode symbols.
INTERSECTION = r"(?P<intersection>)(?:&|\u2229)"

LT = r"(?P<lt>)<"  # 6.0.4 index of symbols, '<'.
GT = r"(?P<gt>)>"  # 6.0.4 index of symbols, '>'.
PLUS = r"(?P<plus>)\+"  # 6.0.4 index of symbols, '+'.
STAR = r"(?P<star>)\*"  # 6.0.4 index of symbols, '*'.
MODULUS = r"(?P<modulus>)%"  # 6.0.4 index of symbols, '\'.
DIVIDE = r"(?P<divide>)/"  # 6.0.4 index of symbols, '/'.
MINUS = r"(?P<minus>)-"  # 6.0.4 index of symbols, '-'.  Minus or unary minus.
COMPLEMENT = r"(?P<complement>)~"  # 6.0.4 index of symbols, '~'.

# 6.0.4 index of symbols, '|'.  6.2 unicode symbols.
UNION = r"(?P<union>)(?:\||\u222a)"

# 6.0.4 index of symbols, '='.  6.2 unicode symbols.
# Assign to variable or '=T' construct in '--' or '[x]' filters.
ASSIGN = r"(?P<assign>)="

REPEAT_0_OR_1 = r"(?P<repeat_0_or_1>)\?"  # 6.2 ascii symbols, '?'.
COUNT_FILTER = r"(?P<count_filter>)#"  # 6.0.4 index of symbols, '#'.

# 6.0.4 index of symbols, ','.
# Definition not used because the PIECE_DESIGNATOR pattern handles it.
SQUARE_SEPARATOR = r"(?P<square_separator>),"

BACKSLASH = r'(?P<backslash>)\\[n"tr\\]'

# 6.0.4 slice a string.  6.1 dictionary key.
# According to comments in .filters module the piece designator and
# regular expression uses are handled elsewhere.
BRACKET_LEFT = r"(?P<bracket_left>)\["
BRACKET_RIGHT = r"(?P<bracket_right>)\]"

ABS = r"(?P<abs>)abs(?![\w$])"  # 6.0.4 table of filters.

# parameter for find, piece, and square filters.
ALL = r"(?P<all>)all(?![\w$])"

ANCESTOR = r"(?P<ancestor>)ancestor\s*\("  # 6.0.4 table of filters.
AND = r"(?P<and>)and(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 direction filters.  Not listed in table of filters.
# Also ray parameter.
ANYDIRECTION = r"(?P<anydirection>)anydirection(?![\w$])"

ATTACKEDBY = r"(?P<attackedby>)attackedby(?![\w$])"  # 6.0.4 table of filters.
ATTACKS = r"(?P<attacks>)attacks(?![\w$])"  # 6.0.4 table of filters.
BETWEEN = r"(?P<between>)between\s*\("  # 6.0.4 table of filters.

# Black filter. See ELO and PLAYER for interpretation as parameter.
BLACK = r"(?P<black>)black(?![\w$])"

BTM = r"(?P<btm>)btm(?![\w$])"  # 6.0.4 table of filters.
CAPTURE = r"(?P<capture>)capture(?![\w$])"  # Move parameter.

# Move parameter.  Also filter at 6.2.
CASTLE = r"(?P<castle>)castle(?![\w$])"

CHECK = r"(?P<check>)check(?![\w$])"  # 6.0.4 table of filters.

# Child filter with and without parenthesized argument.
CHILD_PARENTHESES = r"(?P<child_parentheses>)child\s*\("
CHILD = r"(?P<child>)child(?![\w$])"

COLORTYPE = r"(?P<colortype>)colortype(?![\w$])"  # 6.0.4 table of filters.

# Comment filter or parameter to move filter, with and without parenthesized
# argument.  Not mentioned in 6.1 table of filters entry for move, or the
# move documentation, but is mentioned in comment documentation in
# 'Using comment with the move filter' section.
# Nothing is said in 6.2 because move is deprecated and '///' is preferred
# over 'comment' for comments.
COMMENT_PARENTHESES = r"(?P<comment_parentheses>)comment\s*\("
COMMENT = r"(?P<comment>)comment(?![\w$])"

# 6.0.4 table of filters.
CONNECTEDPAWNS = r"(?P<connectedpawns>)connectedpawns(?![\w$])"

# 6.0.4 table of filters.
CONSECUTIVEMOVES = constants.VARIABLE_NAME_CHARS.join(
    (
        r"(?P<consecutivemoves>)consecutivemoves(?:\s+quiet(?:\s+(?:\d+|",
        r"+)(?:\s+(?:\d+|",
        r"+))?)?|\s+(?:\d+|",
        r"+)(?:\s+(?:\d+|",
        r"+))?(?:\s+quiet)?)?\s*\(",
    )
)

COUNT = r"(?P<count>)count(?![\w$])"  # Move parameter.

# 6.0.4 cqlparameters.html (Command line options : override input parameter).
# Collect all characters between '(' and ')' in 'cql(...)', without an
# attempt to parse them.  Filenames including whitespace or ')' must be in
# a quoted string.
CQL = r"cql\s*\((?P<cql>(?:(?:" + constants.QUOTED_STRING + r")|[^)])*)\)"

# 6.0.4 table of filters.
# "\u2219" added to CURRENTPOSITION at 6.2.
CURRENTPOSITION = r"(?P<currentposition>)(?:currentposition(?![\w$])|\u2219)"

# 'currenttransform' argument to comment or message filters.
CURRENTTRANSFORM = r"(?P<currenttransform>)currenttransform(?![\w$])"

DARK = r"(?P<dark>)dark(?![\w$])"  # 6.0.4 table of filters.
DEPTH = r"(?P<depth>)depth(?![\w$])"  # 6.0.4 table of filters.
DESCENDANT = r"(?P<descendant>)descendant\s*\("  # 6.0.4 table of filters.

# 6.0.4 direction filters.  Not listed in table of filters.
# Also ray parameter.
DIAGONAL = r"(?P<diagonal>)diagonal(?![\w$])"

DISTANCE = r"(?P<distance>)distance\s*\("  # 6.0.4 table of filters.

# 6.0.4 table of filters.
DOUBLEDPAWNS = r"(?P<doubledpawns>)doubledpawns(?![\w$])"

# 6.0.4 table of filters, and ray parameter.
DOWN = r"(?P<down>)down(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters.
ECHO = r"".join(
    (
        r"(?P<echo>)echo(?:\s+quiet)?\s*\(\s*\w+\s+\w+\s*\)",
        r"(?:\s*in\s+all(?![\w$]))?\s*",
    )
)

# 6.0.4 table of filters.  With and without black or white parameters.
ELO = r"(?P<elo>)elo(?:\s+(?:black|white))?(?![\w$])"

ELSE = r"(?P<else>)else(?![\w$])"  # If parameter.

# Move parameter.
ENPASSANT = r"(?P<enpassant>)enpassant(?![\w$])"
ENPASSANTSQUARE = r"(?P<enpassantsquare>)enpassantsquare(?![\w$])"

EVENT = r"(?P<event>)event(?![\w$])"  # 6.0.4 table of filters.
FALSE = r"(?P<false>)false(?![\w$])"  # 6.0.4 table of filters.
FEN = r"(?P<fen>)fen(?![\w$])"  # 6.0.4 table of filters.
FILE = r"(?P<file>)file(?![\w$])"  # 6.0.4 table of filters.
FIND = r"(?P<find>)find(?![\w$])"  # 6.0.4 table of filters.

# Line and path parameter.
FIRSTMATCH = r"(?P<firstmatch>)firstmatch(?![\w$])"

# 6.0.4 table of filters.  "\u2735" added at 6.2.
FLIP = r"(?P<flip>)(?:flip(?![\w$])|\u2735)"

# 6.0.4 table of filters.  "\u2b13" added at 6.2.
FLIPCOLOR = r"(?P<flipcolor>)(?:flipcolor(?![\w$])|\u2b13)"

# 6.0.4 table of filters.
FLIPHORIZONTAL = r"(?P<fliphorizontal>)fliphorizontal(?![\w$])"

# 6.0.4 table of filters.
FLIPVERTICAL = r"(?P<flipvertical>)flipvertical(?![\w$])"

FROM = r"(?P<from>)from(?![\w$])"  # Move and pin parameter.

# 6.0.4 table of filters.
FUNCTION = r"function\s+(?P<function>[\w$]+)\s*\([^)]*\)\s*(?=\{)"

# 6.0.4 function (function calling).
FUNCTION_CALL = constants.VARIABLE_NAME_CHARS.join(
    (r"(?P<function_call>", r"+)\s*\(")
)

# 6.0.4 table of filters.
GAMENUMBER = r"(?P<gamenumber>)gamenumber(?![\w$])"

# 6.0.4 table of filters.
# Synonym for 'originalcomment' at 6.1 but is backward compatible.
HASCOMMENT = r"(?P<hascomment>)hascomment(?![\w$])"

# 6.0.4 direction filters, and ray parameter.
HORIZONTAL = r"(?P<horizontal>)horizontal(?![\w$])"

IF = r"(?P<if>)if(?![\w$])"  # 6.0.4 table of filters.
IN_ALL = r"(?P<in_all>)in\s+all(?![\w$])"  # Echo parameter.

# 6.0.4 table of filters, and piece or square parameter
IN = r"(?P<in>)in(?![\w$])"

INITIAL = r"(?P<initial>)initial(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters.
ISOLATEDPAWNS = r"(?P<isolatedpawns>)isolatedpawns(?![\w$])"

# Line and path parameter.
LASTPOSITION = r"(?P<lastposition>)lastposition(?![\w$])"

LCA = r"(?P<lca>)lca\s*\("  # 6.0.4 table of filters.
LEFT = r"(?P<left>)left(?![\w$])"  # 6.0.4 table of filters, and ray parameter.
LEGAL = r"(?P<legal>)legal(?![\w$])"  # Move parameter.
LIGHT = r"(?P<light>)light(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters.  Deprecated at 6.2.
LINE = r"(?P<line>)line(?![\w$])"

LOOP = r"(?P<loop>)loop(?![\w$])"  # 6.0.4 table of filters.

# Not listed in 6.0.4 table of filters or direction filters,
# but behaves as one.
# Also ray parameter.
MAINDIAGONAL = r"(?P<maindiagonal>)maindiagonal(?![\w$])"

MAINLINE = r"(?P<mainline>)mainline(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters.
# String argument option added at 6.1 so two objects now.
MAKESQUARE_PARENTHESES = r"(?P<makesquare_parentheses>)makesquare\s*\("
MAKESQUARE_STRING = r'(?P<makesquare_string>)makesquare(?=\s*")'

MATE = r"(?P<mate>)mate(?![\w$])"  # 6.0.4 table of filters.
MAX = r"(?P<max>)max\s*\("  # 6.0.4 table of filters.

# Path parameter.  Must be after MAX in pattern.
MAX_PARAMETER = r"(?P<max_parameter>)max(?![\w$])"

# 6.0.4 table of filters.  'quiet' added at 6.1.
MESSAGE_PARENTHESES = r"(?P<message_parentheses>)message(?:\s+quiet)?\s*\("
MESSAGE = r"(?P<message>)message(?:\s+quiet)?(?![\w$])"

# 6.0.4 table of filters. 'min' as a sort parameter is caught in SORT.
MIN = r"(?P<min>)min\s*\("

# 6.0.4 table of filters.  Deprecated at 6.2.
MOVE = r"(?P<move>)move(?![\w$])"

MOVENUMBER = r"(?P<movenumber>)movenumber(?![\w$])"  # 6.0.4 table of filters.
NESTBAN = r"(?P<nestban>)nestban(?![\w$])"  # Line and path parameter.

# 6.0.4 table of filters, and ray parameter.
NORTHEAST = r"(?P<northeast>)northeast(?![\w$])"
NORTHWEST = r"(?P<northwest>)northwest(?![\w$])"

NOT = r"(?P<not>)not(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters.
NOTRANSFORM = r"(?P<notransform>)notransform(?![\w$])"

NULL = r"(?P<null>)null(?![\w$])"  # Move parameter.
OO = r"(?P<oo>)o-o(?![\w$])"  # Move parameter.  Also filter at 6.2.
OOO = r"(?P<ooo>)o-o-o(?![\w$])"  # Move parameter.  Also filter at 6.2.

# Not listed in 6.0.4 table of filters or direction filters,
# but behaves as one.
# Also ray parameter.
OFFDIAGONAL = r"(?P<offdiagonal>)offdiagonal(?![\w$])"

# 6.0.4 direction filters.  Not listed in table of filters.
# Also ray parameter.
ORTHOGONAL = r"(?P<orthogonal>)orthogonal(?![\w$])"

OR = r"(?P<or>)or(?![\w$])"  # 6.0.4 table of filters.
PARENT = r"(?P<parent>)parent(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters.
PASSEDPAWNS = r"(?P<passedpawns>)passedpawns(?![\w$])"

# 6.0.4 table of filters, with and without quiet parameter.
PERSISTENT_QUIET = constants.VARIABLE_NAME_CHARS.join(
    (
        r"persistent\s+quiet\s+(?P<persistent_quiet>",
        r"+)(?=\s*(?:=|\+=|-=|\*=|/=|%=))",
    )
)
PERSISTENT = constants.VARIABLE_NAME_CHARS.join(
    (r"persistent\s+(?P<persistent>", r"+)(?=\s*(?:=|\+=|-=|\*=|/=|%=))")
)

# 6.0.4 table of filters.
# Piece in filter with or without all parameter.
PIECE = constants.VARIABLE_NAME_CHARS.join(
    (
        r"?:piece\s+(?:all\s+)?(?P<piece>",
        r"+)\s+in(?![\w$])",
    )
)

# 6.0.4 table of filters.
# Piece assignment filter. Must appear before PIECE in pattern.
# In piece assignment "\u25edx=N" means "piece x=N" for example
# (See variables.html#pieceassignment)
# where "\u25ed" is represented as "[Aa]" in ASCII.
# PIECE_VARIABLE is a better name than PIECE_ASSIGNMENT in cql module.
PIECE_VARIABLE = (
    r"(?:piece\s+|\u25ed|\[Aa\])(?P<piece_variable>[\w$]+)\s*(?==)"
)

PIECEID = r"(?P<pieceid>)pieceid(?![\w$])"  # 6.0.4 table of filters.
PIN = r"(?P<pin>)pin(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters, with and without black or white parameter.
PLAYER = r"(?P<player>)player(?:\s+(?:black|white))?(?![\w$])"

PLY = r"(?P<ply>)ply(?![\w$])"  # 6.0.4 table of filters.
POSITION = r"(?P<position>)position(?![\w$])"  # 6.0.4 table of filters.
POSITIONID = r"(?P<positionid>)positionid(?![\w$])"  # 6.0.4 table of filters.
POWER = r"(?P<power>)power(?![\w$])"  # 6.0.4 table of filters.
PREVIOUS = r"(?P<previous>)previous(?![\w$])"  # move parameter.

# Line, move, and path, parameter. Also filter at 6.2.
PRIMARY = r"(?P<primary>)primary(?![\w$])"

PROMOTE = r"(?P<promote>)promote(?![\w$])"  # Move parameter.

# Move parameter.
PSEUDOLEGAL = r"(?P<pseudolegal>)pseudolegal(?![\w$])"

# Consecutivemoves, echo, find, message, path, and persistent, filter
# parameter.  Also cql parameter.
QUIET = r"(?P<quiet>)quiet(?![\w$])"

RANK = r"(?P<rank>)rank(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters, with and without direction parameters.
RAY = r"".join(
    (
        r"(?P<ray>)ray",
        r"(?:\s+(?:",
        r"up|down|right|left|northeast|northwest|southwest|southeast",
        r"|diagonal|orthogonal|vertical|horizontal|anydirection",
        r"))*\s*\(",
    )
)

# 6.1 table of filters.
REMOVECOMMENT = r"(?P<removecomment>)removecomment(?![\w$])"

# 6.0.4 table of filters.
RESULT = r"(?P<result>)result(?![\w$])"

# 6.0.4 table of filters.
REVERSECOLOR = r"(?P<reversecolor>)reversecolor(?![\w$])"

RIGHT = r"(?P<right>)right(?![\w$])"  # 6.0.4 table of filters.
ROTATE45 = r"(?P<rotate45>)rotate45(?![\w$])"  # 6.0.4 table of filters.
ROTATE90 = r"(?P<rotate90>)rotate90(?![\w$])"  # 6.0.4 table of filters.

# Line and move parameter. Also filter at 6.2.
SECONDARY = r"(?P<secondary>)secondary(?![\w$])"

SHIFT = r"(?P<shift>)shift(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters.
SHIFTHORIZONTAL = r"(?P<shifthorizontal>)shifthorizontal(?![\w$])"

# 6.0.4 table of filters.
SHIFTVERTICAL = r"(?P<shiftvertical>)shiftvertical(?![\w$])"

SIDETOMOVE = r"(?P<sidetomove>)sidetomove(?![\w$])"  # 6.0.4 table of filters.

# Line parameter.
SINGLECOLOR = r"(?P<singlecolor>)singlecolor(?![\w$])"

SITE = r"(?P<site>)site(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters.
SORT = r"(?P<sort>)sort(?:\s+min)?(?![\w$])"

# 6.0.4 direction filters.  Not listed in table of filters.
# Also ray filter parameters.
SOUTHEAST = r"(?P<southeast>)southeast(?![\w$])"
SOUTHWEST = r"(?P<southwest>)southwest(?![\w$])"

SQRT = r"(?P<sqrt>)sqrt(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters, with and without all parameter.
SQUARE = constants.VARIABLE_NAME_CHARS.join(
    (
        r"?:square\s+(?:all\s+)?(?P<square>",
        r"+)\s+in(?![\w$])",
    )
)

STALEMATE = r"(?P<stalemate>)stalemate(?![\w$])"  # 6.0.4 table of filters.

# filter.
TERMINAL = r"(?P<terminal>)terminal(?![\w$])"  # 6.0.4 table of filters.

# if parameter.
THEN = r"(?P<then>)then(?![\w$])"

# pin parameter.
THROUGH = r"(?P<through>)through(?![\w$])"

# set filter, move parameter and pin parameter.
TO = r"(?P<to>)to(?![\w$])"

TRUE = r"(?P<true>)true(?![\w$])"  # 6.0.4 table of filters.
TYPE = r"(?P<type>)type(?![\w$])"  # 6.0.4 table of filters.

# 6.0.4 table of filters, and ray parameter.
UP = r"(?P<up>)up(?![\w$])"

# filter.
VARIATION = r"(?P<variation>)variation(?![\w$])"

# 6.0.4 direction filters.  Not listed in table of filters.
# Also ray parameter.
VERTICAL = r"(?P<vertical>)vertical(?![\w$])"

# 6.0.4 table of filters.
VIRTUALMAINLINE = r"(?P<virtualmainline>)virtualmainline(?![\w$])"

# 6.0.4 table of filters, elo and player parameter.
WHITE = r"(?P<white>)white(?![\w$])"

WTM = r"(?P<wtm>)wtm(?![\w$])"  # 6.0.4 table of filters.
XRAY = r"(?P<xray>)xray\s*\("  # 6.0.4 table of filters.
YEAR = r"(?P<year>)year(?![\w$])"  # 6.0.4 table of filters.

# Keywords defined at CQL-6.1.

ASCII = r"(?P<ascii>)ascii(?![\w$])"  # 6.1 table of filters.
ASSERT = r"(?P<assert>)assert(?![\w$])"  # 6.1 table of filters.
DATE = r"(?P<date>)date(?![\w$])"  # 6.1 table of filters.

# 6.1 table of filters.
DICTIONARY = constants.VARIABLE_NAME_CHARS.join(
    (
        r"(?:local\s+)?dictionary\s+(?P<dictionary>",
        r"+)",
    )
)

ECO = r"(?P<eco>)eco(?![\w$])"  # 6.1 table of filters.
EVENTDATE = r"(?P<eventdate>)eventdate(?![\w$])"  # 6.1 table of filters.

# 6.1 table of filters.
# 6.1 table of filters entry is inconsistent on '(' and ')' but main
# documnetation is clear.
INDEXOF = r"(?P<indexof>)indexof\s*\("

# 6.1 table of filters.
INITIALPOSITION = r"(?P<initialposition>)initialposition(?![\w$])"

INT = r"(?P<int>)int(?![\w$])"  # 6.1 table of filters.
ISBOUND = r"(?P<isbound>)isbound(?![\w$])"  # 6.1 table of filters.
ISUNBOUND = r"(?P<isunbound>)isunbound(?![\w$])"  # 6.1 table of filters.
LOWERCASE = r"(?P<lowercase>)lowercase(?![\w$])"  # 6.1 table of filters.

# 6.1 table of filters.
ORIGINALCOMMENT = r"(?P<originalcomment>)originalcomment(?![\w$])"

READFILE = r"(?P<readfile>)readfile(?![\w$])"  # 6.1 table of filters.
SETTAG = r"(?P<settag>)settag\s*\("  # 6.1 table of filters.

# 6.1 table of filters, with parenthesized arguments or string argument.
STR_PARENTHESES = r"(?P<str_parentheses>)str\s*\("
STR = r"(?P<str>)str(?![\w$])"

TAG = r"(?P<tag>)tag(?![\w$])"  # 6.1 table of filters.
UNBIND = r"(?P<unbind>)unbind(?![\w$])"  # 6.1 table of filters.

# 6.2 table of filters.
# In 6.1 table of filters the entry says lowercase but goes to correct place
# for uppercase.
UPPERCASE = r"(?P<uppercase>)uppercase(?![\w$])"

WHILE = r"(?P<while>)while(?=\s*\()"  # 6.1 table of filters.
WRITEFILE = r"(?P<writefile>)writefile\s*\("  # 6.1 table of filters.

# Keywords defined at CQL-6.2.

# 6.2 table of filters.  Entry is atomic variables but keyword is atomic.
ATOMIC = constants.VARIABLE_NAME_CHARS.join(
    (r"atomic\s+(?P<atomic>", r"+)(?=\s*(?:=))")
)

COUNTMOVES = r"(?P<countmoves>)countmoves(?![\w$])"  # 6.2 table of filters.

# 6.2 table of filters.
# Entry is 'currentmove filter' but keyword is currentmove.
CURRENTMOVE = r"(?P<currentmove>)currentmove(?![\w$])"

ELEMENT = r"(?P<element>)(?:\[element\]|\u220a)"  # 6.2 unicode symbols.

# 6.2 unicode symbols.  Path parameter.  Must be before FOCUS in pattern.
FOCUS_CAPTURE = r"(?P<focus_capture>)(?:focus\s+|\u25ce\s*)capture(?![\w$])"

# 6.2 unicode symbols.  Path parameter.
FOCUS = r"(?P<focus>)(?:focus(?![\w$])|\u25ce)"

# 6.2 unicode symbols.
# universal quantification of filter; no value.
# Not used in pattern because the symbol exists only as a variable name
# prefix associated with existence and universal iteration at 6.2.
FORALL = r"(?P<forall>)(?:\[forall\]|\u2200)"

IDEALMATE = r"(?P<idealmate>)idealmate(?![\w$])"  # 6.2 table of filters.

# 6.2 table of filters.
IDEALSTALEMATE = r"(?P<idealstalemate>)idealstalemate(?![\w$])"

KEEPALLBEST = r"(?P<keepallbest>)keepallbest(?![\w$])"  # Path parameter.

# 6.2 table of filters.
LASTGAMENUMBER = r"(?P<lastgamenumber>)lastgamenumber(?![\w$])"

LOCAL = r"(?P<local>)local(?![\w$])"  # 6.2 table of filters.
MODELMATE = r"(?P<modelmate>)modelmate(?![\w$])"  # 6.2 table of filters.

# 6.2 table of filters.
MODELSTALEMATE = r"(?P<modelstalemate>)modelstalemate(?![\w$])"

NULLMOVE = r"(?P<nullmove>)nullmove(?![\w$])"  # 6.2 table of filters.
PATH = r"(?P<path>)(?:path(?![\w$])|\u22a2)"  # 6.2 table of filters.

PATHCOUNT = r"(?P<pathcount>)pathcount(?![\w$])"  # 6.2 table of filters.

# 6.2 table of filters.
PATHCOUNTUNFOCUSED = r"(?P<pathcountunfocused>)pathcountunfocused(?![\w$])"
PATHLASTPOSITION = r"(?P<pathlastposition>)pathlastposition(?![\w$])"

PATHSTART = r"(?P<pathstart>)pathstart(?![\w$])"  # 6.2 table of filters.
PIECENAME = r"(?P<piecename>)piecename(?![\w$])"  # 6.2 table of filters.
PIECEPATH = r"(?P<piecepath>)piecepath(?![\w$])"  # Path parameter.
PUREMATE = r"(?P<puremate>)puremate(?![\w$])"  # 6.2 table of filters.

# 6.2 table of filters.
PURESTALEMATE = r"(?P<purestalemate>)purestalemate(?![\w$])"

TITLE = r"(?P<title>)title(?![\w$])"  # Path parameter.
TRY = r"(?P<try>)try(?![\w$])"  # 6.2 table of filters.
TYPENAME = r"(?P<typename>)typename(?![\w$])"  # 6.2 table of filters.
VERBOSE = r"(?P<verbose>)verbose(?![\w$])"  # Path parameter.

# 6.0.4 piece designators.
# 6.1 piece designators.
# 6.2 piece designators.
# The building blocks for PIECE_DESIGNATOR.
_SIMPLE_SQUARE = "".join(
    (
        r"[",
        constants.FILE_RANGE,
        r"](?:-[",
        constants.FILE_RANGE,
        r"])?[",
        constants.RANK_RANGE,
        r"](?:-[",
        constants.RANK_RANGE,
        r"])?",
    )
)
_COMPOUND_SQUARE = _SIMPLE_SQUARE.join((r"\[", r"(?:,", r")*\]"))
_PIECE_CHARS = constants.PIECE_NAMES.join((r"[", r"]"))
_SIMPLE_PIECE = _PIECE_CHARS + r"(?![\w$])"
_COMPOUND_PIECE = _PIECE_CHARS.join((r"\[", r"(?:", r")*\]"))
_UNICODE_PIECE_CHARS = r"".join(
    (
        r"\u25b3",  # ascii 'A'
        r"\u2654",  # ascii 'K'
        r"\u2655",  # ascii 'Q'
        r"\u2656",  # ascii 'R'
        r"\u2657",  # ascii 'B'
        r"\u2658",  # ascii 'N'
        r"\u2659",  # ascii 'P'
        r"\u25b2",  # ascii 'a'
        r"\u265a",  # ascii 'k'
        r"\u265b",  # ascii 'q'
        r"\u265c",  # ascii 'r'
        r"\u265d",  # ascii 'b'
        r"\u265e",  # ascii 'n'
        r"\u265f",  # ascii 'p'
        r"\u25a1",  # ascii '_'
    )
)
_UNICODE_PIECES = _UNICODE_PIECE_CHARS.join((r"(?:[", r"]+)|\[(?:[", r"]+)\]"))
_ALL_PIECES = r"\u25ed"  # Equivalent to '[Aa]'.
_SQUARE_OPTIONS = r"|".join((_COMPOUND_SQUARE, _SIMPLE_SQUARE))
PIECE_OPTIONS = r"|".join(
    (_COMPOUND_PIECE, _PIECE_CHARS, _UNICODE_PIECES, _ALL_PIECES)
)

# 6.0.4 piece designators.
# 6.1 piece designators.
# 6.2 piece designators.
PIECE_DESIGNATOR = "".join(
    (
        r"(?P<piece_designator>)",
        r"(?:(?:",
        PIECE_OPTIONS.join(("(?:", ")?")),
        _SQUARE_OPTIONS.join(("(?:", ")")),
        r")|(?:",
        r"|".join(
            (_COMPOUND_PIECE, _SIMPLE_PIECE, _UNICODE_PIECES, _ALL_PIECES)
        ),
        r"))",
    )
)

# 6.0.4 variables.
# 6.0.4 function.
# 6.1 dictionary.
VARIABLE = constants.VARIABLE_NAME_CHARS.join((r"(?P<variable>", r"+)"))

# 6.0.4 variables.
# 6.0.4 table of filters, in particular symbolic filter '='.
# 6.1 dictionary.
VARIABLE_ASSIGN = constants.VARIABLE_NAME_CHARS.join(
    (r"(?P<variable_assign>", r"+)(?=\s*=[^=])")
)

# 6.2 unicode symbols, in particular '[element]' and '[forall]'.
EXISTENTIAL_SQUARE_VARIABLE = "".join(
    (
        r"(?:)",
        r"(?P<existential_square_variable>",
        constants.VARIABLE_NAME_CHARS,
        r"+)(?=\s*(?:\[element\]|\u220a))",
    )
)
EXISTENTIAL_PIECE_VARIABLE = "".join(
    (
        r"(?:\[Aa\]|\u25ed)",
        r"(?P<existential_piece_variable>",
        constants.VARIABLE_NAME_CHARS,
        r"+)(?=\s*(?:\[element\]|\u220a))",
    )
)
UNIVERSAL_SQUARE_VARIABLE = "".join(
    (
        r"(?:\[forall\]|\u2200)\s*",
        r"(?P<universal_square_variable>",
        constants.VARIABLE_NAME_CHARS,
        r"+)(?=\s*(?:\[element\]|\u220a))",
    )
)
UNIVERSAL_PIECE_VARIABLE = "".join(
    (
        r"(?:\[forall\]|\u2200)\s*",
        r"(?:\[Aa\]|\u25ed)",
        r"(?P<universal_piece_variable>",
        constants.VARIABLE_NAME_CHARS,
        r"+)(?=\s*(?:\[element\]|\u220a))",
    )
)

# 6.0.4 result argument.
RESULT_ARGUMENT = r"(?P<result_argument>)(?:1-0|1/2-1/2|0-1)"

# Positive or negative number filter. count, or element of range, parameters.
INTEGER = r"(?P<integer>)\d+"
