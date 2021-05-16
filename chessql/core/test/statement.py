# statement.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""statement tests for cql"""

import unittest
from copy import copy, deepcopy
import re
import collections

from .. import constants
from .. import statement
from .. import node


class Constants(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__raises(self):
        """"""
        pass

    def test____assumptions(self):
        """"""
        self.assertEqual(statement.CQL_PARAMETERS,
                         (r'output',
                          r'input',
                          r'gamenumber',
                          r'year',
                          r'silent',
                          r'player',
                          r'elo',
                          r'site',
                          r'event',
                          r'matchcount',
                          r'sort',
                          ))
        self.assertEqual(statement.RAY_DIRECTIONS,
                         frozenset(
                             (r'up',
                              r'down',
                              r'left',
                              r'right',
                              r'northeast',
                              r'northwest',
                              r'southeast',
                              r'southwest',
                              r'vertical',
                              r'horizontal',
                              r'diagonal',
                              r'orthogonal',
                              r'anydirection',
                              r'attack',
                              )))
        self.assertEqual(statement.TRANSFORM_FILTERS,
                         frozenset(
                             (r'flip',
                              r'flipdihedral',
                              r'fliphorizontal',
                              r'flipvertical',
                              r'flipcolor',
                              r'rotate45',
                              r'rotate90',
                              r'shift',
                              r'shifthorizontal',
                              r'shiftvertical',
                              )))
        self.assertEqual(statement.STAR_FILTERS,
                         frozenset(
                             (r'next\*',
                              r'previous\*',
                              )))
        self.assertEqual(statement.MOVE_MODIFIERS,
                         frozenset(
                             (r'mainline',
                              r'previous',
                              r'next',
                              r'empty',
                              )))
        self.assertEqual(statement.RELATION_ECHO_PARAMETERS,
                         frozenset(
                             (r'echoflip',
                              r'echoflipvertical',
                              r'echofliphorizontal',
                              r'echoshift',
                              r'echoshifthorizontal',
                              r'echoshiftvertical',
                              r'echorotate90',
                              )))
        self.assertEqual(statement.RELATION_TOMOVE_ARGUMENTS,
                         frozenset(
                             (r'match',
                              r'mismatch',
                              )))
        self.assertEqual(statement.RELATION_LCA_PLAIN_PARAMETERS,
                         frozenset(
                             (r'ancestor',
                              r'descendant',
                              )))
        self.assertIsInstance(statement.Token(*('',)*44), statement.Token)
        self.assertIs(statement.Statement.create_node, node.Node)


class StatementMethods(unittest.TestCase):

    def setUp(self):
        self.statement = statement.Statement()

    def tearDown(self):
        pass

    def expected_matches(self, match_spec):
        # Create list of matches in format produced by re.findall().
        em = []
        for t, p in match_spec:
            m = [''] * 44
            m[p] = t
            em.append(tuple(m))
        return em

    def keyword_error(
        self, keyword, method, nslen, poptokens=0, nextmethod=None):
        # For testing keywords in isolation.
        s = self.statement
        tokens = s.tokens.copy()
        cql_tokens = s.cql_tokens.copy()
        self.assertEqual(method(), True)
        self.assertEqual(len(s.node_stack), nslen)
        if nextmethod:
            if isinstance(nextmethod, list):
                self.assertEqual(s.stack, nextmethod)
            else:
                self.assertEqual(s.stack, [nextmethod])
        else:
            self.assertEqual(s.stack, [s.p_error])
        self.assertEqual(s.cql_tokens + s.tokens, cql_tokens + tokens)
        self.assertEqual(len(tokens) - poptokens, len(s.tokens))

    def keyword_ok(self,
                   keyword,
                   method,
                   nodestr,
                   nextmethod,
                   nslen,
                   poptokens=1,
                   method_return=None):
        # For testing keywords in isolation.
        s = self.statement
        tokens = s.tokens.copy()
        cql_tokens = s.cql_tokens.copy()
        self.assertEqual(method(), method_return)
        self.assertEqual(len(s.node_stack), nslen)
        if nslen:
            self.assertEqual(str(s.node_stack[0]), nodestr)
        if nextmethod:
            if isinstance(nextmethod, list):
                self.assertEqual(s.stack, nextmethod)
            else:
                self.assertEqual(s.stack, [nextmethod])
        else:
            self.assertEqual(s.stack, [])
        self.assertEqual(s.cql_tokens + s.tokens, cql_tokens + tokens)
        self.assertEqual(len(tokens) - poptokens, len(s.tokens))

    def keyword_reprocess_ok(
        self, keyword, method, nodestr, nextmethod, nslen):
        # For testing keywords in isolation.
        s = self.statement
        tokens = s.tokens.copy()
        cql_tokens = s.cql_tokens.copy()
        self.assertEqual(method(), None)
        self.assertEqual(len(s.node_stack), nslen)
        if nslen:
            self.assertEqual(str(s.node_stack[0]), nodestr)
        if nextmethod:
            if isinstance(nextmethod, list):
                self.assertEqual(s.stack, nextmethod)
            else:
                self.assertEqual(s.stack, [nextmethod])
        else:
            self.assertEqual(s.stack, [])
        self.assertEqual(s.cql_tokens + s.tokens, cql_tokens + tokens)
        self.assertEqual(len(tokens), len(s.tokens))

    def body_keyword_error(self, keyword, method, nslen):
        # For testing keywords in isolation.
        s = self.statement
        tokens = s.tokens.copy()
        cql_tokens = s.cql_tokens.copy()
        self.assertEqual(method(statement.Token(*s.tokens[0])), True)
        self.assertEqual(len(s.node_stack), nslen)
        self.assertEqual(s.stack, [s.p_error])
        self.assertEqual(s.cql_tokens + s.tokens, cql_tokens + tokens)
        self.assertEqual(len(tokens), len(s.tokens))

    def body_keyword_ok(
        self, keyword, method, nodestr, nextmethod, nslen, poptokens=1):
        # For testing keywords in isolation.
        s = self.statement
        tokens = s.tokens.copy()
        cql_tokens = s.cql_tokens.copy()
        self.assertEqual(method(statement.Token(*s.tokens[0])), None)
        self.assertEqual(len(s.node_stack), nslen)
        if nslen:
            self.assertEqual(str(s.node_stack[0]), nodestr)
        if nextmethod:
            if isinstance(nextmethod, list):
                self.assertEqual(s.stack, nextmethod)
            else:
                self.assertEqual(s.stack, [nextmethod])
        else:
            self.assertEqual(s.stack, [])
        self.assertEqual(s.cql_tokens + s.tokens, cql_tokens + tokens)
        self.assertEqual(len(tokens) - poptokens, len(s.tokens))

    def add_keyword_method_stackmethod(self,
                                       keyword,
                                       method,
                                       nodestr,
                                       next_,
                                       nslen,
                                       response,
                                       children=None,
                                       cql_tokens=None,
                                       extra_tokens=None,
                                       variables=None,
                                       node_stack=None,
                                       variable_stack=None,
                                       stack=None):
        # For testing keywords in isolation.
        s = self.statement
        if node_stack:
            s.node_stack.extend(node_stack)
        else:
            s.node_stack.append(statement.Statement.create_node('cql'))
        if children:
            s.node_stack[-1].children.extend(children)
        if variables:
            s.variables.update(variables)
        if variable_stack:
            s.variables_stack.extend(variable_stack)
        if not stack:
            stack = ['gash']
        else:
            stack.insert(0, 'gash')
        s.stack = stack.copy()
        s.tokens = self.expected_matches((keyword,))
        if extra_tokens:
            s.tokens.extend(self.expected_matches(extra_tokens))
        if cql_tokens:
            s.cql_tokens = self.expected_matches(cql_tokens)
        self.assertEqual(method(statement.Token(*s.tokens[0]), next_),
                         response)
        if next_:
            if isinstance(next_, list):
                stack.extend(next_)
            else:
                stack.append(next_)
            self.assertEqual(s.stack, stack)
        if nslen:
            self.assertEqual(str(s.node_stack[0]), nodestr)

    def test____init__(self):
        s = self.statement
        self.assertEqual(len(s.__dict__), 12)
        self.assertEqual(s._description_string, '')
        self.assertEqual(s._statement_string, '')
        self.assertEqual(s._error_information, None)
        self.assertEqual(s.tokens, None)
        self.assertEqual(s.cql_tokens, [])
        self.assertEqual(s.stack, [])
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.brace_parenthesis_stack, [])
        self.assertEqual(s.cql_parameters, None)
        self.assertEqual(s.cql_filters, None)
        self.assertEqual(s.variables, {})
        self.assertEqual(s.variables_stack, [])

    def test__reset_state(self):
        s = self.statement
        s._reset_state()
        self.assertEqual(len(s.__dict__), 12)
        self.assertEqual(hasattr(s, '_description_string'), True)
        self.assertEqual(hasattr(s, '_statement_string'), True)
        self.assertEqual(s._error_information, False)
        self.assertEqual(s.tokens, None)
        self.assertEqual(s.cql_tokens, [])
        self.assertEqual(s.stack, [])
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.brace_parenthesis_stack, [])
        self.assertEqual(s.cql_parameters, None)
        self.assertEqual(s.cql_filters, None)
        self.assertEqual(s.variables, {})
        self.assertEqual(s.variables_stack, [])

    def test_cql_error(self):
        s = self.statement
        self.assertIs(s.cql_error, s._error_information)

    def test_get_name_text(self):
        s = self.statement
        self.assertIs(s.get_name_text(), s._description_string)

    def test_get_name_statement_text(self):
        s = self.statement
        self.assertEqual(s.get_name_statement_text(), '\n')

    def test_get_statement_text(self):
        s = self.statement
        self.assertIs(s.get_statement_text(), s._statement_string)

    def test_lex_01_null_string(self):
        s = self.statement
        s._statement_string = ''
        s.lex()
        self.assertEqual(s._error_information, False)
        self.assertEqual(s.tokens, [])

    def test_lex_02_whitespace_string(self):
        s = self.statement
        s._statement_string = ' \n '
        s.lex()
        self.assertEqual(s._error_information, False)
        self.assertEqual(s.tokens, [])

    def test_lex_03_error_string(self):
        s = self.statement
        s._statement_string = 'qwerty'
        s.lex()
        self.assertEqual(s._error_information, None)
        self.assertEqual(s.tokens, self.expected_matches((('qwerty', 43),)))

    def test_lex_04_ok_string(self):
        s = self.statement
        s._statement_string = 'cql()'
        s.lex()
        self.assertEqual(s._error_information, None)
        self.assertEqual(s.tokens,
                         self.expected_matches((('cql', 5),
                                                ('(', 0),
                                                (')', 1),
                                                )))

    def test_parse_01_error(self):
        s = self.statement
        em = self.expected_matches((('cql', 5), ('(', 0), (')', 1),))
        s.tokens = em
        s._error_information = True
        s.parse()
        self.assertEqual(s.tokens, em)
        self.assertEqual(s.stack, [])
        self.assertEqual(s._error_information, True)

    def test_parse_02_no_tokens(self):
        s = self.statement
        s.tokens = []
        s._error_information = False
        s.parse()
        self.assertEqual(s.tokens, [])
        self.assertEqual(s._error_information, False)
        self.assertEqual(s.stack, [s.look_for_cql_parameters_or_body])

    def test_parse_03_error_tokens(self):
        s = self.statement
        em = self.expected_matches((('cql', 5), ('(', 0), (')', 1),))
        s.tokens = em.copy()
        s.parse()
        self.assertEqual(s.tokens, [])
        self.assertEqual(s.cql_tokens, em)
        self.assertEqual(s._error_information, None)
        self.assertIsInstance(s.cql_parameters, statement.Statement.create_node)
        self.assertEqual(s.cql_filters, None)

    def test_parse_04_ok_tokens(self):
        s = self.statement
        em = self.expected_matches((('cql', 5), ('(', 0), (')', 1), ('z', 6),))
        s.tokens = em.copy()
        s.parse()
        self.assertEqual(s.tokens, [])
        self.assertEqual(s.cql_tokens, em)
        self.assertEqual(s._error_information, None)
        self.assertIsInstance(s.cql_parameters, node.Node)
        self.assertIsInstance(s.cql_filters, statement.Statement.create_node)

    def test_validate_01_error(self):
        s = self.statement
        s._error_information = not bool(None)
        self.assertIs(s.validate(), s._error_information)

    def test_validate_02_ok(self):
        s = self.statement
        self.assertEqual(s.validate(), None)

    def test_process_statement_01_bad_token(self):
        s = self.statement
        self.assertEqual(s.process_statement('text'), False)
        self.assertIsInstance(s._error_information, statement.ErrorInformation)
        self.assertEqual(s.tokens, self.expected_matches((('text', 43),)))

    def test_process_statement_02_bad_token(self):
        s = self.statement
        self.assertEqual(s.process_statement('text\nmore'), None)
        self.assertIsInstance(s._error_information, statement.ErrorInformation)
        self.assertEqual(s.tokens,
                         self.expected_matches((('more', 43),)))

    def test_process_statement_03_ok(self):
        s = self.statement
        self.assertEqual(s.process_statement('cql()k'), True)
        self.assertEqual(s._error_information, False)

    def test_process_statement_04_ok(self):
        s = self.statement
        self.assertEqual(s.process_statement('text\ncql()k'), True)
        self.assertEqual(s._error_information, False)

    def test_is_statement_01_error(self):
        s = self.statement
        s._error_information = statement.ErrorInformation(s)
        self.assertEqual(s.is_statement(), False)

    def test_is_statement_01_ok(self):
        s = self.statement
        self.assertEqual(s.is_statement(), True)

    def test_p_error(self):
        s = self.statement
        s._statement_string = '  text  '
        s.cql_tokens = ['elements']
        self.assertEqual(s.p_error(), True)
        self.assertIsInstance(s._error_information, statement.ErrorInformation)
        self.assertEqual(s._error_information._statement, 'text')
        self.assertEqual(s._error_information.tokens, ['elements'])

    def test_look_for_cql_parameters_or_body_01_(self):
        s = self.statement
        self.assertEqual(s.look_for_cql_parameters_or_body(), None)
        self.assertEqual(bool(s.tokens), False)
        self.assertIs(s.cql_parameters, None)
        self.assertIs(s.cql_filters, None)
        self.assertEqual(s.stack, [])

    def test_look_for_cql_parameters_or_body_02_(self):
        s = self.statement
        s.cql_filters = []
        self.assertEqual(s.look_for_cql_parameters_or_body(), None)
        self.assertEqual(bool(s.tokens), False)
        self.assertIs(s.cql_parameters, None)
        self.assertIsNot(s.cql_filters, None)
        self.assertEqual(s.stack, [])

    def test_look_for_cql_parameters_or_body_03_(self):
        s = self.statement
        s.cql_parameters = []
        self.assertEqual(s.look_for_cql_parameters_or_body(), None)
        self.assertEqual(bool(s.tokens), False)
        self.assertIsNot(s.cql_parameters, None)
        self.assertIs(s.cql_filters, None)
        self.assertEqual(s.stack, [])

    def test_look_for_cql_parameters_or_body_04_(self):
        s = self.statement
        s.tokens = ['elements']
        self.assertEqual(s.look_for_cql_parameters_or_body(), None)
        self.assertEqual(bool(s.tokens), True)
        self.assertIs(s.cql_parameters, None)
        self.assertIs(s.cql_filters, None)
        self.assertEqual(s.stack, [s.p_cql])

    def test_look_for_cql_parameters_or_body_05_(self):
        s = self.statement
        s.tokens = ['elements']
        s.cql_filters = []
        self.assertEqual(s.look_for_cql_parameters_or_body(), None)
        self.assertEqual(bool(s.tokens), True)
        self.assertIs(s.cql_parameters, None)
        self.assertEqual(s.cql_filters, [])
        self.assertEqual(s.stack, [s.p_cql])

    def test_look_for_cql_parameters_or_body_06_(self):
        s = self.statement
        s.tokens = ['elements']
        s.cql_parameters = []
        self.assertEqual(s.look_for_cql_parameters_or_body(), None)
        self.assertEqual(bool(s.tokens), True)
        self.assertEqual(s.cql_parameters, [])
        self.assertIs(s.cql_filters, None)
        self.assertEqual(s.stack, [s.b_cql])

    def test_look_for_cql_parameters_or_body_07_(self):
        s = self.statement
        s.tokens = ['elements']
        s.cql_filters = []
        s.cql_parameters = []
        self.assertEqual(s.look_for_cql_parameters_or_body(), True)
        self.assertEqual(bool(s.tokens), True)
        self.assertEqual(s.cql_parameters, [])
        self.assertEqual(s.cql_filters, [])
        self.assertEqual(s.stack, [])

    def test_pop_top_of_stack_01_(self):
        s = self.statement
        s.node_stack.append('elements')
        s.stack.append('elements')
        self.assertEqual(s.pop_top_of_stack(), None)
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.stack, [])

    def test_pop_top_of_stack_02_(self):
        s = self.statement
        s.stack.append('elements')
        self.assertRaises(IndexError, s.pop_top_of_stack)
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.stack, ['elements'])

    def test_pop_top_of_stack_03_(self):
        s = self.statement
        s.node_stack.append('elements')
        self.assertRaises(IndexError, s.pop_top_of_stack)
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.stack, [])

    def test_pop_top_of_stack_04_(self):
        s = self.statement
        self.assertRaises(IndexError, s.pop_top_of_stack)
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.stack, [])

    def test_p_numbers_01_(self):
        s = self.statement
        s.node_stack.append('elements')
        s.stack.append('elements')
        s.tokens = self.expected_matches((('z', 6),))
        self.assertEqual(s.p_numbers(), False)
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.stack, [])
        self.assertEqual(s.tokens, self.expected_matches((('z', 6),)))
        self.assertEqual(s.cql_tokens, [])

    def test_p_numbers_02_(self):
        s = self.statement
        node = statement.Statement.create_node('number')
        s.node_stack.append(node)
        s.stack.append('elements')
        s.tokens = self.expected_matches((('x', 12),('y', 12),('z', 12),))
        self.assertEqual(s.p_numbers(), None)
        self.assertEqual(s.node_stack, [node])
        self.assertEqual(s.stack, ['elements'])
        self.assertEqual(s.tokens,
                         self.expected_matches((('y', 12),('z', 12),)))
        self.assertEqual(s.cql_tokens,
                         self.expected_matches((('x', 12),)))
        self.assertEqual(s.node_stack[-1].range, ['x'])
        self.assertEqual(s.p_numbers(), None)
        self.assertEqual(s.node_stack, [node])
        self.assertEqual(s.stack, ['elements'])
        self.assertEqual(s.tokens,
                         self.expected_matches((('z', 12),)))
        self.assertEqual(s.cql_tokens,
                         self.expected_matches((('x', 12),('y', 12),)))
        self.assertEqual(s.node_stack[-1].range, ['x', 'y'])
        self.assertEqual(s.p_numbers(), True)
        self.assertEqual(s.node_stack, [node])
        self.assertEqual(s.stack, ['elements', s.p_error])
        self.assertEqual(s.tokens,
                         self.expected_matches((('z', 12),)))
        self.assertEqual(s.cql_tokens,
                         self.expected_matches((('x', 12),('y', 12),)))
        self.assertEqual(s.node_stack[-1].range, ['x', 'y'])

    def test_b_numbers_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_numbers(), None)

    def test_b_numbers_02_(self):
        s = self.statement
        s.node_stack.append('elements')
        s.stack.append('elements')
        s.tokens = self.expected_matches((('z', 6),))
        self.assertEqual(s.b_numbers(), False)
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.stack, [])
        self.assertEqual(s.tokens, self.expected_matches((('z', 6),)))
        self.assertEqual(s.cql_tokens, [])

    def test_p_range_01_(self):
        s = self.statement
        node = statement.Statement.create_node('number')
        s.node_stack.append(node)
        s.stack.append('elements')
        s.tokens = self.expected_matches((('x', 12),('y', 12),('z', 12),))
        self.assertEqual(s.p_range(), None)
        self.assertEqual(s.node_stack, [node])
        self.assertEqual(s.stack, ['elements'])
        self.assertEqual(s.tokens,
                         self.expected_matches((('y', 12),('z', 12),)))
        self.assertEqual(s.cql_tokens,
                         self.expected_matches((('x', 12),)))
        self.assertEqual(s.node_stack[-1].range, ['x'])
        self.assertEqual(s.p_range(), None)
        self.assertEqual(s.node_stack, [node])
        self.assertEqual(s.stack, ['elements'])
        self.assertEqual(s.tokens,
                         self.expected_matches((('z', 12),)))
        self.assertEqual(s.cql_tokens,
                         self.expected_matches((('x', 12),('y', 12),)))
        self.assertEqual(s.node_stack[-1].range, ['x', 'y'])
        self.assertEqual(s.p_range(), True)
        self.assertEqual(s.node_stack, [node])
        self.assertEqual(s.stack, ['elements', s.p_error])
        self.assertEqual(s.tokens,
                         self.expected_matches((('z', 12),)))
        self.assertEqual(s.cql_tokens,
                         self.expected_matches((('x', 12),('y', 12),)))
        self.assertEqual(s.node_stack[-1].range, ['x', 'y'])

    def test_p_range_02_only_one_number_token(self):
        s = self.statement
        node = statement.Statement.create_node('number')
        s.node_stack.append(node)
        s.stack.append('elements')
        s.tokens = self.expected_matches((('x', 12),))
        self.assertEqual(s.p_range(), True)
        self.assertEqual(s.node_stack, [node])
        self.assertEqual(s.stack, ['elements', s.p_error])
        self.assertEqual(s.tokens, [])
        self.assertEqual(s.cql_tokens,
                         self.expected_matches((('x', 12),)))
        self.assertEqual(s.node_stack[-1].range, ['x'])

    def test_p_cql_01_(self):
        token = ('cqll', 5)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_cql, 0)

    def test_p_cql_02_(self):
        token = ('cql', 5)
        nodestr = '(cql, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql, nodestr, s.p_left_parenthesis, 1)

    def test_p_left_parenthesis_01_(self):
        token = ('gg', 0)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_left_parenthesis, 0)

    def test_p_left_parenthesis_02_(self):
        token = ('(', 0)
        nodestr = '(gash, [((, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_left_parenthesis, nodestr, s.p_cql_parameter, 2)

    def test_p_cql_parameter_01_input_output(self):
        token = ('input', 7)
        nodestr = '(gash, [(input, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_allowed_strings_filename, 2)

    def test_p_cql_parameter_02_variations(self):
        token = ('variations', 7)
        nodestr = '(gash, [(variations, [], True, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, None, 1)

    def test_p_cql_parameter_03_gamenumber(self):
        token = ('gamenumber', 7)
        nodestr = '(gash, [(gamenumber, [], [], None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_gamenumber, 2)

    def test_p_cql_parameter_04_matchcount(self):
        token = ('matchcount', 7)
        nodestr = '(gash, [(matchcount, [], [], None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_matchcount, 2)

    def test_p_cql_parameter_05_repeated(self):
        # To be done.
        token = ('input', 7)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))

    def test_p_cql_parameter_06_error(self):
        token = ('gash', 7)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_cql_parameter, 2)

    def test_p_cql_parameter_07_site_event(self):
        token = ('event', 35)
        nodestr = '(gash, [(event, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_double_quoted_string, 2)

    def test_p_cql_parameter_08_site_event_repeated(self):
        # To be done.
        token = ('event', 35)

    def test_p_cql_parameter_09_player(self):
        token = ('player', 27)
        nodestr = '(gash, [(player, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_player_white_black, 2)

    def test_p_cql_parameter_10_elo(self):
        token = ('elo', 19)
        nodestr = '(gash, [(elo, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_elo_white_black, 2)

    def test_p_cql_parameter_11_year(self):
        token = ('year', 33)
        nodestr = '(gash, [(year, [], [], None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_range, 2)

    def test_p_cql_parameter_12_year_repeated(self):
        # To be done.
        token = ('year', 33)

    def test_p_cql_parameter_13_silent(self):
        token = ('silent', 34)
        nodestr = '(gash, [(silent, [], True, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, None, 1)

    def test_p_cql_parameter_14_silent_repeated(self):
        # To be done.
        token = ('silent', 34)
        
    def test_p_cql_parameter_15_sort(self):
        token = ('sort', 32)
        nodestr = '(gash, [(sort, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_sort_matchcount, 2)

    def test_p_cql_parameter_16_sort_repeated(self):
        # To be done.
        token = ('sort', 32)

    def test_p_cql_parameter_17_result(self):
        token = ('result', 31)
        nodestr = '(gash, [(result, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, s.p_allowed_strings_result, 2)

    def test_p_cql_parameter_18_result_repeated(self):
        # To be done.
        token = ('result', 31)

    def test_p_cql_parameter_19_right_parenthesis(self):
        token = (')', 1)
        nodestr = '(cql, [], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.stack.append('gash')
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_cql_parameter, nodestr, None, 0)

    def test_p_cql_parameter_20_right_parenthesis_len(self):
        token = (')', 1)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_cql_parameter, 0)

    def test_p_cql_parameter_21_right_parenthesis_type(self):
        token = (')', 1)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cqll'))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_cql_parameter, 1)

    def test_p_cql_parameter_22_other_token(self):
        token = ('z', 20)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_cql_parameter, 0)

    def test_p_allowed_strings_filename_01_ok(self):
        token = ('file.pgn', 41)
        nodestr = '(gash, [], file.pgn, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack.append(s.node_stack[-1])
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_allowed_strings_filename, nodestr, None, 1)

    def test_p_allowed_strings_filename_02_error(self):
        token = ('file', 41)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_allowed_strings_filename, 0)

    def test_p_allowed_strings_result_01_ok(self):
        token = ('file', 41)
        nodestr = '(gash, [], file, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack.append(s.node_stack[-1])
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_allowed_strings_result, nodestr, None, 1)

    def test_p_allowed_strings_result_02_error(self):
        token = ('file.pgn', 41)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_allowed_strings_result, 0)

    def test_b_allowed_strings_result_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_allowed_strings_result(), None)

    def test_b_allowed_strings_result_02_ok(self):
        token = ('file', 41)
        nodestr = '(gash, [], file, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack.append(s.node_stack[-1])
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.b_allowed_strings_result, nodestr, None, 1)

    def test_p_gamenumber_01_ok(self):
        token = ('10', 12)
        s = self.statement
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_reprocess_ok(token, s.p_gamenumber, None, s.p_range, 0)

    def test_p_gamenumber_02_error(self):
        token = ('10', 20)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_gamenumber, 0)

    def test_p_matchcount_01_ok(self):
        token = ('10', 12)
        s = self.statement
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_reprocess_ok(token, s.p_matchcount, None, s.p_range, 0)

    def test_p_matchcount_02_error(self):
        token = ('10', 20)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_matchcount, 0)

    def test_p_double_quoted_string_01_ok(self):
        token = ('"Smith"', 13)
        nodestr = '(gash, [], "Smith", None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack.append(s.node_stack[-1])
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_double_quoted_string, nodestr, None, 1)

    def test_p_double_quoted_string_02_error(self):
        token = ('"Smith"', 41)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_double_quoted_string, 0)

    def test_b_double_quoted_string_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_double_quoted_string(), None)

    def test_b_double_quoted_string_02_ok(self):
        token = ('"Smith"', 13)
        nodestr = '(gash, [], "Smith", None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack.append(s.node_stack[-1])
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.b_double_quoted_string, nodestr, None, 1)

    def test_p_sort_matchcount_01_ok(self):
        # To be done.
        token = ('matchcount', 1)
        s = self.statement

    def test_p_sort_matchcount_02_error(self):
        # To be done.
        token = ('matchcount', 1)
        s = self.statement

    def test_p_player_white_black_01_white(self):
        token = ('white', 40)
        nodestr = '(gash, [(white, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_player_white_black, nodestr, s.p_double_quoted_string, 2)

    def test_p_player_white_black_02_white_repeated(self):
        s = self.statement

    def test_p_player_white_black_03_string(self):
        token = ('"Smith"', 13)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_reprocess_ok(
            token, s.p_player_white_black, nodestr, s.p_double_quoted_string, 2)

    def test_p_player_white_black_04_string_repeated(self):
        # To be done.
        s = self.statement

    def test_p_player_white_black_05_type(self):
        token = ('gash', 1)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('player'))
        s.stack.append('gash')
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_reprocess_ok(
            token, s.p_player_white_black, None, 'gash', 0)
        self.assertEqual(len(s.stack), 1)

    def test_p_player_white_black_06_error(self):
        token = ('gash', 1)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_player_white_black, 1)

    def test_p_elo_white_black_01_white(self):
        token = ('white', 40)
        nodestr = '(gash, [(white, [], [], None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token, s.p_elo_white_black, nodestr, s.p_numbers, 2)

    def test_p_elo_white_black_02_white_repeated(self):
        # To be done.
        s = self.statement

    def test_p_elo_white_black_03_number(self):
        token = ('1500', 12)
        nodestr = '(gash, [], [], None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_reprocess_ok(
            token, s.p_elo_white_black, nodestr, s.p_range, 2)

    def test_p_elo_white_black_04_string_repeated(self):
        # To be done.
        s = self.statement

    def test_p_elo_white_black_05_type(self):
        token = ('gash', 1)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('elo'))
        s.stack.append('gash')
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_reprocess_ok(
            token, s.p_elo_white_black, None, 'gash', 0)
        self.assertEqual(len(s.stack), 1)

    def test_p_elo_white_black_06_error(self):
        token = ('gash', 1)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.p_elo_white_black, 1)

    def test_b_pop_top_of_stack_01_others(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.assertEqual(s.b_pop_top_of_stack(), None)
        self.assertEqual(s.node_stack, [])
        self.assertEqual(s.stack, [])
        self.assertEqual(s.variables_stack, [])
        self.assertEqual(s.variables, {})

    def test_b_pop_nested_stack_01_(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('{'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('on'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        s.node_stack.append(
            statement.Statement.create_node(
                'gash', children=[node.Node('g'), node.Node('g')]))
        s.stack.append('gash')
        self.assertEqual(s.b_pop_nested_stack(), None)
        self.assertEqual(s.stack, ['gash', 'gash'])
        self.assertEqual(len(s.node_stack), 2)
        self.assertEqual(str(s.node_stack[0]), '(gash, [], None, None)')
        self.assertEqual(str(s.node_stack[1]), '({, [], None, None)')

    def test_b_pop_nested_stack_to_implied_brace_01_(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('{'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('on'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        self.assertEqual(s.b_pop_nested_stack_to_implied_brace(), None)
        self.assertEqual(s.stack, ['gash', 'gash', 'gash'])
        self.assertEqual(len(s.node_stack), 3)
        self.assertEqual(str(s.node_stack[0]), '(gash, [], None, None)')
        self.assertEqual(str(s.node_stack[1]), '({, [], None, None)')
        self.assertEqual(str(s.node_stack[2]), '(on, [], None, None)')

    def test_b_pop_top_of_stack_and_nested_01_(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('{'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('on'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        s.node_stack.append(
            statement.Statement.create_node(
                'gash', children=[node.Node('g'), node.Node('g')]))
        s.stack.append('gash')
        s.node_stack.append(
            statement.Statement.create_node('{', children=[None, None]))
        s.stack.append('gash')
        self.assertEqual(s.b_pop_top_of_stack_and_nested(), None)
        self.assertEqual(s.stack, ['gash', 'gash'])
        self.assertEqual(len(s.node_stack), 2)
        self.assertEqual(str(s.node_stack[0]), '(gash, [], None, None)')
        self.assertEqual(str(s.node_stack[1]), '({, [], None, None)')

    def test_b_pop_variables_stack_01_(self):
        s = self.statement
        s.variables_stack.append({'$x':'gash'})
        s.variables['$x'] = 'gash'
        s.variables['$y'] = 'gash'
        self.assertEqual(s.b_pop_variables_stack(), None)
        self.assertEqual(len(s.variables_stack), 0)
        self.assertEqual(s.variables, {'$y':'gash'})

    def test_b_cql_01_(self):
        s = self.statement
        self.assertEqual(s.b_cql(), None)
        self.assertEqual(len(s.node_stack), 1)
        self.assertEqual(s.stack, [s.b_body])
        self.assertEqual(s.variables_stack, [set()])
        self.assertEqual(str(s.node_stack[0]), '(cql, [], None, None)')

    def test_b_body_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        self.assertRaises(IndexError, s.b_body)

    def test_b_body_02_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_body(), None)

    def test_b_body_03_tokens(self):
        s = self.statement
        token = ('', 0)
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.assertEqual(s.b_body(), True)

    def test_b_piece_square_in_set_body_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        self.assertRaises(IndexError, s.b_piece_square_in_set_body)

    def test_b_piece_square_in_set_body_02_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_piece_square_in_set_body(), None)

    def test_b_piece_square_in_set_body_03_tokens(self):
        s = self.statement
        token = ('', 0)
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.assertEqual(s.b_piece_square_in_set_body(), True)

    def test_b_collapse_filters_stack_01_rays_collapse_stack(self):
        s = self.statement
        ns = s.node_stack
        ns.extend([statement.Statement.create_node('cql'),
                   statement.Statement.create_node('{'),
                   statement.Statement.create_node('up')])
        ns[0].children.append(ns[1])
        ns[1].children.append(ns[2])
        s.stack.append('gash')
        self.assertEqual(s.b_collapse_filters_stack(), None)
        self.assertEqual(s.stack, [s.b_pop_top_of_stack])
        self.assertEqual(len(s.node_stack), 3)

    def test_b_collapse_filters_stack_02_no_collapse(self):
        s = self.statement
        ns = s.node_stack
        ns.extend([statement.Statement.create_node('cql'),
                   statement.Statement.create_node('{'),
                   statement.Statement.create_node('wtm')])
        ns[0].children.append(ns[1])
        ns[1].children.append(ns[2])
        s.stack.append('gash')
        self.assertEqual(s.b_collapse_filters_stack(), None)
        self.assertEqual(s.stack, ['gash'])
        self.assertEqual(len(s.node_stack), 3)

    def test_b_collapse_parameters_stack_01_(self):
        s = self.statement
        self.assertEqual(s.b_collapse_parameters_stack(), None)

    def test_b_collapse_parameters_stack_02_(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.assertEqual(s.b_collapse_parameters_stack(), None)

    def test_b_collapse_parameters_stack_03_(self):
        s = self.statement
        token = ('or', 14)
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('or'))
        self.assertEqual(s.b_collapse_parameters_stack(), None)

    def test_b_collapse_04_parameters_stack_(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack.append(statement.Statement.create_node('from'))
        s.stack.append('gash')
        self.assertEqual(s.b_collapse_parameters_stack(), None)

    def test_b_end_01_nslen_not_1(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('{'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('on'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        self.assertEqual(s.b_end(), None)
        self.assertEqual(s.stack, ['gash', 'gash'])
        self.assertEqual(len(s.node_stack), 2)
        self.assertEqual(str(s.node_stack[0]), '(cql, [], None, None)')
        self.assertEqual(str(s.node_stack[1]), '({, [], None, None)')

    def test_b_end_02_nslen_1(self):
        s = self.statement
        n = statement.Statement.create_node('cql')
        s.node_stack.append(n)
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('on'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = [1, 2]
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_end(), None)
        self.assertEqual(s.stack, ['gash'])
        self.assertEqual(s.variables_stack, [])
        self.assertEqual(len(s.node_stack), 0)
        self.assertEqual(len(s.node_stack), 0)
        self.assertEqual(str(s.cql_filters), '(cql, [], None, None)')
        self.assertIs(s.cql_filters, n)

    def test_add_piece_square_in_set_body_01_piece_designator(self):
        self.add_keyword_method_stackmethod(
            ('k', 6),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(piece_designator, [], k, True)], None, None)',
            None,
            1,
            None)

    def test_add_piece_square_in_set_body_02_plain(self):
        self.add_keyword_method_stackmethod(
            ('darksquares', 9),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(plain, [], darksquares, True)], None, None)',
            None,
            1,
            None)

    def test_add_piece_square_in_set_body_03_plain(self):
        self.add_keyword_method_stackmethod(
            ('lightsquares', 9),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(plain, [], lightsquares, True)], None, None)',
            None,
            1,
            None)

    def test_add_piece_square_in_set_body_04_plain(self):
        self.add_keyword_method_stackmethod(
            ('wtm', 9),
            self.statement.add_piece_square_in_set_body,
            '(cql, [], None, None)',
            None,
            1,
            True)

    def test_add_piece_square_in_set_body_05_not(self):
        self.add_keyword_method_stackmethod(
            ('not', 15),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(not, [], None, None)], None, None)',
            None,
            1,
            None)

    def test_add_piece_square_in_set_body_06_or(self):
        self.add_keyword_method_stackmethod(
            ('or', 14),
            self.statement.add_piece_square_in_set_body,
            '(cql, [], None, None)',
            None,
            1,
            True)

    def test_add_piece_square_in_set_body_07_or(self):
        self.add_keyword_method_stackmethod(
            ('or', 14),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(or, [(op1, [], None, None)], None, None)], None, None)',
            None,
            1,
            None,
            children=[statement.Statement.create_node('op1')],
            cql_tokens=[('k', 6)])

    def test_add_piece_square_in_set_body_08_on(self):
        self.add_keyword_method_stackmethod(
            ('on', 26),
            self.statement.add_piece_square_in_set_body,
            '(cql, [], None, None)',
            None,
            1,
            True)

    def test_add_piece_square_in_set_body_09_on(self):
        self.add_keyword_method_stackmethod(
            ('on', 26),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(on, [(op1, [], None, None)], None, None)], None, None)',
            None,
            1,
            None,
            children=[statement.Statement.create_node('op1')],
            cql_tokens=[('k', 6)])

    def test_add_piece_square_in_set_body_10_transform(self):
        self.add_keyword_method_stackmethod(
            ('right', 8),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(right, [], None, None)], None, None)',
            None,
            1,
            None)

    def test_add_piece_square_in_set_body_11_attack(self):
        self.add_keyword_method_stackmethod(
            ('attack', 16),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(attack, [], None, None)], None, None)',
            None,
            1,
            None)

    def test_add_piece_square_in_set_body_12_move(self):
        self.add_keyword_method_stackmethod(
            ('move', 23),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(move, [], None, None)], None, None)',
            None,
            1,
            None)

    def test_add_piece_square_in_set_body_13_left_brace(self):
        self.add_keyword_method_stackmethod(
            ('{', 2),
            self.statement.add_piece_square_in_set_body,
            '(cql, [({, [], None, None)], None, None)',
            None,
            1,
            None)

    def test_add_piece_square_in_set_body_14_right_brace_node_stack_cleared(
        self):
        s = self.statement
        ns = [statement.Statement.create_node(
            'cql', children=[node.Node('g'), node.Node('h')])]
        self.add_keyword_method_stackmethod(
            ('}', 3),
            self.statement.add_piece_square_in_set_body,
            '(cql, [(g, [], None, None), (h, [], None, None)], None, None)',
            None,
            0,
            True,
            node_stack=ns,
            variable_stack=[{}])

    def test_add_piece_square_in_set_body_15_right_brace_left(self):
        s = self.statement
        ns = [statement.Statement.create_node('cql'),
              statement.Statement.create_node(
                  '{', children=[node.Node('g'), node.Node('h')])]
        ns[0].children.append(ns[1])
        self.add_keyword_method_stackmethod(
            ('}', 3),
            self.statement.add_piece_square_in_set_body,
            ''.join((
                '(cql, [({, ',
                '[(g, [], None, None), (h, [], None, None)], '
                'None, False)], None, None)',
                )),
            None,
            1,
            None,
            node_stack=ns,
            variable_stack=[{}])

    def test_add_piece_square_in_set_body_16_right_brace_left_variables(self):
        s = self.statement
        ns = [statement.Statement.create_node('cql'),
              statement.Statement.create_node(
                  '{', children=[node.Node('g'), node.Node('h')])]
        ns[0].children.append(ns[1])
        self.add_keyword_method_stackmethod(
            ('}', 3),
            self.statement.add_piece_square_in_set_body,
            ''.join((
                '(cql, [({, ',
                '[(g, [], None, None), (h, [], None, None)], '
                'None, False)], None, None)',
                )),
            None,
            1,
            None,
            variables={'$x':'gash', '$y':'keep'},
            node_stack=ns,
            variable_stack=[{'$x':'gash'}])
        self.assertEqual(self.statement.variables, {'$y':'keep'})

    def test_add_piece_square_in_set_body_17_right_brace_cql(self):
        s = self.statement
        ns = [statement.Statement.create_node('cql'),
              statement.Statement.create_node('{'),
              statement.Statement.create_node(
                  'cql', children=[node.Node('g'), node.Node('h')])]
        ns[0].children.append(ns[1])
        ns[1].children.append(ns[2])
        self.add_keyword_method_stackmethod(
            ('}', 3),
            self.statement.add_piece_square_in_set_body,
            ''.join((
                '(cql, [({, [(cql, ',
                '[(g, [], None, None), (h, [], None, None)], '
                'None, False)], None, False)], None, None)',
                )),
            None,
            1,
            None,
            node_stack=ns,
            variable_stack=[{}, {}],
            stack=['gash1', 'gash2'])

    def test_add_piece_square_in_set_body_18_right_brace_cql_variables(self):
        s = self.statement
        ns = [statement.Statement.create_node('cql'),
              statement.Statement.create_node('{'),
              statement.Statement.create_node(
                  'cql', children=[node.Node('g'), node.Node('h')])]
        ns[0].children.append(ns[1])
        ns[1].children.append(ns[2])
        self.add_keyword_method_stackmethod(
            ('}', 3),
            self.statement.add_piece_square_in_set_body,
            ''.join(('(cql, [({, [(cql, ',
                     '[(g, [], None, None), (h, [], None, None)], ',
                     'None, False)], None, False)], None, None)',)),
            None,
            1,
            None,
            variables={'$x':'gash', '$y':'keep'},
            node_stack=ns,
            variable_stack=[{}, {'$x':'gash'}],
            stack=['gash1', 'gash2'])
        self.assertEqual(self.statement.variables, {'$y':'keep'})

    def test_add_piece_square_in_set_body_19_right_brace_not(self):
        s = self.statement
        ns = [statement.Statement.create_node('cql'),
              statement.Statement.create_node('{'),
              statement.Statement.create_node(
                  'not', children=[node.Node('g'), node.Node('h')])]
        ns[0].children.append(ns[1])
        ns[1].children.append(ns[2])
        self.add_keyword_method_stackmethod(
            ('}', 3),
            self.statement.add_piece_square_in_set_body,
            ''.join(('(cql, [({, [(not, [(g, [], None, None), (h, [], None, None)], ',
                     'None, False)], None, False)], None, None)',
                     )),
            None,
            1,
            None,
            node_stack=ns,
            variable_stack=[{}],
            stack=['gash1', 'gash2'])

    def test_add_piece_square_in_set_body_20_right_brace_error(self):
        s = self.statement
        ns = [statement.Statement.create_node('cql'),
              statement.Statement.create_node('{'),
              statement.Statement.create_node('k')]
        ns[0].children.append(ns[1])
        ns[1].children.append(ns[2])
        self.add_keyword_method_stackmethod(
            ('}', 3),
            self.statement.add_piece_square_in_set_body,
            '(cql, [({, [(k, [], None, None)], None, None)], None, None)',
            None,
            1,
            True,
            node_stack=ns)

    def test_add_piece_square_in_set_body_21_right_brace_more_tokens(self):
        s = self.statement
        ns = [statement.Statement.create_node('cql'),
              statement.Statement.create_node('{'),
              statement.Statement.create_node(
                  'not', children=[node.Node('g'), node.Node('h')])]
        ns[0].children.append(ns[1])
        ns[1].children.append(ns[2])
        self.add_keyword_method_stackmethod(
            ('}', 3),
            self.statement.add_piece_square_in_set_body,
            ''.join(('(cql, [({, [(not, [(g, [], None, None), ',
                     '(h, [], None, None)], None, False)], None, False)], ',
                     'None, None)',
                     )),
            None,
            1,
            None,
            node_stack=ns,
            variable_stack=[{}],
            stack=['gash1', 'gash2'],
            extra_tokens=(('k', 6),))

    def test_add_piece_square_in_set_body_22_error(self):
        self.add_keyword_method_stackmethod(
            ('white', 40),
            self.statement.add_piece_square_in_set_body,
            '(cql, [], None, None)',
            None,
            1,
            True)

    def test_add_set_body_01_plain(self):
        self.add_keyword_method_stackmethod(
            ('wtm', 9),
            self.statement.add_set_body,
            '(cql, [(plain, [], wtm, False)], None, None)',
            None,
            1,
            None)

    def test_add_set_body_02_square_variable(self):
        # variables argument is unrealistic because the node tree does not give
        # type and name of variable.
        self.add_keyword_method_stackmethod(
            ('$x', 39),
            self.statement.add_set_body,
            '(cql, [($, [], gash, None)], None, None)',
            None,
            1,
            None,
            variables={'$x':'gash'})

    def test_add_set_body_03_delegate_to_add_piece_square_in_set_body(self):
        self.add_keyword_method_stackmethod(
            ('move', 23),
            self.statement.add_set_body,
            '(cql, [(move, [], None, None)], None, None)',
            None,
            1,
            None)

    def test_add_cql_body_01_piece_square_variable(self):
        self.add_keyword_method_stackmethod(
            ('$x', 39),
            self.statement.add_cql_body,
            '(cql, [($, [], psvtarget, None)], None, None)',
            None,
            1,
            None,
            variables={'$x':'psvtarget'})

    def test_add_cql_body_02_number(self):
        s = self.statement
        self.add_keyword_method_stackmethod(
            ('7', 12),
            s.add_cql_body,
            '(cql, [], None, None)',
            s.b_range,
            2,
            None)
        self.assertEqual(s.node_stack[0], s.node_stack[1])

    def test_add_cql_body_08_delegate_to_add_set_body(self):
        self.add_keyword_method_stackmethod(
            ('move', 23),
            self.statement.add_cql_body,
            '(cql, [(move, [], None, None)], None, None)',
            None,
            1,
            None)

    def test_add_piece_designator_01_(self):
        token = ('k', 6)
        nodestr = '(cql, [(piece_designator, [], k, True)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.body_keyword_ok(token, s.add_piece_designator, nodestr, 'gash', 1)

    def test_add_left_parenthesis_01_(self):
        token = ('(', 0)
        nodestr = '(gash, [((, [], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.body_keyword_ok(token, s.add_left_parenthesis, nodestr, None, 2)
        self.assertEqual(s.variables_stack, [set()])

    def test_add_piece_square_variable_01_error(self):
        token = ('$x', 39)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        self.assertEqual(s.variables, {})
        self.body_keyword_error(token, s.add_piece_square_variable, 0)

    def test_add_piece_square_variable_02_ok(self):
        token = ('$x', 39)
        nodestr = '(cql, [($, [], psvtarget, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        s.variables['$x'] = 'psvtarget'
        self.body_keyword_ok(
            token, s.add_piece_square_variable, nodestr, 'gash', 1)

    def test_add_plain_filter_01_(self):
        token = ('btm', 9)
        nodestr = '(cql, [(plain, [], btm, False)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.body_keyword_ok(token, s.add_plain_filter, nodestr, 'gash', 1)

    def test_add_move_from_to_enpassantsquare_parameter_01_(self):
        token = ('to', 11)
        nodestr = '(gash, [(gash, [(to, [], None, None)], None, None)], None, None)'
        node = statement.Statement.create_node('gash')
        node.children.append(statement.Statement.create_node('gash'))
        s = self.statement
        s.node_stack.append(node)
        s.tokens = self.expected_matches((token,))
        self.body_keyword_ok(
            token,
            s.add_move_from_to_enpassantsquare_parameter,
            nodestr,
            s.b_body,
            2)

    # See definition of add_move_promote_parameter in ..core.statement
    test_add_move_promote_parameter_01_ = (
        test_add_move_from_to_enpassantsquare_parameter_01_)

    def test_b_move_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_move(), None)

    def test_b_move_02_mainline(self):
        token = ('mainline', 22)
        nodestr = '(cql, [(mainline, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        self.keyword_ok(token, s.b_move, nodestr, s.b_move_from, 1)

    def test_b_move_03_next_previous(self):
        token = ('previous', 25)
        nodestr = '(cql, [(previous, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        self.keyword_ok(token, s.b_move, nodestr, s.b_move_from, 1)

    def test_b_move_04_move_parameter(self):
        token = ('from', 11)
        nodestr = '(cql, [(next, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_move, nodestr, s.b_move_from, 1)

    def test_b_move_05_children(self):
        token = ('from', 11)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_move, 1)

    def test_b_move_06_children_not_token(self):
        token = ('k', 6)
        nodestr = '(cql, [(gash, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.node_stack[-1].children.append(
            statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_move, nodestr, s.b_move_from, 1)

    def test_b_move_from_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_move_from(), None)

    def test_b_move_from_02_ok(self):
        token = ('from', 11)
        nodestr = '(gash, [(gash, [(from, [], None, None)], None, None)], None, None)'
        node = statement.Statement.create_node('gash')
        node.children.append(statement.Statement.create_node('gash'))
        s = self.statement
        s.node_stack.append(node)
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token,
            s.b_move_from,
            nodestr,
            [s.b_move_to, s.b_body],
            2)

    def test_b_move_from_03_not_from_token(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_move_from, None, s.b_move_to, 0)

    def test_b_move_to_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_move_to(), None)

    def test_b_move_to_02_ok(self):
        token = ('to', 11)
        nodestr = '(gash, [(gash, [(to, [], None, None)], None, None)], None, None)'
        node = statement.Statement.create_node('gash')
        node.children.append(statement.Statement.create_node('gash'))
        s = self.statement
        s.node_stack.append(node)
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token,
            s.b_move_to,
            nodestr,
            [s.b_move_promote, s.b_body],
            2)

    def test_b_move_to_03_not_to_token(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_move_to, None, s.b_move_promote, 0)

    def test_b_move_promote_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_move_to(), None)

    def test_b_move_promote_02_ok(self):
        token = ('promote', 11)
        nodestr = '(gash, [(gash, [(promote, [], None, None)], None, None)], None, None)'
        node = statement.Statement.create_node('gash')
        node.children.append(statement.Statement.create_node('gash'))
        s = self.statement
        s.node_stack.append(node)
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token,
            s.b_move_promote,
            nodestr,
            [s.b_move_enpassantsquare, s.b_body],
            2)

    def test_b_move_promote_03_not_promote_token(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.stack.append('gash')
        self.keyword_reprocess_ok(
            token, s.b_move_promote, None, s.b_move_enpassantsquare, 0)

    def test_b_move_enpassantsquare_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_move_to(), None)

    def test_b_move_enpassantsquare_02_ok(self):
        token = ('enpassantsquare', 11)
        nodestr = '(gash, [(gash, [(enpassantsquare, [], None, None)], None, None)], None, None)'
        node = statement.Statement.create_node('gash')
        node.children.append(statement.Statement.create_node('gash'))
        s = self.statement
        s.node_stack.append(node)
        s.stack.append('gash')
        s.tokens = self.expected_matches((token,))
        self.keyword_ok(
            token,
            s.b_move_enpassantsquare,
            nodestr,
            ['gash', s.b_body],
            2)

    def test_b_move_enpassantsquare_03_enpassant(self):
        token = ('enpassant', 11)
        nodestr = '(gash, [(gash, [(enpassantsquare, [], a-h1-8, None)], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(token, s.b_move_enpassantsquare, nodestr, None, 0)

    def test_b_move_enpassantsquare_04_not_an_enpassant_token(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append('gash')
        s.stack.append('gash')
        self.keyword_reprocess_ok(
            token, s.b_move_enpassantsquare, None, None, 0)

    # Tests for filters using add_filter(token_identity, next_method) still to
    # be added.
    # Most, if not all, tests in *_add_relation_* style will be converted too.

    def test_b_two_set_filters_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_two_set_filters(), None)

    def test_b_two_set_filters_02_right_parenthesis_type_error(self):
        token = (')', 1)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_two_set_filters, 1)

    def test_b_two_set_filters_03_right_parenthesis_children_error(self):
        token = (')', 1)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_two_set_filters, 1)

    def test_b_two_set_filters_04_right_parenthesis_ok(self):
        token = (')', 1)
        nodestr = '((, [(gash, [], None, None), (gash, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_ok(token,
                        s.b_two_set_filters,
                        nodestr,
                        ['gash', s.p_error],
                        1,
                        poptokens=0,
                        method_return=True)

    def test_b_two_set_filters_05_children_error(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_two_set_filters, 1)

    def test_b_two_set_filters_06_ok(self):
        token = ('k', 6)
        nodestr = '((, [(gash, [], None, None), (piece_designator, [], k, True)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_two_set_filters, nodestr, None, 1)

    def test_b_one_set_filter_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_one_set_filter(), None)

    def test_b_one_set_filter_02_children_error(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_one_set_filter, 1)

    def test_b_one_set_filter_03_children_ok(self):
        token = ('k', 6)
        nodestr = '(gash, [(gash, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token,
                        s.b_one_set_filter,
                        nodestr,
                        ['gash', s.p_error],
                        1,
                        poptokens=0,
                        method_return=True)

    def test_b_one_set_filter_04_ok(self):
        token = ('k', 6)
        nodestr = '((, [(gash, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.stack.append('gash')
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token,
                        s.b_one_set_filter,
                        nodestr,
                        ['gash', s.p_error],
                        1,
                        poptokens=0,
                        method_return=True)

    def test_b_two_or_more_set_filters_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_two_or_more_set_filters(), None)

    def test_b_two_or_more_set_filters_02_right_parenthesis_type_error(self):
        token = (')', 1)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_two_or_more_set_filters, 1)

    def test_b_two_or_more_set_filters_03_right_parenthesis_children_error(
        self):
        token = (')', 1)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_two_or_more_set_filters, 1)

    def test_b_two_or_more_set_filters_04_right_parenthesis_ok(self):
        token = (')', 1)
        nodestr = '((, [(gash, [], None, None), (gash, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_ok(token,
                        s.b_two_or_more_set_filters,
                        nodestr,
                        ['gash', s.p_error],
                        1,
                        poptokens=0,
                        method_return=True)

    def test_b_two_or_more_set_filters_05_ok(self):
        token = ('k', 6)
        nodestr = '((, [(gash, [], None, None), (piece_designator, [], k, True)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_two_or_more_set_filters, nodestr, None, 1)

    def test_b_one_or_more_re_set_filters_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_one_or_more_re_set_filters(), None)

    def test_b_one_or_more_re_set_filters_02_right_parenthesis_type_error(self):
        token = (')', 1)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_one_or_more_re_set_filters, 1)

    def test_b_one_or_more_re_set_filters_03_right_parenthesis_children_error(
        self):
        token = (')', 1)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_one_or_more_re_set_filters, 1)

    def test_b_one_or_more_re_set_filters_04_right_parenthesis_ok(self):
        token = (')', 1)
        nodestr = '((, [(gash, [], None, None), (gash, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_ok(token,
                        s.b_one_or_more_re_set_filters,
                        nodestr,
                        ['gash', s.p_error],
                        1,
                        poptokens=0,
                        method_return=True)

    def test_b_one_or_more_re_set_filters_05_ok(self):
        token = ('k', 6)
        nodestr = '((, [(gash, [], None, None), (piece_designator, [], k, True)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_one_or_more_re_set_filters, nodestr, None, 1)

    def test_b_one_or_more_filters_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_one_or_more_filters(), None)

    def test_b_one_or_more_filters_02_right_parenthesis_type_error(self):
        token = (')', 1)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_one_or_more_filters, 1)

    def test_b_one_or_more_filters_03_right_parenthesis_children_error(
        self):
        token = (')', 1)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_one_or_more_filters, 1)

    def test_b_one_or_more_filters_04_right_parenthesis_ok(self):
        token = (')', 1)
        nodestr = '((, [(gash, [], None, None), (gash, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_ok(token,
                        s.b_one_or_more_filters,
                        nodestr,
                        ['gash', s.p_error],
                        1,
                        poptokens=0,
                        method_return=True)

    def test_b_one_or_more_filters_05_ok(self):
        token = ('k', 6)
        nodestr = '((, [(gash, [], None, None), (piece_designator, [], k, True)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_one_or_more_filters, nodestr, None, 1)

    def test_b_attack_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_attack(), None)

    def test_b_attack_02_token_after_attack_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_attack, None, None, 0)

    def test_b_attack_03_left_parenthesis(self):
        token = ('(', 0)
        nodestr = '(gash, [((, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_attack, nodestr, s.b_two_set_filters, 2)

    def test_b_attack_04_number_after_attack_parameters(self):
        token = ('15', 12)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = ['gash', 'gash']
        self.keyword_error(token, s.b_attack, 1)

    def test_b_attack_05_number(self):
        token = ('15', 12)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_reprocess_ok(token, s.b_attack, nodestr, s.p_range, 2)

    def test_b_attack_06_token_before_attack_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_attack, 1)

    def test_b_between_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_between(), None)

    def test_b_between_02_token_after_attack_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_between, None, None, 0)

    def test_b_between_03_left_parenthesis(self):
        token = ('(', 0)
        nodestr = '(gash, [((, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_between, nodestr, s.b_two_set_filters, 2)

    def test_b_between_04_token_before_attack_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_between, 1)

    def test_b_countsquares_power_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_countsquares_power(), None)

    def test_b_countsquares_power_02_token_after_parameter(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_countsquares_power, None, None, 0)

    def test_b_countsquares_power_04_number_after_parameter(self):
        token = ('15', 12)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = ['gash', 'gash']
        self.keyword_error(token, s.b_countsquares_power, 1)

    def test_b_countsquares_power_05_number(self):
        token = ('15', 12)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_reprocess_ok(
            token,
            s.b_countsquares_power,
            nodestr,
            [s.b_one_set_filter, s.p_range],
            3)

    def test_b_countsquares_power_06_token_before_parameter(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_countsquares_power, 1)

    def test_b_powerdifference_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_powerdifference(), None)

    def test_b_powerdifference_02_token_after_powerdifference_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_powerdifference, None, None, 0)

    def test_b_powerdifference_03_left_parenthesis_no_range(self):
        token = ('(', 0)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_powerdifference, 1)

    def test_b_powerdifference_04_left_parenthesis(self):
        token = ('(', 0)
        nodestr = '(gash<1,1>, [((, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        n = statement.Statement.create_node('gash')
        n.range = [1, 1]
        s.node_stack.append(n)
        self.keyword_ok(
            token, s.b_powerdifference, nodestr, s.b_two_set_filters, 2)

    def test_b_powerdifference_05_number_after_powerdifference_parameters(self):
        token = ('15', 12)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = ['gash', 'gash']
        self.keyword_error(token, s.b_powerdifference, 1)

    def test_b_powerdifference_06_number(self):
        token = ('15', 12)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_reprocess_ok(
            token, s.b_powerdifference, nodestr, s.p_range, 2)

    def test_b_powerdifference_07_token_before_powerdifference_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_powerdifference, 1)

    def test_b_ray_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_ray(), None)

    def test_b_ray_02_token_after_ray_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_ray, None, None, 0)

    def test_b_ray_03_left_parenthesis(self):
        token = ('(', 0)
        nodestr = '(gash, [((, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_ray, nodestr, s.b_two_or_more_set_filters, 2)

    def test_b_ray_04_number_after_ray_parameters(self):
        token = ('15', 12)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = ['gash', 'gash']
        self.keyword_error(token, s.b_ray, 1)

    def test_b_ray_05_number(self):
        token = ('15', 12)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_reprocess_ok(token, s.b_ray, nodestr, s.p_range, 2)

    def test_b_ray_06_attack_before_ray_parameters(self):
        token = ('attack', 16)
        nodestr = '(gash, [(attack, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_ray, nodestr, s.b_ray, 2)

    def test_b_ray_07_direction_before_ray_parameters(self):
        token = ('horizontal', 8)
        nodestr = '(gash, [(horizontal, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token, s.b_ray, nodestr, s.b_ray, 2)

    def test_b_ray_08_token_before_ray_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_ray, 1)

    def test_b_next_previous_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_next_previous(), None)

    def test_b_next_previous_02_token_after_next_previous_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(token, s.b_next_previous, None, None, 0)

    def test_b_next_previous_03_left_parenthesis(self):
        token = ('(', 0)
        nodestr = '(gash, [((, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_ok(token,
                        s.b_next_previous,
                        nodestr,
                        s.b_one_or_more_re_set_filters,
                        2)

    def test_b_next_previous_04_number_after_next_previous_parameters(self):
        token = ('15', 12)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = ['gash', 'gash']
        self.keyword_error(token, s.b_next_previous, 1)

    def test_b_next_previous_05_number(self):
        token = ('15', 12)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_reprocess_ok(
            token, s.b_next_previous, nodestr, s.p_range, 2)

    def test_b_next_previous_06_token_before_next_previous_parameters(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_next_previous, 1)

    def test_b_relation_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_relation(), None)

    def test_b_relation_02_echo_parameter(self):
        token = ('echoflip', 10)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(
            token, s.b_relation, nodestr, s.b_relation_parameter, 1)

    def test_b_relation_03_non_echo_parameter(self):
        token = ('tomove', 10)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_relation, 1)

    def test_b_relation_04_left_parenthesis(self):
        token = ('(', 0)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(
            token, s.b_relation, nodestr, s.b_relation_parameter, 1)

    def test_b_relation_05_targetfilter(self):
        token = ('k', 6)
        nodestr = '(relation, [(piece_designator, [], k, True)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('relation'))
        s.stack.append('relation')
        self.keyword_ok(token, s.b_relation, nodestr, 'relation', 1)

    def test_b_relation_parameter_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_relation_parameter(), None)

    def test_b_relation_parameter_02_echo_parameter(self):
        token = ('echoflip', 10)
        nodestr = '(gash, [(echoflip, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter,
            nodestr,
            ['gash', s.b_relation_parameter_left_parenthesis],
            2)

    def test_b_relation_parameter_03_non_echo_parameter(self):
        token = ('tomove', 10)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_relation_parameter, 1)

    def test_b_relation_parameter_04_left_parenthesis(self):
        token = ('(', 0)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(
            token,
            s.b_relation_parameter,
            nodestr,
            s.b_relation_parameter_left_parenthesis,
            1)

    def test_b_relation_parameter_05_other_tokens(self):
        token = ('k', 6)
        nodestr = '({, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('{'))
        s.stack.append('{')
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_reprocess_ok(
            token,
            s.b_relation_parameter,
            nodestr,
            '{',
            1)

    def test_b_relation_parameter_left_parenthesis_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_relation_parameter_left_parenthesis(), None)

    def test_b_relation_parameter_left_parenthesis_02_right_relation_top(self):
        token = (')', 1)
        nodestr = '({, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('relation'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_left_parenthesis,
            nodestr,
            None,
            0)

    def test_b_relation_parameter_left_parenthesis_03_right_other_top(self):
        token = (')', 1)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_left_parenthesis,
            nodestr,
            s.b_relation_parameter,
            1)

    def test_b_relation_parameter_left_parenthesis_04_right_more_tokens(self):
        token = (')', 1)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token, ('q',6)))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_left_parenthesis,
            nodestr,
            s.b_relation_parameter,
            1)

    def test_b_relation_parameter_left_parenthesis_05_other_tokens(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_relation_parameter_left_parenthesis, 1)

    def test_b_relation_parameter_left_parenthesis_06_token(self):
        token = ('(', 0)
        nodestr = '(gash, [((, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_left_parenthesis,
            nodestr,
            ['gash', s.b_relation_parameter_type],
            2)

    def test_b_relation_parameter_type_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_relation_parameter_type(), None)

    def test_b_relation_parameter_type_02_lca_range(self):
        token = ('lcasum', 10)
        nodestr = '(gash, [(lcasum, [], [], None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_type,
            nodestr,
            ['gash', s.p_range],
            2)

    def test_b_relation_parameter_type_03_lca_plain(self):
        token = ('ancestor', 10)
        nodestr = '(gash, [(relation_parameter, [], ancestor, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_type,
            nodestr,
            'gash',
            1)

    def test_b_relation_parameter_type_04_tomove(self):
        token = ('tomove', 10)
        nodestr = '(gash, [(tomove, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_type,
            nodestr,
            ['gash', s.b_relation_tomove_argument],
            2)

    def test_b_relation_parameter_type_05_square_tomove(self):
        token = ('match', 10)
        nodestr = '(gash, [(match, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_type,
            nodestr,
            ['gash', s.b_relation_square_tomove_argument],
            2)

    def test_b_relation_parameter_type_06_square_set_filter(self):
        token = ('targetsquares', 10)
        nodestr = '(gash, [(targetsquares, [], None, None)], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_type,
            nodestr,
            ['gash', s.b_one_set_filter],
            2)

    def test_b_relation_parameter_type_07_right_parenthesis(self):
        token = (')', 1)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.node_stack.append(statement.Statement.create_node('('))
        s.stack.append('gash')
        self.keyword_ok(
            token,
            s.b_relation_parameter_type,
            nodestr,
            'gash',
            1,
            poptokens=0)

    def test_b_relation_parameter_type_08_other_tokens(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_relation_parameter_type, 1)

    def test_b_relation_tomove_argument_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_relation_tomove_argument(), None)

    def test_b_relation_tomove_argument_02_no_tokens_after(self):
        token = ('match', 10)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_error(token,
                           s.b_relation_tomove_argument,
                           1,
                           poptokens=1,
                           nextmethod=['gash', s.p_error])

    def test_b_relation_tomove_argument_03_not_right_parenthesis_after(self):
        token = ('match', 10)
        s = self.statement
        s.tokens = self.expected_matches((token, ('k', 6)))
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_error(token,
                           s.b_relation_tomove_argument,
                           1,
                           poptokens=1,
                           nextmethod=['gash', s.p_error])

    def test_b_relation_tomove_argument_04_right_parenthesis_after(self):
        token = ('match', 10)
        nodestr = '(gash, [], match, None)'
        s = self.statement
        s.tokens = self.expected_matches((token, (')', 1)))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_ok(token,
                        s.b_relation_tomove_argument,
                        nodestr,
                        s.b_relation_parameter_type,
                        1,
                        poptokens=1)

    def test_b_relation_tomove_argument_05_other_tokens(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(token, s.b_relation_tomove_argument, 1)

    def test_b_relation_square_tomove_argument_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_relation_square_tomove_argument(), None)

    def test_b_relation_sqaure_tomove_argument_02_no_range(self):
        token = ('k', 6)
        nodestr = '(gash, [], None, None)'
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_ok(token,
                        s.b_relation_square_tomove_argument,
                        nodestr,
                        ['gash', s.p_numbers],
                        2,
                        poptokens=0)

    def test_b_relation_sqaure_tomove_argument_03_range(self):
        token = ('k', 6)
        nodestr = "((<1,1>, [], ['1'], False)"
        s = self.statement
        s.tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('('))
        s.node_stack.append(s.node_stack[-1])
        s.node_stack[-1].range = ['1']
        s.stack.append('gash')
        s.stack.append('gash')
        s.variables_stack.append({})
        self.keyword_ok(token,
                        s.b_relation_square_tomove_argument,
                        nodestr,
                        'gash',
                        1,
                        poptokens=0)

    # The next few tests are markers for full tests which will be added when
    # add_<filter_name>(token) methods are replaced by
    # add_filter(token_identity, next_method) calls, which needs a modified
    # add_keyword_method_stackmethod(..) method for the add_cql_body() tests.

    def test_b_elo_white_black_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_elo_white_black(), None)

    def test_b_player_white_black_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_player_white_black(), None)

    def test_b_site_event_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_double_quoted_string(), None)

    def test_b_result_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_allowed_strings_result(), None)

    def test_b_year_01_no_tokens(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.stack.append('gash')
        s.variables_stack.append({})
        self.assertEqual(s.b_numbers(), None)

    # End of marker tests

    def test__is_binary_operator_not_allowed_01_true_second_binary(self):
        token = ('or', 14)
        s = self.statement
        s.tokens = []
        s.cql_tokens = self.expected_matches((token,))
        self.keyword_error(None, s._is_binary_operator_not_allowed, 0)

    def test__is_binary_operator_not_allowed_02_true_no_previous_token(self):
        s = self.statement
        s.tokens = []
        self.keyword_error(None, s._is_binary_operator_not_allowed, 0)

    def test__is_binary_operator_not_allowed_03_true_node_empty(self):
        token = ('k', 6)
        s = self.statement
        s.tokens = []
        s.cql_tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.keyword_error(None, s._is_binary_operator_not_allowed, 1)

    def test__is_binary_operator_not_allowed_04_false_children(self):
        token = ('k', 6)
        nodestr = '(gash, [(gash, [], None, None)], None, None)'
        s = self.statement
        s.tokens = []
        s.cql_tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('gash'))
        self.keyword_reprocess_ok(
            None, s._is_binary_operator_not_allowed, nodestr, None, 1)

    def test__is_binary_operator_not_allowed_05_false_leaf(self):
        token = ('k', 6)
        nodestr = '(gash, [], gash, None)'
        s = self.statement
        s.tokens = []
        s.cql_tokens = self.expected_matches((token,))
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].leaf = 'gash'
        self.keyword_reprocess_ok(
            None, s._is_binary_operator_not_allowed, nodestr, None, 1)

    def test_add_argument_01_(self):
        token_identity = 'k'
        token = (token_identity, 6)
        nodestr = '(gash, [(k, [], None, None)], None, None)'
        node = statement.Statement.create_node('gash')
        s = self.statement
        s.node_stack.append(node)
        s.tokens = self.expected_matches((token,))
        s.add_argument(token_identity, 'gash')
        self.assertEqual(s.node_stack[0], node)
        self.assertEqual(s.node_stack[-1], node.children[0])
        self.assertEqual(str(s.node_stack[0]), nodestr)
        self.assertEqual(s.stack, ['gash'])

    def test_add_argument_leaf_01_(self):
        token_identity = 'ancestor'
        token = (token_identity, 10)
        nodestr = '(gash, [(relation_parameter, [], ancestor, None)], None, None)'
        node = statement.Statement.create_node('gash')
        s = self.statement
        s.node_stack.append(node)
        s.tokens = self.expected_matches((token,))
        s.add_argument_leaf('relation_parameter', token_identity)
        self.assertEqual(s.node_stack[0], node)
        self.assertEqual(s.node_stack[-1], node)
        self.assertEqual(str(s.node_stack[0]), nodestr)
        self.assertEqual(s.stack, [])

    def test_add_binary_argument_01_error(self):
        token = ('or', 14)
        s = self.statement
        s.tokens = self.expected_matches((token,))
        #self.body_keyword_error(token, s.add_or, 0)

    def test_add_binary_argument_02_ok(self):
        token = ('or', 14)
        nodestr = '(gash, [(or, [(op1, [], None)], None)], None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].children.append(statement.Statement.create_node('op1'))
        s.tokens = self.expected_matches((token, ('gash', 1),))
        s.cql_tokens.extend(self.expected_matches((('gash', 3),)))
        #self.body_keyword_ok(token, s.add_or, nodestr, None, 2)

    def test_b_piece_square_filter_01_error_piece_all(self):
        token = ('all', 37)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.b_piece_square_filter, 1)

    def test_b_piece_square_filter_02_error_square_all_variable(self):
        token = ('all', 37)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('square'))
        s.tokens = self.expected_matches((token, ('k', 6),))
        self.keyword_error(token, s.b_piece_square_filter, 1, poptokens=1)

    def test_b_piece_square_filter_03_error_square_all_variable_exists(self):
        token = ('all', 37)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('square'))
        s.variables = {'$x':None}
        s.tokens = self.expected_matches((token, ('$x', 39),))
        self.keyword_error(token, s.b_piece_square_filter, 1, poptokens=1)

    def test_b_piece_square_filter_04_error_square_variable(self):
        token = ('k', 6)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.b_piece_square_filter, 1)

    def test_b_piece_square_filter_05_error_square_variable_exists(self):
        token = ('$x', 39)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.variables = {'$x':None}
        s.tokens = self.expected_matches((token,))
        self.keyword_error(token, s.b_piece_square_filter, 1)

    def test_b_piece_square_filter_06_error_square_all_variable_in(self):
        token = ('all', 37)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('square'))
        s.tokens = self.expected_matches((token, ('$x', 39), ('k', 6),))
        self.keyword_error(token, s.b_piece_square_filter, 1, poptokens=2)

    def test_b_piece_square_filter_07_error_square_variable_in(self):
        token = ('$x', 39)
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token, ('k', 6),))
        self.keyword_error(token, s.b_piece_square_filter, 1, poptokens=1)

    def test_b_piece_square_filter_08_ok_square_all_variable_in(self):
        token = ('all', 37)
        nodestr = '(square<all,all>, [($x, [(in, [], None, None)], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('square'))
        s.tokens = self.expected_matches((token, ('$x', 39), ('in', 37),))
        self.keyword_ok(token,
                        s.b_piece_square_filter,
                        nodestr,
                        [s.b_note_piece_square_variable,
                         s.b_piece_square_in_set_body],
                        3,
                        poptokens=3)

    def test_b_piece_square_filter_09_ok_square_variable_in(self):
        token = ('$x', 39)
        nodestr = '(square, [($x, [(in, [], None, None)], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('square'))
        s.tokens = self.expected_matches((token, ('in', 37),))
        self.keyword_ok(token,
                        s.b_piece_square_filter,
                        nodestr,
                        [s.b_note_piece_square_variable,
                         s.b_piece_square_in_set_body],
                        3,
                        poptokens=2)

    def test_b_piece_square_filter_10_ok_piece_variable_in(self):
        token = ('$x', 39)
        nodestr = '(gash, [($x, [(in, [], None, None)], None, None)], None, None)'
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.tokens = self.expected_matches((token, ('in', 37),))
        self.keyword_ok(token,
                        s.b_piece_square_filter,
                        nodestr,
                        [s.b_note_piece_square_variable,
                         s.b_piece_square_in_set_body],
                        3,
                        poptokens=2)

    def test_b_note_piece_square_variable_01_node_stack_too_small(self):
        self.assertEqual(self.statement.b_note_piece_square_variable(), True)

    def test_b_note_piece_square_variable_02_no_piece_square_keyword(self):
        s = self.statement
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack.append(statement.Statement.create_node('gash'))
        self.assertEqual(s.b_note_piece_square_variable(), True)

    def test_b_note_piece_square_variable_03_ok(self):
        s = self.statement
        n = statement.Statement.create_node('piece')
        s.node_stack.append(statement.Statement.create_node('cql'))
        s.node_stack.append(n)
        s.node_stack[-1].range = [1, 2]
        s.node_stack.append(statement.Statement.create_node('gash'))
        s.node_stack[-1].range = [1, 2]
        s.variables_stack.append(set())
        s.stack.append('gash')
        s.stack.append('gash')
        self.assertEqual(s.b_note_piece_square_variable(), None)
        self.assertEqual(s.variables_stack, [{'gash'}])
        self.assertEqual(s.variables, {'gash':n})
        self.assertEqual(len(s.stack), 0)
        self.assertEqual(len(s.node_stack), 1)
        

if __name__ == '__main__':
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Constants))
    runner().run(loader(StatementMethods))

