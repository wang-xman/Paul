#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.matrix.matrix.py

Main test:
    Matrix validator

Updated:
    23 September 2021
"""
import unittest
import numpy as np

from linear_space.matrix.matrix import MatrixInitValidator


class Test_MatrixValidator(unittest.TestCase):
    def test_valid(self):
        array = np.array([[1.0, 2.0, 3], [3,4,5]])
        validator = MatrixInitValidator(array=array)
        self.assertTrue(validator.is_valid)

    def test_invalid_1d_array(self):
        array = np.array([1.0, 2.0, 3])
        validator = MatrixInitValidator(array=array)
        # Error: 1D numpy array
        self.assertFalse(validator.is_valid)

    def test_invalid_row_like(self):
        array = np.array([[1.0, 2.0, 3]])
        validator = MatrixInitValidator(array=array)
        # Error: row-like array
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)

    def test_invalid_column_like(self):
        array = np.array([[1.0], [2.0], [3]])
        validator = MatrixInitValidator(array=array)
        # Error: column-like array
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)
