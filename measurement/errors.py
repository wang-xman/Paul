#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

measurement.errors.py

PATH

[app_root]/measurement/errors.py

INTRO

Dedicated error classes.

LOG

Updated on 28 September 2021 | Created on 05 April 2021
"""
from .base import MeasurementBaseError, MeasurementBaseValidationError


class TargetSystemValidationError(MeasurementBaseValidationError):
    """ Target system validation error

    ENTRY

    `validators.TargetSystemValidator`
    """
    header = 'Target_System_Validation_Error'


class PartialTraceError(MeasurementBaseError):
    """ Partial trace error

    ENTRY

    Module `partial_trace`
    """
    header = 'Partial_Trace_Error'


class ProjectiveMeasurementError(MeasurementBaseError):
    """ Projective measurement error

    ENTRY

    Module `projective`
    """
    header = "Projective_Measurement_Error"
