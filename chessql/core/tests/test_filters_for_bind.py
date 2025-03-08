# test_filters_for_bind.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for isunbound and unbind filters.

Currently 'isbound x' 'isunbound x' and 'unbind x', when 'x' is a function,
cannot be handled.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FiltersBind(verify.Verify):

    def test_055_isbound_01(self):  # chessql gets this wrong.
        self.verify("isbound", [], returncode=1)

    def test_055_isbound_02(self):  # chessql gets this wrong.
        self.verify("isbound x", [])

    def test_055_isbound_03(self):  # chessql gets this wrong.
        self.verify("x=0 isbound x", [(3, "Isunbound")])

    def test_057_isunbound_01(self):  # chessql gets this wrong.
        self.verify("isunbound", [], returncode=1)

    def test_057_isunbound_02(self):  # chessql gets this wrong.
        self.verify("isunbound x", [])

    def test_057_isunbound_03(self):  # chessql gets this wrong.
        self.verify("x=0 isunbound x", [(3, "Isunbound")])

    def test_137_unbind_01(self):
        self.verify("unbind", [], returncode=1)

    def test_137_unbind_02_variable(self):  # chessql wrong.
        self.verify("unbind x", [], returncode=1)

    def test_137_unbind_03_variable(self):
        self.verify(
            "x=1 unbind x",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Unbind"),
                (4, "Variable"),
            ],
        )

    def test_137_unbind_04_dictionary(self):
        self.verify(
            "dictionary v unbind v",
            [
                (3, "Dictionary"),
                (3, "Unbind"),
                (4, "Dictionary"),
            ],
        )

    def test_137_unbind_04_dictionary_key_01(self):
        self.verify('dictionary v unbind v["key"]', [], returncode=1)

    def test_137_unbind_04_dictionary_key_02(self):
        self.verify(
            'dictionary v["key"]="value" unbind v["key"]',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
                (3, "Unbind"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
            ],
        )

    def test_137_unbind_04_dictionary_key_03(self):
        self.verify(
            'dictionary v["key"]="value" unbind v',
            [
                (3, "Assign"),
                (4, "BracketLeft"),
                (5, "Dictionary"),
                (5, "String"),
                (4, "String"),
                (3, "Unbind"),
                (4, "Dictionary"),
            ],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FiltersBind))
