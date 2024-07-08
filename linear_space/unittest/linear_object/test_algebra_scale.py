"""
File under test:
    linear_space.linear_object.algebra.py

Main test:
    Linear algebraic methods associated with linear object.

Updated:
    23 September 2021
"""
import unittest
import numpy as np

from linear_space.linear_object import LinearObject, is_column_like, is_row_like, \
    is_matrix_like
from linear_space.linear_object.algebra import scale, LinearObjectAlgebraError


class Test_Scale(unittest.TestCase):
    def test_row_like(self):
        factor = 0.5
        row_array = np.array([[1,2,3,4]])
        row = LinearObject(array=row_array)
        res = scale(factor, row)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 4)
        self.assertEqual(res.get_nrows(), 1)
        self.assertEqual(res.get_element(0,0), 0.5)
        self.assertTrue(is_row_like(res))

    def test_col_like(self):
        factor = 100
        col_array = np.array([[1],[2],[3],[4]])
        col = LinearObject(array=col_array)
        # should be a scalar
        res = scale(factor, col)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 1)
        self.assertEqual(res.get_nrows(), 4)
        self.assertEqual(res.get_element(0,0), 100)
        self.assertTrue(is_column_like(res))

    def test_matrix_like(self):
        factor = 10
        array_a = np.array([[1,2,3],[1,2,3]])
        mata = LinearObject(array=array_a)
        res = scale(factor, mata)
        self.assertTrue(is_matrix_like(res))
        self.assertEqual(res.get_element(0,0), 10)
        self.assertEqual(res.get_element(1,2), 30)
