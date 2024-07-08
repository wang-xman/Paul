#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

measurement.validators.py

PATH

[app_root]/measurement/validators.py

INTRO

Specialised valiators used in packge.

LOG

Updated on 06 October 2021 | Created on 05 April 2021
"""
from quantum_state import QuantumState
from density_matrix import DensityMatrix

from .base import MeasurementBaseValidator
from .errors import TargetSystemValidationError


class TargetSystemValidator(MeasurementBaseValidator):
    """ Validate target system

    Target system is used in partial trace, measurement,
    etc.

    A target system must be a quantum state or a density
    matrix that represent a mixed ensemble.

    TODO Not in use. Consider convert this into a target
    system type.
    """
    error_class = TargetSystemValidationError

    def __init__(self, system):
        super().__init__()
        self.validate(system=system)

    def validate(self, system=None):
        if not isinstance(system, DensityMatrix) and \
                not isinstance(system, QuantumState):
            self.report_errors("Target system is neither " +\
                    "a quantum state nor a density matrix.")
