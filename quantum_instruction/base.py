#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_instruction.base.py

PATH

[app_root]/quantum_instruction/base.py

INTRO

Subpack-level base error and validators.

Quantum instruction converts a JSON-like user input, i.e.
instruction dictionary, into an instruction object that is
embedded into an operation object. (An operation object
interprets instruction and creates an operator.)

Quantum instruction functions as an interface between user
and operation.

CONTENT

LOG

Updated on 01 October 2021 | Created on 12 August 2021
"""
from common.validator import Base_Validator
from common.exception import Generic_Error, Validation_Error


class InstructionBaseError(Generic_Error):
    header = "Instruction_Base_Error"


class InstructionBaseValidationError(Validation_Error):
    header = "Instruction_Base_Validation_Error"


class InstructionBaseValidator(Base_Validator):
    """ Base class to all validators """
    error_class = InstructionBaseValidationError
