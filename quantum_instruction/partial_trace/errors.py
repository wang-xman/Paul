"""
MODULE

quantum_instruction.partial_trace.errors.py

PATH

[app_root]/quantum_instruction/partial_trace/errors.py

INTRO

Dedicated errors used in subpack.

LOG

Updated on 01 October 2021 | Created on 13 August 2021
"""
from quantum_instruction.base import InstructionBaseError, \
    InstructionBaseValidationError


class PartialTraceInstructionDictValidationError(
        InstructionBaseValidationError):
    """ Error raise by partial-trace instruc dict validator

    ENTRY

    `validators.LocalReferenceValidator`
    """
    header = 'Partial_Trace_Instruction_Dict_Validation_Error'


class PartialTraceInstructionError(InstructionBaseError):
    """ Error raise by partia-trace instruc object
    ENTRY

    `instructions.PartialTraceInsrtuction`
    """
    header = 'Partial_Trace_Instruction_Error'
