
#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    quantum_state.algebra.py

Main test:
    State outer product function.

Updated:
    25 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector
from linear_space.matrix import Matrix, SquareMatrix

from quantum_state.quantum_state import QuantumState
from quantum_state.superposition import QuantumSuperposition
from quantum_state.algebra import state_outer, QuantumStateAlgebraFunctionError


class Test_State_State(unittest.TestCase):
    def test_sucess(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j]]))
        s2 = QuantumState(vector=v2)
        outer = state_outer(s1, s2)
        self.assertTrue(isinstance(outer, Matrix))
        self.assertTrue(isinstance(outer, SquareMatrix))
        expected_array = np.array([[0.5, -0.5j],[0.5, -0.5j]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_with_self_sucess(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        outer = state_outer(s1, s1)
        expected_array = np.array([[0.5, 0.5],[0.5, 0.5]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_mimatched_dimension(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j], [1.0]]))
        s2 = QuantumState(vector=v2)
        # Shouldn't be error according to linear algebra.
        outer = state_outer(s1, s2)
        expected_array = np.array([[1., 1.j, 1.0],[1., 1.j, 1.0]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_mimatched_type(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j], [1.0]]))
        s2 = QuantumState(vector=v2)
        # Error: mismatched type
        self.assertRaises(QuantumStateAlgebraFunctionError, state_outer, s1, v2)


class Test_State_QSP(unittest.TestCase):
    def test_sucess(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j]]))
        s2 = QuantumState(vector=v2)
        qsp = QuantumSuperposition(superlist=[(1.0, s2)])
        outer = state_outer(s1, qsp)
        self.assertTrue(isinstance(outer, Matrix))
        self.assertTrue(isinstance(outer, SquareMatrix))
        expected_array = np.array([[0.5, -0.5j],[0.5, -0.5j]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_qsp_state(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j]]))
        s2 = QuantumState(vector=v2)
        qsp = QuantumSuperposition(superlist=[(1.0, s1)])
        outer = state_outer(qsp, s2)
        self.assertTrue(isinstance(outer, Matrix))
        self.assertTrue(isinstance(outer, SquareMatrix))
        expected_array = np.array([[0.5, -0.5j],[0.5, -0.5j]])
        self.assertEqual(outer.as_array().all(), expected_array.all())

    def test_qsp_qsp(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.0], [1.j]]))
        s2 = QuantumState(vector=v2)
        qsp1 = QuantumSuperposition(superlist=[(1.0, s1)])
        qsp2 = QuantumSuperposition(superlist=[(1.0, s2)])
        outer = state_outer(qsp1, qsp2)
        self.assertTrue(isinstance(outer, Matrix))
        self.assertTrue(isinstance(outer, SquareMatrix))
        expected_array = np.array([[0.5, -0.5j],[0.5, -0.5j]])
        self.assertEqual(outer.as_array().all(), expected_array.all())
