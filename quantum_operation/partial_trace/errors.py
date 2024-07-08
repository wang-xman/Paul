#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.partial_trace.errors.py

PATH

[app_root]/quantum_operation/partial_trace/errors.py

INTRO

Dedicated errors for partial trace operations.
LOG

Updated on 02 October 2021 | Created on 02 August 2021
"""
from quantum_operation.base import OperationBaseValidationError, \
    OperationBaseError


class PartialTraceOperationValidationError(OperationBaseValidationError):
    """ Error raised by partial-trace operation validators

    ENTRY

    `validators.LocalReferencedOperationValidator`
    """
    header = 'Partial_Trace_Operation_Validation_Error'


class PartialTraceOperationError(OperationBaseError):
    """ Error raise by partial trace operation

    ENTRY

    `operations.PartialTraceOperation`
    """
    header = 'Partial_Trace_Operation'
