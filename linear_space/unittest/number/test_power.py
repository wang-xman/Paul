#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.number.py

Updated:
    29 September 2021
"""
import unittest

from linear_space.number.utils import is_power_of_two, exponent_of_two, NumberError


class TestIsPowerOfTwo(unittest.TestCase):
    def test_float(self):
        value = 0.9
        self.assertFalse(is_power_of_two(value))

    def test_complex(self):
        value = 4j
        self.assertFalse(is_power_of_two(value))

    def test_integer(self):
        value = 7
        self.assertFalse(is_power_of_two(value))

    def test_true(self):
        value = 8
        self.assertTrue(is_power_of_two(value))

    def test_one(self):
        value = 1
        self.assertTrue(is_power_of_two(value))


class TestExponentOfTwo(unittest.TestCase):
    def test_float(self):
        value = 0.9
        #exponent_of_two(value)
        self.assertRaises(NumberError, exponent_of_two, value)

    def test_complex(self):
        value = 4j
        self.assertRaises(NumberError, exponent_of_two, value)

    def test_integer(self):
        value = 7
        self.assertRaises(NumberError, exponent_of_two, value)

    def test_true(self):
        value = 8
        result = exponent_of_two(value)
        self.assertEqual(3, result)

    def test_one(self):
        value = 1
        result = exponent_of_two(value)
        self.assertEqual(0, result)
