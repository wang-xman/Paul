#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

bit.base.py

PATH

[app_root]/bit/base.py

INTRO

Base classes and objected used in this package.

LOG

Updated on 30 September 2021 | Created on 06 November 2020
"""
from common.validator import Base_Validator
from common.exception import Generic_Error, Validation_Error


class BitBaseValidationError(Validation_Error):
    """ Package wide validation error"""
    header = 'Bit_Base_Validation_Error'


class BitBaseError(Generic_Error):
    """ Package wide base error

    Excluding bit validation error.
    """
    header = 'Bit_Base_Error'


class BitBaseValidator(Base_Validator):
    """ Package wide base validator """
    error_class = BitBaseValidationError
