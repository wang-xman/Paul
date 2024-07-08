#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.measurement.utils.py

PATH

[app_root]/quantum_operation/measurement/utils.py

INTRO

Utility functions

LOG

Updated on 02 October 2021 | Created on 01 August 2021
"""
from quantum_instruction.measurement import MeasurementInstruction
# from same subpack
from .errors import MeasurementOperationError
from .operations import MeasurementOperation

_MODULE_LOCATION_ = 'quantum_operation.measurement.utils'


def measurement_operation_from_instruction_dict(instruc_dict):
    """ Returns measurement operation from an instruction dict

    ARGUMENTS

    `instruc_dict` (`dict`) : instruction dictionary

    RETURN

    `measurement_op` (`MeasurementOperation`) : a measurement
    operation instance

    NOTE Not tested.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ +\
            '.measurement_operation_from_instruction_dict'
    try:
        instruc = MeasurementInstruction(instruc_dict)
        measurement_op = MeasurementOperation(instruction=instruc)
        return measurement_op
    except Exception as err:
        raise MeasurementOperationError(str(err), location=_ERROR_LOCATION_)
