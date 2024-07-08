#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    bit.bitstring.py

Main test:
    Bitstring object testing

Updated:
    24 September 2021
"""
import unittest
import numpy as np

from bit.validators import BitstringValidator, BitstringValidationError
from bit.bitstring import Bitstring, BitstringError

def error_raiser(validator):
    validator.raise_last_error()


class Test_Bitstring_Init(unittest.TestCase):
    def test_bitstring_validity(self):
        # Fail: must raise value error.
        trial = '020'
        self.assertRaises(BitstringValidationError, Bitstring, trial)


class Test_Bitstring_Stringify(unittest.TestCase):
    def test_as_string(self):
        binstr = '010'
        bs = Bitstring(bitstring=binstr)
        self.assertTrue(bs.as_string() == binstr)

    def test_str_method(self):
        binstr = '01001010'
        bs = Bitstring(bitstring=binstr)
        self.assertTrue(str(bs) == binstr)


class Test_Bitstring_To_Integer(unittest.TestCase):
    def test_as_integer_2(self):
        binstr = '010'
        integer = 2
        bs = Bitstring(bitstring=binstr)
        self.assertEqual(bs.as_integer(), integer)

    def test_as_integer_4(self):
        binstr = '0100'
        integer = 4
        bs = Bitstring(bitstring=binstr)
        self.assertEqual(bs.as_integer(),integer)

    def test_array(self):
        binstr = '0100'
        bs = Bitstring(bitstring=binstr)
        array = np.array([0,1,0,0], dtype=np.intc)
        self.assertTrue(np.array_equal(bs.as_array(), array))


class Test_Bitstring_To_Fraction(unittest.TestCase):
    def test_as_fraction_one(self):
        binstr = '11'
        frac = 0.75
        bs = Bitstring(bitstring=binstr)
        self.assertEqual(bs.as_fraction(), frac)

    def test_as_fraction_two(self):
        binstr = '011'
        frac = 0.375
        bs = Bitstring(bitstring=binstr)
        self.assertEqual(bs.as_fraction(), frac)

    def test_as_fraction_three(self):
        binstr = '0011'
        frac = 0.1875
        bs = Bitstring(bitstring=binstr)
        self.assertEqual(bs.as_fraction(), frac)

    def test_as_fraction_four(self):
        binstr = '0'
        frac = 0.0
        bs = Bitstring(bitstring=binstr)
        self.assertEqual(bs.as_fraction(), frac)

    def test_as_fraction_five(self):
        binstr = '1'
        frac = 0.5
        bs = Bitstring(bitstring=binstr)
        self.assertEqual(bs.as_fraction(), frac)
