# cqli_example.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running cqli in a subprocess to return '-parse' output.

'wine64 cqli.exe -parse -i sample.pgn <cql file>.cql' outputs a str containing
approximations to repr(token) for each token and repr(<abstract syntax tree>)
for the content of '<cql file>.cql'.

The '-i sample.pgn' argument overrides whatever the <cql file>.cql file
says in the cql(input <pgn file>.pgn) clause, but that does not matter
when parsing only and some cql files do not give a pgn file.

The source is assumed to start at the first line starting 'cql('.

The AST is assumed to start at the first line starting 'QueryContainer '.

"""
import subprocess
import os
import re
import tkinter.filedialog

token_re = re.compile(
    r"^(?:  )*(?:[\| ] )*(?:[`|]-).*|^(?:QueryContainer .*)?$"
)


def process_cqli_parse_output(cqloutput):
    """Print tokens from 'cqli -parse' for a *.cql file."""
    source = False
    tree = False
    for line in cqloutput.split("\n"):
        if not source:
            if line.startswith("cql("):
                print("****** cql source ******")
                source = True
        if not tree:
            if line.startswith("QueryContainer "):
                print("****** cql AST ******")
                tree = True
            else:
                print(repr(line))
                continue
        group = token_re.match(line)
        if not group:
            print("***** Next line does not match")
        print(repr(line))


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
                "wine64",
                os.path.expanduser(
                    os.path.join("~", ".local", "bin", "cqli.exe")
                ),
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
        print("stdout start")
        print(p.stdout)
        print("stdout end")
        print("****************************")
        process_cqli_parse_output(p.stdout)
        print("****************************")