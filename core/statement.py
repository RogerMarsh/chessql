# statement.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) statement parser.

The basic structure of a CQL statement at version 5.1 is:

'cql ( parameters ) list_of_filters'.

This module allows both parameters and list_of_filters to be empty.

The keywords 'or', 'not', and '{ ... }', alter the default implied 'and' between
adjacent filters in the list.  All three keywords generate a filter which takes
it's place in a list_of_filters.

A number of named operations may be applied to a filter in the form:

'operation optional_range filter' where filter is something that can appear as
a single element in a list_of_filters.  Operations can be chained:

'operation1 optional_range1 operation2 opetional_range2 ... filter', and the
generated filter appears as a single element in a list of filters.

A number of named operations take arguments in the form '( arguments )'. Some
arguments are list_of_filters.

"""

import re
import collections

import pgn_read.core.constants

from . import constants, node

CQL_PARAMETERS = (constants.OUTPUT,
                  constants.INPUT,
                  constants.GAMENUMBER,
                  constants.YEAR,
                  constants.SILENT,
                  constants.PLAYER,
                  constants.ELO,
                  constants.SITE,
                  constants.EVENT,
                  constants.MATCHCOUNT,
                  constants.SORT,
                  )

# ATTACK is a shorthand for:
# 'ray orthogonal ( [QqRr] on s, ... ) or ray diagonal ( [QqBb] on s, ... )
# and is included as a RAY_DIRECTION.
# ATTACK is not the 'attack' filter in this context.
RAY_DIRECTIONS = frozenset(
    constants.DIRECTION_FILTER.union((constants.ATTACK,)))

TRANSFORM_FILTERS = frozenset((constants.FLIP,
                               constants.FLIPDIHEDRAL,
                               constants.FLIPHORIZONTAL,
                               constants.FLIPVERTICAL,
                               constants.FLIPCOLOR,
                               constants.ROTATE45,
                               constants.ROTATE90,
                               constants.SHIFT,
                               constants.SHIFTHORIZONTAL,
                               constants.SHIFTVERTICAL,
                               ))
STAR_FILTERS = frozenset((constants.NEXT_STAR,
                          constants.PREVIOUS_STAR,
                          ))

# MAINLINE, PREVIOUS, and NEXT, are move modifiers not filters in this context.
MOVE_MODIFIERS = frozenset((constants.MAINLINE,
                            constants.PREVIOUS,
                            constants.NEXT,
                            constants.EMPTY,
                            ))

RELATION_ECHO_PARAMETERS = frozenset((constants.ECHOFLIP,
                                      constants.ECHOFLIPVERTICAL,
                                      constants.ECHOFLIPHORIZONTAL,
                                      constants.ECHOSHIFT,
                                      constants.ECHOSHIFTHORIZONTAL,
                                      constants.ECHOSHIFTVERTICAL,
                                      constants.ECHOROTATE90,
                                      ))
RELATION_TOMOVE_ARGUMENTS = frozenset((constants.MATCH,
                                       constants.MISMATCH,
                                       ))
RELATION_LCA_PLAIN_PARAMETERS = frozenset((constants.ANCESTOR,
                                           constants.DESCENDANT,
                                           ))
RELATION_LCA_RANGE_PARAMETERS = frozenset((constants.LCAMAX,
                                           constants.LCASOURCE,
                                           constants.LCASUBSTRING,
                                           constants.LCASUM,
                                           constants.LCATARGET,
                                           ))
RELATION_SQUARE_PARAMETERS = frozenset((constants.MATCH,
                                        constants.MISMATCH,
                                        constants.SOURCESQUARES,
                                        constants.TARGETSQUARES,
                                        ))
GAME_RESULTS = (
    pgn_read.core.constants.WHITE_WIN,
    pgn_read.core.constants.BLACK_WIN,
    pgn_read.core.constants.DRAW)
REAL_BRACES = frozenset((constants.CQL,
                         constants.LEFT_BRACE_FILTER,
                         constants.LEFT_PARENTHESIS_FILTER,
                         constants.RELATION,
                         ))
IMPLIED_BRACES = frozenset((constants.CQL,
                            constants.LEFT_BRACE_FILTER,
                            constants.LEFT_PARENTHESIS_FILTER,
                            constants.RELATION,
                            constants.NOT,
                            constants.OR,
                            constants.ON,
                            constants.TO,
                            constants.FROM,
                            constants.IN,
                            ))
PARAMETER_BRACES = frozenset((constants.OR,
                              constants.ON,
                              constants.TO,
                              constants.FROM,
                              constants.IN,
                              ))
VARIABLE_TYPES = frozenset((constants.PIECE, constants.SQUARE))

# Better name needed to indicate shared syntax.
RAY_FILTERS = frozenset(
    RAY_DIRECTIONS.union(TRANSFORM_FILTERS.union(STAR_FILTERS)))

COUNTABLE_FILTERS = frozenset()
COUNTABLE_RANGE_FILTERS = frozenset((constants.ATTACK,
                                     constants.COUNTSQUARES,
                                     constants.SQUARE,
                                     constants.NEXT,
                                     constants.PREVIOUS,
                                     constants.NEXT2,
                                     constants.PREVIOUS2,
                                     constants.NEXT_STAR,
                                     constants.PREVIOUS_STAR,
                                     constants.POWER,
                                     constants.POWERDIFFERENCE,
                                     constants.MOVENUMBER,
                                     constants.YEAR,
                                     constants.ELO,
                                     constants.RAY,
                                     constants.MATCHCOUNT,
                                     ))

Token = collections.namedtuple('Token', constants.TOKEN_NAMES)

_ROTATE45_VALIDATION_TABLE = str.maketrans('12345678', 'xxxxxxxx')


class StatementError(Exception):
    pass


class Statement:
    """CQL statement parser for version 5.1.

    Parse text for a CQL statement.
    
    """
    create_node = node.Node

    def __init__(self):
        """"""
        super().__init__()
        self._description_string = ''
        self._statement_string = ''

        # Error handling is slightly different to .querystatement module.
        # The error information object is held directly here while it is held
        # in the Where instance used to calculate the query there.
        # This module processes instructions used to generate Where instances.
        self._reset_state()
        self._error_information = None

    def _reset_state(self):
        """Initialiase the CQL parsing state.

        The analyser is able to have at least two goes at a statement.

        """
        self._error_information = False
        self.tokens = None
        self.cql_tokens = []
        self.stack = []
        self.node_stack = []
        self.brace_parenthesis_stack = []
        self.cql_parameters = None
        self.cql_filters = None

        # The scoping rules for piece and square variables at cql5.1 seem to be:
        # $name is unique across piece and square use and cannot be redefined.
        # $name is visible in all enclosed scopes.
        # $name scope is bounded by '( ... )' and '{ ... }'.
        # This is not certain because:
        # '{square $x in h1-8 attack (R $x)} attack (Q $x)' gives error unbound,
        # 'square $x in h1-8 attack (R $x) attack (Q $x)' is ok,
        # '{shift 1 square $x in h1-8 attack (R $x)} attack (Q $x)' is ok.
        # However:
        # '{shift 0 square $x in h1-8 attack (R $x)} attack (Q $x)' gives
        # error undeclared so 'attack (Q $x)' is probably ignored in the
        # 'shift 1' version because the shift filter evaluates False or empty,
        # so the scoping assumption is probably sound.

        # All declared variable names.
        self.variables = {}

        # Variable names declared in scope.
        self.variables_stack = []

    @property
    def cql_error(self):
        return self._error_information

    @cql_error.setter
    def cql_error(self, value):
        if self._error_information:
            return
        self._error_information = ErrorInformation(
            self._statement_string.strip())
        self._error_information.description = value

    def get_name_text(self):
        """Return name text."""
        return self._description_string

    def get_name_statement_text(self):
        """Return name and statement text."""
        return constants.NAME_DELIMITER.join(
            (self._description_string,
             self._statement_string,
             ))

    def get_statement_text(self):
        """Return statement text."""
        return self._statement_string
        
    def lex(self):
        """Split the ChessQL statement into tokens."""
        self.tokens = re.findall(constants.CQL_PATTERN,
                                 self._statement_string)
        if self._statement_string.strip() == '':
            self._error_information = False
            return
        
    def parse(self):
        """Generate a tree from tokens describing the query."""

        # lex() sets self._error_information False if statement is worth
        # parsing
        if self._error_information:
            return
        
        self.stack.append(self.look_for_cql_parameters_or_body)
        while len(self.tokens):

            # 'bool(self.stack[-1]()) == True' means an error is detected and
            # an error reporter has been appended to self.stack.
            if self.stack[-1]():
                self.stack[-1]()
                break

        else:
            self.stack[-1]()

    def validate(self):
        """Return None if query is valid, or a WhereStatementError instance."""

        if self._error_information:
            return self._error_information
        if not self.cql_filters:
            return None
        return self._rotate45_specific_squares(self.cql_filters, [])
        
    def _rotate45_specific_squares(self, filter_, rotate45stack):
        if filter_.type == constants.ROTATE45:
            rotate45stack.append(None)
        for n in filter_.children:
            if rotate45stack and n.type == constants.PIECE_DESIGNATOR_FILTER:
                #if {c for c in n.leaf}.intersection('12345678'))
                if n.leaf != n.leaf.translate(_ROTATE45_VALIDATION_TABLE):
                    self._error_information = ErrorInformation(
                        self._statement_string.strip())
                    self._error_information.description = (
                        'rotate45 on specific squares')
                    return self._error_information
            r45ss = self._rotate45_specific_squares(n, rotate45stack)
            if r45ss:
                return r45ss
        if filter_.type == constants.ROTATE45:
            rotate45stack.pop()
        return None
        
    def process_statement(self, text):
        """Lex and parse the ChessQL statement."""

        # Assume no error, but set False indicating process_query_statement
        # has been called.
        self._error_information = False

        # First attempt treats whole text as a ChessQL statement.
        # Second attempt treats first line, of at least two, as the query's
        # name and the rest as a ChessQL statement.
        for rule in (('', text.strip()),
                     [t.strip()
                      for t in text.split(constants.NAME_DELIMITER, 1)]):
            
            if len(rule) == 1:

                # The second element of rule is being processed and the text in
                # rule[1] cannot be a valid ChessQL statement because it is the
                # text which was processed from the first element of rule.
                return False

            self._reset_state()
            self._description_string, self._statement_string = rule
            self.lex()
            self.parse()
            if self.validate():
                continue
            return True

        return None

    def is_statement(self):
        return not self._error_information

    def p_error(self):
        self._error_information = ErrorInformation(
            self._statement_string.strip())
        self._error_information.tokens = self.cql_tokens.copy()
        if self.tokens:
            self._error_information.next_token = self.tokens[0]
        return True

    def look_for_cql_parameters_or_body(self):
        if self.tokens:
            if self.cql_parameters is None:
                self.stack.append(self.p_cql)
                return
            if self.cql_filters is None:
                self.stack.append(self.b_cql)
                return
            self.p_error()
            return True

    def pop_top_of_stack(self):
        self.node_stack.pop()
        self.stack.pop()

    def p_numbers(self, stackexit=None):
        # Minimum and maximum are held in the range attribute.  In most cases
        # numbers are applied to the following filter, but year and elo are
        # notable exceptions which need not be processed by p_range().
        ns = self.node_stack
        token = Token(*self.tokens[0])
        if not token.number:
            if stackexit is None:
                self.pop_top_of_stack()
            else:
                self.stack[-1] = stackexit
            return False
        if len(ns[-1].range) > 1:
            self.stack.append(self.p_error)
            return True
        ns[-1].range.append(token.number)
        self.cql_tokens.append(self.tokens.pop(0))

    def b_numbers(self):
        if not self.tokens:
            self.b_end()
            return
        return self.p_numbers()

    def p_range(self, stackexit=None):
        # When processing a number as part of a range there must be at least
        # one more token: the object of the range.
        if self.p_numbers(stackexit=stackexit):
            return True
        if not len(self.tokens):
            self.stack.append(self.p_error)
            return True

    def b_range(self):
        # Hack so '... shift 8 left b ...' and similar come out correct.
        return self.p_range(stackexit=self.b_body)

    # p_* methods deal with 'cql(...)' part of 'cql(...)...' statement.
    # b_* methods deal with final '...' part of 'cql(...)...' statement .

    def p_cql(self):
        token = Token(*self.tokens[0])
        if token.cql != constants.CQL:
            self.stack.append(self.p_error)
            return True
        self.node_stack.append(self.create_node(token.cql))
        self.stack.append(self.p_left_parenthesis)
        self.cql_tokens.append(self.tokens.pop(0))

    def p_left_parenthesis(self):
        token = Token(*self.tokens[0])
        if token.left_parenthesis == constants.LEFT_PARENTHESIS_FILTER:
            self.add_argument(token.left_parenthesis, self.p_cql_parameter)
        else:
            self.stack.append(self.p_error)
            return True

    def p_cql_parameter(self):
        ns = self.node_stack
        token = Token(*self.tokens[0])
        if token.cql_parameter:
            if ns[-1].repeated_parameter(token.cql_parameter):
                self.stack.append(self.p_error)
                return True
            ns[-1].children.append(self.create_node(token.cql_parameter))
            ns.append(ns[-1].children[-1])
            if token.cql_parameter in (constants.INPUT, constants.OUTPUT):
                self.stack.append(self.p_allowed_strings_filename)
            elif token.cql_parameter == constants.VARIATIONS:
                ns[-1].leaf = True
                ns.pop() # Cancel the ns.append(...) before 'if' clause.
            elif token.cql_parameter == constants.GAMENUMBER:
                self.stack.append(self.p_gamenumber)
                ns[-1].leaf = ns[-1].range
            elif token.cql_parameter == constants.MATCHCOUNT:
                self.stack.append(self.p_matchcount)
                ns[-1].leaf = ns[-1].range
            else:
                self.stack.append(self.p_error)
                return True
            self.cql_tokens.append(self.tokens.pop(0))
        elif token.site_event:

            # Multiple event or site parameters are accepted by cql5.1, but
            # all of each must match.
            #if ns[-1].repeated_parameter(token.site_event):
            #    self.stack.append(self.p_error)
            #    return True
            
            self.add_argument(token.site_event, self.p_double_quoted_string)
        elif token.player:
            ns.append(ns[-1].get_repeatable_parameter(token.player,
                                                      self.create_node))
            self.stack.append(self.p_player_white_black)
            self.cql_tokens.append(self.tokens.pop(0))
        elif token.elo:
            ns.append(ns[-1].get_repeatable_parameter(token.elo,
                                                      self.create_node))
            self.stack.append(self.p_elo_white_black)
            self.cql_tokens.append(self.tokens.pop(0))
        elif token.year:

            # Multiple year parameters are accepted by cql5.1, but all years
            # must match.
            #if ns[-1].repeated_parameter(token.year):
            #    self.stack.append(self.p_error)
            #    return True
            
            self.add_argument(token.year, self.p_range)
            ns[-1].leaf = ns[-1].range
        elif token.silent:

            # Multiple silent parameters are accepted but it is not clear if
            # instruction is tied to all filters or just to next parameter.
            # Apply to all seems most likely but why allow multiple silent
            # parameters when all other parameters are restricted to a single
            # occurrence.
            #if ns[-1].repeated_parameter(token.silent):
            #    self.stack.append(self.p_error)
            #    return True
            
            self.add_argument_leaf(token.silent, True)
        elif token.sort:
            if ns[-1].repeated_parameter(token.sort):
                self.stack.append(self.p_error)
                return True
            self.add_argument(token.sort, self.p_sort_matchcount)
        elif token.result:

            # Multiple result parameters are accepted by cql5.1 but all results
            # must match.
            #if ns[-1].repeated_parameter(token.result):
            #    self.stack.append(self.p_error)
            #    return True

            self.add_argument(token.result, self.p_allowed_strings_result)
        elif token.right_parenthesis == constants.RIGHT_PARENTHESIS_TYPE:
            self.pop_top_of_stack()
            if len(ns) != 1:
                self.stack.append(self.p_error)
                return True
            if ns[-1].type != constants.CQL:
                self.stack.append(self.p_error)
                return True
            self.cql_parameters = ns[-1]
            self.pop_top_of_stack()
            self.stack.pop()
            self.cql_tokens.append(self.tokens.pop(0))
        else:
            self.stack.append(self.p_error)
            return True

    def p_allowed_strings_filename(self):
        token = Token(*self.tokens[0])
        if not token.allowed_strings.endswith(constants.PGN_FILE_VALUE):
            self.stack.append(self.p_error)
            return True
        self.node_stack[-1].leaf = token.allowed_strings
        self.pop_top_of_stack()
        self.cql_tokens.append(self.tokens.pop(0))

    def p_allowed_strings_result(self):
        token = Token(*self.tokens[0])
        if token.allowed_strings.endswith(constants.PGN_FILE_VALUE):
            self.stack.append(self.p_error)
            return True
        self.node_stack[-1].leaf = token.allowed_strings
        self.pop_top_of_stack()
        self.cql_tokens.append(self.tokens.pop(0))

    def b_allowed_strings_result(self):
        if not self.tokens:
            self.b_end()
            return
        return self.p_allowed_strings_result()

    def b_allowed_strings_flipcolor_result(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.allowed_strings.endswith(constants.PGN_FILE_VALUE):
            self.stack.append(self.p_error)
            return True
        self.node_stack[-1].leaf = token.allowed_strings
        self.pop_top_of_stack()

        # Extra pop-op, compared with p_allowed_strings_result to reverse the
        # push-op done for flipcolor.  Now looks like a mistake to press
        # p_allowed_strings_result into all three cases.
        self.pop_top_of_stack()

        self.cql_tokens.append(self.tokens.pop(0))

    def p_gamenumber(self):
        token = Token(*self.tokens[0])
        if not token.number:
            self.stack.append(self.p_error)
            return True
        self.stack[-1] = self.p_range

    def p_matchcount(self):
        token = Token(*self.tokens[0])
        if not token.number:
            self.stack.append(self.p_error)
            return True
        self.stack[-1] = self.p_range

    def p_double_quoted_string(self):
        token = Token(*self.tokens[0])
        if not token.double_quoted_string:
            self.stack.append(self.p_error)
            return True
        self.node_stack[-1].leaf = token.double_quoted_string
        self.pop_top_of_stack()
        self.cql_tokens.append(self.tokens.pop(0))

    def b_double_quoted_string(self):
        if not self.tokens:
            self.b_end()
            return
        return self.p_double_quoted_string()

    def p_sort_matchcount(self):
        token = Token(*self.tokens[0])
        if not token.cql_parameter == constants.MATCHCOUNT:
            self.stack.append(self.p_error)
            return True
        self.node_stack[-1].leaf = True
        self.pop_top_of_stack()

    # Differs from b_player_white_black due to rules for mixing parameters.
    def p_player_white_black(self):
        ns = self.node_stack
        token = Token(*self.tokens[0])
        if token.white_black_keywords:
            if (ns[-1].repeated_parameter(token.white_black_keywords) or
                ns[-1].leaf
                ):
                self.stack.append(self.p_error)
                return True
            self.add_argument(token.white_black_keywords,
                              self.p_double_quoted_string)
        elif token.double_quoted_string:
            if len(ns[-1].children):
                self.stack.append(self.p_error)
                return True
            if ns[-1].leaf:
                self.stack.append(self.p_error)
                return True
            ns.append(ns[-1])
            self.stack.append(self.p_double_quoted_string)
        elif ns[-1].type == constants.PLAYER:
            self.pop_top_of_stack()
        else:
            self.stack.append(self.p_error)
            return True

    # Differs from p_elo_white_black_body following rules for mixing parameters.
    # Uses p_range rather than p_numbers.
    def p_elo_white_black(self):
        ns = self.node_stack
        token = Token(*self.tokens[0])
        if token.white_black_keywords:
            if (ns[-1].repeated_parameter(token.white_black_keywords) or
                ns[-1].range
                ):
                self.stack.append(self.p_error)
                return True
            self.add_argument(token.white_black_keywords, self.p_numbers)
            ns[-1].leaf = ns[-1].range
        elif token.number:
            if len(ns[-1].children):
                self.stack.append(self.p_error)
                return True
            if ns[-1].range:
                self.stack.append(self.p_error)
                return True
            ns.append(ns[-1])
            self.stack.append(self.p_range)
            ns[-1].leaf = ns[-1].range
        elif ns[-1].type == constants.ELO:
            self.pop_top_of_stack()
        else:
            self.stack.append(self.p_error)
            return True

    # p_* methods deal with 'cql(...)' part of 'cql(...)...' statement.
    # b_* methods deal with final '...' part of 'cql(...)...' statement .

    def b_pop_top_of_stack(self):
        self.pop_top_of_stack()

    def b_pop_nested_stack(self):
        while True:
            if self.node_stack[-1].type in REAL_BRACES:
                break
            self.node_stack[-1].derive_filter_type_from_children()
            self.b_pop_top_of_stack()

    def b_pop_nested_stack_to_implied_brace(self):
        while True:
            if self.node_stack[-1].type in IMPLIED_BRACES:
                break
            self.node_stack[-1].derive_filter_type_from_children()
            self.b_pop_top_of_stack()

    def b_pop_top_of_stack_and_nested(self):

        # Caller is responsible for setting self.node_stack[-1].setfilter to
        # fit b_pop_top_of_stack. 
        self.b_pop_top_of_stack()
        self.b_pop_nested_stack()

    def b_pop_variables_stack(self):
        for v in self.variables_stack[-1]:
            del self.variables[v]
        self.variables_stack.pop()

    # Intend to use this to frame square and piece filters
    # square variable_name in in_set filter1 filter2 ...
    # For example
    # shift square $x in h1-8 attack ( R $x ) attack ( $x K )
    # is different to
    # shift { square $x in h1-8 attack ( R $x ) } attack ( $x K )
    # because the scope of square is limited by {} in the second version.
    def b_cql(self):
        self.node_stack.append(self.create_node(constants.CQL))
        self.stack.append(self.b_body)
        self.variables_stack.append(set())

    def b_body(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        self.b_collapse_filters_stack()
        return self.add_cql_body(token, self.b_body)

    def b_piece_square_in_set_body(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        self.b_collapse_filters_stack()
        return self.add_piece_square_in_set_body(
            token, self.b_piece_square_in_set_body)

    def b_collapse_filters_stack(self):
        # Collapse stack at end of filters chain before processing token.
        # Originally first thing in add_cql_body() but needs to be done before
        # this and add_set_body() and add_piece_square_in_set_body() calls.
        if self.node_stack[-1].type in RAY_FILTERS:
            self.stack[-1] = self.b_pop_top_of_stack

    def b_collapse_parameters_stack(self):
        # Collapse stack at end of 'or' and 'on' sequences after parameters
        # such as 'from' and 'to'
        if not self.tokens:
            return
        token = Token(*self.tokens[0])
        while True:
            if self.node_stack[-1].type not in PARAMETER_BRACES:
                break
            if token.or_ or token.on:
                break
            self.b_pop_top_of_stack()

    def b_end(self):
        # Collapse stack for 'cql() not { ... }' and similar: 'not' is left on
        # stack at end of tokens in this example.
        self.b_pop_nested_stack()
        if len(self.node_stack) == 1:
            self.cql_filters = self.node_stack[-1]
            self.node_stack.pop()
            self.variables_stack.pop()

    def add_piece_square_in_set_body(self, token, b_method):
        # square and piece excluded because statements like:
        # 'square $x in square y$ in ...' are not allowed.
        if token.piece_designator:
            self.add_piece_designator(token)
        elif token.plain:
            if token.plain == constants.DARKSQUARES:
                self.add_plain_filter(token)
            elif token.plain == constants.LIGHTSQUARES:
                self.add_plain_filter(token)
            else:
                self.stack.append(self.p_error)
                return True
        elif token.not_:
            self.add_argument(token.not_, self.b_body)
        elif token.or_:
            if self.add_binary_argument(token.or_, b_method):
                return True
        elif token.on:
            if self.add_binary_argument(token.on, b_method):
                return True
        elif token.transform: # includes direction filters
            self.add_argument(token.transform, self.b_body)
        elif token.attack:
            self.add_argument(token.attack, self.b_attack)
        elif token.move:
            self.add_argument(token.move, self.b_move)
        elif token.between: # not listed as a set filter, but described so.
            self.add_argument(token.between, self.b_between)
        elif token.left_brace:
            self.variables_stack.append(set())
            self.add_argument(token.left_brace, self.b_body)
        elif token.right_brace:
            node_stack = self.node_stack
            stack = self.stack
            variables = self.variables
            variables_stack = self.variables_stack
            while True:
                if not node_stack:
                    stack.append(self.p_error)
                    return True
                elif node_stack[-1].type == constants.LEFT_BRACE_FILTER:
                    node_stack[-1].derive_brace_filter_type_from_children()
                    for v in variables_stack[-1]:
                        del variables[v]
                    variables_stack.pop()
                    node_stack.pop()
                    stack.pop()
                    break
                elif node_stack[-1].type == constants.CQL:
                    node_stack[-1].derive_brace_filter_type_from_children()
                    for v in variables_stack[-1]:
                        del variables[v]
                    variables_stack.pop()
                    node_stack.pop()
                    stack.pop()
                elif node_stack[-1].type == constants.NOT:
                    node_stack[-1].derive_brace_filter_type_from_children()
                    node_stack.pop()
                    stack.pop()
                else:
                    stack.append(self.p_error)
                    return True
            self.cql_tokens.append(self.tokens.pop(0))
            if len(self.tokens) == 0:
                self.b_pop_nested_stack()
        else:
            self.stack.append(self.p_error)
            return True

    def add_set_body(self, token, b_method):

        # Do not delegate plain filter to add_piece_square_in_set_body
        if token.plain:
            self.add_plain_filter(token)

        elif token.piece_square_variable:
            return self.add_piece_square_variable(token)
        else:
            return self.add_piece_square_in_set_body(token, b_method)

    def add_cql_body(self, token, b_method):
        if token.piece_square:
            self.add_argument(token.piece_square, self.b_piece_square_filter)
        elif token.number:
            self.node_stack.append(self.node_stack[-1])
            self.stack.append(self.b_range) # Hides a hack which needs fixing.
        elif token.countsquares_power:
            self.add_argument(token.countsquares_power,
                              self.b_countsquares_power)
        elif token.powerdifference:
            self.add_argument(token.powerdifference, self.b_powerdifference)
        elif token.next_previous:
            self.add_argument(token.next_previous, self.b_next_previous)
        elif token.ray:
            self.add_argument(token.ray, self.b_ray)
        elif token.relation:
            self.add_argument(token.relation, self.b_relation)
        elif token.elo:
            self.add_argument(token.elo, self.b_elo_white_black)
        elif token.player:
            self.add_argument(token.player, self.b_player_white_black)
        elif token.site_event:
            self.add_argument(token.site_event, self.b_double_quoted_string)
        elif token.result:
            if self.node_stack[-1].type == constants.FLIPCOLOR:
                self.add_argument(token.result,
                                  self.b_allowed_strings_flipcolor_result)
            else:
                self.add_argument(token.result, self.b_allowed_strings_result)
        elif token.year:
            self.add_argument(token.year, self.b_numbers)
            self.node_stack[-1].leaf = self.node_stack[-1].range
        elif token.cql_parameter == constants.GAMENUMBER:
            self.add_argument(token.cql_parameter, self.b_numbers)
            self.node_stack[-1].leaf = self.node_stack[-1].range
        elif token.mainline:
            self.add_argument_leaf(constants.PLAIN_FILTER, token.mainline)
            self.b_pop_nested_stack_to_implied_brace()
            self.b_collapse_parameters_stack()
        elif token.hascomment:
            self.add_argument(token.hascomment, self.b_double_quoted_string)
        elif token.silent:
            if len(self.tokens) < 2:
                self.stack.append(self.p_error)
                return True
            t = Token(*self.tokens[1])
            if t.next_previous or t.relation:
                self.add_argument_leaf(token.silent, True)
            else:
                self.stack.append(self.p_error)
                return True

        # Incomplete because there is no list of filters which are countable
        # without a range: there are some because the possibility is mentioned,
        # and the filter's documentation will say.
        #
        # Syntax of sort appears to be, with 'max' as default:
        # sort [max|min] ["Documentation string"] <countable filter>.
        #
        elif token.sort:
            if len(self.tokens) < 2:
                self.stack.append(self.p_error)
                return True
            t = ''.join(Token(*self.tokens[1]))
            if t in COUNTABLE_FILTERS:
                self.add_argument_leaf(token.sort, True)
            elif t in COUNTABLE_RANGE_FILTERS:
                self.add_argument_leaf(token.sort, True)
            else:
                self.stack.append(self.p_error)
                return True

        # Some set filters may not be such if qualified by a range.  This is
        # acceptable because the point is reliably identifying tokens which
        # can be ignored: if it turns out that 'comment' should not have been
        # used it does not matter because comment filters are ignored.
        elif token.comment:
            if len(self.tokens) < 2:
                self.stack.append(self.p_error)
                return True
            t = Token(*self.tokens[1])
            if t.double_quoted_string:
                self.add_argument_leaf(token.comment, t.double_quoted_string)
                self.cql_tokens.append(self.tokens.pop(0))
            elif t.piece_designator:
                self.add_argument_leaf(token.comment, True)

            # Default action for any other set filter.
            # Dihedral and shift transforms have been added to SET_FILTERS
            # since this was written: it may be incorrect now.
            elif ''.join(t) in constants.SET_FILTER:
                self.add_argument_leaf(token.comment, True)

            else:
                self.stack.append(self.p_error)
                return True

        else:
            return self.add_set_body(token, b_method)

    def add_re_cql_body(self, token, b_method):
        #
        # Copied from http://www.gadycosteff.com/cql/doc/next.html (cql5.1)
        #
        # next-filter := 'next' opt-range '(' constituent+ ')'
        # previous-filter := 'previous' opt-range '(' constituent+ ')'
        # constituent := filter
        #              | filter '*'
        #              | filter '+'
        #              | filter '?'
        #              | '(' filter-list ')'
        #
        # next2 and previous2 have the same syntax.
        #
        if token.left_parenthesis:
            self.add_left_parenthesis(token)
            self.stack.append(self.b_one_or_more_filters)
        elif token.repeat_operators:
            children = self.node_stack[-1].children
            if not children:
                self.stack.append(self.p_error)
                return True
            if children[-1].repeat:
                self.stack.append(self.p_error)
                return True
            if children[-1].type == constants.LEFT_PARENTHESIS_FILTER:
                self.stack.append(self.p_error)
                return True
            children[-1].repeat = token.repeat_operators
            self.cql_tokens.append(self.tokens.pop(0))
        else:
            return self.add_cql_body(token, b_method)

    def add_piece_designator(self, token):
        c = self.node_stack[-1].children
        c.append(self.create_node(constants.PIECE_DESIGNATOR_FILTER))
        c[-1].leaf = token.piece_designator
        c[-1].setfilter = True
        self.b_pop_nested_stack_to_implied_brace()
        self.cql_tokens.append(self.tokens.pop(0))
        self.b_collapse_parameters_stack()

    def add_left_parenthesis(self, token):
        self.node_stack[-1].children.append(
            self.create_node(token.left_parenthesis))
        self.node_stack.append(self.node_stack[-1].children[-1])
        self.variables_stack.append(set())
        self.cql_tokens.append(self.tokens.pop(0))

    def add_piece_square_variable(self, token):
        psv = token.piece_square_variable
        if psv not in self.variables:
            self.stack.append(self.p_error)
            return True
        self.node_stack[-1].children.append(self.create_node(psv[0]))
        self.node_stack[-1].children[-1].leaf = self.variables[psv]
        self.b_pop_nested_stack()
        self.cql_tokens.append(self.tokens.pop(0))

    def add_plain_filter(self, token):
        c = self.node_stack[-1].children
        c.append(self.create_node(constants.PLAIN_FILTER))
        c[-1].leaf = token.plain
        if token.plain in (constants.DARKSQUARES, constants.LIGHTSQUARES):
            c[-1].setfilter = True
        else:
            c[-1].setfilter = False
        self.b_pop_nested_stack_to_implied_brace()
        self.cql_tokens.append(self.tokens.pop(0))
        self.b_collapse_parameters_stack()

    def add_move_from_to_enpassantsquare_parameter(self, token):
        n = self.create_node(token.move_parameter)
        self.node_stack[-1].children[-1].children.append(n)
        self.cql_tokens.append(self.tokens.pop(0))
        self.node_stack.append(n)
        self.stack.append(self.b_body)
        self.variables_stack.append(set())

    # 'K' '[kb]' 'k or b' 'k on b' are acceptable values for promote parameter
    # but 'a1' 'ka1' 'shift k' are not.
    # Separate method to be done.
    add_move_promote_parameter = add_move_from_to_enpassantsquare_parameter

    def b_move(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        t = token.mainline
        if not t:
            t = token.next_previous
        if not t:
            t = token.move_parameter
        if len(self.node_stack[-1].children):
            if t:
                self.stack.append(self.p_error)
                return True
        elif t in MOVE_MODIFIERS:
            self.node_stack[-1].children.append(self.create_node(t))
            self.cql_tokens.append(self.tokens.pop(0))
        else:
            self.node_stack[-1].children.append(
                self.create_node(constants.NEXT))
        self.stack[-1] = self.b_move_from

    def b_move_from(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        self.stack[-1] = self.b_move_to
        if token.move_parameter == constants.FROM:
            self.add_move_from_to_enpassantsquare_parameter(token)

    def b_move_to(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        self.stack[-1] = self.b_move_promote
        if token.move_parameter == constants.TO:
            self.add_move_from_to_enpassantsquare_parameter(token)

    def b_move_promote(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        self.stack[-1] = self.b_move_enpassantsquare
        if token.move_parameter == constants.PROMOTE:
            self.add_move_promote_parameter(token)

    def b_move_enpassantsquare(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.move_parameter == constants.ENPASSANTSQUARE:
            self.add_move_from_to_enpassantsquare_parameter(token)
            return
        elif token.move_parameter == constants.ENPASSANT:
            n = self.create_node(constants.ENPASSANTSQUARE)
            self.node_stack[-1].children[-1].children.append(n)
            n.leaf = 'a-h1-8'
            self.cql_tokens.append(self.tokens.pop(0))
        self.pop_top_of_stack()

    def b_two_set_filters(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.right_parenthesis:
            tns = self.node_stack[-1]
            if tns.type != constants.LEFT_PARENTHESIS_FILTER:
                self.stack.append(self.p_error)
                return True

            # Exactly two set-filters required.
            elif len(tns.children) != 2:
                self.stack.append(self.p_error)
                return True

            if not tns.set_filter_type_all_children_setfilters():
                self.stack.append(self.p_error)
                return True
            self.b_pop_variables_stack()
            self.b_pop_top_of_stack()
            self.cql_tokens.append(self.tokens.pop(0))

        # Exactly two set-filters required.
        elif len(self.node_stack[-1].children) > 1:
            self.stack.append(self.p_error)
            return True

        else:
            self.b_collapse_filters_stack()
            return self.add_set_body(token, self.b_two_set_filters)

    def b_one_set_filter(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])

        # Exactly one set-filter required.
        tns = self.node_stack[-1]
        c = len(tns.children)
        if c > 1:
            self.stack.append(self.p_error)
            return True
        elif c:
            if not tns.set_filter_type_all_children_setfilters():
                self.stack.append(self.p_error)
                return True
            self.b_pop_top_of_stack()

        else:
            self.b_collapse_filters_stack()
            return self.add_set_body(token, self.b_one_set_filter)

    def b_two_or_more_set_filters(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.right_parenthesis:
            tns = self.node_stack[-1]
            if tns.type != constants.LEFT_PARENTHESIS_FILTER:
                self.stack.append(self.p_error)
                return True
            elif len(tns.children) < 2:
                self.stack.append(self.p_error)
                return True
            if not tns.set_filter_type_all_children_setfilters():
                self.stack.append(self.p_error)
                return True
            self.b_pop_variables_stack()
            self.b_pop_top_of_stack()
            self.cql_tokens.append(self.tokens.pop(0))
        else:
            self.b_collapse_filters_stack()
            return self.add_set_body(token, self.b_two_or_more_set_filters)

    def b_one_or_more_re_set_filters(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.right_parenthesis:
            tns = self.node_stack[-1]
            if tns.type != constants.LEFT_PARENTHESIS_FILTER:
                self.stack.append(self.p_error)
                return True
            elif len(tns.children) < 1:
                self.stack.append(self.p_error)
                return True
            if not tns.set_filter_type_all_children_setfilters():
                self.stack.append(self.p_error)
                return True
            self.b_pop_variables_stack()
            self.b_pop_top_of_stack()
            self.cql_tokens.append(self.tokens.pop(0))
        else:
            self.b_collapse_filters_stack()
            return self.add_re_cql_body(
                token, self.b_one_or_more_re_set_filters)

    def b_one_or_more_filters(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.right_parenthesis:
            tns = self.node_stack[-1]
            if tns.type != constants.LEFT_PARENTHESIS_FILTER:
                self.stack.append(self.p_error)
                return True
            elif len(tns.children) < 1:
                self.stack.append(self.p_error)
                return True
            if not tns.set_filter_type_all_children_setfilters():
                self.stack.append(self.p_error)
                return True
            self.b_pop_variables_stack()
            self.b_pop_top_of_stack()
            self.cql_tokens.append(self.tokens.pop(0))
        else:
            self.b_collapse_filters_stack()
            return self.add_cql_body(token, self.b_one_or_more_filters)

    def b_attack(self):
        if not self.tokens:
            self.b_end()
            return
        elif len(self.node_stack[-1].children) == 1:
            self.b_pop_top_of_stack()
            return
        token = Token(*self.tokens[0])
        if token.left_parenthesis:
            self.add_left_parenthesis(token)
            self.stack.append(self.b_two_set_filters)
        elif token.number:
            if self.node_stack[-1].range:
                self.stack.append(self.p_error)
                return True
            self.node_stack.append(self.node_stack[-1])
            self.stack.append(self.p_range)
        else:
            self.stack.append(self.p_error)
            return True

    def b_between(self):
        if not self.tokens:
            self.b_end()
            return
        elif len(self.node_stack[-1].children) == 1:
            self.b_pop_top_of_stack()
            return
        token = Token(*self.tokens[0])
        if token.left_parenthesis:
            self.add_left_parenthesis(token)
            self.stack.append(self.b_two_set_filters)
        else:
            self.stack.append(self.p_error)
            return True

    def b_countsquares_power(self):
        if not self.tokens:
            self.b_end()
            return
        elif len(self.node_stack[-1].children) == 1:
            self.b_pop_top_of_stack()
            return
        token = Token(*self.tokens[0])
        if token.number:
            if self.node_stack[-1].range:
                self.stack.append(self.p_error)
                return True
            self.node_stack.append(self.node_stack[-1])
            self.node_stack.append(self.node_stack[-1])
            self.stack.append(self.b_one_set_filter)
            self.stack.append(self.p_range)
        else:
            self.stack.append(self.p_error)
            return True

    def b_powerdifference(self):
        if not self.tokens:
            self.b_end()
            return
        elif len(self.node_stack[-1].children) == 1:
            self.b_pop_top_of_stack()
            return
        token = Token(*self.tokens[0])
        if token.left_parenthesis:
            if not self.node_stack[-1].range:
                self.stack.append(self.p_error)
                return True
            self.add_left_parenthesis(token)
            self.stack.append(self.b_two_set_filters)
        elif token.number:
            if self.node_stack[-1].range:
                self.stack.append(self.p_error)
                return True
            self.node_stack.append(self.node_stack[-1])
            self.stack.append(self.p_range)
        else:
            self.stack.append(self.p_error)
            return True

    def b_ray(self):
        if not self.tokens:
            self.b_end()
            return
        elif len(self.node_stack[-1].children) == 1:
            self.b_pop_top_of_stack()
            return
        token = Token(*self.tokens[0])
        if token.left_parenthesis:
            self.add_left_parenthesis(token)
            self.stack.append(self.b_two_or_more_set_filters)
        elif token.number:
            if self.node_stack[-1].range:
                self.stack.append(self.p_error)
                return True
            self.node_stack.append(self.node_stack[-1])
            self.stack.append(self.p_range)

        # These can be filters by themselves, when their child is never a '(',
        # but are direction keywords for the ray filter here.
        elif token.attack:
            self.add_argument(token.attack, self.b_ray)
        elif token.transform in constants.DIRECTION_FILTER:
            self.add_argument(token.transform, self.b_ray)

        else:
            self.stack.append(self.p_error)
            return True

    def b_next_previous(self):
        if not self.tokens:
            self.b_end()
            return
        elif len(self.node_stack[-1].children) == 1:
            self.b_pop_top_of_stack()
            return
        token = Token(*self.tokens[0])
        if token.left_parenthesis:
            self.add_left_parenthesis(token)
            self.stack.append(self.b_one_or_more_re_set_filters)
        elif token.number:
            if self.node_stack[-1].range:
                self.stack.append(self.p_error)
                return True
            self.node_stack.append(self.node_stack[-1])
            self.stack.append(self.p_range)
        else:
            self.stack.append(self.p_error)
            return True

    def b_relation(self):
        # Copied from http://www.gadycosteff.com/cql/doc/relation.html (cql5.1)
        # relation := 'relation' targetfilters relationparameters
        # targetfilters := filter*
        # relationparameters := relation_parameter+
        #
        # The b_relation_*() methods make the relation syntax equivalent to
        # relation := 'relation' '(' targetfilters relationparameters ')' ...
        # because filter can be {...} and relation_parameter can be (...).
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        t = token.relation_parameter
        if t in RELATION_ECHO_PARAMETERS:
            self.stack[-1] = self.b_relation_parameter
        elif t:
            self.stack.append(self.p_error)
            return True
        elif token.left_parenthesis:
            self.stack[-1] = self.b_relation_parameter
        else:
            return self.add_cql_body(token, self.b_relation)

    def b_relation_parameter(self):
        # Assume only calls are via b_relation().
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        t = token.relation_parameter
        if t in RELATION_ECHO_PARAMETERS:
            self.add_argument(t, self.b_relation_parameter_left_parenthesis)
        elif t:
            self.stack.append(self.p_error)
            return True
        elif token.left_parenthesis:
            self.stack[-1] = self.b_relation_parameter_left_parenthesis
        else:
            # relation is treated as implying parentheses because '(...)' and
            # '{...}' can repeat as part of relation filter.
            self.node_stack[-1].setfilter = False
            self.b_pop_top_of_stack_and_nested()

    def b_relation_parameter_left_parenthesis(self):
        # Assume only calls are via b_relation_parameter().
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.right_parenthesis:
            self.stack[-1] = self.b_relation_parameter
            self.cql_tokens.append(self.tokens.pop(0))
            if not self.tokens:
                if self.node_stack[-1].type == constants.RELATION:
                    self.b_pop_top_of_stack()
            return
        elif not token.left_parenthesis:
            self.stack.append(self.p_error)
            return True
        self.add_argument(token.left_parenthesis,
                          self.b_relation_parameter_type)

    def b_relation_parameter_type(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.relation_parameter in RELATION_LCA_RANGE_PARAMETERS:
            self.add_argument(token.relation_parameter, self.p_range)
            self.node_stack[-1].leaf = self.node_stack[-1].range
        elif token.relation_parameter in RELATION_LCA_PLAIN_PARAMETERS:
            self.add_argument_leaf(constants.RELATION_PARAMETER_NAME,
                                   token.relation_parameter)
        elif token.relation_parameter == constants.TOMOVE:
            self.add_argument(token.relation_parameter,
                              self.b_relation_tomove_argument)
        elif token.relation_parameter in RELATION_SQUARE_PARAMETERS:
            if token.relation_parameter in RELATION_TOMOVE_ARGUMENTS:
                self.add_argument(token.relation_parameter,
                                  self.b_relation_square_tomove_argument)
            else:
                self.add_argument(token.relation_parameter,
                                  self.b_one_set_filter)
        elif token.right_parenthesis:
            self.pop_top_of_stack()
        else:
            self.stack.append(self.p_error)
            return True

    def b_relation_tomove_argument(self):
        if not self.tokens:
            self.b_end()
            return
        token = Token(*self.tokens[0])
        if token.relation_parameter in RELATION_TOMOVE_ARGUMENTS:
            self.node_stack[-1].leaf = token.relation_parameter
            self.cql_tokens.append(self.tokens.pop(0))
            if not self.tokens:
                self.stack.append(self.p_error)
                return True
            if not Token(*self.tokens[0]).right_parenthesis:
                self.stack.append(self.p_error)
                return True
            self.stack[-1] = self.b_relation_parameter_type
        else:
            self.stack.append(self.p_error)
            return True

    def b_relation_square_tomove_argument(self):
        if not self.tokens:
            self.b_end()
            return
        ns = self.node_stack
        if not ns[-1].range:
            ns.append(ns[-1])
            self.stack.append(self.p_numbers)
            return
        ns[-1].leaf = ns[-1].range
        ns[-1].setfilter = False
        self.b_pop_top_of_stack_and_nested()

    def b_elo_white_black(self):
        if not self.tokens:
            self.b_end()
            return
        ns = self.node_stack
        token = Token(*self.tokens[0])
        if token.white_black_keywords:
            if ns[-1].range:
                self.stack.append(self.p_error)
                return True
            self.add_argument(token.white_black_keywords, self.b_numbers)
            ns[-1].leaf = ns[-1].range
        elif token.number:
            if len(ns[-1].children):
                self.stack.append(self.p_error)
                return True
            ns.append(ns[-1])
            self.stack.append(self.b_numbers)
            ns[-1].leaf = ns[-1].range
        elif ns[-1].type == constants.ELO:
            self.pop_top_of_stack()
        else:
            self.stack.append(self.p_error)
            return True

    def b_player_white_black(self):
        if not self.tokens:
            self.b_end()
            return
        ns = self.node_stack
        token = Token(*self.tokens[0])
        if token.white_black_keywords:
            if ns[-1].leaf:
                self.stack.append(self.p_error)
                return True
            self.add_argument(token.white_black_keywords,
                              self.p_double_quoted_string)
        elif token.double_quoted_string:
            if len(ns[-1].children):
                self.stack.append(self.p_error)
                return True
            ns.append(ns[-1])
            self.stack.append(self.p_double_quoted_string)
        elif ns[-1].type == constants.PLAYER:
            self.pop_top_of_stack()
        else:
            self.stack.append(self.p_error)
            return True

    def _is_binary_operator_not_allowed(self):

        # Prior token can indicate with certainty 'or' or 'on' is not allowed,
        # but not that 'or' or 'on' is allowed.  For the latter case assume
        # stack has been collapsed to context expecting a filter.
        ct = self.cql_tokens
        if len(ct):
            if (ct[-1][constants.NOT_INDEX] or
                ct[-1][constants.OR_INDEX] or
                ct[-1][constants.ON_INDEX] or
                ct[-1][constants.LEFT_BRACE_INDEX]
                ):
                self.stack.append(self.p_error)
                return True
        else:
            self.stack.append(self.p_error)
            return True
        if not self.node_stack[-1].children and not self.node_stack[-1].leaf:
            self.stack.append(self.p_error)
            return True

    # Rename as add_argument_child?
    def add_argument(self, token_identity, method):
        ns = self.node_stack
        ns[-1].children.append(self.create_node(token_identity))
        self.node_stack.append(ns[-1].children[-1])
        self.stack.append(method)
        self.cql_tokens.append(self.tokens.pop(0))

    # Add method argument following add_argument style?
    def add_argument_leaf(self, token_identity, leaf):
        ns = self.node_stack
        ns[-1].children.append(self.create_node(token_identity))
        ns[-1].children[-1].leaf = leaf
        self.cql_tokens.append(self.tokens.pop(0))

    def add_binary_argument(self, token_identity, method):

        # Binding is:
        # { check <op> { Ra3 <op> { next ( any Qa2 ) <op> hascomment "eh?" } } }
        if self._is_binary_operator_not_allowed():
            return True
        n = self.create_node(token_identity)
        ns = self.node_stack
        n.children.append(ns[-1].children[-1])
        ns[-1].children[-1] = n
        ns.append(n)
        self.stack.append(method)
        self.cql_tokens.append(self.tokens.pop(0))

    def b_piece_square_filter(self):
        token = Token(*self.tokens[0])
        if token.piece_square_keywords == constants.ALL:
            if self.node_stack[-1].type != constants.SQUARE:
                self.stack.append(self.p_error)
                return True
            self.node_stack[-1].range.extend([token.piece_square_keywords] * 2)
            self.cql_tokens.append(self.tokens.pop(0))
            token = Token(*self.tokens[0])
        if not token.piece_square_variable:
            self.stack.append(self.p_error)
            return True
        if token.piece_square_variable in self.variables:
            self.stack.append(self.p_error)
            return True
        self.node_stack[-1].children.append(
            self.create_node(token.piece_square_variable))
        self.cql_tokens.append(self.tokens.pop(0))
        token = Token(*self.tokens[0])
        if token.piece_square_keywords != constants.IN:
            self.stack.append(self.p_error)
            return True
        self.node_stack.append(self.node_stack[-1].children[-1])
        self.stack.append(self.b_note_piece_square_variable)
        self.cql_tokens.append(self.tokens.pop(0))
        self.node_stack.append(self.create_node(constants.IN))
        self.stack.append(self.b_piece_square_in_set_body)
        self.node_stack[-2].children.append(self.node_stack[-1])

    def b_note_piece_square_variable(self):
        ns = self.node_stack
        if len(ns) < 2:
            self.stack.append(self.p_error)
            return True
        elif ns[-2].type not in VARIABLE_TYPES:
            self.stack.append(self.p_error)
            return True
        self.variables[ns[-1].type] = ns[-2]
        self.variables_stack[-1].add(ns[-1].type)
        self.b_pop_nested_stack()


class ErrorInformation(object):
    """Error information about a ChessQL query and report fomatters.

    This class assumes processing a query stops when the first error is met.

    The CQLStatement parse() and validate() methods return a ErrorInformation
    instance if any attribute other than _statement is bound to an object other
    than None.

    """

    def __init__(self, statement):
        """"""
        self._statement = statement
        self._tokens = None
        self._next_token = None
        self._description = ''

    @property
    def statement(self):
        return self._statement

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, value):
        if self._tokens is not None:
            raise StatementError('A token error already exists.')
        self._tokens = value

    @property
    def next_token(self):
        return self._next_token

    @next_token.setter
    def next_token(self, value):
        if self._next_token is not None:
            raise StatementError('A token error already exists.')
        self._next_token = value

    @property
    def description(self):
        return self._description

    @tokens.setter
    def description(self, value):
        if self._description:
            raise StatementError('A description error already exists.')
        self._description = value

    @property
    def error_found(self):
        return self._tokens is not None or self._description

    def get_error_report(self):
        """Return a str for error dialogue noting token being processed."""
        if self.error_found:
            if self._description:
                return ''.join(
                    ('Error processing statement:\n\n',
                     self._statement.strip(),
                     '\n\n',
                     self._description,
                     '.',
                     ))
            if self._next_token:
                next_token = ''.join(
                    ('\n\nThe item being processed is:\n\n',
                     ''.join(self._next_token),
                     ))
            else:
                next_token = ''
            return ''.join(
                ('Error, likely at or just after end of:\n\n',
                 ' '.join(''.join(t) for t in self._tokens),
                 '\n\nderived from:\n\n',
                 self._statement.strip(),
                 next_token,
                 ))
        return ''.join(('An unidentified error seems to exist in:\n\n',
                         self._statement.strip(),
                         ))

    def add_error_report_to_message(self, message, sep='\n\n'):
        """Return message extended with an error report."""
        return ''.join((message, sep, self.get_error_report()))
    

if __name__ == '__main__':


    # Interactive testing.

    import sys

    # Arguments are the stack[1] entries to cause tracing.
    # This entry will be either p_cql or b_cql at time of writing, referring
    # to parameters or body in 'cql ( <parameters> ) <body>'.

    _trace = frozenset(sys.argv[1:])
    del sys


    class Statement(Statement):

        def parse(self):
            if self._error_information:
                return
            self.stack.append(self.look_for_cql_parameters_or_body)
            while len(self.tokens):
                if self._trace_and_call_top_of_stack():
                    self._trace_and_call_top_of_stack()
                    break
            else:
                self._trace_and_call_top_of_stack()

        def _trace_and_call_top_of_stack(self):
            if len(self.stack) > 1:
                if self.stack[1].__name__ in _trace:
                    print(self._trace(self.stack[-1].__name__))
            return self.stack[-1]()

        def _trace_start(self, method_name):
            return ' '.join(('--', str(method_name)))

        def _trace_body(self):
            ts = [' '.join(('  ', str(len(self.variables)), 'variables'))]
            if self.variables:
                for s in sorted(self.variables):
                    ts.append(' '.join(('     ', s, str(self.variables[s]))))
            ts.append(' '.join(('  ',
                                str(len(self.variables_stack)),
                                'variables_stack')))
            for s in self.variables_stack:
                ts.append(' '.join(('     ', str(s))))
            ts.append(' '.join(('  ', str(len(self.stack)), 'stack')))
            for s in self.stack:
                try:
                    s = s.__name__
                except:
                    pass
                ts.append(' '.join(('     ', s)))
            ts.append(' '.join(('  ', str(len(self.node_stack)), 'node_stack')))
            for s in self.node_stack:
                ts.append(' '.join(('     ', str(s))))
            return '\n'.join(ts)

        def _trace_end(self):
            return '-- end'

        def _trace(self, method_name):
            return '\n'.join((self._trace_start(method_name),
                              self._trace_body(),
                              self._trace_end(),
                              ))


    token_map = {e:v for e, v in enumerate(constants.TOKEN_NAMES.split())}
    while True:
        try:
            s = input('cql> ')
        except EOFError as exc:
            print(exc)
            break
        except KeyboardInterrupt:
            print()
            break
        #if not s:
        #    continue
        try:
            cql = Statement()
            cql.process_statement(s)
            print()
            for t in cql.tokens:
                print(*[(v, token_map[e]) for e, v in enumerate(t) if v][0],
                      sep='\t')
            print(cql.cql_parameters)
            print(cql.cql_filters)
            print(cql.node_stack)
            print(cql.variables_stack)
            if cql.cql_error:
                print('error:', s)
            else:
                print('ok:', s)
            print()
        except RuntimeError as exc:
            print(exc)
