# test_filters_implicit_search.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for implicit search parameter filters.

The verification methods are provided by the Verify superclass.

Generally the test statements are the simplest which are accepted by CQL
for each filter.  Sometimes these will not make sense as queries to
evaluate.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FiltersImplicitSearch(verify.Verify):

    def test_024_date(self):
        self.verify("date", [(3, "Date")])

    def test_033_event(self):
        self.verify("event", [(3, "Event")])

    def test_034_eventdate_01(self):
        self.verify("eventdate", [(3, "EventDate")])

    def test_098_player_01(self):
        self.verify("player", [(3, "Player")])

    def test_098_player_02(self):
        self.verify(
            'player "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_099_player_white_01(self):  # chessql gets this wrong.
        self.verify("player white", [(3, "Player")])

    def test_099_player_white_02(self):  # chessql gets this wrong.
        self.verify(
            'player white "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_100_player_black_01(self):  # chessql gets this wrong.
        self.verify("player black", [(3, "Player")])

    def test_100_player_black_02(self):  # chessql gets this wrong.
        self.verify(
            'player black "Kasparov"',
            [(3, "Player"), (4, "ImplicitSearchParameter")],
        )

    def test_124_site_01(self):
        self.verify("site", [(3, "Site")])

    def test_124_site_02_value(self):
        self.verify(
            'site "place"',
            [(3, "Site"), (4, "ImplicitSearchParameter")],
        )

    # Make sure all other implicit search parameter filters have this test.
    def test_124_site_03_value_match(self):
        self.verify(
            'site ~~ "place"',
            [(3, "RegexMatch"), (4, "Site"), (4, "String")],
        )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FiltersImplicitSearch))
