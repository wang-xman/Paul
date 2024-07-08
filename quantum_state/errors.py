#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.errors.py

PATH

[app_root]/quantum_state/errors.py

INTRO

Dedicated errors

CONTENT


LOG

Updated on 30 September 2021 | Created on 23 June 2020
"""
from superposition.errors import SuperlistValidationError
from .base import QuantumStateBaseValidationError, QuantumStateBaseError


class QuantumStateVectorValidationError(QuantumStateBaseValidationError):
    """
    ENTRY

    `validators.QuantumStateVectorValidator`
    """
    header = 'Quantum_State_Vector_Validation_Error'


class QuantumStateError(QuantumStateBaseError):
    header = 'Quantum_State_Error'


class QuantumSuperlistValdiationError(SuperlistValidationError):
    """
    ENTRY

    `validators.QuantumSuperlistValidator`
    """
    header = 'Quantum_Superlist_Valdiation_Error'


class BraketValidationError(QuantumStateBaseValidationError):
    """
    ENTRY

    `validators.BraketValidator`
    """
    header = 'Braket_Validation_Error'


class QuantumStateConjugateError(QuantumStateBaseError):
    header = 'Quantum_State_Conjugate_Error'
