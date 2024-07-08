"""
MODULE

quantum_operation.gate.errors.py

PATH

[app_root]/quantum_operation/gate/errors.py

INTRO

Dedicate errors for gate opertaion

LOG

Updated on 02 October 2021 | Created on 12 July 2021
"""
from quantum_operation.base import OperationBaseValidationError, \
    OperationBaseError

class GateOperationValidationError(OperationBaseValidationError):
    """ Error raised by gate operation validator

    ENTRY

    `validators.GateOperationValidator`
    """

class GateOperationError(OperationBaseError):
    """ Error raised by gate operation object

    ENTRY

    `operations.GateOperation`
    """
