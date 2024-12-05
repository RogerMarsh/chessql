# tokenmap.py
# Copyright 2020, 2024 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Unit tests for core.tokenmap module."""

import unittest
import re

from .. import pattern
from .. import tokenmap


class ClassFromTokenName(unittest.TestCase):
    def test_01_class_from_token_name_keys(self):
        ae = self.assertEqual
        found = set()
        for match_ in re.finditer(r"(?:\?P<)(\w+)(?:>)", pattern.CQL_TOKENS):
            ae(match_[1] in tokenmap.class_from_token_name, True)
            found.add(match_[1])
        msg = None
        if len(tokenmap.class_from_token_name) > len(found):
            msg = str(
                set(tokenmap.class_from_token_name.keys()).difference(found)
            )
        elif len(tokenmap.class_from_token_name) < len(found):
            msg = str(
                set(found.difference(tokenmap.class_from_token_name.keys()))
            )
        ae(len(tokenmap.class_from_token_name), len(found), msg=msg)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(ClassFromTokenName))
