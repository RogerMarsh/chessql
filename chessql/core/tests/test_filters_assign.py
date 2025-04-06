# test_filters_assign.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for '=' filter and variants.

The assignment filters' tests for '=', '=?', '+=', '-=', '*=', '/=', and
'%=', are in this module.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify
from .. import cqltypes
from .. import filters


class FiltersAssign(verify.Verify):

    def test_199_assign_01_bare(self):
        self.verify("=", [], returncode=1)

    def test_199_assign_02_name(self):
        self.verify("y=", [], returncode=1)

    def test_199_assign_03_set_01_set_variable(self):
        self.verify_assign(
            "y=k",
            [(3, "Assign"), (4, "Variable"), (4, "PieceDesignator")],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_03_set_02_piece_variable(self):
        self.verify_assign(
            "piece y=k",
            [(3, "Assign"), (4, "PieceVariable"), (4, "PieceDesignator")],
            "y",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_04_integer(self):
        self.verify_assign(
            "y=3",
            [(3, "Assign"), (4, "Variable"), (4, "Integer")],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_199_assign_05_string(self):
        self.verify_assign(
            'y="str"',
            [(3, "Assign"), (4, "Variable"), (4, "String")],
            "y",
            cqltypes.VariableType.STRING,
            cqltypes.FilterType.STRING,
        )

    def test_199_assign_06_logical(self):
        self.verify("y=true", [], returncode=1)

    def test_199_assign_07_position(self):
        self.verify_assign(
            "y=currentposition",
            [(3, "Assign"), (4, "Variable"), (4, "CurrentPosition")],
            "y",
            cqltypes.VariableType.POSITION,
            cqltypes.FilterType.POSITION,
        )

    def test_199_assign_08_function_set_01_set_variable(self):
        self.verify_assign(
            "function x(){k} y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_08_function_set_02_piece_variable(self):
        self.verify_assign(
            "function x(){k} piece y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_09_function_integer_01(self):
        self.verify_assign(
            "function x(){(7)} y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "ParenthesisLeft"),
                (8, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_199_assign_09_function_integer_02(self):
        self.verify_assign(
            "function x(){k 7} y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "PieceDesignator"),
                (7, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_199_assign_10_function_string(self):
        self.verify_assign(
            'function x(){"a"} y=x()',
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "String"),
            ],
            "y",
            cqltypes.VariableType.STRING,
            cqltypes.FilterType.STRING,
        )

    def test_199_assign_11_function_logical(self):
        self.verify("function x(){true} y=x()", [], returncode=1)

    def test_199_assign_12_function_position(self):
        self.verify_assign(
            "function x(){currentposition} y=x()",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "CurrentPosition"),
            ],
            "y",
            cqltypes.VariableType.POSITION,
            cqltypes.FilterType.POSITION,
        )

    def test_199_assign_13_set_01_integer(self):
        self.verify("y=k y=7", [], returncode=1)

    def test_199_assign_13_set_02_string(self):
        self.verify('y=k y="a"', [], returncode=1)

    def test_199_assign_13_set_03_position(self):
        self.verify("y=k y=currentposition", [], returncode=1)

    def test_199_assign_13_set_04_piece(self):
        self.verify("y=k piece y=q", [], returncode=1)

    def test_199_assign_13_set_05_piece(self):
        self.verify_assign(
            "y=k piece x=y",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "Variable"),
            ],
            "x",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_13_set_06_piece(self):
        self.verify_assign(
            "piece x=q y=k piece x=y",
            [
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "Variable"),
            ],
            "x",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_13_set_07_piece(self):
        self.verify_assign(
            "piece x=q piece y=k piece y=x",
            [
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceVariable"),
            ],
            "y",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_13_set_08_piece(self):
        self.verify("piece x=q piece y=k y=x", [], returncode=1)

    def test_199_assign_14_integer_01_set(self):
        self.verify("y=7 y=k", [], returncode=1)

    def test_199_assign_14_integer_02_string(self):
        self.verify('y=7 y="a"', [], returncode=1)

    def test_199_assign_14_integer_03_position(self):
        self.verify("y=7 y=currentposition", [], returncode=1)

    def test_199_assign_14_integer_04_piece(self):
        self.verify("y=7 piece y=q", [], returncode=1)

    def test_199_assign_15_string_01_set(self):
        self.verify('y="a" y=k', [], returncode=1)

    def test_199_assign_15_string_02_integer(self):
        self.verify('y="a" y=7', [], returncode=1)

    def test_199_assign_15_string_03_position(self):
        self.verify('y="a" y=currentposition', [], returncode=1)

    def test_199_assign_15_string_04_piece(self):
        self.verify('y="a" piece y=q', [], returncode=1)

    def test_199_assign_16_position_01_set(self):
        self.verify("y=currentposition y=k", [], returncode=1)

    def test_199_assign_16_position_02_integer(self):
        self.verify("y=currentposition y=7", [], returncode=1)

    def test_199_assign_16_position_03_string(self):
        self.verify('y=currentposition y="a"', [], returncode=1)

    def test_199_assign_16_position_04_piece(self):
        self.verify("y=currentposition piece y=q", [], returncode=1)

    def test_199_assign_17_piece_01_set(self):
        self.verify("piece y=q y=k", [], returncode=1)

    def test_199_assign_17_piece_02_integer(self):
        self.verify("piece y=q y=7", [], returncode=1)

    def test_199_assign_17_piece_03_string(self):
        self.verify('piece y=q y="a"', [], returncode=1)

    def test_199_assign_17_piece_04_position(self):
        self.verify("piece y=q y=currentposition", [], returncode=1)

    def test_199_assign_17_piece_05_piece(self):
        self.verify_assign(
            "piece y=q piece y=q",
            [
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
                (3, "Assign"),
                (4, "PieceVariable"),
                (4, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.PIECE,
            cqltypes.FilterType.SET,
        )

    def test_199_assign_18_variable_01_variable(self):
        self.verify("y=x", [], returncode=1)

    def test_199_assign_18_variable_02_piece_variable(self):
        self.verify("piece y=x", [], returncode=1)

    def test_199_assign_19_name_integer(self):
        self.verify("y[3]", [], returncode=1)

    def test_199_assign_20_name_integer_assign(self):
        self.verify("y[3]=", [], returncode=1)

    def test_199_assign_21_name_integer_integer(self):
        self.verify("y[3]=4", [], returncode=1)

    def test_199_assign_22_name_integer_string(self):
        self.verify('y[3]="a"', [], returncode=1)

    def test_199_assign_23_name_integer_piecedesignator(self):
        self.verify("y[3]=r", [], returncode=1)

    def test_199_assign_24_name_integer_other_set(self):
        self.verify("y[3]=from", [], returncode=1)

    def test_199_assign_25_name_integer_position(self):
        self.verify("y[3]=currentposition", [], returncode=1)

    def test_199_assign_26_name_integer_logical(self):
        self.verify("y[3]=true", [], returncode=1)

    def test_199_assign_27_name_string_integer(self):
        self.verify('y["here"]=4', [], returncode=1)

    def test_199_assign_28_name_string_string(self):
        self.verify('y["here"]="a"', [], returncode=1)

    def test_199_assign_29_name_string_piecedesignator(self):
        self.verify('y["here"]=r', [], returncode=1)

    def test_199_assign_30_name_string_other_set(self):
        self.verify('y["here"]=from', [], returncode=1)

    def test_199_assign_31_name_string_position(self):
        self.verify('y["here"]=currentposition', [], returncode=1)

    def test_199_assign_32_name_string_logical(self):
        self.verify('y["here"]=true', [], returncode=1)

    def test_199_assign_33_name_bad_piecedesignator_integer(self):
        self.verify("y[rc4]=4", [], returncode=1)

    def test_199_assign_34_name_bad_piecedesignator_string(self):
        self.verify('y[rc4]="a"', [], returncode=1)

    def test_199_assign_35_name_bad_piecedesignator_piecedesignator(self):
        self.verify("y[rc4]=r", [], returncode=1)

    def test_199_assign_36_name_bad_piecedesignator_other_set(self):
        self.verify("y[rc4]=from", [], returncode=1)

    def test_199_assign_37_name_bad_piecedesignator_position(self):
        self.verify("y[rc4]=currentposition", [], returncode=1)

    def test_199_assign_38_name_bad_piecedesignator_logical(self):
        self.verify("y[rc4]=true", [], returncode=1)

    def test_199_assign_39_name_piecedesignator_integer(self):
        self.verify("y[ rc4 ]=4", [], returncode=1)

    def test_199_assign_40_name_piecedesignator_string(self):
        self.verify('y[ rc4 ]="a"', [], returncode=1)

    def test_199_assign_41_name_piecedesignator_piecedesignator(self):
        self.verify("y[ rc4 ]=r", [], returncode=1)

    def test_199_assign_42_name_piecedesignator_other_set(self):
        self.verify("y[ rc4 ]=from", [], returncode=1)

    def test_199_assign_43_name_piecedesignator_position(self):
        self.verify("y[ rc4 ]=currentposition", [], returncode=1)

    def test_199_assign_44_name_piecedesignator_logical(self):
        self.verify("y[ rc4 ]=true", [], returncode=1)

    def test_199_assign_45_name_position_integer(self):
        self.verify("y[currentposition]=4", [], returncode=1)

    def test_199_assign_46_name_position_string(self):
        self.verify('y[currentposition]="a"', [], returncode=1)

    def test_199_assign_47_name_position_piecedesignator(self):
        self.verify("y[currentposition]=r", [], returncode=1)

    def test_199_assign_48_name_position_other_set(self):
        self.verify("y[currentposition]=from", [], returncode=1)

    def test_199_assign_49_name_position_position(self):
        self.verify("y[currentposition]=currentposition", [], returncode=1)

    def test_199_assign_50_name_position_logical(self):
        self.verify("y[currentposition]=true", [], returncode=1)

    def test_199_assign_51_name_logical_integer(self):
        self.verify("y[false]=4", [], returncode=1)

    def test_199_assign_52_name_logical_string(self):
        self.verify('y[false]="a"', [], returncode=1)

    def test_199_assign_53_name_logical_piecedesignator(self):
        self.verify("y[false]=r", [], returncode=1)

    def test_199_assign_54_name_logical_other_set(self):
        self.verify("y[false]=from", [], returncode=1)

    def test_199_assign_55_name_logical_position(self):
        self.verify("y[false]=currentposition", [], returncode=1)

    def test_199_assign_56_name_logical_logical(self):
        self.verify("y[false]=true", [], returncode=1)

    def test_200_assignif_01_bare(self):
        self.verify("=?", [], returncode=1)

    def test_200_assignif_02_name(self):
        self.verify("y=?", [], returncode=1)

    def test_200_assignif_03_set(self):
        self.verify_assign(
            "y=?k",
            [(3, "AssignIf"), (4, "Variable"), (4, "PieceDesignator")],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_200_assignif_04_piece(self):
        self.verify("piece y=?3", [], returncode=1)

    def test_200_assignif_05_integer(self):
        self.verify("y=?3", [], returncode=1)

    def test_200_assignif_06_string(self):
        self.verify('y=?"str"', [], returncode=1)

    def test_200_assignif_07_logical(self):
        self.verify("y=?true", [], returncode=1)

    def test_200_assignif_08_position(self):
        self.verify("y=?currentposition", [], returncode=1)

    def test_200_assignif_09_function_set(self):
        self.verify_assign(
            "function x(){k} y=?x()",
            [
                (3, "Function"),
                (3, "AssignIf"),
                (4, "Variable"),
                (4, "FunctionCall"),
                (5, "BraceLeft"),
                (6, "BraceLeft"),
                (7, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_200_assignif_10_function_piece(self):
        self.verify("function x(){k} piece y=?x()", [], returncode=1)

    def test_200_assignif_11_function_integer_01(self):
        self.verify("function x(){(7)} y=?x()", [], returncode=1)

    def test_200_assignif_11_function_integer_02(self):
        self.verify("function x(){k 7} y=?x()", [], returncode=1)

    def test_200_assignif_12_function_string(self):
        self.verify('function x(){"a"} y=?x()', [], returncode=1)

    def test_200_assignif_13_function_logical(self):
        self.verify("function x(){true} y=?x()", [], returncode=1)

    def test_200_assignif_14_function_position(self):
        self.verify("function x(){currentposition} y=?x()", [], returncode=1)

    def test_200_assignif_15_set_01_set(self):
        self.verify_assign(
            "y=k y=?q",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "PieceDesignator"),
                (3, "AssignIf"),
                (4, "Variable"),
                (4, "PieceDesignator"),
            ],
            "y",
            cqltypes.VariableType.SET,
            cqltypes.FilterType.SET,
        )

    def test_200_assignif_15_set_02_piece(self):
        self.verify("piece y=k y=?q", [], returncode=1)

    def test_200_assignif_15_set_03_integer(self):
        self.verify("y=7 y=?q", [], returncode=1)

    def test_200_assignif_15_set_04_string(self):
        self.verify('y="a" y=?q', [], returncode=1)

    def test_200_assignif_15_set_05_position(self):
        self.verify("y=currentposition y=?q", [], returncode=1)

    def test_201_count_01_bare(self):
        self.verify("#", [], returncode=1)

    def test_201_count_02_set(self):
        self.verify("#k", [(3, "CountFilter"), (4, "PieceDesignator")])

    def test_201_count_03_integer(self):
        self.verify("#3", [], returncode=1)

    def test_201_count_04_string(self):
        self.verify('#"str"', [(3, "CountFilter"), (4, "String")])

    def test_201_count_05_logical(self):
        self.verify("#false", [], returncode=1)

    def test_201_count_06_position(self):
        self.verify("#currentposition", [], returncode=1)

    def test_202_assign_plus_01_bare_01(self):
        self.verify("+=", [], returncode=1)

    def test_202_assign_plus_01_bare_02(self):
        self.verify("y=k +=", [], returncode=1)

    def test_202_assign_plus_01_bare_03(self):
        self.verify("y=k y+=", [], returncode=1)

    def test_202_assign_plus_02_undefined_01_set(self):
        self.verify("y+=k", [], returncode=1)

    def test_202_assign_plus_02_undefined_02_integer(self):
        self.verify("y+=7", [], returncode=1)

    def test_202_assign_plus_02_undefined_03_string(self):
        self.verify('y+="a"', [], returncode=1)

    def test_202_assign_plus_02_undefined_04_logical(self):
        self.verify("y+=true", [], returncode=1)

    def test_202_assign_plus_02_undefined_05_position(self):
        self.verify("y+=currentposition", [], returncode=1)

    def test_202_assign_plus_03_set(self):
        self.verify("y=k y+=q", [], returncode=1)

    def test_202_assign_plus_04_integer(self):
        self.verify_assign(
            "y=3 y+=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignPlus"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_202_assign_plus_05_string(self):
        self.verify_assign(
            'y="3" y+="4"',
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "String"),
                (3, "AssignPlus"),
                (4, "Variable"),
                (4, "String"),
            ],
            "y",
            cqltypes.VariableType.STRING,
            cqltypes.FilterType.STRING,
        )

    def test_202_assign_plus_06_logical(self):
        self.verify("y=true y+=false", [], returncode=1)

    def test_202_assign_plus_07_position(self):
        self.verify("y=initialposition y+=currentposition", [], returncode=1)

    def test_203_assign_minus_01_bare_01(self):
        self.verify("-=", [], returncode=1)

    def test_203_assign_minus_01_bare_02(self):
        self.verify("y=k -=", [], returncode=1)

    def test_203_assign_minus_01_bare_03(self):
        self.verify("y=k y-=", [], returncode=1)

    def test_203_assign_minus_02_undefined_01_set(self):
        self.verify("y-=k", [], returncode=1)

    def test_203_assign_minus_02_undefined_02_integer(self):
        self.verify("y-=7", [], returncode=1)

    def test_203_assign_minus_02_undefined_03_string(self):
        self.verify('y-="a"', [], returncode=1)

    def test_203_assign_minus_02_undefined_04_logical(self):
        self.verify("y-=true", [], returncode=1)

    def test_203_assign_minus_02_undefined_05_position(self):
        self.verify("y-=currentposition", [], returncode=1)

    def test_203_assign_minus_03_set(self):
        self.verify("y=k y-=q", [], returncode=1)

    def test_203_assign_minus_04_integer(self):
        self.verify_assign(
            "y=3 y-=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignMinus"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_203_assign_minus_05_string(self):
        self.verify('y="3" y-="4"', [], returncode=1)

    def test_203_assign_minus_06_logical(self):
        self.verify("y=true y-=false", [], returncode=1)

    def test_203_assign_minus_07_position(self):
        self.verify("y=initialposition y-=currentposition", [], returncode=1)

    def test_204_assign_divide_01_bare_01(self):
        self.verify("/=", [], returncode=1)

    def test_204_assign_divide_01_bare_02(self):
        self.verify("y=k /=", [], returncode=1)

    def test_204_assign_divide_01_bare_03(self):
        self.verify("y=k y/=", [], returncode=1)

    def test_204_assign_divide_02_undefined_01_set(self):
        self.verify("y/=k", [], returncode=1)

    def test_204_assign_divide_02_undefined_02_integer(self):
        self.verify("y/=7", [], returncode=1)

    def test_204_assign_divide_02_undefined_03_string(self):
        self.verify('y/="a"', [], returncode=1)

    def test_204_assign_divide_02_undefined_04_logical(self):
        self.verify("y/=true", [], returncode=1)

    def test_204_assign_divide_02_undefined_05_position(self):
        self.verify("y/=currentposition", [], returncode=1)

    def test_204_assign_divide_03_set(self):
        self.verify("y=k y/=q", [], returncode=1)

    def test_204_assign_divide_04_integer(self):
        self.verify_assign(
            "y=3 y/=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignDivide"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_204_assign_divide_05_string(self):
        self.verify('y="3" y/="4"', [], returncode=1)

    def test_204_assign_divide_06_logical(self):
        self.verify("y=true y/=false", [], returncode=1)

    def test_204_assign_divide_07_position(self):
        self.verify("y=initialposition y/=currentposition", [], returncode=1)

    def test_205_assign_multiply_01_bare_01(self):
        self.verify("*=", [], returncode=1)

    def test_205_assign_multiply_01_bare_02(self):
        self.verify("y=k *=", [], returncode=1)

    def test_205_assign_multiply_01_bare_03(self):
        self.verify("y=k y*=", [], returncode=1)

    def test_205_assign_multiply_02_undefined_01_set(self):
        self.verify("y*=k", [], returncode=1)

    def test_205_assign_multiply_02_undefined_02_integer(self):
        self.verify("y*=7", [], returncode=1)

    def test_205_assign_multiply_02_undefined_03_string(self):
        self.verify('y*="a"', [], returncode=1)

    def test_205_assign_multiply_02_undefined_04_logical(self):
        self.verify("y*=true", [], returncode=1)

    def test_205_assign_multiply_02_undefined_05_position(self):
        self.verify("y*=currentposition", [], returncode=1)

    def test_205_assign_multiply_03_set(self):
        self.verify("y=k y*=q", [], returncode=1)

    def test_205_assign_multiply_04_integer(self):
        self.verify_assign(
            "y=3 y*=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignMultiply"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_205_assign_multiply_05_string(self):
        self.verify('y="3" y*="4"', [], returncode=1)

    def test_205_assign_multiply_06_logical(self):
        self.verify("y=true y*=false", [], returncode=1)

    def test_205_assign_multiply_07_position(self):
        self.verify("y=initialposition y*=currentposition", [], returncode=1)

    def test_206_assign_modulus_01_bare_01(self):
        self.verify("%=", [], returncode=1)

    def test_206_assign_modulus_01_bare_02(self):
        self.verify("y=k %=", [], returncode=1)

    def test_206_assign_modulus_01_bare_03(self):
        self.verify("y=k y%=", [], returncode=1)

    def test_206_assign_modulus_02_undefined_01_set(self):
        self.verify("y%=k", [], returncode=1)

    def test_206_assign_modulus_02_undefined_02_integer(self):
        self.verify("y%=7", [], returncode=1)

    def test_206_assign_modulus_02_undefined_03_string(self):
        self.verify('y%="a"', [], returncode=1)

    def test_206_assign_modulus_02_undefined_04_logical(self):
        self.verify("y%=true", [], returncode=1)

    def test_206_assign_modulus_02_undefined_05_position(self):
        self.verify("y%=currentposition", [], returncode=1)

    def test_206_assign_modulus_03_set(self):
        self.verify("y=k y%=q", [], returncode=1)

    def test_206_assign_modulus_04_integer(self):
        self.verify_assign(
            "y=3 y%=4",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "AssignModulus"),
                (4, "Variable"),
                (4, "Integer"),
            ],
            "y",
            cqltypes.VariableType.NUMERIC,
            cqltypes.FilterType.NUMERIC,
        )

    def test_206_assign_modulus_05_string(self):
        self.verify('y="3" y%="4"', [], returncode=1)

    def test_206_assign_modulus_06_logical(self):
        self.verify("y=true y%=false", [], returncode=1)

    def test_206_assign_modulus_07_position(self):
        self.verify("y=initialposition y%=currentposition", [], returncode=1)


if __name__ == "__main__":
    if verify.is_cql_on_path():
        runner = unittest.TextTestRunner
        loader = unittest.defaultTestLoader.loadTestsFromTestCase
        runner().run(loader(FiltersAssign))
