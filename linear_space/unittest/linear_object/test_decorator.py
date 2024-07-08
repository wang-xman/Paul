"""
File under test:
    linear_space.linear_object.decorator.py

Main test:
    Linear algebra function decorator.

Updated:
    27 September 2021
"""
import unittest
#import numpy as np

#from linear_space.linear_object import LinearObject, is_column_like, \
#    is_row_like, is_scalar_like, is_matrix_like

from linear_space.linear_object.decorator import algebra_function_decorator,\
    LinearObjectAlgebraError


@algebra_function_decorator(
    argument_type = {
        'alpha': int,
        'beta': int
    }
)
def test_fully_declared(alpha, beta):
    return alpha + beta


class Test_Fully_Declared(unittest.TestCase):
    def test_okay(self):
        res = test_fully_declared(1,1)
        self.assertEqual(res, 2)

    def test_wrong_type(self):
        self.assertRaises(LinearObjectAlgebraError, test_fully_declared, 1, 0.5)

    def test_wrong_type_2(self):
        self.assertRaises(LinearObjectAlgebraError, test_fully_declared, 0.1, 5)

    def test_wrong_type_3(self):
        self.assertRaises(LinearObjectAlgebraError, test_fully_declared, 0.1, 0.5)


@algebra_function_decorator(
    argument_type = {
        'beta': int
    }
)
def test_partly_declared(alpha, beta):
    return alpha + beta


class Test_Partly_Declared(unittest.TestCase):
    def test_okay(self):
        res = test_partly_declared(1,1)
        self.assertEqual(res, 2)
    
    def test_okay_2(self):
        res = test_partly_declared(0.5, 2)
        self.assertEqual(res, 2.5)

    def test_wrong_type(self):
        self.assertRaises(LinearObjectAlgebraError,
                          test_partly_declared, 1, 0.5)

    def test_wrong_type_3(self):
        self.assertRaises(LinearObjectAlgebraError,
                          test_partly_declared, 0.1, 0.5)
