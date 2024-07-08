#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    density_matrix.validator.py

Main test:
    Density matrix validator.

Updated:
    26 September 2021
"""
import unittest
import numpy as np

from common import Validation_Error
from linear_space.vector import UnitVector
from quantum_state import QuantumState

from density_matrix.validators import DensityMatrixInitValidator

def error_raiser(validator):
    if not validator.is_valid:
        validator.raise_last_error()


class TestDensityMatrixValidator_SingleState(unittest.TestCase):
    def test_one_state(self):
        vector = UnitVector(array=np.array([[1],[1]]))
        state = QuantumState(vector=vector)
        validator = DensityMatrixInitValidator(state=state)
        # validated state shall be the same as state
        validated_state = validator.validated_data()['state']
        self.assertTrue(state == validated_state)


class TestDensityMatrixValidator_Ensemble(unittest.TestCase):
    def test_single_item(self):
        # Creating a density matrix using one single item in ensemble list
        # is prohibited. In this case, creation shall be done for a pure state.
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        ensemble = [(0.5, state)]
        # Error
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_nontuple_1(self):
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Error: each item shall be tuple
        ensemble = [(0.5, state), state]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_nontuple_2(self):
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Error: each item shall be tuple
        ensemble = [state, state]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_tuple_with_wrong_number_of_elements_1(self):
        vector = UnitVector(array=np.array([[1],[1]]))
        state = QuantumState(vector=vector)
        # Error: each tuple shall have two elements
        ensemble = [(state,), (state,)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_tuple_with_wrong_number_of_elements_2(self):
        vector = UnitVector(array=np.array([[1],[1]]))
        state = QuantumState(vector=vector)
        # Error: probability must be positive
        ensemble = [(state,state), (state,state)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_tuple_with_wrong_number_of_elements_3(self):
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Error: probability must be a positive number
        ensemble = [(state,state), (0.5,state)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_tuple_with_wrong_number_of_elements_4(self):
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Error: probability must be positive number
        ensemble = [(0.5,state), (state,state)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_tuple_with_wrong_number_of_elements_5(self):
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Error: probability must be positive number
        ensemble = [('0.5', state), ('0.5',state)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_tuple_with_wrong_number_of_elements_6(self):
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Error: probability must be positive number
        ensemble = [(-0.5, state), (0.5,state)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_tuple_with_wrong_number_of_elements_7(self):
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Okay: probability is a positive number
        prob = 0.5
        ensemble = [(prob, state), (prob,state)]
        validator = DensityMatrixInitValidator(state=ensemble)


class TestDensityMatrixValidator_EnsembleNonUnityProbability(unittest.TestCase):
    def test_multiple_item(self):        
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Error: probability is a positive number
        prob = 0.6
        ensemble = [(prob, state), (prob,state)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_multiple_item_2(self):        
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        # Okay
        prob = 0.6
        ensemble = [(prob, state), (0.4,state)]
        validator = DensityMatrixInitValidator(state=ensemble)


class TestDensityMatrixValidator_EnsembleMismatchedStateDimension(unittest.TestCase):
    def test_1(self):
        v1 = UnitVector(array=np.array([[1], [1]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[1], [1], [1]]))
        s2 = QuantumState(vector=v2)
        prob = 0.6
        # Error: dimensions are different
        ensemble = [(prob, s1), (0.4,s2)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_2(self):
        v1 = UnitVector(array=np.array([[1], [1]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[1], [1], [1]]))
        s2 = QuantumState(vector=v2)
        prob = 0.6
        # Error: dimensions are different
        ensemble = [(prob, s1), (0.4,s1), (0.4,s2)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)
        #self.assertRaises(Validation_Error, DensityMatrixInitValidator, ensemble)
        #validator = DensityMatrixInitValidator(state=ensemble)

    def test_3(self):
        v1 = UnitVector(array=np.array([[1], [1]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[1], [1], [1]]))
        s2 = QuantumState(vector=v2)
        prob = 0.6
        # Error: there is a negative probability
        ensemble = [(prob, s1), (0.4,s1), (-0.4,s1)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)


class TestDensityMatrixValidator_EnsembleSuccess(unittest.TestCase):
    def test_with_zero_probability(self):
        v1 = UnitVector(array=np.array([[1], [1]]))
        s1 = QuantumState(vector=v1)
        #v2 = UnitVector(array=np.array([1,1,1]))
        #s2 = QuantumState(vector=v2)
        prob = 0.6
        # Okay
        ensemble = [(prob, s1), (0.4, s1), (0, s1)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertTrue(validator.is_valid)

    def test_with_zero_probability_2(self):
        v1 = UnitVector(array=np.array([[1], [1]]))
        s1 = QuantumState(vector=v1)
        #v2 = UnitVector(array=np.array([1,1,1]))
        #s2 = QuantumState(vector=v2)
        # Okay
        ensemble = [(1.0, s1), (0,s1), (0,s1)]
        validator = DensityMatrixInitValidator(state=ensemble)
        valdiated_data = validator.validated_data()['state']
        #print(valdiated_data)

    def test_with_zero_probability_3(self):
        v2 = UnitVector(array=np.array([[1], [1], [1]]))
        s2 = QuantumState(vector=v2)
        # Okay
        ensemble = [(0.5, s2), (0.25,s2), (0.25,s2)]
        validator = DensityMatrixInitValidator(state=ensemble)
