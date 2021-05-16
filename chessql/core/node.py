# node.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) statement filter node."""

import copy


class Node:
    """"""
    # self.type == 'not' means the result of the first child node is inverted.
    # 'cql() not p k' produces a 'not' node with two children, 'p' node first.
    # 'cql() not p or k produces a 'not' node with one child, an 'or' node
    #  which has two children, nodes for 'p' and 'q'.
    
    def __init__(self, type_, children=None, leaf=None):
        """"""
        super().__init__()
        self.type = type_
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf
        self.range = []
        self.repeat = False
        self.setfilter = None

    def __deepcopy__(self, memo):
        """"""
        newcopy = empty_copy(self)
        newcopy.type = self.type
        newcopy.children = copy.deepcopy(self.children, memo)
        newcopy.leaf = copy.deepcopy(self.leaf, memo)
        newcopy.range = copy.deepcopy(self.range, memo)
        newcopy.repeat = self.repeat
        newcopy.setfilter = self.setfilter
        return newcopy

    def __str__(self):
        if not self.range:
            s = str(self.type)
        elif len(self.range) == 1:
            b, = self.range
            s = ''.join(str(i) for i in (self.type, '<', b, ',', b, '>'))
        elif len(self.range) == 2:
            b, e = self.range
            s = ''.join(str(i) for i in (self.type, '<', b, ',', e, '>'))
        else:
            s = ''.join(str(i) for i in (self.type, '<', '?', ',', '?', '>'))
        if self.repeat:
            s = ''.join((s, '<', self.repeat, '>'))
        return ', '.join((str(s),
                          ', '.join((str(c)
                                     for c in self.children)).join(('[', ']')),
                          str(self.leaf),
                          str(self.setfilter),
                          )).join(('(', ')'))

    @property
    def occupied(self):
        return bool(self.children or self.leaf)

    @property
    def children_setfilter_types(self):
        return {n.setfilter for n in self.children}

    def derive_filter_type_from_children(self):
        csft = self.children_setfilter_types
        if len(csft) > 1:
            self.setfilter = False
        elif self.range:
            self.setfilter = False
        else:
            self.setfilter = csft.pop()

    def derive_brace_filter_type_from_children(self):
        if len(self.children) > 1:
            self.setfilter = False
        elif self.range:
            self.setfilter = False
        else:
            self.derive_filter_type_from_children()

    def set_filter_type_all_children_setfilters(self):
        csft = self.children_setfilter_types
        if False in csft or True not in csft:
            return False
        elif self.range:
            self.setfilter = False
            return True
        self.setfilter = True
        return True

    def repeated_parameter(self, t=None):
        """"""
        if t is None:
            t = self.type
        return t in {n.type for n in self.children}

    def get_repeatable_parameter(self, t, node_factory):
        """"""
        for n in self.children:
            if t == n.type:
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
