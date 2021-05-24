# node.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) statement filter node."""

import copy

from .cql import TokenTypes, Token, RANGE, QUOTED_STRING, FUNCTION_NAME


class NodeError(Exception):
    pass


class Node:
    """"""
    # self.tokendef.name == 'not' means the result of the first child node is
    # inverted.
    # 'cql() not p k' produces a 'not' node with two children, 'p' node first.
    # 'cql() not p or k produces a 'not' node with one child, an 'or' node
    #  which has two children, nodes for 'p' and 'q'.
    
    def __init__(self, tokendef, children=None, leaf=None):
        """"""
        super().__init__()
        self.tokendef = tokendef
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf
        self.parameters = {}
        self._precedence = None
        self._returntype = None

    @property
    def name(self):
        t = self.tokendef
        return t.variant_name if t.variant_name is not None else t.name

    @property
    def precedence(self):
        if self._precedence is None:
            return self.tokendef.precedence
        else:
            return self._precedence

    @precedence.setter
    def precedence(self, value):
        if self._precedence is None:
            self._precedence = value

    @property
    def returntype(self):
        if self._returntype is None:
            return self.tokendef.returntype
        else:
            return self._returntype

    @returntype.setter
    def returntype(self, value):
        if self._returntype is None:
            if len(self.tokendef.returntype) > 1:
                self._returntype = frozenset((value,))

    # The name, tokendef[0] is always different; flags and arguments are
    # usually the same; and returntype is usually different.
    # The precedence and pattern, tokendef[2:4], are always the same.
    def set_tokendef_to_variant(
            self,
            tokendef,
            same_flags=True,
            same_returntype=False,
            same_arguments=True):
        if same_flags:
            assert tokendef[1] == self.tokendef[1]
            pass
        assert tokendef[2] == self.tokendef[2]
        #assert tokendef[3] in self.tokendef[3]
        if same_returntype:
            assert tokendef[4] == self.tokendef[4]
            pass
        if same_arguments:
            assert tokendef[5] == self.tokendef[5]
            pass
        self.tokendef = tokendef

    def __deepcopy__(self, memo):
        """"""
        newcopy = empty_copy(self)
        newcopy.tokendef = self.tokendef
        newcopy.children = copy.deepcopy(self.children, memo)
        newcopy.leaf = copy.deepcopy(self.leaf, memo)
        newcopy.parameters = copy.deepcopy(self.parameters, memo)
        return newcopy

    def __str__(self):

        # Assumption is these four parameters are mutually exclusive.
        for rp in (RANGE, Token.REPEATRANGE, Token.FUNCTION, QUOTED_STRING,
                   FUNCTION_NAME):
            if rp in self.parameters:
                r = self.parameters[rp]
                if isinstance(r, str):
                    s = [''.join((self.name, '<', r, '>'))]
                elif len(r) == 1:
                    s = [''.join((self.name, '<', str(r[0]), '>'))]
                elif len(r) == 2:
                    s = [''.join(
                        (self.name, '<', str(r[0]), ',', str(r[1]), '>'))]
                elif rp is Token.FUNCTION:
                    s = [''.join((self.name, '<', ','.join(r), '>'))]
                else:
                    s = [''.join((self.name, '<?,?>'))]
                break
        else:
            s = [self.name]

        for p in self.parameters:
            if p is rp:
                continue
            s.extend(('<', p.name, '>'))
        if self.children:
            d = ', '.join((str(c) for c in self.children)).join(('[', ']'))
        else:
            d = str(self.leaf)
        return ', '.join((''.join(s), d)).join(('(', ')'))

    @property
    def occupied(self):
        return bool(self.children or self.leaf)

    # Not used at present: *.tokendef may need changing to *.name.
    def repeated_parameter(self, t=None):
        """"""
        if t is None:
            t = self.tokendef
        return t in {n.tokendef for n in self.children}

    # Not used at present: *.tokendef may need changing to *.name.
    def get_repeatable_parameter(self, t, node_factory):
        """"""
        for n in self.children:
            if t == n.tokendef:
                return n
        self.children.append(node_factory(t))
        return self.children[-1]


def empty_copy(obj):
    class Empty(obj.__class__):
        def __init__(self):
            pass
    newcopy = Empty()
    newcopy.__class__ = obj.__class__
    return newcopy
