#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    superposition.superposition.py

Main test:
    Superposition validator test.

Updated:
    24 September 2021
"""
import unittest
from superposition.superposition import SuperpositionValidator


class component_type_for_test:
    pass


class component_type_with_add:
    def __add__(self, item):
        pass


class component_type_with_all:
    def __add__(self, item):
        pass

    def __mul__(self, item):
        pass

    def __eq__(self, item):
        pass


class TestSuperpositionValidator(unittest.TestCase):
    def test_superlist_empty(self):
        superlist = []
        validator = SuperpositionValidator(
                superlist=superlist, component_type=component_type_for_test)
        self.assertFalse(validator.is_valid)


class TestComponentTypeIncorrect(unittest.TestCase):
    def test_1(self):
        obj1 = component_type_for_test()
        obj2 = component_type_for_test()
        superlist = [(1, obj1), (1, obj2)]
        validator = SuperpositionValidator(
                superlist=superlist, component_type=1)
        # Error: object type is not a type or class
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])


class TestInhomogeneousComponentTypes(unittest.TestCase):
    def test_1(self):
        superlist = [(1, 'a'), (1, 2.0)]
        validator = SuperpositionValidator(superlist=superlist)
        # Error: inhomogeneous type
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_2(self):
        obj1 = component_type_for_test()
        superlist = [(1, obj1), (1, 2.0)]
        validator = SuperpositionValidator(
                superlist=superlist, component_type=component_type_for_test)
        # Error: inhomogeneous type
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])


class TestObjectClassProblem(unittest.TestCase):
    def test(self):
        obj1 = component_type_for_test()
        obj2 = component_type_for_test()
        superlist = [(1, obj1), (1, obj2)]
        validator = SuperpositionValidator(
                superlist=superlist, component_type=component_type_for_test)
        # Okay
        self.assertTrue(validator.is_valid)

    def test_has_add(self):
        obj1 = component_type_with_add()
        obj2 = component_type_with_add()
        superlist = [(1, obj1), (1, obj2)]
        validator = SuperpositionValidator(
                superlist=superlist, component_type=component_type_with_add)
        # Okay
        self.assertTrue(validator.is_valid)

    def test_okay(self):
        obj1 = component_type_with_all()
        obj2 = component_type_with_all()
        superlist = [(1, obj1), (1, obj2)]
        validator = SuperpositionValidator(
                superlist=superlist, component_type=component_type_with_all)
        # Okay
        self.assertTrue(validator.is_valid)
