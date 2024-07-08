#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    state.quantum_state.py

Updated:
    27 April 2021
"""
import unittest
import numpy as np

import unittest
import numpy as np

from linear_space.vector import ColumnVector
from linear_space.algebra import kronecker

from quantum_state.null_state import NULL_STATE
from quantum_state.quantum_state import QuantumState
from quantum_state.superposition import QuantumSuperposition
from quantum_state.algebra import state_kronecker, QuantumStateAlgebraFunctionError

class Test_State_State(unittest.TestCase):
    def test_state_state(self):
        # tensor product of two normalised states
        # shall also be a normalised one.
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        s3 = state_kronecker(s1, s2)
        # use unit vectors
        expected_vector = kronecker(v1.normalize(), v2.normalize())
        # this vector must be normalised
        self.assertTrue(expected_vector.is_normalized)
        expected_state = QuantumState(vector=expected_vector)
        # compare vectors
        self.assertTrue(s3.as_vector() == expected_vector)
        # compare states
        self.assertTrue(s3 == expected_state)


class Test_State_QSP(unittest.TestCase):
    def test_tensor(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        qsp = QuantumSuperposition(superlist=[(1.0, s2)])
        s3 = state_kronecker(s1, qsp)
        # use unit vectors
        expected_vector = kronecker(v1.normalize(), v2.normalize())
        # this vector must be normalised
        self.assertTrue(expected_vector.is_normalized)
        expected_state = QuantumState(vector=expected_vector)
        # compare vectors
        self.assertTrue(s3.as_vector() == expected_vector)
        # compare states
        self.assertTrue(s3 == expected_state)


class Test_QSP_QSP(unittest.TestCase):
    def test_qsp_and_qsp(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        qsp1 = QuantumSuperposition(superlist=[(1.0, s1)])
        qsp2 = QuantumSuperposition(superlist=[(1.0, s2)])
        s3 = state_kronecker(qsp1, qsp2)
        # use unit vectors
        expected_vector = kronecker(v1.normalize(), v2.normalize())
        # this vector must be normalised
        self.assertTrue(expected_vector.is_normalized)
        expected_state = QuantumState(vector=expected_vector)
        # compare vectors
        self.assertTrue(s3.as_vector() == expected_vector)
        # compare states
        self.assertTrue(s3 == expected_state)


class Test_State_Null(unittest.TestCase):
    def test_state_null(self):
        # tensor product of two normalised states
        # shall also be a normalised one.
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        s3 = state_kronecker(s1, NULL_STATE)
        self.assertTrue(s3 == NULL_STATE)

    def test_null_and_state(self):
        # tensor product of two normalised states
        # shall also be a normalised one.
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        s3 = state_kronecker(NULL_STATE, s1)
        self.assertTrue(s3 == NULL_STATE)

    def test_null_and_null(self):
        s3 = state_kronecker(NULL_STATE, NULL_STATE)
        self.assertTrue(s3 == NULL_STATE)
