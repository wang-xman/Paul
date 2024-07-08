#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_register.base.py

PATH

[app_root]/quantum_register/base.py

INTRO

Base classes for subpack

LOG

Updated on 30 September 2021 | Created on 09 May 2021
"""
from common.validator import Base_Validator
from common.exception import Generic_Error, Validation_Error

__MODULE_LOCATION__ = 'quantum_register.base'


class RegisterBaseValidationError(Validation_Error):
    """ Exception class for register validation """
    header = "Register_Base_Validation_Error"


class RegisterBaseError(Generic_Error):
    header = "Register_Base_Error"


class RegisterBaseValidator(Base_Validator):
    error_class = RegisterBaseValidationError


class AbstractQuantumRegister:
    """ Abstract class to all registers """
