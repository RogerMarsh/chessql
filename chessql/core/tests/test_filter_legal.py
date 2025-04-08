# test_filter_legal.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'legal' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FilterLegal(verify.Verify):

    def test_060_legal_01_plain_01_bare(self):
        self.verify("legal", [], returncode=1)

    def test_060_legal_01_plain_04_target_01_btm(self):
        self.verify("legal --(btm)", [], returncode=1)

    def test_060_legal_01_plain_04_target_02_o_o(self):
        self.verify(
            "legal --(o-o)",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
            ],
        )

    def test_060_legal_01_plain_04_target_03_o_o_o(self):
        self.verify(
            "legal --(o-o-o)",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OOO"),
            ],
        )

    def test_060_legal_01_plain_04_target_04_castle(self):
        self.verify(
            "legal --(castle)",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "Castle"),
            ],
        )

    def test_060_legal_01_plain_04_target_05_enpassant(self):
        self.verify(
            "legal --(enpassant)",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "EnPassant"),
            ],
        )

    def test_060_legal_01_plain_04_target_06_o_o_set(self):
        self.verify("legal --(o-o to)", [], returncode=1)

    def test_060_legal_01_plain_04_target_07_set_o_o(self):
        self.verify("legal --(Rc4 o-o)", [], returncode=1)

    def test_060_legal_02(self):
        self.verify("legal k", [], returncode=1)

    def test_060_legal_03_dash_ascii(self):
        self.verify(
            "legal --",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_060_legal_04_dash_utf8(self):
        self.verify(
            "legal ――",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_060_legal_05_not_allowed_01_take_ascii(self):
        self.verify("legal [x]", [], returncode=1)

    def test_060_legal_05_not_allowed_02_take_utf8(self):
        self.verify("legal ×", [], returncode=1)

    def test_060_legal_06_da_01_plain_06_rep_01_zero_up(self):
        self.verify("legal --*", [], returncode=1)

    def test_060_legal_06_da_01_plain_06_rep_02_one_up(self):
        self.verify("legal --+", [], returncode=1)

    def test_060_legal_06_da_01_plain_06_rep_03_optional(self):
        self.verify("legal --?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_01_plain_06_rep_04_exact(self):
        self.verify("legal --{5}", [], returncode=1)

    def test_060_legal_06_da_01_plain_06_rep_05_range(self):
        self.verify("legal --{3,5}", [], returncode=1)

    def test_060_legal_06_da_01_plain_06_rep_06_up_to(self):
        self.verify("legal --{,5}", [], returncode=1)

    def test_060_legal_06_da_01_plain_06_rep_07_and_over(self):
        self.verify("legal --{3,}", [], returncode=1)

    def test_060_legal_06_da_01_plain_06_rep_08_force_zero_up(self):
        self.verify("legal --{*}", [], returncode=1)

    def test_060_legal_06_da_01_plain_06_rep_09_force_one_up(self):
        self.verify("legal --{+}", [], returncode=1)

    def test_060_legal_06_da_02_left_06_rep_01_zero_up(self):
        self.verify("legal e2--*", [], returncode=1)

    def test_060_legal_06_da_02_left_06_rep_02_one_up(self):
        self.verify("legal e2--+", [], returncode=1)

    def test_060_legal_06_da_02_left_06_rep_03_optional(self):
        self.verify("legal e2--?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_02_left_06_rep_04_exact(self):
        self.verify("legal e2--{5}", [], returncode=1)

    def test_060_legal_06_da_02_left_06_rep_05_range(self):
        self.verify("legal e2--{3,5}", [], returncode=1)

    def test_060_legal_06_da_02_left_06_rep_06_up_to(self):
        self.verify("legal e2--{,5}", [], returncode=1)

    def test_060_legal_06_da_02_left_06_rep_07_and_over(self):
        self.verify("legal e2--{3,}", [], returncode=1)

    def test_060_legal_06_da_02_left_06_rep_08_force_zero_up(self):
        self.verify("legal e2--{*}", [], returncode=1)

    def test_060_legal_06_da_02_left_06_rep_09_force_one_up(self):
        self.verify("legal e2--{+}", [], returncode=1)

    def test_060_legal_06_da_03_right_06_rep_01_zero_up(self):
        self.verify("legal --Qa4*", [], returncode=1)

    def test_060_legal_06_da_03_right_06_rep_02_one_up(self):
        self.verify("legal --Qa4+", [], returncode=1)

    def test_060_legal_06_da_03_right_06_rep_03_optional(self):
        self.verify("legal --Qa4?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_03_right_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal --Qa4{5}",
            [
                (3, "Legal"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_03_right_06_rep_05_range(self):
        self.verify("legal --Qa4{3,5}", [], returncode=1)

    def test_060_legal_06_da_03_right_06_rep_06_up_to(self):
        self.verify("legal --Qa4{,5}", [], returncode=1)

    def test_060_legal_06_da_03_right_06_rep_07_and_over(self):
        self.verify("legal --Qa4{3,}", [], returncode=1)

    def test_060_legal_06_da_03_right_06_rep_08_force_zero_up(self):
        self.verify("legal --Qa4{*}", [], returncode=1)

    def test_060_legal_06_da_03_right_06_rep_09_force_one_up(self):
        self.verify("legal --Qa4{+}", [], returncode=1)

    def test_060_legal_06_da_04_lr_06_rep_01_zero_up(self):
        self.verify("legal e2--Qa4*", [], returncode=1)

    def test_060_legal_06_da_04_lr_06_rep_02_one_up(self):
        self.verify("legal e2--Qa4+", [], returncode=1)

    def test_060_legal_06_da_04_lr_06_rep_03_optional(self):
        self.verify("legal e2--Qa4?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_04_lr_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2--Qa4{5}",
            [
                (3, "Legal"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_04_lr_06_rep_05_range(self):
        self.verify("legal e2--Qa4{3,5}", [], returncode=1)

    def test_060_legal_06_da_04_lr_06_rep_06_up_to(self):
        self.verify("legal e2--Qa4{,5}", [], returncode=1)

    def test_060_legal_06_da_04_lr_06_rep_07_and_over(self):
        self.verify("legal e2--Qa4{3,}", [], returncode=1)

    def test_060_legal_06_da_04_lr_06_rep_08_force_zero_up(self):
        self.verify("legal e2--Qa4{*}", [], returncode=1)

    def test_060_legal_06_da_04_lr_06_rep_09_force_one_up(self):
        self.verify("legal e2--Qa4{+}", [], returncode=1)

    def test_060_legal_06_da_05_prom_06_rep_01_zero_up(self):
        self.verify("legal --=q*", [], returncode=1)

    def test_060_legal_06_da_05_prom_06_rep_02_one_up(self):
        self.verify("legal --=q+", [], returncode=1)

    def test_060_legal_06_da_05_prom_06_rep_03_optional(self):
        self.verify("legal --=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_05_prom_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal --=q{5}",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_05_prom_06_rep_05_range(self):
        self.verify("legal --=q{3,5}", [], returncode=1)

    def test_060_legal_06_da_05_prom_06_rep_06_up_to(self):
        self.verify("legal --=q{,5}", [], returncode=1)

    def test_060_legal_06_da_05_prom_06_rep_07_and_over(self):
        self.verify("legal --=q{3,}", [], returncode=1)

    def test_060_legal_06_da_05_prom_06_rep_08_force_zero_up(self):
        self.verify("legal --=q{*}", [], returncode=1)

    def test_060_legal_06_da_05_prom_06_rep_09_force_one_up(self):
        self.verify("legal --=q{+}", [], returncode=1)

    def test_060_legal_06_da_06_left_prom_06_rep_01_zero_up(self):
        self.verify("legal e2--=q*", [], returncode=1)

    def test_060_legal_06_da_06_left_prom_06_rep_02_one_up(self):
        self.verify("legal e2--=q+", [], returncode=1)

    def test_060_legal_06_da_06_left_prom_06_rep_03_optional(self):
        self.verify("legal e2--=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_06_left_prom_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2--=q{5}",
            [
                (3, "Legal"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_06_left_prom_06_rep_05_range(self):
        self.verify("legal e2--=q{3,5}", [], returncode=1)

    def test_060_legal_06_da_06_left_prom_06_rep_06_up_to(self):
        self.verify("legal e2--=q{,5}", [], returncode=1)

    def test_060_legal_06_da_06_left_prom_06_rep_07_and_over(self):
        self.verify("legal e2--=q{3,}", [], returncode=1)

    def test_060_legal_06_da_06_left_prom_06_rep_08_force_zero_up(self):
        self.verify("legal e2--=q{*}", [], returncode=1)

    def test_060_legal_06_da_06_left_prom_06_rep_09_force_one_up(self):
        self.verify("legal e2--=q{+}", [], returncode=1)

    def test_060_legal_06_da_07_right_prom_06_rep_01_zero_up(self):
        self.verify("legal --Qa4=q*", [], returncode=1)

    def test_060_legal_06_da_07_right_prom_06_rep_02_one_up(self):
        self.verify("legal --Qa4=q+", [], returncode=1)

    def test_060_legal_06_da_07_right_prom_06_rep_03_optional(self):
        self.verify("legal --Qa4=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_07_right_prom_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal --Qa4=q{5}",
            [
                (3, "Legal"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_07_right_prom_06_rep_05_range(self):
        self.verify("legal --Qa4=q{3,5}", [], returncode=1)

    def test_060_legal_06_da_07_right_prom_06_rep_06_up_to(self):
        self.verify("legal --Qa4=q{,5}", [], returncode=1)

    def test_060_legal_06_da_07_right_prom_06_rep_07_and_over(self):
        self.verify("legal --Qa4=q{3,}", [], returncode=1)

    def test_060_legal_06_da_07_right_prom_06_rep_08_force_zero_up(self):
        self.verify("legal --Qa4=q{*}", [], returncode=1)

    def test_060_legal_06_da_07_right_prom_06_rep_09_force_one_up(self):
        self.verify("legal --Qa4=q{+}", [], returncode=1)

    def test_060_legal_06_da_08_lr_prom_06_rep_01_zero_up(self):
        self.verify("legal e2--Qa4=q*", [], returncode=1)

    def test_060_legal_06_da_08_lr_prom_06_rep_02_one_up(self):
        self.verify("legal e2--Qa4=q+", [], returncode=1)

    def test_060_legal_06_da_08_lr_prom_06_rep_03_optional(self):
        self.verify("legal e2--Qa4=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_08_lr_prom_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2--Qa4=q{5}",
            [
                (3, "Legal"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_08_lr_prom_06_rep_05_range(self):
        self.verify("legal e2--Qa4=q{3,5}", [], returncode=1)

    def test_060_legal_06_da_08_lr_prom_06_rep_06_up_to(self):
        self.verify("legal e2--Qa4=q{,5}", [], returncode=1)

    def test_060_legal_06_da_08_lr_prom_06_rep_07_and_over(self):
        self.verify("legal e2--Qa4=q{3,}", [], returncode=1)

    def test_060_legal_06_da_08_lr_prom_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal e2--Qa4=q{*}", [], returncode=1)

    def test_060_legal_06_da_08_lr_prom_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal e2--Qa4=q{+}", [], returncode=1)

    def test_060_legal_06_da_09_target_06_rep_01_zero_up(self):
        self.verify("legal --(o-o)*", [], returncode=1)

    def test_060_legal_06_da_09_target_06_rep_02_one_up(self):
        self.verify("legal --(o-o)+", [], returncode=1)

    def test_060_legal_06_da_09_target_06_rep_03_optional(self):
        self.verify("legal --(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_09_target_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal --(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_09_target_06_rep_05_range(self):
        self.verify("legal --(o-o){3,5}", [], returncode=1)

    def test_060_legal_06_da_09_target_06_rep_06_up_to(self):
        self.verify("legal --(o-o){,5}", [], returncode=1)

    def test_060_legal_06_da_09_target_06_rep_07_and_over(self):
        self.verify("legal --(o-o){3,}", [], returncode=1)

    def test_060_legal_06_da_09_target_06_rep_08_force_zero_up(self):
        self.verify("legal --(o-o){*}", [], returncode=1)

    def test_060_legal_06_da_09_target_06_rep_09_force_one_up(self):
        self.verify("legal --(o-o){+}", [], returncode=1)

    def test_060_legal_06_da_10_left_target_06_rep_01_zero_up(self):
        self.verify("legal e2--(o-o)*", [], returncode=1)

    def test_060_legal_06_da_10_left_target_06_rep_02_one_up(self):
        self.verify("legal e2--(o-o)+", [], returncode=1)

    def test_060_legal_06_da_10_left_target_06_rep_03_optional(self):
        self.verify("legal e2--(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_10_left_target_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2--(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_10_left_target_06_rep_05_range(self):
        self.verify("legal e2--(o-o){3,5}", [], returncode=1)

    def test_060_legal_06_da_10_left_target_06_rep_06_up_to(self):
        self.verify("legal e2--(o-o){,5}", [], returncode=1)

    def test_060_legal_06_da_10_left_target_06_rep_07_and_over(self):
        self.verify("legal e2--(o-o){3,}", [], returncode=1)

    def test_060_legal_06_da_10_left_target_06_rep_08_force_zero_up(self):
        self.verify("legal e2--(o-o){*}", [], returncode=1)

    def test_060_legal_06_da_10_left_target_06_rep_09_force_one_up(self):
        self.verify("legal e2--(o-o){+}", [], returncode=1)

    def test_060_legal_06_da_11_right_target_06_rep_01_zero_up(self):
        self.verify("legal --Qa4(o-o)*", [], returncode=1)

    def test_060_legal_06_da_11_right_target_06_rep_02_one_up(self):
        self.verify("legal --Qa4(o-o)+", [], returncode=1)

    def test_060_legal_06_da_11_right_target_06_rep_03_optional(self):
        self.verify("legal --Qa4(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_11_right_target_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal --Qa4(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_11_right_target_06_rep_05_range(self):
        self.verify("legal --Qa4(o-o){3,5}", [], returncode=1)

    def test_060_legal_06_da_11_right_target_06_rep_06_up_to(self):
        self.verify("legal --Qa4(o-o){,5}", [], returncode=1)

    def test_060_legal_06_da_11_right_target_06_rep_07_and_over(self):
        self.verify("legal --Qa4(o-o){3,}", [], returncode=1)

    def test_060_legal_06_da_11_right_target_06_rep_08_force_zero_up(self):
        self.verify("legal --Qa4(o-o){*}", [], returncode=1)

    def test_060_legal_06_da_11_right_target_06_rep_09_force_one_up(self):
        self.verify("legal --Qa4(o-o){+}", [], returncode=1)

    def test_060_legal_06_da_12_lr_target_06_rep_01_zero_up(self):
        self.verify("legal e2--Qa4(o-o)*", [], returncode=1)

    def test_060_legal_06_da_12_lr_target_06_rep_02_one_up(self):
        self.verify("legal e2--Qa4(o-o)+", [], returncode=1)

    def test_060_legal_06_da_12_lr_target_06_rep_03_optional(self):
        self.verify("legal e2--Qa4(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_12_lr_target_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2--Qa4(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_12_lr_target_06_rep_05_range(self):
        self.verify("legal e2--Qa4(o-o){3,5}", [], returncode=1)

    def test_060_legal_06_da_12_lr_target_06_rep_06_up_to(self):
        self.verify("legal e2--Qa4(o-o){,5}", [], returncode=1)

    def test_060_legal_06_da_12_lr_target_06_rep_07_and_over(self):
        self.verify("legal e2--Qa4(o-o){3,}", [], returncode=1)

    def test_060_legal_06_da_12_lr_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal e2--Qa4(o-o){*}", [], returncode=1)

    def test_060_legal_06_da_12_lr_target_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal e2--Qa4(o-o){+}", [], returncode=1)

    def test_060_legal_06_da_13_prom_targ_06_rep_01_zero_up(self):
        self.verify("legal --=q(o-o)*", [], returncode=1)

    def test_060_legal_06_da_13_prom_targ_06_rep_02_one_up(self):
        self.verify("legal --=q(o-o)+", [], returncode=1)

    def test_060_legal_06_da_13_prom_targ_06_rep_03_optional(self):
        self.verify("legal --=q(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_13_prom_targ_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal --=q(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_13_prom_targ_06_rep_05_range(self):
        self.verify("legal --=q(o-o){3,5}", [], returncode=1)

    def test_060_legal_06_da_13_prom_targ_06_rep_06_up_to(self):
        self.verify("legal --=q(o-o){,5}", [], returncode=1)

    def test_060_legal_06_da_13_prom_targ_06_rep_07_and_over(self):
        self.verify("legal --=q(o-o){3,}", [], returncode=1)

    def test_060_legal_06_da_13_prom_targ_06_rep_08_force_zero_up(self):
        self.verify("legal --=q(o-o){*}", [], returncode=1)

    def test_060_legal_06_da_13_prom_targ_06_rep_09_force_one_up(self):
        self.verify("legal --=q(o-o){+}", [], returncode=1)

    def test_060_legal_06_da_14_l_prom_targ_06_rep_01_zero_up(self):
        self.verify("legal e2--=q(o-o)*", [], returncode=1)

    def test_060_legal_06_da_14_l_prom_targ_06_rep_02_one_up(self):
        self.verify("legal e2--=q(o-o)+", [], returncode=1)

    def test_060_legal_06_da_14_l_prom_targ_06_rep_03_optional(self):
        self.verify("legal e2--=q(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_14_l_prom_targ_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2--=q(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_14_l_prom_targ_06_rep_05_range(self):
        self.verify("legal e2--=q(o-o){3,5}", [], returncode=1)

    def test_060_legal_06_da_14_l_prom_targ_06_rep_06_up_to(self):
        self.verify("legal e2--=q(o-o){,5}", [], returncode=1)

    def test_060_legal_06_da_14_l_prom_targ_06_rep_07_and_over(self):
        self.verify("legal e2--=q(o-o){3,}", [], returncode=1)

    def test_060_legal_06_da_14_l_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal e2--=q(o-o){*}", [], returncode=1)

    def test_060_legal_06_da_14_l_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal e2--=q(o-o){+}", [], returncode=1)

    def test_060_legal_06_da_15_r_prom_targ_06_rep_01_zero_up(self):
        self.verify("legal --Qa4=q(o-o)*", [], returncode=1)

    def test_060_legal_06_da_15_r_prom_targ_06_rep_02_one_up(self):
        self.verify("legal --Qa4=q(o-o)+", [], returncode=1)

    def test_060_legal_06_da_15_r_prom_targ_06_rep_03_optional(self):
        self.verify("legal --Qa4=q(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_15_r_prom_targ_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal --Qa4=q(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_15_r_prom_targ_06_rep_05_range(self):
        self.verify("legal --Qa4=q(o-o){3,5}", [], returncode=1)

    def test_060_legal_06_da_15_r_prom_targ_06_rep_06_up_to(self):
        self.verify("legal --Qa4=q(o-o){,5}", [], returncode=1)

    def test_060_legal_06_da_15_r_prom_targ_06_rep_07_and_over(self):
        self.verify("legal --Qa4=q(o-o){3,}", [], returncode=1)

    def test_060_legal_06_da_15_r_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal --Qa4=q(o-o){*}", [], returncode=1)

    def test_060_legal_06_da_15_r_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal --Qa4=q(o-o){+}", [], returncode=1)

    def test_060_legal_06_da_16_lr_prom_targ_06_rep_01_zero_up(self):
        self.verify("legal e2--Qa4=q(o-o)*", [], returncode=1)

    def test_060_legal_06_da_16_lr_prom_targ_06_rep_02_one_up(self):
        self.verify("legal e2--Qa4=q(o-o)+", [], returncode=1)

    def test_060_legal_06_da_16_lr_prom_targ_06_rep_03_optional(self):
        self.verify("legal e2--Qa4=q(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_06_da_16_lr_prom_targ_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2--Qa4=q(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_06_da_16_lr_prom_targ_06_rep_05_range(self):
        self.verify("legal e2--Qa4=q(o-o){3,5}", [], returncode=1)

    def test_060_legal_06_da_16_lr_prom_targ_06_rep_06_up_to(self):
        self.verify("legal e2--Qa4=q(o-o){,5}", [], returncode=1)

    def test_060_legal_06_da_16_lr_prom_targ_06_rep_07_and_over(self):
        self.verify("legal e2--Qa4=q(o-o){3,}", [], returncode=1)

    def test_060_legal_06_da_16_lr_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal e2--Qa4=q(o-o){*}", [], returncode=1)

    def test_060_legal_06_da_16_lr_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal e2--Qa4=q(o-o){+}", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_01_zero_up(self):
        self.verify("legal ――*", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_02_one_up(self):
        self.verify("legal ――+", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_03_optional(self):
        self.verify("legal ――?", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_04_exact(self):
        self.verify("legal ――{5}", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_05_range(self):
        self.verify("legal ――{3,5}", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_06_up_to(self):
        self.verify("legal ――{,5}", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_07_and_over(self):
        self.verify("legal ――{3,}", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_08_force_zero_up(self):
        self.verify("legal ――{*}", [], returncode=1)

    def test_060_legal_07_du_01_plain_06_rep_09_force_one_up(self):
        self.verify("legal ――{+}", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_01_zero_up(self):
        self.verify("legal e2――*", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_02_one_up(self):
        self.verify("legal e2――+", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_03_optional(self):
        self.verify("legal e2――?", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_04_exact(self):
        self.verify("legal e2――{5}", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_05_range(self):
        self.verify("legal e2――{3,5}", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_06_up_to(self):
        self.verify("legal e2――{,5}", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_07_and_over(self):
        self.verify("legal e2――{3,}", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_08_force_zero_up(self):
        self.verify("legal e2――{*}", [], returncode=1)

    def test_060_legal_07_du_02_left_06_rep_09_force_one_up(self):
        self.verify("legal e2――{+}", [], returncode=1)

    def test_060_legal_07_du_03_right_06_rep_01_zero_up(self):
        self.verify("legal ――Qa4*", [], returncode=1)

    def test_060_legal_07_du_03_right_06_rep_02_one_up(self):
        self.verify("legal ――Qa4+", [], returncode=1)

    def test_060_legal_07_du_03_right_06_rep_03_optional(self):
        self.verify("legal ――Qa4?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_03_right_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal ――Qa4{5}",
            [
                (3, "Legal"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_03_right_06_rep_05_range(self):
        self.verify("legal ――Qa4{3,5}", [], returncode=1)

    def test_060_legal_07_du_03_right_06_rep_06_up_to(self):
        self.verify("legal ――Qa4{,5}", [], returncode=1)

    def test_060_legal_07_du_03_right_06_rep_07_and_over(self):
        self.verify("legal ――Qa4{3,}", [], returncode=1)

    def test_060_legal_07_du_03_right_06_rep_08_force_zero_up(self):
        self.verify("legal ――Qa4{*}", [], returncode=1)

    def test_060_legal_07_du_03_right_06_rep_09_force_one_up(self):
        self.verify("legal ――Qa4{+}", [], returncode=1)

    def test_060_legal_07_du_04_lr_06_rep_01_zero_up(self):
        self.verify("legal e2――Qa4*", [], returncode=1)

    def test_060_legal_07_du_04_lr_06_rep_02_one_up(self):
        self.verify("legal e2――Qa4+", [], returncode=1)

    def test_060_legal_07_du_04_lr_06_rep_03_optional(self):
        self.verify("legal e2――Qa4?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_04_lr_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2――Qa4{5}",
            [
                (3, "Legal"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_04_lr_06_rep_05_range(self):
        self.verify("legal e2――Qa4{3,5}", [], returncode=1)

    def test_060_legal_07_du_04_lr_06_rep_06_up_to(self):
        self.verify("legal e2――Qa4{,5}", [], returncode=1)

    def test_060_legal_07_du_04_lr_06_rep_07_and_over(self):
        self.verify("legal e2――Qa4{3,}", [], returncode=1)

    def test_060_legal_07_du_04_lr_06_rep_08_force_zero_up(self):
        self.verify("legal e2――Qa4{*}", [], returncode=1)

    def test_060_legal_07_du_04_lr_06_rep_09_force_one_up(self):
        self.verify("legal e2――Qa4{+}", [], returncode=1)

    def test_060_legal_07_du_05_prom_06_rep_01_zero_up(self):
        self.verify("legal ――=q*", [], returncode=1)

    def test_060_legal_07_du_05_prom_06_rep_02_one_up(self):
        self.verify("legal ――=q+", [], returncode=1)

    def test_060_legal_07_du_05_prom_06_rep_03_optional(self):
        self.verify("legal ――=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_05_prom_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal ――=q{5}",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_05_prom_06_rep_05_range(self):
        self.verify("legal ――=q{3,5}", [], returncode=1)

    def test_060_legal_07_du_05_prom_06_rep_06_up_to(self):
        self.verify("legal ――=q{,5}", [], returncode=1)

    def test_060_legal_07_du_05_prom_06_rep_07_and_over(self):
        self.verify("legal ――=q{3,}", [], returncode=1)

    def test_060_legal_07_du_05_prom_06_rep_08_force_zero_up(self):
        self.verify("legal ――=q{*}", [], returncode=1)

    def test_060_legal_07_du_05_prom_06_rep_09_force_one_up(self):
        self.verify("legal ――=q{+}", [], returncode=1)

    def test_060_legal_07_du_06_left_prom_06_rep_01_zero_up(self):
        self.verify("legal e2――=q*", [], returncode=1)

    def test_060_legal_07_du_06_left_prom_06_rep_02_one_up(self):
        self.verify("legal e2――=q+", [], returncode=1)

    def test_060_legal_07_du_06_left_prom_06_rep_03_optional(self):
        self.verify("legal e2――=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_06_left_prom_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2――=q{5}",
            [
                (3, "Legal"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_06_left_prom_06_rep_05_range(self):
        self.verify("legal e2――=q{3,5}", [], returncode=1)

    def test_060_legal_07_du_06_left_prom_06_rep_06_up_to(self):
        self.verify("legal e2――=q{,5}", [], returncode=1)

    def test_060_legal_07_du_06_left_prom_06_rep_07_and_over(self):
        self.verify("legal e2――=q{3,}", [], returncode=1)

    def test_060_legal_07_du_06_left_prom_06_rep_08_force_zero_up(self):
        self.verify("legal e2――=q{*}", [], returncode=1)

    def test_060_legal_07_du_06_left_prom_06_rep_09_force_one_up(self):
        self.verify("legal e2――=q{+}", [], returncode=1)

    def test_060_legal_07_du_07_right_prom_06_rep_01_zero_up(self):
        self.verify("legal ――Qa4=q*", [], returncode=1)

    def test_060_legal_07_du_07_right_prom_06_rep_02_one_up(self):
        self.verify("legal ――Qa4=q+", [], returncode=1)

    def test_060_legal_07_du_07_right_prom_06_rep_03_optional(self):
        self.verify("legal ――Qa4=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_07_right_prom_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal ――Qa4=q{5}",
            [
                (3, "Legal"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_07_right_prom_06_rep_05_range(self):
        self.verify("legal ――Qa4=q{3,5}", [], returncode=1)

    def test_060_legal_07_du_07_right_prom_06_rep_06_up_to(self):
        self.verify("legal ――Qa4=q{,5}", [], returncode=1)

    def test_060_legal_07_du_07_right_prom_06_rep_07_and_over(self):
        self.verify("legal ――Qa4=q{3,}", [], returncode=1)

    def test_060_legal_07_du_07_right_prom_06_rep_08_force_zero_up(self):
        self.verify("legal ――Qa4=q{*}", [], returncode=1)

    def test_060_legal_07_du_07_right_prom_06_rep_09_force_one_up(self):
        self.verify("legal ――Qa4=q{+}", [], returncode=1)

    def test_060_legal_07_du_08_lr_prom_06_rep_01_zero_up(self):
        self.verify("legal e2――Qa4=q*", [], returncode=1)

    def test_060_legal_07_du_08_lr_prom_06_rep_02_one_up(self):
        self.verify("legal e2――Qa4=q+", [], returncode=1)

    def test_060_legal_07_du_08_lr_prom_06_rep_03_optional(self):
        self.verify("legal e2――Qa4=q?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_08_lr_prom_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2――Qa4=q{5}",
            [
                (3, "Legal"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_08_lr_prom_06_rep_05_range(self):
        self.verify("legal e2――Qa4=q{3,5}", [], returncode=1)

    def test_060_legal_07_du_08_lr_prom_06_rep_06_up_to(self):
        self.verify("legal e2――Qa4=q{,5}", [], returncode=1)

    def test_060_legal_07_du_08_lr_prom_06_rep_07_and_over(self):
        self.verify("legal e2――Qa4=q{3,}", [], returncode=1)

    def test_060_legal_07_du_08_lr_prom_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal e2――Qa4=q{*}", [], returncode=1)

    def test_060_legal_07_du_08_lr_prom_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal e2――Qa4=q{+}", [], returncode=1)

    def test_060_legal_07_du_09_target_06_rep_01_zero_up(self):
        self.verify("legal ――(o-o)*", [], returncode=1)

    def test_060_legal_07_du_09_target_06_rep_02_one_up(self):
        self.verify("legal ――(o-o)+", [], returncode=1)

    def test_060_legal_07_du_09_target_06_rep_03_optional(self):
        self.verify("legal ――(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_09_target_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal ――(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_09_target_06_rep_05_range(self):
        self.verify("legal ――(o-o){3,5}", [], returncode=1)

    def test_060_legal_07_du_09_target_06_rep_06_up_to(self):
        self.verify("legal ――(o-o){,5}", [], returncode=1)

    def test_060_legal_07_du_09_target_06_rep_07_and_over(self):
        self.verify("legal ――(o-o){3,}", [], returncode=1)

    def test_060_legal_07_du_09_target_06_rep_08_force_zero_up(self):
        self.verify("legal ――(o-o){*}", [], returncode=1)

    def test_060_legal_07_du_09_target_06_rep_09_force_one_up(self):
        self.verify("legal ――(o-o){+}", [], returncode=1)

    def test_060_legal_07_du_10_left_target_06_rep_01_zero_up(self):
        self.verify("legal e2――(o-o)*", [], returncode=1)

    def test_060_legal_07_du_10_left_target_06_rep_02_one_up(self):
        self.verify("legal e2――(o-o)+", [], returncode=1)

    def test_060_legal_07_du_10_left_target_06_rep_03_optional(self):
        self.verify("legal e2――(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_10_left_target_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2――(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_10_left_target_06_rep_05_range(self):
        self.verify("legal e2――(o-o){3,5}", [], returncode=1)

    def test_060_legal_07_du_10_left_target_06_rep_06_up_to(self):
        self.verify("legal e2――(o-o){,5}", [], returncode=1)

    def test_060_legal_07_du_10_left_target_06_rep_07_and_over(self):
        self.verify("legal e2――(o-o){3,}", [], returncode=1)

    def test_060_legal_07_du_10_left_target_06_rep_08_force_zero_up(self):
        self.verify("legal e2――(o-o){*}", [], returncode=1)

    def test_060_legal_07_du_10_left_target_06_rep_09_force_one_up(self):
        self.verify("legal e2――(o-o){+}", [], returncode=1)

    def test_060_legal_07_du_11_right_target_06_rep_01_zero_up(self):
        self.verify("legal ――Qa4(o-o)*", [], returncode=1)

    def test_060_legal_07_du_11_right_target_06_rep_02_one_up(self):
        self.verify("legal ――Qa4(o-o)+", [], returncode=1)

    def test_060_legal_07_du_11_right_target_06_rep_03_optional(self):
        self.verify("legal ――Qa4(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_11_right_target_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal ――Qa4(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_11_right_target_06_rep_05_range(self):
        self.verify("legal ――Qa4(o-o){3,5}", [], returncode=1)

    def test_060_legal_07_du_11_right_target_06_rep_06_up_to(self):
        self.verify("legal ――Qa4(o-o){,5}", [], returncode=1)

    def test_060_legal_07_du_11_right_target_06_rep_07_and_over(self):
        self.verify("legal ――Qa4(o-o){3,}", [], returncode=1)

    def test_060_legal_07_du_11_right_target_06_rep_08_force_zero_up(self):
        self.verify("legal ――Qa4(o-o){*}", [], returncode=1)

    def test_060_legal_07_du_11_right_target_06_rep_09_force_one_up(self):
        self.verify("legal ――Qa4(o-o){+}", [], returncode=1)

    def test_060_legal_07_du_12_lr_target_06_rep_01_zero_up(self):
        self.verify("legal e2――Qa4(o-o)*", [], returncode=1)

    def test_060_legal_07_du_12_lr_target_06_rep_02_one_up(self):
        self.verify("legal e2――Qa4(o-o)+", [], returncode=1)

    def test_060_legal_07_du_12_lr_target_06_rep_03_optional(self):
        self.verify("legal e2――Qa4(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_12_lr_target_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2――Qa4(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_12_lr_target_06_rep_05_range(self):
        self.verify("legal e2――Qa4(o-o){3,5}", [], returncode=1)

    def test_060_legal_07_du_12_lr_target_06_rep_06_up_to(self):
        self.verify("legal e2――Qa4(o-o){,5}", [], returncode=1)

    def test_060_legal_07_du_12_lr_target_06_rep_07_and_over(self):
        self.verify("legal e2――Qa4(o-o){3,}", [], returncode=1)

    def test_060_legal_07_du_12_lr_target_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal e2――Qa4(o-o){*}", [], returncode=1)

    def test_060_legal_07_du_12_lr_target_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal e2――Qa4(o-o){+}", [], returncode=1)

    def test_060_legal_07_du_13_prom_targ_06_rep_01_zero_up(self):
        self.verify("legal ――=q(o-o)*", [], returncode=1)

    def test_060_legal_07_du_13_prom_targ_06_rep_02_one_up(self):
        self.verify("legal ――=q(o-o)+", [], returncode=1)

    def test_060_legal_07_du_13_prom_targ_06_rep_03_optional(self):
        self.verify("legal ――=q(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_13_prom_targ_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal ――=q(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_13_prom_targ_06_rep_05_range(self):
        self.verify("legal ――=q(o-o){3,5}", [], returncode=1)

    def test_060_legal_07_du_13_prom_targ_06_rep_06_up_to(self):
        self.verify("legal ――=q(o-o){,5}", [], returncode=1)

    def test_060_legal_07_du_13_prom_targ_06_rep_07_and_over(self):
        self.verify("legal ――=q(o-o){3,}", [], returncode=1)

    def test_060_legal_07_du_13_prom_targ_06_rep_08_force_zero_up(self):
        self.verify("legal ――=q(o-o){*}", [], returncode=1)

    def test_060_legal_07_du_13_prom_targ_06_rep_09_force_one_up(self):
        self.verify("legal ――=q(o-o){+}", [], returncode=1)

    def test_060_legal_07_du_14_l_prom_targ_06_rep_01_zero_up(self):
        self.verify("legal e2――=q(o-o)*", [], returncode=1)

    def test_060_legal_07_du_14_l_prom_targ_06_rep_02_one_up(self):
        self.verify("legal e2――=q(o-o)+", [], returncode=1)

    def test_060_legal_07_du_14_l_prom_targ_06_rep_03_optional(self):
        self.verify("legal e2――=q(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_14_l_prom_targ_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2――=q(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashLI"),
                (5, "PieceDesignator"),
                (5, "AnySquare"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_14_l_prom_targ_06_rep_05_range(self):
        self.verify("legal e2――=q(o-o){3,5}", [], returncode=1)

    def test_060_legal_07_du_14_l_prom_targ_06_rep_06_up_to(self):
        self.verify("legal e2――=q(o-o){,5}", [], returncode=1)

    def test_060_legal_07_du_14_l_prom_targ_06_rep_07_and_over(self):
        self.verify("legal e2――=q(o-o){3,}", [], returncode=1)

    def test_060_legal_07_du_14_l_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal e2――=q(o-o){*}", [], returncode=1)

    def test_060_legal_07_du_14_l_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal e2――=q(o-o){+}", [], returncode=1)

    def test_060_legal_07_du_15_r_prom_targ_06_rep_01_zero_up(self):
        self.verify("legal ――Qa4=q(o-o)*", [], returncode=1)

    def test_060_legal_07_du_15_r_prom_targ_06_rep_02_one_up(self):
        self.verify("legal ――Qa4=q(o-o)+", [], returncode=1)

    def test_060_legal_07_du_15_r_prom_targ_06_rep_03_optional(self):
        self.verify("legal ――Qa4=q(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_15_r_prom_targ_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal ――Qa4=q(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashIR"),
                (5, "AnySquare"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_15_r_prom_targ_06_rep_05_range(self):
        self.verify("legal ――Qa4=q(o-o){3,5}", [], returncode=1)

    def test_060_legal_07_du_15_r_prom_targ_06_rep_06_up_to(self):
        self.verify("legal ――Qa4=q(o-o){,5}", [], returncode=1)

    def test_060_legal_07_du_15_r_prom_targ_06_rep_07_and_over(self):
        self.verify("legal ――Qa4=q(o-o){3,}", [], returncode=1)

    def test_060_legal_07_du_15_r_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal ――Qa4=q(o-o){*}", [], returncode=1)

    def test_060_legal_07_du_15_r_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal ――Qa4=q(o-o){+}", [], returncode=1)

    def test_060_legal_07_du_16_lr_prom_targ_06_rep_01_zero_up(self):
        self.verify("legal e2――Qa4=q(o-o)*", [], returncode=1)

    def test_060_legal_07_du_16_lr_prom_targ_06_rep_02_one_up(self):
        self.verify("legal e2――Qa4=q(o-o)+", [], returncode=1)

    def test_060_legal_07_du_16_lr_prom_targ_06_rep_03_optional(self):
        self.verify("legal e2――Qa4=q(o-o)?", [], returncode=1)

    # CQL-6.2 always sees pattern '{\d+}' as a repetition specification.
    def test_060_legal_07_du_16_lr_prom_targ_06_rep_04_exact(self):
        self.verify_declare_fail(
            "legal e2――Qa4=q(o-o){5}",
            [
                (3, "Legal"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (5, "TargetParenthesisLeft"),
                (6, "OO"),
                (3, "BraceLeft"),
                (4, "Integer"),
            ],
        )

    def test_060_legal_07_du_16_lr_prom_targ_06_rep_05_range(self):
        self.verify("legal e2――Qa4=q(o-o){3,5}", [], returncode=1)

    def test_060_legal_07_du_16_lr_prom_targ_06_rep_06_up_to(self):
        self.verify("legal e2――Qa4=q(o-o){,5}", [], returncode=1)

    def test_060_legal_07_du_16_lr_prom_targ_06_rep_07_and_over(self):
        self.verify("legal e2――Qa4=q(o-o){3,}", [], returncode=1)

    def test_060_legal_07_du_16_lr_prom_targ_06_rep_08_force_zero_up(
        self,
    ):
        self.verify("legal e2――Qa4=q(o-o){*}", [], returncode=1)

    def test_060_legal_07_du_16_lr_prom_targ_06_rep_09_force_one_up(
        self,
    ):
        self.verify("legal e2――Qa4=q(o-o){+}", [], returncode=1)


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterLegal))
