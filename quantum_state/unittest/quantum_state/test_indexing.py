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
from common import Generic_Error
from linear_space.vector import ColumnVector
from quantum_state.quantum_state import QuantumState, QuantumStateError


class TestQuantumState_GetItem(unittest.TestCase):
    def test_get_item(self):
        test_vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        self.assertEqual(state[0], 0.5)

    def test_get_item_out_of_range(self):
        test_vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        def get_item(index):
            return state[index]
        # index of range.
        self.assertRaises(Generic_Error, get_item, 10)
