#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.linear_object.types.py

Main test:
    Artificial types created to categorise linear
    objects.

Updated:
    23 September 2021
"""
import unittest
import numpy as np

from linear_space.linear_object.linear_object import LinearObjectError
from linear_space.linear_object.linear_object import LinearObjectValidator
from linear_space.linear_object.linear_object import LinearObject

from linear_space.linear_object.utils import is_column_like, is_row_like, \
    is_matrix_like
from linear_space.linear_object.types import Column_Like, Row_Like, Matrix_Like


class Test_Column_Like(unittest.TestCase):
    def test_okay(self):
        test_array = np.array([[1],[2],[3],[4]])
        lo = LinearObject(array=test_array)
        self.assertTrue(is_column_like(lo))
        self.assertTrue(isinstance(lo, Column_Like))
        self.assertFalse(is_row_like(lo))


class Test_Row_Like(unittest.TestCase):
    def test_okay(self):
        test_array = np.array([[1,2,3,4]])
        lo = LinearObject(array=test_array)
        self.assertFalse(is_column_like(lo))
        self.assertTrue(isinstance(lo, Row_Like))
        self.assertFalse(isinstance(lo, Column_Like))
        self.assertTrue(is_row_like(lo))


class Test_Matrix_Like(unittest.TestCase):
    def test_matrix_like(self):
        test_array = np.array([[1,2,3],[0.1,0.2j,3j]])
        lo = LinearObject(array=test_array)
        self.assertFalse(isinstance(lo, Row_Like))
        self.assertTrue(is_matrix_like(lo))
        self.assertTrue(isinstance(lo, Matrix_Like))
        self.assertFalse(isinstance(lo, Column_Like))
