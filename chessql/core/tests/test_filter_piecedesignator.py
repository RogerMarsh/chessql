# test_filter_piecedesignator.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for piece designator filters.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterPieceDesignator(verify.Verify):

    def test_149_piecedsignator_01_K_ascii(self):
        self.verify("K", [(3, "PieceDesignator")])

    def test_149_piecedsignator_01_K_utf8(self):
        self.verify("♔", [(3, "PieceDesignator")])

    def test_149_piecedsignator_02_A_ascii(self):
        self.verify("A", [(3, "PieceDesignator")])

    def test_149_piecedsignator_02_A_utf8(self):
        self.verify("△", [(3, "PieceDesignator")])

    def test_149_piecedsignator_03_a_ascii(self):
        self.verify("a", [(3, "PieceDesignator")])

    def test_149_piecedsignator_03_a_utf8(self):
        self.verify("▲", [(3, "PieceDesignator")])

    def test_149_piecedsignator_04_Aa_ascii(self):
        self.verify("[Aa]", [(3, "PieceDesignator")])

    def test_149_piecedsignator_04_Aa_utf8(self):
        self.verify("◭", [(3, "PieceDesignator")])

    def test_149_piecedsignator_05_empty_ascii(self):
        self.verify("_", [(3, "PieceDesignator")])

    def test_149_piecedsignator_05_empty_utf8(self):
        self.verify("□", [(3, "PieceDesignator")])

    def test_149_piecedsignator_06_all_squares_ascii(self):
        self.verify("a-h1-8", [(3, "PieceDesignator")])

    # utf8 '▦' is textually equivalent to ascii '.' not ascii 'a-h1-8'.
    # '<piece>▦' is two set filters, not one like '<piece>a-h1-8'.
    def test_149_piecedsignator_06_all_squares_utf8(self):
        self.verify("▦", [(3, "AnySquare")])

    def test_149_piecedsignator_07_some_pieces_ascii(self):
        self.verify("[QrbNp]", [(3, "PieceDesignator")])

    def test_149_piecedsignator_07_some_pieces_utf8(self):
        self.verify("♕♜♝♘♟", [(3, "PieceDesignator")])

    def test_149_piecedsignator_08_some_pieces_some_squares_ascii_01(self):
        self.verify("[QrbNp]b-c4-5", [(3, "PieceDesignator")])

    def test_149_piecedsignator_08_some_pieces_some_squares_ascii_02(self):
        self.verify("[QrbNp][a5,b-c4-5,h1-2,e-g4]", [(3, "PieceDesignator")])

    def test_149_piecedsignator_08_some_pieces_some_squares_utf8_01(self):
        self.verify("♕♜♝♘♟b-c4-5", [(3, "PieceDesignator")])

    def test_149_piecedsignator_08_some_pieces_some_squares_utf8_02(self):
        self.verify("♕♜♝♘♟[a5,b-c4-5,h1-2,e-g4]", [(3, "PieceDesignator")])

    def test_149_piecedsignator_09_mix_ascii_utf8_pieces(self):
        self.verify("[♕♜B♘♟]", [], returncode=1)


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterPieceDesignator))
