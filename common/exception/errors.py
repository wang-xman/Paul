#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.exception.errors.py

PATH

[app_root]/common/exception/errors.py

INTRO

Application-wide base error and exception.

Error classes in this module are NOT to be
instantiated directly.

CONTENT

`Validation_Error`  - Base class to all errors raised
directly from validaator

`Algebra_Error` - Base class to all errors raised directly
from algebra functions

`Generic_Error` - Base class to all errors that are neither
raised by validator nor algebra function

LOG

Updated on 02 October 2021 | Created on 15 November 2020
"""
from .base import Base_Error


class Validation_Error(Base_Error):
    """ Validation error

    Error directly raised by validator
    """
    header = "Application_Level_Validation_Error"


class Algebra_Error(Base_Error):
    """ Algebra error

    Error directly raised by algebra function.
    """
    header = "Application_Level_Algebra_Error"


class Generic_Error(Base_Error):
    """ Generic error

    Error that is neither raised by validator
    nor by algebra function.

    Base class to most errors in the application.
    """
    header = "Application_Level_Generic_Error"
