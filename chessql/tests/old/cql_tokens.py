# cql_tokens.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Investigate token class generation from 'cql -parse' output.

'cql -parse -i sample.pgn <cql file>.cql' outputs a str containing
approximations to repr(token) for each token and repr(<abstract syntax tree>)
for the content of '<cql file>.cql'.

The '-i sample.pgn' argument overrides whatever the <cql file>.cql file
says in the cql(input <pgn file>.pgn) clause, but that does not matter
when parsing only and some cql files do not give a pgn file.

Most token names have the suffix 'Token'.  Some token names contain space
characters, 'DashToken L R x con' for example.  'KeywordToken' and
'SpecialToken' both have lots of distinct values and here the assumption is
each value should be a separate class.

Token is the base class and the 'Token' suffix is removed from the name to
generate the class name.

Thus the token 'DashToken L R x con' becomes class DashLRXCon to conform to
Python's class naming conventions.  Since there are nine 'DashToken ...'
tokens it is assumed a Dash class will prove useful so the hierarchy for
DashLRXCon is 'DashLRXCon : Dash : Token : Object'.

"""
import subprocess
import os
import re
import tkinter.filedialog

tokenre = re.compile(
    r"^Token \d+ of \d+\<(?:([^{]+) +\{Line \d+\, Column \d+\} ?(.*))\>$"
)
square_designator_re = re.compile(r"([a-h])(?:-([a-h]))?([1-8])(?:-([1-8]))?")
FILES = "abcdefgh"
RANKS = "12345678"


class _PieceTypeDesignator:
    """Define a piece type designator."""

    def __init__(self, value):
        """Set value of piece type designator."""
        self._piece_types_string = value
        self.piece_types = tuple(sorted(set(value)))

    def __str__(self):
        """Return str representation of piece type designator."""
        return self._piece_types_string


class _SquareDesignator:
    """Define a comound square designator.

    The string from the 'cql -parse' output is kept.
    The file and rank ranges for each element of the designator are kept.
    The individual squares are kept.

    The ranges are kept because horizontal shifts applied to whole ranks,
    and vertical shifts on whole files leave the designator unchanged.

    [a-h1-8] is unchanged by shift, shifthorizontal, or shiftvertical, but
    [a1, a2, ..., h8] which enumerates all the squares is changed by shift,
    shifthorizontal, and shiftvertical, with a large enough transformation
    emptying the designator.

    """

    def __init__(self, value):
        """Set value of square designator."""
        self._square_designator_string = value
        self.compound_square_designator = ()
        self.squares = ()

    def __str__(self):
        """Return str representation of square designator."""
        return str(self.compound_square_designator)

    def expand_square_designator(self):
        """Expand square designator into complete set of components."""
        compound_square_designator = []
        squares = set()
        for square_designator in square_designator_re.findall(
            self._square_designator_string
        ):
            compound_square_designator.append("".join(square_designator))
            left, right, low, high = square_designator
            assert left in FILES
            assert low in RANKS
            if right:
                assert right in FILES
                assert right > left
            else:
                right = left
            if high:
                assert high in RANKS
                assert high > low
            else:
                high = low
            for file in range(FILES.index(left), FILES.index(right) + 1):
                for rank in range(RANKS.index(low), RANKS.index(high) + 1):
                    squares.add(FILES[file] + RANKS[rank])
        self.compound_square_designator = tuple(compound_square_designator)
        self.squares = tuple(sorted(squares))

    @staticmethod
    def _hyphenated_square_designator(left, right, low, high):
        """Return hyphenated version of designator components."""
        if not right and not high:
            return left + low
        if not right:
            return "".join((left, low, "-", high))
        if not hign:
            return "".join((left, "-", right, low))
        return "".join((left, "-", right, low, "-", high))

    @staticmethod
    def _split_square_designator(designator):
        """Return file and rank components of designator."""
        if len(designator) == 2:
            return (designator[0], "", designator[1], "")
        if len(designator) == 3:
            if designator[1].isdigit():
                return (designator[0], "", designator[1], designator[2])
            return (designator[0], designator[1], designator[2], "")
        return tuple(designator)

    def shift_horizontal(self, shift):
        """Return _SquareDesignator for self shifted horizontally by shift."""
        compound_square_designator = []
        for designator in self.compound_square_designator:
            left, right, low, high = self._split_square_designator(designator)
            if left == FILES[0] and right == FILES[-1]:
                compound_square_designator.append(designator)
                continue
            leftindex = FILES.index(left) + shift
            if leftindex < 0 or leftindex > len(FILES):
                continue
            left = FILES[leftindex]
            if right:
                rightindex = FILES.index(right) + shift
                if rightindex < 0 or rightindex > len(FILES):
                    continue
                right = FILES[rightindex]
            compound_square_designator.append(left + right + low + high)
        shifted_designator = self.__class__(
            self._hyphenated_square_designator(left, right, low, high)
        )
        shifted_designator.expand_square_designator()
        return shifted_designator

    def shift_vertical(self, shift):
        """Return _SquareDesignator for self shifted vertically by shift."""
        compound_square_designator = []
        for designator in self.compound_square_designator:
            left, right, low, high = self._split_square_designator(designator)
            if low == RANKS[0] and high == RANKS[-1]:
                compound_square_designator.append(designator)
                continue
            lowindex = RANKS.index(low) + shift
            if lowindex < 0 or lowindex > len(RANKS):
                continue
            low = RANKS[lowindex]
            if high:
                highindex = RANKS.index(high) + shift
                if highindex < 0 or highindex > len(RANKS):
                    continue
                high = RANKS[highindex]
            compound_square_designator.append(left + right + low + high)
        shifted_designator = self.__class__(
            self._hyphenated_square_designator(left, right, low, high)
        )
        shifted_designator.expand_square_designator()
        return shifted_designator


class Token:
    """Base class for tokens used in 'cql -parse' output."""

    def __init__(self, name, value):
        """Set name and value of Token."""
        self.name = name
        self.value = value

    def __str__(self):
        """Return string representation of Token."""
        return " ".join(
            (
                self.__class__.__name__,
                self.name.join(("'", "'")),
                self.value.join(("'", "'")),
            )
        )


class Dash(Token):
    """Represent dash token from 'cql -parse."""


class DashL(Token):
    """Represent dah left token from 'cql -parse."""


class DashLR(Token):
    """Represent dash left right token from 'cql -parse."""


class DashLRCon(Token):
    """Represent dash left right ? token from 'cql -parse."""


class DashLRXCon(Token):
    """Represent dash left right capture ? token from 'cql -parse."""


class DashLCon(Token):
    """Represent dash left ? token from 'cql -parse."""


class DashR(Token):
    """Represent dash right token from 'cql -parse."""


class DashRCon(Token):
    """Represent dah right ? token from 'cql -parse."""


class DashCon(Token):
    """Represent dash ? token from 'cql -parse."""


class EndLineComment(Token):
    """Represent comment to end of line token from 'cql -parse."""


class EndPath(Token):
    """Represent end path token from 'cql -parse."""


class GroupNumber(Token):
    """Represent group number token from 'cql -parse."""


class Id(Token):
    """Represent identity token from 'cql -parse."""


class InputFile(Token):
    """Represent input file name token from 'cql -parse."""


class Int(Token):
    """Represent integer token from 'cql -parse."""


class Keyword(Token):
    """Represent keyword token from 'cql -parse."""


class LineComment(Token):
    """Represent line comment token from 'cql -parse."""


class PieceDeclaration(Token):
    """Represent piece declaration token from 'cql -parse."""


class PieceDesignator(Token):
    """Represent piece designator token from 'cql -parse."""

    def __init__(self, name, value):
        """Set name and value of piece designator."""
        value = value.split()
        super().__init__(
            name, (_PieceTypeDesignator(value[1]), _SquareDesignator(value[3]))
        )
        self.value[1].expand_square_designator()

    def __str__(self):
        """Return str representation of piece designatoe."""
        return " ".join(
            (
                self.__class__.__name__,
                self.name.join(("'", "'")),
                " ".join('"' + str(v) + '"' for v in self.value).join(
                    ("'", "'")
                ),
                self.value[1]._square_designator_string.join(("'", "'")),
            )
        )


class QuotedString(Token):
    """Represent quoted string token from 'cql -parse."""


class Special(Token):
    """Represent special token from 'cql -parse."""


class String(Token):
    """Represent string token from 'cql -parse."""


class WildcardPlus(Token):
    """Represent wildcard '+' token from 'cql -parse."""


class WildcardStar(Token):
    """Represent wildcard '*' token from 'cql -parse."""


_known_tokens = {
    "DashToken": Dash,
    "DashToken L": DashL,
    "DashToken L R": DashLR,
    "DashToken L R con": DashLRCon,
    "DashToken L R x con": DashLRXCon,
    "DashToken L con": DashLCon,
    "DashToken R": DashR,
    "DashToken R con": DashRCon,
    "DashToken con": DashCon,
    "EndLineCommentToken": EndLineComment,
    "EndPathToken": EndPath,
    "GroupNumberToken:": GroupNumber,
    "IdToken:": Id,
    "InputFileToken:": InputFile,
    "IntToken:": Int,
    "KeywordToken:": Keyword,
    "LineCommentToken": LineComment,
    "PieceDeclarationToken": PieceDeclaration,
    "PieceDesignatorToken": PieceDesignator,
    "QuotedStringToken:": QuotedString,
    "SpecialToken:": Special,
    "StringToken:": String,
    "WildcardPlus": WildcardPlus,
    "WildcardStar": WildcardStar,
}


def convert_token_to_class(name, value):
    """Return class instance for token name and value."""
    return _known_tokens[name](name, value)


def process_cql_parse_output(cqloutput):
    """Print tokens from 'cql -parse' for *.cql files in a directory."""
    tokens = []
    for line in cqloutput.split("\n"):
        token = tokenre.match(line)
        if token:
            tokens.append(convert_token_to_class(*token.groups()))
    return tokens


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
                tokens[file] = process_cql_parse_output(p.stdout)
        for file, tokenclasses in sorted(tokens.items()):
            print()
            print(file)
            for tokenclass in tokenclasses:
                print("    ", tokenclass)
