"""
Module under test:
    quantum_operator.quantum_operators.py

Main test:
    Quantum operator initialisation

Updated:
    29 April 2021
"""
import unittest
import numpy as np

from common.exception import Validation_Error
from linear_space.matrix import SquareMatrix
from quantum_operator.quantum_operators import QuantumOperator


class TestInit(unittest.TestCase):
    def test_init_success(self):
        array = np.array([[1.0, 0.0],[0.0, 1.0]])
        matrix = SquareMatrix(array=array)
        operator = QuantumOperator(matrix=matrix)

    def test_init_fail(self):
        array = np.array([[1.0],[0.0]])
        # NOTE Cause by vector validation, not operator
        self.assertRaises(Validation_Error, SquareMatrix, array)


class TestInternalMatrix(unittest.TestCase):
    array = np.array([[1.0, 0.0],[0.0, 1.0]])
    default_matrix = SquareMatrix(array=array)

    def test_as_matrix(self):
        operator = QuantumOperator(matrix=self.default_matrix)
        self.assertTrue(operator.as_matrix() == self.default_matrix)

    def test_empty(self):
        operator = QuantumOperator()
        self.assertFalse(operator.has_matrix())
        self.assertTrue(operator.as_matrix() is None)
        operator.update_matrix(self.default_matrix)
        self.assertTrue(operator.has_matrix())
        self.assertFalse(operator.as_matrix() is None)
        self.assertTrue(operator.as_matrix() == self.default_matrix)
