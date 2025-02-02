# filters.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

# pylint C0302 too-many-lines.
# Think of good criteria for putting the definitions in one module rather
# than another.
# Perhaps the superclass signatures of the defined classes would do.
"""Chess Query Language (CQL) object class definitions.

This module defines the classes and functions which are values in the
tokenmap.class_from_token_name dict.  This includes classes for which
instances are returned by those values which are functions.  Classes
referencedd by these object are included too.

The classes represent filters and parameters to these filters.

Some keywords are also keywords for parameters of the cql(<parameters>)
statement.  See the parameters module for that usage.

"""
import re

from . import basenode
from . import constants
from . import cqltypes
from . import hhdb
from . import querycontainer
from . import cql
from . import structure

# Type designator string is limited to "QBRNKPAqbrnkpa_" characters.
_type_designator_string_re = re.compile(
    constants.PIECE_NAMES.join((r"^\"[", ']+"$'))
)

# Split a match on 'echo' filter pattern into components.
# The negative look-ahead after 'all' in pattern.ECHO is not needed.
_echo_filter_re = re.compile(
    r"echo(\s+quiet)?\s*\(\s*(\w+)\s+(\w+)\s*\)\s*(in\s+all)?\s*"
)

# Whitespace which terminates a 'path' filter.
_blank_line_re = re.compile(r"\n\s*\n$")

# This gives misleading information about variable name derivation but
# fits the pattern to detect 'echo' filters.
_echo_variable_re = re.compile(r"(?P<variable>.*)")

# Split a match on 'consecutivemoves' filter pattern into components.
# The elements.CONSECUTIVEMOVES pattern ensures at most one 'quiet' matches.
_consecutivemoves_filter_re = re.compile(
    r"consecutivemoves(?:\s+(quiet))?"
    + r"(?:\s+(\d+|[a-zA-Z0-9_$]+))?(?:\s+(\d+|[a-zA-Z0-9_$]+))?"
    + r"(?:\s+(quiet))?\s*\("
)

# This gives misleading information about range integer derivation but
# fits the pattern to detect 'consecutivemoves' filters.
_range_integer_re = re.compile(r"(?P<integer>.*)")

# This gives misleading information about variable name derivation but
# fits the pattern to detect 'function call' variable names.
_range_variable_re = _echo_variable_re


class MoveParameterImpliesSet(structure.ParameterArgument):
    """Set 'move' filter type to set for qualifying first parameters.

    This class is not a value in the cql.class_from_token_name dict but
    is refernced by classes and functions that are mentioned.
    """

    def place_node_in_tree(self):
        """Delegate then adjust parent filter type as required."""
        super().place_node_in_tree()
        parent = self.parent
        if not isinstance(parent, Move):
            return
        children = parent.children
        if len(children) == 1 and isinstance(
            self, (FromParameter, ToParameter, Capture)
        ):
            parent.filter_type = cqltypes.FilterType.SET
            return


class MoveParameterImpliesNumeric(structure.NoArgumentsParameter):
    """Set 'move' filter type to numeric if 'count' parameter present.

    This class is not a value in the cql.class_from_token_name dict but
    is refernced by classes and functions that are mentioned.
    """

    def place_node_in_tree(self):
        """Delegate then adjust parent filter type as required."""
        super().place_node_in_tree()
        parent = self.parent
        if not isinstance(parent, Move):
            return
        for child in parent.children:
            if isinstance(child, Count):
                parent.filter_type = cqltypes.FilterType.NUMERIC
                return


class IgnoreToEOL(structure.Complete):
    r"""Behaviour shared by tokens which ignore text to end of line.

    This class is not a value in the cql.class_from_token_name dict but
    is refernced by classes and functions that are mentioned.
    """

    def place_node_in_tree(self):
        r"""Override, move to whitespace, finish 'path' and '///' filters.

        'path' filter is completed if pattern match ends '\n\n' and a
        Path instance is first non-full filter in ancestor chain.

        '///' filter is completed if a CommentSymbol instance is first
        non-full filter in ancestor chain.

        The cursor becomes the first non-full node encountered in self's
        ancestor chain.

        The test is full, not complete, because an IgnoreToEOL instance
        will not complete any filters except a Path or CommentSymbol
        instance.

        """
        # The code involving cs_in_tree is added to cope with difference
        # between pins.cql example for CQL 6.2 and earlier versions.  It
        # is almost certainly not general enough.
        # The earlier versions use the 'comment' filter while 6.2 uses
        # the '///' filter.
        container = self.container
        container.whitespace.append(self.parent.children.pop())
        container.cursor = self.parent
        cs_in_tree = False
        node = self
        while node:
            if isinstance(node, CommentSymbol):
                cs_in_tree = True
                break
            node = node.parent
        node = self.parent
        while node and node.full():
            node = node.parent
        if not isinstance(node, (Path, CommentSymbol)):
            if cs_in_tree and isinstance(node, Pin):
                node = node.parent
            while node:
                node = node.parent
                if isinstance(node, CommentSymbol):
                    raise basenode.NodeError(
                        container.cursor.__class__.__name__
                        + ": cannot complete earlier '///' filter"
                    )
            self.parent = None
            return
        if (
            isinstance(node, Path)
            and _blank_line_re.match(self.match_.group()) is None
        ):
            self.parent = None
            return
        # Do the loop again, calling verify_children_and_set_filter_type()
        # this time, because the cursor will be moved.
        node = self.parent
        while node and node.full():
            node.verify_children_and_set_filter_type()
            node = node.parent
        assert isinstance(node, (Path, CommentSymbol))
        container.cursor = node.parent
        self.parent = None


class RightCompoundPlace(structure.CQLObject):
    """Place node for '{}' or '()' and similar and record as whitespace.

    The cursor is set to self's parent: the caller should verify parent.

    This class is not a value in the cql.class_from_token_name dict but
    is refernced by classes and functions that are mentioned.
    """

    def place_node_in_tree(self):
        r"""Override, move to whitespace and set cursor to parent.

        The superclass place_node_in_tree method assumes placement is done
        when an incomplete node is found which can be completed by this
        node.

        However '}' can complete multiple nodes, for example the nodes for
        '{' and 'path' in '{ ... path ... }' where the '\n\n' way of
        completing the 'path' filter is not present because 'path' is
        the last filter in the '{}' block.

        """
        while True:
            node = self.parent
            while node and node.complete():
                node.children[-1].parent = node.parent
                node.parent.children.append(node.children.pop())
                node.verify_children_and_set_filter_type(
                    set_node_completed=True
                )
                node = node.parent
            if not isinstance(node, Path):
                break
            node.children[-1].parent = node.parent
            node.parent.children.append(node.children.pop())
            node.verify_children_and_set_filter_type()
        container = self.container
        container.whitespace.append(self)
        del self.parent.children[-1]
        self.parent.completed = True
        container.cursor = self.parent
        # Class instances for tokens treated as whitespace have no parent.
        self.parent = None


class TransformFilterType(structure.CQLObject):
    """Determine filter type of transform filters.

    Presence of the count argument causes the transform to be a
    'numeric' filter.

    The filter type of the argument has these effects:
    'set' filters cause the transform to be a 'set' filter.
    'numeric' filters cause the transform to be a 'numeric' filter.
    'logical' filters cause the transform to be a 'logical' filter.
    'string' filters cause the transform to be a 'logical' filter.
    'position' filters cause the transform to be a 'logical' filter.

    This class is not a value in the cql.class_from_token_name dict but
    is refernced by classes and functions that are mentioned.
    """

    @property
    def filter_type(self):
        """Return filter type of last child if BraceLeft completed."""
        if self.completed:
            children = self.children
            for child in children[:-1]:
                if isinstance(child, Count):
                    return cqltypes.FilterType.NUMERIC
            if children[-1].filter_type is cqltypes.FilterType.SET:
                return cqltypes.FilterType.SET
            if children[-1].filter_type is cqltypes.FilterType.NUMERIC:
                return cqltypes.FilterType.NUMERIC
            return cqltypes.FilterType.LOGICAL
        return super().filter_type


class RepeatConstituent(structure.Complete):
    """Provide '+' and '*' regular expression operator shared behaviour.

    '+' and '*' operate on constituents in 'line' and 'path' filters.

    Parsing behaviour is identical: evaluation differs because lower limit
    is 0 and 1 respectively.  There are four classes representing these
    operations, with each having two character expressions.

    This class is not a value in the cql.class_from_token_name dict but
    is refernced by classes and functions that are mentioned.
    """

    # Probably best to define a class which is in constituent superclasses.
    # Something shared by ArrowForward, ArrowBackward, and 'path'
    # equivalents (not yet represented).
    def place_node_in_tree(self):
        """Override to place repeat operator in tree and set cursor to self.

        The repeat operator becomes a sibling of constituent.

        """
        node = self.parent
        while (
            node
            and node.complete()
            and not isinstance(node, (ArrowForward, ArrowBackward))
        ):
            node.children[-1].parent = node.parent
            node.parent.children.append(node.children.pop())
            node.verify_children_and_set_filter_type(set_node_completed=True)
            node = node.parent
        self.container.cursor = self


class TypeDesignator(structure.NoArgumentsFilter):
    """Represent one or more piece types with ASCII or unicode chess symbols.

    This class is used by the '--' filter.

    The '--' filter is a major part of the 'path' filter.
    """

    def place_node_in_tree(self):
        """Override, verify parent and set target interrupt to False.

        The parent node must be a MoveInfix instance.

        """
        self._raise_if_node_not_child_of_filters(
            self.match_.group(), structure.MoveInfix
        )
        self.container.target_move_interrupt = False


class BlockComment(structure.CQLObject):
    """Represent a '/*....*/' comment in a *.cql file."""

    _is_allowed_first_object_in_container = True

    def place_node_in_tree(self):
        """Override, move to whitespace and set cursor to parent."""
        container = self.container
        container.whitespace.append(self.parent.children.pop())
        container.cursor = self.parent
        self.parent = None


class LineComment(IgnoreToEOL):
    r"""Represent a '//.....\n' comment in a *.cql file.

    Note that '////....\n', and more leading '/' characters, is a LineComment
    but '///....\n' is a CommentSymbol (one of two CQL comment filters).
    """

    _is_allowed_first_object_in_container = True


class String(structure.NoArgumentsFilter):
    """Represent 'string' string filter."""

    _filter_type = cqltypes.FilterType.STRING


def is_documentation_parameter_accepted_by(node):
    """Return True if node accepts documentation parameter."""
    return isinstance(node, Sort)


class Documentation(structure.NoArgumentsParameter):
    """Represent 'documentation' parameter to 'sort' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_documentation_parameter_accepted_by(self.parent)


def is_implicit_search_parameter_accepted_by(node):
    """Return True if node accepts implicit_search parameter."""
    return isinstance(node, structure.ImplicitSearchFilter)


class ImplicitSearchParameter(structure.NoArgumentsParameter):
    """Represent 'implicit search' parameter to 'implicit search' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_implicit_search_parameter_accepted_by(self.parent)


def _is_type_designator_string(match_):
    """Return True if string represents a set of type designators."""
    return bool(_type_designator_string_re.match(match_.group()))


def string(match_=None, container=None):
    """Return a String or TypeDesignator instance or raise NodeError.

    NodeError is raised if a type designator string is expected, in
    '--' filter context, but the string contains non-piece name
    characters including 'A', 'a', and '_'.

    """
    if hhdb.is_hhdb_token_accepted_by(container.cursor):
        if match_.group() in hhdb.KEYWORD_STRINGS:
            return hhdb.HHDBToken(match_=match_, container=container)
    if isinstance(container.cursor, AssignPromotion):
        if _is_type_designator_string(match_):
            return TypeDesignator(match_=match_, container=container)
        raise basenode.NodeError(
            container.cursor.__class__.__name__
            + ": type designator string "
            + match_.group()
            + " contains characters other than '"
            + constants.PIECE_NAMES
            + "'"
        )
    if is_documentation_parameter_accepted_by(container.cursor):
        return Documentation(match_=match_, container=container)
    if is_implicit_search_parameter_accepted_by(container.cursor):
        return ImplicitSearchParameter(match_=match_, container=container)
    return String(match_=match_, container=container)


class EndOfLine(IgnoreToEOL):
    """Terminate '///' and 'path' filters, and record as whitespace."""

    _is_allowed_first_object_in_container = True


class WhiteSpace(structure.Complete):
    """Store whitespace to account for all text."""

    _is_allowed_first_object_in_container = True

    def place_node_in_tree(self):
        """Override, move self to whitespace and set cursor to parent."""
        container = self.container
        container.whitespace.append(self.parent.children.pop())
        container.cursor = self.parent
        self.parent = None


class ConstituentBraceRight(RightCompoundPlace):
    """Close ConstituentBraceLeft and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then verify cursor class is ConstituentBraceLeft."""
        super().place_node_in_tree()
        # '(' is allowed at the top level, as a container child.
        # Assume '(' is correct: ignore possibility '(' is inside
        # a 'cql ( ... )' clause, which might get fixed by a
        # separate parser for this clause.
        assert isinstance(self.container.cursor, ConstituentBraceLeft)


class BraceRight(RightCompoundPlace):
    """Close BraceLeft and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then verify cursor class is BraceLeft or Plus."""
        super().place_node_in_tree()
        # Path is terminated by '}' but the Plus should have been seen as
        # a RepeatPlus within a Path (itself terminated by '}') in
        # cql6-9-493-windows/examples/followpath.cql query.
        assert isinstance(self.container.cursor, (BraceLeft, Plus))


class FunctionBodyRight(RightCompoundPlace):
    """Close FunctionBodyLeft and record input tokens for replay."""

    def place_node_in_tree(self):
        """Delegate then decrement function_body_count and adjust cursor.

        The cursor is set to cursor's parent when function_body_count
        reaches zero.

        """
        super().place_node_in_tree()
        container = self.container
        assert isinstance(container.cursor, FunctionBodyLeft)
        assert container.function_body_count > 0
        container.function_body_count -= 1
        if container.function_body_count == 0:
            container.function_body_cursor = None
            container.cursor = container.cursor.parent
            del container.cursor.children[-1]
            container.cursor = container.cursor.parent


def brace_right(match_=None, container=None):
    """Return class instance for '}' in context or raise NodeError.

    BraceRight, FunctionBodyRight, and ConstituentBraceRight, are the
    relevant classes.

    """
    # Start at container.cursor and move up the parent chain while node
    # is complete.
    # The first node which is not complete should be a ConstituentBraceLeft,
    # FunctionBodyLeft or BraceLeft instance: NodeError is raised if not.
    # For example in the sequence '{...consecutivemoves(x y)}' a completed
    # ConsecutiveMoves instance will be at container.cursor and there may
    # be others in the parent chain depending on the detail of '...'.
    node = container.cursor
    while node:
        if not node.full():
            if isinstance(node, BraceLeft):
                if not node.children:
                    raise basenode.NodeError(
                        node.__class__.__name__
                        + ": '{' block must contain at least one filter"
                    )
                return BraceRight(match_=match_, container=container)
            if isinstance(node, ConstituentBraceLeft):
                if not node.children:
                    raise basenode.NodeError(
                        node.__class__.__name__
                        + ": '{' constituent block must contain"
                        + " at least one filter"
                    )
                return ConstituentBraceRight(
                    match_=match_, container=container
                )
            if isinstance(node, FunctionBodyLeft):
                return FunctionBodyRight(match_=match_, container=container)
            if isinstance(node, ParenthesisLeft):
                raise basenode.NodeError(
                    node.__class__.__name__
                    + ": cannot close a '(' parenthesized block with '}'"
                )
            if isinstance(
                node,
                (
                    ConstituentParenthesisLeft,
                    LineConstituentParenthesisLeft,
                ),
            ):
                raise basenode.NodeError(
                    node.__class__.__name__
                    + ": cannot close a '(' top level constituent with '}'"
                )
            if isinstance(node, BracketLeft):
                raise basenode.NodeError(
                    node.__class__.__name__
                    + ": cannot close a '[' string index with '}'"
                )
            if isinstance(node, structure.ParenthesizedArguments):
                raise basenode.NodeError(
                    node.__class__.__name__
                    + ": cannot close parenthesized arguments with '}'"
                )
        node = node.parent
    raise basenode.NodeError(
        "Unexpected " + str(node) + " found while trying to match a '}'"
    )


# This has same effect as PlusRepeat.
class WildcardPlus(RepeatConstituent):
    """Represent '{+}' repetition operation on a constituent filter.

    The 'path' and 'line' filters use constituent filters.

    The filter exists to clarify, and perhaps disambiguate, '+' as add or
    concatenation, and '+' as pattern repetition.
    """

    _precedence = cqltypes.Precedence.P20


# This has same effect as StarRepeat.
class WildcardStar(RepeatConstituent):
    """Represent '{*}' repetition operation on a constituent filter.

    The 'path' and 'line' filters use constituent filters.

    The filter exists to clarify, and perhaps disambiguate, '*' as
    multiplication, and '*' as pattern repetition.
    """

    _precedence = cqltypes.Precedence.P20


class RegexRepeat(RepeatConstituent):
    """Represent '{n,m}' repetition operation on a constituent filter.

    The 'path' and 'line' filters use constituent filters.

    The 6.0 syntax option '{2 3}' is not supported because it would allow
    '{2 3}' at 6.1 and later. '{2,3}' is supported at 6.0 but the examples
    use the '{2 3}' option.
    """


# The replaced complete() method returned False.
# Verify ConstituentBraceRight sets completed True.
class ConstituentBraceLeft(structure.BlockLeft):
    """Represent '{' top level constituent filter in 'path' filter."""

    def is_left_brace_or_parenthesis(self):
        """Override and return True."""
        return True


class FunctionBodyLeft(structure.BlockLeft):
    """Represent '{' body of function filter definition."""

    def place_node_in_tree(self):
        """Delegate then increment function_body_count.

        A superclass is expected to set cursor to self.

        """
        super().place_node_in_tree()
        self.container.function_body_count += 1


class BraceLeft(structure.BlockLeft):
    """Represent '{' compound filter of type determined by children.

    See ConstituentBraceLeft for top level constituents in 'path' filter.
    """

    @property
    def filter_type(self):
        """Return filter type of last child if BraceLeft completed."""
        if self.completed:
            return self.children[-1].filter_type
        return super().filter_type

    def is_left_brace_or_parenthesis(self):
        """Override and return True."""
        return True


def _is_brace_left_constituent(container):
    """Return True if '{' is at top level within a 'path' filter.

    Search ancestors for nearest of ConstituentBraceLeft, BraceLeft, and
    Path, instances.

    """
    node = container.cursor
    while node:
        if isinstance(node, (ConstituentBraceLeft, BraceLeft)):
            return False
        if isinstance(node, Path):
            return True
        node = node.parent
    return False


# Test for return ConstituentBraceLeft(...) alternative is not yet determined.
def brace_left(match_=None, container=None):
    """Return BraceLeft or ConstituentBraceLeft instance."""
    if isinstance(container.cursor, Function):
        return FunctionBodyLeft(match_=match_, container=container)
    if _is_brace_left_constituent(container):
        return ConstituentBraceLeft(match_=match_, container=container)
    return BraceLeft(match_=match_, container=container)


# The replaced place_node_in_tree() method does
# self._raise_if_node_not_child_of_filters("(", MoveInfix)
# before the super().place_node_in_tree() call.
class TargetParenthesisLeft(structure.BlockLeft):
    """Represent '(' target conditions in '--' or '[x]' filter."""


# The replaced complete() method returned False.
# Verify LineConstituentParenthesisRight sets completed True.
class LineConstituentParenthesisLeft(structure.BlockLeft):
    """Represent '(' top level chain constituent in 'line' filter.

    Separated from ConstituentParenthesisLeft to cope with the '-->' and
    '<--' symbols allowed in the 'line' filter.
    """

    def is_left_brace_or_parenthesis(self):
        """Override and return True."""
        return True


# The replaced complete() method returned False.
# Verify ConstituentParenthesisRight sets completed True.
class ConstituentParenthesisLeft(structure.BlockLeft):
    """Represent '(' top level chain constituent in 'path' filter."""

    def is_left_brace_or_parenthesis(self):
        """Override and return True."""
        return True


class ParenthesisLeft(structure.BlockLeft):
    """Represent '(' in various CQL statement contexts.

    See ConstituentParenthesisLeft for '(' as top level chain constituent.
    """

    @property
    def filter_type(self):
        """Return filter type of last child if ParenthesisLeft completed.

        There will be only one child in the completed filter.
        """
        if self.completed:
            assert len(self.children) == 1  # Remove if moved to BlockLeft.
            return self.children[-1].filter_type
        return super().filter_type

    def is_left_brace_or_parenthesis(self):
        """Override and return True."""
        return True


# There need to be three kinds of '(' apart from parenthesized arguments.
#   Precedence control.
#   Chain consituents in 'path' filter.  'path (check)'.
#   Target move conditions in '--' filter.  '--d4(check)'.
#   '(' for parenthesized arguments are caught in the filter pattern.
def parenthesis_left(match_=None, container=None):
    """Return appropriate ...ParenthesisLeft instance.

    Search ancestors for nearest of ConstituentBraceLeft, BraceLeft, Line,
    Path, and LineConstituentParenthesisLeft instances.

    Both '('s in '(<optional1>(...)<optional2>)' should return True by these
    tests, or both should return False, provided '<optional1>' does not have
    'line', 'path', or '{'.

    """
    if not container.target_move_interrupt:
        return TargetParenthesisLeft(match_=match_, container=container)
    node = container.cursor
    while node:
        if isinstance(node, (ConstituentBraceLeft, BraceLeft)):
            break
        if isinstance(node, Path):
            return ConstituentParenthesisLeft(
                match_=match_, container=container
            )
        if isinstance(node, Line):
            return LineConstituentParenthesisLeft(
                match_=match_, container=container
            )
        node = node.parent
    return ParenthesisLeft(match_=match_, container=container)


class LineConstituentParenthesisRight(RightCompoundPlace):
    """Close LineConstituentParenthesisLeft and record as whitespace.

    Separated from ConstituentParenthesisRight to cope with the '-->' and
    '<--' symbols allowed in the 'line' filter.
    """

    def place_node_in_tree(self):
        """Delegate then verify cursor class.

        The cursor must be a LineConstituentParenthesisLeft instance.

        """
        super().place_node_in_tree()
        # '(' is allowed at the top level, as a container child.
        # Assume '(' is correct: ignore possibility '(' is inside
        # a 'cql ( ... )' clause, which might get fixed by a
        # separate parser for this clause.
        assert isinstance(
            self.container.cursor, LineConstituentParenthesisLeft
        )


class ConstituentParenthesisRight(RightCompoundPlace):
    """Close ConstituentParenthesisLeft and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then verify cursor class is ConstituentParenthesisLeft."""
        super().place_node_in_tree()
        assert isinstance(self.container.cursor, ConstituentParenthesisLeft)


class ParenthesisRight(RightCompoundPlace):
    """Close ParenthesisLeft and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then verify cursor class is ParenthesisLeft."""
        super().place_node_in_tree()
        assert isinstance(self.container.cursor, ParenthesisLeft)


class ParenthesizedArgumentsEnd(RightCompoundPlace):
    """Close ParenthesizedArguments subclass and record as whitespace.

    ParenthesizedArgumentsEnd should not be instatiated itself.
    """

    def place_node_in_tree(self):
        """Delegate then verify cursor class is ParenthesizedArguments.

        A ParenthesizedArgumentsEnd instance marks the end of arguments
        to a subclass of ParenthesizedArguments.

        """
        super().place_node_in_tree()
        assert isinstance(
            self.container.cursor, structure.ParenthesizedArguments
        )


class TargetConditionsEnd(structure.CQLObject):
    """Close TargetParenthesisLeft subclass and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then set cursor to parent and collect ')' as whitespace.

        A TargetConditionsEnd instance marks the end of conditions on the
        target of a subclass of MoveInfix.  The filter type of associated
        MoveInfix instance becomes filter type of final filter in target
        conditions.

        """
        super().place_node_in_tree()
        container = self.container
        container.whitespace.append(self)
        children = self.parent.children
        del children[-1]
        parent_parent = self.parent.parent
        if isinstance(parent_parent, structure.MoveInfix):
            parent_parent.filter_type = children[-1].filter_type
        self.parent.completed = True
        container.cursor = self.parent


def is_find_backward_parameter_accepted_by(node):
    """Return True if node accepts find_backward parameter."""
    return isinstance(node, Find)


class FindBackward(structure.NoArgumentsParameter):
    """Represent '<--' parameter to 'find' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_find_backward_parameter_accepted_by(self.parent)


def is_line_arrow_parameter_accepted_by(node):
    """Return True if node accepts a line_arrow parameter."""
    return isinstance(node, (Line, LineConstituentParenthesisLeft))


class LineArrow(structure.CQLObject):
    """Represent '<--' and '-->' shared behaviour in 'line' filter.

    This class is not a value, nor returned by a function that is a value,
    in cql.class_from_token_name dict.  But it is defined in filters,
    not structure, module because it refers to classes which are defined
    in filters module.
    """

    def place_node_in_tree(self):
        """Move self to nearest ancestor which is a 'line' node.

        Caller should call self.raise_if_name_parameter_not_for_filters
        to raise NodeError if the parent is not a Line instance on exit.

        """
        container = self.container
        node = container.cursor
        while True:
            if node is None:
                break
            if (
                isinstance(
                    node,
                    (
                        BraceLeft,
                        ConstituentBraceLeft,
                        ParenthesisLeft,
                        ConstituentParenthesisLeft,
                        LineConstituentParenthesisLeft,
                        structure.ParenthesizedArguments,
                    ),
                )
                and not node.full()
            ):
                break
            if isinstance(node, Line):
                break
            # Is this ok for path filter?
            # Why is test against complete(), like in superclass, incorrect?
            if not node.full():
                break
            node.children[-1].parent = node.parent
            node.parent.children.append(node.children.pop())
            node.verify_children_and_set_filter_type(set_node_completed=True)
            node = node.parent


class ArrowBackward(LineArrow, structure.Argument):
    """Represent '<--' keyword for 'line' filter.  Deprecated at 6.2.

    '<--' is not called a parameter in CQL documentation at 6.1 but is
    processed here as a parameter which takes one mandatory argument called
    a constituent.
    """

    _is_parameter = True
    _precedence = cqltypes.Precedence.P10

    def place_node_in_tree(self):
        """Delegate then verify '<--' parameter and set cursor to self."""
        super().place_node_in_tree()
        self.raise_if_name_parameter_not_for_filters()
        if len(self.parent.children) > 1:
            if isinstance(self.parent.children[-2], ArrowForward):
                raise basenode.NodeError(
                    "'<--'"
                    + ": cannot be mixed with existing "
                    + "'-->'"
                    + " parameters"
                )
        self.container.cursor = self

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_line_arrow_parameter_accepted_by(self.parent)


def arrow_backward(match_=None, container=None):
    """Return FindBackward or ArrowBackward instance."""
    if is_find_backward_parameter_accepted_by(container.cursor):
        return FindBackward(match_=match_, container=container)
    return ArrowBackward(match_=match_, container=container)


class ArrowForward(LineArrow, structure.Argument):
    """Represent '-->' keyword for 'line' filter.  Deprecated at 6.2.

    '-->' is not called a parameter in CQL documentation at 6.1 but is
    processed here as a parameter which takes one mandatory argument called
    a constituent.
    """

    _is_parameter = True
    _precedence = cqltypes.Precedence.P10

    def place_node_in_tree(self):
        """Delegate then verify '-->' parameter and set cursor to self."""
        super().place_node_in_tree()
        self.raise_if_name_parameter_not_for_filters()
        if len(self.parent.children) > 1:
            if isinstance(self.parent.children[-2], ArrowBackward):
                raise basenode.NodeError(
                    "'-->'"
                    + ": cannot be mixed with existing "
                    + "'<--'"
                    + " parameters"
                )
        self.container.cursor = self

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_line_arrow_parameter_accepted_by(self.parent)


class AfterEq(structure.ComparePosition, structure.InfixRight):
    """Represent '[>=]' (≽) position filter."""

    _precedence = cqltypes.Precedence.P30  # From 'descendant'.


class AfterNE(structure.ComparePosition, structure.InfixRight):
    """Represent '[>]' (≻) position filter."""

    _precedence = cqltypes.Precedence.P30  # From 'descendant'


class BeforeEq(structure.ComparePosition, structure.InfixRight):
    """Represent '[<=]' (≼) position filter."""

    _precedence = cqltypes.Precedence.P30  # From 'ancestor'


class BeforeNE(structure.ComparePosition, structure.InfixRight):
    """Represent '[<]' (≺) position filter."""

    _precedence = cqltypes.Precedence.P30  # from 'ancestor'.


class CapturesLR(structure.MoveInfix):
    """Represent '[x]' ('×') filter like F[x]G.

    F and G are set filters where whitespace between them and '[x]' matters.

    CapturesLR is an infix operator with neither LHS nor RHS implicit: F is
    the LHS and G is the RHS.
    """

    def place_node_in_tree(self):
        """Delegate then set target interrupt to False."""
        super().place_node_in_tree()
        self.container.target_move_interrupt = False


class CapturesL(structure.MoveInfix):
    """Represent '[x]' ('×') filter like F[x] G.

    F and G are set filters where whitespace between them and '[x]' matters.

    CapturesL is an infix operator with only RHS implicit: F is the LHS and
    G is not the RHS.  The RHS is the '.' filter, equivalent to 'a-h1-8'.
    """

    def place_node_in_tree(self):
        """Delegate then append the implied '.' filter."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        AnySquare(match_=self.match_, container=container).place_node_in_tree()
        container.target_move_interrupt = False


class CapturesR(structure.MoveInfix):
    """Represent '[x]' ('×') filter like F [x]G.

    F and G are set filters where whitespace between them and '[x]' matters.

    CapturesR is an infix operator with only LHS implicit: F is not the LHS
    and G is the RHS.  The LHS is the '.' filter, equivalent to 'a-h1-8'.
    """

    def __init__(self, match_=None, container=None):
        """Create the implied '.' filter then delegate."""
        AnySquare(match_=match_, container=container).place_node_in_tree()
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        """Delegate then set cursor to self and target interrupt to False."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        container.target_move_interrupt = False


class Captures(structure.MoveInfix):
    """Represent '[x]' ('×') filter like F [x] G.

    F and G are set filters where whitespace between them and '[x]' matters.
    Captures is an infix operator with both LHS and RHS implicit: F is not
    the LHS and G is not the RHS.  Both LHS and RHS are the '.' filter,
    equivalent to 'a-h1-8'.
    """

    def __init__(self, match_=None, container=None):
        """Create the implied '.' filter then delegate."""
        AnySquare(match_=match_, container=container).place_node_in_tree()
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        """Delegate then append the implied '.' filter."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        AnySquare(match_=self.match_, container=container).place_node_in_tree()
        container.target_move_interrupt = False


class CommentSymbol(structure.BlockLeft):
    """Represent '///' logical filter.

    CommentSymbol does not follow Comment and CommentParentheses in having
    a parameter version for interaction with Move because the '///' filter
    is introduced at CQL-6.2 and 'move' filter is deprecated at CQL-6.2.

    The '///' filter is terminated by a newline.  This is similar to the
    'path' filter which is terminated by a blank line.
    """

    _filter_type = cqltypes.FilterType.LOGICAL


class AttackArrow(structure.MoveInfix):
    """Represent '->' (→) set filter."""

    _filter_type = cqltypes.FilterType.SET


class AttackedArrow(structure.MoveInfix):
    """Represent '<-' (←) set filter."""

    _filter_type = cqltypes.FilterType.SET


class SingleMoveLR(structure.MoveInfix):
    """Represent '--' ('―') filter like F--G.

    F and G are set filters where whitespace between them and '--' matters.

    Targets are within '()' like 'F--G(check)' for example.

    SingleMoveLR is an infix operator with neither LHS nor RHS implicit: F
    is the LHS and G is the RHS.
    """

    def place_node_in_tree(self):
        """Delegate then set target interrupt to False."""
        super().place_node_in_tree()
        self.container.target_move_interrupt = False


class SingleMoveL(structure.MoveInfix):
    """Represent '--' ('―') filter like F-- G.

    F and G are set filters where whitespace between them and '--' matters.

    Targets are within '()' like 'F--(check) G' for example.

    SingleMoveL is an infix operator with only RHS implicit: F is the LHS
    and G is not the RHS.  The RHS is the '.' filter, equivalent to
    'a-h1-8'.
    """

    def place_node_in_tree(self):
        """Delegate then append the implied '.' filter."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        AnySquare(match_=self.match_, container=container).place_node_in_tree()
        container.target_move_interrupt = False


class SingleMoveR(structure.MoveInfix):
    """Represent '--' ('―') filter like F --G.

    F and G are set filters where whitespace between them and '--' matters.

    Targets are within '()' like 'F --G(check)' for example.

    SingleMoveR is an infix operator with only LHS implicit: F is not the
    LHS and G is the RHS.  The LHS is the '.' filter, equivalent to 'a-h1-8'.
    """

    def __init__(self, match_=None, container=None):
        """Create the implied '.' filter then delegate."""
        AnySquare(match_=match_, container=container).place_node_in_tree()
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        """Delegate then set cursor to self and target interrupt to False."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        container.target_move_interrupt = False


class SingleMove(structure.MoveInfix):
    """Represent '--' ('―') filter like F -- G.

    F and G are set filters where whitespace between them and '--' matters.

    Targets are within '()' like 'F --(check) G' for example.

    SingleMove is an infix operator with both LHS and RHS implicit: F is not
    the LHS and G is not the RHS.  Both LHS and RHS are the '.' filter,
    equivalent to 'a-h1-8'.
    """

    def __init__(self, match_=None, container=None):
        """Create the implied '.' filter then delegate."""
        AnySquare(match_=match_, container=container).place_node_in_tree()
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        """Delegate then append the implied '.' filter."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        AnySquare(match_=self.match_, container=container).place_node_in_tree()
        container.target_move_interrupt = False


# RegexMatch, RegexCapturedGroup, and RegexCapturedGroupIndex,
# deduced from query:
# gamenumber==1
# initial
# v="footballboot"~~"oo"
# ///\0
# ///\-0
# ///v+"w"


class RegexMatch(structure.InfixLeft):
    """Represent the '~~' string filter.

    Both arguments of '~~' are quoted strings.
    """

    _filter_type = cqltypes.FilterType.STRING
    _precedence = cqltypes.Precedence.P220


class RegexCapturedGroup(structure.CQLObject):
    r"""Represent the variable named r'\\\d+' string filter.

    An example of the variable name is '\0'.
    """

    _filter_type = cqltypes.FilterType.STRING


class RegexCapturedGroupIndex(structure.CQLObject):
    r"""Represent the index of variable named r'\\-\d+' string filter.

    An example of the index variable name is '\-0'.
    """

    _filter_type = cqltypes.FilterType.NUMERIC


class EmptySquares(structure.CQLObject):
    """Represent '[]' set filter."""

    _filter_type = cqltypes.FilterType.SET


class LE(structure.Compare, structure.InfixRight):
    """Represent '<=' ('≤') numeric filter or string filter."""

    _precedence = cqltypes.Precedence.P80


class GE(structure.Compare, structure.InfixRight):
    """Represent '>=' ('≥') numeric filter or string filter."""

    _precedence = cqltypes.Precedence.P80


class Eq(structure.CompareSet, structure.Compare, structure.InfixRight):
    """Represent '==' numeric filter or string filter."""

    _precedence = cqltypes.Precedence.P80


class NE(structure.CompareSet, structure.Compare, structure.InfixRight):
    """Represent '!=' ('≠') numeric filter or string filter."""

    _precedence = cqltypes.Precedence.P80


class AssignIf(structure.InfixLeft):
    """Represent '=?' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL

    # CQL does not include '=?' in precedence table (with '+=' for example)
    # but CQLi gives it same precedence as these.  Follow CQLi and assign
    # precedence of 90.
    _precedence = cqltypes.Precedence.P90

    def verify_children_and_set_filter_type(self, set_node_completed=False):
        """Delegate then adjust filter type if complete or full.

        This method should be called only from a place_node_in_tree method.

        """
        # pylint R0801 duplicate code.  Ignored.
        # See structure.ModifyAssign.verify_children_and_set_filter_type().
        if self.container.function_body_cursor is not None:
            return
        super().verify_children_and_set_filter_type(
            set_node_completed=set_node_completed
        )
        lhs = self.children[0]
        assert isinstance(lhs, structure.VariableName)
        rhs = self.children[1]
        if (
            lhs.filter_type is cqltypes.FilterType.ANY
            and rhs.filter_type is cqltypes.FilterType.SET
        ):
            self.container.definitions[lhs.name].filter_type = rhs.filter_type
            return
        if (
            lhs.filter_type is rhs.filter_type
            and rhs.filter_type is cqltypes.FilterType.SET
        ):
            return
        # pylint R0801 duplicate code.  Ignored.
        # See structure.ModifyAssign.verify_children_and_set_filter_type().
        raise basenode.NodeError(
            self.__class__.__name__
            + ": cannot assign "
            + str(rhs.filter_type)
            + " to "
            + lhs.name
            + " filter of type "
            + str(lhs.filter_type)
        )


class AssignPlus(structure.InfixLeft):
    """Represent '+=' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P90

    def verify_children_and_set_filter_type(self, set_node_completed=False):
        """Delegate then adjust filter type if complete or full.

        This method should be called only from a place_node_in_tree method.

        """
        if self.container.function_body_cursor is not None:
            return
        super().verify_children_and_set_filter_type(
            set_node_completed=set_node_completed
        )
        lhs = self.children[0]
        assert isinstance(lhs, structure.VariableName)
        rhs = self.children[1]
        if lhs.filter_type is cqltypes.FilterType.ANY and (
            rhs.filter_type is cqltypes.FilterType.NUMERIC
            or rhs.filter_type is cqltypes.FilterType.STRING
        ):
            self.container.definitions[lhs.name].filter_type = rhs.filter_type
            return
        if lhs.filter_type is rhs.filter_type and (
            rhs.filter_type is cqltypes.FilterType.NUMERIC
            or rhs.filter_type is cqltypes.FilterType.STRING
        ):
            return
        raise basenode.NodeError(
            self.__class__.__name__
            + ": cannot assign "
            + str(rhs.filter_type)
            + " to "
            + lhs.name
            + " filter of type "
            + str(lhs.filter_type)
        )


class AssignMinus(structure.ModifyAssign, structure.InfixLeft):
    """Represent '-=' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P90


class AssignDivide(structure.ModifyAssign, structure.InfixLeft):
    """Represent '/=' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P90


class AssignMultiply(structure.ModifyAssign, structure.InfixLeft):
    """Represent '*=' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P90


class AssignModulus(structure.ModifyAssign, structure.InfixLeft):
    """Represent '%=' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P90


class Abs(structure.Argument):
    """Represent 'abs' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P90


def is_all_parameter_accepted_by(node):
    """Return True if node accepts all parameter.

    The patterns for 'piece' and 'square' filters catch the 'all'
    parameter.

    """
    return isinstance(node, Find)


class All(structure.NoArgumentsParameter):
    """Represent 'all' parameter to various filters.

    The filters are:
        find
        piece ('all' caught in PIECE pattern)
        square ('all' caught in SQUARE pattern)
    """

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_all_parameter_accepted_by(self.parent)

    def place_node_in_tree(self):
        """Delegate then adjust parent filter type for 'find' filter."""
        super().place_node_in_tree()
        parent = self.parent
        # These filter type adjustments are best done when completing
        # the parent filter.
        if isinstance(parent, Find):
            parent.filter_type = cqltypes.FilterType.NUMERIC
            return


class Ancestor(structure.ParenthesizedArguments):
    """Represent 'ancestor' numeric filter.

    'ancestor' is deprecated: the "\u227a" ('[<]') filter should be used
    instead.  It is called 'before_ne' here.
    """

    # Deduced from '-parse' of following query,
    # v=ancestor(position 1 position 2)
    # w="er"
    # x=position 1
    # because v is a numeric variable
    # although the 'v=..' clause gets a CQL internal error on running
    # the query.
    # Note that '-parse' of
    # y=(position 1 [<] position 2)
    # with [<] replacing the deprecated ancestor filter
    # gives y as a position variable.
    # Parse of
    # v=ancestor(position 1 position 2)
    # in cqli-1.0.3 gives error
    # Right operand ... must be a numeric, position, string, or set value
    # suggesting 'ancestor' should be a logical filter.
    # 'descendant' has similar behaviour.
    _filter_type = cqltypes.FilterType.NUMERIC


class And(structure.InfixLeft):
    """Represent 'and' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P50


class AnyDirection(structure.Argument):
    """Represent 'anydirection' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class AnyDirectionParameter(structure.DirectionParameter):
    """Represent 'anydirection' transform filter direction parameter."""


def anydirection(match_=None, container=None):
    """Return Up or UpParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return AnyDirectionParameter(match_=match_, container=container)
    return AnyDirection(match_=match_, container=container)


class ASCII(structure.Argument):
    """Represent 'ascii' numeric filter or string filter."""

    _filter_type = cqltypes.FilterType.NUMERIC | cqltypes.FilterType.STRING
    _precedence = cqltypes.Precedence.P100


class Assert(structure.Argument):
    """Represent 'assert' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


# Prefix to variable, 'atomic variables' in Table of Filters.
class Atomic(structure.CQLObject):
    """Represent variable with 'atomic' prefix."""

    def place_node_in_tree(self):
        """Delegate then verify variable name is not a CQL keyword."""
        super().place_node_in_tree()
        cqltypes.variable(self.match_.groupdict()["atomic"], self.container)


class AttackedBy(structure.InfixLeft):
    """Represent 'attackedby' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P190


class Attacks(structure.InfixLeft):
    """Represent 'attacks' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P190


class Between(structure.ParenthesizedArguments):
    """Represent 'between' set filter."""

    _filter_type = cqltypes.FilterType.SET
    # Between is only subclass of ParenthesizedArguments which overrides
    # _child_count: is it necessary?
    _child_count = 2
    # Both CQL-6.2 and CQLi-1.0.3 allocate a precedence, with CQLi
    # commenting 'each argument of the between filter'.
    # I do not see why precedence is relevant to 'between'.
    # 'between(k r)' is complete: 'between(k r) <something>' in the sense
    # of 'shift k', where 'shift' is not complete, is nonsense.
    # Unless 'between' is a unary operator which accepts only a '(..)'
    # argument.
    # (later) When fixing problem getting '>=' correct in bristol-universal
    # it seemed 'between (Back Front) >= 3' and 'between (Back Front >= 3)'
    # are distinguished by the notion of a completed filter used in
    # InfixRight.place_node_in_tree() method.  The tree structure below
    # 'sort' here is similar to that in 'cqli -parse ...'.
    # _precedence = cqltypes.Precedence.P150


# 'black' is defined as a numeric filter with value -1 on the 'black.html'
# page referenced from the table of filters at 'filtertable.html'.
# 'black' is referred to as a 'built-in tag query filter' on the
# 'tagqueryfilters.html' page, but it seems be correspond to 'player black'
# in the table of filters.
# 'black' is not described as having an 'implicit search parameter' in the
# table of filters.
# On the 'implicitsearch.html' page it is called 'black', but the example
# 'player white' suggests it is describing the 'player black' filter from
# the table of filters.
class Black(structure.CQLObject):
    """Represent 'black' numeric filter with value -1."""

    _filter_type = cqltypes.FilterType.NUMERIC


class BTM(structure.NoArgumentsFilter):
    """Represent 'btm' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Capture(MoveParameterImpliesSet):
    """Represent 'capture' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


class Castle(structure.NoArgumentsFilter):
    """Represent 'castle' logical filter or parameter to 'move' filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class CastleParameter(structure.NoArgumentsParameter):
    """Represent 'castle' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


def castle(match_=None, container=None):
    """Return Castle or CastleParameter instance.

    'castle' may be either a set filter or a parameter.  CQL does not
    treat the second 'castle' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if isinstance(node, Move):
            return CastleParameter(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return Castle(match_=match_, container=container)


class Check(structure.NoArgumentsFilter):
    """Represent 'check' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class ChildParentheses(structure.ParenthesizedArguments):
    """Represent 'child' position filter with argument."""

    _filter_type = cqltypes.FilterType.POSITION


class Child(structure.NoArgumentsFilter):
    """Represent 'child' position filter without argument."""

    _filter_type = cqltypes.FilterType.POSITION


class ColorType(structure.Argument):
    """Represent 'colortype' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P150


def is_comment_parameter_accepted_by(node):
    """Return True if node accepts comment parameter."""
    return isinstance(node, Move)


class Comment(structure.Argument):
    """Represent 'comment' logical filter.

    A 'comment' filter immediately after a 'move' filter is parsed as a
    parameter of the 'move' filter but is the last parameter.

    The examples-ascii/turton-old.cql query combines 'line', 'move', and
    'comment', filters demonstrates why: the 'line' filter makes no
    allowance for 'comment' filters after constituent filters before the
    next '-->' or '<--'.
    """

    _filter_type = cqltypes.FilterType.LOGICAL


class CommentParameter(structure.Argument):
    """Represent 'comment' filter immediately after 'move' filter."""

    _is_parameter = True
    _filter_type = cqltypes.FilterType.LOGICAL

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_comment_parameter_accepted_by(self.parent)


def comment(match_=None, container=None):
    """Return Comment or CommentParameter instance.

    CommentParameter is returned if parent is 'move' filter.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if is_comment_parameter_accepted_by(node):
            return CommentParameter(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return Comment(match_=match_, container=container)


class CommentParentheses(structure.ParenthesizedArguments):
    """Represent 'comment' logical filter.

    A 'comment' filter immediately after a 'move' filter is parsed as a
    parameter of the 'move' filter but is the last parameter.

    The examples-ascii/turton-old.cql query combines 'line', 'move', and
    'comment', filters demonstrates why: the 'line' filter makes no
    allowance for 'comment' filters after constituent filters before the
    next '-->' or '<--'.
    """

    _filter_type = cqltypes.FilterType.LOGICAL


class CommentParenthesesParameter(structure.ParenthesizedArguments):
    """Represent 'comment' filter immediately after 'move' filter."""

    _is_parameter = True
    _filter_type = cqltypes.FilterType.LOGICAL

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_comment_parameter_accepted_by(self.parent)


def comment_parentheses(match_=None, container=None):
    """Return CommentParentheses or CommentParenthesesParameter instance.

    CommentParenthesesParameter is returned if parent is 'move' filter.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if is_comment_parameter_accepted_by(node):
            return CommentParenthesesParameter(
                match_=match_, container=container
            )
        if not node.full():
            break
        node = node.parent
    return CommentParentheses(match_=match_, container=container)


class ConnectedPawns(structure.NoArgumentsFilter):
    """Represent 'connectedpawns' set filter."""

    _filter_type = cqltypes.FilterType.SET


class ConsecutiveMoves(structure.ParenthesizedArguments):
    """Represent 'consecutivemoves' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC

    def place_node_in_tree(self):
        """Delegate then set cursor to self and append parameter instances."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        groups = _consecutivemoves_filter_re.match(
            self.match_.group()
        ).groups()
        if groups[0]:
            Quiet(match_=self.match_, container=container).place_node_in_tree()
            container.cursor = self
        for count in (1, 2):
            if not groups[count]:
                continue
            if groups[count].isdigit():
                range_item = RangeInteger(
                    match_=_range_integer_re.match(groups[count]),
                    container=container,
                )
            else:
                range_item = RangeVariable(
                    match_=_range_variable_re.match(groups[count]),
                    container=container,
                )
            range_item.place_node_in_tree()
            container.cursor = self
        if groups[3]:
            Quiet(match_=self.match_, container=container).place_node_in_tree()
            container.cursor = self


def is_count_parameter_accepted_by(node):
    """Return True if node accepts count parameter."""
    return isinstance(
        node,
        (
            Flip,
            FlipColor,
            FlipHorizontal,
            FlipVertical,
            Rotate45,
            Rotate90,
            Shift,
            ShiftHorizontal,
            ShiftVertical,
            Move,
            Find,
        ),
    )


class Count(structure.NoArgumentsParameter):
    """Represent 'count' parameter to various filters.

    The word 'count' usually appears in the parameter column of 'table of
    filters' for filters which accept the 'count' parameter.  It does not
    appear for deprecated filters, where the filter documentation or an
    earlier version of the table must be examined.

    The 'count' parameter can only be present in the 'move' filter if
    either the 'legal' or the 'pseudoleagal' is also present.
    """

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_count_parameter_accepted_by(self.parent)

    def place_node_in_tree(self):
        """Delegate then adjust parent filter type for affected filters.

        The 'move' and 'line' filters may change their filter type.

        """
        super().place_node_in_tree()
        parent = self.parent
        # These filter type adjustments are best done when completing
        # the parent filter.
        if isinstance(parent, Find):
            parent.filter_type = cqltypes.FilterType.NUMERIC
            return
        if not isinstance(parent, Move):
            return
        for child in parent.children:
            if isinstance(child, (LegalParameter, PseudolegalParameter)):
                parent.filter_type = cqltypes.FilterType.NUMERIC
                return


class CountMoves(structure.CQLObject):
    """Represent 'countmoves' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class CurrentMove(structure.CQLObject):
    """Represent 'currentmove' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class CurrentPosition(structure.NoArgumentsFilter):
    """Represent 'currentposition' position filter."""

    _filter_type = cqltypes.FilterType.POSITION


class CurrentTransform(structure.NoArgumentsFilter):
    """Represent 'currenttransform' string filter."""

    _filter_type = cqltypes.FilterType.STRING


class Dark(structure.Argument):
    """Represent 'dark' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


# Refers to an 'implicit search parameter' in table of filters.
# In tagqueryfilters.html it is referred to as an 'implicit search filter'.
class Date(structure.ImplicitSearchFilter):
    """Represent 'date' string filter."""

    _filter_type = cqltypes.FilterType.STRING


class Depth(structure.NoArgumentsFilter):
    """Represent 'depth' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class Descendant(structure.ParenthesizedArguments):
    """Represent 'descendant' numeric filter."""

    # Deduced from '-parse' of following query,
    # v=descendant(position 2 position 1)
    # w="er"
    # x=position 2
    # because v is a numeric variable
    # although the 'v=..' clause gets a CQL internal error on running
    # the query.
    # Note that '-parse' of
    # y=(position 2 [>] position 1)
    # with [>] replacing the deprecated descendant filter
    # gives y as a position variable.
    # Parse of
    # v=descendant(position 2 position 1)
    # in cqli-1.0.3 gives error
    # Right operand ... must be a numeric, position, string, or set value
    # suggesting 'descendant' should be a logical filter.
    # 'ancestor' has similar behaviour.
    _filter_type = cqltypes.FilterType.NUMERIC

    # See Ancestor.
    # Treated as 'descendant (' not 'descendant' then '(' and ... ')'.
    # _precedence = cqltypes.Precedence.P30


class Diagonal(structure.Argument):
    """Represent 'diagonal' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class DiagonalParameter(structure.DirectionParameter):
    """Represent 'diagonal' transform filter direction parameter."""


def diagonal(match_=None, container=None):
    """Return Diagonal or DiagonalParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return DiagonalParameter(match_=match_, container=container)
    return Diagonal(match_=match_, container=container)


class Dictionary(structure.Complete, structure.Name):
    """Represent 'dictionary' logical filter, and the 'local' variant.

    All keys in a dictionary must be one type, and all values too.  But
    the key and value types in a dictionary can be different.

    Thus 'a2' and 'b1-8' are allowed as keys but accessing the dictionary
    element by 'D[a2]' may pose problems because '[a2]' is normally a piece
    designator and, 'D[ a2 ]' is confusing because of the whitespace, and
    'b1-8' has the '-' character not allowed in variable names.

    However 'a2' does indicate the key type is set filter.
    """

    _filter_type = cqltypes.FilterType.LOGICAL
    _key_type = None
    _value_type = None

    def __init__(self, match_=None, container=None):
        """Delegate then register the dictionary name."""
        super().__init__(match_=match_, container=container)

        # 'dictionary <name>' or '<name>' caught by VARIABLE pattern when
        # <name> already defined as a dictionary.
        groupdict = match_.groupdict()
        self.name = groupdict["dictionary"] or groupdict["variable"]

        self._raise_if_name_invalid(cqltypes.Dictionary)
        if self.name not in container.definitions:
            cqltypes.dictionary(self.name, container)
        self._raise_if_already_defined(
            cqltypes.DefinitionType.ANY ^ cqltypes.DefinitionType.DICTIONARY,
            cqltypes.DefinitionType.DICTIONARY,
        )

    @property
    def key_type(self):
        """Return the type of the dictionary's keys."""
        return self._key_type

    @property
    def value_type(self):
        """Return the type of the dictionary's values."""
        return self._value_type

    def place_node_in_tree(self):
        """Delegate then verify variable and set cursor to self.

        The variable name must not be a CQL keyword.

        """
        super().place_node_in_tree()
        container = self.container
        cqltypes.dictionary(
            self.match_.groupdict()["dictionary"]
            or self.match_.groupdict()["variable"],
            container,
        )
        # This test implies either Echo or Variable detection needs to be
        # changed somehow?  What about Function too?
        if isinstance(self.parent, ParenthesisLeft):
            if isinstance(self.parent.parent, Echo):
                return
        container.cursor = self
        return


class Distance(structure.ParenthesizedArguments):
    """Represent 'distance' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    # See Ancestor too.
    # Treated as 'distance (' not 'distance' then '(' and ... ')'.
    # _precedence = cqltypes.Precedence.P30


class DoubledPawns(structure.NoArgumentsFilter):
    """Represent 'doubledpawns' set filter."""

    _filter_type = cqltypes.FilterType.SET


class Down(structure.Argument):
    """Represent 'down' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class DownParameter(structure.DirectionParameter):
    """Represent 'down' transform filter direction parameter."""


def down(match_=None, container=None):
    """Return Down or DownParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return DownParameter(match_=match_, container=container)
    return Down(match_=match_, container=container)


# The 'echo' documentation page describes the filter as:
# 'echo (source_var target_var) body_filter'
# but the 'echo' entry in table of filters misleadingly describes the
# parameters as 'in', 'all', and 'echo quiet' and the arguments as
# '(variable variable)' and does not mention the 'body filter' as the
# argument at all.
# The 'echo' documentation page mentions the optional phrases 'quiet'
# and 'in all' which may appear in the filter like:
# 'echo quiet (source_var target_var) in all body_filter'.
# The pattern for the 'echo' filter catches 'echo ... all'.
class Echo(structure.Argument):
    """Represent 'echo' filter of all types.

    The filter type of the argument has these effects:
    'set' filters cause 'echo' to be a 'logical' filter.
    'numeric' filters cause 'echo' to be a 'numeric' filter.
    'logical' filters cause 'echo' to be a 'logical' filter.
    'string' filters cause 'echo' to be a 'logical' filter.
    'position' filters cause 'echo' to be a 'logical' filter.
    """

    _precedence = cqltypes.Precedence.P30

    @property
    def filter_type(self):
        """Return filter type of last child if BraceLeft completed."""
        if self.completed:
            if self.children[-1].filter_type is cqltypes.FilterType.NUMERIC:
                return cqltypes.FilterType.NUMERIC
            return cqltypes.FilterType.LOGICAL
        return super().filter_type

    def place_node_in_tree(self):
        """Delegate then append parameters with self as cursor."""
        super().place_node_in_tree()
        container = self.container
        groups = _echo_filter_re.match(self.match_.group()).groups()
        if groups[0]:
            Quiet(match_=self.match_, container=container).place_node_in_tree()
            self._child_count = self._child_count + 1
        if groups[3]:
            InAll(match_=self.match_, container=container).place_node_in_tree()
            self._child_count = self._child_count + 1
        for count in (1, 2):
            echovariable = Variable(
                match_=_echo_variable_re.match(groups[count]),
                container=container,
            )
            echovariable.place_node_in_tree()
            echovariable.set_types(
                cqltypes.VariableType.POSITION,
                cqltypes.FilterType.POSITION,
            )
            container.cursor = self
            self._child_count = self._child_count + 1


# Refers to an 'implicit search parameter' in table of filters.
# In tagqueryfilters.html it is referred to as an 'implicit search filter'.
# It is not mentioned on implicitsearch.html
class ECO(structure.ImplicitSearchFilter):
    """Represent 'eco' string filter."""

    _filter_type = cqltypes.FilterType.STRING


# Operates on existential and universal piece and square variables against
# a set filter (Z) to evaluate any filter (F).
# For example:
# 'x∊Z F' "matches the position if F is true for some value x in Z".
# A variable without prefix is an existential square varaiable,
# A variable with '[Aa]' or '◭' prefix is an existential piece varaiable,
# A variable with the additional '[forall]' or '∀' prefix is a
# universalsquare or piece variable.
# '[element]' is treated as an infix operator but was not given a
# precedence because it does not appear in the table of precedence.
# This does not cause a problem provided '[element]' is not exposed to
# operator swapping on precedence: at one point ExistentialSquareVariable
# incorrectly had a precedence which provided exposure.
class Element(structure.MoveInfix):
    """Represent the '∊' set filter. (ASCII '[element]')."""

    _filter_type = cqltypes.FilterType.SET | cqltypes.FilterType.LOGICAL


# 'elo' does not have an implicit search filter, unlike many of the other
# PGN Tag filters.
# CQL-6.2 table of filters describes 'white' and 'black' as parameters,
# unlike the 'player' filter.
class Elo(structure.NoArgumentsFilter):
    """Represent 'elo', 'elo black, and 'elo white', numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class Else(structure.Argument):
    """Represent 'else' keyword in 'if' filter.

    The full form is 'if condition consequent else alternative', where
    'condition', 'consequent', and 'alternative', can be any filter.

    'else' introduces the optional 'else alternative' part.
    """

    _precedence = (
        cqltypes.Precedence.P30
    )  # Does this matter?  Reference is 'if/then/else'.

    # 'else', along with 'then', is described as a parameter of the 'if'
    # filter at CQL-6.0.4 but not at CQL-6.1 or CQL-6.2.

    @property
    def filter_type(self):
        """Return filter type of last child if FunctionLeft completed."""
        if self.completed:
            return self.children[-1].filter_type
        return super().filter_type

    def complete(self):
        """Return True if Else node is complete."""
        return len(self.children) > 1

    def full(self):
        """Return True if Else node is full."""
        return len(self.children) > 0

    def place_node_in_tree(self):
        """Delegate then verify parent is 'if' filter with one 'else'."""
        super().place_node_in_tree()
        self.raise_if_name_parameter_not_for_filters()
        parent = self.parent
        if len(parent.children) != 3:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": incorrect number of children to have 'else' in "
                + parent.__class__.__name__
            )

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, If)


# The 'enpassant' filter is not listed in the Table of Filters but is
# listed as a currentmove filter in currentmove.html documentation.
class EnPassant(structure.NoArgumentsFilter):
    """Represent 'enpassant' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class EnPassantParameter(structure.NoArgumentsParameter):
    """Represent 'enpassant' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


def enpassant(match_=None, container=None):
    """Return EnPassant or EnPassantParameter instance.

    'enpassant' may be either a set filter or a parameter.  CQL does not
    treat the second 'enpassant' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if isinstance(node, Move):
            return EnPassantParameter(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return EnPassant(match_=match_, container=container)


# The 'enpassantsquare' filter is not listed in the Table of Filters but is
# listed as a currentmove filter in currentmove.html documentation.
class EnPassantSquare(structure.NoArgumentsFilter):
    """Represent 'enpassantsquare' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class EnPassantSquareParameter(structure.NoArgumentsParameter):
    """Represent 'enpassantsquare' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


def enpassantsquare(match_=None, container=None):
    """Return EnPassantSquare or EnPassantSquareParameter instance.

    'enpassantsquare' may be either a set filter or a parameter.  CQL does
    not treat the second 'enpassantsquare' in a sequence of parameters as a
    filter: but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if isinstance(node, Move):
            return EnPassantSquareParameter(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return EnPassantSquare(match_=match_, container=container)


# Refers to an 'implicit search parameter' in table of filters.
# In tagqueryfilters.html it is referred to as an 'implicit search filter'.
class EventDate(structure.ImplicitSearchFilter):
    """Represent 'eventdate' string filter."""

    _filter_type = cqltypes.FilterType.STRING


# Refers to an 'implicit search parameter' in table of filters.
# In tagqueryfilters.html it is referred to as an 'implicit search filter'.
class Event(structure.ImplicitSearchFilter):
    """Represent 'event' string filter."""

    _filter_type = cqltypes.FilterType.STRING


# pylint C0103 naming style.  'false' is a CQL keyword which is represented
# as a class with the same capitalized name, and suffix '_' to avoid clash
# with Python keyword 'False'.
# In cases where CQL does not define a name (symbols) the Python class name
# is chosen to avoid similar problems.
class False_(structure.NoArgumentsFilter):
    """Represent 'false' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


# Mentioned as similar to ImplicitSearchFilter.
# Treat FEN as having an inplicit search parameter to start with, but this
# may have to be changed because the interpretation is different.
class FEN(structure.ImplicitSearchFilter):
    """Represent 'fen' string filter."""

    _filter_type = cqltypes.FilterType.STRING


class File(structure.Argument):
    """Represent 'file' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P150


# 'v = find all K' suggests 'find' is a numeric filter.
# 'v = find 0 50 K' suggests 'find' is a numeric filter.
# 'v = find 0 K' suggests 'find' is a numeric filter.
# 'v = find 0 50 all K' is a syntax error: use 'range' or 'all', not both.
# 'v = find K' suggests 'find' is a position filter.
# 'v = find 0 50 6 K' is interpreted as range '0 50' and body filter '6'
#                     followed by piece designator 'K'.
class Find(structure.Argument):
    """Represent 'find' numeric filter or position filter.

    The parameter 'all' or a range, '1' or '2 6' for example, make 'find'
    a numeric filter.

    The absence of both 'all' and a range make 'find' a position filter.
    """

    # The 'all' parameter changes the filter type to 'numeric'.
    _filter_type = cqltypes.FilterType.POSITION
    _precedence = cqltypes.Precedence.P30


def is_firstmatch_parameter_accepted_by(node):
    """Return True if node accepts firstmatch parameter."""
    return isinstance(node, (Line, Path))


class FirstMatch(structure.NoArgumentsParameter):
    """Represent 'firstmatch' parameter to 'line' and 'path' filters."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_firstmatch_parameter_accepted_by(self.parent)


# See comment preceding Shift: same seen for FlipColor.
class FlipColor(TransformFilterType, structure.Argument):
    """Represent 'flipcolor' filter of all types."""

    _precedence = cqltypes.Precedence.P30


# See comment preceding Shift: same seen for FlipVertical.
class FlipHorizontal(TransformFilterType, structure.Argument):
    """Represent 'fliphorizontal' filter of all types."""

    _precedence = cqltypes.Precedence.P30


# See comment preceding Shift: same seen for FlipVertical.
class FlipVertical(TransformFilterType, structure.Argument):
    """Represent 'flipvertical' filter of all types."""

    _precedence = cqltypes.Precedence.P30


# See comment preceding Shift: same seen for Flip.
class Flip(TransformFilterType, structure.Argument):
    """Represent 'flip' filter of all types."""

    _precedence = cqltypes.Precedence.P30


def is_focus_capture_parameter_accepted_by(node):
    """Return True if node accepts focus capture parameter."""
    return isinstance(node, Path)


class FocusCapture(structure.ParameterArgument):
    """Represent 'focus capture' parameter of 'path' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_focus_capture_parameter_accepted_by(self.parent)


def is_focus_parameter_accepted_by(node):
    """Return True if node accepts focus parameter."""
    return isinstance(node, Path)


class Focus(structure.ParameterArgument):
    """Represent 'focus' parameter of 'path' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_focus_parameter_accepted_by(self.parent)


# Not a value in cql.class_from_token_name but called by place_node_in_tree()
# method in ExistentialSquareIterator.
class ExistentialSquareVariable(structure.Complete, structure.VariableName):
    """Represent 'square variable' for the 'square iteration' filter.

    The variable name has no prefix but must be followed by '[element]' or
    '\u220a' (∊).

    The value of an existential square variable is a Set filter.
    """

    # Not in table of precedence: probably a typo so commented.
    # _precedence = cqltypes.Precedence.P30

    def __init__(self, match_=None, container=None):
        """Delegate then register set variable name for existence filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["existential_square_variable"]
        self._register_variable_type(cqltypes.VariableType.SET)
        self.set_types(cqltypes.VariableType.SET, cqltypes.FilterType.SET)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class ExistentialSquareIterator(structure.Argument):
    """Represent implied 'existential square iteration' filter."""

    _filter_type = cqltypes.FilterType.SET
    _child_count = 2

    def place_node_in_tree(self):
        """Delegate then append child ExistentialSquareVariable instance."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        ExistentialSquareVariable(
            match_=self.match_, container=container
        ).place_node_in_tree()


# Not a value in cql.class_from_token_name but called by place_node_in_tree()
# method in ExistentialPieceIterator.
class ExistentialPieceVariable(structure.Complete, structure.VariableName):
    """Represent 'piece variable' for the 'piece iteration' filter.

    The variable name is prefixed by '[Aa]' or '\u25ed' (◭) and must be
    followed by '[element]' or '\u220a' (∊).

    The value of an existential piece variable is a Set filter.
    """

    # Not in table of precedence: probably a typo so commented.
    # _precedence = cqltypes.Precedence.P30

    def __init__(self, match_=None, container=None):
        """Delegate then register piece variable name for existence filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["existential_piece_variable"]
        self._register_variable_type(cqltypes.VariableType.PIECE)
        self.set_types(cqltypes.VariableType.PIECE, cqltypes.FilterType.SET)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class ExistentialPieceIterator(structure.Argument):
    """Represent implied 'existential piece iteration' filter."""

    _filter_type = cqltypes.FilterType.SET
    _child_count = 2

    def place_node_in_tree(self):
        """Delegate then append child ExistentialPieceVariable instance."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        ExistentialPieceVariable(
            match_=self.match_, container=container
        ).place_node_in_tree()


# Not a value in cql.class_from_token_name but called by place_node_in_tree()
# method in UniversalSquareIterator.
class UniversalSquareVariable(structure.Complete, structure.VariableName):
    """Represent 'square variable' for 'universal square iteration' filter..

    The variable name is prefixed by '[forall]' or '\u2200' (∀) and must be
    followed by '[element]' or '\u220a' (∊).

    The value of a universal square variable is a Set filter.
    """

    _precedence = cqltypes.Precedence.P30

    def __init__(self, match_=None, container=None):
        """Delegate then register set variable name for universal filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["universal_square_variable"]
        self._register_variable_type(cqltypes.VariableType.SET)
        self.set_types(cqltypes.VariableType.SET, cqltypes.FilterType.SET)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class UniversalSquareIterator(structure.Argument):
    """Represent implied 'universal square iteration' filter."""

    _filter_type = cqltypes.FilterType.SET
    _child_count = 2

    def place_node_in_tree(self):
        """Delegate then append child UniversalSquareVariable instance."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        UniversalSquareVariable(
            match_=self.match_, container=container
        ).place_node_in_tree()


# Not a value in cql.class_from_token_name but called by place_node_in_tree()
# method in UniversalPieceIterator.
class UniversalPieceVariable(structure.Complete, structure.VariableName):
    """Represent 'piece variable' for 'universal piece iteration' filter.

    The variable name is prefixed by '[forall][Aa]' or '\u2200\u25ed' (∀◭)
    and must be followed by '[element]' or '\u220a' (∊).

    The value of a universal piece variable is a Set filter.
    """

    _precedence = cqltypes.Precedence.P30

    def __init__(self, match_=None, container=None):
        """Delegate then register piece variable name for universal filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["universal_piece_variable"]
        self._register_variable_type(cqltypes.VariableType.PIECE)
        self.set_types(cqltypes.VariableType.PIECE, cqltypes.FilterType.SET)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class UniversalPieceIterator(structure.Argument):
    """Represent implied 'universal piece iteration' filter."""

    _filter_type = cqltypes.FilterType.SET
    _child_count = 2

    def place_node_in_tree(self):
        """Delegate then append child UniversalPieceVariable instance."""
        super().place_node_in_tree()
        container = self.container
        container.cursor = self
        UniversalPieceVariable(
            match_=self.match_, container=container
        ).place_node_in_tree()


class From(structure.NoArgumentsFilter):
    """Represent 'from' set filter."""

    _filter_type = cqltypes.FilterType.SET


def is_from_parameter_accepted_by(node):
    """Return True if node accepts from parameter."""
    return isinstance(node, (Move, Pin))


class FromParameter(MoveParameterImpliesSet):
    """Represent 'from' parameter of 'pin' and 'move' filters.

    'from' and 'pin from from', are accepted by cql-6.2 parser; but
    'pin from' and 'pin from from from' give a syntax error.
    """

    _precedence = cqltypes.Precedence.P200  # 'pin' filter only.

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_from_parameter_accepted_by(self.parent)


# 'from' is a reserved word in Python.
def from_(match_=None, container=None):
    """Return From or FromParameter instance.

    'from' may be either a set filter or a parameter.  CQL does not
    treat the second 'from' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if is_from_parameter_accepted_by(node):
            return FromParameter(match_=match_, container=container)
        node = node.parent
    return From(match_=match_, container=container)


class Function(structure.Name, structure.Argument):
    """Represent 'function' filter of any type.

    The filter type is the filter type of the compound filter argument
    when evaluated as a function call.
    """

    _precedence = cqltypes.Precedence.P30

    def __init__(self, match_=None, container=None):
        """Delegate then register the function and parameter names.

        Details for user defined items, variables and functions, are not
        updated when encountered during collection of functions bodies.

        """
        super().__init__(match_=match_, container=container)
        names = match_.group().replace("(", " ").replace(")", " ").split()[1:]
        self.name = names.pop(0)
        self._raise_if_name_invalid(cqltypes.Function)
        self._raise_if_already_defined(
            cqltypes.DefinitionType.ANY,
            cqltypes.DefinitionType.VARIABLE,
        )
        if len(names) != len(set(names)):
            raise basenode.NodeError(
                "Function '" + self.name + "' has duplicate parameter names"
            )
        cqltypes.function(self.name, container)
        if container.function_body_cursor is None:
            container.definitions[self.name].parameters = names

    def place_node_in_tree(self):
        """Delegate then set function body cursor to self if None."""
        # Cannot set function_body_cursor in __init__ because there may be
        # things that need doing when 'function' causes completion of an
        # earlier filter.
        super().place_node_in_tree()
        if self.container.function_body_cursor is None:
            self.container.function_body_cursor = self


class FunctionCall(structure.Name, structure.ParenthesizedArguments):
    """Represent 'function call' filter of any type.

    The filter type is the filter type of the compound filter argument.
    """

    # See Ancestor too.
    # Treated as '<function> (' not '<function>' then '(' and ... ')'.
    # _precedence = cqltypes.Precedence.P30

    @property
    def filter_type(self):
        """Return filter type of last child if FunctionLeft completed."""
        # The superclass filter_type property is in BaseNode giving ~ANY as
        # return value.  This should cause a parsing error above this
        # node in the tree.
        if self.completed:
            return self.children[-1].filter_type
        return super().filter_type

    def __init__(self, match_=None, container=None):
        """Delegate then register the function and parameter names."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["function_call"]
        self._raise_if_name_invalid(cqltypes.Function)
        self._raise_if_function_not_defined()

    def _raise_if_function_not_defined(self):
        """Raise NodeError if name exists with type in definition_types."""
        name = self._name
        container = self.container
        if name not in container.definitions:
            raise basenode.NodeError(
                "'" + name + "' is not defined so cannot be a function call"
            )
        if (
            container.definitions[name].definition_type
            is not cqltypes.DefinitionType.FUNCTION
        ):
            raise basenode.NodeError(
                "'"
                + name
                + "' is a '"
                + container.definitions[name].definition_type.name
                + "' so cannot be a function call"
            )

    # This method exists to allow BaseNode and FunctionCall classes to be in
    # separate modules.
    # Reimplement parse_tree_trace() to do this? or
    # Map reserved variable names to function call names?
    def is_node_functioncall_instance(self):
        """Return True."""
        return True


def variable_then_parenthesis(match_=None, container=None):
    """Insert Variable instance and return ParenthesisLeft instance."""
    var = Variable(match_=match_, container=container)
    var.name = match_.groupdict()["function_call"]
    var.place_node_in_tree()
    return ParenthesisLeft(match_=match_, container=container)


def function_call(match_=None, container=None):
    """Return FunctionCall or ParenthesisLeft instance.

    If the match_.group() is in the register of function names return a
    FunctionCall instance.

    Otherwise call variable_then_parenthesis method to process the token
    as a variable name and return a ParenthesisLeft instance for the '('
    at end of token.

    """
    name = match_.groupdict()["function_call"]
    if name in container.definitions:
        if (
            container.definitions[name].definition_type
            is cqltypes.DefinitionType.FUNCTION
        ):
            return FunctionCall(match_=match_, container=container)
    return variable_then_parenthesis(match_=match_, container=container)


class GameNumber(structure.NoArgumentsFilter):
    """Represent 'gamenumber' numeric filter.

    The 'gamenumber' keyword also appears in the parameter module.
    """

    _filter_type = cqltypes.FilterType.NUMERIC


class HasComment(structure.Argument):
    """Represent 'hascomment' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Horizontal(structure.Argument):
    """Represent 'horizontal' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class HorizontalParameter(structure.DirectionParameter):
    """Represent 'horizontal' transform filter direction parameter."""


def horizontal(match_=None, container=None):
    """Return Horizontal or HorizontalParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return HorizontalParameter(match_=match_, container=container)
    return Horizontal(match_=match_, container=container)


class IdealMate(structure.NoArgumentsFilter):
    """Represent 'idealmate' set filter."""

    _filter_type = cqltypes.FilterType.SET


class IdealStaleMate(structure.NoArgumentsFilter):
    """Represent 'idealstalemate' set filter."""

    _filter_type = cqltypes.FilterType.SET


class If(structure.Argument):
    """Represent 'if' filter.

    The full form is 'if condition then consequent else alternative',
    where 'condition', 'consequent', and 'alternative', can be any filter.

    'else alternative' is optional and introduced by 'else' keyword.

    At versions of CQL earlier than 6.2 the 'then' keyword, referred to as
    a parameter, was mandatory.

    At version 6.2 the 'then' keyword is deprecated.
    """

    _precedence = cqltypes.Precedence.P30

    @property
    def filter_type(self):
        """Return filter type of last child if FunctionLeft completed."""
        if self.completed:
            children = self.children
            if len(children) == 2:
                return cqltypes.FilterType.LOGICAL
            child1_filter_type = children[1].filter_type
            if child1_filter_type is not children[2].filter_type:
                return cqltypes.FilterType.LOGICAL
            if child1_filter_type is cqltypes.FilterType.LOGICAL:
                return cqltypes.FilterType.LOGICAL
            if child1_filter_type is cqltypes.FilterType.STRING:
                return cqltypes.FilterType.LOGICAL
            return child1_filter_type
        return super().filter_type

    # May not work for 'if <cond> [then] <arg> else a == 3' which will
    # put an Eq instance as final child of If when complete.  Eq is an
    # example of Infix.
    def complete(self):
        """Return True if If node is complete."""
        if len(self.children) > 3:
            return True
        if len(self.children) > 2:
            return not isinstance(self.children[2], (Else, structure.Infix))
        return False

    # May not work for 'if <cond> [then] <arg> else a == 3' which will
    # put an Eq instance as final child of If when full.  Eq is an
    # example of Infix.
    def full(self):
        """Return True if If node is full."""
        if len(self.children) > 2:
            return True
        if len(self.children) > 1:
            return not isinstance(self.children[1], (Else, structure.Infix))
        return False


class IndexOf(structure.ParenthesizedArguments):
    """Represent 'indexof' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class InitialPosition(structure.NoArgumentsFilter):
    """Represent 'initialposition' position filter."""

    _filter_type = cqltypes.FilterType.POSITION


class Initial(structure.NoArgumentsFilter):
    """Represent 'initial' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Int(structure.Argument):
    """Represent 'int' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P100


class InAll(structure.NoArgumentsParameter):
    """Represent 'in all' parameter of 'echo' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Echo)


class In(structure.InfixLeft):
    """Represent 'in' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P70


class InParameter(structure.NoArgumentsParameter):
    """Represent ''in' parameter to 'piece' and 'square' filters."""

    _precedence = cqltypes.Precedence.P150

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, (Piece, Square))


# 'in' is a Python keyword.
def in_(match_=None, container=None):
    """Return In or InParameter instance.

    'in' may be either a logical filter or a parameter.
    CQL does not treat the second 'in' in a sequence of parameters as a
    filter: but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    if isinstance(container.cursor, (Piece, Square)):
        return InParameter(match_=match_, container=container)
    return In(match_=match_, container=container)


class IsBound(structure.NoArgumentsFilter):
    """Represent 'isbound' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class IsolatedPawns(structure.NoArgumentsFilter):
    """Represent 'isolatedpawns' set filter."""

    _filter_type = cqltypes.FilterType.SET


class IsUnbound(structure.NoArgumentsFilter):
    """Represent 'isunbound' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


def is_keepallbest_parameter_accepted_by(node):
    """Return True if node accepts keepallbest parameter."""
    return isinstance(node, Path)


class KeepAllBest(structure.NoArgumentsParameter):
    """Represent 'keepallbest' parameter of 'path' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_keepallbest_parameter_accepted_by(self.parent)


class LastGameNumber(structure.NoArgumentsFilter):
    """Represent 'lastgamenumber' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


def is_lastposition_parameter_accepted_by(node):
    """Return True if node accepts lastposition parameter."""
    return isinstance(node, (Line, Path))


class LastPosition(structure.NoArgumentsParameter):
    """Represent 'lastposition' parameter to 'line' and 'path' filters."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_lastposition_parameter_accepted_by(self.parent)

    def place_node_in_tree(self):
        """Delegate then adjust parent filter type for 'line' filter."""
        super().place_node_in_tree()
        parent = self.parent
        # These filter type adjustments are best done when completing
        # the parent filter.
        if isinstance(parent, Line):
            parent.filter_type = cqltypes.FilterType.POSITION
            return


class LCA(structure.ParenthesizedArguments):
    """Represent 'lca' position filter."""

    _filter_type = cqltypes.FilterType.POSITION
    # See Ancestor too.
    # Treated as 'lca (' not 'lca' then '(' and ... ')'.
    # _precedence = cqltypes.Precedence.P30


class Left(structure.Argument):
    """Represent 'left' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class LeftParameter(structure.DirectionParameter):
    """Represent 'left' transform filter direction parameter."""


def left(match_=None, container=None):
    """Return Left or LeftParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return LeftParameter(match_=match_, container=container)
    return Left(match_=match_, container=container)


class Legal(structure.Argument):
    """Represent 'legal' set filter or parameter to 'move' filter."""

    _filter_type = cqltypes.FilterType.SET


class LegalParameter(MoveParameterImpliesNumeric):
    """Represent 'legal' parameter of 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


def legal(match_=None, container=None):
    """Return Legal or LegalParameter instance.

    'legal' may be either a set filter or a parameter.  CQL does not
    treat the second 'legal' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if isinstance(node, Move):
            return LegalParameter(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return Legal(match_=match_, container=container)


class Light(structure.Argument):
    """Represent 'light' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class Line(structure.CompleteParameterArguments):
    """Represent 'line' numeric or position filter."""

    # The 'lastposition' parameter changes the filter type to 'position'.
    _filter_type = cqltypes.FilterType.NUMERIC
    # CQL-6.1 describes '-->' and '<--' as symbols rather than parameters
    # or filters.  It seems best to treat them as parameters of 'line'
    # though the filter must have one or more of either '-->' or '<--'
    # but not both.  This breaks the rule, everywhere else, that only one
    # instance of a parameter is allowed in each filter.  If treated as
    # filters it is implied '-->' and '<--' are the only filters allowed
    # as arguments of 'line': and their type is unclear.  Elsewhere multiple
    # filters are grouped together by the '{ ... }' construct or by listing
    # them within parentheses like in 'between', 'ray', or 'comment' and
    # so forth.
    # The filters used within the 'line' filter are held as children of
    # '-->' or '<--', one per arrow.
    # At CQL-6.2 the 'path' filter introduces the idea of ending a filter
    # by a blank line: avoiding separator symbols like '-->' or '<--' and
    # the '{ ... }' or '( ... )' ways of grouping filters.

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class Local(structure.CQLObject):
    """Represent 'local' not caught elsewhere for specific purposes.

    Caught in Dictionary: 'local' is only allowed to precede 'dictionary'
    and appearance elsewhere is an error.
    """

    def place_node_in_tree(self):
        """Delegate then raise NodeError because bare 'local' not allowed."""
        super().place_node_in_tree()
        raise basenode.NodeError(r"Unexpected bare 'local' found")


class Loop(structure.Argument):
    """Represent 'loop' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P30


class LowerCase(structure.Argument):
    """Represent 'lowercase' string filter."""

    _filter_type = cqltypes.FilterType.STRING
    _precedence = cqltypes.Precedence.P120


class MainDiagonal(structure.Argument):
    """Represent 'maindiagonal' set filter.

    'maindiagonal' is not mentioned in CQL documentation but behaves like
    a direction filter; and cannot be used as a variable name.

    'maindiagonal' is described in CQLi documentation.
    """

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class MainDiagonalParameter(structure.DirectionParameter):
    """Represent 'maindiagonal' transform filter direction parameter.

    'maindiagonal' is not mentioned in CQL documentation but behaves like
    a transform filter parameter; and cannot be used as a variable name.

    'maindiagonal' is described in CQLi documentation.
    """


def main_diagonal(match_=None, container=None):
    """Return MainDiagonal or MainDiagonalParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return MainDiagonalParameter(match_=match_, container=container)
    return MainDiagonal(match_=match_, container=container)


class MainLine(structure.NoArgumentsFilter):
    """Represent 'mainline' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


def mainline(match_=None, container=None):
    """Return MainLine or HHDBToken instance."""
    if hhdb.is_hhdb_token_accepted_by(container.cursor):
        return hhdb.HHDBToken(match_=match_, container=container)
    return MainLine(match_=match_, container=container)


class MakeSquareParentheses(structure.ParenthesizedArguments):
    """Represent 'makesquare' set filter for parenthesized arguments."""

    _filter_type = cqltypes.FilterType.SET
    # See Ancestor too.
    # Treated as 'makesquare (' not 'makesquare' then '(' and ... ')'.
    # _precedence = cqltypes.Precedence.P90


class MakeSquareString(structure.CQLObject):
    """Represent 'makesquare' set filter for string argument."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P90


class Mate(structure.NoArgumentsFilter):
    """Represent 'mate' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


def is_max_parameter_accepted_by(node):
    """Return True if node accepts max parameter."""
    return isinstance(node, Path)


class Max(structure.ParenthesizedArguments):
    """Represent 'max' numeric or string filter."""

    _filter_type = cqltypes.FilterType.NUMERIC | cqltypes.FilterType.STRING


class MaxParameter(structure.ParameterArgument):
    """Represent 'max' parameter of 'path' (⊢) filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_max_parameter_accepted_by(self.parent)


# 'max' is a Python built-in function.
def max_(match_=None, container=None):
    """Return Max or MaxParameter instance.

    'max' may be either a numeric filter or a string filter, or a parameter.
    CQL does not treat the second 'max' in a sequence of parameters as a
    filter: but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    if hhdb.is_hhdb_token_accepted_by(container.cursor):
        return hhdb.HHDBToken(match_=match_, container=container)
    # This is probably too simple because the parent may be at the end of a
    # chain of ancestors, one of which takes 'max' as a parameter, and can
    # accept the parameter.  For example the chain may belong to another
    # parameter of the suitable ancestor.
    if is_max_parameter_accepted_by(container.cursor):
        return MaxParameter(match_=match_, container=container)
    return Max(match_=match_, container=container)


class Message(structure.ParenthesizedArguments):
    """Represent 'message' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Min(structure.ParenthesizedArguments):
    """Represent 'min' numeric or string filter."""

    _filter_type = cqltypes.FilterType.NUMERIC | cqltypes.FilterType.STRING


def is_min_parameter_accepted_by(node):
    """Return True if node accepts min parameter."""
    return isinstance(node, Sort)


class MinParameter(structure.ParameterArgument):
    """Represent 'min' parameter of 'sort' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_min_parameter_accepted_by(self.parent)


# 'min' is a Python built-in function.
def min_(match_=None, container=None):
    """Return Min or MinParameter instance.

    'min' may be either a numeric filter or a string filter, or a parameter.
    CQL does not treat the second 'min' in a sequence of parameters as a
    filter: but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    # This is probably too simple because the parent may be at the end of a
    # chain of ancestors, one of which takes 'min' as a parameter, and can
    # accept the parameter.  For example the chain may belong to another
    # parameter of the suitable ancestor.
    if is_min_parameter_accepted_by(container.cursor):
        return MinParameter(match_=match_, container=container)
    return Min(match_=match_, container=container)


class ModelMate(structure.NoArgumentsFilter):
    """Represent 'modelmate' set filter."""

    _filter_type = cqltypes.FilterType.SET


class ModelStalemate(structure.NoArgumentsFilter):
    """Represent 'modelstalemate' set filter."""

    _filter_type = cqltypes.FilterType.SET


class MoveNumber(structure.NoArgumentsFilter):
    """Represent 'movenumber' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


# Delete all but first line of docstring when implemented.
# Other lines are a precis of what documentation says about 'move' filter.
class Move(
    structure.PrecedenceFromChild, structure.CompleteParameterArguments
):
    """Represent 'move' set, logical, or numeric, filter.

    At CQL-6.2 'move' is:
        set filter if 'from', 'to', or 'capture' is first parameter;
        numeric filter if 'count' parameter is present, and either 'legal'
            or 'pseudolegal' parameter is present;
        logical filter otherwise.
        The presence of 'count' takes precedence over location of 'from',
        'to', or 'capture' parameters.

    At CQL-6.2 the parameter interpretation takes precedence over the
    filter specification where a keyword could be either.  For example
    'move o-o o-o' is double specification of 'o-o' parameter: the second
    'o-o' is not seen as a set filter like in 'move o-o b o-o'.

    """

    _filter_type = cqltypes.FilterType.LOGICAL

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


def is_nestban_parameter_accepted_by(node):
    """Return True if node accepts nestban parameter."""
    return isinstance(node, (Line, Path))


class NestBan(structure.NoArgumentsParameter):
    """Represent 'nestban' parameter to 'line' and 'path' filters."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_nestban_parameter_accepted_by(self.parent)


class Northeast(structure.Argument):
    """Represent 'northeast' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class NortheastParameter(structure.DirectionParameter):
    """Represent 'northeast' transform filter direction parameter."""


def northeast(match_=None, container=None):
    """Return Northeast or NortheastParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return NortheastParameter(match_=match_, container=container)
    return Northeast(match_=match_, container=container)


class Northwest(structure.Argument):
    """Represent 'northwest' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class NorthwestParameter(structure.DirectionParameter):
    """Represent 'northwest' transform filter direction parameter."""


def northwest(match_=None, container=None):
    """Return Northwest or NorthwestParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return NorthwestParameter(match_=match_, container=container)
    return Northwest(match_=match_, container=container)


class NoTransform(structure.Argument):
    """Represent 'notransform' filter of type of argument filter.

    For example 'notransform K' is a set filter because 'K' is a set filter
    and 'notransform wtm' is a logical filter because 'wtm' is a logical
    filter.
    """

    _filter_type = (
        cqltypes.FilterType.SET
        | cqltypes.FilterType.LOGICAL
        | cqltypes.FilterType.NUMERIC
        | cqltypes.FilterType.STRING
        | cqltypes.FilterType.POSITION
    )


class Not(structure.Argument):
    """Represent 'not' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P60


class NullMove(structure.NoArgumentsFilter):
    """Represent 'nullmove' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Null(structure.NoArgumentsParameter):
    """Represent 'null' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


# O_O_O is an unconventional class name according to black formatter.
class OOO(structure.NoArgumentsFilter):
    """Represent 'o-o-o' logical filter or parameter to 'move' filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


# O_O_OParameter is an unconventional class name according to black formatter.
class OOOParameter(structure.NoArgumentsParameter):
    """Represent 'o-o-o' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


# o-o-o is not an attribute name in Python.
def o_o_o(match_=None, container=None):
    """Return OOO or OOOParameter instance.

    'o-o-o' may be either a set filter or a parameter.  CQL does not
    treat the second 'o-o-o' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if isinstance(node, Move):
            return OOOParameter(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return OOO(match_=match_, container=container)


# O_O is an unconventional class name according to black formatter.
class OO(structure.NoArgumentsFilter):
    """Represent 'o-o' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


# O_OParameter is an unconventional class name according to black formatter.
class OOParameter(structure.NoArgumentsParameter):
    """Represent 'o-o' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


# o-o is not an attribute name in Python.
def o_o(match_=None, container=None):
    """Return OO or OOParameter instance.

    'o-o' may be either a set filter or a parameter.  CQL does not
    treat the second 'o-o' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if isinstance(node, Move):
            return OOParameter(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return OO(match_=match_, container=container)


class OffDiagonal(structure.Argument):
    """Represent 'offdiagonal' set filter.

    'offdiagonal' is not mentioned in CQL documentation but behaves like
    a direction filter; and cannot be used as a variable name.

    'offdiagonal' is described in CQLi documentation.
    """

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class OffDiagonalParameter(structure.DirectionParameter):
    """Represent 'offdiagonal' transform filter direction parameter.

    'offdiagonal' is not mentioned in CQL documentation but behaves like
    a transform filter parameter; and cannot be used as a variable name.

    'offdiagonal' is described in CQLi documentation.
    """


def off_diagonal(match_=None, container=None):
    """Return OffDiagonal or OffDiagonalParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return OffDiagonalParameter(match_=match_, container=container)
    return OffDiagonal(match_=match_, container=container)


# Mentioned as similar to ImplicitSearchFilter.
# If the string argument is a NAG, the interpretation is not implicit search.
class OriginalComment(structure.ImplicitSearchFilter):
    """Represent 'originalcomment' string filter."""

    _filter_type = cqltypes.FilterType.STRING


class Orthogonal(structure.Argument):
    """Represent 'orthogonal' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class OrthogonalParameter(structure.DirectionParameter):
    """Represent 'orthogonal' transform filter direction parameter."""


def orthogonal(match_=None, container=None):
    """Return Orthogonal or OrthogonalParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return OrthogonalParameter(match_=match_, container=container)
    return Orthogonal(match_=match_, container=container)


class Or(structure.InfixLeft):
    """Represent 'or' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P40


class Parent(structure.NoArgumentsFilter):
    """Represent 'parent' position filter."""

    _filter_type = cqltypes.FilterType.POSITION


class PassedPawns(structure.NoArgumentsFilter):
    """Represent 'passedpawns' set filter."""

    _filter_type = cqltypes.FilterType.SET


class PathCountUnfocused(structure.Complete):
    """Ignore experimental 'pathcountunfocused' filter at 6.2."""

    _filter_type = cqltypes.FilterType.NUMERIC

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class PathCount(structure.Complete):
    """Ignore experimental 'pathcount' filter at 6.2."""

    _filter_type = cqltypes.FilterType.NUMERIC

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class PathLastPosition(structure.Complete):
    """Ignore experimental 'pathlastposition' filter at 6.2."""

    _filter_type = cqltypes.FilterType.POSITION

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class PathStart(structure.Complete):
    """Ignore experimental 'pathstart' filter at 6.2."""

    _filter_type = cqltypes.FilterType.POSITION

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class Path(structure.BlockLeft):
    """Represent 'path' numeric filter.

    The 'path' filters' children should be read as parameters followed by
    a sequence of "dash", or the capturing equivalent, filters with any
    other filters being the target of the preceding "dash" filter.  This
    interpretation is derived from what the '-parse' option output from
    CQL-6.2 is for '... path -- secondary secondary'.  But '... path a'
    causes generation of a "HolderCon" node rather than giving a syntax
    error.

    The 'path' filter is terminated by a blank line (CQL documentation says
    'may be terminated by' but it is not clear what other sequence, except
    end of file, acts as a terminator).  This is similar to the '///'
    filter which is terminated by a newline.
    """

    _filter_type = cqltypes.FilterType.NUMERIC


class PersistentQuiet(structure.Complete, structure.VariableName):
    """Represent variable with 'persistent quiet' prefix.

    'persistent quiet' must be first use of variable name.

    The value of a persistent quiet variable is a Numeric, Set, or String,
    filter.
    """

    def __init__(self, match_=None, container=None):
        """Delegate then register the variable name."""
        super().__init__(match_=match_, container=container)
        groupdict = match_.groupdict()
        self.name = groupdict["persistent_quiet"]
        if self.name in self.container.definitions:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": '"
                + self.name
                + "' is already defined and cannot be set persistent"
            )
        self._register_variable_type(cqltypes.VariableType.ANY)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class Persistent(structure.Complete, structure.VariableName):
    """Represent variable with 'persistent' prefix.

    'persistent' must be first use of variable name.

    The value of a persistent quiet variable is a Numeric, Set, or String,
    filter.
    """

    def __init__(self, match_=None, container=None):
        """Delegate then register the variable name."""
        super().__init__(match_=match_, container=container)
        groupdict = match_.groupdict()
        self.name = groupdict["persistent"]
        if self.name in self.container.definitions:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": '"
                + self.name
                + "' is already defined and cannot be set persistent"
            )
        self._register_variable_type(cqltypes.VariableType.ANY)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class PieceId(structure.Argument):
    """Represent 'pieceid' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P150


class PieceName(structure.Argument):
    """Represent 'piecename' string filter."""

    _filter_type = cqltypes.FilterType.STRING


def is_piecepath_parameter_accepted_by(node):
    """Return True if node accepts piecepath parameter."""
    return isinstance(node, Path)


class PiecePath(structure.NoArgumentsParameter):
    """Represent 'piecepath' parameter to 'path' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_piecepath_parameter_accepted_by(self.parent)


class Piece(structure.VariableName, structure.Argument):
    """Represent 'piece', without 'all' parameter, set filter.

    The optional 'all' keyword is not present,

    The value of a piece variable is a Set filter.
    """

    _precedence = cqltypes.Precedence.P30
    _child_count = 2

    def __init__(self, match_=None, container=None):
        """Delegate then register the set variable name for piece filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["piece"]
        self._register_variable_type(cqltypes.VariableType.PIECE)
        self.set_types(cqltypes.VariableType.PIECE, cqltypes.FilterType.SET)


class PieceAll(structure.VariableName, structure.Argument):
    """Represent 'piece', with 'all' parameter, logical filter.

    The optional 'all' keyword is present,

    The value of a piece all variable is a Set filter.
    """

    _precedence = cqltypes.Precedence.P30
    _child_count = 2

    def __init__(self, match_=None, container=None):
        """Delegate then register set variable name for pieceall filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["piece"]
        self._register_variable_type(cqltypes.VariableType.PIECE)
        self.set_types(cqltypes.VariableType.PIECE, cqltypes.FilterType.SET)


def piece(match_=None, container=None):
    """Return PieceAll instance if 'all' in match_, or Piece instance."""
    if " all " in match_.group():
        return PieceAll(match_=match_, container=container)
    return Piece(match_=match_, container=container)


class PieceVariable(structure.Complete, structure.VariableName):
    """Represent the name of a piece variable set filter.

    The value of a piece variable is a Set filter.
    """

    def __init__(self, match_=None, container=None):
        """Delegate then register the piece variable name."""
        super().__init__(match_=match_, container=container)
        # The 'variable' pattern may find a name already defined as a
        # piece variable and divert it to PieceVariable class.
        # This is because piece variables are assigned by 'piece x =' or
        # on of the synonyms but referenced as 'v = x' for example.  In
        # particular (at CQL-6.2) 'v = piece x' is a syntax error.
        groupdict = match_.groupdict()
        self.name = groupdict["piece_variable"] or groupdict["variable"]
        self._register_variable_type(cqltypes.VariableType.PIECE)
        self.set_types(cqltypes.VariableType.PIECE, cqltypes.FilterType.SET)

    def place_node_in_tree(self):
        """Delegate then set cursor to self after checking tree structure.

        Keep current cursor if tree is *-Echo-ParenthesisLeft-self-*,
        otherwise set cursor to self.

        """
        super().place_node_in_tree()
        # This test implies either Echo or Variable detection needs to be
        # changed somehow?  What about Function too?
        if isinstance(self.parent, ParenthesisLeft):
            if isinstance(self.parent.parent, Echo):
                return
        self.container.cursor = self
        return


class Pin(structure.PrecedenceFromChild, structure.CompleteParameterArguments):
    """Represent 'pin' set filter.

    'pin' takes three optional parameters, 'from', 'through', and 'to'.

    'from' and 'through' default to any piece if absent.

    'to' defaults to '[Kk]' if absent.

    'pin from through' and 'pin to through' are not accepted by CQL because
    'through' does not have an interpretation as a filter.  Both 'to' and
    'from' do have interpretations as filters so 'pin through to' and
    'pin to from' and similar are accepted by CQL but do not mean the
    'from', 'to', and 'through', parameters with default filters.
    """

    _filter_type = cqltypes.FilterType.SET

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


# Perhaps this should be three filters: 'player', 'player black' and
# 'player white'.  A consequence is 'white' and 'black' are just filters,
# not filters or optional parameters of 'player'.
# The table of filters gives a single row with the three filter names and
# refers to their implicit search parameter.
# CQL-6.2 table of filters describes 'white' and 'black' as parameters in
# the 'elo' filter.
# In implicitsearch.html 'player' is named as such, and the references to
# 'black' and 'white' are assumed to be references to 'player black' and
# 'player white'.
# In tagqueryfilters.html none of 'player', 'player black' and 'player white'
# are shown in the 'table of tag query filters'; but it is assumed the
# reference means these are 'implicit search filter's too.
class Player(structure.ImplicitSearchFilter):
    """Represent 'player', 'player black, and 'player white', string filter."""

    _filter_type = cqltypes.FilterType.STRING


class Ply(structure.NoArgumentsFilter):
    """Represent 'ply' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class PositionId(structure.NoArgumentsFilter):
    """Represent 'positionid' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class Position(structure.Argument):
    """Represent 'position' position filter."""

    _filter_type = cqltypes.FilterType.POSITION
    _precedence = cqltypes.Precedence.P90


class Power(structure.Argument):
    """Represent 'power' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P150


class Previous(structure.NoArgumentsParameter):
    """Represent 'previous' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


def is_primary_parameter_accepted_by(node):
    """Return True if node accepts primary parameter."""
    return isinstance(node, (Line, Move, Path))


class Primary(structure.NoArgumentsFilter):
    """Represent 'primary' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class PrimaryParameter(structure.NoArgumentsParameter):
    """Represent 'primary' parameter to line, move, and path filters."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_primary_parameter_accepted_by(self.parent)


def primary(match_=None, container=None):
    """Return Primary or PrimaryParameter instance.

    'primary' may be either a logical filter or a parameter.  CQL does not
    treat the second 'primary' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.  However once a filter has been found
    the second and subsequent 'primary's are treated as filters.

    """
    node = container.cursor
    while True:
        if is_primary_parameter_accepted_by(node):
            break
        if isinstance(node, querycontainer.QueryContainer):
            break
        if not node.full():
            break
        node = node.parent
    if isinstance(node, Line):
        if isinstance(node.children[-1], (ArrowBackward, ArrowForward)):
            return Primary(match_=match_, container=container)
    if len(node.children) == 0:
        return PrimaryParameter(match_=match_, container=container)
    if not node.children[-1].is_parameter:
        return Primary(match_=match_, container=container)
    return PrimaryParameter(match_=match_, container=container)


class Promote(structure.ParameterArgument):
    """Represent 'promote' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


class Pseudolegal(structure.CQLObject):
    """Represent 'pseudolegal' set filter."""

    _filter_type = cqltypes.FilterType.SET


class PseudolegalParameter(MoveParameterImpliesNumeric):
    """Represent 'pseudolegal' parameter of 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


def pseudolegal(match_=None, container=None):
    """Return Pseudolegal or PseudolegalParameter instance.

    'pseudolegal' may be either a set filter or a parameter.  CQL does not
    treat the second 'pseudolegal' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if isinstance(node, Move):
            return PseudolegalParameter(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return Pseudolegal(match_=match_, container=container)


class PureMate(structure.NoArgumentsFilter):
    """Represent 'puremate' set filter."""

    _filter_type = cqltypes.FilterType.SET


class PureStalemate(structure.NoArgumentsFilter):
    """Represent 'purestalemate' set filter."""

    _filter_type = cqltypes.FilterType.SET


def is_quiet_parameter_accepted_by(node):
    """Return True if node accepts quiet parameter."""
    return isinstance(
        node, (ConsecutiveMoves, Echo, Find, Line, Message, Path)
    )


class Quiet(structure.NoArgumentsParameter):
    """Represent 'quiet' parameter to various filters and 'cql' keyword.

    The filters are:
        consecutivemoves
        echo
        find
        message
        path
        line (from CQL-6.1)

    The echo filter pattern catches the quiet parameter.

    The persistent filter has two variant patterns, one of which catches
    the quiet parameter.

    The 'quiet' keyword also appears in the parameter module.
    """

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_quiet_parameter_accepted_by(self.parent)


class Rank(structure.Argument):
    """Represent 'rank' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P150


class Ray(structure.ParenthesizedArguments):
    """Represent 'ray' set filter.

    The pattern for 'ray' filter captures the parameter and '(' tokens.

    Multiple directions can be given as parameters, but not duplicated.

    Compound directions are expanded to the basic directions before
    checking for duplicates.
    """

    _filter_type = cqltypes.FilterType.SET


class ReadFile(structure.Argument):
    """Represent 'readfile' string filter."""

    _filter_type = cqltypes.FilterType.STRING


class RemoveComment(structure.NoArgumentsFilter):
    """Represent 'removecomment' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Result(structure.Argument):
    """Represent 'result' logical filter.

    The 'result' keyword also appears in the parameter module.
    """

    _filter_type = cqltypes.FilterType.LOGICAL


# Definition of ReverseColor derived from:
# 'reversecolor "a"' gets a message saying the attempt to match the position
#     to a string literal is probably inadvertent, and stops running query.
# 'v=reversecolor "a"' gets CQL syntax error: right hand side is not a
#     'set','numeric', 'position', or 'string', filter.
# 'reversecolor position 0' matches.
# 'v=reversecolor position 0' gets CQL syntax error: right hand side is not a
#     'set', 'numeric', 'position', or 'string', filter.
# 'reversecolor 0' gets a message saying the attempt to match the position
#     against the number is not technically an error, and stops running the
#     query.  A different outcome from 'shift' but effect here is same.
# 'reversecolor int "0"' matches.
# v='reversecolor int "0"' matches and implies this 'reversecolor' is a
#     'numeric' filter.
# 'reversecolor K' matches.
# v='reversecolor K' matches and implies this 'reversecolor' is a 'set'
#     filter.
# 'reversecolor true' matches.
# 'v=reversecolor true' gets CQL syntax error: right hand side is not a
#     'set', 'numeric', 'position', or 'string', filter.
class ReverseColor(TransformFilterType, structure.Argument):
    """Represent 'reversecolor' filter of all types."""

    _precedence = cqltypes.Precedence.P30

    # CQL documentation for reversecolor does not say a count parameter is
    # accepted, and the '-parse' option and evaluation agree.  (See how
    # this is covered for rotate45 and rotate90.)  The non-definitive
    # 'table of filters' says a count parameter is accepted.
    # The shifts take count parameter while directions take range parameter.


class Right(structure.Argument):
    """Represent 'right' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class RightParameter(structure.DirectionParameter):
    """Represent 'right' transform filter direction parameter."""


def right(match_=None, container=None):
    """Return Right or RightParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return RightParameter(match_=match_, container=container)
    return Right(match_=match_, container=container)


# See comment preceding Shift: same seen for Rotate45.
class Rotate45(TransformFilterType, structure.Argument):
    """Represent 'rotate45' filter of all types."""

    _precedence = cqltypes.Precedence.P30


# See comment preceding Shift: same seen for Rotate90.
class Rotate90(TransformFilterType, structure.Argument):
    """Represent 'rotate90' filter of all types."""

    _precedence = cqltypes.Precedence.P30


class Secondary(structure.NoArgumentsFilter):
    """Represent 'secondary' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class SecondaryParameter(structure.NoArgumentsParameter):
    """Represent 'secondary' parameter to line, and move, filters."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, (Line, Move, Path))


def secondary(match_=None, container=None):
    """Return Secondary or SecondaryParameter instance.

    'secondary' may be either a logical filter or a parameter.  CQL does not
    treat the second 'secondary' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while not isinstance(node, (Line, Move, querycontainer.QueryContainer)):
        if not node.full():
            break
        node = node.parent
    if isinstance(node, Line):
        if isinstance(node.children[-1], (ArrowBackward, ArrowForward)):
            return Secondary(match_=match_, container=container)
    if len(node.children) == 0:
        return SecondaryParameter(match_=match_, container=container)
    if not node.children[-1].is_parameter:
        return Secondary(match_=match_, container=container)
    return SecondaryParameter(match_=match_, container=container)


class SetTag(structure.ParenthesizedArguments):
    """Represent 'settag' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


# See comment preceding Shift: same seen for ShiftHorizontal.
class ShiftHorizontal(TransformFilterType, structure.Argument):
    """Represent 'shifthorizontal' filter of all types."""

    _precedence = cqltypes.Precedence.P30


# See comment preceding Shift: same seen for ShiftVertical.
class ShiftVertical(TransformFilterType, structure.Argument):
    """Represent 'shiftvertical' filter of all types."""

    _precedence = cqltypes.Precedence.P30


# Definition of Shift derived from:
# 'shift "a"' gets a message saying the attempt to match the position to
#     a string literal is probably inadvertent, and stops running query.
# 'v=shift "a"' gets CQL syntax error: right hand side is not a
#     'set','numeric', 'position', or 'string', filter.
# 'shift position 0' matches.
# 'v=shift position 0' gets CQL syntax error: right hand side is not a
#     'set', 'numeric', 'position', or 'string', filter.
# 'shift 0' gets CQL syntax error: filter expected.
# 'shift int "0"' matches.
# v='shift int "0"' matches and implies this 'shift' is a 'numeric' filter.
# 'shift K' matches.
# v='shift K' matches and implies this 'shift' is a 'set' filter.
# 'shift true' matches.
# 'v=shift true' gets CQL syntax error: right hand side is not a
#     'set', 'numeric', 'position', or 'string', filter.
class Shift(TransformFilterType, structure.Argument):
    """Represent 'shift' filter of all types."""

    _precedence = cqltypes.Precedence.P30


class SideToMove(structure.NoArgumentsFilter):
    """Represent 'sidetomove' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class SingleColor(structure.NoArgumentsParameter):
    """Represent 'singlecolor' parameter to 'line' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Line)


# Refers to an 'implicit search parameter' in table of filters.
# In tagqueryfilters.html it is referred to as an 'implicit search filter'.
class Site(structure.ImplicitSearchFilter):
    """Represent 'site' string filter."""

    _filter_type = cqltypes.FilterType.STRING


class Sort(structure.Argument):
    """Represent 'sort' and 'sort min' numeric or string filter.

    The 'string' in  _accepted_parameters is not a CQL keyword but the
    name of the pattern which spots quoted strings in a *.cql file.
    """

    _filter_type = cqltypes.FilterType.NUMERIC | cqltypes.FilterType.STRING
    _accepted_parameters = frozenset(("min", "string"))
    # Precedence removed from 'sort' because it applies to 'body of sort'
    # according to Table of Precedences.
    # At time of writing removing precedence makes 'sort' interact with
    # infix filters correctly: a case where assigning the precedence to
    # the body filter matters has not yet been seen.
    # Are 'echo', 'piece', and 'square', the same?  They are listed with
    # 'sort'.

    @property
    def filter_type(self):
        """Return filter type of last child if BraceLeft completed."""
        if self.completed:
            return self.children[-1].filter_type
        return super().filter_type


def sort(match_=None, container=None):
    """Return Sort or HHDBToken instance."""
    if hhdb.is_hhdb_token_accepted_by(container.cursor):
        return hhdb.HHDBToken(match_=match_, container=container)
    return Sort(match_=match_, container=container)


class Southeast(structure.Argument):
    """Represent 'southeast' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class SoutheastParameter(structure.DirectionParameter):
    """Represent 'southeast' transform filter direction parameter."""


def southeast(match_=None, container=None):
    """Return Southeast or SoutheastParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return SoutheastParameter(match_=match_, container=container)
    return Southeast(match_=match_, container=container)


class Southwest(structure.Argument):
    """Represent 'southwest' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class SouthwestParameter(structure.DirectionParameter):
    """Represent 'southwest' transform filter direction parameter."""


def southwest(match_=None, container=None):
    """Return Southwest or SouthwestParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return SouthwestParameter(match_=match_, container=container)
    return Southwest(match_=match_, container=container)


class Sqrt(structure.Argument):
    """Represent 'sqrt' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P90


class Square(structure.VariableName, structure.Argument):
    """Represent 'square', without 'all' parameter, set filter.

    The optional 'all' keyword is not present,

    The value of a square variable is a Set filter.
    """

    _precedence = cqltypes.Precedence.P30
    _child_count = 2

    def __init__(self, match_=None, container=None):
        """Delegate then register the set variable name for square filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["square"]
        self._register_variable_type(cqltypes.VariableType.SET)
        self.set_types(cqltypes.VariableType.SET, cqltypes.FilterType.SET)


class SquareAll(structure.VariableName, structure.Argument):
    """Represent 'square', with 'all' parameter, logical filter.

    The optional 'all' keyword is present,

    The value of a square all variable is a Set filter.
    """

    _precedence = cqltypes.Precedence.P30
    _child_count = 2

    def __init__(self, match_=None, container=None):
        """Delegate then register set variable name for squareall filter."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["square"]
        self._register_variable_type(cqltypes.VariableType.SET)
        self.set_types(cqltypes.VariableType.SET, cqltypes.FilterType.SET)


def square(match_=None, container=None):
    """Return Square or SquareAll instance."""
    if "all" in match_.group().split():
        return SquareAll(match_=match_, container=container)
    return Square(match_=match_, container=container)


class Stalemate(structure.NoArgumentsFilter):
    """Represent 'stalemate' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class StrParentheses(structure.ParenthesizedArguments):
    """Represent 'str' string filter with parentheses."""

    _filter_type = cqltypes.FilterType.STRING


class Str(structure.Argument):
    """Represent 'str' string filter without parentheses."""

    _filter_type = cqltypes.FilterType.STRING


class Tag(structure.Argument):
    """Represent 'tag' string filter."""

    _filter_type = cqltypes.FilterType.STRING


class Terminal(structure.NoArgumentsFilter):
    """Represent 'terminal' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Then(structure.Complete):
    """Represent 'then' keyword in 'if' filter.

    At versions of CQL earlier than 6.2 the 'then' parameter was mandatory.

    At version 6.2 the 'then' keyword is deprecated.
    """

    _precedence = (
        cqltypes.Precedence.P30
    )  # Does this matter?  Reference is 'if/then/else'.

    def place_node_in_tree(self):
        """Delegate then verify tree structure and set cursor as parent.

        Instances of Then are treated as whitespace, partly because 'then'
        is deprecated, and partly because it is not needed.

        """
        super().place_node_in_tree()
        # This stops '<non if> ... then'.
        # At time of writing same test as would be in
        # self.is_parameter_accepted_by_filter() called by
        # self.raise_if_name_parameter_not_for_filters()
        # but 'then' keyword is in a category of it's own.
        if not isinstance(self.parent, If):
            raise basenode.NodeError(
                self.__class__.__name__
                + " instance is not associated with "
                + self.parent.__class__.__name__
                + " instance"
            )
        # This stops 'if then' and 'if <condition> <action> then' but not
        # 'if <condition> then then <action>'.
        if len(self.parent.children) != 2:
            raise basenode.NodeError(
                self.__class__.__name__
                + " instance is only allowed after the condition of a "
                + self.parent.__class__.__name__
                + " instance"
            )
        # 'then then' occurs if there is an unbroken sequence of whitespace
        # back to a 'then'.
        container = self.container
        start = self.match_.start()
        for item in reversed(container.whitespace):
            if not isinstance(item, (WhiteSpace, EndOfLine, Then)):
                break
            if start != item.match_.end():
                break
            if isinstance(item, Then):
                raise basenode.NodeError(
                    self.__class__.__name__
                    + " instance is separated from previous "
                    + item.__class__.__name__
                    + " instance only by whitespace"
                )
            start = item.match_.start()
        container.whitespace.append(self.parent.children.pop())
        container.cursor = self.parent
        self.parent = None


def is_through_parameter_accepted_by(node):
    """Return True if node accepts through parameter."""
    return isinstance(node, Pin)


class Through(structure.ParameterArgument):
    """Represent 'through' parameter to 'pin' filter."""

    _precedence = cqltypes.Precedence.P200

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_through_parameter_accepted_by(self.parent)


def is_title_parameter_accepted_by(node):
    """Return True if node accepts title parameter."""
    return isinstance(node, Path)


class Title(structure.ParameterArgument):
    """Represent 'title' parameter to 'path' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_title_parameter_accepted_by(self.parent)


class To(structure.NoArgumentsFilter):
    """Represent 'to' set filter."""

    _filter_type = cqltypes.FilterType.SET


def is_to_parameter_accepted_by(node):
    """Return True if node accepts to parameter."""
    return isinstance(node, (Move, Pin))


class ToParameter(MoveParameterImpliesSet):
    """Represent 'to' parameter of 'pin' and 'move' filters.

    'to' and 'pin to to', are accepted by cql-6.2 parser; but 'pin to' and
    'pin to to from' give a syntax error.
    """

    _precedence = cqltypes.Precedence.P200  # 'pin' filter only.

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_to_parameter_accepted_by(self.parent)


def to(match_=None, container=None):
    """Return To or ToParameter instance.

    'to' may be either a set filter or a parameter.  CQL does not
    treat the second 'to' in a sequence of parameters as a filter:
    but as a second statement of the parameter which is treated as a
    syntax error for some filters.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if is_to_parameter_accepted_by(node):
            return ToParameter(match_=match_, container=container)
        node = node.parent
    return To(match_=match_, container=container)


# pylint C0103 naming style.  'true' is a CQL keyword which is represented
# as a class with the same capitalized name, and suffix '_' to avoid clash
# with Python keyword 'True'.
# In cases where CQL does not define a name (symbols) the Python class name
# is chosen to avoid similar problems.
class True_(structure.NoArgumentsFilter):
    """Represent 'true' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Try(structure.NoArgumentsFilter):
    """Represent 'try' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class TypeName(structure.Argument):
    """Represent 'typename' string filter."""

    _filter_type = cqltypes.FilterType.STRING


class Type(structure.Argument):
    """Represent 'type' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P150


class Unbind(structure.Argument):
    """Represent 'unbind' logical filter.

    'unbind' removes the value associated with a variable, dictionary or
    dictionary entry, but does not affect the variable or dictionary type.
    """

    _filter_type = cqltypes.FilterType.LOGICAL


class UpperCase(structure.Argument):
    """Represent 'uppercase' string filter."""

    _filter_type = cqltypes.FilterType.STRING
    _precedence = cqltypes.Precedence.P120


class Up(structure.Argument):
    """Represent 'up' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class UpParameter(structure.DirectionParameter):
    """Represent 'up' transform filter direction parameter."""


def up(match_=None, container=None):
    """Return Up or UpParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return UpParameter(match_=match_, container=container)
    return Up(match_=match_, container=container)


class Variation(structure.NoArgumentsFilter):
    """Represent 'variation' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


def variation(match_=None, container=None):
    """Return Variation or HHDBToken instance."""
    if hhdb.is_hhdb_token_accepted_by(container.cursor):
        return hhdb.HHDBToken(match_=match_, container=container)
    return Variation(match_=match_, container=container)


def is_verbose_parameter_accepted_by(node):
    """Return True if node accepts verbose parameter."""
    return isinstance(node, Path)


class Verbose(structure.NoArgumentsParameter):
    """Represent 'verbose' parameter of 'path' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_verbose_parameter_accepted_by(self.parent)


class Vertical(structure.Argument):
    """Represent 'vertical' set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P210


class VerticalParameter(structure.DirectionParameter):
    """Represent 'vertical' transform filter direction parameter."""


def vertical(match_=None, container=None):
    """Return Vertical or VerticalParameter instance."""
    if structure.is_direction_parameter_accepted_by(container.cursor):
        return VerticalParameter(match_=match_, container=container)
    return Vertical(match_=match_, container=container)


class VirtualMainLine(structure.NoArgumentsFilter):
    """Represent 'virtualmainline' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class While(structure.ParenthesizedArguments):
    """Represent 'while' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _child_count = 2

    def complete(self):
        """Override to use basenode.BaseNode version of complete method."""
        return super(structure.CQLObject, self).complete()

    def full(self):
        """Override to use basenode.BaseNode version of full method."""
        return super(structure.CQLObject, self).full()


# 'white' is defined as a numeric filter with value 1 on the 'white.html'
# page referenced from the table of filters at 'filtertable.html'.
# 'white' is referred to as a 'built-in tag query filter' on the
# 'tagqueryfilters.html' page, but it seems be correspond to 'player white'
# in the table of filters.
# 'white' is not described as having an 'implicit search parameter' in the
# table of filters.
# On the 'implicitsearch.html' page it is called 'white', but the example
# 'player white' suggests it is describing the 'player white' filter from
# the table of filters.
class White(structure.CQLObject):
    """Represent 'white' numeric filter with value 1."""

    _filter_type = cqltypes.FilterType.NUMERIC


class WriteFile(structure.ParenthesizedArguments):
    """Represent 'writefile' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class WTM(structure.NoArgumentsFilter):
    """Represent 'wtm' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class XRay(structure.ParenthesizedArguments):
    """Represent 'xray' set filter."""

    _filter_type = cqltypes.FilterType.SET


class Year(structure.NoArgumentsFilter):
    """Represent 'year' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC


class PieceDesignator(structure.NoArgumentsFilter):
    """Represent piece designator.

    The simplest piece designator has one piece and one square, such as
    'Ba4'.  'R' is more complex since it means 'Ra1' or 'Ra2' or ... or
    'Rh7' or 'Rh8'; a white rook on one or more squares.  'qc-e4-6' is
    more complex since it means 'qc4' or 'qd4' or ... or 'qe5' or 'qe6';
    a black queen on one or more squares in the rectangle bounded by
    opposite corners 'c4' and 'e6'.  There are other ecceptable forms.
    """

    _filter_type = cqltypes.FilterType.SET


class ResultArgument(structure.NoArgumentsFilter):
    """Represent the argument of the result filter.

    Value is '1-0', '0-1', or '1/2-1/2'.
    """


def is_range_parameter_accepted_by(node):
    """Return True if node accepts range parameter."""
    return isinstance(
        node,
        (
            AnyDirection,
            ConsecutiveMoves,
            Find,
            Diagonal,
            Down,
            Horizontal,
            Left,
            Line,
            MainDiagonal,
            Northeast,
            Northwest,
            OffDiagonal,
            Orthogonal,
            Right,
            Southeast,
            Southwest,
            Up,
            Vertical,
        ),
    )


class RangeInteger(structure.Complete):
    """Represent a positive or negative integer of a range parameter."""

    _is_parameter = True

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_range_parameter_accepted_by(self.parent)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class Integer(structure.Complete):
    """Represent a positive or negative integer numeric set."""

    _filter_type = cqltypes.FilterType.NUMERIC

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


def is_too_many_range_integers(node):
    """Return True if there is more than one integer parameter in node.

    Adding this integer as a parameter will mean there are too many.
    """
    return (
        len(
            [
                c
                for c in node.children
                if isinstance(c, (RangeInteger, RangeVariable))
            ]
        )
        > 1
    )


def is_range_start_or_continuation(node):
    """Return True if a range can be started or continuesd in node.

    True can be returned if there is no range integer present or the
    most recent child ia a range integer.
    """
    if (
        len(
            [
                c
                for c in node.children
                if isinstance(c, (RangeInteger, RangeVariable))
            ]
        )
        == 0
    ):
        return True
    return isinstance(node.children[-1], (RangeInteger, RangeVariable))


def integer(match_=None, container=None):
    """Return Integer or RangeInteger, instance."""
    node = container.cursor
    while True:
        if node is None:
            break
        if is_range_parameter_accepted_by(node):
            if is_too_many_range_integers(node):
                return Integer(match_=match_, container=container)
            if is_range_start_or_continuation(node):
                return RangeInteger(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return Integer(match_=match_, container=container)


class RangeVariable(structure.Complete, structure.VariableName):
    """Represent an integer variable in a range parameter.

    CQL-6.2 rejects 'v=1 up v v v' but accepts 'v=1 z=k up v v z',
    'v=1 z=k up v v z v', and 'v=1 z=k up v k', and so forth but
    'z=k up int "4" z' and 'up #k z' are rejected while
    'v=int "4" z=k up v z' and 'v=#k z=k up v z' are accepted.
    """

    _is_parameter = True

    def __init__(self, match_=None, container=None):
        """Delegate then register the variable name."""
        super().__init__(match_=match_, container=container)
        self.name = match_.groupdict()["variable"]
        self._register_variable_type(cqltypes.VariableType.NUMERIC)
        self.set_types(
            cqltypes.VariableType.NUMERIC, cqltypes.FilterType.NUMERIC
        )

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_range_parameter_accepted_by(self.parent)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class Variable(structure.Complete, structure.VariableName):
    """Represent the name of a variable filter of various types.

    If the variable already exists set this instance to same type as the
    existing reference.

    The variable types, with their filter type in parentheses, are:
        numeric (numeric)
        set (set)
        piece (set)
        string (string)
        position (position)

    The value of a variable is a Numeric, Position, Set, or String, filter.

    """

    def __init__(self, match_=None, container=None):
        """Delegate then register the variable name."""
        super().__init__(match_=match_, container=container)
        groupdict = match_.groupdict()
        # The "variable" reference must be first to allow for variables
        # defined by 'echo' pattern.
        self.name = groupdict["variable"] or groupdict["variable_assign"]
        self._register_variable_type(cqltypes.VariableType.ANY)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self

    def is_variable(self):
        """Override and return True."""
        return True


def variable(match_=None, container=None):
    """Return Variable, RangeVariable, PieceVariable, or Dictionary instance.

    A Dictionary instance is returned only if the name is already defined
    as a dictionary.

    Function definition and call variables are detected by patterns tuned
    to functions.

    Assignment to variables is detected by patterns tuned to the piece,
    square, and plain variable, cases.

    """
    name = match_.groupdict()["variable"]
    if hhdb.is_hhdb_token_accepted_by(container.cursor):
        if name in hhdb.KEYWORD_VARIABLES:
            return hhdb.HHDBToken(match_=match_, container=container)
    definitions = container.definitions
    if name in definitions:
        definition_type = definitions[name].definition_type
        if definition_type is cqltypes.DefinitionType.DICTIONARY:
            return Dictionary(match_=match_, container=container)
        variable_type = definitions[name].variable_type
        if variable_type is cqltypes.VariableType.NUMERIC:
            if is_range_parameter_accepted_by(container.cursor):
                if is_too_many_range_integers(container.cursor):
                    return Variable(match_=match_, container=container)
                if is_range_start_or_continuation(container.cursor):
                    return RangeVariable(match_=match_, container=container)
        if variable_type is cqltypes.VariableType.PIECE:
            return PieceVariable(match_=match_, container=container)
    return Variable(match_=match_, container=container)


def variable_assign(match_=None, container=None):
    """Return Variable instance is assign context.

    Piece, square, and persistent, assignments are detected by patterns
    tuned to those cases.

    Other references to variables, of all kinds, are detected by the
    VARIABLE pattern.

    """
    definitions = container.definitions
    name = match_.groupdict()["variable_assign"]
    if name in definitions:
        definition_type = definitions[name].definition_type
        if definition_type is not cqltypes.DefinitionType.VARIABLE:
            raise basenode.NodeError(
                container.cursor.__class__.__name__
                + ": cannot assign to a '"
                + definition_type.name.lower()
                + "' as a plain variable"
            )
        variable_type = definitions[name].variable_type
        if variable_type is cqltypes.VariableType.PIECE:
            raise basenode.NodeError(
                container.cursor.__class__.__name__
                + ": cannot assign to a '"
                + variable_type.name.lower()
                + "' variable as a plain variable"
            )
    return Variable(match_=match_, container=container)


# '\' is used in three ways,
#   to indicate certain single-character strings such as '\n'
#   to indicate the value of, or index into source string of, capturing group
#   to indicate special characters in regular expressions
# All these are represented by specific classes: a bare '\' indicates an
# error.
class Backslash(structure.CQLObject):
    r"""Represent '\' not caught elsewhere for specific purposes."""

    def place_node_in_tree(self):
        r"""Delegate then raise NodeError because bare '\' not allowed."""
        super().place_node_in_tree()
        raise basenode.NodeError(r"Unexpected bare '\' found")


# See also AllSquares.
class AnySquare(structure.NoArgumentsFilter):
    """Represent '.' set filter.

    It is a piece designator meaning all squares.

    In CQL() parameters it appears in file names unprotected by quotes.
    """

    _filter_type = cqltypes.FilterType.SET


# '[' and ']' are used in five ways,
#   textual regular expressions: caught in String
#   piece designators: caught in piece designator classes
#   empty set: caught in EmptySet
#   string index: caught by
#      '[', <numeric filter> child, ':' child, <numeric filter> child, ']'.
#      where [0], [0:], [:0], and [0:0], demonstrate the allowed forms.
#   dictionary key where can be string, number, position, or set of squares.
#      at 6.1 key was string only, but 6.2 changes allowed types.
# The string index form implies there are two ways of using ':'.
# BracketLeft has to be added to the classes that halt a search for close
# '(' and '{' in their various forms.


# BracketLeft is called 'Slice' (which is what it is) by CQLi, which treats
# it as infix.
class BracketLeft(structure.CompleteBlock, structure.InfixLeft):
    """Represent '[' which starts a string index operator."""

    # Do not override _child_count even though '[a:b:c]' is a possible
    # extension.  '[' is ended by ']' as indicated by the override of
    # complete() and full().

    _precedence = cqltypes.Precedence.P220


def bracket_left(match_=None, container=None):
    """Return Slice or Key instance, or raise NodeError.

    '[...]' is used in five ways,
      textual regular expressions: caught in String
      piece designators: caught in piece designator classes
      empty set: caught in EmptySet
      string index: caught by
        '[', <numeric filter> child, ':' child, <numeric filter> child, ']'.
        where [0], [0:], [:0], and [0:0], demonstrate the allowed forms.
      dictionary key where can be string, number, position, or set of squares.
        at 6.1 key was string only, but 6.2 changes allowed types.

    Textual reguar expressions, piece designators, and empty set, are caught
    in String, piece designator, and EmptySet, classes.

    """
    return BracketLeft(match_=match_, container=container)


class BracketRight(RightCompoundPlace):
    """Close BracketLeft and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then verify cursor is a BracketLeft instance."""
        super().place_node_in_tree()
        assert isinstance(self.container.cursor, BracketLeft)


def bracket_right(match_=None, container=None):
    """Return BracketRight instance."""
    node = container.cursor
    while node:
        if isinstance(node, BracketLeft):
            return BracketRight(match_=match_, container=container)
        if isinstance(node, ParenthesisLeft):
            raise basenode.NodeError(
                node.__class__.__name__
                + ": cannot close a '(' parenthesized block with ']'"
            )
        if isinstance(
            node,
            (ConstituentParenthesisLeft, LineConstituentParenthesisLeft),
        ):
            raise basenode.NodeError(
                node.__class__.__name__
                + ": cannot close a '(' top level constituent with ']'"
            )
        if isinstance(node, BraceLeft):
            raise basenode.NodeError(
                node.__class__.__name__
                + ": cannot close a '{' compound filter with ']'"
            )
        if isinstance(node, ConstituentBraceLeft):
            raise basenode.NodeError(
                node.__class__.__name__
                + ": cannot close a '{' constituent filter with ']'"
            )
        if isinstance(node, structure.ParenthesizedArguments):
            raise basenode.NodeError(
                node.__class__.__name__
                + ": cannot close parenthesized arguments with ']'"
            )
        node = node.parent
    raise basenode.NodeError(
        "Unexpected " + str(node) + " found while trying to match a ']'"
    )


class Colon(structure.InfixRight):
    """Represent ':' filter between a position filter and a filter."""

    _filter_type = cqltypes.FilterType.ANY
    _precedence = cqltypes.Precedence.P230  # Reference says ':', no context.

    def verify_children_and_set_filter_type(self, set_node_completed=False):
        """Delegate then adjust filter type if complete or full.

        This method should be called only from a place_node_in_tree method.

        """
        if self.container.function_body_cursor is not None:
            return
        super().verify_children_and_set_filter_type(
            set_node_completed=set_node_completed
        )
        self.filter_type = self.children[-1].filter_type

    def place_node_in_tree(self):
        """Delegate then verify first child is a Position filter."""
        super().place_node_in_tree()
        assert self.children
        if self.container.function_body_cursor is not None:
            return
        if self.children[0].filter_type is not cqltypes.FilterType.POSITION:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": lhs filter type must be "
                + str(cqltypes.FilterType.POSITION)
                + " but actual filter is "
                + self.children[0].__class__.__name__
                + " of type "
                + str(self.children[0].filter_type)
            )


class ColonStringIndex(structure.CQLObject):
    """Represent ':' string index operator between two numeric filters.

    CQL-6.2 rejects 'cql()"abc"[1:#q]' and 'cql()"abc"[1:q>1]' but
    accepts 'cql()"abc"[1:(#q)]' and 'cql()"abc"[1:(q>1)]'.

    CQLi-1.0.3 accepts all four.

    At present this module does the reverse to CQL-6.2 on all four.

    At present this module allows whitespace without a ':' like '[1 2]'.

    'cql()"abc"[1:{#q}]' and 'cql()"abc"[1:{q>1}]' are accepted by this
    module, CQL-6.2, and CQLi-1.0.3.

    The CQL and CQLi samples assume use of the command line options '-input',
    '-output' and '-parse'.
    """

    _precedence = cqltypes.Precedence.P220  # Reference says ':', no context.

    def place_node_in_tree(self):
        """Override, verify name parameter then move to whitespace."""
        self.raise_if_name_parameter_not_for_filters()
        self.container.whitespace.append(self.parent.children.pop())
        self.parent = None

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Integer) and isinstance(
            self.parent.parent, BracketLeft
        )


def colon(match_=None, container=None):
    """Return True if parent of ':' is '['."""
    if isinstance(container.cursor.parent, BracketLeft):
        return ColonStringIndex(match_=match_, container=container)
    return Colon(match_=match_, container=container)


class Intersection(structure.InfixLeft):
    """Represent '&' (∩) of two Set or two Position filters.

    Intersection itself is a Set filter.
    """

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P170

    # It did not seem possible to do the children verification in
    # verify_children_and_set_filter_type() method for BraceLeft so
    # switch to verifying in the filter_type property.  At time of writing
    # the 'BraceLeft' parsing failures are fixed but others, where
    # filter type is not yet handled, still fail parsing with the addition
    # of child verification.  It is assumed possible the children of a node
    # may not be in their completed configuration if verification is done
    # in verify_children_and_set_filter_type().
    @property
    def filter_type(self):
        """Verify children are both Set filters or both Position filters.

        This method should be called only from a place_node_in_tree method.
        """
        children = self.children
        filtertype = cqltypes.FilterType
        for child in children[:2]:
            if not child.filter_type & (filtertype.SET | filtertype.POSITION):
                raise basenode.NodeError(
                    self.__class__.__name__
                    + ": cannot apply intersection to '"
                    + str(child.filter_type)
                    + "' filter '"
                    + child.__class__.__name__
                    + "')"
                )
        if not children[0].filter_type & children[1].filter_type:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": both lhs and rhs filters must be same type, "
                + " but lhs filter is '"
                + str(children[0].filter_type)
                + "' and rhs filter is '"
                + str(children[1].filter_type)
                + "')"
            )
        return self._filter_type


class LT(structure.Compare, structure.InfixRight):
    """Represent '>' numeric or string filter between two filters."""

    _precedence = cqltypes.Precedence.P80


class GT(structure.Compare, structure.InfixRight):
    """Represent '>' numeric or string filter between two filters."""

    _precedence = cqltypes.Precedence.P80


# The '*' in 'line --> not move from Front*', 'Front' is a piece variable
# in this example, is the regular expression repetition operator not the
# arithmetic multiplication operator.
def _is_repeat_0_or_1_to_many(container):
    """Return True if token is at top level in a Line or Path filter.

    A completed ConstituentBraceLeft counts as the top level of a Line or
    Path filter, along with a Line or Path instance as the cursor.

    """
    node = container.cursor
    while True:
        if node is None:
            return False
        if (
            isinstance(
                node,
                (
                    ConstituentBraceLeft,
                    ConstituentParenthesisLeft,
                    LineConstituentParenthesisLeft,
                ),
            )
            and node.complete()
        ):
            return True
        if isinstance(node, (Path, Line)):
            return True
        if not node.full():
            return False
        node = node.parent


# This has same effect as WildcardPlus.
class PlusRepeat(RepeatConstituent):
    """Represent '+' repetition operation on a constituent filter.

    The 'path' and 'line' filters use constituent filters.
    """

    _precedence = cqltypes.Precedence.P20


class Plus(structure.InfixLeft):
    """Represent '+' filter between two numeric or string filters."""

    _filter_type = cqltypes.FilterType.NUMERIC | cqltypes.FilterType.STRING
    _precedence = cqltypes.Precedence.P110


def plus(match_=None, container=None):
    """Return a Plus, or PlusRepeat, instance depending on context of '+'."""
    if _is_repeat_0_or_1_to_many(container):
        return PlusRepeat(match_=match_, container=container)
    return Plus(match_=match_, container=container)


# This has same effect as WildcardStar.
class StarRepeat(RepeatConstituent):
    """Represent '*' repetition operation on a constituent filter.

    The 'path' and 'line' filters use constituent filters.
    """

    _precedence = cqltypes.Precedence.P20


class Star(structure.InfixLeft):
    """Represent '*' filter between two numeric filters."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P140


def star(match_=None, container=None):
    """Return a Star, or StarRepeat, instance depending on context of '*'."""
    if _is_repeat_0_or_1_to_many(container):
        return StarRepeat(match_=match_, container=container)
    return Star(match_=match_, container=container)


class Modulus(structure.InfixLeft):
    """Represent '%' filter between two numeric filters."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P140


class Divide(structure.InfixLeft):
    """Represent '/' filter between two numeric filters."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P140


class Minus(structure.InfixLeft):
    """Represent '-' filter between two numeric filters, eg '1 + 2'."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P110


class UnaryMinus(structure.Argument):
    """Represent '-' filter before a numeric filter, eg 'v = -1'."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P130


def minus(match_=None, container=None):
    """Return Minus or UnaryMinus instance."""
    # Start picking UnaryMinus cases.
    if isinstance(container.cursor, structure.Infix):
        return UnaryMinus(match_=match_, container=container)
    return Minus(match_=match_, container=container)


class Complement(structure.Argument):
    """Represent '~' filter on a set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P180


class Union(structure.InfixLeft):
    """Represent '|' filter between two set filters."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P160


# Because 'cql() variable=1' is ok but 'cql() variable' is not ok. (? later)
# BracketLeft added into tests to allow 'D[pathcount]=to', for example, to
# be accepted.  More work needed because there are no restrictions on what
# is inside the '[]'.
class Assign(structure.MoveInfix):
    """Represent '=', variable assignment, logical filter.

    CQLi-1.0.3 describes '=' as 'Boolean' with the RHS as a 'Numeric',
    'Position', 'Set', or 'String', filter.

    Note CQL-6.2 accepts 'cql()shift First=k', but CQLi rejects this
    saying 'left operand to assignment operator' must be an identifier
    after warning 'shift' is superfluous.  The error markings suggest
    'shift First' is seen as an invalid identifier.  However
    'cql()shift (First=k)' is fine and verifies 'shift' is a Logical
    filter, from '=', not a Set filter, from 'k', here.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # pylint R0912 too many branches.
    # Sequence of 'elif' clauses changed to 'if ... return'.  This is
    # clearer but gains a 'pylint R0911 too many returns' report.
    # The block of 'isinstance(lhs, structure.VariableName)' tests is
    # moved to _verify_children_lhs_variable_name_and_set_types() method
    # getting rid of both pylint reports.
    def verify_children_and_set_filter_type(self, set_node_completed=False):
        """Delegate then adjust filter type if complete or full.

        This method should be called only from a place_node_in_tree method.

        """
        if self.container.function_body_cursor is not None:
            return
        super().verify_children_and_set_filter_type(
            set_node_completed=set_node_completed
        )
        lhs = self.children[0]
        assert isinstance(lhs, (structure.VariableName, BracketLeft))
        rhs = self.children[1]
        if isinstance(rhs, structure.VariableName):
            defn = self.container.definitions
            variable_type = defn[rhs.name].variable_type
            if variable_type is cqltypes.VariableType.PIECE:
                if (
                    defn[lhs.name].variable_type
                    is not cqltypes.VariableType.PIECE
                ):
                    variable_type = cqltypes.VariableType.SET
            # Hack to get serialpin examples prior to CQL-6.2 past a
            # parsing failure at 'piece CurrentPinner=Pinner' where
            # 'Pinner' is thought to be ANY rather than PIECE from
            # the 'piece Pinner' declaration.
            # Getting variable type and filter correct is thought to
            # be a major task by itself.
            if not (
                defn[lhs.name].variable_type is cqltypes.VariableType.PIECE
                and variable_type is cqltypes.VariableType.ANY
            ):
                lhs.set_types(
                    variable_type,
                    defn[rhs.name].filter_type,
                )
            return
        if isinstance(lhs, structure.VariableName):
            if self._verify_children_lhs_variable_name_and_set_types(lhs, rhs):
                return
        if isinstance(rhs, (structure.InfixLeft, structure.InfixRight)):
            # Partial solution to filter type resolution when assigning
            # infix operator value to variable.
            # May not be possible to move this to Infix.complete() as
            # it stands because the three objects involved may be
            # allowed to have different filter types depending on
            # operator.
            def child_in_children_filter_type_fit(node):
                for child in node.children:
                    if child_in_children_filter_type_fit(child):
                        return True
                if node.filter_type in lhs.filter_type:
                    return True
                return False

            if not child_in_children_filter_type_fit(rhs):
                raise basenode.NodeError(
                    self.__class__.__name__
                    + ": unable to partially match RHS filter types "
                    + "with filter type of variable named '"
                    + lhs.name
                    + "')"
                )
            return
        if isinstance(rhs, FunctionCall):
            # Partial solution to filter type resolution when assigning
            # infix operator value to variable.
            # It may not be possible to do more because the filter type
            # of the function call may depend on the interaction between
            # filter types of function arguments and the function body.
            return
        if isinstance(lhs, structure.VariableName):
            raise basenode.NodeError(
                self.__class__.__name__
                + ": only set, numeric, position, or string filters "
                + "can be assigned to a variable (named '"
                + lhs.name
                + "')"
            )

    def place_node_in_tree(self):
        """Delegate then vefify LHS is a variable."""
        # It is not clear the plausible replacement code following this
        # super() call is progress.
        super().place_node_in_tree()
        # self.children.append(self.parent)
        # del self.parent.children[-1]
        # self.parent = self.parent.parent
        # self.container.cursor = self
        if not isinstance(
            self.children[-1],
            (
                Variable,
                Persistent,
                PersistentQuiet,
                PieceVariable,
                BracketLeft,  # For slices and dictionary keys.
            ),
        ):
            raise basenode.NodeError(
                self.__class__.__name__
                + ": LHS object for '=' operator must be a variable"
            )
        if isinstance(self.parent, Assign):
            raise basenode.NodeError(
                self.__class__.__name__ + ": cannot chain variable assignment"
            )

    def _verify_children_lhs_variable_name_and_set_types(self, lhs, rhs):
        """Return True if lhs and rhs combination is valid."""
        if rhs.is_set_filter:
            lhs.set_types(
                self.container.definitions[lhs.name].variable_type,
                cqltypes.FilterType.SET,
            )
            return True
        if rhs.is_logical_filter:
            raise basenode.NodeError(
                self.__class__.__name__
                + ": cannot assign logical filter to variable "
                + "(named '"
                + lhs.name
                + "')"
            )
        if rhs.is_numeric_filter:
            lhs.set_types(
                cqltypes.VariableType.NUMERIC,
                cqltypes.FilterType.NUMERIC,
            )
            return True
        if rhs.is_string_filter:
            lhs.set_types(
                cqltypes.VariableType.STRING,
                cqltypes.FilterType.STRING,
            )
            return True
        if rhs.is_position_filter:
            lhs.set_types(
                cqltypes.VariableType.POSITION,
                cqltypes.FilterType.POSITION,
            )
            return True
        return False


class AssignPromotion(structure.Argument):
    """Represent '=T', construct in '--' and '[x]' filters.

    T is abbreviation of 'typename designator'.  Any piece name is accepted
    but colour is ignored.

    CQL-6.2 accepts any of the following as a typename designator:
        [QBRNKPAqbrnkpa_]
        [<unicode equivalents of [QBRNKPAqbrnkpa_]>]+
        "[QBRNKPAqbrnkpa_]+"
    where the middle one is a loose description of a pattern, and the other
    two are patterns, in a regular expression.
    """

    def place_node_in_tree(self):
        """Verify and apply node to tree then set cursor to self."""
        # This tests the situation if the following parent relationships
        # are applied.
        self._raise_if_node_not_child_of_filters("(", AnySquare)
        node = self.parent
        node.children[-1].parent = node.parent
        node.parent.children.append(node.children.pop())
        self.container.cursor = self


def assign(match_=None, container=None):
    """Return Assign or AssignPromotion instance."""
    if not container.target_move_interrupt:
        return AssignPromotion(match_=match_, container=container)
    return Assign(match_=match_, container=container)


class RepeatZeroOrOne(RepeatConstituent):
    """Represent '?' which means 0 or 1 repetitions of a constituent.

    Constituent is an element of the 'line' and 'path' filters.
    """


class CountFilter(structure.Argument):
    """Represent '#' numeric filter which is size of a set or string filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P100


class AnythingElse(structure.CQLObject):
    """Represent any (Python) str not caught by any other pattern.

    This construct also occurs in parameters module.
    """

    def place_node_in_tree(self):
        """Delegate then raise NodeError for unexpected token."""
        super().place_node_in_tree()
        raise basenode.NodeError(
            "Unexpected '" + self.match_.group() + "' found"
        )


class EndOfStream(structure.Complete):
    """Represent end of str containing CQL statement.

    The 'end of stream' construct also appears in the parameter module.
    """

    _is_allowed_first_object_in_container = True

    def place_node_in_tree(self):
        r"""Override, move to whitespace, finish final filter.

        'path' filter is completed if a Path instance is first non-full
        filter in ancestor chain.

        '///' filter is completed if a CommentSymbol instance is first
        non-full filter in ancestor chain.

        Raise NodeError exception if the node stack has not collapsed to
        the QueryContainer or CQL instance.

        """
        container = self.container
        container.whitespace.append(self.parent.children.pop())
        node = self.parent
        while node and node.full():
            node = node.parent
        if not isinstance(node, (Path, CommentSymbol)):
            pc_node = node
            while pc_node:
                pc_node = pc_node.parent
                if isinstance(pc_node, CommentSymbol):
                    raise basenode.NodeError(
                        container.cursor.__class__.__name__
                        + ": cannot complete earlier '///' filter"
                    )

        else:
            # EndOfStream completes 'path' and '///' filters.
            node.completed = True

        # EndOfStream completes 'line', 'move', and 'pin', filters.
        # The 'line' and 'move' filters are deprecated at CQL 6.2.
        if isinstance(node, (Line, Move, Pin)):
            node = node.parent
        else:
            node = self.parent

        while node and node.full():
            node.verify_children_and_set_filter_type()
            node = node.parent
        if not isinstance(
            node.parent, (querycontainer.QueryContainer, cql.CQL)
        ):
            raise basenode.NodeError("Unexpected end of statement found")
        self.parent = None
