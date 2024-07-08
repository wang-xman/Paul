#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.matrix.identity_matrix.py

Updated:
    23 September 2021
"""
import unittest
from linear_space.matrix.identity_matrix import IdentityMatrix
from linear_space.matrix.errors import MatrixInitValidationError


class TestIdentityMatrix(unittest.TestCase):
    def test_success(self):
        size = 3
        idm = IdentityMatrix(row_size=size)
        self.assertTrue(idm.size == (3,3))

    def test_wrong_row_size_type(self):
        size = 'a'
        # Error: row size is not an integer
        #IdentityMatrix(row_size=size)
        self.assertRaises(MatrixInitValidationError, IdentityMatrix, size)

    def test_row_size_too_short(self):
        size = 1
        # Error: row size smaller than 2
        #IdentityMatrix(row_size=size)
        self.assertRaises(MatrixInitValidationError, IdentityMatrix, size)
