#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.fourier.py

Main test:
    Flow makers of QFT operations

Updated:
    28 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory

from quantum_flow import quantum_fourier_flow_on_register, \
    inverse_quantum_fourier_flow_on_register


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


class Test_QFT(unittest.TestCase):
    def test_one_bit(self):
        s3 = qubit_from_bitlist([(1, '0')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = quantum_fourier_flow_on_register(register=reg3)
        flow.launch_on_memory(memory=test_memory)
        #print(test_memory.get_global_state())
        expected = qubit_from_bitlist([(1, '0'), (1, '1')])
        self.assertTrue(test_memory.get_global_state() == expected)


class Test_QFT_and_IQFT(unittest.TestCase):
    def test_one_bit(self):
        s3 = qubit_from_bitlist([(1, '0')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = quantum_fourier_flow_on_register(register=reg3)
        invflow = inverse_quantum_fourier_flow_on_register(register=reg3)
        # Fourier transform
        flow.launch_on_memory(memory=test_memory)
        # Inverse QFT
        invflow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '0')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_two_bit(self):
        s3 = qubit_from_bitlist([(1, '01')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = quantum_fourier_flow_on_register(register=reg3)
        invflow = inverse_quantum_fourier_flow_on_register(register=reg3)
        # Fourier transform
        flow.launch_on_memory(memory=test_memory)
        # Inverse QFT
        invflow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '01')])
        self.assertTrue(test_memory.get_global_state() == expected)

    def test_seven_bit(self):
        s3 = qubit_from_bitlist([(1, '011001'), (1, '100001')])
        reg3 = QubitRegister(label='reg3', state=s3)
        # memory
        test_memory = QubitMemory(register=[reg3])
        flow = quantum_fourier_flow_on_register(register=reg3)
        invflow = inverse_quantum_fourier_flow_on_register(register=reg3)
        # Fourier transform
        flow.launch_on_memory(memory=test_memory)
        # Inverse QFT
        invflow.launch_on_memory(memory=test_memory)
        expected = qubit_from_bitlist([(1, '011001'), (1, '100001')])
        self.assertTrue(test_memory.get_global_state() == expected)
