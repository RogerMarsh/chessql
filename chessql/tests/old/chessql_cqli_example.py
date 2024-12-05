# chessql_cqli_example.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running cqli to produce '-parse' output."""

import os
import re
import tkinter.filedialog
import sys
import subprocess
import platform


if __name__ == "__main__":
    if platform.system() == "Windows":
        run_prefix = []
    elif platform.system() == "FreeBSD":
        run_prefix = ["wine64"]
    else:
        run_prefix = ["wine"]
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
            run_prefix
            + [
                "cqli",
                "-input",
                os.path.expanduser(os.path.join("~", "sample.pgn")),
                # "-output",
                # os.path.expanduser(os.path.join("~", "sample-out.pgn")),
                "-parse",
                query,
            ]
        )
        print(process.returncode)
