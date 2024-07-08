#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.matrix.matrix.py

PATH

[app_root]/linear_space/matrix/matrix.py

TODO

[1] Implement matrix string representation.

INTRO

Matrix is modelled as a container object that stores a
2D numpy array as its internal array.

CONTENT

`Matrix` - Generic matrix class and is the base class to
all matrices; matrix is itself a subclass of `LinearObject`

LOG

Updated on 30 September 2021 | Created on 15 November 2020
"""
from linear_space.linear_object.linear_object import LinearObject
from .validators import MatrixInitValidator

_MODULE_LOCATION_ = 'linear_space.matrix.matrix'


class Matrix(LinearObject):
    """ Two-dimensional matrix

    Matrix is a subclass of linear object that stores a
    two-dimensional numpy array as the internal array.
    A matrix is at least 2-by-2, other situations are vector.

    CONSTRUCTOR

    `array` (`numpy.ndarray`): a two-dimensional numpy array

    ATTRIBUTES

    `self.size` : Returns size tuple of a matrix

    `self.nrows` : Return number of rows

    `self.ncols` : Returns number of columns

    `self.__getitem__(, row_index)` : Returns a subarray that
    represents a row indexed by the given row index

    `self.setring_representation()` : Returns a stringified
    representation of matrix TODO Add this!!
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.Matrix'

    def __init__(self, array=None):
        """ Matrix :: init """
        validator = MatrixInitValidator(array=array)
        if validator.is_valid:
            super().__init__(array=array)
        else:
            validator.raise_last_error(
                    location=self._ERROR_LOCATION_+'.__init__')

    @property
    def size(self):
        """ Matrix :: size tuple of a matrix """
        return super().get_size()

    @property
    def nrows(self):
        """ Matrix :: number of rows """
        return super().get_nrows()

    @property
    def ncols(self):
        """ Matrix :: number of columns """
        return super().get_ncols()

    def __getitem__(self, row_index):
        """ Matrix :: Returns a subarray as a row

        The subarray can be further indexed.
        """
        try:
            return super().get_subarray(row_index)
        except Exception as err:
            raise err.relocate(self._ERROR_LOCATION_+'.__getitem__')

    def string_representation(self):
        """ TODO Implement this string repr

        Need to introduce ... symbol to shorten the strings
        """
        pass
