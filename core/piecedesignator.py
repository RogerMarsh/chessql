# piecedesignator.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (ChessQL) piece designator evaluator.

"""
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
    RANK_NAMES,
    )


# Originally written to the cql1.0 definition.
# The composite piece types U, M, m, I, i, and ?, had disappeared by the cql5.0
# definition.
# The CQL syntax is very different but the piece designator syntax is the same,
# so some of this class needs to be re-written.
class PieceDesignator:
    """ChessQL piece designator base class.

    Impossible piece square combinations are accepted, pawns on ranks 1 and 8
    for example, but later processing may make assumptions about the need to
    look at the database for them.

    """

    # Assume string selected by cql.core.constants.PIECE_DESIGNATOR when using
    # these re elements, which have the same names as their counterparts.
    SIMPLE_SQUARE_DESIGNATOR = r''.join(
        (r'(', FILE_RANGE, RANK_RANGE, r')', r'|',
         r'(', FILE_RANGE, RANK_DESIGNATOR, r')', r'|',
         r'(', FILE_DESIGNATOR, RANK_RANGE, r')', r'|',
         r'(', FILE_DESIGNATOR, RANK_DESIGNATOR, r')'
         ))
    SQUARE_DESIGNATOR = r''.join(
        (r'(?:', COMPOUND_DESIGNATOR_START,
         r'([a-h][-a-h1-8]*[1-8](?:,[a-h][-a-h1-8]*[1-8])*)',
         COMPOUND_DESIGNATOR_END, r')', r'|',
         r'(?:', SIMPLE_SQUARE_DESIGNATOR, r')',
         ))
    PIECE_TYPE_DESIGNATOR = r''.join(
        (r'(?:', COMPOUND_DESIGNATOR_START,
         r'([^', COMPOUND_DESIGNATOR_END, r']+)',
         COMPOUND_DESIGNATOR_END, r')', r'|',
         r'([', PIECE_NAMES, r'])',
         ))
    PIECE_DESIGNATOR = r''.join(
        (r'(?:', SQUARE_DESIGNATOR, r')', r'|',
         r'(?:(?:(?:', PIECE_TYPE_DESIGNATOR,
         r')(?:', SQUARE_DESIGNATOR, r'))', r'|',
         r'(?:', PIECE_TYPE_DESIGNATOR, r')',
         r')',
         ))
    piece_designator = re.compile(PIECE_DESIGNATOR)

    PieceDesignator = collections.namedtuple(
        'PieceDesignator',
        ' '.join(('compoundsquare',
                  'filerankrange',
                  'filerange',
                  'rankrange',
                  'square',
                  'compoundpiece_s',
                  'piece_s',
                  'p_compoundsquare',
                  'p_filerankrange',
                  'p_filerange',
                  'p_rankrange',
                  'p_square',
                  'compoundpiece',
                  'piece',
                  )))

    # Default value.
    # When True the items in designator_set must not be in position.
    emptysquare = False

    def __init__(self, token):
        """"""
        self._token = token
        self._designator_set = None
        self._square_ranges_valid = None
        self._match = None
        self._groups = None

    def parse(self):
        """"""
        self._match = self.piece_designator.match(self._token)
        if self._match:
            self._groups = self.PieceDesignator(*self._match.groups(default=''))

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
        """"""
        return self._designator_set

    @staticmethod
    def _expand_composite_square(startfile, endfile, startrank, endrank):
        """"""
        files = FILE_NAMES[
            FILE_NAMES.index(startfile):FILE_NAMES.index(endfile)]
        files += endfile
        ranks = RANK_NAMES[
            RANK_NAMES.index(startrank):RANK_NAMES.index(endrank)]
        ranks += endrank
        return {f + r for f in files for r in ranks}

    def expand_piece_designator(self):
        """"""
        if self._groups is None:
            return
        squareset = set()
        self._square_ranges_valid = True
        for s in self.get_squares_list():
            if len(s) == 2:
                squareset.update(self._expand_composite_square(
                    s[0], s[0], s[1], s[1]))
            elif len(s) == 6:
                if s[0] > s[2] or s[3] > s[5]:
                    self._square_ranges_valid = False
                squareset.update(self._expand_composite_square(
                    s[0], s[2], s[3], s[5]))
            elif len(s) == 4:
                if s[1] == '-':
                    if s[0] > s[2]:
                        self._square_ranges_valid = False
                    squareset.update(self._expand_composite_square(
                        s[0], s[2], s[3], s[3]))
                elif s[2] == '-':
                    if s[1] > s[3]:
                        self._square_ranges_valid = False
                    squareset.update(self._expand_composite_square(
                        s[0], s[0], s[1], s[3]))
            else:
                squareset.add('') # Any square, s assumed to be ''.

        # Back to 'for p in self.get_pieces()' if 'all white pieces' and
        # 'all black pieces' indexes are created.  Similarely 'empty square',
        # which does not, and cannot, give correct answer yet.
        self._designator_set = {p + s
                                for p in self.get_pieces()
                                for s in squareset}

    @staticmethod
    def piece_square_to_index(designator_set, index_prefix):
        """Convert piece designator set values to index format: Qa4 to a4Q.

        Assumed that having all index values for a square adjacent is better
        than having index values for piece together, despite the need for
        conversion.

        """
        ds = set()
        for ps in designator_set:
            if len(ps) != 1:
                ds.add(index_prefix + ps)
            else:
                ds.update({index_prefix + ps + s
                           for s in PieceDesignator._expand_composite_square(
                               FILE_NAMES[0],
                               FILE_NAMES[-1],
                               RANK_NAMES[0],
                               RANK_NAMES[-1])})
        return ds

    # If 'square piece' is better order than 'piece square'
    @staticmethod
    def piece_square_to_index(designator_set, index_prefix):
        """Convert piece designator set values to index format: Qa4 to a4Q.

        Assumed that having all index values for a square adjacent is better
        than having index values for piece together, despite the need for
        conversion.

        """
        ds = set()
        for ps in designator_set:
            if len(ps) != 1:
                ds.add(index_prefix + ps[1:] + ps[0])
            else:
                ds.update({index_prefix + s + ps
                           for s in PieceDesignator._expand_composite_square(
                               FILE_NAMES[0],
                               FILE_NAMES[-1],
                               RANK_NAMES[0],
                               RANK_NAMES[-1])})
        return ds

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
        lowrank = RANK_NAMES[-1]
        highrank = RANK_NAMES[0]
        for s in self.get_squares_list():
            if len(s) == 2:
                lowfile = min(lowfile, s[0])
                highfile = max(highfile, s[0])
                lowrank = min(lowrank, s[1])
                highrank = max(highrank, s[1])
            elif len(s) == 6:
                if s[0] > s[2] or s[3] > s[5]:
                    self._square_ranges_valid = False
                if s[0] != FILE_NAMES[0] or s[2] != FILE_NAMES[-1]:
                    lowfile = min(lowfile, s[0])
                    highfile = max(highfile, s[2])
                if s[3] != RANK_NAMES[0] or s[5] != RANK_NAMES[-1]:
                    lowrank = min(lowrank, s[3])
                    highrank = max(highrank, s[5])
            elif len(s) == 4:
                if s[1] == RANGE_SEPARATOR:
                    if s[0] > s[2]:
                        self._square_ranges_valid = False
                    if (s[0] != FILE_NAMES[0] or
                        s[2] != FILE_NAMES[-1]):
                        lowfile = min(lowfile, s[0])
                        highfile = max(highfile, s[2])
                    lowrank = min(lowrank, s[3])
                    highrank = max(highrank, s[3])
                elif s[2] == RANGE_SEPARATOR:
                    if s[1] > s[3]:
                        self._square_ranges_valid = False
                    lowfile = min(lowfile, s[0])
                    highfile = max(highfile, s[0])
                    if (s[1] != RANK_NAMES[0] or
                        s[3] != RANK_NAMES[-1]):
                        lowrank = min(lowrank, s[1])
                        highrank = max(highrank, s[3])
        if ranklimits:
            ranklimits[0] = min(ranklimits[0], lowrank)
            ranklimits[1] = max(ranklimits[1], highrank)
        if filelimits:
            filelimits[0] = min(filelimits[0], lowfile)
            filelimits[1] = max(filelimits[1], highfile)

    def get_pieces(self):
        """"""
        g = self._groups
        pieces = ''.join((g.compoundpiece_s,
                          g.piece_s,
                          g.compoundpiece,
                          g.piece))
        if not pieces:
            pieces = ANY_WHITE_PIECE_NAME + ANY_BLACK_PIECE_NAME
        return pieces

    def get_squares(self):
        """"""
        g = self._groups
        return ''.join((g.compoundsquare,
                        g.filerankrange,
                        g.filerange,
                        g.rankrange,
                        g.square,
                        g.p_compoundsquare,
                        g.p_filerankrange,
                        g.p_filerange,
                        g.p_rankrange,
                        g.p_square))

    def get_squares_list(self):
        """"""
        return self.get_squares().split(SQUARE_DESIGNATOR_SEPARATOR)

    def is_compound_squares(self):
        """"""
        return self._groups.compoundsquare or self._groups.p_compoundsquare

    def is_compound_pieces(self):
        """"""
        return self._groups.compoundpiece_s or self._groups.compoundpiece


def empty_copy(obj):
    class Empty(obj.__class__):
        def __init__(self):
            pass
    newcopy = Empty()
    newcopy.__class__ = obj.__class__
    return newcopy
