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
from quantum_instruction.base import InstructionBaseError
from quantum_instruction.measurement.instructions import MeasurementInstruction


def raiser(validator):
    validator.raise_last_error()


def instruction(instruc_dict):
    return MeasurementInstruction(instruc_dict=instruc_dict)


class Test_without_State(unittest.TestCase):
    def test_without_local_range(self):
        instruc_dict = {
            'register': 'REG1',
        }
        instruc = instruction(instruc_dict)
        self.assertEqual(instruc.register, 'REG1')
        self.assertFalse(instruc.has_state)
        self.assertRaises(InstructionBaseError, getattr, instruc,
                          'state')


class Test_with_State(unittest.TestCase):
    def test_with_local_range(self):
        state = qubit_from_bitlist([(1,'100')])
        instruc_dict = {
            'register': 'REG1',
            'state': state
        }
        instruc = instruction(instruc_dict)
        self.assertEqual(instruc.register, 'REG1')
        self.assertTrue(instruc.has_state)
        self.assertTrue(instruc.state == state)
