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

from linear_space.linear_object.linear_object import LinearObject
from linear_space.linear_object import Column_Like, Row_Like, is_column_like, \
    is_row_like, is_scalar_like, is_matrix_like
from linear_space.linear_object.algebra import transpose, LinearObjectAlgebraError


class Test_Transpose(unittest.TestCase):
    def test_to_row_like(self):
        a1 = np.array([[1],[2]])
        col1 = LinearObject(array=a1)
        row1 = transpose(col1)
        self.assertTrue(is_row_like(row1))
        self.assertTrue(isinstance(row1, Row_Like))

    def test_to_column_like(self):
        a2 = np.array([[1,2,3,4,5,]])
        row2 = LinearObject(array=a2)
        col2 = transpose(row2)
        self.assertTrue(is_column_like(col2))
        self.assertTrue(isinstance(col2, Column_Like))

    def test_matrix(self):
        a2 = np.array([[1,2],[3,4], [4,5]])
        mat = LinearObject(array=a2)
        matt = transpose(mat)
        self.assertTrue(is_matrix_like(matt))
