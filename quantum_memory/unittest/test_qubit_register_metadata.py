#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    memory.qubit_memory.py

Main test:
    Qubit register metadata class

Updated:
    11 August 2021
"""
import unittest
import numpy as np

from quantum_state.quantum_state import QuantumState
from qubit.qubit import QubitState
from qubit.utils import qubit_from_bitlist
from linear_space.vector import UnitVector
from density_matrix.density_matrix import DensityMatrix
from quantum_register.registers import QubitRegister, QuantumRegister

from quantum_memory.validators import QubitMemoryRegisterValidator
from quantum_memory.qubit_memory import QubitMemory, QubitRegisterMetadata
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


class Test_init_failure(unittest.TestCase):
    def test_wrong_type(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        # Error: not even a register
        self.assertRaises(QuantumMemoryError, QubitRegisterMetadata, s1)


class Test_metadata_object(unittest.TestCase):
    def test_register_takes_in_different_state(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        #reg2 = QubitRegister(label='reg2', state=s2)
        md = QubitRegisterMetadata(reg1)
        #print(md.register_type)
        self.assertTrue(md.label == 'reg1')
        self.assertTrue(md.noq == 3)
        self.assertTrue(md.local_index_range == range(0,3))
        # register takes different state
        reg1.intake(s2)
        self.assertTrue(md.label == 'reg1')
        self.assertTrue(md.noq == 2)
        self.assertTrue(md.local_index_range == range(0,2))

    def test_set_register(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        md = QubitRegisterMetadata(reg1)
        self.assertTrue(md.label == 'reg1')
        self.assertTrue(md.noq == 3)
        self.assertTrue(md.local_index_range == range(0,3))
        # manually sets a referenced register
        md.set_register(reg2)
        self.assertTrue(md.label == 'reg2')
        self.assertTrue(md.noq == 2)
        self.assertTrue(md.local_index_range == range(0,2))


class Test_metadata_dict(unittest.TestCase):
    def test_(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        md = QubitRegisterMetadata(reg1)
        mddct = md.as_dict()
        self.assertTrue(mddct['label'] == 'reg1')
        self.assertTrue(mddct['register_type'] == 'QubitRegister')
        self.assertTrue(mddct['noq'] == 3)
        self.assertTrue(mddct['local_index_range'] == range(0,3))
        self.assertTrue(mddct['rank'] is None)
        self.assertTrue(mddct['status'] is None)
