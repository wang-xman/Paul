#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    memory.base.py

Main test:
    Base quantum memory classes.

Updated:
    18 July 2021
"""
import unittest
import numpy as np

from quantum_state.quantum_state import QuantumState
from qubit.qubit import QubitState
from qubit.utils import qubit_from_bitlist

from linear_space.vector import UnitVector
from quantum_register.registers import QubitRegister
from quantum_memory.base_memory import BaseMemory
from quantum_memory.errors import QuantumMemoryError


class Test_BaseMemory_with_Registers(unittest.TestCase):
    def test_okay(self):
        memory = BaseMemory()
        self.assertFalse(memory.has_global_state)
        self.assertTrue(memory.get_global_state() is None)


class TestGlobalStateFormation(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '0'), (1, '1')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '0')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '1')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = BaseMemory()
        memory._update_global_state_with_register([reg1, reg2, reg3])
        self.assertTrue(memory.has_global_state)
        self.assertTrue(memory.has_global_state)
        self.assertTrue(isinstance(memory.get_global_state(), QubitState))
        expected = qubit_from_bitlist([(1, '001'), (1, '101')])
        self.assertTrue(memory.get_global_state() == expected)

    def test_with_empty_register(self):
        s1 = qubit_from_bitlist([(1, '0'), (1, '1')])
        reg1 = QubitRegister(label='reg1', state=s1)
        #s2 = qubit_from_bitlist([(1, '0')])
        #reg2 = QubitRegister(label='reg2', state=s2)
        reg2 = QubitRegister(label='reg2')
        s3 = qubit_from_bitlist([(1, '1')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = BaseMemory()
        self.assertFalse(memory.has_global_state)
        self.assertRaises(Exception, memory._update_global_state_with_register,
                         [reg1, reg2, reg3])


class Test_ManuallyUpdateGlobalState(unittest.TestCase):
    def test_okay(self):
        memory = BaseMemory()
        state = qubit_from_bitlist([(1, '001'), (1, '101')])
        self.assertTrue(memory.get_global_state() is None)
        # update global state
        memory.set_global_state(state)
        self.assertTrue(memory.get_global_state() == state)
