#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_circuit.phase_estimation.py

PATH

[app_root]/quantum_circuit/phase_estimation.py

INTRO

Phase estimation circuit.

CONTENT

NOTE Current version is tested successful for oracle
gate that is applicable only to a single-qubit ancilla
register. This must be generalised to multiple bit
ancilla. Change to be made in gate application, not here.

TODO

[1] In gate application, I need a function to calculate
U^n type of matrix product for gate matrix.

LOG

Updated on 02 October 2021 | Created on 17 November 2020
"""
from math import pow as power
from quantum_operation.gate import gate_operation_from_instruction_dict as GOfID

from quantum_flow.quantum_flow import QuantumFlow
from quantum_flow.makers.fourier import inverse_quantum_fourier_flow_on_register
from quantum_flow.makers.walsh_hadamard import hadamard_flow_on_register


def controlled_operation_flow(computer=None, ancilla=None, oracle=None):
    """ Controlled operation flow

    Returns a flow to perform c-U, cU^2, c-U^4, ... operations.
    """
    noq = computer.noq
    controlled_operations_list = []
    for index in range(noq-1, -1, -1):
        controlled_operation_dict = {
            'gate': {
                'instance': oracle,
                'parameters': {
                    'n': int(power(noq - 1 - index, 2))
                }
            },
            'target': {
                'register': ancilla.label,
                'local_index': 0
            },
            'control': {
                'list': [
                    {
                        'register': computer.label,
                        'local_index': index,
                        'state': '1'
                    }
                ]
            }
        }
        controlled_operations_list.append(GOfID(controlled_operation_dict))
    return QuantumFlow(operation=controlled_operations_list)


def phase_estimation(computer=None, ancilla=None, oracle=None):
    """ Phase estimation

    TODO
    [1] Initialise computational register to |0...00>

    """
    hadamard_flow = hadamard_flow_on_register(computer)
    controlled_operations = controlled_operation_flow(
        computer=computer, ancilla=ancilla, oracle=oracle)
    IQFT_flow = inverse_quantum_fourier_flow_on_register(register=computer)
    total_flow = hadamard_flow.merge(controlled_operations).merge(IQFT_flow)
    return total_flow
