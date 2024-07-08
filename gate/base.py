#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.base.py

PATH

[app_root]/gate/base.py

INTRO

Base error and validators used throughout the pacakge.

LOG

Updated on 30 September 2021 | Created on 16 November 2020
"""
from common.validator import Base_Validator
from common.exception import Generic_Error, Validation_Error


class GateBaseError(Generic_Error):
    """ Generic exception class for gate operation """
    header = "Gate_Base_Error"


class GateBaseValidationError(Validation_Error):
    """ Base class for validation """
    header = "Gate_Base_Validation_Error"


class GateRegistrationError(Generic_Error):
    """ Generic exception class for gate operation """
    header = "Gate_Registration_Error"


class GateBaseValidator(Base_Validator):
    """ Base gate validator class """
    error_class = GateBaseValidationError
