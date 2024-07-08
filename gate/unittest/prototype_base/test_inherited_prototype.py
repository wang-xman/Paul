#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.validator.py

Main test:
    Validate a prototype that inherits from another prototype.
    A prototype can inherit all properties and method from
    its parent class.

    In earlier version, this is not possible due to the use
    of searching `.__dict__` instead of `getattr()` method.

Updated:
    06 September 2021
"""
import unittest
from gate.prototype.base import GatePrototypeValidator


def error_raiser(validator):
    if not validator.is_valid:
        validator.raise_last_error()


class gate_empty_parameters:
    alias = 'AlphaBeta'
    minimal_number_of_qubits = 1
    parameters = {}

    def gate_matrix(self):
        pass

class inherited_gate(gate_empty_parameters):
    """ Inherited from another gate prototype

    Should cause any error since all properties are
    inherited.
    """


class Test_Inherited_Gate(unittest.TestCase):
    def test_inherited_gate(self):
        test_gate = inherited_gate
        # Okay
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertTrue(validator.is_valid)
