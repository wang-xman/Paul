#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.prototype.errors.py

PATH

[app_root]/gate/prototype/errors.py

INTRO

LOG

Updated on 30 September 2021 | Created on 12 March 2021
"""
from gate.base import GateBaseValidationError, GateBaseError


class GatePrototypeValidationError(GateBaseValidationError):
    """ Prototype class validation error

    ENTRY

    `base.GatePrototypeValidator`
    """
    header = 'Gate_Prototype_Validation_Error'


class GateError(GateBaseError):
    """ FIXME Not in use """
    header = 'Gate_Error'
