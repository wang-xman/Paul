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
from linear_space.vector.row_vector import RowVector
from linear_space.algebra.functions import outer


class Test_VectorOuterProduct(unittest.TestCase):
    def test_equal_length(self):
        array_a = np.array([[1.0], [1.0j]])
        array_b = np.array([[1.0], [1.0j]])
        vec_a = ColumnVector(array=array_a)
        vec_b = ColumnVector(array=array_b)
        mat = outer(vec_a, vec_b)
        self.assertTrue(isinstance(mat, SquareMatrix))
        self.assertEqual(mat[0][0], 1)
        self.assertEqual(mat[0][1], -1.0j)
        self.assertEqual(mat[1][0], 1.0j)
        self.assertEqual(mat[1][1], 1.0)

    def test_nonequal_length(self):
        array_a = np.array([[1.0], [2.0j]])
        array_b = np.array([[1.0], [2.0j], [3.0]])
        vec_a = ColumnVector(array=array_a)
        vec_b = ColumnVector(array=array_b)
        mat = outer(vec_a, vec_b)
        self.assertFalse(isinstance(mat, SquareMatrix))
        self.assertEqual(mat.nrows, 2)
        self.assertEqual(mat.ncols, 3)
        # element
        self.assertEqual(mat[0][0], 1)
        self.assertEqual(mat[0][1], -2.0j)
        self.assertEqual(mat[1][0], 2.0j)
        self.assertEqual(mat[1][2], 6.0j)

    def test_row_and_column(self):
        array_a = np.array([[1.0, 1.0j]])
        array_b = np.array([[1.0], [1.0j]])
        vec_a = RowVector(array=array_a)
        vec_b = ColumnVector(array=array_b)
        mat = outer(vec_a, vec_b)
        self.assertTrue(isinstance(mat, SquareMatrix))
        self.assertEqual(mat[0][0], 1)
        self.assertEqual(mat[0][1], -1.0j)
        self.assertEqual(mat[1][0], -1.0j)
        self.assertEqual(mat[1][1], -1.0)

    def test_row_and_row(self):
        array_a = np.array([[1.0, 1.0j]])
        array_b = np.array([[1.0, 1.0j]])
        vec_a = RowVector(array=array_a)
        vec_b = RowVector(array=array_b)
        mat = outer(vec_a, vec_b)
        self.assertTrue(isinstance(mat, SquareMatrix))
        self.assertEqual(mat[0][0], 1)
        self.assertEqual(mat[0][1], 1.0j)
        self.assertEqual(mat[1][0], -1.0j)
        self.assertEqual(mat[1][1], 1.0)

    def test_nonequal_length_row_row(self):
        array_a = np.array([[1.0, 2.0j]])
        array_b = np.array([[1.0, 2.0j, 3.0]])
        vec_a = RowVector(array=array_a)
        vec_b = RowVector(array=array_b)
        mat = outer(vec_a, vec_b)
        self.assertFalse(isinstance(mat, SquareMatrix))
        self.assertEqual(mat.nrows, 2)
        self.assertEqual(mat.ncols, 3)
        # element
        self.assertEqual(mat[0][0], 1)
        self.assertEqual(mat[0][1], 2.0j)
        self.assertEqual(mat[1][0], -2.0j)
        self.assertEqual(mat[1][2], -6.0j)
