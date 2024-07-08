#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    memory.base.py

Main test:
    Quantum memory class

Updated:
    09 August 2021
"""
import unittest
import numpy as np
from common.exception import Validation_Error, Generic_Error
from quantum_state.quantum_state import QuantumState
from qubit.qubit import QubitState
from qubit.utils import qubit_from_bitlist
from linear_space.vector import UnitVector
from density_matrix.density_matrix import DensityMatrix
from quantum_register.registers import QubitRegister, QuantumRegister

from quantum_memory.validators import QubitMemoryRegisterValidator
from quantum_memory.qubit_memory import QubitMemory
from quantum_memory.errors import QuantumMemoryError


class Test_QubitMemoryRegisterValidator(unittest.TestCase):
    def test_one_register(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        validator = QubitMemoryRegisterValidator(register=reg1,
                                                 register_class=QubitRegister)
        self.assertTrue(validator.is_valid)

    def test_empty_register(self):
        #s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1')
        validator = QubitMemoryRegisterValidator(register=reg1,
                                                 register_class=QubitRegister)
        self.assertFalse(validator.is_valid)

    def test_register_list(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3', state=s3)
        validator = QubitMemoryRegisterValidator(register=[reg1, reg2, reg3], 
                                                 register_class=QubitRegister)
        self.assertTrue(validator.is_valid)

    def test_register_list_with_empty(self):
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        #s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3')
        validator = QubitMemoryRegisterValidator(register=[reg1, reg2, reg3],
                                                 register_class=QubitRegister)
        self.assertFalse(validator.is_valid)


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


class Test_Initialisation(unittest.TestCase):
    def test_label_double_entry(self):
        """ Two registers have the same label """
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg2', state=s3)
        # Error: two register of same label
        self.assertRaises(Validation_Error, QubitMemorySample,
                          [reg1, reg2, reg3])

    def test_empty_register(self):
        """ One register is empty """
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '101')])
        reg3 = QubitRegister(label='reg3')
        #memory = QubitMemorySample(register=[reg1, reg2, reg3])
        # Error: reg3 is empty
        self.assertRaises(Validation_Error, QubitMemorySample,
                          [reg1, reg2, reg3])

    def test_single_register_okay(self):
        """ Single register init """
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1', state=s1)
        memory = QubitMemorySample(register=[reg1])
        global_state = memory.get_global_state()
        self.assertTrue(s1 == global_state)

    def test_single_register_empty(self):
        """ Single register is empty """
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QubitRegister(label='reg1')
        # Error: reg1 is empty
        self.assertRaises(Validation_Error, QubitMemorySample, reg1)

    def test_single_register_wrong_type(self):
        """ Single register is not a qubit register """
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QuantumRegister(label='reg1')
        # Error: reg1 is not qubit register
        self.assertRaises(Validation_Error, QubitMemorySample, reg1)

    def test_single_register_wrong_type_as_list(self):
        """ Single register is not a qubit register """
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        reg1 = QuantumRegister(label='reg1')
        # Error: reg1 is not qubit register
        self.assertRaises(Validation_Error, QubitMemorySample, [reg1])

    def test_non_register(self):
        """ Non register is used in initialisation """
        s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
        #memory = QubitMemorySample(register=s1)
        # Error: not a (list of) register(s)
        self.assertRaises(Validation_Error, QubitMemorySample, s1)


class Test_metadata_list(unittest.TestCase):
    def test_okay(self):
        memory = trio_register_memory()
        metadata = memory.get_register_metadata_list()
        self.assertTrue(memory.get_global_state().noq == 8)
        self.assertTrue(len(metadata) == 3)
        self.assertTrue(metadata[0].label == 'reg1')
        self.assertTrue(metadata[0].noq == 3)
        self.assertTrue(metadata[1].label == 'reg2')
        self.assertTrue(metadata[2].label == 'reg3')

    def test_individual_metadata(self):
        memory = trio_register_memory()
        # RegisterManager.get_register_metadata_by_label
        md = memory.get_register_metadata_by_label('reg3')
        self.assertTrue(md.label == 'reg3')
        self.assertTrue(md.rank == 2)
        self.assertTrue(md.local_index_range == range(0,3))
        self.assertTrue(md.noq == 3)


class Test_number_of_registers(unittest.TestCase):
    def test_okay(self):
        memory = trio_register_memory()
        self.assertTrue(memory.number_of_registers == 3)

class Test_get_global_density_matrix(unittest.TestCase):
    def test_okay(self):
        memory = trio_register_memory()
        # density matrix wasn't formed automatically.
        self.assertFalse(isinstance(memory.get_global_density_matrix(),
                                   DensityMatrix))


class Test_append_register(unittest.TestCase):
    def test_append_one_register(self):
        s1 = qubit_from_bitlist([(1, '11')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        memory = QubitMemorySample(register=[reg1])
        global_before_append = s1
        self.assertTrue(global_before_append == memory.get_global_state())
        # append
        memory.append_register(reg2)
        global_after_append = qubit_from_bitlist([(1, '1100')])
        self.assertTrue(global_after_append == memory.get_global_state())

    def test_append_one_register_as_list(self):
        s1 = qubit_from_bitlist([(1, '11')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        memory = QubitMemorySample(register=[reg1])
        global_before_append = s1
        self.assertTrue(global_before_append == memory.get_global_state())
        # append
        memory.append_register([reg2])
        global_after_append = qubit_from_bitlist([(1, '1100')])
        self.assertTrue(global_after_append == memory.get_global_state())

    def test_append_one_register_label_clash(self):
        s1 = qubit_from_bitlist([(1, '11')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        # mind the label
        reg2 = QubitRegister(label='reg1', state=s2)
        memory = QubitMemorySample(register=[reg1])
        # Error: label already exists.
        self.assertRaises(QuantumMemoryError, memory.append_register, reg2)
        self.assertRaises(QuantumMemoryError, memory.append_register, [reg2])

    def test_append_register_list(self):
        s1 = qubit_from_bitlist([(1, '11')])
        reg1 = QubitRegister(label='reg1', state=s1)
        memory = QubitMemorySample(register=[reg1])
        s2 = qubit_from_bitlist([(1, '0')])
        reg2 = QubitRegister(label='reg2', state=s2)
        reg3 = QubitRegister(label='reg3', state=s2)
        self.assertTrue(s1 == memory.get_global_state())
        # append
        memory.append_register([reg2, reg3])
        global_after_append = qubit_from_bitlist([(1, '1100')])
        self.assertTrue(global_after_append == memory.get_global_state())

    def test_append_register_list_label_clash(self):
        s1 = qubit_from_bitlist([(1, '11')])
        reg1 = QubitRegister(label='reg1', state=s1)
        memory = QubitMemorySample(register=[reg1])
        s2 = qubit_from_bitlist([(1, '0')])
        reg2 = QubitRegister(label='reg2', state=s2)
        # already in memory
        reg3 = QubitRegister(label='reg1', state=s2)
        self.assertTrue(s1 == memory.get_global_state())
        # Error: label already exists in memory.
        self.assertRaises(QuantumMemoryError,
                          memory.append_register, [reg2, reg3])


def quad_register_memory():
    s1 = qubit_from_bitlist([(1, '000'), (1, '111')])
    reg1 = QubitRegister(label='reg1', state=s1)
    s2 = qubit_from_bitlist([(1, '00')])
    reg2 = QubitRegister(label='reg2', state=s2)
    s3 = qubit_from_bitlist([(1, '101')])
    reg3 = QubitRegister(label='reg3', state=s3)
    s4 = qubit_from_bitlist([(1, '01')])
    reg4 = QubitRegister(label='reg4', state=s4)
    memory = QubitMemorySample(register=[reg1, reg2, reg3, reg4])
    return memory

class Test_Metadata_Removal_Label(unittest.TestCase):
    def test_removal_by_label(self):
        memory = quad_register_memory()
        self.assertTrue(memory.number_of_registers == 4)
        memory.remove_register_metadata_by_label('reg4')
        self.assertTrue(memory.number_of_registers == 3)
        self.assertFalse('reg4' in memory.get_all_labels())
        # reg4 has been removed, further attempt triggers error
        self.assertRaises(QuantumMemoryError,
                          memory.remove_register_metadata_by_label, 'reg4')

    def test_label_not_found(self):
        memory = quad_register_memory()
        self.assertTrue(memory.number_of_registers == 4)
        self.assertRaises(QuantumMemoryError,
                          memory.remove_register_metadata_by_label, 'reg5')


class Test_Metadata_Removal_Rank(unittest.TestCase):
    def test_removal_by_rank_1(self):
        memory = quad_register_memory()
        self.assertTrue(memory.number_of_registers == 4)
        # remove reg1
        memory.remove_register_metadata_by_rank(0)
        # total number of registers has changed
        self.assertTrue(memory.number_of_registers == 3)
        # access to reg1 causes error
        self.assertRaises(QuantumMemoryError,
                          memory.remove_register_metadata_by_label, 'reg1')
        # at rank 0, it is reg2
        self.assertTrue(memory.get_label_by_rank(0) == 'reg2')

    def rest_remove_by_rank_two(self):
        memory = quad_register_memory()
        self.assertTrue(memory.number_of_registers == 4)
        # remove reg2
        memory.remove_register_metadata_by_rank(1)
        # access to reg2 causes error
        self.assertRaises(QuantumMemoryError,
                          memory.remove_register_metadata_by_label, 'reg2')
        # then reg3 occupies rank 1
        self.assertTrue(memory.get_label_by_rank(1) == 'reg3')
        self.assertTrue(memory.get_label_by_rank(2) == 'reg4')
