#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.number.types.py

PATH

[app_root]/linear_space/number/types.py

INTRO

Artifically defined number classes used solely for
`isinstance` checking in algebra functions.

NOTE Numberic types introduced in this module are
NOT subclassable and NOT instantiable.

CONTENT

LOG

Updated on 30 September 2021 | Created on 14 April 2021
"""
from linear_space.numpy_lib import np_intc, np_int8, np_int16, \
    np_int32, np_int64
from linear_space.numpy_lib import np_float, np_float64, \
    np_complex, np_complex128
from common.mixins import Non_Instantiable_Mixin, Non_Subclassable_Mixin


VALID_INTEGER_TYPES = (int, np_intc, np_int8, np_int16, np_int32, np_int64,)
# integer is NOT float
VALID_FLOAT_TYPES = (float, np_float, np_float64,)
# real -> integer + float
VALID_REAL_TYPES = VALID_INTEGER_TYPES + VALID_FLOAT_TYPES
# real is NOT complex
VALID_COMPLEX_TYPES = (complex, np_complex, np_complex128,)
# all -> real + complex
VALID_NUMERIC_TYPES = VALID_REAL_TYPES + VALID_COMPLEX_TYPES


# integer
class _IntegerMeta_(Non_Subclassable_Mixin, type):
    """ Integer number meta """
    def __instancecheck__(cls, _number):
        """ Manual instance check """
        ret = False
        if isinstance(_number, VALID_INTEGER_TYPES):
            ret = True
        return ret

class Integer(Non_Instantiable_Mixin, metaclass=_IntegerMeta_):
    """ Integer number """


# float
class _FloatMeta_(Non_Subclassable_Mixin, type):
    """ Float meta class """
    def __instancecheck__(cls, _number):
        """ Manual instance check """
        ret = False
        if isinstance(_number, VALID_FLOAT_TYPES):
            ret = True
        return ret

class Float(Non_Instantiable_Mixin, metaclass=_FloatMeta_):
    """ Float number """


# real
class _RealMeta_(Non_Subclassable_Mixin, type):
    """ Real number meta """
    def __instancecheck__(cls, _number):
        """ Manual instance check """
        ret = False
        if isinstance(_number, VALID_REAL_TYPES):
            ret = True
        return ret

class Real(Non_Instantiable_Mixin, metaclass=_RealMeta_):
    """ Real number

    Real is NOT Complex.
    """


# complex
class _ComplexMeta_(Non_Subclassable_Mixin, type):
    """ Complex number meta """
    def __instancecheck__(cls, _number):
        """ Manual instance check """
        ret = False
        if isinstance(_number, VALID_COMPLEX_TYPES):
            ret = True
        return ret

class Complex(Non_Instantiable_Mixin, metaclass=_ComplexMeta_):
    """ Complex number """


# imaginary
class _ImaginaryMeta_(Non_Subclassable_Mixin, type):
    """ Imaginary number meta """
    def __instancecheck__(cls, _number):
        """ Manual instance check """
        ret = False
        if isinstance(_number, VALID_COMPLEX_TYPES) \
                and _number.real == 0.0:
            ret = True
        return ret

class Imaginary(Non_Instantiable_Mixin, metaclass=_ImaginaryMeta_):
    """ Imaginary number

    Imaginary IS also Complex. Imaginary number is
    validated by checking if real part is vanishing.
    """


# number
class _NumberMeta_(Non_Subclassable_Mixin, type):
    """ Number meta """
    def __instancecheck__(cls, _number):
        """ Used in isinstance check
        """
        ret = False
        if isinstance(_number, VALID_NUMERIC_TYPES) \
                or isinstance(_number, Imaginary):
            ret = True
        return ret

class Number(Non_Instantiable_Mixin, metaclass=_NumberMeta_):
    """ Number """
