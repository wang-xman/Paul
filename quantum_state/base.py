#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.base.py

PATH

[app_root]/quantum_state/base.py

INTRO

Base classes to quantums state package. An abstract
quantum state class is created to be the base to all
quantum states.

LOG

Updated on 30 September 2021 | Created on 20 June 2020
"""
from abc import ABC
from common import Generic_Error, Validation_Error, Algebra_Error
from common import Base_Validator


class QuantumStateBaseError(Generic_Error):
    header = 'Quantum_State_Base_Error'


class QuantumStateBaseValidationError(Validation_Error):
    """ Used in validators """
    header = 'Quantum_State_Base_Validation_Error'


class QuantumStateBaseAlgebraError(Algebra_Error):
    """ Use in algebra functions """
    header = 'Quantum_State_Base_Algebra_Error'


class QuantumStateBaseValidator(Base_Validator):
    """ Base validator used in package """
    error_class = QuantumStateBaseValidationError


class SingletonMeta(type):
    """ Singleton metaclass """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                    super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractQuantumState(ABC):
    """ Abstract quantum state """
