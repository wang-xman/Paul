#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    linear_space.vector.base.py

Updated:
    23 September 2021
"""
import unittest
import numpy as np

from linear_space.linear_object.linear_object import LinearObject

from linear_space.vector.validators import BaseVectorInitValidator
from linear_space.vector.base_vector import BaseVector


class TestBaseVectorValidator(unittest.TestCase):
    def test_scalar(self):
        test_array = np.array([[1]])
        validator = BaseVectorInitValidator(array=test_array)
        # Error: a scalar
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_lower_than_2D(self):
        test_array = np.array([2,3,4])
        validator = BaseVectorInitValidator(array=test_array)
        # Error: not 2D, but 1D
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_higher_than_2D(self):
        test_array = np.array([[[1],[2]]])
        validator = BaseVectorInitValidator(array=test_array)
        # Error: not 2D
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_subarray_non_uniform_size(self):
        test_array = np.array([[1e-13, 0.4], [0.5], [0, 1.0j, 0.5+0.5j]])
        validator = BaseVectorInitValidator(array=test_array)
        # Error: subarray not 1D
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_subarray_contains_non_numeric(self):
        test_array = np.array([[[1],1]])
        validator = BaseVectorInitValidator(array=test_array)
        # Error: this is list
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_subarray_contains_string(self):
        test_array = np.array([[1],['2'],[3]])
        validator = BaseVectorInitValidator(array=test_array)
        # Error: this is list
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_matrix_like(self):
        test_array = np.array([[1e-13, 0.4], [0.5, 1e9], [1.0j,0.5j]])
        validator = BaseVectorInitValidator(array=test_array)
        # Error: matrix like
        self.assertFalse(validator.is_valid)


class Test_BaseVectorValidator_Okay(unittest.TestCase):
    def test_okay_row_like(self):
        test_array = np.array([[1e-13, 0.5, 1.0j]])
        validator = BaseVectorInitValidator(array=test_array)
        # okay
        self.assertTrue(validator.is_valid)

    def test_okay_column_like(self):
        test_array = np.array([[1e-13], [0.5], [1.0j]])
        validator = BaseVectorInitValidator(array=test_array)
        # okay
        self.assertTrue(validator.is_valid)


class Test_BaseVector(unittest.TestCase):
    def test_row_base_vector(self):
        test_array = np.array([[1,2,3,4,5]])
        bv = BaseVector(array=test_array)
        self.assertTrue(isinstance(bv, LinearObject))
        self.assertTrue(isinstance(bv, BaseVector))

    def test_column_base_vector(self):
        test_array = np.array([[1],[2],[3],[4]])
        bv = BaseVector(array=test_array)
        self.assertTrue(isinstance(bv, LinearObject))
        self.assertTrue(isinstance(bv, BaseVector))


class SampleNakedVector(BaseVector):
    pass


class SampleFullVector(BaseVector):
    def element(self):
        pass

    @property
    def size(self):
        pass


class TestBaseVectorSubclassing(unittest.TestCase):
    def test_sample_naked(self):
        def init(dump):
            vec = SampleNakedVector()
        # Error: missing methods
        self.assertRaises(Exception, init, None)

    def test_sample_full(self):
        array = np.array([[1,2,3]])
        vec = SampleFullVector(array=array)
        def init(dump):
            vec = SampleFullVector()
        # Error: no array provided
        #self.assertRaises(Exception, init, None)
