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

from linear_space.linear_object import LinearObject, is_scalar_like
from linear_space.linear_object.algebra import inner, LinearObjectAlgebraError


class Test_Inner(unittest.TestCase):
    def test_row_and_col(self):
        row_array = np.array([[1,2,3,4]])
        row = LinearObject(array=row_array)
        col_array = np.array([[1],[2],[3],[4]])
        col = LinearObject(array=col_array)
        # should be a scalar
        res = inner(row,col)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 1)
        self.assertEqual(res.get_nrows(), 1)
        self.assertEqual(res.get_element(0,0), 30)
        self.assertTrue(is_scalar_like(res))

    def test_row_and_row(self):
        row_array = np.array([[1,2.j]])
        row = LinearObject(array=row_array)
        row_array2 = np.array([[1,2]])
        row2 = LinearObject(array=row_array2)
        # should be a scalar
        res = inner(row, row2)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 1)
        self.assertEqual(res.get_nrows(), 1)
        self.assertEqual(res.get_element(0,0), 1.0 + 4.j)
        self.assertTrue(is_scalar_like(res))

    def test_col_and_row(self):
        col_array = np.array([[1],[2.j]])
        col = LinearObject(array=col_array)
        row_array2 = np.array([[1,2]])
        row2 = LinearObject(array=row_array2)
        # should be a scalar
        res = inner(col, row2)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 1)
        self.assertEqual(res.get_nrows(), 1)
        self.assertEqual(res.get_element(0,0), 1.0 - 4.j)
        self.assertTrue(is_scalar_like(res))

    def test_col_and_col(self):
        col_array = np.array([[1],[2.j]])
        col = LinearObject(array=col_array)
        col_array2 = np.array([[1.],[2.j]])
        col2 = LinearObject(array=col_array2)
        # should be a scalar
        res = inner(col, col2)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 1)
        self.assertEqual(res.get_nrows(), 1)
        self.assertEqual(res.get_element(0,0), 5)
        self.assertTrue(is_scalar_like(res))

    def test_col_and_col_size_problem(self):
        col_array = np.array([[1],[2.j]])
        col = LinearObject(array=col_array)
        col_array2 = np.array([[1.],[2.j],[2.j]])
        col2 = LinearObject(array=col_array2)
        # Error
        #res = inner(col, col2)
        self.assertRaises(LinearObjectAlgebraError, inner, col, col2)