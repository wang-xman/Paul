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

from linear_space.linear_object import LinearObject, is_column_like, is_row_like
from linear_space.linear_object.algebra import add, LinearObjectAlgebraError


class Test_Add(unittest.TestCase):
    def test_non_linear_object(self):
        a1 = np.array([[1],[2],[3],[4]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4], [4]])
        #add(col1,a2)
        self.assertRaises(LinearObjectAlgebraError, add, col1, a2)

    def test_col_like(self):
        a1 = np.array([[1],[2],[3],[4]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4]])
        col2 = LinearObject(array=a2)
        col = add(col1,col2)
        # column like
        self.assertEqual(col.get_ncols(), 1)
        self.assertEqual(col.get_nrows(), 4)
        self.assertTrue(is_column_like(col))

    def test_col_like_wrong_size(self):
        a1 = np.array([[1],[2],[3],[4]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4], [4]])
        col2 = LinearObject(array=a2)
        #add(col1,col2)
        self.assertRaises(LinearObjectAlgebraError, add, col1, col2)

    def test_row_like(self):
        a1 = np.array([[1,2,3,4]])
        row1 = LinearObject(array=a1)
        a2 = np.array([[1,2,3,4]])
        row2 = LinearObject(array=a2)
        row = add(row1,row2)
        # row like
        self.assertEqual(row.get_ncols(), 4)
        self.assertEqual(row.get_nrows(), 1)
        self.assertFalse(is_column_like(row))
        self.assertTrue(is_row_like(row))

    def test_row_like_wrong(self):
        a1 = np.array([[1,2,3,4]])
        row1 = LinearObject(array=a1)
        a2 = np.array([[1,2,3,4,5]])
        row2 = LinearObject(array=a2)
        # Error: mismatched size
        self.assertRaises(LinearObjectAlgebraError, add, row1, row2)