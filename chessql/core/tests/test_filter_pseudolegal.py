# test_filter_pseudolegal.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'pseudolegal filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class Filters(verify.Verify):

    def test_106_pseudolegal_01(self):
        self.verify("pseudolegal", [], returncode=1)

    def test_106_pseudolegal_02_dash(self):
        self.verify("pseudolegal k", [], returncode=1)

    def test_106_pseudolegal_03_dash_ascii(self):
        self.verify(
            "pseudolegal --",
            [
                (3, "Pseudolegal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_106_pseudolegal_04_dash_utf8(self):
        self.verify(
            "pseudolegal ――",
            [
                (3, "Pseudolegal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_106_pseudolegal_05_take_ascii(self):
        self.verify("pseudolegal [x]", [], returncode=1)

    def test_106_pseudolegal_06_take_utf8(self):
        self.verify("pseudolegal ×", [], returncode=1)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Filters))
