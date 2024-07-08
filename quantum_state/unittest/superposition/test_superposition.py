#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    quantum_state.superposition.py

Updated:
    25 September 2021
"""
import unittest
import numpy as np
from linear_space.vector import ColumnVector
from superposition.errors import SuperlistValidationError
from quantum_state.quantum_state import QuantumState
from quantum_state.superposition import QuantumSuperposition


class Test_QuantumSuperposition_Init(unittest.TestCase):

    def test_success(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        superlist1 = [(0.5, s1), (0.5j, s2)]
        sp1 = QuantumSuperposition(superlist=superlist1)


class Test_QuantumSuperposition_as_state(unittest.TestCase):

    def test_success(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        superlist1 = [(0.5, s1), (0.5j, s2)]
        sp1 = QuantumSuperposition(superlist=superlist1)
        self.assertTrue(sp1.as_state().is_normalized)


class TestQuantumSuperposition_ValidationError(unittest.TestCase):
    def test_wrong_object_type(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        superlist = [(0.5, s1), (0.5j, '01010')]
        #QuantumSuperposition(superlist=superlist)
        self.assertRaises(SuperlistValidationError, QuantumSuperposition, superlist)

    def test_nonuniform_tuple(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        # Error: tuple doesn't have exactly 2 elements
        superlist = [(0.5, s1), (0.5j, s1, 0.5)]
        self.assertRaises(SuperlistValidationError, QuantumSuperposition, superlist)
        #sp1 = QuantumSuperposition(superlist=superlist)

    def test_non_tuple(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        # Error: non-tuple in list
        superlist = [[0.5, s1], (0.5j, s1)]
        self.assertRaises(SuperlistValidationError, QuantumSuperposition, superlist)
        #sp1 = QuantumSuperposition(superlist=superlist)


class Test_States_with_Different_Dims(unittest.TestCase):

    def test_different_dimension(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        superlist1 = [(0.5, s1), (0.5j, s2)]
        #sp1 = QuantumSuperposition(superlist=superlist1)
        # Error: dimensions are different
        self.assertRaises(SuperlistValidationError, QuantumSuperposition, superlist1)
