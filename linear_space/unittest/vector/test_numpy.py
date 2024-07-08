#!/usr/bin/env python3
#-*- coding:utf-8 -*- 
"""
File under test:
    linear_algebra.vector.py

Updated:
    06 April 2021
"""
import unittest
import numpy as np

from linear_algebra.vector import VectorValidator, StandardBasisVectorValidator, \
    Vector, UnitVector, StandardBasisVector, VectorError
from common.exception import BaseError


class TestNumpyArray(unittest.TestCase):
    """ Numpy array and algebra tests """
    def test_array_dimension(self):
        array = np.array([1.j, 2.0, 3.0])
        """
        print("array.ndim {}".format(array.ndim))
        print("array.size {}".format(array.size))
        print("len on array {}".format(len(array)))
        print("type of array element {}".format(type(array[0])))
        transposed = np.transpose([array])
        print("transposed.ndim {}".format(transposed.ndim))
        print("transposed.size {}".format(transposed.size))
        print("len on transposed {}".format(len(transposed)))
        print("type of element in transposed {}".format(type(transposed[0])))
        print("len of element in transposed {}".format(len(transposed[0])))
        print("tranposed divided by 2 {}".format(transposed / 2.0))
        print("complex conjugate of tranposed {}".format(np.conj(transposed)))
        """

    def test_addition(self):
        a1 = np.array([1.0, 2.0, 3.0])
        v1 = np.transpose([a1])
        a2 = np.array([10., 20.0, 30.0])
        v2 = np.transpose([a2])
        v3 = v1 + v2
        #print(v3)
    
    def test_norm(self):
        a1 = np.array([1.0, 1.0, 1.0, 1.0])
        v1 = np.transpose([a1])
        norm = np.linalg.norm(v1)
        #print("norm is {}".format(norm))
    
    def test_vector_transpose(self):
        a1 = np.array([1.0, 1.0, 1.0, 1.0])
        v1 = np.transpose([a1])
        tv1 = np.transpose(v1)[0]
        #print("type of the tranposed vector {}".format(type(tv1)))
        #print("dimension of the tranposed vector {}".format(tv1.ndim))
        #print("transposed vector is {}".format(tv1)) 
        #print(tv1.dot(v1))
        #print(tv1.dot(a1))
    
    def test_kronecker_with_vector(self):
        a1 = np.array([1.0, 2.0, 3.0])
        v1 = np.transpose([a1])
        a2 = np.array([1., 2.0, 3.0])
        v2 = np.transpose([a2])
        tensor = np.kron(v1, v2)
        #print(tensor)
    
    def test_kronecker_with_matrix(self):
        a1 = np.array([1.0, 2.0, 3.0])
        v1 = np.transpose([a1])
        mat = np.array([[1.0, 2.0], [3,4]])
        tensor = np.kron(v1, mat)
        #print(tensor)
    
    def test_outer_with_vector(self):
        a1 = np.array([1.0, 2.0, 3.0])
        v1 = np.transpose([a1])
        a2 = np.array([1.j, 2.0, 3.0])
        v2 = np.transpose([a2])
        outer = np.outer(v1, np.conj(v2))
        tensor = np.kron(v1, v2)
        tensor_with_row = np.kron(v1, np.transpose(v2)[0])
        #print("outer is {}".format(outer))
        #print("tensor is {}".format(tensor))
        #print("tensor with a row {}".format(tensor_with_row))


class TestNumpyArray_2D(unittest.TestCase):
    def test_matrix_and_vector(self):
        mat = np.array([[1.0, 2.0], [3,4]])
        a1 = np.array([1.0, 2.0])
        v1 = np.transpose([a1])
        vec = mat.dot(v1)
        #print(vec)
    
    def test_matrix_and_matrix(self):
        mat = np.array([[1.0, 2.0], [3,4]])
        mat2 = np.array([[1.0, 2.0, 3], [3,4,5]])
        matnew = mat.dot(mat2)
        #print(matnew)
    
    def test_matrix_addition(self):
        mat = np.array([[1.0, 2.0], [3,4]])
        mat2 = np.array([[1.0, 2.0], [3,4]])
        matnew = mat + mat2
        print(matnew)