# cqli_token_source.py
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
    "".join(
        (
            r"(Find\(all\)|\w+)([+*?])?\s*(.*?)\s*({[^}]*}) ",
            r"(?:<[^:]*:(\d+):(\d+)(?:-(\d+))?>|<[^>]*>)",
        )
    )
)


def process_cqli_parse_output(cqloutput, filters, cqlfile):
    """Print references from 'cqli -parse' for *.cql files in directory."""
    source = False
    tree = False
    with open(cqlfile, mode="r", encoding="utf-8") as file:
        lines = file.read().split("\n")
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
            (
                filter_name,
                repetition,
                value,
                filter_type,
                cqlfile_line,
                cqlfile_char_start,
                cqlfile_char_end,
            ) = definition.groups()
            if cqlfile_line is None:
                source_ref = None
                source_str = None
            elif cqlfile_char_end is None:
                source_ref = cqlfile_line + ":" + cqlfile_char_start
                source_str = lines[int(cqlfile_line) - 1][
                    int(cqlfile_char_start) - 1
                ]
            else:
                source_ref = (
                    cqlfile_line
                    + ":"
                    + cqlfile_char_start
                    + "-"
                    + cqlfile_char_end
                )
                # pycodestyle E203 whitespace before ':'.
                # black insists on " : " format.
                source_str = lines[int(cqlfile_line) - 1][
                    int(cqlfile_char_start) - 1 : int(cqlfile_char_end)
                ]
            print(
                filter_name,
                repr(value),
                source_ref,
                repr(source_str) if source_str is not None else None,
            )
            filters.setdefault(filter_name, set()).add(filter_type)
            if repetition:
                filters[filter_name].add(repetition)


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
            cqlfile = os.path.join(cql, file)
            p = subprocess.run(
                [
                    "wine64",
                    os.path.expanduser(
                        os.path.join("~", ".local", "bin", "cqli.exe")
                    ),
                    "-parse",
                    cqlfile,
                ],
                capture_output=True,
                encoding="utf-8",
            )
            if p.returncode:
                print("stderr", repr(p.stderr), file)
            else:
                process_cqli_parse_output(p.stdout, filters, cqlfile)
        for item in sorted(filters.items()):
            print(item)
