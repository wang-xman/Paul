#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    superposition.superlist.py

Main test:
    Superlist validator

Updated:
    18 April 2021
"""
import unittest
from superposition.validators import SuperlistValidator


class TestSuperlist(unittest.TestCase):
    def test_one_item(self):
        superlist = [(1, 'abc')]
        validator = SuperlistValidator(superlist=superlist)
        self.assertTrue(validator.is_valid)

    def test_not_a_list(self):
        superlist = ((),())
        validator = SuperlistValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0].message)

    def test_nontuple_element(self):
        superlist = [[1,2],(1,2)]
        validator = SuperlistValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0].message)

    def test_empty_tuple_1(self):
        superlist = [(1,2),()]
        validator = SuperlistValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        # Error: empty tuple
        #print(validator.report_errors()[0].message)

    def test_empty_tuple_2(self):
        superlist = [(),(1,2)]
        validator = SuperlistValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        # Error: empty tuple
        #print(validator.report_errors()[0].message)

    def test_empty_tuple_3(self):
        superlist = [(),()]
        validator = SuperlistValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        # Error: empty tuple
        #print(validator.report_errors()[0].message)


class TestSuperlist_EmptyList(unittest.TestCase):
    def test_empty_list(self):
        superlist = []
        validator = SuperlistValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0].message)


class TestSuperlist_NonNumericAmplitude(unittest.TestCase):
    def test_has_nondigital_amp(self):
        superlist = [('a', 'ab'), (1,'cd')]
        validator = SuperlistValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0].message)


class TestSuccess(unittest.TestCase):
    def test_1(self):
        superlist = [(2, 'ab'), (1,'cd')]
        validator = SuperlistValidator(superlist=superlist)
        self.assertTrue(validator.is_valid)

    def test_2(self):
        superlist = [(2j, 1), (1e-13, 'cd')]
        validator = SuperlistValidator(superlist=superlist)
        self.assertTrue(validator.is_valid)
