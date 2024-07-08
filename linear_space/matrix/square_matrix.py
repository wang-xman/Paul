#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.matrix.square_matrix.py

PATH

[app_root]/linear_space/matrix/square_matrix.py

INTRO

Square matrix has equal number of rows and columns.

CONTENT

`SquareMatrix` - Square matrix is a special matrix

LOG

Updated on 30 September 2021 | Created on 15 November 2020
"""
from .matrix import Matrix
from .validators import SquareMatrixInitValidator

_MODULE_LOCATION_ = 'linear_space.matrix.square_matrix'


class SquareMatrix(Matrix):
    """ Square Matrix

    Square matrix has a number of columns that equals to its
    number of rows. It is a specialised two-dimensional matrix.
    Concept of eigen system is only applicable to square matrices.

    ATTRIBUTES

    `self.trace` : property; returns the trace of a square matrix
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.SquareMatrix'

    def __init__(self, array=None):
        """ Square Matrix :: init """
        validator = SquareMatrixInitValidator(array=array)
        if validator.is_valid:
            super().__init__(array=array)
        else:
            validator.raise_last_error(
                location=self._ERROR_LOCATION_+'.__init__')

    @property
    def trace(self):
        """ Square Matrix :: Returns the trace """
        summation = 0. + 0.j
        for i in range(0, self.nrows, 1):
            summation += self.as_array()[i][i]
        return summation
