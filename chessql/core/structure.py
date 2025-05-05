# structure.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

# pylint C0302 too-many-lines.
# Ignore.

"""Chess Query Language (CQL) object class definitions.

This module defines the classes and functions needed by objects referred
to by the object which are values in the cql.class_from_token_name dict
which are not such values themselves.  Classes for whom instances are
returned by those values which are functions are kept in filters even
if not values in cql.class_from_token_name dict.

"""
import re

from . import basenode
from . import constants
from . import cqltypes
from . import keywords

# No simple designator can be a variable name.
_simple_designator_re = re.compile(
    r"".join(
        (
            r"^(?:",
            r"|".join(
                (
                    constants.PIECE_NAMES.join((r"[", r"]")),
                    constants.FILE_RANGE.join((r"[", r"]")),
                    r"".join(
                        (
                            constants.PIECE_NAMES.join((r"[", r"]?")),
                            constants.FILE_RANGE.join((r"[", r"]")),
                            constants.RANK_RANGE.join((r"[", r"]")),
                        )
                    ),
                )
            ),
            r")$",
        )
    )
)


class CQLObject(basenode.BaseNode):
    """Base class of classes which represent .constants.CQL_TOKENS matches."""

    # Most CQLObjects are not allowed as first item in QueryContainer.
    # Probably only CQL class will ever return True.
    _is_allowed_first_object_in_container = False

    def __init__(self, match_=None, container=None):
        """Delegate then set details for this instance and add to tree."""
        if not isinstance(match_, re.Match):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects a ",
                re.Match.__name__.join("''"),
                " instance but sees a ",
                match_.__class__.__name__.join("''"),
            )
        super().__init__(match_=match_, container=container)
        if container.cursor is container:
            if (
                len(container.cursor.children) == 1
                and not self.is_allowed_first_object_in_container
            ):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " instance must not be first item in query tree",
                )

    @property
    def parent(self):
        """Return self._parent."""
        return self._parent

    @parent.setter
    def parent(self, value):
        """Set self._parent."""
        self._parent = value

    @property
    def is_set_filter(self):
        """Return True if CQLobject instance is a Set Filter."""
        return self.filter_type is cqltypes.FilterType.SET

    @property
    def is_logical_filter(self):
        """Return True if CQLobject instance is a Logical Filter."""
        return self.filter_type is cqltypes.FilterType.LOGICAL

    @property
    def is_numeric_filter(self):
        """Return True if CQLobject instance is a Numeric Filter."""
        return self.filter_type is cqltypes.FilterType.NUMERIC

    @property
    def is_string_filter(self):
        """Return True if CQLobject instance is a String Filter."""
        return self.filter_type is cqltypes.FilterType.STRING

    @property
    def is_position_filter(self):
        """Return True if CQLobject instance is a Position Filter."""
        return self.filter_type is cqltypes.FilterType.POSITION

    @property
    def is_allowed_first_object_in_container(self):
        """Return True if CQLobject instance is allowed first in container."""
        return bool(self._is_allowed_first_object_in_container)

    def raise_if_name_parameter_not_for_filters(self):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        if not self.is_parameter_accepted_by_filter():
            if self.parent:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " instance is not a parameter of ",
                    self.parent.__class__.__name__.join("''"),
                    " instance",
                )
            self.raise_nodeerror(
                self.__class__.__name__,
                " instance cannot be a parameter because it has no parent",
            )

    # CQL-6.2 does not care if 'find' parameters are duplicated or about the
    # order of presentation.
    # Perhaps this is true of all parameters for all filters unless stated
    # otherwise: and maybe not even then because 'find' documentation talks
    # about parameter order.
    # 'line' rejects duplicates but 'move' does not.
    def _raise_if_name_parameter_duplicated(self):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        if (
            len(
                [
                    c
                    for c in self.parent.children
                    if isinstance(c, self.__class__)
                ]
            )
            > 1
        ):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " instance is duplicate parameter for instance of ",
                self.parent.__class__.__name__.join("''"),
            )

    def _raise_if_node_not_child_of_filters(self, name, filters):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        if self.parent:
            if not isinstance(self.parent, filters):
                if isinstance(filters, type):
                    filters = (filters,)
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " named ",
                    name.join("''"),
                    "' must be a child of one of ",
                    str([c.__name__ for c in filters]),
                    ", not ",
                    self.parent.__class__.__name__.join("''"),
                )
            return
        self.raise_nodeerror(
            name.join("''"),
            "' is not allowed for ",
            self.__class__.__name__.join("''"),
            " if parent does not exist",
        )

    # This method exists to allow BaseNode and CQLObject classes to be in
    # separate modules.
    def _match_string(self):
        """Return str containing the span of the match."""
        return " ".join((str(self.match_.span()), repr(self.match_[0])))

    def raise_if_not_number_of_children(self, number):
        """Raise NodeError if parent does not have number children."""
        if len(self.children) != number:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects ",
                str(number).join("''"),
                " children but got ",
                str(len(self.children)).join("''"),
            )

    def raise_if_not_same_filter_type(
        self, operation, filter_type=None, allowany=False
    ):
        """Raise NodeError if self's children are different filter types.

        self should be instance of one of '+=', '-=', '*=', '/=', %=',
        and comparison, classes.

        Any filter type except ANY is acceptable as rhs.

        When lhs is first mention of a variable, it's filter type will be
        ANY, nd any allowed rhs filter type is acceptable.

        """
        if self.container.function_body_cursor is not None:
            return
        lhs = self.children[0]
        rhs = self.children[1]
        if filter_type is not None and rhs.filter_type not in filter_type:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot ",
                operation,
                " because rhs filter type is ",
                str(rhs.filter_type).join("''"),
            )
        if lhs.filter_type is not rhs.filter_type and not allowany:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot ",
                operation,
                " because lhs filter type is ",
                str(lhs.filter_type).join("''"),
                " and rhs is ",
                str(rhs.filter_type).join("''"),
            )

    def raise_if_not_filter_type(self, child, filter_type):
        """Raise NodeError if child of parent is not a filter type.

        filter_type is the union of the allowed filter types.

        """
        if self.container.function_body_cursor is not None:
            return
        if child.filter_type not in filter_type:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects a ",
                filter_type.name.lower().join("''"),
                " argument but got a ",
                child.filter_type.name.lower().join("''"),
            )

    def raise_if_not_instance(self, child, instance, msg):
        """Raise NodeError if child of parent is not an instance.

        instance is a class or tuple of classses.

        """
        if not isinstance(child, instance):
            if isinstance(instance, tuple):
                names = ", ".join([c.__name__ for c in instance])
            else:
                names = instance.__name__
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " ",
                msg,
                " ",
                names.join("''"),
                " not a ",
                child.__class__.__name__.join("''"),
            )

    def is_instance_accepting_parameters(self):
        """Return True.

        This method is intended to qualify the answer of functions such
        as filters.is_range_parameter_accepted_by(node).  It should be
        extended by subclassses as needed (to return True or False).

        """
        return True


class Complete(CQLObject):
    """Define 'complete' and 'full' methods for filters with no children.

    Subclasses are filters which take no arguments or parameters, and
    parameters which take no arguments.

    NoArgumentsFilter is suitable as a superclass for filters which take
    no arguments but do take parameters.
    """

    def complete(self):
        """Return True.  Complete instances are always complete."""
        return True

    def full(self):
        """Return True.  Complete instances are always full.

        The full condition is the same as the complete condition.

        """
        return True


class CompleteBlock(CQLObject):
    """Define 'complete' and 'full' methods for filters in a block.

    The 'completed' attribute is initally False and is set True when the
    condition for the block of filters being complete is met.  Detection
    of ')' matching a '(' for example.
    """

    def complete(self):
        """Return True if self.completed is True."""
        return self.completed

    def full(self):
        """Return True if self.completed is True.

        The full condition is the same as the complete condition.

        """
        return self.completed


# This class was introduced when the precedence rule it implements was
# seen to fix a problem in puremate example at CQL-6.1.  Similar known
# problems with the order of filters in the parse tree for idealmate,
# modelmate, and parallelpaths, were fixed too.
# A number of examples with no current known problems have the order of
# filters changed: idealstalemate, indian, modelstalemate, pins, and
# pinstalemate.  The changed order looks correct.
class PrecedenceFromChild(CQLObject):
    """Define filter precedence from precedence of children.

    The observed behaviour, seen with CQLi-1.0.3 -parse option, for
    parameters to move and pin filters based on what is said in the
    precedence table documentation for CQL-6.1 is implemented by
    this class.  The CQLi-1.0.3 parse tree is assumed correct when
    compared with the CQL-6.1 parse tree because both CQLi-1.0.3 and
    CQL-6.1 produce the same answer when a CQL query is evaluated.

    Similar statements like 'arguments to ...', 'body of ...',
    'right side of ...', and 'parameter to ...' for piece and square
    filters, in the table of precedences suggest this class may be
    relevant for filters other than move and pin.  Places where this
    matters have not yet been spotted.
    """

    @property
    def precedence(self):
        """Return a non-None child precedence or self.precedence."""
        # The parameter's position in filter's children does not matter.
        # Perhaps this code works only because parameters involved have
        # a high precedence and clauses like 'move <parameters>:<filter>'
        # are not allowed by CQL-6.1, although CQLi-1.0.3 apparently
        # ignores the ':' and parses successfully making 'A' an
        # 'ImagineExpr' child of 'move', as in:
        # 'cql(input heijden.pgn) move o-o : A'.
        for child in self.children:
            precedence = child.precedence
            if precedence is not None:
                return precedence
        return self._precedence


class CompleteParameterArguments(CQLObject):
    """Define 'complete' and 'full' for filters with parameter arguments.

    The 'to' parameter of 'pin' filter take one argument for example.
    """

    def complete(self):
        """Return True if node representing filter is complete.

        The node must have one or more of the allowed parameters but no
        filters.  Each of the allowed parameters takes one filter as it's
        argument.

        """
        if len(self.children) == 0:
            return False
        if self.children[-1].is_parameter:
            if self.children[-1].is_parameter_accepted_by_filter():
                return False
        return True

    def full(self):
        """Return True if node representing filter is full.

        The node must have one or more of the allowed parameters but no
        filters.  Each of the allowed parameters takes one filter as it's
        argument.

        """
        if len(self.children) == 0:
            return True
        if self.children[-1].is_parameter:
            if not self.children[-1].full():
                return False
        return True


class Name(CQLObject):
    """Subclass of CQLObject for user defined names in CQL statements."""

    @basenode.BaseNode.name.setter
    def name(self, value):
        """Set self._name."""
        if self._name is None or self._name == value:
            self._name = value
            return
        self.raise_nodeerror(
            "A ",
            self.__class__.__name__.join("''"),
            " instance's name, ",
            str(self._name).join("''"),
            ", cannot be changed to ",
            value.join("''"),
            " once set",
        )

    def replace_formal_name(self, formal):
        """Set self._name to name in formal mapping."""
        name = self._name
        if name in formal and name in self.container.definitions:
            self._name = formal[name]
            return
        self.raise_nodeerror(
            "A ",
            self.__class__.__name__.join("''"),
            " instance expects it's name ",
            name.join("''"),
            ", to be in both the 'formal' parameter and the container ",
            "definitions",
        )

    def _raise_if_already_defined(self, definition_types, definition_type):
        """Raise NodeError if name exists with type in definition_types."""
        name = self._name
        container = self.container
        if (
            name in container.definitions
            and container.definitions[name].definition_type in definition_types
        ):
            self.raise_nodeerror(
                name.join("''"),
                " is a ",
                container.definitions[name]
                .definition_type.name.lower()
                .join("''"),
                " object so cannot be defined as a ",
                definition_type.name.lower().join("''"),
                " object",
            )

    def _raise_if_characters_invalid(self, type_):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        name = self._name
        if name in keywords.KEYWORDS:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " named ",
                name.join("''"),
                " is a keyword and cannot be a ",
                type_.__name__.lower().join("''"),
                " name",
            )
        if _simple_designator_re.match(name):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " named ",
                name.join("''"),
                " is a piece designator and cannot be a ",
                type_.__name__.lower().join("''"),
                " name",
            )
        if name[0].isdigit():
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " named ",
                name.join("''"),
                " starts with a digit and cannot be a ",
                type_.__name__.lower().join("''"),
                " name",
            )
        if name.isdigit():
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " named ",
                name.join("''"),
                " is all digits and cannot be a ",
                type_.__name__.lower().join("''"),
                " name",
            )

    def _raise_if_name_reserved(self, type_):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        name = self._name
        if name.startswith(constants.UPPER_CASE_CQL_PREFIX):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " of ",
                type_.join("''"),
                " named ",
                type_.__name__.lower().join("''"),
                " starts with reserved sequence ",
                constants.UPPER_CASE_CQL_PREFIX.join("''"),
            )
        if name.startswith(constants.LOWER_CASE_CQL_PREFIX):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " of ",
                type_.join("''"),
                " named ",
                type_.__name__.lower().join("''"),
                " starts with reserved sequence ",
                constants.LOWER_CASE_CQL_PREFIX.join("''"),
            )

    def _raise_if_name_invalid(self, type_):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        self._raise_if_characters_invalid(type_)
        self._raise_if_name_reserved(type_)

    def _raise_if_wrong_variable_type(self, variable_type):
        """Raise NodeError if name exists as a variable of another type."""
        name = self._name
        container = self.container
        if name in container.definitions and not container.definitions[
            name
        ].is_variable_type(variable_type):
            self.raise_nodeerror(
                name.join("''"),
                " is a ",
                container.definitions[name]
                .variable_type.name.lower()
                .join("''"),
                " variable so cannot be a ",
                variable_type.name.lower().join("''"),
                " variable",
            )


class VariableTypeSetter(Name):
    """Subclass of Name for setting properties of variable names in CQL.

    The various types of variable have behaviour which differs from
    function and dictionary in CQL.
    """

    def raise_if_child_cannot_be_index(self, child):
        """Raise NodeError if child cannot be index into self's value.

        This method implements the default test, which is for user defined
        variables.  In particular the Dictionary subclass must override to
        implement tests appropriate to user defined dictionaries.

        """
        if child.filter_type is cqltypes.FilterType.STRING:
            self.raise_nodeerror(
                child.__class__.__name__.join("''"),
                " cannot index a ",
                self.__class__.__name__.join("''"),
                " instance",
            )

    # Some of this should be delegated to class Name because it looks to
    # be shared with classes for the 'function' and 'dictionary' filters.
    def _set_variable_filter_type(self, filter_type, nametype="variable"):
        """Set filter type of variable instance.

        The variable's name must have been registered by a prior call of
        _register_variable_type.

        The variable's variable type is set to variable_type if it is
        cqltypes.VariableType.ANY currently.

        The variable's filter type is set to filter_type if it is
        cqltypes.FilterType.ANY currently.

        A NodeError exception is raised on attempting to change any other
        variable type or filter type value.

        Details for user defined items, variables and functions, are not
        updated when encountered during collection of functions bodies.

        """
        container = self.container
        if container.function_body_cursor is not None:
            return
        definitions = container.definitions
        name = self.name
        if name not in definitions:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " of ",
                nametype.join("''"),
                " named ",
                name.join("''"),
                " has not been registered (",
                "by _register_variable_type)",
            )
        item = definitions[name]
        if item.filter_type is cqltypes.FilterType.ANY:
            item.filter_type = filter_type
        if item.filter_type is not filter_type:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " of ",
                nametype.join("''"),
                " named ",
                name.join("''"),
                " is a ",
                item.filter_type.name.lower().join("''"),
                " filter so cannot be set as a ",
                filter_type.name.lower().join("''"),
                " filter",
            )

    def _set_persistence_type(self, persistence_type, check_types=None):
        """Register variable as persistence_type or validate existing entry.

        Details for user defined items, variables and functions, are not
        updated when encountered during collection of functions bodies.

        """
        definitions = self.container.definitions
        name = self.name
        if name not in definitions:
            if self.container.function_body_cursor is not None:
                return
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                "' cannot set persistence type because ",
                name.join("''"),
                " is not in definitions ",
                "(has _register_variable_type been called?)",
            )
        item = definitions[name]
        if item.persistence_type is cqltypes.PersistenceType.ANY:
            item.persistence_type = persistence_type
            return
        if check_types is None:
            check_types = persistence_type
        for test in check_types:
            if test in persistence_type and test not in item.persistence_type:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " cannot set ",
                    name.join("''"),
                    " as '",
                    test.name.lower().join("''"),
                    " because it is not already ",
                    test.name.lower().join("''"),
                )


class VariableName(VariableTypeSetter):
    """Subclass of VariableTypeSetter for user defined variable names in CQL.

    The various types of variable have behaviour which differs from
    function and dictionary in CQL.
    """

    # Probably should be able to put this in class Name but cannot now.
    @property
    def filter_type(self):
        """Return filter_type from variable's entry in definitions."""
        if self.container.function_body_count > 0:
            if self.name not in self.container.definitions:
                return cqltypes.FilterType.ANY
        try:
            return self.container.definitions[self.name].filter_type
        except KeyError as exc:
            raise basenode.NodeError(
                "".join(
                    (
                        "Name definition '",
                        str(self.name),
                        "' referenced before it is set",
                    )
                )
            ) from exc

    def _register_variable_type(self, variable_type):
        """Register variable as variable_type or validate existing entry.

        Details for user defined items, variables and functions, are not
        updated when encountered during collection of functions bodies.

        """
        definitions = self.container.definitions
        name = self.name
        self._raise_if_name_invalid(cqltypes.Variable)
        if name not in definitions:
            cqltypes.variable(name, self.container)
            if self.container.function_body_cursor is None:
                definitions[name].variable_type = variable_type
        self._raise_if_already_defined(
            cqltypes.DefinitionType.ANY ^ cqltypes.DefinitionType.VARIABLE,
            cqltypes.DefinitionType.VARIABLE,
        )
        self._raise_if_wrong_variable_type(variable_type)

    def set_variable_types(
        self, variable_type, filter_type, nametype="variable"
    ):
        """Set variable type and filter type of variable instance.

        The variable's name must have been registered by a prior call of
        _register_variable_type.

        The variable's variable type is set to variable_type if it is
        cqltypes.VariableType.ANY currently.

        The variable's filter type is set to filter_type if it is
        cqltypes.FilterType.ANY currently.

        A NodeError exception is raised on attempting to change any other
        variable type or filter type value.

        Details for user defined items, variables and functions, are not
        updated when encountered during collection of functions bodies.

        """
        if self.container.function_body_cursor is not None:
            return
        super()._set_variable_filter_type(filter_type, nametype=nametype)
        item = self.container.definitions[self.name]
        if item.variable_type is cqltypes.VariableType.ANY:
            item.variable_type = variable_type
        if item.variable_type is not variable_type:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " of ",
                nametype.join("''"),
                " naamed ",
                self.name.join("''"),
                " is a ",
                item.variable_type.name.lower().join("''"),
                " variable so cannot be set as a ",
                variable_type.name.lower().join("''"),
                " variable",
            )

    def _set_persistence_type(self, persistence_type, check_types=None):
        """Delegate, checking for 'PERSISTENT' persistence type only."""
        super()._set_persistence_type(
            persistence_type, check_types=cqltypes.PersistenceType.PERSISTENT
        )

    # This method exists to allow BaseNode and VariableName classes to
    # be in separate modules.
    def _is_node_variablename_instance(self):
        """Return True."""
        return True


class DictionaryName(VariableTypeSetter):
    """Subclass of VariableTypeSetter for user defined dictionary names.

    The various types of dictionary have behaviour which differs from
    function and variable in CQL.
    """

    # Introduced to allow filters._DashOrTake to become structure.DashOrTake
    # so InfixLeft.place_node_in_tree() can refer to it easily.
    # VariableName already exists for variable and additions to dictionary
    # behaviour in CQL may make this necessary in future anyway.
    # Tests with BaseNode.is_node__dashortake_instance(), which returns
    # False, and _DashOrTake.is_node__dashortake_instance(), which returns
    # True, show the unittest ERROR outcomes can be replaced by fewer
    # unittest FAIL outcomes in different tests which passed before.
    # The problem is constructively changed to one involving the relative
    # precedence of 'and', 'or', and the various '--'-like filters.

    def raise_if_child_cannot_be_index(self, child):
        """Raise NodeError if child cannot be index into self's value.

        This method implements the test for user defined dictionaries.

        """
        if child.filter_type is cqltypes.FilterType.LOGICAL:
            self.raise_nodeerror(
                child.__class__.__name__.join("''"),
                " cannot index a ",
                self.__class__.__name__.join("''"),
                " instance",
            )
        # Assume dictionary is either PERSISTENT or LOCAL.
        if (
            child.filter_type is cqltypes.FilterType.POSITION
            and self.container.definitions[self.name].persistence_type
            is cqltypes.PersistenceType.PERSISTENT
        ):
            self.raise_nodeerror(
                child.__class__.__name__.join("''"),
                " can only index a ",
                cqltypes.PersistenceType.LOCAL.name.join("''"),
                " ",
                self.__class__.__name__.join("''"),
                " instance",
            )


class Argument(CQLObject):
    """Subclass of CQLObject for keywords with unparenthesized argument.

    The argument may be a compound or simple filter.  This implies nesting
    of '()' and '{}' compound filter clauses is permitted.
    """

    # Keywords with unparenthesized argument take one child by default.
    _child_count = 1

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class LeftParenthesisInfix(CQLObject):
    """Subclass of CQLObject for keywords with implied block to next Infix.

    The query 'countmoves -- == 1' is equivalent to '(countmoves --) == 1'.

    This class exists to allow filters represented by Infix instances to
    spot ancestor filters like 'countmoves' and adjust the cursor so the
    query is not seen as 'countmoves (-- == 1)'.
    """

    def is_countmoves(self):
        """Return True if self is an instance of filters.CountMoves.

        To cope with 'countmoves legal -- == 1 and 'legal -- == 1'.

        """
        return False


class BindArgument(Argument):
    """The variable argument for 'isbound', 'isunbound' and 'unbind'.

    CQL-6.2 Table of Precedence does not give any binding filter a
    precedence.  For 'unbind v or unbind w' the 'unbind' filter must have
    a precedence greater than the comparison operators.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    @property
    def precedence(self):
        """Return precedence greater than logical when comparing.

        The logical operator will be the '-1' child of cursor at time
        of precedence checking.

        """
        if isinstance(self.container.cursor.children[-1], Infix):
            if not isinstance(self.container.cursor, DictionaryName):
                return cqltypes.Precedence.PHIGH  # Higher than P80.
        return self._precedence

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        child = self.children[0]
        if not isinstance(child, Name):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects a variable name but got a ",
                child.__class__.__name__.join("''"),
            )


class BlockLeft(CompleteBlock):
    """Subclass of CQLObject for keywords which start a block.

    These are '(' and '{' in various contexts represented by different
    classes.

    Subclasses may override the _child_count attribute but at time of
    writing seems unnecessary though the Between subclass does this.

    The corresponding *Right class, sometimes *End, is expected to set
    completed to True.

    BracketLeft is not included because it is treated as an InfixLeft subclass
    but Path might be included because it is ended by a blank line.
    """

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class ParenthesizedArguments(BlockLeft):
    """Subclass of CQLObject for keywords with parenthesized arguments.

    Each argument may be a compound or simple filter.  This implies nesting
    of '()' and '{}' compound filter clauses is permitted.
    """


class MaxOrMin(ParenthesizedArguments):
    """Subclass of ParenthesizedArguments for 'min' and 'max' filters."""

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if len(self.children) < 2:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have at least two arguments",
            )
        filter_types = set()
        for child in self.children:
            self.raise_if_not_filter_type(
                child,
                cqltypes.FilterType.NUMERIC | cqltypes.FilterType.STRING,
            )
            filter_types.add(child.filter_type)
        if len(filter_types) != 1:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " arguments must be all string or all numeric",
            )
        if self.container.function_body_cursor is not None:
            return
        self.filter_type = self.children[-1].filter_type


# An infix operator is first encountered in the sequence 'G P I' where
# G is grandparent node, P is parent node, and infix operator I is self.
# This sequence implies G.parent(P) and P.parent(I) with P and I being
# the '-1' child of the parent.  Changing the sequence changes these
# relationships to fit.
# P has to be a full filter: so P could be last token provided all it's
# ancestors are full.
# If G is not a filter the sequence is changed to 'G I P' and P becomes
# complete, and marked so if child count does not decide, so I is now
# the container cursor.
# G is assumed to be a filter below.
# If G has higher precedence than I the sequence is changed to 'I G P'.
# If G has lower precedence than I the sequence is changed to 'G I P'
# and I is now the container cursor.
# Filters with the same precedence must have the same associativity:
# left, right, or None.
# G and I are assumed to have same associativity below.
# If G and I have left associativity the sequence is changed to 'I G P'.
# If G and I have right associativity the sequence is changed to 'G I P'
# and I is now the container cursor.
# 'G P I' cannot be said if G and I have no associativity.
class Infix(CQLObject):
    """Subclass of CQLObject for infix operators."""

    # Keywords for infix operators take two childs.
    _child_count = 2

    def __init__(self, match_=None, container=None):
        """Adjust container cursor for operator precedence then delegate."""
        # QueryContainer is not full until all tokens have been consumed.
        # '{', '(', and '[', will be container only when no non-whitespace
        # tokens have been consumed since before this one; and are not
        # full until the corresponding '}', ')', or ']', is consumed.
        # Infix operators are not full until their second argument has
        # been consumed.
        if not container.cursor.full():
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot apply this operator to incomplete ",
                container.cursor.__class__.__name__.join("''"),
            )
        if len(container.cursor.parent.children) == 0:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cursor's parent (a ",
                container.cursor.parent.__class__.__name__.join("''"),
                ") should have at least one child but has none",
            )
        if container.cursor is not container.cursor.parent.children[-1]:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cursor (a ",
                container.cursor.__class__.__name__.join("''"),
                ") is not the last child of it's parent",
            )
        super().__init__(match_=match_, container=container)

    def _swap_tree_position(self, ancestor):
        """Make ancestor self's parent, and self parent of last child."""
        self.children.append(ancestor.children.pop(-1))
        ancestor.children.append(self)
        del self.parent.children[-1]
        self.parent = ancestor
        self.children[-1].parent = self
        self.container.cursor = self

    def _end_left_parenthesis_infix_block(self):
        """Adjust cursor if a LeftParenthesisInfix ancestor is found.

        Four sets of statements are handled: 'countmoves legal --',
        'countmoves --', 'legal --', and 'pseudolegal --', where '--'
        could be any of the '--' or '[x]' variants; where followed by
        an infix operator.

        """
        countmoves_loop_done = False
        while True:
            # The obvious thing to do is start node at 'self' but that
            # attracts a pylint E1101 no-member report at the following
            # 'node.is_countmoves()'.  That statement is unreachable for
            # an Infix instance, so start node at 'self.parent' instead
            # because self is an Infix instance.
            node = self.parent
            while node:
                if isinstance(node, BlockLeft) and not node.complete():
                    break
                if isinstance(node, LeftParenthesisInfix) and node.full():
                    if node.is_countmoves() or countmoves_loop_done:
                        self._swap_tree_position(node.parent)
                        return True
                node = node.parent
            if countmoves_loop_done:
                break
            countmoves_loop_done = True
        return False

    def _verify_and_set_filter_type(self, node):
        """Verify children and set filter type for ancestors of node."""
        # The test on CompleteParameterArguments causes the two 'colon'
        # filters which operate on a 'move' filter terminated by an 'and'
        # filter to get their correct filter type in the castleecho example.
        # The problem is the 'move' filter never gets marked complete.
        # The problem affects the 'pin' filter too, but not the 'line'
        # filter because 'line --> check' has to be within '()' to get the
        # same request structure.
        while True:
            node = node.parent
            if not node.full():
                if not isinstance(node, CompleteParameterArguments):
                    break
            node.verify_children_and_set_types(set_node_completed=True)

    def _raise_if_parent_is_not_cursor(self, parent):
        """Raise NodeError if parent is not cursor."""
        if parent is not self.container.cursor:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects it's parent, a ",
                parent.__class__.__name__.join("''"),
                ", to be the cursor but the cursor is some other node",
            )

    def _raise_if_precedence_is_none(self):
        """Raise NodeError if precedence is None."""
        if self.precedence is None:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " has precedence None but it should have a ",
                cqltypes.Precedence.__name__.join("''"),
                " precedence value",
            )


class InfixLeft(Infix):
    """Subclass of CQLObject for left associative infix operators."""

    # Class CQL implements implicit top-level '{}' block at present.
    def place_node_in_tree(self):
        """Adjust node hierarchy, assert cursor is parent."""
        parent = self.parent
        ancestor = parent.parent
        self._raise_if_parent_is_not_cursor(parent)
        self._raise_if_precedence_is_none()
        if self._end_left_parenthesis_infix_block():
            return
        while True:
            if isinstance(ancestor, BlockLeft):
                break
            grand_ancestor_precedence = ancestor.parent.precedence
            if grand_ancestor_precedence is None:
                break
            if grand_ancestor_precedence.value < self.precedence.value:
                break
            ancestor = ancestor.parent
        if ancestor.precedence is None:
            if not isinstance(ancestor, CompleteParameterArguments):
                self._swap_tree_position(ancestor)
            else:
                self._swap_tree_position(ancestor.parent.parent)
            parent.verify_children_and_set_types(set_node_completed=True)
            self._verify_and_set_filter_type(parent)
            return
        # For 'if 1 + 2 then k' (legal nonsense left association in 'if').
        if ancestor.complete() and not isinstance(ancestor, DashOrTake):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects to swap places in an incomplete ",
                ancestor.__class__.__name__.join("''"),
                " instance but sees a completed one",
            )
        if self.precedence.value < ancestor.precedence.value:
            self._swap_tree_position(ancestor.parent)
            self._verify_and_set_filter_type(parent)
            return
        if ancestor.precedence.value < self.precedence.value:
            self._swap_tree_position(ancestor)
            self._verify_and_set_filter_type(parent)
            return
        if not isinstance(ancestor, InfixLeft):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects to swap places with a ",
                InfixLeft.__name__.join("''"),
                " instance but sees a ",
                ancestor.__class__.__name__.join("''"),
            )
        self._swap_tree_position(ancestor.parent)
        self._verify_and_set_filter_type(parent)
        return


class InfixRight(Infix):
    """Subclass of CQLObject for right associative infix operators."""

    # Class CQL implements implicit top-level '{}' block at present.
    def place_node_in_tree(self):
        """Adjust node hierarchy, assert cursor is parent."""
        parent = self.parent
        ancestor = parent.parent
        self._raise_if_parent_is_not_cursor(parent)
        self._raise_if_precedence_is_none()
        if self._end_left_parenthesis_infix_block():
            return
        while True:
            if isinstance(ancestor, BlockLeft):
                break
            grand_ancestor_precedence = ancestor.parent.precedence
            if grand_ancestor_precedence is None:
                break
            if grand_ancestor_precedence.value < self.precedence.value:
                break
            ancestor = ancestor.parent
        if ancestor.precedence is None:
            if not isinstance(ancestor, CompleteParameterArguments):
                self._swap_tree_position(ancestor)
            else:
                self._swap_tree_position(ancestor.parent)
            parent.verify_children_and_set_types(set_node_completed=True)
            self._verify_and_set_filter_type(parent)
            return
        # For 'if 1 > 2 then k' (legal nonsense right association in 'if').
        if ancestor.complete():
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects to swap places in an incomplete ",
                ancestor.__class__.__name__.join("''"),
                " instance but sees a completed one",
            )
        if self.precedence.value < ancestor.precedence.value:
            self._swap_tree_position(ancestor.parent)
            self._verify_and_set_filter_type(parent)
            return
        if ancestor.precedence.value < self.precedence.value:
            self._swap_tree_position(ancestor)
            self._verify_and_set_filter_type(parent)
            return
        if not isinstance(ancestor, InfixRight):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects to swap places with a ",
                InfixRight.__name__.join("''"),
                " instance but sees a ",
                ancestor.__class__.__name__.join("''"),
            )
        self._swap_tree_position(ancestor)
        self._verify_and_set_filter_type(parent)
        return


# Name is inappropriate now because this class no longer has anything to
# do with the '--' and '[x]' filters (see DashOrTake class).
class MoveInfix(Infix):
    """Subclass of Infix for '→', '←', '∊', and '=?' operators.

    '->' is the ascii version of '→'.
    '<-' is the ascii version of '←'.
    '[element]' is the ascii version of '∊'.
    '=?' is ascii with no utf8 equivalent.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Class CQL implements implicit top-level '{}' block at present.
    def place_node_in_tree(self):
        """Make prior sibling a child of self, assert cursor is parent."""
        parent = self.parent
        self._raise_if_parent_is_not_cursor(parent)
        if self.precedence is not None:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " is expected to have precedence None but it is ",
                self.precedence.name.join("''"),
            )
        self._swap_tree_position(parent.parent)
        self._verify_and_set_filter_type(parent)


class DashOrTake(InfixLeft):
    """Represent shared behaviour of '--' and '[x]' filters.

    The '--' and '[x]' filters may have either, or both, promotion and
    target conditions in addition to the LHS and RHS filters accepted by
    InfixLeft.

    The promotion condition is idicated by a trailing '=' clause, and the
    target condition is indicated by a trailing '(...)' clause.  The '='
    clause appears first if both are present.

    The filter_type of final filter in target condition becomes filter type
    of the DashOrTake instance.  The absence of target conditions cause the
    DashOrTake instance to be a logical filter.
    """

    def place_node_in_tree(self):
        """Delegate then set container cursor to self."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self

    def _end_left_parenthesis_infix_block(self):
        """Override, do nothing.

        Class LeftParenthesisInfix is introduced to protect DashOrTake
        instances from disruption by other Infix class instances.

        This protection is not required for DashOrTake instances.
        """

    def _raise_if_dash_or_take_arguments_are_not_filter_type_set(self):
        """Raise NodeError if first two arguments of filter_ are not sets.

        Dash and Take instances can have up to four arguments, the last two
        being AssignPromotion and TargetParenthesisLeft instances.

        """
        for item, child in enumerate(self.children):
            if item < 2:
                if (
                    self.container.function_body_count is not None
                    and isinstance(child, (VariableName, DictionaryName))
                ):
                    continue
                if child.filter_type is not cqltypes.FilterType.SET:
                    if child.filter_type:
                        name = child.filter_type.name.lower()
                    else:
                        name = str(None)
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " expects a ",
                        cqltypes.FilterType.SET.name.lower().join("''"),
                        " but got a ",
                        name.join("''"),
                    )

    def _raise_if_dash_or_take_has_dash_or_take_argument(self):
        """Raise NodeError if '--' or '[x]' is one of first two arguments.

        This situation arises from queries like '--(k)--'.

        """
        for item, child in enumerate(self.children):
            if item < 2 and isinstance(child, DashOrTake):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " got a ",
                    child.__class__.__name__.join("''"),
                    " argument likely due to missing space between",
                    " target and next '--' or '[x]' filter",
                )

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self._raise_if_dash_or_take_arguments_are_not_filter_type_set()
        self._raise_if_dash_or_take_has_dash_or_take_argument()


class Numeric(InfixLeft):
    """Subclass of InfixLeft for numeric operators."""

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        self.raise_if_not_same_filter_type(
            "apply arithmetic operation",
            filter_type=cqltypes.FilterType.NUMERIC,
        )


class ComparePosition(CQLObject):
    """Subclass of CQLObject for comparing only Position filters."""

    @property
    def filter_type(self):
        """Verify children are comparable filter types.

        This method should be called only from a place_node_in_tree method.
        """
        children = self.children
        filtertype = cqltypes.FilterType
        left_child = children[0]
        right_child = children[1]
        if (
            left_child.filter_type is filtertype.POSITION
            and right_child.filter_type is filtertype.POSITION
        ):
            return filtertype.POSITION
        return super().filter_type

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        self.raise_if_not_same_filter_type(
            "compare", filter_type=cqltypes.FilterType.POSITION
        )


class CompareSet(CQLObject):
    """Subclass of CQLObject for comparing only Set filters."""

    @property
    def filter_type(self):
        """Verify children are comparable filter types.

        This method should be called only from a place_node_in_tree method.
        """
        children = self.children
        filtertype = cqltypes.FilterType
        left_child = children[0]
        right_child = children[1]
        if (
            left_child.filter_type is filtertype.SET
            and right_child.filter_type is filtertype.SET
        ):
            return filtertype.SET
        return super().filter_type


class Compare(CQLObject):
    """Subclass of CQLObject for comparing filters."""

    # For all relational filters except '=='.
    _comparable_filter_types = (
        cqltypes.FilterType.NUMERIC
        | cqltypes.FilterType.STRING
        | cqltypes.FilterType.POSITION
    )

    _coerce_to_numeric = cqltypes.FilterType.SET | cqltypes.FilterType.NUMERIC

    @property
    def filter_type(self):
        """Verify children are comparable filter types.

        This method should be called only from a place_node_in_tree method.
        """
        children = self.children
        filtertype = cqltypes.FilterType
        left_child = children[0]
        right_child = children[1]
        if (
            left_child.filter_type is filtertype.POSITION
            and right_child.filter_type is filtertype.POSITION
        ):
            return filtertype.POSITION
        if (
            left_child.filter_type is filtertype.STRING
            and right_child.filter_type is filtertype.STRING
        ):
            return filtertype.STRING
        if (
            left_child.filter_type is filtertype.NUMERIC
            and right_child.filter_type is filtertype.NUMERIC
        ):
            return filtertype.NUMERIC
        if (
            left_child.filter_type is filtertype.NUMERIC
            or right_child.filter_type is filtertype.NUMERIC
        ) and (
            left_child.filter_type is filtertype.SET
            or right_child.filter_type is filtertype.SET
        ):
            return filtertype.NUMERIC
        return super().filter_type

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        if (
            self.children[0].filter_type | self.children[1].filter_type
            == self._coerce_to_numeric
        ):
            return
        self.raise_if_not_same_filter_type(
            "compare",
            filter_type=self._comparable_filter_types,
            allowany=self.container.function_body_count > 0,
        )


class ParameterArgument(CQLObject):
    """Subclass of CQLObject for parameters which take an argument."""

    _is_parameter = True
    # Keywords with unparenthesized argument take one child by default.
    _child_count = 1

    @property
    def filter_type(self):
        """Return filter type of child.

        Look at the '-1' child because usually the last in a list of
        things determines the type of the container.  For example
        '{2 k}' is a set filter and '{k 2}' is a numeric filter.

        """
        return self.children[-1].filter_type

    def place_node_in_tree(self):
        """Delegate then verify parameter and set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self
        self.raise_if_name_parameter_not_for_filters()
        self._raise_if_name_parameter_duplicated()


class NoArgumentsParameter(Complete):
    """Subclass of CQLObject for parameters which do not take arguments."""

    _is_parameter = True

    def place_node_in_tree(self):
        """Delegate then verify parameter and set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self
        self.raise_if_name_parameter_not_for_filters()
        self._raise_if_name_parameter_duplicated()


def is_direction_parameter_accepted_by(node):
    """Return True if node accepts a direction parameter."""
    del node
    # The 'ray' pattern catches both parameter and '('.  It is the only
    # filter which accepts any of the direction parameters.
    # If the pattern is changed to look ahead for parameter and '(' this
    # return statement should be uncommented.
    # return isinstance(node, Ray)


class DirectionParameter(NoArgumentsParameter):
    """Subclass of NoArgumentsParameter for direction parameters."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_direction_parameter_accepted_by(self.parent)


class NoArgumentsFilter(CQLObject):
    """Subclass of CQLObject for filters which do not take arguments.

    Where a number of keywords are chained to define a filter these filters
    terminate the chain.

    Complete is suitable as a superclass for filters which take neither
    arguments nor parameters.
    """

    # Keywords no argument take zero childs.
    _child_count = 0

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class ImplicitSearchFilter(NoArgumentsFilter):
    """Subclass of CQLObject for filters with optional string search argument.

    Without the quoted string argument the value of the relevant PGN Tag
    matches.  In other words <any value> can be taken as the argument.
    """

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if len(self.children) > 1:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects at most one argument but ",
                str(len(self).children).join("''"),
                " but has 2",
            )


class ModifyAssign(CQLObject):
    """Shared behaviour of '<operator>=' filters which have numeric rhs."""

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        lhs = self.children[0]
        self.raise_if_not_instance(lhs, VariableName, "lhs must be a")
        rhs = self.children[1]
        if self.container.function_body_cursor is None or not isinstance(
            rhs, VariableName
        ):
            if rhs.filter_type is not cqltypes.FilterType.NUMERIC:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " rhs must be a Numeric filter",
                )
        set_persistent_variable_filter_type(lhs, rhs)
        if self.container.function_body_cursor is None or not isinstance(
            rhs, VariableName
        ):
            self.raise_if_not_same_filter_type("assign")


class SquareIn(VariableName, Argument):
    """Represent 'square in', with or without 'all' parameter, filter.

    Filter type is the _filter_type of a subclass, not the filter_type from
    the definition of the associated variable.
    """

    _precedence = cqltypes.Precedence.P30
    _child_count = 2

    def __init__(self, match_=None, container=None):
        """Delegate then register the set variable name for square filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["square"]
        self._register_variable_type(cqltypes.VariableType.SET)
        self.set_variable_types(
            cqltypes.VariableType.SET, cqltypes.FilterType.SET
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)

    @property
    def filter_type(self):
        """Return filter_type for class."""
        return self._filter_type

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        self.raise_if_not_filter_type(
            self.children[0],
            cqltypes.FilterType.SET,
        )


def set_persistent_variable_filter_type(lhs, rhs):
    """Set filter type of lhs from rhs if not already set.

    This function is intended for calling by filters.AssignPlus and
    ModifyAssign only.

    Validation and raise are assumed to be done by caller.

    """
    container = lhs.container
    if container.function_body_cursor is not None:
        return
    definition = container.definitions[lhs.name]
    if definition.filter_type is not cqltypes.FilterType.ANY:
        return
    if definition.persistence_type is cqltypes.PersistenceType.PERSISTENT:
        definition.filter_type = rhs.filter_type
