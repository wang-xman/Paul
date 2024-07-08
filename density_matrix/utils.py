#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

density_matrix.utils.py

PATH

[app_root]/density_matrix/utils.py

INTRO

Utility functions.

LOG

Updated on 26 September 2021 | Created on 23 February 2021
"""
from quantum_state import QuantumState
from .density_matrix import DensityMatrix


def density_matrix_from_state(state):
    """ Construct density matrix from single state

    FIXME This function doesn't do much.
    """
    ret = None
    if isinstance(state, QuantumState):
        ret = DensityMatrix(state=state)
    return ret
