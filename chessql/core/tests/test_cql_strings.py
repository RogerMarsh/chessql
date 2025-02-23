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

    def test_01_single_move_ascii(self):
        self.verify("--", ["--", ""], ["single_move", "end_of_stream"])

    def test_02_single_move_utf8(self):
        self.verify("――", ["――", ""], ["single_move", "end_of_stream"])

    def test_03_single_move_left_ascii(self):
        self.verify(
            "R--",
            ["R", "--", ""],
            ["piece_designator", "single_move_l", "end_of_stream"],
        )

    def test_04_single_move_left_utf8(self):
        self.verify(
            "R――",
            ["R", "――", ""],
            ["piece_designator", "single_move_l", "end_of_stream"],
        )

    def test_05_single_move_right_ascii(self):
        self.verify(
            "--R",
            ["--", "R", ""],
            ["single_move_r", "piece_designator", "end_of_stream"],
        )

    def test_06_single_move_right_utf8(self):
        self.verify(
            "――R",
            ["――", "R", ""],
            ["single_move_r", "piece_designator", "end_of_stream"],
        )

    def test_07_single_move_left_right_ascii(self):
        self.verify(
            "b--R",
            ["b", "--", "R", ""],
            [
                "piece_designator",
                "single_move_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_08_single_move_left_right_utf8(self):
        self.verify(
            "b――R",
            ["b", "――", "R", ""],
            [
                "piece_designator",
                "single_move_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_09_single_move_right_ascii(self):
        self.verify(
            "b --R",
            ["b", " ", "--", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "single_move_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_10_single_move_right_utf8(self):
        self.verify(
            "b ――R",
            ["b", " ", "――", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "single_move_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_11_single_move_left_ascii(self):
        self.verify(
            "b-- R",
            ["b", "--", " ", "R", ""],
            [
                "piece_designator",
                "single_move_l",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_12_single_move_left_utf8(self):
        self.verify(
            "b―― R",
            ["b", "――", " ", "R", ""],
            [
                "piece_designator",
                "single_move_l",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_13_single_move_ascii(self):
        self.verify(
            "b -- R",
            ["b", " ", "--", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "single_move",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_14_single_move_utf8(self):
        self.verify(
            "b ―― R",
            ["b", " ", "――", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "single_move",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_15_single_move_ascii(self):
        self.verify(
            " -- ",
            [" ", "--", " ", ""],
            [
                "whitespace",
                "single_move",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_16_single_move_utf8(self):
        self.verify(
            " ―― ",
            [" ", "――", " ", ""],
            [
                "whitespace",
                "single_move",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_17_single_move_promote_ascii(self):
        self.verify(
            "--=q",
            ["--", "=", "q", ""],
            ["single_move_p", "assign", "piece_designator", "end_of_stream"],
        )

    def test_18_single_move_promote_utf8(self):
        self.verify(
            "――=q",
            ["――", "=", "q", ""],
            ["single_move_p", "assign", "piece_designator", "end_of_stream"],
        )

    def test_19_single_move_left_promote_ascii(self):
        self.verify(
            "R--=q",
            ["R", "--", "=", "q", ""],
            [
                "piece_designator",
                "single_move_l_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_20_single_move_left_promote_utf8(self):
        self.verify(
            "R――=q",
            ["R", "――", "=", "q", ""],
            [
                "piece_designator",
                "single_move_l_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_21_single_move_right_promote_ascii(self):
        self.verify(
            "--R=q",
            ["--", "R", "=", "q", ""],
            [
                "single_move_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_22_single_move_right_promote_utf8(self):
        self.verify(
            "――R=q",
            ["――", "R", "=", "q", ""],
            [
                "single_move_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_23_single_move_left_right_promote_ascii(self):
        self.verify(
            "b--R=n",
            ["b", "--", "R", "=", "n", ""],
            [
                "piece_designator",
                "single_move_lr_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_24_single_move_left_right_promote_utf8(self):
        self.verify(
            "b――R=n",
            ["b", "――", "R", "=", "n", ""],
            [
                "piece_designator",
                "single_move_lr_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_25_single_move_right_promote_ascii(self):
        self.verify(
            "b --R=n",
            ["b", " ", "--", "R", "=", "n", ""],
            [
                "piece_designator",
                "whitespace",
                "single_move_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_26_single_move_right_promote_utf8(self):
        self.verify(
            "b ――R=n",
            ["b", " ", "――", "R", "=", "n", ""],
            [
                "piece_designator",
                "whitespace",
                "single_move_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_27_single_move_left_promote_ascii(self):
        self.verify(
            "b--=r R",
            ["b", "--", "=", "r", " ", "R", ""],
            [
                "piece_designator",
                "single_move_l_p",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_28_single_move_left_promote_utf8(self):
        self.verify(
            "b――=r R",
            ["b", "――", "=", "r", " ", "R", ""],
            [
                "piece_designator",
                "single_move_l_p",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_29_single_move_promote_ascii(self):
        self.verify(
            "b --=Q R",
            ["b", " ", "--", "=", "Q", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "single_move_p",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_30_single_move_promote_utf8(self):
        self.verify(
            "b ――=Q R",
            ["b", " ", "――", "=", "Q", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "single_move_p",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_31_single_move_promote_ascii(self):
        self.verify(
            " --=Q ",
            [" ", "--", "=", "Q", " ", ""],
            [
                "whitespace",
                "single_move_p",
                "assign",
                "piece_designator",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_32_single_move_promote_utf8(self):
        self.verify(
            " ――=Q ",
            [" ", "――", "=", "Q", " ", ""],
            [
                "whitespace",
                "single_move_p",
                "assign",
                "piece_designator",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_33_single_move_parenthesisleft_ascii(self):
        self.verify(
            "(--",
            ["(", "--", ""],
            ["parenthesis_left", "single_move_bl", "end_of_stream"],
        )

    def test_34_single_move_parenthesisleft_utf8(self):
        self.verify(
            "(――",
            ["(", "――", ""],
            ["parenthesis_left", "single_move_bl", "end_of_stream"],
        )

    def test_35_single_move_braceleft_ascii(self):
        self.verify(
            "{--",
            ["{", "--", ""],
            ["brace_left", "single_move_bl", "end_of_stream"],
        )

    def test_36_single_move_braceleft_utf8(self):
        self.verify(
            "{――",
            ["{", "――", ""],
            ["brace_left", "single_move_bl", "end_of_stream"],
        )

    def test_37_single_move_parenthesisleft_promote_ascii(self):
        self.verify(
            "(--=Q",
            ["(", "--", "=", "Q", ""],
            [
                "parenthesis_left",
                "single_move_bl_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_38_single_move_parenthesisleft_promote_utf8(self):
        self.verify(
            "(――=Q",
            ["(", "――", "=", "Q", ""],
            [
                "parenthesis_left",
                "single_move_bl_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_39_single_move_braceleft_promote_ascii(self):
        self.verify(
            "{--=Q",
            ["{", "--", "=", "Q", ""],
            [
                "brace_left",
                "single_move_bl_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_40_single_move_brace_left_promote_utf8(self):
        self.verify(
            "{――=Q",
            ["{", "――", "=", "Q", ""],
            [
                "brace_left",
                "single_move_bl_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_41_single_move_parenthesisright_ascii(self):
        self.verify(
            "--)",
            ["--", ")", ""],
            ["single_move_br", "parenthesis_right", "end_of_stream"],
        )

    def test_42_single_move_parenthesisright_utf8(self):
        self.verify(
            "――)",
            ["――", ")", ""],
            ["single_move_br", "parenthesis_right", "end_of_stream"],
        )

    def test_43_single_move_braceright_ascii(self):
        self.verify(
            "--}",
            ["--", "}", ""],
            ["single_move_br", "brace_right", "end_of_stream"],
        )

    def test_44_single_move_braceright_utf8(self):
        self.verify(
            "――}",
            ["――", "}", ""],
            ["single_move_br", "brace_right", "end_of_stream"],
        )

    def test_45_single_move_parenthesisleft_parenthesisright_ascii(self):
        self.verify(
            "(--)",
            ["(", "--", ")", ""],
            [
                "parenthesis_left",
                "single_move_blbr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_46_single_move_parenthesisleft_parenthesisright_utf8(self):
        self.verify(
            "(――)",
            ["(", "――", ")", ""],
            [
                "parenthesis_left",
                "single_move_blbr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_47_single_move_braceleft_braceright_ascii(self):
        self.verify(
            "{--}",
            ["{", "--", "}", ""],
            [
                "brace_left",
                "single_move_blbr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_48_single_move_braceleft_braceright_utf8(self):
        self.verify(
            "{――}",
            ["{", "――", "}", ""],
            [
                "brace_left",
                "single_move_blbr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_49_single_move_parenthesisleft_right_ascii(self):
        self.verify(
            "(--R",
            ["(", "--", "R", ""],
            [
                "parenthesis_left",
                "single_move_bl_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_50_single_move_parenthesisleft_right_utf8(self):
        self.verify(
            "(――R",
            ["(", "――", "R", ""],
            [
                "parenthesis_left",
                "single_move_bl_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_51_single_move_braceleft_right_ascii(self):
        self.verify(
            "{--N",
            ["{", "--", "N", ""],
            [
                "brace_left",
                "single_move_bl_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_52_single_move_braceleft_right_utf8(self):
        self.verify(
            "{――N",
            ["{", "――", "N", ""],
            [
                "brace_left",
                "single_move_bl_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_53_single_move_parenthesisleft_right_promote_ascii(self):
        self.verify(
            "(--R=q",
            ["(", "--", "R", "=", "q", ""],
            [
                "parenthesis_left",
                "single_move_bl_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_54_single_move_parenthesisleft_right_promote_utf8(self):
        self.verify(
            "(――R=q",
            ["(", "――", "R", "=", "q", ""],
            [
                "parenthesis_left",
                "single_move_bl_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_55_single_move_braceleft_right_promote_ascii(self):
        self.verify(
            "{--N=q",
            ["{", "--", "N", "=", "q", ""],
            [
                "brace_left",
                "single_move_bl_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_56_single_move_braceleft_right_promote_utf8(self):
        self.verify(
            "{――N=q",
            ["{", "――", "N", "=", "q", ""],
            [
                "brace_left",
                "single_move_bl_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_57_single_move_left_parenthesisright_promote_ascii(self):
        self.verify(
            "R--)",
            ["R", "--", ")", ""],
            [
                "piece_designator",
                "single_move_l_br",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_58_single_move_left_parenthesisright_promote_utf8(self):
        self.verify(
            "R――)",
            ["R", "――", ")", ""],
            [
                "piece_designator",
                "single_move_l_br",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_59_single_move_left_braceright_promote_ascii(self):
        self.verify(
            "N--}",
            ["N", "--", "}", ""],
            [
                "piece_designator",
                "single_move_l_br",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_60_single_move_left_braceright_promote_utf8(self):
        self.verify(
            "N――}",
            ["N", "――", "}", ""],
            [
                "piece_designator",
                "single_move_l_br",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_61_captures_ascii(self):
        self.verify("[x]", ["[x]", ""], ["captures", "end_of_stream"])

    def test_62_captures_utf8(self):
        self.verify("×", ["×", ""], ["captures", "end_of_stream"])

    def test_63_captures_left_ascii(self):
        self.verify(
            "R[x]",
            ["R", "[x]", ""],
            ["piece_designator", "captures_l", "end_of_stream"],
        )

    def test_64_captures_left_utf8(self):
        self.verify(
            "R×",
            ["R", "×", ""],
            ["piece_designator", "captures_l", "end_of_stream"],
        )

    def test_65_captures_right_ascii(self):
        self.verify(
            "[x]R",
            ["[x]", "R", ""],
            ["captures_r", "piece_designator", "end_of_stream"],
        )

    def test_66_captures_right_utf8(self):
        self.verify(
            "×R",
            ["×", "R", ""],
            ["captures_r", "piece_designator", "end_of_stream"],
        )

    def test_67_captures_left_right_ascii(self):
        self.verify(
            "b[x]R",
            ["b", "[x]", "R", ""],
            [
                "piece_designator",
                "captures_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_68_captures_left_right_utf8(self):
        self.verify(
            "b×R",
            ["b", "×", "R", ""],
            [
                "piece_designator",
                "captures_lr",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_69_captures_right_ascii(self):
        self.verify(
            "b [x]R",
            ["b", " ", "[x]", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "captures_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_70_captures_right_utf8(self):
        self.verify(
            "b ×R",
            ["b", " ", "×", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "captures_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_71_captures_left_ascii(self):
        self.verify(
            "b[x] R",
            ["b", "[x]", " ", "R", ""],
            [
                "piece_designator",
                "captures_l",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_72_captures_left_utf8(self):
        self.verify(
            "b× R",
            ["b", "×", " ", "R", ""],
            [
                "piece_designator",
                "captures_l",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_73_captures_ascii(self):
        self.verify(
            "b [x] R",
            ["b", " ", "[x]", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "captures",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_74_captures_utf8(self):
        self.verify(
            "b × R",
            ["b", " ", "×", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "captures",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_75_captures_ascii(self):
        self.verify(
            " [x] ",
            [" ", "[x]", " ", ""],
            [
                "whitespace",
                "captures",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_76_captures_utf8(self):
        self.verify(
            " × ",
            [" ", "×", " ", ""],
            [
                "whitespace",
                "captures",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_77_captures_promote_ascii(self):
        self.verify(
            "[x]=q",
            ["[x]", "=", "q", ""],
            ["captures_p", "assign", "piece_designator", "end_of_stream"],
        )

    def test_78_captures_promote_utf8(self):
        self.verify(
            "×=q",
            ["×", "=", "q", ""],
            ["captures_p", "assign", "piece_designator", "end_of_stream"],
        )

    def test_79_captures_left_promote_ascii(self):
        self.verify(
            "R[x]=q",
            ["R", "[x]", "=", "q", ""],
            [
                "piece_designator",
                "captures_l_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_80_captures_left_promote_utf8(self):
        self.verify(
            "R×=q",
            ["R", "×", "=", "q", ""],
            [
                "piece_designator",
                "captures_l_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_81_captures_right_promote_ascii(self):
        self.verify(
            "[x]R=q",
            ["[x]", "R", "=", "q", ""],
            [
                "captures_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_82_captures_right_promote_utf8(self):
        self.verify(
            "×R=q",
            ["×", "R", "=", "q", ""],
            [
                "captures_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_83_captures_left_right_promote_ascii(self):
        self.verify(
            "b[x]R=n",
            ["b", "[x]", "R", "=", "n", ""],
            [
                "piece_designator",
                "captures_lr_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_84_captures_left_right_promote_utf8(self):
        self.verify(
            "b×R=n",
            ["b", "×", "R", "=", "n", ""],
            [
                "piece_designator",
                "captures_lr_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_85_captures_right_promote_ascii(self):
        self.verify(
            "b [x]R=n",
            ["b", " ", "[x]", "R", "=", "n", ""],
            [
                "piece_designator",
                "whitespace",
                "captures_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_86_captures_right_promote_utf8(self):
        self.verify(
            "b ×R=n",
            ["b", " ", "×", "R", "=", "n", ""],
            [
                "piece_designator",
                "whitespace",
                "captures_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_87_captures_left_promote_ascii(self):
        self.verify(
            "b[x]=r R",
            ["b", "[x]", "=", "r", " ", "R", ""],
            [
                "piece_designator",
                "captures_l_p",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_88_captures_left_promote_utf8(self):
        self.verify(
            "b×=r R",
            ["b", "×", "=", "r", " ", "R", ""],
            [
                "piece_designator",
                "captures_l_p",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_89_captures_promote_ascii(self):
        self.verify(
            "b [x]=Q R",
            ["b", " ", "[x]", "=", "Q", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "captures_p",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_90_captures_promote_utf8(self):
        self.verify(
            "b ×=Q R",
            ["b", " ", "×", "=", "Q", " ", "R", ""],
            [
                "piece_designator",
                "whitespace",
                "captures_p",
                "assign",
                "piece_designator",
                "whitespace",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_91_captures_promote_ascii(self):
        self.verify(
            " [x]=Q ",
            [" ", "[x]", "=", "Q", " ", ""],
            [
                "whitespace",
                "captures_p",
                "assign",
                "piece_designator",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_92_captures_promote_utf8(self):
        self.verify(
            " ×=Q ",
            [" ", "×", "=", "Q", " ", ""],
            [
                "whitespace",
                "captures_p",
                "assign",
                "piece_designator",
                "whitespace",
                "end_of_stream",
            ],
        )

    def test_93_captures_parenthesisleft_ascii(self):
        self.verify(
            "([x]",
            ["(", "[x]", ""],
            ["parenthesis_left", "captures_bl", "end_of_stream"],
        )

    def test_94_captures_parenthesisleft_utf8(self):
        self.verify(
            "(×",
            ["(", "×", ""],
            ["parenthesis_left", "captures_bl", "end_of_stream"],
        )

    def test_95_captures_braceleft_ascii(self):
        self.verify(
            "{[x]",
            ["{", "[x]", ""],
            ["brace_left", "captures_bl", "end_of_stream"],
        )

    def test_96_captures_braceleft_utf8(self):
        self.verify(
            "{×",
            ["{", "×", ""],
            ["brace_left", "captures_bl", "end_of_stream"],
        )

    def test_97_captures_parenthesisleft_promote_ascii(self):
        self.verify(
            "([x]=Q",
            ["(", "[x]", "=", "Q", ""],
            [
                "parenthesis_left",
                "captures_bl_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_98_captures_parenthesisleft_promote_utf8(self):
        self.verify(
            "(×=Q",
            ["(", "×", "=", "Q", ""],
            [
                "parenthesis_left",
                "captures_bl_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_99_captures_braceleft_promote_ascii(self):
        self.verify(
            "{[x]=Q",
            ["{", "[x]", "=", "Q", ""],
            [
                "brace_left",
                "captures_bl_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_100_captures_brace_left_promote_utf8(self):
        self.verify(
            "{×=Q",
            ["{", "×", "=", "Q", ""],
            [
                "brace_left",
                "captures_bl_p",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_101_captures_parenthesisright_ascii(self):
        self.verify(
            "[x])",
            ["[x]", ")", ""],
            ["captures_br", "parenthesis_right", "end_of_stream"],
        )

    def test_102_captures_parenthesisright_utf8(self):
        self.verify(
            "×)",
            ["×", ")", ""],
            ["captures_br", "parenthesis_right", "end_of_stream"],
        )

    def test_103_captures_braceright_ascii(self):
        self.verify(
            "[x]}",
            ["[x]", "}", ""],
            ["captures_br", "brace_right", "end_of_stream"],
        )

    def test_104_captures_braceright_utf8(self):
        self.verify(
            "×}",
            ["×", "}", ""],
            ["captures_br", "brace_right", "end_of_stream"],
        )

    def test_105_captures_parenthesisleft_parenthesisright_ascii(self):
        self.verify(
            "([x])",
            ["(", "[x]", ")", ""],
            [
                "parenthesis_left",
                "captures_blbr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_106_captures_parenthesisleft_parenthesisright_utf8(self):
        self.verify(
            "(×)",
            ["(", "×", ")", ""],
            [
                "parenthesis_left",
                "captures_blbr",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_107_captures_braceleft_braceright_ascii(self):
        self.verify(
            "{[x]}",
            ["{", "[x]", "}", ""],
            [
                "brace_left",
                "captures_blbr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_108_captures_braceleft_braceright_utf8(self):
        self.verify(
            "{×}",
            ["{", "×", "}", ""],
            [
                "brace_left",
                "captures_blbr",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_109_captures_parenthesisleft_right_ascii(self):
        self.verify(
            "([x]R",
            ["(", "[x]", "R", ""],
            [
                "parenthesis_left",
                "captures_bl_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_110_captures_parenthesisleft_right_utf8(self):
        self.verify(
            "(×R",
            ["(", "×", "R", ""],
            [
                "parenthesis_left",
                "captures_bl_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_111_captures_braceleft_right_ascii(self):
        self.verify(
            "{[x]N",
            ["{", "[x]", "N", ""],
            [
                "brace_left",
                "captures_bl_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_112_captures_braceleft_right_utf8(self):
        self.verify(
            "{×N",
            ["{", "×", "N", ""],
            [
                "brace_left",
                "captures_bl_r",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_113_captures_parenthesisleft_right_promote_ascii(self):
        self.verify(
            "([x]R=q",
            ["(", "[x]", "R", "=", "q", ""],
            [
                "parenthesis_left",
                "captures_bl_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_114_captures_parenthesisleft_right_promote_utf8(self):
        self.verify(
            "(×R=q",
            ["(", "×", "R", "=", "q", ""],
            [
                "parenthesis_left",
                "captures_bl_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_115_captures_braceleft_right_promote_ascii(self):
        self.verify(
            "{[x]N=q",
            ["{", "[x]", "N", "=", "q", ""],
            [
                "brace_left",
                "captures_bl_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_116_captures_braceleft_right_promote_utf8(self):
        self.verify(
            "{×N=q",
            ["{", "×", "N", "=", "q", ""],
            [
                "brace_left",
                "captures_bl_r_p",
                "piece_designator",
                "assign",
                "piece_designator",
                "end_of_stream",
            ],
        )

    def test_117_captures_left_parenthesisright_promote_ascii(self):
        self.verify(
            "R[x])",
            ["R", "[x]", ")", ""],
            [
                "piece_designator",
                "captures_l_br",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_118_captures_left_parenthesisright_promote_utf8(self):
        self.verify(
            "R×)",
            ["R", "×", ")", ""],
            [
                "piece_designator",
                "captures_l_br",
                "parenthesis_right",
                "end_of_stream",
            ],
        )

    def test_119_captures_left_braceright_promote_ascii(self):
        self.verify(
            "N[x]}",
            ["N", "[x]", "}", ""],
            [
                "piece_designator",
                "captures_l_br",
                "brace_right",
                "end_of_stream",
            ],
        )

    def test_120_captures_left_braceright_promote_utf8(self):
        self.verify(
            "N×}",
            ["N", "×", "}", ""],
            [
                "piece_designator",
                "captures_l_br",
                "brace_right",
                "end_of_stream",
            ],
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(Patterns))
