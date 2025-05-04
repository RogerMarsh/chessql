# test_constants.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Unittests for chessql.core.constants module."""

import unittest

from .. import constants


class Constants(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test____assumptions(self):
        ae = self.assertEqual
        ae(constants.PIECE_NAMES, r"QBRNKPAqbrnkpa_")
        ae(constants.RANK_RANGE, "1-8")
        ae(constants.FILE_RANGE, "a-h")
        ae(constants.VARIABLE_NAME_CHARS, r"[a-zA-Z0-9_$]")
        ae(constants.QUOTED_STRING, r'"[^\\"]*(?:\\.[^\\"]*)*"')
        ae(constants.UPPER_CASE_CQL_PREFIX, r"__CQL")
        ae(constants.LOWER_CASE_CQL_PREFIX, r"cql__")
        ae(constants.FUNCTION_BODY_PREFIX, r"%%_body_")
        ae(len([c for c in dir(constants) if not c.startswith("__")]), 8)
        ae(
            len(
                [
                    c
                    for c in constants.FUNCTION_BODY_PREFIX[:2]
                    if c.isalnum() or c in "_$"
                ]
            ),
            0,
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Constants))
