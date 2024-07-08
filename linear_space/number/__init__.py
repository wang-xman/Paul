#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
SUBPACK

Number subpack

PATH

[app_root]/linear_space/number/

INTRO

In linear space, number refers to c-number used in
quantum mechanics.

LOG

Updated on 29 September 2021 | Created on 14 April 2021
"""
from .types import VALID_INTEGER_TYPES, VALID_FLOAT_TYPES, VALID_REAL_TYPES, \
    VALID_COMPLEX_TYPES, VALID_NUMERIC_TYPES
from .types import Integer, Float, Real, Complex, Imaginary, Number
from .utils import is_integer, is_float, is_real, is_complex, is_number, \
    is_one, is_zero, is_power_of_two, exponent_of_two, power_of_two
