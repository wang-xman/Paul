#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

density_matrix.errors.py

PATH

[app_root]/density_matrix/errors.py

INTRO

Dedicated errors.

LOG

Updated on 26 September 2021 | Created on 23 February 2021
"""
from .base import DensityMatrixBaseError, DensityMatrixBaseValidationError


class DensityMatrixValidationError(DensityMatrixBaseValidationError):
    """
    ENTRY

    `validators.StateInitValidator`
    """
    header = 'Density_Matrix_Validation_Error'


class DensityMatrixError(DensityMatrixBaseError):
    """
    ENTRY

    `density_matrix.DensityMatrix`
    """
    header = 'Density_Matrix_Error'
