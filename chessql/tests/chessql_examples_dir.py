# chessql_examples_dir.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running chessql to produce output equivalent to '-parse'."""

import os
import tkinter.filedialog
import sys

from ..core import parser


def print_query(container):
    """Print parsed query."""
    print(container)
    print({k: v for k, v in container.__dict__.items() if k != "children"})
    print("children")
    for cqlobject in container.children:
        print(cqlobject.__class__.__name__, " ", cqlobject.match_)


if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[-1]):
        querydir = sys.argv[-1]
    else:
        querydir = tkinter.filedialog.askdirectory(
            title="CQL query directory", initialdir=os.path.expanduser("~")
        )
    if querydir:
        files_only = "files_only" in sys.argv[1:-1]
        print("directory", querydir)
        for file in sorted(os.listdir(querydir)):
            if os.path.splitext(file)[-1] != ".cql":
                continue
            querypath = os.path.join(querydir, file)
            if not files_only:
                print()
            print(querypath)
            with open(querypath, mode="r", encoding="utf-8") as queryfile:
                container = parser.parse(queryfile.read())
                if not files_only:
                    print_query(container)
