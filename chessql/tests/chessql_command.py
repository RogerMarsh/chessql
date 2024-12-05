# chessql_command.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running chessql to produce output equivalent to '-parse'."""

from ..core import parser


if __name__ == "__main__":
    container = parser.parse_command_line_query()
    print("** option errors **")
    for error in container.options.errors:
        print(error)
    print("** options **")
    for element in container.options.options:
        print(element.__class__.__name__, element.operands)
    print("** parameters **")
    if container.parameters:
        print("\n".join(container.parse_parameter_trace()))
    print("** tree **")
    tree_trace = []
    container.parse_tree_trace(trace=tree_trace)
    if tree_trace:
        print("\n".join(tree_trace))
    print("** done **")
