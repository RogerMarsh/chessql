# cql_ast_names.py
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

astre = re.compile(r"(\s*Token[^\n]*|<\w+|\w*>)")
specialtokenre = re.compile(
    r"<\d+ of \d+:|if/>|<-?\d+,-?\d+>|<all>|<=|<|>=|[<]|<-|-->|>|->"
)


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
        # "<all>": "[all]",  # "[allsquares]" better? but see "<-1,1>" too.
        "if/>": "IfNode>",
    }
    group = match.group()
    if group.startswith("<") and group.endswith(":"):
        return group[-1] + group[1:]
    if group.startswith("<") and group.endswith(">"):
        return "[" + group[1:-1] + "]"
    return replacements.get(group, group)


def process_cql_parse_output(cqloutput):
    """Print token names from 'cql -parse' for *.cql files in a directory."""
    print()
    print(cqloutput)
    print()
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
    cql = tkinter.filedialog.askdirectory(
        title="CQL query directory", initialdir=os.path.expanduser("~")
    )
    if cql:
        print("directory", cql)
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
                process_cql_parse_output(p.stdout)
