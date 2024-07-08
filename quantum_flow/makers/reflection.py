#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_flow.makers.reflection.py

PATH

[app_root]/quantum_flow/makers/reflection.py

INTRO

Specialised flow makers.

Reflection about a state is to implement operator such
as `S = I - 2 |00...0><00...0|` which reverses the sign
of the `|00...0>` component in state.

CONTENT

TODO Flow maker shall only work with the metadata of the
register, such as register info. It needs no real presence
of register object.

LOG

Updated on 28 Spetember 2021 | Created on 31 August 2021
"""
from quantum_operation.gate import gate_operation_from_instruction_dict as GOfID

from quantum_flow.quantum_flow.utils import validate_register_for_flow
from quantum_flow.quantum_flow.errors import QuantumFlowError
from quantum_flow.quantum_flow import QuantumFlow

_MODULE_LOCATION_ = 'quantum_flow.makers.reflection'


class ReflectionFlowError(QuantumFlowError):
    """ Error raised by reflection flow maker"""
    header = 'Reflection_Flow_Error'


def reflection_flow_about_zeros(register):
    """ Reflection flow to reflect about state `|00...0>`

    Operator to be implemented is `S = I - 2 |00...0><00...0|`.
    For the single bit case, operator `S` reduces to
        `S = -Z = X Z X`
    which is implmented as
        `S = X H X H X`

    For a multiple-bit register, reflection is implemented as
    a multiple-controlled single-qubit operation. By default,
    single-qubit gates are applied to the LAST qubit.

    ARGUMENTS

    `register` (`QubitRegister` or `QubitRegisterMetadata`) :
    register on which reflection flow is applied to
    """
    oplist = None
    validate_register_for_flow(
        register,
        caller_location=_MODULE_LOCATION_ + 'reflection_flow_about_zero')
    # register has one only bit
    if register.noq == 1:
        # single qubit flip on last bit
        flip_dict = {
            'gate': {
                'alias': 'Flip',
            },
            'target': {
                'register': register.label,
                'local_index': 0
            }
        }
        # Hadamard on last bit
        hadamard_dict = {
            'gate': {
                'alias': 'Hadamard',
            },
            'target': {
                'register': register.label,
                'local_index': 0
            }
        }
        oplist = [
            GOfID(flip_dict),
            GOfID(hadamard_dict),
            GOfID(flip_dict),
            GOfID(hadamard_dict),
            GOfID(flip_dict)
        ]
    else:
        # control list, excludes the last bit
        control_list = []
        for i in range(0, register.noq - 1):
            # instruction dict for each qubit
            single_control_dict = {
                'register': register.label,
                'local_index': i,
                'state': '0'
            }
            control_list.append(single_control_dict)
        # controlled flip
        multiple_controlled_flip_dict = {
            'gate': {
                'alias': 'Flip',
            },
            'target': {
                'register': register.label,
                'local_index': register.noq - 1
            },
            'control': {
                'list': control_list
            }
        }
        # single qubit flip on last bit
        single_qubit_flip_dict = {
            'gate': {
                'alias': 'Flip',
            },
            'target': {
                'register': register.label,
                'local_index': register.noq - 1
            }
        }
        # Hadamard on last bit
        single_qubit_hadamard_dict = {
            'gate': {
                'alias': 'Hadamard',
            },
            'target': {
                'register': register.label,
                'local_index': register.noq - 1
            }
        }
        # full operation list
        oplist = [
            GOfID(single_qubit_flip_dict),
            GOfID(single_qubit_hadamard_dict),
            GOfID(multiple_controlled_flip_dict),
            GOfID(single_qubit_hadamard_dict),
            GOfID(single_qubit_flip_dict)
        ]
    return QuantumFlow(operation=oplist)
