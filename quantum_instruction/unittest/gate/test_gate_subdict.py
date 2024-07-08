#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_instruction.gate_instruction.py

Main test:
    Gate dictionary for gate operation instruction.

Updated:
    03 September 2021
"""
import unittest
from gate import single_qubit_gates as singles
from quantum_instruction.base import InstructionBaseValidationError
from quantum_instruction.gate.validators import GateSubdictValidator


def error_raiser(validator):
    validator.raise_last_error()


class TestGateDictValidator(unittest.TestCase):
    def test_no_alias(self):
        gate_dict = {
            'label': 'Hahah',
            'parameters': None
        }
        validator = GateSubdictValidator(gate_dict=gate_dict)
        self.assertFalse(validator.is_valid)
        # Error: alias is missing
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_non_string_alias(self):
        gate_dict = {
            'alias': 10,
            'parameters': None
        }
        validator = GateSubdictValidator(gate_dict=gate_dict)
        self.assertFalse(validator.is_valid)
        # Error: alias is not a string
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_gate_cannot_be_found(self):
        gate_dict = {
            'alias' : 'flip',
            'parameters': None
        }
        validator = GateSubdictValidator(gate_dict=gate_dict)
        # Error: gate can not be found
        self.assertFalse(validator.is_valid)


class TestGateDictValidator_Parameters(unittest.TestCase):
    def test_empty_parameters(self):
        gate_dict = {
            'alias': 'PhaseRotation',
            'parameters': {}
        }
        validator = GateSubdictValidator(gate_dict=gate_dict)
        self.assertTrue(validator.is_valid)

    def test_missing_parameters(self):
        gate_dict = {
            'alias': 'PhaseRotation'
        }
        validator = GateSubdictValidator(gate_dict=gate_dict)
        # Error: parameters dictionary is missing
        self.assertFalse(validator.is_valid)


class TestGateDictValidator_User_Defined(unittest.TestCase):
    def test_instance_wrong_type(self):
        gate_dict = {
            'instance': 'PhaseRotation',
            'alias': 'PhaseRotation',
            'parameters': {}
        }
        validator = GateSubdictValidator(gate_dict=gate_dict)
        self.assertFalse(validator.is_valid)
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_with_instance(self):
        gate_instance = singles['Flip']
        gate_dict = {
            'instance': gate_instance,
            'parameters': {}
        }
        validator = GateSubdictValidator(gate_dict=gate_dict)
        self.assertTrue(validator.is_valid)

    def test_with_instance_and_mismatched_alias(self):
        gate_instance = singles['Flip']
        gate_dict = {
            'instance': gate_instance,
            'alias': 'Not_Flip',
            'parameters': {}
        }
        validator = GateSubdictValidator(gate_dict=gate_dict)
        self.assertFalse(validator.is_valid)
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)
