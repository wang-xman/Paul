#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

measurement.decorators.py

PATH

[app_root]/measurement/decorators.py

INTRO

Measurement function decorators.

LOG

Updated on 08 October 2021 | Created on 10 April 2021
"""
from common.function.decorators import FunctionInvocationDecorator
from .errors import ProjectiveMeasurementError

class as_measurement_function(FunctionInvocationDecorator):
    """ Used by measurement functions

    Used to validate common arguments defined in all
    measurement functions.
    """
    error_class = ProjectiveMeasurementError
