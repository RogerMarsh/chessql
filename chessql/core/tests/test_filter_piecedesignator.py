# test_filter_piecedesignator.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for piece designator filter.

Piece designators get used in many tests where it is assumed detection
of piece designators just works.  In those tests the simplest piece
designator patterns are used even if the example is therefore not
realistic.

The tests in this module try examples of all patterns expected to produce
a single filter representing a piece designator.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify

# The expand_composite_square() tests do not go through verify module.
from .. import parser


class FilterPieceDesignator(verify.Verify):

    def test_220_piece_designator_01_all_piece_identities(self):
        """All singular piece identities are valid piece designators."""
        for piece in "AKQRBNPakqrbnp_▲△□♚♛♜♝♞♟♔♕♖♗♘♙":
            with self.subTest(piece=piece):
                self.verify(piece, [(3, "PieceDesignator")])

    def test_220_piece_designator_02_all_squares(self):
        """All square names are valid piece designators."""
        for file in "abcdefgh":
            for rank in "12345678":
                with self.subTest(file=file, rank=rank):
                    self.verify(file + rank, [(3, "PieceDesignator")])

    def test_220_piece_designator_03_all_pieces(self):
        """'all pieces' symbols are valid piece designators."""
        for allpieces in ("[Aa]", "◭"):
            with self.subTest(allpieces=allpieces):
                self.verify(allpieces, [(3, "PieceDesignator")])

    def test_220_piece_designator_04_all_piece_locations(self):
        """All single piece location symbols are valid piece designators."""
        for piece in "AKQRBNPakqrbnp_▲△□♚♛♜♝♞♟♔♕♖♗♘♙":
            for file in "abcdefgh":
                for rank in "12345678":
                    with self.subTest(piece=piece, file=file, rank=rank):
                        self.verify(
                            piece + file + rank, [(3, "PieceDesignator")]
                        )

    def test_220_piece_designator_05_sample_compound_pieces_ascii(self):
        """ASCII compound pieces are valid piece designators."""
        for piece in (
            "AKQRBNPakqrbnp_",
            "A_",
            "a_",
            "KQRBN",
            "kqrbn",
            "KRNkrn",
            "KQkr_",
            "B_",
            "b_",
            "N",
            "p",
        ):
            with self.subTest(piece=piece):
                self.verify(piece.join("[]"), [(3, "PieceDesignator")])

    def test_220_piece_designator_06_sample_compound_pieces_utf8(self):
        """UTF8 compound pieces are valid piece designators."""
        for piece in (
            "▲△□♚♛♜♝♞♟♔♕♖♗♘♙",
            "△□",
            "▲□",
            "♔♕♖♗♘",
            "♚♛♜♝♞",
            "♚♜♞♔♖♘",
            "□♚♜♔♕",
            "□♗",
            "□♝",
            "♘",
            "♟",
        ):
            with self.subTest(piece=piece):
                self.verify(piece, [(3, "PieceDesignator")])

    def test_220_piece_designator_07_all_square_ranges(self):
        """All single square range symbols are valid piece designators."""
        files = "abcdefgh"
        ranks = "12345678"
        for ef1, file1 in enumerate(files):
            for file2 in files[ef1:]:
                for er1, rank1 in enumerate(ranks):
                    for rank2 in ranks[er1:]:
                        if file1 == file2 and rank1 == rank2:
                            continue  # see *_02_all_squares test.
                        if file1 == file2:
                            square_range = file1 + "-".join(rank1 + rank2)
                        elif rank1 == rank2:
                            square_range = "-".join(file1 + file2) + rank1
                        else:
                            square_range = "".join(
                                (
                                    "-".join(file1 + file2),
                                    "-".join(rank1 + rank2),
                                )
                            )
                        with self.subTest(square_range=square_range):
                            self.verify(square_range, [(3, "PieceDesignator")])

    def test_220_piece_designator_08_sample_compound_squares(self):
        """Compound squares are valid piece designators."""
        for compound_square in (
            "[b2,c3-4,d-e5,f-g6-7]",
            "[a1,h1,a8,h8]",
            "[a1-8,a-h1,a-h8,h1-8]",
            "[a-h1-8,c-f3-6]",
        ):
            with self.subTest(compound_square=compound_square):
                self.verify(compound_square, [(3, "PieceDesignator")])

    def test_220_piece_designator_09_sample_compound_piece_square_ascii(self):
        """Compound piece designators are valid piece designators."""
        for piece in (
            "AKQRBNPakqrbnp_",
            "A_",
            "a_",
            "KQRBN",
            "kqrbn",
            "KRNkrn",
            "KQkr_",
            "B_",
            "b_",
            "N",
            "p",
        ):
            for compound_square in (
                "[b2,c3-4,d-e5,f-g6-7]",
                "[a1,h1,a8,h8]",
                "[a1-8,a-h1,a-h8,h1-8]",
                "[a-h1-8,c-f3-6]",
            ):
                with self.subTest(compound_square=compound_square):
                    self.verify(
                        "".join((piece.join("[]"), compound_square)),
                        [(3, "PieceDesignator")],
                    )

    def test_220_piece_designator_10_sample_compound_piece_square_utf8(self):
        """Compound piece designators are valid piece designators."""
        for piece in (
            "▲△□♚♛♜♝♞♟♔♕♖♗♘♙",
            "△□",
            "▲□",
            "♔♕♖♗♘",
            "♚♛♜♝♞",
            "♚♜♞♔♖♘",
            "□♚♜♔♕",
            "□♗",
            "□♝",
            "♘",
            "♟",
        ):
            for compound_square in (
                "[b2,c3-4,d-e5,f-g6-7]",
                "[a1,h1,a8,h8]",
                "[a1-8,a-h1,a-h8,h1-8]",
                "[a-h1-8,c-f3-6]",
            ):
                with self.subTest(compound_square=compound_square):
                    self.verify(
                        "".join((piece, compound_square)),
                        [(3, "PieceDesignator")],
                    )

    def test_220_piece_designator_11_bad_file_or_rank_range(self):
        """File and rank ranges like 'g-e' and '5-1' are not allowed."""
        for designator in ("h4-2", "h-a2", "[e2,g-f1]", "[b6-3,d7]"):
            with self.subTest(designator=designator):
                self.verify(designator, [], returncode=1)

    def test_220_piece_designator_14_expand_composite_square_01_none(self):
        con = parser.parse("cql()" + "_")
        node = con.children[-1].children[-1]
        self.assertRaisesRegex(
            TypeError,
            "".join(
                (
                    r"PieceDesignator.expand_composite_square\(\) ",
                    r"missing 4 required positional arguments: ",
                    r"'startfile', 'endfile', 'startrank', and 'endrank'$",
                )
            ),
            node.expand_composite_square,
            *(),
        )

    def test_220_piece_designator_14_expand_composite_square_02_bad(self):
        """Reject file and rank ranges outside 'a-h' and '1-8'."""
        con = parser.parse("cql()" + "_")
        node = con.children[-1].children[-1]
        for arguments in (
            ("z", "h", "1", "8"),
            ("a", "4", "1", "8"),
            ("a", "h", "0", "8"),
            ("a", "1", "1", "a"),
        ):
            with self.subTest(arguments=arguments):
                self.assertRaisesRegex(
                    ValueError,
                    "substring not found$",
                    node.expand_composite_square,
                    *arguments,
                )

    def test_220_piece_designator_14_expand_composite_square_03_order(self):
        """File and rank ranges like 'g-e' and '5-1' are not allowed."""
        con = parser.parse("cql()" + "_")
        node = con.children[-1].children[-1]
        for arguments, answer in (
            (("h", "a", "1", "8"), set()),
            (("a", "h", "8", "1"), set()),
        ):
            with self.subTest(arguments=arguments, answer=answer):
                self.assertEqual(
                    node.expand_composite_square(*arguments), answer
                )

    def test_220_piece_designator_14_expand_composite_square_04_good(self):
        """Expand a selection of acceptable square ranges."""
        con = parser.parse("cql()" + "_")
        node = con.children[-1].children[-1]
        for arguments, answer in (
            (
                ("a", "h", "1", "8"),
                set(
                    ("a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8")
                    + ("b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8")
                    + ("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8")
                    + ("d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8")
                    + ("e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8")
                    + ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8")
                    + ("g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8")
                    + ("h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8")
                ),
            ),
            (("c", "d", "4", "6"), set(["c4", "c5", "c6", "d4", "d5", "d6"])),
            (
                ("f", "f", "1", "8"),
                set(["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"]),
            ),
            (
                ("a", "h", "7", "7"),
                set(["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]),
            ),
            (("b", "b", "7", "7"), set(["b7"])),
        ):
            with self.subTest(arguments=arguments):
                self.assertEqual(
                    node.expand_composite_square(*arguments), answer
                )


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FilterPieceDesignator))
