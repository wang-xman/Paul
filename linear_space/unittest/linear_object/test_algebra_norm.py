"""
File under test:
    linear_space.linear_object.algebra.py

Main test:
    Linear algebraic methods associated with linear object.

Updated:
    29 September 2021
"""
import unittest
import numpy as np

from linear_space.linear_object import LinearObject
from linear_space.linear_object.algebra import norm
from linear_space.linear_object.errors import LinearObjectAlgebraError


class Test_Number(unittest.TestCase):
    def test_positive_number(self):
        num = 2.0
        res = norm(num)
        self.assertTrue(res == num)

    def test_negative_number(self):
        num = -2.0
        res = norm(num)
        self.assertTrue(res == -1.0 *num)

    def test_complex_number(self):
        num = 3.0 + 4.j
        res = norm(num)
        self.assertTrue(res == 5.0)


class Test_Linear_Object(unittest.TestCase):
    def test_column_like(self):
        lin = LinearObject(array=np.array([[3],[4]]))
        res = norm(lin)
        self.assertTrue(res == 5.0)

    def test_row_like(self):
        lin = LinearObject(array=np.array([[3, 4.j]]))
        res = norm(lin)
        self.assertTrue(res == 5.0)

    def test_matrix_like(self):
        lin = LinearObject(array=np.array([[3, 4.j], [1, 2]]))
        #res = norm(lin)
        self.assertRaises(LinearObjectAlgebraError, norm, lin)
