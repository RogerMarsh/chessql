# parser.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) parser.

The basic structure of a CQL statement at version 6.0 is:

'cql ( parameters ) list_of_filters'.

All filters have a class definition, and most filters are referred to by
a keyword ('between' for example) or a symbol ('<=' for example).

The Piece Designator filter does not have a keyword or a symbol; any
string with a particular structure is a reference to a piece designator
CQL object.

Many parameters, including parameters of filters, are referred to by
keyword.  These parameters have a class definition.

Other strings are interpreted as variables or integers, and these become
instances of the 'Variable' and 'integer' classes.

Every 'name' in a '(?P<name>)' clause in the .constants.CQL_TOKENS pattern
has a class definition here.  The 'between' filter is represented in
CQL_TOKENS by BETWEEN which causes a match on the word 'between' captured
under key 'between' in the group dictionary.  The corresponding class here
is 'Between'.

CQLi-1.0.3 accepts this query but CQL-6.2 rejects it (give the -parse
option because actually running the query is not relevant here):

cql(input heijden.pgn)
function Z(){function Y(){k} Y() W=1}
function X(){function Y(){q} Y() W="a"}
Z()
X()

CQL-6.2 objects to Y as a function name in the body of function X.

On changing both 'Y's in the body of function X to V CQL-6.2 objects to
assigning a string to variable W in the body of function X.

On additionally changing the W to T in the body of function X CQL-6.2
accepts the query.

On additionally adding a second function call to X or Z CQL-6.2 rejects
the query because either V or Y is already defined, for example:

cql(input heijden.pgn)
function Z(){function Y(){k} Y() W=1}
function X(){function V(){q} V() T="a"}
Z()
X()
Z()

but CQLi-1.0.3 accepts it.

Since this module is following CQL, not CQLi, the global scope of user
defined names is acceptable.

"""
import re
import os

from . import elements
from . import pattern
from . import tokenmap
from . import querycontainer
from . import options

_comment_re = re.compile(
    r"|".join(
        (
            elements.BLOCK_COMMENT,
            elements.LINE_COMMENT,
            elements.STRING,
            elements.COMMENT_SYMBOL,
            r'(?P<anything_else>)[^/"]+',  # Not elements.ANYTHING_ELSE set.
            r'[/"]',
        )
    )
)


def populate_container(container, string, *args):
    """Populate container instance from parsed query in string."""
    container.place_node_in_tree()
    for token in pattern.cql_re.finditer(
        _remove_comments(string, container), *args
    ):
        container.current_token = token
        classes = {
            key: tokenmap.class_from_token_name[key]
            for key, value in token.groupdict().items()
            if value is not None
        }
        container.raise_if_not_single_match_groupdict_entry(token, classes)
        for value in classes.values():
            value(
                match_=token,
                container=container,
            ).place_node_in_tree()


def parse(string):
    """Return a QueryContainer instance for query in string.

    A basenode.NodeError is raised if the parse fails.

    The command line is ignored: the caller must make arrangements to
    provide a query string.

    """
    container = querycontainer.QueryContainer()
    populate_container(container, string)
    return container


def parse_command_line_query():
    """Return QueryContainer instance for query specified in command line.

    A basenode.NodeError is raised if the parse fails.

    The query is taken from the final option on the command line: assumed
    to refer to a *.cql file name.

    """
    container = querycontainer.QueryContainer()
    container.options.get_options()
    opts = container.options.options
    if not opts or not isinstance(opts[-1], options.CqlFileName):
        raise options.OptionError("No cql file name in command line options")
    if len(opts[-1].operands) == 0:
        raise options.OptionError("No cql file name given")
    if len(opts[-1].operands) > 1:
        raise options.OptionError("Extra options after cql file name")
    query = os.path.expanduser(opts[-1].operands[0])
    name, ext = os.path.splitext(query)
    if ext not in frozenset(("", ".cql", ".CQL")):
        raise options.OptionError("File name is not a '.cql' name")
    if not ext:
        query = name + ".cql"
    with open(query, mode="r", encoding="utf-8") as queryfile:
        populate_container(container, queryfile.read())
    return container


def parse_debug(string, tree_only=False, tokens_only=False):
    """Print debug trace and return QueryContainer instance for string.

    A basenode.NodeError is raised if the parse fails.

    """
    if tree_only:
        tokens_only = False
    container = querycontainer.QueryContainer()
    container.place_node_in_tree()
    for token in pattern.cql_re.finditer(_remove_comments(string, container)):
        classes = {
            key: tokenmap.class_from_token_name[key]
            for key, value in token.groupdict().items()
            if value is not None
        }
        container.raise_if_not_single_match_groupdict_entry(token, classes)
        for value in classes.values():
            if not tree_only:
                if not tokens_only:
                    print()
                print(token)
                if not tokens_only:
                    print("*cursor*", _parent_class_trace(container.cursor))
            cqlobj = value(match_=token, container=container)
            if not tree_only:
                if not tokens_only:
                    print("*init match*", _parent_match_trace(cqlobj))
                    print("*init class*", _parent_class_trace(cqlobj))
            cqlobj.place_node_in_tree()
            if not tree_only:
                if not tokens_only:
                    print("*place match*", _parent_match_trace(cqlobj))
                    print("*place class*", _parent_class_trace(cqlobj))
                    print(
                        "*cursor*",
                        _parent_class_trace(container.cursor),
                    )
    return container


def _remove_comments(string, container):
    """Return str replacing comments in string with spaces.

    The removed comments are added to container's whitespace property.

    The spaces ensure the location of the represented objects in the
    source is reported correctly in the regular expression match objects
    if these are examined.

    Filters with parenthesized arguments are represented in the pattern
    as '<filter><paramerters or whitespace>(' with separate entries for
    each argument and the final ')'.  The parameters are always a small
    set of values which can be handled easily in the pattern.

    However CQL allows comments to be placed between the filter and the
    "(", for example 'ray /* from Rook to king */ (R k)'.

    The simplest solution given the pattern is pre-process the query to
    remove the comments.

    """
    # It looks possible to have another class to represent the kind of
    # left parenthesis in 'ray(R k)', chosen in the parenthesis_left()
    # function when the filter pointed at by the cursor is a subclass of
    # ParenthesizedArguments.  However this loses the ability to verify
    # the syntax of the affected filters in the pattern.
    if not isinstance(container, querycontainer.QueryContainer):
        container.raise_nodeerror(
            "_remove_comments() function expects container to be a ",
            querycontainer.QueryContainer.__class__.__name__.join("''"),
            " but it is a ",
            container.__class__.__name__.join("''"),
        )
    block_comment = tokenmap.filters.BlockComment
    line_comment = tokenmap.filters.LineComment
    no_comments = []
    for token in _comment_re.finditer(string):
        group = token.group
        if group(1) is not None:
            no_comments.append(" " * len(group()))
            block_comment(
                match_=token, container=container
            ).place_node_in_tree()
        elif group(2) is not None:
            # Retain the assumed trailing '\n' because, for example,
            # 'path nestban quiet // comment\nwtm' is valid but
            # 'path nestban quiet // comment\n\nwtm' is not valid.
            no_comments.append(" " * (len(group()) - 1) + group()[-1])
            line_comment(
                match_=token, container=container
            ).place_node_in_tree()
        else:
            no_comments.append(group())
    return "".join(no_comments)


def _parent_match_trace(leaf):
    """Return match trace for node through parents to root node."""
    node = leaf
    stack = []
    while node:
        stack.append(node)
        node = node.parent
    stack = [s.match_[0] if s.parent else None for s in stack]
    return (leaf.__class__.__name__, len(stack), stack)


def _parent_class_trace(leaf):
    """Return class trace for node through parents to root node."""
    node = leaf
    stack = []
    while node:
        stack.append(node)
        node = node.parent
    stack = [s.__class__.__name__ if s.parent else None for s in stack]
    return (leaf.__class__.__name__, len(stack), stack)
