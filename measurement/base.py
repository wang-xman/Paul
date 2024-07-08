#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

measurement.base.py

PATH

[app_root]/measurement/base.py

INTRO

Error and validator error classes used in application.

LOG

Updated on 28 September 2021 | Created on 05 April 2021
"""
from common.exception import Generic_Error, Validation_Error
from common.validator import Base_Validator


class MeasurementBaseError(Generic_Error):
    header = "Measurement_Base_Error"


class MeasurementBaseValidationError(Validation_Error):
    header = "Measurement_Base_Validatiaon_Error"


class MeasurementBaseValidator(Base_Validator):
    error_class = MeasurementBaseValidationError
