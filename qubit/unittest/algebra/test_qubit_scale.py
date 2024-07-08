#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.algebra.py

Main test:
    Qubit scale function.

Updated:
    26 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector
from quantum_state import QuantumState, NullState, NULL_STATE
from qubit.qubit import QubitSuperposition
from qubit.qubit import QubitState, ComputationalBasis
from qubit.algebra import qubit_scale, QubitAlgebraFunctionError


class Test_with_QubitState(unittest.TestCase):
    def test_scale_state(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QubitState(vector=vector)
        factor = 0.5
        # scale into a superposition
        ns = qubit_scale(factor, state1)
        self.assertTrue(isinstance(ns, QubitSuperposition))
        # same vector
        self.assertTrue(ns.as_state().as_vector() == state1.as_vector())

    def test_scale_null_state(self):
        factor = 0.5
        # still null
        ns = qubit_scale(factor, NULL_STATE)
        self.assertTrue(isinstance(ns, NullState))

    def test_factor_zero(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QubitState(vector=vector)
        factor = 0.0
        # scale into null
        ns = qubit_scale(factor, state1)
        self.assertTrue(isinstance(ns, NullState))


class Test_with_CompBasis(unittest.TestCase):
    def test_single_basis(self):
        basis1 = ComputationalBasis(bitstring='1')
        #basis2 = ComputationalBasis(bitstring='0')
        factor = 0.5
        # scale into a superposition
        ns = qubit_scale(factor, basis1)
        self.assertTrue(isinstance(ns, QubitSuperposition))
        # same vector
        self.assertTrue(ns.as_state().as_vector() == basis1.as_vector())

    def test_multi_basis(self):
        basis1 = ComputationalBasis(bitstring='10101')
        #basis2 = ComputationalBasis(bitstring='0')
        factor = 0.5
        # scale into a superposition
        ns = qubit_scale(factor, basis1)
        self.assertTrue(isinstance(ns, QubitSuperposition))
        # same vector
        self.assertTrue(ns.as_state().as_vector() == basis1.as_vector())


class Test_Non_Numeric_Factor(unittest.TestCase):
    def test_non_numeric(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        factor = '1'
        # Error: factor not number
        self.assertRaises(QubitAlgebraFunctionError, qubit_scale, factor, state1)

    def test_non_numeric_1(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QuantumState(vector=vector)
        factor = np.array([[1]]) # scalar like
        # Error: factor not number
        self.assertRaises(QubitAlgebraFunctionError, qubit_scale, factor, state1)


class Test_Non_State(unittest.TestCase):
    def test_non_state(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        factor = 1
        #state_scale(factor, vector)
        # Error: only for state
        self.assertRaises(QubitAlgebraFunctionError, qubit_scale, factor, vector)


class Test_Superposition(unittest.TestCase):
    def test_okay(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state1 = QubitState(vector=vector)
        state2 = QubitState(vector=vector)
        factor = 0.5
        # a superposition
        sp = QubitSuperposition(superlist=[(1.0, state1,), (1.0, state2,)])
        scaled = qubit_scale(factor, sp)
        self.assertTrue(isinstance(scaled, QubitSuperposition))
        self.assertTrue(scaled.as_superlist()[0][0] == 0.5)
        self.assertTrue(scaled.as_superlist()[1][0] == 0.5)
        # still the same state.
        self.assertTrue(scaled.as_state() == state1)
