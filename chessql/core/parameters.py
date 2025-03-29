# parameters.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) cql() statement parameter class definitions.

This module defines the classes which represent parameters to the
cql(<squence of parameters>) statement.

Some keywords for these parameters are also keywords for filters or
parameters to these filters.  See the filters module for that usage.

These are values in the cql.class_from_token_name dict.

The 'cql -parse ...' command allows at most one each of 'input', 'output',
'gamenumber', 'matchcount', and 'sort matchcount'.  Also 'matchcount' and
'sort matchcount' are mutually exclusive.

The 'cql -parse ...' command allows any number of 'quiet', 'result ...',
'silent', and 'variations',

This module provides separate classes for 'matchcount', 'sort matchcount',
'result 1-0', 'result 0-1', and 'result 1/2-1/2'.

The CQL documentation gives no reason for allowing multiple occurrences
of 'results 1-0' for example.  This module ignores the repeats rather
than reject them like with 'input' and friends.
"""


class CQLParameterError(Exception):
    """Exception raised for problems in CQLParameter and subclasses."""


class CQLParameter:
    """Base class of classes which represent .cql._CQL_PARAMETERS matches."""

    # Default.  Subclasses may bind instance attribute to suitable value.
    _parameter_value = None

    def __init__(self, match_=None, container=None):
        """Initialise cql parameter attributes."""
        self.match_ = match_
        self._container = container

    @property
    def container(self):
        """Return self._container."""
        return self._container

    @property
    def parameter_value(self):
        """Return self._parameter_value."""
        return self._parameter_value

    def place_node_in_container_parameters(self):
        """Add self to container's cql parameters."""
        self._set_parameter()

    def _set_parameter(self):
        """Add to container.parameters if instance of self's class absent."""
        for item in self._container.parameters:
            if isinstance(self, item.__class__):
                return
        self._container.parameters.add(self)

    def _raise_if_match_groupdict_item_is_none(self, item):
        """Raise NodeError if cursor is not expected class."""
        if self.match_[item] is not None:
            return
        raise CQLParameterError(
            "".join(
                (
                    "'",
                    self.__class__.__name__,
                    "' expects item '",
                    item,
                    "' to be part of match but it is a '",
                    None.__class__.__name__,
                    "' in match's groupdict",
                )
            )
        )


class _NoDuplicateParameter(CQLParameter):
    """Base class of parameter classes where duplicates are not allowed."""

    def _set_parameter(self):
        """Raise Parameter error if duplicated then delegate."""
        for item in self._container.parameters:
            if isinstance(self, item.__class__):
                raise CQLParameterError(
                    self.__class__.__name__
                    + ": instance of this class is already a parameter"
                )
        super()._set_parameter()


class AnythingElse(CQLParameter):
    """Represent '<unexpected> cql(output <unexpected>) keyword.

    The 'unexpected' construct also occurs in filters module.
    """

    def place_node_in_container_parameters(self):
        """Raise CQLParameterError exception."""
        raise CQLParameterError(
            self.__class__.__name__
            + ": '"
            + self.match_.group().split()[0]
            + "' is not a CQL parameter"
        )


class GameNumber(_NoDuplicateParameter):
    """Represent 'gamenumber' cql(gamenumber <range>) keyword.

    The 'gamenumber' keyword also represents a filter.
    """

    def __init__(self, match_=None, container=None):
        """Initialise gamenumber cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("gamenumber")
        self._parameter_value = self.match_["gamenumber"].split()


class EndOfStream(CQLParameter):
    """Represent '<end of stream> cql(<optional><end of stream>) keyword.

    The 'end of stream>' construct also occurs in filters module.
    """

    def place_node_in_container_parameters(self):
        """Do nothing."""


class Input(_NoDuplicateParameter):
    """Represent 'input' cql(input <file name>) keyword."""

    def __init__(self, match_=None, container=None):
        """Initialise input cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("input")
        self._parameter_value = self.match_["input"]


class MatchCount(_NoDuplicateParameter):
    """Represent 'matchcount' cql(matchcount <range>) keyword.

    The 'matchcount' patameter cannot be given if the 'sort matchcount'
    parameter is already given.
    """

    def __init__(self, match_=None, container=None):
        """Initialise matchcount cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("matchcount")
        self._parameter_value = self.match_["matchcount"].split()

    def _set_parameter(self):
        """Raise Parameter error if duplicated then delegate."""
        for item in self._container.parameters:
            if isinstance(SortMatchCount, item.__class__):
                raise CQLParameterError(
                    self.__class__.__name__
                    + ": instance of this class is already a parameter"
                )
        super()._set_parameter()


class MatchString(CQLParameter):
    """Represent 'matchstring' cql(matchstring <quoted string>) keyword."""

    def __init__(self, match_=None, container=None):
        """Initialise matchstring cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("matchstring")
        self._parameter_value = self.match_["matchstring"]


class Output(_NoDuplicateParameter):
    """Represent 'output' cql(output <file name>) keyword."""

    def __init__(self, match_=None, container=None):
        """Initialise output cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("output")
        self._parameter_value = self.match_["output"]


class ResultDraw(CQLParameter):
    """Represent 'result 1/2-1/2' cql(result <result string>) keyword.

    'result' is also the keyword for a filter taking '1-0', '1/2-1/2' or
    '0-1' as it's argument.
    """

    def __init__(self, match_=None, container=None):
        """Initialise result draw cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("result_draw")


class ResultLoss(CQLParameter):
    """Represent 'result 0-1' cql(result <result string>) keyword.

    'result' is also the keyword for a filter taking '1-0', '1/2-1/2' or
    '0-1' as it's argument.
    """

    def __init__(self, match_=None, container=None):
        """Initialise result loss cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("result_loss")


class ResultWin(CQLParameter):
    """Represent 'result 1-0' cql(result <result string>) keyword.

    'result' is also the keyword for a filter taking '1-0', '1/2-1/2' or
    '0-1' as it's argument.
    """

    def __init__(self, match_=None, container=None):
        """Initialise result win cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("result_win")


class Quiet(CQLParameter):
    """Represent 'quiet' cql(quiet) keyword.

    The 'quiet' keyword also represents a parameter to some filters.
    """


class Silent(CQLParameter):
    """Represent 'silent' cql(silent) keyword."""


class SortMatchCount(_NoDuplicateParameter):
    """Represent 'sort matchcount' cql(sort matchcount <range>).

    The 'sort matchcount' patameter cannot be given if the 'matchcount'
    parameter is already given.
    """

    def __init__(self, match_=None, container=None):
        """Initialise 'sort matchcount' cql parameter attributes."""
        super().__init__(match_=match_, container=container)
        self._raise_if_match_groupdict_item_is_none("sort_matchcount")
        self._parameter_value = self.match_["sort_matchcount"].split()

    def _set_parameter(self):
        """Raise Parameter error if duplicated then delegate."""
        for item in self._container.parameters:
            if isinstance(MatchCount, item.__class__):
                raise CQLParameterError(
                    self.__class__.__name__
                    + ": instance of this class is already a parameter"
                )
        super()._set_parameter()


class Variations(CQLParameter):
    """Represent 'variations' cql(output <file name>) keyword."""


class_from_token_name = {
    "anything_else": AnythingElse,
    "end_of_stream": EndOfStream,
    "gamenumber": GameNumber,
    "input": Input,
    "matchcount": MatchCount,
    "matchstring": MatchString,
    "output": Output,
    "quiet": Quiet,
    "result_win": ResultWin,
    "result_loss": ResultLoss,
    "result_draw": ResultDraw,
    "silent": Silent,
    "sort_matchcount": SortMatchCount,
    "variations": Variations,
}
