# chessql_cql_example.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running cql to produce '-parse' output."""

import os
import re
import tkinter.filedialog
import sys
import subprocess


if __name__ == "__main__":
    if len(sys.argv) == 2 and os.path.isfile(sys.argv[-1]):
        query = sys.argv[-1]
    elif len(sys.argv) == 2 and os.path.isdir(sys.argv[-1]):
        query = tkinter.filedialog.askopenfilename(
            title="CQL file", initialdir=os.path.expanduser(sys.argv[-1])
        )
    else:
        query = tkinter.filedialog.askopenfilename(
            title="CQL file", initialdir=os.path.expanduser("~")
        )
    if query:
        process = subprocess.run(
            [
                "cql",
                "-input",
                os.path.expanduser(os.path.join("~", "sample.pgn")),
                # "-output",
                # os.path.expanduser(os.path.join("~", "sample-out.pgn")),
                "-parse",
                query,
            ]
        )
        print(process.returncode)
