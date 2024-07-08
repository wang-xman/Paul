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

from linear_space.linear_object import LinearObject, is_matrix_like
from linear_space.linear_object.algebra import outer, LinearObjectAlgebraError


class Test_Outer(unittest.TestCase):
    def test_col_and_row(self):
        col_array = np.array([[3],[4]])
        col = LinearObject(array=col_array)
        row_array = np.array([[1,2]])
        row = LinearObject(array=row_array)
        # should be a scalar
        res = outer(col, row)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 2)
        self.assertEqual(res.get_nrows(), 2)
        self.assertEqual(res.get_element(0,0), 3)
        self.assertTrue(is_matrix_like(res))

    def test_col_and_row_2(self):
        col_array = np.array([[3],[4]])
        col = LinearObject(array=col_array)
        row_array = np.array([[1,2, 3]])
        row = LinearObject(array=row_array)
        # should be a scalar
        res = outer(col, row)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 3)
        self.assertEqual(res.get_nrows(), 2)
        self.assertEqual(res.get_element(0,0), 3)
        self.assertTrue(is_matrix_like(res))

    def test_col_and_col(self):
        col_array = np.array([[3],[4j]])
        col = LinearObject(array=col_array)
        #row_array = np.array([[1,2, 3]])
        #row = LinearObject(array=row_array)
        # should be a scalar
        res = outer(col, col)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 2)
        self.assertEqual(res.get_nrows(), 2)
        self.assertEqual(res.get_element(0,1), -12.j)
        self.assertTrue(is_matrix_like(res))

    def test_row_and_col(self):
        col_array = np.array([[3],[4j]])
        col = LinearObject(array=col_array)
        row_array = np.array([[1,2j, 3]])
        row = LinearObject(array=row_array)
        # should be a scalar
        res = outer(row, col)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 2)
        self.assertEqual(res.get_nrows(), 3)
        self.assertEqual(res.get_element(1,0), -6j)
        self.assertTrue(is_matrix_like(res))
