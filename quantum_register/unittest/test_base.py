#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    register.base.py

Main test:
    Test validators and base register class
"""
import unittest
import numpy as np

from linear_space.vector import UnitVector
from quantum_state.quantum_state import QuantumState
#from qubit.qubit import ComputationalBasis, QubitState

from quantum_register.errors import RegisterError, RegisterBaseValidationError,\
    BaseRegisterInitValidationError
from quantum_register.base_register import BaseRegister


class naked_register(BaseRegister):
    pass

class TestSubclass_NakeClass(unittest.TestCase):
    def test_init(self):
        # Error: no state_class
        self.assertRaises(RegisterBaseValidationError, naked_register)


class register_illegal_state_class(BaseRegister):
    state_class = UnitVector

class TestSubclass_IllegalStateClass(unittest.TestCase):
    def test_init(self):
        # Error: no state_class
        self.assertRaises(RegisterBaseValidationError, register_illegal_state_class)


class register_parent(BaseRegister):
    state_class = QuantumState

class register_child(register_parent):
    pass

class TestSubclass_InheritedStateClass(unittest.TestCase):
    def test_okay(self):
        label = 'register_child'
        state = QuantumState(vector=UnitVector(array=np.array([[1],[1]])))
        # Okay
        register = register_child(**{'state': state, 'label': label})
        self.assertTrue(isinstance(register, BaseRegister))
        self.assertTrue(register.label == label)
        self.assertFalse(register.is_empty)
        self.assertTrue(register.has_state)

    def test_okay_without_state(self):
        label = 'register_child'
        state = QuantumState(vector=UnitVector(array=np.array([[1],[1]])))
        # Okay
        register = register_child(**{'label': label})
        self.assertTrue(isinstance(register, BaseRegister))
        self.assertTrue(register.label == label)
        self.assertTrue(register.is_empty)
        self.assertFalse(register.has_state)

    def test_error_without_label(self):
        label = 'register_child'
        state = QuantumState(vector=UnitVector(array=np.array([[1],[1]])))
        # Error: no label
        self.assertRaises(BaseRegisterInitValidationError, register_child,
                          **{'state': state})

    def test_label_issue(self):
        label = 'register child'
        state = QuantumState(vector=UnitVector(array=np.array([[1],[1]])))
        # Error: label contains space
        self.assertRaises(BaseRegisterInitValidationError, register_child,
                          **{'state': state, 'label': label})


class TestSubclass_IntakeMethod(unittest.TestCase):
    def test_intake(self):
        label = 'register_child'
        state = QuantumState(vector=UnitVector(array=np.array([[1],[1]])))
        # Okay
        register = register_child(**{'label': label})
        self.assertTrue(isinstance(register, BaseRegister))
        self.assertTrue(register.label == label)
        self.assertTrue(register.is_empty)
        self.assertFalse(register.has_state)
        register.intake(state)
        self.assertFalse(register.is_empty)
        self.assertTrue(register.has_state)

    def test_wrong_type(self):
        label = 'register_child'
        univec = UnitVector(array=np.array([[1],[1]]))
        state = QuantumState(vector=univec)
        # Okay
        register = register_child(**{'label': label})
        self.assertTrue(isinstance(register, BaseRegister))
        self.assertTrue(register.label == label)
        self.assertTrue(register.is_empty)
        self.assertFalse(register.has_state)
        self.assertRaises(RegisterError, register.intake, univec)
