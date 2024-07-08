#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.qubit.py

Main test:
    Qubit superposition

Updated:
    28 April 2021
"""
import unittest
import numpy as np

from linear_space.vector import UnitVector
from quantum_state.quantum_state import QuantumState

from qubit.qubit import QubitState, QubitSuperposition


class Test_as_state(unittest.TestCase):
    def test_as_state(self):
        array = np.array([[1.0], [1.0]])
        vector = UnitVector(array=array)
        state = QuantumState(vector=vector)
        qubit = QubitState(vector=vector)
        superlist = [(1.0, qubit)]
        qsp = QubitSuperposition(superlist=superlist)
        self.assertTrue(qsp.as_state() == qubit)
        self.assertTrue(isinstance(qsp.as_state(), QubitState))
