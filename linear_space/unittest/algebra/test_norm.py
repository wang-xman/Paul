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
from linear_space.algebra.functions import norm, LSAFE


class Test_Norm(unittest.TestCase):
    def test_non_flat(self):
        lst = [[1, 1, 2.0]]
        self.assertRaises(LSAFE, norm, lst)

    def test_wrong_type(self):
        lst = ['a', 1, 2.0]
        self.assertRaises(LSAFE, norm, lst)

    def test_2d_array(self):
        array = np.array([[1,2,3,4]])
        # Error: 2D array
        self.assertRaises(LSAFE, norm, array)
