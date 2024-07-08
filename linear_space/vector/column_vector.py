#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.vector.column_vector.py

PATH

[app_root]/linear_space/vector/column_vector.py

INTRO

Column vector is one of the most foundamental object
in linear algebra and quantum mechanics.

Column vector here doesn't implement any linear algebra
operation.

CONTENT

`ColumnVector` - Column vector is modelled as a container
that has a 2D (N-by-1) numpy array as the internal array;
also serves as base class to other column vectors.

LOG

Updated on 30 September 2021 | Created on 07 November 2020
"""
from linear_space.numpy_lib import np_conj, np_transpose
from linear_space.number import is_zero
from linear_space.linear_object.algebra import subtract, norm

from .base_vector import BaseVector
from .errors import ColumnVectorError
from .validators import ColumnVectorInitValidator

_MODULE_LOCATION_ = 'linear_space.vector.column_vector'


class ColumnVector(BaseVector):
    """ Column vector

    A column vector is a linear object that packs a N-by-1
    numpy array, for example
        [[1]
         [2]
         [3]]
    where it is stored internally as a 2D numpy array.
    A column vector is naturally column-like. A column vector
    is a subclass of `BaseVector`.

    CONSTRUCTOR

    `array` (`np.ndarray`) : an N-by-1 column like numpy array

    ATTRIBUTES

    `self.size`: property; the number of rows of a column-like
    linear object

    `self.as_1d_list()`: returns numpy array as list of numbers

    `self.element(,index)`: returns the element reference by the
    index

    `self.__getitem__(,index)`: identical to `self.element`

    `self.is_equal_to(, other_vector)`: verifies if `other_vector`
    is identical to this vector

    `self.__eq__(, other_vector)`: identical to `is_equal_to`

    `self.string_representation()`: returns a string
    representation of vector
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.ColumnVector'

    def __init__(self, array=None, datatype=None):
        """ Column Vector :: init

        Should `datatype` be provided, the validated array is
        converted into that type. Otherwise, default datatype
        is `np.complex`. See validator.
        """
        validator = ColumnVectorInitValidator(array=array, datatype=datatype)
        if validator.is_valid:
            vdarray = validator.validated_data()['array']
            super().__init__(array=vdarray)
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    @property
    def size(self):
        """ Column Vector :: Number of elements in array

        Size of a vector is a different concept from
        the length of it.
        """
        return self.get_nrows()

    def as_1d_list(self):
        """ Column Vector :: Returns a 1D list of numbers """
        return list(np_transpose(self.as_array())[0])

    def element(self, index):
        """ Column Vector :: Returns element by index """
        ret = None
        if self.is_valid_index(index):
            ret = super().get_element(index, 0)
        else:
            raise ColumnVectorError('Vector index out of range.',
                    location=self._ERROR_LOCATION_+'.element')
        return ret

    def __getitem__(self, index):
        """ Column Vector :: Return vector component at given index """
        try:
            return self.element(index)
        except Exception as err:
            raise err.relocate(self._ERROR_LOCATION_+'.__getitem__')

    def is_equal_to(self, other_vector):
        """ Column Vector :: Verify if two vectors are identical

        Returns `True`, if two internal arrays are identical
        or within tolerance; otherwise `False`.

        If the difference between two vectors are with a tolerance,
        two vectors are considered equal. Avoid comparing difference
        directly to zero.
        """
        value = None
        if isinstance(other_vector, ColumnVector):
            difflinobj = subtract(self, other_vector)
            # if difference is close zero, consider them equal.
            value = is_zero(norm(difflinobj))
        else:
            raise ColumnVectorError("Column vector 'is_equal_to' " +\
                    "method compares only column vectors.",
                    location=self._ERROR_LOCATION_+'.is_equal_to')
        return value

    def __eq__(self, other_vector):
        """ Column Vector :: Operator == """
        return self.is_equal_to(other_vector)

    def string_representation(self):
        """ Column Vector :: String representation

        Returns the internal array as a column-like vector string,
        for example,
            [0.89 + 0.27j
             0.45 + 1.60j
             10.12 + 0.76j],
        with each amplitude formatted as a complex number that has
        two decimal points. Attention must go to the complex number
        with negative imaginary part, as the symbol connecting real
        and imaginary parts is minus (-).
        """
        vector_size = len(self.as_array())
        fullstring = "\n["
        for i, item in enumerate(self.as_array()):
            if i == 0:
                if item[0].imag >= 0:
                    fullstring += "{c.real:.2f} + {c.imag:.2f}j\n".format(
                            c=item[0])
                else:
                    fullstring += "{c.real:.2f} - {a.imag:.2f}j\n".format(
                            c=item[0], a=np_conj(item[0]))
            elif i != vector_size - 1:
                if item[0].imag >=0:
                    fullstring += " {c.real:.2f} + {c.imag:.2f}j\n".format(
                            c=item[0])
                else:
                    fullstring += " {c.real:.2f} - {a.imag:.2f}j\n".format(
                            c=item[0], a=np_conj(item[0]))
            else:
                if item[0].imag >= 0:
                    fullstring += " {c.real:.2f} + {c.imag:.2f}j".format(
                            c=item[0])
                else:
                    fullstring += " {c.real:.2f} - {a.imag:.2f}j".format(
                            c=item[0], a=np_conj(item[0]))
        fullstring += "]\n"
        return fullstring
