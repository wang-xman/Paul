#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.base.py

PATH

[app_root]/linear_space/base.py

INTRO

Package-wide base classes.

CONTENT

`LinearSpaceBaseError` - Base error class to all classes
in package, except the validation error

`LinearSpaceBaseValidationError` - Base validation error
class to all validation errors in package

`LinearSpaceBaseAlgebraError` - Base error class for errors
raise by algebra functions

`LinearSpaceBaseValidator` - Base validator class to all
validators in package

LOG

Updated on 02 October 2021 | Created on 15 November 2020
"""
from common.exception import Generic_Error, Validation_Error, Algebra_Error
from common.validator import Base_Validator


class LinearSpaceBaseError(Generic_Error):
    """ Generic base error for package """
    header = 'Linear_Space_Base_Error'


class LinearSpaceBaseValidationError(Validation_Error):
    """ Base validation error for package """
    header = 'Linear_Space_Base_Validation_Error'


class LinearSpaceBaseAlgebraError(Algebra_Error):
    """ Base algebra error for package

    Algebra error is meant to be used in algebra functions.
    """
    header = 'Linear_Space_Base_Algebra_Error'


class LinearSpaceBaseValidator(Base_Validator):
    """ Package-wide base validator """
    error_class = LinearSpaceBaseValidationError
