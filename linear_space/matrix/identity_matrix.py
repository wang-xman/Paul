#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.matrix.identity_matrix.py

PATH

[app_root]/linear_space/matrix/identity_matrix.py

INTRO

Identity matrix is a specialised square matrix that
has only 1 on the diagonal entries, all other elements
are zero.

CONTENT

`IdentityMatrix` - Identiy matrix is a specialised
square matrix

LOG

Updated on 30 September 2021 | Created on 15 November 2020
"""
from linear_space.numpy_lib import np_identity
from .square_matrix import SquareMatrix
from .validators import IdentityMatrixSizeValidator

_MODULE_LOCATION_ = 'linear_space.matrix.identity_matrix'


class IdentityMatrix(SquareMatrix):
    """ Identity matrix

    Identify matrix is a square matrix with 1 on the diagonal
    entries and all other entries are zero. Instantiation of
    this matrix is therefore reduced to use simply the size of
    either column or row which is represetned by argument
    `row_size` in the constructor.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.IdentityMatrix'

    def __init__(self, row_size=2):
        """ Identity Matrix :: init """
        row_size_validator = IdentityMatrixSizeValidator(row_size)
        if row_size_validator.is_valid:
            super().__init__(array=np_identity(row_size))
        else:
            row_size_validator.raise_last_error(
                    location=self._ERROR_LOCATION_+'.__init__')
