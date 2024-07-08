#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

bit.bitlist.py

PATH

[app_root]/bit/bitlist.py

INTRO

Bitlist is a list of tuples where each tuple has
two elements, first one being a number, and the
second is a bitstring.

Bitlist is used extensively to represent the bare
bone of quantum superposition. In this case,
relationship between two tuples is interpreted as
addition; relationship between items within a tuple
is interpreted as multiply.

LOG

Updated on 24 September 2021 | Created on 24 September 2021
"""
from .validators import BitlistValidator
from .utils import bitlist_to_vector

_MODULE_LOCATION_ = 'bit.bitlist'


class Bitlist:
    """ Bitlist object

    Bitlist object is a wrapper class that stores a valid
    bitlist and implements methods.

    TODO Not tested.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.Bitlist'

    def __init__(self, bitlist=None):
        """ Bitlist :: init """
        validator = BitlistValidator(bitlist=bitlist)
        if validator.is_valid:
            self._internal_list = bitlist
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    def as_list(self):
        """ Bitlist :: Return bitlist """
        return self._internal_list

    def as_vector(self):
        """ Bitlist :: Convert to vector """
        return bitlist_to_vector(self._internal_list)
