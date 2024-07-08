"""
Module under test:
    quantum_operator.generic.py

Main test:
    Quantum operator apply method

Updated:
    29 April 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector
from linear_space.matrix import SquareMatrix
from quantum_state import QuantumState, NullState
from qubit import QubitState
from quantum_operator.quantum_operators import QuantumOperator, QuantumOperatorError


class TestQuantumOperator_apply(unittest.TestCase):

    def test_on_state(self):
        vector = ColumnVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # identity operator
        marray = np.array([[1.0, 0.0],[0.0, 1.0]])
        matrix = SquareMatrix(array=marray)
        operator = QuantumOperator(matrix=matrix)
        new_state = operator.apply(state)
        self.assertTrue(isinstance(new_state, QuantumState))
        self.assertTrue(new_state == state)

    def test_on_state_mismatched_dimension(self):
        vector = ColumnVector(array=np.array([[1],[1],[1]]))
        state = QuantumState(vector=vector)
        marray = np.array([[1.0, 0.0], [0.0, 1.0]])
        matrix = SquareMatrix(array=marray)
        operator = QuantumOperator(matrix=matrix)
        self.assertRaises(QuantumOperatorError, operator.apply, state)

    def test_on_zerostate(self):
        zs = NullState()
        marray = np.array([[1.0, 0.0],[0.0, 1.0]])
        matrix = SquareMatrix(array=marray)
        operator = QuantumOperator(matrix=matrix)
        # Operating on a zero state gives a zero state.
        ns = operator.apply(zs)
        self.assertTrue(isinstance(ns, NullState))


class TestQubitState(unittest.TestCase):
    vector = ColumnVector(array=np.array([[1], [1]]))
    qubit_state = QubitState(vector=vector)

    def test_resulting_state_type(self):
        # identity operator
        marray = np.array([[1.0, 0.0],[0.0, 1.0]])
        matrix = SquareMatrix(array=marray)
        operator = QuantumOperator(matrix=matrix)
        res = operator.apply(self.qubit_state)
        # NOTE Returned type is not qubit state
        self.assertFalse(isinstance(res, QubitState))
        self.assertTrue(isinstance(res, QuantumState))
        self.assertTrue(res == self.qubit_state)
