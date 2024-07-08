#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    operation.gate_operation.py

Main test:
    Gate operation on memory validator.

Updated:
    11 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_instruction.gate import GateInstruction
from quantum_operation.gate import GateOperationValidator
from quantum_memory.qubit_memory import QubitMemory


class QuantumMemorySample(QubitMemory):
    label = 'Test_QuantumMemory'


def get_test_memory():
    """ Test memory """
    # 1st register
    s1 = qubit_from_bitlist([(1, '0100'), (1, '1011')])
    reg1 = QubitRegister(label='reg1', state=s1)
    # 2nd register
    s2 = qubit_from_bitlist([(1, '001')])
    reg2 = QubitRegister(label='reg2', state=s2)
    # 3rd register
    s3 = qubit_from_bitlist([(1, '1010')])
    reg3 = QubitRegister(label='reg3', state=s3)
    # memory
    memory = QuantumMemorySample(register=[reg1, reg2, reg3])
    return memory


class TestGateOperationMemoryValidator(unittest.TestCase):
    def test_okay(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 2,
            'state': '1'
        }
        opdict = {
            'gate': {
                'alias': 'Flip',
                'parameters': {}
            },
            'target': {
                'register': 'reg3',
                'local_index': 0
            },
            'control': {
                'list': [el, el2]
            },
        }
        instruc = GateInstruction(instruc_dict=opdict)
        validator = GateOperationValidator(instruction=instruc,
                                              memory=get_test_memory())
        self.assertTrue(validator.is_valid)

    def test_control_out_of_range(self):
        el = {
            'register': 'reg1',
            'local_index': 5,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 2,
            'state': '1'
        }
        opdict = {
            'gate': {
                'alias': 'Flip',
                'parameters': {}
            },
            'target': {
                'register': 'reg3',
                'local_index': 0
            },
            'control': {
                'list': [el, el2]
            },
        }
        instruc = GateInstruction(instruc_dict=opdict)
        validator = GateOperationValidator(instruction=instruc,
                                              memory=get_test_memory())
        #error_raiser(validator)
        # Error: control index is outside local range
        self.assertFalse(validator.is_valid)

    def test_target_out_of_range(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 2,
            'state': '1'
        }
        opdict = {
            'gate': {
                'alias': 'Flip',
                'parameters': {}
            },
            'target': {
                'register': 'reg3',
                'local_index': 10
            },
            'control': {
                'list': [el, el2]
            },
        }
        instruc = GateInstruction(instruc_dict=opdict)
        validator = GateOperationValidator(instruction=instruc,
                                              memory=get_test_memory())
        #error_raiser(validator)
        # Error: control index is outside local range
        self.assertFalse(validator.is_valid)
