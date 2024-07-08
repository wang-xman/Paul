#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.linear_object.linear_object.py

PATH

[app_root]/linear_space/linear_object/linear_object.py

INTRO

Linear object is the core object in this module.
Scalar, vector and matrix are all derived from
linear object.

CONTENT

`LinearObjectValidationError` - Linear object validation
error used in validator

`LinearObjectValidator` - Linear object valdiator used
by class `LinearObject`

`LinearObjectError` - Error class used in linear object
class

`LinearObject` - Linear object class; core object

LOG

Updated on 30 September 2021 | Created on 22 April 2021
"""
from .errors import LinearObjectError
from .validators import LinearObjectValidator

__MODULE_LOCATION__ = 'linear_space.linear_object.linear_object'


class LinearObject:
    """ Linear object

    NOTE Linear object class is not intended for direct
    instantiation.

    Linear object is a generic 2D matrix defined in linear
    algebra.

    Linear object is constructed as a container object that
    stores a 2D numpy array, ofeen referred to as internal
    array. The first dimension of the internal array contains
    subarrays. Each subarray is interpreted as row, and within
    each subarray the position of number is interpreted as column.

    For example, a matrix
        [[1, 2, 3, 4, 5]
         [9, 10, 11, 12, 13]]
    is a linear object that stores a two-dimensional array of
    2 rows and 5 columns.

    Vector is a specialised linear object that has one dimension
    with size restricted to 1. From this perspective, a vector is
    a container that stores a 2D array, too. There are two types
    of vectors, column vector and row vector.

    Matrix is a specialised linear object that has both dimensions
    with size higher than 1 (at least 2).

    Here, linear object defines the most common features and
    properties to all linear object derivatives.

    ATTRIBUTES

    [Dimension]

    `self.as_array()` : returns internal numpy array

    `self.get_dimension()` : returns the dimension of the
    internal array, which is 2

    `self.get_dim()` : identical to `self.dimension()`

    `self.get_number_of_rows()` : returns the number of rows
    of the internal array

    `self.get_nrows()` : identical to `self.get_number_of_rows`

    `self.get_number_of_columns()` : returns the number of
    columns of the internal array

    `self.get_ncols()` : identical to `self.number_of_columns`

    `self.get_size()` : returns a tuple (nrows, ncols)

    [Indexing]

    `self.is_valid_row_index(,index)` : returns `True`(`False`)
    if an index to reference a row is(not) valid

    `self.is_valid_column_index(,index)`: returns `True`(`False`)
    if an index to reference a column is(not) valid

    `self.get_subarray(,row_index)`: returns a row referenced by
    the `row_index`

    `self.get_element(,row_index,column_index)`: returns an element
    at given row and column indices
    """
    __ERROR_LOCATION__ = __MODULE_LOCATION__ + '.LinearObject'

    def __init__(self, array=None):
        """ Linear Object :: init """
        validator = LinearObjectValidator(array=array)
        if validator.is_valid:
            self._array = validator.validated_data()['array']
        else:
            validator.raise_last_error(self.__ERROR_LOCATION__+'.__init__')

    def as_array(self):
        """ Linear Object :: Returns internal array """
        return self._array

    def set_array(self, array):
        """ Linear Object :: Sets internal array """
        validator = LinearObjectValidator(array=array)
        if validator.is_valid:
            self._array = validator.validated_data()['array']
        else:
            validator.raise_last_error(self.__ERROR_LOCATION__+'.set_array')

    def get_dimension(self):
        """ Linear Object :: Dimension of a 2D matrix is 2 """
        return self._array.ndim

    def get_dim(self):
        """ Linear Object :: Alias to `dimension()` """
        return self._array.ndim

    def get_number_of_rows(self):
        """ Linear Object :: Number of rows in a matrix """
        return len(self._array)

    def get_nrows(self):
        """ Linear Object :: Alias to number_of_rows """
        return len(self._array)

    def get_number_of_columns(self):
        """ Linear Object :: Number of columns of a matrix """
        return len(self._array[0])

    def get_ncols(self):
        """ Linear Object :: Alias to number_of_columns """
        return len(self._array[0])

    def get_size(self):
        """ Linear Object :: Size of a matrix is a tuple

        First element in tuple is the number of rows, the second
        is the number of columns.
        """
        return (self.get_number_of_rows(), self.get_number_of_columns())

    def is_valid_row_index(self, index):
        """ Linear Object :: Verifies if an index is a valid row index """
        ret = False
        if index in range(0, self.get_nrows(), 1):
            ret = True
        return ret

    def is_valid_column_index(self, index):
        """ Linear Object :: Verifies if an index is a valid column index """
        ret = False
        if index in range(0, self.get_ncols(), 1):
            ret = True
        return ret

    def get_subarray(self, row_index):
        """ Linear Object :: Retrieve a row or subarray

        The subarray can be further indexed.
        """
        ret = None
        if self.is_valid_row_index(row_index):
            ret = self._array[row_index]
        else:
            raise LinearObjectError('Index used to reference ' +\
                    'a row of linear object is out of range.',
                    location=self.__ERROR_LOCATION__+'.get_subarray')
        return ret

    def get_element(self, row_index, col_index):
        """ Linear Object :: Retrieve an element """
        ret = None
        if self.is_valid_row_index(row_index) \
                and self.is_valid_column_index(col_index):
            ret = self._array[row_index][col_index]
        else:
            raise LinearObjectError('Indices used to retrieve ' +\
                    'element of linear object is out of range ' +\
                    'or invalid.',
                    location=self.__ERROR_LOCATION__+'.get_element')
        return ret
