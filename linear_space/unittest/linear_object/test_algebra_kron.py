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
from linear_space.linear_object.algebra import kronecker, LinearObjectAlgebraError


class Test_Kronecker(unittest.TestCase):
    def test_col_like(self):
        a1 = np.array([[1],[2]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2]])
        col2 = LinearObject(array=a2)
        # Kronecker
        col = kronecker(col1, col2)
        #print(col.as_array())
        expected = np.array([[1],[2],[2],[4]])
        self.assertTrue(is_column_like(col))
        self.assertTrue(np.array_equal(col.as_array(), expected))

    def test_row_like(self):
        a1 = np.array([[1,2]])
        row1 = LinearObject(array=a1)
        a2 = np.array([[1,2]])
        row2 = LinearObject(array=a2)
        row = kronecker(row1,row2)
        expected = np.array([[1,2,2,4]])
        #print(row.as_array())
        self.assertFalse(is_column_like(row))
        self.assertTrue(is_row_like(row))
        self.assertTrue(np.array_equal(row.as_array(), expected))

    def test_col_and_row(self):
        a1 = np.array([[1],[2]])
        col = LinearObject(array=a1)
        a2 = np.array([[1,2]])
        row = LinearObject(array=a2)
        res = kronecker(col,row)
        expected = np.array([[1,2],[2,4]])
        self.assertFalse(is_column_like(res))
        self.assertFalse(is_row_like(res))
        self.assertTrue(is_matrix_like(res))
        self.assertTrue(np.array_equal(res.as_array(), expected))

    def test_col_and_matrix(self):
        a1 = np.array([[1],[2]])
        col = LinearObject(array=a1)
        a2 = np.array([[1,2],[3,4]])
        mat = LinearObject(array=a2)
        res = kronecker(col,mat)
        expected = np.array([[1,2],[3,4],[2,4],[6,8]])
        self.assertFalse(is_column_like(res))
        self.assertFalse(is_row_like(res))
        self.assertTrue(is_matrix_like(res))
        self.assertTrue(np.array_equal(res.as_array(), expected))

    def test_matrix_and_col(self):
        a1 = np.array([[1],[2]])
        col = LinearObject(array=a1)
        a2 = np.array([[1,2],[3,4]])
        mat = LinearObject(array=a2)
        res = kronecker(mat, col)
        expected = np.array([[1,2],[2,4],[3,4],[6,8]])
        self.assertFalse(is_column_like(res))
        self.assertFalse(is_row_like(res))
        self.assertTrue(is_matrix_like(res))
        self.assertTrue(np.array_equal(res.as_array(), expected))

    def test_matrix_and_matrix(self):
        a1 = np.array([[2,1],[3,2]])
        mat1 = LinearObject(array=a1)
        a2 = np.array([[1,2],[3,4]])
        mat2 = LinearObject(array=a2)
        res = kronecker(mat1,mat2)
        expected = np.array([[2,4,1,2],[6,8,3,4],[3,6,2,4],[9,12,6,8]])
        self.assertFalse(is_column_like(res))
        self.assertFalse(is_row_like(res))
        self.assertTrue(is_matrix_like(res))
        self.assertTrue(np.array_equal(res.as_array(), expected))
