#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operator.base.py

PATH

[app_root]/quantum_operator/base.py

NOTE

[IMPORTANT] Don't name any file as 'operator.py' due to
clash with Python's internal module of the same name.
To avoid such clashes and ambiguity, quantum operator
is used.

INTRO

Base error and validator.

CONTENT


LOG

Updated on 30 July 2021 | Created on 08 March 2021
"""
from common.exception import Validation_Error, Generic_Error


class QuantumOperatorBaseValidationError(Validation_Error):
    header = 'Quantum_Operator_Base_Validation_Error'


class QuantumOperatorBaseError(Generic_Error):
    header = 'Quantum_Operator_Base_Error'
