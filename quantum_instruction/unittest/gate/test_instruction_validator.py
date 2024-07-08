"""
File under test
    quantum_instruction.gate.instructions.py

Main test:
    Gate(-operation) instruction validator.

Updated:
    12 August 2021
"""
import unittest
from quantum_instruction.gate.validators import GateInstructionDictValidator


def error_raiser(validator):
    validator.raise_last_error()


class TestValidator(unittest.TestCase):
    def test_okay(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 1,
            'state': '1'
        }
        opdict = {
            'gate': {
                'alias': 'Flip',
                'parameters': {}
            },
            'target': {
                'register': 'reg2',
                'local_index': 1
            },
            'control': {
                'list':[el, el2]
            }
        }
        validator = GateInstructionDictValidator(instruc_dict=opdict)
        #raise validator.report_errors()[0]
        self.assertTrue(validator.is_valid)
        # Error: key list is non list
        #self.assertRaises(OperationValidationError, error_raiser, validator)


class Test_UnknownKeysWarning(unittest.TestCase):
    def test_warning_on_unknown_keys(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 2,
            'state': '1'
        }
        opdict = {
            'gate': {
                'alias': 'Flip',
                'parameters': {}
            },
            'target': {
                'register': 'reg1',
                'local_index': 3
            },
            'control': {
                'list': [el, el2]
            },
            'extra': 10
        }
        # A warning is triggered
        validator = GateInstructionDictValidator(instruc_dict=opdict)
        self.assertTrue(validator.is_valid)
