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

from linear_space.linear_object import LinearObject, is_scalar_like, is_matrix_like
from linear_space.linear_object.algebra import dot, LinearObjectAlgebraError


class Test_Dot_MatrixMultiplication(unittest.TestCase):
    def test_row_and_col(self):
        row_array = np.array([[1,2,3,4]])
        row = LinearObject(array=row_array)
        col_array = np.array([[1],[2],[3],[4]])
        col = LinearObject(array=col_array)
        # should be a scalar
        res = dot(row,col)
        self.assertTrue(isinstance(res, LinearObject))
        self.assertEqual(res.get_ncols(), 1)
        self.assertEqual(res.get_nrows(), 1)
        self.assertEqual(res.get_element(0,0), 30)
        self.assertTrue(is_scalar_like(res))

    def test_row_and_col_mismatch(self):
        row_array = np.array([[1,2,3,4,5]])
        row = LinearObject(array=row_array)
        col_array = np.array([[1],[2],[3],[4]])
        col = LinearObject(array=col_array)
        # Error: incompatible
        #res = row.dot(col)
        self.assertRaises(LinearObjectAlgebraError, dot, row, col)

    def test_col_and_row(self):
        """ Result is the outer product """
        row_array = np.array([[1,2,3,4,5]])
        row = LinearObject(array=row_array)
        col_array = np.array([[1],[2],[3],[4]])
        col = LinearObject(array=col_array)
        # Outer product
        res = dot(col,row)

    def test_matrix_like(self):
        """ Regular matrix multiplication """
        array_a = np.array([[1,2,3],[1,2,3]])
        mata = LinearObject(array=array_a)
        array_b = np.array([[0, 3],[1, 4],[2, 5]])
        matb = LinearObject(array=array_b)
        # Outer product
        res = dot(mata,matb)
        self.assertTrue(is_matrix_like(res))
        #print(res)

    def test_matrix_like_mismatch(self):
        array_a = np.array([[1,2,3,4],[4,1,2,3]])
        mata = LinearObject(array=array_a)
        array_b = np.array([[0, 3],[1, 4],[2, 5]])
        matb = LinearObject(array=array_b)
        # Error: size mismatch
        #res = mata.dot(matb)
        self.assertRaises(LinearObjectAlgebraError, dot, mata, matb)
        #print(matb.dot(mata))