#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.measurement.validators.py

PATH

[app_root]/quantum_operation/measurement/validators.py

INTRO

Dedicated validators for measurement.

LOG

Updated on 02 October 2021 | Created on 01 August 2021
"""
from quantum_state import NullState
from quantum_operation.base import OperationBaseValidator
from .errors import MeasurementOperationValidationError

_MODULE_LOCATION_ = 'quantum_operation.measurement.validators'


class MeasurementOperationValidator(OperationBaseValidator):
    """ Validate measurement dict against memory """
    error_class = MeasurementOperationValidationError
    error_location = _MODULE_LOCATION_ + '.MeasurementOperationValidator'

    def __init__(self, instruction, memory=None):
        super().__init__()
        self.validate(instruction, memory)

    def validate(self, instruc, memory):
        """ Main validate method """
        self.validate_register(instruc, memory)
        if self.is_valid:
            if instruc.has_state:
                self.validate_state(instruc, memory)

    def validate_register(self, instruc, memory):
        """ Validate register against memory """
        if not memory.has_register_label(instruc.register):
            self.report_errors("Register with label " +\
                    "'{}' cannot be found ".format(instruc.register) +\
                    "in memory '{}'.".format(memory.label))

    def validate_state(self, instruc, memory):
        """ Validate state used as projection

        State used as projection must have the same number of
        qubits as the state in the register.
        """
        if isinstance(instruc.state, NullState):
            self.report_errors(message="State used as projection " +\
                    "cannot be a zero state.")
        elif instruc.state.noq != \
                memory.get_register_metadata_by_label(instruc.register).noq:
            self.report_errors("State used as projection " +\
                    "has a different number of qubits as " +\
                    "the state in the register.")
