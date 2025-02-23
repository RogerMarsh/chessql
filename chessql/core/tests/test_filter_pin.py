# test_filter_pin.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'pin' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterPin(verify.Verify):

    def test_097_pin_01(self):
        self.verify("pin", [(3, "Pin")])

    def test_097_pin_02_from(self):
        self.verify("pin from", [], returncode=1)

    def test_097_pin_03_from_set(self):
        self.verify(
            "pin from Q",
            [(3, "Pin"), (4, "FromParameter"), (5, "PieceDesignator")],
        )

    def test_097_pin_04_from_set_to(self):
        self.verify("pin from Q to", [], returncode=1)

    def test_097_pin_05_from_set_to_set(self):
        self.verify(
            "pin from Q to k",
            [
                (3, "Pin"),
                (4, "FromParameter"),
                (5, "PieceDesignator"),
                (4, "ToParameter"),
                (5, "PieceDesignator"),
            ],
        )

    def test_097_pin_06_through(self):
        self.verify("pin through", [], returncode=1)

    def test_097_pin_07_through_set(self):
        self.verify(
            "pin through n",
            [(3, "Pin"), (4, "Through"), (5, "PieceDesignator")],
        )

    def test_097_pin_08_through_set_from(self):
        self.verify("pin through n from", [], returncode=1)

    def test_097_pin_09_through_set_from_set(self):
        self.verify(
            "pin through n from Q",
            [
                (3, "Pin"),
                (4, "Through"),
                (5, "PieceDesignator"),
                (4, "FromParameter"),
                (5, "PieceDesignator"),
            ],
        )

    def test_097_pin_10_to(self):
        self.verify("pin to", [], returncode=1)

    def test_097_pin_11_to_set(self):
        self.verify(
            "pin to k",
            [(3, "Pin"), (4, "ToParameter"), (5, "PieceDesignator")],
        )

    def test_097_pin_12_to_set_through(self):
        self.verify("pin to k through", [], returncode=1)

    def test_097_pin_13_to_set_through_set(self):
        self.verify(
            "pin to k through n",
            [
                (3, "Pin"),
                (4, "ToParameter"),
                (5, "PieceDesignator"),
                (4, "Through"),
                (5, "PieceDesignator"),
            ],
        )

    def test_097_pin_14_to_set_from_set_through(self):
        self.verify("pin to k from Q through", [], returncode=1)

    def test_097_pin_15_to_set_from_set_through_set(self):
        self.verify(
            "pin to k from Q through n",
            [
                (3, "Pin"),
                (4, "ToParameter"),
                (5, "PieceDesignator"),
                (4, "FromParameter"),
                (5, "PieceDesignator"),
                (4, "Through"),
                (5, "PieceDesignator"),
            ],
        )

    def test_097_pin_16_to_to(self):  # chessql gets this wrong.
        self.verify("pin to to", [(3, "Pin"), (4, "ToParameter"), (5, "To")])

    def test_097_pin_17_to_from(self):  # chessql gets this wrong.
        self.verify(
            "pin to from", [(3, "Pin"), (4, "ToParameter"), (5, "From")]
        )

    def test_097_pin_18_to_through(self):
        self.verify("pin to through", [], returncode=1)

    def test_097_pin_19_from_to(self):  # chessql gets this wrong.
        self.verify(
            "pin from to", [(3, "Pin"), (4, "FromParameter"), (5, "To")]
        )

    def test_097_pin_20_from_from(self):  # chessql gets this wrong.
        self.verify(
            "pin from from", [(3, "Pin"), (4, "FromParameter"), (5, "From")]
        )

    def test_097_pin_21_from_through(self):
        self.verify("pin from through", [], returncode=1)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterPin))
