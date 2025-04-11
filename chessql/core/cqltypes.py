# cqltypes.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Classes defining properties of named Chess Query Language objects.

The names of user defined functions, variables, and dictionaries need to
be managed: names must be unique and each ones properties persist through
a query unless explicitly removed by the 'unbind' filter.
"""
import enum


class TokenType(enum.Flag):
    """Define the operand, unary operator, and binary operator token types.

    This guides conversion of CQL statement from infix to postfix notation.

    Tokens with TokenType.OPERAND will not have a Precedence, their
    _precedence attribute will be None.
    """

    OPERAND = enum.auto()
    UNARY = enum.auto()  # Left and right versions? '{+}' and '-' for example.
    BINARY = enum.auto()


class FilterType(enum.Flag):
    """Define the set, logical, numeric, string, and position, filter types.

    The ANY filter type exists to assist deciding the actual filter type
    when several possiblities exist.  for example '{' before any component
    filters are defined.

    'boolean' may be a better name for 'logical' filter, but CQL naming is
    followed rather than CQLi naming.
    """

    SET = enum.auto()
    LOGICAL = enum.auto()
    NUMERIC = enum.auto()
    STRING = enum.auto()
    POSITION = enum.auto()
    ANY = SET | LOGICAL | NUMERIC | STRING | POSITION


class DefinitionType(enum.Flag):
    """Define the dictionary, function, and variable, definition types.

    The ANY definition type exists to assist banning function redefinition.
    """

    DICTIONARY = enum.auto()
    FUNCTION = enum.auto()
    VARIABLE = enum.auto()
    ANY = DICTIONARY | FUNCTION | VARIABLE


class VariableType(enum.Flag):
    """Define the numeric, set, piece, string, and position, variable types.

    A variable is given the ANY type before the actual type is determined.
    """

    NUMERIC = enum.auto()
    SET = enum.auto()
    PIECE = enum.auto()
    STRING = enum.auto()
    POSITION = enum.auto()
    ANY = NUMERIC | SET | PIECE | STRING | POSITION


class PersistenceType(enum.Flag):
    """Define the persistence types for variables and dictionaries.

    Dictionaries and variables are either persistent or local.  A persistent
    item retains it's value between games.  A local item is initialized for
    each game.

    A PERSISTENT item may be QUIET too, but QUIET is not allowed otherwise.
    """

    ATOMIC = enum.auto()
    LOCAL = enum.auto()
    PERSISTENT = enum.auto()
    QUIET = enum.auto()
    ANY = ATOMIC | LOCAL | PERSISTENT | QUIET


class DefinitionError(Exception):
    """Exception raised for problems in definition module."""


def _definition(name, container, definition_):
    """Set user defined object name and add name, if new, to container.

    If the name is already registered as an object of type definition_
    the duplication is allowed without changing the registration,
    otherwise a DefinitionError exception is raised.

    """
    if name in container.definitions:
        if not isinstance(container.definitions[name], definition_):
            raise DefinitionError(
                "".join(
                    (
                        name.join("''"),
                        " is already a ",
                        container.definitions[name].__class__.__name__.join(
                            "''"
                        ),
                        " name so cannot be a ",
                        definition_.__class__.__name__.join("''"),
                        " name",
                    )
                )
            )
        return
    container.definitions[name] = definition_(name)


class _Definition:
    """Set name of user defined object."""

    _definition_type = DefinitionType.ANY

    def __init__(self, name):
        """Set self._name to name."""
        self._name = name

    @property
    def name(self):
        """Return self._name."""
        return self._name

    @property
    def definition_type(self):
        """Return self._definition_type."""
        return self._definition_type

    def _raise_definition_error(self, *message_str):
        """Raise a DefinitionError with concatenated *message_str."""
        raise DefinitionError("".join(message_str))

    def _raise_value_type_error(self, value, type_):
        """Raise exception with value is not type_ description."""
        self._raise_definition_error(
            value.__class__.__name__.join("''"),
            " instance is not a ",
            type_.join("''"),
            " type",
        )


class Function(_Definition):
    """Set name of function."""

    _definition_type = DefinitionType.FUNCTION

    def __init__(self, name):
        """Delegate then set self._parameters to None."""
        super().__init__(name)
        self._parameters = None
        self._body = []

    @property
    def parameters(self):
        """Return self._parameters."""
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        """Bind self._parameters to value."""
        if not isinstance(value, (tuple, list)):
            self._raise_value_type_error(value, "tuple or list")
        self._parameters = value

    @property
    def body(self):
        """Return self._body."""
        return self._body


def function(name, container):
    """Define name in container as a Function.

    Details for user defined items, variables and functions, are not
    updated when encountered during collection of functions bodies.

    """
    if container.function_body_cursor is None:
        _definition(name, container, Function)


class _Variable(_Definition):
    """Set filter and persistence types for Variable and Dictionary."""

    def __init__(self, name):
        """Delegate then set filter and persistence types to defaults."""
        super().__init__(name)
        self._filter_type = FilterType.ANY  # Should exclude LOGICAL.
        self._persistence_type = PersistenceType.ANY

    @property
    def filter_type(self):
        """Return self._filter_type."""
        return self._filter_type

    @filter_type.setter
    def filter_type(self, value):
        """Bind self._filter_type to value if current value is ANY."""
        if value not in FilterType:
            self._raise_value_type_error(value, "filter")
        if value is not FilterType.ANY:
            if self._filter_type is not FilterType.ANY:
                if self._filter_type is not value:
                    self._raise_definition_error(
                        "'",
                        self._name,
                        "' is already a '",
                        self._filter_type.name.lower(),
                        "' filter so cannot be set as a '",
                        value.name.lower(),
                        "' filter",
                    )
        self._filter_type = value

    @property
    def persistence_type(self):
        """Return self._persistence_type."""
        return self._persistence_type

    @persistence_type.setter
    def persistence_type(self, value):
        """Bind self._persistence_type to value if current value is ANY."""
        if value & PersistenceType.ANY != value:
            self._raise_value_type_error(value, "allowed persistence")
        if value is not PersistenceType.ANY:
            if self._persistence_type is not PersistenceType.ANY:
                if self._persistence_type is not value:
                    self._raise_definition_error(
                        "'",
                        self._name,
                        "' is already '",
                        self._persistence_type.name.lower(),
                        "' so cannot be set as '",
                        value.name.lower(),
                        "'",
                    )
        self._persistence_type = value


class Variable(_Variable):
    """Set filter, variable, and persistence types, and anme, of variable."""

    _definition_type = DefinitionType.VARIABLE

    # Need pairs of _variable_type and _filter_type to cope with parsing
    # function bodies and calling functions.  In 'function F(){v=1} up v k'
    # the variable 'v' cannot be used as a range parameter to 'up' because
    # the function F has not been called.
    def __init__(self, name):
        """Delegate then set self._variable_type to VariableType.ANY."""
        super().__init__(name)
        self._variable_type = VariableType.ANY

    @property
    def variable_type(self):
        """Return self._variable_type."""
        return self._variable_type

    # This is not correct yet because a variable's type depends on when the
    # first assignment is made.
    # 'function fun(){v=1} up v k' is not allowed, failing at 'up v',
    # because v's type is not known until 'fun' is called but
    # 'function fun(){v=1} fun() up v k' is allowed.
    # 'function fun(){v=1} v=k fun() up v k' is not allowed, failing at
    # 'fun()' in 'v=k fun()', because v's type is SET when 'v=1' is done
    # in the 'fun()' call.
    @variable_type.setter
    def variable_type(self, value):
        """Bind self._variable_type to value if current value is ANY."""
        if value not in VariableType:
            self._raise_value_type_error(value, "variable")
        if value is not VariableType.ANY:
            if self._variable_type is not VariableType.ANY:
                if self._variable_type is not value:
                    self._raise_definition_error(
                        self._name.join("''"),
                        " is already a ",
                        self._variable_type.name.lower().join("''"),
                        " variable so cannot be set as a ",
                        value.name.lower().join("''"),
                        " variable",
                    )
        self._variable_type = value

    def is_variable_type(self, value):
        """Return True if value is self._variable_type or VariableType.ANY.

        ANY is allowed because a variable's type is not known when first
        mentioned: the first mention will be 'v=1' or similar and the
        actual variable type is decided when the RHS of assignment is
        processed.

        """
        if value not in VariableType:
            self._raise_value_type_error(value, "variable")
        return value is self._variable_type or value in VariableType.ANY


def variable(name, container):
    """Define name in container as a Variable.

    Details for user defined items, variables and functions, are not
    updated when encountered during collection of functions bodies.

    """
    if container.function_body_cursor is None:
        _definition(name, container, Variable)


class Dictionary(_Variable):
    """Set filter, key, and persistence types, and anme, of dictionary."""

    _definition_type = DefinitionType.DICTIONARY

    def __init__(self, name):
        """Delegate then set self._key_filter_type to FilterType.ANY."""
        super().__init__(name)
        self._key_filter_type = FilterType.ANY  # Should exclude LOGICAL.

    @property
    def key_filter_type(self):
        """Return self._key_filter_type."""
        return self._key_filter_type

    @key_filter_type.setter
    def key_filter_type(self, value):
        """Bind self._key_filter_type to value if current value is ANY."""
        if value not in FilterType:
            self._raise_value_type_error(value, "filter")
        if value is not FilterType.ANY:
            if self._key_filter_type is not FilterType.ANY:
                if self._key_filter_type is not value:
                    self._raise_definition_error(
                        self._name.join("''"),
                        " key is already a ",
                        self._key_filter_type.name.lower().join("''"),
                        " filter so cannot be a ",
                        value.name.lower().join("''"),
                        " filter",
                    )
        self._key_filter_type = value


def dictionary(name, container):
    """Define name in container as a Dictionary.

    Details for user defined items, variables and functions, are not
    updated when encountered during collection of functions bodies.

    """
    if container.function_body_cursor is None:
        _definition(name, container, Dictionary)


class Precedence(enum.Enum):
    """Define the precedences available to operators."""

    P10 = 10
    P20 = 20
    P30 = 30
    P40 = 40
    P50 = 50
    P60 = 60
    P65 = 65
    P70 = 70
    P80 = 80
    P90 = 90
    P100 = 100
    P110 = 110
    P120 = 120
    P130 = 130
    P140 = 140
    P150 = 150
    P160 = 160
    P170 = 170
    P180 = 180
    P190 = 190
    P200 = 200
    P210 = 210
    P220 = 220
    P230 = 230

    # One of the precedences allocated to '--' and '[x]' filters.
    # Has to be greater than precedence of 'not' to stop the 'not' in
    # 'not --' grabbing the implicit LHS set filter to '--'.
    # Precedence of 'not' is P60.
    # The same reasoning applies to the '=' filter whose precedence has
    # been set as described in a comment to filters.Assign class.
    # Has to be less than precedence of '|' to allow the '|' in 'k|q--'
    # to take the 'q' from the '--' filter.
    # Precedence of '|' is P160.
    PLOW = 66

    # One of the precedences allocated to '--' and '[x]' filters.
    # Has to be greater than precedence of ':' to stop the ':' in
    # 'currentpostion: --' grabbing the implicit LHS set filter to '--'.
    # Precedence of ':' is P230.
    PHIGH = 999

    def __ge__(self, other):
        """Return True for 'self >= other' for ordered enumeration."""
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        """Return True for 'self > other' for ordered enumeration."""
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        """Return True for 'self <= other' for ordered enumeration."""
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        """Return True for 'self < other' for ordered enumeration."""
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
