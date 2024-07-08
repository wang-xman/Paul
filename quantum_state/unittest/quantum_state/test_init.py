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
from common import Validation_Error, Generic_Error
from linear_space.vector import ColumnVector, UnitVector

from quantum_state.quantum_state import QuantumState



class TestQuantumState_Init(unittest.TestCase):
    def test_instantiation_with_unitvector(self):
        # Pass:
        test_vector = UnitVector(array=np.array([[1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        self.assertTrue(isinstance(state.as_vector(), UnitVector))

    def test_instantiation_with_zerovector(self):
        # Fail: error is triggered at the stage of making unit vector
        try:
            test_vector = UnitVector(array=np.array([[0.0], [0.0]]))
            state = QuantumState(vector=test_vector)
            self.assertTrue(isinstance(state.as_vector(), UnitVector))
        except Generic_Error as e:
            pass
            #print(e.full_message)

    def test_instantiation_with_vector(self):
        # Pass: 
        test_vector = ColumnVector(array=np.array([[1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        self.assertTrue(isinstance(state.as_vector(),UnitVector))

    def test_instantiation_with_array(self):
        # Error: init with array is not allowed
        self.assertRaises(Validation_Error, QuantumState, np.array([1.0, 1.0]))

    def test_instantiation_with_list(self):
        # Error: init with list is not allowed
        test = [0,1,1]
        self.assertRaises(Validation_Error, QuantumState, test)

    def test_instantiation_with_number(self):
        # Error: init with number is not allowed
        test = 105
        self.assertRaises(Validation_Error, QuantumState, test)

    def test_instantiation_with_string(self):
        # Error: init with number is not allowed
        test = '105'
        self.assertRaises(Validation_Error, QuantumState, test)
