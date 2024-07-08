#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

qubit.errors.py

PATH

[app_root]/qubit/errors.py

INTRO

Validators for objects in states. Instantiate the validator
with data for validation. Invoke `is_valid` method before
acquiring validated data.

CONTENT

LOG

Updated on 30 September 2021 | Created on 23 June 2020
"""
from .base import QubitBaseValidationError, QubitBaseError, \
    QubitBaseAlgebraError


class QubitStateValidationError(QubitBaseValidationError):
    """
    ENTRY

    `validators.QubitStateValidator`
    """
    header = 'Qubit_State_Validation_Error'


class SingleQubitBasisValidationError(QubitBaseValidationError):
    """
    ENTRY

    `validators.SingleQubitBasisValidator`
    """
    header = 'Single_Qubit_Basis_Validation_Error'


class QubitStateError(QubitBaseError):
    """
    ENTRY

    `qubit.QubitState`
    """
    header = 'Qubit_Error'


class QubitAlgebraFunctionError(QubitBaseAlgebraError):
    header = 'Qubit_Algebra_Function_Error'


# index range related
class IndexRangeBoundValidationError(QubitBaseValidationError):
    """ Index range bound validation error

    ENTRY

    `index_range.IndexRangeBoundValidator`
    """
    header = 'Index_Range_Bound_Validation_Error'


class IndexRangeValidationError(IndexRangeBoundValidationError):
    """ Index range validation error

    Index range is a different concept from index-range bound.

    ENTRY

    `index_range.IndexRangeValidator`
    """
    header = 'Index_Range_Validation_Error'
