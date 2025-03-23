# test_hhdb.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Unittests for chessql.core.elements module.

Verify the values of constant attributes defined in ..elements module.
Changes in ..elements not done here too will be highlighted.
"""

import unittest

from .. import hhdb


class HHDB(unittest.TestCase):

    def test_001_attributes(self):
        self.assertEqual(
            [a for a in sorted(dir(hhdb)) if a.isupper()],
            [
                "ANTICIPATION",
                "AWARD",
                "COLORS_REVERSED",
                "COMMENDATION",
                "COMPOSER",
                "COOK",
                "COOKED",
                "CORRECTED_SOLUTION",
                "CORRECTION",
                "DIAGRAM",
                "DUAL",
                "DUAL_AFTER_MOVE_1",
                "DUAL_AT_MOVE_1",
                "EG",
                "EGDIAGRAM",
                "FIRSTCOMMENT",
                "GBR",
                "GBR_KINGS",
                "GBR_MATERIAL",
                "GBR_PAWNS",
                "GBR_PIECES",
                "HHDB",
                "HM",
                "MAIN",
                "MAINLINE",
                "MAX",
                "MINOR_DUAL",
                "MODIFICATION",
                "OR",
                "POSTHUMOUS",
                "PRIZE",
                "SEARCH",
                "SORT",
                "SOUND",
                "SPECIAL",
                "STIPULATION",
                "THEME_TOURNEY",
                "THEORETICAL_ENDING",
                "TOO_MANY_COMPOSERS",
                "TWIN",
                "UNREACHABLE",
                "UNSOUND",
                "VARIATION",
                "VERSION",
                "WHITE_FAILS",
                "WHITE_WINS_IN_DRAW",
                "_AWARD_KEYWORDS",
                "_HHDB_KEYWORDS",
            ],
        )

    def test_002_cook(self):
        self.assertEqual(hhdb.COOK, r'"<cook>"')

    def test_003_eg(self):
        self.assertEqual(hhdb.EG, r'"<eg>"')

    def test_004_main(self):
        self.assertEqual(hhdb.MAIN, r'"<main>"')

    def test_005_minor_dual(self):
        self.assertEqual(hhdb.MINOR_DUAL, r'"<minor_dual>"')

    def test_006_or(self):
        self.assertEqual(hhdb.OR, r'"<or>"')

    def test_007_mainline(self):
        self.assertEqual(hhdb.MAINLINE, r"mainline")

    def test_008_variation(self):
        self.assertEqual(hhdb.VARIATION, r"variation")

    def test_009_cooked(self):
        self.assertEqual(hhdb.COOKED, r"cooked")

    def test_010_dual(self):
        self.assertEqual(hhdb.DUAL, r"dual")

    def test_011_sound(self):
        self.assertEqual(hhdb.SOUND, r"sound")

    def test_012_unsound(self):
        self.assertEqual(hhdb.UNSOUND, r"unsound")

    def test_013_correction(self):
        self.assertEqual(hhdb.CORRECTION, r'"\(c\)"|correction')

    def test_014_modification(self):
        self.assertEqual(hhdb.MODIFICATION, r'"\(m\)"|modification')

    def test_015_corrected_solution(self):
        self.assertEqual(
            hhdb.CORRECTED_SOLUTION, r'"\(s\)"|corrected_solution'
        )

    def test_016_version(self):
        self.assertEqual(hhdb.VERSION, r'"\(v\)"|version')

    def test_017_anticipation(self):
        self.assertEqual(hhdb.ANTICIPATION, r"AN|anticipation")

    def test_018_colors_reversed(self):
        self.assertEqual(hhdb.COLORS_REVERSED, r"CR|colors_reversed")

    def test_019_too_many_composers(self):
        self.assertEqual(hhdb.TOO_MANY_COMPOSERS, r"MC|too_many_composers")

    def test_020_posthumous(self):
        self.assertEqual(hhdb.POSTHUMOUS, r"PH|posthumous")

    def test_021_theoretical_ending(self):
        self.assertEqual(hhdb.THEORETICAL_ENDING, r"TE|theoretical_ending")

    def test_022_theme_tourney(self):
        self.assertEqual(
            hhdb.THEME_TOURNEY, r"TT|theme_tourney|theme_tournament"
        )

    def test_023_twin(self):
        self.assertEqual(hhdb.TWIN, r"TW|twin")

    def test_024_dual_at_move_1(self):
        self.assertEqual(hhdb.DUAL_AT_MOVE_1, r"U1|dual_at_move_1")

    def test_025_dual_after_move_1(self):
        self.assertEqual(hhdb.DUAL_AFTER_MOVE_1, r"U2|dual_after_move_1")

    def test_026_white_fails(self):
        self.assertEqual(hhdb.WHITE_FAILS, r"U3|white_fails")

    def test_027_white_wins_in_draw(self):
        self.assertEqual(hhdb.WHITE_WINS_IN_DRAW, r"U4|white_wins_in_draw")

    def test_028_unreachable(self):
        self.assertEqual(hhdb.UNREACHABLE, r"U5|unreachable")

    def test_029_egdiagram(self):
        self.assertEqual(hhdb.EGDIAGRAM, r"egdiagram")

    def test_030_composer(self):
        self.assertEqual(hhdb.COMPOSER, r"composer")

    def test_031_diagram(self):
        self.assertEqual(hhdb.DIAGRAM, r"diagram")

    def test_032_firstcomment(self):
        self.assertEqual(hhdb.FIRSTCOMMENT, r"firstcomment")

    def test_033_gbr(self):
        self.assertEqual(hhdb.GBR, r"gbr")

    def test_034_gbr_kings(self):
        self.assertEqual(hhdb.GBR_KINGS, r"gbr\s+kings")

    def test_035_gbr_material(self):
        self.assertEqual(hhdb.GBR_MATERIAL, r"gbr\s+material")

    def test_036_gbr_pawns(self):
        self.assertEqual(hhdb.GBR_PAWNS, r"gbr\s+pawns")

    def test_037_gbr_pieces(self):
        self.assertEqual(hhdb.GBR_PIECES, r"gbr\s+pieces")

    def test_038_search(self):
        self.assertEqual(hhdb.SEARCH, r"search")

    def test_039_stipulation(self):
        self.assertEqual(hhdb.STIPULATION, r"stipulation")

    def test_040_max(self):
        self.assertEqual(hhdb.MAX, r"max")

    def test_041_sort(self):
        self.assertEqual(hhdb.SORT, r"sort")

    def test_042_award(self):
        self.assertEqual(hhdb.AWARD, r"award")

    def test_043_commendation(self):
        self.assertEqual(hhdb.COMMENDATION, r"commendation")

    def test_044_hm(self):
        self.assertEqual(hhdb.HM, r"hm")

    def test_045_prize(self):
        self.assertEqual(hhdb.PRIZE, r"prize")

    def test_046_special(self):
        self.assertEqual(hhdb.SPECIAL, r"special")

    def test_047_hhdb(self):
        self.assertEqual(
            hhdb.HHDB,
            "".join(
                (
                    r"(?P<hhdb>)hhdb",
                    r'\s+(?:"<cook>"',
                    r'|"<eg>"|"<main>"|"<minor_dual>"|"<or>"|mainline',
                    r"|variation|cooked|dual|sound|unsound",
                    r'|"\(c\)"|correction|"\(m\)"|modification',
                    r'|"\(s\)"|corrected_solution|"\(v\)"|version',
                    r"|AN|anticipation|CR|colors_reversed",
                    r"|MC|too_many_composers|PH|posthumous",
                    r"|TE|theoretical_ending",
                    r"|TT|theme_tourney|theme_tournament|TW|twin",
                    r"|U1|dual_at_move_1|U2|dual_after_move_1",
                    r"|U3|white_fails|U4|white_wins_in_draw",
                    r"|U5|unreachable|egdiagram|composer|diagram",
                    r"|firstcomment|gbr\s+kings|gbr\s+material|gbr\s+pawns",
                    r"|gbr\s+pieces|gbr|search|stipulation",
                    r"|(?:(?:(?:max|sort)\s+(?:award|commendation|hm|prize)",
                    r"\s+(?:special))|(?:(?:max|sort)\s+(?:special)",
                    r"\s+(?:award|commendation|hm|prize))",
                    r"|(?:(?:special)\s+(?:award|commendation|hm|prize)",
                    r"\s+(?:max))|(?:(?:special)\s+(?:max|sort)",
                    r"\s+(?:award|commendation|hm|prize))",
                    r"|(?:(?:award|commendation|hm|prize)",
                    r"\s+(?:special)\s+(?:max))",
                    r"|(?:(?:award|commendation|hm|prize)\s+",
                    r"(?:max|sort)\s+(?:special))|(?:(?:max|sort)\s+",
                    r"(?:award|commendation|hm|prize))|(?:(?:special)\s+",
                    r"(?:award|commendation|hm|prize))",
                    r"|(?:(?:award|commendation|hm|prize)\s+",
                    r"(?:max))|(?:(?:award|commendation|hm|prize)\s+",
                    r"(?:special))|(?:(?:max|sort)\s+(?:special))",
                    r"|(?:(?:special)\s+(?:max))",
                    r"|(?:award|commendation|hm|prize)|(?:special)|(?:max)))",
                    r"(?![\w$])",
                )
            ),
        )


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(HHDB))
