# structure.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

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
                    constants.FILE_NAMES.join((r"[", r"]")),
                    r"".join(
                        (
                            constants.PIECE_NAMES.join((r"[", r"]?")),
                            constants.FILE_NAMES.join((r"[", r"]")),
                            constants.RANK_NAMES.join((r"[", r"]")),
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
        assert isinstance(match_, re.Match)
        super().__init__(match_=match_, container=container)
        if container.cursor is container:
            if (
                len(container.cursor.children) == 1
                and not self.is_allowed_first_object_in_container
            ):
                raise basenode.NodeError(
                    self.__class__.__name__
                    + ": '"
                    + self.__class__.__name__
                    + "' instance must not be first item in query tree"
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
                raise basenode.NodeError(
                    self.__class__.__name__
                    + " instance is not a parameter of "
                    + self.parent.__class__.__name__
                    + " instance"
                )
            raise basenode.NodeError(
                self.__class__.__name__
                + " instance cannot be a parameter because it has no parent"
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
            raise basenode.NodeError(
                self.__class__.__name__
                + " instance is duplicate parameter for instance of "
                + self.parent.__class__.__name__
            )

    def _raise_if_node_not_child_of_filters(self, name, filters):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        if self.parent:
            if not isinstance(self.parent, filters):
                if isinstance(filters, type):
                    filters = (filters,)
                raise basenode.NodeError(
                    self.__class__.__name__
                    + ": '"
                    + name
                    + "' must be a child of one of "
                    + str([c.__name__ for c in filters])
                    + ", not "
                    + self.parent.__class__.__name__
                )
            return
        raise basenode.NodeError(
            "'"
            + name
            + "' is not allowed for "
            + self.__class__.__name__
            + " if parent does not exist"
        )

    # This method exists to allow BaseNode and CQLObject classes to be in
    # separate modules.
    def _match_string(self):
        """Return str containing the span of the match."""
        return " ".join((str(self.match_.span()), repr(self.match_[0])))


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
        """Return True if node representing filter is complete.

        The full condition is the same as the complete condition.

        """
        if len(self.children) == 0:
            return False
        if self.children[-1].is_parameter:
            if self.children[-1].is_parameter_accepted_by_filter():
                return False
        return True


class Name(CQLObject):
    """Subclass of CQLObject for user defined names in CQL statements."""

    @basenode.BaseNode.name.setter
    def name(self, value):
        """Set self._name."""
        assert self._name is None or self._name == value
        self._name = value

    def replace_formal_name(self, formal):
        """Set self._name to name in formal mapping."""
        name = self._name
        assert name in formal and name in self.container.definitions
        self._name = formal[name]

    def _raise_if_already_defined(self, definition_types, definition_type):
        """Raise NodeError if name exists with type in definition_types."""
        name = self._name
        container = self.container
        if (
            name in container.definitions
            and container.definitions[name].definition_type in definition_types
        ):
            raise basenode.NodeError(
                "'"
                + name
                + "' is a '"
                + container.definitions[name].definition_type.name.lower()
                + "' object so cannot be defined as a '"
                + definition_type.name.lower()
                + "' object"
            )

    def _raise_if_characters_invalid(self, type_):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        name = self._name
        if name in keywords.KEYWORDS:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": '"
                + name
                + "' is a keyword and cannot be a "
                + type_.__name__.lower()
                + " name"
            )
        if _simple_designator_re.match(name):
            raise basenode.NodeError(
                self.__class__.__name__
                + ": '"
                + name
                + "' is a piece designator and cannot be a "
                + type_.__name__.lower()
                + " name"
            )
        if name[0].isdigit():
            raise basenode.NodeError(
                self.__class__.__name__
                + ": '"
                + name
                + "' starts with a digit and cannot be a "
                + type_.__name__.lower()
                + " name"
            )
        if name.isdigit():
            raise basenode.NodeError(
                self.__class__.__name__
                + ": '"
                + name
                + "' is all digits and cannot be a "
                + type_.__name__.lower()
                + " name"
            )

    def _raise_if_name_reserved(self, type_):
        """Raise NodeError if conditions are met.

        Should be defined in CQLObject but put in BaseNode if necessary.
        """
        name = self._name
        if name.startswith(constants.UPPER_CASE_CQL_PREFIX):
            raise basenode.NodeError(
                self.__class__.__name__
                + ": "
                + type_
                + "'"
                + type_.__name__.lower()
                + "' starts with reserved sequence "
                + constants.UPPER_CASE_CQL_PREFIX
            )
        if name.startswith(constants.LOWER_CASE_CQL_PREFIX):
            raise basenode.NodeError(
                self.__class__.__name__
                + ": "
                + type_
                + "'"
                + type_.__name__.lower()
                + "' starts with reserved sequence "
                + constants.LOWER_CASE_CQL_PREFIX
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
            raise basenode.NodeError(
                "'"
                + name
                + "' is a '"
                + container.definitions[name].variable_type.name.lower()
                + "' variable so cannot be a '"
                + variable_type.name.lower()
                + "' variable"
            )


class VariableName(Name):
    """Subclass of Name for user defined variable names in CQL.

    The various types of variable have behaviour which differs from
    function and dictionary in CQL.
    """

    # Probably should be able to put this in class Name but cannot now.
    @property
    def filter_type(self):
        """Return filter_type from variable's entry in definitions."""
        try:
            return self.container.definitions[self.name].filter_type
        except KeyError as exc:
            raise basenode.NodeError(
                "Name definition '"
                + str(self.name)
                + "' referenced before it is set"
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

    def set_types(self, variable_type, filter_type):
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
        container = self.container
        if container.function_body_cursor is not None:
            return
        definitions = container.definitions
        name = self.name
        if name not in definitions:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": variable '"
                + name
                + "' has not been registered ("
                + "by _register_variable_type)"
            )
        if definitions[name].variable_type is cqltypes.VariableType.ANY:
            definitions[name].variable_type = variable_type
        if definitions[name].filter_type is cqltypes.FilterType.ANY:
            definitions[name].filter_type = filter_type
        if definitions[name].variable_type is not variable_type:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": variable '"
                + name
                + "' is a '"
                + definitions[name].variable_type.name.lower()
                + "' variable so cannot be set as a '"
                + variable_type.name.lower()
                + "' variable"
            )
        if definitions[name].filter_type is not filter_type:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": variable '"
                + name
                + "' is a '"
                + definitions[name].filter_type.__name__.lower()
                + "' filter so cannot be set as a '"
                + filter_type.__name__.lower()
                + "' filter"
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
            raise basenode.NodeError(
                self.__class__.__name__
                + ": cannot apply this operator to incomplete "
                + container.cursor.__class__.__name__
            )
        assert len(container.cursor.parent.children) > 0
        assert container.cursor is container.cursor.parent.children[-1]
        super().__init__(match_=match_, container=container)

    def _swap_tree_position(self, ancestor):
        """Make ancestor self's parent, and self parent of last child."""
        self.children.append(ancestor.children.pop(-1))
        ancestor.children.append(self)
        del self.parent.children[-1]
        self.parent = ancestor
        self.children[-1].parent = self
        self.container.cursor = self

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
            node.verify_children_and_set_filter_type(set_node_completed=True)


class InfixLeft(Infix):
    """Subclass of CQLObject for left associative infix operators."""

    # Class CQL implements implicit top-level '{}' block at present.
    def place_node_in_tree(self):
        """Adjust node hierarchy, assert cursor is parent."""
        parent = self.parent
        ancestor = parent.parent
        assert parent is self.container.cursor
        assert self.precedence is not None
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
                self._verify_and_set_filter_type(parent)
                return
            self._swap_tree_position(ancestor.parent.parent)
            self._verify_and_set_filter_type(parent)
            return
        # For 'if 1 + 2 then k' (legal nonsense left association in 'if').
        assert not ancestor.complete()
        if self.precedence.value < ancestor.precedence.value:
            self._swap_tree_position(ancestor.parent)
            self._verify_and_set_filter_type(parent)
            return
        if ancestor.precedence.value < self.precedence.value:
            self._swap_tree_position(ancestor)
            self._verify_and_set_filter_type(parent)
            return
        assert isinstance(ancestor, InfixLeft)
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
        assert parent is self.container.cursor
        assert self.precedence is not None
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
                self._verify_and_set_filter_type(parent)
                return
            self._swap_tree_position(ancestor.parent)
            self._verify_and_set_filter_type(parent)
            return
        # For 'if 1 > 2 then k' (legal nonsense right association in 'if').
        assert not ancestor.complete()
        if self.precedence.value < ancestor.precedence.value:
            self._swap_tree_position(ancestor.parent)
            self._verify_and_set_filter_type(parent)
            return
        if ancestor.precedence.value < self.precedence.value:
            self._swap_tree_position(ancestor)
            self._verify_and_set_filter_type(parent)
            return
        assert isinstance(ancestor, InfixRight)
        self._swap_tree_position(ancestor)
        self._verify_and_set_filter_type(parent)
        return


class MoveInfix(Infix):
    """Subclass of Infix for '--' and '[x]' symbol operators.

    The '--' and '[x]' filters may have either, or both, promotion and
    target conditions in addition to the LHS and RHS filters accepted by
    InfixLeft.

    The promotion condition is idicated by a trailing '=' clause, and the
    target condition is indicated by a trailing '(...)' clause.  The '='
    clause appears first if both are present.

    The filter_type of final filter in target condition becomes filter type
    of the MoveInfix instance.  The absence of target conditions cause the
    MoveInfix instance to be a logical filter.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Class CQL implements implicit top-level '{}' block at present.
    def place_node_in_tree(self):
        """Make prior sibling a child of self, assert cursor is parent."""
        parent = self.parent
        assert parent is self.container.cursor
        assert self.precedence is None
        self._swap_tree_position(parent.parent)
        self._verify_and_set_filter_type(parent)


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
    """Subclass of CQLObject for comparing String and Numeric filters."""

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


class ParameterArgument(CQLObject):
    """Subclass of CQLObject for parameters which take an argument."""

    _is_parameter = True
    # Keywords with unparenthesized argument take one child by default.
    _child_count = 1

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


class ModifyAssign(CQLObject):
    """Verify lhs variable can be assigned a numeric filter and modify."""

    def verify_children_and_set_filter_type(self, set_node_completed=False):
        """Delegate then adjust filter type if complete or full.

        This method should be called only from a place_node_in_tree method.

        """
        # pylint R0801 duplicate code.  Ignored.
        # See filters.AssignIf.verify_children_and_set_filter_type().
        if self.container.function_body_cursor is not None:
            return
        super().verify_children_and_set_filter_type(
            set_node_completed=set_node_completed
        )
        lhs = self.children[0]
        assert isinstance(lhs, VariableName)
        rhs = self.children[1]
        if (
            lhs.filter_type is cqltypes.FilterType.ANY
            and rhs.filter_type is cqltypes.FilterType.NUMERIC
        ):
            self.container.definitions[lhs.name].filter_type = rhs.filter_type
            return
        if (
            lhs.filter_type is rhs.filter_type
            and rhs.filter_type is cqltypes.FilterType.NUMERIC
        ):
            return
        # pylint R0801 duplicate code.  Ignored.
        # See filters.AssignIf.verify_children_and_set_filter_type().
        raise basenode.NodeError(
            self.__class__.__name__
            + ": cannot assign "
            + str(rhs.filter_type)
            + " to "
            + lhs.name
            + " filter of type "
            + str(lhs.filter_type)
        )
