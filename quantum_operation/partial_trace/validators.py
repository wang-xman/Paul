#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.partial_trace.validators.py

PATH

[app_root]/quantum_operation/partial_trace/validators.py

INTRO

Dedicated validators for partial trace operations.

LOG

Updated on 02 October 2021 | Created on 02 August 2021
"""
from quantum_operation.base import OperationBaseValidator
from .errors import PartialTraceOperationValidationError

_MODULE_LOCATION_ = 'quantum_operation.partial_trace.validators'


class LocalReferencedOperationValidator(OperationBaseValidator):
    """ Validate local-referenced operation against memory """
    error_class = PartialTraceOperationValidationError
    error_location = _MODULE_LOCATION_ + '.LocalReferencedOperationValidator'

    def __init__(self, instruction, memory):
        super().__init__()
        self.validate(instruction, memory)

    def validate(self, instruc, memory):
        if not memory.has_register_label(instruc.register):
            self.report_errors("Register with label " +\
                    "'{}' does not ".format(instruc.register) +\
                    "exist in memory '{}'.".format(memory.label))
        else:
            # if local index range exists
            if instruc.has_local_index_range:
                valid_range = \
                    memory.get_local_index_range_by_label(instruc.register)
                if min(instruc.local_index_range) < min(valid_range) \
                        or max(instruc.local_index_range) > max(valid_range):
                    self.report_errors("Local index range " +\
                            "requested is beyond the valid range of " +\
                            "register '{}'.".format(instruc['register']))


class GlobalReferencedOperationValidator(OperationBaseValidator):
    """ Validate global-referenced operation against memory """
    error_class = PartialTraceOperationValidationError
    error_location = _MODULE_LOCATION_ + '.GlobalReferencedOperationValidator'

    def __init__(self, instruction, memory):
        super().__init__()
        self.validate(instruction, memory)

    def validate(self, instruc, memory):
        valid_range = memory.global_index_range()
        if min(instruc.global_index_range) < min(valid_range) \
                or max(instruc.global_index_range) > max(valid_range):
            self.report_errors("Global index range " +\
                    "requested is beyond the valid range of " +\
                    "the memory.")


class PartialTraceOperationValidator(OperationBaseValidator):
    """ Validate partial trace operation against memory """
    error_class = PartialTraceOperationValidationError
    error_location = _MODULE_LOCATION_ + '.PartialTraceOperationValidator'

    def __init__(self, instruction, memory=None):
        super().__init__()
        self.validate(instruc=instruction, memory=memory)

    def validate(self, instruc=None, memory=None):
        validator = None
        if not instruc.has_register:
            validator = GlobalReferencedOperationValidator(instruc, memory)
        else:
            validator = LocalReferencedOperationValidator(instruc, memory)
        if not validator.is_valid:
            self.report_errors(validator.get_errors())
