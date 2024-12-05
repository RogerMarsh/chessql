# chessql_options.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running chessql to produce output equivalent to '-parse'."""

from ..core import options


if __name__ == "__main__":
    opt = options.Options()
    opt.get_options()
    print("** errors **")
    for error in opt.errors:
        print(error)
    print("** options **")
    for element in opt.options:
        print(element.__class__.__name__, element.operands)
