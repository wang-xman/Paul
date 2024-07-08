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
from common import Algebra_Error
from linear_space.vector import ColumnVector, UnitVector
from linear_space.algebra import inner

from quantum_state.null_state import NULL_STATE
from quantum_state.quantum_state import QuantumState
from quantum_state.superposition import QuantumSuperposition
from quantum_state.algebra import state_inner, QuantumStateAlgebraFunctionError


class Test_State_and_State(unittest.TestCase):
    def test_ss(self):
        v1 = UnitVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[0.0], [1.0], [0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        # state inner product
        sip = state_inner(s1, s2)
        # vector inner product
        vip = inner(v1, v2)
        self.assertTrue(sip == vip)

    def test_state_innerproduct_complex(self):
        """ Inner product of two states

        Important notice: Inner product of two states
        involves the complex conjugate of one state
        vector and the vector of the other. The definition
        of state's inner product is therefore different
        from the one for common vectors.
        """
        v1 = UnitVector(array=np.array([[1.0], [1.j]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        # state inner product
        sip = state_inner(s1, s2)
        # vector inner product
        vip = inner(v1, v2)
        self.assertTrue(sip == vip)

    def test_state_innerproduct_complex2(self):
        v1 = ColumnVector(array=np.array([[1.j], [1.j]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[1.j], [1.j]]))
        s2 = QuantumState(vector=v2)
        # unnormalised vectors
        nvip = inner(v1, v2) 
        # Pass auf: Non-unit vector needs to be normalised first.
        vip = inner(v1.normalize(), v2.normalize())
        # state inner prod
        sip = state_inner(s1, s2)
        self.assertTrue(sip == vip)
        self.assertTrue(sip != nvip)

    def test_state_innerproduct_mismatched_dimension(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = ColumnVector(array=np.array([[0.0], [1.0], [0.0]]))
        s2 = QuantumState(vector=v2)
        # Error: error rooted in linear algebra
        self.assertRaises(Algebra_Error, state_inner, s1, s2)

    def test_state_innerproduct_mismatched_types(self):
        v1 = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        s2 = 1.0
        # Error: dimension error
        self.assertRaises(QuantumStateAlgebraFunctionError, state_inner, s1, s2)


class Test_State_and_QSP(unittest.TestCase):
    def test_state_sp(self):
        v1 = UnitVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[0.0], [1.0], [0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        # 
        qsp = QuantumSuperposition(superlist=[(1.0, s1),(1.0, s2)])
        # state inner product
        sip = state_inner(s1, qsp)
        # vector inner product
        vip = inner(v1, qsp.as_state().as_vector())
        self.assertTrue(sip == vip)

    def test_sp_state(self):
        v1 = UnitVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[0.0], [1.0], [0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        # 
        qsp = QuantumSuperposition(superlist=[(1.0, s1),(1.0, s2)])
        # state inner product
        sip = state_inner(qsp, s1)
        # vector inner product
        vip = inner(qsp.as_state().as_vector(), v1)
        self.assertTrue(sip == vip)


class Test_QSP_and_QSP(unittest.TestCase):
    def test_sp_sp(self):
        v1 = UnitVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[0.0], [1.0], [0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        #
        qsp1 = QuantumSuperposition(superlist=[(1.0, s1),(1.0, s2)])
        qsp2 = QuantumSuperposition(superlist=[(2.0, s1),(1.0, s2)])
        # state inner product
        sip = state_inner(qsp1, qsp2)
        # vector inner product
        vip = inner(qsp1.as_state().as_vector(), qsp2.as_state().as_vector())
        self.assertTrue(sip == vip)


class Test_Null(unittest.TestCase):
    def test_state_null(self):
        v1 = UnitVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[0.0], [1.0], [0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        # state inner product
        sip = state_inner(s1, NULL_STATE)
        # vector inner product
        self.assertTrue(sip == 0.0)

    def test_qsp_null(self):
        v1 = UnitVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        s1 = QuantumState(vector=v1)
        v2 = UnitVector(array=np.array([[0.0], [1.0], [0.0], [1.0]]))
        s2 = QuantumState(vector=v2)
        qsp1 = QuantumSuperposition(superlist=[(1.0, s1),(1.0, s2)])
        # state inner product
        sip = state_inner(qsp1, NULL_STATE)
        # vector inner product
        self.assertTrue(sip == 0.0)

    def test_null_null(self):
        sip = state_inner(NULL_STATE, NULL_STATE)
        # vector inner product
        self.assertTrue(sip == 0.0)
