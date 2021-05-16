# constants.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""constants tests for cql"""

import unittest
from copy import copy, deepcopy
import re

from .. import constants


class CQLConstants(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def expected_matches(self, match_spec):
        """"""
        em = []
        for t, p in match_spec:
            m = [''] * 44
            m[p] = t
            em.append(tuple(m))
        return em

    def test__raises(self):
        """"""
        pass

    def test____assumptions(self):
        """"""
        self.assertEqual(constants.FILE_RANGE, r'[a-h]-[a-h]')
        self.assertEqual(constants.RANK_RANGE, r'[1-8]-[1-8]')
        self.assertEqual(constants.RANGE_SEPARATOR, r'-')
        self.assertEqual(constants.COMPOUND_DESIGNATOR_START, r'\[')
        self.assertEqual(constants.COMPOUND_DESIGNATOR_END, r'\]')
        self.assertEqual(constants.FILE_DESIGNATOR, '[a-h]')
        self.assertEqual(constants.RANK_DESIGNATOR, '[1-8]')
        self.assertEqual(constants.SQUARE_DESIGNATOR_SEPARATOR, r',')
        self.assertEqual(constants.FILE_RANGE, '[a-h]-[a-h]')
        self.assertEqual(constants.RANK_RANGE, '[1-8]-[1-8]')
        self.assertEqual(
            constants.SIMPLE_SQUARE_DESIGNATOR,
            ''.join(('(?:[a-h]-[a-h][1-8]-[1-8])|(?:[a-h]-[a-h][1-8])|',
                     '(?:[a-h][1-8]-[1-8])|(?:[a-h][1-8])')))
        self.assertEqual(
            constants.SQUARE_DESIGNATOR,
            ''.join(('(?:(?:[a-h]-[a-h][1-8]-[1-8])|(?:[a-h]-[a-h][1-8])|',
                     '(?:[a-h][1-8]-[1-8])|(?:[a-h][1-8]))|',
                     '(?:\\[(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                     '(?:[a-h]-[a-h][1-8])|(?:[a-h][1-8]-[1-8])|',
                     '(?:[a-h][1-8]))(?:,(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                     '(?:[a-h]-[a-h][1-8])|(?:[a-h][1-8]-[1-8])|',
                     '(?:[a-h][1-8])))*\\])')))
        self.assertEqual(constants.WHITE_PIECE_NAMES, r'KQRBNP')
        self.assertEqual(constants.ANY_WHITE_PIECE_NAME, r'A')
        self.assertEqual(constants.BLACK_PIECE_NAMES, r'kqrbnp')
        self.assertEqual(constants.ANY_BLACK_PIECE_NAME, r'a')
        self.assertEqual(constants.EMPTY_SQUARE_NAME, r'.')
        self.assertEqual(constants.PIECE_NAMES, r'KQRBNPkqrbnpAa\.')
        self.assertEqual(
            constants.PIECE_TYPE_DESIGNATOR,
            '(?:[KQRBNPkqrbnpAa\\.])|(?:\\[[KQRBNPkqrbnpAa\\.]+\\])')
        self.assertEqual(
            constants.PIECE_DESIGNATOR,
            ''.join(('(?:(?:(?:(?:[KQRBNPkqrbnpAa\\.])|',
                     '(?:\\[[KQRBNPkqrbnpAa\\.]+\\]))',
                     '(?:(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                     '(?:[a-h]-[a-h][1-8])|(?:[a-h][1-8]-[1-8])|',
                     '(?:[a-h][1-8]))|(?:\\[(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                     '(?:[a-h]-[a-h][1-8])|(?:[a-h][1-8]-[1-8])|',
                     '(?:[a-h][1-8]))(?:,(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                     '(?:[a-h]-[a-h][1-8])|(?:[a-h][1-8]-[1-8])|',
                     '(?:[a-h][1-8])))*\\])))|',
                     '(?:(?:(?:[a-h]-[a-h][1-8]-[1-8])|(?:[a-h]-[a-h][1-8])|',
                     '(?:[a-h][1-8]-[1-8])|(?:[a-h][1-8]))|',
                     '(?:\\[(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                     '(?:[a-h]-[a-h][1-8])|(?:[a-h][1-8]-[1-8])|',
                     '(?:[a-h][1-8]))(?:,(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                     '(?:[a-h]-[a-h][1-8])|(?:[a-h][1-8]-[1-8])|',
                     '(?:[a-h][1-8])))*\\]))|(?:(?:[KQRBNPkqrbnpAa\\.])|',
                     '(?:\\[[KQRBNPkqrbnpAa\\.]+\\])))')))
        self.assertEqual(constants.ANY, r'any')
        self.assertEqual(constants.ATTACK, r'attack')
        self.assertEqual(constants.BEGINVARIATION, r'beginvariation')
        self.assertEqual(constants.BETWEEN, r'between')
        self.assertEqual(constants.BTM, r'btm')
        self.assertEqual(constants.CHECK, r'check')
        self.assertEqual(constants.COMMENT, r'comment')
        self.assertEqual(constants.COUNTSQUARES, r'countsquares')
        self.assertEqual(constants.CQL, r'cql')
        self.assertEqual(constants.DARKSQUARES, r'darksquares')
        self.assertEqual(constants.UP, r'up')
        self.assertEqual(constants.DOWN, r'down')
        self.assertEqual(constants.LEFT, r'left')
        self.assertEqual(constants.RIGHT, r'right')
        self.assertEqual(constants.NORTHEAST, r'northeast')
        self.assertEqual(constants.NORTHWEST, r'northwest')
        self.assertEqual(constants.SOUTHEAST, r'southeast')
        self.assertEqual(constants.SOUTHWEST, r'southwest')
        self.assertEqual(constants.VERTICAL, r'vertical')
        self.assertEqual(constants.HORIZONTAL, r'horizontal')
        self.assertEqual(constants.DIAGONAL, r'diagonal')
        self.assertEqual(constants.ORTHOGONAL, r'orthogonal')
        self.assertEqual(constants.ANYDIRECTION, r'anydirection')
        self.assertEqual(constants.ELO, r'elo')
        self.assertEqual(constants.EVENT, r'event')
        self.assertEqual(constants.FLIP, r'flip')
        self.assertEqual(constants.FLIPDIHEDRAL, r'flipdihedral')
        self.assertEqual(constants.FLIPHORIZONTAL, r'fliphorizontal')
        self.assertEqual(constants.FLIPVERTICAL, r'flipvertical')
        self.assertEqual(constants.FLIPCOLOR, r'flipcolor')
        self.assertEqual(constants.GAMENUMBER, r'gamenumber')
        self.assertEqual(constants.HASCOMMENT, r'hascomment')
        self.assertEqual(constants.INITIAL, r'initial')
        self.assertEqual(constants.INPUT, r'input')
        self.assertEqual(constants.LIGHTSQUARES, r'lightsquares')
        self.assertEqual(constants.MAINLINE, r'mainline')
        self.assertEqual(constants.MATCHCOUNT, r'matchcount')
        self.assertEqual(constants.MATE, r'mate')
        self.assertEqual(constants.MOVE, r'move')
        self.assertEqual(constants.FROM, r'from')
        self.assertEqual(constants.TO, r'to')
        self.assertEqual(constants.PROMOTE, r'promote')
        self.assertEqual(constants.MAINLINE, r'mainline')
        self.assertEqual(constants.PREVIOUS, r'previous')
        self.assertEqual(constants.ENPASSANT, r'enpassant')
        self.assertEqual(constants.ENPASSANTSQUARE, r'enpassantsquare')
        self.assertEqual(constants.MOVENUMBER, r'movenumber')
        self.assertEqual(constants.NEXT, r'next')
        self.assertEqual(constants.NEXT2, r'next2')
        self.assertEqual(constants.NEXT_STAR, r'next\*')
        self.assertEqual(constants.NOT, r'not')
        self.assertEqual(constants.ON, r'on')
        self.assertEqual(constants.OR, r'or')
        self.assertEqual(constants.ORIGIN, r'origin')
        self.assertEqual(constants.OUTPUT, r'output')
        self.assertEqual(constants.PIECE, r'piece')
        self.assertEqual(constants.IN, r'in')
        self.assertEqual(constants.PLAYER, r'player')
        self.assertEqual(constants.WHITE, r'white')
        self.assertEqual(constants.BLACK, r'black')
        self.assertEqual(constants.POWER, r'power')
        self.assertEqual(constants.POWERDIFFERENCE, r'powerdifference')
        self.assertEqual(constants.PREVIOUS, r'previous')
        self.assertEqual(constants.PREVIOUS2, r'previous2')
        self.assertEqual(constants.PREVIOUS_STAR, r'previous\*')
        self.assertEqual(constants.RAY, r'ray')
        self.assertEqual(constants.RELATION, r'relation')
        self.assertEqual(constants.ANCESTOR, r'ancestor')
        self.assertEqual(constants.DESCENDANT, r'descendant')
        self.assertEqual(constants.ECHOFLIP, r'echoflip')
        self.assertEqual(constants.ECHOFLIPVERTICAL, r'echoflipvertical')
        self.assertEqual(constants.ECHOFLIPHORIZONTAL, r'echofliphorizontal')
        self.assertEqual(constants.ECHOSHIFT, r'echoshift')
        self.assertEqual(constants.ECHOSHIFTHORIZONTAL, r'echoshifthorizontal')
        self.assertEqual(constants.ECHOSHIFTVERTICAL, r'echoshiftvertical')
        self.assertEqual(constants.ECHOROTATE45, r'echorotate45')
        self.assertEqual(constants.ECHOROTATE90, r'echorotate90')
        self.assertEqual(constants.LCAMAX, r'lcamax')
        self.assertEqual(constants.LCASOURCE, r'lcasource')
        self.assertEqual(constants.LCASUM, r'lcasum')
        self.assertEqual(constants.LCATARGET, r'lcatarget')
        self.assertEqual(constants.LCASUBSTRING, r'lcasubstring')
        self.assertEqual(constants.MATCH, r'match')
        self.assertEqual(constants.MISMATCH, r'mismatch')
        self.assertEqual(constants.SOURCESQUARES, r'sourcesquares')
        self.assertEqual(constants.TARGETSQUARES, r'targetsquares')
        self.assertEqual(constants.TOMOVE, r'tomove')
        self.assertEqual(constants.RESULT, r'result')
        self.assertEqual(constants.ROTATE45, r'rotate45')
        self.assertEqual(constants.ROTATE90, r'rotate90')
        self.assertEqual(constants.SHIFT, r'shift')
        self.assertEqual(constants.SHIFTHORIZONTAL, r'shifthorizontal')
        self.assertEqual(constants.SHIFTVERTICAL, r'shiftvertical')
        self.assertEqual(constants.SILENT, r'silent')
        self.assertEqual(constants.SITE, r'site')
        self.assertEqual(constants.SORT, r'sort')
        self.assertEqual(constants.SQUARE, r'square')
        self.assertEqual(constants.ALL, r'all')
        self.assertEqual(constants.IN, r'in')
        self.assertEqual(constants.STALEMATE, r'stalemate')
        self.assertEqual(constants.TERMINAL, r'terminal')
        self.assertEqual(constants.VARIATION, r'variation')
        self.assertEqual(constants.VARIATIONS, r'variations')
        self.assertEqual(constants.WTM, r'wtm')
        self.assertEqual(constants.YEAR, r'year')
        self.assertEqual(constants.PIECE_SQUARE, r'square|piece')
        self.assertEqual(constants.PIECE_SQUARE_KEYWORDS, r'all|in')
        self.assertEqual(constants.WHITE_BLACK_KEYWORDS, r'white|black')
        self.assertEqual(constants.SITE_EVENT, r'event|site')
        self.assertEqual(constants.COUNTSQUARES_POWER, r'countsquares|power')
        self.assertEqual(constants.NEXT_PREVIOUS,
                         r'previous2|previous|next2|next')
        self.assertEqual(constants.PLAIN,
                         r'|'.join((r'beginvariation',
                                    r'lightsquares',
                                    r'darksquares',
                                    r'variation',
                                    r'stalemate',
                                    r'terminal',
                                    r'initial',
                                    r'check',
                                    r'mate',
                                    r'wtm',
                                    r'btm',
                                    r'any',
                                    )))
        self.assertEqual(constants.PLAIN_FILTER, 'plain')
        self.assertEqual(constants.RELATION_PARAMETER,
                         r'|'.join((r'echoshifthorizontal',
                                    r'echofliphorizontal',
                                    r'echoshiftvertical',
                                    r'echoflipvertical',
                                    r'targetsquares',
                                    r'sourcesquares',
                                    r'lcasubstring',
                                    r'echorotate90',
                                    r'echorotate45',
                                    r'descendant',
                                    r'lcatarget',
                                    r'lcasource',
                                    r'echoshift',
                                    r'mismatch',
                                    r'echoflip',
                                    r'ancestor',
                                    r'tomove',
                                    r'lcasum',
                                    r'lcamax',
                                    r'match',
                                    )))
        self.assertEqual(constants.MOVE_PARAMETER,
                         r'enpassantsquare|enpassant|promote|empty|from|to')
        self.assertEqual(constants.CQL_PARAMETER,
                         r'variations|matchcount|gamenumber|output|input')
        self.assertEqual(constants.CYCLIC_FILTER,
                         {r'up',
                          r'down',
                          r'left',
                          r'right',
                          r'northeast',
                          r'northwest',
                          r'southeast',
                          r'southwest',
                          })
        self.assertEqual(constants.DIRECTION_FILTER,
                         {r'up',
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
                          })
        self.assertEqual(constants.DIHEDRAL_FILTER,
                         {r'flip',
                          r'flipdihedral',
                          r'fliphorizontal',
                          r'flipvertical',
                          r'rotate90',
                          })
        self.assertEqual(constants.SHIFT_FILTER,
                         {r'shifthorizontal',
                          r'shiftvertical',
                          r'shift',
                          })
        self.assertEqual(constants.TRANSFORM,
                         r'|'.join((r'shifthorizontal',
                                    r'fliphorizontal',
                                    r'shiftvertical',
                                    r'flipvertical',
                                    r'flipdihedral',
                                    r'anydirection',
                                    r'previous\*',
                                    r'orthogonal',
                                    r'horizontal',
                                    r'southwest',
                                    r'southeast',
                                    r'northwest',
                                    r'northeast',
                                    r'flipcolor',
                                    r'vertical',
                                    r'rotate90',
                                    r'rotate45',
                                    r'diagonal',
                                    r'next\*',
                                    r'shift',
                                    r'right',
                                    r'left',
                                    r'flip',
                                    r'down',
                                    r'up',
                                    )))
        self.assertEqual(constants.LEFT_PARENTHESIS, r'\(')
        self.assertEqual(constants.RIGHT_PARENTHESIS, r'\)')
        self.assertEqual(constants.LEFT_BRACE, r'\{')
        self.assertEqual(constants.RIGHT_BRACE, r'\}')
        self.assertEqual(constants.NUMBER, r'\d+')
        self.assertEqual(constants.DOUBLE_QUOTED_STRING,
                         r'"[^\\"]*(?:\\.[^\\"]*)*"')
        self.assertEqual(constants.COMMENT_STRING, r';[^\n]*')
        self.assertEqual(constants.PGN_FILE, r'\.pgn')
        self.assertEqual(constants.ALLOWED_STRINGS,
                         r'(?:1-0)|(?:0-1)|(?:1/2-1/2)|(?:[^\s]+\.pgn)')
        self.assertEqual(constants.ZERO_OR_MORE, r'\*')
        self.assertEqual(constants.ONE_OR_MORE, r'\+')
        self.assertEqual(constants.REPEAT_OPERATORS, r'\?|\*|\+')
        self.assertEqual(constants.BAD_TOKEN, r'\S+')
        self.assertEqual(constants.EDGING, r'\s|\(|\)|\{|\}')
        self.assertEqual(constants.REPEAT_EDGING, r'\s|\(|\)|\{|\}|\?|\*|\+')
        self.assertEqual(constants.LEADING, '(?<=\\s|\\(|\\)|\\{|\\})')
        self.assertEqual(constants.TRAILING, '(?=\s|\(|\)|\{|\}|\Z)')
        self.assertEqual(constants.REPEAT_TRAILING,
                         '(?=\s|\(|\)|\{|\}|\?|\*|\+|\Z)')
        self.assertEqual(
            constants.CQL_PATTERN,
            ''.join((
                '(\\()|',
                '(\\))|',
                '(\\{)|',
                '(\\})|',
                '(;[^\\n]*)|',
                '(?:\\A\\s*)(cql)(?=\\s|',
                '\\()|',
                '(?<=\\s|',
                '\\(|',
                '\\)|',
                '\\{|',
                '\\})((?:(?:(?:(?:[KQRBNPkqrbnpAa\\.])|',
                '(?:\\[[KQRBNPkqrbnpAa\\.]+\\]))(?:(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                '(?:[a-h]-[a-h][1-8])|',
                '(?:[a-h][1-8]-[1-8])|',
                '(?:[a-h][1-8]))|',
                '(?:\\[(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                '(?:[a-h]-[a-h][1-8])|',
                '(?:[a-h][1-8]-[1-8])|',
                '(?:[a-h][1-8]))(?:,(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                '(?:[a-h]-[a-h][1-8])|',
                '(?:[a-h][1-8]-[1-8])|',
                '(?:[a-h][1-8])))*\\])))|',
                '(?:(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                '(?:[a-h]-[a-h][1-8])|',
                '(?:[a-h][1-8]-[1-8])|',
                '(?:[a-h][1-8]))|',
                '(?:\\[(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                '(?:[a-h]-[a-h][1-8])|',
                '(?:[a-h][1-8]-[1-8])|',
                '(?:[a-h][1-8]))(?:,(?:(?:[a-h]-[a-h][1-8]-[1-8])|',
                '(?:[a-h]-[a-h][1-8])|',
                '(?:[a-h][1-8]-[1-8])|',
                '(?:[a-h][1-8])))*\\]))|',
                '(?:(?:[KQRBNPkqrbnpAa\\.])|',
                '(?:\\[[KQRBNPkqrbnpAa\\.]+\\]))))(?=\\s|',
                '\\(|\\)|\\{|\\}|\\?|\\*|\\+|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(variations|',
                'matchcount|gamenumber|output|',
                'input)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(shifthorizontal|',
                'fliphorizontal|shiftvertical|flipvertical|flipdihedral|',
                'anydirection|previous\\*|orthogonal|horizontal|',
                'southwest|southeast|northwest|northeast|flipcolor|',
                'vertical|rotate90|rotate45|diagonal|next\\*|shift|',
                'right|left|flip|down|up)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(beginvariation|',
                'lightsquares|darksquares|variation|stalemate|terminal|',
                'initial|check|mate|wtm|btm|',
                'any)(?=\\s|\\(|\\)|\\{|\\}|\\?|\\*|\\+|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(echoshifthorizontal|',
                'echofliphorizontal|echoshiftvertical|echoflipvertical|',
                'targetsquares|sourcesquares|lcasubstring|echorotate90|',
                'echorotate45|descendant|lcatarget|lcasource|echoshift|',
                'mismatch|echoflip|ancestor|tomove|lcasum|lcamax|',
                'match)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(enpassantsquare|',
                'enpassant|promote|empty|from|',
                'to)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(\\d+)(?=\\s|\\(|\\)|\\{|\\}|\\?|\\*|\\+|\\Z)|',
                '("[^\\\\"]*(?:\\\\.[^\\\\"]*)*")|',
                '(?<=\\s|\\(|\\)|\\{|\\})(or)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(not)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(attack)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(between)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(countsquares|',
                'power)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(elo)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(comment)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(hascomment)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(mainline)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(move)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(movenumber)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(previous2|',
                'previous|next2|next)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(on)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(player)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(powerdifference)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(ray)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(relation)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(result)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(sort)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(year)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(silent)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(event|site)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(square|piece)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(all|in)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(origin)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(\\$[a-zA-Z0-9]+)(?=\\s|\\(|\\)|\\{|\\}|\\?|\\*|\\+|\\Z)|',
                '(?<=\\s|\\(|\\)|\\{|\\})(white|black)(?=\\s|\\(|\\)|\\{|\\}|\\Z)|',
                '((?:1-0)|(?:0-1)|(?:1/2-1/2)|(?:[^\\s]+\\.pgn))|(\\?|\\*|\\+)|',
                '(\\S+)',
                )))
        self.assertEqual(constants.TOKEN_NAMES,
                         ' '.join(('left_parenthesis',
                                   'right_parenthesis',
                                   'left_brace',
                                   'right_brace',
                                   'comment_string',
                                   'cql',
                                   'piece_designator',
                                   'cql_parameter',
                                   'transform',
                                   'plain',
                                   'relation_parameter',
                                   'move_parameter',
                                   'number',
                                   'double_quoted_string',
                                   'or_',
                                   'not_',
                                   'attack',
                                   'between',
                                   'countsquares_power',
                                   'elo',
                                   'comment',
                                   'hascomment',
                                   'mainline',
                                   'move',
                                   'movenumber',
                                   'next_previous',
                                   'on',
                                   'player',
                                   'powerdifference',
                                   'ray',
                                   'relation',
                                   'result',
                                   'sort',
                                   'year',
                                   'silent',
                                   'site_event',
                                   'piece_square',
                                   'piece_square_keywords',
                                   'origin',
                                   'piece_square_variable',
                                   'white_black_keywords',
                                   'allowed_strings',
                                   'repeat_operators',
                                   'bad_token',
                                   )))
        self.assertEqual(constants.RANGE, 'range')
        self.assertEqual(constants.NAME_DELIMITER, '\n')
        self.assertEqual(len([c for c in dir(constants)
                              if not c.startswith('__')]), 185)
        self.assertEqual(len(constants.TOKEN_NAMES.split(' ')),
                         len(self.expected_matches((('', 1),))[0]))
        self.assertEqual(constants.RIGHT_PARENTHESIS_INDEX, 1)
        self.assertEqual(constants.LEFT_BRACE_INDEX, 2)
        self.assertEqual(constants.RIGHT_BRACE_INDEX, 3)
        self.assertEqual(constants.PIECE_DESIGNATOR_INDEX, 6)
        self.assertEqual(constants.PLAIN_INDEX, 9)
        self.assertEqual(constants.OR_INDEX, 14)
        self.assertEqual(constants.NOT_INDEX, 15)
        self.assertEqual(constants.ON_INDEX, 26)

    def test_compiled_CQL_PATTERN(self):
        """"""
        pm = re.compile(constants.CQL_PATTERN, flags=re.DOTALL)

        # Examples of each element in the match.
        self.assertEqual(
            pm.findall('('),
            self.expected_matches((('(', 0),)))
        self.assertEqual(
            pm.findall(')'),
            self.expected_matches(((')', 1),)))
        self.assertEqual(
            pm.findall('{'),
            self.expected_matches((('{', 2),)))
        self.assertEqual(
            pm.findall('}'),
            self.expected_matches((('}', 3),)))
        self.assertEqual(
            pm.findall(';comment'),
            self.expected_matches(((';comment', 4),)))
        self.assertEqual(
            pm.findall('cql('),
            self.expected_matches((('cql', 5),('(', 0),)))
        self.assertEqual(
            pm.findall(' cql('),
            self.expected_matches((('cql', 5),('(', 0),)))
        self.assertEqual(
            pm.findall('cql ('),
            self.expected_matches((('cql', 5),('(', 0),)))
        self.assertEqual(
            pm.findall(' cql ('),
            self.expected_matches((('cql', 5),('(', 0),)))
        self.assertEqual(
            pm.findall(' K'),
            self.expected_matches((('K', 6),)))
        self.assertEqual(
            pm.findall('(K'),
            self.expected_matches((('(', 0),('K', 6),)))
        self.assertEqual(
            pm.findall('{K'),
            self.expected_matches((('{', 2),('K', 6),)))
        self.assertEqual(
            pm.findall('( K'),
            self.expected_matches((('(', 0),('K', 6),)))
        self.assertEqual(
            pm.findall('{ K'),
            self.expected_matches((('{', 2),('K', 6),)))
        self.assertEqual(
            pm.findall(' K)'),
            self.expected_matches((('K', 6),(')', 1),)))
        self.assertEqual(
            pm.findall(' K )'),
            self.expected_matches((('K', 6),(')', 1),)))
        self.assertEqual(
            pm.findall(' K}'),
            self.expected_matches((('K', 6),('}', 3),)))
        self.assertEqual(
            pm.findall(' K }'),
            self.expected_matches((('K', 6),('}', 3),)))
        self.assertEqual(
            pm.findall(')K'),
            self.expected_matches(((')', 1),('K', 6),)))
        self.assertEqual(
            pm.findall('}K'),
            self.expected_matches((('}', 3),('K', 6),)))
        self.assertEqual(
            pm.findall(') K'),
            self.expected_matches(((')', 1),('K', 6),)))
        self.assertEqual(
            pm.findall('} K'),
            self.expected_matches((('}', 3),('K', 6),)))
        self.assertEqual(
            pm.findall(' K('),
            self.expected_matches((('K', 6),('(', 0),))) # lex only here
        self.assertEqual(
            pm.findall(' K ('),
            self.expected_matches((('K', 6),('(', 0),))) # lex only here
        self.assertEqual(
            pm.findall(' K{'),
            self.expected_matches((('K', 6),('{', 2),)))
        self.assertEqual(
            pm.findall(' K {'),
            self.expected_matches((('K', 6),('{', 2),)))
        self.assertEqual(
            pm.findall(' input'),
            self.expected_matches((('input', 7),)))
        self.assertEqual(
            pm.findall(' shift'),
            self.expected_matches((('shift', 8),)))
        self.assertEqual(
            pm.findall(' wtm'),
            self.expected_matches((('wtm', 9),)))
        self.assertEqual(
            pm.findall(' lcamax'),
            self.expected_matches((('lcamax', 10),)))
        self.assertEqual(
            pm.findall(' from'),
            self.expected_matches((('from', 11),)))
        self.assertEqual(
            pm.findall(' 13'),
            self.expected_matches((('13', 12),)))
        self.assertEqual(
            pm.findall('"string"'),
            self.expected_matches((('"string"', 13),)))
        self.assertEqual(
            pm.findall(' or'),
            self.expected_matches((('or', 14),)))
        self.assertEqual(
            pm.findall(' not'),
            self.expected_matches((('not', 15),)))
        self.assertEqual(
            pm.findall(' attack'),
            self.expected_matches((('attack', 16),)))
        self.assertEqual(
            pm.findall(' between'),
            self.expected_matches((('between', 17),)))
        self.assertEqual(
            pm.findall(' power'),
            self.expected_matches((('power', 18),)))
        self.assertEqual(
            pm.findall(' elo'),
            self.expected_matches((('elo', 19),)))
        self.assertEqual(
            pm.findall(' comment'),
            self.expected_matches((('comment', 20),)))
        self.assertEqual(
            pm.findall(' hascomment'),
            self.expected_matches((('hascomment', 21),)))
        self.assertEqual(
            pm.findall(' mainline'),
            self.expected_matches((('mainline', 22),)))
        self.assertEqual(
            pm.findall(' move'),
            self.expected_matches((('move', 23),)))
        self.assertEqual(
            pm.findall(' movenumber'),
            self.expected_matches((('movenumber', 24),)))
        self.assertEqual(
            pm.findall(' next2'),
            self.expected_matches((('next2', 25),)))
        self.assertEqual(
            pm.findall(' on'),
            self.expected_matches((('on', 26),)))
        self.assertEqual(
            pm.findall(' player'),
            self.expected_matches((('player', 27),)))
        self.assertEqual(
            pm.findall(' powerdifference'),
            self.expected_matches((('powerdifference', 28),)))
        self.assertEqual(
            pm.findall(' ray'),
            self.expected_matches((('ray', 29),)))
        self.assertEqual(
            pm.findall(' relation'),
            self.expected_matches((('relation', 30),)))
        self.assertEqual(
            pm.findall(' result'),
            self.expected_matches((('result', 31),)))
        self.assertEqual(
            pm.findall(' sort'),
            self.expected_matches((('sort', 32),)))
        self.assertEqual(
            pm.findall(' year'),
            self.expected_matches((('year', 33),)))
        self.assertEqual(
            pm.findall(' silent'),
            self.expected_matches((('silent', 34),)))
        self.assertEqual(
            pm.findall(' event'),
            self.expected_matches((('event', 35),)))
        self.assertEqual(
            pm.findall(' piece'),
            self.expected_matches((('piece', 36),)))
        self.assertEqual(
            pm.findall(' in'),
            self.expected_matches((('in', 37),)))
        self.assertEqual(
            pm.findall(' origin'),
            self.expected_matches((('origin', 38),)))
        self.assertEqual(
            pm.findall(' $x '),
            self.expected_matches((('$x', 39),))) # Trailing [^a-zA-Z0-9] ends.
        self.assertEqual(
            pm.findall(' white'),
            self.expected_matches((('white', 40),)))
        self.assertEqual(
            pm.findall(' 1-0'),
            self.expected_matches((('1-0', 41),)))
        self.assertEqual(
            pm.findall('*'),
            self.expected_matches((('*', 42),)))
        self.assertEqual(
            pm.findall('qwerty'),
            self.expected_matches((('qwerty', 43),)))

        # Some which look like valid Chess Query Language
        self.assertEqual(
            pm.findall('\n'.join(('cql (',
                                  'input myfile.pgn',
                                  'output myfile_out.pgn',
                                  'gamenumber 100 25000',
                                  'year 1999 2013',
                                  'silent',
                                  'player "Jones"',
                                  'player white "Smith"',
                                  'player black "Wilson"',
                                  'elo 2200 2300',
                                  'elo white 1900 2000',
                                  'elo black 2050 2100',
                                  'site "London"',
                                  'event "4NCL"',
                                  'matchcount 1',
                                  'sort matchcount 1 3',
                                  ')'
                                  'Ra7',
                                  '{',
                                  '[Kk]a2-4',
                                  '}',
                                  'result 0-1',
                                  'result 1-0',
                                  'result 1/2-1/2',
                                  '; End of test',
                                  ))),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   ('input', 7),
                                   ('myfile.pgn', 41),
                                   ('output', 7),
                                   ('myfile_out.pgn', 41),
                                   ('gamenumber', 7),
                                   ('100', 12),
                                   ('25000', 12),
                                   ('year', 33),
                                   ('1999', 12),
                                   ('2013', 12),
                                   ('silent', 34),
                                   ('player', 27),
                                   ('"Jones"', 13),
                                   ('player', 27),
                                   ('white', 40),
                                   ('"Smith"', 13),
                                   ('player', 27),
                                   ('black', 40),
                                   ('"Wilson"', 13),
                                   ('elo', 19),
                                   ('2200', 12),
                                   ('2300', 12),
                                   ('elo', 19),
                                   ('white', 40),
                                   ('1900', 12),
                                   ('2000', 12),
                                   ('elo', 19),
                                   ('black', 40),
                                   ('2050', 12),
                                   ('2100', 12),
                                   ('site', 35),
                                   ('"London"', 13),
                                   ('event', 35),
                                   ('"4NCL"', 13),
                                   ('matchcount', 7),
                                   ('1', 12),
                                   ('sort', 32),
                                   ('matchcount', 7),
                                   ('1', 12),
                                   ('3', 12),
                                   (')', 1),
                                   ('Ra7', 6),
                                   ('{', 2),
                                   ('[Kk]a2-4', 6),
                                   ('}', 3),
                                   ('result', 31),
                                   ('0-1', 41),
                                   ('result', 31),
                                   ('1-0', 41),
                                   ('result', 31),
                                   ('1/2-1/2', 41),
                                   ('; End of test', 4),
                                   )))
        self.assertEqual(
            pm.findall('cql () wtm'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('wtm', 9),
                                   )))
        self.assertEqual(
            pm.findall('cql () shift 1 3 k'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('shift', 8),
                                   ('1', 12),
                                   ('3', 12),
                                   ('k', 6),
                                   )))
        self.assertEqual(
            pm.findall('cql() diagonal k or q'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('diagonal', 8),
                                   ('k', 6),
                                   ('or', 14),
                                   ('q', 6),
                                   )))
        self.assertEqual(
            pm.findall('cql() not k'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('not', 15),
                                   ('k', 6),
                                   )))
        self.assertEqual(
            pm.findall('cql(){}'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('{', 2),
                                   ('}', 3),
                                   )))
        self.assertEqual(
            pm.findall('cql();comment'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   (';comment', 4),
                                   )))
        self.assertEqual(
            pm.findall('cql()attack(Q r)'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('attack', 16),
                                   ('(', 0),
                                   ('Q', 6),
                                   ('r', 6),
                                   (')', 1),
                                   )))
        self.assertEqual(
            pm.findall('cql() elo 2500'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('elo', 19),
                                   ('2500', 12),
                                   )))
        self.assertEqual(
            pm.findall('cql() mainline'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('mainline', 22),
                                   )))
        self.assertEqual(
            pm.findall('cql()mainline'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('mainline', 22),
                                   )))
        self.assertEqual(
            pm.findall('cql() variation'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('variation', 9)
                                   )))
        self.assertEqual(
            pm.findall('cql() move 20 35'),
            self.expected_matches((('cql', 5),
                                   ('(', 0),
                                   (')', 1),
                                   ('move', 23),
                                   ('20', 12),
                                   ('35', 12),
                                   )))
        

if __name__ == '__main__':
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(CQLConstants))

