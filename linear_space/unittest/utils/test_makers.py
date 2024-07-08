#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    linear_space.utils.maker.py

Main test:
    Object maker functions

Updated:
    23 September 2021
"""
import unittest

from linear_space.matrix.square_matrix import SquareMatrix
from linear_space.utils.errors import LinearSpaceUtilityFunctionError as HelperFunctionError
from linear_space.utils.makers import vector_from_list, vector_from_tuple, \
    vector, unitvector, matrix_from_list, matrix


class Test_vector_from_list(unittest.TestCase):
    def test_sucess(self):
        lst = [1,2,3]
        vector = vector_from_list(lst)

    def test_list_with_char(self):
        lst = [1,2,'3']
        #vector = vector_from_list(lst)
        self.assertRaises(HelperFunctionError, vector_from_list, lst)


class Test_vector_from_tuple(unittest.TestCase):
    def test_sucess(self):
        obj = (1,2,3,)
        vector = vector_from_tuple(obj)

    def test_tuple_with_char(self):
        obj = (1,2,'3',)
        self.assertRaises(HelperFunctionError, vector_from_tuple, obj)


class Test_vector(unittest.TestCase):
    def test_success(self):
        v1 = vector([1,2,3])
        v2 = vector((1,2,3,))
        self.assertTrue(v1 == v2)


class Test_unitvector(unittest.TestCase):
    def test_success(self):
        v1 = unitvector([1,2,3])
        v2 = unitvector((1,2,3,))
        #print(v1.as_array())
        self.assertTrue(v1 == v2)
        self.assertTrue(v1.is_normalized)
        self.assertTrue(v2.is_normalized)


class Test_matrix_from_list(unittest.TestCase):
    def test_one_column(self):
        obj = [[1],[2],[3]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix, obj)
        # This is in fact a vector
        #self.assertEqual(mat.ncols, 1)
        #self.assertEqual(mat.nrows, 3)

    def test_one_row(self):
        obj = [[1,2,3]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix, obj)
        # This is in fact a vector
        #self.assertEqual(mat.ncols, 3)
        #self.assertEqual(mat.nrows, 1)

    def test_nonuniform_length(self):
        obj = [[1],[1,2],[3]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix_from_list, obj)

    def test_nondigits(self):
        obj = [[1],['2'],[3]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix_from_list, obj)

    def test_sublist_contains_list(self):
        obj = [[[1]],[2],[3]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix_from_list, obj)

    def test_empty_sublists(self):
        obj = [[],[],[]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix_from_list, obj)

    def test_success(self):
        obj = [[1,2],[2,1],[3,4]]
        mat = matrix_from_list(obj)

    def test_squarematrix(self):
        obj = [[1,2,1],[2,1,1],[3,4,1]]
        mat = matrix_from_list(obj)
        self.assertTrue(isinstance(mat, SquareMatrix))


class Test_matrix(unittest.TestCase):
    def test_one_column(self):
        obj = [[1],[2],[3]]
        #mat = matrix(obj)
        # This is in fact a column vector
        self.assertRaises(HelperFunctionError, matrix, obj)
        # This is in fact a vector
        #self.assertEqual(mat.ncols, 1)
        #self.assertEqual(mat.nrows, 3)

    def test_one_row(self):
        obj = [[1,2,3]]
        #mat = matrix(obj)
        # This is in fact a row vector
        self.assertRaises(HelperFunctionError, matrix, obj)

        #self.assertEqual(mat.ncols, 3)
        #self.assertEqual(mat.nrows, 1)

    def test_nonuniform_length(self):
        obj = [[1],[1,2],[3]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix, obj)

    def test_nondigits(self):
        obj = [[1],['2'],[3]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix, obj)

    def test_sublist_contains_list(self):
        obj = [[[1]],[2],[3]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix, obj)

    def test_empty_sublists(self):
        obj = [[],[],[]]
        #mat = matrix_from_list(obj)
        self.assertRaises(HelperFunctionError, matrix, obj)

    def test_success(self):
        obj = [[1,2],[2,1],[3,4]]
        mat = matrix(obj)

    def test_squarematrix(self):
        obj = [[1,2,1],[2,1,1],[3,4,1]]
        mat = matrix(obj)
        self.assertTrue(isinstance(mat, SquareMatrix))
