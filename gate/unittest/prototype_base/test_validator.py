#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.validator.py

Main test:
    Gate prototype validators and validator errors

Updated:
    06 September 2021
"""
import unittest

from common import Validation_Error
from gate.prototype.base import GatePrototypeValidator
from gate.parameter import InputQubitState


def error_raiser(validator):
    if not validator.is_valid:
        validator.raise_last_error()


class naked_gate:
    pass


class TestGateValidator_NakedGate(unittest.TestCase):
    def test_naked_gate(self):
        test_gate = naked_gate
        # Error: first complain mssing parameters
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)


class gate_without_parameters:
    alias = 'AlphaBeta'
    minimal_number_of_qubits = 1

    def gate_matrix(self):
        pass

class gate_empty_parameters:
    alias = 'AlphaBeta'
    minimal_number_of_qubits = 1
    parameters = {}

    def gate_matrix(self):
        pass

class gate_no_input_state_without_gate_apply:
    alias = 'AlphaBeta'
    minimal_number_of_qubits = 1
    parameters = {'alpha_state': InputQubitState()}

    def gate_matrix(self):
        pass

class gate_with_gate_apply:
    alias = 'AlphaBeta'
    minimal_number_of_qubits = 1
    parameters = {'alpha_state': InputQubitState()}

    def gate_apply(self):
        pass

    def gate_matrix(self):
        pass

class gate_with_gate_apply_without_gate_matrix:
    alias = 'AlphaBeta'
    minimal_number_of_qubits = 1
    parameters = {
        'input_state': InputQubitState(),
        'alpha_state': InputQubitState()}

    def gate_apply(self):
        pass

class TestGateValidator_Parameters(unittest.TestCase):
    def test_gate_without_parameters(self):
        test_gate = gate_without_parameters
        # Error: no parameters
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_gate_with_gate_apply_without_gate_matrix(self):
        test_gate = gate_with_gate_apply_without_gate_matrix
        # Pass:
        GatePrototypeValidator(prototype=test_gate)


class gate_without_default_noq:
    alias = 'AlphaBeta'
    parameters = {'alpha_state': InputQubitState()}

    def gate_apply(self):
        pass

class gate_without_default_noq_2:
    alias = 'AlphaBeta'
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class gate_default_noq_noninteger:
    alias = 'AlphaBeta'
    minimal_number_of_qubits = 0.5
    parameters = {'alpha_state': InputQubitState()}

    def gate_apply(self):
        pass

class gate_default_noq_noninteger_2:
    alias = 'AlphaBeta'
    minimal_number_of_qubits = '0.5'
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class TestGateValidator_NOQ(unittest.TestCase):
    def test_gate_without_default_noq(self):
        test_gate = gate_without_default_noq
        # Error: no default noq
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_gate_without_default_noq_2(self):
        test_gate = gate_without_default_noq_2
        # Error: no default noq
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_gate_default_noq_noninteger(self):
        test_gate = gate_default_noq_noninteger
        # Error: non integer default noq
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_gate_default_noq_noninteger_2(self):
        test_gate = gate_default_noq_noninteger_2
        # Error: non integer default noq
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)


class gate_no_alias:
    minimal_number_of_qubits = 1
    parameters = {'alpha_state': InputQubitState()}

    def gate_apply(self):
        pass

class gate_no_alias_2:
    minimal_number_of_qubits = 1
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class gate_nonstring_alias:
    alias = 10
    minimal_number_of_qubits = 1
    parameters = {'alpha_state': InputQubitState()}

    def gate_apply(self):
        pass

class gate_nonstring_alias_2:
    alias = 0.5
    minimal_number_of_qubits = 1
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class gate_alias_empty_string:
    alias = ''
    minimal_number_of_qubits = 1
    parameters = {'alpha_state': InputQubitState()}

    def gate_apply(self):
        pass

class gate_alias_empty_string_2:
    alias = ''
    minimal_number_of_qubits = 1
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class gate_alias_with_space:
    alias = 'A '
    minimal_number_of_qubits = 1
    parameters = {'alpha_state': InputQubitState()}

    def gate_apply(self):
        pass

class gate_alias_with_space_2:
    alias = ' BR'
    minimal_number_of_qubits = 1
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class TestGateValidator_Alais(unittest.TestCase):
    def test_gate_no_alias(self):
        test_gate = gate_no_alias
        # Error: no alias
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_gate_no_alias_2(self):
        test_gate = gate_no_alias_2
        # Error: no alias
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_nonstring_alias(self):
        test_gate = gate_nonstring_alias
        # Error: not a string
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_nonstring_alias_2(self):
        test_gate = gate_nonstring_alias_2
        # Error: not a string
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_alias_empty_string(self):
        test_gate = gate_alias_empty_string
        # Error: empty string
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_alias_empty_string_2(self):
        test_gate = gate_alias_empty_string_2
        # Error: empty string
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_alias_with_space(self):
        test_gate = gate_alias_with_space
        # Error: alias has space
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_alias_with_space_2(self):
        test_gate = gate_alias_with_space_2
        # Error: alias has space
        validator = GatePrototypeValidator(prototype=test_gate)
        self.assertRaises(Validation_Error, error_raiser, validator)
