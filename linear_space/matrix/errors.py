#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.matrix.errors.py

PATH

[app_root]/linear_space/matrix/errors.py


INTRO

Errors used in subpack

CONTENT


LOG

Updated on 30 September 2021 | Created on 15 November 2020
"""
from linear_space.base import LinearSpaceBaseError, \
    LinearSpaceBaseValidationError


class MatrixError(LinearSpaceBaseError):
    """ Used in matrix class """
    header = 'Matrix_Error'


class MatrixInitValidationError(LinearSpaceBaseValidationError):
    """
    ENTRY

    `validators.MatrixInitValidator`
    """
    header = 'Matrix_Init_Validation_Error'


class SquareMatrixInitValidationError(MatrixInitValidationError):
    """
    ENTRY

    `validators.SqaureMatrixInitValidator`
    """
    header = 'Square_Matrix_Init_Validation_Error'



class IdentityMatrixValidationError(MatrixInitValidationError):
    """
    ENTRY

    `validators.IdentityMatrixSizeValidator`
    """
    header = 'Identity_Matrix_Validation_Error'
