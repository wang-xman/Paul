#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.function.signature.py

PATH

[app_root]/common/function/signature.py

INTRO

Function signature analyzers

CONTENT

`function_signature(func, skip_list=)` - a function
signature analyzer

`method_signature(func)` - method signature to skip `self`
argument

LOG

Updated on 30 September 2021 | Created on 19 December 2020
"""
import inspect
from .errors import FunctionSignatureError
from .validators import SkipListValidator

_MODULE_LOCATION_ = 'common.function.signature'


def function_signature(func, skip_list=None):
    """ Function signature analyzer

    Analyse and parse function invocation signature.

    Positional arguments are stored in a tuple following the
    order of the original signature. Keyword arguments are
    stored in a dictionary with default values as values.

    Returns a dictionary that contains two keys
    {
        'args': a tuple of names positional arguments;
                orders are observed
        'kwargs: a dictionary of keyword arguments and
                 corresponding default values
    }
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.function_signature'
    valid_skip_list = []
    if not skip_list is None:
        validator = SkipListValidator(skip_list=skip_list)
        if validator.is_valid:
            valid_skip_list = skip_list
        else:
            validator.raise_last_error()

    if hasattr(func, '__call__'):
        # this is an OrderedDict
        parameters = inspect.signature(func).parameters
        # sort out positional arguments into a tuple
        argstuple = tuple()
        kwargsdict = {}
        for arg, v in parameters.items():
            # positional argument has empty default
            if v.default is inspect.Parameter.empty:
                # skip the argument in skiplist
                if len(valid_skip_list) != 0:
                    if not arg in valid_skip_list:
                        argstuple += (arg,)
                # skiplist is empty -> nothing to skip
                else:
                    argstuple += (arg,)
            # keyword arguments
            else:
                # skip the argument in skiplist
                if len(valid_skip_list) != 0:
                    if not arg in valid_skip_list:
                        kwargsdict[arg] = v.default
                # skiplist is empty -> nothing to skip
                else:
                    kwargsdict[arg] = v.default
        return {
            'args': argstuple,
            'kwargs': kwargsdict
        }
    else:
        raise FunctionSignatureError('To analyze function call '+\
                'signature, a function must be provided.',
                location=_ERROR_LOCATION_)


def method_signature(func):
    """ Method signature analyzer

    Method signature analyzer contains a skiplist that has `self`.

    For function that is an instance method, apply this function
    to skip the first positional argument `self`.

    WARNING If the first positional argument of a method is not
    `self`, it won't be skipped.
    """
    skiplist = ['self']
    return function_signature(func, skip_list=skiplist)
