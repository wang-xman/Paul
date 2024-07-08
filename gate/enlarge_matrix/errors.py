#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.enlarge_matrix.errors.py

PATH

[package_root]/gate/enlarge_matrix/errors.py

INTRO

Dedicated errors for matrix enlargement.

CONTENT

LOG

Updated on 30 September 2021 | Created on 10 September 2021
"""

from gate.base import GateBaseValidationError, GateBaseError


class GateMatrixEnlargeValidationError(GateBaseValidationError):
    """ Gate matrix enlargment validation error

    ENTRY

    `common.GenericGateMatrixEnlargeValidator`
    """
    header = "Gate_Matrix_Enlarge_Validation_Error"


class GateMatrixEnlargeError(GateBaseError):
    """ Gate matrix enlarge error

    Error class used in gate matrix enlarge functions.

    ENTRY

    Module `noncontrolled`
    """
    header = "Gate_Matrix_Enlarge_Error"
