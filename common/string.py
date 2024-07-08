#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.string.py

PATH

[app_root]/common/string.py

INTRO

Package-wide string verification and helper functions.

CONTENT

LOG

Updated on 27 July 2021 | Created on 15 April 2021
"""
from .exception import Generic_Error

_MODULE_LOCATION_ = "common.string"


class StringError(Generic_Error):
    header = "String_Error"


def is_string(value):
    """ Verify if a given value is a string """
    ret = False
    if isinstance(value, str):
        ret = True
    return ret


def is_empty_string(value):
    """ Verify if a string is empty """
    ret = False
    if not is_string(value):
        raise StringError("Function is_empty_string " +\
                "is only applicable to a string.")
    else:
        if len(value) == 0:
            ret = True
    return ret


def has_space(value):
    """ Verify if a string has a space in it """
    ret = False
    space_counter = 0
    if not is_string(value):
        raise StringError("Function has_space is " +\
                "only applicable to a string.")
    else:
        for char in value:
            if char.isspace():
                space_counter += 1
        if space_counter != 0:
            ret = True
    return ret


def has_bitchars_only(value):
    """ Verify if a string contains only bit character

    Bit character refers to '0' and '1'.

    Returns `True` if the string contains only bit characters;
    otherwise `False`.
    """
    ret = False
    if is_string(value) and not is_empty_string(value) and not has_space(value):
        counter = 0
        for char in list(value):
            if not char in set(['0','1']):
                counter += 1
        if counter == 0:
            ret = True
    return ret


def is_bitstring(value):
    """ Verify if a string is a bit string

    Bit string contains only 0 or 1 or both, it cannot be empty,
    and it can't contain space.
    """
    return has_bitchars_only(value)
