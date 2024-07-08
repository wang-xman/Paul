#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    memory.base.py

Main test:
    Quantum memory register metadata manager.

Updated:
    09 August 2021
"""
import unittest
import numpy as np

from quantum_state.quantum_state import QuantumState
from qubit.qubit import QubitState
from qubit.utils import qubit_from_bitlist

from linear_space.vector import UnitVector
from quantum_register.registers import QubitRegister, QuantumRegister
from quantum_memory.base_memory import BaseMemory
from quantum_memory.qubit_memory import QubitMemory
from quantum_memory.errors import QuantumMemoryError


class QubitMemorySample(QubitMemory):
    label = 'memory_sample'


def trio_register_memory():
    s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
    reg1 = QubitRegister(label='reg1', state=s1)
    s2 = qubit_from_bitlist([(1, '00')])
    reg2 = QubitRegister(label='reg2', state=s2)
    s3 = qubit_from_bitlist([(1, '101')])
    reg3 = QubitRegister(label='reg3', state=s3)
    memory = QubitMemorySample(register=[reg1, reg2, reg3])
    return memory


class Test_get_all_labels(unittest.TestCase):
    def test_okay(self):
        memory = trio_register_memory()
        labels = memory.get_all_labels()
        self.assertTrue(isinstance(labels, list))
        self.assertTrue(len(labels) == 3)
        self.assertTrue(labels[0] == 'reg1')
        self.assertTrue(labels[2] == 'reg3')


class Test_has_register_label(unittest.TestCase):
    def test_okay(self):
        memory = trio_register_memory()
        self.assertTrue(memory.has_register_label('reg1'))
        self.assertFalse(memory.has_register_label('areg3'))


class Test_get_rank_by_label(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.get_rank_by_label('reg2') == 1)
        self.assertTrue(memory.get_rank_by_label('reg1') == 0)
        self.assertTrue(memory.get_rank_by_label('reg3') == 2)

    def test_nonexistent_label(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertRaises(QuantumMemoryError, memory.get_rank_by_label, 'reg4')


class Test_get_label_by_rank(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.get_label_by_rank(1) == 'reg2')
        self.assertTrue(memory.get_label_by_rank(0) == 'reg1')
        self.assertTrue(memory.get_label_by_rank(2) == 'reg3')

    def test_rank_out_of_range(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertRaises(QuantumMemoryError, memory.get_label_by_rank, 4)

    def test_non_integer_rank(self):
        memory = trio_register_memory()
        # Error: non integer
        self.assertRaises(QuantumMemoryError, memory.get_label_by_rank, '3')


class Test_get_register_metadata_by_label(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '10110')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        info = memory.get_register_metadata_by_label('reg3')
        ##print(info)
        self.assertTrue(info.label == 'reg3')
        self.assertTrue(info.rank == 2)
        self.assertTrue(info.noq == 5)


class Test_get_noq_by_label(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '10110')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.get_noq_by_label('reg2') == 2)
        self.assertTrue(memory.get_noq_by_label('reg3') == 5)
        self.assertTrue(memory.get_noq_by_label('reg1') == 3)
        # Error: label doesn't exist
        self.assertRaises(QuantumMemoryError, memory.get_noq_by_label, 'reg')


class Test_get_noq_by_rank(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '10110')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.get_noq_by_rank(0) == 3)
        self.assertTrue(memory.get_noq_by_rank(2) == 5)
        self.assertTrue(memory.get_noq_by_rank(1) == 2)
        # Error: label doesn't exist
        self.assertRaises(QuantumMemoryError, memory.get_noq_by_rank, 5)
