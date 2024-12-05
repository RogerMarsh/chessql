# hhdb.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) definition of HHDB keywords.

The initial definition is for CQL-6.2 with additions for later versions.

The HHDB keyword syntax is different to the CQL keyword syntax and has
conflicts with the CQL syntax related to '(', ')', '<', and '>'.  The
CQL solution is to enclose the problem HHDB keywords in '"'s which moves
the problem to a conflict with CQL quoted strings.
"""
from . import structure


# These 'hhdb' filter commands must be presented as string literals,
# for example 'hhdb "<cook>"', and are handled as special cases of the
# CQL quoted string parsing.
# The 'hhdb' filter with these commands is a Logical filter.
KEYWORD_STRINGS = frozenset(
    (
        "<cook>",
        "<eg>",
        "<main>",  # Only with cql(.. variations ..) or -variations option.
        "<minor_dual>",
        "<or>",  # Only with cql(.. variations ..) or -variations option.
        "(c)",
        "(m)",
        "(s)",
        "(v)",
    )
)

# These 'hhdb' filter commands are also CQL keywords and are handled as
# special cases of the CQL keyword parsing.
# The 'hhdb' filter with these commands, except max, is a Logical filter.
# 'hhdb max' is a Numeric filter.
KEYWORD_KEYWORDS = frozenset(
    (
        "mainline",  # Only with cql(.. variations ..) or -variations option.
        "max",  # May be followed by one of hm prize commendation award.
        "sort",  # Must be followed by one of hm prize commendation award.
        "variation",  # Only with cql(.. variations ..) or -variations option.
    )
)

# These 'hhdb' filter commands are also CQL variable names and are
# handled as special cases of the CQL variable parsing.
# The 'hhdb' filter with these commands is a Logical filter unless marked.
# Derived from 'hhdb <keyword>' and 'v = hhdb <keyword>'.
KEYWORD_VARIABLES = frozenset(
    (
        "correction",
        "modification",
        "corrected_solution",
        "version",
        "AN",
        "anticipation",
        "CR",
        "colors_reversed",
        "MC",
        "too_many_composers",
        "PH",
        "posthumous",
        "TE",
        "theoretical_ending",
        "TT",
        "theme_tourney",
        "theme_tournament",
        "TW",
        "twin",
        "U1",
        "dual_at_move_1",
        "U2",
        "dual_after_move_1",
        "U3",
        "white_fails",
        "U4",
        "white_wins_in_draw",
        "U5",
        "unreachable",
        "unsound",
        "sound",
        "prize",  # Numeric filter.  May be preceded by 'sort' or 'max'.
        "award",  # Numeric filter.  May be preceded by 'sort' or 'max'.
        "hm",  # Numeric filter.  May be preceded by 'sort' or 'max'.
        "commendation",  # Numeric filter.  May be preceded by 'sort' or 'max'.
        "special",  # Numeric filter.
        "stipulation",  # String filter.
        "gbr",  # String filter.  Optional qualifiers noted below.
        "kings",  # preceded by 'gbr' if present (eg 'hhdb gbr kings').
        "material",  # preceded by 'gbr' if present (eg 'hhdb gbr material').
        "pieces",  # preceded by 'gbr' if present (eg 'hhdb gbr pieces').
        "pawns",  # preceded by 'gbr' if present (eg 'hhdb gbr pawns').
        "search",  # String filter.
        "firstcomment",  # String filter.
        "egdiagram",  # Numeric filter.
        "diagram",  # String filter.
        "composer",  # String filter.
    )
)


class HHDB(structure.CQLObject):
    """Represent an HHDB statement within CQL.

    This class is in hhdb, rather than filters, module because it is
    referred to by is_hhdb_token_accepted_by function.
    """

    def complete(self):
        """Return True if HHDB instance has more than one child.

        If the first child is for 'gbr', 'max', or 'sort', the HDDB
        instance is allowed two childen.

        """
        if len(self.children) == 0:
            return False
        if len(self.children) > 2:
            return True
        token_name = self.children[0].match_.group()
        if token_name == "sort":
            return False
        if token_name in frozenset(("max", "gbr")):
            return not isinstance(self.children[-1], HHDBToken)
        return len(self.children) > 1

    def full(self):
        """Return True if HHDB instance has at least one child.

        If the first child is for 'gbr', 'max', or 'sort', the HDDB
        instance is allowed two childen.

        """
        if len(self.children) == 0:
            return False
        if len(self.children) > 1:
            return True
        token_name = self.children[0].match_.group()
        if token_name == "sort":
            return False
        if token_name in frozenset(("max", "gbr")):
            return not isinstance(self.children[-1], HHDBToken)
        return len(self.children) > 0

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


def is_hhdb_token_accepted_by(node):
    """Return True if node or an ancestor accepts HHDB token.

    This function is in hhdb, rather than filters, module because it is
    referred to by HHDBToken class.
    """
    while node is not None:
        if isinstance(node, HHDB):
            return True
        node = node.parent
    return False


class HHDBToken(structure.Complete):
    """Represent a token in an HHDB filter.

    This class is in hhdb, rather than filters, module to keep HHDB
    keyword separate from CQL keyword processing.
    """

    _is_parameter = True

    def place_node_in_tree(self):
        """Delegate then verify parameter name and set cursor to parent."""
        super().place_node_in_tree()
        self.container.cursor = self.parent
        self.raise_if_name_parameter_not_for_filters()

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_hhdb_token_accepted_by(self.parent)
