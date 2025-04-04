# verify.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify 'cql -parse' returncode against chessql.core.parser output.

Subclasses will call the verify(...) method for the many CQL filters.

Most filters are simple enough to put in one big unittest class.

Examples of filters which get their own module are '--' (utf8 '――' or
'\u2015\u2015') sometimes called 'dash', '[x]' (utf8 'x' or '\u00d7') the
captures version of 'dash', 'line', 'move', and 'path' (utf8 '⊢' or
'\u22a2').

Generally the test statements are the simplest which are accepted by CQL
for each filter.  Sometimes these will not make sense as queries to
evaluate.
"""

import unittest
import shlex
import subprocess
import os

from .. import parser
from .. import querycontainer
from .. import cqltypes
from ..basenode import NodeError

# An input file must be specified, but need not exist, with '-parse' option.
_CQL_PREFIX = "cql -input null.pgn -parse -cql "
_CQL_RUN_PREFIX = "cql -input chessql/core/tests/tiny.pgn -cql "

# Assume any cql output is to the default output file.
_CQL_DEFAULT_OUTPUT = "cqldefault-out.pgn"

_CHESSQL_PREFIX = "cql() "
_TRACE_PREFIX = [(1, "QueryContainer"), (2, "CQL")]


def is_cql_on_path():
    """Return True if the cql executable can be run."""
    try:
        process = subprocess.run(
            ["cql"],
            stdout=subprocess.DEVNULL,
        )
        return True
    except FileNotFoundError:
        print(
            "".join(
                (
                    "'FileNotFoundError' exception trying to run 'cql':",
                    " is it on PATH?",
                )
            )
        )
        return False


class Verify(unittest.TestCase):
    """Implement verify_*() methods for many unittests."""

    def verify_chessql(self, string, classname_structure):
        """Verify string produces tokens and names for tokens.

        Run the string through the chessql parser to verify the expected
        tree structure is produced.

        This method can be used on it's own, but it exists to provide
        chessql parsing tests for the other verify_* methods.

        """
        container = parser.parse(_CHESSQL_PREFIX + string)
        trace = []
        container.parse_tree_node(trace=trace)
        self.assertEqual(
            [(e, n.__class__.__name__) for e, n in trace],
            _TRACE_PREFIX + classname_structure,
        )
        return container

    def verify(self, string, classname_structure, returncode=0):
        """Verify string produces tokens and names for tokens.

        Run 'cql' in a subprocess to verify the string is accepted by cql.

        Call self.verify_chessql().

        """
        process = subprocess.run(
            shlex.split(_CQL_PREFIX) + [string],
            stdout=subprocess.DEVNULL,
        )
        self.assertEqual(process.returncode, returncode)
        if returncode != 0:
            self.assertRaisesRegex(
                NodeError,
                ".*$",
                parser.parse,
                *(_CHESSQL_PREFIX + string,),
            )
            return None
        return self.verify_chessql(string, classname_structure)

    def verify_run(self, string, classname_structure, returncode=0):
        """Verify string produces tokens and names for tokens.

        Run 'cql' in a subprocess to verify the string is accepted by cql
        and the evaluation succeeds, but set returncode to 1 if evaluation
        is declared a failure.

        Call self.verify_chessql().

        """
        process = subprocess.run(
            shlex.split(_CQL_RUN_PREFIX) + [string],
            stdout=subprocess.DEVNULL,
        )
        self.assertEqual(process.returncode, returncode)
        try:
            os.remove(_CQL_DEFAULT_OUTPUT)
        except FileNotFoundError:
            pass
        return self.verify_chessql(string, classname_structure)

    def verify_run_fail(self, string):
        """Verify string produces run failure after parse and no tokens.

        Run 'cql' in a subprocess to verify the string is accepted by cql
        parser.

        Run 'cql' in a subprocess to verify the string gets a run error
        on evaluation by cql.

        Verify a NodeError is raised by the chessql parser.

        """
        process = subprocess.run(
            shlex.split(_CQL_PREFIX) + [string],
            stdout=subprocess.DEVNULL,
        )
        self.assertEqual(process.returncode, 0)
        run = subprocess.run(
            shlex.split(_CQL_RUN_PREFIX) + [string],
            stdout=subprocess.DEVNULL,
        )
        self.assertEqual(run.returncode, 1)
        self.assertRaisesRegex(
            NodeError,
            ".*$",
            parser.parse,
            *(_CHESSQL_PREFIX + string,),
        )

    def verify_declare_fail(self, string, classname_structure):
        """Verify string produces parse failure although technically legal.

        Run 'cql' in a subprocess to verify the string is rejected by cql
        parser.

        Call self.verify_chessql().

        'sort min' without a 'documentation' filter, for example.

        """
        process = subprocess.run(
            shlex.split(_CQL_PREFIX) + [string],
            stdout=subprocess.DEVNULL,
        )
        self.assertEqual(process.returncode, 1)
        return self.verify_chessql(string, classname_structure)

    def verify_tolerant(self, string, classname_structure):
        """Verify string produces parse success although technically illegal.

        Run 'cql' in a subprocess to verify the string is accepted by cql
        parser.

        Call self.verify_chessql().  The classname_structure argument is
        set depending on chessql attitude to query.

        '--or --' for example.

        """
        process = subprocess.run(
            shlex.split(_CQL_PREFIX) + [string],
            stdout=subprocess.DEVNULL,
        )
        self.assertEqual(process.returncode, 0)
        if classname_structure:
            return self.verify_chessql(string, classname_structure)
        self.assertRaisesRegex(
            NodeError,
            ".*$",
            parser.parse,
            *(_CHESSQL_PREFIX + string,),
        )

    def verify_assign(
        self, string, classname_structure, name, variable_type, filter_type
    ):
        """Verify string produces variable with specified types.

        Call Verify.verify to parse the string.

        Check the name exists in query definitions and has the specified
        variable and filter types.

        """
        container = self.verify(string, classname_structure)
        self.assertEqual(name in container.definitions, True)
        variable = container.definitions[name]
        self.assertEqual(isinstance(variable, cqltypes.Variable), True)
        self.assertEqual(variable.name, name)
        self.assertEqual(variable.variable_type, variable_type)
        self.assertEqual(variable.filter_type, filter_type)

    def verify_capture_cql_output(
        self, string, classname_structure, cql_output, returncode=0
    ):
        """Verify string produces tokens and names for tokens.

        This method is very sensistive to changes in the output produced
        by the unsupported '-parse' option when running CQL.

        The CQL subprocess is run with 'stdout=subprocess.PIPE' so tests
        can be done on the result of the 'cql ... -parse ...' run against
        the cql_output argument.  The test is that cql_output is in the
        stdout of subprocess.

        Run 'cql' in a subprocess to verify the string is accepted by cql.

        Call self.verify_chessql().

        """
        process = subprocess.run(
            shlex.split(_CQL_PREFIX) + [string],
            stdout=subprocess.PIPE,
            encoding="utf8",
        )
        self.assertEqual(process.returncode, returncode)
        if returncode != 0:
            self.assertRaisesRegex(
                NodeError,
                ".*$",
                parser.parse,
                *(_CHESSQL_PREFIX + string,),
            )
            return None
        self.assertEqual(cql_output in process.stdout, True)
        return self.verify_chessql(string, classname_structure)


if __name__ == "__main__":

    class CQLAssumptions(unittest.TestCase):
        """Confirm operation of cql command with '-cql' option.

        Tests test_03_anynode(), test_04_count_anynode(), and test_05_kall(),
        indicate the 'AnyNode' inserted from 'cqldefault.cql' can be taken
        to have no effect on the validity of the statement in the '-cql'
        argument.
        """

        LEX_PREFIX = "".join(
            (
                "\nParser: lexing file: cqldefault.cql",
                "\ngenCqlNodes::Got return of ntokens: 4",
                "\nPrinting the token stream for file: ",
                "cqldefault.cql",
                "\nTokens: Bottom: 0 size: 4",
                "\nToken 0 of 4<KeywordToken: ",
                '{Line 1, Column 2} "cql">',
                "\nToken 1 of 4<SpecialToken: ",
                '{Line 1, Column 4} "(">',
                "\nToken 2 of 4<SpecialToken: ",
                '{Line 1, Column 5} ")">',
                "\nToken 3 of 4<SpecialToken: ",
                '{Line 1, Column 6} ".">',
            )
        )

        def run_cql(self, string):
            """Return the subprocess run to parse cql statement in string."""
            return subprocess.run(
                shlex.split(_CQL_PREFIX) + [string],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

        def good_request_stdout(self, process):
            """Verify lexer output for 'cql' jobs which succeed."""
            self.assertEqual(
                "".join(
                    (
                        self.LEX_PREFIX,
                        "\n\n<CqlNode  inputfile: null.pgn ",
                        "outputfile: cqldefault-out.pgn ",
                        "searchVariations: 0",
                        "\n CqlNode body: ",
                        "\n <CompoundNode at ",
                    )
                )
                in process.stdout,
                True,
            )

        def test_01_null_string(self):
            """Verify output for '-cql ""' option."""
            process = self.run_cql("")
            self.assertEqual(process.returncode, 1)
            self.assertEqual(
                process.stdout.endswith(
                    "\n\nempty filter following '--cql'\n"
                ),
                True,
            )

        def test_02_bare_count(self):
            """Verify output for '-cql "#"' option."""
            process = self.run_cql("#")
            self.assertEqual(process.returncode, 1)
            self.assertEqual(
                process.stdout.endswith(
                    "".join(
                        (
                            self.LEX_PREFIX,
                            "\n\n\n\nCQL syntax error: ",
                            "Expected either a string filter or a set ",
                            "filter following '#' but the filter parsed ",
                            "was of neither type",
                            "\nUnable to parse the following token: ",
                            "<SpecialToken: ",
                            '{Line 2, Column 1} "}">',
                            "\n\n",
                        )
                    )
                ),
                True,
            )

        def test_03_anynode(self):
            """Verify output for '-cql "."' option."""
            process = self.run_cql(".")
            self.assertEqual(process.returncode, 0)
            self.good_request_stdout(process)
            # Ignore the '0x..' assumed to be an address within process.
            self.assertEqual(
                process.stdout.endswith(
                    "".join(
                        (
                            ": 2 specs:",
                            "\n  <0 of 2: <AnyNode>",
                            "\n  <1 of 2: <AnyNode> CompoundNode>  CqlNode>",
                            "\n",
                        )
                    )
                ),
                True,
            )

        def test_04_count_anynode(self):
            """Verify output for '-cql "#."' option."""
            process = self.run_cql("#.")
            self.assertEqual(process.returncode, 0)
            self.good_request_stdout(process)
            # Ignore the '0x..' assumed to be an address within process.
            self.assertEqual(
                process.stdout.endswith(
                    "".join(
                        (
                            ": 2 specs:",
                            "\n  <0 of 2: <CountSquaresNode <AnyNode>>",
                            "\n  <1 of 2: <AnyNode> CompoundNode>  CqlNode>",
                            "\n",
                        )
                    )
                ),
                True,
            )

        def test_05_kall(self):
            """Verify output for '-cql "k"' option."""
            process = self.run_cql("k")
            self.assertEqual(process.returncode, 0)
            self.good_request_stdout(process)
            # Ignore the '0x..' assumed to be an address within process.
            self.assertEqual(
                process.stdout.endswith(
                    "".join(
                        (
                            ": 2 specs:",
                            "\n  <0 of 2: k<all>",
                            "\n  <1 of 2: <AnyNode> CompoundNode>  CqlNode>",
                            "\n",
                        )
                    )
                ),
                True,
            )

    class VerifyTest(Verify):
        """Unittests for Verify class."""

        def test_verify_chessql(self):
            """Unittest for chessql parse."""
            value = self.verify_chessql("b", [(3, "PieceDesignator")])
            self.assertEqual(
                isinstance(value, querycontainer.QueryContainer), True
            )

        def test_verify_returncode_0(self):
            """Unittest for returncode 0 from cql job."""
            value = self.verify("b", [(3, "PieceDesignator")])
            self.assertEqual(
                isinstance(value, querycontainer.QueryContainer), True
            )

        def test_verify_returncode_1(self):
            """Unittest for returncode 1 from cql job."""
            value = self.verify("down", [], returncode=1)
            self.assertEqual(value is None, True)

        def test_verify_declare_fail(self):
            """Unittest for returncode 1 from cql job when parse succeeds."""
            value = self.verify_declare_fail(
                "sort 3", [(3, "Sort"), (4, "Integer")]
            )
            self.assertEqual(
                isinstance(value, querycontainer.QueryContainer), True
            )

        def test_verify_tolerant(self):
            """Unittest for returncode 0 from cql job when query tolerated."""
            value = self.verify_tolerant("--or --", [])
            self.assertEqual(
                isinstance(value, querycontainer.QueryContainer), False
            )

        def test_verify_run_fail(self):
            """Unittest for returncode 1 from cql job when run fails."""
            self.verify_run_fail("1[<]A")

        def test_verify_assign(self):
            """Unittest for returncode 1 from cql job when assign variable."""
            self.verify_assign(
                "v=b",
                [(3, "Assign"), (4, "Variable"), (4, "PieceDesignator")],
                "v",
                cqltypes.VariableType.SET,
                cqltypes.FilterType.SET,
            )

        def test_verify_capture_cql_output(self):
            """Unittest for returncode 0 from cql job."""
            self.verify_capture_cql_output(
                "line --> ka5{2 }",
                [
                    (3, "Line"),
                    (4, "ArrowForward"),
                    (5, "PieceDesignator"),
                    (3, "BraceLeft"),
                    (4, "Integer"),
                ],
                "<NumberNode:",
            )

    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(CQLAssumptions))
    runner().run(loader(VerifyTest))
