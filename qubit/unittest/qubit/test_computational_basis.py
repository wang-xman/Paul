#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.qubit.py

Main test:
    Computational basis state initialisation, indexing,
    superposition, etc.

Updated:
    25 September 2021
"""
import unittest
from common import Validation_Error
from qubit.qubit import ComputationalBasis, SingleQubitBasis


class TestInitialisation(unittest.TestCase):
    def test_init(self):
        bitstring = '001'
        basis = ComputationalBasis(bitstring=bitstring)
        #print(basis)

    def test_init_error(self):
        bitstring = 'a001'
        #basis = ComputationalBasis(bitstring=bitstring)
        self.assertRaises(Validation_Error, ComputationalBasis, bitstring)


class TestBitstring(unittest.TestCase):
    def test_bit_string(self):
        bitstring = '001100'
        basis = ComputationalBasis(bitstring=bitstring)
        self.assertTrue(basis.as_bitstring() == bitstring)
        self.assertTrue(basis.bitstring == bitstring)

    def test_as_list_and_tuple(self):
        bitstring = '001100'
        lst = [0,0,1,1,0,0]
        tup = (0,0,1,1,0,0,)
        basis = ComputationalBasis(bitstring=bitstring)
        self.assertTrue(basis.as_list() == lst)
        self.assertTrue(basis.as_tuple() == tup)


class TestDecompose(unittest.TestCase):
    def test_decomp(self):
        bitstring = '001100'
        basis = ComputationalBasis(bitstring=bitstring)
        basis_tuple = basis.decompose()
        self.assertTrue(isinstance(basis_tuple, tuple))
        self.assertTrue(len(basis_tuple) == len(bitstring))
        self.assertTrue(basis_tuple[0] == SingleQubitBasis(bitstring='0'))
        self.assertTrue(basis_tuple[2] == SingleQubitBasis(bitstring='1'))

    def test_indexing(self):
        bitstring = '001100'
        basis = ComputationalBasis(bitstring=bitstring)
        #basis_tuple = basis.decompose()
        #self.assertTrue(isinstance(basis_tuple, tuple))
        #self.assertTrue(len(basis_tuple) == len(bitstring))
        self.assertTrue(basis[0] == SingleQubitBasis(bitstring='0'))
        self.assertTrue(basis[2] == SingleQubitBasis(bitstring='1'))
        self.assertTrue(basis[3] == SingleQubitBasis(bitstring='1'))

    def test_get_state_at(self):
        bitstring = '001100'
        basis = ComputationalBasis(bitstring=bitstring)
        self.assertTrue(basis[1] == SingleQubitBasis(bitstring='0'))
        self.assertTrue(basis[4] == SingleQubitBasis(bitstring='0'))
        self.assertTrue(basis[5] == SingleQubitBasis(bitstring='0'))
        self.assertTrue(basis[1] == basis.get_state_at(1))
        self.assertTrue(basis[4] == basis.get_state_at(0))
        self.assertTrue(basis[5] == basis.get_state_at(1))


class TestBraket(unittest.TestCase):
    def test_ket(self):
        bitstring = '000'
        basis = ComputationalBasis(bitstring=bitstring)
        #print(basis.as_ket())
        #print(basis.as_bra())
