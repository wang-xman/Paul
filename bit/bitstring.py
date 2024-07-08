#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

bit.bitstring.py

PATH

[app_root]/bit/bitstring.py

INTRO

Tow main concepts, bitstring literal and bitstring.

Bitstring literal is a string or char that consists of
only '1' and (or) '0'. For example '10001' is a valid
bitstring literal. Single bit such as '1' and '0' are
the shortest valid bitstring literal.

Bitstring object is a wrapping class that stores an
internal bitstring literal and implements conversion
methods.

LOG

Updated on 08 October 2021 | Created on 06 November 2020
"""
from common.mixins import Non_Subclassable_Mixin, Non_Instantiable_Mixin
from linear_space.numpy_lib import np_array, np_intc

from .errors import BitstringError
from .validators import BitstringValidator
from .utils import is_index_valid_on_bitstring, bitstring_to_integer, \
    bitstring_to_fraction, bitstring_to_standard_basis

_MODULE_LOCATION_ = 'bit.bitstring'


class _BitstringLiteralMeta_(Non_Subclassable_Mixin, type):
    """ Bitstring literal meta """
    def __instancecheck__(cls, _bitstring):
        """ Manual instance check """
        ret = False
        validator = BitstringValidator(bitstring=_bitstring)
        if validator.is_valid:
            ret = True
        return ret


class Bitstring_Literal_Type(Non_Instantiable_Mixin,
                             metaclass=_BitstringLiteralMeta_):
    """ Bitstring literal type

    This type is used to verify is a bitstring literal
    such as '10010' is valid bitstring. Composite types
    like this helps unify the function call interface.
    """


class Bitstring:
    """ Bitstring object

    Bistring object is simply a wrapper class for a bitstring.

    CONSTRUCTOR

    `bitstring` (`str`): a bitstring

    ATTRIBUTES

    `self._internal_string` (`str`) : internal bitstring

    `self.as_string()` : returns internal bitstring

    `self.__str__()` : returns internal bitstring while
    object called by `str`

    `self.number_of_digits`: property that returns the length of
    the bitstring

    `self.as_integer()`: returns an integer that is converted to
    using the bitstring as a binary number; invokes static method
    `bitstring_to_integer()`

    `self.as_fraction()`: returns a factional number that is
    converted to using the bitstring as a binary number

    `self.as_array()`: converts the bitstring into an array of
    integer 1 and/or 0; for example array([0,1,0,1]), the content
    is number, not char or string

    `self.as_list()`: converts the bitstring into a list of
    integers 1 and/or 0; for example, [1,0,0,1,0]; content is number,
    not char or string

    `self.as_tuple()`: converts the bitstring into a tuple of
    integers 1 and/or 0

    `self.as_standard_basis()`: converts the bitstring into a
    standard basis vector

    `self.is_valid_index(, index)`: returns `True`/`False` if the
    index to label a bit in the bitstring is valid/invalid; index
    must be scientific index starting from 0

    `self.__getitem__(,index)`: returns a bit in the bitstring;
    in string type

    `self.get_bit_at(, index)`: same as `self.__getitem__()` method
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.Bitstring'

    def __init__(self, bitstring=None):
        """ Bitstring :: init """
        validator = BitstringValidator(bitstring=bitstring)
        if validator.is_valid:
            self._internal_string = bitstring
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    def as_string(self):
        """ Bitstring :: As a string """
        return self._internal_string

    def __str__(self):
        """ Bitstring :: As a string

        Apply `str` method on this object triggers this method.
        """
        return self._internal_string

    @property
    def number_of_digits(self):
        return len(self._internal_string)

    def as_integer(self):
        """ Bitstring :: Convert to a decimal integer """
        return bitstring_to_integer(self._internal_string)

    def as_fraction(self):
        """ Bitstring :: Convert to a decimal fraction """
        return bitstring_to_fraction(self._internal_string)

    def as_list(self):
        """ Bitstring :: Return a list of 0s and 1s

        All elements are integers, not chars.
        """
        integer_list = []
        for item in self._internal_string:
            integer_list.append(np_intc(item))
        return integer_list

    def as_integer_list(self):
        return self.as_list()

    def as_array(self):
        """ Bitstring :: As an array of integers """
        return np_array(self.as_list(), dtype=np_intc)

    def as_integer_array(self):
        """ Bitstring :: As an array of integers """
        return np_array(self.as_list(), dtype=np_intc)

    def as_tuple(self):
        """ Bitstring :: As a tuple of integers """
        return tuple(self.as_list())

    def as_integer_tuple(self):
        """ Bitstring :: As a tuple of integers """
        return tuple(self.as_list())

    def as_standard_basis(self):
        """ Bitstring :: Convert to a standard basis vector """
        uv = bitstring_to_standard_basis(self.as_string())
        return uv

    def is_valid_index(self, index):
        """ Bitstring :: Verify an index

        Index is in scientific index starting from 0.
        """
        return is_index_valid_on_bitstring(self._internal_string, index)

    def __getitem__(self, index):
        """ Bitstring :: Returns a selected bit in string

        Return either '0' or '1'
        """
        ret = None
        if self.is_valid_index(index):
            ret = self._bitstring[index]
        else:
            raise BitstringError("Index is out of range.",
                    location=self._ERROR_LOCATION_+'.__getitem__')
        return ret

    def get_bit_at(self, index):
        """ Bitstring :: Same as above """
        return self.__getitem__(index)
