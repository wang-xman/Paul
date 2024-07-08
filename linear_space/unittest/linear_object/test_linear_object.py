#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.linear_object.linear_object.py

Main test:
    Instantiation and basic properties of linear object

Updated:
    23 September 2021
"""
import unittest
import numpy as np

from linear_space.linear_object.linear_object import LinearObjectError
from linear_space.linear_object.linear_object import LinearObjectValidator
from linear_space.linear_object.linear_object import LinearObject


class Test_AnEmptyArray(unittest.TestCase):
    def test_subarray_empty(self):
        test_array = np.array([[ ]])
        validator = LinearObjectValidator(array=test_array)
        #print(len(test_array))
        #print(len(test_array[0]))
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_subarray_empty_2(self):
        test_array = np.array([[],[1]])
        validator = LinearObjectValidator(array=test_array)
        self.assertFalse(validator.is_valid)


class Test_Validator(unittest.TestCase):
    def test_with_list(self):
        test_array = [1,2,3,4]
        validator = LinearObjectValidator(array=test_array)
        self.assertFalse(validator.is_valid)
        #raise validator.report_errors()[0]

    def test_with_tuple(self):
        test_array = (1,2,3,4,)
        validator = LinearObjectValidator(array=test_array)
        self.assertFalse(validator.is_valid)
        #raise validator.report_errors()[0]

    def test_1d_array(self):
        test_array = np.array([1,2,3,4])
        validator = LinearObjectValidator(array=test_array)
        self.assertFalse(validator.is_valid)
        #raise validator.get_errors()[0]

    def test_3d_array(self):
        test_array = np.array([[[1,2,3,4]]])
        validator = LinearObjectValidator(array=test_array)
        self.assertFalse(validator.is_valid)
        #raise validator.report_errors()[0]

    def test_2d_array(self):
        test_array = np.array([[1,2,3,4]])
        validator = LinearObjectValidator(array=test_array)
        # Okay
        self.assertTrue(validator.is_valid)


class Test_Dimension(unittest.TestCase):
    def test_init(self):
        test_array = np.array([[1,2,3,4]])
        lo = LinearObject(array=test_array)

    def test_dimension(self):
        test_array = np.array([[1,2,3,4]])
        lo = LinearObject(array=test_array)
        self.assertEqual(lo.get_dimension(), 2)
        self.assertEqual(lo.get_dim(), 2)

    def test_row_like(self):
        test_array = np.array([[1,2,3,4]])
        lo = LinearObject(array=test_array)
        self.assertEqual(lo.get_nrows(), 1)
        self.assertEqual(lo.get_ncols(), 4)

    def test_col_like(self):
        test_array = np.array([[1],[2],[3],[4]])
        lo = LinearObject(array=test_array)
        self.assertEqual(lo.get_ncols(), 1)
        self.assertEqual(lo.get_nrows(), 4)

    def test_matrix_like(self):
        test_array = np.array([[1,2,3],[1,2,3]])
        lo = LinearObject(array=test_array)
        self.assertEqual(lo.get_size(), (2,3))
        self.assertEqual(lo.get_nrows(), 2)
        self.assertEqual(lo.get_ncols(), 3)


class Test_Indexing(unittest.TestCase):
    def test_index_row_like(self):
        test_array = np.array([[1,2,3,4]])
        lo = LinearObject(array=test_array)
        # row
        self.assertFalse(lo.is_valid_row_index(1))
        self.assertFalse(lo.is_valid_row_index(3))
        self.assertTrue(lo.is_valid_row_index(0))
        # column
        self.assertTrue(lo.is_valid_column_index(1))
        self.assertTrue(lo.is_valid_column_index(3))
        self.assertFalse(lo.is_valid_column_index(5))
        self.assertFalse(lo.is_valid_column_index(4))

    def test_index_col_like(self):
        test_array = np.array([[1],[2],[3],[4]])
        lo = LinearObject(array=test_array)
        self.assertTrue(lo.is_valid_row_index(1))
        self.assertTrue(lo.is_valid_row_index(3))
        self.assertTrue(lo.is_valid_row_index(0))
        self.assertFalse(lo.is_valid_row_index(4))
        # column
        self.assertTrue(lo.is_valid_column_index(0))
        self.assertFalse(lo.is_valid_column_index(3))
        self.assertFalse(lo.is_valid_column_index(5))
        self.assertFalse(lo.is_valid_column_index(4))

    def test_matrix_like(self):
        test_array = np.array([[1,2,3],[0.1,0.2j,3j]])
        lo = LinearObject(array=test_array)
        self.assertEqual(lo.get_element(0,1), 2)
        self.assertEqual(lo.get_element(1,1), 0.2j)
