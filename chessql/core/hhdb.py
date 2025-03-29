# hhdb.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) definition of HHDB keywords.

The initial definition is for CQL-6.2 with additions for later versions.

The HHDB keyword syntax is different to the CQL keyword syntax and has
conflicts with the CQL syntax related to '(', ')', '<', and '>'.  The
CQL solution is to enclose the problem HHDB keywords in '"'s which moves
the problem to a conflict with CQL quoted strings.

The HHDB keywords are also valid CQL keywords or variable names.  The
conflict is resolved by catching all HHDB keywords in the pattern for
the 'hhdb' filter.

"""
from . import structure
from . import cqltypes

# Position Attributes. (Logical filters.)
COOK = r'"<cook>"'
EG = r'"<eg>"'
MAIN = r'"<main>"'
MINOR_DUAL = r'"<minor_dual>"'
OR = r'"<or>"'
MAINLINE = r"mainline"
VARIATION = r"variation"

# Study Attributes. (Logical filters.)
COOKED = r"cooked"
DUAL = r"dual"
SOUND = r"sound"
UNSOUND = r"unsound"
CORRECTION = r'"\(c\)"|correction'
MODIFICATION = r'"\(m\)"|modification'
CORRECTED_SOLUTION = r'"\(s\)"|corrected_solution'
VERSION = r'"\(v\)"|version'
ANTICIPATION = r"AN|anticipation"
COLORS_REVERSED = r"CR|colors_reversed"
TOO_MANY_COMPOSERS = r"MC|too_many_composers"
POSTHUMOUS = r"PH|posthumous"
THEORETICAL_ENDING = r"TE|theoretical_ending"
THEME_TOURNEY = r"TT|theme_tourney|theme_tournament"
TWIN = r"TW|twin"
DUAL_AT_MOVE_1 = r"U1|dual_at_move_1"
DUAL_AFTER_MOVE_1 = r"U2|dual_after_move_1"
WHITE_FAILS = r"U3|white_fails"
WHITE_WINS_IN_DRAW = r"U4|white_wins_in_draw"
UNREACHABLE = r"U5|unreachable"

_LOGICAL_FILTERS = r"|".join(
    (
        COOK,
        EG,
        MAIN,
        MINOR_DUAL,
        OR,
        MAINLINE,
        VARIATION,
        COOKED,
        DUAL,
        SOUND,
        UNSOUND,
        CORRECTION,
        MODIFICATION,
        CORRECTED_SOLUTION,
        VERSION,
        ANTICIPATION,
        COLORS_REVERSED,
        TOO_MANY_COMPOSERS,
        POSTHUMOUS,
        THEORETICAL_ENDING,
        THEME_TOURNEY,
        TWIN,
        DUAL_AT_MOVE_1,
        DUAL_AFTER_MOVE_1,
        WHITE_FAILS,
        WHITE_WINS_IN_DRAW,
        UNREACHABLE,
    )
)
# Numeric Attributes. (Numeric filters.  Implicit search parameter.)
EGDIAGRAM = r"egdiagram"

# String Attributes. (String filters.  Implicit search parameter.)
COMPOSER = r"composer"
DIAGRAM = r"diagram"
FIRSTCOMMENT = r"firstcomment"
GBR = r"gbr"
GBR_KINGS = r"gbr\s+kings"
GBR_MATERIAL = r"gbr\s+material"
GBR_PAWNS = r"gbr\s+pawns"
GBR_PIECES = r"gbr\s+pieces"
SEARCH = r"search"
STIPULATION = r"stipulation"

_STRING_FILTERS = r"|".join(
    (
        COMPOSER,
        DIAGRAM,
        FIRSTCOMMENT,
        GBR_KINGS,
        GBR_MATERIAL,
        GBR_PAWNS,
        GBR_PIECES,
        GBR,
        SEARCH,
        STIPULATION,
    )
)

# Award Attributes. (Numeric filters.)
# The commented statements for SORT, _SORT, and SPECIAL, were derived from
# the CQLi-1.0.4 manual because clear rules are stated on what combinations
# are allowed.
# CQL does not accept 'sortable' or 'nonspecial'.  It seems 'sortable'
# may exist to allow CQLi to support 'hddb sort' where 'sort' could also
# be the CQL keyword 'sort'.  Not sure on 'nonspecial'.
# SORT = r"sortable|max|sort"
# _SORT = r"sortable|max"
# SPECIAL = r"special|nonspecial"
MAX = r"max"
AWARD = r"award"
COMMENDATION = r"commendation"
HM = r"hm"
PRIZE = r"prize"
SORT = r"sort"
SPECIAL = r"special"
_SORT = r"|".join((MAX, SORT))
_AWARD = r"|".join((AWARD, COMMENDATION, HM, PRIZE))
_AWARD1 = r"(?:(?:" + r")\s+(?:".join((_SORT, _AWARD, SPECIAL)) + r"))"
_AWARD2 = r"(?:(?:" + r")\s+(?:".join((_SORT, SPECIAL, _AWARD)) + r"))"
_AWARD3 = r"(?:(?:" + r")\s+(?:".join((SPECIAL, _AWARD, MAX)) + r"))"
_AWARD4 = r"(?:(?:" + r")\s+(?:".join((SPECIAL, _SORT, _AWARD)) + r"))"
_AWARD5 = r"(?:(?:" + r")\s+(?:".join((_AWARD, SPECIAL, MAX)) + r"))"
_AWARD6 = r"(?:(?:" + r")\s+(?:".join((_AWARD, _SORT, SPECIAL)) + r"))"
_AWARD7 = r"(?:(?:" + r")\s+(?:".join((_SORT, _AWARD)) + r"))"
_AWARD8 = r"(?:(?:" + r")\s+(?:".join((SPECIAL, _AWARD)) + r"))"
_AWARD9 = r"(?:(?:" + r")\s+(?:".join((_AWARD, MAX)) + r"))"
_AWARD10 = r"(?:(?:" + r")\s+(?:".join((_AWARD, SPECIAL)) + r"))"
_AWARD11 = r"(?:(?:" + r")\s+(?:".join((_SORT, SPECIAL)) + r"))"
_AWARD12 = r"(?:(?:" + r")\s+(?:".join((SPECIAL, MAX)) + r"))"
_AWARD13 = r"(?:" + _AWARD + r")"
_AWARD14 = r"(?:" + SPECIAL + r")"
_AWARD15 = r"(?:" + MAX + r")"

_AWARDS = r"".join(
    (
        r"(?:",
        r"|".join(
            (
                _AWARD1,
                _AWARD2,
                _AWARD3,
                _AWARD4,
                _AWARD5,
                _AWARD6,
                _AWARD7,
                _AWARD8,
                _AWARD9,
                _AWARD10,
                _AWARD11,
                _AWARD12,
                _AWARD13,
                _AWARD14,
                _AWARD15,
            ),
        ),
        r")",
    )
)

# HHDB filter.
HHDB = r"".join(
    (
        r"(?P<hhdb>)hhdb\s+",
        r"(?:",
        r"|".join((_LOGICAL_FILTERS, EGDIAGRAM, _STRING_FILTERS, _AWARDS)),
        r")",
        r"(?![\w$])",
    )
)

del _SORT, _AWARDS, _AWARD, _LOGICAL_FILTERS, _STRING_FILTERS
del _AWARD1, _AWARD2, _AWARD3, _AWARD4, _AWARD5, _AWARD6, _AWARD7, _AWARD8
del _AWARD9, _AWARD10, _AWARD11, _AWARD12, _AWARD13, _AWARD14, _AWARD15

_HHDB_KEYWORDS = frozenset(
    (
        COOK,
        EG,
        MAIN,
        MINOR_DUAL,
        OR,
        MAINLINE,
        VARIATION,
        COOKED,
        DUAL,
        SOUND,
        UNSOUND,
        CORRECTION,
        MODIFICATION,
        CORRECTED_SOLUTION,
        VERSION,
        ANTICIPATION,
        COLORS_REVERSED,
        TOO_MANY_COMPOSERS,
        POSTHUMOUS,
        THEORETICAL_ENDING,
        THEME_TOURNEY,
        TWIN,
        DUAL_AT_MOVE_1,
        DUAL_AFTER_MOVE_1,
        WHITE_FAILS,
        WHITE_WINS_IN_DRAW,
        UNREACHABLE,
        EGDIAGRAM,
        COMPOSER,
        DIAGRAM,
        FIRSTCOMMENT,
        GBR,
        GBR_KINGS,
        GBR_MATERIAL,
        GBR_PAWNS,
        GBR_PIECES,
        SEARCH,
        STIPULATION,
        MAX,
        AWARD,
        COMMENDATION,
        HM,
        PRIZE,
        SORT,
        SPECIAL,
    )
)
_AWARD_KEYWORDS = frozenset(
    (MAX, AWARD, COMMENDATION, HM, PRIZE, SORT, SPECIAL)
)


class HHdbCook(structure.CQLObject):
    """Represent '"<cook>"' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbEG(structure.CQLObject):
    """Represent '"<eg>"' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbMain(structure.CQLObject):
    """Represent '"<main>"' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbMinorDual(structure.CQLObject):
    """Represent '"<minor_dual>"' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbOr(structure.CQLObject):
    """Represent '"<or>"' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbMainline(structure.CQLObject):
    """Represent 'mainline' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbVariation(structure.CQLObject):
    """Represent 'variation' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbCooked(structure.CQLObject):
    """Represent 'cooked' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbDual(structure.CQLObject):
    """Represent 'dual' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbSound(structure.CQLObject):
    """Represent 'sound' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbUnsound(structure.CQLObject):
    """Represent 'unsound' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbCorrection(structure.CQLObject):
    """Represent 'correction' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbModification(structure.CQLObject):
    """Represent 'modification' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbCorrectedSolution(structure.CQLObject):
    """Represent 'corrected_solution' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbVersion(structure.CQLObject):
    """Represent 'version' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbAnticipation(structure.CQLObject):
    """Represent 'anticipation' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbColorsReversed(structure.CQLObject):
    """Represent 'colors_reversed' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbTooManyComposers(structure.CQLObject):
    """Represent 'too_many_composers' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbPosthumous(structure.CQLObject):
    """Represent 'posthumous' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbTheoreticalEnding(structure.CQLObject):
    """Represent 'theoretical_ending' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbThemeTourney(structure.CQLObject):
    """Represent 'theme_tourney' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbTwin(structure.CQLObject):
    """Represent 'twin' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbDualAtMove1(structure.CQLObject):
    """Represent 'dual_at_move_1' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbDualAfterMove1(structure.CQLObject):
    """Represent 'dual_after_move_1' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbWhiteFails(structure.CQLObject):
    """Represent 'white_fails' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbWhiteWinsInDraw(structure.CQLObject):
    """Represent 'white_wins_in_draw' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbUnreachable(structure.CQLObject):
    """Represent 'unreachable' Logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class HHdbEGDiagram(structure.ImplicitSearchFilter):
    """Represent 'egdiagram' Numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class HHdbComposer(structure.ImplicitSearchFilter):
    """Represent 'composer' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbDiagram(structure.ImplicitSearchFilter):
    """Represent 'diagram' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbFirstcomment(structure.ImplicitSearchFilter):
    """Represent 'firstcomment' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbGBR(structure.ImplicitSearchFilter):
    """Represent 'gbr' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbGBRKings(structure.ImplicitSearchFilter):
    """Represent 'gbr kings' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbGBRMaterial(structure.ImplicitSearchFilter):
    """Represent 'gbr material' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbGBRPawns(structure.ImplicitSearchFilter):
    """Represent 'gbr pawns' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbGBRPieces(structure.ImplicitSearchFilter):
    """Represent 'gbr pieces' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbSearch(structure.ImplicitSearchFilter):
    """Represent 'search' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbStipulation(structure.ImplicitSearchFilter):
    """Represent 'stipulation' String filter."""

    _filter_type = cqltypes.FilterType.STRING


class HHdbAward(structure.ImplicitSearchFilter):
    """Represent 'award' Numeric filter.

    An 'award' filter is indicated by allowed combinations of the 'max',
    'sort', 'award', 'commendation', 'hm', 'prize', and 'special' HHDB
    keywords.

    See 'https://gadycosteff.com/cql/hhdb.html' for the CQL definitions
    for HHDB.

    See the 'HHdbVI Database Interface' part of 'Other Features' in
    'manual.pdf' in any of the downloads from 'cql64.com' for a tabular
    presentation of the definitions.  Note the available options are not
    identical to those in CQL for awards.
    """

    _filter_type = cqltypes.FilterType.NUMERIC

    def is_max(self):
        """Return True if 'max' is given with the 'hhdb' keyword."""
        return MAX in self.match_.group().split()

    def is_award(self):
        """Return True if 'award' is given with the 'hhdb' keyword."""
        return AWARD in self.match_.group().split()

    def is_commendation(self):
        """Return True if 'commendation' is given with the 'hhdb' keyword."""
        return COMMENDATION in self.match_.group().split()

    def is_hm(self):
        """Return True if 'hm' is given with the 'hhdb' keyword."""
        return HM in self.match_.group().split()

    def is_prize(self):
        """Return True if 'prize' is given with the 'hhdb' keyword."""
        return PRIZE in self.match_.group().split()

    def is_sort(self):
        """Return True if 'sort' is given with the 'hhdb' keyword."""
        return SORT in self.match_.group().split()

    def is_special(self):
        """Return True if 'special' is given with the 'hhdb' keyword."""
        return SPECIAL in self.match_.group().split()


_keyword_to_class = {
    COOK: HHdbCook,
    EG: HHdbEG,
    MAIN: HHdbMain,
    MINOR_DUAL: HHdbMinorDual,
    OR: HHdbOr,
    MAINLINE: HHdbMainline,
    VARIATION: HHdbVariation,
    COOKED: HHdbCooked,
    DUAL: HHdbDual,
    SOUND: HHdbSound,
    UNSOUND: HHdbUnsound,
    CORRECTION: HHdbCorrection,
    MODIFICATION: HHdbModification,
    CORRECTED_SOLUTION: HHdbCorrectedSolution,
    VERSION: HHdbVersion,
    ANTICIPATION: HHdbAnticipation,
    COLORS_REVERSED: HHdbColorsReversed,
    TOO_MANY_COMPOSERS: HHdbTooManyComposers,
    POSTHUMOUS: HHdbPosthumous,
    THEORETICAL_ENDING: HHdbTheoreticalEnding,
    THEME_TOURNEY: HHdbThemeTourney,
    TWIN: HHdbTwin,
    DUAL_AT_MOVE_1: HHdbDualAtMove1,
    DUAL_AFTER_MOVE_1: HHdbDualAfterMove1,
    WHITE_FAILS: HHdbWhiteFails,
    WHITE_WINS_IN_DRAW: HHdbWhiteWinsInDraw,
    UNREACHABLE: HHdbUnreachable,
    EGDIAGRAM: HHdbEGDiagram,
    COMPOSER: HHdbComposer,
    DIAGRAM: HHdbDiagram,
    FIRSTCOMMENT: HHdbFirstcomment,
    GBR: HHdbGBR,
    GBR_KINGS: HHdbGBRKings,
    GBR_MATERIAL: HHdbGBRMaterial,
    GBR_PAWNS: HHdbGBRPawns,
    GBR_PIECES: HHdbGBRPieces,
    SEARCH: HHdbSearch,
    STIPULATION: HHdbStipulation,
    MAX: HHdbAward,
    AWARD: HHdbAward,
    COMMENDATION: HHdbAward,
    HM: HHdbAward,
    PRIZE: HHdbAward,
    SORT: HHdbAward,
    SPECIAL: HHdbAward,
}


def hhdb_not_implemented(match_=None, container=None):
    """Return instance of class representing the 'hhdb' filter."""
    keywords = match_.group().split()
    if len(keywords) < 2:
        raise container.raise_nodeerror(
            container.cursor.__class__.__name__.join("''"),
            " an HHDB filter needs at least one keyword after 'hhdb'",
        )
    if keywords[0] != "hhdb":
        raise container.raise_nodeerror(
            container.cursor.__class__.__name__.join("''"),
            " the first keyword must be 'hhdb' in an HHDB filter",
        )
    hhdb_keywords = set(keywords[1:]) & _HHDB_KEYWORDS
    if (
        len(hhdb_keywords) > 1
        and hhdb_keywords & _AWARD_KEYWORDS != hhdb_keywords
    ):
        raise container.raise_nodeerror(
            container.cursor.__class__.__name__.join("''"),
            " only 'hhdb' award filters can have more than one keyword",
        )
    hhdb_class = _keyword_to_class.get(keywords[1])
    if hhdb_class is None:
        raise container.raise_nodeerror(
            container.cursor.__class__.__name__.join("''"),
            " the 'hhdb' ",
            keywords[1].join("''"),
            " filter is not implemented yet",
        )
    return hhdb_class(match_=match_, container=container)
