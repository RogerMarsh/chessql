# test_filter_function.py
# Copyright 2025 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Verify chessql.core.parser output for 'function' filter.

The verification methods are provided by the Verify superclass.
"""

import unittest

from . import verify


class FilterFunction(verify.Verify):

    def test_044_function_01_bare(self):
        self.verify("function", [], returncode=1)

    def test_044_function_02_name_bare(self):
        self.verify("function fn", [], returncode=1)

    def test_044_function_03_no_body(self):
        self.verify("function fn()", [], returncode=1)

    def test_044_function_04_body_named_filter(self):
        self.verify("function fn(){wtm}", [(3, "Function")])

    def test_044_function_05_body_named_filter_call(self):
        self.verify(
            "function fn(){wtm} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "WTM"),
            ],
        )

    def test_044_function_06_argument_body_named_filter_call(self):
        self.verify(
            "function fn(y){y==1} x=1 fn(x)",
            [
                (3, "Function"),
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Eq"),
                (7, "Variable"),
                (7, "Integer"),
            ],
        )

    def test_044_function_07_body_set_call(self):
        self.verify(
            "function fn(){k} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "PieceDesignator"),
            ],
        )

    def test_044_function_08_body_integer_call_01_bare(self):
        self.verify("function fn(){1} fn()", [], returncode=1)

    def test_044_function_08_body_integer_call_02_parentheses(self):
        self.verify(
            "function fn(){(1)} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "ParenthesisLeft"),
                (7, "Integer"),
            ],
        )

    def test_044_function_08_body_integer_call_03_variable(self):
        self.verify(
            "v=1 function fn(){v} fn()",
            [
                (3, "Assign"),
                (4, "Variable"),
                (4, "Integer"),
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "Variable"),
            ],
        )

    def test_044_function_09_body_string_call(self):
        self.verify(
            'function fn(){"a"} fn()',
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "String"),
            ],
        )

    def test_044_function_10_body_logical_call(self):
        self.verify(
            "function fn(){true} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "True_"),
            ],
        )

    def test_044_function_11_body_position_call(self):
        self.verify(
            "function fn(){initialposition} fn()",
            [
                (3, "Function"),
                (3, "FunctionCall"),
                (4, "BraceLeft"),
                (5, "BraceLeft"),
                (6, "InitialPosition"),
            ],
        )

    def test_044_function_12_body_integer_01_bare(self):
        self.verify("function fn(){1}", [], returncode=1)

    def test_044_function_12_body_integer_02_parentheses(self):
        self.verify("function fn(){(1)}", [(3, "Function")])

    def test_044_function_12_body_integer_03_variable(self):
        self.verify(
            "v=1 function fn(){v}",
            [(3, "Assign"), (4, "Variable"), (4, "Integer"), (3, "Function")],
        )

    def test_044_function_13_body_string(self):
        self.verify('function fn(){"a"}', [(3, "Function")])

    def test_044_function_14_body_logical(self):
        self.verify("function fn(){true}", [(3, "Function")])

    def test_044_function_15_body_position(self):
        self.verify("function fn(){initialposition}", [(3, "Function")])


if __name__ == "__main__":
    runner = unittest.TextTestRunner
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    runner().run(loader(FilterFunction))
