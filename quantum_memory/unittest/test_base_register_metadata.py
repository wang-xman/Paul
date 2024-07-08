#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    memory.metadata.py

Main test:
    Base register metadata class

Updated:
    23 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist

from quantum_register.registers import QubitRegister
from quantum_memory.errors import QuantumMemoryError
from quantum_memory.metadata import BaseRegisterMetadata


state = qubit_from_bitlist([(1, '10')])
register = QubitRegister(state=state, label='TEST_REG')
test_metadata = BaseRegisterMetadata(register)


class Test_Init_Failure(unittest.TestCase):
    def test_okay(self):
        self.assertRaises(QuantumMemoryError, BaseRegisterMetadata, state)


class Test_Init(unittest.TestCase):
    def test_label(self):
        self.assertTrue(test_metadata.label == 'TEST_REG')

    def test_register_type(self):
        self.assertTrue(test_metadata.register_type == 'QubitRegister')

    def test_get_register(self):
        reg = test_metadata.get_register()
        self.assertTrue(isinstance(reg, QubitRegister))
        self.assertTrue(reg.label == 'TEST_REG')


class Test_Dict(unittest.TestCase):
    def test_as_dict(self):
        dct = test_metadata.as_dict()
        self.assertTrue(dct['label'] == 'TEST_REG')
        self.assertTrue(dct['register_type'] == 'QubitRegister')


class Test_Manually_Replace_Register(unittest.TestCase):
    def test_replace(self):
        new_state = qubit_from_bitlist([(1, '100')])
        new_register = QubitRegister(state=new_state, label='NEW_REG')
        test_metadata.set_register(new_register)
        self.assertFalse(test_metadata.label == 'TEST_REG')
        self.assertTrue(test_metadata.label == 'NEW_REG')
        self.assertTrue(test_metadata.get_register().noq == 3)

    def test_replace_error(self):
        self.assertRaises(QuantumMemoryError, test_metadata.set_register, state)
