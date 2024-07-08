#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.utils.errors.py

PATH

[app_root]/linear_space/utils/errors.py

INTRO

Common objects used in subpack.

CONTENT

LOG

Updated on 23 September 2021 | Created on 23 September 2021
"""
from linear_space.base import LinearSpaceBaseError


class LinearSpaceUtilityFunctionError(LinearSpaceBaseError):
    header = "Linear_Space_Utility_Function_Error"
