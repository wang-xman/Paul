#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.algebra.py

Main test:
    Qubit kronecker function.

Updated:
    26 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector
from quantum_state import QuantumState, NULL_STATE
from qubit.qubit import QubitSuperposition, ComputationalBasis
from qubit.utils import qubit_from_bitlist
from qubit.algebra import qubit_kronecker, QubitAlgebraFunctionError


class Test_QubitState(unittest.TestCase):
    def test_with_qubit(self):
        bitlist = [(1.0, '0'), (1.0,'1')]
        q1 = qubit_from_bitlist(bitlist)
        q2 = qubit_from_bitlist(bitlist)
        # relative value of amplitude matters.
        newbitlist = [(10., '00'), (10.0,'01'), (10.0,'10'), (10.0,'11')]
        expected = qubit_from_bitlist(newbitlist)
        #print(expected.as_vector().as_array())
        qubit = qubit_kronecker(q1, q2)
        self.assertTrue(expected == qubit)

    def test_with_basis(self):
        bitlist = [(1.0, '0'), (1.0,'1')]
        q1 = qubit_from_bitlist(bitlist)
        basis = ComputationalBasis(bitstring='00')
        newq = qubit_kronecker(q1, basis)
        # expected
        explist = [(1.0, '000'), (1.0,'100')]
        expqubit = qubit_from_bitlist(explist)
        self.assertTrue(newq == expqubit)

    def test_with_superposition(self):
        l1 = [(1.0,'0')]
        q1 = qubit_from_bitlist(l1)
        l2 = [(1.0,'1')]
        q2 = qubit_from_bitlist(l2)
        superlist = [(1, q1), (2, q2)]
        # the superposition
        sp = QubitSuperposition(superlist=superlist)
        # the qubit
        bitlist = [(1.0, '0'), (1.0,'1')]
        qubit = qubit_from_bitlist(bitlist)
        newstate = qubit_kronecker(qubit, sp)
        expected_list = [(1.0/np.sqrt(10.0), '00'), (2.0/np.sqrt(10.0), '01'),
                         (1.0/np.sqrt(10.0), '10'), (2.0/np.sqrt(10.0), '11')]
        expected_state = qubit_from_bitlist(expected_list)
        self.assertTrue(newstate == expected_state)

    def test_with_superposition_single(self):
        l1 = [(1.0,'0')]
        q1 = qubit_from_bitlist(l1)
        #l2 = [(1.0,'1')]
        #q2 = qubit_from_bitlist(l2)
        superlist = [(1, q1)]
        # the superposition
        sp = QubitSuperposition(superlist=superlist)
        # the qubit
        bitlist = [(1.0, '0'), (1.0,'1')]
        qubit = qubit_from_bitlist(bitlist)
        newstate = qubit_kronecker(qubit, sp)
        expected_list = [(1.0/np.sqrt(2.0), '00'), (1.0/np.sqrt(2.0), '10'), 
                         (0., '11'), (0., '01'),]
        expected_state = qubit_from_bitlist(expected_list)
        self.assertTrue(newstate == expected_state)

    def test_with_zero_state(self):
        bitlist = [(1.0, '0'), (1.0,'1')]
        qubit = qubit_from_bitlist(bitlist)
        newstate = qubit_kronecker(qubit, NULL_STATE)
        self.assertTrue(newstate is NULL_STATE)

    def test_with_quantum_state(self):
        bitlist = [(1.0, '00'), (1.0,'10')]
        qubit = qubit_from_bitlist(bitlist)
        state = QuantumState(vector=ColumnVector(array=np.array([[1],[1],[1]])))
        ns = qubit_kronecker(qubit, state)
        # should be a quantum state
        self.assertTrue(isinstance(ns, QuantumState))
        # dimension is 12
        self.assertTrue(ns.dim == 12)
        self.assertTrue(np.abs(ns[7]-1.0/np.sqrt(6)) < 1e-15)

    def test_trigger_error(self):
        bitlist = [(1.0, '00'), (1.0,'10'), (1.0, '11')]
        qubit = qubit_from_bitlist(bitlist)
        test_array = np.array([[1],[1],[1]])
        vector = ColumnVector(array=test_array)
        # Error comes from vector
        self.assertRaises(QubitAlgebraFunctionError, qubit_kronecker, qubit, vector)


class Test_QubitState_with_CompBasis(unittest.TestCase):
    def test_with_basis_1(self):
        bitlist = [(1.0, '0'), (1.0,'1')]
        q1 = qubit_from_bitlist(bitlist)
        basis = ComputationalBasis(bitstring='00')
        newq = qubit_kronecker(basis, q1)
        # expected
        explist = [(1.0, '000'), (1.0,'001')]
        expqubit = qubit_from_bitlist(explist)
        self.assertTrue(newq == expqubit)

    def test_with_basis_2(self):
        bitlist = [(1.0, '0'), (10.0,'1')]
        q1 = qubit_from_bitlist(bitlist)
        basis = ComputationalBasis(bitstring='000')
        newq = qubit_kronecker(basis, q1)
        # expected
        explist = [(1.0, '0000'), (10.0,'0001')]
        expqubit = qubit_from_bitlist(explist)
        self.assertTrue(newq == expqubit)

    def test_with_basis_3(self):
        bitlist = [(1.0, '0'), (100000.0,'0')]
        # q1 is just '0' state.
        q1 = qubit_from_bitlist(bitlist)
        basis = ComputationalBasis(bitstring='000')
        newq = qubit_kronecker(basis, q1)
        # expected
        explist = [(1.0, '0000')]
        expqubit = qubit_from_bitlist(explist)
        self.assertTrue(newq == expqubit)

    def test_with_zero_state(self):
        bitlist = [(1.0, '0'), (1.0,'1')]
        qubit = qubit_from_bitlist(bitlist)
        newstate = qubit_kronecker(NULL_STATE, qubit)
        self.assertTrue(newstate is NULL_STATE)

    def test_with_quantum_state(self):
        bitlist = [(1.0, '00'), (1.0,'10')]
        qubit = qubit_from_bitlist(bitlist)
        state = QuantumState(vector=ColumnVector(array=np.array([[1],[1],[1]])))
        ns = qubit_kronecker(state, qubit)
        # should be a quantum state
        self.assertTrue(isinstance(ns, QuantumState))
        # dimension is 12
        self.assertTrue(ns.dim == 12)
        self.assertTrue(np.abs(ns[2]-1.0/np.sqrt(6)) < 1e-15)
        self.assertTrue(np.abs(ns[6]-1.0/np.sqrt(6)) < 1e-15)

    def test_with_superposition(self):
        l1 = [(1.0,'0')]
        q1 = qubit_from_bitlist(l1)
        l2 = [(1.0,'1')]
        q2 = qubit_from_bitlist(l2)
        superlist = [(1, q1), (2, q2)]
        # the superposition
        sp = QubitSuperposition(superlist=superlist)
        # the qubit
        bitlist = [(1.0, '0'), (1.0,'1')]
        qubit = qubit_from_bitlist(bitlist)
        newstate = qubit_kronecker(sp, qubit)
        #print(type(newstate))
        expected_list = [(1.0/np.sqrt(10.0), '00'), (1.0/np.sqrt(10.0), '01'),
                         (2.0/np.sqrt(10.0), '10'), (2.0/np.sqrt(10.0), '11')]
        expected_state = qubit_from_bitlist(expected_list)
        self.assertTrue(newstate == expected_state)

    def test_with_superposition_single(self):
        l1 = [(1.0,'0')]
        q1 = qubit_from_bitlist(l1)
        superlist = [(1, q1)]
        # the superposition
        sp = QubitSuperposition(superlist=superlist)
        # the qubit
        bitlist = [(1.0, '0'), (1.0,'1')]
        qubit = qubit_from_bitlist(bitlist)
        newstate = qubit_kronecker(sp, qubit)
        expected_list = [(1.0/np.sqrt(2.0), '00'), (1.0/np.sqrt(2.0), '01'), 
                         (0., '10'), (0., '11'),]
        expected_state = qubit_from_bitlist(expected_list)
        self.assertTrue(newstate == expected_state)
