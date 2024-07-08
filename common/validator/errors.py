#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.validator.errors.py

PATH

[app_root]/common/validator/errors.py

INTRO

Dedicated errors for application-wide base validator.

LOG

Updated on 30 September 2021 | Created on 29 June 2020
"""
from common.exception.errors import Validation_Error


class BaseValidatorError(Validation_Error):
    """ Error raised by base validator

    ENTRY

    `base_validator.Base_Validator`
    """
    header = 'Base_Validator_Error'
