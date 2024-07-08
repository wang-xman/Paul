#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_flow.base.py

PATH

[app_root]/quantum_flow/base.py

INTRO

Quantum operation flow (quantum flow or simply flow), is a
sequence of quantum operations. Although a flow can contain
only one operation, it is not what flow is designed for.

In a gate-bases quantum computer, a flow executes operations
- transformation via application of quantum gates - on a memory,
along the direction of time evolution.

Viewed from the perspective of algorithm, a flow is equivalent to
executing algorithm steps; in a quantum circuit, these steps are
quantum operations applied on a quantum memory by quantum gates.

In this package, flow object store an internal operation list.
Index of each operation in the list is referred to as its rank;
operation with a lower rank is executed earlier.

LOG

Updated on 28 August 2021 | Created on 12 July 2021
"""
from common.validator import Base_Validator
from common.exception import Generic_Error, Validation_Error


class QuantumFlowBaseError(Generic_Error):
    """ Generic error in quantum flow application """
    header = "Quantum_Flow_Error"


class QuantumFlowBaseValidationError(Validation_Error):
    """ Generic error in quantum flow application """
    header = "Quantum_Flow_Validation_Error"


class QuantumFlowBaseValidator(Base_Validator):
    """ Quantum flow validator """
    error_class = QuantumFlowBaseValidationError
