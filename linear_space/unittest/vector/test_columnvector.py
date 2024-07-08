#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_sapce.vector.column_vector.py

Main test:
    Column-like vectors

Updated:
    23 September 2021
"""
import unittest
import numpy as np

from linear_space.linear_object.linear_object import LinearObject
from linear_space.vector.base_vector import BaseVector
from linear_space.vector.column_vector import ColumnVectorInitValidator, \
    ColumnVector, ColumnVectorError
from linear_space.linear_object import Column_Like, Row_Like, Matrix_Like


class Test_ColumnVectorValidator_Error(unittest.TestCase):
    def test_one_row(self):
        test_array = np.array([[1,2]])
        validator = ColumnVectorInitValidator(array=test_array)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_one_row_one_colum(self):
        test_array = np.array([[1]])
        validator = ColumnVectorInitValidator(array=test_array)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])


class Test_ColumnVectorValidator_Okay(unittest.TestCase):
    def test_column_like(self):
        test_array = np.array([[1],[2],[1],[1]])
        validator = ColumnVectorInitValidator(array=test_array)
        self.assertTrue(validator.is_valid)
        va = validator.validated_data()['array']
        #print(va)


class Test_Init(unittest.TestCase):
    def test_type(self):
        test_array = np.array([[1],[2],[1],[1]])
        cv = ColumnVector(array=test_array)
        self.assertTrue(isinstance(cv, BaseVector))
        self.assertTrue(isinstance(cv, LinearObject))


class Test_Size(unittest.TestCase):
    def test_size(self):
        test_array = np.array([[1.j],[2],[0.1j],[1e-10]])
        colv = ColumnVector(array=test_array)
        self.assertTrue(colv.nrows == 4)
        self.assertTrue(colv.ncols == 1)
        self.assertTrue(colv.size == 4)
        self.assertTrue(colv.size == colv.nrows)


class Test_ElementWise(unittest.TestCase):
    def test_element(self):
        test_array = np.array([[1.j],[2],[0.1j],[1e-10]])
        colv = ColumnVector(array=test_array)
        self.assertTrue(colv.element(0) == 1.j)
        self.assertTrue(colv.element(0) == colv.first)
        self.assertTrue(colv.element(3) == colv.last)
        self.assertTrue(colv.element(3) == test_array[3][0])

    def test_index_range(self):
        test_array = np.array([[1.j],[2],[0.1j],[1e-10]])
        colv = ColumnVector(array=test_array)
        self.assertRaises(ColumnVectorError, colv.element, colv.size + 1)

    def test_getitem(self):
        test_array = np.array([[1.j],[2],[0.1j],[1e-10]])
        colv = ColumnVector(array=test_array)
        self.assertTrue(colv.element(0) == colv[0])
        self.assertTrue(colv.element(0) == colv.first)
        self.assertTrue(colv.element(3) == colv[3])
        self.assertTrue(colv.element(3) == test_array[3][0])


class Test_Norm_Normalisation(unittest.TestCase):
    def test_norm(self):
        test_array = np.array([[2],[2],[2],[2]])
        col = ColumnVector(array=test_array)
        self.assertEqual(col.norm, 4)
        self.assertFalse(col.is_normalized)
        newcol = col.normalize()
        self.assertTrue(newcol.is_normalized)


class Test_Equal(unittest.TestCase):
    def test_equal(self):
        test_array = np.array([[2],[2],[2],[2]])
        test_array_2 = np.array([[0.5],[0.5],[0.5],[0.5]])
        col1 = ColumnVector(array=test_array)
        col2 = ColumnVector(array=test_array_2)
        self.assertFalse(col1 == col2)
        self.assertTrue(col1.normalize() == col2)

    def test_different_type(self):
        test_array = np.array([[2],[2],[2],[2]])
        test_array_2 = np.array([[0.5],[0.5],[0.5],[0.5]])
        col1 = ColumnVector(array=test_array)
        col2 = LinearObject(array=test_array_2)
        self.assertRaises(ColumnVectorError, col1.is_equal_to, col2)


class Test_Linear_Object_Subtype(unittest.TestCase):
    def test_okay(self):
        test_array = np.array([[2],[2],[2],[2]])
        #test_array_2 = np.array([[0.5],[0.5],[0.5],[0.5]])
        col1 = ColumnVector(array=test_array)
        self.assertTrue(isinstance(col1, Column_Like))
        self.assertFalse(isinstance(col1, Row_Like))
        self.assertFalse(isinstance(col1, Matrix_Like))
