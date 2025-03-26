# test_cql_strings.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Unittests for CQL strings againstchessql.core.pattern module."""

import unittest
import re

from .. import pattern

cql_re = re.compile(pattern.CQL_TOKENS)


class Patterns(unittest.TestCase):

    def verify(self, string, tokens, names):
        """Verify string produces tokens and names for tokens."""
        matches = [m for m in cql_re.finditer(string)]
        groups = []
        for match in matches:
            item = []
            for k, v in match.groupdict().items():
                if v is not None:
                    item.append(k)
            groups.append(item)
        self.assertEqual(
            [m.group() for m in matches],
            tokens,
        )
        for item, group in enumerate(groups):
            self.assertEqual(len(group), 1)
            self.assertEqual(group[0], names[item])

    def test_01_dash_ascii(self):
        self.verify("--", ["--", ""], ["dash_ii", "end_of_stream"])

    def test_02_dash_utf8(self):
        self.verify("――", ["――", ""], ["dash_ii", "end_of_stream"])

    def test_03_dash_left_ascii(self):
        self.verify(
            "R--",
            ["R", "--", ""],
            ["piece_designator", "dash_li", "end_of_stream"],
        )

    def test_04_dash_left_utf8(self):
        self.verify(
            "R――",
            ["R", "――", ""],
            ["piece_designator", "dash_li", "end_of_stream"],
        )

    def test_05_dash_right_ascii(self):
        self.verify(
            "--R",
            ["--", "R", ""],
            ["dash_ir", "piece_designator", "end_of_stream"],
        )

    def test_06_dash_right_utf8(self):
        self.verify(
            "――R",
            ["――", "R", ""],
            ["dash_ir", "piece_designator", "end_of_stream"],
        )

    def test_07_dash_left_right_ascii(self):
        self.verify(
            "b--R",
            ["b", "--", "R", ""],
            [
                "piece_designator",
                "dash_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_08_dash_left_right_utf8(self):
        self.verify(
            "b――R",
            ["b", "――", "R", ""],
            [
                "piece_designator",
                "dash_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_09_dash_right_ascii(self):
        self.verify(
            "b --R",
            ["b", " ", "--", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "dash_ir",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_10_dash_right_utf8(self):
        self.verify(
            "b ――R",
            ["b", " ", "――", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "dash_ir",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_11_dash_left_ascii(self):
        self.verify(
            "b-- R",
            ["b", "--", " ", "R", ""],
            [
                "piece_designator",
                "dash_li",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_12_dash_left_utf8(self):
        self.verify(
            "b―― R",
            ["b", "――", " ", "R", ""],
            [
                "piece_designator",
                "dash_li",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_13_dash_ascii(self):
        self.verify(
            "b -- R",
            ["b", " ", "--", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "dash_ii",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_14_dash_utf8(self):
        self.verify(
            "b ―― R",
            ["b", " ", "――", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "dash_ii",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_15_dash_ascii(self):
        self.verify(
            " -- ",
            [" ", "--", " ", ""],
            [
                "whitespace",
                "dash_ii",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_16_dash_utf8(self):
        self.verify(
            " ―― ",
            [" ", "――", " ", ""],
            [
                "whitespace",
                "dash_ii",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_17_dash_promote_ascii(self):
        self.verify(
            "--=q",
            ["--", "=", "q", ""],
            ["dash_ir", "assign", "piece_designator", "end_of_stream"],
        )

    def test_18_dash_promote_utf8(self):
        self.verify(
            "――=q",
            ["――", "=", "q", ""],
            ["dash_ir", "assign", "piece_designator", "end_of_stream"],
        )

    def test_19_dash_left_promote_ascii(self):
        self.verify(
            "R--=q",
            ["R", "--", "=", "q", ""],
            [
                "piece_designator",
                "dash_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_20_dash_left_promote_utf8(self):
        self.verify(
            "R――=q",
            ["R", "――", "=", "q", ""],
            [
                "piece_designator",
                "dash_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_21_dash_right_promote_ascii(self):
        self.verify(
            "--R=q",
            ["--", "R", "=", "q", ""],
            [
                "dash_ir",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_22_dash_right_promote_utf8(self):
        self.verify(
            "――R=q",
            ["――", "R", "=", "q", ""],
            [
                "dash_ir",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_23_dash_left_right_promote_ascii(self):
        self.verify(
            "b--R=n",
            ["b", "--", "R", "=", "n", ""],
            [
                "piece_designator",
                "dash_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_24_dash_left_right_promote_utf8(self):
        self.verify(
            "b――R=n",
            ["b", "――", "R", "=", "n", ""],
            [
                "piece_designator",
                "dash_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_25_dash_right_promote_ascii(self):
        self.verify(
            "b --R=n",
            ["b", " ", "--", "R", "=", "n", ""],
            [
                "piece_designator",
                "whitespace",
                "dash_ir",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_26_dash_right_promote_utf8(self):
        self.verify(
            "b ――R=n",
            ["b", " ", "――", "R", "=", "n", ""],
            [
                "piece_designator",
                "whitespace",
                "dash_ir",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_27_dash_left_promote_ascii(self):
        self.verify(
            "b--=r R",
            ["b", "--", "=", "r", " ", "R", ""],
            [
                "piece_designator",
                "dash_lr",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_28_dash_left_promote_utf8(self):
        self.verify(
            "b――=r R",
            ["b", "――", "=", "r", " ", "R", ""],
            [
                "piece_designator",
                "dash_lr",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_29_dash_promote_ascii(self):
        self.verify(
            "b --=Q R",
            ["b", " ", "--", "=", "Q", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "dash_ir",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_30_dash_promote_utf8(self):
        self.verify(
            "b ――=Q R",
            ["b", " ", "――", "=", "Q", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "dash_ir",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_31_dash_promote_ascii(self):
        self.verify(
            " --=Q ",
            [" ", "--", "=", "Q", " ", ""],
            [
                "whitespace",
                "dash_ir",
                "assign",
                "piece_designator",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_32_dash_promote_utf8(self):
        self.verify(
            " ――=Q ",
            [" ", "――", "=", "Q", " ", ""],
            [
                "whitespace",
                "dash_ir",
                "assign",
                "piece_designator",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_33_dash_parenthesisleft_ascii(self):
        self.verify(
            "(--",
            ["(", "--", ""],
            ["parenthesis_left", "dash_li", "end_of_stream"],
        )

    def test_34_dash_parenthesisleft_utf8(self):
        self.verify(
            "(――",
            ["(", "――", ""],
            ["parenthesis_left", "dash_li", "end_of_stream"],
        )

    def test_35_dash_braceleft_ascii(self):
        self.verify(
            "{--",
            ["{", "--", ""],
            ["brace_left", "dash_li", "end_of_stream"],
        )

    def test_36_dash_braceleft_utf8(self):
        self.verify(
            "{――",
            ["{", "――", ""],
            ["brace_left", "dash_li", "end_of_stream"],
        )

    def test_37_dash_parenthesisleft_promote_ascii(self):
        self.verify(
            "(--=Q",
            ["(", "--", "=", "Q", ""],
            [
                "parenthesis_left",
                "dash_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_38_dash_parenthesisleft_promote_utf8(self):
        self.verify(
            "(――=Q",
            ["(", "――", "=", "Q", ""],
            [
                "parenthesis_left",
                "dash_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_39_dash_braceleft_promote_ascii(self):
        self.verify(
            "{--=Q",
            ["{", "--", "=", "Q", ""],
            [
                "brace_left",
                "dash_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_40_dash_brace_left_promote_utf8(self):
        self.verify(
            "{――=Q",
            ["{", "――", "=", "Q", ""],
            [
                "brace_left",
                "dash_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_41_dash_parenthesisright_ascii(self):
        self.verify(
            "--)",
            ["--", ")", ""],
            ["dash_ir", "parenthesis_right", "end_of_stream"],
        )

    def test_42_dash_parenthesisright_utf8(self):
        self.verify(
            "――)",
            ["――", ")", ""],
            ["dash_ir", "parenthesis_right", "end_of_stream"],
        )

    def test_43_dash_braceright_ascii(self):
        self.verify(
            "--}",
            ["--", "}", ""],
            ["dash_ir", "brace_right", "end_of_stream"],
        )

    def test_44_dash_braceright_utf8(self):
        self.verify(
            "――}",
            ["――", "}", ""],
            ["dash_ir", "brace_right", "end_of_stream"],
        )

    def test_45_dash_parenthesisleft_parenthesisright_ascii(self):
        self.verify(
            "(--)",
            ["(", "--", ")", ""],
            [
                "parenthesis_left",
                "dash_lr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_46_dash_parenthesisleft_parenthesisright_utf8(self):
        self.verify(
            "(――)",
            ["(", "――", ")", ""],
            [
                "parenthesis_left",
                "dash_lr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_47_dash_braceleft_braceright_ascii(self):
        self.verify(
            "{--}",
            ["{", "--", "}", ""],
            [
                "brace_left",
                "dash_lr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_48_dash_braceleft_braceright_utf8(self):
        self.verify(
            "{――}",
            ["{", "――", "}", ""],
            [
                "brace_left",
                "dash_lr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_49_dash_parenthesisleft_right_ascii(self):
        self.verify(
            "(--R",
            ["(", "--", "R", ""],
            [
                "parenthesis_left",
                "dash_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_50_dash_parenthesisleft_right_utf8(self):
        self.verify(
            "(――R",
            ["(", "――", "R", ""],
            [
                "parenthesis_left",
                "dash_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_51_dash_braceleft_right_ascii(self):
        self.verify(
            "{--N",
            ["{", "--", "N", ""],
            [
                "brace_left",
                "dash_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_52_dash_braceleft_right_utf8(self):
        self.verify(
            "{――N",
            ["{", "――", "N", ""],
            [
                "brace_left",
                "dash_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_53_dash_parenthesisleft_right_promote_ascii(self):
        self.verify(
            "(--R=q",
            ["(", "--", "R", "=", "q", ""],
            [
                "parenthesis_left",
                "dash_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_54_dash_parenthesisleft_right_promote_utf8(self):
        self.verify(
            "(――R=q",
            ["(", "――", "R", "=", "q", ""],
            [
                "parenthesis_left",
                "dash_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_55_dash_braceleft_right_promote_ascii(self):
        self.verify(
            "{--N=q",
            ["{", "--", "N", "=", "q", ""],
            [
                "brace_left",
                "dash_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_56_dash_braceleft_right_promote_utf8(self):
        self.verify(
            "{――N=q",
            ["{", "――", "N", "=", "q", ""],
            [
                "brace_left",
                "dash_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_57_dash_left_parenthesisright_promote_ascii(self):
        self.verify(
            "R--)",
            ["R", "--", ")", ""],
            [
                "piece_designator",
                "dash_lr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_58_dash_left_parenthesisright_promote_utf8(self):
        self.verify(
            "R――)",
            ["R", "――", ")", ""],
            [
                "piece_designator",
                "dash_lr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_59_dash_left_braceright_promote_ascii(self):
        self.verify(
            "N--}",
            ["N", "--", "}", ""],
            [
                "piece_designator",
                "dash_lr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_60_dash_left_braceright_promote_utf8(self):
        self.verify(
            "N――}",
            ["N", "――", "}", ""],
            [
                "piece_designator",
                "dash_lr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_61_take_ascii(self):
        self.verify("[x]", ["[x]", ""], ["take_ii", "end_of_stream"])

    def test_62_take_utf8(self):
        self.verify("×", ["×", ""], ["take_ii", "end_of_stream"])

    def test_63_take_left_ascii(self):
        self.verify(
            "R[x]",
            ["R", "[x]", ""],
            ["piece_designator", "take_li", "end_of_stream"],
        )

    def test_64_take_left_utf8(self):
        self.verify(
            "R×",
            ["R", "×", ""],
            ["piece_designator", "take_li", "end_of_stream"],
        )

    def test_65_take_right_ascii(self):
        self.verify(
            "[x]R",
            ["[x]", "R", ""],
            ["take_ir", "piece_designator", "end_of_stream"],
        )

    def test_66_take_right_utf8(self):
        self.verify(
            "×R",
            ["×", "R", ""],
            ["take_ir", "piece_designator", "end_of_stream"],
        )

    def test_67_take_left_right_ascii(self):
        self.verify(
            "b[x]R",
            ["b", "[x]", "R", ""],
            [
                "piece_designator",
                "take_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_68_take_left_right_utf8(self):
        self.verify(
            "b×R",
            ["b", "×", "R", ""],
            [
                "piece_designator",
                "take_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_69_take_right_ascii(self):
        self.verify(
            "b [x]R",
            ["b", " ", "[x]", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "take_ir",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_70_take_right_utf8(self):
        self.verify(
            "b ×R",
            ["b", " ", "×", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "take_ir",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_71_take_left_ascii(self):
        self.verify(
            "b[x] R",
            ["b", "[x]", " ", "R", ""],
            [
                "piece_designator",
                "take_li",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_72_take_left_utf8(self):
        self.verify(
            "b× R",
            ["b", "×", " ", "R", ""],
            [
                "piece_designator",
                "take_li",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_73_take_ascii(self):
        self.verify(
            "b [x] R",
            ["b", " ", "[x]", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "take_ii",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_74_take_utf8(self):
        self.verify(
            "b × R",
            ["b", " ", "×", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "take_ii",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_75_take_ascii(self):
        self.verify(
            " [x] ",
            [" ", "[x]", " ", ""],
            [
                "whitespace",
                "take_ii",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_76_take_utf8(self):
        self.verify(
            " × ",
            [" ", "×", " ", ""],
            [
                "whitespace",
                "take_ii",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_77_take_promote_ascii(self):
        self.verify(
            "[x]=q",
            ["[x]", "=", "q", ""],
            ["take_ir", "assign", "piece_designator", "end_of_stream"],
        )

    def test_78_take_promote_utf8(self):
        self.verify(
            "×=q",
            ["×", "=", "q", ""],
            ["take_ir", "assign", "piece_designator", "end_of_stream"],
        )

    def test_79_take_left_promote_ascii(self):
        self.verify(
            "R[x]=q",
            ["R", "[x]", "=", "q", ""],
            [
                "piece_designator",
                "take_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_80_take_left_promote_utf8(self):
        self.verify(
            "R×=q",
            ["R", "×", "=", "q", ""],
            [
                "piece_designator",
                "take_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_81_take_right_promote_ascii(self):
        self.verify(
            "[x]R=q",
            ["[x]", "R", "=", "q", ""],
            [
                "take_ir",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_82_take_right_promote_utf8(self):
        self.verify(
            "×R=q",
            ["×", "R", "=", "q", ""],
            [
                "take_ir",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_83_take_left_right_promote_ascii(self):
        self.verify(
            "b[x]R=n",
            ["b", "[x]", "R", "=", "n", ""],
            [
                "piece_designator",
                "take_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_84_take_left_right_promote_utf8(self):
        self.verify(
            "b×R=n",
            ["b", "×", "R", "=", "n", ""],
            [
                "piece_designator",
                "take_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_85_take_right_promote_ascii(self):
        self.verify(
            "b [x]R=n",
            ["b", " ", "[x]", "R", "=", "n", ""],
            [
                "piece_designator",
                "whitespace",
                "take_ir",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_86_take_right_promote_utf8(self):
        self.verify(
            "b ×R=n",
            ["b", " ", "×", "R", "=", "n", ""],
            [
                "piece_designator",
                "whitespace",
                "take_ir",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_87_take_left_promote_ascii(self):
        self.verify(
            "b[x]=r R",
            ["b", "[x]", "=", "r", " ", "R", ""],
            [
                "piece_designator",
                "take_lr",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_88_take_left_promote_utf8(self):
        self.verify(
            "b×=r R",
            ["b", "×", "=", "r", " ", "R", ""],
            [
                "piece_designator",
                "take_lr",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_89_take_promote_ascii(self):
        self.verify(
            "b [x]=Q R",
            ["b", " ", "[x]", "=", "Q", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "take_ir",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_90_take_promote_utf8(self):
        self.verify(
            "b ×=Q R",
            ["b", " ", "×", "=", "Q", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "take_ir",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_91_take_promote_ascii(self):
        self.verify(
            " [x]=Q ",
            [" ", "[x]", "=", "Q", " ", ""],
            [
                "whitespace",
                "take_ir",
                "assign",
                "piece_designator",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_92_take_promote_utf8(self):
        self.verify(
            " ×=Q ",
            [" ", "×", "=", "Q", " ", ""],
            [
                "whitespace",
                "take_ir",
                "assign",
                "piece_designator",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_93_take_parenthesisleft_ascii(self):
        self.verify(
            "([x]",
            ["(", "[x]", ""],
            ["parenthesis_left", "take_li", "end_of_stream"],
        )

    def test_94_take_parenthesisleft_utf8(self):
        self.verify(
            "(×",
            ["(", "×", ""],
            ["parenthesis_left", "take_li", "end_of_stream"],
        )

    def test_95_take_braceleft_ascii(self):
        self.verify(
            "{[x]",
            ["{", "[x]", ""],
            ["brace_left", "take_li", "end_of_stream"],
        )

    def test_96_take_braceleft_utf8(self):
        self.verify(
            "{×",
            ["{", "×", ""],
            ["brace_left", "take_li", "end_of_stream"],
        )

    def test_97_take_parenthesisleft_promote_ascii(self):
        self.verify(
            "([x]=Q",
            ["(", "[x]", "=", "Q", ""],
            [
                "parenthesis_left",
                "take_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_98_take_parenthesisleft_promote_utf8(self):
        self.verify(
            "(×=Q",
            ["(", "×", "=", "Q", ""],
            [
                "parenthesis_left",
                "take_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_99_take_braceleft_promote_ascii(self):
        self.verify(
            "{[x]=Q",
            ["{", "[x]", "=", "Q", ""],
            [
                "brace_left",
                "take_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_100_take_brace_left_promote_utf8(self):
        self.verify(
            "{×=Q",
            ["{", "×", "=", "Q", ""],
            [
                "brace_left",
                "take_lr",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_101_take_parenthesisright_ascii(self):
        self.verify(
            "[x])",
            ["[x]", ")", ""],
            ["take_ir", "parenthesis_right", "end_of_stream"],
        )

    def test_102_take_parenthesisright_utf8(self):
        self.verify(
            "×)",
            ["×", ")", ""],
            ["take_ir", "parenthesis_right", "end_of_stream"],
        )

    def test_103_take_braceright_ascii(self):
        self.verify(
            "[x]}",
            ["[x]", "}", ""],
            ["take_ir", "brace_right", "end_of_stream"],
        )

    def test_104_take_braceright_utf8(self):
        self.verify(
            "×}",
            ["×", "}", ""],
            ["take_ir", "brace_right", "end_of_stream"],
        )

    def test_105_take_parenthesisleft_parenthesisright_ascii(self):
        self.verify(
            "([x])",
            ["(", "[x]", ")", ""],
            [
                "parenthesis_left",
                "take_lr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_106_take_parenthesisleft_parenthesisright_utf8(self):
        self.verify(
            "(×)",
            ["(", "×", ")", ""],
            [
                "parenthesis_left",
                "take_lr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_107_take_braceleft_braceright_ascii(self):
        self.verify(
            "{[x]}",
            ["{", "[x]", "}", ""],
            [
                "brace_left",
                "take_lr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_108_take_braceleft_braceright_utf8(self):
        self.verify(
            "{×}",
            ["{", "×", "}", ""],
            [
                "brace_left",
                "take_lr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_109_take_parenthesisleft_right_ascii(self):
        self.verify(
            "([x]R",
            ["(", "[x]", "R", ""],
            [
                "parenthesis_left",
                "take_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_110_take_parenthesisleft_right_utf8(self):
        self.verify(
            "(×R",
            ["(", "×", "R", ""],
            [
                "parenthesis_left",
                "take_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_111_take_braceleft_right_ascii(self):
        self.verify(
            "{[x]N",
            ["{", "[x]", "N", ""],
            [
                "brace_left",
                "take_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_112_take_braceleft_right_utf8(self):
        self.verify(
            "{×N",
            ["{", "×", "N", ""],
            [
                "brace_left",
                "take_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_113_take_parenthesisleft_right_promote_ascii(self):
        self.verify(
            "([x]R=q",
            ["(", "[x]", "R", "=", "q", ""],
            [
                "parenthesis_left",
                "take_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_114_take_parenthesisleft_right_promote_utf8(self):
        self.verify(
            "(×R=q",
            ["(", "×", "R", "=", "q", ""],
            [
                "parenthesis_left",
                "take_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_115_take_braceleft_right_promote_ascii(self):
        self.verify(
            "{[x]N=q",
            ["{", "[x]", "N", "=", "q", ""],
            [
                "brace_left",
                "take_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_116_take_braceleft_right_promote_utf8(self):
        self.verify(
            "{×N=q",
            ["{", "×", "N", "=", "q", ""],
            [
                "brace_left",
                "take_lr",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_117_take_left_parenthesisright_promote_ascii(self):
        self.verify(
            "R[x])",
            ["R", "[x]", ")", ""],
            [
                "piece_designator",
                "take_lr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_118_take_left_parenthesisright_promote_utf8(self):
        self.verify(
            "R×)",
            ["R", "×", ")", ""],
            [
                "piece_designator",
                "take_lr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_119_take_left_braceright_promote_ascii(self):
        self.verify(
            "N[x]}",
            ["N", "[x]", "}", ""],
            [
                "piece_designator",
                "take_lr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_120_take_left_braceright_promote_utf8(self):
        self.verify(
            "N×}",
            ["N", "×", "}", ""],
            [
                "piece_designator",
                "take_lr",
                "brace_right",
                "end_of_stream",
            ],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Patterns))
