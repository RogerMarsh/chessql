# chessql_examples_fail_dir.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running chessql to produce output equivalent to '-parse'.

To see exception traces inline in 'less' run this module in a script then
view the script file with 'less'.
"""

import os
import tkinter.filedialog
import sys

from ..core import parser

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
                    container.print_parse_tree_trace()
