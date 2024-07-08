#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    register.registers.py

Note:
    Test different types of quantum registers
"""
import unittest
import numpy as np

from linear_space.vector import UnitVector
from quantum_state import QuantumState
from qubit import ComputationalBasis, QubitState

from quantum_register.registers import QuantumRegister, QubitRegister, \
    ComputationalRegister
from quantum_register.errors import RegisterError, BaseRegisterInitValidationError


class TestQuantumRegister(unittest.TestCase):
    def test(self):
        label = 'test_one'
        univec = UnitVector(array=np.array([[1],[1]]))
        state = QuantumState(vector=univec)
        register = QuantumRegister(state=state, label=label)
        self.assertTrue(register.state_class == QuantumState)
        self.assertTrue(register.label == label)
        self.assertTrue(register._state == state)


class TestQubitRegister(unittest.TestCase):
    def test_wrong_state_type(self):
        label = 'test_one'
        univec = UnitVector(array=np.array([[1],[1]]))
        state = QuantumState(vector=univec)
        # Error: Qubit register doesn't take quatum state
        self.assertRaises(BaseRegisterInitValidationError, QubitRegister,
                          **{'state': state, 'label': label})

    def test_pass(self):
        label = 'compureg'
        bitstring = '01010101'
        state = ComputationalBasis(bitstring=bitstring)
        register = QubitRegister(state=state, label=label)
        self.assertTrue(register.state_class == QubitState)
        self.assertTrue(register.label == label)
        self.assertTrue(register._state == state)
        self.assertTrue(register.noq == state.noq)


class TestQubitRegister_Info(unittest.TestCase):
    def test_pass(self):
        label = 'compureg'
        bitstring = '01010101'
        state = ComputationalBasis(bitstring=bitstring)
        register = QubitRegister(state=state, label=label)
        info = register.info
        self.assertTrue(info['label'] == label)
        self.assertTrue(info['noq'] != 10)
        self.assertTrue(info['noq'] == len(bitstring))


class TestComputationalRegister(unittest.TestCase):
    def test(self):
        label = 'compureg'
        #univec = UnitVector(array=np.array([[1],[1]]))
        bitstring = '01010101'
        state = ComputationalBasis(bitstring=bitstring)
        register = ComputationalRegister(state=state, label=label)
        self.assertTrue(register.state_class == QubitState)
        self.assertTrue(register.label == label)
        self.assertTrue(register._state == state)
