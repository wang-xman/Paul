#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Gate under test:
    Phase rotation

File under test:
    gate.single.py

Updated:
    23 July 2021
"""
import unittest
import numpy as np

from linear_space.vector import UnitVector
from qubit import QubitState, SingleQubitBasis
from gate.base import GateBaseError
from gate import single_qubit_gates as singles


class TestPhaseRotation_with_DefaultValues(unittest.TestCase):
    gate = singles['PhaseRotation']

    def test_with_default_values(self):
        test_state = SingleQubitBasis(bitstring='0')
        new_state = self.gate(input_state=test_state)
        exp_state = QubitState(vector=UnitVector(array=np.array([[1],[0]])))
        self.assertTrue(new_state == exp_state)

    def test_with_default_values_2(self):
        test_state = SingleQubitBasis(bitstring='1')
        new_state = self.gate(input_state=test_state)
        exp_state = QubitState(vector=UnitVector(array=np.array([[0], [-1.0]])))
        self.assertTrue(new_state == exp_state)


class TestPhaseRotation_with_UserProvidedValues(unittest.TestCase):
    gate = singles['PhaseRotation']

    def test_as_identity(self):
        test_state = SingleQubitBasis(bitstring='0')
        new_state = self.gate(input_state=test_state, n=2)
        exp_state = QubitState(vector=UnitVector(array=np.array([[1],[0]])))
        self.assertTrue(new_state == exp_state)

    def test_as_identity_2(self):
        test_state = SingleQubitBasis(bitstring='1')
        new_state = self.gate(input_state=test_state, n=2)
        exp_state = QubitState(vector=UnitVector(array=np.array([[0],[1]])))
        self.assertTrue(new_state == exp_state)

    def test_with_undeclared_argument(self):
        test_state = SingleQubitBasis(bitstring='0')
        #new_state = self.gate(input_state=test_state, info=2)
        self.assertRaises(GateBaseError, self.gate,
                          **{'input_state':test_state, 'info':2})
