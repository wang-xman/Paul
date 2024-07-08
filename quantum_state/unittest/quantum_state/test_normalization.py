#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    state.quantum_state.py

Updated:
    27 April 2021
"""
import unittest
import numpy as np
from linear_space.vector import ColumnVector
from quantum_state.quantum_state import QuantumState


class TestQuantumState_Normalisation(unittest.TestCase):
    def test_state_normalisation(self):
        # Pass
        test_vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        self.assertTrue(state.is_normalized)
        state.normalize()
        self.assertTrue(state.is_normalized)
        self.assertTrue(test_vector.normalize() == state.normalize().vector)
        normalised_vector = ColumnVector(array=np.array([[0.5], [0.5], [0.5], [0.5]]))
        self.assertTrue(state.vector == normalised_vector)
