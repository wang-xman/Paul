#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    operation.gate_operation.py

Main test:
    Gate operation launch method.

Updated:
    12 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_instruction.gate import GateInstruction
from quantum_operation.gate import GateOperation
from quantum_memory.qubit_memory import QubitMemory


def error_raiser(validator):
    validator.raise_last_error()


class MemorySample(QubitMemory):
    label = 'Test_QubitMemorySample'


def single_register_memory():
    """ Single register memory for testing """
    # 1st register
    s1 = qubit_from_bitlist([(1, '111')])
    reg1 = QubitRegister(label='reg1', state=s1)
    memory = MemorySample(register=[reg1])
    return memory


def multiple_register_memory():
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

# Toffoli requires at least 3 bits.
toffoli_dict = {
    'gate': {
        'alias': 'Flip'
    },
    'target': {
        'register': 'reg1',
        'local_index': 2
    },
    'control': {
        'list': [
            {
                'register': 'reg1',
                'local_index': 0,
                'state': '1'
            },
            {
                'register': 'reg1',
                'local_index': 1,
                'state': '1'
            }
        ]
    }
}

phaserotation_dict = {
    'gate': {
        'alias': 'PhaseRotation',
        'parameters':{
            'n': 1,
            'm': 2
        }
    },
    'target': {
        'register': 'reg1',
        'local_index': 2
    },
    'control': {
        'list': [
            {
                'register': 'reg1',
                'local_index': 0,
                'state': '1'
            },
            {
                'register': 'reg1',
                'local_index': 1,
                'state': '1'
            }
        ]
    }
}

class TestOperation_Apply(unittest.TestCase):
    def test_toffoli(self):
        print('--- --- --- Toffoli operation --- --- ---')
        instruc = GateInstruction(instruc_dict=toffoli_dict)
        op = GateOperation(instruction=instruc)
        memory = single_register_memory()
        #memory.form_global_state()
        print(memory.get_global_state())
        #op.socket_launcher(memory)
        memory.operation_socket(op)
        print(memory.get_global_state())

    def test_phase_rotation(self):
        print('--- --- --- Phase rotation operation --- --- ---')
        instruc = GateInstruction(instruc_dict=phaserotation_dict)
        op = GateOperation(instruction=instruc)
        memory = single_register_memory()
        #memory.form_global_state()
        print(memory.get_global_state())
        #op.socket_launcher(memory)
        memory.operation_socket(op)
        print(memory.get_global_state())
