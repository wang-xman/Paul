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
from linear_space.matrix.matrix import Matrix
from linear_space.matrix.square_matrix import SquareMatrix
from linear_space.vector.column_vector import ColumnVector
from linear_space.vector.row_vector import RowVector
from linear_space.algebra.functions import hermitian_conjugate


class TestHermitianConjugate(unittest.TestCase):
    def test_column_vector(self):
        array_a = np.array([[1.0], [1.0j], [2.0], [2.0j], [3.0]])
        vec = ColumnVector(array=array_a)
        res = hermitian_conjugate(vec)
        self.assertTrue(isinstance(res, RowVector))
        self.assertTrue(res[1], -1j)
        self.assertTrue(res[3], -2j)

    def test_row_vector(self):
        array_a = np.array([[1.0, 1.0j, 2.0, 2.0j, 3.0]])
        vec = RowVector(array=array_a)
        res = hermitian_conjugate(vec)
        self.assertTrue(isinstance(res, ColumnVector))
        self.assertTrue(res[1], -1j)
        self.assertTrue(res[3], -2j)

    def test_square_matrix(self):
        array_a = np.array([[1.0, 1.0j], [2.0, 2.0j]])
        mat = SquareMatrix(array=array_a)
        res = hermitian_conjugate(mat)
        self.assertTrue(isinstance(res, SquareMatrix))
        self.assertTrue(res.nrows, 2)
        self.assertTrue(res.ncols, 2)
        self.assertEqual(res[0][0], 1)
        self.assertEqual(res[0][1], 2)
        self.assertEqual(res[1][0], -1j)
        self.assertEqual(res[1][1], -2j)

    def test_matrix(self):
        array_a = np.array([[1.0, 1.0j, 2.0], [1.0j, 1.0, 2.0j]])
        mat = Matrix(array=array_a)
        res = hermitian_conjugate(mat)
        self.assertTrue(isinstance(res, Matrix))
        self.assertTrue(res.nrows, 3)
        self.assertTrue(res.ncols, 2)
        self.assertEqual(res[0][1], -1j)
        self.assertEqual(res[1][0], -1j)
        self.assertEqual(res[2][1], -2j)
