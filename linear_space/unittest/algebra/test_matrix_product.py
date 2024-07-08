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
from linear_space.matrix.identity_matrix import IdentityMatrix
from linear_space.vector.column_vector import ColumnVector
from linear_space.vector.row_vector import RowVector
from linear_space.algebra.decorator import LinearSpaceAlgebraFunctionError
from linear_space.algebra.functions import matrix_product


class Test_MatrixProduct(unittest.TestCase):
    def test_idm_with_vector(self):
        idm = IdentityMatrix(row_size=3)
        array_a = np.array([[1.0], [1.0j], [2.0]])
        vec = ColumnVector(array=array_a)
        res = matrix_product(idm, vec)
        self.assertTrue(isinstance(res, ColumnVector))
        self.assertTrue(res[1] == 1.0j)
        self.assertTrue(res[2] == 2.0)

    def test_idm_with_vector_error(self):
        idm = IdentityMatrix(row_size=4)
        array_a = np.array([[1.0], [1.0j], [2.0]])
        vec = ColumnVector(array=array_a)
        #res = matrix_product(idm, vec)
        # Error: size doesn't match
        self.assertRaises(LinearSpaceAlgebraFunctionError, matrix_product, idm, vec)

    def test_matrix_with_vector(self):
        array_a = np.array([[1.0, 1.0j], [2.0, 2.0j]])
        mat = SquareMatrix(array=array_a)
        array_b = np.array([[1.0], [1.0j]])
        vec = ColumnVector(array=array_b)
        res = matrix_product(mat, vec)
        self.assertTrue(isinstance(res, ColumnVector))
        self.assertTrue(res[0] == 0. + 0.j)
        self.assertTrue(res[1] == 0. + 0.j)

    def test_matrix_with_vector_size_error(self):
        array_a = np.array([[1.0, 1.0j], [2.0, 2.0j]])
        mat = Matrix(array=array_a)
        array_b = np.array([[1.0], [1.0j], [1.0]])
        vec = ColumnVector(array=array_b)
        #res = matrix_product(mat, vec)
        # Error: size doesn't match
        self.assertRaises(LinearSpaceAlgebraFunctionError, matrix_product, mat, vec)

    def test_matrix_with_matrix(self):
        array_a = np.array([[1.0, 1.0j], [2.0, 2.0j], [3.0, 3.0j]])
        mata = Matrix(array=array_a)
        array_b = np.array([[1.0, 2.0], [1.0j, 2.0j]])
        matb = SquareMatrix(array=array_b)
        res = matrix_product(mata, matb)
        self.assertTrue(isinstance(res, Matrix))
        self.assertEqual(res.nrows, 3)
        self.assertEqual(res.ncols, 2)
        self.assertEqual(res[0][0], 0.)
        self.assertEqual(res[0][1], 0.)
        self.assertEqual(res[1][1], 0.)
        self.assertEqual(res[2][1], 0.)
        self.assertEqual(res[2][0], 0.)

    def test_matrix_matrix_to_square(self):
        array_a = np.array([[1.0, 1.0j], [2.0, 2.0j], [3.0, 3.0j]])
        mata = Matrix(array=array_a)
        array_b = np.array([[1.0, 2.0, 3.0], [1.0j, 2.0j, 3.0j]])
        matb = Matrix(array=array_b)
        res = matrix_product(mata, matb)
        self.assertTrue(isinstance(res, SquareMatrix))
        self.assertEqual(res.nrows, 3)
        self.assertEqual(res.ncols, 3)
        self.assertEqual(res[0][0], 0.)
        self.assertEqual(res[0][1], 0.)
        self.assertEqual(res[0][2], 0.)
        self.assertEqual(res[1][1], 0.)
        self.assertEqual(res[2][1], 0.)
        self.assertEqual(res[2][0], 0.)
        self.assertEqual(res[2][2], 0.)

    def test_row_vector_with_vector(self):
        array_a = np.array([[1.0, 1.0j]])
        mat = RowVector(array=array_a)
        array_b = np.array([[1.0], [2.0j]])
        vec = ColumnVector(array=array_b)
        res = matrix_product(mat, vec)
        self.assertFalse(isinstance(res, ColumnVector))
        # res is just a number
        self.assertTrue(res == -1.0)

    def test_row_vector_with_vector_error(self):
        array_a = np.array([[1.0, 1.0j, 2.0]])
        mat = RowVector(array=array_a)
        array_b = np.array([[1.0], [2.0j]])
        vec = ColumnVector(array=array_b)
        #res = matrix_product(mat, vec)
        self.assertRaises(LinearSpaceAlgebraFunctionError, matrix_product, mat, vec)
