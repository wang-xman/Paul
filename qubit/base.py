#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

qubit.base.py

PATH

[app_root]/qubit/base.py

INTRO

Base error and validator for package.

CONTENT

LOG

Updated on 02 September 2021 | Created on 23 June 2020
"""
from common import Generic_Error, Validation_Error, Algebra_Error
from common import Base_Validator


class QubitBaseError(Generic_Error):
    """ Package-wide base error class """
    header = 'Qubit_Base_Error'


class QubitBaseValidationError(Validation_Error):
    """ Package-wide base validation error """
    header = 'Qubit_Base_Validation_Error'


class QubitBaseAlgebraError(Algebra_Error):
    """ Use in algebra functions """
    header = 'Qubit_Base_Algorithm_Error'


class QubitBaseValidator(Base_Validator):
    """ Package-wide base validator """
    error_class = QubitBaseValidationError
