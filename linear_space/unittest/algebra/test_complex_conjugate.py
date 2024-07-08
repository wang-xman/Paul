#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    linear_space.algebra.functions.py

Main test:
    Linear algebraic operation functions

Updated:
    23 September 2021
"""
import unittest
import numpy as np

from linear_space.matrix.square_matrix import SquareMatrix
from linear_space.vector.column_vector import ColumnVector
from linear_space.algebra.functions import complex_conjugate


class Test_ComplexConjugate(unittest.TestCase):
    def test_square_matrix(self):
        array_a = np.array([[1.0, 1.0j], [2.0, 2.0j]])
        mat = SquareMatrix(array=array_a)
        res = complex_conjugate(mat)
        self.assertTrue(isinstance(res, SquareMatrix))
        self.assertTrue(res.nrows, 2)
        self.assertTrue(res.ncols, 2)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], -1j)
        self.assertEqual(res[1][0], 2)
        self.assertEqual(res[1][1], -2j)

    def test_vector(self):
        array_a = np.array([[1.0], [1.0j], [2.0], [2.0j], [3.0]])
        vec = ColumnVector(array=array_a)
        res = complex_conjugate(vec)
        self.assertTrue(isinstance(res, ColumnVector))
        self.assertTrue(res[1], -1j)
        self.assertTrue(res[3], -2j)
