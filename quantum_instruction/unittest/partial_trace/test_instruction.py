"""
File under test
    quantum_instruction.partial_trace_instruction.py

Main test:
    Partial trace instruction object.

Updated:
    14 August 2021
"""
import unittest

from quantum_instruction.base import InstructionBaseError
from quantum_instruction.partial_trace.instructions import \
    PartialTraceInstruction


def raiser(validator):
    validator.raise_last_error()


def instruction(instruc_dict):
    return PartialTraceInstruction(instruc_dict=instruc_dict)


class Test_LocalReference(unittest.TestCase):
    def test_local_reference_without_local_range(self):
        instruc_dict = {
            'register': 'REG1',
        }
        instruc = instruction(instruc_dict)
        self.assertTrue(instruc.has_register)
        self.assertFalse(instruc.has_local_index_range)
        self.assertFalse(instruc.has_global_index_range)
        self.assertEqual(instruc.register, 'REG1')
        self.assertRaises(InstructionBaseError, getattr, instruc, 'local_index_range')
        self.assertRaises(InstructionBaseError, getattr, instruc, 'global_index_range')

    def test_local_reference_with_local_range(self):
        instruc_dict = {
            'register': 'REG1',
            'local_index_range': [0,2]
        }
        instruc = instruction(instruc_dict)
        self.assertTrue(instruc.has_register)
        self.assertTrue(instruc.has_local_index_range)
        self.assertFalse(instruc.has_global_index_range)
        self.assertEqual(instruc.register, 'REG1')
        self.assertListEqual(instruc.local_index_range, [0,2])
        self.assertRaises(InstructionBaseError, getattr, instruc, 'global_index_range')


class Test_GlobalReference(unittest.TestCase):
    def test_pass(self):
        instruc_dict = {
            'global_index_range': [0,2]
        }
        instruc = instruction(instruc_dict)
        self.assertFalse(instruc.has_register)
        self.assertFalse(instruc.has_local_index_range)
        self.assertTrue(instruc.has_global_index_range)
        self.assertTrue(instruc.global_index_range == [0,2])
