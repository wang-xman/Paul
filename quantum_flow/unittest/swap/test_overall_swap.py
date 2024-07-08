#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.swap.py

Main test:
    Dedicated flow makers -> Flow of overall swap operations

Updated:
    28 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory

from quantum_flow import overall_swap_flow_on_register


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


class Test_OverallSwap_OnRegister(unittest.TestCase):
    def test_two_bits(self):
        s3 = qubit_from_bitlist([(1, '10')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = overall_swap_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '01')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_three_bits(self):
        s3 = qubit_from_bitlist([(1, '100')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = overall_swap_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '001')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_four_bits(self):
        s3 = qubit_from_bitlist([(1, '1010')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = overall_swap_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '0101')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_seven_bits(self):
        s3 = qubit_from_bitlist([(1, '0101001')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = overall_swap_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '1001010')])
        self.assertTrue(test_memory.get_global_state() == expected)
