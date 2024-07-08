#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.swap.py

Main test:
    Dedicated flow makers -> Flow of swap operations

Updated:
    28 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory

from quantum_flow import swap_flow


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


class Test_Swap(unittest.TestCase):
    def test_two_bits(self):
        s3 = qubit_from_bitlist([(1, '10')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = swap_flow(0,1,register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '01')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_four_bits(self):
        s3 = qubit_from_bitlist([(1, '1010')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = swap_flow(0,3,register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '0011')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_three_bits(self):
        s3 = qubit_from_bitlist([(1, '100'), (1, '110')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = swap_flow(0,2,register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '001'), (1, '011')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_five_bits(self):
        s3 = qubit_from_bitlist([(1, '10001'), (1, '10110')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = swap_flow(0,1,register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '01001'), (1, '01110')])
        self.assertTrue(test_memory.get_global_state() == expected)


class Test_Swap_Failure(unittest.TestCase):
    def test_indices_out_of_range(self):
        s3 = qubit_from_bitlist([(1, '10')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        # Error: index out of range
        self.assertRaises(Exception, swap_flow, 0,2,reg3)

    def test_identical_target_control(self):
        s3 = qubit_from_bitlist([(1, '10')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        # Error: target is identical to control, at validation level
        self.assertRaises(Exception, swap_flow, 0,0,reg3)


class Test_Swap_via_Launch_on_Global_State(unittest.TestCase):
    def test_five_bits(self):
        s3 = qubit_from_bitlist([(1, '10001'), (1, '10110')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow1 = swap_flow(0, 1, register=reg3)
        flow1.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '01001'), (1, '01110')])
        self.assertTrue(test_memory.get_global_state() == expected)
        # use on global state
        s4 = qubit_from_bitlist([(1, '10001'), (1, '10110')])
        reg4 = QubitRegister(label='reg4', state=s4)
        test_memory2 = QubitMemory(register=[reg4])
        flow2 = swap_flow(0, 1, register=reg4)
        flow2.launch_on_global_state(memory=test_memory2)
        self.assertTrue(test_memory2.get_global_state() == expected)
        self.assertTrue(test_memory.get_global_state() == test_memory2.get_global_state())
