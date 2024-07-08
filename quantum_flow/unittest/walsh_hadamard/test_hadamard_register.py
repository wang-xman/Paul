#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.walsh_hadamard.py

Main test:
    Flow makers of bitwise Walsh-Hadamard operations.
    Flow is applied on a selected register in a memory.

Updated:
    28 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory

from quantum_flow import hadamard_flow_on_register


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


class Test_HadamardFlowRegister_OnlyRegister(unittest.TestCase):
    def test_00(self):
        s3 = qubit_from_bitlist([(1, '00')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = hadamard_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '00'),(1, '01'),
                                       (1, '10'),(1, '11')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_11(self):
        s3 = qubit_from_bitlist([(1, '11')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = hadamard_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '00'),(-1, '01'),
                                       (-1, '10'),(1, '11')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_10(self):
        s3 = qubit_from_bitlist([(1, '10')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = hadamard_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '00'),(1, '01'),
                                       (-1, '10'),(-1, '11')])
        self.assertTrue(test_memory.get_global_state() == expected)


class Test_HadamardFlowRegister_Register(unittest.TestCase):
    def test_on_00_and_00(self):
        s3 = qubit_from_bitlist([(1, '00')])
        reg3 = QubitRegister(label='reg3', state=s3)
        s5 = qubit_from_bitlist([(1, '00')])
        reg5 = QubitRegister(label='reg5', state=s5)
        # memory
        test_memory = QubitMemory(register=[reg3, reg5])
        flow = hadamard_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '0000'),(1, '0100'),
                                       (1, '1000'),(1, '1100')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_on_00_and_101(self):
        s3 = qubit_from_bitlist([(1, '00')])
        reg3 = QubitRegister(label='reg3', state=s3)
        s5 = qubit_from_bitlist([(1, '101')])
        reg5 = QubitRegister(label='reg5', state=s5)
        # memory
        test_memory = QubitMemory(register=[reg3, reg5])
        flow = hadamard_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '00101'),(1, '01101'),
                                       (1, '10101'),(1, '11101')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_00_and_on_00(self):
        s3 = qubit_from_bitlist([(1, '00')])
        reg3 = QubitRegister(label='reg3', state=s3)
        s5 = qubit_from_bitlist([(1, '00')])
        reg5 = QubitRegister(label='reg5', state=s5)
        # memory
        test_memory = QubitMemory(register=[reg3, reg5])
        flow = hadamard_flow_on_register(register=reg5)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '0000'),(1, '0001'),
                                       (1, '0010'),(1, '0011')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_0_and_on_00_and_1(self):
        """ Flow executes on the register in the middle """
        s1 = qubit_from_bitlist([(1, '0')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s5 = qubit_from_bitlist([(1, '1')])
        reg5 = QubitRegister(label='reg5', state=s5)
        # memory
        test_memory = QubitMemory(register=[reg1, reg2, reg5])
        flow = hadamard_flow_on_register(register=reg2)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '0001'),(1, '0011'),
                                       (1, '0101'),(1, '0111')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_10_and_on_00_and_11(self):
        """ Flow executes on the register in the middle """
        s1 = qubit_from_bitlist([(1, '10')])
        reg1 = QubitRegister(label='reg1', state=s1)
        s2 = qubit_from_bitlist([(1, '00')])
        reg2 = QubitRegister(label='reg2', state=s2)
        s5 = qubit_from_bitlist([(1, '11')])
        reg5 = QubitRegister(label='reg5', state=s5)
        # memory
        test_memory = QubitMemory(register=[reg1, reg2, reg5])
        flow = hadamard_flow_on_register(register=reg2)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '100011'),(1, '100111'),
                                       (1, '101011'),(1, '101111')])
        self.assertTrue(test_memory.get_global_state() == expected)
