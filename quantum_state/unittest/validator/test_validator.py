#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    state.validator.py

Main test:
    Quantum state vector validation.

Updated:
    25 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector, UnitVector
from quantum_state.validators import QuantumStateVectorValidator


class Test_QuantumStateVectorValidator(unittest.TestCase):
    def test_vector_type_error(self):
        # Fail: array doesn't work, must be a Vector instance
        test_array = np.array([[1], [2]])
        validator = QuantumStateVectorValidator(vector=test_array)
        self.assertFalse(validator.is_valid)
        #self.assertRaises(QuantumStateValidationError, QuantumStateValidator,
        #                  test_array)

    def test_vector_type_right(self):
        # Pass:
        test_array = np.array([[1], [2]])
        test_vector = ColumnVector(array=test_array)
        obj = QuantumStateVectorValidator(vector=test_vector)

    def test_no_vector_given(self):
        # Error: no vector given
        test_vector = None
        validator = QuantumStateVectorValidator(vector=test_vector)
        self.assertFalse(validator.is_valid)
        #self.assertRaises(QuantumStateValidationError,QuantumStateValidator,
        #                  test_vector)

    def test_validated_vector(self):
        # Fail: validated vector should be a unit vector
        test_vector = ColumnVector(array=np.array([[1.0], [0.5]]))
        test_obj = QuantumStateVectorValidator(vector=test_vector)
        validated_vector = test_obj.validated_data()['vector']
        self.assertFalse(test_vector == validated_vector)
        self.assertTrue(isinstance(validated_vector, UnitVector))
