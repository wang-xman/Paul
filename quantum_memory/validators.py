#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_memory.validators.py

PATH

[app_root]/quantum_memory/validators.py

INTRO

Validators used in quantum memory package

CONTENT

`QubitMemoryRegisterValidator`

`OperationLauncherValidator`

LOG

Updated on 01 October 2021 | Created on 18 July 2021
"""
from common.function import method_signature
from quantum_register.base_register import BaseRegister

from .errors import QubitMemoryRegisterValidationError, \
    OperationLauncherValidationError

from .base import QuantumMemoryBaseValidator

__MODULE_LOCATION__ = 'quantum_memory.validators'


class QubitMemoryRegisterValidator(QuantumMemoryBaseValidator):
    """ Validate registers for qubit memory

    To initialise a qubit memory, a qubit register or a list
    of qubit registers must be provided. Following conditions
    must be satisfied:

    [1] Register(s) must be qubit register type `QubitRegister`.

    [2] Register(s) can not be empty.

    [3] In case of register list, each register in the list must
    have a unique label. Two registers with identical label are
    not allowed.
    """
    error_class = QubitMemoryRegisterValidationError
    error_location = __MODULE_LOCATION__ + '.QubitMemoryRegisterValidator'

    def __init__(self, register=None, register_class=None):
        """
        NOTE This register class check should be in a base class.
        """
        super().__init__()
        if issubclass(register_class, BaseRegister):
            self.register_class = register_class
            self.validate(register=register)
        else:
            self.report_errors("Register classes accepted " +\
                    "by a quantum memory are not valid register class.")

    def _is_empty_register(self, register):
        """ Verify if register is empty

        If one (or more) register is empty, returns `True`.
        Also returns `True` if the memory has no register at all.

        Containing non-empty registers is a necessary condition
        for a memory to be iterable.
        """
        ret = False
        if register.is_empty:
            ret = True
        return ret

    def _is_qubit_register(self, register):
        """ Verify if a register is a qubit register

        Containing only qubit registers is a necessary
        condition for a memory to be iterable.
        """
        ret = False
        if isinstance(register, self.register_class):
            ret = True
        return ret

    def validate_single_register(self, register):
        """ Validate a single register """
        if not self._is_qubit_register(register):
            self.report_errors("Register '{}'".format(register.label) +\
                    " provided to initialise qubit memory is " +\
                    "of an invalid register type. Qubit memory accepts " +\
                    "only QubitRegister or its subclasses. \n" +\
                    "Qubit memory register validation failed.")
        else:
            if self._is_empty_register(register):
                self.report_errors("Register with " +\
                    "label '{}' ".format(register.label) +\
                    "provided to initialise qubit memory is empty." +\
                    "Qubit memory initialisation requires "+\
                    "non-empty register(s). \n" +\
                    "Qubit memory register validation failed.")

    def validate_list(self, reglist):
        """ Validate a list of registers """
        existing_labels = []
        for reg in reglist:
            if not reg.label in existing_labels:
                existing_labels.append(reg.label)
                self.validate_single_register(reg)
            else:
                self.report_errors("Register with label " +\
                    "'{}' already exists in ".format(reg.label) +\
                    "the register list provided to initialise memory.\n" +\
                    "Qubit memory register validation failed.")

    def validate(self, register=None):
        """ Main validate method """
        if register is not None:
            # a list is provided
            if isinstance(register, list):
                self.validate_list(register)
            # not a list, but a register
            elif isinstance(register, BaseRegister):
                self.validate_single_register(register)
            else:
                self.report_errors("To initialise a qubit " +\
                        "memory, either a qubit register or a list of " +\
                        "qubit registers must be provided. \n" +\
                        "Qubit memory register validation failed.")


class OperationLauncherValidator(QuantumMemoryBaseValidator):
    """ On memory operation launcher validator

    Validate operation launcher function passed in to
    memory's operation socket.

    Operation launcher passed to operation socket must be
    a function. This function must have only one positional
    argument named `memory`.
    """
    error_class = OperationLauncherValidationError
    error_location = __MODULE_LOCATION__ + '.OperationLauncherValidator'

    def __init__(self, operation_launcher):
        super().__init__()
        self.validate(func=operation_launcher)

    def validate(self, func=None):
        """ Main validate method """
        sig = method_signature(func)
        if not 'memory' in sig['args']:
            self.report_errors("Operation launcher function " +\
                    "for memory socket is missing a required " +\
                    "positional argument 'memory'.")
    