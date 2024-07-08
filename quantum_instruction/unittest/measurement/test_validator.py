"""
File under test
    quantum_instruction.measurement_instruction.py

Main test:
    Measurement instruction object.

[Measure a register in computational basis]
To measure an entire register labelled 'COMPREG' in its
computational basis
    {
        'register': 'COMPREG'
    }
is the required operation dictionary.

[Measure a register in designated projection state]
To measure a register labelled 'COMPUREG' using a given
qubit state, operation dictionary
    {
        'register': 'COMPREG',
        'state': QubitState instance
    }
where value to `state` is a `QubitState` instance.

Updated:
    25 August 2021
"""
import unittest
from qubit.utils import qubit_from_bitlist
from quantum_instruction.base import InstructionBaseValidationError
from quantum_instruction.measurement.validators import \
    MeasurementInstructionDictValidator

def raiser(validator):
    validator.raise_last_error()

proj_state = qubit_from_bitlist([(1, '010')])


class Test_without_State(unittest.TestCase):
    def test_okay(self):
        instruc_dict = {
            'register': 'REG1',
        }
        validator = MeasurementInstructionDictValidator(instruc_dict=instruc_dict)
        self.assertTrue(validator.is_valid)

    def test_missing_register(self):
        instruc_dict = {
            'what_register': 'REG1',
        }
        validator = MeasurementInstructionDictValidator(instruc_dict=instruc_dict)
        self.assertFalse(validator.is_valid)
        self.assertRaises(InstructionBaseValidationError, raiser, validator)


class Test_with_State(unittest.TestCase):
    def test_okay(self):
        instruc_dict = {
            'register': 'REG1',
            'state': proj_state
        }
        validator = MeasurementInstructionDictValidator(instruc_dict=instruc_dict)
        self.assertTrue(validator.is_valid)
        vd = validator.validated_data()
        self.assertTrue(vd['state'] == proj_state)

    def test_missing_register(self):
        instruc_dict = {
            'what_register': 'REG1',
            'state': proj_state
        }
        validator = MeasurementInstructionDictValidator(instruc_dict=instruc_dict)
        self.assertFalse(validator.is_valid)
        self.assertRaises(InstructionBaseValidationError, raiser, validator)

    def test_state_wrong_type(self):
        instruc_dict = {
            'what_register': 'REG1',
            'state': 'ALFA'
        }
        validator = MeasurementInstructionDictValidator(instruc_dict=instruc_dict)
        self.assertFalse(validator.is_valid)
        self.assertRaises(InstructionBaseValidationError, raiser, validator)
