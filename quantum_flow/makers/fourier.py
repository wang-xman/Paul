#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_flow.fourier.py

PATH

[app_root]/quantum_flow/fourier.py

INTRO

Specialised flow maker functions.

Quantum Fourier transform related flow makers.

CONTENT

`fourier_flow_on_register(register=None)` - Returns
a `Flow` object to apply quantum Fourier transform
on the state in a register; this `Flow` object replaces
the quantum transform

`fourier_flow_on_memory(memory=None)` - Returns a `Flow`
object to apply quantum Fourier transform on the state
in a memory

TODO Flow maker shall only work with the metadata of the
register, such as register info. It needs no real presence
of register object.

LOG

Updated on 28 September 2021 | Created on 20 July 2021
"""
from quantum_operation.gate import gate_operation_from_instruction_dict as GOfID

from quantum_flow.quantum_flow.utils import validate_register_for_flow
from quantum_flow.quantum_flow.errors import QuantumFlowError
from quantum_flow.quantum_flow import QuantumFlow

from .swap import overall_swap_flow_on_register

_MODULE_LOCATION_ = 'quantum_flow.makers.fourier'


class FourierFlowError(QuantumFlowError):
    """ Error raised by SWAP flow maker"""
    header = 'Swap_Flow_Error'


# Quantum Fourier related flows
def quantum_fourier_flow_on_register(register=None):
    """ Quantum Fourier flow : Apply QFT on a register

    Quantum Fourier transform on the selected register.
    """
    validate_register_for_flow(
        register,
        caller_location=_MODULE_LOCATION_+'.quantum_fourier_flow_on_register')
    oplist = []
    noq = register.noq
    for i in range(0, noq, 1):
        # first, Walsh-Hadamard
        hadamard_instruc_dict = {
            'gate': {
                'alias': 'Hadamard',
            },
            'target': {
                'register': register.label,
                'local_index': i
            }
        }
        oplist.append(GOfID(hadamard_instruc_dict))
        # then, controlled phase rotation
        for j in range(i + 1, noq, 1):
            ctrl_phase_rotation_instruc_dict = {
                'gate': {
                    'alias': 'PhaseRotation',
                    'parameters': {
                        'n': 1,
                        'm': j - i + 1
                    }
                },
                'target': {
                    'register': register.label,
                    'local_index': i
                },
                'control': {
                    'list': [
                        {
                            'register': register.label,
                            'local_index': j,
                            'state': '1'
                        }
                    ]
                }
            }
            oplist.append(GOfID(ctrl_phase_rotation_instruc_dict))
    total_flow = QuantumFlow(operation=oplist)
    # last, overall swap
    final_swap = overall_swap_flow_on_register(register)
    return total_flow.merge(final_swap)


def fourier_flow_on_memory(memory=None):
    """ Operation Helper : Flow to apply QFT on a memory

    TODO Implement this.
    """


def inverse_quantum_fourier_flow_on_register(register=None):
    """ Operation Helper : Flow to apply IQFT on a register

    Inverse quantum Fourier transform on the selected register.
    """
    validate_register_for_flow(
        register,
        caller_location=_MODULE_LOCATION_ + \
                '.inverse_quantum_fourier_flow_on_register'
    )
    oplist = []
    noq = register.noq
    for i in range(0, noq, 1):
        # first, Walsh-Hadamard
        hadamard_instruc_dict = {
            'gate': {
                'alias': 'Hadamard',
            },
            'target': {
                'register': register.label,
                'local_index': i
            }
        }
        oplist.append(GOfID(hadamard_instruc_dict))
        # then, controlled phase rotation
        for j in range(i + 1, noq, 1):
            ctrl_phase_rotation_instruc_dict = {
                'gate': {
                    'alias': 'InversePhaseRotation',
                    'parameters': {
                        'n': 1,
                        'm': j - i + 1
                    }
                },
                'target': {
                    'register': register.label,
                    'local_index': i
                },
                'control': {
                    'list': [
                        {
                            'register': register.label,
                            'local_index': j,
                            'state': '1'
                        }
                    ]
                }
            }
            oplist.append(GOfID(ctrl_phase_rotation_instruc_dict))
    total_flow = QuantumFlow(operation=oplist)
    # last, overall swap
    final_swap = overall_swap_flow_on_register(register)
    return total_flow.merge(final_swap)
