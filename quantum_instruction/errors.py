#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_instruction.errors.py

TODO Is this needed?

PATH

[app_root]/quantum_instruction/errors.py

INTRO

Dedicated errors

CONTENT

LOG

Updated on 01 October 2021 | Created on 12 August 2021
"""
from .base import InstructionBaseError

class IndexRangeError(InstructionBaseError):
    """ Index range error """
    header = "Index_Range_Error"
