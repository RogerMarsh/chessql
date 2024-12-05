# chessql_cqli_examples_dir.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Run cqli to produce '-parse' output for files in directory.

Written for wine64 on FreeBSD.
"""

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
    if len(sys.argv) == 2 and os.path.isdir(sys.argv[-1]):
        querydir = sys.argv[-1]
    elif len(sys.argv) > 2:
        querydir = ""
        print("Too many arguments")
    else:
        querydir = tkinter.filedialog.askdirectory(
            title="CQL query directory", initialdir=os.path.expanduser("~")
        )
    if querydir:
        print("directory", querydir)
        for file in sorted(os.listdir(querydir)):
            if os.path.splitext(file)[-1] != ".cql":
                continue
            querypath = os.path.join(querydir, file)
            print(querypath)
            process = subprocess.run(
                run_prefix
                + [
                    os.path.expanduser(os.path.join("~", "bin", "cqli.exe")),
                    "-input",
                    os.path.expanduser(os.path.join("~", "sample.pgn")),
                    # "-output",
                    # os.path.expanduser(os.path.join("~", "sample-out.pgn")),
                    "-parse",
                    querypath,
                ]
            )
            print(process.returncode)
