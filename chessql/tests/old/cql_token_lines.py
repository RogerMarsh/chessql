# cql_token_lines.py
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


def process_cql_parse_output(cqloutput, tokens):
    """Print lines from 'cql -parse' for *.cql files in a directory."""
    for line in cqloutput.split("\n"):
        token = tokenre.match(line)
        if token:
            key, value = token.groups()
            tokens.setdefault(key, set()).add(value)


if __name__ == "__main__":
    cql = tkinter.filedialog.askdirectory(
        title="CQL query directory", initialdir=os.path.expanduser("~")
    )
    if cql:
        print("directory", cql)
        tokens = {}
        for file in os.listdir(cql):
            if os.path.splitext(file)[-1] != ".cql":
                continue
            p = subprocess.run(
                [
                    os.path.expanduser(
                        os.path.join("~", ".local", "bin", "cql")
                    ),
                    "-parse",
                    os.path.join(cql, file),
                ],
                capture_output=True,
                encoding="utf-8",
            )
            if p.returncode:
                print("stderr", repr(p.stderr), file)
            else:
                process_cql_parse_output(p.stdout, tokens)
        for item in sorted(tokens.items()):
            print(item)
