"""
MODULE

quantum_instruction.measurement.errors.py

PATH

[app_root]/quantum_instruction/measurement/errors.py

INTRO

Dedicated errors for measurement instruction subpack.

LOG

Updated on 01 October 2021 | Created on 13 August 2021
"""
from quantum_instruction.base import InstructionBaseValidationError, \
    InstructionBaseError


class MeasurementInstructionDictValidationError(InstructionBaseValidationError):
    """ Error raised by measurement instruction dict validator

    ENTRY

    `validators.MeasurementInstructionDictValidator`
    """
    header = 'Measurement_Instruction_Dict_Validation_Error'


class MeasurementInstructionError(InstructionBaseError):
    """ Error raised by measurement instruction object

    ENTRY

    `instructions.MeasurementInstruction`
    """
    header = 'Measurement_Instruction'
