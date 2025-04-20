# test_filter_path.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'path' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterPath(verify.Verify):

    def test_087_path_01_bare(self):
        self.verify("path", [], returncode=1)

    def test_087_path_02_parameter_only_01_one(self):
        self.verify("path primary", [], returncode=1)

    def test_087_path_02_parameter_only_02_all_without_arguments(self):
        self.verify(
            "".join(
                (
                    "path primary verbose keepallbest quiet nestban"
                    " firstmatch lastposition",
                )
            ),
            [],
            returncode=1,
        )

    def test_087_path_02_parameter_only_02_all(self):
        self.verify(
            "".join(
                (
                    "path primary verbose keepallbest quiet nestban"
                    ' firstmatch lastposition title "test"',
                    " focus Q piecepath max 3",
                )
            ),
            [],
            returncode=1,
        )

    def test_087_path_03_argument_01_no_parameters(self):
        self.verify("path k", [(3, "Path"), (4, "PieceDesignator")])

    def test_087_path_03_argument_02_one_parameter_01_before(self):
        self.verify(
            "path quiet k", [(3, "Path"), (4, "Quiet"), (4, "PieceDesignator")]
        )

    def test_087_path_03_argument_02_one_parameter_02_after(self):
        self.verify("path k quiet", [], returncode=1)

    def test_087_path_03_argument_03_all_parameters_without_arguments(self):
        self.verify(
            "".join(
                (
                    "path primary verbose keepallbest quiet nestban"
                    " firstmatch lastposition k",
                )
            ),
            [
                (3, "Path"),
                (4, "PrimaryParameter"),
                (4, "Verbose"),
                (4, "KeepAllBest"),
                (4, "Quiet"),
                (4, "NestBan"),
                (4, "FirstMatch"),
                (4, "LastPosition"),
                (4, "PieceDesignator"),
            ],
        )

    # CQL-6.2 says 'legal but not implemented' and gives syntax error.
    # Keyword 'primary' cannot be in same 'path' filter as 'focus'.
    def test_087_path_03_argument_04_all_parameters(self):
        self.verify_declare_fail(
            "".join(
                (
                    "path primary verbose keepallbest quiet nestban"
                    ' firstmatch lastposition title "test"',
                    " focus Q piecepath max 3 k",
                )
            ),
            [
                (3, "Path"),
                (4, "PrimaryParameter"),
                (4, "Verbose"),
                (4, "KeepAllBest"),
                (4, "Quiet"),
                (4, "NestBan"),
                (4, "FirstMatch"),
                (4, "LastPosition"),
                (4, "Title"),
                (5, "String"),
                (4, "Focus"),
                (5, "PieceDesignator"),
                (4, "PiecePath"),
                (4, "MaxParameter"),
                (5, "Integer"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_03_argument_05_all_parameters_no_focus(self):
        self.verify(
            "".join(
                (
                    "path primary verbose keepallbest quiet nestban"
                    ' firstmatch lastposition title "test"',
                    " piecepath max 3 k",
                )
            ),
            [],
            returncode=1,
        )

    def test_087_path_03_argument_06_all_parameters_no_focus_piecepath(self):
        self.verify(
            "".join(
                (
                    "path primary verbose keepallbest quiet nestban"
                    ' firstmatch lastposition title "test"',
                    " max 3 k",
                )
            ),
            [
                (3, "Path"),
                (4, "PrimaryParameter"),
                (4, "Verbose"),
                (4, "KeepAllBest"),
                (4, "Quiet"),
                (4, "NestBan"),
                (4, "FirstMatch"),
                (4, "LastPosition"),
                (4, "Title"),
                (5, "String"),
                (4, "MaxParameter"),
                (5, "Integer"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_03_argument_07_all_parameters_no_primary(self):
        self.verify(
            "".join(
                (
                    "path verbose keepallbest quiet nestban"
                    ' firstmatch lastposition title "test"',
                    " focus Q piecepath max 3 k",
                )
            ),
            [
                (3, "Path"),
                (4, "Verbose"),
                (4, "KeepAllBest"),
                (4, "Quiet"),
                (4, "NestBan"),
                (4, "FirstMatch"),
                (4, "LastPosition"),
                (4, "Title"),
                (5, "String"),
                (4, "Focus"),
                (5, "PieceDesignator"),
                (4, "PiecePath"),
                (4, "MaxParameter"),
                (5, "Integer"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_04_greekgift_01_target_syntax(self):
        self.verify(
            "B[x]h7(check k[x]h7(N--g5 check))",
            [
                (3, "TakeLR"),
                (4, "PieceDesignator"),
                (4, "PieceDesignator"),
                (4, "TargetParenthesisLeft"),
                (5, "Check"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (6, "TargetParenthesisLeft"),
                (7, "DashLR"),
                (8, "PieceDesignator"),
                (8, "PieceDesignator"),
                (7, "Check"),
            ],
        )

    def test_087_path_04_greekgift_02_path_syntax_01_ascii(self):
        self.verify(
            "path B[x]h7 check k[x]h7 N--g5 check",
            [
                (3, "Path"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "Check"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "Check"),
            ],
        )

    def test_087_path_04_greekgift_02_path_syntax_02_utf8(self):
        self.verify(
            "path ♗×h7 check ♚×h7 ♘――g5 check",
            [
                (3, "Path"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "Check"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "Check"),
            ],
        )

    def test_087_path_04_greekgift_02_path_syntax_03_utf8_promote(self):
        self.verify(
            "path ♗×h7 check ♚×h7 ♘――g5=♕ check",
            [
                (3, "Path"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "Check"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "DashLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (5, "AssignPromotion"),
                (6, "PieceDesignator"),
                (4, "Check"),
            ],
        )

    # CQL-6.2 sees 'parenthesized expression' and gives syntax error.
    def test_087_path_04_greekgift_03_path_with_target_syntax_01(self):
        self.verify_declare_fail(
            "path B[x]h7(check k[x]h7(N--g5 check))",
            [
                (3, "Path"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "ConstituentParenthesisLeft"),
                (5, "Check"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (5, "ConstituentParenthesisLeft"),
                (6, "DashLR"),
                (7, "PieceDesignator"),
                (7, "PieceDesignator"),
                (6, "Check"),
            ],
        )

    # CQL-6.2 sees 'parenthesized expression' and gives syntax error.
    def test_087_path_04_greekgift_03_path_with_target_syntax_02_promote(self):
        self.verify_declare_fail(
            "path B[x]h7(check k[x]h7(N--g5=Q check))",
            [
                (3, "Path"),
                (4, "TakeLR"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "ConstituentParenthesisLeft"),
                (5, "Check"),
                (5, "TakeLR"),
                (6, "PieceDesignator"),
                (6, "PieceDesignator"),
                (5, "ConstituentParenthesisLeft"),
                (6, "DashLR"),
                (7, "PieceDesignator"),
                (7, "PieceDesignator"),
                (7, "AssignPromotion"),
                (8, "PieceDesignator"),
                (6, "Check"),
            ],
        )

    def test_087_path_05_chain_constituent_01_no_chain_01_no_space(self):
        self.verify(
            "path-- --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_01_no_chain_02_space(self):
        self.verify(
            "path -- --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_02_chain(self):
        self.verify(
            "path (-- --)",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_03_chain_chain(self):
        self.verify(
            "path ((-- --) -- --)",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "ConstituentParenthesisLeft"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (6, "DashII"),
                (7, "AnySquare"),
                (7, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_04_piece_chain_01_no_space(self):
        self.verify(
            "path k(-- --)",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_04_piece_chain_02_space(self):
        self.verify(
            "path k ( -- -- )",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    # CQL-6.2 sees 'parenthesized expression' and gives syntax error.
    def test_087_path_05_chain_constituent_05_dash_chain_01_no_space(self):
        self.verify_declare_fail(
            "path --(-- --)",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    # CQL-6.2 sees 'parenthesized expression' and gives syntax error.
    def test_087_path_05_chain_constituent_05_dash_chain_02_space(self):
        self.verify_declare_fail(
            "path -- ( -- -- )",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_06_chain_piece_01_no_space(self):
        self.verify(
            "path (-- --)k",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_05_chain_constituent_06_chain_piece_02_space_in(self):
        self.verify(
            "path ( -- -- )k",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_05_chain_constituent_06_chain_piece_03_space_out(self):
        self.verify(
            "path (-- --) k",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_05_chain_constituent_06_chain_piece_04_all_space(self):
        self.verify(
            "path ( -- -- ) k",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_05_chain_constituent_07_chain_dash_01_no_space(self):
        self.verify(
            "path (-- --)--",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_07_chain_dash_02_space_in(self):
        self.verify(
            "path ( -- -- )--",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_07_chain_dash_03_space_out(self):
        self.verify(
            "path (-- --) --",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_05_chain_constituent_07_chain_dash_04_all_space(self):
        self.verify(
            "path ( -- -- ) --",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    # From CQL-6.2 dingstheme example.
    def test_087_path_05_chain_constituent_10_after_attack_arrow(self):
        self.verify(
            "path -- P->(.<-k)",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "AttackArrow"),
                (5, "PieceDesignator"),
                (5, "ConstituentParenthesisLeft"),
                (6, "AttackedArrow"),
                (7, "AnySquare"),
                (7, "PieceDesignator"),
            ],
        )

    # From CQL-6.2 dingstheme-simple example.
    def test_087_path_05_chain_constituent_11_after_attack_arrow_union(self):
        self.verify(
            "path -- P->(.<-k)|k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "AttackArrow"),
                (5, "PieceDesignator"),
                (5, "Union"),
                (6, "ConstituentParenthesisLeft"),
                (7, "AttackedArrow"),
                (8, "AnySquare"),
                (8, "PieceDesignator"),
                (6, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_01_piece_01_plus(self):
        self.verify("path k +", [], returncode=1)

    def test_087_path_06_regex_02_dash_01_plus(self):
        self.verify(
            "path -- +",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PlusRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_02_star(self):
        self.verify(
            "path -- *",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "StarRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_03_optional(self):
        self.verify(
            "path -- ?",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RepeatZeroOrOne"),
            ],
        )

    def test_087_path_06_regex_02_dash_04_fixed(self):
        self.verify(
            "path -- {3}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_05_range_fixed(self):
        self.verify(
            "path -- {3,7}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_06_range_open_start(self):
        self.verify(
            "path -- {,7}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_07_range_open_end(self):
        self.verify(
            "path -- {3,}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_08_force_plus(self):
        self.verify(
            "path -- {+}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardPlus"),
            ],
        )

    def test_087_path_06_regex_02_dash_09_force_star(self):
        self.verify(
            "path -- {*}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardStar"),
            ],
        )

    def test_087_path_06_regex_02_dash_10_piece_plus(self):
        self.verify(
            "path -- k +",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "PlusRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_11_piece_star(self):
        self.verify(
            "path -- k *",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "StarRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_12_piece_optional(self):
        self.verify(
            "path -- k ?",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "RepeatZeroOrOne"),
            ],
        )

    def test_087_path_06_regex_02_dash_13_piece_fixed(self):
        self.verify(
            "path -- k {3}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_14_piece_range_fixed(self):
        self.verify(
            "path -- k {3,7}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_15_piece_range_open_start(self):
        self.verify(
            "path -- k {,7}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_16_piece_range_open_end(self):
        self.verify(
            "path -- k {3,}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_17_piece_force_plus(self):
        self.verify(
            "path -- k {+}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "WildcardPlus"),
            ],
        )

    def test_087_path_06_regex_02_dash_18_piece_force_star(self):
        self.verify(
            "path -- k {*}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PieceDesignator"),
                (4, "WildcardStar"),
            ],
        )

    def test_087_path_06_regex_02_dash_19_initial_piece_plus(self):
        self.verify(
            "path k -- +",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PlusRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_20_initial_piece_star(self):
        self.verify(
            "path k -- *",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "StarRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_21_initial_piece_optional(self):
        self.verify(
            "path k -- ?",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RepeatZeroOrOne"),
            ],
        )

    def test_087_path_06_regex_02_dash_22_initial_piece_fixed(self):
        self.verify(
            "path k -- {3}",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_23_initial_piece_range_fixed(self):
        self.verify(
            "path k -- {3,7}",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_24_initial_piece_range_open_start(self):
        self.verify(
            "path k -- {,7}",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_25_initial_piece_range_open_end(self):
        self.verify(
            "path k -- {3,}",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_26_initial_piece_force_plus(self):
        self.verify(
            "path k -- {+}",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardPlus"),
            ],
        )

    def test_087_path_06_regex_02_dash_27_initial_piece_force_star(self):
        self.verify(
            "path k -- {*}",
            [
                (3, "Path"),
                (4, "PieceDesignator"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardStar"),
            ],
        )

    def test_087_path_06_regex_02_dash_28_dash_plus(self):
        self.verify(
            "path -- -- +",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PlusRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_29_dash_star(self):
        self.verify(
            "path -- -- *",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "StarRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_30_dash_optional(self):
        self.verify(
            "path -- -- ?",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RepeatZeroOrOne"),
            ],
        )

    def test_087_path_06_regex_02_dash_31_dash_fixed(self):
        self.verify(
            "path -- -- {3}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_32_dash_range_fixed(self):
        self.verify(
            "path -- -- {3,7}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_33_dash_range_open_start(self):
        self.verify(
            "path -- -- {,7}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_34_dash_range_open_end(self):
        self.verify(
            "path -- -- {3,}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_35_dash_force_plus(self):
        self.verify(
            "path -- -- {+}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardPlus"),
            ],
        )

    def test_087_path_06_regex_02_dash_36_dash_force_star(self):
        self.verify(
            "path -- -- {*}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardStar"),
            ],
        )

    def test_087_path_06_regex_02_dash_37_compound_range_open_end(self):
        self.verify(
            "path -- {B R} {10,}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "BraceLeft"),
                (5, "PieceDesignator"),
                (5, "PieceDesignator"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_38_compound_dash_target_open(self):
        self.verify(
            "path -- {B --(R)} {10,}",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "BraceLeft"),
                (5, "PieceDesignator"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (6, "TargetParenthesisLeft"),
                (7, "PieceDesignator"),
                (4, "RegexRepeat"),
            ],
        )

    def test_087_path_06_regex_02_dash_37_final_piece_plus(self):
        self.verify(
            "path -- + k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PlusRepeat"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_38_final_piece_star(self):
        self.verify(
            "path -- * k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "StarRepeat"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_39_final_piece_optional(self):
        self.verify(
            "path -- ? k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RepeatZeroOrOne"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_40_final_piece_fixed(self):
        self.verify(
            "path -- {3} k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_41_final_piece_range_fixed(self):
        self.verify(
            "path -- {3,7} k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_42_final_piece_range_open_start(self):
        self.verify(
            "path -- {,7} k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_43_final_piece_range_open_end(self):
        self.verify(
            "path -- {3,} k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_44_final_piece_force_plus(self):
        self.verify(
            "path -- {+} k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardPlus"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_45_final_piece_force_star(self):
        self.verify(
            "path -- {*} k",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardStar"),
                (4, "PieceDesignator"),
            ],
        )

    def test_087_path_06_regex_02_dash_46_final_dash_plus(self):
        self.verify(
            "path -- + --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "PlusRepeat"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_02_dash_47_final_dash_star(self):
        self.verify(
            "path -- * --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "StarRepeat"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_02_dash_48_final_dash_optional(self):
        self.verify(
            "path -- ? --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RepeatZeroOrOne"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_02_dash_49_final_dash_fixed(self):
        self.verify(
            "path -- {3} --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_02_dash_50_final_dash_range_fixed(self):
        self.verify(
            "path -- {3,7} --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_02_dash_51_final_dash_range_open_start(self):
        self.verify(
            "path -- {,7} --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_02_dash_52_final_dash_range_open_end(self):
        self.verify(
            "path -- {3,} --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "RegexRepeat"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_02_dash_53_final_dash_force_plus(self):
        self.verify(
            "path -- {+} --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardPlus"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_02_dash_54_final_dash_force_star(self):
        self.verify(
            "path -- {*} --",
            [
                (3, "Path"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
                (4, "WildcardStar"),
                (4, "DashII"),
                (5, "AnySquare"),
                (5, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_03_chain_constituents_01_flat_internal(self):
        self.verify(
            "path (-- -- --) (-- -- --)+ (-- -- --)* (-- -- --)",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "PlusRepeat"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "StarRepeat"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )

    def test_087_path_06_regex_03_chain_constituents_02_repeat_internal(self):
        self.verify(
            "path (-- --? --) (-- --? --)+ (-- -- --)* (-- -- --)",
            [
                (3, "Path"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "RepeatZeroOrOne"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "RepeatZeroOrOne"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "PlusRepeat"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (4, "StarRepeat"),
                (4, "ConstituentParenthesisLeft"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
                (5, "DashII"),
                (6, "AnySquare"),
                (6, "AnySquare"),
            ],
        )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterPath))
