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

from linear_space.linear_object import LinearObject, is_column_like, \
    is_scalar_like
from linear_space.linear_object.algebra import multiply, LinearObjectAlgebraError


class Test_Multiply(unittest.TestCase):
    def test_col_like(self):
        a1 = np.array([[1],[2],[3],[4]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4]])
        col2 = LinearObject(array=a2)
        # Kronecker
        col = multiply(col1,col2)
        self.assertTrue(is_column_like(col))
        #print(col.as_array())

    def test_col_like_2(self):
        a1 = np.array([[1],[2]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4]])
        col2 = LinearObject(array=a2)
        # Kronecker
        col = multiply(col1,col2)
        self.assertTrue(is_column_like(col))
        #print(col.as_array())

    def test_col_like_3(self):
        a1 = np.array([[1],[2]])
        col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4]])
        col2 = LinearObject(array=a2)
        col = multiply(col2,col1)
        self.assertTrue(is_column_like(col))
        #print(col.as_array())

    def test_col_like_with_number(self):
        #a1 = np.array([[1],[2]])
        #col1 = LinearObject(array=a1)
        a2 = np.array([[1],[2],[3],[4]])
        col2 = LinearObject(array=a2)
        # same result
        #colleft = 5 * col2
        colright = multiply(col2,5)
        self.assertTrue(is_column_like(colright))

    def test_2_numbers(self):
        res = multiply(2,5)
        self.assertTrue(is_scalar_like(res))

    def test_wrong_type(self):
        # Error: number and string, no.
        self.assertRaises(LinearObjectAlgebraError, multiply, 2, 'Halo')
        self.assertRaises(LinearObjectAlgebraError, multiply, '2', 5)
        self.assertRaises(LinearObjectAlgebraError, multiply, '2', 'Halo')
        self.assertRaises(LinearObjectAlgebraError, multiply, '2',
                          np.array([[1],[2],[3],[4]]))
