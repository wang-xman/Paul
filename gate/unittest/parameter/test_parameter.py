#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.base.py

Updated:
    20 April 2021
"""
import unittest
import numpy as np

from qubit import QubitState, ComputationalBasis
from qubit.utils import qubit_from_bitlist

# parameters
from gate.parameter import InputQubitState, QubitIndex


class TestInputQubitStateParameter(unittest.TestCase):
    def test_generic_qubit(self):
        qubit = qubit_from_bitlist([(1.0, '0'), (1.0, '1')])
        iqs = InputQubitState()
        self.assertTrue(iqs.is_valid(qubit))

    def test_basis(self):
        qubit = ComputationalBasis(bitstring='1000')
        iqs = InputQubitState()
        self.assertTrue(iqs.is_valid(qubit))

    def test_with_default_qubit(self):
        qubit = qubit_from_bitlist([(1.0, '0'), (1.0, '1')])
        iqs = InputQubitState(default=qubit)
        self.assertTrue(iqs.is_valid(qubit))
        self.assertTrue(iqs.default_value == qubit)

    def test_with_default_basis(self):
        qubit = ComputationalBasis(bitstring='1000')
        qubit2 = ComputationalBasis(bitstring='1100')
        iqs = InputQubitState(default=qubit)
        self.assertTrue(iqs.is_valid(qubit))
        self.assertTrue(iqs.default_value == qubit)
        self.assertFalse(iqs.default_value == qubit2)


class TestQubitIndexParameter(unittest.TestCase):
    def test_without_max(self):
        qindex = QubitIndex()
        self.assertEqual(qindex.minimum, 0)
        self.assertTrue(qindex.is_valid(0))
        self.assertTrue(qindex.is_valid(3))
        self.assertFalse(qindex.is_valid(-1))

    def test_with_max(self):
        qindex = QubitIndex(maximum=9)
        self.assertEqual(qindex.minimum, 0)
        self.assertEqual(qindex.maximum, 9)
        self.assertTrue(qindex.is_valid(0))
        self.assertTrue(qindex.is_valid(5))
        self.assertTrue(qindex.is_valid(9))
        self.assertFalse(qindex.is_valid(10))
        self.assertFalse(qindex.is_valid(-1))
