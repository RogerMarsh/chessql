# cql.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) cql keyword.

The pattern for cql parameters treats 'matchcount', 'sort matchcount',
'result 1-0', 'result 0-1', and 'result 1/2-1/2', as different parameters
because of how the 'cql -parse ...' command handles repeated 'matchcount'
and 'result' parameters.

"""
import re

from . import constants
from . import parameters
from . import structure

_RANGE = r"(?:\s+\d+(?:\s+\d+)?)?"
_FILENAME = constants.QUOTED_STRING + r"|\S*"
_SEPARATOR = r"(?:\s+|$)"
_OUTPUT = r"output\s+(?P<output>" + _FILENAME + r")" + _SEPARATOR
_INPUT = r"input\s+(?P<input>" + _FILENAME + r")" + _SEPARATOR
_MATCHCOUNT = r"matchcount(?P<matchcount>" + _RANGE + r")" + _SEPARATOR
_GAMENUMBER = r"gamenumber(?P<gamenumber>" + _RANGE + r")" + _SEPARATOR
_RESULT_WIN = r"result\s+1-0(?P<result_win>" + _SEPARATOR + r")"
_RESULT_LOSS = r"result\s+0-1(?P<result_loss>" + _SEPARATOR + r")"
_RESULT_DRAW = r"result\s+1/2-1/2(?P<result_draw>" + _SEPARATOR + r")"
_SILENT = r"silent(?P<silent>" + _SEPARATOR + r")"
_QUIET = r"quiet(?P<quiet>" + _SEPARATOR + r")"
_SORT_MATCHCOUNT = (
    r"sort\s+matchcount(?P<sort_matchcount>" + _RANGE + r")" + _SEPARATOR
)
_VARIATIONS = r"variations(?P<variations>" + _SEPARATOR + r")"
_MATCHSTRING = (
    r"matchstring\s+(?P<matchstring>"
    + constants.QUOTED_STRING
    + r")"
    + _SEPARATOR
)
_END_OF_STREAM = r"(?P<end_of_stream>)$"
_ANYTHING_ELSE = r"(?P<anything_else>" + r"\S+" + _SEPARATOR + r")"
_CQL_PARAMETERS = r")|(".join(
    (
        r"(" + _OUTPUT,
        _INPUT,
        _MATCHCOUNT,
        _GAMENUMBER,
        _RESULT_WIN,
        _RESULT_LOSS,
        _RESULT_DRAW,
        _SILENT,
        _QUIET,
        _SORT_MATCHCOUNT,
        _VARIATIONS,
        _MATCHSTRING,
        _ANYTHING_ELSE,
        _END_OF_STREAM + r")",
    )
)

_parameters_re = re.compile(_CQL_PARAMETERS)


# Make CQL the implicit '{}' for the query.
# May have a separate class for that when CQL parameters are handled.
# See Infix.place_node_in_tree() too.
class CQL(structure.CompleteBlock):
    """Represent 'cql' parameters and implicit top level {} filter."""

    _is_allowed_first_object_in_container = True

    def place_node_in_tree(self):
        """Delegate then verify container and set cursor to self.

        The container.cursor must be the container and the conainer must
        have only one child.

        """
        container = self.container
        if container.cursor is not container:
            self.raise_nodeerror(
                container.__class__.__name__.join("''"),
                " is not the class of parent instance  of ",
                self.__class__.__name__.join("''"),
            )
        if len(container.cursor.children) != 1:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " instance must be first item in query tree",
            )
        container.cursor = self
        self.parse(self.match_["cql"])

    def parse(self, string):
        """Populate container with parameters extracted from string.

        A basenode.NodeError is raised if the parse fails.

        """
        container = self.container
        for token in _parameters_re.finditer(string):
            classes = {
                key: parameters.class_from_token_name[key]
                # pylint R0801 duplicate code.  Ignored.
                # See tokenmap.FunctionCallEnd.place_node_in_tree().
                # Shortening the 'raise_...' function name enough would
                # remove the pylint report after black reformatting.
                for key, value in token.groupdict().items()
                if value is not None
            }
            container.raise_if_not_single_match_groupdict_entry(token, classes)
            for value in classes.values():
                value(
                    match_=token,
                    container=container,
                ).place_node_in_container_parameters()
