#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.algebra.py

Main test:
    Qubit add function.

Updated:
    26 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector
from quantum_state import QuantumState

from qubit.qubit import QubitSuperposition
from qubit.qubit import QubitState, ComputationalBasis
from qubit.utils import qubit_from_bitlist
from qubit.algebra import qubit_scale, qubit_add, QubitAlgebraFunctionError


class TestQubitState_add(unittest.TestCase):

    def test_qubit_addition_equal_weight(self):
        v1 = ColumnVector(array=np.array([[1.0], [0.0]]))
        q1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        q2 = QubitState(vector=v2)
        sp = qubit_add(q1, q2)
        self.assertTrue(isinstance(sp, QubitSuperposition))
        state = sp.as_state()
        self.assertTrue(isinstance(state, QubitState))
        self.assertTrue(state.noq == 1)
        expected_qubit = qubit_from_bitlist([(1.0,'0'),(1.0,'1')])
        self.assertTrue(state == expected_qubit)

    def test_qubit_addition_equal_weight_2(self):
        v1 = ColumnVector(array=np.array([[1.0], [0.0]]))
        q1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        q2 = QubitState(vector=v2)
        # complex weight
        sp = qubit_add(qubit_scale(1.0j, q1), qubit_scale(1.0j, q2))
        self.assertTrue(isinstance(sp, QubitSuperposition))
        state = sp.as_state()
        self.assertTrue(isinstance(state, QubitState))
        self.assertTrue(state.noq == 1)
        expected_qubit = qubit_from_bitlist([(1.0,'0'),(1.0,'1')])
        self.assertTrue(state == expected_qubit)

    def test_qubit_addition_unequal_weight(self):
        v1 = ColumnVector(array=np.array([[1.0], [0.0]]))
        q1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        q2 = QubitState(vector=v2)
        sp = qubit_add(qubit_scale(1.0, q1), qubit_scale(2.0, q2))
        self.assertTrue(isinstance(sp, QubitSuperposition))
        state = sp.as_state()
        self.assertTrue(isinstance(state, QubitState))
        self.assertTrue(state.noq == 1)
        expected_qubit = qubit_from_bitlist([(1.0,'0'),(2.0,'1')])
        self.assertTrue(state == expected_qubit)

    def test_qubit_addition_unequal_weight_2(self):
        v1 = ColumnVector(array=np.array([[1.0], [0.0]]))
        q1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        q2 = QubitState(vector=v2)
        sp = qubit_add(qubit_scale(1.0,q1), qubit_scale(2.j,q2))
        self.assertTrue(isinstance(sp, QubitSuperposition))
        state = sp.as_state()
        self.assertTrue(isinstance(state, QubitState))
        self.assertTrue(state.noq == 1)
        expected_qubit = qubit_from_bitlist([(1.0,'0'),(2.0j,'1')])
        self.assertTrue(state == expected_qubit)

    def test_with_superposition(self):
        v1 = ColumnVector(array=np.array([[1.0], [0.0]]))
        q1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0]]))
        q2 = QubitState(vector=v2)
        self.assertTrue(qubit_scale(2.j,q2), QubitSuperposition)
        sp = qubit_add(q1, qubit_scale(2.j,q2))
        self.assertTrue(isinstance(sp, QubitSuperposition))
        state = sp.as_state()
        self.assertTrue(isinstance(state, QubitState))
        self.assertTrue(state.noq == 1)
        expected_qubit = qubit_from_bitlist([(1.0,'0'),(2.0j,'1')])
        self.assertTrue(state == expected_qubit)

    def test_addition_with_mismatched_dimensions(self):
        v1 = ColumnVector(array=np.array([[1.0], [0.0]]))
        q1 = QubitState(vector=v1)
        #print(q1.noq)
        v2 = ColumnVector(array=np.array([[0.0], [1.0], [0.0], [1.0]]))
        q2 = QubitState(vector=v2)
        # Error: mismatched dimension
        self.assertRaises(QubitAlgebraFunctionError, qubit_add, q1, q2)

    def test_addition_with_quantum_state(self):
        v1 = ColumnVector(array=np.array([[1.0], [0.0]]))
        q1 = QubitState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0], [0.0], [1.0]]))
        q2 = QuantumState(vector=v2)
        # Error: States of different dimension
        self.assertRaises(QubitAlgebraFunctionError, qubit_add, q1, q2)


class TestBasis_add(unittest.TestCase):
    def test_basis_with_basis(self):
        basis1 = ComputationalBasis(bitstring='1')
        basis2 = ComputationalBasis(bitstring='0')
        newbasis = qubit_add(basis1, basis2)
        self.assertTrue(isinstance(newbasis, QubitSuperposition))
        self.assertTrue(isinstance(newbasis.as_state(), QubitState))

    def test_basis_with_qubit(self):
        basis = ComputationalBasis(bitstring='1')
        qubit = qubit_from_bitlist([(1.0,'0'),(1.0,'1')])
        sp = qubit_add(basis, qubit)
        self.assertTrue(isinstance(sp, QubitSuperposition))
        self.assertTrue(isinstance(sp.as_state(), QubitState))
