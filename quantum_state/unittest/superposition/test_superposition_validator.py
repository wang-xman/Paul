#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    quantum_state.superposition.py

Main test:
    New desgin as per 25/09/2021 allows object in
    superposition to be free of several operators.
    This design is inline with the general overhaul
    to delegate such algebra to helper functions,
    which is a better way to centrally manage such
    computationally expensive operations.

Updated:
    25 September 2021
"""
import unittest
from superposition.superposition import SuperpositionValidator


class ExampleObject:
    """ For test: class implementing required methods """
    def __add__(self, item):
        pass

    def __mul__(self, item):
        pass

    def __eq__(self, item):
        pass

class ExampleObject2:
    """ For test: class implementing required methods """
    def __add__(self, item):
        pass

    def __mul__(self, item):
        pass

    def __eq__(self, item):
        pass


class TestSuperpositionValidator_GenericObject(unittest.TestCase):
    def test_success(self):
        obj1 = ExampleObject()
        obj2 = ExampleObject()
        superlist = [(0.1, obj1), (0.2, obj2)]
        validator = SuperpositionValidator(superlist=superlist)
        vd = validator.validated_data()['superlist']

    def test_emptylist(self):
        superlist = []
        validator = SuperpositionValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        # Error: empty list
        #self.assertRaises(ValidationError, SuperpositionValidator, superlist)

    def test_nonlist(self):
        superlist = ([],)
        validator = SuperpositionValidator(superlist=superlist)
        self.assertFalse(validator.is_valid)
        # Error: non list
        #self.assertRaises(ValidationError, SuperpositionValidator, superlist)

    def test_nontuple_in_list(self):
        obj1 = ExampleObject()
        obj2 = ExampleObject()
        superlist = [[0.1, obj1], (0.2, obj2)]
        validator = SuperpositionValidator(superlist=superlist)
        # Error: non tuple in list
        self.assertFalse(validator.is_valid)
        #self.assertRaises(ValidationError, SuperpositionValidator, superlist)

    def test_tuple_length_problem(self):
        obj1 = ExampleObject()
        obj2 = ExampleObject()
        superlist = [(obj1,), (0.2, obj2)]
        validator = SuperpositionValidator(superlist=superlist)
        # Error: first tuple has only one element
        self.assertFalse(validator.is_valid)
        #self.assertRaises(ValidationError, SuperpositionValidator, superlist)

    def test_tuple_length_problem_2(self):
        obj1 = ExampleObject()
        obj2 = ExampleObject()
        superlist = [(1, obj1), (obj2,)]
        validator = SuperpositionValidator(superlist=superlist)
        # Error: second tuple has only one element
        self.assertFalse(validator.is_valid)
        #self.assertRaises(ValidationError, SuperpositionValidator, superlist)

    def test_nonnumeric_amplitude(self):
        obj1 = ExampleObject()
        obj2 = ExampleObject2()
        superlist = [('a', obj1), (1, obj1,)]
        validator = SuperpositionValidator(superlist=superlist, 
                                           component_type=ExampleObject)
        # Error: first tuple has non-numeric amplitude
        self.assertFalse(validator.is_valid)
        #self.assertRaises(ValidationError, SuperpositionValidator, 
        #                  superlist, ExampleObject)

    def test_nonuniform_component_types(self):
        obj1 = ExampleObject()
        obj2 = ExampleObject2()
        superlist = [(1, obj1), (1, obj2,)]
        validator = SuperpositionValidator(superlist=superlist)
        # Error: objects are of different types
        self.assertFalse(validator.is_valid)
        #self.assertRaises(ValidationError, SuperpositionValidator, superlist)

    def test_mismatched_component_types(self):
        obj1 = ExampleObject()
        obj2 = ExampleObject2()
        superlist = [(1, obj1), (1, obj2,)]
        validator = SuperpositionValidator(superlist=superlist, 
                                           component_type=ExampleObject)
        # Error: objects are of different types
        self.assertFalse(validator.is_valid)
        #self.assertRaises(ValidationError, SuperpositionValidator, 
        #                  superlist, ExampleObject)

    def test_mismatched_component_types_2(self):
        obj1 = ExampleObject()
        obj2 = ExampleObject2()
        superlist = [(1, obj1), (1, obj2,)]
        validator = SuperpositionValidator(superlist=superlist, 
                                           component_type=ExampleObject2)
        # Error: objects are of different types
        self.assertFalse(validator.is_valid)
        #self.assertRaises(ValidationError, SuperpositionValidator, 
        #                  superlist, ExampleObject2)


class ExampleObjectNoOperators:
    """ For test: object without __add__, __mul__, and __eq__ methods """
    pass


class Test_SuperpositionValidator_NoOperators(unittest.TestCase):
    def test_no_operators(self):
        obj1 = ExampleObjectNoOperators()
        superlist = [(0.1, obj1)]
        validator = SuperpositionValidator(
                superlist=superlist, component_type=ExampleObjectNoOperators)
        self.assertTrue(validator.is_valid)
        #self.assertRaises(ValidationError, SuperpositionValidator, superlist)
