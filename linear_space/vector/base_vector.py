#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.vector.base_vector.py

PATH

[app_root]/linear_space/vector/base_vector.py

INTRO

Base vector class implements common properties to
all vector objects. Most importantly, base vector
class defines the shape of vector, i.e. either
one column or one row.

CONTENT

`BaseVector` - Generic base class for vector-like,
both column- and row-like objects; Column and row vector
classes are subclass of `BaseVector`; `BaseVector` itself
is subclass of `LinearObject`.

LOG

Updated on 30 September 2021 | Created on 07 November 2020
"""
from linear_space.numpy_lib import np_norm
from linear_space.number import is_zero, is_one
from linear_space.linear_object.linear_object import LinearObject

from .errors import VectorError
from .validators import BaseVectorInitValidator

_MODULE_LOCATION_ = 'linear_space.vector.base_vector'


class BaseVector(LinearObject):
    """ Base vector class

    Base class to column and row vectors. Base vector stores a
    2D numpy array that has along one dimension length 1,
    a column vector has exactly 1 column, a row has exactly 1 row.

    Size of a vector refers to the total number of elements in
    the internal array and is strictly distinguished from the
    mathematical definition of 'length' which is the norm of
    a vector.

    Base vector class implements features and methods that are
    common to both column and row vectors.

    NOTE Subclass must implement `self.size`, `self.element`, and
    `self.string_representation` methods.

    Indices are all in scientific index.

    CONSTRUCTOR

    `array` (`numpy.ndarray`): after validation it becomes the
    internal array of the vector instance.

    ATTRIBUTES

    `self.is_valid_index(,index)`: verifies if a given index to
    retrieve a vector component is valid

    `self.el(,index)`: retrieve the vector component at given index;
    subclass must implement a `self.element(,index)` method

    `self.first`: property; returns the first element of the vector

    `self.last`: property; returns the last element of the vector

    `self.norm`: property; returns the two-norm of the vector

    `self.is_normalised`: property; returns `True`(`False`) if norm
    is(not) one

    `self.is_normalized`: identical to `self.normalised`

    `self.normalise()`: normalise internal array and returns the
    normalised vector; raises error is the norm of a vector is too
    close to zero

    `self.normalize()`: identical to `self.normalise()`

    `self.__str__()`: returns `self.string_representation()`; subclass must
    implement `self.string_representation()`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.BaseVector'

    def __new__(cls, *args, **kwargs):
        """ Base Vector :: Regulate subclass

        Subclass must implement `self.size` and `self.element`
        methods. This class is excluded.
        """
        if cls != BaseVector:
            error_message = None
            if not getattr(cls, 'size', None):
                error_message ='Immediate subclass of '   +\
                        'BaseVector must implement size ' +\
                        'method to determine and return ' +\
                        'the number of elements in the vector.'
            elif not getattr(cls, 'element', None):
                error_message= 'Immediate subclass of ' +\
                        'BaseVector must implement an ' +\
                        'element method to return a '   +\
                        'component of the vector requested using an index.'
            else:
                pass
            if error_message is not None:
                raise VectorError(error_message,
                        location=cls._ERROR_LOCATION_+'.__new__')
        return super().__new__(cls)

    def __init__(self, array=None):
        """ Base Vector :: Initialiser """
        validator = BaseVectorInitValidator(array=array)
        if validator.is_valid:
            super().__init__(array=array)
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    @property
    def nrows(self):
        """ Base Vector :: Number of rows """
        return self.get_nrows()

    @property
    def ncols(self):
        """ Base Vector :: Number of columns """
        return self.get_ncols()

    def is_valid_index(self, index):
        """ Base Vector :: Validate index

        Subclass must implment and override `LinearObject.size`
        property.
        """
        ret = False
        if index in range(0, self.size, 1):
            ret = True
        return ret

    def el(self, index):
        """ Base Vector :: Alias to element

        Subclass must implement a method `self.element()` to get
        an item at the given index.
        """
        return self.element(index=index)

    @property
    def first(self):
        """ Base Vector :: Return first element """
        return self.element(index=0)

    @property
    def last(self):
        """ Base Vector :: Return last element """
        return self.element(index=self.size - 1)

    @property
    def norm(self):
        """ Base Vector :: Return two-norm of vector """
        norm = np_norm(self.as_array())
        return norm

    @property
    def is_normalized(self):
        """ Base Vector :: Returns `True`/`False` if is/not normalized

        It is a bad taste to compare norm - 1.0 with zero.
        In numerical analysis, zero must be replaced by a very
        small number.
        """
        ret = False
        if is_one(self.norm):
            ret = True
        return ret

    def normalize(self):
        """ Base Vector :: Normalise internal array """
        norm = self.norm
        if not is_zero(norm):
            if not self.is_normalized:
                self.set_array(self.as_array() / self.norm)
        else:
            raise VectorError('Norm of the vector is very ' +\
                    'close to zero. Normalisation aborted.',
                    location=self._ERROR_LOCATION_+'.normalize')
        return self

    def __str__(self):
        """ Base Vector :: __str__ method

        Subclass must implement `self.string_representation()`
        """
        return self.string_representation()
