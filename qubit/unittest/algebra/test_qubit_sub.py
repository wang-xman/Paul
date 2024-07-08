#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.algebra.py

Main test:
    Qubit sub function.

Updated:
    26 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector
from quantum_state import NullState
from quantum_state.superposition import QuantumSuperposition
from qubit.qubit import QubitSuperposition
from qubit.qubit import QubitState, ComputationalBasis
from qubit.utils import qubit_from_bitlist
from qubit.algebra import qubit_scale, qubit_sub


class Test_QubitState_StateSubtraction(unittest.TestCase):
    def test_state_state_subtraction(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QubitState(vector=vector)
        state2 = QubitState(vector=vector)
        # this is a superposition,
        # see addition rules of quantum state
        sp3 = qubit_sub(state1, state2)
        self.assertTrue(isinstance(sp3, QubitSuperposition))
        # null state
        self.assertTrue(isinstance(sp3.as_state(), NullState))

    def test_sp_state_subtraction(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QubitState(vector=vector)
        state2 = QubitState(vector=vector)
        # this is a superposition,
        # see addition rules of quantum state
        sp3 = qubit_sub(qubit_scale(3.0, state1), state2)
        self.assertTrue(isinstance(sp3, QubitSuperposition))
        self.assertTrue(sp3.as_state() == state1)

    def test_state_sp_subtraction(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QubitState(vector=vector)
        state2 = QubitState(vector=vector)
        # this is a superposition,
        # see addition rules of quantum state
        sp3 = qubit_sub(state1, qubit_scale(2.0, state2))
        self.assertTrue(isinstance(sp3, QubitSuperposition))
        self.assertTrue(sp3.as_state() == state1)

    def test_state_sp_subtraction_2(self):
        vector1 = ColumnVector(array=np.array([[1.0], [1.0]]))
        vector2 = ColumnVector(array=np.array([[3.0], [4.0]]))
        state1 = QubitState(vector=vector1)
        state2 = QubitState(vector=vector2)
        # this is a superposition,
        # see addition rules of quantum state
        sp3 = qubit_sub(state1, qubit_scale(2.0, state2))
        self.assertTrue(isinstance(sp3, QuantumSuperposition))
        self.assertFalse(sp3.as_state() == state1)
        self.assertFalse(sp3.as_state() == state2)


class Test_CompBasis(unittest.TestCase):
    def test_basis_with_basis(self):
        basis1 = ComputationalBasis(bitstring='1')
        basis2 = ComputationalBasis(bitstring='0')
        newbasis = qubit_sub(basis1, basis2)
        self.assertTrue(isinstance(newbasis, QubitSuperposition))
        self.assertTrue(isinstance(newbasis.as_state(), QubitState))

    def test_basis_with_qubit(self):
        basis = ComputationalBasis(bitstring='1')
        qubit = qubit_from_bitlist([(1.0,'0'),(1.0,'1')])
        sp = qubit_sub(basis, qubit)
        self.assertTrue(isinstance(sp, QubitSuperposition))
        self.assertTrue(isinstance(sp.as_state(), QubitState))
