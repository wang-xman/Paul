#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.vector.unit_vector.py

Main test:
    Basic properties of unit vector.

Updated:
    23 September 2021
"""
import unittest
import numpy as np
from linear_space.vector.errors import VectorValidationError
from linear_space.vector.unit_vector import UnitVector



class Test_UnitVector(unittest.TestCase):
    def test_one_element(self):
        test_array = np.array([[0.5]])
        #vector = UnitVector(array=test_array)
        # Error: this is a scalar
        self.assertRaises(VectorValidationError, UnitVector, test_array)

    def test_initialisation_success(self):
        test_array = np.array([[0.5], [0.5], [0.5], [0.5],
                               [0.5], [0.5], [0.5], [0.5]])
        vector = UnitVector(array=test_array)
        self.assertTrue(vector.is_normalized)


class Test_Element(unittest.TestCase):
    def test_element(self):
        test_array = np.array([[0.5], [0.5], [0.5], [0.5]])
        vector = UnitVector(array=test_array)
        self.assertEqual(vector.element(1), 0.5)
        self.assertEqual(vector.element(2), 0.5)

    def test_size(self):
        test_array = np.array([[0.5], [0.5], [0.5], [0.5], [0.5], [0.5]])
        vector = UnitVector(array=test_array)
        self.assertEqual(vector.size, 6)
