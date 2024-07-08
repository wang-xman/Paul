#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Main test:
    Projective measurement on all basis states
"""
import unittest
import numpy as np

from qubit import qubit_from_bitlist
from density_matrix.density_matrix import DensityMatrix
from measurement.projective import projective, projective_all


def complex_equal(c1, c2):
    ret = False
    inf = 1e-13
    if np.linalg.norm(c1 - c2) <= inf:
        ret = True
    return ret


class TestAll_via_DensityMatrix(unittest.TestCase):
    def test_3bits(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=target_state)
        probdict = projective_all(density_matrix)
        #print(probdict)
        self.assertTrue(complex_equal(probdict['000'], 0.5))
        self.assertTrue(complex_equal(probdict['011'], 0.5))

    def test_3bits_4(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011'), 
                                           (1.0, '111'), (1.0, '101')])
        density_matrix = DensityMatrix(state=target_state)
        probdict = projective_all(density_matrix)
        #print(probdict)
        self.assertTrue(complex_equal(probdict['000'], 0.25))
        self.assertTrue(complex_equal(probdict['011'], 0.25))


class TestAll_via_State(unittest.TestCase):
    def test_3bits(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        #density_matrix = DensityMatrix(state=target_state)
        probdict = projective_all(target_state)
        #print(probdict)
        self.assertTrue(complex_equal(probdict['000'], 0.5))
        self.assertTrue(complex_equal(probdict['011'], 0.5))

    def test_3bits_4(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011'), 
                                           (1.0, '111'), (1.0, '101')])
        #density_matrix = DensityMatrix(state=target_state)
        probdict = projective_all(target_state)
        #print(probdict)
        self.assertTrue(complex_equal(probdict['000'], 0.25))
        self.assertTrue(complex_equal(probdict['011'], 0.25))


class TestAll_via_ProjectiveFunction(unittest.TestCase):
    def test_3bits(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        #density_matrix = DensityMatrix(state=target_state)
        probdict = projective(target_state)
        #print(probdict)
        self.assertTrue(complex_equal(probdict['000'], 0.5))
        self.assertTrue(complex_equal(probdict['011'], 0.5))

    def test_3bits_4(self):
        target_state = qubit_from_bitlist([(1.0, '000'), (1.0, '011'), 
                                           (1.0, '111'), (1.0, '101')])
        #density_matrix = DensityMatrix(state=target_state)
        probdict = projective(target_state)
        #print(probdict)
        self.assertTrue(complex_equal(probdict['000'], 0.25))
        self.assertTrue(complex_equal(probdict['011'], 0.25))