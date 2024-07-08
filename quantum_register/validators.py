
#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_register.validators.py

PATH

[app_root]/quantum_register/validators.py

INTRO

LOG

Updated on 30 September 2021 | Created on 09 May 2021
"""
from common.string import is_string, is_empty_string, has_space
from quantum_state.quantum_state import QuantumState

from .errors import RegisterClassValidationError, BaseRegisterInitValidationError
from .base import RegisterBaseValidator, AbstractQuantumRegister

_MODULE_LOCATION_ = 'quantum_register.validators'


class RegisterClassValidator(RegisterBaseValidator):
    """ Validator for register class

    Register class must implement `state_class` as a
    class attribute
    """
    error_class = RegisterClassValidationError
    error_location = _MODULE_LOCATION_ + '.RegisterClassValidator'

    def __init__(self, register_class=None):
        super().__init__()
        self.validate(register_class)

    def validate(self, register_class):
        """ Main validate method """
        base_classes = register_class.__bases__
        if not getattr(register_class, 'state_class', None):
            # search in base class
            for base in base_classes:
                if issubclass(base, AbstractQuantumRegister):
                    if not 'state_class' in base.__dict__:
                        self.report_errors("Register class " +\
                                "{} ".format(register_class.__name__) +\
                                "is missing a class attribute named " +\
                                "'state_class' to declare the type " +\
                                "of state it stores.")
        else:
            if not register_class.state_class == QuantumState:
                if not issubclass(register_class.state_class, QuantumState):
                    self.report_errors("State class declared " +\
                            "in register "+\
                            "class {} ".format(register_class.__name__) +\
                            "is not quantum state or subclass of it.")


class BaseRegisterInitValidator(RegisterBaseValidator):
    """ Validator for register initialisation

    A label for the register is required, and the
    initial state can be empty and updated later.
    """
    error_class = BaseRegisterInitValidationError
    error_location = _MODULE_LOCATION_ + '.BaseRegisterInitValidator'

    def __init__(self, state=None, label=None, state_class=None):
        super().__init__()
        self.__state_class = state_class
        self.__validated_state = None
        self.__validated_label = None
        self.validate(state=state, label=label)

    def validate(self, state=None, label=None):
        if label is None:
            self.report_errors("To create a register, " +\
                    "a label must be provided as a unique identifier.")
        elif not is_string(label):
            self.report_errors("Label provided to identify a " +\
                    "register is not a string.")
        elif is_empty_string(label) or has_space(label):
            self.report_errors("Label provided to identify a " +\
                    "register is either empty or contains space.")
        else:
            self.__validated_label = label

        if state is None:
            self.__validated_state = None
        else:
            if isinstance(state, self.__state_class):
                self.__validated_state = state
            else:
                self.report_errors("State provided to register " +\
                        "is incompatible with declared state class.")

    def validated_data(self):
        return {
            'state': self.__validated_state,
            'label': self.__validated_label,
        }
