# statement.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) statement parser.

The basic structure of a CQL statement at version 6.0.4 is:

'cql ( parameters ) list_of_filters'.

This module allows both parameters and list_of_filters to be empty.

Compared with CQL version 5.0 several filters have been retired and many have
been added.  The scope of this module has been extended to cover parsing all
filters because the CQL documentation now gives a clear path to tackle the
task.  Evaluation of filters is outside the scope of this module because it
depends on the data structures which store chess games.

The Statement class has methods named for each filter and filter parameter,
and in most cases the CQL documentation is used exclusively to guide the
method implementations.  It seems necessary to provide docstrings for a few
methods to clarify interpretation of the CQL documentation.

The restrictions on combining parameters of the 'move' filter are often not
stated, and in some cases are not immediately obvious when exposed by a
'cql -parse' statement.  Each method for a 'move' filter parameter has the
restrictions stated in it's docstring, even if the method would not otherwise
get a docstring.

"""
import re

from .constants import WHITE_WIN, BLACK_WIN, DRAW
from .node import Node
from . import cql

GAME_RESULTS = WHITE_WIN, BLACK_WIN, DRAW


class StatementError(Exception):
    """Exception raised for problems in Statement."""


class Statement:
    """CQL statement parser for version 6.0.4 of CQL.

    Parse text for a CQL statement.

    """

    create_node = Node

    # Otherwise pylint makes attribute-defined-outside-init reports for all
    # _range, tokens, and cql_filters, references except the ones in
    # _reset_state() called by __init__().
    # However putting tokens here causes a report for the query.tokens[0]
    # reference in the code after 'if __name__ == "__main__":', which does
    # not occur when tokens is not here..
    _range = None
    tokens = None
    cql_filters = None

    def __init__(self):
        """Initialise as a valid empty statement."""
        super().__init__()
        self._statement_string = ""
        self._reset_state()
        self._error_information = None

    def _reset_state(self):
        """Initialiase the CQL parsing state.

        The analyser is able to have at least two goes at a statement.

        """
        self._error_information = False
        self.tokens = None
        self.cql_tokens_stack = [[]]
        self.node_stack = []
        self.cql_parameters = None
        self.cql_filters = None

        # Scoping rules for piece and square variables at cql5.1 seem to be:
        # $name is unique across piece and square use and cannot be redefined.
        # $name is visible in all enclosed scopes.
        # $name scope is bounded by '( ... )' and '{ ... }'.
        # This is not certain because:
        # '{square $x in h1-8 attack (R $x)} attack (Q $x)' gets error unbound,
        # 'square $x in h1-8 attack (R $x) attack (Q $x)' is ok,
        # '{shift 1 square $x in h1-8 attack (R $x)} attack (Q $x)' is ok.
        # However:
        # '{shift 0 square $x in h1-8 attack (R $x)} attack (Q $x)' gives
        # error undeclared so 'attack (Q $x)' is probably ignored in the
        # 'shift 1' version because the shift filter evaluates False or empty,
        # so the scoping assumption is probably sound.

        # At cql6.0.4 the description of variable scoping is:
        # The value of a variable cannot be accessed before it is defined. Once
        # defined, the variable retains its type, but not necessarily its value
        # as the program progresses.
        # At cql6.0.4 the description of variable values is:
        # There are four types of variables: numeric variables, set variables,
        # piece variables and position variables.  Once assigned, a variable
        # cannot change its type.
        # In addition, numeric variables can be either persistent or normal:
        # persistent values (sic) retain their value between games.
        # A variable must have been assigned a value before the variable is
        # used, and (except for persistent variables) the value of a variable
        # is unassigned before CQL begins parsing of a new game.
        # A variable is assign using the = filter.
        # More is said about variable assignment for each of the four types of
        # variable.
        # Numeric: assigned using = and modified using +=, -=, /=, *=, and %=.
        # Set: assigned using =, including =? variant, or the square filter.
        # Position: assigned using =.
        # Piece: assigned using the piece filter or piece assignment filter.
        # The piece filter is 'piece x in A ...'
        # The piece assignment filter is 'piece x = <set filter>'.

        # All declared variable names.
        self.variables = {}

        # For collecting ranges where filter allows it.
        self._range = []

        # Prevent recursive user-defined function calls, including indirect.
        self._called_functions = set()

        # Include in variable names corresponding to formal parameter names
        # and increment to guarantee unique names.
        self._formal_parameter_number = 0

    @property
    def cql_error(self):
        """Return the error information for the CQL statement."""
        return self._error_information

    @cql_error.setter
    def cql_error(self, value):
        if not self._error_information:
            self._error_information = ErrorInformation(
                self._statement_string.strip()
            )
        self._error_information.description = value

    def get_statement_text(self):
        """Return statement text."""
        return self._statement_string

    def lex(self):
        """Split the ChessQL statement into tokens."""
        # pylint complains 'unnecessary list comprehension' about the
        # commented version of the self.tokens binding. True, but
        # '[list(...)]' looks equally odd to me; and the apparent
        # alternatives 'list(list(<finditer>))' and [[<finditer>]] both
        # get a TypeError exception at the 'if len(tokens):' comparison
        # in self.parse (just below).  'list([<finditer>])', tried for
        # completeness, does not work either.
        #
        # It's finditer() rather than findall() for access to the dict of
        # groups whose keys are the names of methods in the Statement class.
        #
        # self.tokens = [[m for m in re.finditer(cql.CQL_PATTERN,
        #                                       self._statement_string)]]
        self.tokens = [
            list(re.finditer(cql.CQL_PATTERN, self._statement_string))
        ]
        if self._statement_string.strip() == "":
            self._error_information = False
            return

    def parse(self):
        """Generate a tree from tokens describing the query."""
        # lex() sets self._error_information False if statement is worth
        # parsing
        if self._error_information:
            return

        tokens = self.tokens[-1]
        node_stack = self.node_stack

        # Insist on first filter being 'cql', and give opportunity to create a
        # null cql filter if it isn't, so everything else has a parent node
        # available.
        if len(tokens):
            if not tokens[0].groupdict()["cql"]:
                node_stack.append(self.create_node(cql.CQL_TOKENS["cql"]))

        while len(tokens):
            match = tokens[0]
            groupkey = "".join(
                k
                for k, v in match.groupdict().items()
                if v is not None and ("_" not in k[:-1])
            )
            self._process_token(match, groupkey)
            if self._error_information and self._error_information.error_found:
                break
        self._collapse_stack_frame(cql.Flags.STATEMENT_FRAME)
        if self.cql_error:
            return
        if len(node_stack) == 1:
            self.cql_filters = node_stack[-1]
        else:
            self.cql_error = "Incomplete statement"

    def _collapse_stack_frame(self, frame):
        node_stack = self.node_stack
        if (
            node_stack
            and cql.Flags.ALLOWED_TOP_STACK_AT_END
            in node_stack[-1].tokendef.flags
        ):
            while True:
                if (
                    cql.Flags.END_FILTER_NON_PARAMETER
                    in node_stack[-1].tokendef.flags
                ):
                    getattr(self, "collapse_" + node_stack[-1].name)()
                    if self.cql_error:
                        return
                self._pop_top_stack(node_stack)

                # Normally INCOMPLETE_IF_ON_STACK is sufficient to halt the
                # collapse leaving an error condition.  But a valid IF filter
                # can be at end of statement because it is not converted to
                # one of IF_LOGICAL, IF_NUMERIC, IF_POSITION, and IF_SET, until
                # the next token.  So call _pop_top_stack for IF filter.
                if (
                    cql.Flags.INCOMPLETE_IF_ON_STACK
                    in node_stack[-1].tokendef.flags
                ):
                    if frame is not cql.Flags.STATEMENT_FRAME:
                        break
                    if node_stack[-1].tokendef is not cql.Token.IF:
                        break
                    self._pop_top_stack(node_stack)
                    if self.cql_error:
                        return
                    if frame in node_stack[-1].tokendef.flags:
                        break

                if (
                    cql.Flags.HALT_POP_CHAINED_FILTERS
                    in node_stack[-1].tokendef.flags
                ):
                    if frame not in node_stack[-1].tokendef.flags:
                        self._pop_top_stack(node_stack)
                    break

    # Defined so it can be overridden in "if __name__ == '__main__':" at end
    # of module: to print a trace of parsing in particular.
    def _process_token(self, match, groupkey):
        getattr(self, groupkey)(match, cql.CQL_TOKENS[groupkey])

    # For some entries there is still work to do before popping.  This method
    # was introduced to compare the _filter_type attributes of the variable and
    # number children in an assign, '=', item such as 'test = 20', or the now
    # illegal 'test = K', appearing after the first use of 'test' as a numeric
    # variable in, say, 'test = 0'.  It will likely have other uses.
    # Code was present for filters 'assign', 'variable', 'persistent', and
    # 'move', before it proved easier to deal with most of these elsewhere.
    # The code for 'move' remains because the absence of 'pseudolegal' and
    # 'legal' matters and some parameters, such as 'from', take a wide range
    # of set filter expressions as arguments: simplest sign that 'move' is
    # finished is when it is popped from stack.
    # All gone elsewhere, but retain structure for now.
    # Can override or extend for tracing: as in self-test at end.
    # Seems to be needed to turn a 'eq_set' into a 'eq_both_sets' when the
    # right operand is seen to be a set filter.  (Having a subclass of Node
    # for each TokenDefinition would allow a special <Node>.pop(stack) method
    # where needed.)  Similar for a 'ne_set'.
    def _pop_top_stack(self, stack):
        top = stack.pop()
        if top.tokendef is cql.EQ_SET:
            if cql.TokenTypes.SET_FILTER in top.children[-1].returntype:
                top.set_tokendef_to_variant(
                    cql.EQ_BOTH_SETS, same_arguments=False
                )
        elif top.tokendef is cql.NE_SET:
            if cql.TokenTypes.SET_FILTER in top.children[-1].returntype:
                top.set_tokendef_to_variant(
                    cql.NE_BOTH_SETS, same_arguments=False
                )

        # Presence of valid ELSE clause is assumed to imply presence of valid
        # THEN clause.
        elif top.tokendef is cql.Token.IF:
            if cql.Token.ELSE in top.parameters and len(top.children) != 3:
                self.cql_error = "".join(
                    (
                        "'",
                        top.tokendef.name,
                        "' filter does not have a filter as the '",
                        cql.Token.ELSE.name,
                        "' parameter",
                    )
                )
            elif cql.Token.THEN in top.parameters and len(top.children) < 2:
                self.cql_error = "".join(
                    (
                        "'",
                        top.tokendef.name,
                        "' filter does not have a filter as the '",
                        cql.Token.THEN.name,
                        "' parameter",
                    )
                )
            elif cql.Token.THEN not in top.parameters:
                self.cql_error = "".join(
                    (
                        "'",
                        top.tokendef.name,
                        "' filter does not have the '",
                        cql.Token.THEN.name,
                        "' parameter",
                    )
                )
            elif cql.Token.ELSE in top.parameters:
                srt = top.children[1].returntype.intersection(
                    top.children[2].returntype
                )
                if cql.TokenTypes.NUMERIC_FILTER in srt:
                    variant = cql.IF_NUMERIC
                elif cql.TokenTypes.POSITION_FILTER in srt:
                    variant = cql.IF_POSITION
                elif cql.TokenTypes.SET_FILTER in srt:
                    variant = cql.IF_SET
                else:
                    variant = cql.IF_LOGICAL
                top.set_tokendef_to_variant(
                    variant, same_flags=False, same_arguments=False
                )
            else:
                top.set_tokendef_to_variant(
                    cql.IF_LOGICAL, same_flags=False, same_arguments=False
                )

        elif len(top.returntype) > 1:
            for returntype in top.children[-1].returntype:
                top.returntype = returntype
                break
        return top

    def _discard_token(self):
        return self.tokens[-1].pop(0)

    def _peek_token(self, index):
        return self.tokens[-1][index]

    @property
    def tokens_available(self):
        """Return the number of tokens not yet consumed."""
        return len(self.tokens[-1])

    def _consume_token(self, tokendef):
        self.cql_tokens_stack[-1].append((self.tokens[-1].pop(0), tokendef))

    @property
    def tokens_consumed(self):
        """Return the consumed tokens."""
        return len(self.cql_tokens_stack[-1])

    @property
    def most_recent_token_consumed(self):
        """Return the most recently consumed token."""
        return self.cql_tokens_stack[-1][-1]

    def get_filter_type_of_variable(self, variable_name):
        """Return the type (CQL) of variable name."""
        variable = self.variables[variable_name]
        return variable["type"]

    def process_statement(self, text):
        """Lex and parse the ChessQL statement."""
        # Assume no error, but set False indicating process_statement
        # has been called.
        self._error_information = False
        self._reset_state()
        self._statement_string = text
        self.lex()
        self.parse()

    def is_statement(self):
        """Return True if the statement has no errors."""
        return not self._error_information

    def abs(self, match, tokendef):
        """Add the CQL 'abs' filter."""
        assert tokendef is cql.Token.ABS
        self._insert_filter(match, tokendef)

    def all(self, match, tokendef):
        """Add 'all' parameter to 'find' filter.

        Multiple 'all' parameters are not allowed.

        The 'find' filter is converted from a position filter to a numeric
        filter.

        """
        assert tokendef is cql.Token.ALL
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_find_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        tns.set_tokendef_to_variant(cql.FIND_NUMERIC)
        self._add_filter_parameter(tokendef, tns)

    def ancestor(self, match, tokendef):
        """Add the CQL 'ancestor' filter.

        Matches 'ancestor (' and collapse_ancestor is called for the
        paired ')'.

        """
        assert tokendef is cql.Token.ANCESTOR
        self._insert_filter(match, tokendef)

    def collapse_ancestor(self, *args):
        """Add ')' for 'ancestor' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses()

    def and_(self, match, tokendef):
        """Add the CQL 'and' filter."""
        assert tokendef is cql.Token.AND
        self._insert_infix_boolean(match, tokendef)

    def anydirection(self, match, tokendef):
        """Add the CQL 'anydirection' filter."""
        assert tokendef is cql.Token.ANYDIRECTION
        self._insert_filter(match, tokendef)
        self._range = []

    def assign(self, match, tokendef):
        r"""Add the CQL '=\??' (assign) filter.

        '=' does the assignment unconditionally, but '=?' does not
        change an existing assignment.

        """
        assert tokendef is cql.Token.ASSIGN
        self._insert_infix_assign(match, tokendef)

    def attackedby(self, match, tokendef):
        """Add the CQL 'attackedby' filter."""
        assert tokendef is cql.Token.ATTACKEDBY
        self._insert_infix(match, tokendef)

    def attacks(self, match, tokendef):
        """Add the CQL 'attacks' filter."""
        assert tokendef is cql.Token.ATTACKS
        self._insert_infix(match, tokendef)

    # Called by methods associated with illegal tokens.  This includes legal
    # tokens which are always consumed by preceding legal tokens, for example
    # 'silent' a parameter for 'cql'.
    def _badtoken(self, match, tokendef):
        self.cql_error = "".join(
            (
                "Either unknown token or misplaced known token '",
                match.groupdict()[tokendef.name],
                "'",
            )
        )

    # Named 'z' rather than 'badtoken' as the name must sort high when creating
    # the full statement regular expression using the (?P<>) construct because
    # any word matches.
    def z(self, match, tokendef):
        """Add unrecognized CQL token.

        See # comment in module for reason method name is 'z'.

        """
        assert tokendef is cql.Token.BADTOKEN
        self._badtoken(match, tokendef)

    def between(self, match, tokendef):
        """Add the CQL 'between' filter.

        Matches 'between (' and collapse_between is called for the
        paired ')'.

        """
        assert tokendef is cql.Token.BETWEEN
        self._insert_filter(match, tokendef)

    def collapse_between(self, *args):
        """Add ')' for 'between' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses()

    def black(self, match, tokendef):
        """Add the CQL 'black' filter."""
        assert tokendef is cql.Token.BLACK
        self._insert_leaf_filter(match, tokendef)

    def blockcomment(self, match, tokendef):
        """Ignore the CQL <block comment> filter.

        <block comment is '/* <text> */'

        """
        assert tokendef is cql.Token.BLOCKCOMMENT
        del match
        self._discard_token()

    def btm(self, match, tokendef):
        """Add the CQL 'btm' filter."""
        assert tokendef is cql.Token.BTM
        self._insert_leaf_filter(match, tokendef)

    def capture(self, match, tokendef):
        """Add 'capture' parameter to 'move' filter.

        Multiple 'capture' parameters are allowed.  The 'capture' parameter
        is not allowed if the 'legal' or 'pseodolegal' parameter is also a
        parameter.

        The 'move' filter is converted from a logical filter to a set filter
        when 'capture' is the first parameter,

        """
        assert tokendef is cql.Token.CAPTURE
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._legal_or_pseudolegal_parameter_present(tokendef, tns):
            return
        if not tns.parameters:
            tns.set_tokendef_to_variant(cql.MOVE_SET)
        self._insert_filter(match, tokendef)
        self._add_filter_parameter(tokendef, tns, consume_token=False)
        if not self.tokens_available:
            self.cql_error = "".join(
                (
                    "Expecting filter as argument for '",
                    self.node_stack[-1].name.strip("_"),
                    "' parameter",
                )
            )

    def castle(self, match, tokendef):
        """Add 'castle' parameter to 'move' filter.

        The 'castle' parameter cannot be repeated.  Only one of the 'castle',
        'o-o', and 'o-o-o', parameters can be present.

        """
        assert tokendef is cql.Token.CASTLE
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        if self._multiple_castling_parameters(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def check(self, match, tokendef):
        """Add the CQL 'check' filter."""
        assert tokendef is cql.Token.CHECK
        self._insert_leaf_filter(match, tokendef)

    def child(self, match, tokendef):
        """Add the CQL 'child' filter.

        Matches 'child' or 'child (' and collapse_child is called for
        the paired ')'if needed.

        """
        assert tokendef is cql.Token.CHILD
        if len(match.group().split()) == 1:
            self._insert_leaf_filter(match, tokendef)
            self.node_stack[-1].set_tokendef_to_variant(
                cql.CHILD_NO_ARGUMENT, same_flags=False, same_arguments=False
            )
            return
        self._insert_filter(match, tokendef)

    def collapse_child(self, *args):
        """Add ')' for 'child' filter if filter is like 'child ( ... )'.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses(argument_count=1)

    def colon(self, match, tokendef):
        """Add ':' operator.

        The : operator has the form 'position : filter' where position is a
        'position filter' and filter is any 'filter'.  The CQL version 6 parser
        accepts a literal number as a filter, but evaluation rejects it.

        """
        assert tokendef is cql.Token.COLON
        self._insert_infix_colon(match, tokendef)

    def colortype(self, match, tokendef):
        """Add the CQL 'colortype' filter."""
        assert tokendef is cql.Token.COLORTYPE
        self._insert_filter(match, tokendef)

    def comment(self, match, tokendef):
        """Add 'comment' as parameter to 'move' filter or as statement filter.

        The comment keyword indicates a move parameter when it is preceded by
        a move parameter or the move filter keyword.  A comment parameter is
        the last parameter of a move filter.  It is not possible to attempt to
        specify a comment parameter to a move filter more than once: in
        'move comment "one" comment "two"'
        the second comment keyword indicates a comment filter.

        """
        assert tokendef is cql.Token.COMMENT
        node_stack = self.node_stack
        tns = node_stack[-1]
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 1:
            node_stack[-1].set_tokendef_to_variant(
                cql.SINGLE_COMMENT_ARGUMENT, same_flags=False
            )
        if tns.tokendef is cql.Token.MOVE or tns.tokendef is cql.MOVE_SET:
            child = node_stack[-2].children.pop()
            node_stack[-2].children[-1].children.append(child)

    def collapse_comment(self, *args):
        """Add ')' for 'comment' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses(argument_count=None, minimum_arguments=1)

    def connectedpawns(self, match, tokendef):
        """Add the CQL 'connectedpawns' filter."""
        assert tokendef is cql.Token.CONNECTEDPAWNS
        self._insert_leaf_filter(match, tokendef)

    # A 'runtime' error occurs in cql.exe if the consecutivemoves filter is run
    # while the variables are undeclared.  The difference is seen with the
    # -parse option to cql at CQL version 6.0.4.
    # Assume variables will be declared later.  A syntax error, not a runtime
    # error, occurs if the variables are not declared as position variables.
    # The runtime error still occurs if the variables are declared as position
    # variables: 'consecutivemoves(x y) x=parent y=child' for example.
    # It looks safe to let consecutivemoves(x y) put position variables in
    # self.variables if they are not already present. (User defined functions?)
    def consecutivemoves(self, match, tokendef):
        """Add the CQL 'consecutivemoves' filter."""
        assert tokendef is cql.Token.CONSECUTIVEMOVES
        if self.node_stack[-1].tokendef is cql.Token.CONSECUTIVEMOVES:
            self._badtoken(match, tokendef)
            return
        self._insert_filter(match, tokendef)
        self._range = []

    def collapse_consecutivemoves_leftparenthesis(self, *args):
        """Complete the 'consecutivemoves' filter.

        Called when token is not a 'consecutivemoves' parameter after
        'consecutivemoves' filter.

        """
        del args
        self._close_parentheses()

    def count(self, match, tokendef):
        """Add 'count' parameter to 'move' filter.

        'count' is allowed in the presence of the 'legal' or 'pseudolegal'
        parameters.  Validation is postponned till all the parameters to this
        move filter have been collected.

        Multiple 'count' parameters are allowed.

        """
        assert tokendef is cql.Token.COUNT
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def cql(self, match, tokendef):
        """Add the CQL 'cql' filter."""
        assert tokendef is cql.Token.CQL
        if self.tokens_consumed:
            self.cql_error = "".join(
                ("The 'cql' keyword is only allowed at start of statement",)
            )
            return
        cql_name, cql_parameters = (
            match.groupdict()[cql.Token.CQL.name]
            .split(maxsplit=1)[-1]
            .split("(", 1)
        )
        if len(cql_parameters.split(")")) == 1:
            self.cql_error = "".join(
                (
                    "The ",
                    cql_name,
                    " keyword must have parenthesized parameters, ",
                    "even if empty like '()'",
                )
            )
            return
        self.node_stack.append(self.create_node(tokendef))
        self._consume_token(tokendef)

    def currentposition(self, match, tokendef):
        """Add the CQL 'currentposition' filter."""
        assert tokendef is cql.Token.CURRENTPOSITION
        self._insert_leaf_filter(match, tokendef)

    def dark(self, match, tokendef):
        """Add the CQL 'dark' filter."""
        assert tokendef is cql.Token.DARK
        self._insert_filter(match, tokendef)

    def depth(self, match, tokendef):
        """Add the CQL 'depth' filter."""
        assert tokendef is cql.Token.DEPTH
        self._insert_leaf_filter(match, tokendef)

    def descendant(self, match, tokendef):
        """Add the CQL 'descendant' filter.

        Matches 'descendant (' and collapse_descendant is called for the
        paired ')'.

        """
        assert tokendef is cql.Token.DESCENDANT
        self._insert_filter(match, tokendef)

    def collapse_descendant(self, *args):
        """Add ')' for 'descedant' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses()

    def diagonal(self, match, tokendef):
        """Add the CQL 'diagonal' filter."""
        assert tokendef is cql.Token.DIAGONAL
        self._insert_filter(match, tokendef)
        self._range = []

    def distance(self, match, tokendef):
        """Add the CQL 'distance' filter.

        Matches 'distance (' and collapse_distance is called for the
        paired ')'.

        """
        assert tokendef is cql.Token.DISTANCE
        self._insert_filter(match, tokendef)

    def collapse_distance(self, *args):
        """Add ')' for 'distance' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses()

    def divide(self, match, tokendef):
        """Add the CQL '/' (divide) filter."""
        assert tokendef is cql.Token.DIVIDE
        self._insert_infix_arithmetic(match, tokendef)

    def dot(self, match, tokendef):
        """Add the CQL '.' (dot) filter."""
        assert tokendef is cql.Token.DOT
        self._insert_leaf_filter(match, tokendef)

    def doubledpawns(self, match, tokendef):
        """Add the CQL 'doubledpawns' filter."""
        assert tokendef is cql.Token.DOUBLEDPAWNS
        self._insert_leaf_filter(match, tokendef)

    def down(self, match, tokendef):
        """Add the CQL 'down' filter."""
        assert tokendef is cql.Token.DOWN
        self._insert_filter(match, tokendef)
        self._range = []

    def echo(self, match, tokendef):
        """Add the CQL 'echo' filter."""
        assert tokendef is cql.Token.ECHO
        self._insert_filter(match, tokendef)
        words = match.group().split()
        for name in words[2], words[3]:
            if name.startswith(cql.CQL_RESERVED_VARIABLE_NAME_PREFIX):
                self.cql_error = "".join(
                    (
                        "Variable name '",
                        name,
                        "' starts with reserved sequence '",
                        cql.CQL_RESERVED_VARIABLE_NAME_PREFIX,
                        "' in '",
                        tokendef.name,
                        "' filter",
                    )
                )
                return
            if (
                name in self.variables
                and self.variables[name]
                is not cql.TokenTypes.POSITION_VARIABLE
            ):
                self.cql_error = "".join(
                    (
                        "Variable name '",
                        name,
                        "' exists but is not a ",
                        cql.TokenTypes.POSITION_VARIABLE.value,
                        "' in '",
                        tokendef.name,
                        "' filter",
                    )
                )
                return
            variable = re.match(cql.CQL_PATTERN, name)
            if variable is None:
                self.cql_error = "".join(
                    (
                        "'",
                        name,
                        "' is not allowed as a ",
                        cql.TokenTypes.POSITION_VARIABLE.value,
                        "' in '",
                        tokendef.name,
                        "' filter",
                    )
                )
                return
            if variable.groupdict()["y"] is None:
                self.cql_error = "".join(
                    (
                        "'",
                        name,
                        "' is not allowed as a ",
                        cql.TokenTypes.POSITION_VARIABLE.value,
                        "' in '",
                        tokendef.name,
                        "' filter",
                    )
                )
                return
            if name not in self.variables:
                self.variables[name] = {"type": cql.POSITION_VARIABLE}
            node_stack = self.node_stack
            child = node_stack[-1].children
            child.append(self.create_node(cql.POSITION_VARIABLE, leaf=name))

            # Note following pop.
            self._append_node_to_node_stack(child[-1])
            self.node_stack.pop().set_tokendef_to_variant(
                self.get_filter_type_of_variable(name)
            )

        # 'in all' clause present.
        if len(words) == 7:
            self.node_stack[-1].set_tokendef_to_variant(cql.ECHO_IN_ALL)

    def elo(self, match, tokendef):
        """Add the CQL 'elo' filter."""
        assert tokendef is cql.Token.ELO
        self._insert_leaf_filter(match, tokendef)
        words = match.group().split()
        if len(words) > 1:
            if words[1] == cql.ELO_BLACK.pattern:
                self.node_stack[-1].set_tokendef_to_variant(cql.ELO_BLACK)
            elif words[1] == cql.ELO_WHITE.pattern:
                self.node_stack[-1].set_tokendef_to_variant(cql.ELO_WHITE)

    def leftbrace(self, match, tokendef):
        """Add the CQL '{' (compound) filter.

        '{' starts a compound filter.  A matching '}' completes the
        filter.

        Compound filters are sometimes used to override the default
        precedence of filters.

        """
        assert tokendef is cql.Token.LEFTBRACE
        self._insert_filter(match, tokendef)

    def collapse_leftbrace(self):
        """Add '}' for '{' token.

        Called by self.rightbrace for the relevant '}' token.

        """
        clbns = self.node_stack[-1]
        self._consume_token(cql.Token.RIGHTBRACE)
        self._pop_top_stack(self.node_stack)
        if len(clbns.children) == 0:
            self.cql_error = "Empty compound filter found"
            return
        for child in clbns.children:
            if (
                child.tokendef is cql.Token.NUMBER
                or child.tokendef is cql.NUMERIC_VARIABLE
            ):
                self.cql_error = "".join(
                    (
                        "Literal numbers and numeric variables are not ",
                        "accepted in compound filters",
                    )
                )
                return
        variant = cql.map_filter_type_to_leftbrace_type.get(
            clbns.children[-1].returntype
        )
        if variant is None:
            self.cql_error = "".join(
                ("Unable to set filter type for compound filter'",)
            )
            return
        clbns.set_tokendef_to_variant(
            variant, same_flags=False, same_arguments=False
        )

        # Same as _insert_filter version except clbns.tokendef for tokendef.
        tns = self.node_stack[-1]
        if tns.tokendef is cql.Token.ASSIGN and len(clbns.returntype) == 1:
            variable_name = tns.children[0].leaf
            variable = self.variables.get(variable_name)
            if variable is None:
                self.cql_error = "".join(
                    (
                        "Variable '",
                        variable_name,
                        "' is not defined so it's type cannot be set",
                    )
                )
                return
            type_ = cql.map_filter_assign_to_variable.get(clbns.returntype)
            if type_:
                variable_type = variable["type"]
                if cql.TokenTypes.UNSET_VARIABLE in variable_type.returntype:
                    variable["type"] = type_
                    tns.children[0].tokendef = type_
                elif variable_type is not type_:
                    self.cql_error = "".join(
                        (
                            "Variable '",
                            variable_name,
                            "' is a '",
                            tns.children[0].name,
                            "' but assigned filter is a '",
                            self.create_node(clbns.tokendef).name,
                            "'",
                        )
                    )
                    return

        self._append_node_to_node_stack(clbns)

    # At present collapse_leftbrace() ignores stacked_arguments.
    def rightbrace(self, match, tokendef):
        """End the compound filter started by the matching leftbrace.

        There is one kind of compound filter, started by a bare leftbrace, so
        a set of collapse_* methods is not needed like with parentheses, but
        collapse_leftbrace defined for familiarity.

        From CQL version 6 documentation:
        The value of a compound filter is the value (if any) of its last
        filter, one of set, position, or numeric.  It is assumed a compound
        filter can be a logical filter because '{true}' is accepted and
        'w={true}' is rejected by -parse option saying rhs must be a set,
        countable, or position, filter.

        """
        assert tokendef is cql.Token.RIGHTBRACE
        del match
        stacked_arguments = []
        node_stack = self.node_stack
        while True:
            if not node_stack:
                self.cql_error = "".join(("Unmatched '}'",))
                return
            if (
                cql.Flags.PARENTHESIZED_ARGUMENTS
                not in node_stack[-1].tokendef.flags
            ):
                stacked_arguments.append(self._pop_top_stack(node_stack))
                continue
            getattr(self, "collapse_" + node_stack[-1].name)()
            break

    def leftparenthesis(self, match, tokendef):
        """Add '(' to filter.

        A '(' following a filter which does not have arguments enclosed in a
        '()' pair accepts a lone filter or an arithemitic expression composed
        with numeric filters. 'shift {k q r}' counts as a lone filter because
        'shift' takes a single filter as it's argument. 'pin from (q)' is an
        example with a parameter which takes an argument.

        The '()' pair following a filter which has arguments in parentheses
        contains a list of filters.  <filter>(<filter list>) generates a
        filter from <filter list> by rules defined for <filter>.

        '{(<filter list>)', if it were legal to write this, could be seen as
        equivalent to '{<filter list>}', where the bare '{' generates it's
        filter by anding the values of the filters in <filter list>.

        """
        assert tokendef is cql.Token.LEFTPARENTHESIS
        tns = self.node_stack[-1]
        left_tokendef = cql.map_filter_to_leftparenthesis.get(tns.tokendef)
        if left_tokendef:
            tns.tokendef = left_tokendef
            self._consume_token(tokendef)
        else:
            self._insert_filter(match, tokendef)

    def collapse_leftparenthesis(self, *args):
        """Add ')' for '(' token.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        clpns = self.node_stack[-1]
        self._consume_token(cql.Token.RIGHTPARENTHESIS)
        self._pop_top_stack(self.node_stack)
        if len(clpns.children) == 0:
            self.cql_error = "Empty parenthesized expression found"
            return
        if len(clpns.children) != 1:
            self.cql_error = "".join(
                ("Parenthesized expression contains more than one filter")
            )
            return
        clpns.set_tokendef_to_variant(
            cql.map_filter_type_to_leftparenthesis_type[
                clpns.children[0].returntype
            ],
            same_flags=False,
            same_arguments=False,
        )

        # Same as _insert_filter version except clpns.tokendef for tokendef.
        tns = self.node_stack[-1]
        if tns.tokendef is cql.Token.ASSIGN and len(clpns.returntype) == 1:
            variable_name = tns.children[0].leaf
            variable = self.variables.get(variable_name)
            if variable is None:
                self.cql_error = "".join(
                    (
                        "Variable '",
                        variable_name,
                        "' is not defined so it's type cannot be set",
                    )
                )
                return
            type_ = cql.map_filter_assign_to_variable.get(clpns.returntype)
            if type_:
                variable_type = variable["type"]
                if cql.TokenTypes.UNSET_VARIABLE in variable_type.returntype:
                    variable["type"] = type_
                    tns.children[0].tokendef = type_
                elif variable_type is not type_:
                    self.cql_error = "".join(
                        (
                            "Variable '",
                            variable_name,
                            "' is a '",
                            tns.children[0].name,
                            "' but assigned filter is a '",
                            self.create_node(clpns.tokendef).name,
                            "'",
                        )
                    )
                    return

        self._append_node_to_node_stack(clpns)

    # At present collapse_leftparenthesis() ignores stacked_arguments.
    def rightparenthesis(self, match, tokendef):
        """Add ')' to complete a comound filter started with '('."""
        assert tokendef is cql.Token.RIGHTPARENTHESIS
        del match
        stacked_arguments = []
        node_stack = self.node_stack
        while True:
            if not node_stack:
                self.cql_error = "Empty node stack"
                break
            if (
                cql.Flags.PARENTHESIZED_ARGUMENTS
                not in node_stack[-1].tokendef.flags
            ):
                stacked_arguments.append(self._pop_top_stack(node_stack))
                continue
            getattr(self, "collapse_" + node_stack[-1].name)(stacked_arguments)
            break

    def enpassant(self, match, tokendef):
        """Add 'enpassant' parameter to 'move' filter.

        The 'enpassant' parameter cannot be repeated.  Only one of the
        'enpassant' and 'enpassantsquare' parameters can be present.  The
        'enpassant' parameter is not allowed if the 'null' or 'promote'
        parameter is also a parameter.

        """
        assert tokendef is cql.Token.ENPASSANT
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        if self._multiple_enpassant_parameters(tokendef, tns):
            return
        if self._null_or_promote_parameter_present(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def enpassantsquare(self, match, tokendef):
        """Add 'enpassantsquare' parameter to 'move' filter.

        The 'enpassantsquare' parameter cannot be repeated.  Only one of the
        'enpassant' and 'enpassantsquare' parameters can be present.  The
        'enpassantsquare' parameter is not allowed if the 'null' or 'promote'
        parameter is also a parameter.

        """
        assert tokendef is cql.Token.ENPASSANT_SQUARE
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        if self._multiple_enpassant_parameters(tokendef, tns):
            return
        if self._null_or_promote_parameter_present(tokendef, tns):
            return
        self._insert_filter(match, tokendef)
        self._add_filter_parameter(tokendef, tns, consume_token=False)
        if not self.tokens_available:
            self.cql_error = "".join(
                (
                    "Expecting filter as argument for '",
                    self.node_stack[-1].name.strip("_"),
                    "' parameter",
                )
            )

    def eolcomment(self, match, tokendef):
        """Add the CQL 'eolcomment' filter."""
        assert tokendef is cql.Token.EOLCOMMENT
        del match
        self._discard_token()

    def eq(self, match, tokendef):
        """Add the CQL '==' (equal) filter."""
        assert tokendef is cql.Token.EQ
        self._insert_infix_relational(match, tokendef)
        self._adjust_infix_relational_tokendef(cql.EQ_SET, cql.EQ_POSITION)

    def event(self, match, tokendef):
        """Add the CQL 'event' filter."""
        assert tokendef is cql.Token.EVENT
        self._insert_leaf_filter(match, tokendef)
        self.node_stack[-1].leaf = match.group().split(maxsplit=1)[-1]

    def false(self, match, tokendef):
        """Add the CQL 'false' filter."""
        assert tokendef is cql.Token.FALSE
        self._insert_leaf_filter(match, tokendef)

    def fen(self, match, tokendef):
        """Add the CQL 'fen' filter."""
        assert tokendef is cql.Token.FEN
        self._insert_leaf_filter(match, tokendef)
        self.node_stack[-1].leaf = match.group().split(maxsplit=1)[-1]

    def file(self, match, tokendef):
        """Add the CQL 'file' filter."""
        assert tokendef is cql.Token.FILE
        self._insert_filter(match, tokendef)

    def find(self, match, tokendef):
        """Add the CQL 'find' filter."""
        assert tokendef is cql.Token.FIND
        self._insert_filter(match, tokendef)

    def firstmatch(self, match, tokendef):
        """Add 'firstmatch' parameter to 'line' filter.

        Multiple 'firstmatch' parameters are not allowed.

        """
        del match
        assert tokendef is cql.Token.FIRSTMATCH
        tns = self.node_stack[-1]
        if not self._accept_as_line_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def flip(self, match, tokendef):
        """Add the CQL 'flip' filter."""
        assert tokendef is cql.Token.FLIP
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(cql.FLIP_COUNT)

    def flipcolor(self, match, tokendef):
        """Add the CQL 'flipcolor' filter."""
        assert tokendef is cql.Token.FLIPCOLOR
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(cql.FLIPCOLOR_COUNT)

    def fliphorizontal(self, match, tokendef):
        """Add the CQL 'fliphorizontal' filter."""
        assert tokendef is cql.Token.FLIPHORIZONTAL
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(
                cql.FLIPHORIZONTAL_COUNT
            )

    def flipvertical(self, match, tokendef):
        """Add the CQL 'flipvertical' filter."""
        assert tokendef is cql.Token.FLIPVERTICAL
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(cql.FLIPVERTICAL_COUNT)

    def from_(self, match, tokendef):
        """Add from parameter to move or pin filter.

        The 'from' parameter cannot be repeated.

        The 'move' filter is converted from a logical filter to a set filter
        when 'from' is the first parameter,

        """
        assert tokendef is cql.Token.FROM
        tns = self.node_stack[-1]
        if not self._accept_as_move_or_pin_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        if tns.tokendef is cql.Token.MOVE:
            if not tns.children and not tns.parameters:
                tns.set_tokendef_to_variant(cql.MOVE_SET)
        self._insert_filter(match, tokendef)
        self._add_filter_parameter(tokendef, tns, consume_token=False)
        if not self.tokens_available:
            self.cql_error = "".join(
                (
                    "Expecting filter as argument for '",
                    self.node_stack[-1].name.strip("_"),
                    "' parameter",
                )
            )

    # 'y=currentposition function z(y){shift y} z(y)' is accepted by -parse
    # but is rejected as a likely error when evaluated by CQL version 6.0.4.
    # With z(k) instead of z(y) the evaluation succeeds.
    # 'x=r y=currentposition function z(y){shift y x=1} z(y)' is rejected by
    # -parse at x=1 because x is a set variable, and
    # 'y=currentposition function z(y){shift y x=1} z(y) x=r' is rejected by
    # -parse at x=r because x is a numeric variable.  The rejection reason is
    # not stated as such, but the earlier assignment implies the reason given,
    # together with the acceptance of
    # 'y=currentposition function z(y){shift y x=1} x=r' where 'x=1' is not
    # evaluated because z is never called.
    def function(self, match, tokendef):
        """Collect formal parameters and function body tokens.

        CQL 6.0.4 documentation for the 'function' filter states:

        '
        Invocation of a function is performed as follows:

        1. For each actual argument z of the function call:
            If z is a variable then the corresponding variable of z is z
            Otherwise, z is assigned to a new, unique variable Z which is
            clled the corresponding variable for z.
        2. The body of the function is modified as follows: each occurrence of
            a formal parameter w in the body corresponding to an argument z of
            the function call is renamed to be the corresponding variable for z
        3. The modified body of the function is evaluated in place of the
            function call
        '

        The example given suggests reserved variable names, starting '__CQL',
        are used as Z names although 'CQL_var_1' and 'CQL_var_2' are the actual
        names in the example.

        Matches 'function (<variable name1> ...) {' and collapse_function
        is called.

        """
        assert tokendef is cql.Token.FUNCTION
        function_name, function_parameters = (
            match.groupdict()[cql.Token.FUNCTION.name]
            .split(maxsplit=1)[-1]
            .split("(", 1)
        )
        function_parameters = function_parameters.split(")")[0].split()
        if function_name.startswith(cql.CQL_RESERVED_VARIABLE_NAME_PREFIX):
            self.cql_error = "".join(
                (
                    "Function name '",
                    function_name,
                    "' starts with reserved sequence '",
                    cql.CQL_RESERVED_VARIABLE_NAME_PREFIX,
                    "' in '",
                    tokendef.name,
                    "' filter",
                )
            )
            return
        if function_name in self.variables:
            self.cql_error = "".join(
                (
                    "Variable name '",
                    function_name,
                    "' exists already and cannot be name of a new function",
                )
            )
            return
        fn_match = re.match(cql.CQL_PATTERN, function_name)
        if fn_match.groupdict()[cql.Token.VARIABLE.name] is None:
            self.cql_error = "".join(
                ("'", function_name, "' cannot be name of a function")
            )
            return
        parameters = []
        for name in function_parameters:
            if name.startswith(cql.CQL_RESERVED_VARIABLE_NAME_PREFIX):
                self.cql_error = "".join(
                    (
                        "Parameter name '",
                        name,
                        "' starts with reserved sequence '",
                        cql.CQL_RESERVED_VARIABLE_NAME_PREFIX,
                        "' in '",
                        tokendef.name,
                        "' filter",
                    )
                )
                return
            if name in parameters:
                self.cql_error = "".join(
                    (
                        "Parameter name '",
                        name,
                        "' exists already and cannot be name of ",
                        "another parameter in function '",
                        function_name,
                        "'",
                    )
                )
                return
            fn_match = re.match(cql.CQL_PATTERN, name)
            if fn_match.groupdict()[cql.Token.VARIABLE.name] is None:
                self.cql_error = "".join(
                    ("'", name, "' cannot be name of a function parameter")
                )
                return
            parameters.append(name)
        self.variables[function_name] = {
            "type": cql.Token.FUNCTION,
            "parameters": tuple(parameters),
        }

        # Strictly it is not necessary to put the function definition on the
        # node stack, but doing so makes the definition visible in traces.
        # Function detail is held and displayed in variables trace so function
        # definition is removed from stack when '}' closing body found.
        self._insert_filter(match, tokendef)
        self.node_stack[-1].parameters[cql.Token.FUNCTION] = parameters
        self.node_stack[-1].leaf = function_name

        function_body = ["{"]
        brace_stack = []
        while self.tokens_available:
            match = self._peek_token(0)
            groupkey = "".join(
                k
                for k, v in match.groupdict().items()
                if v is not None and ("_" not in k[:-1])
            )
            token_definition = cql.CQL_TOKENS[groupkey]
            if token_definition is cql.Token.LEFTBRACE:
                brace_stack.append((match, token_definition))
            elif token_definition is cql.Token.RIGHTBRACE:
                if not brace_stack:
                    self.variables[function_name]["body"] = function_body
                    break
                brace_stack.pop()
            function_body.append(match.group())
            self._consume_token(token_definition)

    # Node for 'function' has it's name in the leaf attribute but it is not
    # processed as a leaf node, by calling _insert_leaf_node, because textual
    # substitution when calling the function is needed.
    # Do self.node_stack.pop() rather than call self._pop_top_stack(...).
    def collapse_function(self):
        """Add '}' for 'function' filter definition.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        self._consume_token(cql.Token.RIGHTBRACE)
        variable = self.variables[self.node_stack.pop().leaf]
        del self.node_stack[-1].children[-1]
        variable["body"].append("}")
        variable["body"] = tuple(w.strip() for w in variable["body"])

    # There is not a 'function_call' method because function names are a subset
    # of variable names.
    def collapse_function_call(self, *args):
        """Add ')' for <function name> function call.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._consume_token(cql.Token.RIGHTPARENTHESIS)
        top = self._pop_top_stack(self.node_stack)
        child = top.children
        function_name = child[0].leaf
        if len(child) - 1 != len(self.variables[function_name]["parameters"]):
            self.cql_error = "".join(
                (
                    "Function '",
                    child[0].leaf,
                    "' takes ",
                    str(len(self.variables[function_name]["parameters"])),
                    " arguments but ",
                    str(len(child) - 1),
                    " were given",
                )
            )
            return

        # Replace the formal parameters in the function definition body by the
        # actual parameters in the function call.  The constructed compound
        # filter is appended to the children attribute of the function call
        # node.  The constructed compound filter could replace the function
        # call node but is not so the function call is visible in traces.
        # Evaluation code must evaluate just the final child node of a function
        # call node.
        # The example definition 'function sets_smaller(x y){#x<#y)' expands to
        # '{__CQL_0_x=[Qq] __CQL_1_y=[Rr] {#__CQL_0_x<#__CQL_1_y}}' given the
        # call 'sets_smaller ([Qq] [Rr])'.  The actual variables in CQL version
        # 6.0.4 may be CQL-0-x and so forth given the parsing error produced by
        # 'function c ( x ) { k } c ( true )' complaining about the actual
        # argument 'true': the otherwise illegal names avoid name clashes.
        # Also '__CQL' names seem to be reserved by convention rather than by
        # an enforced rule.  It is safe to use __CQL names as corresponding
        # variables because the data structures generated here do not get
        # evaluated by CQL version 6.0.4.
        # The function body is extended to '{<variable definitions>{<body>}}'.
        substitutions = {}
        local_variables = []
        parameters = self.variables[function_name]["parameters"]
        for item, node in enumerate(child[1:]):
            if node.tokendef in cql.ASSIGNMENT_VARIABLE_TYPES:
                substitutions[parameters[item]] = node.leaf
            else:
                substitutions[parameters[item]] = "_".join(
                    (
                        cql.CQL_RESERVED_VARIABLE_NAME_PREFIX,
                        str(self._formal_parameter_number),
                        parameters[item],
                    )
                )
                local_variables.append(
                    (substitutions[parameters[item]], child[item + 1])
                )
                self._formal_parameter_number += 1
        body = [
            substitutions.get(node, node)
            for node in self.variables[function_name]["body"]
        ]

        # Create variable assignment structures.
        # 'v = 1' is '(assign, [(numeric_variable, v), (x, 1)])'.
        # 'v = k' is '(assign, [(set_variable, v), (piece_designator, k)])'
        # 'piece v = k' is
        # '(pieceassignment, [(piece_variable, v), (piece_designator, k)])'
        # 'v = parent' is
        # 'assign, [(position_variable, v), (parent, parent)])'
        # Append entries to node_stack and cql_tokens for constructed '{ v = ?'
        # statement start, and process the modified function body plus the '}'
        # matching the '{' in '{ v = ?'.
        # Implication is filters like 'true' cannot be actual arguments.
        self.tokens.append(re.finditer(cql.CQL_PATTERN, " ".join(body)))
        self.cql_tokens_stack.append([])
        top.tokendef = cql.Token.LEFTBRACE
        top.parameters[top.children[0].tokendef] = function_name
        if local_variables:
            self.node_stack.append(self.node_stack[-1].children[-1])
            top.children = [
                self.create_node(cql.Token.LEFTBRACE, children=top.children)
            ]
            body.append("}")
        for item, local_variable in enumerate(local_variables):
            lvname, apnode = local_variable
            lvtype = cql.map_filter_assign_to_variable.get(apnode.returntype)
            if lvtype is None:
                self.cql_error = "".join(
                    (
                        "Invalid argument type for corresponding variable '",
                        lvname,
                        "'",
                    )
                )
                break
            top.children.insert(
                item,
                self.create_node(
                    cql.Token.ASSIGN,
                    children=[self.create_node(lvtype, leaf=lvname), apnode],
                ),
            )
            self.variables[lvname] = {"persistent": False, "type": lvtype}
        if local_variables:
            top.children[-1].children.clear()
        else:
            top.children.clear()
        self.node_stack.append(self.node_stack[-1].children[-1])

        # Parse the function body.  The leading '{' must be ignored because a
        # '{' has already been put on node stack.  The second '{' has to be
        # fitted manually to the correct leftbrace variant, so there may be no
        # point in mimicking the stack structure for '{ ... {' above.
        # Cannot call parse() because it assumes cql parameters must be present
        # or defaulted.
        # Attempts to define functions within the body of a function fail here,
        # but succeed in CQL version 6.0.4 only to meet a syntax error if the
        # enclosing function is called more than once because the function name
        # is being defined more than once.  Although the error messages do not
        # indicate the problem the code is left as it is for now.
        self._consume_token(cql.Token.LEFTBRACE)
        while len(self.tokens[-1]):
            match = self.tokens[-1][0]
            groupkey = "".join(
                k
                for k, v in match.groupdict().items()
                if v is not None and ("_" not in k[:-1])
            )
            self._process_token(match, groupkey)
            if self._error_information and self._error_information.error_found:
                break
        if local_variables:
            self.node_stack[-2].tokendef = self.node_stack[-1].tokendef
        self._collapse_stack_frame(cql.Flags.STATEMENT_FRAME)

        # Finally remove function name from called functions and the function
        # token stacks.
        for lvname, apnode in local_variables:
            del self.variables[lvname]
        self.tokens.pop()
        self.cql_tokens_stack.pop()
        self._called_functions.remove(function_name)

    def gamenumber(self, match, tokendef):
        """Add the CQL 'gamenumber' filter."""
        assert tokendef is cql.Token.GAMENUMBER
        self._insert_leaf_filter(match, tokendef)

    def ge(self, match, tokendef):
        """Add the CQL '>=' (greater than or equal to) filter."""
        assert tokendef is cql.Token.GE
        self._insert_infix_relational(match, tokendef)
        self._adjust_infix_relational_tokendef(cql.GE_SET, cql.GE_POSITION)

    def gt(self, match, tokendef):
        """Add the CQL '>' (greater than) filter."""
        assert tokendef is cql.Token.GT
        self._insert_infix_relational(match, tokendef)
        self._adjust_infix_relational_tokendef(cql.GT_SET, cql.GT_POSITION)

    def hascomment(self, match, tokendef):
        """Add the CQL 'hascomment' filter."""
        assert tokendef is cql.Token.HASCOMMENT
        self._insert_leaf_filter(match, tokendef)
        self.node_stack[-1].leaf = match.group().split(maxsplit=1)[-1]

    def hash(self, match, tokendef):
        """Add the CQL '#' (hash) filter."""
        assert tokendef is cql.Token.HASH
        self._insert_filter(match, tokendef)

    def horizontal(self, match, tokendef):
        """Add the CQL 'horizontal' filter."""
        assert tokendef is cql.Token.HORIZONTAL
        self._insert_filter(match, tokendef)
        self._range = []

    def in_(self, match, tokendef):
        """Add the CQL 'in' filter."""
        assert tokendef is cql.Token.IN
        self._insert_infix(match, tokendef)

    def initial(self, match, tokendef):
        """Add the CQL 'initial' filter."""
        assert tokendef is cql.Token.INITIAL
        self._insert_leaf_filter(match, tokendef)

    def input_(self, match, tokendef):
        """Add the CQL 'input' parameter."""
        assert tokendef is cql.Token.INPUT
        self._badtoken(match, tokendef)

    def intersection(self, match, tokendef):
        """Add the CQL '&' (intersection) filter."""
        assert tokendef is cql.Token.INTERSECTION
        self._insert_infix_binary(match, tokendef)
        if self.cql_error:
            return
        tns = self.node_stack[-1]
        lhsrt = tns.children[0].returntype
        if cql.TokenTypes.POSITION_FILTER in lhsrt:
            tns.set_tokendef_to_variant(
                cql.INTERSECTION_POSITION,
                same_returntype=True,
                same_arguments=False,
            )
        elif cql.TokenTypes.SET_FILTER in lhsrt:
            tns.set_tokendef_to_variant(
                cql.INTERSECTION_SET,
                same_returntype=True,
                same_arguments=False,
            )
        else:
            self.cql_error = "".join(
                (
                    "Left argument for '",
                    tokendef.name,
                    "' filter must be a '",
                    cql.TokenTypes.POSITION_FILTER.value,
                    "' or '",
                    cql.TokenTypes.SET_FILTER.value,
                    "' filter",
                )
            )

    def ipdivide(self, match, tokendef):
        """Add the CQL '%=' (in-place divide) filter."""
        assert tokendef is cql.Token.IPDIVIDE
        self._insert_infix_arithmetic_inplace(match, tokendef)

    def ipminus(self, match, tokendef):
        """Add the CQL '-=' (in-place minus) filter."""
        assert tokendef is cql.Token.IPMINUS
        self._insert_infix_arithmetic_inplace(match, tokendef)

    def ipmodulus(self, match, tokendef):
        """Add the CQL '%=' (in-place modulus) filter."""
        assert tokendef is cql.Token.IPMODULUS
        self._insert_infix_arithmetic_inplace(match, tokendef)

    def ipmultiply(self, match, tokendef):
        """Add the CQL '*=' (in-place multiply) filter."""
        assert tokendef is cql.Token.IPMULTIPLY
        self._insert_infix_arithmetic_inplace(match, tokendef)

    def ipplus(self, match, tokendef):
        """Add the CQL '+='(in-place plus) filter."""
        assert tokendef is cql.Token.IPPLUS
        self._insert_infix_arithmetic_inplace(match, tokendef)

    def isolatedpawns(self, match, tokendef):
        """Add the CQL 'isolatedpawns' filter."""
        assert tokendef is cql.Token.ISOLATEDPAWNS
        self._insert_leaf_filter(match, tokendef)

    def lastposition(self, match, tokendef):
        """Add 'lastposition' parameter to 'line' filter.

        Multiple 'lastposition' parameters are allowed.

        """
        assert tokendef is cql.Token.LASTPOSITION
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_line_parameter(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def lca(self, match, tokendef):
        """Add the CQL 'lca' filter.

        Matches 'lca (' and collapse_lca is called for the paired ')'.

        """
        assert tokendef is cql.Token.LCA
        self._insert_filter(match, tokendef)

    def collapse_lca(self, *args):
        """Add ')' for 'lca' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses()

    def left(self, match, tokendef):
        """Add the CQL 'left' filter."""
        assert tokendef is cql.Token.LEFT
        self._insert_filter(match, tokendef)
        self._range = []

    def leftarrow(self, match, tokendef):
        """Add '<--' parameter to 'find' or 'line' filters.

        The '<--' parameter must be the first parameter of the 'find' filter
        if present.  The same would happen for the 'find_numeric' filter, but
        the conversion from 'find' to 'find_numeric' is triggered by the 'all'
        and 'range' parameters, the only other parameters available in 'find'.
        So 'find all <--' reports an illegal parameter, not a misplaced one.

        The first use of the '<--' or '-->' parameters in a 'line' filter
        restricts it's later parameters to be that '<--' or '-->'.

        """
        assert tokendef is cql.Token.LEFTARROW
        self._collapse_stack_frame(cql.Flags.LINE_FRAME)
        tns = self.node_stack[-1]
        if not self._accept_as_find_or_line_parameter(tokendef, tns):
            return
        if tns.tokendef is cql.Token.FIND or tns.tokendef is cql.FIND_NUMERIC:
            if tns.parameters:
                self.cql_error = "".join(
                    (
                        "Parameter '",
                        tokendef.name,
                        "' can only be first parameter in '",
                        tns.name,
                        "' filter",
                    )
                )
                return
            self._add_filter_parameter(tokendef, tns)
        elif tns.tokendef is cql.Token.LINE:
            self._insert_filter(match, tokendef)
            self._add_filter_parameter(tokendef, tns, consume_token=False)
            tns.set_tokendef_to_variant(
                cql.LINE_LEFTARROW, same_arguments=False, same_flags=False
            )
        elif tns.tokendef is cql.LINE_LEFTARROW:
            self._insert_filter(match, tokendef)
            self._add_filter_parameter(tokendef, tns, consume_token=False)
        else:
            self._badtoken(match, tokendef)
            return

    def light(self, match, tokendef):
        """Add the CQL 'light' filter."""
        assert tokendef is cql.Token.LIGHT
        self._insert_filter(match, tokendef)

    def line(self, match, tokendef):
        """Add the CQL 'line' filter."""
        assert tokendef is cql.Token.LINE
        if self.node_stack[-1].tokendef is cql.Token.LINE:
            self._badtoken(match, tokendef)
            return
        self._insert_filter(match, tokendef)

    def loop(self, match, tokendef):
        """Add the CQL 'loop' filter."""
        assert tokendef is cql.Token.LOOP
        self._insert_filter(match, tokendef)

    def le(self, match, tokendef):
        """Add the CQL '<=' (less than or equal to) filter."""
        assert tokendef is cql.Token.LE
        self._insert_infix_relational(match, tokendef)
        self._adjust_infix_relational_tokendef(cql.LE_SET, cql.LE_POSITION)

    def lt(self, match, tokendef):
        """Add the CQL '<' (less than) filter."""
        assert tokendef is cql.Token.LT
        self._insert_infix_relational(match, tokendef)
        self._adjust_infix_relational_tokendef(cql.LT_SET, cql.LT_POSITION)

    def mainline(self, match, tokendef):
        """Add the CQL 'mainline' filter."""
        assert tokendef is cql.Token.MAINLINE
        self._insert_leaf_filter(match, tokendef)

    def makesquare(self, match, tokendef):
        """Add the CQL 'makesquare' filter.

        Matches 'makesquare (' and collapse_makesquare is called for the
        paired ')'.

        """
        assert tokendef is cql.Token.MAKESQUARE
        self._insert_filter(match, tokendef)

    def collapse_makesquare(self, *args):
        """Add ')' for 'makesquare' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses()

    def matchcount(self, match, tokendef):
        """Add the CQL 'matchcount' parameter."""
        assert tokendef is cql.Token.MATCHCOUNT
        self._badtoken(match, tokendef)

    def matchstring(self, match, tokendef):
        """Add the CQL 'matchstring' parameter."""
        assert tokendef is cql.Token.MATCHSTRING
        self._badtoken(match, tokendef)

    def mate(self, match, tokendef):
        """Add the CQL 'mate' filter."""
        assert tokendef is cql.Token.MATE
        self._insert_leaf_filter(match, tokendef)

    def max(self, match, tokendef):
        """Add the CQL 'max' filter.

        Matches 'max (' and collapse_max is called for the paired ')'.

        """
        assert tokendef is cql.Token.MAX
        self._insert_filter(match, tokendef)

    def collapse_max(self, *args):
        """Add ')' for 'max' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses(argument_count=None, minimum_arguments=2)

    def message(self, match, tokendef):
        """Add the CQL 'message' filter.

        Matches 'message (' and collapse_message is called for the
        paired ')'.

        """
        assert tokendef is cql.Token.MESSAGE
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 1:
            self.node_stack[-1].set_tokendef_to_variant(
                cql.SINGLE_MESSAGE_ARGUMENT, same_flags=False
            )

    def collapse_message(self, *args):
        """Add ')' for 'message' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses(argument_count=None, minimum_arguments=1)

    def min(self, match, tokendef):
        """Add the CQL 'min' filter.

        Matches 'min (' and collapse_min is called for the paired ')'.

        """
        assert tokendef is cql.Token.MIN
        self._insert_filter(match, tokendef)

    def collapse_min(self, *args):
        """Add ')' for 'min' filter.

        Called by self.rightparenthesis for the relevant ')' token.

        """
        del args
        self._close_parentheses(argument_count=None, minimum_arguments=2)

    # Right now the only idea I have to implement unary minus is to define a
    # 'unary_minus' parameter attached to the relevant nodes with the NUMBER or
    # NUMERIC_VARIABLE TokenDefinition as their tokendef attribute.
    def minus(self, match, tokendef):
        """Add arithmetic minus or unary minus filter.

        In '-1-1' the second '-' is arithmetic minus and the first '-' is
        unary minus.  Unary minus is accepted in arithmetic and comparison
        operations, and as the right hand operand of assignment so numeric
        variables with negative values are accepted in arithmetic and
        comparion operations.

        Experiments with CQL version 6 were done to establish the likely scope
        of unary minus.  Note that '+' does not have a unary interpretation.

        '-1' and 'w' after 'w=-1' are numbers, not numeric filters, because
        '{#q k}' is evaluated and gives a count of matches and 'w=#q {w k}
        gives warning 'single numeric variable always matches' without a count
        of matches.

        In 'w=1 k -w-1' the '-' just before 'w' in '-w-1' is unary minus.

        """
        assert tokendef is cql.Token.MINUS
        if self.tokens_available < 2:
            self.cql_error = cql.UNARY_MINUS.name.join(
                ("'", "' operator at end of statement")
            )
            return

        # Left operand is countable if unary minus could be applied to it, in
        # which case the minus being processed is arithmetic minus not unary
        # minus.  Looking at right operand cannot answer this question, and
        # for '{' in particular it is not possible yet to decide if it is
        # countable.  The _append_node_to_node_stack method was added hoping
        # judicious choice of stack appends will make it possible to answer
        # the question.
        node_stack = self.node_stack
        while node_stack:
            if len(node_stack) == 1:
                self._insert_unary_minus(
                    match, cql.CQL_TOKENS[self._peek_token(0).lastgroup]
                )
                return
            if tokendef.precedence > node_stack[-1].precedence:
                self._pop_top_stack(node_stack)
                continue
            if cql.Flags.ALLOWED_UNARY_MINUS in node_stack[-1].tokendef.flags:
                self._insert_infix_arithmetic(match, tokendef)
            else:
                self._insert_unary_minus(
                    match, cql.CQL_TOKENS[self._peek_token(0).lastgroup]
                )
            return

    def modulus(self, match, tokendef):
        """Add the CQL '%' (modulus) filter."""
        assert tokendef is cql.Token.MODULUS
        self._insert_infix_arithmetic(match, tokendef)

    # Documentation for move filter parameter combinations does not agree with
    # cql -parse reports.
    def move(self, match, tokendef):
        """Add the CQL 'move' filter."""
        assert tokendef is cql.Token.MOVE
        if self.node_stack[-1].tokendef is cql.Token.MOVE:
            self._pop_top_stack(self.node_stack)
        self._insert_filter(match, tokendef)

    def collapse_move(self, *args):
        """Complete the 'move' filter.

        Called when token is not a 'move' parameter after 'move' filter.

        """
        del args
        top = self.node_stack[-1]
        if top.tokendef is cql.Token.MOVE:
            if (
                cql.Token.COUNT in top.parameters
                and cql.Token.LEGAL not in top.parameters
                and cql.Token.PSEUDOLEGAL not in top.parameters
            ):
                self.cql_error = "".join(
                    (
                        "Parameter 'count' present in 'move' filter ",
                        "without 'legal' or 'pseudolegal' parameters",
                    )
                )

    # Because there is a MOVE_SET version of MOVE to collapse too, and the
    # same things are done.
    collapse_move_set = collapse_move

    def legal(self, match, tokendef):
        """Add 'legal' parameter to 'move' filter.

        Multiple 'legal' parameters are allowed.  Only one of the 'legal',
        'pseudolegal', and 'previous', parameters can be present.  The 'legal'
        parameter is not allowed if the 'capture', 'null', 'primary',
        'promote', or 'secondary' parameter is also a parameter.

        """
        assert tokendef is cql.Token.LEGAL
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._multiple_move_kind_parameters(tokendef, tns):
            return
        if self._parameters_incompatible_with_legal_present(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def previous(self, match, tokendef):
        """Add 'previous' parameter to 'move' filter.

        Multiple 'previous' parameters are allowed.  Only one of the 'legal',
        'pseudolegal', and 'previous', parameters can be present.

        """
        assert tokendef is cql.Token.PREVIOUS
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._multiple_move_kind_parameters(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def pseudolegal(self, match, tokendef):
        """Add 'pseudolegal' parameter to 'move' filter.

        Multiple 'pseudolegal' parameters are allowed.  Only one of the
        'legal', 'pseudolegal', and 'previous', parameters can be present.
        The 'legal' parameter is not allowed if the 'capture', 'null',
        'primary', 'promote', or 'secondary' parameter is also a parameter.

        """
        assert tokendef is cql.Token.PSEUDOLEGAL
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._multiple_move_kind_parameters(tokendef, tns):
            return
        if self._parameters_incompatible_with_legal_present(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def movenumber(self, match, tokendef):
        """Add the CQL 'movenumber' filter."""
        assert tokendef is cql.Token.MOVENUMBER
        self._insert_leaf_filter(match, tokendef)

    def star(self, match, tokendef):
        """Add numeric multiply or regular expression repeat zero or more."""
        assert tokendef is cql.Token.STAR
        self._insert_infix_arithmetic(match, tokendef)

    def ne(self, match, tokendef):
        """Add the CQL '!=' (not equal) filter."""
        assert tokendef is cql.Token.NE
        self._insert_infix_relational(match, tokendef)
        self._adjust_infix_relational_tokendef(cql.NE_SET, cql.NE_POSITION)

    def nestban(self, match, tokendef):
        """Add 'nestban' parameter to 'line' filter.

        Multiple 'nestban' parameters are not allowed.

        """
        assert tokendef is cql.Token.NESTBAN
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_line_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def northeast(self, match, tokendef):
        """Add the CQL 'northeast' filter."""
        assert tokendef is cql.Token.NORTHEAST
        self._insert_filter(match, tokendef)
        self._range = []

    def northwest(self, match, tokendef):
        """Add the CQL 'northwest' filter."""
        assert tokendef is cql.Token.NORTHWEST
        self._insert_filter(match, tokendef)
        self._range = []

    # Precedence of 'not' filter is seriously confusing at CQL version 6.0.4.
    # Filters lower in the table of precedence have higher precedence.  This
    # is used to explain why '2+3*5' means 2+(3*5), which is my expectation.
    # 'not' is lower in the table than 'or', but in the documentation for
    # compound filters, the section on their use, it says 'not Ra3 or Bb5' is
    # a single 'not' filter with argument 'Ra3 or Bb5'; and if either no R on
    # a3 or a B on b5 is wanted the expression is '{ not Ra3 } or Bb5'.
    # The 'not' and 'or' example contradicts the precedence table while the '+'
    # and '*' example agrees with the precedence table.
    # Descriptions of precedence for 'or', 'and', and 'not', in other contexts
    # are consistent with the 'not' and 'or' example being wrong.
    # In other words 'not Ra3 or Bb5' means '{ not Ra3 } or Bb5' rather than
    # 'not { Ra3 or Bb5 }'.
    # Simplest case of 'not' is to negate a piece designator, so use same
    # code, except for leaf node stuff, as piecedesignator method.
    # Difference is 'not' has an argument but piece designator does not.
    def not_(self, match, tokendef):
        """Add the CQL 'not' filter."""
        assert tokendef is cql.Token.NOT
        self._insert_filter(match, tokendef)

    def notransform(self, match, tokendef):
        """Add the CQL 'notransform' filter."""
        assert tokendef is cql.Token.NOTRANSFORM
        self._insert_filter(match, tokendef)

    def null(self, match, tokendef):
        """Add 'null' parameter to 'move' filter.

        Multiple 'null' parameters are allowed.  The 'null' parameter is not
        allowed if the 'enpassant', 'enpassantsquare', 'from', 'legal',
        'pseudolegal', 'promote', or 'to' parameter is also a parameter.

        """
        assert tokendef is cql.Token.NULL
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._parameters_incompatible_with_null_present(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    # Named 'x' rather than 'number' for consistency with 'variable' whose name
    # must sort high when creating the full statement regular expression using
    # the (?P<>) construct.  This method is used to collect ranges.  Numeric
    # variables are accepted as range elements so a simple regular expression
    # catching numbers and numeric variables catches filter names too.
    # 'cql -parse ...' where the only filter is a number is legal but 'cql ...'
    # attracts the error '... likely a result of an unexpected parse'.  The
    # 'cql(...)' construct at start of a *.cql file is not a filter.
    def x(self, match, tokendef):
        """Add number as range element, parameter, or variable assignment.

        A number is accepted as a filter by the CQL parser but attracts the
        error '... likely a result of an unexpected parse' when evaluated.
        Here, for example, the error "Number '5' is not allowed at this point'
        is given while parsing.

        """
        assert tokendef is cql.Token.NUMBER
        node_stack = self.node_stack
        if cql.Flags.NO_ARITHMETIC_FILTERS in node_stack[-1].tokendef.flags:
            self.cql_error = "".join(
                (
                    "Attempt to use number as constituent of '",
                    cql.Token.LINE.name,
                    "' filter",
                )
            )
            return
        if node_stack[-1].tokendef is cql.Token.NUMBER:
            self._pop_top_stack(node_stack)
        tns = node_stack[-1]
        if (
            cql.Flags.NAMED_COMPOUND_FILTER in tns.tokendef.flags
            or tns.tokendef.arguments.intersection(tokendef.returntype)
        ):
            self._insert_leaf_filter(match, tokendef)
        elif cql.Flags.ACCEPT_RANGE in node_stack[-1].tokendef.flags:
            if len(self._range) > 1:
                self.cql_error = "".join(
                    (
                        "Attempt to collect second range for '",
                        tns.name,
                        "' filter",
                    )
                )
                return
            range_ = self._range
            if cql.RANGE not in tns.parameters:
                tns.parameters[cql.RANGE] = range_
            if tns.parameters[cql.RANGE] is not range_:
                self.cql_error = "".join(
                    (
                        "Attempt to collect different range for '",
                        tns.name,
                        "' filter",
                    )
                )
                return
            if len(tns.parameters[cql.RANGE]) > 1:
                self.cql_error = "".join(
                    (
                        "Attempt to collect more than two items in ",
                        "range for '",
                        tns.name,
                        "' filter",
                    )
                )
                return
            range_.append(match.groupdict()[tokendef.name])
            self._consume_token(tokendef)
        else:
            self.cql_error = "".join(
                (
                    "Number '",
                    match.group(),
                    "' is not allowed at this point",
                )
            )

    def oo(self, match, tokendef):
        """Add 'o-o' parameter to 'move' filter.

        The 'o-o' parameter cannot be repeated.  Only one of the 'castle',
        'o-o', and 'o-o-o', parameters can be present.

        """
        assert tokendef is cql.Token.OO
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        if self._multiple_castling_parameters(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def ooo(self, match, tokendef):
        """Add 'o-o-o' parameter to 'move' filter.

        The 'o-o' parameter cannot be repeated.  Only one of the 'castle',
        'o-o', and 'o-o-o', parameters can be present.

        """
        assert tokendef is cql.Token.OOO
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        if self._multiple_castling_parameters(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def or_(self, match, tokendef):
        """Add the CQL 'or' filter."""
        assert tokendef is cql.Token.OR
        self._insert_infix_boolean(match, tokendef)

    def orthogonal(self, match, tokendef):
        """Add the CQL 'orthogonal' filter."""
        assert tokendef is cql.Token.ORTHOGONAL
        self._insert_filter(match, tokendef)
        self._range = []

    def output(self, match, tokendef):
        """Add the CQL 'output' parameter."""
        assert tokendef is cql.Token.OUTPUT
        self._badtoken(match, tokendef)

    def parent(self, match, tokendef):
        """Add the CQL 'parent' filter."""
        assert tokendef is cql.Token.PARENT
        self._insert_leaf_filter(match, tokendef)

    def passedpawns(self, match, tokendef):
        """Add the CQL 'passedpawns' filter."""
        assert tokendef is cql.Token.PASSEDPAWNS
        self._insert_leaf_filter(match, tokendef)

    def piecedesignator(self, match, tokendef):
        """Add the CQL piece designator filter.

        A piece designator is a description of a set of piece-square values.

        See the CQL documentation for details.

        """
        assert tokendef is cql.Token.PIECE_DESIGNATOR
        self._insert_leaf_filter(match, tokendef)

    # 'persistent name' seems to be treated as 'persistent name = 0' by CQL
    # version 6.0.4 judging by the '-parse' output.
    # 'persistent' is accepted just before a variable name, but nowhere else,
    # so put 'persistent' on node_stack and check next token is a variable;
    # delaying processing for 'persistent' until this 'variable' token is
    # processed.
    def persistent(self, match, tokendef):
        """Add the CQL 'persistent' filter.

        Usage seems to be 'persistent <variable name> [= <value>]'
        where <value> defaults to 0 (zero).

        """
        assert tokendef is cql.Token.PERSISTENT
        self._insert_filter(match, tokendef)
        if not self.tokens_available:
            self.cql_error = "".join(
                (
                    "Filter '",
                    self.node_stack[-1].name,
                    "' found at end of statement",
                )
            )
        elif self._peek_token(0).groupdict()[cql.Token.VARIABLE.name] is None:
            self.cql_error = "".join(
                (
                    "A variable name must follow '",
                    self.node_stack[-1].name,
                    "' filter, not '",
                    self._peek_token(0).group().strip(),
                    "'",
                )
            )

    def piece(self, match, tokendef):
        """Add the CQL 'piece' parameter."""
        assert tokendef is cql.Token.PIECE
        self._badtoken(match, tokendef)

    def piecein(self, match, tokendef):
        """Add the CQL 'piece <variable name> in' filter."""
        assert tokendef is cql.Token.PIECE_IN
        self.piece_or_square_variable(
            match, tokendef, cql.PIECE_VARIABLE, cql.TokenTypes.PIECE_VARIABLE
        )

    def pieceallin(self, match, tokendef):
        """Add the CQL 'piece all <variable name> in' filter."""
        assert tokendef is cql.Token.PIECE_ALL_IN
        self.piece_or_square_variable(
            match, tokendef, cql.PIECE_VARIABLE, cql.TokenTypes.PIECE_VARIABLE
        )

    def pieceassignment(self, match, tokendef):
        """Add the CQL 'piece <variable name> =' filter."""
        assert tokendef is cql.Token.PIECE_ASSIGNMENT
        self.piece_or_square_variable(
            match, tokendef, cql.PIECE_VARIABLE, cql.TokenTypes.PIECE_VARIABLE
        )

    def piece_or_square_variable(
        self, match, tokendef, filtertype, variabletype
    ):
        """Add variable name to CQL statement.

        The name must not start '__CQL'.

        The name must not already exist with an incompatible type for
        the current point in the statement.

        The name must be allowed at the current point in the statement.

        """
        self._insert_filter(match, tokendef)
        name = match.group().split()[-2]
        if name.startswith(cql.CQL_RESERVED_VARIABLE_NAME_PREFIX):
            self.cql_error = "".join(
                (
                    "Variable name '",
                    name,
                    "' starts with reserved sequence '",
                    cql.CQL_RESERVED_VARIABLE_NAME_PREFIX,
                    "' in '",
                    tokendef.name,
                    "' filter",
                )
            )
            return
        if name in self.variables and self.variables[name] is not variabletype:
            self.cql_error = "".join(
                (
                    "Variable name '",
                    name,
                    "' exists but is not a ",
                    variabletype.value,
                    "' in '",
                    tokendef.name,
                    "'",
                )
            )
            return
        variable = re.match(cql.CQL_PATTERN, name)
        if variable is None:
            self.cql_error = "".join(
                (
                    "'",
                    name,
                    "' is not allowed as a ",
                    variabletype.value,
                    "' in '",
                    tokendef.name,
                    "'",
                )
            )
            return
        if variable.groupdict()["y"] is None:
            self.cql_error = "".join(
                (
                    "'",
                    name,
                    "' is not allowed as a ",
                    variabletype.value,
                    "' in '",
                    tokendef.name,
                    "'",
                )
            )
            return
        if name not in self.variables:
            self.variables[name] = {"type": filtertype}
        node_stack = self.node_stack
        child = node_stack[-1].children
        child.append(self.create_node(cql.PIECE_VARIABLE, leaf=name))

        # Note following pop.
        self._append_node_to_node_stack(child[-1])
        self.node_stack.pop().set_tokendef_to_variant(
            self.get_filter_type_of_variable(name)
        )

    def pieceid(self, match, tokendef):
        """Add the CQL 'pieceid' filter."""
        assert tokendef is cql.Token.PIECEID
        self._insert_filter(match, tokendef)

    def pin(self, match, tokendef):
        """Add the CQL 'pin' filter."""
        assert tokendef is cql.Token.PIN
        if self.node_stack[-1].tokendef is cql.Token.PIN:
            self._badtoken(match, tokendef)
            return
        self._insert_filter(match, tokendef)

    def collapse_pin(self, *args):
        """Complete the 'pin' filter.

        Called when token is not a 'pin' parameter after 'pin' filter.

        """

    def player(self, match, tokendef):
        """Add the CQL 'player' filter."""
        assert tokendef is cql.Token.PLAYER
        self._insert_leaf_filter(match, tokendef)
        words = match.group().split()
        if len(words) > 2:
            if words[1] == cql.PLAYER_BLACK.pattern:
                self.node_stack[-1].set_tokendef_to_variant(cql.PLAYER_BLACK)
            elif words[1] == cql.PLAYER_WHITE.pattern:
                self.node_stack[-1].set_tokendef_to_variant(cql.PLAYER_WHITE)
        self.node_stack[-1].leaf = words[-1]

    def plus(self, match, tokendef):
        """Add arithmetic plus or regular expression repeat one or more.

        '+' does not have the unary interpretation but '-' does (from
        experiments with CQL version 6).

        """
        assert tokendef is cql.Token.PLUS
        self._insert_infix_arithmetic(match, tokendef)

    def ply(self, match, tokendef):
        """Add the CQL 'ply' filter."""
        assert tokendef is cql.Token.PLY
        self._insert_leaf_filter(match, tokendef)

    def position(self, match, tokendef):
        """Add the CQL 'position' filter."""
        assert tokendef is cql.Token.POSITION
        self._insert_filter(match, tokendef)

    def positionid(self, match, tokendef):
        """Add the CQL 'positionid' filter."""
        assert tokendef is cql.Token.POSITIONID
        self._insert_leaf_filter(match, tokendef)

    def power(self, match, tokendef):
        """Add the CQL 'power' filter."""
        assert tokendef is cql.Token.POWER
        self._insert_filter(match, tokendef)

    def primary(self, match, tokendef):
        """Add 'primary' parameter to 'line' or 'move' filter.

        Move filter.
        Multiple 'primary' parameters are allowed.  The 'primary' parameter
        is not allowed if the 'legal' or 'pseodolegal' parameter is also a
        parameter.  Only one of the 'primary' and 'secondary' parameters can
        be present.

        Line filter.
        Multiple 'primary' parameters are not allowed.  Only one of the
        'primary' and 'secondary' parameters can be present.

        """
        assert tokendef is cql.Token.PRIMARY
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_line_or_move_parameter(tokendef, tns):
            return
        if tns.tokendef is cql.Token.MOVE or tns.tokendef is cql.MOVE_SET:
            if self._legal_or_pseudolegal_parameter_present(tokendef, tns):
                return
        elif tns.tokendef is cql.Token.LINE:
            if self._duplicate_parameter(tokendef, tns):
                return
        if self._multiple_variation_parameters(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def promote(self, match, tokendef):
        """Add 'promote' parameter to 'move' filter.

        The 'promote' parameter must be a piece designator that does not
        specify any squares explicitly.

        The 'promote' parameter cannot be repeated.  The 'promote' parameter
        is not allowed if the 'legal' or 'pseodolegal' parameter is also a
        parameter.  The 'promote' parameter is not allowed if the 'enpassent',
        'enpassantsquare', or 'null', parameter is also a parameter.

        """
        assert tokendef is cql.Token.PROMOTE
        tns = self.node_stack[-1]
        if not self._accept_as_move_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        if self._legal_or_pseudolegal_parameter_present(tokendef, tns):
            return
        if self._null_or_enpassant_parameter_present(tokendef, tns):
            return
        self._insert_filter(match, tokendef)
        self._add_filter_parameter(tokendef, tns, consume_token=False)
        if not self.tokens_available:
            self.cql_error = "".join(
                (
                    "Expecting filter as argument for '",
                    self.node_stack[-1].name.strip("_"),
                    "' parameter",
                )
            )

    def quiet(self, match, tokendef):
        """Add 'quiet' parameter to 'consecutivemoves' filter.

        The 'quiet' parameter can be repeated.

        """
        assert tokendef is cql.Token.QUIET
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_consecutivemoves_parameter(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)
        self._range = []

    def rank(self, match, tokendef):
        """Add the CQL 'rank' filter."""
        assert tokendef is cql.Token.RANK
        self._insert_filter(match, tokendef)

    def ray(self, match, tokendef):
        """Add the CQL 'ray' filter."""
        assert tokendef is cql.Token.RAY
        self._insert_filter(match, tokendef)
        tns = self.node_stack[-1]
        words = match.group().split()[1:-1]
        for name in words:
            directions = cql.CQL_DIRECTIONS[cql.CQL_TOKENS[name]]
            for line in directions:
                if line in tns.parameters:
                    self.cql_error = "".join(
                        (
                            "Direction parameter '",
                            line.name,
                            "' duplicated by '",
                            name,
                            "' in '",
                            match.group(),
                            "' filter",
                        )
                    )
                    return
                tns.parameters[line] = True

    def collapse_ray(self, *args):
        """Add the CQL ')' keyword for a 'ray' filter."""
        del args
        self._close_parentheses(argument_count=None, minimum_arguments=2)

    def query(self, match, tokendef):
        """Add the CQL '?' (0 or 1) filter."""
        assert tokendef is cql.Token.QUERY
        self._insert_repeat_regular_expression(match, tokendef)

    def repeatplus(self, match, tokendef):
        """Add the CQL '+' (repeat) filter."""
        assert tokendef is cql.Token.REPEATPLUS
        self._insert_repeat_regular_expression(match, tokendef)

    def repeatrange(self, match, tokendef):
        """Add range specification to filter.

        A range is one or two numbers enclosed in '{}'.

        """
        assert tokendef is cql.Token.REPEATRANGE
        self._insert_repeat_regular_expression(
            match,
            tokendef,
            value=tuple(
                int(s)
                for s in match.group().strip().lstrip("{").rstrip("}").split()
            ),
        )

    def repeatstar(self, match, tokendef):
        """Add the CQL '*' (repeat) filter."""
        assert tokendef is cql.Token.REPEATSTAR
        self._insert_repeat_regular_expression(match, tokendef)

    def result(self, match, tokendef):
        """Add the CQL 'result' filter."""
        assert tokendef is cql.Token.RESULT
        self._insert_leaf_filter(match, tokendef)
        self.node_stack[-1].leaf = match.group().split(maxsplit=1)[-1]

    def reversecolor(self, match, tokendef):
        """Add the CQL 'reversecolor' filter."""
        assert tokendef is cql.Token.REVERSECOLOR
        self._insert_filter(match, tokendef)

    def right(self, match, tokendef):
        """Add the CQL 'right' filter."""
        assert tokendef is cql.Token.RIGHT
        self._insert_filter(match, tokendef)
        self._range = []

    def rightarrow(self, match, tokendef):
        """Add '-->' parameter to 'line' filter.

        The '-->' parameter can be repeated.

        The 'line' filter to which '-->' is a parameter is converted to a
        'line rightarrow' filter because '-->' is the only parameter accepted
        afterwards in this 'line' filter,

        """
        assert tokendef is cql.Token.RIGHTARROW
        self._collapse_stack_frame(cql.Flags.LINE_FRAME)
        tns = self.node_stack[-1]
        if not self._accept_as_line_rightarrow_parameter(tokendef, tns):
            return
        self._insert_filter(match, tokendef)
        self._add_filter_parameter(tokendef, tns, consume_token=False)
        if tns.tokendef is cql.Token.LINE:
            tns.set_tokendef_to_variant(
                cql.LINE_RIGHTARROW, same_arguments=False, same_flags=False
            )

    def rotate45(self, match, tokendef):
        """Add the CQL 'rotate45' filter."""
        assert tokendef is cql.Token.ROTATE45
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(cql.ROTATE45_COUNT)

    def rotate90(self, match, tokendef):
        """Add the CQL 'rotate90' filter."""
        assert tokendef is cql.Token.ROTATE90
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(cql.ROTATE90_COUNT)

    def secondary(self, match, tokendef):
        """Add 'secondary' parameter to 'line' or 'move' filter.

        Move filter.
        Multiple 'secondary' parameters are allowed.  The 'secondary' parameter
        is not allowed if the 'legal' or 'pseodolegal' parameter is also a
        parameter.  Only one of the 'primary' and 'secondary' parameters can
        be present.

        Line filter.
        Multiple 'secondary' parameters are not allowed.  Only one of the
        'primary' and 'secondary' parameters can be present.

        """
        assert tokendef is cql.Token.SECONDARY
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_line_or_move_parameter(tokendef, tns):
            return
        if tns.tokendef is cql.Token.MOVE or tns.tokendef is cql.MOVE_SET:
            if self._legal_or_pseudolegal_parameter_present(tokendef, tns):
                return
        elif tns.tokendef is cql.Token.LINE:
            if self._duplicate_parameter(tokendef, tns):
                return
        if self._multiple_variation_parameters(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def shift(self, match, tokendef):
        """Add the CQL 'shift' filter."""
        assert tokendef is cql.Token.SHIFT
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(cql.SHIFT_COUNT)

    def shifthorizontal(self, match, tokendef):
        """Add the CQL 'shifthorizontal' filter."""
        assert tokendef is cql.Token.SHIFTHORIZONTAL
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(
                cql.SHIFTHORIZONTAL_COUNT
            )

    def shiftvertical(self, match, tokendef):
        """Add the CQL 'shiftvertical' filter."""
        assert tokendef is cql.Token.SHIFTVERTICAL
        self._insert_filter(match, tokendef)
        if len(match.group().split()) == 2:
            self.node_stack[-1].set_tokendef_to_variant(
                cql.SHIFTVERTICAL_COUNT
            )

    def sidetomove(self, match, tokendef):
        """Add the CQL 'sidetomove' filter."""
        assert tokendef is cql.Token.SIDETOMOVE
        self._insert_leaf_filter(match, tokendef)

    def silent(self, match, tokendef):
        """Add the CQL 'silent' parameter."""
        assert tokendef is cql.Token.SILENT
        self._badtoken(match, tokendef)

    def singlecolor(self, match, tokendef):
        """Add 'singlecolor' parameter to 'line' filter.

        Multiple 'singlecolor' parameters are not allowed.

        """
        assert tokendef is cql.Token.SINGLECOLOR
        del match
        tns = self.node_stack[-1]
        if not self._accept_as_line_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        self._add_filter_parameter(tokendef, tns)

    def site(self, match, tokendef):
        """Add the CQL 'site' filter."""
        assert tokendef is cql.Token.SITE
        self._insert_leaf_filter(match, tokendef)
        self.node_stack[-1].leaf = match.group().split(maxsplit=1)[-1]

    def sort(self, match, tokendef):
        """Add the CQL 'sort' filter."""
        assert tokendef is cql.Token.SORT
        self._insert_filter(match, tokendef)
        node_stack = self.node_stack
        words = re.match(cql.QUOTED_STRING.pattern, match.group())
        if words.group(2):
            node_stack[-1].set_tokendef_to_variant(cql.SORT_MIN)
        if words.group(3):
            node_stack[-1].parameters[cql.QUOTED_STRING] = words.group(
                3
            ).strip()

    def southeast(self, match, tokendef):
        """Add the CQL 'southeast' filter."""
        assert tokendef is cql.Token.SOUTHEAST
        self._insert_filter(match, tokendef)
        self._range = []

    def southwest(self, match, tokendef):
        """Add the CQL 'southwest' filter."""
        assert tokendef is cql.Token.SOUTHWEST
        self._insert_filter(match, tokendef)
        self._range = []

    def sqrt(self, match, tokendef):
        """Add the CQL 'sqrt' filter."""
        assert tokendef is cql.Token.SQRT
        self._insert_filter(match, tokendef)

    def square(self, match, tokendef):
        """Add the CQL 'square' parameter."""
        assert tokendef is cql.Token.SQUARE
        self._badtoken(match, tokendef)

    # Both 'x=k square x in h1 x attack K' and 'square x in h1 x attack K x=k'
    # are accepted by -parse, implying a set variable is meant when square
    # filter documentation refers to square variables.  This is consistent
    # with variable documentation reference to four types of variable: set,
    # numeric, piece, and position.
    # The square documentation does say, formally, variable is a set variable
    # but then procedes to talk about square variables. (Easy to miss.)

    def squarein(self, match, tokendef):
        """Add the CQL 'square <variable name> in' filter."""
        assert tokendef is cql.Token.SQUARE_IN
        self.piece_or_square_variable(
            match, tokendef, cql.SET_VARIABLE, cql.TokenTypes.SET_VARIABLE
        )

    def squareallin(self, match, tokendef):
        """Add the CQL 'square all <variable name> in' filter."""
        assert tokendef is cql.Token.SQUARE_ALL_IN
        self.piece_or_square_variable(
            match, tokendef, cql.SET_VARIABLE, cql.TokenTypes.SET_VARIABLE
        )

    def stalemate(self, match, tokendef):
        """Add the CQL 'stalemate' filter."""
        assert tokendef is cql.Token.STALEMATE
        self._insert_leaf_filter(match, tokendef)

    def terminal(self, match, tokendef):
        """Add the CQL 'terminal' filter."""
        assert tokendef is cql.Token.TERMINAL
        self._insert_leaf_filter(match, tokendef)

    def through(self, match, tokendef):
        """Add 'through' parameter to 'pin' filter.

        The 'through' parameter cannot be repeated.

        """
        assert tokendef is cql.Token.THROUGH
        tns = self.node_stack[-1]
        if not self._accept_as_pin_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        self._insert_filter(match, tokendef)
        self._add_filter_parameter(tokendef, tns, consume_token=False)
        if not self.tokens_available:
            self.cql_error = "".join(
                (
                    "Expecting filter as argument for '",
                    self.node_stack[-1].name.strip("_"),
                    "' parameter",
                )
            )

    def tilde(self, match, tokendef):
        """Add the CQL '~' filter."""
        assert tokendef is cql.Token.TILDE
        self._insert_filter(match, tokendef)

    def to(self, match, tokendef):
        """Add 'to' parameter to 'move' or 'pin' filter.

        The 'to' parameter cannot be repeated.

        The 'move' filter is converted from a logical filter to a set filter
        when 'to' is the first parameter,

        """
        assert tokendef is cql.Token.TO
        tns = self.node_stack[-1]
        if not self._accept_as_move_or_pin_parameter(tokendef, tns):
            return
        if self._duplicate_parameter(tokendef, tns):
            return
        if tns.tokendef is cql.Token.MOVE:
            if not tns.children and not tns.parameters:
                tns.set_tokendef_to_variant(cql.MOVE_SET)
        self._insert_filter(match, tokendef)
        self._add_filter_parameter(tokendef, tns, consume_token=False)
        if not self.tokens_available:
            self.cql_error = "".join(
                (
                    "Expecting filter as argument for '",
                    self.node_stack[-1].name.strip("_"),
                    "' parameter",
                )
            )

    def true(self, match, tokendef):
        """Add the CQL 'true' filter."""
        assert tokendef is cql.Token.TRUE
        self._insert_leaf_filter(match, tokendef)

    def type(self, match, tokendef):
        """Add the CQL 'type' filter."""
        assert tokendef is cql.Token.TYPE
        self._insert_filter(match, tokendef)

    def union(self, match, tokendef):
        """Add the CQL '|' filter."""
        assert tokendef is cql.Token.UNION
        self._insert_infix_binary(match, tokendef)

    def up(self, match, tokendef):
        """Add the CQL 'up' filter."""
        assert tokendef is cql.Token.UP
        self._insert_filter(match, tokendef)
        self._range = []

    # Named 'y' rather than 'variable' as the name must sort high when creating
    # the full statement regular expression using the (?P<>) construct because
    # any word matches.
    def y(self, match, tokendef):
        """Add the CQL 'variable' keyword.

        See # comment in module for reason method name is 'y'.

        """
        assert tokendef is cql.Token.VARIABLE
        variable_name = match.groupdict()[tokendef.name]
        if variable_name.startswith(cql.CQL_RESERVED_VARIABLE_NAME_PREFIX):
            self.cql_error = "".join(
                (
                    "Variable name '",
                    variable_name,
                    "' starts with reserved sequence '",
                    cql.CQL_RESERVED_VARIABLE_NAME_PREFIX,
                    "'",
                )
            )
            return
        node_stack = self.node_stack
        variable = self.variables.get(variable_name)
        if node_stack[-1].tokendef is cql.Token.PERSISTENT:
            if variable and not variable["persistent"]:
                self.cql_error = "".join(
                    (
                        "Variable '",
                        variable_name,
                        "' exists but is not a persistent numeric variable",
                    )
                )
                return
            del node_stack[-1]
            del node_stack[-1].children[-1]
            if variable:
                tokendef = variable["type"]
                assert tokendef is cql.NUMERIC_VARIABLE
                self._insert_leaf_filter(match, tokendef)
                return
            self._insert_leaf_filter(match, cql.NUMERIC_VARIABLE)
            self.variables[variable_name] = {
                "persistent": True,
                "type": node_stack[-1].tokendef,
            }
            return
        if variable:
            tokendef = variable["type"]
            if tokendef is cql.Token.VARIABLE:
                self.cql_error = "".join(
                    (
                        "Variable '",
                        variable_name,
                        "' exists but has not been set to a value",
                    )
                )
                return
            if tokendef is cql.NUMERIC_VARIABLE:
                if (
                    cql.Flags.NO_ARITHMETIC_FILTERS
                    in node_stack[-1].tokendef.flags
                ):
                    self.cql_error = "".join(
                        (
                            "Attempt to use numeric variable '",
                            variable_name,
                            "' as constituent of '",
                            cql.Token.LINE.name,
                            "' filter",
                        )
                    )
                    return
            if tokendef is cql.Token.FUNCTION:
                if variable_name in self._called_functions:
                    self.cql_error = "".join(
                        (
                            "Attempt to call function '",
                            variable_name,
                            "' within a call of function '",
                            variable_name,
                            "'",
                        )
                    )
                    return
                self._called_functions.add(variable_name)
                self._insert_filter(match, cql.FUNCTION_CALL)
                child = node_stack[-1].children
                child.append(self.create_node(cql.FUNCTION_NAME))
                child[-1].leaf = variable_name
                return
            self._insert_leaf_filter(match, tokendef)
            return
        if cql.Flags.NO_ARITHMETIC_FILTERS in node_stack[-1].tokendef.flags:
            self.cql_error = "".join(
                (
                    "Attempt to use unset variable '",
                    variable_name,
                    "' as constituent of '",
                    cql.Token.LINE.name,
                    "' filter",
                )
            )
            return
        if (
            self.tokens_available == 1
            or self._peek_token(1).groupdict()[cql.Token.ASSIGN.name] is None
        ):
            self.cql_error = "".join(
                (
                    "Expecting assignment to variable '",
                    variable_name,
                    "' on first use",
                )
            )
            return
        if node_stack[-1].tokendef is cql.CONSECUTIVEMOVES_LEFTPARENTHESIS:
            type_ = cql.POSITION_VARIABLE
        elif (
            node_stack[-1].tokendef is cql.POSITION_VARIABLE
            and node_stack[-2].tokendef is cql.CONSECUTIVEMOVES_LEFTPARENTHESIS
        ):
            type_ = cql.POSITION_VARIABLE
        else:
            type_ = cql.Token.VARIABLE
        self.variables[variable_name] = {"persistent": False, "type": type_}
        self._insert_leaf_filter(match, type_)

    def variation(self, match, tokendef):
        """Add the CQL 'variation' filter."""
        assert tokendef is cql.Token.VARIATION
        self._insert_leaf_filter(match, tokendef)

    def variations(self, match, tokendef):
        """Add the CQL 'variations' parameter."""
        assert tokendef is cql.Token.BADTOKEN
        self._badtoken(match, tokendef)

    def vertical(self, match, tokendef):
        """Add the CQL 'vertical' filter."""
        assert tokendef is cql.Token.VERTICAL
        self._insert_filter(match, tokendef)
        self._range = []

    def virtualmainline(self, match, tokendef):
        """Add the CQL 'virtualmainline' filter."""
        assert tokendef is cql.Token.VIRTUALMAINLINE
        self._insert_leaf_filter(match, tokendef)

    def white(self, match, tokendef):
        """Add the CQL 'white' filter."""
        assert tokendef is cql.Token.WHITE
        self._insert_leaf_filter(match, tokendef)

    def wtm(self, match, tokendef):
        """Add the CQL 'wtm' filter."""
        assert tokendef is cql.Token.WTM
        self._insert_leaf_filter(match, tokendef)

    def xray(self, match, tokendef):
        """Add the CQL 'xray' filter."""
        assert tokendef is cql.Token.XRAY
        self._insert_filter(match, tokendef)

    def collapse_xray(self, *args):
        """Add the CQL ')' keyword for an 'xray' clause."""
        del args
        self._close_parentheses(argument_count=None, minimum_arguments=2)

    def year(self, match, tokendef):
        """Add the CQL 'year' filter."""
        assert tokendef is cql.Token.YEAR
        self._insert_leaf_filter(match, tokendef)

    # if <filter> then <filter> else <filter>.
    # The three filters are the 'condition', 'then', and 'else', filters.
    # 'if if k>2 then r==1 then mate else Q' is a valid 'if' filter and gives
    # a non-trivial answer, for 97-98.pgn downloaded from 4ncl, of 17 matches
    # out of 1056 games.

    def if_(self, match, tokendef):
        """Add the CQL 'if' filter."""
        assert tokendef is cql.Token.IF
        self._insert_filter(match, tokendef)

    def then(self, match, tokendef):
        """Add the CQL 'then' filter."""
        assert tokendef is cql.Token.THEN
        del match
        self._collapse_stack_frame(cql.Flags.IF_FRAME)
        if self.cql_error:
            return
        node_stack = self.node_stack
        while True:
            if len(node_stack[-1].children) < 1:
                self.cql_error = "".join(
                    (
                        "'",
                        tokendef.name,
                        "' parameter given before condition filter for '",
                        node_stack[-1].tokendef.name,
                        "' filter",
                    )
                )
                return
            if len(node_stack[-1].children) > 1:
                self._pop_top_stack(node_stack)
                continue
            break
        tns = self.node_stack[-1]
        if tokendef in tns.parameters:
            self.cql_error = "".join(
                (
                    "'",
                    tokendef.name,
                    "' parameter already present in '",
                    tns.tokendef.name,
                    "' filter",
                )
            )
            return
        if tns.tokendef is not cql.Token.IF:
            self.cql_error = "".join(
                (
                    "'",
                    tokendef.name,
                    "' parameter is not allowed in '",
                    tns.tokendef.name,
                    "' filter",
                )
            )
            return
        self._consume_token(tokendef)
        tns.parameters[cql.Token.THEN] = True

    def else_(self, match, tokendef):
        """Add the CQL 'else' filter."""
        del match
        assert tokendef is cql.Token.ELSE
        self._collapse_stack_frame(cql.Flags.IF_FRAME)
        if self.cql_error:
            return
        node_stack = self.node_stack
        while True:
            if len(node_stack[-1].children) < 2:
                self.cql_error = "".join(
                    (
                        "'",
                        tokendef.name,
                        "' parameter given before then filter for '",
                        node_stack[-1].tokendef.name,
                        "' filter",
                    )
                )
                return
            if len(node_stack[-1].children) > 2:
                self._pop_top_stack(node_stack)
                continue
            break
        tns = self.node_stack[-1]
        if tokendef in tns.parameters:
            self.cql_error = "".join(
                (
                    "'",
                    tokendef.name,
                    "' parameter already present in '",
                    tns.tokendef.name,
                    "' filter",
                )
            )
            return
        if tns.tokendef is not cql.Token.IF:
            self.cql_error = "".join(
                (
                    "'",
                    tokendef.name,
                    "' parameter is not allowed in '",
                    tns.tokendef.name,
                    "' filter",
                )
            )
            return
        if cql.Token.THEN not in tns.parameters:
            self.cql_error = "".join(
                (
                    "'",
                    tokendef.name,
                    "' parameter is not allowed unless '",
                    cql.Token.THEN.name,
                    "' parameter is already given in '",
                    tns.tokendef.name,
                    "' filter",
                )
            )
            return
        if len(tns.children) != 2:
            self.cql_error = "".join(
                (
                    "The filter for '",
                    cql.Token.THEN.name,
                    "' parameter has not been given in '",
                    tns.tokendef.name,
                    "' filter: cannot specify '",
                    tokendef.name,
                    "' parameter",
                )
            )
            return
        self.node_stack[-1].parameters[cql.Token.ELSE] = True
        self._consume_token(tokendef)

    # Do not forget to change the definition in the Statement subclass in the
    # self-test code of this module to fit changes to this definition.
    def _append_node_to_node_stack(self, node):
        node_stack = self.node_stack
        if not self.tokens_available:
            node_stack.append(node)

        # Put node on stack if next token will generate a node which grabs it
        # from the filter to left.  Precedence comparison and '{}' and '()'
        # will decide this.
        elif (
            cql.CQL_TOKENS[self._peek_token(0).lastgroup].precedence
            > node_stack[-1].precedence
        ):
            node_stack.append(node)

        # So this method can replace existing 'node_stack.append(node)'
        # equivalents.
        else:
            node_stack.append(node)

    # Why is it not as simple as pop top while top does not accept tokendef?
    # 1: there are tokens like '{' which stay active until a matching '}'.
    # 2: if terminal token is top then pop until condition 1 ignoring cases
    #    where terminal token is acceptable to intermediate tops of stack.
    # 3: there are tokens like 'move' which stay active until a token that is
    #    not a parameter token for 'move' is found (allowing for parameters
    #    which take an argument).
    # 4: The HALT_POP_NO_BODY_FILTER is correct for 'echo ( x y ) q K' but not
    #    'echo ( x y ) x & y'; while 'echo ( x y ) { x & y }' is correct.  The
    #    version without '{}' incorrectly gives echo body higher precedence
    #    than '&' (and all the other infix operators too).  See if this is only
    #    only problem shortly.
    # 5. 'Q attacks parent' should give syntax error because both arguments of
    #    attacks must be set filters; implying the pop after all the 'if's
    #    cannot be reached.
    def _insert_filter(self, match, tokendef):
        del match
        node_stack = self.node_stack

        # Same as collapse_leftparenthesis version except tokendef for
        # clpns.tokendef.
        tns = node_stack[-1]
        if tns.tokendef is cql.Token.ASSIGN and len(tokendef.returntype) == 1:
            variable_name = tns.children[0].leaf
            variable = self.variables.get(variable_name)
            if variable is None:
                self.cql_error = "".join(
                    (
                        "Variable '",
                        variable_name,
                        "' is not defined so it's type cannot be set",
                    )
                )
                return
            type_ = cql.map_filter_assign_to_variable.get(tokendef.returntype)
            if type_:
                variable_type = variable["type"]
                if cql.TokenTypes.UNSET_VARIABLE in variable_type.returntype:
                    variable["type"] = type_
                    tns.children[0].tokendef = type_
                elif variable_type is not type_:
                    self.cql_error = "".join(
                        (
                            "Variable '",
                            variable_name,
                            "' is a '",
                            tns.children[0].name,
                            "' but assigned filter is a '",
                            self.create_node(tokendef).name,
                            "'",
                        )
                    )
                    return

        while True:
            if (
                cql.Flags.ALLOWED_TOP_STACK_AT_END
                in node_stack[-1].tokendef.flags
            ):
                while True:
                    if (
                        cql.Flags.HALT_POP_CHAINED_FILTERS
                        in node_stack[-1].tokendef.flags
                    ):
                        break
                    if (
                        cql.Flags.HALT_POP_NO_BODY_FILTER
                        in node_stack[-1].tokendef.flags
                    ):
                        if len(node_stack[-1].children) < 3:
                            break
                    if (
                        cql.Flags.END_FILTER_NON_PARAMETER
                        in node_stack[-1].tokendef.flags
                    ):
                        getattr(self, "collapse_" + node_stack[-1].name)()
                        if self.cql_error:
                            return
                        break
                    self._pop_top_stack(node_stack)
            if (
                cql.Flags.HALT_POP_CHAINED_FILTERS
                in node_stack[-1].tokendef.flags
            ):
                break
            if (
                cql.Flags.HALT_POP_CHAINED_FILTERS in tokendef.flags
                and cql.Flags.PARAMETER_TAKES_ARGUMENT
                in node_stack[-1].tokendef.flags
            ):
                break
            if (
                cql.Flags.HALT_POP_NO_BODY_FILTER
                in node_stack[-1].tokendef.flags
            ):
                if len(node_stack[-1].children) < 3:
                    break
            if tokendef.returntype.intersection(
                node_stack[-1].tokendef.arguments
            ):
                break
            if (
                cql.Flags.END_FILTER_NON_PARAMETER
                in node_stack[-1].tokendef.flags
            ):
                getattr(self, "collapse_" + node_stack[-1].name)()
                if self.cql_error:
                    return
                break
            self.cql_error = "".join(
                (
                    "'",
                    tokendef.name.strip("_"),
                    "' filter type does not fit expected filter types for '",
                    node_stack[-1].name.strip("_"),
                    "'",
                )
            )
            return

            # Unreachable, or was it supposed to be one level left?
            # self._pop_top_stack(node_stack)

        self._consume_token(tokendef)
        child = node_stack[-1].children
        child.append(self.create_node(tokendef))
        self._append_node_to_node_stack(child[-1])

    def _insert_leaf_filter(self, match, tokendef):
        node_stack = self.node_stack
        itnstd = node_stack[-1].tokendef
        self._insert_filter(match, tokendef)
        if self.cql_error:
            return
        tns = node_stack[-1]
        tns.leaf = match.groupdict()[tokendef.name]
        if cql.Flags.PARAMETER_TAKES_ARGUMENT in itnstd.flags:
            while True:
                if self._pop_top_stack(node_stack).tokendef is itnstd:
                    break

    # If tns is 'assign' the associated variable must be numeric already or
    # converted to numeric if it is not a set or position variable.
    # Insertion is done by _insert_leaf_filter if the token does not take
    # arguments, and _insert_filter otherwise.
    def _insert_unary_minus(self, match, definition):
        node_stack = self.node_stack
        tns = node_stack[-1]
        if tns.tokendef is cql.Token.ASSIGN:
            variable_name = tns.children[0].leaf
            variable_type = self.variables[variable_name]["type"]
            if variable_type is not cql.NUMERIC_VARIABLE:
                if variable_type is not cql.Token.VARIABLE:
                    self.cql_error = "".join(
                        (
                            "Operand to left of '",
                            tns.tokendef.name,
                            "', a '",
                            variable_type.variant_name,
                            "', can not be used with '",
                            cql.UNARY_MINUS.variant_name,
                            "'",
                        )
                    )
                    return
                self.variables[variable_name]["type"] = cql.NUMERIC_VARIABLE
                tns.children[0].set_tokendef_to_variant(cql.NUMERIC_VARIABLE)
        if definition.arguments:
            self._insert_filter(match, definition)
        else:
            self._insert_leaf_filter(match, definition)
        if not self.cql_error:
            node_stack[-1].parameters[cql.UNARY_MINUS] = True

    def _insert_infix_arithmetic(self, match, tokendef):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack

        # Collapse stack until a higher precedence filter is found.  If this
        # is a numeric filter arithmetic can be done.
        # For minus this step has been done while testing for unary minus.
        while node_stack:
            if len(node_stack) == 1:
                break
            if (
                cql.Flags.NO_ARITHMETIC_FILTERS
                in node_stack[-1].tokendef.flags
            ):
                self._consume_token(tokendef)
                if tokendef is cql.Token.STAR:
                    self._pop_top_stack(node_stack).parameters[
                        cql.Token.REPEATSTAR
                    ] = True
                elif tokendef is cql.Token.PLUS:
                    self._pop_top_stack(node_stack).parameters[
                        cql.Token.REPEATPLUS
                    ] = True
                else:
                    self._pop_top_stack(node_stack).parameters[tokendef] = True
                return
            if tokendef.precedence > node_stack[-1].precedence:
                self._pop_top_stack(node_stack)
                continue
            break

        # Avoid the test for a bare filter which take arguments if the filter
        # has children or a leaf value.
        if cql.Flags.ALLOWED_UNARY_MINUS in node_stack[-1].tokendef.flags and (
            node_stack[-1].leaf or node_stack[-1].children
        ):
            pass
        elif (
            cql.Flags.ALLOWED_TOP_STACK_AT_END
            not in node_stack[-1].tokendef.flags
        ):
            self.cql_error = tokendef.name.strip("_").join(
                ("Argument expected, not '", "' filter")
            )
            return

        if cql.TokenTypes.NUMERIC_FILTER not in node_stack[-1].returntype:
            self.cql_error = "".join(
                (
                    "Operand to left of '",
                    tokendef.name,
                    "' is not a '",
                    cql.TokenTypes.NUMERIC_FILTER.value,
                    "' filter",
                )
            )
            return
        self._consume_token(tokendef)
        child = self._pop_top_stack(node_stack)
        if not node_stack:
            self.cql_error = tokendef.name.strip("_").join(
                ("Empty node stack found processing '", "'")
            )
            return
        if cql.Flags.CLOSE_BRACE_OR_PARENTHESIS in child.tokendef.flags:
            child = node_stack[-1].children[-1]
        if node_stack[-1].precedence > tokendef.precedence:
            node = self.create_node(tokendef)
            node.children.append(self._pop_top_stack(node_stack))
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
        elif (
            node_stack[-1].tokendef is not tokendef
            and cql.Flags.NAMED_COMPOUND_FILTER in tokendef.flags
        ):
            node = self.create_node(tokendef)
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
            node_stack[-1].children.append(child)

    def _insert_infix_arithmetic_inplace(self, match, tokendef):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack
        if (
            cql.Flags.ALLOWED_TOP_STACK_AT_END
            not in node_stack[-1].tokendef.flags
        ):
            self.cql_error = tokendef.name.strip("_").join(
                ("Argument expected, not '", "' filter")
            )
            return
        if not tokendef.arguments.intersection(node_stack[-1].returntype):
            filter_types = [f.value for f in tokendef.arguments]
            if len(filter_types) == 1:
                filter_type_report = filter_types[0]
            elif filter_types:
                filter_type_report = "' or '".join(filter_types)
            else:
                filter_type_report = ""
            self.cql_error = "".join(
                (
                    "Operand to left of '",
                    tokendef.name,
                    "' is not a '",
                    filter_type_report,
                    "' filter",
                )
            )
            return
        self._consume_token(tokendef)
        child = self._pop_top_stack(node_stack)
        if (
            node_stack
            and cql.Flags.CLOSE_BRACE_OR_PARENTHESIS in child.tokendef.flags
        ):
            child = node_stack[-1].children[-1]
        if not node_stack:
            self.cql_error = tokendef.name.strip("_").join(
                ("Empty node stack found processing '", "'")
            )
            return
        if node_stack[-1].precedence > tokendef.precedence:
            node = self.create_node(tokendef)
            node.children.append(self._pop_top_stack(node_stack))
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
        elif (
            node_stack[-1].tokendef is not tokendef
            and cql.Flags.NAMED_COMPOUND_FILTER in tokendef.flags
        ):
            node = self.create_node(tokendef)
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
            node_stack[-1].children.append(child)

    def _adjust_infix_relational_tokendef(self, set_, position):
        tns = self.node_stack[-1]
        left_operand_type = tns.children[0].returntype
        if cql.TokenTypes.SET_FILTER in left_operand_type:
            tns.set_tokendef_to_variant(set_, same_arguments=False)
        elif cql.TokenTypes.POSITION_FILTER in left_operand_type:
            tns.set_tokendef_to_variant(position, same_arguments=False)

    def _insert_infix_relational(self, match, tokendef):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack
        if (
            cql.Flags.ALLOWED_TOP_STACK_AT_END
            not in node_stack[-1].tokendef.flags
        ):
            self.cql_error = tokendef.name.strip("_").join(
                ("Argument expected, not '", "' filter")
            )
            return
        if not tokendef.arguments.intersection(node_stack[-1].returntype):
            filter_types = [f.value for f in tokendef.arguments]
            if len(filter_types) == 1:
                filter_type_report = filter_types[0]
            elif filter_types:
                filter_type_report = "' or '".join(filter_types)
            else:
                filter_type_report = ""
            self.cql_error = "".join(
                (
                    "Operand to left of '",
                    tokendef.name,
                    "' is not a '",
                    filter_type_report,
                    "' filter",
                )
            )
            return
        self._consume_token(tokendef)
        child = self._pop_top_stack(node_stack)
        if (
            node_stack
            and cql.Flags.CLOSE_BRACE_OR_PARENTHESIS in child.tokendef.flags
        ):
            child = node_stack[-1].children[-1]
        if not node_stack:
            self.cql_error = tokendef.name.strip("_").join(
                ("Empty node stack found processing '", "'")
            )
            return
        if node_stack[-1].precedence > tokendef.precedence:
            node = self.create_node(tokendef)
            node.children.append(self._pop_top_stack(node_stack))
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
        elif (
            node_stack[-1].tokendef is not tokendef
            and cql.Flags.NAMED_COMPOUND_FILTER in tokendef.flags
        ):
            node = self.create_node(tokendef)
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
            node_stack[-1].children.append(child)

    def _insert_infix_binary(self, match, tokendef):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack
        if not tokendef.arguments.intersection(node_stack[-1].returntype):
            filter_types = [f.value for f in tokendef.arguments]
            if len(filter_types) == 1:
                filter_type_report = filter_types[0]
            elif filter_types:
                filter_type_report = "' or '".join(filter_types)
            else:
                filter_type_report = ""
            self.cql_error = "".join(
                (
                    "Operand to left of '",
                    tokendef.name,
                    "' is not a '",
                    filter_type_report,
                    "' filter",
                )
            )
            return
        self._consume_token(tokendef)
        child = self._pop_top_stack(node_stack)
        if (
            node_stack
            and cql.Flags.CLOSE_BRACE_OR_PARENTHESIS in child.tokendef.flags
        ):
            child = node_stack[-1].children[-1]
        if not node_stack:
            self.cql_error = tokendef.name.strip("_").join(
                ("Empty node stack found processing '", "'")
            )
            return
        if node_stack[-1].precedence > tokendef.precedence:
            node = self.create_node(tokendef)
            node.children.append(self._pop_top_stack(node_stack))
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
        elif (
            node_stack[-1].tokendef is not tokendef
            and cql.Flags.NAMED_COMPOUND_FILTER in tokendef.flags
        ):
            node = self.create_node(tokendef)
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
            node_stack[-1].children.append(child)

    def _insert_infix_boolean(self, match, tokendef):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack
        if (
            cql.Flags.ALLOWED_TOP_STACK_AT_END
            not in node_stack[-1].tokendef.flags
        ):
            self.cql_error = tokendef.name.strip("_").join(
                ("Argument expected, not '", "' filter")
            )
            return
        self._consume_token(tokendef)
        child = self._pop_top_stack(node_stack)
        if (
            node_stack
            and cql.Flags.CLOSE_BRACE_OR_PARENTHESIS in child.tokendef.flags
        ):
            child = node_stack[-1].children[-1]
        if not node_stack:
            self.cql_error = tokendef.name.strip("_").join(
                ("Empty node stack found processing '", "'")
            )
            return
        if node_stack[-1].precedence > tokendef.precedence:
            node = self.create_node(tokendef)
            node.children.append(self._pop_top_stack(node_stack))
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
        elif (
            node_stack[-1].tokendef is not tokendef
            and cql.Flags.NAMED_COMPOUND_FILTER in tokendef.flags
        ):
            node = self.create_node(tokendef)
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
            node_stack[-1].children.append(child)

    def _insert_infix_colon(self, match, tokendef):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack
        if cql.TokenTypes.POSITION_FILTER not in node_stack[-1].returntype:
            self.cql_error = "".join(
                (
                    "Operand to left of '",
                    tokendef.name,
                    "' is not a '",
                    cql.TokenTypes.POSITION_FILTER.value,
                    "' filter",
                )
            )
            return
        self._consume_token(tokendef)
        child = self._pop_top_stack(node_stack)
        if (
            node_stack
            and cql.Flags.CLOSE_BRACE_OR_PARENTHESIS in child.tokendef.flags
        ):
            child = node_stack[-1].children[-1]
        if not node_stack:
            self.cql_error = tokendef.name.strip("_").join(
                ("Empty node stack found processing '", "'")
            )
            return
        if node_stack[-1].precedence > tokendef.precedence:
            node = self.create_node(tokendef)
            node.children.append(self._pop_top_stack(node_stack))
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
        elif (
            node_stack[-1].tokendef is not tokendef
            and cql.Flags.NAMED_COMPOUND_FILTER in tokendef.flags
        ):
            node = self.create_node(tokendef)
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
            node_stack[-1].children.append(child)

    def _insert_infix_assign(self, match, tokendef):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack
        if cql.Flags.ASSIGN_TO_VARIABLE not in node_stack[-1].tokendef.flags:
            self.cql_error = (
                node_stack[-1]
                .name.strip("_")
                .join(("Cannot assign to a '", "', only a variable"))
            )
            return
        self._consume_token(tokendef)
        child = self._pop_top_stack(node_stack)
        if not node_stack:
            self.cql_error = tokendef.name.strip("_").join(
                ("Empty node stack found processing '", "'")
            )
            return
        if cql.Flags.NAMED_COMPOUND_FILTER in tokendef.flags:
            node = self.create_node(tokendef)
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
            node_stack[-1].children.append(child)
            return
        if node_stack[-1].precedence >= tokendef.precedence:
            node = self.create_node(tokendef)
            node.children.append(self._pop_top_stack(node_stack))
            node_stack[-1].children[-1] = node
            return

    def _insert_infix(self, match, tokendef):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack
        if cql.TokenTypes.SET_FILTER not in node_stack[-1].returntype:
            self.cql_error = "".join(
                (
                    "Operand to left of '",
                    tokendef.name,
                    "' is not a '",
                    cql.TokenTypes.SET_FILTER.value,
                    "' filter",
                )
            )
            return
        self._consume_token(tokendef)
        child = self._pop_top_stack(node_stack)
        if (
            node_stack
            and cql.Flags.CLOSE_BRACE_OR_PARENTHESIS in child.tokendef.flags
        ):
            child = node_stack[-1].children[-1]
        if not node_stack:
            self.cql_error = tokendef.name.strip("_").join(
                ("Empty node stack found processing '", "'")
            )
            return
        if cql.Flags.NAMED_COMPOUND_FILTER in tokendef.flags:
            node = self.create_node(tokendef)
            node_stack[-1].children[-1] = node
            self._append_node_to_node_stack(node)
            node_stack[-1].children.append(child)
            return
        if node_stack[-1].precedence >= tokendef.precedence:
            node = self.create_node(tokendef)
            node.children.append(self._pop_top_stack(node_stack))
            node_stack[-1].children[-1] = node
            return

    def _insert_repeat_regular_expression(self, match, tokendef, value=True):
        del match
        if not self.tokens_consumed:
            self.cql_error = tokendef.name.strip("_").join(
                ("'", "' operator at start of statement")
            )
            return
        node_stack = self.node_stack
        while node_stack:
            if len(node_stack) == 1:
                break
            if (
                cql.Flags.NO_ARITHMETIC_FILTERS
                in node_stack[-1].tokendef.flags
            ):
                self._consume_token(tokendef)
                self._pop_top_stack(node_stack).parameters[tokendef] = value
                return
            self._pop_top_stack(node_stack)
        self.cql_error = tokendef.name.strip("_").join(
            ("'", "' operator found outside 'line' filter")
        )

    def _close_parentheses(self, argument_count=2, minimum_arguments=None):
        node_stack = self.node_stack
        if argument_count and len(node_stack[-1].children) != argument_count:
            self.cql_error = "".join(
                (
                    "Filter '",
                    node_stack[-1].name,
                    "' with parentheses takes ",
                    str(argument_count),
                    " arguments but ",
                    str(len(node_stack[-1].children)),
                    " given",
                )
            )
            return
        if not argument_count:
            if minimum_arguments is None:
                minimum_arguments = 1
            if len(node_stack[-1].children) < minimum_arguments:
                self.cql_error = "".join(
                    (
                        "Filter '",
                        node_stack[-1].name,
                        "' with parentheses takes ",
                        str(minimum_arguments),
                        " or more arguments but none given",
                    )
                )
                return
        self._consume_token(self.node_stack[-1].tokendef)
        self._pop_top_stack(self.node_stack)

        # All 'v = <filter> ( <arguments> )' statements fail after this because
        # the assign node is top of stack and blocks everything.  Various
        # errors are reported depending on what, if anything, follows.
        # Plain '<filter> ( <arguments> )' statements seem to be fine.
        # Hack the assign node out of the way.
        if node_stack[-1].tokendef is cql.Token.ASSIGN:
            self._pop_top_stack(self.node_stack)

    def _add_filter_parameter(self, tokendef, filternode, consume_token=True):
        filternode.parameters[tokendef] = True
        if consume_token:
            self._consume_token(tokendef)

    def _accept_as_filter_parameter(self, tokendef, filternode, tokenset):
        if filternode.tokendef in tokenset:
            return True
        self.cql_error = "".join(
            (
                "'",
                tokendef.name,
                "' is not a parameter of the '",
                filternode.name,
                "' filter",
            )
        )
        return False

    def _accept_as_consecutivemoves_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef, filternode, {cql.Token.CONSECUTIVEMOVES}
        )

    def _accept_as_find_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef, filternode, {cql.Token.FIND}
        )

    def _accept_as_line_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef, filternode, {cql.Token.LINE}
        )

    def _accept_as_find_or_line_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef,
            filternode,
            {cql.Token.FIND, cql.Token.LINE, cql.LINE_LEFTARROW},
        )

    def _accept_as_line_leftarrow_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef, filternode, {cql.LINE_LEFTARROW}
        )

    def _accept_as_line_rightarrow_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef, filternode, {cql.Token.LINE, cql.LINE_RIGHTARROW}
        )

    def _accept_as_move_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef, filternode, {cql.Token.MOVE, cql.MOVE_SET}
        )

    def _accept_as_pin_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef, filternode, {cql.Token.PIN}
        )

    def _accept_as_line_or_move_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef,
            filternode,
            {cql.Token.LINE, cql.Token.MOVE, cql.MOVE_SET},
        )

    def _accept_as_move_or_pin_parameter(self, tokendef, filternode):
        return self._accept_as_filter_parameter(
            tokendef, filternode, {cql.Token.MOVE, cql.MOVE_SET, cql.Token.PIN}
        )

    def _legal_or_pseudolegal_parameter_present(self, tokendef, filternode):
        if (
            cql.Token.LEGAL not in filternode.parameters
            and cql.Token.PSEUDOLEGAL not in filternode.parameters
        ):
            return False
        names = "".join(
            (
                cql.Token.LEGAL.name,
                "' or '",
                cql.Token.PSEUDOLEGAL.name,
            )
        )
        self.cql_error = "".join(
            (
                "Parameter '",
                tokendef.name,
                "' cannot be used with '",
                names,
                "' in '",
                filternode.name,
                "' filter",
            )
        )
        return True

    def _parameters_incompatible_with_legal_present(
        self, tokendef, filternode
    ):
        if (
            cql.Token.CAPTURE not in filternode.parameters
            and cql.Token.NULL not in filternode.parameters
            and cql.Token.PRIMARY not in filternode.parameters
            and cql.Token.PROMOTE not in filternode.parameters
            and cql.Token.SECONDARY not in filternode.parameters
        ):
            return False
        names = "".join(
            (
                cql.Token.CAPTURE.name,
                "', '",
                cql.Token.NULL.name,
                "', '",
                cql.Token.PRIMARY.name,
                "', '",
                cql.Token.PROMOTE.name,
                "', or '",
                cql.Token.SECONDARY.name,
            )
        )
        self.cql_error = "".join(
            (
                "Parameter '",
                tokendef.name,
                "' cannot be used with '",
                names,
                "' in '",
                filternode.name,
                "' filter",
            )
        )
        return True

    def _parameters_incompatible_with_null_present(self, tokendef, filternode):
        if (
            cql.Token.ENPASSANT not in filternode.parameters
            and cql.Token.ENPASSANT_SQUARE not in filternode.parameters
            and cql.Token.FROM not in filternode.parameters
            and cql.Token.LEGAL not in filternode.parameters
            and cql.Token.PSEUDOLEGAL not in filternode.parameters
            and cql.Token.PROMOTE not in filternode.parameters
            and cql.Token.TO not in filternode.parameters
        ):
            return False
        names = "".join(
            (
                cql.Token.ENPASSANT.name,
                "', '",
                cql.Token.ENPASSANT_SQUARE.name,
                "', '",
                cql.Token.FROM.name,
                "', '",
                cql.Token.LEGAL.name,
                "', '",
                cql.Token.PSEUDOLEGAL.name,
                "', '",
                cql.Token.PROMOTE.name,
                "', or '",
                cql.Token.TO.name,
            )
        )
        self.cql_error = "".join(
            (
                "Parameter '",
                tokendef.name,
                "' cannot be used with '",
                names,
                "' in '",
                filternode.name,
                "' filter",
            )
        )
        return True

    def _null_or_promote_parameter_present(self, tokendef, filternode):
        if (
            cql.Token.NULL not in filternode.parameters
            and cql.Token.PROMOTE not in filternode.parameters
        ):
            return False
        names = "".join(
            (
                cql.Token.NULL.name,
                "' or '",
                cql.Token.PROMOTE.name,
            )
        )
        self.cql_error = "".join(
            (
                "Parameter '",
                tokendef.name,
                "' cannot be used with '",
                names,
                "' in '",
                filternode.name,
                "' filter",
            )
        )
        return True

    def _null_or_enpassant_parameter_present(self, tokendef, filternode):
        if (
            cql.Token.NULL not in filternode.parameters
            and cql.Token.ENPASSANT not in filternode.parameters
            and cql.Token.ENPASSANT_SQUARE not in filternode.parameters
        ):
            return False
        names = "".join(
            (
                cql.Token.NULL.name,
                "', '",
                cql.Token.ENPASSANT.name,
                "', or '",
                cql.Token.ENPASSANT_SQUARE.name,
            )
        )
        self.cql_error = "".join(
            (
                "Parameter '",
                tokendef.name,
                "' cannot be used with '",
                names,
                "' in '",
                filternode.name,
                "' filter",
            )
        )
        return True

    def _duplicate_parameter(self, tokendef, filternode):
        if tokendef not in filternode.parameters:
            return False
        self.cql_error = "".join(
            (
                "Parameter '",
                tokendef.name,
                "' cannot be repeated in '",
                filternode.name,
                "' filter",
            )
        )
        return True

    def _multiple_castling_parameters(self, tokendef, filternode):
        if (
            (
                cql.Token.CASTLE in filternode.parameters
                and tokendef is not cql.Token.CASTLE
            )
            or (
                cql.Token.OO in filternode.parameters
                and tokendef is not cql.Token.OO
            )
            or (
                cql.Token.OOO in filternode.parameters
                and tokendef is not cql.Token.OOO
            )
        ):
            names = "".join(
                (
                    cql.Token.CASTLE.name,
                    "', '",
                    cql.Token.OO.name,
                    "', and '",
                    cql.Token.OOO.name,
                )
            )
            self.cql_error = "".join(
                (
                    "Parameter '",
                    tokendef.name,
                    "' cannot be present in '",
                    filternode.name,
                    "' filter with other parameters from '",
                    names,
                    "'",
                )
            )
            return True
        return False

    def _multiple_move_kind_parameters(self, tokendef, filternode):
        if (
            (
                cql.Token.LEGAL in filternode.parameters
                and tokendef is not cql.Token.LEGAL
            )
            or (
                cql.Token.PSEUDOLEGAL in filternode.parameters
                and tokendef is not cql.Token.PSEUDOLEGAL
            )
            or (
                cql.Token.PREVIOUS in filternode.parameters
                and tokendef is not cql.Token.PREVIOUS
            )
        ):
            names = "".join(
                (
                    cql.Token.LEGAL.name,
                    "', '",
                    cql.Token.PSEUDOLEGAL.name,
                    "', and '",
                    cql.Token.PREVIOUS.name,
                )
            )
            self.cql_error = "".join(
                (
                    "Parameter '",
                    tokendef.name,
                    "' cannot be present in '",
                    filternode.name,
                    "' filter with other parameters from '",
                    names,
                    "'",
                )
            )
            return True
        return False

    def _multiple_enpassant_parameters(self, tokendef, filternode):
        if (
            cql.Token.ENPASSANT in filternode.parameters
            and tokendef is not cql.Token.ENPASSANT
        ) or (
            cql.Token.ENPASSANT_SQUARE in filternode.parameters
            and tokendef is not cql.Token.ENPASSANT_SQUARE
        ):
            names = "".join(
                (
                    cql.Token.ENPASSANT.name,
                    "', and '",
                    cql.Token.ENPASSANT_SQUARE.name,
                )
            )
            self.cql_error = "".join(
                (
                    "Parameter '",
                    tokendef.name,
                    "' cannot be present in '",
                    filternode.name,
                    "' filter with other parameters from '",
                    names,
                    "'",
                )
            )
            return True
        return False

    def _multiple_variation_parameters(self, tokendef, filternode):
        if (
            cql.Token.PRIMARY in filternode.parameters
            and tokendef is not cql.Token.PRIMARY
        ) or (
            cql.Token.SECONDARY in filternode.parameters
            and tokendef is not cql.Token.SECONDARY
        ):
            names = "".join(
                (
                    cql.Token.PRIMARY.name,
                    "', and '",
                    cql.Token.SECONDARY.name,
                )
            )
            self.cql_error = "".join(
                (
                    "Parameter '",
                    tokendef.name,
                    "' cannot be present in '",
                    filternode.name,
                    "' filter with other parameters from '",
                    names,
                    "'",
                )
            )
            return True
        return False


class ErrorInformation:
    """Error information about a ChessQL query and report fomatters.

    This class assumes processing a query stops when the first error is met.

    The Statement parse() method returns a ErrorInformation instance if any
    attribute other than _statement is bound to an object other than None.

    """

    def __init__(self, statement):
        """Initialise error information for the CQL statement.

        The initial values mean no error found.

        """
        self._statement = statement
        self._tokens = None
        self._next_token = None
        self._description = ""

    @property
    def statement(self):
        """Return the CQL statement."""
        return self._statement

    @property
    def tokens(self):
        """Return the list of tokens yet to be processed."""
        return self._tokens

    @tokens.setter
    def tokens(self, value):
        if self._tokens is not None:
            raise StatementError("A token error already exists.")
        self._tokens = value

    @property
    def next_token(self):
        """Return the token being processed."""
        return self._next_token

    @next_token.setter
    def next_token(self, value):
        if self._next_token is not None:
            raise StatementError("A token error already exists.")
        self._next_token = value

    @property
    def description(self):
        """Return the error description."""
        return self._description

    @description.setter
    def description(self, value):
        if self._description:
            return
        self._description = value

    @property
    def error_found(self):
        """Return True if unprocessed tokens or an error description exists."""
        return self._tokens is not None or self._description

    def get_error_report(self):
        """Return a str for error dialogue noting token being processed."""
        if self.error_found:
            if self._description:
                return "".join(
                    (
                        "Error processing statement:\n\n",
                        self._statement.strip(),
                        "\n\n",
                        self._description,
                        ".",
                    )
                )
            if self._next_token:
                next_token = "".join(
                    (
                        "\n\nThe item being processed is:\n\n",
                        "".join(self._next_token),
                    )
                )
            else:
                next_token = ""
            return "".join(
                (
                    "Error, likely at or just after end of:\n\n",
                    " ".join("".join(t) for t in self._tokens),
                    "\n\nderived from:\n\n",
                    self._statement.strip(),
                    next_token,
                )
            )
        return "".join(
            (
                "An unidentified error seems to exist in:\n\n",
                self._statement.strip(),
            )
        )

    def add_error_report_to_message(self, message, sep="\n\n"):
        """Return message extended with an error report."""
        return "".join((message, sep, self.get_error_report()))


if __name__ == "__main__":

    # To try out CQL version 6.0.4 statements run:
    # "python -m chessql.core.statement".
    # To additionally include a trace of the parsing run:
    # "python -m chessql.core.statement trace".

    import sys

    from .node import NodeError

    class StatementTest(Statement):
        """Extend Statement to demonstrate CQL statement parsing."""

        _options = set(s.lower() for s in sys.argv[1:])

        if "trace" in _options:

            if "append" in _options or "pop" in _options:

                def _process_token(self, match, groupkey):
                    print(
                        "_process_token", match.lastgroup, repr(match.group())
                    )
                    getattr(self, groupkey)(match, cql.CQL_TOKENS[groupkey])
                    print(self._trace(groupkey))

            else:

                def _process_token(self, match, groupkey):
                    getattr(self, groupkey)(match, cql.CQL_TOKENS[groupkey])
                    print(self._trace(groupkey))

        if "pop" in _options:

            def _pop_top_stack(self, stack):
                print("_pop_top_stack", stack[-1])
                return super()._pop_top_stack(stack)

        if "insert" in _options:

            # The 'end', 'precedence', 'skip', and 'default', annotations give
            # the condition in which a node is added to stack for tracing
            # purposes.
            # Do not forget to change this definition to fit changes in the
            # superclass definition.
            def _append_node_to_node_stack(self, node):
                ret = "skip"
                node_stack = self.node_stack
                if not self.tokens_available:
                    node_stack.append(node)
                    ret = "end"
                elif (
                    cql.CQL_TOKENS[self._peek_token(0).lastgroup].precedence
                    > node_stack[-1].precedence
                ):
                    node_stack.append(node)
                    ret = "precedence"
                else:
                    node_stack.append(node)
                    ret = "default"
                print("_append_node_to_node_stack", ret, node)

            def _insert_filter(self, *args):
                print("_insert_filter")
                super()._insert_filter(*args)

            def _insert_leaf_filter(self, *args):
                print("_insert_leaf_filter")
                super()._insert_leaf_filter(*args)

            def _insert_unary_minus(self, *args):
                print("_insert_unary_minus")
                super()._insert_unary_minus(*args)

            def _insert_infix_arithmetic(self, *args):
                print("_insert_infix_arithmetic")
                super()._insert_infix_arithmetic(*args)

            def _insert_infix_arithmetic_inplace(self, *args):
                print("_insert_infix_arithmetic_inplace")
                super()._insert_infix_arithmetic_inplace(*args)

            def _insert_infix_relational(self, *args):
                print("_insert_infix_relational")
                super()._insert_infix_relational(*args)

            def _insert_infix_binary(self, *args):
                print("_insert_infix_binary")
                super()._insert_infix_binary(*args)

            def _insert_infix_boolean(self, *args):
                print("_insert_infix_boolean")
                super()._insert_infix_boolean(*args)

            def _insert_infix_colon(self, *args):
                print("_insert_infix_colon")
                super()._insert_infix_colon(*args)

            def _insert_infix_assign(self, *args):
                print("_insert_infix_assign")
                super()._insert_infix_assign(*args)

            def _insert_infix(self, *args):
                print("_insert_infix")
                super()._insert_infix(*args)

        del _options

        @staticmethod
        def _trace_start(method_name):
            return " ".join(("--", str(method_name)))

        def _trace_body(self):
            variables = self.variables
            trace = [" ".join(("  ", str(len(variables)), "variables"))]
            if variables:
                for name, var in sorted(variables.items()):
                    type_ = var["type"]
                    svtn = str(
                        type_.variant_name
                        if type_.variant_name is not None
                        else type_.name
                    )
                    if var.get("persistent"):
                        varstr = "persistent " + svtn
                    else:
                        varstr = svtn
                    parameters = var.get("parameters")
                    if parameters:
                        varstr += ",".join(parameters).join(("<", ">"))
                    body = var.get("body")
                    if body:
                        bodystr = " ".join(body)
                        if len(bodystr) > 40:
                            bodystr = " ... ".join(
                                (bodystr[:25], bodystr[-6:])
                            )
                        varstr += bodystr.join(("<", ">"))
                    trace.append(" ".join(("     ", name, varstr)))
            trace.append(
                " ".join(("  ", str(len(self.node_stack)), "node_stack"))
            )
            for node in self.node_stack:
                trace.append(" ".join(("     ", str(node))))
            return "\n".join(trace)

        @staticmethod
        def _trace_end():
            return "-- end"

        def _trace(self, method_name):
            return "\n".join(
                (
                    self._trace_start(method_name),
                    self._trace_body(),
                    self._trace_end(),
                )
            )

    del sys

    while True:
        try:
            s = input("cql> ")
        except EOFError as exc:
            print(exc)
            break
        except KeyboardInterrupt:
            print()
            break
        if not s:
            continue
        try:
            query = StatementTest()
            query.process_statement(s)
            print()
            # See Statement class attribute declarations for comment on the
            # unsubscriptable-object report generated for this statement.
            for stmatch in query.tokens[0]:
                print(
                    *[(k, v) for k, v in stmatch.groupdict().items() if v],
                    sep="\t"
                )
            # pylint objection to svtn, vs, and bs, as dodgy constant
            # names was not understood: especially as s, t, p, v, (at
            # least) in nearby code do not attract the snake_case
            # comment.  I did see an example where the pylint constant
            # name comment was fixed by adding a module docstring,
            # techbeamers.com/pylint-tool/, but I do not understand that
            # either.  It seems reasonable to argue SVTN binds to a
            # constant, but does this not apply to the techbeamers
            # example, 'a = 23' and so forth?
            #
            # Here my objective is to get rid of the invalid-name
            # comments, otherwise I would have changed vn and v below
            # to variable_name and variable, and probably other names
            # too.
            for vn, v in sorted(query.variables.items()):
                t = v["type"]
                print(type(v), type(t))
                SVTN = str(
                    t.variant_name if t.variant_name is not None else t.name
                )
                if v.get("persistent"):
                    VS = "persistent " + SVTN
                else:
                    VS = SVTN
                p = v.get("parameters")
                if p:
                    VS += ",".join(p).join(("<", ">"))
                b = v.get("body")
                if b:
                    BS = " ".join(b)
                    if len(BS) > 50:
                        BS = " ... ".join((BS[:30], BS[-11:]))
                    VS += BS.join(("<", ">"))
                print(" ".join((vn, VS)))
            print(query.cql_parameters)
            print(query.cql_filters)
            print(query.node_stack)
            if query.cql_error:
                print(
                    "".join(
                        (
                            "error: ",
                            query.cql_error.description,
                            "\nin query: '",
                            s,
                            "'\nafter: '",
                            " ".join(
                                (
                                    m.groupdict(default="<?>").get(k.name, "")
                                    for m, k in query.cql_tokens_stack[0]
                                )
                            ),
                            "'",
                        )
                    )
                )
            else:

                # Should not need this: it means stack has not collapsed in
                # the correct way.
                if not query.cql_filters and query.node_stack:
                    print("node_stack[0]", query.node_stack[0])

                print("ok:", s)
            print()
        except (NodeError, StatementError) as exc:
            print()
            print(exc)
            print()
            print(
                "".join(
                    (
                        "error in query:\n'",
                        s,
                        "'\nafter:\n'",
                        " ".join(
                            (
                                m.groupdict(default="<?>").get(k.name, "")
                                for m, k in query.cql_tokens_stack[0]
                            )
                        ),
                        "'",
                    )
                )
            )
            print()
            continue
        except RuntimeError as exc:
            print()
            print(exc)
