# filters.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

# pylint C0302 too-many-lines.
# Think of good criteria for putting the definitions in one module rather
# than another.
# Perhaps the superclass signatures of the defined classes would do.
# The classes for the 'hhdb' filter are put in a separate module.
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
from . import querycontainer
from . import cql
from . import structure
from . import pattern
from . import elements

BLOCK_COMMENT = "block_comment"
END_OF_LINE = "end_of_line"
END_OF_STREAM = "end_of_stream"
LINE_COMMENT = "line_comment"
WHITESPACE = "whitespace"
_ALL_WHITESPACE = frozenset(
    (BLOCK_COMMENT, END_OF_LINE, END_OF_STREAM, LINE_COMMENT, WHITESPACE)
)
ARROW_BACKWARD = "arrow_backward"
ARROW_FORWARD = "arrow_forward"
BRACE_RIGHT = "brace_right"
BRACKET_RIGHT = "bracket_right"
PARENTHESIS_RIGHT = "parenthesis_right"
_ARROWS = frozenset((ARROW_BACKWARD, ARROW_FORWARD))
_BLOCK_ENDS = frozenset((BRACE_RIGHT, BRACKET_RIGHT, PARENTHESIS_RIGHT))

# Type designator string is limited to "QBRNKPAqbrnkpa_" characters.
_type_designator_string_re = re.compile(
    constants.PIECE_NAMES.join((r"^\"[", ']+"$'))
)

# Type designator piece designator must not specify squares.
_type_designator_piece_re = re.compile(elements.PIECE_OPTIONS)

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

# This gives misleading information about range integer derivation but
# fits the pattern to detect 'consecutivemoves' filters.
_range_integer_re = re.compile(r"(?P<integer>.*)")

# This gives misleading information about variable name derivation but
# fits the pattern to detect 'function call' variable names.
_range_variable_re = _echo_variable_re

# Find 'a-h' and '1-8' style square specifications in piece designators
# so sequences like 'h-a' and '8-1' can be rejected.  Sequences like
# '1-h' and 'a-8' are ruled out by the pattern for piece designators.
_file_rank_re = re.compile(r"([a-h1-8])-([a-h1-8])")

# Find the square designator part of a piece designator.
# The 'rotate45' filter operates only on sets containin all squares.
# This pattern assumes any string scanned has been accepted by the piece
# designator pattern.
_square_designator_re = re.compile(
    elements.PIECE_OPTIONS.join((r"(?:", ")?(.*)"))
)

# Map compound directions to basic directions.
_directions = {
    "up": ["up"],
    "down": ["down"],
    "right": ["right"],
    "left": ["left"],
    "northeast": ["northeast"],
    "northwest": ["northwest"],
    "southeast": ["southeast"],
    "southwest": ["southwest"],
    "diagonal": ["northeast", "northwest", "southeast", "southwest"],
    "orthogonal": ["up", "down", "left", "right"],
    "vertical": ["up", "down"],
    "horizontal": ["left", "right"],
    "anydirection": [
        "up",
        "down",
        "left",
        "right",
        "northeast",
        "northwest",
        "southeast",
        "southwest",
    ],
}


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
            node = super().place_node_in_tree()
            if not isinstance(node, Path):
                break
            node.children[-1].parent = node.parent
            node.parent.children.append(node.children.pop())
            node.verify_children_and_set_types()
        container = self.container
        container.whitespace.append(self)
        del self.parent.children[-1]
        # Setting completed outside verify_children_and_set_types()
        # needs a note of justification.
        self.parent.completed = True
        container.cursor = self.parent
        # Class instances for tokens treated as whitespace have no parent.
        self.parent = None

    def _raise_if_cursor_is_not_expected_class(self, expected_class):
        """Raise NodeError if cursor is not expected class."""
        if isinstance(self.container.cursor, expected_class):
            return
        self.raise_nodeerror(
            self.__class__.__name__.join("''"),
            " expects cursor to be a ",
            expected_class.__name__.join("''"),
            " but it is a ",
            self.container.cursor.__class__.__name__.join("''"),
        )


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

    def place_node_in_tree(self):
        """Override to place repeat operator in tree and set cursor to self.

        The repeat operator becomes a sibling of constituent.

        """
        # Check for 'path' filter first.
        node = self.container.cursor
        while node:
            if isinstance(node, BraceLeft) and not node.complete():
                break
            if (
                isinstance(node, (Path, ConstituentParenthesisLeft))
                and not node.complete()
            ):
                node.children.append(self.container.cursor.children.pop())
                node.children[-1].parent = node
                self.container.cursor.verify_children_and_set_types(
                    set_node_completed=True
                )
                self.container.cursor = self
                return
            node = node.parent
        # Now check for 'line' filter.
        node = self.parent
        while node and node.complete() and not isinstance(node, LineArrow):
            node.children[-1].parent = node.parent
            node.parent.children.append(node.children.pop())
            node.verify_children_and_set_types(set_node_completed=True)
            node = node.parent
        if not isinstance(
            self.parent, (LineArrow, LineConstituentParenthesisLeft)
        ):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " is not in a 'line' or 'path' filter",
            )
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
            self.match_.group(), AssignPromotion
        )


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
    if isinstance(container.cursor, AssignPromotion):
        if _is_type_designator_string(match_):
            return TypeDesignator(match_=match_, container=container)
        container.raise_nodeerror(
            "'",
            container.cursor.__class__.__name__,
            "' type designator string ",
            match_.group(),
            " contains characters other than '",
            constants.PIECE_NAMES,
            "'",
        )
    if is_documentation_parameter_accepted_by(container.cursor):
        return Documentation(match_=match_, container=container)
    if is_implicit_search_parameter_accepted_by(container.cursor):
        if not isinstance(
            container.cursor.parent,
            (
                StrParentheses,
                MessageParentheses,
                CommentParentheses,
                CommentSymbol,
            ),
        ):
            return ImplicitSearchParameter(match_=match_, container=container)
    return String(match_=match_, container=container)


class EndCommentSymbol(structure.CQLObject):
    """Terminate '///' filter and following 'path' filters."""

    def __init__(self, match_=None, container=None):
        """Verify no open compound filters after '///' in then delegate."""
        node = container.cursor
        while node:
            if isinstance(node, CommentSymbol):
                break
            if isinstance(node, structure.CompleteBlock):
                if not node.full():
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " cannot end '///' filter in open block filter",
                    )
            node = node.parent
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        r"""Override, terminate all 'path' filters and remove from stack.

        The sequence '\n' and similar completes the '///' filter and any
        following 'path' filters.

        """
        container = self.container
        container.whitespace.append(self)
        node = self.parent
        while True:
            while node and node.full():
                # All cases of suppressing implicit search parameter like
                # '/// (Event "Open")' avoid a '() has too many children'
                # exception with the test on node.completed present.
                # But verify_children_and_set_types() is, in principle,
                # the only place where completed is set True, so the test
                # may indicate another problem.
                if not node.completed:
                    node.verify_children_and_set_types(set_node_completed=True)
                node = node.parent
            if not isinstance(node, (Path, CommentSymbol)):
                self.raise_nodeerror(
                    node.__class__.__name__.join("''"),
                    " not complete while handling ",
                    self.__class__.__name__.join("''"),
                )
            node.verify_children_and_set_types(set_node_completed=True)
            if isinstance(node, CommentSymbol):
                break
            p_node = node.parent
            while p_node:
                if isinstance(p_node, (Path, CommentSymbol)):
                    break
                p_node = p_node.parent
            if p_node is None:
                break
            node = node.parent
        container.cursor = node.parent
        # Class instances for tokens treated as whitespace have no parent.
        del self.parent.children[-1]
        self.parent = None


class EndPaths(structure.CQLObject):
    """Terminate all 'path' filters and the '///' filter if present."""

    def place_node_in_tree(self):
        r"""Override, terminate all 'path' filters and remove from stack.

        The sequence '\n\n' and similar completes multiple 'path' filters,
        and a '///' filter if present.

        """
        container = self.container
        container.whitespace.append(self)
        node = self.parent
        while True:
            while node and node.full():
                # All cases of suppressing implicit search parameter like
                # '/// (Event "Open")' avoid a '() has too many children'
                # exception with the test on node.completed present.
                # But verify_children_and_set_types() is, in principle,
                # the only place where completed is set True, so the test
                # may indicate another problem.
                if not node.completed:
                    node.verify_children_and_set_types(set_node_completed=True)
                node = node.parent
            if not isinstance(node, (Path, CommentSymbol)):
                self.raise_nodeerror(
                    node.__class__.__name__.join("''"),
                    " not complete while handling ",
                    self.__class__.__name__.join("''"),
                )
            node.verify_children_and_set_types(set_node_completed=True)
            p_node = node.parent
            while p_node:
                if isinstance(p_node, (Path, CommentSymbol)):
                    break
                p_node = p_node.parent
            if p_node is None:
                break
            node = node.parent
        container.cursor = node.parent
        # Class instances for tokens treated as whitespace have no parent.
        del self.parent.children[-1]
        self.parent = None


class WhiteSpace(structure.Complete):
    """Store whitespace to account for all text."""

    _is_allowed_first_object_in_container = True

    def place_node_in_tree(self):
        """Override, move self to whitespace and set cursor to parent."""
        container = self.container
        container.whitespace.append(self.parent.children.pop())
        container.cursor = self.parent
        self.parent = None


class BlockComment(WhiteSpace):
    """Represent a '/*....*/' comment in a *.cql file."""


class LineComment(WhiteSpace):
    r"""Represent a '//.....\n' comment in a *.cql file.

    Note that '////....\n', and more leading '/' characters, is a LineComment
    but '///....\n' is a CommentSymbol (one of two CQL comment filters).
    """


def _path_or_comment_symbols_found(match_, container):
    """Return set of Path and CommentSymbol classes in ancestors."""
    if _blank_line_re.search(match_.group()):
        search_for = (CommentSymbol, Path)
    else:
        search_for = CommentSymbol
    found = set()
    node = container.cursor
    while node:
        if isinstance(node, search_for):
            found.add(node.__class__)
            if not isinstance(search_for, tuple):
                break
        node = node.parent
    return found


def end_of_line(match_=None, container=None):
    """Return a WhiteSpace, EndCommentSymbol, or EndPaths, instance."""
    found = _path_or_comment_symbols_found(match_, container)
    if found:
        if Path in found:
            return EndPaths(match_=match_, container=container)
        return EndCommentSymbol(match_=match_, container=container)
    return WhiteSpace(match_=match_, container=container)


def line_comment(match_=None, container=None):
    """Return a WhiteSpace, EndCommentSymbol, or EndPaths, instance."""
    found = _path_or_comment_symbols_found(match_, container)
    if found:
        if Path in found:
            return EndPaths(match_=match_, container=container)
        return EndCommentSymbol(match_=match_, container=container)
    return WhiteSpace(match_=match_, container=container)


class BraceRight(RightCompoundPlace):
    """Close BraceLeft and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then verify cursor class is BraceLeft or Plus."""
        super().place_node_in_tree()
        # Path is terminated by '}' but the Plus should have been seen as
        # a RepeatPlus within a Path (itself terminated by '}') in
        # cql6-9-493-windows/examples/followpath.cql query.
        if not isinstance(self.container.cursor, (BraceLeft, Plus)):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects cursor to be a ",
                BraceLeft.__name__.join("''"),
                " or a ",
                Plus.__name__,
                " but it is a ",
                self.container.cursor.__class__.__name__.join("''"),
            )


class FunctionBodyRight(RightCompoundPlace):
    """Close FunctionBodyLeft and record input tokens for replay."""

    def place_node_in_tree(self):
        """Delegate then decrement function_body_count and adjust cursor.

        The cursor is set to cursor's parent when function_body_count
        reaches zero.

        """
        super().place_node_in_tree()
        container = self.container
        self._raise_if_cursor_is_not_expected_class(FunctionBodyLeft)
        if container.function_body_count == 0:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects cursor to be within a function body definition ",
                "but function_body_count is ",
                str(container.function_body_count).join("''"),
            )
        container.function_body_count -= 1
        if container.function_body_count == 0:
            container.function_body_cursor = None
            container.cursor = container.cursor.parent
            del container.cursor.children[-1]
            container.cursor = container.cursor.parent


def brace_right(match_=None, container=None):
    """Return class instance for '}' in context or raise NodeError.

    BraceRight and FunctionBodyRight are the relevant classes.

    """
    # Start at container.cursor and move up the parent chain while node
    # is complete.
    # The first node which is not complete should be a FunctionBodyLeft or
    # BraceLeft instance: NodeError is raised if not.
    # For example in the sequence '{...consecutivemoves(x y)}' a completed
    # ConsecutiveMoves instance will be at container.cursor and there may
    # be others in the parent chain depending on the detail of '...'.
    node = container.cursor
    while node:
        if not node.full():
            if isinstance(node, BraceLeft):
                if not node.children:
                    node.raise_nodeerror(
                        "'",
                        node.__class__.__name__,
                        "' '{' block must contain at least one filter",
                    )
                return BraceRight(match_=match_, container=container)
            if isinstance(node, FunctionBodyLeft):
                return FunctionBodyRight(match_=match_, container=container)
            if isinstance(node, ParenthesisLeft):
                node.raise_nodeerror(
                    "'",
                    node.__class__.__name__,
                    "' cannot close a '(' parenthesized block with '}'",
                )
            if isinstance(
                node,
                (
                    ConstituentParenthesisLeft,
                    LineConstituentParenthesisLeft,
                ),
            ):
                node.raise_nodeerror(
                    "'",
                    node.__class__.__name__,
                    "' cannot close a '(' top level constituent with '}'",
                )
            if isinstance(node, BracketLeft):
                node.raise_nodeerror(
                    "'",
                    node.__class__.__name__,
                    "' cannot close a '[' string index with '}'",
                )
            if isinstance(node, structure.ParenthesizedArguments):
                node.raise_nodeerror(
                    "'",
                    node.__class__.__name__,
                    "' cannot close parenthesized arguments with '}'",
                )
        node = node.parent
    container.raise_nodeerror(
        "Unexpected ", str(node), " found while trying to match a '}'"
    )
    # A pylint R1710 inconsistent-return-statements report indicates the
    # absence of this statement.
    raise RuntimeError("This point is intentionally unreachable")


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

    def __init__(self, match_=None, container=None):
        """Delegate then set details for this instance and add to tree."""
        super().__init__(match_=match_, container=container)
        if isinstance(container.cursor, Function):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot be applied to ",
                container.cursor.__class__.__name__.join("''"),
                " instance",
            )


def regex_repeat(match_=None, container=None):
    """Return RegexRepeat instance or generate compound filter.

    '{<digits>}' could be a compound filter or a RegexRepeat.

    The compound filter is generated by creating the BraceLeft and Integer
    instance and returning the BraceRight instance which completes the
    compound filter.

    '{<digits>}' can only be a RegexRepeat when part of a 'line' or 'path'
    filter. Thus in:

    'line --> K {4}' the '{4}' is a RegexRepeat,
    'line --> {4}' the '{4}' is a compound filter,
    'line --> { K {4} }' the '{4}' is a compound filter,
    'line --> { K qa5 }{4}' the '{4}' is a RegexRepeat.

    If there is any whitespace between the '{' and '}' the sequence is
    seen as a compound filter, and evaluation does not go through this
    path.

    """
    if not match_.group()[1:-1].isdigit():
        return RegexRepeat(match_=match_, container=container)
    node = container.cursor
    while node is not None:
        if not node.full():
            if isinstance(node, (Path, ConstituentParenthesisLeft)):
                return RegexRepeat(match_=match_, container=container)
            break
        if isinstance(node, LineArrow):
            return RegexRepeat(match_=match_, container=container)
        node = node.parent
    # Re-evaluation of the pattern match is necessary to get the expected
    # characters in the match's group.
    # Also re-evaluation of the pattern match is necessary with 'function'
    # definitions to prevent three repetitions of the 'BraceLeft Integer'
    # sequence when the function call is expanded from the original matched
    # text held in each object.
    start, end = match_.span()
    if isinstance(node, Function):
        braceleft = FunctionBodyLeft
        braceright = FunctionBodyRight
    else:
        braceleft = BraceLeft
        braceright = BraceRight
    braceleft(
        match_=pattern.cql_re.match(match_.string, start, start + 1),
        container=container,
    ).place_node_in_tree()
    Integer(
        match_=pattern.cql_re.match(match_.string, start + 1, end - 1),
        container=container,
    ).place_node_in_tree()
    return braceright(
        match_=pattern.cql_re.match(match_.string, end - 1, end),
        container=container,
    )


class FunctionBodyLeft(structure.BlockLeft):
    """Represent '{' body of function filter definition."""

    def place_node_in_tree(self):
        """Delegate then increment function_body_count.

        A superclass is expected to set cursor to self.

        """
        super().place_node_in_tree()
        self.container.function_body_count += 1


class BraceLeft(structure.BlockLeft):
    """Represent '{' compound filter of type determined by children."""

    @property
    def filter_type(self):
        """Return filter type of last child if BraceLeft completed."""
        if self.completed:
            return self.children[-1].filter_type
        return super().filter_type

    def is_left_brace_or_parenthesis(self):
        """Override and return True."""
        return True


def brace_left(match_=None, container=None):
    """Return BraceLeft or FunctionBodyLeft instance."""
    if isinstance(container.cursor, Function):
        return FunctionBodyLeft(match_=match_, container=container)
    return BraceLeft(match_=match_, container=container)


# The replaced place_node_in_tree() method does
# self._raise_if_node_not_child_of_filters("(", MoveInfix)
# before the super().place_node_in_tree() call.
class TargetParenthesisLeft(structure.BlockLeft):
    """Represent '(' target conditions in '--' or '[x]' filter."""

    def place_node_in_tree(self):
        """Place as child of '--' or '[x]' if possible."""
        node = self.container.cursor
        while node:
            if _is_dash_or_capture(node):
                node.children.append(self.parent.children.pop())
                self.parent = node
                self.container.cursor = self
                return
            node = node.parent
        super().place_node_in_tree()


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

    @property
    def filter_type(self):
        """Return filter type of last child if filter completed."""
        if self.completed and len(self.children) > 0:
            return self.children[-1].filter_type
        return super().filter_type


class ParenthesisLeft(structure.BlockLeft):
    """Represent '(' in various CQL statement contexts.

    See ConstituentParenthesisLeft for '(' as top level chain constituent.
    """

    @property
    def filter_type(self):
        """Return filter type of last child if ParenthesisLeft completed.

        There will be only one child in the completed filter.
        """
        if self.completed and len(self.children) == 1:
            return self.children[-1].filter_type
        return super().filter_type

    def is_left_brace_or_parenthesis(self):
        """Override and return True."""
        return True

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if len(self.children) != 1:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects one child filter but has ",
                str(len(self.children)),
            )


# There need to be three kinds of '(' apart from parenthesized arguments.
#   Precedence control.
#   Chain consituents in 'path' filter.  'path (check)'.
#   Target move conditions in '--' filter.  '--d4(check)'.
#   '(' for parenthesized arguments are caught in the filter pattern.
def parenthesis_left(match_=None, container=None):
    """Return appropriate ...ParenthesisLeft instance.

    Search ancestors for nearest of  BraceLeft, Line, Path, and
    LineConstituentParenthesisLeft instances.

    Both '('s in '(<optional1>(...)<optional2>)' should return True by these
    tests, or both should return False, provided '<optional1>' does not have
    'line', 'path', or '{'.

    """
    left_parenthesis_class = ParenthesisLeft
    for cursor in (container.cursor.parent, container.cursor.parent.parent):
        if _is_dash_or_capture(cursor):
            if _no_intervening_whitespace(cursor.match_, match_):
                left_parenthesis_class = TargetParenthesisLeft
                break
    node = container.cursor
    while node:
        if isinstance(node, structure.BlockLeft):
            if isinstance(node, (Path, ConstituentParenthesisLeft)):
                left_parenthesis_class = ConstituentParenthesisLeft
                break
            if isinstance(node, (CommentSymbol, ParenthesisLeft)):
                node = node.parent
                continue
            break
        if isinstance(node, LineArrow):
            if node.full():
                break
            if left_parenthesis_class is ParenthesisLeft:
                left_parenthesis_class = LineConstituentParenthesisLeft
            break
        node = node.parent
    return left_parenthesis_class(match_=match_, container=container)


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
        self._raise_if_cursor_is_not_expected_class(
            LineConstituentParenthesisLeft
        )


class ConstituentParenthesisRight(RightCompoundPlace):
    """Close ConstituentParenthesisLeft and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then verify cursor class is ConstituentParenthesisLeft."""
        super().place_node_in_tree()
        self._raise_if_cursor_is_not_expected_class(ConstituentParenthesisLeft)


class ParenthesisRight(RightCompoundPlace):
    """Close ParenthesisLeft and record as whitespace."""

    def place_node_in_tree(self):
        """Delegate then verify cursor class is ParenthesisLeft."""
        super().place_node_in_tree()
        self._raise_if_cursor_is_not_expected_class(ParenthesisLeft)


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
        self._raise_if_cursor_is_not_expected_class(
            structure.ParenthesizedArguments
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
        if isinstance(self.parent, TargetParenthesisLeft):
            self.parent.filter_type = children[-1].filter_type
        if isinstance(
            parent_parent, (structure.MoveInfix, structure.DashOrTake)
        ):
            parent_parent.filter_type = children[-1].filter_type
        # Setting completed outside verify_children_and_set_types()
        # needs a note of justification.
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

    _precedence = cqltypes.Precedence.P10

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
            node.verify_children_and_set_types(set_node_completed=True)
            node = node.parent
        self.raise_if_name_parameter_not_for_filters()
        self._raise_if_other_line_arrow_present()
        self.container.cursor = self

    def _raise_if_other_line_arrow_present(self):
        """Raise NodeError if conditions are met.

        Assumption is only ArrowBackward and ArrowForward are subclasses
        of LineArrow.

        """
        node = self.container.cursor
        while node:
            if isinstance(node, Line):
                for child in node.children:
                    if not child.is_parameter and not isinstance(
                        child, self.__class__
                    ):
                        existing, current = (
                            ("<--", "-->")
                            if isinstance(self, ArrowForward)
                            else ("-->", "<--")
                        )
                        self.raise_nodeerror(
                            self.__class__.__name__.join("''"),
                            current.join("''"),
                            " cannot be mixed with existing ",
                            existing.join("''"),
                            "s",
                            " in 'line' filter",
                        )
                break
            node = node.parent

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_line_arrow_parameter_accepted_by(self.parent)


class ArrowBackward(LineArrow, structure.Argument):
    """Represent '<--' keyword for 'line' filter.  Deprecated at 6.2.

    '<--' is not called a filter or a parameter in CQL documentation at
    6.1 and is processed here as a filter which has one mandatory child
    filter called a constituent.  The '<--' is validated like a parameter
    since it is allowed only in the 'line' filter.
    """


def arrow_backward(match_=None, container=None):
    """Return FindBackward or ArrowBackward instance."""
    node = container.cursor
    while True:
        if not node.is_parameter:
            break
        node = node.parent
    if is_find_backward_parameter_accepted_by(node):
        return FindBackward(match_=match_, container=container)
    return ArrowBackward(match_=match_, container=container)


class ArrowForward(LineArrow, structure.Argument):
    """Represent '-->' keyword for 'line' filter.  Deprecated at 6.2.

    '-->' is not called a filter or a parameter in CQL documentation at
    6.1 and is processed here as a filter which has one mandatory child
    filter called a constituent.  The '-->' is validated like a parameter
    since it is allowed only in the 'line' filter.
    """


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


class TakeII(structure.DashOrTake):
    """Represent '[x]' ('×') filter like F [x] G.

    F and G are set filters where whitespace between them and '[x]' matters.
    TakeII is an infix operator with both LHS and RHS implicit: F is not
    the LHS and G is not the RHS.  Both LHS and RHS are the '.' filter,
    equivalent to 'a-h1-8'.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Prevent other filters taking implicit arguments by precedence.
    _precedence = cqltypes.Precedence.PHIGH

    def __init__(self, match_=None, container=None):
        """Create the implied '.' filter then delegate."""
        AnySquare(match_=match_, container=container).place_node_in_tree()
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        """Delegate then append the implied '.' filter."""
        super().place_node_in_tree()
        AnySquare(
            match_=self.match_, container=self.container
        ).place_node_in_tree()


class TakeLI(structure.DashOrTake):
    """Represent '[x]' ('×') filter like F[x] G.

    F and G are set filters where whitespace between them and '[x]' matters.

    TakeLI is an infix operator with only RHS implicit: F is the LHS and
    G is not the RHS.  The RHS is the '.' filter, equivalent to 'a-h1-8'.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Allow other filters to take lhs argument by precedence.
    # '--'has extremely low precedence and lhs filter is not implicit.
    # Once placed in tree precedence must become PHIGH to prevent other
    # filters taking the implicit rhs filter.
    _precedence = cqltypes.Precedence.PLOW

    def place_node_in_tree(self):
        """Delegate then append the implied '.' filter."""
        super().place_node_in_tree()
        AnySquare(
            match_=self.match_, container=self.container
        ).place_node_in_tree()

    @property
    def precedence(self):
        """Return self._precedence appropriate to RHS filter."""
        if len(self.children) > 1 and isinstance(self.children[1], AnySquare):
            return cqltypes.Precedence.PHIGH
        return self._precedence


class TakeIR(structure.DashOrTake):
    """Represent '[x]' ('×') filter like F [x]G.

    F and G are set filters where whitespace between them and '[x]' matters.

    TakeIR is an infix operator with only LHS implicit: F is not the LHS
    and G is the RHS.  The LHS is the '.' filter, equivalent to 'a-h1-8'.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Prevent other filters taking implicit lhs argument by precedence.
    # Once placed in tree precedence must become PLOW because '--' has
    # extremely low precedence and rhs filter is not implicit.
    _precedence = cqltypes.Precedence.PHIGH

    def __init__(self, match_=None, container=None):
        """Create the implied '.' filter then delegate."""
        AnySquare(match_=match_, container=container).place_node_in_tree()
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        """Delegate then set instance precedence to PLOW."""
        super().place_node_in_tree()
        self._precedence = cqltypes.Precedence.PLOW


class TakeLR(structure.DashOrTake):
    """Represent '[x]' ('×') filter like F[x]G.

    F and G are set filters where whitespace between them and '[x]' matters.

    TakeLR is an infix operator with neither LHS nor RHS implicit: F is
    the LHS and G is the RHS.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Allow other filters to take lhs and rhs argument by precedence.
    # '--'has extremely low precedence and both lhs filter and rhs filter
    # are not implicit.
    _precedence = cqltypes.Precedence.PLOW


def take_li(match_=None, container=None):
    """Return a TakeII or TakeLI instance depending on match_ detail.

    A TakeII instance is returned if character preceding match_.group()
    is a ':'.  Otherwise return a TakeLI instance.

    """
    if _is_lhs_implicit(match_, container):
        return TakeII(match_=match_, container=container)
    return TakeLI(match_=match_, container=container)


def take_lr(match_=None, container=None):
    """Return a Take[II|IR|LI|LR|] instance depending on match_ detail."""
    if _is_lhs_implicit(match_, container):
        return take_ir(match_=match_, container=container)
    if _is_rhs_implicit(match_):
        return TakeLI(match_=match_, container=container)
    return TakeLR(match_=match_, container=container)


def take_ir(match_=None, container=None):
    """Return a TakeII or TakeIR instance depending on match_ detail.

    A TakeLI instance is returned if character following match_.group()
    is a '=' or '('.  Otherwise return a TakeLR instance.

    """
    if _is_rhs_implicit(match_):
        return TakeII(match_=match_, container=container)
    return TakeIR(match_=match_, container=container)


class CommentSymbol(structure.BlockLeft):
    """Represent '///' logical filter.

    CommentSymbol does not follow Comment and CommentParentheses in having
    a parameter version for interaction with Move because the '///' filter
    is introduced at CQL-6.2 and 'move' filter is deprecated at CQL-6.2.

    The '///' filter is terminated by a newline.  This is similar to the
    'path' filter which is terminated by a blank line.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    def __init__(self, match_=None, container=None):
        """Verify no '///' filter in ancestors then delegate."""
        node = container.cursor
        while node:
            if isinstance(node, CommentSymbol):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " cannot have more than one '///' filter on a line",
                )
            node = node.parent
        super().__init__(match_=match_, container=container)

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if not self.children or isinstance(
            self.children[0], (EndPaths, EndCommentSymbol)
        ):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"), " has no items in comment"
            )


class AttackArrow(structure.MoveInfix):
    """Represent '->' (→) set filter."""

    _filter_type = cqltypes.FilterType.SET

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.SET)
        if isinstance(self.children[-1], AttackedArrow):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot be chained to an ",
                AttackedArrow.__name__.join("''"),
            )


class AttackedArrow(structure.MoveInfix):
    """Represent '<-' (←) set filter."""

    _filter_type = cqltypes.FilterType.SET

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.SET)
        if isinstance(self.children[-1], AttackArrow):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot be chained to an ",
                AttackArrow.__name__.join("''"),
            )


class DashII(structure.DashOrTake):
    """Represent '--' ('―') filter like F -- G.

    F and G are set filters where whitespace between them and '--' matters.

    Targets are within '()' like 'F --(check) G' for example.

    DashII is an infix operator with both LHS and RHS implicit: F is not
    the LHS and G is not the RHS.  Both LHS and RHS are the '.' filter,
    equivalent to 'a-h1-8'.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Prevent other filters taking implicit arguments by precedence.
    _precedence = cqltypes.Precedence.PHIGH

    def __init__(self, match_=None, container=None):
        """Create the implied '.' filter then delegate."""
        AnySquare(match_=match_, container=container).place_node_in_tree()
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        """Delegate then append the implied '.' filter."""
        super().place_node_in_tree()
        AnySquare(
            match_=self.match_, container=self.container
        ).place_node_in_tree()


class DashLI(structure.DashOrTake):
    """Represent '--' ('―') filter like F-- G.

    F and G are set filters where whitespace between them and '--' matters.

    Targets are within '()' like 'F--(check) G' for example.

    DashLI is an infix operator with only RHS implicit: F is the LHS and
    G is not the RHS.  The RHS is the '.' filter, equivalent to 'a-h1-8'.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Allow other filters to take lhs argument by precedence.
    # '--'has extremely low precedence and lhs filter is not implicit.
    # Once placed in tree precedence must become PHIGH to prevent other
    # filters taking the implicit rhs filter.
    _precedence = cqltypes.Precedence.PLOW

    def place_node_in_tree(self):
        """Delegate then append the implied '.' filter."""
        super().place_node_in_tree()
        AnySquare(
            match_=self.match_, container=self.container
        ).place_node_in_tree()

    @property
    def precedence(self):
        """Return self._precedence appropriate to RHS filter."""
        if len(self.children) > 1 and isinstance(self.children[1], AnySquare):
            return cqltypes.Precedence.PHIGH
        return self._precedence


class DashIR(structure.DashOrTake):
    """Represent '--' ('―') filter like F --G.

    F and G are set filters where whitespace between them and '--' matters.

    Targets are within '()' like 'F --G(check)' for example.

    DashIR is an infix operator with only LHS implicit: F is not the LHS
    and G is the RHS.  The LHS is the '.' filter, equivalent to 'a-h1-8'.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Prevent other filters taking implicit lhs argument by precedence.
    # Once placed in tree precedence must become PLOW because '--' has
    # extremely low precedence and rhs filter is not implicit.
    _precedence = cqltypes.Precedence.PHIGH

    def __init__(self, match_=None, container=None):
        """Create the implied '.' filter then delegate."""
        AnySquare(match_=match_, container=container).place_node_in_tree()
        super().__init__(match_=match_, container=container)

    def place_node_in_tree(self):
        """Delegate then set instance precedence to PLOW."""
        super().place_node_in_tree()
        self._precedence = cqltypes.Precedence.PLOW


class DashLR(structure.DashOrTake):
    """Represent '--' ('―') filter like F--G.

    F and G are set filters where whitespace between them and '--' matters.

    Targets are within '()' like 'F--G(check)' for example.

    DashLR is an infix operator with neither LHS nor RHS implicit: F is the
    LHS and G is the RHS.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # Allow other filters to take lhs and rhs argument by precedence.
    # '--'has extremely low precedence and both lhs filter and rhs filter
    # are not implicit.
    _precedence = cqltypes.Precedence.PLOW


def dash_li(match_=None, container=None):
    """Return a DashII or DashLI instance depending on match_ detail.

    A DashII instance is returned if character preceding match_.group()
    is a ':'.  Otherwise return a DashLI instance.

    """
    if _is_lhs_implicit(match_, container):
        return DashII(match_=match_, container=container)
    return DashLI(match_=match_, container=container)


def dash_lr(match_=None, container=None):
    """Return a Dash[II|IR|LI|LR|] instance depending on match_ detail."""
    if _is_lhs_implicit(match_, container):
        return dash_ir(match_=match_, container=container)
    if _is_rhs_implicit(match_):
        return DashLI(match_=match_, container=container)
    return DashLR(match_=match_, container=container)


def dash_ir(match_=None, container=None):
    """Return a DashII or DashIR instance depending on match_ detail.

    A DashLI instance is returned if character following match_.group()
    is a '=' or '('.  Otherwise return a DashLR instance.

    """
    if _is_rhs_implicit(match_):
        return DashII(match_=match_, container=container)
    return DashIR(match_=match_, container=container)


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

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        self.raise_if_not_same_filter_type(
            "match pattern",
            filter_type=cqltypes.FilterType.STRING,
        )


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
    _comparable_filter_types = (
        cqltypes.FilterType.SET
        | cqltypes.FilterType.NUMERIC
        | cqltypes.FilterType.STRING
        | cqltypes.FilterType.POSITION
    )


class NE(structure.CompareSet, structure.Compare, structure.InfixRight):
    """Represent '!=' ('≠') numeric filter or string filter."""

    _precedence = cqltypes.Precedence.P80
    _comparable_filter_types = (
        cqltypes.FilterType.SET
        | cqltypes.FilterType.NUMERIC
        | cqltypes.FilterType.STRING
    )


class AssignPlus(structure.InfixLeft):
    """Represent '+=' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL
    _precedence = cqltypes.Precedence.P90

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        lhs = self.children[0]
        self.raise_if_not_instance(
            lhs, structure.VariableName, "lhs must be a"
        )
        rhs = self.children[1]
        if self.container.function_body_cursor is None or not isinstance(
            rhs, structure.VariableName
        ):
            if (
                rhs.filter_type is not cqltypes.FilterType.NUMERIC
                and rhs.filter_type is not cqltypes.FilterType.STRING
            ):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " rhs must be a Numeric or String filter",
                )
        structure.set_persistent_variable_filter_type(lhs, rhs)
        if self.container.function_body_cursor is None or not isinstance(
            rhs, structure.VariableName
        ):
            self.raise_if_not_same_filter_type("assign")


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

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if self.container.function_body_cursor is not None:
            # Maybe see if argument is a variable too.
            return
        child_filter_type = self.children[0].filter_type
        if child_filter_type is cqltypes.FilterType.NUMERIC:
            self.filter_type = cqltypes.FilterType.STRING
            return
        if child_filter_type is cqltypes.FilterType.STRING:
            self.filter_type = cqltypes.FilterType.NUMERIC
            return
        self.raise_nodeerror(
            self.__class__.__name__.join("''"),
            " expects a ",
            self.filter_type.name.lower().join("''"),
            " argument but got a ",
            child_filter_type.name.lower().join("''"),
        )


class Assert(structure.Argument):
    """Represent 'assert' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


# Prefix to variable, 'atomic variables' in Table of Filters.
class Atomic(structure.Complete, structure.VariableName):
    """Represent variable with 'atomic' prefix."""

    def __init__(self, match_=None, container=None):
        """Delegate then register the variable name."""
        super().__init__(match_=match_, container=container)
        groupdict = match_.groupdict()
        self.name = groupdict["atomic"]
        self._register_variable_type(cqltypes.VariableType.ANY)
        self._set_persistence_type(
            cqltypes.PersistenceType.ATOMIC | cqltypes.PersistenceType.LOCAL,
            check_types=cqltypes.PersistenceType.LOCAL,
        )

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self

    def is_variable(self):
        """Override and return True."""
        return True


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


# Assumption is 'move <parameters> comment <arguments>' should be marked
# different from '<non-move filter> comment <arguments>'.
class CommentParameter(structure.Argument):
    """Represent 'comment' filter immediately after 'move' filter."""

    _is_parameter = True
    _filter_type = cqltypes.FilterType.LOGICAL

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return is_comment_parameter_accepted_by(self.parent)


def comment(match_=None, container=None):
    """Return Comment or CommentParameter instance.

    CommentParameter is returned if parent is 'move' filter and does
    not already have either 'legal' or 'pseudolegal' parameter.

    """
    return _string_or_parentheses_comment(
        match_, container, Comment, CommentParameter
    )


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


# Assumption is 'move <parameters> comment <arguments>' should be marked
# different from '<non-move filter> comment <arguments>'.
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
    return _string_or_parentheses_comment(
        match_, container, CommentParentheses, CommentParenthesesParameter
    )


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
        items = self.match_.group().rstrip("(").split()[1:]
        if "quiet" in items:
            Quiet(match_=self.match_, container=container).place_node_in_tree()
            container.cursor = self
            items.remove("quiet")
        for item in items:
            if item.isdigit():
                range_item = RangeInteger(
                    match_=_range_integer_re.match(item),
                    container=container,
                )
            else:
                if item not in container.definitions:
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " range variable ",
                        item.join("''"),
                        " not defined",
                    )
                range_item = RangeVariable(
                    match_=_range_variable_re.match(item),
                    container=container,
                )
            range_item.place_node_in_tree()
            container.cursor = self

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        components = [c for c in self.children if not c.is_parameter]
        if len(components) != 2:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have exactly two components",
            )
        definitions = self.container.definitions
        for child in components:
            if (
                not isinstance(child, Variable)
                or not definitions[child.name].variable_type
                in cqltypes.VariableType.POSITION
            ):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " argument must be a position variable",
                )


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


class CountMoves(structure.Argument, structure.LeftParenthesisInfix):
    """Represent 'countmoves' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC

    def is_countmoves(self):
        """Override, return True.

        To cope with 'countmoves legal -- == 1 and 'legal -- == 1'.

        """
        return True

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(1)
        child = self.children[0]
        if not _is_dash_or_capture(child) and not isinstance(
            child, (Legal, Pseudolegal)
        ):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " argument must be a '--', '[x]', 'legal', ",
                "or 'pseudolegal', filter, not a ",
                self.children[0].__class__.__name__.join("''"),
                " filter",
            )


class CurrentMove(structure.Argument):
    """Represent 'currentmove' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL

    @property
    def precedence(self):
        """Return precedence greater than logical operators when comparing.

        The logical operator will be the '-1' child of cursor at time
        of precedence checking.

        """
        if isinstance(self.container.cursor.children[-1], (And, Or)):
            return cqltypes.Precedence.PHIGH  # Higher than P50.
        return self._precedence

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(1)
        if not _is_dash_or_capture(self.children[0]):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " argument must be a '--' or '[x]' filter, not a ",
                self.children[0].__class__.__name__.join("''"),
                " filter",
            )


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


class Dictionary(structure.Complete, structure.DictionaryName):
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
        if match_.group().split()[0] == "local":
            persistence_type = cqltypes.PersistenceType.LOCAL
        elif (
            cqltypes.PersistenceType.ANY
            in container.definitions[self.name].persistence_type
        ):
            persistence_type = cqltypes.PersistenceType.PERSISTENT
        elif (
            cqltypes.PersistenceType.LOCAL
            in container.definitions[self.name].persistence_type
        ):
            persistence_type = cqltypes.PersistenceType.LOCAL
        else:
            persistence_type = cqltypes.PersistenceType.PERSISTENT
        self._set_persistence_type(
            persistence_type,
            check_types=cqltypes.PersistenceType.PERSISTENT
            | cqltypes.PersistenceType.LOCAL,
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

    def set_variable_types(
        self, key_filter_type, filter_type, nametype="dictionary"
    ):
        """Set key_filter_type and filter type of dictionary instance.

        The dictionary's name must have been registered by a prior call of
        _register_variable_type.

        A NodeError exception is raised on attempting to change any other
        filter type value.

        The dictionary persistence type is deduced from self's match_
        attribute, the string may start with the keyword 'local', and
        validated and applied.

        Details for user defined items, variables and functions, are not
        updated when encountered during collection of functions' bodies.

        """
        if self.container.function_body_cursor is not None:
            return
        super()._set_variable_filter_type(filter_type, nametype=nametype)
        name = self.name
        item = self.container.definitions[name]
        if item.key_filter_type is cqltypes.FilterType.ANY:
            item.key_filter_type = key_filter_type
        if item.key_filter_type is not key_filter_type:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " existing keys in dictionary ",
                name.join("''"),
                " are ",
                item.key_filter_type.name.lower().join("''"),
                " filters so cannot set key as a ",
                key_filter_type.name.lower().join("''"),
                " filter",
            )
        if self.match_.group().startswith("local"):
            persistence_type = cqltypes.PersistenceType.LOCAL
        elif self.match_.group().startswith("dictionary"):
            persistence_type = cqltypes.PersistenceType.PERSISTENT
        elif item.persistence_type is cqltypes.PersistenceType.ANY:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " dictionary ",
                name.join("''"),
                " has not been declared ",
                cqltypes.PersistenceType.LOCAL.name.lower().join("''"),
                " or ",
                cqltypes.PersistenceType.PERSISTENT.name.lower().join("''"),
                " previously",
            )
        else:
            persistence_type = item.persistence_type
        if item.persistence_type is cqltypes.PersistenceType.ANY:
            item.persistence_type = persistence_type
        if item.persistence_type is not persistence_type:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " dictionary ",
                name.join("''"),
                " is a ",
                item.persistence_type.name.lower().join("''"),
                " dictionary so cannot be set as a ",
                persistence_type.name.lower().join("''"),
                " dictionary",
            )

    # This method exists to allow BaseNode and Dictionary classes to be in
    # separate modules.
    def _is_node_dictionary_instance(self):
        """Return True."""
        return True


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
        if groups[3]:
            InAll(match_=self.match_, container=container).place_node_in_tree()
        for count in (1, 2):
            echovariable = Variable(
                match_=_echo_variable_re.match(groups[count]),
                container=container,
            )
            echovariable.place_node_in_tree()
            echovariable.set_variable_types(
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

    def _verify_children_and_set_own_types(self):
        """Verify filter has two arguments and the second is a SET filter."""
        # Note the instance filter type remains the default SET|LOGICAL
        # and is not resolved to one of the two.  This should be done at
        # some point.
        self.raise_if_not_number_of_children(self.child_count)
        if self.container.function_body_cursor is not None:
            return
        rhs = self.children[-1]
        if rhs.filter_type is not cqltypes.FilterType.SET:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects a ",
                cqltypes.FilterType.SET.name.join("''"),
                " domain but got a ",
                rhs.filter_type.name.join("''"),
            )


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
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " incorrect number of children to have 'else' in ",
                parent.__class__.__name__.join("''"),
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


class EnPassantSquareParameter(MoveParameterImpliesSet):
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

    def _verify_children_and_set_own_types(self):
        """Extend, raise NodeError if FEN verification fails."""
        super()._verify_children_and_set_own_types()
        if len(self.children) == 0:
            return
        fen = self.children[0].match_.group()[1:-1].split()
        if len(fen) > 6:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects at most six fields in it's argument but has ",
                str(len(fen)).join("''"),
            )
        if len(fen) > 5 and not fen[5].isdigit():
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects digits as the full move number but found ",
                fen[5].join("''"),
            )
        if len(fen) > 4 and not fen[4].isdigit():
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects digits as the half move clock but found ",
                fen[4].join("''"),
            )
        if len(fen) > 3 and re.match(r"(?:(?:[a-h][36])|-)$", fen[3]) is None:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects an en-passant destination square but found ",
                fen[3].join("''"),
            )
        if len(fen) > 2 and re.match(r"(?:(?:K?Q?k?q?)|-)$", fen[2]) is None:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects castling options such as 'KQkq' but found ",
                fen[2].join("''"),
            )
        if len(fen) > 1 and re.match(r"[wb]$", fen[1]) is None:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects the 'white or black to move' flag but found ",
                fen[1].join("''"),
            )
        ranks = fen[0].split("/")
        if len(ranks) != 8:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects exactly eight rank specifications but found ",
                str(len(ranks)).join("''"),
            )
        for rank in ranks:
            if re.match(r"[Aa._BKNPQRbknpqr1-8]+$", rank) is None:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " expects piece names or gap lengths in rank but found ",
                    str(rank).join("''"),
                )
            gap = re.search(r"[1-8](?=[1-8])", rank)
            if gap is not None:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " expects single digit gap lengths in rank but found ",
                    gap.group().join("''"),
                    " in ",
                    str(rank).join("''"),
                )
            rank_length = sum(int(i) if i.isdigit() else 1 for i in rank)
            if rank_length != 8:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " expects eight squares allocated in a rank but found ",
                    str(rank_length).join("''"),
                    " squares allocated in ",
                    str(rank).join("''"),
                )


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

    _filter_type = cqltypes.FilterType.POSITION
    _precedence = cqltypes.Precedence.P30

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        filters = set(
            f.__class__
            for f in self.children
            if isinstance(f, (All, RangeInteger, RangeVariable))
        )
        if All in filters and len(filters) > 1:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " specify either a range or 'all' parameter but not both",
            )


def is_firstmatch_parameter_accepted_by(node):
    """Return True if node accepts firstmatch parameter."""
    return (
        isinstance(node, (Line, Path))
        and node.is_instance_accepting_parameters()
    )


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
        self.set_variable_types(
            cqltypes.VariableType.SET, cqltypes.FilterType.SET
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)

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
        self.set_variable_types(
            cqltypes.VariableType.PIECE, cqltypes.FilterType.SET
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)

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
        self.set_variable_types(
            cqltypes.VariableType.SET, cqltypes.FilterType.SET
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class UniversalSquareIterator(structure.Argument):
    """Represent implied 'universal square iteration' filter."""

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
        self.set_variable_types(
            cqltypes.VariableType.PIECE, cqltypes.FilterType.SET
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class UniversalPieceIterator(structure.Argument):
    """Represent implied 'universal piece iteration' filter."""

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
    return _set_or_parameter(
        match_, container, From, FromParameter, is_from_parameter_accepted_by
    )


class FromDefaultPinParameter(FromParameter):
    """Represent default 'from' parameter to 'pin' filter."""

    def __init__(self, match_=None, container=None):
        """Initialise node parent and children attributes."""
        super().__init__(match_=match_, container=container)
        container.cursor = self
        AnyPiece(match_=match_, container=container).place_node_in_tree()

    def get_match_text(self):
        """Override and return 'from', the 'pin' parameter."""
        return "from"


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
            self.raise_nodeerror(
                "Function ",
                self.name.join("''"),
                " has duplicate parameter names",
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
        self.formal = {}

    def _raise_if_function_not_defined(self):
        """Raise NodeError if name exists with type in definition_types."""
        name = self._name
        container = self.container
        if name not in container.definitions:
            self.raise_nodeerror(
                name.join("''"), " is not defined so cannot be a function call"
            )
        if (
            container.definitions[name].definition_type
            is not cqltypes.DefinitionType.FUNCTION
        ):
            self.raise_nodeerror(
                name.join("''"),
                " is a ",
                container.definitions[name].definition_type.name.join("''"),
                " so cannot be a function call",
            )

    # This method exists to allow BaseNode and FunctionCall classes to be in
    # separate modules.
    def is_node_functioncall_instance(self):
        """Return True."""
        return True


def function_call(match_=None, container=None):
    """Return a FunctionCall, ParenthesisLeft, or TargetParenthesisLeft.

    If the cursor is an AssignPromotion return a TargetParenthesisLeft.

    If the match_.group() is in the register of function names return a
    FunctionCall instance.

    Otherwise call variable_then_parenthesis method to process the token
    as a variable name and return a ParenthesisLeft instance for the '('
    at end of token.

    """
    name = match_.groupdict()["function_call"]
    if isinstance(container.cursor, AssignPromotion):
        if container.function_body_cursor is not None:
            var = Variable(match_=match_, container=container)
            var.place_node_in_tree()
            return TargetParenthesisLeft(match_=match_, container=container)
        if name not in container.definitions:
            node = container.cursor
            while node:
                if isinstance(node, FunctionCall):
                    name = node.formal.get(name, name)
                    break
                node = node.parent
        if (
            container.definitions[name].definition_type
            is cqltypes.DefinitionType.VARIABLE
        ):
            var = Variable(match_=match_, container=container)
            var.place_node_in_tree()
        else:
            string(match_=match_, container=container).place_node_in_tree()
        return TargetParenthesisLeft(match_=match_, container=container)
    if name in container.definitions:
        if (
            container.definitions[name].definition_type
            is cqltypes.DefinitionType.FUNCTION
        ):
            return FunctionCall(match_=match_, container=container)
    var = Variable(match_=match_, container=container)
    var.name = name
    var.place_node_in_tree()
    return ParenthesisLeft(match_=match_, container=container)


class GameNumber(structure.NoArgumentsFilter):
    """Represent 'gamenumber' numeric filter.

    The 'gamenumber' keyword also appears in the parameter module.
    """

    _filter_type = cqltypes.FilterType.NUMERIC


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
        # Maybe this should be like in full() for Infix.
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
            if isinstance(self.children[1], structure.Infix):
                return self.children[1].completed
            return not isinstance(self.children[1], Else)
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

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        self.raise_if_not_same_filter_type(
            "apply intersection operation",
            filter_type=cqltypes.FilterType.SET | cqltypes.FilterType.STRING,
        )


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


class IsBound(structure.BindArgument):
    """Represent 'isbound' logical filter."""


class IsolatedPawns(structure.NoArgumentsFilter):
    """Represent 'isolatedpawns' set filter."""

    _filter_type = cqltypes.FilterType.SET


class IsUnbound(structure.BindArgument):
    """Represent 'isunbound' logical filter."""


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
    return (
        isinstance(node, (Line, Path))
        and node.is_instance_accepting_parameters()
    )


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


class _Legal(structure.LeftParenthesisInfix):
    """Provide shared behaviour of Legal and Pseudolegal filters."""

    _filter_type = cqltypes.FilterType.SET

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(1)
        if not _is_dash(self.children[0]):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " argument must be a '--' filter, not a ",
                self.children[0].__class__.__name__.join("''"),
                " filter",
            )
        for target in self.children[0].children:
            if not isinstance(target, TargetParenthesisLeft):
                continue
            if len(target.children) != 1:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " expects '1' target filter but got ",
                    str(len(target.children)).join("''"),
                )
            target.raise_if_not_number_of_children(1)
            self.raise_if_not_instance(
                target.children[0],
                (OO, OOO, Castle, EnPassant),
                "expects",
            )


class Legal(structure.Argument, _Legal):
    """Represent 'legal' set filter."""


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


class _LineOrMove(structure.CompleteParameterArguments):
    """Represent shared behaviour of 'line' and 'move' filters."""

    def _raise_if_primary_and_secondary_parameter_present(self):
        """Raise NodeError if both 'primary' and 'secondary present."""
        if (
            len(
                set(
                    c
                    for c in self.children
                    if c.__class__ in (PrimaryParameter, SecondaryParameter)
                )
            )
            > 1
        ):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot have both 'primary' and 'secondary' parameters",
            )


class Line(_LineOrMove):
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

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if len(self.children) == 0:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have at least one '<--' or '-->' component",
            )
        self._raise_if_primary_and_secondary_parameter_present()

    def is_instance_accepting_parameters(self):
        """Return False if a LineArrow is in children, otherwise delegate."""
        for child in self.children:
            if isinstance(child, LineArrow):
                return False
        return super().is_instance_accepting_parameters()


class Local(structure.CQLObject):
    """Represent 'local' not caught elsewhere for specific purposes.

    Caught in Dictionary: 'local' is only allowed to precede 'dictionary'
    and appearance elsewhere is an error.
    """

    def place_node_in_tree(self):
        """Delegate then raise NodeError because bare 'local' not allowed."""
        super().place_node_in_tree()
        self.raise_nodeerror(r"Unexpected bare 'local' found")


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
    return MainLine(match_=match_, container=container)


class MakeSquareParentheses(structure.ParenthesizedArguments):
    """Represent 'makesquare' set filter for parenthesized arguments."""

    _filter_type = cqltypes.FilterType.SET
    # See Ancestor too.
    # Treated as 'makesquare (' not 'makesquare' then '(' and ... ')'.
    # _precedence = cqltypes.Precedence.P90

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.NUMERIC)
        if len(self.children) != 2:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have exactly two components",
            )


class MakeSquareString(structure.Argument):
    """Represent 'makesquare' set filter for string argument."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P90


class Mate(structure.NoArgumentsFilter):
    """Represent 'mate' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


def is_max_parameter_accepted_by(node):
    """Return True if node accepts max parameter."""
    return isinstance(node, Path)


class Max(structure.MaxOrMin):
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
    # This is probably too simple because the parent may be at the end of a
    # chain of ancestors, one of which takes 'max' as a parameter, and can
    # accept the parameter.  For example the chain may belong to another
    # parameter of the suitable ancestor.
    if is_max_parameter_accepted_by(container.cursor):
        return MaxParameter(match_=match_, container=container)
    return Max(match_=match_, container=container)


class MessageParentheses(structure.ParenthesizedArguments):
    """Represent 'message' string filter with parentheses."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Message(structure.Argument):
    """Represent 'message' string filter without parentheses."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Min(structure.MaxOrMin):
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


class Move(structure.PrecedenceFromChild, _LineOrMove):
    """Represent 'move' set, logical, or numeric, filter.

    Copy-typed from CQLi-1.0.4 manual:

    The result type of the 'move' filter is either Boolean, Set, or
    Numeric depending on the parameters used.  If the 'count' parameter
    is specified, the result is a Numeric value indicating the number
    of matching moves at the current position.  Otherwise, if the first
    parameter is 'from', 'to', or 'capture', the result has type Set.
    Otherwise the result is Boolean and matches the position only if
    there are any matching moves at the position.

    CQL calls Boolean filters Logical filters.

    """

    _filter_type = cqltypes.FilterType.LOGICAL

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        count_allowed = False
        count_present = False
        from_to_capture_present = False
        for item, child in enumerate(self.children):
            if isinstance(child, CommentParenthesesParameter):
                if item != len(self.children) - 1:
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " parameters follow 'comment' after 'move'",
                    )
            if isinstance(child, (LegalParameter, PseudolegalParameter)):
                count_allowed = True
            if isinstance(child, Count):
                count_present = True
            if isinstance(child, (FromParameter, ToParameter, Capture)):
                from_to_capture_present = True
        if count_present and not count_allowed:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " 'legal' or 'pseudolegal' parameter must be ",
                "present with 'count' parameter ",
            )
        self._raise_if_primary_and_secondary_parameter_present()
        if count_present:
            self.filter_type = cqltypes.FilterType.NUMERIC
        elif from_to_capture_present:
            self.filter_type = cqltypes.FilterType.SET


def is_nestban_parameter_accepted_by(node):
    """Return True if node accepts nestban parameter."""
    return (
        isinstance(node, (Line, Path))
        and node.is_instance_accepting_parameters()
    )


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

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.filter_type = self.children[-1].filter_type


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

    def _verify_children_and_set_own_types(self):
        """Raise NodeError if no arguments or bad parameter combination."""
        argument_present = False
        focus_present = False
        piecepath_present = False
        repeat_allowed = False
        for child in self.children:
            if not child.is_parameter and not isinstance(child, EndPaths):
                argument_present = True
            if isinstance(child, (Focus, FocusCapture)):
                focus_present = True
            elif isinstance(child, PiecePath):
                piecepath_present = True
            elif isinstance(
                child, (structure.DashOrTake, ConstituentParenthesisLeft)
            ):
                repeat_allowed = True
            elif isinstance(child, RepeatConstituent):
                if not repeat_allowed:
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " has ",
                        child.__class__.__name__.join("''"),
                        " without a constituent filter after nearest",
                        " earlier 'repeat' filter",
                    )
                repeat_allowed = True
        if not argument_present:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have at least one argument after any parameters",
            )
        if piecepath_present and not focus_present:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " 'piecepath' parameter given without 'focus' parameter",
            )

    def is_instance_accepting_parameters(self):
        """Return False if a filter is in children, otherwise delegate."""
        for child in self.children:
            if not child.is_parameter:
                return False
        return super().is_instance_accepting_parameters()


class PersistentQuiet(structure.Complete, structure.VariableName):
    """Represent variable with 'persistent quiet' prefix.

    'persistent quiet' must be first use of variable name.

    The value of a persistent quiet variable is a Numeric, Set, or String,
    filter.  The Position filter is included too because CQL-6.2 accepts it.
    """

    def __init__(self, match_=None, container=None):
        """Delegate then register the variable name."""
        super().__init__(match_=match_, container=container)
        groupdict = match_.groupdict()
        self.name = groupdict["persistent_quiet"]
        self._register_variable_type(cqltypes.VariableType.ANY)
        self._set_persistence_type(
            cqltypes.PersistenceType.PERSISTENT
            | cqltypes.PersistenceType.QUIET
        )

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class Persistent(structure.Complete, structure.VariableName):
    """Represent variable with 'persistent' prefix.

    'persistent' must be first use of variable name.

    The value of a persistent quiet variable is a Numeric, Set, or String,
    filter.  The Position filter is included too because CQL-6.2 accepts it.
    """

    def __init__(self, match_=None, container=None):
        """Delegate then register the variable name."""
        super().__init__(match_=match_, container=container)
        groupdict = match_.groupdict()
        self.name = groupdict["persistent"]
        self._register_variable_type(cqltypes.VariableType.ANY)
        self._set_persistence_type(cqltypes.PersistenceType.PERSISTENT)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


class PieceId(structure.Argument):
    """Represent 'pieceid' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P150


class PieceName(structure.Argument):
    """Represent 'piecename' string filter.

    CQL-6.2 Table of Precedence does not give the 'pieceename' filter a
    precedence.  For 'piecename q == piecename Q' the 'piecename' filter
    must have a precedence greater than the comparison operators.
    """

    _filter_type = cqltypes.FilterType.STRING

    @property
    def precedence(self):
        """Return precedence greater than comparison when comparing.

        The comparison operator will be the '-1' child of cursor at time
        of precedence checking.

        """
        if isinstance(self.container.cursor.children[-1], structure.Infix):
            return cqltypes.Precedence.PHIGH  # Higher than P80.
        return self._precedence

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.SET)


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
        self.set_variable_types(
            cqltypes.VariableType.PIECE, cqltypes.FilterType.SET
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)


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
        self.set_variable_types(
            cqltypes.VariableType.PIECE, cqltypes.FilterType.SET
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)


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
        self.set_variable_types(
            cqltypes.VariableType.PIECE, cqltypes.FilterType.SET
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)

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

    def _verify_children_and_set_own_types(self):
        """Add missing parameters to self.children.

        The expected parameters are 'through', 'from', and 'to'.  If it
        is missing the 'through' parameter is added first.

        """
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.SET)
        saved_cursor = self.container.cursor
        present = set(i.__class__ for i in self.children)
        if Through not in present:
            self.container.cursor = self
            ThroughDefaultPinParameter(
                match_=self.match_, container=self.container
            ).place_node_in_tree()
        if FromParameter not in present:
            self.container.cursor = self
            FromDefaultPinParameter(
                match_=self.match_, container=self.container
            ).place_node_in_tree()
        if ToParameter not in present:
            self.container.cursor = self
            ToDefaultPinParameter(
                match_=self.match_, container=self.container
            ).place_node_in_tree()
        self.container.cursor = saved_cursor


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
        if len(node.children) == 0:
            return PrimaryParameter(match_=match_, container=container)
        if isinstance(node.children[-1], (ArrowBackward, ArrowForward)):
            return Primary(match_=match_, container=container)
    if len(node.children) == 0:
        if isinstance(node, cql.CQL):
            return Primary(match_=match_, container=container)
        return PrimaryParameter(match_=match_, container=container)
    if not node.children[-1].is_parameter:
        return Primary(match_=match_, container=container)
    return PrimaryParameter(match_=match_, container=container)


class Promote(structure.ParameterArgument):
    """Represent 'promote' parameter to 'move' filter."""

    def is_parameter_accepted_by_filter(self):
        """Return True if parent accepts self as a parameter."""
        return isinstance(self.parent, Move)


class Pseudolegal(structure.Argument, _Legal):
    """Represent 'pseudolegal' set filter."""


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
    return (
        isinstance(node, (ConsecutiveMoves, Echo, Find, Line, Message, Path))
        and node.is_instance_accepting_parameters()
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

    def __init__(self, match_=None, container=None):
        """Delegate then set details for this instance and add to tree."""
        super().__init__(match_=match_, container=container)
        directions = []
        for word in match_.group().split()[1:-1]:
            directions.extend(_directions[word])
        if len(directions) != len(set(directions)):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " duplicate directions in ",
                " ".join(match_.group().split()[1:-1]),
            )

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.SET)
        if len(self.children) < 2:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have at least two components",
            )


class ReadFile(structure.Argument):
    """Represent 'readfile' string filter.

    CQL-6.2 Table of Precedence does not give the 'readfile' filter a
    precedence.  For 'readfile "f" == readfile "f"' the 'readfile' filter
    must have a precedence greater than the comparison operators.
    """

    _filter_type = cqltypes.FilterType.STRING

    @property
    def precedence(self):
        """Return precedence greater than comparison when comparing.

        The comparison operator will be the '-1' child of cursor at time
        of precedence checking.

        """
        if isinstance(self.container.cursor.children[-1], structure.Infix):
            return cqltypes.Precedence.PHIGH  # Higher than P80.
        return self._precedence

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.STRING)


class RemoveComment(structure.NoArgumentsFilter):
    """Represent 'removecomment' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class Result(structure.Argument):
    """Represent 'result' logical filter.

    The 'result' keyword also appears in the parameter module.

    CQL-6.2 Table of Precedence does not give the 'result' filter a
    precedence.  For 'result "1-0" == result "1-0"' the 'result' filter
    must have a precedence greater than the comparison operators.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    @property
    def precedence(self):
        """Return precedence greater than comparison when comparing.

        The comparison operator will be the '-1' child of cursor at time
        of precedence checking.

        """
        if isinstance(self.container.cursor.children[-1], structure.Infix):
            return cqltypes.Precedence.PHIGH  # Higher than P80.
        return self._precedence

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.STRING)


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

    def _verify_children_and_set_own_types(self):
        """Override, verify PieceDesignator descendant square references."""
        self.__verify_piece_designator_descendants(self.children)

    def __verify_piece_designator_descendants(self, children):
        """Verify all PieceDesignator descendants refer to all squares."""
        for child in children:
            if isinstance(child, NoTransform):
                continue
            if isinstance(child, PieceDesignator):
                match_ = _square_designator_re.match(child.match_.group())
                if match_ is None:
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " unable to find square set in ",
                        child.match_.group().join("''"),
                    )
                match_text = match_.group(1)
                if not match_text or "a-h1-8" in match_text:
                    continue
                if "," not in match_text:
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " can only be applied to an 'all squares' ",
                        " piece designator but a ",
                        match_text.join("''"),
                        " square was found",
                    )
                    continue
                squareset = set()
                for sqr in match_text[1:-1].split(","):
                    if len(sqr) == 2:
                        squareset.add(sqr)
                    elif len(sqr) == 6:
                        squareset.update(
                            child.expand_composite_square(
                                sqr[0], sqr[2], sqr[3], sqr[5]
                            )
                        )
                    elif sqr[1] == "-":
                        squareset.update(
                            child.expand_composite_square(
                                sqr[0], sqr[2], sqr[3], sqr[3]
                            )
                        )
                    elif sqr[2] == "-":
                        squareset.update(
                            child.expand_composite_square(
                                sqr[0], sqr[0], sqr[1], sqr[3]
                            )
                        )
                if len(squareset) != 64:
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " can only be applied to an 'all squares' ",
                        " piece designator but ",
                        str(len(squareset)),
                        " squares are specified in ",
                        child.match_.group().join("''"),
                    )
                continue
            self.__verify_piece_designator_descendants(child.children)


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
        if len(node.children) == 0:
            return SecondaryParameter(match_=match_, container=container)
        if isinstance(node.children[-1], (ArrowBackward, ArrowForward)):
            return Secondary(match_=match_, container=container)
    if len(node.children) == 0:
        if isinstance(node, cql.CQL):
            return Secondary(match_=match_, container=container)
        return SecondaryParameter(match_=match_, container=container)
    if not node.children[-1].is_parameter:
        return Secondary(match_=match_, container=container)
    return SecondaryParameter(match_=match_, container=container)


class SetTag(structure.ParenthesizedArguments):
    """Represent 'settag' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if len(self.children) != 2:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have exactly two arguments",
            )
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.STRING)


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
        return (
            isinstance(self.parent, Line)
            and self.parent.is_instance_accepting_parameters()
        )


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
    _precedence = cqltypes.Precedence.P30

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        child = self.children[0]
        self.raise_if_not_filter_type(
            child,
            (
                cqltypes.FilterType.NUMERIC
                | cqltypes.FilterType.STRING
                | cqltypes.FilterType.SET
            ),
        )
        if child.filter_type in cqltypes.FilterType.SET:
            self._filter_type = cqltypes.FilterType.NUMERIC
        else:
            self._filter_type = child.filter_type


def sort(match_=None, container=None):
    """Return Sort or HHDBToken instance."""
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


class Square(structure.SquareIn):
    """Represent 'square', without 'all' parameter, set filter.

    The optional 'all' keyword is not present,

    The value of a square variable is a Set filter.
    """

    _filter_type = cqltypes.FilterType.SET


class SquareAll(structure.SquareIn):
    """Represent 'square', with 'all' parameter, logical filter.

    The optional 'all' keyword is present,

    The value of a square all variable is a Logical filter.
    """

    _filter_type = cqltypes.FilterType.LOGICAL


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

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.STRING)


class Tag(structure.Argument):
    """Represent 'tag' string filter.

    CQL-6.2 Table of Precedence does not give the 'tag' filter a
    precedence.  For 'tag "t" == tag "t"' the 'tag' filter
    must have a precedence greater than the comparison operators.
    """

    _filter_type = cqltypes.FilterType.STRING

    @property
    def precedence(self):
        """Return precedence greater than comparison when comparing.

        The comparison operator will be the '-1' child of cursor at time
        of precedence checking.

        """
        if isinstance(self.container.cursor.children[-1], structure.Infix):
            return cqltypes.Precedence.PHIGH  # Higher than P80.
        return self._precedence

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.STRING)


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
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " instance is not associated with ",
                self.parent.__class__.__name__.join("''"),
                " instance",
            )
        # This stops 'if then' and 'if <condition> <action> then' but not
        # 'if <condition> then then <action>'.
        if len(self.parent.children) != 2:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " instance is only allowed after the condition of a ",
                self.parent.__class__.__name__.join("''"),
                " instance",
            )
        # 'then then' occurs if there is an unbroken sequence of whitespace
        # back to a 'then'.
        container = self.container
        start = self.match_.start()
        for item in reversed(container.whitespace):
            if not isinstance(item, (WhiteSpace, EndCommentSymbol, Then)):
                break
            if start != item.match_.end():
                break
            if isinstance(item, Then):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " instance is separated from previous ",
                    item.__class__.__name__.join("''"),
                    " instance only by whitespace",
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


class ThroughDefaultPinParameter(Through):
    """Represent default 'through' parameter to 'pin' filter."""

    def __init__(self, match_=None, container=None):
        """Initialise node parent and children attributes."""
        super().__init__(match_=match_, container=container)
        container.cursor = self
        AnyPiece(match_=match_, container=container).place_node_in_tree()

    def get_match_text(self):
        """Override and return 'through', the 'pin' parameter."""
        return "through"


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
    return _set_or_parameter(
        match_, container, To, ToParameter, is_to_parameter_accepted_by
    )


class ToDefaultPinParameter(ToParameter):
    """Represent default 'to' parameter to 'pin' filter."""

    def __init__(self, match_=None, container=None):
        """Initialise node parent and children attributes."""
        super().__init__(match_=match_, container=container)
        container.cursor = self
        AnyKing(match_=match_, container=container).place_node_in_tree()

    def get_match_text(self):
        """Override and return 'to', the 'pin' parameter."""
        return "to"


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
    """Represent 'typename' string filter.

    CQL-6.2 Table of Precedence does not give the 'typename' filter a
    precedence.  For 'typename q == typename Q' the 'typename' filter
    must have a precedence greater than the comparison operators.
    """

    _filter_type = cqltypes.FilterType.STRING

    @property
    def precedence(self):
        """Return precedence greater than comparison when comparing.

        The comparison operator will be the '-1' child of cursor at time
        of precedence checking.

        """
        if isinstance(self.container.cursor.children[-1], structure.Infix):
            return cqltypes.Precedence.PHIGH  # Higher than P80.
        return self._precedence

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.SET)


class Type(structure.Argument):
    """Represent 'type' numeric filter."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P150


class Unbind(structure.BindArgument):
    """Represent 'unbind' logical filter.

    'unbind' removes the value associated with a variable, dictionary or
    dictionary entry, but does not affect the variable or dictionary type.
    """

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        subject = self.children[0]
        if not isinstance(subject, BracketLeft):
            super()._verify_children_and_set_own_types()
        else:
            subject = subject.children[0]
        name = subject.name
        if name not in self.container.definitions:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects the name of an existing dictionary, ",
                "function, or variable",
            )
        # Referring to an unbound key, 'D[<key>]' where 'D[<key>]=<value>' has
        # not been done is ok except for 'unbind D[<key>]'.
        # 'unbind D' is always ok after 'dictionary D' with or without key
        # bindings.
        if subject is self.children[0]:
            return
        item = self.container.definitions[name]
        if isinstance(item, cqltypes.Dictionary):
            if item.key_filter_type is cqltypes.FilterType.ANY:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " expects the name of a bound key to dictionary ",
                    item.__class__.__name__.join("''"),
                )


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

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if len(self.children) != 2:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have exactly two components",
            )
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.STRING)


class WTM(structure.NoArgumentsFilter):
    """Represent 'wtm' logical filter."""

    _filter_type = cqltypes.FilterType.LOGICAL


class XRay(structure.ParenthesizedArguments):
    """Represent 'xray' set filter."""

    _filter_type = cqltypes.FilterType.SET

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        for child in self.children:
            self.raise_if_not_filter_type(child, cqltypes.FilterType.SET)
        if len(self.children) < 2:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " must have at least two components",
            )


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

    def __init__(self, match_=None, container=None):
        """Verify 'a-h' and '2-5' style file and rank specifications."""
        super().__init__(match_=match_, container=container)
        for first, last in _file_rank_re.findall(self.match_.group()):
            if first > last:
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " file" if first in "abcdefgh" else " rank",
                    " specification ",
                    "-".join((first, last)),
                    " is not allowed in ",
                    self.match_.group().join("''"),
                )

    # Originally left to a piece designator evaluation class, but 'rotate45'
    # filter parsing needs this to decide if the operation is allowed.
    @staticmethod
    def expand_composite_square(startfile, endfile, startrank, endrank):
        """Return the set of squares implied by a square designator."""
        file_names = constants.FILE_NAMES
        cql_rank_names = constants.CQL_RANK_NAMES
        files = file_names[
            file_names.index(startfile) : file_names.index(endfile) + 1
        ]
        ranks = cql_rank_names[
            cql_rank_names.index(startrank) : cql_rank_names.index(endrank) + 1
        ]
        return {f + r for f in files for r in ranks}


class ResultArgument(structure.NoArgumentsFilter):
    """Represent the argument of the result filter.

    Value is '1-0', '0-1', or '1/2-1/2'.
    """


def is_range_parameter_accepted_by(node):
    """Return True if node accepts range parameter."""
    return (
        isinstance(
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
        and node.is_instance_accepting_parameters()
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
        self.set_variable_types(
            cqltypes.VariableType.NUMERIC, cqltypes.FilterType.NUMERIC
        )
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)

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
        # The 'function_call' reference is needed because 'T(' in '--=T(R)'
        # is seen as a function call by pattern matching and has to be
        # diverted if the '=' was seen as an 'AssignPromotion' instance.
        self.name = (
            groupdict["variable"]
            or groupdict["variable_assign"]
            or groupdict["function_call"]
        )
        self._register_variable_type(cqltypes.VariableType.ANY)
        self._set_persistence_type(cqltypes.PersistenceType.LOCAL)

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self

    def is_variable(self):
        """Override and return True."""
        return True


class BindName(structure.Complete, structure.Name):
    """Represent the name of a dictionary, function, or variable.

    Intended to support the 'isbound', 'isunbound', and 'unbind' filters.

    None of these filters cause the name to be registed, but 'unbind'
    expects the name to be in the register.

    """

    def __init__(self, match_=None, container=None):
        """Delegate then register the variable name."""
        super().__init__(match_=match_, container=container)
        groupdict = match_.groupdict()
        # The "variable" reference must be first to allow for variables
        # defined by 'echo' pattern.
        self.name = groupdict["variable"] or groupdict["variable_assign"]

    def place_node_in_tree(self):
        """Delegate then set cursor to self."""
        super().place_node_in_tree()
        self.container.cursor = self


def _numeric_variable(match_=None, container=None):
    """Return Variable, or RangeVariable if collecting a range."""
    node = container.cursor
    while True:
        if not node.is_parameter:
            break
        node = node.parent
    if is_range_parameter_accepted_by(node):
        if is_too_many_range_integers(container.cursor):
            return Variable(match_=match_, container=container)
        if is_range_start_or_continuation(container.cursor):
            return RangeVariable(match_=match_, container=container)
    return Variable(match_=match_, container=container)


def variable(match_=None, container=None):
    """Return an instance of a class representing a variable name.

    These are Variable, PieceVariable, Dictionary, BindName, and
    HHDBToken.  The called function _numeric_variable adds RangeVariable
    to the list.

    A Dictionary instance is returned only if the name is already defined
    as a dictionary.

    Function definition and call variables are detected by patterns tuned
    to functions.

    Assignment to variables is detected by patterns tuned to the piece,
    square, and plain variable, cases.

    """
    name = match_.groupdict()["variable"]
    definitions = container.definitions
    if name in definitions:
        definition_type = definitions[name].definition_type
        if definition_type is cqltypes.DefinitionType.DICTIONARY:
            return Dictionary(match_=match_, container=container)
        if definition_type is not cqltypes.DefinitionType.VARIABLE:
            container.raise_nodeerror(
                "Name '",
                name,
                "' should be a '",
                cqltypes.DefinitionType.VARIABLE.name,
                "' but is a '",
                definition_type.name,
                "'",
            )
        variable_type = definitions[name].variable_type
        if variable_type is cqltypes.VariableType.NUMERIC:
            return _numeric_variable(match_=match_, container=container)
        if variable_type is cqltypes.VariableType.PIECE:
            return PieceVariable(match_=match_, container=container)
    if isinstance(container.cursor, structure.BindArgument):
        return BindName(match_=match_, container=container)
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
            container.raise_nodeerror(
                "'",
                container.cursor.__class__.__name__,
                "' cannot assign to a '",
                definition_type.name.lower(),
                "' as a plain variable",
            )
        variable_type = definitions[name].variable_type
        if variable_type is cqltypes.VariableType.PIECE:
            container.raise_nodeerror(
                "'",
                container.cursor.__class__.__name__,
                "' cannot assign to a '",
                variable_type.name.lower(),
                "' variable as a plain variable",
            )
    return Variable(match_=match_, container=container)


# '\' is used in three ways,
#   to indicate certain single-character strings such as '\n'
#   to indicate the value of, or index into source string of, capturing group
#   to indicate special characters in regular expressions
# All these are represented by specific classes: a bare '\' indicates an
# error.
class Backslash(structure.CQLObject):
    r"""Represent escaped strings '\\', '\"', '\n', '\r', and '\t'."""

    _filter_type = cqltypes.FilterType.STRING


class AnySquare(PieceDesignator):
    """Represent '.' set filter (utf8 ▦ '\u25a6').

    It is a piece designator meaning all squares.

    The text '.' and '▦' in a CQL query causes an AnySquare instance to
    be generated.

    For '--'-like filters it is the implicit lhs or rhs argument where
    an explicit filter is absent.

    In CQL() parameters it appears in file names unprotected by quotes.
    """

    def get_match_text(self):
        """Override and return '.', ASCII form of 'any square' filter."""
        return "."


class AnyPiece(PieceDesignator):
    """Represent '[Aa]' set filter (utf8 ◭ '\u25ed').

    It is a piece designator meaning any white or black piece.

    The text '[Aa]' and '◭' in a CQL query causes a PieceDesignator
    instance to be generated.

    For 'pin' filters it is the argument of the implied 'through' and
    'from' parameters if these parameters are not explicit.
    """

    def get_match_text(self):
        """Override and return '[Aa]', ASCII form of 'any piece' filter."""
        return "[Aa]"


class AnyKing(PieceDesignator):
    """Represent '[Kk]' set filter (utf8 ♔♚ '\u2654\u265a').

    It is a piece designator meaning any white or black king.

    The text '[Kk]' and '♔♚' in a CQL query causes a PieceDesignator
    instance to be generated.

    For 'pin' filters it is the argument of the implied 'to' parameter
    if this parameter is not explicit.
    """

    def get_match_text(self):
        """Override and return '[Kk]', ASCII form of 'either king' filter."""
        return "[Kk]"


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

    @property
    def filter_type(self):
        """Return filter_type from variable's entry in definitions."""
        name = self.children[0].name
        if self.container.function_body_count > 0:
            if name not in self.container.definitions:
                return cqltypes.FilterType.ANY
        try:
            return self.container.definitions[name].filter_type
        except KeyError as exc:
            raise basenode.NodeError(
                "".join(
                    (
                        "Name definition '",
                        str(name),
                        "' referenced before it is set",
                    )
                )
            ) from exc

    def set_variable_types(self, variable_type, filter_type):
        """Set filter type of self.children[0] instance.

        This is assumed to be a Dictionary instance at present.

        """
        if isinstance(self.children[0], Dictionary):
            self.children[0].set_variable_types(
                self.children[1].filter_type, filter_type
            )
        else:
            self.children[0].set_variable_types(variable_type, filter_type)

    # Some verification done in Assign._verify_children_and_set_own_types can
    # be moved here now this method exists.
    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        lhs = self.children[0]
        if isinstance(lhs, (IsBound, IsUnbound)):
            name = lhs.children[0].name
            if name not in self.container.definitions:
                self.raise_nodeerror(
                    lhs.__class__.__name__.join("''"),
                    " expects the name of a dictionary, not ",
                    name.join("''"),
                )
            if not isinstance(lhs.children[0], Dictionary):
                self.raise_nodeerror(
                    lhs.__class__.__name__.join("''"),
                    " expects name ",
                    name.join("''"),
                    " to refer to a dictionary, not a ",
                    lhs.children[0].__class__.__name__.join("''"),
                )
            return
        if isinstance(lhs, structure.VariableName):
            if (
                lhs.container.definitions[lhs.name].filter_type
                is cqltypes.FilterType.ANY
            ):
                self.raise_nodeerror(
                    lhs.__class__.__name__.join("''"),
                    " cannot reference an undefined variable by ",
                    "index (like V[1])",
                )


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
        self._raise_if_cursor_is_not_expected_class(BracketLeft)


def bracket_right(match_=None, container=None):
    """Return BracketRight instance."""
    node = container.cursor
    while node:
        if isinstance(node, BracketLeft):
            if len(node.children) > 1 and isinstance(
                node.children[0], structure.VariableTypeSetter
            ):
                for child in node.children[1:]:
                    node.children[0].raise_if_child_cannot_be_index(child)
            return BracketRight(match_=match_, container=container)
        if isinstance(node, ParenthesisLeft):
            node.raise_nodeerror(
                "'",
                node.__class__.__name__,
                "' cannot close a '(' parenthesized block with ']'",
            )
        if isinstance(
            node,
            (ConstituentParenthesisLeft, LineConstituentParenthesisLeft),
        ):
            node.raise_nodeerror(
                "'",
                node.__class__.__name__,
                "' cannot close a '(' top level constituent with ']'",
            )
        if isinstance(node, BraceLeft):
            node.raise_nodeerror(
                "'",
                node.__class__.__name__,
                "' cannot close a '{' compound filter with ']'",
            )
        if isinstance(node, structure.ParenthesizedArguments):
            node.raise_nodeerror(
                "'",
                node.__class__.__name__,
                "' cannot close parenthesized arguments with ']'",
            )
        node = node.parent
    container.raise_nodeerror(
        "Unexpected ", str(node), " found while trying to match a ']'"
    )
    # A pylint R1710 inconsistent-return-statements report indicates the
    # absence of this statement.
    raise RuntimeError("This point is intentionally unreachable")


class Colon(structure.InfixRight):
    """Represent ':' filter between a position filter and a filter."""

    _filter_type = cqltypes.FilterType.ANY
    _precedence = cqltypes.Precedence.P230  # Reference says ':', no context.

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        if self.container.function_body_cursor is not None:
            return
        self.filter_type = self.children[-1].filter_type

    def place_node_in_tree(self):
        """Delegate then verify first child is a Position filter."""
        super().place_node_in_tree()
        if len(self.children) == 0:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"), " has no arguments"
            )
        if self.container.function_body_cursor is not None:
            return
        if self.children[0].filter_type is not cqltypes.FilterType.POSITION:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " lhs filter type must be ",
                str(cqltypes.FilterType.POSITION),
                " but actual filter is ",
                self.children[0].__class__.__name__.join("''"),
                " of type ",
                str(self.children[0].filter_type).join("''"),
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
    # verify_children_and_set_types() method for BraceLeft so
    # switch to verifying in the filter_type property.  At time of writing
    # the 'BraceLeft' parsing failures are fixed but others, where
    # filter type is not yet handled, still fail parsing with the addition
    # of child verification.  It is assumed possible the children of a node
    # may not be in their completed configuration if verification is done
    # in verify_children_and_set_types().
    # The override of filter_type property should not be needed if this
    # _verify_children_and_set_own_types method gets called before accessing
    # the property.
    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        self.raise_if_not_same_filter_type(
            "apply intersection operation",
            filter_type=cqltypes.FilterType.SET | cqltypes.FilterType.POSITION,
        )


class LT(structure.Compare, structure.InfixRight):
    """Represent '>' numeric or string filter between two filters."""

    _precedence = cqltypes.Precedence.P80


class GT(structure.Compare, structure.InfixRight):
    """Represent '>' numeric or string filter between two filters."""

    _precedence = cqltypes.Precedence.P80


def _lookahead(match_, token_names):
    """Return True if first token found beyond match_ is in token_names.

    If no tokens are found beyond match_ return True.

    True means treat the '+' or '*' as a repetition operator, not an
    arithmetic operator.

    """
    for token in pattern.cql_re.finditer(match_.string, match_.end()):
        tokens = {
            key
            for key, value in token.groupdict().items()
            if value is not None and key not in _ALL_WHITESPACE
        }
        if tokens:
            return token_names & tokens
    return True


# The '*' in 'line --> not move from Front*', 'Front' is a piece variable
# in this example, is the regular expression repetition operator not the
# arithmetic multiplication operator.
def _is_repeat_0_or_1_to_many(match_, container, filter_types):
    """Return True if match_ represents a regular expression operation."""
    node = container.cursor
    while True:
        if node is None:
            return False
        if (
            isinstance(
                node,
                (LineConstituentParenthesisLeft, ConstituentParenthesisLeft),
            )
            and node.complete()
        ):
            break  # return True
        if isinstance(node, LineArrow):
            if container.cursor.filter_type in filter_types:
                return _lookahead(match_, _ARROWS | _BLOCK_ENDS)
            break  # return True
        if not node.full():
            if isinstance(node, (Path, ConstituentParenthesisLeft)):
                break  # return True
            if not isinstance(node, LineConstituentParenthesisLeft):
                return False
            if container.cursor.filter_type is not cqltypes.FilterType.NUMERIC:
                break  # return True
            return _lookahead(match_, _ARROWS)
        node = node.parent
    # Avoid pylint R0911 too-many-return-statements with 'break'.
    return True


# This has same effect as WildcardPlus.
class PlusRepeat(RepeatConstituent):
    """Represent '+' repetition operation on a constituent filter.

    The 'path' and 'line' filters use constituent filters.
    """

    _precedence = cqltypes.Precedence.P20


class Plus(structure.Numeric):
    """Represent '+' filter between two numeric or string filters."""

    _filter_type = cqltypes.FilterType.NUMERIC | cqltypes.FilterType.STRING
    _precedence = cqltypes.Precedence.P110

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        self.raise_if_not_same_filter_type(
            "apply arithmetic or string concatenation operation",
            filter_type=cqltypes.FilterType.NUMERIC
            | cqltypes.FilterType.STRING,
        )
        if self.container.function_body_cursor is None:
            self.filter_type = self.children[0].filter_type


def plus(match_=None, container=None):
    """Return a Plus, or PlusRepeat, instance depending on context of '+'."""
    if _is_repeat_0_or_1_to_many(
        match_,
        container,
        (cqltypes.FilterType.NUMERIC, cqltypes.FilterType.STRING),
    ):
        return PlusRepeat(match_=match_, container=container)
    return Plus(match_=match_, container=container)


# This has same effect as WildcardStar.
class StarRepeat(RepeatConstituent):
    """Represent '*' repetition operation on a constituent filter.

    The 'path' and 'line' filters use constituent filters.
    """

    _precedence = cqltypes.Precedence.P20


class Star(structure.Numeric):
    """Represent '*' filter between two numeric filters."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P140


def star(match_=None, container=None):
    """Return a Star, or StarRepeat, instance depending on context of '*'."""
    if _is_repeat_0_or_1_to_many(
        match_, container, cqltypes.FilterType.NUMERIC
    ):
        return StarRepeat(match_=match_, container=container)
    return Star(match_=match_, container=container)


class Modulus(structure.Numeric):
    """Represent '%' filter between two numeric filters."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P140


class Divide(structure.Numeric):
    """Represent '/' filter between two numeric filters."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P140


class Minus(structure.Numeric):
    """Represent '-' filter between two numeric filters, eg '1 + 2'."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P110


class UnaryMinus(structure.Argument):
    """Represent '-' filter before a numeric filter, eg 'v = -1'."""

    _filter_type = cqltypes.FilterType.NUMERIC
    _precedence = cqltypes.Precedence.P130

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(1)
        if self.container.function_body_cursor is not None:
            return
        if self.children[0].filter_type is not cqltypes.FilterType.NUMERIC:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects a numeric argument but got a ",
                self.children[0].filter_type.name.lower().join("''"),
            )


def minus(match_=None, container=None):
    """Return Minus or UnaryMinus instance."""
    node = container.cursor
    while node and node.full():
        if node.filter_type is cqltypes.FilterType.NUMERIC:
            return Minus(match_=match_, container=container)
        if isinstance(node, structure.BlockLeft):
            return UnaryMinus(match_=match_, container=container)
        node = node.parent
    if isinstance(node, structure.Compare):
        return UnaryMinus(match_=match_, container=container)
    if node and node.filter_type is cqltypes.FilterType.NUMERIC:
        return Minus(match_=match_, container=container)
    return UnaryMinus(match_=match_, container=container)


class Complement(structure.Argument):
    """Represent '~' filter on a set filter."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P180

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(1)
        self.raise_if_not_filter_type(
            self.children[0],
            cqltypes.FilterType.SET,
        )


class Union(structure.InfixLeft):
    """Represent '|' filter between two set filters."""

    _filter_type = cqltypes.FilterType.SET
    _precedence = cqltypes.Precedence.P160

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(2)
        self.raise_if_not_same_filter_type(
            "apply union operation",
            filter_type=cqltypes.FilterType.SET,
        )


# Because 'cql() variable=1' is ok but 'cql() variable' is not ok. (? later)
# BracketLeft added into tests to allow 'D[pathcount]=to', for example, to
# be accepted.  More work needed because there are no restrictions on what
# is inside the '[]'.
class Assign(structure.InfixLeft):
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

    # '=' has the same precedence as 'find', and others, according to CQLi
    # but no precedence is given in CQL's Table of Precedence.
    # P30 gives an exception for 'v=k or q' but P90, the same as '+=' and
    # similar, does not give exception when combined with changes to
    # class hierarchy.
    # The CQL-6.0.4 and CQL-6.1 idealmate and modelmate examples fail
    # parsing at precedence P90 citing a problem with the 'In' class.
    # No exception occurs at P65 (just below 'In' precedence P70) combined
    # with change in class hierarchy.
    _precedence = cqltypes.Precedence.P65

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        lhs = self.children[0]
        self.raise_if_not_instance(
            lhs,
            (
                Variable,
                Persistent,
                PersistentQuiet,
                PieceVariable,
                BracketLeft,  # For slices and dictionary keys.
                Atomic,
            ),
            "lhs must be a",
        )
        if self.container.function_body_cursor is not None:
            return
        rhs = self.children[1]
        if self.container.function_body_cursor is None or not isinstance(
            rhs, structure.VariableName
        ):
            if (
                rhs.filter_type is not cqltypes.FilterType.SET
                and rhs.filter_type is not cqltypes.FilterType.NUMERIC
                and rhs.filter_type is not cqltypes.FilterType.STRING
                and rhs.filter_type is not cqltypes.FilterType.POSITION
            ):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " rhs must be a Set, Numeric, String,",
                    " or Position, filter",
                )
            if isinstance(lhs, BracketLeft):
                if (
                    isinstance(lhs.children[0], structure.VariableName)
                    and lhs.children[0].filter_type is cqltypes.FilterType.ANY
                ):
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " cannot assign to an undefined variable by ",
                        'index (like V[1]="a")',
                    )
                if (
                    rhs.filter_type is cqltypes.FilterType.POSITION
                    and not _is_local_dictionary(lhs.children[0])
                ):
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " lhs is a 'dictionary' but not 'local' so rhs ",
                        "cannot be a Position filter",
                    )
                # This check on filter type of key is better placed in the
                # BracketLeft, or perhaps BracketRight, class but that area
                # may change because the BracketLeft Dictionary tree looks
                # odd.
                if lhs.children[1].filter_type is cqltypes.FilterType.LOGICAL:
                    self.raise_nodeerror(
                        self.__class__.__name__.join("''"),
                        " lhs is a 'dictionary' and does not accept a ",
                        lhs.children[1].__class__.__name__.join("''"),
                        " as a key",
                    )
            elif (  # Must be a VariableName instance.
                rhs.filter_type is cqltypes.FilterType.POSITION
                and cqltypes.PersistenceType.PERSISTENT
                in self.container.definitions[lhs.name].persistence_type
            ):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " lhs is a persistent variable and cannot be ",
                    "assigned a position filter",
                )
        if self.container.function_body_cursor is None or (
            not isinstance(lhs, structure.VariableName)
            and not isinstance(rhs, structure.VariableName)
        ):
            self.raise_if_not_same_filter_type(
                "assign",
                allowany=(
                    isinstance(lhs, (structure.VariableName, BracketLeft))
                    and lhs.filter_type is cqltypes.FilterType.ANY
                ),
            )
        self._set_types_lhs(lhs, rhs)

    def place_node_in_tree(self):
        """Delegate then vefify LHS is a variable."""
        parent = self.parent
        self._raise_if_parent_is_not_cursor(parent)
        self._swap_tree_position(parent.parent)
        self._verify_and_set_filter_type(parent)
        if isinstance(parent, Assign):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot chain variable assignment",
            )

    def _set_types_lhs(self, lhs, rhs):
        """Set types for lhs filter appropriate for rhs filter.

        The rhs must be a set, numeric, string, or position, filter.

        """
        if rhs.is_set_filter:
            lhs.set_variable_types(
                (
                    cqltypes.VariableType.PIECE
                    if isinstance(lhs, PieceVariable)
                    else cqltypes.VariableType.SET
                ),
                cqltypes.FilterType.SET,
            )
            return
        if rhs.is_numeric_filter:
            lhs.set_variable_types(
                cqltypes.VariableType.NUMERIC,
                cqltypes.FilterType.NUMERIC,
            )
            return
        if rhs.is_string_filter:
            lhs.set_variable_types(
                cqltypes.VariableType.STRING,
                cqltypes.FilterType.STRING,
            )
            return
        if rhs.is_position_filter:
            lhs.set_variable_types(
                cqltypes.VariableType.POSITION,
                cqltypes.FilterType.POSITION,
            )
            return
        self.raise_nodeerror(
            self.__class__.__name__.join("''"),
            " cannot set lhs filter type because rhs filter type is ",
            str(rhs.filter_type).join("''"),
        )


class AssignIf(structure.MoveInfix):
    """Represent '=?', conditional variable assignment, logical filter.

    LHS cannot be PieceVariable or Dictionary item.

    RHS must be a set filter.
    """

    _filter_type = cqltypes.FilterType.LOGICAL

    # '=?' has the same precedence as '+=', and others including all the
    # '<operatore>=' filters, according to CQLi but no precedence is given
    # in CQL's Table of Precedence.
    # _precedence = cqltypes.Precedence.P30
    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        lhs = self.children[0]
        self.raise_if_not_instance(
            lhs,
            (Variable, Persistent, PersistentQuiet),
            "lhs must be a",
        )
        rhs = self.children[1]
        if not isinstance(rhs, structure.VariableName):
            self.raise_if_not_filter_type(rhs, cqltypes.FilterType.SET)
        if not isinstance(lhs, structure.VariableName) and not isinstance(
            rhs, structure.VariableName
        ):
            self.raise_if_not_same_filter_type(
                "assign",
                allowany=(
                    isinstance(lhs, structure.VariableName)
                    and lhs.filter_type is cqltypes.FilterType.ANY
                ),
            )
        self._set_types_lhs(lhs, rhs)

    def place_node_in_tree(self):
        """Delegate then vefify LHS is a variable."""
        super().place_node_in_tree()
        if isinstance(self.parent, Assign):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " cannot chain variable assignment",
            )

    def _set_types_lhs(self, lhs, rhs):
        """Set types for lhs filter appropriate for rhs filter.

        The rhs must be a set filter.

        """
        if self.container.function_body_cursor is not None:
            return
        if rhs.is_set_filter:
            # Probably incomplete because of piece and square variables.
            lhs.set_variable_types(
                cqltypes.VariableType.SET,
                cqltypes.FilterType.SET,
            )
            return
        self.raise_nodeerror(
            self.__class__.__name__.join("''"),
            " cannot set lhs filter type because rhs filter type is ",
            str(rhs.filter_type).join("''"),
        )


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
        # self._raise_if_node_not_child_of_filters("=", AnySquare)
        node = self.parent
        node.children[-1].parent = node.parent
        node.parent.children.append(node.children.pop())
        self.container.cursor = self

    def _verify_children_and_set_own_types(self):
        """Raise NodeError if child cannot be a promotion piece."""
        child = self.children[0]
        # This block has no effect on existing unittests but does allow
        # the CQL-6.2 examples which did not fail parsing to continue not
        # failing.  Comment to be removed when all '--' unittests pass.
        if isinstance(child, (structure.VariableName, Dictionary)):
            if (
                self.container.function_body_cursor is None
                and child.filter_type is not cqltypes.FilterType.STRING
            ):
                self.raise_nodeerror(
                    self.__class__.__name__.join("''"),
                    " expects a piece type designator or string but got a ",
                    child.__class__.__name__.join("''"),
                    " with filter type ",
                    child.filter_type.name.join("''"),
                )
            return
        if isinstance(child, TypeDesignator):
            return
        if isinstance(child, PieceDesignator):
            if _type_designator_piece_re.fullmatch(child.match_.group()):
                return
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects a piece type designator but got a ",
                child.match_.group().join("''"),
                " piece designator",
            )
            # See string() for for validation of promotion piece as quoted
            # string.  Perhaps it must be there for CQL-6.1 syntax.
        # CQL parsing does not ban promotion to king or pawn.
        if child.filter_type is not cqltypes.FilterType.STRING:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects string but got a ",
                child.__class__.__name__.join("''"),
            )
        if _type_designator_piece_re.fullmatch(child.match_.group()[1:-1]):
            return
        self.raise_nodeerror(
            self.__class__.__name__.join("''"),
            " expects a piece type designator but got a ",
            child.match_.group().join("''"),
            " piece designator",
        )


def assign(match_=None, container=None):
    """Return Assign or AssignPromotion instance."""
    if _is_dash_or_capture(container.cursor.parent):
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

    def _verify_children_and_set_own_types(self):
        """Override, raise NodeError if children verification fails."""
        self.raise_if_not_number_of_children(1)
        self.raise_if_not_filter_type(
            self.children[0],
            cqltypes.FilterType.SET | cqltypes.FilterType.STRING,
        )


class AnythingElse(structure.CQLObject):
    """Represent any (Python) str not caught by any other pattern.

    This construct also occurs in parameters module.
    """

    def place_node_in_tree(self):
        """Delegate then raise NodeError for unexpected token."""
        super().place_node_in_tree()
        self.raise_nodeerror(
            "Unexpected ", self.match_.group().join("''"), " found"
        )


class EndOfStream(structure.Complete):
    """Represent end of str containing CQL statement.

    The 'end of stream' construct also appears in the parameter module.
    """

    _is_allowed_first_object_in_container = True

    def place_node_in_tree(self):
        """Delegate then move to container whitespace.

        All nodes should be complete now.

        CQL requires at least one filter.  This parser allows queries
        with no filters and passes the decision on no filters to the
        evaluator (because it fits what ChessTab does).

        """
        super().place_node_in_tree()
        self.container.whitespace.append(self.parent.children.pop())
        if not isinstance(
            self.parent, (querycontainer.QueryContainer, cql.CQL)
        ):
            self.raise_nodeerror("Unexpected end of statement found")
        # This copes with simple non-filter text in a query which is seen
        # as variable names, like 'cql(<stuff>) some thing'.
        # The general case of an unassigned variable hidden in a query is
        # not covered.
        for child in self.parent.children:
            if (
                isinstance(child, Variable)
                and child.filter_type is cqltypes.FilterType.ANY
            ):
                self.raise_nodeerror(
                    "Variable ",
                    child.name.join("''"),
                    " has not been assigned",
                )
        self.parent = None


def end_of_stream(match_=None, container=None):
    """Return a EndOfStream or EndPaths instance."""
    node = container.cursor
    while node:
        if isinstance(node, (CommentSymbol, Path)):
            return EndPaths(match_=match_, container=container)
        node = node.parent
    return EndOfStream(match_=match_, container=container)


def _no_intervening_whitespace(prior, current):
    """Return True if no whitespace exists between prior and current.

    The 'prior' and 'current' arguments should be re.Match objects.

    """
    # pycodestyle E203 whitespace before ':'.
    # black insists on " : " format.
    filler = prior.string[prior.end() : current.start()]
    return not filler or filler.split() == [filler]


def _is_dash_or_capture(filter_):
    """Return True if filter_ class represents '--' or '[x]' filter."""
    return isinstance(
        filter_,
        (DashII, DashIR, DashLI, DashLR, TakeII, TakeIR, TakeLI, TakeLR),
    )


def _is_dash(filter_):
    """Return True if filter_ class represents '--' filter."""
    return isinstance(filter_, (DashII, DashIR, DashLI, DashLR))


def _set_or_parameter(
    match_, container, set_, parameter, is_parameter_accepted_by
):
    """Return set_ or parameter instance for match_.

    This function exists to handle 'to' and 'from' keywords depending on
    the effect of 'pin' and 'move' keywords.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if node.is_parameter and not node.full():
            return set_(match_=match_, container=container)
        if isinstance(node, (CommentParameter, CommentParenthesesParameter)):
            return set_(match_=match_, container=container)
        if is_parameter_accepted_by(node):
            return parameter(match_=match_, container=container)
        node = node.parent
    return set_(match_=match_, container=container)


def _string_or_parentheses_comment(match_, container, general, after_move):
    """Return general or after 'move' filter version of comment.

    This function exists to support 'comment ("s")' and 'comment "s"'.

    """
    node = container.cursor
    while True:
        if node is None:
            break
        if is_comment_parameter_accepted_by(node):
            for child in node.children:
                if isinstance(child, (LegalParameter, PseudolegalParameter)):
                    return general(match_=match_, container=container)
            return after_move(match_=match_, container=container)
        if not node.full():
            break
        node = node.parent
    return general(match_=match_, container=container)


def _is_local_dictionary(filter_):
    """Return True if filter_ class represents 'local dictionary' filter."""
    if not isinstance(filter_, Dictionary):
        return False
    if (
        "local" not in filter_.match_.group()
        and cqltypes.PersistenceType.ANY
        in filter_.container.definitions[filter_.name].persistence_type
    ):
        return False
    return (
        cqltypes.PersistenceType.LOCAL
        in filter_.container.definitions[filter_.name].persistence_type
    )


def _is_lhs_implicit(match_, container):
    """Return True if character before match_implies implicit lhs.

    Relevant to '--' and '[x]' filters.

    """
    # In 'to--' the 'to' is lhs filter but in 'path--' the '--' is an
    # argument of 'path' filter so lhs filter is implicit.  Same for '[x]'
    # and utf8 versions and utf8 version of 'path'.
    peek = match_.string[match_.start() - 1]
    if (
        isinstance(container.cursor, Path)
        or peek in ")"
        and isinstance(container.cursor, ConstituentParenthesisLeft)
    ):
        return True
    return peek in "({:="


def _is_rhs_implicit(match_):
    """Return True if character after match_implies implicit rhs.

    Relevant to '--' and '[x]' filters.

    """
    return match_.string[match_.end()] in "+-*/%><!)}=(?"
