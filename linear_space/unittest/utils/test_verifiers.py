#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    linear_space.helper.verifier.py

Main test:
    Verification functions
    NOTE Imported all verifiers from linear object subpack.

Updated:
    23 September 2021
"""
import unittest
import numpy as np
from linear_space.vector.column_vector import ColumnVector
from linear_space.linear_object.utils import is_flat_list_like, is_empty, \
    has_only_number, has_only_integer, has_double_entry


class Test_is_list_like(unittest.TestCase):
    def test_list_1d(self):
        obj = ['a',1, 2]
        res = is_flat_list_like(obj)
        self.assertTrue(res)

    def test_list_2d(self):
        # NO. This is not a flat list.
        obj = [[],[],[]]
        res = is_flat_list_like(obj)
        self.assertFalse(res)

    def test_tuple_1d(self):
        obj = ('a', 1,'b',)
        res = is_flat_list_like(obj)
        self.assertTrue(res)

    def test_array_1d(self):
        obj = np.array([1,2,3])
        res = is_flat_list_like(obj)
        self.assertTrue(res)

    def test_array_2d(self):
        # 2D array is not considered list like
        obj = np.array([[1],[2],[3]])
        res = is_flat_list_like(obj)
        self.assertFalse(res)

class Test_is_empty(unittest.TestCase):
    def test_not_empty_list(self):
        obj = ['a',1, 2]
        res = is_empty(obj)
        self.assertFalse(res)

    def test_not_empty_tuple(self):
        obj = ('a',1, 2,)
        res = is_empty(obj)
        self.assertFalse(res)


class Test_has_only_number(unittest.TestCase):
    def test_list_with_char(self):
        obj = ['a',1, 2]
        res = has_only_number(obj)
        self.assertFalse(res)

    def test_list_with_number_char(self):
        obj = ['11',1, 2]
        res = has_only_number(obj)
        self.assertFalse(res)

    def test_list_with_float(self):
        obj = [0.1, 1, 2]
        res = has_only_number(obj)
        self.assertTrue(res)

    def test_list_with_complex(self):
        obj = [1.j, 1, 2]
        res = has_only_number(obj)
        self.assertTrue(res)

    def test_list_with_integers(self):
        obj = [1, 1, 2]
        res = has_only_number(obj)
        self.assertTrue(res)

    def test_list_with_all(self):
        obj = [1, 0.01, 1e-12, 0.3j]
        res = has_only_number(obj)
        self.assertTrue(res)

    def test_tuple_with_char(self):
        obj = ('a',1, 2,)
        res = has_only_number(obj)
        self.assertFalse(res)

    def test_tuple_with_number_char(self):
        obj = ('11',1, 2,)
        res = has_only_number(obj)
        self.assertFalse(res)

    def test_tuple_with_float(self):
        obj = (0.1, 1, 2,)
        res = has_only_number(obj)
        self.assertTrue(res)

    def test_tuple_with_complex(self):
        obj = (1.j, 1, 2,)
        res = has_only_number(obj)
        self.assertTrue(res)

    def test_tuple_with_integers(self):
        obj = (1, 1, 2)
        res = has_only_number(obj)
        self.assertTrue(res)

    def test_tuple_with_all(self):
        obj = (1, 0.01, 1e-12, 0.3j,)
        res = has_only_number(obj)
        self.assertTrue(res)


class  Test_has_only_integer(unittest.TestCase):   
    def test_list_with_char(self):
        obj = ['a',1, 2]
        res = has_only_integer(obj)
        self.assertFalse(res)

    def test_list_with_number_char(self):
        obj = ['11',1, 2]
        res = has_only_integer(obj)
        self.assertFalse(res)

    def test_list_with_float(self):
        obj = [0.1, 1, 2]
        res = has_only_integer(obj)
        self.assertFalse(res)

    def test_list_with_complex(self):
        obj = [1.j, 1, 2]
        res = has_only_integer(obj)
        self.assertFalse(res)

    def test_list_with_integers(self):
        obj = [1, 1, 2]
        res = has_only_integer(obj)
        self.assertTrue(res)

    def test_tuple_with_char(self):
        obj = ('a',1, 2,)
        res = has_only_integer(obj)
        self.assertFalse(res)

    def test_tuple_with_number_char(self):
        obj = ('11',1, 2,)
        res = has_only_integer(obj)
        self.assertFalse(res)

    def test_tuple_with_float(self):
        obj = (0.1, 1, 2,)
        res = has_only_integer(obj)
        self.assertFalse(res)

    def test_tuple_with_complex(self):
        obj = (1.j, 1, 2,)
        res = has_only_integer(obj)
        self.assertFalse(res)

    def test_tuple_with_integers(self):
        obj = (1, 1, 2,)
        res = has_only_integer(obj)
        self.assertTrue(res)

    def test_vector_with_integers(self):
        # Vector is force converted into complex.
        obj = ColumnVector(array=np.array([[1],[2],[3]]))
        res = has_only_integer(obj)
        self.assertFalse(res)


class Test_has_double_entry(unittest.TestCase):
    def test_list_has_double(self):
        obj = [1,2,2,3,4]
        res = has_double_entry(obj)
        self.assertTrue(res)

    def test_list_has_no_double(self):
        obj = [1,2,3,4]
        res = has_double_entry(obj)
        self.assertFalse(res)

    def test_tuple_has_double(self):
        obj = (1,2,2,3,4,)
        res = has_double_entry(obj)
        self.assertTrue(res)

    def test_tuple_has_no_double(self):
        obj = (1,2,3,4,)
        res = has_double_entry(obj)
        self.assertFalse(res)
