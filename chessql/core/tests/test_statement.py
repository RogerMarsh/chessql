# statement.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""statement tests for cql"""

import unittest
import re

from .. import constants
from .. import statement
from .. import node
from .. import cql


class Constants(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test____assumptions(self):
        self.assertIs(statement.Statement.create_node, node.Node)

    def test_CQL_PATTERN(self):
        ae = self.assertEqual
        s = statement.Statement()
        for t in [
            m for m in re.finditer(r"P<(?P<key>[^>]*)>", cql.CQL_PATTERN)
        ]:
            a = t.groupdict()["key"]
            ae(hasattr(s, a), True, msg=a)
            ae(callable(getattr(s, a)), True)

    def test__collapse_rightparenthesis(self):
        ae = self.assertEqual
        s = statement.Statement
        pa = frozenset({cql.Flags.PARENTHESIZED_ARGUMENTS})
        for t in [
            getattr(cql.Token, a)
            for a in dir(cql.Token)
            if isinstance(getattr(cql.Token, a), cql.TokenDefinition)
        ]:
            if pa not in t.flags:
                continue
            n = t.name
            ae(hasattr(s, "collapse_" + n), True, msg="n is '" + n + "'")
            ae(
                callable(getattr(s, "collapse_" + n)),
                True,
                msg="n is '" + n + "'",
            )


class StatementMethods(unittest.TestCase):
    def setUp(self):
        self.statement = statement.Statement()

    def tearDown(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Constants))
    runner().run(loader(StatementMethods))
