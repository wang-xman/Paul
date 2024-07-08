#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    density_matrix.density_matrix.py

Main test:
    Density matrix initialization.

Updated:
    26 September 2021
"""
import unittest
import numpy as np

from common import Validation_Error
from linear_space.vector import UnitVector
from quantum_state import QuantumState

from density_matrix.density_matrix import DensityMatrixInitValidator, DensityMatrix

def error_raiser(validator):
    if not validator.is_valid:
        validator.raise_last_error()


class TestDensityMatrix_FromState(unittest.TestCase):
    def test_2by2_real(self):
        vector = UnitVector(array=np.array([[1], [1]]))
        state = QuantumState(vector=vector)
        density_matrix = DensityMatrix(state=state)
        # expected matrix
        expected_array = np.array([[0.5, 0.5],
                                   [0.5, 0.5]])
        self.assertEqual(density_matrix.as_array().all(),
                         expected_array.all())

    def test_3by3_real(self):
        vector = UnitVector(array=np.array([[1], [1], [1]]))
        state = QuantumState(vector=vector)
        density_matrix = DensityMatrix(state=state)
        #print(density_matrix._matrix.as_array())

    def test_2by2_complex(self):
        vector = UnitVector(array=np.array([[1], [1j]]))
        state = QuantumState(vector=vector)
        density_matrix = DensityMatrix(state=state)
        expected_array = np.array([[0.5+0.j, 0. -0.5j],
                                  [0. +0.5j, 0.5+0.j ]])
        self.assertEqual(density_matrix.as_array().all(),
                         expected_array.all())

    def test_4by4_complex(self):
        vector = UnitVector(array=np.array([[1], [1j], [1], [1j]]))
        state = QuantumState(vector=vector)
        density_matrix = DensityMatrix(state=state)
        expected_array = np.array([[0.25, -0.25j, 0.25, -0.25j],
                                   [0.25j, 0.25, 0.25j, 0.25],
                                   [0.25, -0.25j, 0.25, -0.25j],
                                   [0.25j, 0.25, 0.25j, 0.25]])
        self.assertEqual(density_matrix.as_array().all(),
                         expected_array.all())


class TestDensityMatrix_FromEnsemble(unittest.TestCase):
    """ Create density matrix from a list of probability state pairs """

    def test_ensemble_complex_data(self):
        vector1 = UnitVector(array=np.array([[1+0j], [1+0j]]))
        state1 = QuantumState(vector=vector1)
        vector2 = UnitVector(array=np.array([[1], [1j]]))
        state2 = QuantumState(vector=vector2)
        ensemble = [(0.5, state1),(0.5, state2)]
        density_matrix = DensityMatrix(state=ensemble)
        expected_array = np.array([[0.5, 0.25-0.25j],
                                   [0/25+0.25j,0.5]])
        self.assertEqual(density_matrix.as_array().all(), expected_array.all())

    def test_ensemble_mixed_type_data(self):
        vector1 = UnitVector(array=np.array([[1j], [1]]))
        state1 = QuantumState(vector=vector1)
        vector2 = UnitVector(array=np.array([[1], [1j]]))
        state2 = QuantumState(vector=vector2)
        ensemble = [(0.5, state1),(0.5, state2)]
        density_matrix = DensityMatrix(state=ensemble)
        expected_array = np.array([[0.5, 0], [0,0.5]])
        self.assertEqual(density_matrix.as_array().all(), expected_array.all())

    def test_single_item_causes_error(self):
        vector1 = UnitVector(array=np.array([[1j], [1]]))
        state1 = QuantumState(vector=vector1)
        # Error: single item in the ensemble.
        ensemble = [(0.5, state1)]
        validator = DensityMatrixInitValidator(state=ensemble)
        self.assertRaises(Validation_Error, error_raiser, validator)
