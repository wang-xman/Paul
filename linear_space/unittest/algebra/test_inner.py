#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    linear_space.algebra.functions.py

Main test:
    Inner product function

Updated:
    23 September 2021
"""
import unittest
import numpy as np

from linear_space.vector.column_vector import ColumnVector
from linear_space.vector.row_vector import RowVector
from linear_space.algebra.functions import inner


class Test_VectorInnerProduct(unittest.TestCase):
    def test_row_col(self):
        array_a = np.array([[1.0, 1.0j]])
        array_b = np.array([[1.0], [1.0j]])
        vec_a = RowVector(array=array_a)
        vec_b = ColumnVector(array=array_b)
        prod = inner(vec_a, vec_b)
        #print()
        self.assertTrue(prod == 0)

    def test_row_row(self):
        array_a = np.array([[1.0, 1.0j]])
        array_b = np.array([[1.0, 1.0j]])
        vec_a = RowVector(array=array_a)
        vec_b = RowVector(array=array_b)
        prod = inner(vec_a, vec_b)
        self.assertTrue(prod == 2)

    def test_col_col(self):
        array_a = np.array([[1.0], [1.0j]])
        array_b = np.array([[1.0], [1.0j]])
        vec_a = ColumnVector(array=array_a)
        vec_b = ColumnVector(array=array_b)
        prod = inner(vec_a, vec_b)
        self.assertTrue(prod == 2)

    def test_col_row(self):
        array_a = np.array([[1.0], [1.0j]])
        array_b = np.array([[1.0, 1.0j]])
        vec_a = ColumnVector(array=array_a)
        vec_b = RowVector(array=array_b)
        prod = inner(vec_a, vec_b)
        self.assertTrue(prod == 0)