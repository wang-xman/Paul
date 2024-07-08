"""
File under test:
    quantum_state.algebra.py

Main test:
    Quantum state addition.

Updated:
    25 September 2021
"""
import unittest
import numpy as np
from linear_space.vector import ColumnVector

from quantum_state.null_state import NullState, NULL_STATE
from quantum_state.quantum_state import QuantumState
from quantum_state.superposition import QuantumSuperposition

from quantum_state.algebra import QuantumStateAlgebraFunctionError, state_add, state_scale


class Test_Add_States(unittest.TestCase):
    def test_state_state_addition(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # this is a superposition
        state3 = state_add(state1, state2)
        self.assertTrue(isinstance(state3, QuantumSuperposition))
        # still the same state.
        self.assertTrue(state3.as_state() == state1)


class Test_Add_Superpositions(unittest.TestCase):
    def test_state_sp_addition(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # this is a superposition
        state3 = state_add(state1, state_scale(2.0, state2))
        self.assertTrue(isinstance(state3, QuantumSuperposition))
        # still the same state.
        self.assertTrue(state3.as_state() == state1)


class Test_Add_State_Superposition(unittest.TestCase):
    def test_sp_and_state_addition(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # this is a superposition,
        # see addition rules of quantum state
        state3 = state_add(state_scale(2.0, state1), state2)
        self.assertTrue(isinstance(state3, QuantumSuperposition))
        # still the same state.
        self.assertTrue(state3.as_state() == state1)


class Test_Add_Null(unittest.TestCase):
    def test_null_and_state(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # still state2
        state3 = state_add(NULL_STATE, state2)
        self.assertTrue(isinstance(state3, QuantumState))
        # still the same state.
        self.assertTrue(state3 == state1)

    def test_state_and_null(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # still state2
        state3 = state_add(state2, NULL_STATE)
        self.assertTrue(isinstance(state3, QuantumState))
        # still the same state.
        self.assertTrue(state3 == state1)

    def test_sp_and_null(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        sp = QuantumSuperposition(superlist=[(1.0, state1), (1.0, state2)])
        # still sp
        state3 = state_add(sp, NULL_STATE)
        self.assertTrue(isinstance(state3, QuantumSuperposition))
        # still the same state.
        self.assertTrue(state3 == sp)

    def test_null_and_sp(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        sp = QuantumSuperposition(superlist=[(1.0, state1), (1.0, state2)])
        # still sp
        state3 = state_add(NULL_STATE, sp)
        self.assertTrue(isinstance(state3, QuantumSuperposition))
        # still the same state.
        self.assertTrue(state3 == sp)

    def test_null_and_null(self):
        state3 = state_add(NULL_STATE, NULL_STATE)
        self.assertTrue(isinstance(state3, NullState))


class Test_Errors(unittest.TestCase):
    def test_sp_with_wrong_types(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        sp = QuantumSuperposition(superlist=[(1.0, state1), (1.0, state2)])
        # Error
        #state3 = state_add(sp, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_add, sp, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_add, sp, 0.5)

    def test_state_with_wrong_types(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # Error
        #state3 = state_add(sp, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_add, state1, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_add, state1, 10)

    def test_null_with_wrong_types(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        # Error
        #state3 = state_add(sp, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_add, NULL_STATE, vector)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_add, NULL_STATE, 10)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_add, vector, NULL_STATE)
        self.assertRaises(QuantumStateAlgebraFunctionError, state_add, '10', NULL_STATE)
