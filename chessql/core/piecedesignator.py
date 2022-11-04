# piecedesignator.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (ChessQL) piece designator evaluator."""
import re
import collections

from .constants import (
    RANGE_SEPARATOR,
    COMPOUND_DESIGNATOR_START,
    COMPOUND_DESIGNATOR_END,
    ANY_WHITE_PIECE_NAME,
    ANY_BLACK_PIECE_NAME,
    PIECE_NAMES,
    FILE_RANGE,
    RANK_RANGE,
    FILE_DESIGNATOR,
    RANK_DESIGNATOR,
    SQUARE_DESIGNATOR_SEPARATOR,
    FILE_NAMES,
    CQL_RANK_NAMES,
)
from . import empty_copy


# Originally written to the cql1.0 definition.
# The composite piece types U, M, m, I, i, and ?, had disappeared by the cql5.0
# definition.
# The CQL syntax is very different but the piece designator syntax is the same,
# so some of this class needs to be re-written.
# A further change occurs at cql6.0 where empty square is '_', not '.'.
class PieceDesignator:
    """ChessQL piece designator base class.

    Impossible piece square combinations are accepted, pawns on ranks 1 and 8
    for example, but later processing may make assumptions about the need to
    look at the database for them.

    """

    simple_square_designator = r"".join(
        (
            r"(",
            FILE_RANGE,
            RANK_RANGE,
            r")",
            r"|",
            r"(",
            FILE_RANGE,
            RANK_DESIGNATOR,
            r")",
            r"|",
            r"(",
            FILE_DESIGNATOR,
            RANK_RANGE,
            r")",
            r"|",
            r"(",
            FILE_DESIGNATOR,
            RANK_DESIGNATOR,
            r")",
        )
    )
    square_designator = r"".join(
        (
            r"(?:",
            COMPOUND_DESIGNATOR_START,
            r"([a-h][-a-h1-8]*[1-8](?:,[a-h][-a-h1-8]*[1-8])*)",
            COMPOUND_DESIGNATOR_END,
            r")",
            r"|",
            r"(?:",
            simple_square_designator,
            r")",
        )
    )
    piece_type_designator = r"".join(
        (
            r"(?:",
            COMPOUND_DESIGNATOR_START,
            r"([^",
            COMPOUND_DESIGNATOR_END,
            r"]+)",
            COMPOUND_DESIGNATOR_END,
            r")",
            r"|",
            r"([",
            PIECE_NAMES,
            r"])",
        )
    )

    # This is used to split the piece designator to fit the processing needed.
    # The constants module defines a PIECE_DESIGNATOR which consumes a piece
    # designator without collecting the component parts.
    PIECE_DESIGNATOR = r"".join(
        (
            r"(?:",
            square_designator,
            r")",
            r"|",
            r"(?:(?:(?:",
            piece_type_designator,
            r")(?:",
            square_designator,
            r"))",
            r"|",
            r"(?:",
            piece_type_designator,
            r")",
            r")",
        )
    )
    del simple_square_designator, square_designator, piece_type_designator

    piece_designator = re.compile(PIECE_DESIGNATOR)

    # Renamed from PieceDesignator to avoid confusion with class name.
    # Prompted by pylint no-member reports for the item names: such as
    # "compoundpiece_s".
    # It does not stop the no-member messages.
    PieceDesignatorNT = collections.namedtuple(
        "PieceDesignatorNT",
        " ".join(
            (
                "compoundsquare",
                "filerankrange",
                "filerange",
                "rankrange",
                "square",
                "compoundpiece_s",
                "piece_s",
                "p_compoundsquare",
                "p_filerankrange",
                "p_filerange",
                "p_rankrange",
                "p_square",
                "compoundpiece",
                "piece",
            )
        ),
    )

    # Default value.
    # When True the items in designator_set must not be in position.
    emptysquare = False

    def __init__(self, token):
        """Initialise a PieceDesignator instance for token."""
        self._token = token
        self._designator_set = None
        self._square_ranges_valid = None
        self._match = None
        self._groups = None

    def parse(self):
        """Extract the piece designator from this instance's token.

        The groups extracted using the PieceDesignator.PIECE_DESIGNATOR
        regular expression are made available self._groups.

        """
        self._match = self.piece_designator.match(self._token)
        if self._match:
            self._groups = self.PieceDesignatorNT(
                *self._match.groups(default="")
            )

    def __deepcopy__(self, memo):
        """Make a copy to which a transform can be applied.

        The transform is applied to the squares named in _groups and the piece
        designator text in _token.leaf is adjusted to fit.  Then _match and
        _groups are calculated using parse method.  These changes will be made
        to newcopy leaving self alone.

        """
        newcopy = empty_copy(self)
        newcopy._token = self._token
        newcopy._designator_set = None
        newcopy._square_ranges_valid = None
        newcopy._match = None
        newcopy._groups = self._groups
        return newcopy

    @property
    def designator_set(self):
        """Return the piece designator set."""
        return self._designator_set

    @staticmethod
    def expand_composite_square(startfile, endfile, startrank, endrank):
        """Return the set of squares implied by a square designator."""
        files = FILE_NAMES[
            FILE_NAMES.index(startfile) : FILE_NAMES.index(endfile)
        ]
        files += endfile
        ranks = CQL_RANK_NAMES[
            CQL_RANK_NAMES.index(startrank) : CQL_RANK_NAMES.index(endrank)
        ]
        ranks += endrank
        return {f + r for f in files for r in ranks}

    def expand_piece_designator(self):
        """Expand a piece designator into a set of simple piece designators.

        The set is available in property designator_set.

        Return None.

        """
        if self._groups is None:
            return
        squareset = set()
        self._square_ranges_valid = True
        for sqr in self.get_squares_list():
            if len(sqr) == 2:
                squareset.update(
                    self.expand_composite_square(
                        sqr[0], sqr[0], sqr[1], sqr[1]
                    )
                )
            elif len(sqr) == 6:
                if sqr[0] > sqr[2] or sqr[3] > sqr[5]:
                    self._square_ranges_valid = False
                squareset.update(
                    self.expand_composite_square(
                        sqr[0], sqr[2], sqr[3], sqr[5]
                    )
                )
            elif len(sqr) == 4:
                if sqr[1] == "-":
                    if sqr[0] > sqr[2]:
                        self._square_ranges_valid = False
                    squareset.update(
                        self.expand_composite_square(
                            sqr[0], sqr[2], sqr[3], sqr[3]
                        )
                    )
                elif sqr[2] == "-":
                    if sqr[1] > sqr[3]:
                        self._square_ranges_valid = False
                    squareset.update(
                        self.expand_composite_square(
                            sqr[0], sqr[0], sqr[1], sqr[3]
                        )
                    )
            else:
                squareset.add("")  # Any square, s assumed to be ''.
        self._designator_set = {
            p + s for p in self.get_pieces() for s in squareset
        }

    def get_shift_limits(self, ranklimits, filelimits):
        """Adjust ranges in ranklimits and filelimits to fit square designator.

        For first piece designator subject to one of the shift transforms the
        limits are ['8', '1'] and ['h', 'a'].

        The limits are not changed for piece designators which do not limit
        the squares ('q' for example).  Thus 'shift { Q q r }' would leave the
        limits as ['8', '1'] and ['h', 'a'].  The rank range '1-8' and the file
        range 'a-h' do not limit the squares in the relevant direction so these
        two ranges do not adjust the relevant limits.

        A piece designator with a single square sets the low and high limits to
        the square ( 'Kb2' produces ['2', '2'] and ['b', 'b'] for example).

        The four cases with rank and file ranges are:

        'Ra-h1-8' produces limits ['8', '1'] and ['h', 'a'] (not changed)
        'Ra-h2-8' produces limits ['2', '8'] and ['h', 'a']
        'Ra-d1-8' produces limits ['8', '1'] and ['a', 'd']
        'Ra-d2-8' produces limits ['2', '8'] and ['a', 'd']

        A piece designator with a compound square sets the limits to restrict
        shifting:

        'R[b2,g7}' produces ['2', '7'] and ['b', 'g']
        'R[a-h2,g7}' produces ['2', '7'] and ['g', 'g']
        'R[b1-8,g7}' produces ['7', '7'] and ['b', 'g']
        'R[a-h1-8,g7}' produces ['7', '7'] and ['g', 'g']

        Shifts on braced filters are similar:

        'shift { Rb2 kg7 }' produces ['2', '7'] and ['b', 'g']

        and so forth.

        shiftvertical and shifthorizontal generate the same limits but
        application to filters produces different results.

        """
        lowfile = FILE_NAMES[-1]
        highfile = FILE_NAMES[0]
        lowrank = CQL_RANK_NAMES[-1]
        highrank = CQL_RANK_NAMES[0]
        for sqr in self.get_squares_list():
            if len(sqr) == 2:
                lowfile = min(lowfile, sqr[0])
                highfile = max(highfile, sqr[0])
                lowrank = min(lowrank, sqr[1])
                highrank = max(highrank, sqr[1])
            elif len(sqr) == 6:
                if sqr[0] > sqr[2] or sqr[3] > sqr[5]:
                    self._square_ranges_valid = False
                if sqr[0] != FILE_NAMES[0] or sqr[2] != FILE_NAMES[-1]:
                    lowfile = min(lowfile, sqr[0])
                    highfile = max(highfile, sqr[2])
                if sqr[3] != CQL_RANK_NAMES[0] or sqr[5] != CQL_RANK_NAMES[-1]:
                    lowrank = min(lowrank, sqr[3])
                    highrank = max(highrank, sqr[5])
            elif len(sqr) == 4:
                if sqr[1] == RANGE_SEPARATOR:
                    if sqr[0] > sqr[2]:
                        self._square_ranges_valid = False
                    if sqr[0] != FILE_NAMES[0] or sqr[2] != FILE_NAMES[-1]:
                        lowfile = min(lowfile, sqr[0])
                        highfile = max(highfile, sqr[2])
                    lowrank = min(lowrank, sqr[3])
                    highrank = max(highrank, sqr[3])
                elif sqr[2] == RANGE_SEPARATOR:
                    if sqr[1] > sqr[3]:
                        self._square_ranges_valid = False
                    lowfile = min(lowfile, sqr[0])
                    highfile = max(highfile, sqr[0])
                    if (
                        sqr[1] != CQL_RANK_NAMES[0]
                        or sqr[3] != CQL_RANK_NAMES[-1]
                    ):
                        lowrank = min(lowrank, sqr[1])
                        highrank = max(highrank, sqr[3])
        if ranklimits:
            ranklimits[0] = min(ranklimits[0], lowrank)
            ranklimits[1] = max(ranklimits[1], highrank)
        if filelimits:
            filelimits[0] = min(filelimits[0], lowfile)
            filelimits[1] = max(filelimits[1], highfile)

    def get_pieces(self):
        """Return the piece type designator component of the piece designator.

        The absence of any piece type, including empty square, means any white
        or black piece.  In this case 'Aa' is returned.

        """
        groups = self._groups
        # False positive no-member reports by pylint are ignored.
        pieces = "".join(
            (
                groups.compoundpiece_s,
                groups.piece_s,
                groups.compoundpiece,
                groups.piece,
            )
        )
        if not pieces:
            pieces = ANY_WHITE_PIECE_NAME + ANY_BLACK_PIECE_NAME
        return pieces

    def get_squares(self):
        """Return the square designator component of the piece designator."""
        groups = self._groups
        # False positive no-member reports by pylint are ignored.
        return "".join(
            (
                groups.compoundsquare,
                groups.filerankrange,
                groups.filerange,
                groups.rankrange,
                groups.square,
                groups.p_compoundsquare,
                groups.p_filerankrange,
                groups.p_filerange,
                groups.p_rankrange,
                groups.p_square,
            )
        )

    def get_squares_list(self):
        """Return list of squares in the piece designator."""
        return self.get_squares().split(SQUARE_DESIGNATOR_SEPARATOR)

    def is_compound_squares(self):
        """Return True if a compound square is given, otherwise False."""
        groups = self._groups
        # False positive no-member reports by pylint are ignored.
        return bool(groups.compoundsquare or groups.p_compoundsquare)

    def is_compound_pieces(self):
        """Return True if a compound piece is given, otherwise False."""
        groups = self._groups
        # False positive no-member reports by pylint are ignored.
        return bool(groups.compoundpiece_s or groups.compoundpiece)
