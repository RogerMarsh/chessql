# cqli_filters.py
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
    r"(Find\(all\)|\w+)([+*?])?\s*(.*?)\s*({[^}]*}) (<[^>]*>)"
)


class FilterException(Exception):
    """Raise exception for filter problem."""


class FilterType:
    """Define CQL filter type filter_type_name."""

    def __init__(self, filter_type_name):
        """Remove leading and trailing whitespace from filter_type_name."""
        self.filter_type_name = (
            filter_type_name.strip('"').lstrip("{").rstrip("}")
        )

    def __str__(self):
        """Return the filter type name."""
        return self.filter_type_name


class BooleanFilterType(FilterType):
    """Define CQL Boolean filter type."""


class NumericFilterType(FilterType):
    """Define CQL Numeric filter type."""


class PieceFilterType(FilterType):
    """Define CQL Piece filter type."""


class PositionFilterType(FilterType):
    """Define CQL Position filter type."""


class SetFilterType(FilterType):
    """Define CQL Set filter type."""


class StringFilterType(FilterType):
    """Define CQL Set filter type."""


_known_filter_types = {
    "{Boolean}": BooleanFilterType,
    "{Numeric}": NumericFilterType,
    "{Piece}": PieceFilterType,
    "{Position}": PositionFilterType,
    "{Set}": SetFilterType,
    "{String}": StringFilterType,
}


class Filter(list):
    """Define filter and note it's parent and children filters."""

    def __init__(self, definition, parent=None):
        """Set filter details from definition."""
        super().__init__()
        (
            self.name,
            self.repeat_rule,
            self.description,  # May be split into components by subclasses.
            filter_type,
            self.source,
        ) = definition.groups()
        self.whole_match = definition.group()
        self.filter_type = _known_filter_types[filter_type](filter_type)
        self.value = self.description
        self.parent = parent
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
            parent.append(self)

    def show(self):
        """Print item, and depth in structure, details."""
        print(self.depth, self.name, self.filter_type, self)
        for item in self:
            item.show()


_known_filters = {}


def convert_definition_to_filter(definition, parent=None):
    """Return filter type associated with definition."""
    return _known_filters.get(definition.group(1), Filter)(
        definition, parent=parent
    )


def process_cqli_parse_output(cqloutput):
    """Print tokens layout from 'cqli -parse' for *.cql files in directory."""
    source = False
    tree = None
    filter_ = None
    for line in cqloutput.split("\n"):
        if not source:
            if line.startswith("cql("):
                source = True
        if tree is None and not line.startswith("QueryContainer "):
            continue
        token = token_re.match(line)
        if not token:
            print("***** Next line does not match")
            print(repr(line))
            continue
        if not line.strip():
            continue
        definition = definition_re.search(token.group())
        if not definition:
            print("***** Next line does not contain a token definition")
            print(repr(line))
            continue
        depth = definition.start(1) // 2
        if not depth and tree is not None:
            raise FilterException("Root filter already exists")
        if depth and tree is None:
            raise FilterException("Root filter does not exist")
        if not depth and tree is None:
            filter_ = convert_definition_to_filter(definition)
            tree = filter_
            continue
        if depth > filter_.depth + 1:
            raise FilterException("New filter depth too big")
        while filter_.depth >= depth:
            filter_ = filter_.parent
        filter_ = convert_definition_to_filter(definition, parent=filter_)
    return tree


if __name__ == "__main__":
    cql = tkinter.filedialog.askdirectory(
        title="CQL query directory", initialdir=os.path.expanduser("~")
    )
    if cql:
        print("directory", cql)
        filters = None
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
                filters = process_cqli_parse_output(p.stdout)
                filters.show()
