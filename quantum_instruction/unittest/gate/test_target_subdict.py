"""
File under test
    quantum_instruction.gate_instruction.py

Main test:
    Gate operation instruction target sub-dictionary validators.

Updated:
    19 July 2021
"""
import unittest
from quantum_instruction.base import InstructionBaseValidationError
from quantum_instruction.gate.validators import TargetSubdictValidator


def error_raiser(validator):
    validator.raise_last_error()


class TestTargetDictValidator(unittest.TestCase):
    def test_okay(self):
        target_dict = {
            'register': 'reg1',
            'local_index': 0
        }
        validator = TargetSubdictValidator(target_dict=target_dict)
        self.assertTrue(validator.is_valid)

    def test_missing_register_key(self):
        target_dict = {
            'local_index': 0
        }
        validator = TargetSubdictValidator(target_dict=target_dict)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: key register is missing
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_nonstring_register_key(self):
        target_dict = {
            'register': 90,
            'local_index': 0
        }
        validator = TargetSubdictValidator(target_dict=target_dict)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: key register is non string
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_missing_target_index(self):
        target_dict = {
            'register': 'reg1'
        }
        validator = TargetSubdictValidator(target_dict=target_dict)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: key index is missing
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_non_integer_target_index(self):
        target_dict = {
            'register': 'reg1',
            'local_index': 'ab'
        }
        validator = TargetSubdictValidator(target_dict=target_dict)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: key index is non integer
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)
