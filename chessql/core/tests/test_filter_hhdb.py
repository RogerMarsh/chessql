# test_filter_hhdb.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for the 'hhdb' filters.

The verification methods are provided by the Verify superclass.
"""

import unittest
import shlex
import subprocess
import re

from .. import hhdb

# An input file must be specified, but need not exist, with '-parse' option.
_CQL_PREFIX = "cql -input xxxx.pgn -parse -cql "
_CQL_PREFIX_VARIATIONS = "cql -input xxxx.pgn -parse -variations -cql "

_hhdb_re = re.compile(hhdb.HHDB)


class HHDB(unittest.TestCase):

    def verify(self, string, returncode=0):
        """Verify string produces returncode from CQL run.

        Run 'cql' in a subprocess to verify the string is accepted by cql.

        """
        process = subprocess.run(
            shlex.split(_CQL_PREFIX) + [string],
            stdout=subprocess.DEVNULL,
        )
        self.assertEqual(process.returncode, returncode)
        if returncode != 0:
            self.assertEqual(_hhdb_re.match(string) is None, True)
            return
        self.assertEqual(isinstance(_hhdb_re.match(string), re.Match), True)

    def verify_variations(self, string, returncode=0):
        """Verify string produces returncode from CQL run.

        Run 'cql' in a subprocess to verify the string is accepted by cql.

        """
        process = subprocess.run(
            shlex.split(_CQL_PREFIX_VARIATIONS) + [string],
            stdout=subprocess.DEVNULL,
        )
        self.assertEqual(process.returncode, returncode)
        if returncode != 0:
            self.assertEqual(_hhdb_re.match(string) is None, True)
            return
        self.assertEqual(isinstance(_hhdb_re.match(string), re.Match), True)

    def test_hhdb_01_bare(self):
        self.verify("hhdb", returncode=1)

    def test_hhdb_02_unknown_hhdb_keyword(self):
        self.verify("hhdb unknown", returncode=1)

    def test_hhdb_03_cook(self):
        self.verify('hhdb "<cook>"')

    def test_hhdb_04_eg(self):
        self.verify('hhdb "<eg>"')

    def test_hhdb_05_main(self):
        self.verify_variations('hhdb "<main>"')

    def test_hhdb_06_minor_dual(self):
        self.verify('hhdb "<minor_dual>"')

    def test_hhdb_07_or(self):
        self.verify_variations('hhdb "<or>"')

    def test_hhdb_08_mainline(self):
        self.verify_variations("hhdb mainline")

    def test_hhdb_09_variation(self):
        self.verify_variations("hhdb variation")

    def test_hhdb_10_cooked(self):
        self.verify("hhdb cooked")

    def test_hhdb_11_dual(self):
        self.verify("hhdb dual")

    def test_hhdb_12_sound(self):
        self.verify("hhdb sound")

    def test_hhdb_13_unsound(self):
        self.verify("hhdb unsound")

    def test_hhdb_14_correction_01(self):
        self.verify('hhdb "(c)"')

    def test_hhdb_14_correction_02(self):
        self.verify("hhdb correction")

    def test_hhdb_15_modification_01(self):
        self.verify('hhdb "(m)"')

    def test_hhdb_15_modification_02(self):
        self.verify("hhdb modification")

    def test_hhdb_16_corrected_solution_01(self):
        self.verify('hhdb "(s)"')

    def test_hhdb_16_corrected_solution_02(self):
        self.verify("hhdb corrected_solution")

    def test_hhdb_17_version_01(self):
        self.verify('hhdb "(v)"')

    def test_hhdb_17_version_02(self):
        self.verify("hhdb version")

    def test_hhdb_18_anticipation_01(self):
        self.verify("hhdb AN")

    def test_hhdb_18_anticipation_02(self):
        self.verify("hhdb anticipation")

    def test_hhdb_19_colors_reversed_01(self):
        self.verify("hhdb CR")

    def test_hhdb_19_colors_reversed_02(self):
        self.verify("hhdb colors_reversed")

    def test_hhdb_20_too_many_composers_01(self):
        self.verify("hhdb MC")

    def test_hhdb_20_too_many_composers_02(self):
        self.verify("hhdb too_many_composers")

    def test_hhdb_21_posthumous_01(self):
        self.verify("hhdb PH")

    def test_hhdb_21_posthumous_02(self):
        self.verify("hhdb posthumous")

    def test_hhdb_22_theoretical_ending_01(self):
        self.verify("hhdb TE")

    def test_hhdb_22_theoretical_ending_02(self):
        self.verify("hhdb theoretical_ending")

    def test_hhdb_23_theme_tourney_01(self):
        self.verify("hhdb TT")

    def test_hhdb_23_theme_tourney_02(self):
        self.verify("hhdb theme_tourney")

    def test_hhdb_23_theme_tourney_03(self):
        self.verify("hhdb theme_tournament")

    def test_hhdb_24_twin_01(self):
        self.verify("hhdb TW")

    def test_hhdb_24_twin_02(self):
        self.verify("hhdb twin")

    def test_hhdb_25_dual_at_move_1_01(self):
        self.verify("hhdb U1")

    def test_hhdb_25_dual_at_move_1_02(self):
        self.verify("hhdb dual_at_move_1")

    def test_hhdb_26_dual_after_move_1_01(self):
        self.verify("hhdb U2")

    def test_hhdb_26_dual_after_move_1_02(self):
        self.verify("hhdb dual_after_move_1")

    def test_hhdb_27_white_fails_01(self):
        self.verify("hhdb U3")

    def test_hhdb_27_white_fails_02(self):
        self.verify("hhdb white_fails")

    def test_hhdb_28_white_wins_in_draw_01(self):
        self.verify("hhdb U4")

    def test_hhdb_28_white_wins_in_draw_02(self):
        self.verify("hhdb white_wins_in_draw")

    def test_hhdb_29_unreachable_01(self):
        self.verify("hhdb U5")

    def test_hhdb_29_unreachable_02(self):
        self.verify("hhdb unreachable")

    def test_hhdb_30_egdiagram(self):
        self.verify("hhdb egdiagram")

    def test_hhdb_31_composer(self):
        self.verify("hhdb composer")

    def test_hhdb_32_diagram(self):
        self.verify("hhdb diagram")

    def test_hhdb_33_firstcomment(self):
        self.verify("hhdb firstcomment")

    def test_hhdb_34_gbr(self):
        self.verify("hhdb gbr")

    def test_hhdb_35_gbr_kings(self):
        self.verify("hhdb gbr kings")

    def test_hhdb_36_gbr_material(self):
        self.verify("hhdb gbr material")

    def test_hhdb_37_gbr_pawns(self):
        self.verify("hhdb gbr pawns")

    def test_hhdb_38_gbr_pieces(self):
        self.verify("hhdb gbr pieces")

    def test_hhdb_39_search(self):
        self.verify("hhdb search")

    def test_hhdb_40_stipulation(self):
        self.verify("hhdb stipulation")

    def test_hhdb_41_award_01_sort_award_special_09(self):
        self.verify("hhdb max award special")

    def test_hhdb_41_award_01_sort_award_special_11(self):
        self.verify("hhdb max commendation special")

    def test_hhdb_41_award_01_sort_award_special_13(self):
        self.verify("hhdb max hm special")

    def test_hhdb_41_award_01_sort_award_special_15(self):
        self.verify("hhdb max prize special")

    def test_hhdb_41_award_01_sort_award_special_17(self):
        self.verify("hhdb sort award special")

    def test_hhdb_41_award_01_sort_award_special_19(self):
        self.verify("hhdb sort commendation special")

    def test_hhdb_41_award_01_sort_award_special_21(self):
        self.verify("hhdb sort hm special")

    def test_hhdb_41_award_01_sort_award_special_23(self):
        self.verify("hhdb sort prize special")

    def test_hhdb_41_award_02_sort_special_award_09(self):
        self.verify("hhdb max special award")

    def test_hhdb_41_award_02_sort_special_award_10(self):
        self.verify("hhdb max special commendation")

    def test_hhdb_41_award_02_sort_special_award_11(self):
        self.verify("hhdb max special hm")

    def test_hhdb_41_award_02_sort_special_award_12(self):
        self.verify("hhdb max special prize")

    def test_hhdb_41_award_02_sort_special_award_17(self):
        self.verify("hhdb sort special award")

    def test_hhdb_41_award_02_sort_special_award_18(self):
        self.verify("hhdb sort special commendation")

    def test_hhdb_41_award_02_sort_special_award_19(self):
        self.verify("hhdb sort special hm")

    def test_hhdb_41_award_02_sort_special_award_20(self):
        self.verify("hhdb sort special prize")

    def test_hhdb_41_award_03_special_award_sort_02(self):
        self.verify("hhdb special award max")

    def test_hhdb_41_award_03_special_award_sort_04(self):
        self.verify("hhdb special commendation max")

    def test_hhdb_41_award_03_special_award_sort_06(self):
        self.verify("hhdb special hm max")

    def test_hhdb_41_award_03_special_award_sort_08(self):
        self.verify("hhdb special prize max")

    def test_hhdb_41_award_04_special_sort_award_01(self):
        self.verify("hhdb special sort award")

    def test_hhdb_41_award_04_special_sort_award_02(self):
        self.verify("hhdb special sort commendation")

    def test_hhdb_41_award_04_special_sort_award_03(self):
        self.verify("hhdb special sort hm")

    def test_hhdb_41_award_04_special_sort_award_04(self):
        self.verify("hhdb special sort prize")

    def test_hhdb_41_award_04_special_sort_award_05(self):
        self.verify("hhdb special max award")

    def test_hhdb_41_award_04_special_sort_award_06(self):
        self.verify("hhdb special max commendation")

    def test_hhdb_41_award_04_special_sort_award_07(self):
        self.verify("hhdb special max hm")

    def test_hhdb_41_award_04_special_sort_award_08(self):
        self.verify("hhdb special max prize")

    def test_hhdb_41_award_05_award_special_sort_02(self):
        self.verify("hhdb award special max")

    def test_hhdb_41_award_05_award_special_sort_06(self):
        self.verify("hhdb commendation special max")

    def test_hhdb_41_award_05_award_special_sort_10(self):
        self.verify("hhdb hm special max")

    def test_hhdb_41_award_05_award_special_sort_14(self):
        self.verify("hhdb prize special max")

    def test_hhdb_41_award_06_award_sort_special_01(self):
        self.verify("hhdb award sort special")

    def test_hhdb_41_award_06_award_sort_special_03(self):
        self.verify("hhdb award max special")

    def test_hhdb_41_award_06_award_sort_special_05(self):
        self.verify("hhdb commendation sort special")

    def test_hhdb_41_award_06_award_sort_special_07(self):
        self.verify("hhdb commendation max special")

    def test_hhdb_41_award_06_award_sort_special_09(self):
        self.verify("hhdb hm sort special")

    def test_hhdb_41_award_06_award_sort_special_11(self):
        self.verify("hhdb hm max special")

    def test_hhdb_41_award_06_award_sort_special_13(self):
        self.verify("hhdb prize sort special")

    def test_hhdb_41_award_06_award_sort_special_15(self):
        self.verify("hhdb prize max special")

    def test_hhdb_41_award_07_sort_award_05(self):
        self.verify("hhdb max award")

    def test_hhdb_41_award_07_sort_award_06(self):
        self.verify("hhdb max commendation")

    def test_hhdb_41_award_07_sort_award_07(self):
        self.verify("hhdb max hm")

    def test_hhdb_41_award_07_sort_award_08(self):
        self.verify("hhdb max prize")

    def test_hhdb_41_award_07_sort_award_09(self):
        self.verify("hhdb sort award")

    def test_hhdb_41_award_07_sort_award_10(self):
        self.verify("hhdb sort commendation")

    def test_hhdb_41_award_07_sort_award_11(self):
        self.verify("hhdb sort hm")

    def test_hhdb_41_award_07_sort_award_12(self):
        self.verify("hhdb sort prize")

    def test_hhdb_41_award_08_special_award_01(self):
        self.verify("hhdb special award")

    def test_hhdb_41_award_08_special_award_03(self):
        self.verify("hhdb special commendation")

    def test_hhdb_41_award_08_special_award_05(self):
        self.verify("hhdb special hm")

    def test_hhdb_41_award_08_special_award_07(self):
        self.verify("hhdb special prize")

    def test_hhdb_41_award_09_award_sort_02(self):
        self.verify("hhdb award max")

    def test_hhdb_41_award_09_award_sort_04(self):
        self.verify("hhdb commendation max")

    def test_hhdb_41_award_09_award_sort_06(self):
        self.verify("hhdb hm max")

    def test_hhdb_41_award_09_award_sort_08(self):
        self.verify("hhdb prize max")

    def test_hhdb_41_award_10_award_special_01(self):
        self.verify("hhdb award special")

    def test_hhdb_41_award_10_award_special_03(self):
        self.verify("hhdb commendation special")

    def test_hhdb_41_award_10_award_special_05(self):
        self.verify("hhdb hm special")

    def test_hhdb_41_award_10_award_special_07(self):
        self.verify("hhdb prize special")

    def test_hhdb_41_award_11_sort_special_02(self):
        self.verify("hhdb max special")

    def test_hhdb_41_award_11_sort_special_03(self):
        self.verify("hhdb sort special")

    def test_hhdb_41_award_12_special_sort_02(self):
        self.verify("hhdb special max")

    def test_hhdb_41_award_13_award_01(self):
        self.verify("hhdb award")

    def test_hhdb_41_award_13_award_02(self):
        self.verify("hhdb commendation")

    def test_hhdb_41_award_13_award_03(self):
        self.verify("hhdb hm")

    def test_hhdb_41_award_13_award_04(self):
        self.verify("hhdb prize")

    def test_hhdb_41_award_14_special_01(self):
        self.verify("hhdb special")

    def test_hhdb_41_award_15_special_01(self):
        self.verify("hhdb sort", returncode=1)


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(HHDB))
