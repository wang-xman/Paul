#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.algebra.py

Main test:
    Qubit outer function.

Updated:
    26 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector
from linear_space.matrix import Matrix, SquareMatrix
from quantum_state import QuantumState
from qubit.qubit import QubitSuperposition
from qubit.qubit import QubitState
from qubit.algebra import qubit_outer, QubitAlgebraFunctionError


class Test_State_State(unittest.TestCase):
    def test_sucess(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j]]))
        s2 = QubitState(vector=v2)
        outer = qubit_outer(s1, s2)
        self.assertTrue(isinstance(outer, Matrix))
        self.assertTrue(isinstance(outer, SquareMatrix))
        expected_array = np.array([[0.5, -0.5j],[0.5, -0.5j]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_with_self_sucess(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QubitState(vector=v1)
        outer = qubit_outer(s1, s1)
        expected_array = np.array([[0.5, 0.5],[0.5, 0.5]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_mimatched_dimension(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j], [1.0]]))
        s2 = QuantumState(vector=v2)
        # Shouldn't be error according to linear algebra.
        outer = qubit_outer(s1, s2)
        expected_array = np.array([[1., 1.j, 1.0],[1., 1.j, 1.0]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_mimatched_type(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j], [1.0]]))
        # Error: mismatched type
        self.assertRaises(QubitAlgebraFunctionError, qubit_outer, s1, v2)


class Test_State_QSP(unittest.TestCase):
    def test_sucess(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j]]))
        s2 = QubitState(vector=v2)
        qsp = QubitSuperposition(superlist=[(1.0, s2)])
        outer = qubit_outer(s1, qsp)
        self.assertTrue(isinstance(outer, Matrix))
        self.assertTrue(isinstance(outer, SquareMatrix))
        expected_array = np.array([[0.5, -0.5j],[0.5, -0.5j]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_qsp_state(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j]]))
        s2 = QubitState(vector=v2)
        qsp = QubitSuperposition(superlist=[(1.0, s1)])
        outer = qubit_outer(qsp, s2)
        self.assertTrue(isinstance(outer, Matrix))
        self.assertTrue(isinstance(outer, SquareMatrix))
        expected_array = np.array([[0.5, -0.5j],[0.5, -0.5j]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_qsp_qsp(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j]]))
        s2 = QubitState(vector=v2)
        qsp1 = QubitSuperposition(superlist=[(1.0, s1)])
        qsp2 = QubitSuperposition(superlist=[(1.0, s2)])
        outer = qubit_outer(qsp1, qsp2)
        self.assertTrue(isinstance(outer, Matrix))
        self.assertTrue(isinstance(outer, SquareMatrix))
        expected_array = np.array([[0.5, -0.5j],[0.5, -0.5j]])
        self.assertEqual(outer.as_array().all(), expected_array.all())
