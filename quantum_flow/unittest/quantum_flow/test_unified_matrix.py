#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.quantum_flow.py

Main test:
    Convert flow into a unified operator matrix.

Updated:
    24 August 2021
"""
import unittest
from linear_space.algebra import matrix_product
from qubit import QubitState
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

# test operations
CNOT_1st = {
    'gate': {
        'alias': 'Flip',
    },
    'target': {
        'register': 'reg1',
        'local_index': 1
    },
    'control': {
        'list': [
            {
                'register': 'reg1',
                'local_index': 0,
                'state': '1'
            }
        ]
    }
}
CNOT_2nd = {
    'gate': {
        'alias': 'Flip',
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
            }
        ]
    }
}

class TestUnifiedOperatorMatrix(unittest.TestCase):
    def test_okay(self):
        test_memory = single_register_memory()
        op1 = GOfID(CNOT_1st)
        op2 = GOfID(CNOT_2nd)
        flow = QuantumFlow(operation=[op1,op2])
        # unified matrix
        original_state = qubit_from_bitlist([(1, '111')])
        opmat = flow.unified_matrix(test_memory)
        # apply the unified matrix to state vector
        final_vector = matrix_product(opmat, original_state.as_vector())
        expected_state = qubit_from_bitlist([(1, '100')])
        self.assertTrue(final_vector == expected_state.as_vector())


class TestUnifiedOperator(unittest.TestCase):
    def test_okay(self):
        test_memory = single_register_memory()
        op1 = GOfID(CNOT_1st)
        op2 = GOfID(CNOT_2nd)
        flow = QuantumFlow(operation=[op1,op2])
        # create an operator
        op = flow.as_unified_operator(test_memory)
        original_state = qubit_from_bitlist([(1, '111')])
        # apply operator to state vector
        final_state = op.apply(original_state)
        expected_state = qubit_from_bitlist([(1, '100')])
        self.assertTrue(isinstance(final_state, QubitState))
        self.assertTrue(final_state == expected_state)


def multiple_register_memory():
    """ Single register memory for testing """
    # 1st register
    s1 = qubit_from_bitlist([(1, '111')])
    reg1 = QubitRegister(label='reg1', state=s1)
    s2 = qubit_from_bitlist([(1, '10')])
    reg2 = QubitRegister(label='reg2', state=s2)
    memory = QubitMemory(register=[reg1, reg2])
    return memory

class TestUnifiedOperator_TwoRegisters(unittest.TestCase):
    def test_okay(self):
        test_memory = multiple_register_memory()
        op1 = GOfID(CNOT_1st)
        op2 = GOfID(CNOT_2nd)
        flow = QuantumFlow(operation=[op1,op2])
        # create an operator
        op = flow.as_unified_operator(test_memory)
        original_state = qubit_from_bitlist([(1, '11110')])
        # apply operator to state vector
        final_state = op.apply(original_state)
        expected_state = qubit_from_bitlist([(1, '10010')])
        self.assertTrue(isinstance(final_state, QubitState))
        self.assertTrue(final_state == expected_state)


# test operations duo registers
# control and target bits are on two registers
CNOT_1st_2R = {
    'gate': {
        'alias': 'Flip',
    },
    'target': {
        'register': 'reg2',
        'local_index': 0
    },
    'control': {
        'list': [
            {
                'register': 'reg1',
                'local_index': 0,
                'state': '1'
            }
        ]
    }
}
CNOT_2nd_2R = {
    'gate': {
        'alias': 'Flip',
    },
    'target': {
        'register': 'reg2',
        'local_index': 1
    },
    'control': {
        'list': [
            {
                'register': 'reg1',
                'local_index': 1,
                'state': '1'
            }
        ]
    }
}

class TestUnifiedOperator_CrossTwoRegisters(unittest.TestCase):
    def test_okay(self):
        test_memory = multiple_register_memory()
        op1 = GOfID(CNOT_1st_2R)
        op2 = GOfID(CNOT_2nd_2R)
        flow = QuantumFlow(operation=[op1,op2])
        # create an operator
        op = flow.as_unified_operator(test_memory)
        original_state = qubit_from_bitlist([(1, '11110')])
        # apply operator to state vector
        final_state = op.apply(original_state)
        expected_state = qubit_from_bitlist([(1, '11101')])
        self.assertTrue(isinstance(final_state, QubitState))
        self.assertTrue(final_state == expected_state)
