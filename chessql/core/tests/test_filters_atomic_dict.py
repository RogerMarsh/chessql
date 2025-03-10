# test_filters.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'atomic' and 'dictionary' filters.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FiltersAtomicDict(verify.Verify):

    def test_027_dictionary(self):  # chessql gets this wrong.
        self.verify(
            'dictionary X["a"]="bc"',
            [
                (3, "Assign"),
            ],
        )

    def test_063_local_01(self):
        self.verify("local", [], returncode=1)

    def test_063_local_02(self):
        self.verify("local dictionary", [], returncode=1)

    def test_063_local_03(self):
        self.verify("local dictionary K", [], returncode=1)

    def test_063_local_04(self):
        self.verify("local dictionary D", [(3, "Dictionary")])


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FiltersAtomicDict))
