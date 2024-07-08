#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.matrix.validators.py

PATH

[app_root]/linear_space/matrix/validators.py

INTRO

Validators for matrix subpack.

CONTENT

LOG

Updated on 30 September 2021 | Created on 15 November 2020
"""
from linear_space.base import LinearSpaceBaseValidator
from linear_space.linear_object.linear_object import LinearObjectValidator
from linear_space.number import is_integer

from .errors import MatrixInitValidationError, SquareMatrixInitValidationError,\
    IdentityMatrixValidationError

_MODULE_LOCATION_ = 'linear_space.matrix.validators'


class MatrixInitValidator(LinearObjectValidator):
    """ Two-dimensional matrix validator

    By definition, either dimension of a matrix must be
    at least size 2. Other situations fall into either
    column or row vector.
    """
    error_class = MatrixInitValidationError
    error_location = _MODULE_LOCATION_ + '.MatrixInitValidator'

    def __init__(self, array=None):
        super().__init__(array=array)
        if len(self.get_errors()) == 0:
            self.validate_dimension(array=array)
        if len(self.get_errors()) == 0:
            self._validated_array = array

    def validate_dimension(self, array=None):
        """ Matrix is at least 2-by-2 """
        if len(array) < 2: # row like
            self.report_errors('Array passed in to '      +\
                    'instantiate a matrix is a row-like ' +\
                    'vector. Matrix require at least two rows.')
        elif len(array[0]) < 2: # column like
            self.report_errors('Array passed in to '   +\
                    'instantiate a matrix is in fact ' +\
                    'a column-like vector. Matrix '    +\
                    'requires at least two columns.')
        else:
            pass


class SquareMatrixInitValidator(MatrixInitValidator):
    """ Square matrix validator

    Square matrix is a specialised matrix with equal dimensions.
    """
    error_class = SquareMatrixInitValidationError
    error_location = _MODULE_LOCATION_ + '.SquareMatrixInitValidator'

    def __init__(self, array=None):
        super().__init__(array=array)
        if len(self.get_errors()) == 0:
            self.validate_square(array=array)
        if len(self.get_errors()) == 0:
            self._validated_array = array

    def validate_square(self, array=None):
        if len(array) != len(array[0]):
            self.report_errors('Array is incompatible with a '   +\
                    'square matrix. Number of rows of a sqaure ' +\
                    'matrix must be the same as number of columns')


class IdentityMatrixSizeValidator(LinearSpaceBaseValidator):
    """ Validate row size for making identity matrix

    NOTE Must subclass from the base validator, not matrix
    validator, since the object under validation is not
    an array.
    """
    error_class = IdentityMatrixValidationError
    error_location = _MODULE_LOCATION_ + '.IdentityMatrixSizeValidator'

    def __init__(self, row_size):
        """ Identity Matrix Size Validator :: init """
        super().__init__()
        self.validate(row_size)

    def validate(self, row_size):
        """ Identity Matrix Size Validator :: main """
        if not is_integer(row_size):
            self.report_errors("Size of the identity " +\
                    "matrix requested is not an integer.")
        else:
            if row_size < 2:
                self.report_errors("Row size is smaller "  +\
                        "than 2. An identity matrix must " +\
                        "be at least of size 2 by 2.")
