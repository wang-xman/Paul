#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Gate under test:
    Rx gate

File under test:
    gate.single.py

Updated:
    23 July 2021
"""
import unittest
import numpy as np

from quantum_state import NULL_STATE, NullState
from qubit import SingleQubitBasis
from qubit.utils import qubit_from_bitlist

from gate import single_qubit_gates as singles

test_gate = singles['Rx']


class TestRxGate_ZeroState(unittest.TestCase):

    def test_with_zero_state(self):
        state = NullState()
        self.assertTrue(test_gate(input_state=state) == NULL_STATE)


class TestRxGate_DefaultTheta(unittest.TestCase):
    def test_phase_up_state(self):
        up = SingleQubitBasis(bitstring='0')
        new_state = test_gate(input_state=up)
        self.assertTrue(new_state == up)

    def test_phase_down_state(self):
        down = SingleQubitBasis(bitstring='1')
        new_state = test_gate(input_state=down)
        self.assertTrue(new_state == down)

    def test_three_bits(self):
        inps = qubit_from_bitlist([(1, '010'), (1, '101')])
        new_state = test_gate(input_state=inps, target_index=1)
        self.assertTrue(new_state == inps)


class TestRxGate_Pi(unittest.TestCase):
    def test_phase_up_state(self):
        up = SingleQubitBasis(bitstring='0')
        theta = np.pi
        # matrix is [[0 -j], [-j 0]]
        new_state = test_gate(input_state=up, theta=theta)
        expected = qubit_from_bitlist([(-1.j, '1')])
        self.assertTrue(new_state == expected)

    def test_phase_down_state(self):
        down = SingleQubitBasis(bitstring='1')
        theta = np.pi
        new_state = test_gate(input_state=down, theta=theta)
        expected = qubit_from_bitlist([(-1.j, '0')])
        self.assertTrue(new_state == expected)

    def test_three_bits(self):
        inps = qubit_from_bitlist([(1, '010'), (1, '101')])
        theta = np.pi
        new_state = test_gate(input_state=inps, target_index=1, theta=theta)
        expected = qubit_from_bitlist([(-1.j, '000'), (-1.j, '111')])
        self.assertTrue(new_state == expected)


class TestRxGate_HalfPi(unittest.TestCase):
    theta = 0.5 * np.pi
    cos_qp = np.cos(0.25 * np.pi) # cosine quarter pi
    sin_qp = np.sin(0.25 * np.pi) # sine quarter pi

    def test_phase_up_state(self):
        up = SingleQubitBasis(bitstring='0')
        new_state = test_gate(input_state=up, theta=self.theta)
        expected = qubit_from_bitlist([(self.cos_qp, '0'),
                                       (-1.j * self.sin_qp, '1')])
        self.assertTrue(new_state == expected)

    def test_phase_down_state(self):
        down = SingleQubitBasis(bitstring='1')
        new_state = test_gate(input_state=down, theta=self.theta)
        expected = qubit_from_bitlist([(self.cos_qp, '1'),
                                       (-1.j * self.sin_qp, '0')])
        self.assertTrue(new_state == expected)

    def test_three_bits(self):
        inps = qubit_from_bitlist([(1, '010')])
        new_state = test_gate(input_state=inps, target_index=1, theta=self.theta)
        expected = qubit_from_bitlist([(self.cos_qp, '010'),
                                       (-1.j * self.sin_qp, '000')])
        self.assertTrue(new_state == expected)
