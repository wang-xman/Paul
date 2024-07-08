#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_register.errors.py

PATH

[app_root]/quantum_register/errors.py

INTRO

LOG

Updated on 28 September 2021 | Created on 09 May 2021
"""

from .base import RegisterBaseValidationError, RegisterBaseError


class RegisterClassValidationError(RegisterBaseValidationError):
    """
    ENTRY

    `validators.RegisterClassValidator`
    """
    header = 'Register_Class_Validation_Error'


class BaseRegisterInitValidationError(RegisterBaseValidationError):
    """
    ENTRY

    `validators.BaseRegisterInitValidator`
    """
    header = 'Base_Register_Init_Validation_Error'


class RegisterError(RegisterBaseError):
    """
    ENTRY

    `base_register.BaseRegister`
    """
    header = 'Register_Error'
