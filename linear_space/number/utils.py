#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.number.utils.py

PATH

[app_root]/linear_space/number/utils.py

INTRO

Utility functions for numbers.

CONTENT

`is_number(value)` - Verifies if a given value is a number;
returns `True` or `False`

`is_integer(value)` - Verifies if a given value is an integer,
returns `True` or `False`

`is_float(value)` - Verifies if a given value is a float,
returns `True` or `False`

`is_real(value)` - Verifies if a given value is real,
returns `True` or `False`

`is_complex(value)` - Verifies if a given value is complex,
returns `True` or `False`

`is_zero(value)` - Verifies if a given number is in the
neighbourhood of zero by an error tolerance; returns
`True` or `False`

`is_not_zero(value)` - Returns `True`(`False`) if is_zero
returns `False`(`True`)

`is_one(value)` - Verifies if a given number is in the
neighbourhood of 1 by an error tolerance; returns
`True` or `False`

`is_power_of_two(value)` - Verifies if a given integer is
power of 2

`exponent_of_two(value)` - Calculate the exponent n in
power 2^n; the given value must be a power of 2, otherwise
raises `NumberError` which is a subclass of `LinearAlgebraError`

`power_of_two(value)` - For a given value, returns 2^value;
the given value must be a number, otherwise raises `NumberError`

LOG

Updated on 30 September 2021 | Created on 14 April 2021
"""
from math import log as math_log
from linear_space.numpy_lib import np_abs, np_power

from .types import Integer, Float, Real, Complex, Number
from .errors import NumberError

_MODULE_LOCATION_ = 'linear_space.number.utils'

NUMERIC_ERROR_TOLERANCE = 1e-16


# Verifiers
def is_number(value):
    """ Verify if a value is a valid number """
    ret = False
    if isinstance(value, Number):
        ret = True
    return ret

def is_integer(value):
    """ Verify if a value is an integer """
    ret = False
    if isinstance(value, Integer):
        ret = True
    return ret

def is_float(value):
    """ Verify if a value is a float """
    ret = False
    if isinstance(value, Float):
        ret = True
    return ret

def is_real(value):
    """ Verify if a value is a real number """
    ret = False
    if isinstance(value, Real):
        ret = True
    return ret

def is_complex(value):
    """ Verify if a value is a real number """
    ret = False
    if isinstance(value, Complex):
        ret = True
    return ret

def is_zero(value):
    """ Verify if a number is close to zero

    Returns `True` if the given value is close to zero in the error
    tolerance; otherwise `False`.
    """
    ret = False
    if np_abs(value - 0.0) < NUMERIC_ERROR_TOLERANCE:
        ret = True
    return ret

def is_not_zero(value):
    """ A value is NOT zero """
    ret = True
    if is_zero(value):
        ret = False
    return ret

def is_one(value):
    """ Verify if a number is close to one

    NOTE The error tolerance cannot be stricter than 1e-15.
    Most likely due to the precision of numpy.abs function.
    """
    ret = False
    #error_tolerance = 1e-15
    if np_abs(value - 1.0) < 5 * NUMERIC_ERROR_TOLERANCE:
        ret = True
    return ret

def is_power_of_two(value):
    """ Verify is a number is power of 2

    Only when `value` is an integer and an integer power of 2,
    returns `True`; otherwise returns `False`.

    NOTE 1 is a power of two and the power is 0.
    """
    ret = False
    if is_integer(value):
        ret = (value & (value-1) == 0) and value != 0
    return ret


# Builders
def exponent_of_two(value):
    """ Get the exponent n in the power 2^n

    The given `value` must be a power of two.
    """
    ret = 0
    if is_power_of_two(value):
        ret = int(math_log(value, 2))
    else:
        raise NumberError('To acquire the exponent in a ' +\
                'power of 2, the integer must be a power of 2.',
                location=_MODULE_LOCATION_+'.exponent_of_two')
    return ret

def power_of_two(value):
    """ For a given value, returns the power 2^value """
    if is_number(value):
        ret = np_power(2, value)
    else:
        raise NumberError('To calculate the power of 2, ' +\
                'the exponent must be number.',
                location=_MODULE_LOCATION_+'.power_of_two')
    return ret
