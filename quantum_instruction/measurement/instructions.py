#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_instruction.measurement_instruction.py

PATH

[app_root]/quantum_instruction/measurement_instruction.py

INTRO

Measurement instruction is the instruction behind
measurement operation.

Examples

[Measure a register in computational basis]
To measure an entire register labelled 'COMPREG' in its
computational basis
    {
        'register': 'COMPREG'
    }
is the required operation dictionary.

[Measure a register in designated projection state]
To measure a register labelled 'COMPUREG' using a given
qubit state, operation dictionary
    {
        'register': 'COMPREG',
        'state': QubitState instance
    }
where value to `state` is a `QubitState` instance.

LOG

Updated on 01 October 2021 | Created on 13 August 2021
"""
from .validators import MeasurementInstructionDictValidator
from .errors import MeasurementInstructionError

_MODULE_LOCATION_ = 'quantum_instruction.measurement.instructions'


class MeasurementInstruction:
    """ Measurement operation instruction

    NOTE Per the version 25 August 2021, only measurement
    of an entire register is allowed. Therefore, instruction
    dictionary contains the required key 'register' and an
    optional key 'state'.
    """
    def __init__(self, instruc_dict):
        validator = MeasurementInstructionDictValidator(
                instruc_dict=instruc_dict)
        if validator.is_valid:
            self._internal_dict = validator.validated_data()
        else:
            validator.raise_last_error()

    @property
    def register(self):
        """ Measurement Instruction : Returns register label """
        return self._internal_dict['register']

    @property
    def has_state(self):
        """ Measurement Instruction : Verifies if projection state exists """
        ret = False
        if 'state' in self._internal_dict.keys():
            ret = True
        return ret

    @property
    def state(self):
        """ Measurement Instruction : Returns projection state if exists """
        ret = None
        if self.has_state:
            ret = self._internal_dict['state']
        else:
            raise MeasurementInstructionError("Measurement instruction " +\
                    "carries no projection state.")
        return ret
    