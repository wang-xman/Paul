#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_flow.makers.walsh_hadamard.py

PATH

[app_root]/quantum_flow/makers/walsh_hadamard.py

INTRO

Specialised flow makers.

Walsh-Hadamard gate related flow makers.

CONTENT

`hadamard_flow_on_register(register=None)` - Returns a
`Flow` object to apply qubit-wise Walsh-Hadarmard gate
operations on the state in
a register

`hadamard_flow_on_memory(memory=None)` - Returns a `Flow`
object to apply qubit-wise Walsh-Hadarmard gate operations
on the state in a memory

TODO Flow maker shall only work with the metadata of the
register, such as register info. It needs no real presence
of register object.

LOG

Updated on 02 October 2021 | Created on 27 August 2021
"""
from quantum_operation.gate import gate_operation_from_instruction_dict as GOfID

from quantum_flow.quantum_flow.utils import validate_memory_for_flow, \
    validate_register_for_flow
from quantum_flow.quantum_flow.errors import QuantumFlowError
from quantum_flow.quantum_flow import QuantumFlow

_MODULE_LOCATION_ = 'quantum_flow.makers.walsh_hadamard'


class WalshHadamardFlowError(QuantumFlowError):
    """ Error raised by Walsh-Hadamard flow maker"""
    header = 'Walsh_Hadamard_Flow_Error'


# Walsh-Hadamard gate related flows
def hadamard_flow_on_register(register):
    """ Walsh-Hadamard flow on a register

    ARGUMENTS

    `register` (`QubitRegisterMetadata` or `QubitRegister`):
    a register or register metadata instance

    RETURN

    A `QuantumFlow` instance capable of applying Walsh-Hadamard
    gate on every qubit in the register.
    """
    validate_register_for_flow(register,
            caller_location=_MODULE_LOCATION_+'.hadamard_flow_on_register')
    # operation list
    oplist = []
    for i in range(0, register.noq):
        # instruction dict for each qubit
        bitwise_instruc_dict = {
            'gate': {
                'alias': 'Hadamard',
            },
            'target': {
                'register': register.label,
                'local_index': i
            }
        }
        oplist.append(GOfID(bitwise_instruc_dict))
    return QuantumFlow(operation=oplist)


def hadamard_flow_on_memory(memory):
    """ Quantum flow to apply Walsh-Hadamard on a memory

    ARGUMENTS

    `memory` (`QubitMemory`) : an active qubit memory

    RETURN

    A quantum flow that is capable of applyting Walsh-Hadamard
    gate on EACH qubit in a memory. NOTE Walsh-Hadamard gate is
    applied to EVERY qubit in the target memory.
    """
    validate_memory_for_flow(memory,
            caller_location=_MODULE_LOCATION_ + 'hadamard_flow_on_memory')
    oplist = []
    for reglabel in memory.get_all_labels():
        reg_metadata = memory.get_register_metadata_by_label(reglabel)
        for i in range(0, reg_metadata.noq):
            # instruction dict for each qubit
            bitwise_instruc_dict = {
                'gate': {
                    'alias': 'Hadamard',
                },
                'target': {
                    'register': reglabel,
                    'local_index': i
                }
            }
            oplist.append(GOfID(bitwise_instruc_dict))
    return QuantumFlow(operation=oplist)


def hadamard_flow(memory=None, register=None):
    """ Hadamard Flow : Flow to apply Walsh-Hadamard gate

    Generic function to create a hadamard flow.

    ARGUMENTS

    `memory` (`QubitMemory`) : an active qubit memory instance

    `regsiter` (`QubitRegister` or `QubitRegisterMetadata`) :
    a qubit register or qubit register metadata

    RETURN

    `flow` (`QuantumFlow`) : a quantum flow capable of
    performing Walsh-Hadamard operations on designated qubits
    """
    flow = None
    if memory is None and register is None:
        raise QuantumFlowError(message="Hadamard gate operation flow " +\
                "requires a qubit memory or qubit reqister.",
                location=_MODULE_LOCATION_+'.hadamard_flow')
    if memory is not None and register is None:
        flow = hadamard_flow_on_memory(memory)
    elif memory is None and register is not None:
        flow = hadamard_flow_on_register(register)
    elif memory is not None and register is not None:
        if register.label in memory.get_all_labels():
            flow = hadamard_flow_on_register(register)
        else:
            raise QuantumFlowError("Register with " +\
                    "label '{}' ".format(register.label) +\
                    "cannot be found in the target memory.",
                    location=_MODULE_LOCATION_+'.hadamard_flow')
    else:
        raise QuantumFlowError("Hadamard gate operation flow " +\
                "requires a qubit memory or qubit reqister.",
                location=_MODULE_LOCATION_ + '.hadamard_flow')
    return flow
