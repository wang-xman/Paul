#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.matrix.square_matrix.py

Updated:
    25 April 2021
"""
import unittest
import numpy as np

from linear_space.matrix.square_matrix import SquareMatrix, SquareMatrixInitValidator


class TestSquareMatrixValidator(unittest.TestCase):
    def test_non_matrix(self):
        array = np.array([-3, 1, -2, 4])
        validator = SquareMatrixInitValidator(array=array)
        self.assertFalse(validator.is_valid)
        #raise validator.report_errors()[0]

    def test_non_square(self):
        array = np.array([
            [-3, 1, -2, 4],
            [-2, 2, 3, -3],
            [1, -7, 7, -1]
        ])
        validator = SquareMatrixInitValidator(array=array)
        self.assertFalse(validator.is_valid)

    def test_non_square_2(self):
        array = np.array([
            [-3, 1],
            [-2, 2],
            [1, -7]
        ])
        validator = SquareMatrixInitValidator(array=array)
        self.assertFalse(validator.is_valid)


class TestSquareMatrix(unittest.TestCase):
    def test_eigen(self):
        m = np.array([
            [-3, 1, -2, 4],
            [-2, 2, 3, -3],
            [1, -7, 7, -1],
            [3, 0, -1, -2]
        ])
        matrix = SquareMatrix(array=m)
