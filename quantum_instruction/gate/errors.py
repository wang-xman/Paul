"""
MODULE

quantum_instruction.gate.errors.py

PATH

[app_root]/quantum_instruction/gate/errors.py

INTRO

Dedicated errors for gate-instruction subpack.

LOG

Updated on 01 October 2021 | Created on 12 August 2021
"""
from quantum_instruction.base import InstructionBaseValidationError, \
    InstructionBaseError


class GateInstructionDictValidationError(InstructionBaseValidationError):
    """ Error raised by gate instruction dict validator
    ENTRY

    `validators.GateSubdictValidator`
    """
    header = 'Gate_Instruction_Dict_Validation_Error'


class GateInstructionError(InstructionBaseError):
    """ Error raise by gate instruction object

    ENTRY

    `instructions.GateInsrtuction`
    """
    header = 'Gate_Instruction_Error'
