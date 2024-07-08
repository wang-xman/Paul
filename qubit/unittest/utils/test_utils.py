#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.utils.py

Updated:
    28 April 2021
"""
import unittest
import numpy as np

from common import Validation_Error
from quantum_state import NullState
from qubit.utils import qubit_from_bitlist


""" Create qubit from bitlist """
class Test_qubit_from_bitlist(unittest.TestCase):
    def test_single_component_success(self):
        # For single component, the amplitude doesn't matter.
        bitlist = [(1.0, '00')]
        qubit = qubit_from_bitlist(bitlist)
        expected_array = np.array([[1.0], [0.0], [0.0], [0.0]])
        self.assertTrue(np.array_equal(qubit.as_vector().as_array(),
                                       expected_array))

    def test_single_component_with_zero_amplitude(self):
        # A zero state instance is created.
        bitlist = [(0.0, '00')]
        state = qubit_from_bitlist(bitlist)
        self.assertTrue(isinstance(state, NullState))

    def test_bitlist_success(self):
        bitlist = [(1.0, '00'), (1.0, '01'), (1.0,'10'), (1.0, '11')]
        qubit = qubit_from_bitlist(bitlist)
        expected_array = np.array([[0.5], [0.5], [0.5], [0.5]])
        self.assertTrue(np.array_equal(qubit.as_vector().as_array(),
                                       expected_array))

    def test_bitlist_nonequal_string_length(self):
        comp = [(1.0, '00'), (1.0, '010'), (1.0,'10'), (1.0, '11')]
        # Error: bitstrings have different lengths
        self.assertRaises(Validation_Error, qubit_from_bitlist, comp)

    def test_bitlist_double_entry_1(self):
        bitlist = [(1.0, '00'), (1.0, '01'), (0.5,'10'), (0.5,'10'), (1.0, '11')]
        qubit = qubit_from_bitlist(bitlist)
        expected_array = np.array([[0.5], [0.5], [0.5], [0.5]])
        #print(expected_array)
        self.assertTrue(np.array_equal(qubit.as_vector().as_array(),expected_array))

    def test_bitlist_double_entry_2(self):
        bitlist = [(0.5, '000'),(0.5, '000'), (1.0, '011')]
        state = qubit_from_bitlist(bitlist)
        expected_array = np.array([[1.0/np.sqrt(2)], [0.0], [0.0],
                                   [1.0/np.sqrt(2)], [0.0], [0.0],[0.0], [0.0]])
        self.assertTrue(np.array_equal(state.as_vector().as_array(), 
                                       expected_array))
