#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.quantum_flow.py

Main test:
    Quantum flow launch method.

Updated:
    26 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory
from quantum_operation.gate import gate_operation_from_instruction_dict as GOfID
from quantum_flow.quantum_flow import QuantumFlow


def error_raiser(validator):
    validator.raise_last_error()


def single_register_memory():
    """ Single register memory for testing """
    # 1st register
    s1 = qubit_from_bitlist([(1, '111')])
    reg1 = QubitRegister(label='reg1', state=s1)
    memory = QubitMemory(register=[reg1])
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
    memory = QubitMemory(register=[reg1, reg2, reg3])
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


class Test_QuantumFlow_Launch_Toffoli(unittest.TestCase):
    def test_double_toffoli_on_single_register_memory(self):
        print('--- --- --- Double Toffoli operations on ' +\
              'single-register memory --- --- ---')
        op1 = GOfID(toffoli_dict)
        op2 = GOfID(toffoli_dict)
        memory = single_register_memory()
        flow = QuantumFlow(operation=[op1,op2])
        flow.launch_on_memory(memory)
        expected_state = qubit_from_bitlist([(1,'111')])
        self.assertTrue(memory.get_global_state() == expected_state)

    def test_triple_toffoli_on_single_register_memory(self):
        print('--- --- --- Triple Toffoli operations on ' +\
              'single-register memory --- --- ---')
        op1 = GOfID(toffoli_dict)
        op2 = GOfID(toffoli_dict)
        memory = single_register_memory()
        #print(memory.get_global_state())
        flow = QuantumFlow(operation=[op1,op2,op1])
        #print(memory.get_global_state())
        flow.launch_on_memory(memory)
        expected_state = qubit_from_bitlist([(1,'110')])
        self.assertTrue(memory.get_global_state() == expected_state)


# Hadamard is a single-qubit operation
hadamard_dict = {
    'gate': {
        'alias': 'Hadamard'
    },
    'target': {
        'register': 'reg1',
        'local_index': 0
    }
}

class Test_QuantumFlow_Hadamard_then_Toffoli(unittest.TestCase):
    def test_hadamard_then_toffoli(self):
        print('--- --- --- Hadamard then Toffoli operations on ' +\
              'single-register memory --- --- ---')
        op1 = GOfID(hadamard_dict)
        op2 = GOfID(toffoli_dict)
        memory = single_register_memory()
        flow = QuantumFlow(operation=[op1,op2])
        flow.launch_on_memory(memory)
        expected_state = qubit_from_bitlist([(1,'011'), (-1, '110')])
        self.assertTrue(memory.get_global_state() == expected_state)


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
