#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.vector.py

Main test:
    Row vector object

Updated:
    22 April 2021
"""
import unittest
import numpy as np
from linear_space.vector.errors import RowVectorValidationError
from linear_space.vector.row_vector import RowVectorInitValidator, RowVector
from linear_space.linear_object import Row_Like, Column_Like, Matrix_Like


class TestValidator(unittest.TestCase):
    def test_fail_at_matrix_validator(self):
        array = np.array([1,2,3,4])
        validator = RowVectorInitValidator(array=array)
        # Error: not a 2D array, rejected by matrix validator
        self.assertFalse(validator.is_valid)
        #raise validator.report_errors()[0]

    def test_fail_at_row_vector_validator(self):
        array = np.array([[1,2,3],[1,2,4]])
        validator = RowVectorInitValidator(array=array)
        # Error: not a 2D array, rejected by matrix validator
        self.assertFalse(validator.is_valid)
        #raise validator.report_errors()[0]


class TestRowVector(unittest.TestCase):
    def test_fail_validator(self):
        array = np.array([1,2,3,4])
        #rowvec = RowVector(array=array)
        self.assertRaises(RowVectorValidationError, RowVector, array)

    def test_fail_not_1_by_N(self):
        array = np.array([[1,2,3],[1,2,4]])
        #rowvec = RowVector(array=array)
        self.assertRaises(RowVectorValidationError, RowVector, array)

    def test_okay(self):
        array = np.array([[1,2,3]])
        rowvec = RowVector(array=array)


class Test_Linear_Object_Subtypes(unittest.TestCase):
    def test_okay(self):
        array = np.array([[1,2,3]])
        rowvec = RowVector(array=array)
        self.assertTrue(isinstance(rowvec, Row_Like))
        self.assertFalse(isinstance(rowvec, Column_Like))
        self.assertFalse(isinstance(rowvec, Matrix_Like))
