"""
File under test:
    state.quantum_state.py

Updated:
    27 April 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector, UnitVector
from linear_space.algebra import scale
from quantum_state.errors import QuantumStateError
from quantum_state.quantum_state import QuantumState


class Test_QuantumState_CompareStates(unittest.TestCase):
    """ Test method `is_equal_to` of a state """
    def test_compare_states(self):
        vector = ColumnVector(array=np.array([[2.0], [1.0], [1.j], [4.0]]))
        state = QuantumState(vector=vector)
        self.assertTrue(isinstance(state.as_vector(), UnitVector))
        factor = 1+2.j
        scaled_vector = scale(factor, vector)
        new_state = QuantumState(vector=scaled_vector)
        self.assertTrue(isinstance(new_state.as_vector(), UnitVector))
        # two states are identical
        self.assertTrue(new_state == state)
        # but two vectors are not the same
        self.assertFalse(new_state.as_vector() == state.as_vector())

    def test_is_equal_to(self):
        vector = ColumnVector(array=np.array([[2.0], [1.0], [1.j], [4.0]]))
        state = QuantumState(vector=vector)
        factor = 1+2.j
        scaled_vector = scale(factor, vector)
        new_state = QuantumState(vector=scaled_vector)
        # two states are identical
        self.assertTrue(new_state.is_equal_to(state))
        # but two vectors are not the same
        self.assertFalse(new_state.as_vector() == state.as_vector())

    def test_is_equal_to_with_nonstate(self):
        vector = ColumnVector(array=np.array([[2.0], [1.0], [1.j], [4.0]]))
        state = QuantumState(vector=vector)
        factor = 1+2.j
        scaled_vector = scale(factor, vector)
        new_state = QuantumState(vector=scaled_vector)
        self.assertTrue(new_state.is_equal_to(state))
        # Error: only compares states
        self.assertRaises(QuantumStateError, new_state.is_equal_to, vector)
        self.assertRaises(QuantumStateError, new_state.__eq__, vector)
