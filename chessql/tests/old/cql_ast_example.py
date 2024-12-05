# cql_ast_example.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running cql in a subprocess to return '-parse' output.

'cql -parse -i sample.pgn <cql file>.cql' outputs a str containing
approximations to repr(token) for each token and repr(<abstract syntax tree>)
for the content of '<cql file>.cql'.

The '-i sample.pgn' argument overrides whatever the <cql file>.cql file
says in the cql(input <pgn file>.pgn) clause, but that does not matter
when parsing only and some cql files do not give a pgn file.

These SpecialToken names are changed to avoid confusion with '<' and '>' in
the -parse output meaning start and end of element definition:

   <=   to [le]
   <    to [lt]
   >=   to [ge]
   [<]  to [pidlt]
   <-   to [prev]
   -->  to [forward]
   >    to [gt]
   ->   to [next]

   Others like "[<]" are seen in the specification (precedes page) but do
   not occur in examples.  These are not to be confused with the plain
   SpecialTokens like "<".

"""
import subprocess
import os
import re
import tkinter.filedialog

astre = re.compile(r"(\s*Token[^\n]*|<\w+|\w*>)")
specialtokenre = re.compile(r"<all>|<=|<|>=|[<]|<-|-->|>|->")


def replace_specialtoken(match):
    """Return match with some symbols replaced by convenient subsitutes."""
    replacements = {
        "<=": "[le]",
        # "<": "[lt]",
        ">=": "[ge]",
        "[<]": "[pidlt]",
        "<-": "[prev]",
        "-->": "[forward]",
        # ">": "[gt]",
        "->": "[next]",
        "<all>": "[all]",  # "[allsquares]" better?
    }
    return replacements.get(match.group(), match.group())


def process_cql_parse_output(cqloutput):
    """Print token names from 'cql -parse' for a *.cql file."""
    tokens = []
    collect = False
    for element in astre.split(
        specialtokenre.sub(replace_specialtoken, cqloutput)
    ):
        token = element.strip()
        if not collect:
            if token != "<CqlNode":
                continue
            collect = True
        print(repr(token.strip()))


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
        print("stderr", p.stdout)
        print("\n\n*******\n")
        process_cql_parse_output(p.stdout)
