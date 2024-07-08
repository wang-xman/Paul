#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Gate under test:
    Rz gate

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

test_gate = singles['Rz']


class TestRzGate_ZeroState(unittest.TestCase):

    def test_with_zero_state(self):
        state = NullState()
        self.assertTrue(test_gate(input_state=state) == NULL_STATE)


class TestRzGate_DefaultTheta(unittest.TestCase):
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


class TestRzGate_Pi(unittest.TestCase):
    """ Matrix is [[-j 0], [0, j]] """

    def test_phase_up_state(self):
        up = SingleQubitBasis(bitstring='0')
        theta = np.pi
        new_state = test_gate(input_state=up, theta=theta)
        expected = qubit_from_bitlist([(-1.j, '0')])
        self.assertTrue(new_state == expected)

    def test_phase_down_state(self):
        down = SingleQubitBasis(bitstring='1')
        theta = np.pi
        new_state = test_gate(input_state=down, theta=theta)
        expected = qubit_from_bitlist([(1.j, '1')])
        self.assertTrue(new_state == expected)

    def test_three_bits(self):
        inps = qubit_from_bitlist([(1, '010'), (1, '101')])
        theta = np.pi
        new_state = test_gate(input_state=inps, target_index=1, theta=theta)
        expected = qubit_from_bitlist([(1.j, '010'), (-1.j, '101')])
        self.assertTrue(new_state == expected)


class TestRzGate_HalfPi(unittest.TestCase):
    """ Matrix [[exp(-j*pi/4), 0], [0, exp(j*pi/4)]]"""

    theta = 0.5 * np.pi
    exp_qp = np.exp(0.25j * np.pi)
    exp_nqp = np.exp(0.0 - 0.25j * np.pi)

    def test_phase_up_state(self):
        up = SingleQubitBasis(bitstring='0')
        new_state = test_gate(input_state=up, theta=self.theta)
        expected = qubit_from_bitlist([(self.exp_nqp, '0')])
        self.assertTrue(new_state == expected)

    def test_phase_down_state(self):
        down = SingleQubitBasis(bitstring='1')
        new_state = test_gate(input_state=down, theta=self.theta)
        expected = qubit_from_bitlist([(self.exp_qp, '1')])
        self.assertTrue(new_state == expected)

    def test_three_bits(self):
        inps = qubit_from_bitlist([(1, '010')])
        new_state = test_gate(input_state=inps, target_index=1, theta=self.theta)
        expected = qubit_from_bitlist([(self.exp_qp, '010')])
        self.assertTrue(new_state == expected)
