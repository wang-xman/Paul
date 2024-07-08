#!/usr/bin/env python3.6
#-*- coding:utf-8 -*-
"""
File under test
    quantum_circuit.grover.py

Main test
    Grover search using quantum flows.
    In this test, the U operation is a single-qubit
    operator.

Updated
    04 September 2021
"""
import unittest

from qubit.utils import qubit_from_bitlist
from quantum_register import QubitRegister
from quantum_memory.qubit_memory import QubitMemory
from quantum_operation.gate import gate_operation_from_instruction_dict as GOfID
from quantum_operation.measurement import \
    measurement_operation_from_instruction_dict as MOfID

from quantum_circuit.grover import grover_search

def test_memory():
    comp_init_state = qubit_from_bitlist([(1, '0000')])
    comp_reg = QubitRegister(state=comp_init_state, label='COMPUTER')
    anc_init_state = qubit_from_bitlist([(1, '1')])
    anc_reg = QubitRegister(state=anc_init_state, label='ANCILLA')
    return QubitMemory(register=[comp_reg, anc_reg])


def test_oracle_operation(computer=None, ancilla=None):
    """ Oracle operation

    TODO Provide a function to generate oracle flow using
    bit string.
    """
    # search for state |1110>
    # implemented as a multiple-controlled operation
    oracle_dict = {
        'gate': {
            'alias': 'Flip'
        },
        'target': {
            'register': ancilla.label,
            'local_index': 0
        },
        'control':{
            'list': [
                {
                    'register': computer.label,
                    'local_index': 0,
                    'state': '1'
                },
                {
                    'register': computer.label,
                    'local_index': 1,
                    'state': '1'
                },
                {
                    'register': computer.label,
                    'local_index': 2,
                    'state': '1'
                },
                {
                    'register': computer.label,
                    'local_index': 3,
                    'state': '0'
                }
            ]
        }
    }
    return GOfID(oracle_dict)


class Test_Grover_Search(unittest.TestCase):
    def test_okay(self):
        memory = test_memory()
        computer_reg = memory.get_register_metadata_by_label('COMPUTER')
        ancilla_reg = memory.get_register_metadata_by_label('ANCILLA')
        # user-defined oracle operation
        oracle_op = test_oracle_operation(
                computer=computer_reg, ancilla=ancilla_reg)
        # Grover flow
        grover = grover_search(computer=computer_reg, ancilla=ancilla_reg,
                               oracle_operation=oracle_op)
        grover.launch_on_memory(memory)
        measurement_op = MOfID({
            'register': computer_reg.label
        })
        ret = memory.operation_socket(measurement_op)
        print(ret)
