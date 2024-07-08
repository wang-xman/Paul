#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.prototype.py

Main test:
    Gate prototype base class

Updated:
    29 April 2021
"""
import unittest
from gate.base import GateBaseValidationError
from gate.parameter import InputQubitState
from gate.prototype.base import SingleQubitGatePrototype


class gate_pass_1(SingleQubitGatePrototype):
    minimal_number_of_qubits = 1
    alias = "Wookie"
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class gate_pass_2(SingleQubitGatePrototype):
    minimal_number_of_qubits = 1
    alias = "Wookie"
    parameters = {'input_state': InputQubitState()}
    gate_matrix = None

    def gate_apply(self):
        pass

class TestSingleQubitGatePrototype(unittest.TestCase):
    def test_pass(self):
        gate_pass_1()
        gate_pass_2()


class gate_fail_1(SingleQubitGatePrototype):
    """ A single-qubit gate has a mismatched default number of qubits """
    minimal_number_of_qubits = 2
    alias = "Wookie"
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class TestSingleQubitGatePrototype_WrongNOQ(unittest.TestCase):
    def test_gate_fail(self):
        def init(x=None):
            gate_fail_1()
        # Error: instantiating gate_fail_1 causes error;
        # SingleQubitGate requires the default number of qubits to be 1.
        self.assertRaises(GateBaseValidationError, init, None)
