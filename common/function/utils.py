#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.function.utils.py

PATH

[app_root]/common/function/utils.py

INTRO

Function inspection utility functions

CONTENT

`is_method(obj)` - verifies if an object is a method;
BUT it only works on a method called on an instance

`is_function(obj)` - verifies if an object is a function

LOG

Updated on 30 September 2021 | Created on 19 December 2020
"""
import inspect


def is_method(obj):
    """ Returns true if an object is a method

    NOTE Warning! This doesn't always work. Only for a method
    called on an instance.
    """
    ret = False
    if inspect.ismethod(obj):
        ret = True
    return ret


def is_function(obj):
    """ Returns true if obj is a function """
    ret = False
    if callable(obj) and hasattr(obj, '__call__'):
        ret = True
    return ret
