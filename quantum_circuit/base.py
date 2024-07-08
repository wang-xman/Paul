#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_circuit.base.py

PATH

[app_root]/quantum_circuit/base.py

INTRO

Quantum circuit application.

Quantum circuit is an implementation of algorithms on
qubit via gate, quantum operator and measurement.

In Qubit package, quantum circuit is implemented as a
supervisor class of specialised quantum flow applicable
to quantum memory.

CONTENT

`QuantumCircuitValidationError` - Validation
error class for the entire application

`QuantumCircuitValidator` - Base validator class
used in the entire application

`QuantumCircuitError` - Error class for entire
application except validation process

LOG

Updated on 29 August 2021 | Created on 27 November 2020
"""
from common.validator import Base_Validator
from common.exception import Generic_Error, Validation_Error


class QuantumCircuitValidationError(Validation_Error):
    header = "Quantum_Circuit_Validation_Error"


class QuantumCircuitError(Generic_Error):
    """ Base error class

    Base class for all errors except validation errors.
    """
    header = "Quantum_Circuit_Error"


class QuantumCircuitValidator(Base_Validator):
    """ Base validator to all validators """
    error_class = QuantumCircuitValidationError
