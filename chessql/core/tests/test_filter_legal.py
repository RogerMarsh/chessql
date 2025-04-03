# test_filter_legal.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'legal' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class Filters(verify.Verify):

    def test_060_legal_01(self):
        self.verify("legal", [], returncode=1)

    def test_060_legal_02(self):
        self.verify("legal k", [], returncode=1)

    def test_060_legal_03_dash_ascii(self):
        self.verify(
            "legal --",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_060_legal_04_dash_utf8(self):
        self.verify(
            "legal ――",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_060_legal_05_take_ascii(self):
        self.verify("legal [x]", [], returncode=1)

    def test_060_legal_06_take_utf8(self):
        self.verify("legal ×", [], returncode=1)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Filters))
