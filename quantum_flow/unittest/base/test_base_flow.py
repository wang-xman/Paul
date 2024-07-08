#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_flow.base.py

Main test:
    Base quantum flow object.

Updated:
    26 August 2021
"""
import unittest
from quantum_operation.gate import gate_operation_from_instruction_dict as GOfID
from quantum_flow.quantum_flow.base_flow import BaseQuantumFlow, \
    BaseQuantumFlowError
from quantum_flow.quantum_flow import QuantumFlowError

opdict1 = {
    'gate': {
        'alias': 'PhaseRotation',
        'parameters': {
            'n': 0,
            'm': 1
        }
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
                'state': '0'
            },
            {
                'register': 'reg1',
                'local_index': 1,
                'state': '1'
            }
        ]
    }
}

opdict2 = {
    'gate': {
        'alias': 'Flip'
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
                'state': '0'
            },
            {
                'register': 'reg1',
                'local_index': 1,
                'state': '1'
            }
        ]
    }
}

# Toffoli requires at least 3 bits.
opdict3 = {
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

op1 = GOfID(opdict1)
op2 = GOfID(opdict2)
op3 = GOfID(opdict3)


class Test_BaseFlow_Init(unittest.TestCase):
    def test_init_with_one_op(self):
        flow = BaseQuantumFlow(operation=op1)
        self.assertTrue(flow.number_of_operations == 1)
        self.assertFalse(flow.is_empty)

    def test_non_operation_object(self):
        self.assertRaises(BaseQuantumFlowError, BaseQuantumFlow, {})

    def test_with_list(self):
        flow = BaseQuantumFlow(operation=[op1,op2])
        self.assertFalse(flow.is_empty)
        self.assertTrue(flow.number_of_operations == 2)

    def test_with_list_and_nonop(self):
        #flow = Flow(operation=[op1,{'cool': 1}])
        self.assertRaises(BaseQuantumFlowError, BaseQuantumFlow,
                          **{'operation':[op1,{'cool': 1}]})


class Test_BaseFlow_Append(unittest.TestCase):
    def test_init_with_one_op(self):
        flow = BaseQuantumFlow(operation=op1)
        self.assertTrue(flow.number_of_operations == 1)
        self.assertFalse(flow.is_empty)
        flow.append(op2)
        self.assertTrue(flow.number_of_operations == 2)
        op = flow.get_operation_by_rank(1)
        self.assertTrue(op.gate_dict['alias'] == 'Flip')


class Test_BaseFlow_Prepend(unittest.TestCase):
    def test_init_with_one_op(self):
        flow = BaseQuantumFlow(operation=op1)
        self.assertTrue(flow.number_of_operations == 1)
        self.assertFalse(flow.is_empty)
        flow.prepend(op2)
        self.assertTrue(flow.number_of_operations == 2)
        op = flow.get_operation_by_rank(0)
        self.assertTrue(op.gate_dict['alias'] == 'Flip')


class Test_BaseFlow_Insert(unittest.TestCase):
    def test_init_with_two_ops(self):
        flow = BaseQuantumFlow(operation=[op1, op2])
        self.assertTrue(flow.number_of_operations == 2)
        flow.insert(op3, rank=0)
        self.assertTrue(flow.number_of_operations == 3)
        op = flow.get_operation_by_rank(0)
        self.assertTrue(op.gate_dict['alias'] == 'Flip')

    def test_init_with_two_ops_2(self):
        flow = BaseQuantumFlow(operation=[op1, op2])
        self.assertTrue(flow.number_of_operations == 2)
        flow.insert(op3, rank=1)
        self.assertTrue(flow.number_of_operations == 3)
        op = flow.get_operation_by_rank(2)
        self.assertTrue(op.gate_dict['alias'] == 'Flip')

    def test_init_with_two_ops_3(self):
        flow = BaseQuantumFlow(operation=[op2, op3])
        self.assertTrue(flow.number_of_operations == 2)
        # without rank
        flow.insert(op1)
        self.assertTrue(flow.number_of_operations == 3)
        op = flow.get_operation_by_rank(2)
        self.assertTrue(op.gate_dict['alias'] == 'PhaseRotation')

    def test_rank_out_of_range(self):
        flow = BaseQuantumFlow(operation=[op2, op3])
        self.assertTrue(flow.number_of_operations == 2)
        # Error: rank out of range
        #flow.insert(op1, rank=4)
        self.assertRaises(BaseQuantumFlowError, flow.insert, op1, 4)
        #self.assertTrue(flow.number_of_operations == 3)
        #op = flow.op_at_rank(4)
        #self.assertTrue(op.gate['alias'] == 'PhaseRotation')
