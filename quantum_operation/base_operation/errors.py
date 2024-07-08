#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.base_operation.errors.py

PATH

[app_root]/quantum_operation/base_operation/errors.py

INTRO

Dedicated errors for base quantum operation

LOG

Updated on 02 October 2021 | Created on 18 July 2021
"""
from quantum_operation.base import OperationBaseValidationError, \
    OperationBaseError


class BaseOperationSubclassValidationError(OperationBaseValidationError):
    """ Error raised by base operation subclass validator

    ENTRY

    `validators.BaseOperationSubclassValidator`
    """
    header = 'Base_Operation_Subclass_Validation_Error'


class BaseOperationError(OperationBaseError):
    """ Error raised by base operation object

    ENTRY

    `operations.BaseOperation`
    """
    header = 'Base_Operation_Error'
