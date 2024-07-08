"""
File under test:
    quantum_state.algebra.py

Main test:
    State scaling function

Updated:
    25 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector

from quantum_state.null_state import NullState, NULL_STATE
from quantum_state.quantum_state import QuantumState
from quantum_state.superposition import QuantumSuperposition

from quantum_state.algebra import QuantumStateAlgebraFunctionError, state_scale


class Test_with_QuantumState(unittest.TestCase):
    def test_scale_state(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        factor = 0.5
        # scale into a superposition
        ns = state_scale(factor, state1)
        self.assertTrue(isinstance(ns, QuantumSuperposition))
        # same vector
        self.assertTrue(ns.as_state().as_vector() == state1.as_vector())

    def test_scale_null_state(self):
        factor = 0.5
        # still null
        ns = state_scale(factor, NULL_STATE)
        self.assertTrue(isinstance(ns, NullState))

    def test_factor_zero(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        factor = 0.0
        # scale into null
        ns = state_scale(factor, state1)
        self.assertTrue(isinstance(ns, NullState))


class Test_Non_Numeric_Factor(unittest.TestCase):
    def test_non_numeric(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        factor = '1'
        # Error: factor not number
        self.assertRaises(QuantumStateAlgebraFunctionError, state_scale, factor, state1)

    def test_non_numeric_1(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        factor = np.array([[1]]) # scalar like
        # Error: factor not number
        self.assertRaises(QuantumStateAlgebraFunctionError, state_scale, factor, state1)


class Test_Non_State(unittest.TestCase):
    def test_non_state(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        factor = 1
        #state_scale(factor, vector)
        # Error: only for state
        self.assertRaises(QuantumStateAlgebraFunctionError, state_scale, factor, vector)


class Test_Superposition(unittest.TestCase):
    def test_okay(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        state2 = QuantumState(vector=vector)
        factor = 0.5
        # a superposition
        sp = QuantumSuperposition(superlist=[(1.0, state1,), (1.0, state2,)])
        scaled = state_scale(factor, sp)
        self.assertTrue(isinstance(scaled, QuantumSuperposition))
        self.assertTrue(scaled.as_superlist()[0][0] == 0.5)
        self.assertTrue(scaled.as_superlist()[1][0] == 0.5)
        # still the same state.
        self.assertTrue(scaled.as_state() == state1)
