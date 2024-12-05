# options.py
# Copyright 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Chess Query Language (CQL) command line options.

The argparse module is not used because the gamenumber and year options
take one or two operands.

The argparse module is not used because the option name prefix is '--'
or '-', '--gamenumber' or '-gamenumbr' for example, and a few long
option names have short equivalents, '-i' or '--input' or '-input' for
example.
"""

import sys


class OptionError(Exception):
    """Exception raised for problems in Option and subclasses."""


class Option:
    """Base class of classes which represent CQL command line options."""

    operand_count_min = 0
    operand_count_max = 0
    operand_names = ()
    option_names = ()
    operand_error_message = "is invalid"

    def __init__(self):
        """Initialise option."""
        self.operands = []

    def append_operand(self, value):
        """Append value to operands."""
        self.operands.append(value)

    def valid_operand(self, value):
        """Return True.

        Subclasses should override if False is ever reasonable.

        """
        del value
        return True

    # This method avoids a pylint R0912 (too-mamy-branches) report.
    def operand_count_within_limits(self):
        """Return 'too many/few operands' message or None."""
        if len(self.operands) < self.operand_count_min:
            return "few"
        if len(self.operands) > self.operand_count_max:
            return "many"
        return None


class OneOperand(Option):
    """Base class of classes which represent options with one operand."""

    operand_count_min = 1
    operand_count_max = 1


class CqlFileName(OneOperand):
    """Name of file containing CQL query."""

    # The '.cql' extention is assumed if omitted.
    operand_names = ("QUERYFILENAME",)


class A(OneOperand):
    """Convert unicode characters to ASCII.

    The '--a' option must be the first option.

    It is also the only option, when given, because everything after the
    operand is ignored.
    """

    option_names = ("--a", "-a")
    # The '.cql' extention must be present.
    operand_names = ("QUERYFILE",)


class AlwaysComment(Option):
    """Disable smart comments."""

    option_names = ("--alwayscomment", "-alwayscomment")


class Assign(Option):
    """Assign value Y to variable X."""

    option_names = ("--assign", "-assign")
    operand_count_min = 2
    operand_count_max = 2
    operand_names = ("X", "Y")


class Black(OneOperand):
    """Black player must match BLACK."""

    option_names = ("--black", "-black")
    operand_names = ("BLACK",)


class Cql(OneOperand):
    """Positions must match FILTER or 'FILTER FILTER ...'.

    It is assumed FILTER or 'FILTER FILTER ...' is wrapped in '{}' by
    CQL-6.2 because '-cql "cql() Qa5"' gets a syntax error following a
    '{' at line 1 column 2 for 'cql'.
    """

    option_names = ("--cql", "-cql")
    operand_names = ("FILTER | 'FILTER FILTER ...'",)


class Event(OneOperand):
    """Event must match EVENT."""

    option_names = ("--event", "-event")
    operand_names = ("EVENT",)


class Fen(OneOperand):
    """Positions must match FEN board."""

    option_names = ("--fen", "-fen")
    operand_names = ("FENBOARD",)


class Flip(Option):
    """Flip the body of CQL file."""

    option_names = ("--flip", "-flip")


class FlipColor(Option):
    """Allow color interchange in body of CQL file."""

    option_names = ("--flipcolor", "-flipcolor")


class GameNumber(Option):
    """Only consider games in range FROM [.. TO]."""

    option_names = ("--gamenumber", "-gamenumber", "-g")
    operand_count_min = 1
    operand_count_max = 2
    operand_names = ("FROM", "TO")
    operand_error_message = "must be a number"

    def valid_operand(self, value):
        """Return True if value is an integer string."""
        return value.isdigit()


class Gui(Option):
    """Output information for GUI interfaces.

    See gadycosteff.com/cql/gui.html for intended use of '--gui' option.
    """

    option_names = ("--gui", "-gui")


class GuiPgnStdin(Option):
    """Read input PGN from standard input.

    See gadycosteff.com/cql/gui.html for intended use of '--guipgnstdin'
    option.

    This option is not listed in command line options, only gui.html.
    """

    option_names = ("--guipgnstdin", "-guipgnstdin")


class GuiPgnStdout(Option):
    """Write output PGN to standard output.

    See gadycosteff.com/cql/gui.html for intended use of '--guipgnstdout'
    option.

    This option is not listed in command line options, only gui.html.
    """

    option_names = ("--guipgnstdout", "-guipgnstdout")


class Help(Option):
    """Print a help meassage."""

    option_names = ("--help", "-help", "-h")


class Html(Option):
    """Create *-cql.html file from *.cql file.

    The '--html' option does not have an operand.  It applies to the
    *.cql file supplied as final option.
    """

    option_names = ("--html", "-html")


class Input(OneOperand):
    """Read games from the PGN file specified as INPUT."""

    option_names = ("--input", "-input", "-i")
    operand_names = ("INPUT",)


class LineIncrement(OneOperand):
    """Print message every INTERVAL games."""

    option_names = ("--lineincrement", "-lineincrement")
    operand_names = ("INTERVAL",)
    operand_error_message = "must be a number"

    def valid_operand(self, value):
        """Return True if value is an integer string."""
        return value.isdigit()


class Mainline(Option):
    """Search only in the main line."""

    option_names = ("--mainline", "-mainline")


class MatchCount(Option):
    """Output games with matched position count in range FROM [.. TO]."""

    option_names = ("--matchcount", "-matchcount")
    operand_count_min = 1
    operand_count_max = 2
    operand_names = ("FROM", "TO")
    operand_error_message = "must be a number"

    def valid_operand(self, value):
        """Return True if value is an integer string."""
        return value.isdigit()


class MatchString(OneOperand):
    """Change comment inserted for matched position to COMMENT.

    The default is 'CQL'.
    """

    option_names = ("--matchstring", "-matchstring")
    operand_names = ("COMMENT",)
    operand_error_message = "must be a str"

    def valid_operand(self, value):
        """Return True if value is a string."""
        return isinstance(value, str)


class NoHeader(Option):
    """Omit the CQL-generated header before every game."""

    option_names = ("--noheader", "-noheader")


class NoRemoveComment(Option):
    """Ignore remove comment filters."""

    option_names = ("--noremovecomment", "-noremovecomment")


class NoSetTag(Option):
    """Ignore set tag filters."""

    option_names = ("--nosettag", "-nosettag")


class Output(OneOperand):
    """Write games to the PGN file specified as OUTPUT."""

    option_names = ("--output", "-output", "-o")
    operand_names = ("OUTPUT",)


class Player(OneOperand):
    """Player must match PLAYER."""

    option_names = ("--player", "-player")
    operand_names = ("PLAYER",)


class ReverseColor(Option):
    """Reverse the colors in the body of the CQL file."""

    option_names = ("--reversecolor", "-reversecolor")


class Result(OneOperand):
    """Game result must match RESULT."""

    option_names = ("--result", "-result")
    operand_names = ("RESULT",)
    operand_error_message = "must be '1-0', '0-1', or '1/2-1/2'"

    def valid_operand(self, value):
        """Return True if value is 1-0 0-1 or 1/2-1/2.."""
        return value in frozenset(("1-0", "0-1", "1/2-1/2"))


class Shift(Option):
    """Shift the body of the CQL file."""

    option_names = ("--shift", "-shift")


class SimilarPosition(Option):
    """Check each position in target PGN for match with current position.

    .In 'cql --similarposition target.cql' each position in target.pgn is
    checked against the current position in the input PGN file.
    """

    option_names = ("--similarposition", "-similarposition")


class SingleThreaded(Option):
    """Run only one thread."""

    option_names = ("--singlethreaded", "-singlethreaded", "-s")


class ShowMatches(Option):
    """Print the game number of each match as it occurs."""

    option_names = ("--showmatches", "-showmatches")


class Silent(Option):
    """Suppress printing of automatically generated comments."""

    option_names = ("--silent", "-silent")


class Site(OneOperand):
    """Site must match SITE."""

    option_names = ("--site", "-site")
    operand_names = ("SITE",)


class Threads(OneOperand):
    """Run THREADS threads."""

    option_names = ("--threads", "-threads")
    operand_names = ("THREADS",)
    operand_error_message = "must be a number"

    def valid_operand(self, value):
        """Return True if value is an integer string."""
        return value.isdigit()


class U(OneOperand):
    """Convert ASCII to unicode characters where possible.

    The '--u' option must be the first option.

    It is also the only option, when given, because everything after the
    operand is ignored.
    """

    option_names = ("--u", "-u")
    # The '.cql' extention must be present.
    operand_names = ("QUERYFILE",)


class Variations(Option):
    """Search in main line and variations."""

    option_names = ("--variations", "-variations")


class Version(Option):
    """Print version number of this CQL executable."""

    option_names = ("--version", "-version")


class VirtualMainline(Option):
    """Search in virtual main line only."""

    option_names = ("--virtualmainline", "-virtualmainline")


class White(OneOperand):
    """White player must match WHITE."""

    option_names = ("--white", "-white")
    operand_names = ("WHITE",)


class Vi(Option):
    """Read from hhdbvi.pgn."""

    option_names = ("--vi", "-vi")


class Year(Option):
    """Only consider games whose year is in range FROM [.. TO]."""

    option_names = ("--year", "-year")
    operand_count_min = 1
    operand_count_max = 2
    operand_names = ("FROM", "TO")
    operand_error_message = "must be a number"

    def valid_operand(self, value):
        """Return True if value is an integer string."""
        return value.isdigit()


option_map = {
    "--a": A,
    "-a": A,
    "--alwayscomment": AlwaysComment,
    "-alwayscomment": AlwaysComment,
    "--assign": Assign,
    "-assign": Assign,
    "--black": Black,
    "-black": Black,
    "--cql": Cql,
    "-cql": Cql,
    "--event": Event,
    "-event": Event,
    "--fen": Fen,
    "-fen": Fen,
    "--flip": Flip,
    "-flip": Flip,
    "--flipcolor": FlipColor,
    "-flipcolor": FlipColor,
    "--gamenumber": GameNumber,
    "-gamenumber": GameNumber,
    "-g": GameNumber,
    "--gui": Gui,
    "-gui": Gui,
    "--guipgnstdin": GuiPgnStdin,
    "-guipgnstdin": GuiPgnStdin,
    "--guipgnstdout": GuiPgnStdout,
    "-guipgnstdout": GuiPgnStdout,
    "--help": Help,
    "-help": Help,
    "-h": Help,
    "--html": Html,
    "-html": Html,
    "--input": Input,
    "-input": Input,
    "-i": Input,
    "--lineincrement": LineIncrement,
    "-lineincrement": LineIncrement,
    "--mainline": Mainline,
    "-mainline": Mainline,
    "--matchcount": MatchCount,
    "-matchcount": MatchCount,
    "--matchstring": MatchString,
    "-matchstring": MatchString,
    "--noheader": NoHeader,
    "-noheader": NoHeader,
    "--noremovecomment": NoRemoveComment,
    "-noremovecomment": NoRemoveComment,
    "--nosettag": NoSetTag,
    "-nosettag": NoSetTag,
    "--output": Output,
    "-output": Output,
    "-o": Output,
    "--player": Player,
    "-player": Player,
    "--reversecolor": ReverseColor,
    "-reversecolor": ReverseColor,
    "--result": Result,
    "-result": Result,
    "--shift": Shift,
    "-shift": Shift,
    "--similarposition": SimilarPosition,
    "-similarposition": SimilarPosition,
    "--singlethreaded": SingleThreaded,
    "-singlethreaded": SingleThreaded,
    "-s": SingleThreaded,
    "--showmatches": ShowMatches,
    "-showmatches": ShowMatches,
    "--silent": Silent,
    "-silent": Silent,
    "--site": Site,
    "-site": Site,
    "--threads": Threads,
    "-threads": Threads,
    "--u": U,
    "-u": U,
    "--variations": Variations,
    "-variations": Variations,
    "--version": Version,
    "-version": Version,
    "--virtualmainline": VirtualMainline,
    "-virtualmainline": VirtualMainline,
    "--white": White,
    "-white": White,
    "--vi": Vi,
    "-vi": Vi,
    "--year": Year,
    "-year": Year,
}


class Options:
    """Container for CQL command line options."""

    def __init__(self):
        """Initialise options container."""
        self.argv = sys.argv[1:]
        self.options = []
        self.errors = []

    def is_duplicate_option(self, option):
        """Return True if an instance of option's class is in options.

        A message is added to errors if option is a duplicate.

        """
        for item in self.options:
            if isinstance(option, item.__class__):
                self.errors.append(
                    " ".join((item.__class__.__name__, "option", "duplicated"))
                )
                return True
        return False

    def get_options(self):
        """Populate options attribute with classes representing options."""
        if self.options or self.errors:
            return
        options = self.options
        errors = self.errors
        for count, item in enumerate(self.argv):
            if item in option_map and not options:
                option = option_map[item]()
                self.is_duplicate_option(option)
                options.append(option)
                continue
            if item not in option_map:
                if (
                    not options
                    or len(option.operands) >= option.operand_count_max
                ):
                    if count < len(self.argv) - 1:
                        self.report_operand_error(option, item)
                        option.append_operand(item)
                        continue
                    option = CqlFileName()
                    self.is_duplicate_option(option)
                    options.append(option)
                    self.report_operand_error(option, item)
                    options[-1].append_operand(item)
                    continue
                if len(option.operands) >= option.operand_count_min:
                    if option.valid_operand(item):
                        option.append_operand(item)
                        continue
                    if count < len(self.argv) - 1:
                        self.report_operand_error(option, item)
                        option.append_operand(item)
                        continue
                    option = CqlFileName()
                    self.is_duplicate_option(option)
                    options.append(option)
                    self.report_operand_error(option, item)
                    options[-1].append_operand(item)
                    continue
                self.report_operand_error(option, item)
                option.append_operand(item)
                continue
            option = option_map[item]()
            self.is_duplicate_option(option)
            options.append(option)
        for item in self.options:
            # Avoid a pylint R0912 (too-many-branches) report.
            text = item.operand_count_within_limits()
            if text is not None:
                errors.append(
                    " ".join(
                        (
                            item.__class__.__name__,
                            "option",
                            "has too",
                            text,
                            "operands",
                        )
                    )
                )
            if isinstance(item, (A, U)) and len(self.options) != 1:
                errors.append(
                    " ".join(
                        (
                            item.__class__.__name__,
                            "option",
                            "should be the first and only option.",
                        )
                    )
                )

    def report_operand_error(self, option, item):
        """Report operand error for item in option."""
        if not option.valid_operand(item):
            if len(option.option_names) == 0:
                self.errors.append(
                    " ".join(
                        (
                            "Option",
                            option.__class__.__name__,
                            "operand value",
                            item.join(("'", "'")),
                            option.operand_error_message,
                        )
                    )
                )
                return
            self.errors.append(
                " ".join(
                    (
                        "Option",
                        option.__class__.__name__,
                        "operand",
                        option.operand_names[len(option.operands)],
                        "value",
                        item.join(("'", "'")),
                        option.operand_error_message,
                    )
                )
            )
        return
