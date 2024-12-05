# cqli_token_lines.py
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
name_re = re.compile(r"\w+")
definition_re = re.compile(r"(.*) <[^>]*>")


def process_cqli_parse_output(cqloutput, filters):
    """Print lines from 'cqli -parse' for *.cql files in directory."""
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
        group = token_re.match(line)
        if not group:
            print("***** Next line does not match")
            print(repr(line))
            continue
        name = name_re.search(group.group())
        if line and not name:
            print("***** Next line does not contain a token name")
            print(repr(line))
            continue
        if name:
            definition = definition_re.search(line)
            if definition:
                print(definition.group(1))
            filters.add(name.group())


if __name__ == "__main__":
    cql = tkinter.filedialog.askdirectory(
        title="CQL query directory", initialdir=os.path.expanduser("~")
    )
    if cql:
        print("directory", cql)
        filters = set()
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
                print()
                print(file)
                process_cqli_parse_output(p.stdout, filters)
        for item in sorted(filters):
            print(item)
