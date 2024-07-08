#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.partial_trace.utils.py

PATH

[app_root]/quantum_operation/partial_trace/utils.py

INTRO

Utility functions for to perform partial trace
operations.

LOG

Updated on 02 October 2021 | Created on 02 August 2021
"""
from .operations import PartialTraceInstruction, PartialTraceOperation, \
    PartialTraceOperationError

_MODULE_LOCATION_ = 'quantum_operation.partial_trace.utils'


def partial_trace_operation_from_instruction_dict(instruc_dict):
    """ Returns partial trace operation from an instruction dict

    ARGUMENTS

    `instruc_dict` (`dict`) : instruction dictionary

    RETURN

    `partial_trace_op` (`PartialTraceOperation`) : a partial
    trace operation instance

    NOTE Not tested.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ +\
            '.partial_trace_operation_from_instruction_dict'
    try:
        instruc = PartialTraceInstruction(instruc_dict)
        partial_trace_op = PartialTraceOperation(instruction=instruc)
        return partial_trace_op
    except Exception as err:
        raise PartialTraceOperationError(str(err), location=_ERROR_LOCATION_)


def partial_trace_on_memory(instruc_dict, memory):
    """ Partial trace on memory utility function

    Apply designated partial trace operation on user-provided
    memory object.

    ARGUMENTS

    `instruc` (`dict`) : operation dictionary for intended
    partial trace operation

    `memory` (`BaseMemory`) : an active quantum memory object
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.partial_trace_on_memory'
    try:
        partial_trace_instruction = \
                PartialTraceInstruction(instruc_dict=instruc_dict)
        partial_trace_operation = \
                PartialTraceOperation(partial_trace_instruction)
        memory.operation_socket(partial_trace_operation)
    except Exception as err:
        raise PartialTraceOperationError(str(err), location=_ERROR_LOCATION_)
