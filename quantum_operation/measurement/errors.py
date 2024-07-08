#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.measurement.errors.py

PATH

[app_root]/quantum_operation/measurement/errors.py

INTRO

Dedicated errors.

LOG

Updated on 02 October 2021 | Created on 01 August 2021
"""
from quantum_operation.base import OperationBaseError, \
    OperationBaseValidationError


class MeasurementOperationValidationError(OperationBaseValidationError):
    """ Error raised by measurement operation validators
    ENTRY

    `validator.MeasurementOperationValidator`
    """
    header = 'Measurement_Operation_Validation_Error'


class MeasurementOperationError(OperationBaseError):
    """ Error raised measurement operation

    ENTRY

    `operations.MeasurementOperation`
    """
