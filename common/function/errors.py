#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.function.errors.py

PATH

[app_root]/common/function/errors.py

INTRO

Error class for function tool and analyser subpack.

CONTENT

LOG

Updated on 06 September 2021 | Created on 19 December 2020
"""
from common.exception import Generic_Error, Validation_Error


class FunctionSignatureError(Generic_Error):
    """ Used in function signature analyzer

    ENTRY

    `signature.function_signature`
    """
    header = 'Function_Signature_Error'


class SkipListValidationError(Validation_Error):
    """ Used in SkipListValidatior

    ENTRY

    `validators.SkipListValidator`
    """
    header = 'Skip_List_Validation_Error'


class VerifierFunctionDecoratorError(Validation_Error):
    """ Used in verifier function decorator

    ENTRY

    `decorators.FunctionInvocationDecorator`
    """
    header = 'Verifier_Function_Decorator_Error'


class FunctionInvocationDecoratorError(Validation_Error):
    """ Used in base function invocation decorator class

    ENTRY

    `decorators.FunctionInvocationDecorator`
    """
    header = 'Function_Invocation_Decorator_Error'
