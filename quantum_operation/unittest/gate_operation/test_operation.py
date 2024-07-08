#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    operation.gate_operation.py

Main test:
    Gate operation object.

Updated:
    12 August 2021
"""

import unittest

from qubit.utils import qubit_from_bitlist
from gate import single_qubit_gates as singles
from quantum_register.registers import QubitRegister
from quantum_instruction.gate import GateInstructionDictValidationError, \
    GateInstruction
from quantum_operation.gate.errors import GateOperationValidationError
from quantum_operation.gate import GateOperation, \
    gate_operation_from_instruction_dict
from quantum_memory.qubit_memory import QubitMemory


def error_raiser(validator):
    validator.raise_last_error()


class MemorySample(QubitMemory):
    label = 'Test_QubitMemory'


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
    memory = MemorySample(register=[reg1, reg2, reg3])
    return memory


class Test_create_gate_op_via_helper_function(unittest.TestCase):
    def test_with_control(self):
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
        instruc_dict = {
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
        gate_op = gate_operation_from_instruction_dict(instruc_dict)
        self.assertTrue(gate_op.gate_dict['alias'] == 'Flip')
        self.assertDictEqual(gate_op.target_dict,
                             {'register': 'reg3', 'local_index': 0})


class TestOperation_Init(unittest.TestCase):
    def test_with_control(self):
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
        instruc_dict = {
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
        GateOperation(
            instruction=GateInstruction(instruc_dict=instruc_dict))

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
        op = GateOperation(instruction=GateInstruction(opdict))
        # Error: target out of local range.
        #self.assertFalse(op.is_applicable(memory=get_test_memory()))
        self.assertRaises(GateOperationValidationError, op.ready, get_test_memory())

    def test_instruction_validation_failure(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        opdict = {
            'gate': {
                'parameters': {}
            },
            'target': {
                'register': 'reg1',
                'local_index': 0
            },
            'control': {
                'list': [el, el2]
            },
        }
        self.assertRaises(GateInstructionDictValidationError, GateInstruction,
                          opdict)


class Test_on_qubit_memory_TargetErrors(unittest.TestCase):
    def test_target_unknown_register(self):
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
                'register': 'reg11', # memory has no register labelled this
                'local_index': 0
            },
            'control': {
                'list': [el, el2]
            },
        }
        op = GateOperation(instruction=GateInstruction(opdict))
        self.assertRaises(GateOperationValidationError,
                          op.ready, get_test_memory())

    def test_target_index_out_of_range(self):
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
                'register': 'reg1',
                'local_index': 4
            },
            'control': {
                'list': [el, el2]
            },
        }
        op = GateOperation(instruction=GateInstruction(opdict))
        #self.assertFalse(op.is_applicable(memory=get_test_memory()))
        self.assertRaises(GateOperationValidationError, op.ready, get_test_memory())


def simple_memory():
    """ Test memory """
    # 1st register
    s1 = qubit_from_bitlist([(1, '1')])
    reg1 = QubitRegister(label='reg1', state=s1)
    # 2nd register
    s2 = qubit_from_bitlist([(1, '1')])
    reg2 = QubitRegister(label='reg2', state=s2)
    # 3rd register
    s3 = qubit_from_bitlist([(1, '1')])
    reg3 = QubitRegister(label='reg3', state=s3)
    # memory
    memory = MemorySample(register=[reg1, reg2, reg3])
    return memory

class Test_Operation_with_User_Defined_Gate(unittest.TestCase):
    def test_control(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg2',
            'local_index': 0,
            'state': '1'
        }
        # user-defined, though borrowed from repertoire
        instance = singles['Flip']
        instruc_dict = {
            'gate': {
                'instance': instance,
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
        go = GateOperation(
            instruction=GateInstruction(instruc_dict=instruc_dict))
        memory = simple_memory()
        memory.operation_socket(go)
        expected_state = qubit_from_bitlist([(1, '110')])
        self.assertTrue(memory.get_global_state() == expected_state)
