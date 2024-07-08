#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.reflection.py

Main test:
    Flow makers of reflection operation.

Updated:
    31 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory

from quantum_flow import reflection_flow_about_zeros


def error_raiser(validator):
    validator.raise_last_error()


def single_bit_memory():
    """ Test memory """
    # only register
    s1 = qubit_from_bitlist([(1, '0'), (1, '1')])
    reg1 = QubitRegister(label='COMPUT', state=s1)
    # memory
    memory = QubitMemory(register=[reg1])
    return memory

def single_register_memory():
    """ Test memory """
    # only register
    s1 = qubit_from_bitlist([(1, '01'), (1, '00')])
    reg1 = QubitRegister(label='COMPUT', state=s1)
    # memory
    memory = QubitMemory(register=[reg1])
    return memory


def single_register_memory_5bits():
    """ Test memory """
    # only register
    s1 = qubit_from_bitlist([(1, '01110'), (1, '00000'), (1, '01001')])
    reg1 = QubitRegister(label='COMPUT', state=s1)
    # memory
    memory = QubitMemory(register=[reg1])
    return memory

def triple_register_memory():
    """ Test memory """
    # 1st register
    s1 = qubit_from_bitlist([(1, '01'), (1, '10')])
    reg1 = QubitRegister(label='reg1', state=s1)
    # 2nd register
    s2 = qubit_from_bitlist([(1, '001')])
    reg2 = QubitRegister(label='reg2', state=s2)
    # 3rd register
    s3 = qubit_from_bitlist([(1, '10')])
    reg3 = QubitRegister(label='reg3', state=s3)
    # memory
    memory = QubitMemory(register=[reg1, reg2, reg3])
    return memory


class Test_Reflection_About_Zeros_Single_Bit(unittest.TestCase):
    def test_okay(self):
        memory = single_bit_memory()
        reg_metadata = memory.get_register_metadata_by_label('COMPUT')
        flow = reflection_flow_about_zeros(reg_metadata)
        flow.launch_on_memory(memory)
        expected_state = qubit_from_bitlist([(-1, '0'), (1, '1')])
        self.assertTrue(memory.get_global_state() == expected_state)


class Test_Reflection_About_Zeros_Single_Register(unittest.TestCase):
    def test_okay(self):
        memory = single_register_memory()
        reg_metadata = memory.get_register_metadata_by_label('COMPUT')
        flow = reflection_flow_about_zeros(reg_metadata)
        flow.launch_on_memory(memory)
        expected_state = qubit_from_bitlist([(1, '01'), (-1, '00')])
        self.assertTrue(memory.get_global_state() == expected_state)


class Test_Reflection_About_Zeros_Single_Register_5bits(unittest.TestCase):
    def test_okay(self):
        memory = single_register_memory_5bits()
        reg_metadata = memory.get_register_metadata_by_label('COMPUT')
        flow = reflection_flow_about_zeros(reg_metadata)
        flow.launch_on_memory(memory)
        expected_state = qubit_from_bitlist([
            (1, '01110'), (-1, '00000'), (1, '01001')]
        )
        self.assertTrue(memory.get_global_state() == expected_state)
