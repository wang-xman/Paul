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
from linear_space.vector.unit_vector import UnitVector
from linear_space.algebra.decorator import LinearSpaceAlgebraFunctionError
from linear_space.algebra.functions import kronecker


class Test_Kronecker(unittest.TestCase):
    def test_raise_error(self):
        array_a = np.array([[1.0], [1.0j]])
        vec_a = ColumnVector(array=array_a)
        list_b = [1.0, 1.0j]
        #vec = kronecker(vec_a, list_b)
        self.assertRaises(LinearSpaceAlgebraFunctionError, kronecker, vec_a, list_b)

    def test_vector_vector(self):
        array_a = np.array([[1.0], [1.0j]])
        array_b = np.array([[1.0], [1.0j]])
        vec_a = ColumnVector(array=array_a)
        vec_b = ColumnVector(array=array_b)
        vec = kronecker(vec_a, vec_b)
        self.assertTrue(isinstance(vec, ColumnVector))
        self.assertEqual(vec.size, 4)
        self.assertEqual(vec[0], 1)
        self.assertEqual(vec[1], 1j)
        self.assertEqual(vec[2], 1j)
        self.assertEqual(vec[3], -1)

    def test_vector_vector_to_unitvector(self):
        array_a = np.array([[1.0], [1.0j]])/np.sqrt(2.0)
        array_b = np.array([[1.0], [1.0j]])/np.sqrt(2.0)
        vec_a = ColumnVector(array=array_a)
        vec_b = ColumnVector(array=array_b)
        vec = kronecker(vec_a, vec_b)
        self.assertTrue(isinstance(vec, UnitVector))
        self.assertEqual(vec.size, 4)

    def test_row_row(self):
        array_a = np.array([[1.0, 1.0j]])
        array_b = np.array([[1.0, 1.0j]])
        vec_a = RowVector(array=array_a)
        vec_b = RowVector(array=array_b)
        vec = kronecker(vec_a, vec_b)
        #print(vec.as_array())
        self.assertTrue(isinstance(vec, RowVector))
        self.assertEqual(vec.size, 4)

    def test_vector_matrix(self):
        array_a = np.array([[1.0], [1.0j]])
        array_b = np.array([[1.0, 1.0j], [0. - 1.0j, 1.0]])
        vec = ColumnVector(array=array_a)
        mat = SquareMatrix(array=array_b)
        res = kronecker(vec, mat)
        self.assertTrue(isinstance(res, Matrix))
        self.assertEqual(res.nrows, 4)
        self.assertEqual(res.ncols, 2)
        self.assertEqual(res[0][1], 1j)
        self.assertEqual(res[1][0], -1j)
        self.assertEqual(res[2][0], 1j)

    def test_matrix_matrix(self):
        array_a = np.array([[0.5, 0.5j], [-0.5j, 0.5]])
        array_b = np.array([[1.0, 1.0j], [0. - 1.0j, 1.0]])
        mat_a = SquareMatrix(array=array_a)
        mat_b = SquareMatrix(array=array_b)
        res = kronecker(mat_a, mat_b)
        self.assertTrue(isinstance(res, SquareMatrix))
        self.assertEqual(res.nrows, 4)
        self.assertEqual(res.ncols, 4)
        self.assertEqual(res[0][1], 0.5j)
        self.assertEqual(res[1][0], -0.5j)
        self.assertEqual(res[1][2], 0.5)
        self.assertEqual(res[2][0], -0.5j)
        self.assertEqual(res[2][2], 0.5)
        self.assertEqual(res[2][3], 0.5j)
