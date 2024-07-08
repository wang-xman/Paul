#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.base.py

PATH

[app_root]/quantum_operation/base.py

INTRO

Package-wide base errors and validators.

CONTENT

`OperationBaseValidationError` - Package-wide base
validation error class

`OperationBaseError` - Package-wide error base class

`OperationBaseValidator` - Package-wide valdiator
base class; all valdiators must subclass from it

LOG

Updated on 28 September 2021 | Created on 18 July 2021
"""
from common.validator import Base_Validator
from common.exception import Generic_Error, Validation_Error


class OperationBaseValidationError(Validation_Error):
    header = "Operation_Valdiation_Error"


class OperationBaseError(Generic_Error):
    """ Used in class `Operation` """
    header = "Operation_Error"


class OperationBaseValidator(Base_Validator):
    """ Base class to all validators in operation app """
    error_class = OperationBaseValidationError
