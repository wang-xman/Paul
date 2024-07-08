#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_memory.base.py

PATH

[app_root]/quantum_memory/base.py

INTRO

Base validator and error classes for the app.

CONTENT

class `QuantumMemoryValidationError` - Memory validation
error raised by validator or validation

class `QuantumMemoryError` - Primary error class raised
by memory instance or its method

class `QuantumMemoryValidator` - Base validator to all
validators in quantum memory application

LOG

Updated on 30 September 2021 | Created on 18 July 2021
"""
from common.validator import Base_Validator
from common.exception import Generic_Error, Validation_Error

__MODULE_LOCATION__ = 'quantum_memory.base'


class QuantumMemoryBaseValidationError(Validation_Error):
    header = "Quantum_Memory_Validation_Error"


class QuantumMemoryBaseError(Generic_Error):
    header = "Quantum_Memory_Error"


class QuantumMemoryBaseValidator(Base_Validator):
    """ Base validator to all validators """
    error_class = QuantumMemoryBaseValidationError
