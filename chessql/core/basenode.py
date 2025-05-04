# structure.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) object class definitions.

This module defines the classes and functions needed by objects referred
to by the object which are values in the cql.class_from_token_name dict
which are not such values themselves.  Classes for whom instances are
returned by those values which are functions are kept in filters even
if not values in cql.class_from_token_name dict.

"""
from . import constants
from . import cqltypes


def debug(tag, node):
    """Print details of node prefixed by tag."""
    print(
        tag,
        node.__class__.__name__,
        node.complete(),
        node.full(),
        [c.__class__.__name__ for c in node.children],
        node.precedence,
    )


class NodeError(Exception):
    """Exception raised for problems in BaseNode and subclasses."""


class BaseNode:
    """Record the parent, child, and sibling, relationships of nodes.

    The children property contains a list of the class instances which
    represent the parameters and arguments of a filter represented by a
    BaseNode instance.  Parameters are not usually filters themselves
    but arguments usually are filters too.
    """

    # Filters do not have a type by default.
    # Some subclasses may be one several types of filter.
    # The subclass should override _filter_type to the appropriate subset
    # of cqltypes.FilterType.ANY, and each instance should set the instance
    # attribute _filter_type to one of these if the correct one can be
    # deduced.
    # In many cases the subclass _filter_type will be one of the options.
    # See gadycosteff.com/cql/filter.html for derivation of attribute names
    # for the filter type.
    _filter_type = ~cqltypes.FilterType.ANY

    # In BaseNode not CQLObject because the value is tested in a place where
    # node being an instance of QueryContainer cannot be avoided except
    # by an additional 'if not isinstance(<obj>, QueryContainer)' clause
    # protecting the test.  See NoArgumentsFilter.__init__().
    _is_parameter = False

    # Most nodes take zero or one child nodes.  The infix nodes take two
    # child nodes.  The 'If' node takes two or three child nodes, the
    # third being the 'Else' node if present.  The nodes which represent
    # '{}' and '()' sequences can have any number of nodes, but in some
    # contexts the number itself will not be variable.  Nodes which
    # represent filters with an implicit search parameter can have zero
    # or one child node; and None is the appropriate _child_count value.
    # Default is None.  Override with 0 or 1 or 2.
    # Where the default is not overridden the subclass must override the
    # complete() method as needed.
    _child_count = None

    # Operation precedence.
    # Default is set to None but subclasses which accept child filters
    # should set precedence to the appropriate cqltypes.Precedence value
    # to implement the table of precedence in the CQL documentation.
    _precedence = None

    # A filter is not complete until it's completion condition is met.
    # Then the <instance>.completed attribute is set True, done by the
    # complete() method.
    completed = False

    # BaseNode instances do not have a name, except those which are also
    # Name instances.
    _name = None

    def __init__(self, match_=None, container=None):
        """Initialise node parent and children attributes."""
        self._children = []
        self.match_ = match_
        self._container = container
        container.cursor.children.append(self)
        self._parent = container.cursor
        if container.function_body_cursor is not None:
            container.definitions[
                container.function_body_cursor.name
            ].body.append(match_)

    @property
    def filter_type(self):
        """Return self._filter_type."""
        return self._filter_type

    @filter_type.setter
    def filter_type(self, value):
        """Set self._filter_type."""
        self._filter_type = value

    @property
    def children(self):
        """Return self._children."""
        return self._children

    @property
    def container(self):
        """Return self._container."""
        return self._container

    @property
    def parent(self):
        """Return self._parent."""
        return self._parent

    @property
    def name(self):
        """Return self._name.

        The Name class provides a setter for thie property.

        """
        return self._name

    @property
    def is_parameter(self):
        """Return True if BaseNode instance is a Parameter."""
        return bool(self._is_parameter)

    @property
    def child_count(self):
        """Return self._child_count."""
        return self._child_count

    @property
    def precedence(self):
        """Return self._precedence."""
        return self._precedence

    def is_parameter_accepted_by_filter(self):
        """Return False because parameters are not accepted by default.

        Subclasses should override as needed.

        When counting children to test if a filter is complete or full,
        parameters which are not accepted by the filter are included in
        the count but those which are accepted are excluded.

        """
        return False

    def complete(self):
        """Return True if node has more than it's complement of children.

        The next token after the node gets it's complement of children is
        appended to it's children and signals the node stack should be
        collapsed to the nearest ancestor without it's complement of
        children.

        In most cases comparing len(children) with _child_count will do.

        """
        return (
            len(self.children)
            - len(
                [
                    c
                    for c in self.children
                    if c.is_parameter and c.is_parameter_accepted_by_filter()
                ]
            )
            > self._child_count
        )

    def full(self):
        """Return True if node has it's complement of children or more.

        This method differs from complete() in the test on _child_count.

        The method is used when collapsing the ancestor stack to the
        nearest ancestor which could accept the token.

        In most cases comparing len(children) with _child_count will do.

        """
        return (
            len(self.children)
            - len(
                [
                    c
                    for c in self.children
                    if c.is_parameter and c.is_parameter_accepted_by_filter()
                ]
            )
            >= self._child_count
        )

    def _verify_children_and_set_own_types(self):
        """Do nothing: subclasses should override as necessary."""

    def verify_children_and_set_types(self, set_node_completed=False):
        """Verify children and adjust types if complete or full.

        This method is usually called from a place_node_in_tree method.

        Except for CQL user-defined variables this is filter type.  For
        variables the persistence and variable types may need adjusting
        too.

        This method checks the object has not already been verified and
        calls _verify_children_and_set_own_types to do the task.
        """
        verified = self.container.verified
        if self in verified:
            self.raise_nodeerror(
                self.__class__.__name__.join("''"),
                " instance has already been verified",
            )
        verified.add(self)
        if set_node_completed:
            self.completed = True
        self._verify_children_and_set_own_types()

    # An isinstance solution is preferred.
    def _is_variable(self):
        """Return True if token is a Variable instance.

        Subclasses should override and return True if appropriate.

        """
        return False

    def place_node_in_tree(self):
        """Move self to correct container location if initial place is wrong.

        The default action is to do nothing and leave this node where it is.

        This method should be overridden where necessary.

        Nodes are appended to the children of the container.cursor node when
        created.

        Many node types take no children so if this node was created as a
        child of a node of such types it has to be moved.

        Many node types take exactly one child so if this node is the
        second child of a node of such types it has to be moved.

        The remaining node types take different numbers of children so if
        this node is a child of a node of such types it has to be moved
        if conditions dictate.

        When this node is moved container.cursor is adjusted to be the node
        of which this node became a child.

        """
        node = self.parent
        while node and node.complete():
            node.children[-1].parent = node.parent
            node.parent.children.append(node.children.pop())
            node.verify_children_and_set_types(set_node_completed=True)
            node = node.parent
        return node

    def get_match_text(self):
        """Return the text to drive evaluation of represented filter.

        For most BaseNode subclass instances this text will be the text
        in self.match_.group().

        For the other instances this text gives the reason for existence
        of an implicit filter.  In these cases it is assumed the text to
        drive evaluation is some constant.  Subclasses for these cases
        should override this method and return the relevant constant.

        """
        return self.match_.group()

    def _str_filter_type(self):
        """Return name of filter type or an error report."""
        try:
            filter_type = self.filter_type
            name = filter_type.name
            if name is None:
                name = str(None)
            return "f: " + name
        except (NodeError, IndexError) as exc:
            return str(exc)

    def _str_variable_type(self):
        """Return name of variable type or an error report."""
        try:
            item = self.container.definitions.get(self.name)
            if item is None:
                return "v: " + str(None)
            return "v: " + item.variable_type.name
        except AttributeError as exc:
            return str(exc)

    def _str_key_filter_type(self):
        """Return name of dictionary key filter type or an error report."""
        try:
            item = self.container.definitions.get(self.name)
            if item is None:
                return "k: " + str(None)
            return "k: " + item.key_filter_type.name
        except AttributeError as exc:
            return str(exc)

    def _str_persistence_type(self):
        """Return name of persistence type or an error report."""
        try:
            item = self.container.definitions.get(self.name)
            if item is None:
                return "p: " + str(None)
            return "p: " + item.persistence_type.name
        except AttributeError as exc:
            return str(exc)

    def parse_tree_trace(self, trace=None):
        """Populate trace with parse tree for node in a print format.

        Trace should be a list.  On exit it will contain a str for each node
        indicating the number od ancestors, node type, and source string in
        CQL statement represented by the node.

        """
        if trace is None:
            trace = []
        depth = 0
        node = self
        while node:
            depth += 1
            node = node.parent
        if self._is_variable() and self._name.startswith(
            constants.LOWER_CASE_CQL_PREFIX
        ):
            node = self
            while True:
                if node is None:
                    node = " unknown function"
                    break
                if node.is_node_functioncall_instance():
                    node = node.match_[0][:-1].join((" of function '", "'"))
                    break
                node = node.parent
            name = self.match_[0]
            if name.startswith(constants.LOWER_CASE_CQL_PREFIX):
                # pycodestyle E203 whitespace before ':'.
                # black insists on " : " format.
                name = name[len(constants.LOWER_CASE_CQL_PREFIX) :]
                index = name.index("_")
                # pycodestyle E203 whitespace before ':'.
                # black insists on " : " format.
                name = name[index + 1 :]
            match_ = " ".join(
                (
                    str(self.match_.span()),
                    repr(self._name),
                    "".join(
                        (
                            "for parameter '",
                            name,
                            "'",
                            node,
                        )
                    ),
                )
            )
        else:
            match_ = self._match_string()
        type_strings = []
        type_strings.append(self._str_filter_type())
        if self._is_node_dictionary_instance():
            type_strings.append(self._str_key_filter_type())
            type_strings.append(self._str_persistence_type())
        if self._is_node_variablename_instance():
            type_strings.append(self._str_variable_type())
            type_strings.append(self._str_persistence_type())
        # pylint C0209 consider-using-f-string.  f"{depth:>3}" not used
        # because 'depth' gets coloured as a "string" (typically green)
        # rather than as a local attribute (typically black).
        # The f-string documentation colours it 'right':
        # docs.python.org/3.10/reference/lexical_analysis.html#f-strings
        # but the Idle I have colours everything within the quotes green.
        # Ah! See github.com/python/cpython/issues/73473.
        trace.append(
            " ".join(
                (
                    "{:>3}".format(depth),
                    " " * depth,
                    self.__class__.__name__,
                    match_,
                    " ".join(type_strings),
                )
            )
        )
        for node in self._children:
            node.parse_tree_trace(trace=trace)

    def print_parse_tree_trace(self):
        """Print the parse tree rooted at self.

        Convenient for print debugging just before a raise statement.

        """
        tree_trace = []
        self.parse_tree_trace(trace=tree_trace)
        print("\n".join(tree_trace))

    def parse_tree_node(self, trace=None):
        """Return trace with parse tree for node.

        Trace should be a list.  On exit it will contain a tuple:
            (<depth>, <subclass of BaseNode>)
        for each node where depth indicates the number of ancestors.

        """
        if trace is None:
            trace = []
        depth = 0
        node = self
        while node:
            depth += 1
            node = node.parent
        trace.append((depth, self))
        for node in self._children:
            node.parse_tree_node(trace=trace)

    # This method exists to allow BaseNode and CQLObject classes to be in
    # separate modules.
    def _match_string(self):
        """Return class name.

        Subclasses should override to return the span of the match where
        available.

        """
        return self.__class__.__name__

    # This method exists to allow BaseNode and FunctionCall classes to be in
    # separate modules.
    def is_node_functioncall_instance(self):
        """Return False.

        The FunctionCall subclass overrides to return True.

        """
        return False

    # This method exists to allow BaseNode and Dictionary classes to be in
    # separate modules.
    def _is_node_dictionary_instance(self):
        """Return False.

        The Dictionary subclass overrides to return True.

        """
        return False

    # This method exists to allow BaseNode and VariableName classes to be in
    # separate modules.
    def _is_node_variablename_instance(self):
        """Return False.

        The VariableName subclass overrides to return True.

        """
        return False

    def raise_nodeerror(self, *message_str):
        """Raise a NodeError with concatenated *message_str."""
        raise NodeError("".join(message_str))
