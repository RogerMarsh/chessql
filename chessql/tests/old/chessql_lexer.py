# chessql_lexer.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate running chessql to produce output equivalent to '-parse'.

Test all '*.cql' files in a directory.
"""

import os
import re
import tkinter.filedialog

from ...core import pattern

cql_re = re.compile(pattern.CQL_TOKENS)


if __name__ == "__main__":
    cql = tkinter.filedialog.askdirectory(
        title="CQL directory", initialdir=os.path.expanduser("~")
    )
    if cql:
        print()
        print("directory", cql)
        filters = set()
        total_anything_else = 0
        for file in os.listdir(cql):
            if os.path.splitext(file)[-1] != ".cql":
                continue
            print()
            print(file)
            with open(
                os.path.join(cql, file), mode="r", encoding="utf-8"
            ) as cqlfile:
                brace_left = 0
                brace_left_count = 0
                parenthesis_left = 0
                parenthesis_left_count = 0
                anything_else = 0
                end_of_stream = 0
                whitespace = 0
                string = 0
                block_comment = 0
                line_comment = 0
                tokens = []
                text = cqlfile.read()
                for match in cql_re.finditer(text):
                    tokens.append(match.group())
                    group = match.groupdict()
                    if group["anything_else"] is not None:
                        anything_else += 1
                        print("anything else", group["anything_else"])
                        continue
                    if group["whitespace"] is not None:
                        whitespace += 1
                        continue
                    if group["string"] is not None:
                        string += 1
                        continue
                    if group["brace_left"] is not None:
                        brace_left += 1
                        brace_left_count += 1
                        continue
                    if group["brace_right"] is not None:
                        brace_left -= 1
                        continue
                    if group["parenthesis_left"] is not None:
                        parenthesis_left += 1
                        parenthesis_left_count += 1
                        continue
                    if group["parenthesis_right"] is not None:
                        parenthesis_left -= 1
                        continue
                    if group["end_of_stream"] is not None:
                        end_of_stream += 1
                        break
                    if group["block_comment"] is not None:
                        block_comment += 1
                        continue
                    if group["line_comment"] is not None:
                        line_comment += 1
                        continue
                total_anything_else += anything_else
                print(text)
                for item, count in (
                    ("Brace left", brace_left_count),
                    ("Parenthesis left", parenthesis_left_count),
                    ("Anything else", anything_else),
                    ("End of stream", end_of_stream),
                    ("White space", whitespace),
                    ("String", string),
                    ("Block comment", block_comment),
                    ("Line comment", line_comment),
                ):
                    if count:
                        print("   ", count, item)
                if brace_left:
                    print("   ", "Brace unclosed", brace_left)
                if parenthesis_left:
                    print("   ", "Parenthesis unclosed", parenthesis_left)
                for item in tokens:
                    if item.strip():
                        print(item)
        print()
        print("total_anything_else", total_anything_else)
