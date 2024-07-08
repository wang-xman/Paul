#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.parameter.errors.py

PATH

[app_root]/common/parameter/errors.py

INTRO

Error classes for parameter subpack.

CONTENT

LOG

Updated on 30 September 2021 | Created on 19 December 2020
"""
from common.exception.errors import Validation_Error, Generic_Error

_MODULE_LOCATION_ = 'common.parameter.errors.py'


class ParameterValidationError(Validation_Error):
    """ Parameter valdiation error

    Used in parameter validator

    ENTRY

    `parameter.validators.ParameterValidator`
    """
    header = 'Parameter_Validation_Error'


class ParameterError(Generic_Error):
    """ Generic errors reported in paramter objects """
    header = 'Parameter_Error'
