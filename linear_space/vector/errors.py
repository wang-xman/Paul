#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.vector.errors.py

PATH

[app_root]/linear_space/vector/errors.py

INTRO

Errors used in vector subpack.

CONTENT

LOG

Updated on 02 October 2021 | Created on 07 November 2020
"""
from linear_space.base import LinearSpaceBaseError, \
    LinearSpaceBaseValidationError


class VectorError(LinearSpaceBaseError):
    """ Used in base vector

    ENTRY

    `base.BaseVector`
    """
    header = 'Vector_Error'


class VectorValidationError(LinearSpaceBaseValidationError):
    """ Used in base vector init validator
    ENTRY

    `validators.BaseVectorInitValidator`
    """
    header = 'Vector_Validation_Error'


class ColumnVectorError(VectorError):
    """ Used in column vector

    ENTRY

    `column_vector.ColumnVector`
    """
    header = 'Column_Vector_Error'


class ColumnVectorValidationError(VectorValidationError):
    """ Used in column vector init validator
    ENTRY

    `validators.ColumnVectorInitValidator`
    """
    header = 'Column_Vector_Validation_Error'


class StandardBasisVectorValidationError(VectorValidationError):
    """ Used standarf basis vector init validator
    ENTRY

    `validators.StandardBasisVectorInitValidator`
    """
    header = 'Standard_Basis_Vector_Validation_Error'


class RowVectorValidationError(VectorValidationError):
    """ Used in row vector init validator
    ENTRY

    `validators.RowVectorInitValidator`
    """
    header = 'Row_Vector_Validation_Error'


class RowVectorError(VectorError):
    """ Used in row vector

    ENTRY

    `row_vector.RowVector`
    """
    header = 'Row_Vector_Error'
