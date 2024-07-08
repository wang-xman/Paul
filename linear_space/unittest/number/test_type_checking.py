#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.number.numbers.py

Updated:
    29 September 2021
"""
import unittest

from linear_space.number.types import Integer, Float, Real, Complex, Imaginary, Number


class Test_Integer(unittest.TestCase):
    def test_non_subclassable(self):
        self.assertRaises(TypeError, type, 'SubInteger', (Integer,), {})

    def test_non_instantiation(self):
        self.assertRaises(TypeError, Integer)
        
    def test_pass(self):
        self.assertTrue(isinstance(1, Integer))
        self.assertTrue(isinstance(10, Integer))
        self.assertTrue(isinstance(9929, Integer))
        self.assertTrue(isinstance(-86, Integer))

    def test_non_integer(self):
        self.assertFalse(isinstance(0.8, Integer))
        self.assertFalse(isinstance(-20.8, Integer))
        self.assertFalse(isinstance('0.8', Integer))
        self.assertFalse(isinstance(1j, Integer))

class Test_Float(unittest.TestCase):
    def test_non_subclassable(self):
        self.assertRaises(TypeError, type, 'SubFloat', (Float,), {})

    def test_non_instantiation(self):
        self.assertRaises(TypeError, Float)

    def test_integer_is_not_float(self):
        self.assertFalse(isinstance(1, Float))
        self.assertFalse(isinstance(10, Float))
        self.assertFalse(isinstance(9929, Float))
        self.assertFalse(isinstance(-86, Float))

    def test_float(self):
        self.assertTrue(isinstance(1.0, Float))
        self.assertFalse(isinstance(1.0, Integer))
        self.assertTrue(isinstance(0.00001, Float))
        self.assertFalse(isinstance(0.00001, Integer))
        self.assertTrue(isinstance(10.0e-3, Float))
        self.assertFalse(isinstance(10.0e-3, Integer))
        #self.assertTrue(isinstance(9929, Float))
        #self.assertTrue(isinstance(-86, Float))

    def test_non_float(self):
        self.assertFalse(isinstance(0.8j, Float))
        self.assertFalse(isinstance(-20.8j, Float))
        self.assertFalse(isinstance('0.8', Float))
        self.assertFalse(isinstance(1j, Float))

class Test_Real(unittest.TestCase):
    def test_non_subclassable(self):
        self.assertRaises(TypeError, type, 'SubReal', (Real,), {})

    def test_non_instantiable(self):
        self.assertRaises(TypeError, Real)

    def test_integer_is_real(self):
        self.assertTrue(isinstance(1, Real))
        self.assertTrue(isinstance(10, Real))
        self.assertTrue(isinstance(9929, Real))
        self.assertTrue(isinstance(-86, Real))

    def test_float_is_real(self):
        self.assertTrue(isinstance(0.8, Real))
        self.assertTrue(isinstance(20.8, Real))
        self.assertTrue(isinstance(1.0e-4, Real))
        self.assertTrue(isinstance(1000.0, Real))

    def test_not_real(self):
        self.assertFalse(isinstance(0.8j, Float))
        self.assertFalse(isinstance(-20.8j, Float))
        self.assertFalse(isinstance('0.8', Float))
        self.assertFalse(isinstance(1j, Float))


class Test_Complex(unittest.TestCase):
    def test_non_subclassable(self):
        self.assertRaises(TypeError, type, 'SubClass', (Complex,), {})

    def test_non_instantiation(self):
        self.assertRaises(TypeError, Complex)

    def test_complex_is_not_real(self):
        self.assertTrue(isinstance(0.8j, Complex))
        self.assertFalse(isinstance(0.8j, Real))
        self.assertFalse(isinstance(0.8j, Float))
        self.assertFalse(isinstance(0.8j, Integer))

    def test_complex_is_not_real_2(self):
        num = 1. + 0.j
        self.assertTrue(isinstance(num, Complex))
        self.assertFalse(isinstance(num, Real))

    def test_real_is_not_complex(self):
        self.assertTrue(isinstance(0.8, Real))
        self.assertFalse(isinstance(0.8, Complex))
        self.assertTrue(isinstance(8, Real))
        self.assertFalse(isinstance(8, Complex))
        self.assertTrue(isinstance(10000000, Real))
        self.assertFalse(isinstance(10000000, Complex))


class Test_Imaginary(unittest.TestCase):
    def test_non_subclassable(self):
        self.assertRaises(TypeError, type, 'SubClass', (Imaginary,), {})

    def test_non_instantiation(self):
        self.assertRaises(TypeError, Imaginary)

    def test_complex_is_not_always_imag(self):
        num = 1.0 + 0.6j
        self.assertTrue(isinstance(num, Complex))
        self.assertFalse(isinstance(num, Imaginary))
        self.assertFalse(isinstance(num, Real))
        self.assertFalse(isinstance(num, Float))
        self.assertFalse(isinstance(num, Integer))

    def test_imag(self):
        num = 0.6j
        self.assertTrue(isinstance(num, Complex))
        self.assertTrue(isinstance(num, Imaginary))
        self.assertFalse(isinstance(num, Real))
        self.assertFalse(isinstance(num, Float))
        self.assertFalse(isinstance(num, Integer))


class Test_Number(unittest.TestCase):
    def test_non_subclassable(self):
        self.assertRaises(TypeError, type, 'SubNumber', (Number,), {})

    def test_non_instantiation(self):
        self.assertRaises(TypeError, Number)

    def test_integer(self):
        num = 10
        self.assertTrue(isinstance(num, Number))
        self.assertTrue(isinstance(num, Integer))
        self.assertFalse(isinstance(num, Float))
        self.assertTrue(isinstance(num, Real))
        self.assertFalse(isinstance(num, Complex))
        self.assertFalse(isinstance(num, Imaginary))

    def test_float(self):
        num = 10.04
        self.assertTrue(isinstance(num, Number))
        self.assertFalse(isinstance(num, Integer))
        self.assertTrue(isinstance(num, Float))
        self.assertTrue(isinstance(num, Real))
        self.assertFalse(isinstance(num, Complex))
        self.assertFalse(isinstance(num, Imaginary))

    def test_real(self):
        num = 0.04
        self.assertTrue(isinstance(num, Number))
        self.assertFalse(isinstance(num, Integer))
        self.assertTrue(isinstance(num, Float))
        self.assertTrue(isinstance(num, Real))
        self.assertFalse(isinstance(num, Complex))
        self.assertFalse(isinstance(num, Imaginary))

    def test_complex(self):
        num = 0.04 + 1.j
        self.assertTrue(isinstance(num, Number))
        self.assertFalse(isinstance(num, Integer))
        self.assertFalse(isinstance(num, Float))
        self.assertFalse(isinstance(num, Real))
        self.assertTrue(isinstance(num, Complex))
        self.assertFalse(isinstance(num, Imaginary))

    def test_imag(self):
        num = 1.j
        self.assertTrue(isinstance(num, Number))
        self.assertFalse(isinstance(num, Integer))
        self.assertFalse(isinstance(num, Float))
        self.assertFalse(isinstance(num, Real))
        self.assertTrue(isinstance(num, Complex))
        self.assertTrue(isinstance(num, Imaginary))
