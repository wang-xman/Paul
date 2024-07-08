#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.enlarge_matrix.controlled.py

Main test:
    Single-controlled multiple-qubit (SCMQ) operator matrix.

Updated:
    10 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector, UnitVector
from linear_space.matrix import SquareMatrix
from linear_space.utils import identity_by_bits
from linear_space.algebra import matrix_product, matrix_maker
from linear_space.matrix import STATE_ZERO_PROJECTION, STATE_ONE_PROJECTION

from gate.enlarge_matrix.errors import GateMatrixEnlargeValidationError
from gate.enlarge_matrix.controlled import single_controlled_multiple_qubit as scmq


# one-bit identity matrix
one_bit_identity = identity_by_bits(1)

# swap matrix for two bits
swap_matrix = SquareMatrix(array=np.array([
    [1,0,0,0],
    [0,0,1,0],
    [0,1,0,0],
    [0,0,0,1]
]))


class Test_Parameters(unittest.TestCase):
    def test_pass(self):
        noq = 3
        ci = 2
        tr = [0,1]
        scmq(number_of_qubits=noq, control_index=ci, target_range=tr,
             original_matrix=swap_matrix)

    def test_failure(self):
        noq = 3
        ci = 2
        tr = [0,2]
        #scmq(number_of_qubits=noq, control_index=ci, target_range=tr,
        #     original_matrix=swap_matrix)
        # Error: range incompatible with original matrix
        self.assertRaises(GateMatrixEnlargeValidationError, scmq, number_of_qubits=noq,
            control_index=ci, target_range=tr, original_matrix=swap_matrix)

class Test_3_Bits(unittest.TestCase):
    def test_elementwise_compare(self):
        noq = 3
        ci = 2
        tr = [0,1]
        new_matrix = scmq(number_of_qubits=noq, control_index=ci,
            target_range=tr, original_matrix=swap_matrix)
        # on_hold
        do_nothing_matrix = matrix_maker(
            list_of_matrices=[identity_by_bits(2), STATE_ZERO_PROJECTION],
            method='tensor')
        # apply
        apply_matrix = matrix_maker(
            list_of_matrices=[swap_matrix, STATE_ONE_PROJECTION],
            method='tensor')
        # expected
        expected = matrix_maker(
            list_of_matrices=[do_nothing_matrix, apply_matrix],
            method='add')
        for r in range(0, new_matrix.nrows):
            for l in range(0, new_matrix.ncols):
                self.assertTrue(expected[r][l] == new_matrix[r][l])

    def test_controlled_swap(self):
        noq = 3
        ci = 2
        tr = [0,1]
        op_matrix = scmq(number_of_qubits=noq, control_index=ci,
            target_range=tr, original_matrix=swap_matrix)
        # state |101>    
        old_vector = ColumnVector(array=np.array([
            [0],[0],[0],[0],[0],[1],[0],[0]
        ]))
        # after controlled swap |011>
        new_vector = ColumnVector(array=np.array([
            [0],[0],[0],[1],[0],[0],[0],[0]
        ]))
        result = matrix_product(op_matrix, old_vector)
        self.assertEqual(result, new_vector)

    def test_controlled_swap_non(self):
        noq = 3
        ci = 2
        tr = [0,1]
        op_matrix = scmq(number_of_qubits=noq, control_index=ci,
            target_range=tr, original_matrix=swap_matrix)
        # state |100>
        old_vector = UnitVector(array=np.array([
            [0],[0],[0],[0],[1],[0],[0],[0]
        ]))
        # after controlled swap |110>
        new_vector = UnitVector(array=np.array([
            [0],[0],[0],[0],[1],[0],[0],[0]
        ]))
        result = matrix_product(op_matrix, old_vector)
        for r in range(0, result.nrows):
            self.assertTrue(result[r] == new_vector[r])


class Test_3_Bits_Control_at_Front(unittest.TestCase):
    def test_controlled_swap(self):
        noq = 3
        ci = 0
        tr = [1,2]
        op_matrix = scmq(number_of_qubits=noq, control_index=ci,
            target_range=tr, original_matrix=swap_matrix)
        # state |101>    
        old_vector = ColumnVector(array=np.array([
            [0],[0],[0],[0],[0],[1],[0],[0]
        ]))
        # after controlled swap |110>
        new_vector = ColumnVector(array=np.array([
            [0],[0],[0],[0],[0],[0],[1],[0]
        ]))
        result = matrix_product(op_matrix, old_vector)
        self.assertEqual(result, new_vector)

    def test_controlled_swap_non(self):
        noq = 3
        ci = 0
        tr = [1,2]
        op_matrix = scmq(number_of_qubits=noq, control_index=ci,
            target_range=tr, original_matrix=swap_matrix)
        # state |110>
        old_vector = UnitVector(array=np.array([
            [0],[0],[0],[0],[0],[0],[1],[0]
        ]))
        # after controlled swap |101>
        new_vector = UnitVector(array=np.array([
            [0],[0],[0],[0],[0],[1],[0],[0]
        ]))
        result = matrix_product(op_matrix, old_vector)
        for r in range(0, result.nrows):
            self.assertTrue(result[r] == new_vector[r])
