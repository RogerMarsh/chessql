# test_filter_line.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'line' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FilterLine(verify.Verify):

    def test_062_line_01(self):
        self.verify("line", [], returncode=1)

    def test_062_line_02(self):
        self.verify("line -->", [], returncode=1)

    def test_062_line_03(self):
        self.verify(
            "line --> check",
            [(3, "Line"), (4, "ArrowForward"), (5, "Check")],
        )

    def test_062_line_04(self):
        self.verify("line --> check -->", [], returncode=1)

    def test_062_line_05(self):
        self.verify(
            "line --> check --> check",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_06(self):
        self.verify("line --> check <--", [], returncode=1)

    def test_062_line_07(self):
        self.verify("line --> check <-- check", [], returncode=1)

    def test_062_line_08(self):
        self.verify("line <--", [], returncode=1)

    def test_062_line_09(self):
        self.verify(
            "line <-- check",
            [(3, "Line"), (4, "ArrowBackward"), (5, "Check")],
        )

    def test_062_line_10(self):
        self.verify("line <-- check <--", [], returncode=1)

    def test_062_line_11(self):
        self.verify(
            "line <-- check <-- check",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (4, "ArrowBackward"),
                (5, "Check"),
            ],
        )

    def test_062_line_12(self):
        self.verify("line <-- check -->", [], returncode=1)

    def test_062_line_13(self):
        self.verify("line <-- check --> check", [], returncode=1)

    def test_062_line_14(self):
        self.verify(
            "line --> .",
            [(3, "Line"), (4, "ArrowForward"), (5, "AnySquare")],
        )

    def test_062_line_15(self):
        self.verify(
            "line --> .*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "AnySquare"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_16(self):
        self.verify(
            "line --> check+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_17(self):
        self.verify(
            "line --> check?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_18_force_repeat_01_zero_or_more(self):
        self.verify(
            "line --> check{*}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "WildcardStar"),
            ],
        )

    def test_062_line_18_force_repeat_02_one_or_more(self):
        self.verify(
            "line --> check{+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (5, "WildcardPlus"),
            ],
        )

    def test_062_line_19(self):
        self.verify(
            "line --> (check --> r)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "PieceDesignator"),
            ],
        )

    def test_062_line_20(self):
        self.verify(
            "line --> (check --> r)+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "PieceDesignator"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_21(self):
        self.verify(
            "line <-- .",
            [(3, "Line"), (4, "ArrowBackward"), (5, "AnySquare")],
        )

    def test_062_line_22(self):
        self.verify(
            "line <-- .*",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "AnySquare"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_23(self):
        self.verify(
            "line <-- check+",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_24(self):
        self.verify(
            "line <-- check?",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_25_repeat_01_closed_range(self):
        self.verify(
            "line <-- check{2,4}",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RegexRepeat"),
            ],
        )

    def test_062_line_25_repeat_02_closed_range_upper(self):
        self.verify(
            "line <-- check{,4}",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RegexRepeat"),
            ],
        )

    def test_062_line_25_repeat_03_closed_range_lower(self):
        self.verify(
            "line <-- check{2,}",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "Check"),
                (5, "RegexRepeat"),
            ],
        )

    def test_062_line_26(self):
        self.verify(
            "line <-- (check <-- r)",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowBackward"),
                (7, "PieceDesignator"),
            ],
        )

    def test_062_line_27(self):
        self.verify(
            "line <-- (check <-- r)+",
            [
                (3, "Line"),
                (4, "ArrowBackward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowBackward"),
                (7, "PieceDesignator"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_28(self):
        self.verify("line --> (check <-- r)+", [], returncode=1)

    def test_062_line_29(self):
        self.verify("line <-- (check --> r)+", [], returncode=1)

    def test_062_line_30(self):
        self.verify("line primary secondary --> check", [], returncode=1)

    def test_062_line_31(self):
        self.verify(
            "line primary --> check",
            [
                (3, "Line"),
                (4, "PrimaryParameter"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_32(self):
        self.verify(
            "line secondary --> check",
            [
                (3, "Line"),
                (4, "SecondaryParameter"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_33(self):
        self.verify(
            "line firstmatch --> check",
            [
                (3, "Line"),
                (4, "FirstMatch"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_34(self):
        self.verify(
            "line lastposition --> check",
            [
                (3, "Line"),
                (4, "LastPosition"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_35(self):
        self.verify(
            "line singlecolor --> check",
            [
                (3, "Line"),
                (4, "SingleColor"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_36(self):
        self.verify(
            "line quiet --> check",
            [(3, "Line"), (4, "Quiet"), (4, "ArrowForward"), (5, "Check")],
        )

    def test_062_line_37(self):
        self.verify(
            "line nestban --> check",
            [(3, "Line"), (4, "NestBan"), (4, "ArrowForward"), (5, "Check")],
        )

    def test_062_line_38(self):
        self.verify(
            "line singlecolor nestban quiet lastposition --> check",
            [
                (3, "Line"),
                (4, "SingleColor"),
                (4, "NestBan"),
                (4, "Quiet"),
                (4, "LastPosition"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_39(self):
        self.verify(
            "line 1 3 --> check",
            [
                (3, "Line"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_40(self):
        self.verify(
            "line quiet 1 3 firstmatch --> check",
            [
                (3, "Line"),
                (4, "Quiet"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "FirstMatch"),
                (4, "ArrowForward"),
                (5, "Check"),
            ],
        )

    def test_062_line_41(self):
        self.verify(
            "line quiet 1 3 firstmatch <-- check",
            [
                (3, "Line"),
                (4, "Quiet"),
                (4, "RangeInteger"),
                (4, "RangeInteger"),
                (4, "FirstMatch"),
                (4, "ArrowBackward"),
                (5, "Check"),
            ],
        )

    def test_062_line_42(self):
        self.verify("line secondary primary --> check", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_01_zero_or_more(self):
        self.verify("check*", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_02_one_or_more(self):
        self.verify("check+", [], returncode=1)

    def test_062__line_43_regex_no_line_arrow_03_zero_or_one(self):
        self.verify("check?", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_04_zero_or_more(self):
        self.verify("check{*}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_05_one_or_more(self):
        self.verify("check{+}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_06_closed_range(self):
        self.verify("check{2,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_07_closed_range_high(self):
        self.verify("check{,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_08_closed_range_low(self):
        self.verify("check{2,}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_09_group_zero_or_more(self):
        self.verify("(check)*", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_10_group_one_or_more(self):
        self.verify("(check)+", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_11_group_zero_or_one(self):
        self.verify("(check)?", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_12_group_zero_or_more(self):
        self.verify("(check){*}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_13_group_one_or_more(self):
        self.verify("(check){+}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_14_group_closed_range(self):
        self.verify("(check){2,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_15_group_closed_range_high(self):
        self.verify("(check){,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_16_group_closed_range_low(self):
        self.verify("(check){2,}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_17_arrow_zero_or_more(self):
        self.verify("(check --> mate)*", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_18_arrow_one_or_more(self):
        self.verify("(check --> mate)+", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_19_arrow_zero_or_one(self):
        self.verify("(check --> mate)?", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_20_arrow_zero_or_more(self):
        self.verify("(check --> mate){*}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_21_arrow_one_or_more(self):
        self.verify("(check --> mate){+}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_22_arrow_closed_range(self):
        self.verify("(check --> mate){2,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_23_arrow_closed_range_high(self):
        self.verify("(check --> mate){,4}", [], returncode=1)

    def test_062_line_43_regex_no_line_arrow_24_arrow_closed_range_low(self):
        self.verify("(check --> mate){2,}", [], returncode=1)

    def test_062_line_44_regex_line_arrow_01_arrow_zero_or_more(self):
        self.verify(
            "line --> (check --> mate)*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_44_regex_line_arrow_02_arrow_one_or_more(self):
        self.verify(
            "line --> (check --> mate)+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_44_regex_line_arrow_03_arrow_zero_or_one(self):
        self.verify(
            "line --> (check --> mate)?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_44_regex_line_arrow_04_arrow_zero_or_more(self):
        self.verify(
            "line --> (check --> mate){*}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "WildcardStar"),
            ],
        )

    def test_062_line_44_regex_line_arrow_05_arrow_one_or_more(self):
        self.verify(
            "line --> (check --> mate){+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "WildcardPlus"),
            ],
        )

    def test_062_line_44_regex_line_arrow_06_arrow_closed_range(self):
        self.verify_capture_cql_output(
            "line --> (check --> mate){2,4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "RegexRepeat"),
            ],
            "<RepeatConstituent \n    <VectorConstituent ",
        )

    def test_062_line_44_regex_line_arrow_07_arrow_closed_range_high(self):
        self.verify_capture_cql_output(
            "line --> (check --> mate){,4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "RegexRepeat"),
            ],
            "<RepeatConstituent \n    <VectorConstituent ",
        )

    def test_062_line_44_regex_line_arrow_08_arrow_closed_range_low(self):
        self.verify_capture_cql_output(
            "line --> (check --> mate){2,}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Check"),
                (6, "ArrowForward"),
                (7, "Mate"),
                (5, "RegexRepeat"),
            ],
            "<RepeatConstituent \n    <VectorConstituent ",
        )

    def test_062_line_45_regex_line_arrow_08_space_start_repeat_number(self):
        self.verify_capture_cql_output(
            "line --> check{ 2}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
            "<NumberNode:",
        )

    def test_062_line_45_regex_line_arrow_09_space_end_repeat_number(self):
        self.verify_capture_cql_output(
            "line --> check{2 }",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
            "<NumberNode:",
        )

    def test_062_line_45_regex_line_arrow_10_space_around_repeat_number(self):
        self.verify_capture_cql_output(
            "line --> check{ 2 }",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Check"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
            "<NumberNode:",
        )

    def test_062_line_45_regex_line_arrow_11_space_start_repeat_range(self):
        self.verify("line --> check{ 2,}", [], returncode=1)

    def test_062_line_45_regex_line_arrow_12_space_end_repeat_range(self):
        self.verify("line --> check{2, }", [], returncode=1)

    def test_062_line_45_regex_line_arrow_13_space_around_repeat_range(self):
        self.verify("line --> check{ 2, }", [], returncode=1)

    def test_062_line_45_regex_line_arrow_14_space_within_range_01(self):
        self.verify("line --> check{2 ,}", [], returncode=1)

    def test_062_line_45_regex_line_arrow_14_space_within_range_02(self):
        self.verify("line --> check{, 4}", [], returncode=1)

    def test_062_line_45_regex_line_arrow_14_space_within_range_03(self):
        self.verify("line --> check{2 , 4}", [], returncode=1)

    def test_062_line_46_integer_01_bare(self):
        self.verify_declare_fail(
            "line --> 3", [(3, "Line"), (4, "ArrowForward"), (5, "Integer")]
        )

    def test_062_line_46_integer_02_hide_in_parentheses(self):
        self.verify_declare_fail(
            "line --> (3)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
            ],
        )

    def test_062_line_46_integer_03_hide_in_braces(self):
        self.verify_declare_fail(
            "line --> {3}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Integer"),
            ],
        )

    def test_062_line_46_integer_04_bare_plus(self):  # '+' is add.
        self.verify_declare_fail(
            "line --> 3+4",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Plus"),
                (6, "Integer"),
                (6, "Integer"),
            ],
        )

    # '(3)+' is constituent of 'line'. '(4)' is new filter after 'line'.
    def xtest_062_line_46_integer_05_hide_in_parentheses_plus_01(self):
        self.verify_declare_fail(
            "line --> (3)+(4)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "PlusRepeat"),
                (3, "ParenthesisLeft"),
                (4, "Integer"),
            ],
        )

    def test_062_line_46_integer_05_hide_in_parentheses_plus_02(self):
        self.verify_declare_fail(
            "line --> (3+4)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Plus"),
                (7, "Integer"),
                (7, "Integer"),
            ],
        )

    # The constituent of '-->' is the '+' filter adding two compound filters.
    def test_062_line_46_integer_06_hide_in_braces_plus_01(self):
        self.verify_declare_fail(
            "line --> {3}+{4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Plus"),
                (6, "BraceLeft"),
                (7, "Integer"),
                (6, "BraceLeft"),
                (7, "Integer"),
            ],
        )

    def test_062_line_46_integer_06_hide_in_braces_plus_02(self):
        self.verify_declare_fail(
            "line --> {3+4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Plus"),
                (7, "Integer"),
                (7, "Integer"),
            ],
        )

    def test_062_line_46_integer_07_bare_star(self):  # '*' is multiply.
        self.verify_declare_fail(
            "line --> 3*4",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Star"),
                (6, "Integer"),
                (6, "Integer"),
            ],
        )

    # '(3)*' is constituent of 'line'. '(4)' is new filter after 'line'.
    def test_062_line_46_integer_08_hide_in_parentheses_star_01(self):
        self.verify_declare_fail(
            "line --> (3)*(4)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "StarRepeat"),
                (3, "ParenthesisLeft"),
                (4, "Integer"),
            ],
        )

    def test_062_line_46_integer_08_hide_in_parentheses_star_02(self):
        self.verify_declare_fail(
            "line --> (3*4)",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Star"),
                (7, "Integer"),
                (7, "Integer"),
            ],
        )

    # The constituent of '-->' is the '*' filter multiplying two compound
    # filters.
    def test_062_line_46_integer_09_hide_in_braces_star_01(self):
        self.verify_declare_fail(
            "line --> {3}*{4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Star"),
                (6, "BraceLeft"),
                (7, "Integer"),
                (6, "BraceLeft"),
                (7, "Integer"),
            ],
        )

    def test_062_line_46_integer_09_hide_in_braces_star_02(self):
        self.verify_declare_fail(
            "line --> {3*4}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Star"),
                (7, "Integer"),
                (7, "Integer"),
            ],
        )

    def test_062_line_46_integer_10_bare_plus_repeat(self):
        self.verify_declare_fail(
            "line --> 3+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Integer"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_46_integer_11_hide_in_parentheses_plus_repeat(self):
        self.verify_declare_fail(
            "line --> (3)+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_46_integer_12_hide_in_braces_plus_repeat(self):
        self.verify_declare_fail(
            "line --> {3}+",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Integer"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_46_integer_13_bare_star_repeat(self):
        self.verify_declare_fail(
            "line --> 3*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Integer"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_46_integer_14_hide_in_parentheses_star_repeat(self):
        self.verify_declare_fail(
            "line --> (3)*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_46_integer_15_hide_in_braces_star_repeat(self):
        self.verify_declare_fail(
            "line --> {3}*",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Integer"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_46_integer_16_bare_optional(self):
        self.verify_declare_fail(
            "line --> 3?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Integer"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_46_integer_17_hide_in_parentheses_optional(self):
        self.verify_declare_fail(
            "line --> (3)?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Integer"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_46_integer_18_hide_in_braces_optional(self):
        self.verify_declare_fail(
            "line --> {3}?",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Integer"),
                (5, "RepeatZeroOrOne"),
            ],
        )

    def test_062_line_46_string_01_bare(self):
        self.verify(
            'line --> "a"', [(3, "Line"), (4, "ArrowForward"), (5, "String")]
        )

    def test_062_line_46_string_02_hide_in_parentheses(self):
        self.verify(
            'line --> ("a")',
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "String"),
            ],
        )

    def test_062_line_47_string_03_hide_in_braces(self):
        self.verify(
            'line --> {"a"}',
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "String"),
            ],
        )

    def test_062_line_48_integer_variable_01_bare(self):
        self.verify_declare_fail(
            "v=3 line --> v",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Variable"),
            ],
        )

    def test_062_line_48_integer_variable_02_hide_in_parentheses(self):
        self.verify_declare_fail(
            "v=3 line --> (v)",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Variable"),
            ],
        )

    def test_062_line_48_integer_variable_03_hide_in_braces(self):
        self.verify(
            "v=3 line --> {v}",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Variable"),
            ],
        )

    def test_062_line_49_string_variable_01_bare(self):
        self.verify(
            'v="a" line --> v',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Variable"),
            ],
        )

    def test_062_line_49_string_variable_02_hide_in_parentheses(self):
        self.verify(
            'v="a" line --> (v)',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "LineConstituentParenthesisLeft"),
                (6, "Variable"),
            ],
        )

    def test_062_line_49_string_variable_03_hide_in_braces(self):
        self.verify(
            'v="a" line --> {v}',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "BraceLeft"),
                (6, "Variable"),
            ],
        )

    def test_062_line_50_cql_6_1_examples_long_sacrifice_plus_01(self):
        self.verify(
            "{line-->7>=9+}",
            [
                (3, "BraceLeft"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "PlusRepeat"),
            ],
        )

    def test_062_line_50_cql_6_1_examples_long_sacrifice_plus_02(self):
        self.verify(
            "(line-->7>=9+)",
            [
                (3, "ParenthesisLeft"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "PlusRepeat"),
            ],
        )

    def test_062_line_50_cql_6_1_examples_long_sacrifice_plus_03(self):
        # The 'wildcard plus' test at *_062_*_50_*_04 is fine.
        self.verify_declare_fail(
            'v="s"v[line-->7>=9+]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "BracketLeft"),
                (4, "Variable"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "PlusRepeat"),
            ],
        )

    def test_062_line_50_cql_6_1_examples_long_sacrifice_plus_04(self):
        self.verify(
            'v="s"v[line-->7>=9{+}]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "BracketLeft"),
                (4, "Variable"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "WildcardPlus"),
            ],
        )

    def test_062_line_51_cql_6_1_examples_long_sacrifice_plus_01_star(self):
        self.verify(
            "{line-->7>=9*}",
            [
                (3, "BraceLeft"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "StarRepeat"),
            ],
        )

    def test_062_line_51_cql_6_1_examples_long_sacrifice_plus_02_star(self):
        self.verify(
            "(line-->7>=9*)",
            [
                (3, "ParenthesisLeft"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "StarRepeat"),
            ],
        )

    def test_062_line_51_cql_6_1_examples_long_sacrifice_plus_03_star(self):
        # The 'wildcard star' test at *_062_*_51_*_04_star is fine.
        self.verify_declare_fail(
            'v="s"v[line-->7>=9*]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "BracketLeft"),
                (4, "Variable"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "StarRepeat"),
            ],
        )

    def test_062_line_51_cql_6_1_examples_long_sacrifice_plus_04_star(self):
        self.verify(
            'v="s"v[line-->7>=9{*}]',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "BracketLeft"),
                (4, "Variable"),
                (4, "Line"),
                (5, "ArrowForward"),
                (6, "GE"),
                (7, "Integer"),
                (7, "Integer"),
                (6, "WildcardStar"),
            ],
        )

    def test_062_line_52_cql_6_1_examples_turton_01(self):
        self.verify(
            "line -->  move from k *",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (6, "FromParameter"),
                (7, "PieceDesignator"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_52_cql_6_1_examples_turton_02(self):
        self.verify(
            "line -->  move from k {*}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (6, "FromParameter"),
                (7, "PieceDesignator"),
                (5, "WildcardStar"),
            ],
        )

    def test_062_line_52_cql_6_1_examples_turton_03(self):
        self.verify(
            "line -->  move *",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (5, "StarRepeat"),
            ],
        )

    def test_062_line_52_cql_6_1_examples_turton_04(self):
        self.verify(
            "line -->  move {*}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (5, "WildcardStar"),
            ],
        )

    def test_062_line_53_cql_6_1_examples_turton_01_plus(self):
        self.verify(
            "line -->  move from k +",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (6, "FromParameter"),
                (7, "PieceDesignator"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_53_cql_6_1_examples_turton_02_plus(self):
        self.verify(
            "line -->  move from k {+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (6, "FromParameter"),
                (7, "PieceDesignator"),
                (5, "WildcardPlus"),
            ],
        )

    def test_062_line_53_cql_6_1_examples_turton_03_plus(self):
        self.verify(
            "line -->  move +",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (5, "PlusRepeat"),
            ],
        )

    def test_062_line_53_cql_6_1_examples_turton_04_plus(self):
        self.verify(
            "line -->  move {+}",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "Move"),
                (5, "WildcardPlus"),
            ],
        )

    def test_062_line_54_cql_6_1_examples_parallelpaths_simple(self):
        # Further simplification usually causes query to pass parsing
        # before fix applied.
        self.verify(
            "line-->x=?move to .-->y=?move to ~x from k-->z=?move to .",
            [
                (3, "Line"),
                (4, "ArrowForward"),
                (5, "AssignIf"),
                (6, "Variable"),
                (6, "Move"),
                (7, "ToParameter"),
                (8, "AnySquare"),
                (4, "ArrowForward"),
                (5, "AssignIf"),
                (6, "Variable"),
                (6, "Move"),
                (7, "ToParameter"),
                (8, "Complement"),
                (9, "Variable"),
                (7, "FromParameter"),
                (8, "PieceDesignator"),
                (4, "ArrowForward"),
                (5, "AssignIf"),
                (6, "Variable"),
                (6, "Move"),
                (7, "ToParameter"),
                (8, "AnySquare"),
            ],
        )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterLine))
