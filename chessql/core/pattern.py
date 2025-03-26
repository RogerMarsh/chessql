# pattern.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Pattern used when parsing Chess Query Language (CQL) statements.

The initial definition is for CQL-6.0.4 with additions for later versions.

Definitions exist for each token in the CQL language, and these are
combined to form the pattern for the regular expression applied to the
text of a CQL statement.

"""
import re

from . import elements
from . import hhdb

# Pattern for regular expression to parse CQL query files (*.cql).
CQL_TOKENS = r")|(".join(
    (
        # Structure tokens and tokens longer than two characters.
        # Before two character tokens.
        r"(" + elements.BLOCK_COMMENT,  # 6.0.4
        elements.LINE_COMMENT,  # 6.0.4
        elements.STRING,  # 6.0.4
        elements.END_OF_LINE,  # 6.2
        elements.WHITESPACE,  # 6.0.4
        elements.BRACE_RIGHT,  # 6.0.4
        elements.WILDCARD_PLUS,  # 6.0.4
        elements.WILDCARD_STAR,  # 6.0.4
        elements.REGEX_REPEAT,  # 6.1
        elements.BRACE_LEFT,  # 6.0.4
        elements.PARENTHESIS_LEFT,  # 6.0.4
        elements.PARENTHESIS_RIGHT,  # 6.0.4
        elements.ARROW_BACKWARD,  # 6.0.4
        elements.ARROW_FORWARD,  # 6.0.4
        elements.AFTER_EQ,  # 6.2
        elements.AFTER_NE,  # 6.2
        elements.BEFORE_EQ,  # 6.2
        elements.BEFORE_NE,  # 6.2
        elements.TAKE_LR,  # 6.2
        elements.TAKE_LI,  # 6.2
        elements.TAKE_IR,  # 6.2
        elements.TAKE_II,  # 6.2
        elements.COMMENT_SYMBOL,  # 6.2
        # Two character tokens.
        # Before one character tokens.
        elements.ATTACK_ARROW,  # 6.2
        elements.ATTACKED_ARROW,  # 6.2
        elements.DASH_LR,  # 6.2
        elements.DASH_LI,  # 6.2
        elements.DASH_IR,  # 6.2
        elements.DASH_II,  # 6.2
        elements.REGEX_MATCH,  # 6.1
        elements.REGEX_CAPTURED_GROUP,  # 6.1
        elements.REGEX_CAPTURED_GROUP_INDEX,  # 6.1
        elements.EMPTY_SQUARES,  # 6.1
        elements.LE,  # 6.0.4
        elements.GE,  # 6.0.4
        elements.EQ,  # 6.0.4
        elements.NE,  # 6.0.4
        elements.ASSIGN_IF,  # 6.0.4
        elements.ASSIGN_PLUS,  # 6.0.4
        elements.ASSIGN_MINUS,  # 6.0.4
        elements.ASSIGN_DIVIDE,  # 6.0.4
        elements.ASSIGN_MULTIPLY,  # 6.0.4
        elements.ASSIGN_MODULUS,  # 6.0.4
        # Keywords.
        # Before piece designator.
        elements.ABS,  # 6.0.4
        elements.ALL,  # 6.0.4
        elements.ANCESTOR,  # 6.0.4 deprecated 6.2
        elements.AND,  # 6.0.4
        elements.ANYDIRECTION,  # 6.0.4
        elements.ASCII,  # 6.1
        elements.ASSERT,  # 6.1
        elements.ATOMIC,  # 6.2
        elements.ATTACKEDBY,  # 6.0.4 deprecated 6.2
        elements.ATTACKS,  # 6.0.4 deprecated 6.2
        elements.BETWEEN,  # 6.0.4
        elements.BLACK,  # 6.0.4
        elements.BTM,  # 6.0.4
        elements.CAPTURE,  # 6.0.4
        elements.CASTLE,  # 6.0.4
        elements.CHECK,  # 6.0.4
        elements.CHILD_PARENTHESES,  # 6.0.4
        elements.CHILD,  # 6.0.4
        elements.COLORTYPE,  # 6.0.4 deprecated 6.2
        elements.COMMENT_PARENTHESES,  # 6.0.4
        elements.COMMENT,  # 6.0.4
        elements.CONNECTEDPAWNS,  # 6.0.4
        elements.CONSECUTIVEMOVES,  # 6.0.4
        elements.COUNT,  # 6.0.4
        elements.COUNTMOVES,  # 6.2
        elements.CQL,  # 6.0.4
        elements.CURRENTMOVE,  # 6.2
        elements.CURRENTPOSITION,  # 6.0.4
        elements.CURRENTTRANSFORM,  # 6.0.4
        elements.DARK,  # 6.0.4
        elements.DATE,  # 6.1
        elements.DEPTH,  # 6.0.4
        elements.DESCENDANT,  # 6.0.4 deprecated 6.2
        elements.DIAGONAL,  # 6.0.4
        elements.DICTIONARY,  # 6.1
        elements.DISTANCE,  # 6.0.4
        elements.DOUBLEDPAWNS,  # 6.0.4
        elements.DOWN,  # 6.0.4
        elements.ECHO,  # 6.0.4
        elements.ECO,  # 6.1
        elements.ELEMENT,  # 6.2
        elements.ELO,  # 6.0.4
        elements.ELSE,  # 6.0.4
        elements.ENPASSANT,  # 6.0.4
        elements.ENPASSANTSQUARE,  # 6.0.4
        elements.EVENTDATE,  # 6.1
        elements.EVENT,  # 6.0.4
        elements.FALSE,  # 6.0.4
        elements.FEN,  # 6.0.4
        elements.FILE,  # 6.0.4
        elements.FIND,  # 6.0.4
        elements.FIRSTMATCH,  # 6.0.4
        elements.FLIPCOLOR,  # 6.0.4
        elements.FLIPHORIZONTAL,  # 6.0.4
        elements.FLIPVERTICAL,  # 6.0.4
        elements.FLIP,  # 6.0.4
        elements.FOCUS_CAPTURE,  # 6.2
        elements.FOCUS,  # 6.2
        elements.FROM,  # 6.0.4
        elements.FUNCTION,  # 6.0.4
        elements.GAMENUMBER,  # 6.0.4
        elements.HASCOMMENT,  # 6.0.4
        hhdb.HHDB,  # 6.1
        elements.HORIZONTAL,  # 6.0.4
        elements.IDEALMATE,  # 6.2
        elements.IDEALSTALEMATE,  # 6.2
        elements.IF,  # 6.0.4
        elements.INDEXOF,  # 6.1
        elements.INITIALPOSITION,  # 6.1
        elements.INITIAL,  # 6.0.4
        elements.INT,  # 6.1
        elements.IN_ALL,  # 6.0.4
        elements.IN,  # 6.0.4
        elements.ISBOUND,  # 6.1
        elements.ISOLATEDPAWNS,  # 6.0.4
        elements.ISUNBOUND,  # 6.1
        elements.KEEPALLBEST,  # 6.2
        elements.LASTGAMENUMBER,  # 6.2
        elements.LASTPOSITION,  # 6.0.4
        elements.LCA,  # 6.0.4
        elements.LEFT,  # 6.0.4
        elements.LEGAL,  # 6.0.4
        elements.LIGHT,  # 6.0.4
        elements.LINE,  # 6.0.4 deprecated 6.2
        elements.LOCAL,  # 6.2
        elements.LOOP,  # 6.0.4
        elements.LOWERCASE,  # 6.1
        elements.MAINDIAGONAL,  # 6.0.4
        elements.MAINLINE,  # 6.0.4
        elements.MAKESQUARE_PARENTHESES,  # 6.0.4
        elements.MAKESQUARE_STRING,  # 6.0.4
        elements.MATE,  # 6.0.4
        elements.MAX,  # 6.0.4
        elements.MAX_PARAMETER,  # 6.2
        elements.MESSAGE_PARENTHESES,  # 6.0.4
        elements.MESSAGE,  # 6.0.4
        elements.MIN,  # 6.0.4
        elements.MODELMATE,  # 6.2
        elements.MODELSTALEMATE,  # 6.2
        elements.MOVENUMBER,  # 6.0.4
        elements.MOVE,  # 6.0.4 deprecated 6.2
        elements.NESTBAN,  # 6.0.4
        elements.NORTHEAST,  # 6.0.4
        elements.NORTHWEST,  # 6.0.4
        elements.NOTRANSFORM,  # 6.0.4
        elements.NOT,  # 6.0.4
        elements.NULLMOVE,  # 6.2
        elements.NULL,  # 6.0.4
        elements.OFFDIAGONAL,  # 6.0.4
        elements.OOO,  # 6.0.4
        elements.OO,  # 6.0.4
        elements.ORIGINALCOMMENT,  # 6.1
        elements.ORTHOGONAL,  # 6.0.4
        elements.OR,  # 6.0.4
        elements.PARENT,  # 6.0.4
        elements.PASSEDPAWNS,  # 6.0.4
        elements.PATHCOUNTUNFOCUSED,  # 6.2
        elements.PATHCOUNT,  # 6.2
        elements.PATHLASTPOSITION,  # 6.2
        elements.PATHSTART,  # 6.2
        elements.PATH,  # 6.2
        elements.PERSISTENT_QUIET,  # 6.0.4
        elements.PERSISTENT,  # 6.0.4
        elements.PIECEID,  # 6.0.4
        elements.PIECENAME,  # 6.2
        elements.PIECEPATH,  # 6.2
        elements.PIECE_VARIABLE,  # 6.2
        elements.PIECE,  # 6.0.4
        elements.PIN,  # 6.0.4
        elements.PLAYER,  # 6.0.4
        elements.PLY,  # 6.0.4
        elements.POSITIONID,  # 6.0.4
        elements.POSITION,  # 6.0.4
        elements.POWER,  # 6.0.4
        elements.PREVIOUS,  # 6.0.4
        elements.PRIMARY,  # 6.0.4
        elements.PROMOTE,  # 6.0.4
        elements.PSEUDOLEGAL,  # 6.0.4
        elements.PUREMATE,  # 6.2
        elements.PURESTALEMATE,  # 6.2
        elements.QUIET,  # 6.0.4
        elements.RANK,  # 6.0.4
        elements.RAY,  # 6.0.4
        elements.READFILE,  # 6.1
        elements.REMOVECOMMENT,  # 6.1
        elements.RESULT,  # 6.0.4
        elements.REVERSECOLOR,  # 6.0.4
        elements.RIGHT,  # 6.0.4
        elements.ROTATE45,  # 6.0.4
        elements.ROTATE90,  # 6.0.4
        elements.SECONDARY,  # 6.0.4
        elements.SETTAG,  # 6.1
        elements.SHIFTHORIZONTAL,  # 6.0.4
        elements.SHIFTVERTICAL,  # 6.0.4
        elements.SHIFT,  # 6.0.4
        elements.SIDETOMOVE,  # 6.0.4
        elements.SINGLECOLOR,  # 6.0.4
        elements.SITE,  # 6.0.4
        elements.SORT,  # 6.0.4
        elements.SOUTHEAST,  # 6.0.4
        elements.SOUTHWEST,  # 6.0.4
        elements.SQRT,  # 6.0.4
        elements.SQUARE,  # 6.0.4
        elements.STALEMATE,  # 6.0.4
        elements.STR_PARENTHESES,  # 6.1
        elements.STR,  # 6.1
        elements.TAG,  # 6.1
        elements.TERMINAL,  # 6.0.4
        elements.THEN,  # 6.0.4 deprecated 6.1
        elements.THROUGH,  # 6.0.4
        elements.TITLE,  # 6.2
        elements.TO,  # 6.0.4
        elements.TRUE,  # 6.0.4
        elements.TRY,  # 6.2
        elements.TYPENAME,  # 6.2
        elements.TYPE,  # 6.0.4
        elements.UNBIND,  # 6.1
        elements.UPPERCASE,  # 6.1
        elements.UP,  # 6.0.4
        elements.VARIATION,  # 6.0.4
        elements.VERBOSE,  # 6.2
        elements.VERTICAL,  # 6.0.4
        elements.VIRTUALMAINLINE,  # 6.0.4
        elements.WHILE,  # 6.1
        elements.WHITE,  # 6.0.4
        elements.WRITEFILE,  # 6.1
        elements.WTM,  # 6.0.4
        elements.XRAY,  # 6.0.4 deprecated 6.2
        elements.YEAR,  # 6.0.4
        # Before 'all pieces'.
        elements.EXISTENTIAL_SQUARE_VARIABLE,  # 6.2
        elements.EXISTENTIAL_PIECE_VARIABLE,  # 6.2
        elements.UNIVERSAL_SQUARE_VARIABLE,  # 6.2
        elements.UNIVERSAL_PIECE_VARIABLE,  # 6.2
        # Square and piece designators, and variable names and values.
        elements.PIECE_DESIGNATOR,  # 6.0.4
        # Before integer.
        elements.RESULT_ARGUMENT,  # 6.0.4
        elements.INTEGER,  # 6.0.4
        # Various '<keyword>(' constructs are caught earlier, leaving
        # 'keyword' without a suffix to be caught incorrectly by VARIABLE
        # without this entry in the absence of 'keyword(?![\w$])' pattern.
        elements.KEYWORD_ANYTHING_ELSE,  # 6.0.4
        # Immediately before VARIABLE, but with same 'after' conditions.
        elements.FUNCTION_CALL,  # 6.0.4
        # After all keywords and square and piece designators.
        elements.VARIABLE_ASSIGN,  # 6.0.4
        elements.VARIABLE,  # 6.0.4
        # One character tokens.
        elements.BACKSLASH,  # 6.1
        # After piece designator.
        elements.ANY_SQUARE,  # 6.0.4
        # After compound square designator.
        # SQUARE_SEPARATOR,  # 6.0.4  should not need this group.
        elements.BRACKET_LEFT,  # 6.1
        elements.BRACKET_RIGHT,  # 6.1
        # Before anything else.
        # EMPTY_SQUARE,  # 6.0.4  should not need this group.
        elements.COLON,  # 6.0.4
        elements.INTERSECTION,  # 6.0.4
        elements.LT,  # 6.0.4
        elements.GT,  # 6.0.4
        elements.PLUS,  # 6.0.4
        elements.STAR,  # 6.0.4
        elements.MODULUS,  # 6.0.4
        elements.DIVIDE,  # 6.0.4
        elements.MINUS,  # 6.0.4
        elements.COMPLEMENT,  # 6.0.4
        elements.UNION,  # 6.0.4
        elements.ASSIGN,  # 6.0.4
        elements.REPEAT_0_OR_1,  # 6.0.4
        elements.COUNT_FILTER,  # 6.0.4
        # Eventually matching anything else will be a syntax error.
        elements.ANYTHING_ELSE,  # 6.0.4
        # End of CQL statement.
        elements.END_OF_STREAM + r")",  # 6.0.4
    )
)
cql_re = re.compile(CQL_TOKENS)
