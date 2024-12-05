# chessql_example.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running chessql to produce output equivalent to '-parse'."""

import os
import tkinter.filedialog
import sys

from ..core import parser


if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[-1]):
        query = sys.argv[-1]
    elif len(sys.argv) > 1 and os.path.isdir(sys.argv[-1]):
        query = tkinter.filedialog.askopenfilename(
            title="CQL file", initialdir=os.path.expanduser(sys.argv[-1])
        )
    else:
        query = tkinter.filedialog.askopenfilename(
            title="CQL file", initialdir=os.path.expanduser("~")
        )
    if query:
        no_exception = True
        no_trace_exception = True
        tokens_only = "tokens_only" in sys.argv[1:-1]
        tree_only = "tree_only" in sys.argv[1:-1]
        if tree_only:
            tokens_only = False
        with open(query, mode="r", encoding="utf-8") as queryfile:
            container = parser.parse_debug(
                queryfile.read(), tree_only=tree_only, tokens_only=tokens_only
            )
        print()
        flat_trace = []
        container.whitespace_flat_trace(trace=flat_trace)
        print("\n".join(flat_trace))
        print()
        print("\n".join(container.parse_parameter_trace()))
        print()
        tree_trace = []
        container.parse_tree_trace(trace=tree_trace)
        print("\n".join(tree_trace))
