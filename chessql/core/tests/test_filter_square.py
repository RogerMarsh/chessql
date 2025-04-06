# test_filters.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'square' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FilterSquare(verify.Verify):

    def test_127_square_01(self):
        self.verify("square", [], returncode=1)

    def test_127_square_02_in(self):
        self.verify("square in", [], returncode=1)

    def test_127_square_03_variable(self):
        self.verify("square x", [], returncode=1)

    def test_127_square_04_variable_in_01(self):
        self.verify("square x in", [], returncode=1)

    def test_127_square_04_variable_in_02_filter(self):
        self.verify("square x in R", [], returncode=1)

    def test_127_square_04_variable_in_03_filter_body(self):  # chessql wrong.
        self.verify(
            "square x in R btm",
            [(3, "Square"), (4, "PieceDesignator"), (4, "BTM")],
        )

    def test_127_square_05_all(self):
        self.verify("square all", [], returncode=1)

    def test_127_square_06_all_variable(self):
        self.verify("square all x", [], returncode=1)

    def test_127_square_07_all_variable_in_01(self):
        self.verify("square all x in", [], returncode=1)

    def test_127_square_07_all_variable_in_02_filter(self):
        self.verify("square all x in R", [], returncode=1)

    def test_127_square_07_all_variable_in_03_filter_body(self):  # wrong.
        self.verify(
            "square all x in R btm",
            [(3, "SquareAll"), (4, "PieceDesignator"), (4, "BTM")],
        )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterSquare))
