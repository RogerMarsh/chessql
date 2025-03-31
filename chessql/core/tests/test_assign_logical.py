# test_assign_logical.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'r or v = k or n' and similar.

This set of tests added when 'v = k or q' gave unexpected outcome.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterAssignLogical(verify.Verify):

    def test_216_assign_01_then_or_01_plain(self):
        self.verify(
            "v=k or q",
            [
                (3, "Or"),
                (4, "Assign"),
                (5, "Variable"),
                (5, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_216_assign_01_then_or_02_parentheses_or(self):
        self.verify("v=(k or q)", [], returncode=1)

    def test_216_assign_01_then_or_03_braces_or(self):
        self.verify("v={k or q}", [], returncode=1)

    def test_216_assign_01_then_or_04_parentheses_assign(self):
        self.verify(
            "(v=k)or q",
            [
                (3, "Or"),
                (4, "ParenthesisLeft"),
                (5, "Assign"),
                (6, "Variable"),
                (6, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_216_assign_01_then_or_05_braces_assign(self):
        self.verify(
            "{v=k}or q",
            [
                (3, "Or"),
                (4, "BraceLeft"),
                (5, "Assign"),
                (6, "Variable"),
                (6, "PieceDesignator"),
                (4, "PieceDesignator"),
            ],
        )

    def test_216_assign_02_after_or_01_plain(self):
        self.verify(
            "k or v=q",
            [
                (3, "Or"),
                (4, "PieceDesignator"),
                (4, "Assign"),
                (5, "Variable"),
                (5, "PieceDesignator"),
            ],
        )

    def test_216_assign_02_after_or_02_parentheses_assign(self):
        self.verify(
            "q or(v=k)",
            [
                (3, "Or"),
                (4, "PieceDesignator"),
                (4, "ParenthesisLeft"),
                (5, "Assign"),
                (6, "Variable"),
                (6, "PieceDesignator"),
            ],
        )

    def test_216_assign_02_after_or_03_braces_assign(self):
        self.verify(
            "q or{v=k}",
            [
                (3, "Or"),
                (4, "PieceDesignator"),
                (4, "BraceLeft"),
                (5, "Assign"),
                (6, "Variable"),
                (6, "PieceDesignator"),
            ],
        )

    def test_217_assign_plus_01_then_or_01_plain(self):
        self.verify("v+=2 or q", [], returncode=1)

    def test_217_assign_plus_01_then_or_02_plain_persistent(self):
        self.verify(
            "persistent v+=2 or q",
            [
                (3, "Or"),
                (4, "AssignPlus"),
                (5, "Persistent"),
                (5, "Integer"),
                (4, "PieceDesignator"),
            ],
        )

    def test_217_assign_plus_01_then_or_03_plain_after_assign(self):
        self.verify(
            "v=0 v+=2 or q",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Or"),
                (4, "AssignPlus"),
                (5, "Variable"),
                (5, "Integer"),
                (4, "PieceDesignator"),
            ],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterAssignLogical))
