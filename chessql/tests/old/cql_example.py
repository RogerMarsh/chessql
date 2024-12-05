# cql_example.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running cql in a subprocess to return '-parse' output.

'cql -parse -i sample.pgn <cql file>.cql' outputs a str containing
approximations to repr(token) for each token and repr(<abstract syntax tree>)
for the content of '<cql file>.cql'.

The '-i sample.pgn' argument overrides whatever the <cql file>.cql file
says in the cql(input <pgn file>.pgn) clause, but that does not matter
when parsing only and some cql files do not give a pgn file.

"""
import subprocess
import os
import re
import tkinter.filedialog

tokenre = re.compile(
    r"^Token \d+ of \d+\<(?:([^{]+) +\{Line \d+\, Column \d+\} ?(.*))\>$"
)


def process_cql_parse_output(cqloutput):
    """Print tokens from 'cql -parse' for a *.cql file."""
    tokens = []
    for line in cqloutput.split("\n"):
        print(line)
        token = tokenre.match(line)
        if token:
            tokens.append(token.groups())
    print(len(tokens))
    for token in tokens:
        print(token)


if __name__ == "__main__":
    pgn = tkinter.filedialog.askopenfilename(
        title="PGN file", initialdir=os.path.expanduser("~")
    )
    cql = tkinter.filedialog.askopenfilename(
        title="CQL file", initialdir=os.path.expanduser("~")
    )
    if pgn and cql:
        p = subprocess.run(
            [
                os.path.expanduser(os.path.join("~", ".local", "bin", "cql")),
                "-parse",
                "-i",
                pgn,
                cql,
            ],
            capture_output=True,
            encoding="utf-8",
        )
        if p.returncode:
            print("stderr", repr(p.stderr), cql)
        process_cql_parse_output(p.stdout)
