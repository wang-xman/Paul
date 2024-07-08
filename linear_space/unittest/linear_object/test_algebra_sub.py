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

from linear_space.linear_object import LinearObject, is_column_like
from linear_space.linear_object.algebra import subtract, LinearObjectAlgebraError


class Test_Sub(unittest.TestCase):
    def test_col_like(self):
        a1 = np.array([[1],[2],[3],[4]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4]])
        col2 = LinearObject(array=a2)
        col = subtract(col1,col2)
        # column like
        self.assertEqual(col.get_ncols(), 1)
        self.assertEqual(col.get_nrows(), 4)
        self.assertTrue(is_column_like(col))

    def test_col_like_worng_size(self):
        a1 = np.array([[1],[2],[3],[4]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4], [4]])
        col2 = LinearObject(array=a2)
        self.assertRaises(LinearObjectAlgebraError, subtract, col1, col2)