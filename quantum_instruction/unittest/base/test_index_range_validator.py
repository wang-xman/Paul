"""
File under test
    quantum_instruction.base.py

Main test:
    Index range validator.

Updated:
    13 August 2021
"""
import unittest
from quantum_instruction.index_range import IndexRangeValidator
from quantum_instruction. errors import IndexRangeError


def error_raiser(validator):
    validator.raise_last_error()


class TestIndexRangeValidator(unittest.TestCase):
    def test_okay(self):
        test_limits = [0,10]
        validator = IndexRangeValidator(range_limit_list=test_limits)
        self.assertTrue(validator.is_valid)

    def test_okay_identical(self):
        test_limits = [10,10]
        validator = IndexRangeValidator(range_limit_list=test_limits)
        self.assertTrue(validator.is_valid)


class TestIndexRangeValidator_Nonlist(unittest.TestCase):
    def test_nonlist(self):
        test_limits = (10,)
        validator = IndexRangeValidator(range_limit_list=test_limits)
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)
        self.assertRaises(IndexRangeError, error_raiser, validator)

    def test_nonlist_2(self):
        test_limits = 10
        validator = IndexRangeValidator(range_limit_list=test_limits)
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)
        self.assertRaises(IndexRangeError, error_raiser, validator)


class TestIndexRangeValidator_Nonintegers(unittest.TestCase):
    def test_noninteger(self):
        test_limits = [0, 0.5]
        validator = IndexRangeValidator(range_limit_list=test_limits)
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)
        self.assertRaises(IndexRangeError, error_raiser, validator)

    def test_noninteger_string(self):
        test_limits = ['0', 5]
        validator = IndexRangeValidator(range_limit_list=test_limits)
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)
        self.assertRaises(IndexRangeError, error_raiser, validator)

    def test_noninteger_strings(self):
        test_limits = ['0', '5']
        validator = IndexRangeValidator(range_limit_list=test_limits)
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)
        self.assertRaises(IndexRangeError, error_raiser, validator)


class TestIndexRangeValidator_NotTwoElements(unittest.TestCase):
    def test_too_few_elements(self):
        test_limits = [5]
        validator = IndexRangeValidator(range_limit_list=test_limits)
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)
        self.assertRaises(IndexRangeError, error_raiser, validator)

    def test_too_many_elements(self):
        test_limits = [0, 5, 10]
        validator = IndexRangeValidator(range_limit_list=test_limits)
        #print(validator.report_errors()[0])
        self.assertFalse(validator.is_valid)
        self.assertRaises(IndexRangeError, error_raiser, validator)
