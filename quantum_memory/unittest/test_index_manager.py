#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    memory.base.py

Main test:
    Base quantum memory index manager.

Updated:
    20 July 2021
"""
import unittest
import numpy as np

from quantum_state.quantum_state import QuantumState
from qubit.qubit import QubitState
from qubit.utils import qubit_from_bitlist

from linear_space.vector import UnitVector
from quantum_register.registers import QubitRegister, QuantumRegister
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


class Test_global_index_range(unittest.TestCase):
    def test_okay_1(self):
        memory = trio_register_memory()
        self.assertTrue(memory.global_index_range() == range(0,8))

    def test_okay_2(self):
        s1 = qubit_from_bitlist([(1, '0000'), (1, '1101')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '10100')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.global_index_range() == range(0,11))


class Test_to_global_index(unittest.TestCase):
    def test_okay_1(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        local_index = 0
        label = 'reg2'
        global_index = memory.to_global_index(local_index, label)
        self.assertTrue(global_index == 3)

    def test_okay_2(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        local_index = 1
        label = 'reg3'
        global_index = memory.to_global_index(local_index, label)
        self.assertTrue(global_index == 6)

    def test_index_out_of_range(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        local_index = 3
        label = 'reg3'
        # Error: local index is out of range
        self.assertRaises(QuantumMemoryError, memory.to_global_index,
                          local_index, label)

    def test_non_existent_label(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        local_index = 3
        label = 'reg4'
        # Error: label doesn't exit in memory
        #global_index = memory.to_global_index(local_index, label)
        self.assertRaises(QuantumMemoryError, memory.to_global_index,
                          local_index, label)


class Test_to_local_index(unittest.TestCase):

    def test_okay_1(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        global_index = 0
        local_index = memory.to_local_index(global_index)['local_index']
        label = memory.to_local_index(global_index)['label']
        self.assertTrue(local_index == 0)
        self.assertTrue(label == 'reg1')

    def test_okay_2(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        global_index = 2
        local_index = memory.to_local_index(global_index)['local_index']
        label = memory.to_local_index(global_index)['label']
        self.assertTrue(local_index == 2)
        self.assertTrue(label == 'reg1')

    def test_okay_second_reg(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        global_index = 3
        local_index = memory.to_local_index(global_index)['local_index']
        label = memory.to_local_index(global_index)['label']
        self.assertTrue(local_index == 0)
        self.assertTrue(label == 'reg2')
        global_index = 4
        local_index = memory.to_local_index(global_index)['local_index']
        label = memory.to_local_index(global_index)['label']
        self.assertTrue(local_index == 1)
        self.assertTrue(label == 'reg2')

    def test_okay_third_reg(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '10101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        global_index = 7
        local_index = memory.to_local_index(global_index)['local_index']
        label = memory.to_local_index(global_index)['label']
        self.assertTrue(local_index == 2)
        self.assertTrue(label == 'reg3')
        global_index = 9
        local_index = memory.to_local_index(global_index)['local_index']
        label = memory.to_local_index(global_index)['label']
        self.assertTrue(local_index == 4)
        self.assertTrue(label == 'reg3')

    def test_out_of_range(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '10101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        global_index = 10
        self.assertRaises(QuantumMemoryError, memory.to_local_index, global_index)


class Test_get_local_index_range_by_label(unittest.TestCase):
    """ Local index range is accessible from register metadata """
    def test_okay(self):
        memory = trio_register_memory()
        self.assertTrue(memory.get_local_index_range_by_label('reg2') == range(0,2))
        self.assertTrue(memory.get_local_index_range_by_label('reg1') == range(0,3))
        self.assertTrue(memory.get_local_index_range_by_label('reg3') == range(0,3))

    def test_label_unknown(self):
        memory = trio_register_memory()
        self.assertRaises(QuantumMemoryError,
                          memory.get_local_index_range_by_label, 'REGGRE')


class Test_get_global_index_range_by_label(unittest.TestCase):
    """ Global index range is the qubit index range on global state """
    def test_okay(self):
        memory = trio_register_memory()
        self.assertTrue(memory.get_global_index_range_by_label('reg2') == range(3,5))
        self.assertTrue(memory.get_global_index_range_by_label('reg1') == range(0,3))
        self.assertTrue(memory.get_global_index_range_by_label('reg3') == range(5,8))

    def test_nonexistent_label(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertRaises(QuantumMemoryError, memory.get_global_index_range_by_label, 'test')


class Test_get_global_index_range_by_rank(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.get_global_index_range_by_rank(0) == range(0,3))
        self.assertTrue(memory.get_global_index_range_by_rank(1) == range(3,5))
        self.assertTrue(memory.get_global_index_range_by_rank(2) == range(5,8))

    def test_rank_out_of_range(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertRaises(QuantumMemoryError, memory.get_global_index_range_by_rank, 4)
        self.assertRaises(QuantumMemoryError, memory.get_global_index_range_by_rank, 3)
        self.assertRaises(QuantumMemoryError, memory.get_global_index_range_by_rank, -1)


class Test_global_index_range_FirstRegister(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '001010')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.get_global_index_range_first_register() == range(0,3))


class Test_global_index_range_LastRegister(unittest.TestCase):
    def test_okay(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.get_global_index_range_last_register() == range(5,8))

    def test_okay_2(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '0010')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        memory = QubitMemorySample(register=[reg1, reg2, reg3])
        self.assertTrue(memory.get_global_index_range_last_register() == range(7,10))
