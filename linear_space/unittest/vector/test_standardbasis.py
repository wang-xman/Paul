#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.vector.standard_basis.py

Main test:
    Basic properties of standard basis.

Updated:
    29 September 2021
"""
import unittest
import numpy as np

from common.exception import Validation_Error
from linear_space.vector.column_vector import ColumnVector
from linear_space.vector.standard_basis import StandardBasisVectorInitValidator, \
    StandardBasisVector
from linear_space.linear_object import Row_Like, Column_Like, Matrix_Like


class Test_StandardBasisVectorValidator_Success(unittest.TestCase):
    def test_success1(self):
        test_iloc = 3
        test_size = 5
        validator = StandardBasisVectorInitValidator(iloc=test_iloc, size=test_size)
        self.assertTrue(validator.is_valid)
        expected_iloc = 3
        expected_size = 5
        res_iloc = validator.validated_data()['iloc']
        res_size = validator.validated_data()['size']
        self.assertTrue(expected_iloc == res_iloc)
        self.assertTrue(expected_size == res_size)

    def test_success2(self):
        test_iloc = 0
        test_size = 50
        validator = StandardBasisVectorInitValidator(iloc=test_iloc, size=test_size)
        self.assertTrue(validator.is_valid)
        expected_iloc = 0
        expected_size = 50
        res_iloc = validator.validated_data()['iloc']
        res_size = validator.validated_data()['size']
        self.assertTrue(expected_iloc == res_iloc)
        self.assertTrue(expected_size == res_size)

    def test_success3(self):
        test_iloc = 49
        test_size = 50
        validator = StandardBasisVectorInitValidator(iloc=test_iloc, size=test_size)
        self.assertTrue(validator.is_valid)
        expected_iloc = 49
        expected_size = 50
        res_iloc = validator.validated_data()['iloc']
        res_size = validator.validated_data()['size']
        self.assertTrue(expected_iloc == res_iloc)
        self.assertTrue(expected_size == res_size)


class Test_StandardBasisVectorValidator_Failure(unittest.TestCase):
    def test_noninteger_iloc(self):
        test_iloc = 0.1
        test_size = 2
        # Fail: non-integral iloc
        validator = StandardBasisVectorInitValidator(iloc=test_iloc, size=test_size)
        self.assertFalse(validator.is_valid)

    def test_noninteger_size(self):
        test_iloc = 1
        test_size = 2.5
        # Fail: non-integral size
        validator = StandardBasisVectorInitValidator(iloc=test_iloc, size=test_size)
        self.assertFalse(validator.is_valid)

    def test_size_too_short(self):
        test_iloc = 1
        test_size = 1
        # Fail: size too short.
        validator = StandardBasisVectorInitValidator(iloc=test_iloc, size=test_size)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0].full_message)

    def test_iloc_too_large(self):
        test_iloc = 5
        test_size = 3
        # Fail: iloc and size don't match.
        validator = StandardBasisVectorInitValidator(iloc=test_iloc, size=test_size)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0].full_message)

    def test_iloc_negative(self):
        test_iloc = -1
        test_size = 3
        # Fail: iloc is negative.
        validator = StandardBasisVectorInitValidator(iloc=test_iloc, size=test_size)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0].full_message)


class TestStandardBasisVector(unittest.TestCase):
    def test_initialisation(self):
        test_iloc = 1
        test_size = 5
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertTrue(isinstance(vector, ColumnVector))

    def test_initialisation_failure(self):
        test_iloc = 6
        test_size = 5
        # Error: iloc out of range; in validator.
        self.assertRaises(Validation_Error, StandardBasisVector,
                          test_iloc, test_size)

    def test_as_vector(self):
        test_iloc = 1
        test_size = 5
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertTrue(isinstance(vector.as_array(), np.ndarray))

    def test_iloc(self):
        test_iloc = 4
        test_size = 5
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(test_iloc, vector.iloc)

    def test_iloc2(self):
        test_iloc = 0
        test_size = 5
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(test_iloc, vector.iloc)

    def test_iloc3(self):
        test_iloc = 0
        test_size = 5
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(test_iloc, vector.iloc)

    def test_size1(self):
        test_iloc = 4
        test_size = 5
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(test_size, vector.size)

    def test_size2(self):
        test_iloc = 2
        test_size = 3
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(test_size, vector.size)

    def test_size(self):
        test_iloc = 2
        test_size = 100
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(test_size, vector.size)

    def test_string_representation1(self):
        test_iloc = 0
        test_size = 3
        expected_string = '\n[1.0\n 0.0\n 0.0]\n'
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(expected_string, vector.string_representation())

    def test_string_representation2(self):
        test_iloc = 2
        test_size = 6
        expected_string = '\n[0.0\n 0.0\n 1.0\n 0.0\n 0.0\n 0.0]\n'
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(expected_string, vector.string_representation())

    def test_element(self):
        """ Inherited method """
        test_iloc = 5
        test_size = 6
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(vector.element(index=0), 0)
        self.assertEqual(vector.element(index=1), 0)
        self.assertEqual(vector.el(index=5), vector.last)

    def test_first_last(self):
        """ Inherited method """
        test_iloc = 5
        test_size = 6
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertEqual(vector.el(index=0), vector.first)
        self.assertEqual(vector.first, 0)
        self.assertEqual(vector.last, 1)


class Test_Linear_Object_Subtypes(unittest.TestCase):
    def test_okay(self):
        test_iloc = 5
        test_size = 6
        vector = StandardBasisVector(iloc=test_iloc, size=test_size)
        self.assertTrue(isinstance(vector, Column_Like))
        self.assertFalse(isinstance(vector, Row_Like))
        self.assertFalse(isinstance(vector, Matrix_Like))
