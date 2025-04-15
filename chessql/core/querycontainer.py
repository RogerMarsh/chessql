# querycontainer.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) object class definitions.

This module defines the QueryContainer class.  An instance of this class
is the root node of a query structure.

"""
from . import basenode
from . import constants
from . import structure
from . import options


class _QueryParameters(basenode.BaseNode):
    """User definitions, cql parameters, and command line options.

    The parameters property is the set of arguments given in a 'cql()'
    statement at the beginning of a '*.cql' file.

    The options property is an Options instance which contains options
    passed to cql on the command line.
    """

    def __init__(self, match_=None, container=None):
        """Delegate then set details for root of node tree."""
        if match_ is not None:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects match_ to be a ",
                None.__class__.__name__.join("''"),
                " but it is a ",
                match_.__class__.__name__.join("''"),
            )
        if container is not None:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects container to be a ",
                None.__class__.__name__.join("''"),
                " but it is a ",
                container.__class__.__name__.join("''"),
            )
        self._cursor = self

        super().__init__(match_=match_, container=self)

        # Names of user defined objects and their parameters.
        # These are functions, function bodies, variables, and dictionaries.
        self._definitions = {}

        # Unique identifier for generated variable names.
        self._next_reserved_name_id = 0

        # Parameters given as '...' in 'cql(...)' at start of query.
        self._parameters = set()

        # Options given on command line when invoking query.
        # Populate options instance by calling it's get_options method.
        self._options = options.Options()

    @property
    def cursor(self):
        """Return self._cursor."""
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        """Bind self._cursor to value."""
        if not isinstance(value, basenode.BaseNode):
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " expects cursor to be a ",
                basenode.BaseNode.__name__.join("''"),
                " but it is a ",
                value.__class__.__name__.join("''"),
            )
        self._cursor = value

    @property
    def definitions(self):
        """Return self._definitions."""
        return self._definitions

    @property
    def parameters(self):
        """Return self._parameters."""
        return self._parameters

    @property
    def options(self):
        """Return self._options."""
        return self._options


class QueryContainer(_QueryParameters, basenode.BaseNode):
    """The top level node for a CQL statement.

    The children, parameters, and options, properties represent the things
    found in the command line for cqlincluding the *.cql file.
    """

    def __init__(self, match_=None, container=None):
        """Delegate then set details for root of node tree."""
        # FunctionBodyLeft instance accepting input tokens.
        # The instance which caused increment of _function_body_count to 1.
        self._function_body_cursor = None

        super().__init__(match_=match_, container=container)
        self._parent = None
        self._whitespace = []

        # Nodes whose verify_children_and_set_types() method has
        # been called.
        self._verified = set()

        # Number of stacked incomplete function bodies.
        # The count is needed because function definitions can be nested.
        self._function_body_count = 0

        # The match for the token currently being processed.
        # Kept for reporting parsing errors.
        self.current_token = None

    @property
    def function_body_count(self):
        """Return self._function_body_count."""
        return self._function_body_count

    @function_body_count.setter
    def function_body_count(self, value):
        """Bind self._function_body_count to value."""
        self._function_body_count = value

    @property
    def function_body_cursor(self):
        """Return self._function_body_cursor."""
        return self._function_body_cursor

    @function_body_cursor.setter
    def function_body_cursor(self, value):
        """Bind self._function_body_cursor to value."""
        self._function_body_cursor = value

    @property
    def whitespace(self):
        """Return self._whitespace."""
        return self._whitespace

    @property
    def verified(self):
        """Return self._verified."""
        return self._verified

    def get_next_variable_prefix(self):
        """Return str of next prefix for variable names.

        A function call will prefix it's formal parameters with the
        returned value to form the call's argument names.

        """
        self._next_reserved_name_id += 1
        return "_".join(
            (constants.LOWER_CASE_CQL_PREFIX, str(self._next_reserved_name_id))
        )

    def complete(self):
        """Return False.

        The QueryContainer is never full, the query just ends.

        """
        return False

    def full(self):
        """Return False.

        The full condition is the same as the complete condition.

        """
        return False

    def place_node_in_tree(self):
        """Verify container is self with one child, then clear children."""
        container = self.container
        if container is not self:
            self.raise_nodeerror(
                "'container' object is not 'self' QueryContainer node."
            )
        if len(container.children) != 1:
            self.raise_nodeerror(
                "'container' object does not have exactly one child node."
            )
        if container.children[0] is not self:
            self.raise_nodeerror(
                "The child object of 'container' object is not 'self'."
            )
        container.children.clear()

    # This method exists to allow BaseNode and QueryContainer classes to be in
    # separate modules.
    # It should be a design flaw that the test is needed.
    # The existence, and use of this method in BaseNode.__init__(), can do the
    # job of the 'assert isinstance(container, QueryContainer)' statement
    # in BaseNode.__init__().
    def is_cursor_moveinfix_instance(self):
        """Return True if self._cursor is an instance of MoveInfix."""
        return isinstance(self._cursor, structure.MoveInfix)

    def whitespace_flat_trace(self, trace=None):
        """Return whitespace trace for node in a print format."""
        if trace is None:
            trace = []
        for node in self._whitespace:
            match_ = " ".join((str(node.match_.span()), repr(node.match_[0])))
            trace.append(
                " ".join(
                    (
                        node.__class__.__name__,
                        match_,
                    )
                )
            )

    def parse_parameter_trace(self):
        """Return list of parameters for self in a print format."""
        trace = []
        for item in self._parameters:
            trace.append(
                [item.__class__.__name__, item.match_.group().split()[0]]
            )
            if isinstance(item.parameter_value, str):
                trace[-1].append(item.parameter_value)
            elif isinstance(item.parameter_value, list):
                trace[-1].append(" ".join(item.parameter_value))
        return [" ".join(t) for t in sorted(trace)]

    def raise_if_not_single_match_groupdict_entry(self, token, entries):
        """Raise NodeError if entries has more than one item for token."""
        if len(entries) != 1:
            self.raise_nodeerror(
                "'",
                self.__class__.__name__,
                "' a single groupdict entry is expected frpm match on '",
                token.group(),
                "' but got ",
                str(len(entries)),
            )
