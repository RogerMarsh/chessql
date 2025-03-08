# test_filter_find.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'find' filters.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterFind(verify.Verify):

    def test_038_find_01(self):
        self.verify("find", [], returncode=1)

    def test_038_find_02(self):
        self.verify("find check", [(3, "Find"), (4, "Check")])

    def test_038_find_03(self):
        self.verify("find all check", [(3, "Find"), (4, "All"), (4, "Check")])

    def test_038_find_04(self):
        self.verify(
            "find quiet check",
            [(3, "Find"), (4, "Quiet"), (4, "Check")],
        )

    def test_038_find_05(self):
        self.verify(
            "find 3 check", [(3, "Find"), (4, "RangeInteger"), (4, "Check")]
        )

    def test_038_find_06(self):
        self.verify(
            "find 3 10 check",
            [
                (3, "Find"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "Check"),
            ],
        )

    def test_038_find_07(self):
        self.verify(
            "find <-- check", [(3, "Find"), (4, "FindBackward"), (4, "Check")]
        )

    def test_038_find_08(self):
        self.verify(
            "find quiet all check",
            [(3, "Find"), (4, "Quiet"), (4, "All"), (4, "Check")],
        )

    def test_038_find_09(self):
        self.verify(
            "find all quiet check",
            [(3, "Find"), (4, "All"), (4, "Quiet"), (4, "Check")],
        )

    def test_038_find_10(self):
        self.verify("find all 1 check", [], returncode=1)

    def test_038_find_11(self):
        self.verify("find 1 all check", [], returncode=1)

    def test_038_find_12(self):
        self.verify(
            "find quiet 2 4 check",
            [
                (3, "Find"),
                (4, "Quiet"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "Check"),
            ],
        )

    def test_038_find_13(self):
        self.verify(
            "find 2 4 quiet check",
            [
                (3, "Find"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "Quiet"),
                (4, "Check"),
            ],
        )

    def test_038_find_14(self):
        self.verify(
            "find <-- all check",
            [(3, "Find"), (4, "FindBackward"), (4, "All"), (4, "Check")],
        )

    def test_038_find_15(self):  # chessql gets this wrong.
        self.verify(
            "find all <-- check",
            [(3, "Find"), (4, "All"), (4, "FindBackward"), (4, "Check")],
        )

    def test_038_find_16(self):
        self.verify(
            "find <-- 4 check",
            [
                (3, "Find"),
                (4, "FindBackward"),
                (4, "RangeInteger"),
                (4, "Check"),
            ],
        )

    def test_038_find_17(self):  # chessql gets this wrong.
        self.verify(
            "find 4 <-- check",
            [
                (3, "Find"),
                (4, "RangeInteger"),
                (4, "FindBackward"),
                (4, "Check"),
            ],
        )

    def test_038_find_18(self):
        self.verify(
            "find <-- quiet check",
            [
                (3, "Find"),
                (4, "FindBackward"),
                (4, "Quiet"),
                (4, "Check"),
            ],
        )

    def test_038_find_19(self):  # chessql gets this wrong.
        self.verify(
            "find quiet <-- check",
            [
                (3, "Find"),
                (4, "Quiet"),
                (4, "FindBackward"),
                (4, "Check"),
            ],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterFind))
