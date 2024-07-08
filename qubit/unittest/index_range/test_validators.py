#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Main test:
    Index-range bound and index range validators
"""
import unittest

from qubit.errors import QubitBaseValidationError
from qubit.index_range import IndexRangeBoundValidator, IndexRangeValidator


def error_raiser(validator):
    if not validator.is_valid:
        validator.raise_last_error()


class TestBitRangeValidator_Pass(unittest.TestCase):
    def test_normal(self):
        test_noq = 4
        test_range = [0,3]
        valid_range = [0,3]
        validator = IndexRangeBoundValidator(bound=test_range)
        self.assertTrue(validator.is_valid)
        self.assertTrue(validator.validated_data()['bound'] == valid_range)

    def test_identical_limits(self):
        test_noq = 4
        test_range = [2,2]
        # validated limits is still [2,2]
        #valid_range = 2
        validator = IndexRangeBoundValidator(bound=test_range)
        self.assertTrue(validator.is_valid)
        self.assertTrue(validator.validated_data()['bound'] == test_range)

    def test_reversed(self):
        test_noq = 5
        test_range = [3,1]
        valid_range = [1,3]
        validator = IndexRangeBoundValidator(bound=test_range)
        self.assertTrue(validator.is_valid)
        self.assertTrue(validator.validated_data()['bound'] == valid_range)


class TestBitRangeValidator_Fail(unittest.TestCase):
    def test_not_list(self):
        test_noq = 3
        test_range = 2
        validator = IndexRangeBoundValidator(bound=test_range)
        self.assertRaises(QubitBaseValidationError, error_raiser, validator)

    def test_negative_lower(self):
        test_noq = 3
        test_range = [-1,2]
        validator = IndexRangeBoundValidator(bound=test_range)
        self.assertRaises(QubitBaseValidationError, error_raiser, validator)

    def test_negative_upper(self):
        test_noq = 3
        test_range = [1,-2]
        validator = IndexRangeBoundValidator(bound=test_range)
        self.assertRaises(QubitBaseValidationError, error_raiser, validator)


class Test_IndexRange_Validator(unittest.TestCase):
    def test_out_of_range(self):
        test_noq = 3
        test_range = [0,3]
        validator = IndexRangeValidator(noq=test_noq, bound=test_range)
        self.assertRaises(QubitBaseValidationError, error_raiser, validator)
