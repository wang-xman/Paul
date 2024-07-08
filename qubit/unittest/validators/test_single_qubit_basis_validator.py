#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.validator.py

Main test
    Single qubit basis validator

Updated:
    25 September 2021
"""
import unittest
from common import Validation_Error
from qubit.validators import SingleQubitBasisValidator


def error_raiser(validator):
    validator.raise_last_error()


class TestSingleQubitBasisValidator(unittest.TestCase):
    def test_string_with_number(self):
        # Error: string is not a string, but a number.
        tstring = 0
        validator = SingleQubitBasisValidator(bitstring=tstring)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_empty_string(self):
        tstring = ''
        validator = SingleQubitBasisValidator(bitstring=tstring)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_string_has_letters(self):
        # Reports error
        tstring = 'po'
        validator = SingleQubitBasisValidator(bitstring=tstring)
        self.assertRaises(Validation_Error, error_raiser, validator)

    def test_pass(self):    
        # Okay
        tstring = '0'
        test_obj = SingleQubitBasisValidator(bitstring=tstring)
        self.assertTrue(len(test_obj.get_errors()) == 0)
        vd = test_obj.validated_data()
        self.assertEqual(tstring, vd['bitstring'])

        # Okay
        tstring = '1'
        test_obj = SingleQubitBasisValidator(bitstring=tstring)
        self.assertTrue(len(test_obj.get_errors()) == 0)
        vd = test_obj.validated_data()
        self.assertEqual(tstring, vd['bitstring'])

    def test_string_means_more_than_one_qubit(self):
        # Error: string contains more than 1 qubit
        tstring = '01'
        validator = SingleQubitBasisValidator(bitstring=tstring)
        self.assertRaises(Validation_Error, error_raiser, validator)
