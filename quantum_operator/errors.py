#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operator.errors.py

PATH

[app_root]/quantum_operator/errors.py

INTRO

Dedicated errors

CONTENT

LOG

Updated on 30 July 2021 | Created on 08 March 2021
"""
from .base import QuantumOperatorBaseError


class QuantumOperatorError(QuantumOperatorBaseError):
    header = 'Quantum_Operator_Error'
