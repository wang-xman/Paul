#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.gate.operations.py

PATH

[app_root]/quantum_operation/gate/operations.py

INTRO

Utility function for gate operations.

LOG

Updated on 02 October 2021 | Created on 12 July 2021
"""
from .operations import GateOperation, GateInstruction, GateOperationError

_MODULE_LOCATION_ = 'quantum_operation.gate.utils'


def gate_operation_from_instruction_dict(instruc_dict):
    """ Returns gate operation from an instruction dict

    ARGUMENTS

    `instruc_dict` (`dict`) : instruction dictionary

    RETURN

    `gate_op` (`GateOperation`) : a gate operation instance
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ +\
            '.gate_operation_from_instruction_dict'
    try:
        instruc = GateInstruction(instruc_dict)
        gate_op = GateOperation(instruction=instruc)
        return gate_op
    except Exception as err:
        raise GateOperationError(str(err), location=_ERROR_LOCATION_)
