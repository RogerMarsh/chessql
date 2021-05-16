# constants.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Constants used when parsing Chess Query Language statements.
"""
import pgn_read.core.constants

RANGE_SEPARATOR = r'-'
COMPOUND_DESIGNATOR_START = r'\['
COMPOUND_DESIGNATOR_END = r'\]'
FILE_DESIGNATOR = r'[' + pgn_read.core.constants.FNR + r']'
RANK_DESIGNATOR = r'[' + pgn_read.core.constants.RNR + r']'
SQUARE_DESIGNATOR_SEPARATOR = r','
FILE_RANGE = FILE_DESIGNATOR + RANGE_SEPARATOR + FILE_DESIGNATOR
RANK_RANGE = RANK_DESIGNATOR + RANGE_SEPARATOR + RANK_DESIGNATOR
SIMPLE_SQUARE_DESIGNATOR = r''.join(
    (r'(?:', FILE_RANGE, RANK_RANGE, r')', r'|',
     r'(?:', FILE_RANGE, RANK_DESIGNATOR, r')', r'|',
     r'(?:', FILE_DESIGNATOR, RANK_RANGE, r')', r'|',
     r'(?:', FILE_DESIGNATOR, RANK_DESIGNATOR, r')'
     ))
SQUARE_DESIGNATOR = r''.join(
    (r'(?:', SIMPLE_SQUARE_DESIGNATOR, r')', r'|',
     r'(?:', COMPOUND_DESIGNATOR_START,
     r'(?:', SIMPLE_SQUARE_DESIGNATOR, r')',
     r'(?:', SQUARE_DESIGNATOR_SEPARATOR,
     r'(?:', SIMPLE_SQUARE_DESIGNATOR, r')', r')*',
     COMPOUND_DESIGNATOR_END, r')',
     ))

# Perhaps piece names should be imported from pgn_read package?
# See WKING so named to fit pgn_read.core.constants names.
WHITE_PIECE_NAMES = (
    pgn_read.core.constants.WKING +
    pgn_read.core.constants.WQUEEN +
    pgn_read.core.constants.WROOK +
    pgn_read.core.constants.WBISHOP +
    pgn_read.core.constants.WKNIGHT +
    pgn_read.core.constants.WPAWN)
BLACK_PIECE_NAMES = (
    pgn_read.core.constants.BKING +
    pgn_read.core.constants.BQUEEN +
    pgn_read.core.constants.BROOK +
    pgn_read.core.constants.BBISHOP +
    pgn_read.core.constants.BKNIGHT +
    pgn_read.core.constants.BPAWN)

ANY_WHITE_PIECE_NAME = r'A'
ANY_BLACK_PIECE_NAME = r'a'
EMPTY_SQUARE_NAME = r'.'
EMPTY_SQUARE_NAME_RE = r'\.'
ALL_GAMES_MATCH_PIECE_DESIGNATORS = (
    ANY_WHITE_PIECE_NAME +
    ANY_BLACK_PIECE_NAME +
    pgn_read.core.constants.WKING +
    pgn_read.core.constants.BKING +
    EMPTY_SQUARE_NAME)
ALL_PIECES = WHITE_PIECE_NAMES + BLACK_PIECE_NAMES + EMPTY_SQUARE_NAME

PIECE_NAMES = (WHITE_PIECE_NAMES +
               BLACK_PIECE_NAMES +
               ANY_WHITE_PIECE_NAME +
               ANY_BLACK_PIECE_NAME +
               EMPTY_SQUARE_NAME_RE)

PIECE_TYPE_DESIGNATOR = r''.join(
    (r'(?:[', PIECE_NAMES, r'])', r'|',
     r'(?:', COMPOUND_DESIGNATOR_START,
     r'[', PIECE_NAMES, r']+',
     COMPOUND_DESIGNATOR_END, r')',
     ))
PIECE_DESIGNATOR = r''.join(
    (r'(?:(?:(?:', PIECE_TYPE_DESIGNATOR,
     r')(?:', SQUARE_DESIGNATOR, r'))', r'|',
     r'(?:', SQUARE_DESIGNATOR, r')', r'|',
     r'(?:', PIECE_TYPE_DESIGNATOR, r')',
     r')',
     ))
PIECE_SQUARE_VARIABLE = r'\$[a-zA-Z0-9]+'

PIECE_DESIGNATOR_FILTER = 'piece_designator'

ANY = r'any'
ATTACK = r'attack'
BEGINVARIATION = r'beginvariation'
BETWEEN = r'between'
BTM = r'btm'
CHECK = r'check'
COMMENT = r'comment'
COUNTSQUARES = r'countsquares'
CQL = r'cql'
DARKSQUARES = r'darksquares'
# directions
UP = r'up'
DOWN = r'down'
LEFT = r'left' 
RIGHT = r'right'
NORTHEAST = r'northeast'
NORTHWEST = r'northwest'
SOUTHEAST = r'southeast'
SOUTHWEST = r'southwest'
VERTICAL = r'vertical'
HORIZONTAL = r'horizontal'
DIAGONAL = r'diagonal'
ORTHOGONAL = r'orthogonal'
ANYDIRECTION = r'anydirection'
# directions end
ELO = r'elo'
EVENT = r'event'
FLIP = r'flip'
FLIPDIHEDRAL = r'flipdihedral'
FLIPHORIZONTAL = r'fliphorizontal'
FLIPVERTICAL = r'flipvertical'
FLIPCOLOR = r'flipcolor'
GAMENUMBER = r'gamenumber'
HASCOMMENT = r'hascomment'
INITIAL = r'initial'
INPUT = r'input'
LIGHTSQUARES = r'lightsquares'
MAINLINE = r'mainline'
MATCHCOUNT = r'matchcount'
MATE = r'mate'
MOVE = r'move'
# move modifier
EMPTY = r'empty'
# move parameters
FROM = r'from'
TO = r'to'
PROMOTE = r'promote'
ENPASSANT = r'enpassant'
ENPASSANTSQUARE = r'enpassantsquare'
# move parameters end
MOVENUMBER = r'movenumber'
NEXT = r'next'
NEXT2 = r'next2'
NEXT_STAR = r'next\*'
NOT = r'not'
ON = r'on'
OR = r'or'
ORIGIN = r'origin'
OUTPUT = r'output'
PIECE = r'piece'
# piece parameters?
# piece parameters? end
PLAYER = r'player'
# player parameters
WHITE = r'white'
BLACK = r'black'
# player parameters end
POWER = r'power'
POWERDIFFERENCE = r'powerdifference'
PREVIOUS = r'previous'
PREVIOUS2 = r'previous2'
PREVIOUS_STAR = r'previous\*'
RAY = r'ray'
RELATION = r'relation'
# relation parameters
ANCESTOR = r'ancestor'
DESCENDANT = r'descendant'
ECHOFLIP = r'echoflip'
ECHOFLIPVERTICAL = r'echoflipvertical'
ECHOFLIPHORIZONTAL = r'echofliphorizontal'
ECHOSHIFT = r'echoshift'
ECHOSHIFTHORIZONTAL = r'echoshifthorizontal'
ECHOSHIFTVERTICAL = r'echoshiftvertical'
ECHOROTATE45 = r'echorotate45'
ECHOROTATE90 = r'echorotate90'
LCAMAX = r'lcamax'
LCASOURCE = r'lcasource'
LCASUBSTRING = r'lcasubstring'
LCASUM = r'lcasum'
LCATARGET = r'lcatarget'
MATCH = r'match'
MISMATCH = r'mismatch'
SOURCESQUARES = r'sourcesquares'
TARGETSQUARES = r'targetsquares'
TOMOVE = r'tomove'
# relation parameters end
RESULT = r'result'
ROTATE45 = r'rotate45'
ROTATE90 = r'rotate90'
SHIFT = r'shift'
SHIFTHORIZONTAL = r'shifthorizontal'
SHIFTVERTICAL = r'shiftvertical'
SILENT = r'silent'
SITE = r'site'
SORT = r'sort'
SQUARE = r'square'
# square parameters
ALL = r'all'
IN = r'in'
# square parameters end
STALEMATE = r'stalemate'
TERMINAL = r'terminal'
VARIATION = r'variation'
VARIATIONS = r'variations'
WTM = r'wtm'
YEAR = r'year'

# Mostly keywords are collated according to their use signature.
# Some are put together, separate from others with same signature, because
# they can appear in both the parameter and body parts of a statement.
# Those which appear just in the parameter part are put together despite their
# different use sigantures.
PIECE_SQUARE = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {PIECE, SQUARE,}),
                           reverse=True)])
PIECE_SQUARE_KEYWORDS = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {ALL, IN,}),
                           reverse=True)])
WHITE_BLACK_KEYWORDS = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {WHITE, BLACK,}),
                           reverse=True)])
SITE_EVENT = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {SITE, EVENT,}),
                           reverse=True)])
COUNTSQUARES_POWER = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {COUNTSQUARES, POWER,}),
                           reverse=True)])
NEXT_PREVIOUS = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {NEXT,
                                                  NEXT2,
                                                  PREVIOUS,
                                                  PREVIOUS2,}),
                           reverse=True)])
PLAIN = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {ANY,
                                                  BEGINVARIATION,
                                                  BTM,
                                                  CHECK,
                                                  DARKSQUARES,
                                                  INITIAL,
                                                  LIGHTSQUARES,
                                                  MATE,
                                                  TERMINAL,
                                                  VARIATION,
                                                  STALEMATE,
                                                  WTM,}),
                           reverse=True)])
PLAIN_FILTER = 'plain'
RELATION_PARAMETER = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {MATCH,
                                                  MISMATCH,
                                                  SOURCESQUARES,
                                                  TARGETSQUARES,
                                                  ANCESTOR,
                                                  DESCENDANT,
                                                  LCAMAX,
                                                  LCASOURCE,
                                                  LCASUBSTRING,
                                                  LCASUM,
                                                  LCATARGET,
                                                  ECHOFLIP,
                                                  ECHOFLIPHORIZONTAL,
                                                  ECHOFLIPVERTICAL,
                                                  ECHOROTATE45,
                                                  ECHOROTATE90,
                                                  ECHOSHIFT,
                                                  ECHOSHIFTHORIZONTAL,
                                                  ECHOSHIFTVERTICAL,
                                                  TOMOVE,}),
                           reverse=True)])
MOVE_PARAMETER = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {EMPTY,
                                                  FROM,
                                                  TO,
                                                  PROMOTE,
                                                  ENPASSANT,
                                                  ENPASSANTSQUARE,}),
                           reverse=True)])
CQL_PARAMETER = r'|'.join(
    [f[-1] for f in sorted(((len(v), v) for v in {INPUT,
                                                  OUTPUT,
                                                  GAMENUMBER,
                                                  MATCHCOUNT,
                                                  VARIATIONS,}),
                           reverse=True)])
CYCLIC_FILTER = frozenset((UP,
                           DOWN,
                           LEFT,
                           RIGHT,
                           NORTHEAST,
                           NORTHWEST,
                           SOUTHEAST,
                           SOUTHWEST,
                           ))
DIRECTION_FILTER = frozenset(CYCLIC_FILTER.union((VERTICAL,
                                                  HORIZONTAL,
                                                  DIAGONAL,
                                                  ORTHOGONAL,
                                                  ANYDIRECTION,
                                                  )))
DIHEDRAL_FILTER = frozenset((FLIP,
                             FLIPDIHEDRAL,
                             FLIPHORIZONTAL,
                             FLIPVERTICAL,
                             ROTATE90,
                             ))
SHIFT_FILTER = frozenset((SHIFT,
                          SHIFTHORIZONTAL,
                          SHIFTVERTICAL,
                          ))
TRANSFORM = r'|'.join(
    [f[-1] for f in sorted(((len(v), v)
                            for v in DIRECTION_FILTER.union(
                                DIHEDRAL_FILTER.union(
                                    SHIFT_FILTER.union(
                                        {FLIPCOLOR,
                                         NEXT_STAR,
                                         PREVIOUS_STAR,
                                         ROTATE45,
                                         })))),
                           reverse=True)])

# Used as the type of a node in a statement node tree: not to be confused with
# LEFT_PARENTHESIS and LEFT_BRACE defined for use in regular expressions.
LEFT_PARENTHESIS_FILTER = '('
LEFT_BRACE_FILTER = '{'
RELATION_PARAMETER_NAME = 'relation_parameter'
RIGHT_PARENTHESIS_TYPE = ')'
PGN_FILE_VALUE = 'pgn'

# Any filter not in this frozenset is definitely not a set filter.
# Left parenthesis and left brace are included because they are used as the
# node type in the node tree for a statement, and their status depends on the
# enclosed filters.
SET_FILTER = frozenset(
    DIRECTION_FILTER.union(
        DIHEDRAL_FILTER.union(
            SHIFT_FILTER.union({ATTACK,
                                MOVE,
                                DARKSQUARES,
                                LIGHTSQUARES,
                                PIECE,
                                SQUARE,
                                NOT,
                                ON,
                                OR,
                                BETWEEN,
                                PIECE_DESIGNATOR_FILTER,
                                LEFT_BRACE_FILTER,
                                LEFT_PARENTHESIS_FILTER,
                                }))))
                                              

LEFT_PARENTHESIS = r'\('
RIGHT_PARENTHESIS = r'\)'
LEFT_BRACE = r'\{'
RIGHT_BRACE = r'\}'
NUMBER = r'\d+'
DOUBLE_QUOTED_STRING = r'"[^\\"]*(?:\\.[^\\"]*)*"'
COMMENT_STRING = r';[^\n]*'

# PGN allows '*' as a result but CQL does not.
# CQL states filenames must end in the extension '.pgn', and cql5.1 rejects
# commands starting like:
# 'cql ( input my games.pgn )' but accepts:
# 'cql ( input mygames.pgn )'.  Spaces are not allowed in filenames.
PGN_FILE = r'\.pgn'
ALLOWED_STRINGS = r''.join((r'(?:',
                            pgn_read.core.constants.WHITE_WIN,
                            r')|(?:',
                            pgn_read.core.constants.BLACK_WIN,
                            r')|(?:',
                            pgn_read.core.constants.DRAW,
                            r')|(?:[^\s]+',
                            PGN_FILE,
                            r')',
                            ))

# These are used in some CQL examples but documentation is not clear on rules.
# Looks similar to re module usage.
# '*' also appears as the trailing character of 'next*' and 'previous*'.
ZERO_OR_ONE = r'\?'
ZERO_OR_MORE = r'\*'
ONE_OR_MORE = r'\+'

# REPEAT_OPERATORS must appear in CQL_PATTERN after COMMENT_STRING, NEXT_STAR,
# PREVIOUS_STAR, DOUBLE_QUOTED_STRING, and ALLOWED_STRINGS, to avoid treating
# a '*' embedded in something else incorrectly.
# Best to include PIECE_DESIGNATOR in this list although there is no conflict
# of interest at present.
REPEAT_OPERATORS = r'|'.join((ZERO_OR_ONE, ZERO_OR_MORE, ONE_OR_MORE))

BAD_TOKEN = r'\S+'

EDGING = r'|'.join((r'\s',
                    LEFT_PARENTHESIS,
                    RIGHT_PARENTHESIS,
                    LEFT_BRACE,
                    RIGHT_BRACE))
REPEAT_EDGING = r'|'.join((r'\s',
                           LEFT_PARENTHESIS,
                           RIGHT_PARENTHESIS,
                           LEFT_BRACE,
                           RIGHT_BRACE,
                           REPEAT_OPERATORS,
                           ))
LEADING = EDGING.join((r'(?<=', r')'))
TRAILING = EDGING.join((r'(?=', r'|\Z)'))
#REPEAT_LEADING = REPEAT_EDGING.join((r'(?<=', r')'))
REPEAT_TRAILING = REPEAT_EDGING.join((r'(?=', r'|\Z)'))

CQL_PATTERN = r'|'.join((LEFT_PARENTHESIS.join((r'(', r')')),
                         RIGHT_PARENTHESIS.join((r'(', r')')),
                         LEFT_BRACE.join((r'(', r')')),
                         RIGHT_BRACE.join((r'(', r')')),
                         COMMENT_STRING.join((r'(', r')')),
                         CQL.join((r'(', r')')).join(
                             (r'(?:\A\s*)',
                              LEFT_PARENTHESIS.join((r'(?=\s|', r')')))),
                         PIECE_DESIGNATOR.join(
                             (r'(', r')')).join((LEADING, REPEAT_TRAILING)),
                         CQL_PARAMETER.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         TRANSFORM.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         PLAIN.join(
                             (r'(', r')')).join((LEADING, REPEAT_TRAILING)),
                         RELATION_PARAMETER.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         MOVE_PARAMETER.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         NUMBER.join(
                             (r'(', r')')).join((LEADING, REPEAT_TRAILING)),
                         DOUBLE_QUOTED_STRING.join((r'(', r')')),
                         OR.join((r'(', r')')).join((LEADING, TRAILING)),
                         NOT.join((r'(', r')')).join((LEADING, TRAILING)),
                         ATTACK.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL body or ray keyword.
                         BETWEEN.join((r'(', r')')).join((LEADING, TRAILING)),
                         COUNTSQUARES_POWER.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         ELO.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL parameter or CQL body.
                         COMMENT.join((r'(', r')')).join((LEADING, TRAILING)),
                         HASCOMMENT.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         MAINLINE.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL body or move keyword.
                         MOVE.join((r'(', r')')).join((LEADING, TRAILING)),
                         MOVENUMBER.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         NEXT_PREVIOUS.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL body or move keyword.
                         ON.join((r'(', r')')).join((LEADING, TRAILING)),
                         PLAYER.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL parameter or CQL body.
                         POWERDIFFERENCE.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         RAY.join((r'(', r')')).join((LEADING, TRAILING)),
                         RELATION.join((r'(', r')')).join((LEADING, TRAILING)),
                         RESULT.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL parameter or CQL body.
                         SORT.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL parameter or CQL body.
                         YEAR.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL parameter or CQL body.
                         SILENT.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL parameter or CQL body.
                         SITE_EVENT.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # CQL parameter or CQL body.
                         PIECE_SQUARE.join(
                             (r'(', r')')).join((LEADING, TRAILING)),
                         PIECE_SQUARE_KEYWORDS.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # piece or square keywords.
                         ORIGIN.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # piece or square keywords.
                         PIECE_SQUARE_VARIABLE.join((r'(', r')')).join(
                             (LEADING, REPEAT_TRAILING)),
                         WHITE_BLACK_KEYWORDS.join((r'(', r')')).join(
                             (LEADING, TRAILING)), # player or elo keywords.
                         ALLOWED_STRINGS.join(
                             (r'(', r')')), # result, or *.pgn filename.
                         REPEAT_OPERATORS.join((r'(', r')')),
                         BAD_TOKEN.join((r'(', r')')),
                         ))

# The Python names of group items found by the regular expression pattern in
# CQL_PATTERN: the lower case version of the attribute name except where not
# possible due to Python syntax.
TOKEN_NAMES = ' '.join(('LEFT_PARENTHESIS'.lower(),
                        'RIGHT_PARENTHESIS'.lower(),
                        'LEFT_BRACE'.lower(),
                        'RIGHT_BRACE'.lower(),
                        'COMMENT_STRING'.lower(),
                        'CQL'.lower(),
                        'PIECE_DESIGNATOR'.lower(),
                        'CQL_PARAMETER'.lower(),
                        'TRANSFORM'.lower(),
                        'PLAIN'.lower(),
                        'RELATION_PARAMETER'.lower(),
                        'MOVE_PARAMETER'.lower(),
                        'NUMBER'.lower(),
                        'DOUBLE_QUOTED_STRING'.lower(),
                        'or_', #'OR'.lower(),
                        'not_', #'NOT'.lower(),
                        'ATTACK'.lower(),
                        'BETWEEN'.lower(),
                        'COUNTSQUARES_POWER'.lower(),
                        'ELO'.lower(),
                        'COMMENT'.lower(),
                        'HASCOMMENT'.lower(),
                        'MAINLINE'.lower(),
                        'MOVE'.lower(),
                        'MOVENUMBER'.lower(),
                        'NEXT_PREVIOUS'.lower(),
                        'ON'.lower(),
                        'PLAYER'.lower(),
                        'POWERDIFFERENCE'.lower(),
                        'RAY'.lower(),
                        'RELATION'.lower(),
                        'RESULT'.lower(),
                        'SORT'.lower(),
                        'YEAR'.lower(),
                        'SILENT'.lower(),
                        'SITE_EVENT'.lower(),
                        'PIECE_SQUARE'.lower(),
                        'PIECE_SQUARE_KEYWORDS'.lower(),
                        'ORIGIN'.lower(),
                        'PIECE_SQUARE_VARIABLE'.lower(),
                        'WHITE_BLACK_KEYWORDS'.lower(),
                        'ALLOWED_STRINGS'.lower(),
                        'REPEAT_OPERATORS'.lower(),
                        'BAD_TOKEN'.lower(),
                        ))
(RIGHT_PARENTHESIS_INDEX,
 LEFT_BRACE_INDEX,
 RIGHT_BRACE_INDEX,
 PIECE_DESIGNATOR_INDEX,
 PLAIN_INDEX,
 OR_INDEX,
 NOT_INDEX,
 ON_INDEX,
 ) = [
    e for e, t in enumerate(TOKEN_NAMES.split())
    if t in {'right_parenthesis',
             'left_brace',
             'right_brace',
             'piece_designator',
             'plain',
             'or_',
             'not_',
             'on',
             }]

# CQL_PATTERN and TOKEN_NAMES do not use the concept a 'range' is a sequence of
# 1 or 2 'numbers'.  The presence or absence of a 'range' can determine whether
# a filter is a set filter (some filters are not set filters anyway).  This
# matters to 'transform_filter's at least, and the statement module uses RANGE
# to identify 'number's used as ranges.
RANGE = 'range'

# The CQL statement may be preceded by a statement name.
NAME_DELIMITER = '\n'

# File and rank names for piece designators.
FILE_NAMES = ''.join(tuple(sorted(pgn_read.core.constants.MAPFILE)))
RANK_NAMES = ''.join(tuple(sorted(pgn_read.core.constants.MAPRANK)))

# Derive all lists of squares in rays from pgn_read.core.constants.GAPS, where
# GAPS excludes the squares at each end of the gap but these are included in a
# ray when distinct.  Each gap is represented by a bitarray of square numbers,
# but ray processing needs an ordered list of square identities.
mfosn = {v:k
         for k, v
         in pgn_read.core.constants.MAP_PGN_SQUARE_NAME_TO_FEN_ORDER.items()}
RAYS = {}
for ef, f in enumerate(pgn_read.core.constants.GAPS):
    for et, t in enumerate(f):
        if t == pgn_read.core.constants.ALL_SQUARES or t == 0:
            continue
        fr = RAYS.setdefault(mfosn[ef], {})
        ls = [mfosn[ef]]
        fr[mfosn[et]] = ls
        step = 1 if et > ef else -1
        for s in range(ef + step, et, step):
            if pgn_read.core.constants.SQUARE_BITS[s] & t:
                ls.append(mfosn[s])
        ls.append(mfosn[et])

        # Generate rays of length 2 away from edge of board.
        if len(ls) == 3:
            RAYS[ls[0]][ls[1]] = ls[:2]

# There are no rays of length 3 going right from g4 and so forth, but the rays
# going left from h4 and so forth do exist.
supp = []
for fk in RAYS:
    for tv in RAYS[fk].values():
        if len(tv) == 2:
            if tv[0] not in RAYS[tv[1]]:
                supp.append(tv)
for t, f in supp:
    RAYS[f][t] = [f, t]
del ef, f, et, t, fr, mfosn, ls, s, step, supp

# The diagonals of length 2 do not appear as part of a ray of length 3.
RAYS['a2']['b1'] = ['a2', 'b1']
RAYS['a7']['b8'] = ['a7', 'b8']
RAYS['b1']['a2'] = ['b1', 'a2']
RAYS['b8']['a7'] = ['b8', 'a7']
RAYS['h2']['g1'] = ['h2', 'g1']
RAYS['h7']['g8'] = ['h7', 'g8']
RAYS['g1']['h2'] = ['g1', 'h2']
RAYS['g8']['h7'] = ['g8', 'h7']
