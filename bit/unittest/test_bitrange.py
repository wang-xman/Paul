#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    bit.bitrange.py

Main test:
    Bitrange and bitrange limit validator test.

Updated:
    05 October 2021
"""
import unittest
import numpy as np

from bit.validators import BitrangeBoundValidator, BitrangeBoundValidationError,\
    BitrangeValidator, BitrangeValidationError
from bit.bitrange import Bitrange

def error_raiser(validator):
    validator.raise_last_error()

BBV = BitrangeBoundValidator


class Test_Bound_Validator(unittest.TestCase):
    def test_normal_bound(self):
        test_bound = [2,9]
        test_nob = 10
        validator = BBV(bound=test_bound)
        self.assertTrue(validator.is_valid)

    def test_reversed_bound(self):
        test_bound = [5,4]
        test_nob = 10
        validator = BBV(bound=test_bound)
        self.assertTrue(validator.is_valid)

    def test_identical_bounds(self):
        test_bound = [4,4]
        test_nob = 5
        validator = BBV(bound=test_bound)
        self.assertTrue(validator.is_valid)

    def test_negative_bound(self):
        test_bound = [-4,4]
        test_nob = 5
        validator = BBV(bound=test_bound)
        self.assertFalse(validator.is_valid)
        self.assertRaises(BitrangeBoundValidationError, error_raiser, validator)

    def test_negative_upper_bound(self):
        test_bound = [0,-4]
        test_nob = 5
        validator = BBV(bound=test_bound)
        self.assertFalse(validator.is_valid)
        self.assertRaises(BitrangeBoundValidationError, error_raiser, validator)

    def test_negative_both_bounds(self):
        test_bound = [-4,-4]
        test_nob = 0
        validator = BBV(bound=test_bound)
        self.assertFalse(validator.is_valid)
        self.assertRaises(BitrangeBoundValidationError, error_raiser, validator)


class Test_Bitrange_Validator(unittest.TestCase):
    def test_bound_out_of_range(self):
        test_bound = [0,4]
        test_nob = 3
        validator = BitrangeValidator(number_of_bits=test_nob, bound=test_bound)
        self.assertFalse(validator.is_valid)
        self.assertRaises(BitrangeValidationError, error_raiser, validator)

    def test_lower_bound_out_of_range(self):
        test_bound = [4,6]
        test_nob = 3
        validator = BitrangeValidator(number_of_bits=test_nob, bound=test_bound)
        self.assertFalse(validator.is_valid)
        self.assertRaises(BitrangeValidationError, error_raiser, validator)


class Test_Bitrange(unittest.TestCase):
    def test_normal_bound(self):
        test_bound = [2,9]
        test_nob = 10
        bitrange = Bitrange(number_of_bits=test_nob, bound=test_bound)
        self.assertTrue(bitrange.is_normal_range)
        self.assertTrue(bitrange.bound == test_bound)
        self.assertTrue(bitrange.upper_bound == 9)
        self.assertTrue(bitrange.lower_bound == 2)
        self.assertTrue(2 in bitrange.as_range())
        self.assertTrue(9 in bitrange.as_range())

    def test_reversed_bound(self):
        test_bound = [7,3]
        test_nob = 10
        bitrange = Bitrange(number_of_bits=test_nob, bound=test_bound)
        self.assertFalse(bitrange.is_normal_range)
        self.assertTrue(bitrange.bound == test_bound)
        self.assertTrue(bitrange.upper_bound == 7)
        self.assertTrue(bitrange.lower_bound == 3)
        self.assertTrue(7 in bitrange.as_range())
        self.assertTrue(3 in bitrange.as_range())
        self.assertFalse(2 in bitrange.as_range())

    def test_identical_bound(self):
        test_bound = [5,5]
        test_nob = 6
        bitrange = Bitrange(number_of_bits=test_nob, bound=test_bound)
        self.assertTrue(bitrange.is_normal_range)
        self.assertTrue(bitrange.bound == test_bound)
        self.assertTrue(bitrange.upper_bound == 5)
        self.assertTrue(bitrange.lower_bound == 5)
        self.assertFalse(7 in bitrange.as_range())
        self.assertFalse(3 in bitrange.as_range())
        self.assertFalse(2 in bitrange.as_range())
