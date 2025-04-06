# test_filter_regex.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for '~~' and '\' filters.

The verification methods are provided by the Verify superclass.

Generally the test statements are the simplest which are accepted by CQL
for each filter.  Sometimes these will not make sense as queries to
evaluate.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FilterRegex(verify.Verify):

    def test_186_pattern_match_01(self):
        self.verify("~~", [], returncode=1)

    def test_186_pattern_match_02(self):
        self.verify('"king"~~', [], returncode=1)

    def test_186_pattern_match_02(self):
        self.verify('~~"d"', [], returncode=1)

    def test_186_pattern_match_03_01(self):
        self.verify(
            '"king"~~"d"', [(3, "RegexMatch"), (4, "String"), (4, "String")]
        )

    def test_186_pattern_match_03_02(self):
        self.verify(
            '"king" ~~ "d"', [(3, "RegexMatch"), (4, "String"), (4, "String")]
        )

    def test_186_pattern_match_04_01(self):
        self.verify(
            '"king"~~"i"', [(3, "RegexMatch"), (4, "String"), (4, "String")]
        )

    def test_186_pattern_match_04_02(self):
        self.verify(
            '"king" ~~ "i"', [(3, "RegexMatch"), (4, "String"), (4, "String")]
        )

    def test_186_pattern_match_05_set(self):
        self.verify('k~~"d"', [], returncode=1)

    def test_186_pattern_match_06_set(self):
        self.verify('"king"~~k', [], returncode=1)

    def test_186_pattern_match_07_numeric(self):
        self.verify('1~~"d"', [], returncode=1)

    def test_186_pattern_match_08_numeric(self):
        self.verify('"king"~~1', [], returncode=1)

    def test_186_pattern_match_09_logigal(self):
        self.verify('false~~"d"', [], returncode=1)

    def test_186_pattern_match_10_logical(self):
        self.verify('"king"~~false', [], returncode=1)

    def test_186_pattern_match_11_position(self):
        self.verify('currentposition~~"d"', [], returncode=1)

    def test_186_pattern_match_12_position(self):
        self.verify('"king"~~currentposition', [], returncode=1)

    def xtest_187_backslash_string_01_backslash(self):  # wrong.
        self.verify(r"\\", [])

    def xtest_187_backslash_string_02_newline(self):  # wrong.
        self.verify(r"\n", [])

    def xtest_187_backslash_string_03_quote(self):  # wrong.
        self.verify(r"\n", [])

    def xtest_187_backslash_string_04_tab(self):  # wrong.
        self.verify(r"\t", [])

    def xtest_187_backslash_string_05_return(self):  # wrong.
        self.verify(r"\r", [])

    def test_187_backslash_string_06_digit(self):
        self.verify(r"\1", [(3, "RegexCapturedGroup")])

    def test_187_backslash_string_07_index(self):
        self.verify(r"\-1", [(3, "RegexCapturedGroupIndex")])

    def test_187_backslash_string_08_other(self):
        self.verify(r"\a", [], returncode=1)

    def test_187_backslash_string_09_quoted(self):
        self.verify(r'"\a"', [(3, "String")])


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterRegex))
