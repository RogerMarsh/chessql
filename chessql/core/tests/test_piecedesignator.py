# piecedesignator.py
# Copyright 2020 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""piecedesignator tests for cql"""

import unittest
import re

from .. import piecedesignator


class PieceDesignator(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_PIECE_DESIGNATOR(self):
        ae = self.assertEqual
        ae(
            piecedesignator.PieceDesignator.PIECE_DESIGNATOR,
            r"".join(
                (
                    r"(?:(?:\[([a-h][-a-h1-8]*[1-8](?:,[a-h][-a-h1-8]*[1-8])*)",
                    r"\])|(?:([a-h]-[a-h][1-8]-[1-8])|([a-h]-[a-h][1-8])|",
                    r"([a-h][1-8]-[1-8])|([a-h][1-8])))|",
                    r"(?:(?:(?:(?:\[([^\]]+)\])|([KQRBNPkqrbnpAa_]))",
                    r"(?:(?:\[([a-h][-a-h1-8]*[1-8](?:,[a-h][-a-h1-8]*[1-8])*)",
                    r"\])|(?:([a-h]-[a-h][1-8]-[1-8])|([a-h]-[a-h][1-8])|",
                    r"([a-h][1-8]-[1-8])|([a-h][1-8]))))|(?:(?:\[([^\]]+)\])|",
                    r"([KQRBNPkqrbnpAa_])))",
                )
            ),
        )

    def test_02_piece_designator(self):
        ae = self.assertEqual
        ae(
            isinstance(
                piecedesignator.PieceDesignator.piece_designator, re.Pattern
            ),
            True,
        )

    def test_03_emptysquare(self):
        ae = self.assertEqual
        ae(piecedesignator.PieceDesignator.emptysquare, False)

    def test_04_PieceDesignator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator.PieceDesignator(*"abcdefghijklmn")
        ae(pd.compoundsquare, pd[0])
        ae(pd.filerankrange, pd[1])
        ae(pd.filerange, pd[2])
        ae(pd.rankrange, pd[3])
        ae(pd.square, pd[4])
        ae(pd.compoundpiece_s, pd[5])
        ae(pd.piece_s, pd[6])
        ae(pd.p_compoundsquare, pd[7])
        ae(pd.p_filerankrange, pd[8])
        ae(pd.p_filerange, pd[9])
        ae(pd.p_rankrange, pd[10])
        ae(pd.p_square, pd[11])
        ae(pd.compoundpiece, pd[12])
        ae(pd.piece, pd[13])
        ae(len(pd), 14)

        # Allow for 'count' and 'index' methods listed in dir().
        ae(
            len(
                [
                    a
                    for a in dir(
                        piecedesignator.PieceDesignator.PieceDesignator
                    )
                    if not a.startswith("_")
                ]
            )
            - 2,
            14,
        )

    def test_05_match_piece_designator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Ka5")
        ae(pd._token, "Ka5")
        ae(pd._designator_set, None)
        ae(pd._square_ranges_valid, None)
        ae(pd._match, None)
        ae(pd._groups, None)
        m = pd.piece_designator.match(pd._token)
        ae(len(m.groups()), 14)

    def test_06_parse_piece_designator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Ka5")
        pd.parse()
        ae(pd._token, "Ka5")
        ae(pd._designator_set, None)
        ae(pd._square_ranges_valid, None)
        ae(isinstance(pd._match, re.Match), True)
        ae(
            isinstance(
                pd._groups, piecedesignator.PieceDesignator.PieceDesignator
            ),
            True,
        )

    def test_07__expand_composite_square(self):
        ae = self.assertEqual
        ae(
            piecedesignator.PieceDesignator._expand_composite_square(
                "c", "g", "3", "5"
            ),
            {
                "c3",
                "c4",
                "c5",
                "d3",
                "d4",
                "d5",
                "e3",
                "e4",
                "e5",
                "f3",
                "f4",
                "f5",
                "g3",
                "g4",
                "g5",
            },
        )

    def test_08_expand_piece_designator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qa5")
        pd.parse()
        pd.expand_piece_designator()
        ae(pd.designator_set, {"Qa5"})
        ae(pd._square_ranges_valid, True)

    def test_09_expand_piece_designator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qa5-6")
        pd.parse()
        pd.expand_piece_designator()
        ae(pd.designator_set, {"Qa5", "Qa6"})
        ae(pd._square_ranges_valid, True)

    def test_10_expand_piece_designator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qa-c6")
        pd.parse()
        pd.expand_piece_designator()
        ae(pd.designator_set, {"Qa6", "Qb6", "Qc6"})
        ae(pd._square_ranges_valid, True)

    def test_11_expand_piece_designator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qa-c6-7")
        pd.parse()
        pd.expand_piece_designator()
        ae(pd.designator_set, {"Qa6", "Qb6", "Qc6", "Qa7", "Qb7", "Qc7"})
        ae(pd._square_ranges_valid, True)

    def test_12_expand_piece_designator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Q")
        pd.parse()
        pd.expand_piece_designator()
        ae(pd.designator_set, {"Q"})
        ae(pd._square_ranges_valid, True)

    def test_13_expand_piece_designator(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qc-a7-6")
        pd.parse()
        pd.expand_piece_designator()
        ae(pd.designator_set, {"Qa6"})
        ae(pd._square_ranges_valid, False)

    def test_14_get_shift_limits(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qa5")
        pd.parse()
        ae(pd.get_shift_limits(None, None), None)
        filelimits = ["h", "a"]
        ranklimits = ["8", "1"]
        ae(pd.get_shift_limits(ranklimits, filelimits), None)
        ae(filelimits, ["a", "a"])
        ae(ranklimits, ["5", "5"])

    def test_15_get_shift_limits(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qb-f5")
        pd.parse()
        filelimits = ["h", "a"]
        ranklimits = ["8", "1"]
        ae(pd.get_shift_limits(ranklimits, filelimits), None)
        ae(filelimits, ["b", "f"])
        ae(ranklimits, ["5", "5"])

    def test_16_get_shift_limits(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qc3-6")
        pd.parse()
        filelimits = ["h", "a"]
        ranklimits = ["8", "1"]
        ae(pd.get_shift_limits(ranklimits, filelimits), None)
        ae(filelimits, ["c", "c"])
        ae(ranklimits, ["3", "6"])

    def test_17_get_shift_limits(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qc-f6")
        pd.parse()
        filelimits = ["h", "a"]
        ranklimits = ["8", "1"]
        ae(pd.get_shift_limits(ranklimits, filelimits), None)
        ae(filelimits, ["c", "f"])
        ae(ranklimits, ["6", "6"])

    def test_18_get_shift_limits(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qc-f2-4")
        pd.parse()
        filelimits = ["h", "a"]
        ranklimits = ["8", "1"]
        ae(pd.get_shift_limits(ranklimits, filelimits), None)
        ae(filelimits, ["c", "f"])
        ae(ranklimits, ["2", "4"])

    def test_19_get_shift_limits(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Q[c-f2-4,b-e3-5]")
        pd.parse()
        filelimits = ["h", "a"]
        ranklimits = ["8", "1"]
        ae(pd.get_shift_limits(ranklimits, filelimits), None)
        ae(filelimits, ["b", "f"])
        ae(ranklimits, ["2", "5"])

    def test_20_get_pieces(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Qa5")
        pd.parse()
        ae(pd.get_pieces(), "Q")
        pd = piecedesignator.PieceDesignator("[RrNb]a5")
        pd.parse()
        ae(pd.get_pieces(), "RrNb")
        pd = piecedesignator.PieceDesignator("a5")
        pd.parse()
        ae(pd.get_pieces(), "Aa")
        pd = piecedesignator.PieceDesignator("_a5")
        pd.parse()
        ae(pd.get_pieces(), "_")

    def test_21_get_squares(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Q[a5,b-d6,e4-5,c-d7-8]")
        pd.parse()
        ae(pd.get_squares(), "a5,b-d6,e4-5,c-d7-8")

    def test_22_get_squares_list(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Q[a5,b-d6,e4-5,c-d7-8]")
        pd.parse()
        ae(pd.get_squares_list(), ["a5", "b-d6", "e4-5", "c-d7-8"])

    def test_23_is_compound_squares(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Q[a5,b-d6,e4-5,c-d7-8]")
        pd.parse()
        ae(pd.is_compound_squares(), True)

    def test_24_is_compound_pieces(self):
        ae = self.assertEqual
        pd = piecedesignator.PieceDesignator("Q[a5,b-d6,e4-5,c-d7-8]")
        pd.parse()
        ae(pd.is_compound_pieces(), False)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(PieceDesignator))
