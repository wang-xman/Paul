#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

density_matrix.base.py

PATH

[app_root]/density_matrix/base.py

INTRO

Package-wide base errors and validators.

LOG

Updated on 30 September 2021 | Created on 23 February 2021
"""
from common.exception import Generic_Error, Validation_Error
from common.validator import Base_Validator


class DensityMatrixBaseError(Generic_Error):
    header = 'Density_Matrix_Base_Error'


class DensityMatrixBaseValidationError(Validation_Error):
    header = 'Density_Matrix_Base_Validation_Error'


class DensityMatrixBaseValidator(Base_Validator):
    errro_class = DensityMatrixBaseValidationError
