#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    linear_space.algebra.functions.py

Main test:
    Scale function

Updated:
    28 September 2021
"""
import unittest
import numpy as np
from linear_space.vector import ColumnVector, RowVector, UnitVector
from linear_space.matrix import SquareMatrix, IdentityMatrix, Matrix

from linear_space.algebra.functions import scale


class Test_Scale_Vector(unittest.TestCase):
    def test_col(self):
        factor = 0.5
        array_b = np.array([[1.0], [1.0j]])
        vec_b = ColumnVector(array=array_b)
        nvec = scale(factor, vec_b)
        self.assertTrue(isinstance(nvec, ColumnVector))
        self.assertTrue(nvec[1] == 0.5j)

    def test_row(self):
        factor = 10.0
        array_a = np.array([[1.0, 1.0j]])
        vec_a = RowVector(array=array_a)
        nvec = scale(factor, vec_a)
        self.assertTrue(isinstance(nvec, RowVector))
        self.assertTrue(nvec[1] == 10.0j)

    def test_unit_vector(self):
        factor = 1.0
        array_a = np.array([[1.0], [1.0j]])
        vec_a = UnitVector(array=array_a)
        nvec = scale(factor, vec_a)
        self.assertTrue(isinstance(nvec, UnitVector))

    def test_unit_vector_with_not_1(self):
        factor = 0.9
        array_a = np.array([[1.0], [1.0j]])
        vec_a = UnitVector(array=array_a)
        nvec = scale(factor, vec_a)
        self.assertFalse(isinstance(nvec, UnitVector))
        self.assertTrue(isinstance(nvec, ColumnVector))


class Test_Scale_Matrix(unittest.TestCase):
    def test_nonsquare_matrix(self):
        factor = 0.5
        array_a = np.array([[1.0, 1.0j], [2.0, 2.0j], [3.0, 3.0j]])
        mata = Matrix(array=array_a)
        res = scale(factor, mata)
        self.assertTrue(isinstance(res, Matrix))
        self.assertEqual(res.nrows, 3)
        self.assertEqual(res.ncols, 2)
        self.assertEqual(res[0][0], 0.5)
        self.assertEqual(res[0][1], 0.5j)
        self.assertEqual(res[1][1], 1.j)
        self.assertEqual(res[2][1], 1.5j)
        self.assertEqual(res[2][0], 1.5)

    def test_square_matrix(self):
        factor = 1.0
        array_b = np.array([[1.0, 2.0], [1.0j, 2.0j]])
        matb = SquareMatrix(array=array_b)
        res = scale(factor, matb)
        self.assertTrue(isinstance(res, Matrix))
        self.assertTrue(isinstance(res, SquareMatrix))
        self.assertEqual(res.nrows, 2)
        self.assertEqual(res.ncols, 2)
        self.assertEqual(res[0][0], 1.)
        self.assertEqual(res[0][1], 2.)
        self.assertEqual(res[1][0], 1.j)
        self.assertEqual(res[1][1], 2.j)

    def test_identity_matrix(self):
        factor = 1.0
        idm = IdentityMatrix(row_size=3)
        res = scale(factor, idm)
        self.assertTrue(isinstance(res, IdentityMatrix))

    def test_identity_matrix_not_1(self):
        factor = 0.97
        idm = IdentityMatrix(row_size=3)
        res = scale(factor, idm)
        self.assertFalse(isinstance(res, IdentityMatrix))
        self.assertTrue(isinstance(res, SquareMatrix))
        self.assertEqual(res[0][0], 0.97)
        self.assertEqual(res[1][1], 0.97)
        self.assertEqual(res[2][2], 0.97)
