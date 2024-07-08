"""
MODULE

quantum_operation.base_operation.validators.py

PATH

[app_root]/quantum_operation/base_operation/validators.py

INTRO

Dedicated validators for base quantum operation

LOG

Updated on 02 October 2021 | Created on 18 July 2021
"""
from .errors import BaseOperationError
from .validators import BaseOperationSubclassValidator

_MODULE_LOCATION_ = 'quantum_operation.base_operation.operations'


class BaseOperation:
    """ Base class to all quantum operations

    Base operation class is the base class to all operation
    objects.
    """
    error_location = _MODULE_LOCATION_ + '.BaseOperation'

    def __new__(cls, *args, **kwargs):
        """ Base Operation : Contructor

        Any subclass must have two class attributes,
        `instruction_class` and `memory_validator_class`.
        """
        class_validator = BaseOperationSubclassValidator(cls)
        if not class_validator.is_valid:
            class_validator.raise_last_error(cls.error_location+'.__new__')
        return super().__new__(cls)

    def __init__(self, instruction, oplabel=None):
        """ Base Operation : Initialiser

        Arguments

        `instruction` (quantum instruction instance) : instruction
        object converted from the corresponding instruction dictionary

        `oplabel` (`str`): an string to label operation object
        """
        self.label = oplabel
        if isinstance(instruction, self.instruction_class):
            self._instruction = instruction
        else:
            raise BaseOperationError("Quantum operation requires " +\
                    "a corresponding quantum instruction instance " +\
                    "for initialisation.",
                    location=self.error_location+'__init__')
