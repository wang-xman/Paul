#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.algebra.errors.py

PATH

[app_root]/quantum_state/algebra/errors.py

INTRO

Quantum state algebra function error - QSAFE.

CONTENT

LOG

Updated on 29 September 2021 | Created on 20 June 2020
"""
from quantum_state.base import QuantumStateBaseAlgebraError


class QuantumStateAlgebraFunctionError(QuantumStateBaseAlgebraError):
    header = 'Quantum_State_Algebra_Error'
