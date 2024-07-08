#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Gate under test:
    Walsh Hadamard gate

File under test:
    gate.single.py

Updated:
    29 April 2021
"""
import unittest
import numpy as np

from linear_space.vector import UnitVector
from qubit import QubitState, SingleQubitBasis, ComputationalBasis
from gate.base import GateBaseError
from gate import single_qubit_gates as singles


class TestHadamard_SingleQubitBasis(unittest.TestCase):
    gate = singles['Hadamard']

    def test_with_single_basis_up(self):
        up = SingleQubitBasis(bitstring='0')
        #down = SingleQubitBasis(bitstring='1')
        new_state = self.gate(input_state=up)
        exp_state = QubitState(vector=UnitVector(array=np.array([[1], [1]])))
        self.assertTrue(new_state == exp_state)

    def test_with_single_basis_down(self):
        #up = SingleQubitBasis(bitstring='0')
        down = SingleQubitBasis(bitstring='1')
        new_state = self.gate(input_state=down)
        exp_state = QubitState(vector=UnitVector(array=np.array([[1],[-1]])))
        self.assertTrue(new_state == exp_state)


class TestHadamard_Basis(unittest.TestCase):
    gate = singles['Hadamard']

    def test_with_basis_mismatched_bits(self):
        # |010>
        test_state = ComputationalBasis(bitstring='010')
        # Error: no target index.
        self.assertRaises(GateBaseError, self.gate, 
                          **{'input_state': test_state})

    def test_with_basis(self):
        # |010>
        test_state = ComputationalBasis(bitstring='010')
        # apply in index=1 qubit
        new_state = self.gate(input_state=test_state, target_index=1)
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[1],[0],[-1],[0],[0],[0],[0],[0]])
        ))
        self.assertTrue(new_state == exp_state)

    def test_consecutive_applications(self):
        # |010>
        test_state = ComputationalBasis(bitstring='010')
        # apply in index=1 qubit
        s0 = self.gate(input_state=test_state, target_index=0)
        s1 = self.gate(input_state=s0, target_index=1)
        s2 = self.gate(input_state=s1, target_index=2)
        el = np.sqrt(2)/4.0
        nel = 0.0 - np.sqrt(2)/4.0
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[el],[el],[nel],[nel],[el],[el],[nel],[nel]])
        ))
        self.assertTrue(s2 == exp_state)


class TestHadamard_in_Loop(unittest.TestCase):
    gate = singles['Hadamard']

    def test_loop(self):
        # |000>
        test_state = ComputationalBasis(bitstring='000')
        #final = self.gate(input_state=test_state, target_index=0)
        final = test_state
        for index in range(0, test_state.noq):
            final = self.gate(input_state=final, target_index=index)
        # expected
        el = np.sqrt(2)/4.0
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[el], [el], [el], [el], [el], [el], [el], [el]])
        ))
        self.assertTrue(final == exp_state)

    def test_loop_2(self):
        # |010>
        test_state = ComputationalBasis(bitstring='010')
        #final = self.gate(input_state=test_state, target_index=0)
        final = test_state
        for index in range(0, test_state.noq):
            final = self.gate(input_state=final, target_index=index)
        # expected
        el = np.sqrt(2)/4.0
        nel = 0.0 - np.sqrt(2)/4.0
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[el], [el], [nel], [nel], [el], [el], [nel], [nel]])
        ))
        self.assertTrue(final == exp_state)


class TestHadamard_and_FlipGate(unittest.TestCase):
    gate = singles['Hadamard']
    flip = singles['Flip']

    def test_one(self):
        # |010>
        test_state = ComputationalBasis(bitstring='010')
        s0 = self.gate(input_state=test_state, target_index=0)
        s1 = self.flip(input_state=s0, target_index=1)
        s2 = self.gate(input_state=s1, target_index=1)
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[0.5], [0], [0.5], [0], [0.5], [0], [0.5], [0]])
        ))
        self.assertTrue(s2 == exp_state)

    def test_in_loop(self):
        # |111>
        test_state = ComputationalBasis(bitstring='111')
        final = test_state
        for index in range(0, test_state.noq):
            hadamard = self.gate(input_state=final, target_index=index)
            final = self.flip(input_state=hadamard, target_index=index)
        # expected
        el = np.sqrt(2)/4.0
        nel = 0.0 - np.sqrt(2)/4.0
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[nel], [el], [el], [nel], [el], [nel], [nel], [el]])
        ))
        self.assertTrue(final == exp_state)
