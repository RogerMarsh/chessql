# node.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) statement filter node."""

import copy

from .cql import Token, RANGE, QUOTED_STRING, FUNCTION_NAME
from . import empty_copy


class NodeError(Exception):
    """Exception raised for problems in Nodes."""


class Node:
    """An element generated when parsing a CQL statement."""

    # self.tokendef.name == 'not' means the result of the first child node is
    # inverted.
    # 'cql() not p k' produces a 'not' node with two children, 'p' node first.
    # 'cql() not p or k produces a 'not' node with one child, an 'or' node
    #  which has two children, nodes for 'p' and 'q'.

    def __init__(self, tokendef, children=None, leaf=None):
        """Initialise node.

        self.children is set to [] if children evaluates False.

        """
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
        """Return name of token type.

        This is self.tokendef.variant_name if set, or self.tokendef.name
        if not.

        """
        tdf = self.tokendef
        return tdf.variant_name if tdf.variant_name is not None else tdf.name

    @property
    def precedence(self):
        """Return precedence if set, or tokendef.precedence if not."""
        if self._precedence is None:
            return self.tokendef.precedence
        return self._precedence

    @precedence.setter
    def precedence(self, value):
        if self._precedence is None:
            self._precedence = value

    @property
    def returntype(self):
        """Return returntype if set, or tokendef.returntype if not."""
        if self._returntype is None:
            return self.tokendef.returntype
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
        same_arguments=True,
    ):
        """Adjust self to be same kind of token as tokendef."""
        if same_flags:
            assert tokendef[1] == self.tokendef[1]
        assert tokendef[2] == self.tokendef[2]
        # assert tokendef[3] in self.tokendef[3]
        if same_returntype:
            assert tokendef[4] == self.tokendef[4]
        if same_arguments:
            assert tokendef[5] == self.tokendef[5]
        self.tokendef = tokendef

    def __deepcopy__(self, memo):
        """Return deepcopy of self."""
        newcopy = empty_copy(self)
        newcopy.tokendef = self.tokendef
        newcopy.children = copy.deepcopy(self.children, memo)
        newcopy.leaf = copy.deepcopy(self.leaf, memo)
        newcopy.parameters = copy.deepcopy(self.parameters, memo)
        return newcopy

    def __str__(self):
        """Return string representation of self."""
        # Assumption is these four parameters are mutually exclusive.
        for rtd in (
            RANGE,
            Token.REPEATRANGE,
            Token.FUNCTION,
            QUOTED_STRING,
            FUNCTION_NAME,
        ):
            if rtd in self.parameters:
                rng = self.parameters[rtd]
                if isinstance(rng, str):
                    text = ["".join((self.name, "<", rng, ">"))]
                elif len(rng) == 1:
                    text = ["".join((self.name, "<", str(rng[0]), ">"))]
                elif len(rng) == 2:
                    text = [
                        "".join(
                            (
                                self.name,
                                "<",
                                str(rng[0]),
                                ",",
                                str(rng[1]),
                                ">",
                            )
                        )
                    ]
                elif rtd is Token.FUNCTION:
                    text = ["".join((self.name, "<", ",".join(rng), ">"))]
                else:
                    text = ["".join((self.name, "<?,?>"))]
                break
        else:
            text = [self.name]

        for parameter in self.parameters:
            if parameter is rtd:
                continue
            text.extend(("<", parameter.name, ">"))
        if self.children:
            dtxt = ", ".join((str(c) for c in self.children)).join(("[", "]"))
        else:
            dtxt = str(self.leaf)
        return ", ".join(("".join(text), dtxt)).join(("(", ")"))

    @property
    def occupied(self):
        """Return True if self has children or is a leaf."""
        return bool(self.children or self.leaf)

    # Not used at present: *.tokendef may need changing to *.name.
    def repeated_parameter(self, tokendef=None):
        """Return True if tokendef is in self's children."""
        if tokendef is None:
            tokendef = self.tokendef
        return tokendef in {n.tokendef for n in self.children}

    # Not used at present: *.tokendef may need changing to *.name.
    def get_repeatable_parameter(self, tokendef, node_factory):
        """Return first repeatable parameter tokendef in self's children.

        Create one if none exist yet.

        """
        for node in self.children:
            if tokendef == node.tokendef:
                return node
        self.children.append(node_factory(tokendef))
        return self.children[-1]
