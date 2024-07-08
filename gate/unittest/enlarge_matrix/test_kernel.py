#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.enlarge_matrix.controlled_kernel.py

Main test:
    Multiple-controlled multiple-qubit (MCMQ) operator matrix.

Updated:
    12 September 2021
"""
import unittest
import numpy as np

from linear_space.matrix import SquareMatrix
from linear_space.utils import identity_by_bits
from linear_space.matrix import STATE_ZERO_PROJECTION, STATE_ONE_PROJECTION
from linear_space.algebra import matrix_maker

from gate.enlarge_matrix.controlled_kernel import kernel
from gate.enlarge_matrix.controlled_kernel import \
    multiple_controlled_multiple_qubit_operator_matrix as mcmq


# one-bit identity matrix
one_bit_identity = identity_by_bits(1)

# swap matrix for two bits
swap_matrix = SquareMatrix(array=np.array([
    [1,0,0,0],
    [0,0,1,0],
    [0,1,0,0],
    [0,0,0,1]
]))


class Test_Target_Range_at_Front(unittest.TestCase):
    def test_okay(self):
        noq = 4
        tr = [0,1]
        cl = [(2,'1'), (3,'1')]
        new_matrix = mcmq(number_of_qubits=noq, control_list=cl,
            target_range=tr, original_matrix=swap_matrix)
        # expected
        expected = matrix_maker(list_of_matrices=
            [matrix_maker(list_of_matrices=[
                identity_by_bits(2),STATE_ZERO_PROJECTION, STATE_ZERO_PROJECTION],
                          method='tensor'),
            matrix_maker(list_of_matrices=[identity_by_bits(2),
                                           STATE_ZERO_PROJECTION,
                                           STATE_ONE_PROJECTION],
                         method='tensor'),
            matrix_maker(list_of_matrices=[identity_by_bits(2),
                                           STATE_ONE_PROJECTION,
                                           STATE_ZERO_PROJECTION],
                         method='tensor'),
            matrix_maker(list_of_matrices=[swap_matrix,
                                           STATE_ONE_PROJECTION, 
                                           STATE_ONE_PROJECTION],
                         method='tensor')
            ], method='add')
        # compare
        for r in range(0, new_matrix.nrows):
            for l in range(0, new_matrix.ncols):
                self.assertTrue(expected[r][l] == new_matrix[r][l])


class Test_Target_Range_at_End(unittest.TestCase):
    def test_okay(self):
        noq = 4
        tr = [2,3]
        cl = [(0,'1'), (1,'1')]
        new_matrix = mcmq(number_of_qubits=noq, control_list=cl,
            target_range=tr, original_matrix=swap_matrix)
        # expected
        expected = matrix_maker(list_of_matrices=
            [matrix_maker(
            list_of_matrices=[STATE_ZERO_PROJECTION, STATE_ZERO_PROJECTION,
                              identity_by_bits(2)],
            method='tensor'),
            matrix_maker(
            list_of_matrices=[STATE_ZERO_PROJECTION, STATE_ONE_PROJECTION,
                              identity_by_bits(2)],
            method='tensor'),
            matrix_maker(
            list_of_matrices=[STATE_ONE_PROJECTION, STATE_ZERO_PROJECTION,
                              identity_by_bits(2)],
            method='tensor'),
            matrix_maker(
            list_of_matrices=[STATE_ONE_PROJECTION, STATE_ONE_PROJECTION,
                              swap_matrix],
            method='tensor')], method='add')
        # compare
        for r in range(0, new_matrix.nrows):
            for l in range(0, new_matrix.ncols):
                self.assertTrue(expected[r][l] == new_matrix[r][l])


class Test_Target_Range_in_Middle(unittest.TestCase):
    def test_okay(self):
        noq = 4
        tr = [1,2]
        cl = [(0,'1'), (3,'0')]
        new_matrix = kernel(number_of_qubits=noq, control_list=cl,
            target_range=tr, original_matrix=swap_matrix)
        # expected
        expected = matrix_maker(list_of_matrices=
            [matrix_maker(
            list_of_matrices=[STATE_ZERO_PROJECTION, identity_by_bits(2),
                              STATE_ZERO_PROJECTION],
            method='tensor'),
            matrix_maker(
            list_of_matrices=[STATE_ZERO_PROJECTION, identity_by_bits(2),
                              STATE_ONE_PROJECTION],
            method='tensor'),
            matrix_maker(
            list_of_matrices=[STATE_ONE_PROJECTION, identity_by_bits(2),
                              STATE_ONE_PROJECTION],
            method='tensor'),
            matrix_maker(
            list_of_matrices=[STATE_ONE_PROJECTION, swap_matrix,
                              STATE_ZERO_PROJECTION],
            method='tensor')], method='add')
        # compare
        for r in range(0, new_matrix.nrows):
            for l in range(0, new_matrix.ncols):
                self.assertTrue(expected[r][l] == new_matrix[r][l])
