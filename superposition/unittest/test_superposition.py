#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    superposition.superposition.py

Main test:
    Superposition class

Updated:
    24 September 2021
"""
import unittest

from superposition.superposition import Superposition, SuperpositionError
from superposition.errors import SuperpositionValidationError


class string_type:
    def __init__(self, string):
        self.string = string

    def __add__(self, item):
        return self.string + item

    def __mul__(self, item):
        pass

    def __eq__(self, item):
        ret = False
        if self.string == item:
            ret = True
        else:
            ret = False
        return ret

    def __str__(self):
        return self.string


class StringSuper(Superposition):
    component_type = string_type


class Test_Init(unittest.TestCase):
    def test_nonuniform_component_type(self):
        sl = [(1.0, string_type('ab')), (1.0, 'cd')]
        # Error: components types not the same
        self.assertRaises(SuperpositionValidationError, StringSuper, sl)

    def test_single_member(self):
        sp1 = StringSuper([(1.0, string_type('ab'))])
        sp2 = StringSuper([(1.0, string_type('cd'))])
        self.assertEqual(sp1.as_superlist()[0][1], 'ab')
        self.assertEqual(sp2.as_superlist()[0][1], 'cd')

    def test_multiple_member(self):
        sp = StringSuper([(1.0, string_type('ab')), (1.0, string_type('cd'))])
        self.assertEqual(sp.as_superlist()[1][1], 'cd')
        self.assertEqual(sp.as_superlist()[0][1], 'ab')
        self.assertEqual(sp.as_superlist()[0][0], 1.0)


class TestGetItem(unittest.TestCase):
    def test_out_of_range(self):
        sl = [(1.0, string_type('ab')), (1.0, string_type('cd')), (1.0, string_type('efg'))]
        sp = StringSuper(sl)
        # Error: index out of range
        self.assertRaises(SuperpositionError, sp.__getitem__, 4)
