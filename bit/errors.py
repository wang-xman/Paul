#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

bit.errors.py

PATH

[app_root]/bit/errors.py

INTRO

Error classes

LOG

Updated on 05 October 2021 | Created on 06 November 2020
"""
from .base import BitBaseError, BitBaseValidationError


class BitstringError(BitBaseError):
    header = 'Bitstring_Error'


class BitarrayValidationError(BitBaseValidationError):
    """ Bitarray validation error """
    header = "Bitarray_Validation_Error"


# Bitstring related
class BitstringValidationError(BitBaseValidationError):
    """ Bitstring validation error class """
    header = "Biistring_Validation_Error"


# Bitlist related
class BitlistValidationError(BitBaseValidationError):
    header = 'Bitlist_Validation_Error'


# Bitrange related
class BitrangeBoundValidationError(BitBaseValidationError):
    header = 'Bitrange_Bound_Validation_Error'


# Bitrange related
class BitrangeValidationError(BitrangeBoundValidationError):
    header = 'Bitrange_Validation_Error'


class BitUtilityFunctionError(BitBaseError):
    header = 'Bit_Utility_Function_Error'
