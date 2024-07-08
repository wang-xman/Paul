#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    quantum_state.quantum_state.py

Updated:
    25 September 2021
"""
import unittest
import numpy as np
from linear_space.vector import ColumnVector
from quantum_state.quantum_state import QuantumState



class TestQuantumState_Representation(unittest.TestCase):    
    def test_string_representation(self):
        v1 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        s1str = s1.string_representation()
        print(s1)

    def test_as_list(self):
        # init vector is not normalised
        v1 = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        # normalised list
        expected_list = [0.5, 0.5, 0.5, 0.5]
        self.assertEqual(s1.as_list(), expected_list)
        self.assertTrue(isinstance(s1.as_list(), list))

    def test_amplitude_list(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        s1.normalize()
        expected_list = [0.5, 0.5, 0.5, 0.5]
        self.assertTrue(s1.amplitude_list == expected_list)
