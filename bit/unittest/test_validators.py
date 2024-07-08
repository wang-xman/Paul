#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    bit.validator.py

Main test:
    Bit object validator.

Updated:
    24 September 2021
"""
import unittest

from bit.validators import BitstringValidator, BitstringValidationError, \
    BitlistValidator, BitlistValidationError


def error_raiser(validator):
    validator.raise_last_error()


class Test_BitstringValidator(unittest.TestCase):
    def test_pass(self):
        # Pass:
        binstr = '10101010010'
        validator = BitstringValidator(bitstring=binstr)

    def test_failure(self):
        # Fail: 
        binstr = '101010100a0'
        validator = BitstringValidator(bitstring=binstr)
        self.assertRaises(BitstringValidationError, error_raiser, validator)

    def test_empty_string(self):
        # Fail: empty string
        binstr = ''
        validator = BitstringValidator(bitstring=binstr)
        self.assertRaises(BitstringValidationError, error_raiser, validator)

    def test_string_with_space(self):
        # Fail: space is not allowed
        binstr = '1 01'
        validator = BitstringValidator(bitstring=binstr)
        self.assertRaises(BitstringValidationError, error_raiser, validator)


class Test_BitlistValidator(unittest.TestCase):
    def test_pass(self):
        bl = [(0.1, '10'), (0.2, '11'), (0.3, '01')]
        validator = BitlistValidator(bitlist=bl)
        self.assertTrue(validator.is_valid)

    def test_empty_list(self):
        bl = []
        validator = BitlistValidator(bitlist=bl)
        # Error: empty list
        self.assertFalse(validator.is_valid)
        self.assertRaises(BitlistValidationError, error_raiser, validator)

    def test_non_tuple_1(self):
        bl = [[],[]]
        validator = BitlistValidator(bitlist=bl)
        # Error: non tuple
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_non_tuple_2(self):
        bl = [[],()]
        validator = BitlistValidator(bitlist=bl)
        # Error: empty tuple, and non tuple
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_empty_tuple_3(self):
        bl = [(5, '0'),()]
        validator = BitlistValidator(bitlist=bl)
        # Error: empty tuple
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_tuple_has_no_two_elements(self):
        bl = [(1,),(2,)]
        validator = BitlistValidator(bitlist=bl)
        # Error: not two elements in tuple
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_tuple_has_no_two_elements_2(self):
        bl = [(1,1),(2,)]
        validator = BitlistValidator(bitlist=bl)
        # Error: not two elements in tuple
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_tuple_has_no_two_elements_3(self):
        bl = [(1,'1'),(2,)]
        validator = BitlistValidator(bitlist=bl)
        # Error: not two elements in tuple
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_tuple_has_no_two_elements_4(self):
        bl = [(1,'1'),(2,'1', 0)]
        validator = BitlistValidator(bitlist=bl)
        # Error: not two elements in tuple
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)


class Test_BitlistValidator_Amplitude(unittest.TestCase):
    def test_amplitude_non_numeric(self):
        bl = [('1','1'),(2,'0')]
        validator = BitlistValidator(bitlist=bl)
        # Error: non numeric amp
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_amplitude_non_numeric_2(self):
        bl = [('1','1'),('0.2','0')]
        validator = BitlistValidator(bitlist=bl)
        # Error: non numeric amp
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_amplitude_non_numeric_3(self):
        _ = 'Halo'
        bl = [(_,'1'),(0.2,'0')]
        validator = BitlistValidator(bitlist=bl)
        # Error: non numeric amp
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)


class Test_BitlistValidator_Bistring(unittest.TestCase):
    def test_non_string(self):
        bl = [(1,1), (2,'0')]
        validator = BitlistValidator(bitlist=bl)
        # Error: bit string is not string
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_non_bit(self):
        bl = [(1,'2'), (2,'0')]
        validator = BitlistValidator(bitlist=bl)
        # Error: bit string wrong symbol
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_empty(self):
        bl = [(1,''), (2,'0')]
        validator = BitlistValidator(bitlist=bl)
        # Error: bit string wrong symbol
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)

    def test_okay(self):
        bl = [(1, '1'), (2,'0')]
        validator = BitlistValidator(bitlist=bl)
        # okay
        self.assertTrue(validator.is_valid)

    def test_okay_2(self):
        bl = [(1, '10'), (0.02,'01')]
        validator = BitlistValidator(bitlist=bl)
        # okay
        self.assertTrue(validator.is_valid)

    def test_string_nonuniform_length(self):
        bl = [(1, '10'), (0.02,'011')]
        validator = BitlistValidator(bitlist=bl)
        # Error: bit string length non-uniform
        self.assertFalse(validator.is_valid)
        #validator.raise_last_error()
        self.assertRaises(BitlistValidationError, validator.raise_last_error)
