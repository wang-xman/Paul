#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_flow.makers.swap.py

PATH

[app_root]/quantum_flow/makers/swap.py

INTRO

Specialised flow maker functions.

SWAP gate operation related flow makers.

CONTENT

`overall_swap_flow_on_register(register)` - Returns
a `Flow` object to apply overall swap operation on
all qubits in a register

TODO Flow maker shall only work with the metadata of
the register, such as register info. It needs no real
presence of register object.

TODO Introduce decorator to validate indices and memories.

LOG

Updated on 02 October 2021 | Created on 27 August 2021
"""
from quantum_operation.gate import gate_operation_from_instruction_dict as GOfID

from quantum_flow.quantum_flow.utils import validate_memory_for_flow, \
    validate_register_for_flow, validate_local_index_on_register
from quantum_flow.quantum_flow.errors import QuantumFlowError
from quantum_flow.quantum_flow import QuantumFlow

_MODULE_LOCATION_ = 'quantum_flow.makers.swap'


class SwapFlowError(QuantumFlowError):
    """ Error raised by SWAP flow maker"""
    header = 'Swap_Flow_Error'


# Bitwise-SWAP related flows
def swap_flow(local_index_a, local_index_b, register=None):
    """ Bit-Swap Flow Register: swap a pair of selected bits

    For a pair of qubits, swap is implemented as three
    sequential CNOT gate operations. The flow is hence
    consisting of three gate operation instances.

    ARGUMENTS

    `local_index_a` (`int`) : local index of the bit to be swapped

    `local_index_b` (`int`) : local index of the bit to be swapped

    `register` (`QubitRegister` or `QubitRegsiterMetadata`) :
    a qubit register or qubit-regsiter metadata

    RETURN

    A quantum flow
    """
    validate_register_for_flow(register,
            caller_location=_MODULE_LOCATION_ + '.swap_flow')
    validate_local_index_on_register(
        local_index=local_index_a,
        register=register,
        caller_location=_MODULE_LOCATION_ + '.swap_flow')
    validate_local_index_on_register(
        local_index=local_index_b,
        register=register,
        caller_location=_MODULE_LOCATION_ + '.swap_flow')
    oplist = []
    CNOT_1st = {
        'gate': {
            'alias': 'Flip',
        },
        'target': {
            'register': register.label,
            'local_index': local_index_a
        },
        'control': {
            'list': [
                {
                    'register': register.label,
                    'local_index': local_index_b,
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
            'register': register.label,
            'local_index': local_index_b
        },
        'control': {
            'list': [
                {
                    'register': register.label,
                    'local_index': local_index_a,
                    'state': '1'
                }
            ]
        }
    }
    oplist.append(GOfID(CNOT_1st))
    oplist.append(GOfID(CNOT_2nd))
    oplist.append(GOfID(CNOT_1st))
    return QuantumFlow(operation=oplist)


def swap_flow_on_memory(global_index_a, global_index_b, memory=None):
    """ Bit-Swap Flow Memory : Swap two globally indexed qubits

    ARGUMENTS

    `global_index_a` (`int`) : index of a bit with respect to
    the global state in memory

    `global_index_b` (`int`) : index of a bit with respect to
    the global state in memory

    `memory` (`QubitMemory`) : an active qubit memory

    RETURN

    A quantum flow object

    NOTE Not tested.
    """
    validate_memory_for_flow(
        memory,
        caller_location=_MODULE_LOCATION_ + '.swap_flow_on_memory')
    local_a = memory.to_local_index(global_index_a)
    local_b = memory.to_local_index(global_index_b)
    oplist = []
    CNOT_1st = {
        'gate': {
            'alias': 'Flip',
        },
        'target': {
            'register': local_a['label'],
            'local_index': local_a['local_index']
        },
        'control': {
            'list': [
                {
                    'register': local_b['label'],
                    'local_index': local_b['local_index'],
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
            'register': local_b['label'],
            'local_index': local_b['local_index']
        },
        'control': {
            'list': [
                {
                    'register': local_a['label'],
                    'local_index': local_a['local_index'],
                    'state': '1'
                }
            ]
        }
    }
    oplist.append(GOfID(CNOT_1st))
    oplist.append(GOfID(CNOT_2nd))
    oplist.append(GOfID(CNOT_1st))
    return QuantumFlow(operation=oplist)


def overall_swap_flow_on_register(register=None):
    """ Quantum flow to apply overall swap on a register

    Overall swap on all qubits in a register.

    First bit is swapped with the last one; second with the
    penultimate, so on. For an odd number of qubits, middle
    bit is untouched.

    ARGUMENTS

    `register` (`QubitRegister` or `QubitRegisterMetadata`):
    a qubit register or a qubit-register metadata

    RETURN

    A `QuantumFlow` object capable of overall swap on all qubits
    in the register.
    """
    validate_register_for_flow(
        register,
        caller_location=_MODULE_LOCATION_ + \
                '.overall_swap_flow_on_register()'
    )
    # operation list
    oplist = []
    upper = 0
    if register.noq % 2: # noq is odd
        upper = int((register.noq - 1) / 2)
    else: # noq is even
        upper = int(register.noq / 2)
    for i in range(0, upper):
        CNOT_1st = {
            'gate': {
                'alias': 'Flip',
            },
            'target': {
                'register': register.label,
                'local_index': i
            },
            'control': {
                'list': [
                    {
                        'register': register.label,
                        'local_index': register.noq - 1 - i,
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
                'register': register.label,
                'local_index': register.noq - 1 - i
            },
            'control': {
                'list': [
                    {
                        'register': register.label,
                        'local_index': i,
                        'state': '1'
                    }
                ]
            }
        }
        oplist.append(GOfID(CNOT_1st))
        oplist.append(GOfID(CNOT_2nd))
        oplist.append(GOfID(CNOT_1st))
    return QuantumFlow(operation=oplist)
