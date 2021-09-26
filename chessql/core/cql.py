# cql.py
# Copyright 2020 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) statement definitions.

The basic structure of a CQL statement at version 6.0 is:

'cql ( parameters ) list_of_filters'.

This module allows both parameters and list_of_filters to be empty.

The keyword definitions from http://gadycosteff.com/cql/ are provided in the
Token class.

The following precis is from the CQL version 6.0.4 documentation, and helps
describe the definition of the 'returntype' and 'arguments' items in the Token
namedtuple.

The keywords define operations on the four kinds of filter: numeric, set,
position, and logical.  Logical filters never have a value.  The other three
filters have a value when true (match the current position), the alternative
is false (not match the current position):

Set: a set of squares
Numeric: a number
Position: a position

Filters are also described as 'transform filters', 'direction filters',
'binary infix filters', 'infix filters', and 'relational filters'.  Some things
are called 'arithmetic operations' or, generally, 'symbols' but definitions of
the individual things call them filters.

Some filters have parameters: some parameters have an argument and others do
not.  All these parameters exist as TokenDefinition instances in the Token
class.  In many cases a parameter is consumed by the filter's TokenDefinition
regular expression in pattern, and the parameter is defined to prevent it being
used as a variable name.

The 'move' filter TokenDefinition, for example, lists the filter's parameters
in arguments, and a parameter TokenDefinition lists the filter arguments for
the parameter.  The 'move' filter can generate either a 'logical' filter or a
'set' filter and both are listed in Token.returntype.

Variable names with leading '__CQL' are reserved for CQL version 6.0.4 internal
variable names.

There are four types of variable: piece, square, numeric, and position.  These
correspond to the similar filter types, except for piece.  Piece variables are
set filters which represent the square of a particular piece where piece is one
of the pieces, 32 in the normal starting position of a game, present in the
initial position.  This piece identity does not change as the piece moves:
including when a pawn promotes.

Some filters have optional ranges which are expressed as a combination of
numbers and numeric variables.

"""
from collections import namedtuple
from enum import Enum

from . import constants

TokenDefinition = namedtuple(
    "TokenDefinition",
    [
        "name",
        "flags",
        "precedence",
        "pattern",
        "returntype",
        "arguments",
        "variant_name",
    ],
    defaults=(None,),
)


# The assumption a filter with arguments cannot be top of stack when all tokens
# have been processed is broken by the 'move' filter.  It has parameters which
# have arguments, but no arguments that are not labelled by a prefix parameter.
# The 'move' filter is top of stack when waiting for next parameter, and either
# a new filter or the end of the statement may be next.  ALLOW_TOP_STACK_AT_END
# flag replaces non-empty arguments as the indicator.
class Flags(Enum):
    """Flags defined to control parsing of CQL statements."""

    HALT_POP_CHAINED_FILTERS = "halt_pop_chained_filters"
    CLOSE_BRACE_OR_PARENTHESIS = "close_brace_or_parenthesis"
    NAMED_COMPOUND_FILTER = "named_compound_filter"
    INHIBIT_ENCLOSING_TRANSFORMS = "inhibit_enclosing_transforms"
    ASSIGN_TO_VARIABLE = "assign_to_variable"
    INCOMPLETE_IF_ON_STACK = "incomplete_if_on_stack"
    ALLOWED_TOP_STACK_AT_END = "allowed_top_stack_at_end"
    PARAMETER_TAKES_ARGUMENT = "parameter_takes_argument"
    PARENTHESIZED_ARGUMENTS = "parenthesized_arguments"
    HALT_POP_NO_BODY_FILTER = "halt_pop_no_body_filter"
    ACCEPT_RANGE = "accept_range"
    END_FILTER_NON_PARAMETER = "end_filter_non_parameter"
    ALLOWED_UNARY_MINUS = "allowed_unary_minus"
    NO_ARITHMETIC_FILTERS = "no_arithmetic_filters"
    STATEMENT_FRAME = "statement_frame"
    LINE_FRAME = "line_frame"
    IF_FRAME = "if_frame"
    # FUNCTION_FRAME for function calls may not work because function names are
    # not keywords, but a subset of variable names.


_no_flags = frozenset()
_halt_pop_chained_filters = frozenset({Flags.HALT_POP_CHAINED_FILTERS})
_close_brace_or_parenthesis = frozenset({Flags.CLOSE_BRACE_OR_PARENTHESIS})
_named_compound_filter = frozenset({Flags.NAMED_COMPOUND_FILTER})
_assign_to_variable = frozenset({Flags.ASSIGN_TO_VARIABLE})
_incomplete_if_on_stack = frozenset({Flags.INCOMPLETE_IF_ON_STACK})
_allowed_top_stack_at_end = frozenset({Flags.ALLOWED_TOP_STACK_AT_END})
_parameter_takes_argument = frozenset({Flags.PARAMETER_TAKES_ARGUMENT})
_parenthesized_arguments = frozenset({Flags.PARENTHESIZED_ARGUMENTS})
_halt_pop_no_body_filter = frozenset({Flags.HALT_POP_NO_BODY_FILTER})
_accept_range = frozenset({Flags.ACCEPT_RANGE})
_end_filter_non_parameter = frozenset({Flags.END_FILTER_NON_PARAMETER})
_allowed_unary_minus = frozenset({Flags.ALLOWED_UNARY_MINUS})
_no_arithmetic_filters = frozenset({Flags.NO_ARITHMETIC_FILTERS})
_statement_frame = frozenset({Flags.STATEMENT_FRAME})
_line_frame = frozenset({Flags.LINE_FRAME})
_if_frame = frozenset({Flags.IF_FRAME})


class TokenTypes(Enum):
    """The token types defined in the CQL documentation."""

    NUMERAL = "numeral"
    UNSET_VARIABLE = "unset variable"
    NUMERIC_FILTER = "numeric"
    POSITION_FILTER = "position"
    LOGICAL_FILTER = "logical"
    SET_FILTER = "set"

    # CQL documentation for variables says there are four types: numeric, set,
    # piece, and position.  Function names occupy the same name space.  The
    # 'square' filter refers to square variables, which seem to behave as set
    # variables.
    NUMERIC_VARIABLE = "numeric variable"
    POSITION_VARIABLE = "position variable"
    PIECE_VARIABLE = "piece variable"
    SET_VARIABLE = "set variable"

    FUNCTION_CALL = "function call"
    FUNCTION_NAME = "function name"
    PERSISTENT_NUMERIC_VARIABLE = "persistent numeric variable"

    LINE_RE_SYMBOLS = "line re symbols"

    CONSECUTIVEMOVES_PARAMETER = "consecutivemoves parameter"
    MOVE_PARAMETER = "move parameter"
    PIN_PARAMETER = "pin parameter"
    FIND_PARAMETER = "find parameter"
    LINE_PARAMETER = "line parameter"
    LINE_LEFTARROW_PARAMETER = "line leftarrow parameter"
    LINE_RIGHTARROW_PARAMETER = "line rightarrow parameter"

    THEN_PARAMETER = "then parameter"
    ELSE_PARAMETER = "else parameter"


_empty_set = frozenset()
_numeric = frozenset(
    (
        TokenTypes.NUMERAL,
        TokenTypes.NUMERIC_FILTER,
    )
)
_numeric_filter = frozenset((TokenTypes.NUMERIC_FILTER,))
_set_filter = frozenset((TokenTypes.SET_FILTER,))
_logical_filter = frozenset((TokenTypes.LOGICAL_FILTER,))
_position_filter = frozenset((TokenTypes.POSITION_FILTER,))
_any_filter = frozenset(
    (
        TokenTypes.NUMERIC_FILTER,
        TokenTypes.SET_FILTER,
        TokenTypes.LOGICAL_FILTER,
        TokenTypes.POSITION_FILTER,
    )
)
_line_re_symbols = frozenset((TokenTypes.LINE_RE_SYMBOLS,))
_line_constituents = frozenset(
    (
        TokenTypes.NUMERIC_FILTER,
        TokenTypes.SET_FILTER,
        TokenTypes.LOGICAL_FILTER,
        TokenTypes.POSITION_FILTER,
        TokenTypes.LINE_RE_SYMBOLS,
    )
)
_consecutivemoves_parameter = frozenset(
    (TokenTypes.CONSECUTIVEMOVES_PARAMETER,)
)
_move_parameter = frozenset((TokenTypes.MOVE_PARAMETER,))
_pin_parameter = frozenset((TokenTypes.PIN_PARAMETER,))
_find_parameter = frozenset((TokenTypes.FIND_PARAMETER,))
_line_parameter = frozenset((TokenTypes.LINE_PARAMETER,))
_line_leftarrow_parameter = frozenset((TokenTypes.LINE_LEFTARROW_PARAMETER,))
_line_rightarrow_parameter = frozenset((TokenTypes.LINE_RIGHTARROW_PARAMETER,))
_move_or_pin_parameter = frozenset(
    (
        TokenTypes.MOVE_PARAMETER,
        TokenTypes.PIN_PARAMETER,
    )
)
_assign_filters = frozenset(
    (
        TokenTypes.NUMERIC_FILTER,
        TokenTypes.SET_FILTER,
        TokenTypes.POSITION_FILTER,
    )
)
_relation_filters = frozenset(
    (
        TokenTypes.NUMERIC_FILTER,
        TokenTypes.SET_FILTER,
        TokenTypes.POSITION_FILTER,
    )
)
_position_variable = frozenset((TokenTypes.POSITION_VARIABLE,))
_if_constituents = frozenset(
    (
        TokenTypes.NUMERIC_FILTER,
        TokenTypes.SET_FILTER,
        TokenTypes.LOGICAL_FILTER,
        TokenTypes.POSITION_FILTER,
        TokenTypes.THEN_PARAMETER,
        TokenTypes.ELSE_PARAMETER,
    )
)
_then_parameter = frozenset((TokenTypes.THEN_PARAMETER,))
_else_parameter = frozenset((TokenTypes.ELSE_PARAMETER,))
_unset_variable = frozenset((TokenTypes.UNSET_VARIABLE,))


class Token:
    """The attributes defined for Token are the keywords of CQL version 6.0.4.

    A method with the name from each '?P<name>' construct must exist in class
    .statement.Statement taking a match against CQL_PATTERN and the expected
    token's TokenDefinition instance as it's arguments.

    """

    # Four kinds of filter are defined in the filters documentation for CQL
    # version 6.0.4: numeric, set, position, and logical.

    # Some filters are described as transform filters.  These define operations
    # on numeric, set, position, and logical, filters to do things like change
    # the side to move or shift all the pieces one square up the board.  Most
    # transform filters have a count parameter.  Without the count parameter
    # the tranformation does not change the kind of filter.  With the count
    # parameter the transformation changes the kind of filter to numeric since
    # the associated value is a number (something will be counted).  The tokens
    # defined inside class Token for transform filters define filters without
    # the count keyword.  The statement parser instead will use a token defined
    # outside the Token class when the count keyword is present, which defines
    # the transformed filter as numeric.

    # Some filters are described as direction filters.  These translate a set
    # of squares along certain directions by a certain length.  There are eight
    # basic directions and five pre-defined compound directions.  An optional
    # range parameter can be quoted: if absent it is assumed to be '1 7'.  The
    # compound filters define the union of the constituent basic filters: thus
    # 'vertical 3 d4' is '{up 3 d4} or {down 3 d4}' is '[d7,d1]' (copied from
    # directions documentation for CQL version 6.0.1).  A direction filter
    # generates a set from a set.
    # The names of the direction filters are also used as parameters to the ray
    # filter.

    # Some filters are described as binary infix filters.
    # The 'or' filter is not so described, but if the 'and' filter is binary
    # infix surely 'or' is too.  The binary infix filters generate logical
    # filters, unlike the infix filters.

    # Some filters are described as infix filters.
    # The infix filters generate set filters.

    # Some filters are described as relational filters or comparison filters.

    # Some filters are described as allowing arithmetic operations on numeric
    # filters.  (Quoting from the Arithmetic operators documentation:
    # 'each such comparison or arithmetic operator is its own filter')

    # Operator assignments combine the '=' filter with arithmetic operations.
    # These are treated like the '=' filter, which is included here.

    # The '|', '&', '~', and '#' filters.

    # The '(', ')', '{', and '}' filters.
    # These filters can be used to adjust the meaning of a statement compared
    # with their absence. '(' pairs with ')', and '{' with '}'.  Singletons are
    # a syntax error. The parentheses are used in regular expressions and to
    # indicate arguments to the preceding filter.  The braces are used to make
    # a list of filters implicitly linked by 'and' filters.  The parentheses
    # can be used to adjust the precedence of arithmetic operations.

    # Some filters have their arguments wrapped by parentheses.  The child
    # filter is included in this list: the argument is optional and the forms
    # accepted are 'child' and 'child(<numeric filter>)'.

    # Some filters take a single filter as their argument, which may be a
    # compound filter: a list of filters surrounded by a '{ }' pair.

    # Some filters take no arguments.  These filters are allowed to be the last
    # token in a statement.

    # Two tokens describe comments which can be placed in CQL statements.

    # The transform filters: flip through shiftvertical.
    FLIP = TokenDefinition(
        "flip", _no_flags, 40, r"flip(?:\s+count)?\b", _any_filter, _any_filter
    )
    FLIPCOLOR = TokenDefinition(
        "flipcolor",
        _no_flags,
        40,
        r"flipcolor(?:\s+count)?\b",
        _any_filter,
        _any_filter,
    )
    FLIPHORIZONTAL = TokenDefinition(
        "fliphorizontal",
        _no_flags,
        40,
        r"fliphorizontal(?:\s+count)?\b",
        _any_filter,
        _any_filter,
    )
    FLIPVERTICAL = TokenDefinition(
        "flipvertical",
        _no_flags,
        40,
        r"flipvertical(?:\s+count)?\b",
        _any_filter,
        _any_filter,
    )

    # Table of filters gives a count parameter but reversecolor documentation
    # does not.  Syntax error if count included in cql6.exe call.
    REVERSECOLOR = TokenDefinition(
        "reversecolor",
        _no_flags,
        40,
        r"reversecolor\b",
        _any_filter,
        _any_filter,
    )

    ROTATE45 = TokenDefinition(
        "rotate45",
        _no_flags,
        40,
        r"rotate45(?:\s+count)?\b",
        _any_filter,
        _any_filter,
    )
    ROTATE90 = TokenDefinition(
        "rotate90",
        _no_flags,
        40,
        r"rotate90(?:\s+count)?\b",
        _any_filter,
        _any_filter,
    )
    SHIFT = TokenDefinition(
        "shift",
        _no_flags,
        40,
        r"shift(?:\s+count)?\b",
        _any_filter,
        _any_filter,
    )
    SHIFTHORIZONTAL = TokenDefinition(
        "shifthorizontal",
        _no_flags,
        40,
        r"shifthorizontal(?:\s+count)?\b",
        _any_filter,
        _any_filter,
    )
    SHIFTVERTICAL = TokenDefinition(
        "shiftvertical",
        _no_flags,
        40,
        r"shiftvertical(?:\s+count)?\b",
        _any_filter,
        _any_filter,
    )

    # The direction filters: anydirection through vertical.
    # Ranges must be given as numeric literals or numeric variables, examples:
    # up 2 k
    # z=2 up z k
    # z=max(2, #n) up z k
    # function y(){#Q} x=y() up x k
    # Note a clause like '([1-9][0-9]*|[$A-Z_a-z][$0-9A-Z_a-z]*)' will not work
    # because it consumes all the keywords as well as the numeric literals and
    # numeric variables.  An exhaustive list of keywords to reject is possible
    # but, on current thinking, clumsy compared with deciding what to do when a
    # numeric literal or numeric variable token is found.
    ANYDIRECTION = TokenDefinition(
        "anydirection",
        _accept_range,
        200,
        r"anydirection\b",
        _set_filter,
        _set_filter,
    )
    DIAGONAL = TokenDefinition(
        "diagonal", _accept_range, 200, r"diagonal\b", _set_filter, _set_filter
    )
    DOWN = TokenDefinition(
        "down", _accept_range, 200, r"down\b", _set_filter, _set_filter
    )
    HORIZONTAL = TokenDefinition(
        "horizontal",
        _accept_range,
        200,
        r"horizontal\b",
        _set_filter,
        _set_filter,
    )
    LEFT = TokenDefinition(
        "left", _accept_range, 200, r"left\b", _set_filter, _set_filter
    )
    NORTHEAST = TokenDefinition(
        "northeast",
        _accept_range,
        200,
        r"northeast\b",
        _set_filter,
        _set_filter,
    )
    NORTHWEST = TokenDefinition(
        "northwest",
        _accept_range,
        200,
        r"northwest\b",
        _set_filter,
        _set_filter,
    )
    ORTHOGONAL = TokenDefinition(
        "orthogonal",
        _accept_range,
        200,
        r"orthogonal\b",
        _set_filter,
        _set_filter,
    )
    RIGHT = TokenDefinition(
        "right", _accept_range, 200, r"right\b", _set_filter, _set_filter
    )
    SOUTHEAST = TokenDefinition(
        "southeast",
        _accept_range,
        200,
        r"southeast\b",
        _set_filter,
        _set_filter,
    )
    SOUTHWEST = TokenDefinition(
        "southwest",
        _accept_range,
        200,
        r"southwest\b",
        _set_filter,
        _set_filter,
    )
    UP = TokenDefinition(
        "up", _accept_range, 200, r"up\b", _set_filter, _set_filter
    )
    VERTICAL = TokenDefinition(
        "vertical", _accept_range, 200, r"vertical\b", _set_filter, _set_filter
    )

    # The binary infix filters.

    # Almost always 'and' and '{ ... }' are equivalent.  Documentation mentions
    # '{ ... }' sometimes returns a value but 'and' never does.
    AND = TokenDefinition(
        "and_",
        _named_compound_filter,
        60,
        r"and\b",
        _logical_filter,
        _any_filter,
    )
    OR = TokenDefinition(
        "or_",
        _named_compound_filter,
        50,
        r"or\b",
        _logical_filter,
        _any_filter,
    )

    # The infix filters.
    # The ':' operator is included because it has same shape as the explicit
    # infix operators.  ':' is not called an infix operator, and it is stated
    # ':' can appear in the rhs of a ':' operator:
    # 'position 0 : child : comment ("first position")' is the example.
    # But 'Q attacks r attacks K' is a legal statement too.
    ATTACKEDBY = TokenDefinition(
        "attackedby",
        _named_compound_filter,
        180,
        r"attackedby\b",
        _set_filter,
        _set_filter,
    )
    ATTACKS = TokenDefinition(
        "attacks",
        _named_compound_filter,
        180,
        r"attacks\b",
        _set_filter,
        _set_filter,
    )
    COLON = TokenDefinition(
        "colon",
        _named_compound_filter,
        210,
        r":",
        _logical_filter,
        _any_filter,
    )
    IN = TokenDefinition(
        "in_",
        _named_compound_filter,
        80,
        r"in\b",
        _logical_filter,
        _set_filter,
    )

    # The relational filters or comparison filters.
    # '<', '<=', '>', '>=', '==', and '!='.
    # '==' and '!=' behave differently to the others when both operands are
    # set filters.

    # Comparisions are numeric, so '1>2' is accepted.  Exactly one of lhs and
    # rhs can be given as a set filter, so k>1 and 1>k are accepted and are
    # equivalent to '#k>1' and '1>#k'.  '#q<#r' and 'q<#r'are accepted.
    # Exactly both lhs and rhs can be given as position filters, so
    # 'parent>child' is accepted but '3>child' is not accepted.
    # Variants imply the lhs operand found is a set filter or position filter,
    # restricting the rhs operand to be a numeric filter or position filter to
    # fit.  Otherwise the lhs operand found is a numeric filter, and the rhs
    # operand can be a set, position, or numeric, filter.
    LT = TokenDefinition(
        "lt",
        _named_compound_filter,
        90,
        r"<",
        _numeric_filter,
        _relation_filters,
    )
    LE = TokenDefinition(
        "le",
        _named_compound_filter,
        90,
        r"<=",
        _numeric_filter,
        _relation_filters,
    )
    GT = TokenDefinition(
        "gt",
        _named_compound_filter,
        90,
        r">",
        _numeric_filter,
        _relation_filters,
    )
    GE = TokenDefinition(
        "ge",
        _named_compound_filter,
        90,
        r">=",
        _numeric_filter,
        _relation_filters,
    )

    # 'k==q' and 'k!=q' are accepted in addition to the other combinations,
    # implying a set comparison rather than a numeric comparison.
    EQ = TokenDefinition(
        "eq",
        _named_compound_filter,
        90,
        r"==",
        _numeric_filter,
        _relation_filters,
    )
    NE = TokenDefinition(
        "ne",
        _named_compound_filter,
        90,
        r"!=",
        _logical_filter,
        _relation_filters,
    )

    # The arithmetic operations on numeric filters.
    # The arithmetic operator is seen as its own filter.
    # '*', '+', '-', '%', and '/'.

    # These two can be regular expression operators in the 'line' filter too.
    # The arithmetic interpretation takes precedence and the regular expression
    # interpretation is allowed only after a constituent of a 'line' filter.
    # The regular expression interpretation can be forced by '{*}' and '{+}'.
    STAR = TokenDefinition(
        "star", _named_compound_filter, 130, r"\*", _numeric_filter, _numeric
    )
    PLUS = TokenDefinition(
        "plus", _named_compound_filter, 110, r"\+", _numeric_filter, _numeric
    )

    # Currently this is treated as the '2 - 1' minus, not unary minus.
    # If token to left is not a numeric filter or is minus: its unary minus!
    MINUS = TokenDefinition(
        "minus", _named_compound_filter, 110, r"-", _numeric_filter, _numeric
    )

    MODULUS = TokenDefinition(
        "modulus", _named_compound_filter, 130, r"%", _numeric_filter, _numeric
    )
    DIVIDE = TokenDefinition(
        "divide", _named_compound_filter, 130, r"/", _numeric_filter, _numeric
    )

    # The '=' filter and its combinations with arithmetic operations.

    # Precedence not given in precedence table for CQL version 6.0.4: on trying
    # 'x = K or Q' hit a syntax error <RHS is not a set filter ...>, while
    # 'x = K' is fine.  'cql -parse ...' suggests 'or' has higher precedence
    # than '='.  However 'x = K | Q' is a set filter (well, it does not get
    # syntax error response).  Same with 'and' and '&'.
    # RHS must be set filter, countable filter, or a position filter.
    ASSIGN = TokenDefinition(
        "assign",
        _named_compound_filter,
        40,
        r"=\??",
        _assign_filters,
        _assign_filters,
    )

    IPPLUS = TokenDefinition(
        "ipplus",
        _named_compound_filter,
        100,
        r"\+=",
        _numeric_filter,
        _numeric,
    )
    IPMINUS = TokenDefinition(
        "ipminus",
        _named_compound_filter,
        100,
        r"-=",
        _numeric_filter,
        _numeric,
    )
    IPMULTIPLY = TokenDefinition(
        "ipmultiply",
        _named_compound_filter,
        100,
        r"\*=",
        _numeric_filter,
        _numeric,
    )
    IPDIVIDE = TokenDefinition(
        "ipdivide",
        _named_compound_filter,
        100,
        r"/=",
        _numeric_filter,
        _numeric,
    )
    IPMODULUS = TokenDefinition(
        "ipmodulus",
        _named_compound_filter,
        100,
        r"%=",
        _numeric_filter,
        _numeric,
    )

    # The '|', '&', '~', and '#' filters.

    # The lhs and rhs of | must both be set filters.
    UNION = TokenDefinition(
        "union", _named_compound_filter, 150, r"\|", _set_filter, _set_filter
    )

    # The lhs and rhs of & must both be either set filters or position filters.
    # In both cases the result is a set filter.
    # Replaced by position or set filter version before looking for rhs.
    INTERSECTION = TokenDefinition(
        "intersection",
        _named_compound_filter,
        160,
        r"&",
        _set_filter,
        _position_filter.union(_set_filter),
    )

    TILDE = TokenDefinition(
        "tilde", _no_flags, 170, r"~", _set_filter, _set_filter
    )
    HASH = TokenDefinition(
        "hash", _allowed_unary_minus, 140, r"#", _numeric_filter, _set_filter
    )

    # The '(', ')', '{', and '}' filters.
    LEFTBRACE = TokenDefinition(
        "leftbrace",
        _halt_pop_chained_filters.union(_parenthesized_arguments)
        .union(_incomplete_if_on_stack)
        .union(_allowed_unary_minus),
        0,
        r"{",
        _any_filter,
        _any_filter,
    )
    RIGHTBRACE = TokenDefinition(
        "rightbrace",
        _close_brace_or_parenthesis,
        0,
        r"}",
        _empty_set,
        _empty_set,
    )

    # Both returntype and arguments are set to _any_filter because '(' can be
    # used anywhere, although the restrictions on the filters within '()' vary
    # across the cases where parentheses are allowed.
    LEFTPARENTHESIS = TokenDefinition(
        "leftparenthesis",
        _halt_pop_chained_filters.union(_parenthesized_arguments).union(
            _allowed_unary_minus
        ),
        0,
        r"\(",
        _any_filter,
        _any_filter,
    )
    RIGHTPARENTHESIS = TokenDefinition(
        "rightparenthesis",
        _close_brace_or_parenthesis,
        0,
        r"\)",
        _empty_set,
        _empty_set,
    )

    # The filters whose arguments are wrapped by parentheses.  The keyword cql
    # is included in this section.
    # ancestor through xray.
    ANCESTOR = TokenDefinition(
        "ancestor",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        40,
        r"ancestor\s*\(",
        _numeric_filter,
        _position_filter,
    )
    BETWEEN = TokenDefinition(
        "between",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        140,
        r"between\s*\(",
        _set_filter,
        _set_filter,
    )

    # The argument is optional: 'child' and 'child(3)' are acceptable forms.
    CHILD = TokenDefinition(
        "child",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        0,
        r"child(?:\s*\()?",
        _position_filter,
        _numeric,
    )

    # If there is only one argument, the enclosing parentheses can be omitted.
    # Comment is listed as a parameter of move too, but the description of move
    # refers to a 'comment filter immediately follow(ing) a move filter', so
    # comment is not treated as a parameter of move in the sense of the others.
    # Consistent with 'move from k comment "a" to Q' giving a syntax error but
    # 'move from k to Q comment "a"' being accepted by CQL version 6.0.4.
    # Not sure if this needs _allowed_top_stack_at_end flag?
    COMMENT = TokenDefinition(
        "comment",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        0,
        r"comment(?:\s*\()?",
        _logical_filter,
        _any_filter,
    )

    # _halt_pop_chained_filters is not correct any more, '(' is not consumed
    # by this token, but _parameter_takes_argument is not correct either as
    # multiple keywords ending with '(' are taken.
    CONSECUTIVEMOVES = TokenDefinition(
        "consecutivemoves",
        _incomplete_if_on_stack.union(_accept_range),
        0,
        r"consecutivemoves\b",
        _numeric_filter,
        _consecutivemoves_parameter,
    )

    # Always the first token, always 'cql ( ... )' then arbitrary filters.
    # CQL.type is the query's answer.  (Meant something once: nonsense now.)
    # Perhaps {TokenTypes.CQL_PARAMETER} used in other Tokens, such as
    # Token.OUTPUT, should replace
    # {TokenTypes.OUTPUT, ..., TokenTypes.MATCHSTRING}.
    # Characters '(' and ')' are allowed in filenames and quoted strings so
    # r'cql\([^)]+\)' is not good enough to pick up the CQL token.  Check all
    # elements are valid, but perhaps not in the right order.
    # Problem with this definition is any error in 'cql ( ... )' is reported
    # as "cql token not recognized" rather than, for example, "quit ..." if
    # "quiet" were mis-typed.
    # The table of precedence, at CQL version 6.0.4, includes a statement
    # 'constituents of a compound filter', in a cell where all filters named in
    # a cell have the same precedence.  This contradicts all statements of
    # precedence for particular filters in different cells because the top
    # level of a statement is an implicit compound statement. The contradiction
    # can be resolved by restricting 'constituents of a compound filter' to
    # mean filters not named elsewhere in the table.  For example, it seems
    # reasonable piece designators have that precedence.
    # But the same can be said of 'in parameter to piece', 'in parameter to
    # square', and 'right hand side of piece assignment', so maybe a filter's
    # precedence depends on where it is used.
    # Not sure how appropriate any returntype or arguments value is, but say
    # 'logical' and any filter type respectively.
    # The parenthesized parameters are declared optional to avoid a bare 'cql'
    # being taken as a variable name.  Processing for the 'cql' token insists
    # on '( ... )' being present.
    CQL = TokenDefinition(
        "cql",
        _halt_pop_chained_filters.union(_statement_frame),
        0,
        r"|".join(
            (
                r"(?:output|input)\s+\S+\.pgn",
                r"(?:sort\s+)?matchcount(?:\s+[0-9]+){,2}",
                r"gamenumber(?:\s+[0-9]+){,2}",
                r"result\s+(?:1-0|1/2-1/2|0-1)",
                r"silent",
                r"quiet",
                r"variations",
                r'matchstring\s+"(?:[^\\"]|\\.)*"',
            )
        )
        .join((r"(?:(?:", r")\s+)*"))
        .join((r"cql(?:\s*\(\s*", r"\)\s*)?")),
        _logical_filter,
        _any_filter,
    )

    DESCENDANT = TokenDefinition(
        "descendant",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        40,
        r"descendant\s*\(",
        _numeric_filter,
        _position_filter,
    )
    DISTANCE = TokenDefinition(
        "distance",
        _halt_pop_chained_filters.union(_parenthesized_arguments).union(
            _allowed_unary_minus
        ),
        40,
        r"distance\s*\(",
        _numeric_filter,
        _position_filter,
    )

    # 'in all' is described as a parameter to echo but unlike consecutivemoves
    # and ray, the other filters with parameters and parenthesised arguments,
    # the parameter is after the arguments.
    # Since the arguments are variables used in the body filter, not arguments
    # to the filter in the sense used elsewhere, it might work to pretend there
    # are no parameters ('in all') and the parameter is a compound filter, not
    # (variable, variable), and pick up the variables in pattern.
    ECHO = TokenDefinition(
        "echo",
        _incomplete_if_on_stack.union(_halt_pop_no_body_filter),
        0,
        r"".join(
            (
                r"echo\s+\(\s*[$A-Z_a-z][$0-9A-Z_a-z]*",
                r"\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s*\)\s*(?:in\s+all\b)?",
            )
        ),
        _logical_filter,
        _any_filter,
    )

    LCA = TokenDefinition(
        "lca",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        40,
        r"lca\s*\(",
        _position_filter,
        _position_filter,
    )
    MAKESQUARE = TokenDefinition(
        "makesquare",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        100,
        r"makesquare\s*\(",
        _set_filter,
        _numeric,
    )
    MAX = TokenDefinition(
        "max",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        0,
        r"max\s*\(",
        _numeric_filter,
        _numeric,
    )

    # If there is only one argument, the enclosing parentheses can be omitted.
    MESSAGE = TokenDefinition(
        "message",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        0,
        r"message(?:\s*\()?",
        _logical_filter,
        _any_filter,
    )

    MIN = TokenDefinition(
        "min",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        0,
        r"min\s*\(",
        _numeric_filter,
        _numeric,
    )

    # Ray clauses like 'ray up left ( A a )' are allowed: 'anydirection' is a
    # shorthand for listing all of them, for example.
    RAY = TokenDefinition(
        "ray",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        0,
        r"|".join(
            (
                r"up",
                r"down",
                r"right",
                r"left",
                r"northeast",
                r"northwest",
                r"southeast",
                r"southwest",
                r"diagonal",
                r"orthogonal",
                r"vertical",
                r"horizontal",
                r"anydirection",
            )
        ).join((r"ray(?:\s+(?:", r"))*\s*\(")),
        _set_filter,
        _set_filter,
    )

    XRAY = TokenDefinition(
        "xray",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        140,
        r"xray\s*\(",
        _set_filter,
        _set_filter,
    )

    # The filters which take a single filter as their argument.
    ABS = TokenDefinition(
        "abs", _allowed_unary_minus, 100, r"abs\b", _numeric_filter, _numeric
    )
    COLORTYPE = TokenDefinition(
        "colortype",
        _no_flags,
        140,
        r"colortype\b",
        _numeric_filter,
        _set_filter,
    )
    DARK = TokenDefinition(
        "dark", _no_flags, 200, r"dark\b", _set_filter, _set_filter
    )
    FILE = TokenDefinition(
        "file",
        frozenset({Flags.INHIBIT_ENCLOSING_TRANSFORMS}),
        140,
        r"file\b",
        _numeric_filter,
        _set_filter,
    )

    # position filters: x = find check y = find <-- check
    # numeric filters: x = find all check y = find 1 check z = find <-- 2 check
    #                  w = find <-- all check
    # Replace FIND with FIND_NUMERIC if 'all' parameter is present.
    FIND = TokenDefinition(
        "find", _no_flags, 40, r"find\b", _position_filter, _any_filter
    )

    LIGHT = TokenDefinition(
        "light", _no_flags, 200, r"light\b", _set_filter, _set_filter
    )

    # The first '-->' or '<--' converts LINE entry at top of stack to
    # LINE_RIGHTARROW or LINE_LEFTARROW, after which the 'line' filter
    # continues with any filter followed by zero or more [<arrow> <non arrow>]
    # pairs until consecutive <non arrow> filters appear in the token stream,
    # or the stream ends.  Later arrows for a 'line' filter must be same as the
    # first arrow.
    # The flags and arguments items between them accept all parameters of the
    # 'line' filter (probably arguments like the 'move' filter so the arguments
    # entry is wrong).
    # 'cql.exe -parse *.cql' suggests returntype is _numeric_filter.  This is
    # consistent with CQL version 6 documentation on the default value of the
    # 'line' filter; but no description of non-default values is given.
    LINE = TokenDefinition(
        "line",
        _accept_range.union(_halt_pop_chained_filters).union(_line_frame),
        0,
        r"line\b",
        _numeric_filter,
        _line_parameter,
    )

    LOOP = TokenDefinition(
        "loop", _no_flags, 40, r"loop\b", _logical_filter, _any_filter
    )

    # If 'capture', 'from', or 'to', is first parameter of 'move' filter then
    # the node's TokenDefinition must be change to a MOVE_SET.
    MOVE = TokenDefinition(
        "move",
        _end_filter_non_parameter.union(_allowed_top_stack_at_end),
        0,
        r"move\b",
        _logical_filter,
        _move_parameter,
    )

    NOTRANSFORM = TokenDefinition(
        "notransform",
        frozenset({Flags.INHIBIT_ENCLOSING_TRANSFORMS}),
        200,
        r"notransform\b",
        _any_filter,
        _any_filter,
    )
    NOT = TokenDefinition(
        "not_", _no_flags, 70, r"not\b", _logical_filter, _any_filter
    )

    # Two distinct filters with the same keyword, guaranteed different in their
    # last element, 'in' or '='.  Treated as three distinct filters because the
    # outputs are set filters or filters.
    # The second filter after 'in' is the body of the piece filter and can be
    # any filter type: not noted as part of the definition of PIECE_IN or
    # PIECE_ALL_IN.
    PIECE_IN = TokenDefinition(
        "piecein",
        _incomplete_if_on_stack.union(_halt_pop_no_body_filter),
        0,
        r"piece\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b",
        _set_filter,
        _set_filter,
    )
    PIECE_ALL_IN = TokenDefinition(
        "pieceallin",
        _incomplete_if_on_stack.union(_halt_pop_no_body_filter),
        0,
        r"piece\s+all\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b",
        _logical_filter,
        _set_filter,
    )
    PIECE_ASSIGNMENT = TokenDefinition(
        "pieceassignment",
        _no_flags,
        0,
        r"piece\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+=",
        _logical_filter,
        _set_filter,
    )
    PIECEID = TokenDefinition(
        "pieceid", _no_flags, 140, r"pieceid\b", _numeric_filter, _set_filter
    )
    PIN = TokenDefinition(
        "pin",
        _end_filter_non_parameter.union(_allowed_top_stack_at_end),
        0,
        r"pin\b",
        _set_filter,
        _pin_parameter,
    )
    POSITION = TokenDefinition(
        "position", _no_flags, 100, r"position\b", _position_filter, _numeric
    )
    POWER = TokenDefinition(
        "power",
        _allowed_unary_minus,
        140,
        r"power\b",
        _numeric_filter,
        _set_filter,
    )
    RANK = TokenDefinition(
        "rank",
        frozenset({Flags.INHIBIT_ENCLOSING_TRANSFORMS}),
        140,
        r"rank\b",
        _numeric_filter,
        _set_filter,
    )
    SORT = TokenDefinition(
        "sort",
        _no_flags,
        0,
        r'sort(?:\s+min)?(?:\s+"((?:[^\\"]|\\.)*)")?',
        _numeric_filter,
        _numeric_filter,
    )
    SQRT = TokenDefinition(
        "sqrt", _no_flags, 100, r"sqrt\b", _numeric_filter, _numeric
    )
    SQUARE_IN = TokenDefinition(
        "squarein",
        _incomplete_if_on_stack.union(_halt_pop_no_body_filter),
        0,
        r"square\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b",
        _set_filter,
        _set_filter,
    )
    SQUARE_ALL_IN = TokenDefinition(
        "squareallin",
        _incomplete_if_on_stack.union(_halt_pop_no_body_filter),
        0,
        r"square\s+all\s+[$A-Z_a-z][$0-9A-Z_a-z]*\s+in\b",
        _logical_filter,
        _set_filter,
    )
    TYPE = TokenDefinition(
        "type", _no_flags, 140, r"type\b", _numeric_filter, _set_filter
    )

    # The filters which take no arguments.
    BLACK = TokenDefinition(
        "black",
        _allowed_top_stack_at_end,
        0,
        r"black\b",
        _numeric_filter,
        _empty_set,
    )
    BTM = TokenDefinition(
        "btm",
        _allowed_top_stack_at_end,
        0,
        r"btm\b",
        _logical_filter,
        _empty_set,
    )
    CHECK = TokenDefinition(
        "check",
        _allowed_top_stack_at_end,
        0,
        r"check\b",
        _logical_filter,
        _empty_set,
    )
    CONNECTEDPAWNS = TokenDefinition(
        "connectedpawns",
        _allowed_top_stack_at_end,
        0,
        r"connectedpawns\b",
        _set_filter,
        _empty_set,
    )
    CURRENTPOSITION = TokenDefinition(
        "currentposition",
        _allowed_top_stack_at_end,
        0,
        r"currentposition\b",
        _position_filter,
        _empty_set,
    )
    DEPTH = TokenDefinition(
        "depth",
        _allowed_top_stack_at_end,
        0,
        r"depth\b",
        _numeric_filter,
        _empty_set,
    )

    # I have taken the statement 'Directions are also used as a parameter to
    # the ray filter' to imply all direction filters are set filters, but I
    # vaguely recall CQL version 5.1 documentation saying supplying a range to
    # a direction filter stops it being a set filter.

    DOUBLEDPAWNS = TokenDefinition(
        "doubledpawns",
        _allowed_top_stack_at_end,
        0,
        r"doubledpawns\b",
        _set_filter,
        _empty_set,
    )

    # The optional parameters of elo, black and white, are also the names of
    # filters.  It might work to pretend there are no parameters ('black'  or
    # 'white') and pick up the parameters in pattern.  If it is legal to say
    # 'elo black', meaning the filter 'black', say 'elo {black}' instead.
    # In CQL version 6.0.4 the following is seen with -parse option:
    # 'black': ColorValueNode
    # 'elo': EloNode
    # 'elo black': EloNode Black
    # 'elo { black }': EloNode ColorValueNode
    # so picking up white and black in the 'elo' pattern is correct, giving
    # priority to the parameter interpretation.
    # The elo_white and elo_black TokenTypes are defined, consistent with
    # treatment of other filters which have parameters, but could be done
    # without because elo is a leaf node.
    ELO = TokenDefinition(
        "elo",
        _allowed_top_stack_at_end,
        0,
        r"elo(?:\s+(?:black|white))?\b",
        _numeric_filter,
        _empty_set,
    )

    EVENT = TokenDefinition(
        "event",
        _allowed_top_stack_at_end,
        0,
        r'event\s+(?:"((?:[^\\"]|\\.)*)")',
        _logical_filter,
        _empty_set,
    )
    FALSE = TokenDefinition(
        "false",
        _allowed_top_stack_at_end,
        0,
        r"false\b",
        _logical_filter,
        _empty_set,
    )

    # Fen seems to be a set filter because in CQL version 6.0.4 the following
    # is accepted with -parse option:
    # 'up fen "k7/8/8/8/8/8/8/7K"'
    # 'x = fen "..." supports this assumption.
    FEN = TokenDefinition(
        "fen",
        _allowed_top_stack_at_end,
        0,
        r'fen\s+"[^"]*"',
        _set_filter,
        _empty_set,
    )

    # TokenTypes and arguments set to _any_filter because not sure what to do.
    # Function name must not be already defined 'x=1 function x(){}'.
    # Formal arguments must not be duplicated 'function x(y y){}'.
    # Formal arguments can duplicate defined variables 'y=1 function x(y){}' or
    # 'function x(x){}'. 'function x(x){up x} x(g6)' runs successfully at CQL
    # version 6.0.4, and so does 'function x(x){up x} x(x(g6))'.
    FUNCTION = TokenDefinition(
        "function",
        _halt_pop_chained_filters.union(_parenthesized_arguments),
        0,
        r"".join(
            (
                r"function\s+([$A-Z_a-z][$0-9A-Z_a-z]*)\s*",
                r"\(\s*([$A-Z_a-z][$0-9A-Z_a-z]*",
                r"(?:\s[$A-Z_a-z][$0-9A-Z_a-z]*)*)\s*\)",
                r"\s*{",
            )
        ),
        _any_filter,
        _any_filter,
    )

    GAMENUMBER = TokenDefinition(
        "gamenumber",
        _allowed_top_stack_at_end.union(_allowed_unary_minus),
        0,
        r"gamenumber\b",
        _numeric_filter,
        _empty_set,
    )
    HASCOMMENT = TokenDefinition(
        "hascomment",
        _allowed_top_stack_at_end,
        0,
        r'hascomment\s+(?:"((?:[^\\"]|\\.)*)")',
        _logical_filter,
        _empty_set,
    )
    INITIAL = TokenDefinition(
        "initial",
        _allowed_top_stack_at_end,
        0,
        r"initial\b",
        _logical_filter,
        _empty_set,
    )
    ISOLATEDPAWNS = TokenDefinition(
        "isolatedpawns",
        _allowed_top_stack_at_end,
        0,
        r"isolatedpawns\b",
        _set_filter,
        _empty_set,
    )
    MAINLINE = TokenDefinition(
        "mainline",
        _allowed_top_stack_at_end,
        0,
        r"mainline\b",
        _logical_filter,
        _empty_set,
    )
    MATE = TokenDefinition(
        "mate",
        _allowed_top_stack_at_end,
        0,
        r"mate\b",
        _logical_filter,
        _empty_set,
    )
    MOVENUMBER = TokenDefinition(
        "movenumber",
        _allowed_top_stack_at_end.union(_allowed_unary_minus),
        0,
        r"movenumber\b",
        _numeric_filter,
        _empty_set,
    )
    PARENT = TokenDefinition(
        "parent",
        _allowed_top_stack_at_end,
        0,
        r"parent\b",
        _position_filter,
        _empty_set,
    )
    PASSEDPAWNS = TokenDefinition(
        "passedpawns",
        _allowed_top_stack_at_end,
        0,
        r"passedpawns\b",
        _set_filter,
        _empty_set,
    )

    # The table of filters gives persistent an argument 'variable = <value>',
    # but the argument could be just 'variable' implying the initial value 0.
    # Try treating persistent as an optional keyword preceding the variable
    # name. 'persistent' cannot be a variable name.
    # PERSISTENT = TokenDefinition(
    #    'persistent', _no_flags, 100, r'persistent', _empty_set,
    #    TokenTypes.NUMERIC_VARIABLE)
    PERSISTENT = TokenDefinition(
        "persistent",
        _allowed_top_stack_at_end,
        100,
        r"persistent\b",
        _logical_filter,
        _empty_set,
    )

    # This was ok without _allowed_top_stack_at_end flag, so may be broken now.
    PIECE_DESIGNATOR = TokenDefinition(
        "piecedesignator",
        _allowed_top_stack_at_end,
        0,
        constants.PIECE_DESIGNATOR,
        _set_filter,
        _empty_set,
    )

    PLAYER = TokenDefinition(
        "player",
        _allowed_top_stack_at_end,
        0,
        r'player\s+(?:(?:black|white)\s+)?(?:"((?:[^\\"]|\\.)*)")',
        _logical_filter,
        _empty_set,
    )
    PLY = TokenDefinition(
        "ply",
        _allowed_top_stack_at_end.union(_allowed_unary_minus),
        0,
        r"ply\b",
        _numeric_filter,
        _empty_set,
    )
    POSITIONID = TokenDefinition(
        "positionid",
        _allowed_top_stack_at_end.union(_allowed_unary_minus),
        0,
        r"positionid\b",
        _numeric_filter,
        _empty_set,
    )
    RESULT = TokenDefinition(
        "result",
        _allowed_top_stack_at_end,
        0,
        r'result(?:\s+(?:(?:1-0|0-1|1/2-1/2)|"(?:1-0|0-1|1/2-1/2)"))',
        _logical_filter,
        _empty_set,
    )
    SIDETOMOVE = TokenDefinition(
        "sidetomove",
        _allowed_top_stack_at_end,
        0,
        r"sidetomove\b",
        _numeric_filter,
        _empty_set,
    )
    SITE = TokenDefinition(
        "site",
        _allowed_top_stack_at_end,
        0,
        r'site\s+(?:"((?:[^\\"]|\\.)*)")',
        _logical_filter,
        _empty_set,
    )
    STALEMATE = TokenDefinition(
        "stalemate",
        _allowed_top_stack_at_end,
        0,
        r"stalemate\b",
        _logical_filter,
        _empty_set,
    )
    TERMINAL = TokenDefinition(
        "terminal",
        _allowed_top_stack_at_end,
        0,
        r"terminal\b",
        _logical_filter,
        _empty_set,
    )
    TRUE = TokenDefinition(
        "true",
        _allowed_top_stack_at_end,
        0,
        r"true\b",
        _logical_filter,
        _empty_set,
    )
    VARIATION = TokenDefinition(
        "variation",
        _allowed_top_stack_at_end,
        0,
        r"variation\b",
        _logical_filter,
        _empty_set,
    )
    VIRTUALMAINLINE = TokenDefinition(
        "virtualmainline",
        _allowed_top_stack_at_end,
        0,
        r"virtualmainline\b",
        _logical_filter,
        _empty_set,
    )
    WHITE = TokenDefinition(
        "white",
        _allowed_top_stack_at_end,
        0,
        r"white\b",
        _numeric_filter,
        _empty_set,
    )
    WTM = TokenDefinition(
        "wtm",
        _allowed_top_stack_at_end,
        0,
        r"wtm\b",
        _logical_filter,
        _empty_set,
    )
    YEAR = TokenDefinition(
        "year",
        _allowed_top_stack_at_end,
        0,
        r"year\b",
        _numeric_filter,
        _empty_set,
    )
    DOT = TokenDefinition(
        "dot", _allowed_top_stack_at_end, 0, r"\.", _set_filter, _empty_set
    )

    # The '//' and '/* ... */' tokens for comments in CQL statements.

    # Not put on stack so _allowed_top_stack_at_end flag not needed.
    EOLCOMMENT = TokenDefinition(
        "eolcomment", _no_flags, 0, r"//.*(?:\n|\Z)", _empty_set, _empty_set
    )
    BLOCKCOMMENT = TokenDefinition(
        "blockcomment", _no_flags, 0, r"/\*[\S|\s]*\*/", _empty_set, _empty_set
    )

    # The parameter tokens for the 'find' filter.

    ALL = TokenDefinition(
        "all", _no_flags, 0, r"all\b", _find_parameter, _empty_set
    )

    # The parameter tokens for the 'line' filter.

    # Tokens for parameters similar to those used with other filters.  In other
    # words not those for regular expressions.
    FIRSTMATCH = TokenDefinition(
        "firstmatch",
        _no_flags,
        0,
        r"firstmatch\b",
        _line_parameter,
        _empty_set,
    )
    LASTPOSITION = TokenDefinition(
        "lastposition",
        _no_flags,
        0,
        r"lastposition\b",
        _line_parameter,
        _empty_set,
    )
    SINGLECOLOR = TokenDefinition(
        "singlecolor",
        _no_flags,
        0,
        r"singlecolor\b",
        _line_parameter,
        _empty_set,
    )
    NESTBAN = TokenDefinition(
        "nestban", _no_flags, 0, r"nestban\b", _line_parameter, _empty_set
    )

    # '*' has two meanings, multiply, and repeat in regular expressions.
    # To force repeat meaning use '{*}'.
    REPEATSTAR = TokenDefinition(
        "repeatstar",
        _allowed_top_stack_at_end,
        20,
        r"{\*}",
        _line_re_symbols,
        _empty_set,
    )

    # '+' has two meanings, plus, and repeat in regular expressions.
    # To force repeat meaning use '{+}'.
    REPEATPLUS = TokenDefinition(
        "repeatplus",
        _allowed_top_stack_at_end,
        20,
        r"{\+}",
        _line_re_symbols,
        _empty_set,
    )

    # This is safe because a compound filter cannot have a literal number, or
    # a numeric variable, as a constituent filter.  The CQL version 6 runtime
    # messages often say something like 'filter would always match' or
    # 'likely error' in other contexts, rather than give a parsing error.
    # Thus anything like '{1}' or '{1 2}' must be a repeat range for a regular
    # expression if it is allowed at all.
    # Numeric variables are not allowed in repeat ranges.
    REPEATRANGE = TokenDefinition(
        "repeatrange",
        _allowed_top_stack_at_end,
        20,
        r"\s*{\s*[1-9][0-9]*(?:\s+[1-9][0-9]*)?\s*}",
        _line_re_symbols,
        _empty_set,
    )

    QUERY = TokenDefinition(
        "query",
        _allowed_top_stack_at_end,
        20,
        r"\?",
        _line_re_symbols,
        _empty_set,
    )
    RIGHTARROW = TokenDefinition(
        "rightarrow",
        _no_arithmetic_filters,
        10,
        r"-->",
        _line_parameter,
        _line_constituents,
    )

    # The parameter tokens for the 'find' or 'line' filters.

    # 'leftarrow' operates very differently in 'find' and 'line' filters.
    # The 'find' filter use is similar to parameters in other filters so it's
    # definition describes how it works in 'line' filter.
    # Maybe it will be possible to put _line_constituents in the arguments
    # item, replacing _empty_set, if that is sufficient to control the 'line'
    # filter.
    LEFTARROW = TokenDefinition(
        "leftarrow",
        _no_arithmetic_filters,
        10,
        r"<--",
        _line_parameter,
        _line_constituents,
    )

    # Tokens which are parameters of the consecutivemoves filter.
    QUIET = TokenDefinition(
        "quiet",
        _no_flags,
        0,
        r"quiet\b",
        _consecutivemoves_parameter,
        _empty_set,
    )

    # Tokens which are parameters of the move or pin filters.
    # count is also a parameter of transform filters where it is consumed as
    # part of the filter name.
    CAPTURE = TokenDefinition(
        "capture",
        _parameter_takes_argument,
        190,
        r"capture\b",
        _move_parameter,
        _set_filter,
    )
    CASTLE = TokenDefinition(
        "castle",
        _allowed_top_stack_at_end,
        0,
        r"castle\b",
        _move_parameter,
        _empty_set,
    )
    COUNT = TokenDefinition(
        "count",
        _allowed_top_stack_at_end,
        0,
        r"count\b",
        _move_parameter,
        _empty_set,
    )
    ENPASSANT = TokenDefinition(
        "enpassant",
        _allowed_top_stack_at_end,
        0,
        r"enpassant\b",
        _move_parameter,
        _empty_set,
    )
    ENPASSANT_SQUARE = TokenDefinition(
        "enpassantsquare",
        _parameter_takes_argument,
        190,
        r"enpassantsquare\b",
        _move_parameter,
        _set_filter,
    )
    FROM = TokenDefinition(
        "from_",
        _parameter_takes_argument,
        190,
        r"from\b",
        _move_or_pin_parameter,
        _set_filter,
    )
    LEGAL = TokenDefinition(
        "legal",
        _allowed_top_stack_at_end,
        0,
        r"legal\b",
        _move_parameter,
        _empty_set,
    )
    NULL = TokenDefinition(
        "null",
        _allowed_top_stack_at_end,
        0,
        r"null\b",
        _move_parameter,
        _empty_set,
    )
    OO = TokenDefinition(
        "oo",
        _allowed_top_stack_at_end,
        0,
        r"o-o\b",
        _move_parameter,
        _empty_set,
    )
    OOO = TokenDefinition(
        "ooo",
        _allowed_top_stack_at_end,
        0,
        r"o-o-o\b",
        _move_parameter,
        _empty_set,
    )
    PREVIOUS = TokenDefinition(
        "previous",
        _allowed_top_stack_at_end,
        0,
        r"previous\b",
        _move_parameter,
        _empty_set,
    )
    PRIMARY = TokenDefinition(
        "primary",
        _allowed_top_stack_at_end,
        0,
        r"primary\b",
        _move_parameter,
        _empty_set,
    )
    PROMOTE = TokenDefinition(
        "promote",
        _parameter_takes_argument,
        0,
        r"promote\b",
        _move_parameter,
        _set_filter,
    )
    PSEUDOLEGAL = TokenDefinition(
        "pseudolegal",
        _allowed_top_stack_at_end,
        0,
        r"pseudolegal\b",
        _move_parameter,
        _empty_set,
    )
    SECONDARY = TokenDefinition(
        "secondary",
        _allowed_top_stack_at_end,
        0,
        r"secondary\b",
        _move_parameter,
        _empty_set,
    )
    THROUGH = TokenDefinition(
        "through",
        _parameter_takes_argument,
        190,
        r"through\b",
        _pin_parameter,
        _set_filter,
    )
    TO = TokenDefinition(
        "to",
        _parameter_takes_argument,
        190,
        r"to\b",
        _move_or_pin_parameter,
        _set_filter,
    )

    # Tokens for parameters consumed with the filter token, or filters which
    # consume at least one mandatory parameter.
    PIECE = TokenDefinition(
        "piece", _no_flags, 0, r"piece\b", _empty_set, _empty_set
    )
    SQUARE = TokenDefinition(
        "square", _no_flags, 0, r"square\b", _empty_set, _empty_set
    )
    OUTPUT = TokenDefinition(
        "output", _no_flags, 0, r"output\b", _empty_set, _empty_set
    )
    INPUT = TokenDefinition(
        "input_", _no_flags, 0, r"input\b", _empty_set, _empty_set
    )
    MATCHCOUNT = TokenDefinition(
        "matchcount", _no_flags, 0, r"matchcount\b", _empty_set, _empty_set
    )
    SILENT = TokenDefinition(
        "silent", _no_flags, 0, r"silent\b", _empty_set, _empty_set
    )
    VARIATIONS = TokenDefinition(
        "variations", _no_flags, 0, r"variations\b", _empty_set, _empty_set
    )
    MATCHSTRING = TokenDefinition(
        "matchstring", _no_flags, 0, r"matchstring\b", _empty_set, _empty_set
    )

    # Named so they sort high as choices in the regular expression.
    # Variables documentation for CQL version 6.0.4 does not ban a digit as the
    # first character in the name: but a syntax error is raised (which is what
    # I would expect normally).
    NUMBER = TokenDefinition(
        "x",
        _allowed_top_stack_at_end.union(_allowed_unary_minus),
        0,
        r"[0-9]+",
        _numeric_filter,
        _empty_set,
    )

    # Nodes for variables have this TokenDefinition when the variable is first
    # mentioned in a '<variable> = <something>' clause.  The '=' filter forces
    # it to one of the four variable types.
    # A new flag may be needed because _allowed_top_stack_at_end also enables
    # infix operators but <variable> should get this flag only when converted
    # during assignment: 'x = 1' say.
    VARIABLE = TokenDefinition(
        "y",
        _allowed_top_stack_at_end.union(_assign_to_variable).union(
            _allowed_unary_minus
        ),
        0,
        r"[$A-Z_a-z][$0-9A-Z_a-z]*\b",
        _unset_variable,
        _empty_set,
    )

    BADTOKEN = TokenDefinition(
        "z", _no_flags, 0, r"\S+", _empty_set, _empty_set
    )

    # 'if' filter with 'then' and 'else' parameters.

    # Not sure this can work as it stands because the parameter is after the
    # argument, but most filters have it the other way round.
    # Setting Token[4] to _logical_filter for 'then' and 'else' is assumed to
    # be correct: these cannot exist except as qualifiers of 'if', and provide
    # alternative results for whole 'if' filter.

    # Follow, and extend, the treatment of the 'line' filter for 'if' filter
    # token definitions.

    # Parameter sequence is different to 'line' filter in content and style.
    # 'if <filter> then <filter> else <filter>' and no more then or else parts,
    # with the 'else' optional.
    # Initial search is for IF filter, which gets renamed as IF_FILTER while
    # looking for the condition filter, and so forth until the whole filter is
    # found.  The final name is one of IF_LOGICAL and the
    # three similar for numeric, position, and set, filters.
    IF = TokenDefinition(
        "if_",
        _incomplete_if_on_stack.union(_if_frame),
        40,
        r"if\b",
        _any_filter,
        _any_filter,
    )

    # _no_flags compared with LEFTARROW and RIGHTARROW because there is no
    # arithmetic ambiguity arising from the repeat operators.
    THEN = TokenDefinition(
        "then", _no_flags, 40, r"then\b", _then_parameter, _any_filter
    )
    ELSE = TokenDefinition(
        "else_", _no_flags, 40, r"else\b", _else_parameter, _any_filter
    )


# Map token names to definitions: name is in definition.
CQL_TOKENS = {
    getattr(Token, a).name: getattr(Token, a)
    for a in dir(Token)
    if not a.startswith("__")
}

# The pattern to parse CQL version 6.0.4 statements.
CQL_PATTERN = r"".join(
    (
        r"(?:",
        r"|".join(
            [
                r"".join((r"(?P<", i[-1].name, ">", i[-1].pattern, r")"))
                for i in sorted(
                    [
                        (
                            -len(getattr(Token, v)[0]),
                            getattr(Token, v)[0],
                            getattr(Token, v),
                        )
                        for v in dir(Token)
                        if not v.startswith("__")
                    ]
                )
            ]
        ),
        r")",
        r"(?:\s*|\Z)",
    )
)

# Map direction TokenDefinitions to constituent basic directions.
CQL_DIRECTIONS = {
    Token.UP: {Token.UP},
    Token.DOWN: {Token.DOWN},
    Token.RIGHT: {Token.RIGHT},
    Token.LEFT: {Token.LEFT},
    Token.NORTHEAST: {Token.NORTHEAST},
    Token.NORTHWEST: {Token.NORTHWEST},
    Token.SOUTHEAST: {Token.SOUTHEAST},
    Token.SOUTHWEST: {Token.SOUTHWEST},
    Token.DIAGONAL: {
        Token.NORTHEAST,
        Token.NORTHWEST,
        Token.SOUTHEAST,
        Token.SOUTHWEST,
    },
    Token.ORTHOGONAL: {Token.UP, Token.DOWN, Token.RIGHT, Token.LEFT},
    Token.VERTICAL: {Token.UP, Token.DOWN},
    Token.HORIZONTAL: {Token.RIGHT, Token.LEFT},
    Token.ANYDIRECTION: {
        Token.UP,
        Token.DOWN,
        Token.RIGHT,
        Token.LEFT,
        Token.NORTHEAST,
        Token.NORTHWEST,
        Token.SOUTHEAST,
        Token.SOUTHWEST,
    },
}

# Variable names starting '__CQL' are reserved.
CQL_RESERVED_VARIABLE_NAME_PREFIX = "__CQL"

# Variants of filters defined in CQL.
# The Token.name must be unique amongst all Tokens.  (Maybe the definition of
# Token needs an extra field 'variantof' rather than put the name of that Token
# in the 'flags' field.)
# The 'pattern' field is relative to the match found in the CQL Token, not the
# whole CQL statement.
# The piece and square filters, which could be done with this technique, have
# separate entries in CQL to deal with their 'all' parameters.  (I had not
# thought 'do it this way' yet.)
# 'line --> 1' is a parsing error in CQL version 6: attempt to create line
# constituent from single number.
# 'line --> #k* is ok at CQL version 6: the '*' is taken as a repeat operator.
# 'line --> #k*2 is a parsing error in CQL version 6: attempt to create line
# constituent from binary arithmetic operation.
# Thus literal numbers can be rejected, and '*' and '+' interpreted as regular
# expression operators in '-->' and '<--' context.
# 'line --> #k-2 is a parsing error in CQL version 6: attempt to create line
# constituent from binary arithmetic operation.  There is no ambiguous meaning
# for '-', at least yet, but it is still rejected.
LINE_LEFTARROW = TokenDefinition(
    "line_leftarrow",
    _halt_pop_chained_filters.union(_line_frame),
    0,
    r"line\b",
    _numeric_filter,
    _line_leftarrow_parameter,
)
LINE_RIGHTARROW = TokenDefinition(
    "line_rightarrow",
    _halt_pop_chained_filters.union(_line_frame),
    0,
    r"line\b",
    _numeric_filter,
    _line_rightarrow_parameter,
)

IF_LOGICAL = TokenDefinition(
    "if_logical", _no_flags, 40, r"if\b", _logical_filter, _empty_set
)
IF_NUMERIC = TokenDefinition(
    "if_numeric", _no_flags, 40, r"if\b", _numeric_filter, _empty_set
)
IF_POSITION = TokenDefinition(
    "if_position", _no_flags, 40, r"if\b", _position_filter, _empty_set
)
IF_SET = TokenDefinition(
    "if_set", _no_flags, 40, r"if\b", _set_filter, _empty_set
)

# Some filters take optional parameters that are ambiguous when lexing: numeric
# variables as part of a range in particular.  These cannot consume the '(' as
# part of the filter and must have this filter as their last child, or last but
# one if it has a body too.  At present some filters means consecutivemoves but
# there is a case for treating all filters with arguments within '()' this way.
# A list of filters is enclosed by '()' with this definition of '('.
CONSECUTIVEMOVES_LEFTPARENTHESIS = TokenDefinition(
    "consecutivemoves_leftparenthesis",
    _halt_pop_chained_filters.union(_parenthesized_arguments),
    0,
    r"consecutivemoves\b",
    _numeric_filter,
    _position_variable,
)

CHILD_NO_ARGUMENT = TokenDefinition(
    "child_no_argument",
    _allowed_top_stack_at_end,
    0,
    r"child(?:\s*\()?",
    _position_filter,
    _empty_set,
)
FIND_NUMERIC = TokenDefinition(
    "find_numeric", _no_flags, 40, r"find\b", _numeric_filter, _any_filter
)
SINGLE_COMMENT_ARGUMENT = TokenDefinition(
    "single_comment_argument",
    _no_flags,
    0,
    r"comment(?:\s*\()?",
    _logical_filter,
    _any_filter,
)
SINGLE_MESSAGE_ARGUMENT = TokenDefinition(
    "single_message_argument",
    _no_flags,
    0,
    r"message(?:\s*\()?",
    _logical_filter,
    _any_filter,
)
MOVE_SET = TokenDefinition(
    "move_set",
    _end_filter_non_parameter.union(_allowed_top_stack_at_end),
    0,
    r"move\b",
    _set_filter,
    _move_parameter,
)
ECHO_IN_ALL = TokenDefinition(
    "echo_in_all",
    _incomplete_if_on_stack.union(_halt_pop_no_body_filter),
    0,
    r"in\s+all\b",
    _logical_filter,
    _any_filter,
)
FLIP_COUNT = TokenDefinition(
    "flip_count", _no_flags, 40, r"\s+count\b", _numeric_filter, _any_filter
)
FLIPCOLOR_COUNT = TokenDefinition(
    "flipcolor_count",
    _no_flags,
    40,
    r"\s+count\b",
    _numeric_filter,
    _any_filter,
)
FLIPHORIZONTAL_COUNT = TokenDefinition(
    "fliphorizontal_count",
    _no_flags,
    40,
    r"\s+count\b",
    _numeric_filter,
    _any_filter,
)
FLIPVERTICAL_COUNT = TokenDefinition(
    "flipvertical_count",
    _no_flags,
    40,
    r"\s+count\b",
    _numeric_filter,
    _any_filter,
)
ROTATE45_COUNT = TokenDefinition(
    "rotate45_count",
    _no_flags,
    40,
    r"\s+count\b",
    _numeric_filter,
    _any_filter,
)
ROTATE90_COUNT = TokenDefinition(
    "rotate90_count",
    _no_flags,
    40,
    r"\s+count\b",
    _numeric_filter,
    _any_filter,
)
SHIFT_COUNT = TokenDefinition(
    "shift_count", _no_flags, 40, r"\s+count\b", _numeric_filter, _any_filter
)
SHIFTHORIZONTAL_COUNT = TokenDefinition(
    "shifthorizontal_count",
    _no_flags,
    40,
    r"\s+count\b",
    _numeric_filter,
    _any_filter,
)
SHIFTVERTICAL_COUNT = TokenDefinition(
    "shiftvertical_count",
    _no_flags,
    40,
    r"\s+count\b",
    _numeric_filter,
    _any_filter,
)
RANGE = TokenDefinition(
    "range_", _no_flags, 0, r"(?:\s+[0-9]+){,2}", None, _empty_set
)
ELO_BLACK = TokenDefinition(
    "elo_black", _no_flags, 0, r"black\b", _numeric_filter, _empty_set
)
ELO_WHITE = TokenDefinition(
    "elo_white", _no_flags, 0, r"white\b", _numeric_filter, _empty_set
)
PLAYER_BLACK = TokenDefinition(
    "player_black", _no_flags, 0, r"black\b", _logical_filter, _empty_set
)
PLAYER_WHITE = TokenDefinition(
    "player_white", _no_flags, 0, r"white\b", _logical_filter, _empty_set
)
SORT_MIN = TokenDefinition(
    "sort_min", _no_flags, 0, r"min\b", _numeric_filter, _numeric_filter
)
QUOTED_STRING = TokenDefinition(
    "string",
    _no_flags,
    0,
    r'(sort)(\s+min)?(\s+"(?:[^\\"]|\\.)*")?',
    _empty_set,
    _empty_set,
)
LEFTPARENTHESIS_NUMBER = TokenDefinition(
    "leftparenthesis_number",
    _allowed_top_stack_at_end.union(_allowed_unary_minus),
    0,
    r"\(",
    _numeric_filter,
    _empty_set,
)
LEFTPARENTHESIS_POSITION = TokenDefinition(
    "leftparenthesis_position",
    _allowed_top_stack_at_end,
    0,
    r"\(",
    _position_filter,
    _empty_set,
)
LEFTPARENTHESIS_SET = TokenDefinition(
    "leftparenthesis_set",
    _allowed_top_stack_at_end,
    0,
    r"\(",
    _set_filter,
    _empty_set,
)
LEFTPARENTHESIS_LOGICAL = TokenDefinition(
    "leftparenthesis_logical",
    _allowed_top_stack_at_end,
    0,
    r"\(",
    _logical_filter,
    _empty_set,
)
INTERSECTION_POSITION = TokenDefinition(
    "intersection_position",
    _named_compound_filter,
    160,
    r"&",
    _set_filter,
    _position_filter,
)
INTERSECTION_SET = TokenDefinition(
    "intersection_set",
    _named_compound_filter,
    160,
    r"&",
    _set_filter,
    _set_filter,
)
LEFTBRACE_NUMBER = TokenDefinition(
    "leftbrace_number",
    _allowed_top_stack_at_end.union(_allowed_unary_minus),
    0,
    r"{",
    _numeric_filter,
    _empty_set,
)
LEFTBRACE_POSITION = TokenDefinition(
    "leftbrace_position",
    _allowed_top_stack_at_end,
    0,
    r"{",
    _position_filter,
    _empty_set,
)
LEFTBRACE_SET = TokenDefinition(
    "leftbrace_set",
    _allowed_top_stack_at_end,
    0,
    r"{",
    _set_filter,
    _empty_set,
)
LEFTBRACE_LOGICAL = TokenDefinition(
    "leftbrace_logical",
    _allowed_top_stack_at_end,
    0,
    r"{",
    _logical_filter,
    _empty_set,
)

# The kinds of variable after assignment by '<variable> = <something>' or
# 'function <variable> ( <argument list> ) { <body> }'.
# Probably need two kinds for functions: definition and call.
FUNCTION_CALL = TokenDefinition(
    "function_call",
    _halt_pop_chained_filters.union(_parenthesized_arguments),
    0,
    r"[$A-Z_a-z][$0-9A-Z_a-z]*\b",
    _empty_set,
    _any_filter,
)
FUNCTION_NAME = TokenDefinition(
    "function_name",
    _no_flags,
    0,
    r"[$A-Z_a-z][$0-9A-Z_a-z]*\b",
    _empty_set,
    _empty_set,
)
NUMERIC_VARIABLE = TokenDefinition(
    "y",
    _allowed_top_stack_at_end.union(_assign_to_variable).union(
        _allowed_unary_minus
    ),
    0,
    r"[$A-Z_a-z][$0-9A-Z_a-z]*\b",
    _numeric_filter,
    _empty_set,
    "numeric_variable",
)
PIECE_VARIABLE = TokenDefinition(
    "y",
    _allowed_top_stack_at_end.union(_assign_to_variable),
    0,
    r"[$A-Z_a-z][$0-9A-Z_a-z]*\b",
    _set_filter,
    _empty_set,
    "piece_variable",
)
POSITION_VARIABLE = TokenDefinition(
    "y",
    _allowed_top_stack_at_end.union(_assign_to_variable),
    0,
    r"[$A-Z_a-z][$0-9A-Z_a-z]*\b",
    _position_filter,
    _empty_set,
    "position_variable",
)
SET_VARIABLE = TokenDefinition(
    "y",
    _allowed_top_stack_at_end.union(_assign_to_variable),
    0,
    r"[$A-Z_a-z][$0-9A-Z_a-z]*\b",
    _set_filter,
    _empty_set,
    "set_variable",
)

# Unary minus appears twice in the precedence table for CQL version 6: just
# above, alongside others, and just below arithmetic plus and minus.  So 100
# or 120 is the appropriate value for the precedence attribute.  The correct
# choice is assumed to be 120: '-1+1' means '(-1)+1' not '-(1+1)'.
UNARY_MINUS = TokenDefinition(
    "minus", _no_flags, 120, r"-", _numeric_filter, _numeric, "unary_minus"
)

# Comparison operator variants named for the kind of left operand when it is
# not a numeric filter.
# An EQ_SET is changed to an EQ_BOTH_SETS to indicate the correct returntype,
# which depends on the right operand found for EQ_SET.
LT_SET = TokenDefinition(
    "lt",
    _named_compound_filter,
    90,
    r"<",
    _numeric_filter,
    _numeric_filter,
    "lt_set",
)
LE_SET = TokenDefinition(
    "le",
    _named_compound_filter,
    90,
    r"<=",
    _numeric_filter,
    _numeric_filter,
    "le_set",
)
GT_SET = TokenDefinition(
    "gt",
    _named_compound_filter,
    90,
    r">",
    _numeric_filter,
    _numeric_filter,
    "gt_set",
)
GE_SET = TokenDefinition(
    "ge",
    _named_compound_filter,
    90,
    r">=",
    _numeric_filter,
    _numeric_filter,
    "ge_set",
)
EQ_SET = TokenDefinition(
    "eq",
    _named_compound_filter,
    90,
    r"==",
    _numeric_filter,
    _relation_filters.difference(_position_filter),
    "eq_set",
)
EQ_BOTH_SETS = TokenDefinition(
    "eq_both_sets",
    _named_compound_filter,
    90,
    r"==",
    _logical_filter,
    _empty_set,
)
NE_SET = TokenDefinition(
    "ne",
    _named_compound_filter,
    90,
    r"!=",
    _logical_filter,
    _relation_filters.difference(_position_filter),
    "ne_set",
)
NE_BOTH_SETS = TokenDefinition(
    "ne_both_sets",
    _named_compound_filter,
    90,
    r"!=",
    _logical_filter,
    _empty_set,
)
LT_POSITION = TokenDefinition(
    "lt",
    _named_compound_filter,
    90,
    r"<",
    _numeric_filter,
    _position_filter,
    "lt_position",
)
LE_POSITION = TokenDefinition(
    "le",
    _named_compound_filter,
    90,
    r"<=",
    _numeric_filter,
    _position_filter,
    "le_position",
)
GT_POSITION = TokenDefinition(
    "gt",
    _named_compound_filter,
    90,
    r">",
    _numeric_filter,
    _position_filter,
    "gt_position",
)
GE_POSITION = TokenDefinition(
    "ge",
    _named_compound_filter,
    90,
    r">=",
    _numeric_filter,
    _position_filter,
    "ge_position",
)
EQ_POSITION = TokenDefinition(
    "eq",
    _named_compound_filter,
    90,
    r"==",
    _numeric_filter,
    _position_filter,
    "eq_position",
)
NE_POSITION = TokenDefinition(
    "ne",
    _named_compound_filter,
    90,
    r"!=",
    _logical_filter,
    _position_filter,
    "ne_position",
)

ASSIGNMENT_VARIABLE_TYPES = frozenset(
    (
        NUMERIC_VARIABLE,
        POSITION_VARIABLE,
        PIECE_VARIABLE,
        SET_VARIABLE,
    )
)

# A variable is the Token.VARIABLE TokenDefinition when first encountered.  On
# first assignment, <variable> = <?> or piece <variable> in <?>, it becomes a
# NUMERIC_VARIABLE, PIECE_VARIABLE, POSITION_VARIABLE, or SET_VARIABLE.
# The 'piece' filter assigns 'piece' filters to variables:
# 'piece <variable> = <set filter>'.
# The other three assignments are done by plain '<variable> = <filter>'.
# This avoids ambiguity on action for set filters.
map_filter_assign_to_variable = {
    _numeric_filter: NUMERIC_VARIABLE,
    _position_filter: POSITION_VARIABLE,
    _set_filter: SET_VARIABLE,
}

# Many filters with parenthesized arguments do not have parameters preventing
# consuming the '(' with the filter name.  Those which do are mapped to a
# version used after detection of the '(' here.
map_filter_to_leftparenthesis = {
    Token.CONSECUTIVEMOVES: CONSECUTIVEMOVES_LEFTPARENTHESIS,
    FUNCTION_CALL: FUNCTION_CALL,
}

# When a single filter is enclosed in parentheses the parentheses effectively
# inherit the type of the enclosed filter.
map_filter_type_to_leftparenthesis_type = {
    _numeric_filter: LEFTPARENTHESIS_NUMBER,
    _set_filter: LEFTPARENTHESIS_SET,
    _logical_filter: LEFTPARENTHESIS_LOGICAL,
    _position_filter: LEFTPARENTHESIS_POSITION,
}

# The compound filter is the same type as it's last filter.
map_filter_type_to_leftbrace_type = {
    _numeric_filter: LEFTBRACE_NUMBER,
    _set_filter: LEFTBRACE_SET,
    _logical_filter: LEFTBRACE_LOGICAL,
    _position_filter: LEFTBRACE_POSITION,
}

del _empty_set
del _numeric
del _numeric_filter
del _set_filter
del _logical_filter
del _position_filter
del _any_filter
del _line_re_symbols
del _line_constituents
del _move_parameter
del _pin_parameter
del _move_or_pin_parameter
del _assign_filters
del _consecutivemoves_parameter
del _find_parameter
del _line_parameter
del _line_leftarrow_parameter
del _line_rightarrow_parameter
del _position_variable
del _relation_filters
del _if_constituents
del _then_parameter
del _else_parameter
del _unset_variable

del _no_flags
del _halt_pop_chained_filters
del _close_brace_or_parenthesis
del _named_compound_filter
del _assign_to_variable
del _incomplete_if_on_stack
del _allowed_top_stack_at_end
del _parameter_takes_argument
del _parenthesized_arguments
del _halt_pop_no_body_filter
del _accept_range
del _end_filter_non_parameter
del _allowed_unary_minus
del _no_arithmetic_filters
del _statement_frame
del _line_frame
del _if_frame
