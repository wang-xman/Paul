#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    bit.utils.py

Main test:
    Utility functions used in package.

Updated:
    24 September 2021
"""
import unittest
import numpy as np
from linear_space.vector import StandardBasisVector
from bit.base import BitBaseValidationError
from bit.validators import BitstringValidator, BitstringValidationError
from bit.bitstring import Bitstring, BitstringError
from bit.utils import bitstring_to_integer, bitstring_to_standard_basis, \
    integer_to_bitstring, integer_to_bitarray, bitstring_to_fraction, \
    bitlist_to_vector, vector_to_bitlist, flip_bit, flip_all, swap_bits, \
        BitUtilityFunctionError


class Test_Bistring_to_Integer(unittest.TestCase):
    def test_bitstring_to_integer(self):
        binstr = '001'
        integer = bitstring_to_integer(binstr)
        self.assertEqual(1, integer)

        binstr = '011'
        integer = bitstring_to_integer(binstr)
        self.assertEqual(3, integer)

        binstr = '111'
        integer = bitstring_to_integer(binstr)
        self.assertEqual(7, integer)

        binstr = '1111'
        integer = bitstring_to_integer(binstr)
        self.assertEqual(15, integer)


class Test_Integer_to_Bitstring(unittest.TestCase):
    def test_integer_to_bitstring(self):
        integer = 2
        digits = 5
        res = '00010'
        bs = integer_to_bitstring(integer=integer, total_digits=digits)
        self.assertEqual(res, bs)

    def test_integer_to_array(self):
        integer = 2
        digits = 4
        res = np.array([0,0,1,0], dtype=np.intc)
        bs = integer_to_bitarray(integer=integer, total_digits=digits)
        self.assertTrue(np.array_equal(res, bs))

        # Fails
        integer = 2
        digits = 5
        # only 4 digits
        res = np.array([0,0,1,0], dtype=np.intc)
        bs = integer_to_bitarray(integer=integer, total_digits=digits)
        self.assertFalse(np.array_equal(res, bs))


class Test_Bitstring_to_Fraction(unittest.TestCase):
    def test_to_fraction_zero(self):
        bs = '0'
        expected = 0
        frac = bitstring_to_fraction(bs)
        self.assertEqual(frac, expected)

    def test_to_fraction_one(self):
        bs = '1'
        expected = 0.5
        frac = bitstring_to_fraction(bs)
        self.assertEqual(frac, expected)

    def test_to_fraction_two(self):
        bs = '11'
        expected = 0.75
        frac = bitstring_to_fraction(bs)
        self.assertEqual(frac, expected)

    def test_to_fraction_three(self):
        bs = '111'
        expected = 0.875
        frac = bitstring_to_fraction(bs)
        self.assertEqual(frac, expected)

    def test_to_fraction_four(self):
        bs = '0111'
        expected = 0.4375
        frac = bitstring_to_fraction(bs)
        self.assertEqual(frac, expected)


class Test_Bistring_to_Standard_Basis(unittest.TestCase):
    def test_single_bit_0(self):
        bs = '0'
        sbv = bitstring_to_standard_basis(bs)
        expected = StandardBasisVector(iloc=0,size=2)
        self.assertEqual(expected, sbv)

    def test_single_bit_1(self):
        bs = '1'
        sbv = bitstring_to_standard_basis(bs)
        expected = StandardBasisVector(iloc=1,size=2)
        self.assertEqual(expected, sbv)

    def test_two_bit_2(self):
        bs = '10'
        sbv = bitstring_to_standard_basis(bs)
        expected = StandardBasisVector(iloc=2,size=4)
        self.assertEqual(expected, sbv)

    def test_two_bit_3(self):
        bs = '11'
        sbv = bitstring_to_standard_basis(bs)
        expected = StandardBasisVector(iloc=3,size=4)
        self.assertEqual(expected, sbv)


class Test_Bitlist_To_Vector(unittest.TestCase):
    def test_okay(self):
        bl = [(0.5,'1'), (0.5,'0')]
        vec = bitlist_to_vector(bl)
        self.assertEqual(vec[0], 0.5)
        self.assertEqual(vec[1], 0.5)

    def test_okay_3bits(self):
        bl = [(0.5,'000'), (0.5,'010')]
        vec = bitlist_to_vector(bl)
        self.assertEqual(vec[0], 0.5)
        self.assertEqual(vec[2], 0.5)

    def test_not_okay(self):
        bl = [('0.5','1'), (0.5,'0')]
        #vec = bitlist_to_vector(bl)
        self.assertRaises(BitUtilityFunctionError, bitlist_to_vector, bl)


class Test_Flip_Bit(unittest.TestCase):
    def test_flip_1(self):
        bs = '0100'
        nbs = flip_bit(bs, index=2)
        self.assertTrue(nbs == '0110')

    def test_flip_2(self):
        bs = '0100'
        nbs = flip_bit(bs, index=0)
        self.assertTrue(nbs == '1100')

    def test_flip_3(self):
        bs = '0100'
        nbs = flip_bit(bs, index=3)
        self.assertTrue(nbs == '0101')

    def test_flip_fail(self):
        bs = '0100'
        #nbs = flip_bit(bs, 4)
        # Fail: index out of range.
        self.assertRaises(BitUtilityFunctionError, flip_bit, bs, 4)


class Test_Flip_All(unittest.TestCase):
    def test_flip_all(self):
        bs = '010010'
        flipped = '101101'
        nbs = flip_all(bs)
        self.assertEqual(nbs, flipped)

    def test_flip_all_2(self):
        bs = '0000000000'
        flipped = '1111111111'
        nbs = flip_all(bs)
        self.assertEqual(nbs, flipped)


class Test_Swap_Bits(unittest.TestCase):
    def test_swap_bits(self):
        bs = '10010'
        # swap indice 0 and 2
        nbs = swap_bits(bs, 0,2)
        expected = '00110'
        self.assertEqual(nbs, expected)
        nbs = swap_bits(bs, 1,3)
        expected = '11000'
        self.assertEqual(nbs, expected)
