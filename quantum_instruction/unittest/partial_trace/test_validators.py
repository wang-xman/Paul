"""
File under test
    quantum_instruction.partial_trace_instruction.py

Main test:
    Test partial trace instruction validators.

Updated:
    13 August 2021
"""
import unittest

from quantum_instruction.partial_trace.instructions import \
    PartialTraceInstructionDictValidator


def raiser(validator):
    validator.raise_last_error()


def instruction_validator(opdict):
    return PartialTraceInstructionDictValidator(instruc_dict=opdict)


class TestReference_NotBoth(unittest.TestCase):
    def test_both(self):
        opdict = {
            'register': 'REG1',
            'global_index_range': [2,5]
        }
        validator = instruction_validator(opdict)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])
        self.assertRaises(Exception, raiser, validator)


class TestLocalReference_Success(unittest.TestCase):
    def test_okay_register_only(self):
        opdict = {
            'register': 'REG1'
        }
        validator = instruction_validator(opdict)
        self.assertTrue(validator.is_valid)
        self.assertDictEqual(opdict, validator.validated_data())

    def test_okay_with_index_range(self):
        opdict = {
            'register': 'REG1',
            'local_index_range': [2,5]
        }
        validator = instruction_validator(opdict)
        self.assertTrue(validator.is_valid)
        self.assertDictEqual(opdict, validator.validated_data())

    def test_okay_with_index_range_reversed(self):
        opdict = {
            'register': 'REG1',
            'local_index_range': [12,5]
        }
        validator = instruction_validator(opdict)
        self.assertTrue(validator.is_valid)
        self.assertDictEqual(opdict, validator.validated_data())
        self.assertListEqual(opdict['local_index_range'],
                             validator.validated_data()['local_index_range'])


class TestLocalReference_RegisterError(unittest.TestCase):
    def test_register_nonstring(self):
        opdict = {
            'register': 10
        }
        validator = instruction_validator(opdict)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])
        self.assertRaises(Exception, raiser, validator)

    def test_register_missing(self):
        opdict = {
            'local_index_range': [2,5]
        }
        validator = instruction_validator(opdict)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])
        self.assertRaises(Exception, raiser, validator)


class TestLocalReference_LocalIndexError(unittest.TestCase):
    def test_local_range_noninteger(self):
        opdict = {
            'register': 'REG1',
            'local_index_range': [0.1, 5]
        }
        validator = instruction_validator(opdict)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])
        self.assertRaises(Exception, raiser, validator)


class TestGlobalReference(unittest.TestCase):
    def test_global_range_noninteger(self):
        opdict = {
            'global_index_range': [0.1, 5]
        }
        validator = instruction_validator(opdict)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])
        self.assertRaises(Exception, raiser, validator)

    def test_global_range_single_interger(self):
        opdict = {
            'global_index_range': 5
        }
        validator = instruction_validator(opdict)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])
        self.assertRaises(Exception, raiser, validator)


class TestGlobalReference_Success(unittest.TestCase):
    def test_normal_order(self):
        opdict = {
            'global_index_range': [1,5]
        }
        validator = instruction_validator(opdict)
        self.assertTrue(validator.is_valid)
        self.assertDictEqual(opdict, validator.validated_data())

    def test_reversed_order(self):
        opdict = {
            'global_index_range': [11,5]
        }
        validator = instruction_validator(opdict)
        self.assertTrue(validator.is_valid)
        self.assertDictEqual(opdict, validator.validated_data())

    def test_identical_limits(self):
        opdict = {
            'global_index_range': [5,5]
        }
        validator = instruction_validator(opdict)
        self.assertTrue(validator.is_valid)
        self.assertDictEqual(opdict, validator.validated_data())
