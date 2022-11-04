# constants.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Constants used when parsing Chess Query Language statements."""
from pgn_read.core.constants import (
    FILE_NAMES,
    RANK_NAMES,
    FEN_WHITE_KING,
    FEN_WHITE_QUEEN,
    FEN_WHITE_ROOK,
    FEN_WHITE_BISHOP,
    FEN_WHITE_KNIGHT,
    FEN_WHITE_PAWN,
    FEN_BLACK_KING,
    FEN_BLACK_QUEEN,
    FEN_BLACK_ROOK,
    FEN_BLACK_BISHOP,
    FEN_BLACK_KNIGHT,
    FEN_BLACK_PAWN,
)

# PGN results.  pgn_read.core.constants has '*' as DEFAULT_TAG_RESULT_VALUE
# but does not have constants for the other three results.
# CQL does not support the notion of unknown result ('*').
WHITE_WIN = "1-0"
BLACK_WIN = "0-1"
DRAW = "1/2-1/2"

FNR = "-".join((FILE_NAMES[0], FILE_NAMES[-1]))
RNR = "-".join((RANK_NAMES[-1], RANK_NAMES[0]))

# pgn_read.constants.RANK_NAMES is in reverse order to that used in chessql.
# pgn_read.constants.FILE_NAMES is in order used in chessql.
CQL_RANK_NAMES = "".join(reversed(RANK_NAMES))

# The pgn_read package uses "NOPIECE = ''" for empty squares but CQL has to use
# a non-null character to represent empty squares in statements.
# At CQL version 5.1 the value for EMPTY_SQUARE_NAME was '.' but '.' means all
# squares at version 6.0 and the value is now '_'.
EMPTY_SQUARE_NAME = r"_"

# The Portable Game Notation specification does not have the notions of 'any
# white piece' or 'any black piece': nor does the pgn_read package.
# ChessTab supports these notions and 'A', and 'a', were chosen to instantiate
# the notions on databases because these were used by CQL version 5.1.  If CQL
# changes it's mind on the values in future ChessTab will be unable to follow,
# and will have to map the new CQL values to 'A' and 'a' to fit existing
# databases.
ANY_WHITE_PIECE_NAME = r"A"
ANY_BLACK_PIECE_NAME = r"a"

WHITE_PIECE_NAMES = (
    FEN_WHITE_KING
    + FEN_WHITE_QUEEN
    + FEN_WHITE_ROOK
    + FEN_WHITE_BISHOP
    + FEN_WHITE_KNIGHT
    + FEN_WHITE_PAWN
)
BLACK_PIECE_NAMES = (
    FEN_BLACK_KING
    + FEN_BLACK_QUEEN
    + FEN_BLACK_ROOK
    + FEN_BLACK_BISHOP
    + FEN_BLACK_KNIGHT
    + FEN_BLACK_PAWN
)

ALL_GAMES_MATCH_PIECE_DESIGNATORS = (
    ANY_WHITE_PIECE_NAME
    + ANY_BLACK_PIECE_NAME
    + FEN_WHITE_KING
    + FEN_BLACK_KING
    + EMPTY_SQUARE_NAME
)
ALL_PIECES = WHITE_PIECE_NAMES + BLACK_PIECE_NAMES + EMPTY_SQUARE_NAME

PIECE_NAMES = (
    WHITE_PIECE_NAMES
    + BLACK_PIECE_NAMES
    + ANY_WHITE_PIECE_NAME
    + ANY_BLACK_PIECE_NAME
    + EMPTY_SQUARE_NAME
)

# These are used when processing elements of a CQL statement, but not in the
# definition of the regular expression for the whole statement.
# Piece designators in particular.
RANGE_SEPARATOR = r"-"
COMPOUND_DESIGNATOR_START = r"\["
COMPOUND_DESIGNATOR_END = r"\]"
FILE_DESIGNATOR = r"[" + FNR + r"]"
RANK_DESIGNATOR = r"[" + RNR + r"]"
SQUARE_DESIGNATOR_SEPARATOR = r","
FILE_RANGE = FILE_DESIGNATOR + RANGE_SEPARATOR + FILE_DESIGNATOR
RANK_RANGE = RANK_DESIGNATOR + RANGE_SEPARATOR + RANK_DESIGNATOR
SIMPLE_SQUARE_DESIGNATOR = r"".join(
    (
        FNR.join((r"[", r"](?:-[", r"])")),
        RNR.join((r"?[", r"](?:-[", r"])?")),
    )
)
COMPOUND_SQUARE_DESIGNATOR = SIMPLE_SQUARE_DESIGNATOR.join(
    (r"\[", r"(?:,", r")*]")
)

# This is used in the definition of the regular expression for the whole
# statement.  The piecedesignator module has PieceDesignator.PIECE_DESIGNATOR
# which splits things according to the processing required.
# '\b' works as the trailing delimiter only for piece designators consisting of
# a single piece name.
PIECE_DESIGNATOR = r"".join(
    (
        r"(?:",
        r"(?:",
        SIMPLE_SQUARE_DESIGNATOR,
        r"|",
        COMPOUND_SQUARE_DESIGNATOR,
        r")|",
        r"(?:",
        r"(?:",
        PIECE_NAMES.join((r"[", r"]|\[(?:[", r"]+)]")),
        r")",
        r"(?:",
        SIMPLE_SQUARE_DESIGNATOR,
        r"|",
        COMPOUND_SQUARE_DESIGNATOR,
        r")",
        r")|",
        PIECE_NAMES.join((r"\[(?:[", r"]+)]")),
        r")(?![a-zA-Z0-9_[\]])",
        r"|",
        PIECE_NAMES.join((r"[", r"]\b")),
    )
)

# The eight basic direction names.
# These refer to the natural directions on the chessboard from the white
# perspective.
UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"
NORTHEAST = "northeast"
NORTHWEST = "northwest"
SOUTHEAST = "southeast"
SOUTHWEST = "southwest"

# The five compound directions.
DIAGONAL = "diagonal"  # NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST
ORTHOGONAL = "orthogonal"  # UP, DOWN, LEFT, RIGHT
VERTICAL = "vertical"  # UP, DOWN
HORIZONTAL = "horizontal"  # LEFT, RIGHT
ANYDIRECTION = "anydirection"  # ORTHOGONAL, DIAGONAL

del FEN_WHITE_KING
del FEN_WHITE_QUEEN
del FEN_WHITE_ROOK
del FEN_WHITE_BISHOP
del FEN_WHITE_KNIGHT
del FEN_WHITE_PAWN
del FEN_BLACK_KING
del FEN_BLACK_QUEEN
del FEN_BLACK_ROOK
del FEN_BLACK_BISHOP
del FEN_BLACK_KNIGHT
del FEN_BLACK_PAWN
del RANK_NAMES
del FNR, RNR
