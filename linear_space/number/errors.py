#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.number.errors.py

TODO Errors need to be more specific.

PATH

[app_root]/linear_space/number/errors.py

INTRO

Errors use in subpack

LOG

Updated on 30 September 2021 | Created on 14 April 2021
"""
from linear_space.base import LinearSpaceBaseError


class NumberError(LinearSpaceBaseError):
    """ Number errors raise by utils """
    header = 'Number_Error'
