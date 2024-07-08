#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
SUBPACK

Function utility and analysis tools

PATH

[app_root]/common/function/

INTRO

Function signature analyzer and helper functions

CONTENT

`is_method(obj)` - verifies if an object is a method;
BUT it only works on a method called on an instance

`is_function(obj)` - verifies if an object is a function

`function_signature(func, skip_list=)` - a function
signature analyzer

`method_signature(func)` - method signature to skip
`self` argument

LOG

Updated on 30 September 2021 | Created on 19 December 2020
"""
from .utils import is_function, is_method
from .signature import function_signature, method_signature
