#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Gate under test:
    Pauli Z gate

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


test_gate = singles['PauliZ']


class Test_ZeroState(unittest.TestCase):

    def test_with_zero_state(self):
        state = NullState()
        self.assertTrue(test_gate(input_state=state) == NULL_STATE)


class Test_SingleBit(unittest.TestCase):
    def test_on_up_state(self):
        up = SingleQubitBasis(bitstring='0')
        new_state = test_gate(input_state=up)
        self.assertTrue(new_state == up)

    def test_on_down_state(self):
        down = SingleQubitBasis(bitstring='1')
        new_state = test_gate(input_state=down)
        expected = qubit_from_bitlist([(-1.0, '1')])
        self.assertTrue(new_state == expected)


class Test_MultiBit(unittest.TestCase):
    def test_three_bits(self):
        inps = qubit_from_bitlist([(1, '010'), (1, '101')])
        new_state = test_gate(input_state=inps, target_index=1)
        expected = qubit_from_bitlist([(-1.0, '010'), (1, '101')])
        self.assertTrue(new_state == expected)
