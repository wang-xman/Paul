#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.numpy_lib.py

TODO Tidy up!!

PATH

[app_root]/linear_space/numpy_lib.py

INTRO

Functions imported from numpy.
Avoid importing the entire numpy module.

CONTENT

LOG

Updated on 02 October 2021 | Created on 07 November 2020
"""
# integer type
from numpy import intc as np_intc, \
    int8 as np_int8, \
    int16 as np_int16, \
    int32 as np_int32, \
    int64 as np_int64

# float
from numpy import float as np_float, \
    float64 as np_float64

# complex
from numpy import complex as np_complex, \
    complex128 as np_complex128

from numpy import power as np_power
from numpy import sqrt as np_sqrt

from numpy import ndarray as np_ndarray, \
    array as np_array
from numpy.linalg import norm as np_norm
from numpy import transpose as np_transpose
from numpy import conj as np_conj
from numpy import zeros as np_zeros, \
    ones as np_ones
from numpy import abs as np_abs
from numpy import dot as np_dot
from numpy import outer as np_outer
from numpy import kron as np_kron
from numpy import identity as np_identity

from numpy import amax as np_amax, \
    amin as np_amin