#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.walsh_hadamard.py

Main test:
    Flow makers of bitwise Walsh-Hadamard operations.
    Flow is applied on the state in a memory.

Updated:
    28 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory

from quantum_flow import hadamard_flow_on_memory


def error_raiser(validator):
    validator.raise_last_error()


def get_test_memory():
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


class Test_HadamardFlowMemory_SingleRegister(unittest.TestCase):
    def test_single_register_memory(self):
        s3 = qubit_from_bitlist([(1, '00')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = hadamard_flow_on_memory(memory=test_memory)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '00'),(1, '01'),
                                       (1, '10'),(1, '11')])
        self.assertTrue(test_memory.get_global_state() == expected)


class Test_HadamardFlowMemory_MultipleRegister(unittest.TestCase):
    def test_duo_register_memory(self):
        s3 = qubit_from_bitlist([(1, '00')])
        reg3 = QubitRegister(label='reg3', state=s3)
        s4 = qubit_from_bitlist([(1, '00')])
        reg4 = QubitRegister(label='reg4', state=s4)
        # memory
        test_memory = QubitMemory(register=[reg3, reg4])
        flow = hadamard_flow_on_memory(memory=test_memory)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '0000'),(1, '0001'),
                                       (1, '0010'),(1, '0011'),
                                       (1, '0100'),(1, '0101'),
                                       (1, '0110'),(1, '0111'),
                                       (1, '1000'),(1, '1001'),
                                       (1, '1010'),(1, '1011'),
                                       (1, '1100'),(1, '1101'),
                                       (1, '1110'),(1, '1111')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_quad_register_memory(self):
        s1 = qubit_from_bitlist([(1, '0')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '0')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s3 = qubit_from_bitlist([(1, '0')])
        reg3 = QubitRegister(label='reg3', state=s3)
        s4 = qubit_from_bitlist([(1, '0')])
        reg4 = QubitRegister(label='reg4', state=s4)
        # memory
        test_memory = QubitMemory(register=[reg1, reg2, reg3, reg4])
        flow = hadamard_flow_on_memory(memory=test_memory)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '0000'),(1, '0001'),
                                       (1, '0010'),(1, '0011'),
                                       (1, '0100'),(1, '0101'),
                                       (1, '0110'),(1, '0111'),
                                       (1, '1000'),(1, '1001'),
                                       (1, '1010'),(1, '1011'),
                                       (1, '1100'),(1, '1101'),
                                       (1, '1110'),(1, '1111')])
        self.assertTrue(test_memory.get_global_state() == expected)
