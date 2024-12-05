# cqli_tokens.py
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
definition_re = re.compile(
    r"(Find\(all\)|\w+)([+*?])?\s*(.*?)\s*({[^}]*}) <[^>]*>"
)


def process_cqli_parse_output(cqloutput, filters):
    """Print tokens from 'cqli -parse' for *.cql files in a directory."""
    source = False
    tree = False
    for line in cqloutput.split("\n"):
        if not source:
            if line.startswith("cql("):
                source = True
        if not tree:
            if line.startswith("QueryContainer "):
                tree = True
            else:
                continue
        token = token_re.match(line)
        if not token:
            print("***** Next line does not match")
            print(repr(line))
            continue
        definition = definition_re.search(token.group())
        if line and not definition:
            print("***** Next line does not contain a token definition")
            print(repr(line))
            continue
        if definition:
            print(definition.group(1), repr(definition.group(3)))
            filters.setdefault(definition.group(1), set()).add(
                definition.group(4)
            )
            if definition.group(2):
                filters[definition.group(1)].add(definition.group(2))


if __name__ == "__main__":
    cql = tkinter.filedialog.askdirectory(
        title="CQL query directory", initialdir=os.path.expanduser("~")
    )
    if cql:
        print("directory", cql)
        filters = {}
        for file in os.listdir(cql):
            if os.path.splitext(file)[-1] != ".cql":
                continue
            p = subprocess.run(
                [
                    "wine64",
                    os.path.expanduser(
                        os.path.join("~", ".local", "bin", "cqli.exe")
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
                process_cqli_parse_output(p.stdout, filters)
        for item in sorted(filters.items()):
            print(item)
