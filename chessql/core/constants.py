# constants.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Constants used when parsing Chess Query Language statements."""
# It may not be possible to sustain this attempt to break the dependency on
# pgn_read if it proves necessary to retain the 'RAYS' attribute from the
# previous version of constants.
try:
    from pgn_read.core.constants import (
        FNR,
        RNR,
        WKING,
        WQUEEN,
        WROOK,
        WBISHOP,
        WKNIGHT,
        WPAWN,
        BKING,
        BQUEEN,
        BROOK,
        BBISHOP,
        BKNIGHT,
        BPAWN,
    )
except ImportError:  # Not ModuleNotFoundError for Pythons earlier than 3.6
    FNR = "a-h"
    RNR = "1-8"
    WKING = "K"
    WQUEEN = "Q"
    WROOK = "R"
    WBISHOP = "B"
    WKNIGHT = "N"
    WPAWN = "P"
    BKING = "k"
    BQUEEN = "q"
    BROOK = "r"
    BBISHOP = "b"
    BKNIGHT = "n"
    BPAWN = "p"

    # .statement imports these from pgn_read.core.constants if it can, so
    # provide them here in case pgn_read is not available.
    # CQL 5.1 does not allow '*' as a result (CQL 6.0.4 not tried yet).
    WHITE_WIN = "1-0"
    BLACK_WIN = "0-1"
    DRAW = "1/2-1/2"

# Derive FILE_NAMES and RANK_NAMES from FNR and RNR rather than MAPFILE and
# MAPRANK.
FILE_NAMES = "".join([chr(i) for i in range(ord(FNR[0]), ord(FNR[-1]) + 1)])
RANK_NAMES = "".join([chr(i) for i in range(ord(RNR[0]), ord(RNR[-1]) + 1)])

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

WHITE_PIECE_NAMES = WKING + WQUEEN + WROOK + WBISHOP + WKNIGHT + WPAWN
BLACK_PIECE_NAMES = BKING + BQUEEN + BROOK + BBISHOP + BKNIGHT + BPAWN

ALL_GAMES_MATCH_PIECE_DESIGNATORS = (
    ANY_WHITE_PIECE_NAME
    + ANY_BLACK_PIECE_NAME
    + WKING
    + BKING
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
