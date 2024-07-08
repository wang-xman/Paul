#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.vector.row_vector.py

PATH

[app_root]/linear_space/vector/row_vector.py

INTRO

Row vector is a essentially a matrix with just one
row. Linear algebra operations are not implemented
as method of row vector.

CONTENT

`RowVector` - Row vector is a container class that
as 1-by-N numpy array as the internal array.

LOG

Updated on 02 October 2021 | Created on 07 November 2020
"""
from linear_space.numpy_lib import np_conj
from linear_space.number import is_zero
from linear_space.linear_object.algebra import subtract, norm

from .base_vector import BaseVector
from .errors import RowVectorError
from .validators import RowVectorInitValidator

_MODULE_LOCATION_ = 'linear_space.vector.row_vector'


class RowVector(BaseVector):
    """ Row vector

    Row vector is stored as a 1-by-N row matrix.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.RowVector'

    def __init__(self, array=None, datatype=None):
        """ Row Vector :: Initialiser """
        validator = RowVectorInitValidator(array=array, datatype=datatype)
        if validator.is_valid:
            vdarray = validator.validated_data()['array']
            super().__init__(array=vdarray)
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    @property
    def size(self):
        """ Row Vector :: Number of elements in the array

        Size of a row vector is the number of columns.
        """
        return self.get_ncols()

    def as_1d_list(self):
        """ Row Vector :: Returns a 1D list of numbers """
        return list(self.as_array()[0])

    def element(self, index):
        """ Row Vector :: Returns the element by index """
        ret = None
        if self.is_valid_index(index):
            ret = super().get_element(0, index)
        else:
            raise RowVectorError('Vector index out of range.',
                    location=self._ERROR_LOCATION_+'.element')
        return ret

    def __getitem__(self, index):
        """ Row Vector :: Return component at given index """
        ret = None
        if self.is_valid_index(index):
            ret = self.as_array()[0][index]
        else:
            raise RowVectorError("Row vector index out of range.",
                    location=self._ERROR_LOCATION_+'.__getitem__')
        return ret

    def is_equal_to(self, other_vector):
        """ Row Vector :: Check if two vectors are identical

        Returns `True`, if two internal arrays are identical or
        within tolerance; otherwise `False`.

        If the difference between two vectors are with a tolerance,
        two vectors are considered equal. Avoid comparing difference
        directly to zero.
        """
        value = None
        if isinstance(other_vector, RowVector):
            difflinobj = subtract(self, other_vector)
            # if difference is close zero, consider them equal.
            value = is_zero(norm(difflinobj))
        else:
            raise RowVectorError("Row vector is_equal_to method " +\
                    "compares only row vectors.",
                    location=self._ERROR_LOCATION_+'.is_equal_to')
        return value

    def __eq__(self, other_vector):
        """ Row Vector :: Operator == """
        return self.is_equal_to(other_vector)

    def string_representation(self):
        """ Row Vector :: String representation of row vector """
        vector_size = len(self.as_array()[0])
        fullstring = "\n["
        for i, item in enumerate(self.as_array()[0]):
            if i != vector_size - 1:
                if item.imag >=0:
                    fullstring += "{c.real:.2f} + {c.imag:.2f}j, ".format(
                            c=item)
                else:
                    fullstring += "{c.real:.2f} - {a.imag:.2f}j, ".format(
                            c=item, a=np_conj(item))
            else:
                if item.imag >= 0:
                    fullstring += "{c.real:.2f} + {c.imag:.2f}j".format(
                            c=item)
                else:
                    fullstring += "{c.real:.2f} - {a.imag:.2f}j".format(
                            c=item, a=np_conj(item))
        fullstring += "]\n"
        return fullstring
