#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.qubit.py

Updated:
    25 September 2021
"""
import unittest
import numpy as np

from common import Validation_Error, Generic_Error
from linear_space.vector import ColumnVector

from qubit.qubit import QubitState
from qubit.utils import qubit_from_bitlist


class TestQubitState_VectorInit(unittest.TestCase):
    def test_single_qubit(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0]]))
        state = QubitState(vector=vector)
        expected_list = [(1.0/np.sqrt(2), '0'), (1.0/np.sqrt(2), '1')]
        self.assertEqual(state.as_bitlist(), expected_list)
        self.assertEqual(state.noq, 1)

    def test_init_with_vector_success(self):
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state = QubitState(vector=vector)
        self.assertEqual(state.number_of_qubits, 2)
        # Pass: note the normalisation incurred in the creation of state.
        expected = [(0.5, '00'),(0.5, '01'),(0.5,'10'),(0.5, '11')]
        self.assertEqual(state.as_bitlist(), expected)
        #print(state.as_bitlist())

    def test_init_with_vector_success_2(self):
        vector = ColumnVector(array=np.array([[1.0], [0.0], [0.0], [0.0]]))
        state = QubitState(vector=vector)
        self.assertEqual(state.number_of_qubits, 2)
        # Pass: note the normalisation incurred in the creation of state.
        expected = [(1.0, '00')]
        self.assertEqual(state.as_bitlist(), expected)
        #print(state.as_bitlist())

    def test_init_with_vector_success_3(self):
        vector = ColumnVector(array=np.array([[1.0], [0.0], [1.0], [0.0]]))
        state = QubitState(vector=vector)
        self.assertEqual(state.number_of_qubits, 2)
        # Pass: note the normalisation incurred in the creation of state.
        expected = [(1.0/np.sqrt(2), '00'), (1.0/np.sqrt(2),'10')]
        self.assertEqual(state.as_bitlist(), expected)
        #print(state.as_bitlist())


class TestQubitState_InitErrors(unittest.TestCase):
    def test_init_failure_wrong_vector_size(self):
        # Fail: incompatible vector size.
        vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0]]))
        self.assertRaises(Validation_Error, QubitState, vector)

    def test_init_failure_wrong_vector_element(self):
        # Fail: incompatible vector size.
        # WARNING: This error is raised by Vector constructor.
        array=np.array([[1.0], [1.0], ['1.0']])
        self.assertRaises(Validation_Error, ColumnVector, array)


class TestQubitState_ZeroAmplitudeRemoval(unittest.TestCase):
    def test_zero_amplitude_removed(self):
        vector = ColumnVector(array=np.array([[1.0], [0.0], [0.0], [1.0], 
                                              [0.0], [0.0], [0.0], [0.0]]))
        state = QubitState(vector=vector)
        expected_list = [(1.0/np.sqrt(2), '000'), (1.0/np.sqrt(2), '011')]
        self.assertEqual(state.as_bitlist(), expected_list)

    def test_zero_amplitude_removed_2(self):
        vector = ColumnVector(array=np.array([[1.0], [0.0], [0.0], [1.0], [0.0], 
                                        [0.0], [1.0], [0.0]]))
        state = QubitState(vector=vector)
        expected_list = [(1.0/np.sqrt(3), '000'), (1.0/np.sqrt(3), '011'), 
                         (1.0/np.sqrt(3), '110')]
        self.assertEqual(state.as_bitlist(), expected_list)


class TestQubitState_Normalisation(unittest.TestCase):
    def test_normalisation(self):
        vector = ColumnVector(array=np.array([[1.0], [0.0], [1.0], [1.0], [0.0],
                                              [0.0], [1.0], [0.0]]))
        state = QubitState(vector=vector)
        self.assertTrue(state.is_normalized)

    def test_normalisation_2(self):
        vector = ColumnVector(array=np.array([[1.0], [0.0], [0.0], [0.0], [0.0],
                                              [0.0], [0.0], [1.0]]))
        state = QubitState(vector=vector)
        normalised_list = [(1.0/np.sqrt(2), '000'), (1.0/np.sqrt(2), '111')]
        # should be normalisd already.
        self.assertTrue(state.is_normalized)
        self.assertEqual(state.as_bitlist(), normalised_list)


class TestUpDown(unittest.TestCase):
    def test_up(self):
        bitlist = [(1.0, '0')]
        qubit = qubit_from_bitlist(bitlist)
        self.assertTrue(qubit.is_up)
        self.assertFalse(qubit.is_down)

    def test_down(self):
        bitlist = [(1.0, '1')]
        qubit = qubit_from_bitlist(bitlist)
        self.assertTrue(qubit.is_down)
        self.assertFalse(qubit.is_up)

    def test_up_multiple_bits(self):
        bitlist = [(1.0, '00')]
        qubit = qubit_from_bitlist(bitlist)
        self.assertFalse(qubit.is_up)
        self.assertFalse(qubit.is_down)

    def test_down_multiple(self):
        bitlist = [(1.0, '01')]
        qubit = qubit_from_bitlist(bitlist)
        self.assertFalse(qubit.is_down)
        self.assertFalse(qubit.is_up)
