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

from .. import parser
from ..basenode import NodeError

# An input file must be specified, but need not exist, with '-parse' option.
_CQL_PREFIX = "cql -input xxxx.pgn -parse -cql "

_CHESSQL_PREFIX = "cql() "
_TRACE_PREFIX = [(1, "QueryContainer"), (2, "CQL")]


class Verify(unittest.TestCase):
    """Implement verify() method for many unittests."""

    def verify(self, string, classname_structure, returncode=0):
        """Verify string produces tokens and names for tokens.

        Run 'cql' in a subprocess to verify the string is accepted by cql.

        Run the string through the chessql parser to verify the expected
        tree structure is produced.

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
            return
        container = parser.parse(_CHESSQL_PREFIX + string)
        trace = []
        container.parse_tree_node(trace=trace)
        trace = [(e, n.__class__.__name__) for e, n in trace]
        # print(trace)
        self.assertEqual(trace, _TRACE_PREFIX + classname_structure)


if __name__ == "__main__":

    class VerifyTest(Verify):
        """Unittests for Verify class."""

        def test_cql_returncode_0(self):
            """Unittest for returncode 0 from cql job."""
            self.verify("b", [(3, "PieceDesignator")])

        def test_cql_returncode_1(self):
            """Unittest for returncode 1 from cql job."""
            self.verify("down", [], returncode=1)

    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(VerifyTest))
