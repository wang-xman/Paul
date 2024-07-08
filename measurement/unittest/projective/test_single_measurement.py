#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Main test:
    Projective measurement
"""
import unittest
import numpy as np

from linear_space.vector import UnitVector
from qubit import qubit_from_bitlist

from density_matrix.density_matrix import DensityMatrix
from measurement.projective import projective, projective_on_state, \
    projective_on_basis, ProjectiveMeasurementError
from measurement.errors import TargetSystemValidationError


def complex_equal(c1, c2):
    ret = False
    inf = 1e-13
    if np.linalg.norm(c1 - c2) <= inf:
        ret = True
    return ret


class TestProjectiveOnState(unittest.TestCase):
    def test_using_basis(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=target_state)
        state = qubit_from_bitlist([(1.0, '000')])
        prob = projective_on_state(density_matrix, state)
        self.assertTrue(complex_equal(prob, 0.5))

    def test_mismatched_dimension(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=target_state)
        state = qubit_from_bitlist([(1.0, '00')])
        #prob = projective_on_state(density_matrix, state)
        self.assertRaises(ProjectiveMeasurementError, projective_on_state, 
                          density_matrix, state)

    def test_wrong_system(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=target_state)
        state = qubit_from_bitlist([(1.0, '00')])
        vector = UnitVector(array=np.array([[1],[1],[1]]))
        #prob = projective_on_state(vector, state)
        #self.assertRaises(TargetSystemValidationError, projective_on_state,
        #                  vector, state)
        self.assertRaises(ProjectiveMeasurementError, projective_on_state,
                          vector, state)

    def test_using_bell_basis(self):
        target_state = qubit_from_bitlist(
            [(1.0, '00'), (1.0, '01'), (1.0, '10'), (1.0, '11')])
        density_matrix = DensityMatrix(state=target_state)
        state = qubit_from_bitlist([(1.0, '00'),(1.0, '01')])
        prob = projective_on_state(density_matrix, state)
        #print(prob)
        self.assertTrue(complex_equal(prob, 0.5))

    def test_using_bell_basis_2(self):
        target_state = qubit_from_bitlist(
            [(1.0, '00'), (1.0, '01'), (1.0, '10'), (1.0, '11')])
        density_matrix = DensityMatrix(state=target_state)
        state = qubit_from_bitlist([(1.0, '00'), (1.0, '01'), (1.0, '11')])
        prob = projective_on_state(density_matrix, state)
        #print(prob)
        self.assertTrue(complex_equal(prob, 0.75))


class TestProjectiveOnBasis(unittest.TestCase):
    def test_using_basis(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=target_state)
        basis = '000'
        prob = projective_on_basis(density_matrix, basis)
        self.assertTrue(complex_equal(prob, 0.5))
    
    def test_using_basis_2(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=target_state)
        basis = '010'
        prob = projective_on_basis(density_matrix, basis)
        self.assertTrue(complex_equal(prob, 0.0))
    
    def test_using_basis_3(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=target_state)
        basis = '011'
        prob = projective_on_basis(density_matrix, basis)
        self.assertTrue(complex_equal(prob, 0.5))


class TestProjectiveFunction(unittest.TestCase):
    def test_using_state(self):
        target_state = qubit_from_bitlist(
            [(1.0, '00'), (1.0, '01'), (1.0, '10'), (1.0, '11')])
        density_matrix = DensityMatrix(state=target_state)
        state = qubit_from_bitlist([(1.0, '00'), (1.0, '01'), (1.0, '11')])
        prob = projective(density_matrix, state=state)
        #print(prob)
        self.assertTrue(complex_equal(prob, 0.75))

    def test_using_basis(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=target_state)
        basis = '000'
        prob = projective(density_matrix, basis=basis)
        self.assertTrue(complex_equal(prob, 0.5))