# test___init__.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Tests for chessql.core.__init__."""

import unittest
import re

from .. import empty_copy


class InitEmptyCopy(unittest.TestCase):
    def setUp(self):
        class C:
            def __init__(self):
                self.a = "A"

        self.c = C

    def tearDown(self):
        pass

    def test_empty_copy(self):
        ae = self.assertEqual
        instance = empty_copy(self.c())
        ae(instance.__class__, self.c().__class__)
        ae(hasattr(instance, "a"), False)
        ae(hasattr(self.c(), "a"), True)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(InitEmptyCopy))
