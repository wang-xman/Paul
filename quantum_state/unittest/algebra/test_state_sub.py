"""
File under test:
    quantum_state.algebra.py

Main test:
    Quantum state subtraction

Updated:
    25 September 2021
"""
import unittest
import numpy as np
from linear_space.vector import ColumnVector

from quantum_state.null_state import NullState, NULL_STATE
from quantum_state.quantum_state import QuantumState
from quantum_state.superposition import QuantumSuperposition

from quantum_state.algebra import QuantumStateAlgebraFunctionError, state_sub, state_scale


class TestQuantumState_StateSubtraction(unittest.TestCase):
    def test_state_state_subtraction(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # this is a superposition,
        # see addition rules of quantum state
        sp3 = state_sub(state1, state2)
        self.assertTrue(isinstance(sp3, QuantumSuperposition))
        # null state
        self.assertTrue(isinstance(sp3.as_state(), NullState))

    def test_sp_state_subtraction(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # this is a superposition,
        # see addition rules of quantum state
        sp3 = state_sub(state_scale(3.0, state1), state2)
        self.assertTrue(isinstance(sp3, QuantumSuperposition))
        self.assertTrue(sp3.as_state() == state1)

    def test_state_sp_subtraction(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # this is a superposition,
        # see addition rules of quantum state
        sp3 = state_sub(state1, state_scale(2.0, state2))
        self.assertTrue(isinstance(sp3, QuantumSuperposition))
        self.assertTrue(sp3.as_state() == state1)

    def test_state_sp_subtraction_2(self):
        vector1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        vector2 = ColumnVector(array=np.array([[3.0], [4.0]]))
        state1 = QuantumState(vector=vector1)
        state2 = QuantumState(vector=vector2)
        # this is a superposition,
        # see addition rules of quantum state
        sp3 = state_sub(state1, state_scale(2.0, state2))
        self.assertTrue(isinstance(sp3, QuantumSuperposition))
        self.assertFalse(sp3.as_state() == state1)
        self.assertFalse(sp3.as_state() == state2)


class Test_Errors(unittest.TestCase):
    def test_sp_with_wrong_types(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        sp = QuantumSuperposition(superlist=[(1.0, state1), (1.0, state2)])
        # Error
        self.assertRaises(QuantumStateAlgebraFunctionError, state_sub, sp, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_sub, sp, 0.5)

    def test_state_with_wrong_types(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # Error
        self.assertRaises(QuantumStateAlgebraFunctionError, state_sub, state1, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_sub, state1, 10)

    def test_null_with_wrong_types(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # Error
        self.assertRaises(QuantumStateAlgebraFunctionError, state_sub, NULL_STATE, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_sub, NULL_STATE, 10)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_sub, vector, NULL_STATE)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_sub, '10', NULL_STATE)
