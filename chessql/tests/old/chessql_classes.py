# chessql_classes.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Run chessql to produce output from matches stored in CQL object classes.

Test all '*.cql' files in a directory.
"""

import os
import re
import tkinter.filedialog
import sys

from ...core import parser
from ...core import tokenmap
from ...core import querycontainer

cql_re = re.compile(parser.pattern.CQL_TOKENS)


if __name__ == "__main__":
    if len(sys.argv) == 2 and os.path.isdir(sys.argv[-1]):
        querydir = sys.argv[-1]
    else:
        querydir = tkinter.filedialog.askdirectory(
            title="CQL query directory", initialdir=os.path.expanduser("~")
        )
    if querydir:
        print()
        print("directory", querydir)
        filters = set()
        total_anything_else = 0
        class_from_token_name = tokenmap.class_from_token_name
        for file in os.listdir(querydir):
            if os.path.splitext(file)[-1] != ".cql":
                continue
            print()
            print(file)
            container = querycontainer.QueryContainer()
            container.place_node_in_tree()
            with open(
                os.path.join(querydir, file), mode="r", encoding="utf-8"
            ) as opencqlfile:
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
                text = opencqlfile.read()
                for match_ in cql_re.finditer(text):
                    for key, value in match_.groupdict().items():
                        if value is None:
                            continue
                        tokens.append(
                            class_from_token_name[key](
                                match_=match_, container=container
                            )
                        )
                        tokens[-1].place_node_in_tree()
                        if key == "anything_else":
                            anything_else += 1
                            print(
                                "anything else",
                                tokens[-1].match_.groupdict()["anything_else"],
                            )
                            continue
                        if key == "whitespace":
                            whitespace += 1
                            continue
                        if key == "string":
                            string += 1
                            continue
                        if key == "brace_left":
                            brace_left += 1
                            brace_left_count += 1
                            continue
                        if key == "brace_right":
                            brace_left -= 1
                            continue
                        if key == "parenthesis_left":
                            parenthesis_left += 1
                            parenthesis_left_count += 1
                            continue
                        if key == "parenthesis_right":
                            parenthesis_left -= 1
                            continue
                        if key == "end_of_stream":
                            end_of_stream += 1
                            break
                        if key == "block_comment":
                            block_comment += 1
                            continue
                        if key == "line_comment":
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
                    if item.match_[0].strip():
                        print(item.match_[0])
        print()
        print("total_anything_else", total_anything_else)
