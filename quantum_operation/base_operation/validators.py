#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.base_operation.validators.py

PATH

[app_root]/quantum_operation/base_operation/validators.py

INTRO

Dedicated validators for base operation

LOG

Updated on 02 October 2021 | Created on 18 July 2021
"""
from quantum_operation.base import OperationBaseValidator

from .errors import BaseOperationSubclassValidationError

_MODULE_LOCATION_ = 'quantum_operation.base_operation.validators'


class BaseOperationSubclassValidator(OperationBaseValidator):
    """ Operation subclass validator

    Validate operation subclasses.

    Checks the subclass for two class attributes,
    `instruction_class` and `memory_validator_class`.
    The former is used to clarify the type of operation.
    The later is needed to validate operation against
    the target active quantum memory.

    Further check if subclass has method `launch_in_socket`
    to be invoked inside memory's operation socket.
    """
    error_class = BaseOperationSubclassValidationError
    error_location = _MODULE_LOCATION_ + '.OperationSubclassValdiator'

    def __init__(self, opclass):
        super().__init__()
        self.validate(opclass)

    def validate(self, opclass):
        if opclass.__name__ != 'BaseOperation':
            if not getattr(opclass, 'instruction_class', None):
                self.report_errors("Operation class must " +\
                        "implement a class attribute "+\
                        "'instruction_class' intended for " +\
                        "validation of quantum instruction.")
            elif not getattr(opclass, 'memory_validator_class', None):
                self.report_errors("Operation class must " +\
                        "implement a class attribute "+\
                        "'memory_validator_class' " +\
                        "intended for validation of operation against the "+\
                        "quantum memory it is applied to.")
            # TODO Should this be getattr?
            elif not 'launch_in_socket' in dir(opclass):
                self.report_errors(message="Operation class must " +\
                        "implement an instance method "+\
                        "'launch_in_socket' intended for " +\
                        "invocation in memory operation socket.")
            else:
                pass
