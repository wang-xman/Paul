#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.enlarge_matrix.noncontrolled.py

Main test:
    Enlarge a multiple-qubit gate matrix.
    No controls involved.

Updated:
    10 September 2021
"""
import unittest
import numpy as np

from linear_space.matrix import SquareMatrix
from linear_space.utils import identity_by_bits
from linear_space.algebra import matrix_maker

from gate.enlarge_matrix.errors import GateMatrixEnlargeValidationError
from gate.enlarge_matrix.noncontrolled import enlarge_multiple_qubit_matrix

# one-bit identity matrix
one_bit_identity = identity_by_bits(1)

# swap matrix for two bits
swap_matrix = SquareMatrix(array=np.array([
    [1,0,0,0],
    [0,0,1,0],
    [0,1,0,0],
    [0,0,0,1]
]))

single_matrix = SquareMatrix(array=np.array([
    [0,1], [1,0]
]))


class Test_Validation_Failure(unittest.TestCase):
    def test_invalid_target_range(self):
        noq = 3
        target_range = [0,7]
        #new_matrix = enlarge_multiple_qubit_matrix(
        #    number_of_qubits=noq, target_range=target_range,
        #    original_matrix=swap_matrix)
        # Error: original matrix is incompatible with single-qubit
        self.assertRaises(GateMatrixEnlargeValidationError,
            enlarge_multiple_qubit_matrix,
            number_of_qubits=noq, target_range=target_range,
            original_matrix=swap_matrix)

    def test_negative_number_in_target_range(self):
        noq = 3
        target_range = [-2,2]
        #new_matrix = enlarge_multiple_qubit_matrix(
        #    number_of_qubits=noq, target_range=target_range,
        #    original_matrix=swap_matrix)
        # Error: original matrix is incompatible with single-qubit
        self.assertRaises(GateMatrixEnlargeValidationError,
            enlarge_multiple_qubit_matrix,
            number_of_qubits=noq, target_range=target_range,
            original_matrix=swap_matrix)


class Test_3_Bits(unittest.TestCase):
    def test_fail_to_apply_on_1_bit(self):
        noq = 3
        target_range = [1,1]
        # Error: original matrix is incompatible with single-qubit
        self.assertRaises(GateMatrixEnlargeValidationError,
            enlarge_multiple_qubit_matrix,
            number_of_qubits=noq, target_range=target_range,
            original_matrix=swap_matrix)

    def test_on_last_two_bit(self):
        noq = 3
        target_range = [1,2]
        expected = matrix_maker(
            list_of_matrices=[one_bit_identity, swap_matrix],
            method='tensor')
        new_matrix = enlarge_multiple_qubit_matrix(
            number_of_qubits=noq, target_range=target_range,
            original_matrix=swap_matrix)
        self.assertTrue(isinstance(new_matrix, SquareMatrix))
        for r in range(0, new_matrix.nrows):
            for l in range(0, new_matrix.ncols):
                self.assertTrue(expected[r][l] == new_matrix[r][l])

    def test_on_first_two_bit(self):
        noq = 3
        target_range = [0,1]
        expected = matrix_maker(
            list_of_matrices=[swap_matrix, one_bit_identity],
            method='tensor')
        new_matrix = enlarge_multiple_qubit_matrix(
            number_of_qubits=noq, target_range=target_range,
            original_matrix=swap_matrix)
        self.assertTrue(isinstance(new_matrix, SquareMatrix))
        for r in range(0, new_matrix.nrows):
            for l in range(0, new_matrix.ncols):
                self.assertTrue(expected[r][l] == new_matrix[r][l])


class Test_4_Bits(unittest.TestCase):
    def test_on_middle_two_bit(self):
        noq = 4
        target_range = [1,2]
        expected = matrix_maker(
            list_of_matrices=[one_bit_identity, swap_matrix, one_bit_identity],
            method='tensor')
        new_matrix = enlarge_multiple_qubit_matrix(
            number_of_qubits=noq, target_range=target_range,
            original_matrix=swap_matrix)
        self.assertTrue(isinstance(new_matrix, SquareMatrix))
        for r in range(0, new_matrix.nrows):
            for l in range(0, new_matrix.ncols):
                self.assertTrue(expected[r][l] == new_matrix[r][l])


class Test_One_Bits(unittest.TestCase):
    def test_incompatible_matrix(self):
        noq = 3
        target_range = [0,0]
        self.assertRaises(GateMatrixEnlargeValidationError,
            enlarge_multiple_qubit_matrix,
            number_of_qubits=noq, target_range=target_range,
            original_matrix=swap_matrix)

    def test_incompatible_matrix_2(self):
        noq = 3
        target_range = [0,1]
        #new_matrix = enlarge_multiple_qubit_matrix(
        #    number_of_qubits=noq, target_range=target_range,
        #    original_matrix=single_matrix)
        # Error: noq in range is incompatible with original matrix
        self.assertRaises(GateMatrixEnlargeValidationError,
            enlarge_multiple_qubit_matrix,
            number_of_qubits=noq, target_range=target_range,
            original_matrix=single_matrix)

    def test_single_qubit_matrix(self):
        noq = 3
        target_range = [1,1]
        expected = matrix_maker(
            list_of_matrices=[one_bit_identity, single_matrix, one_bit_identity],
            method='tensor')
        # can be used for a single-bit
        new_matrix = enlarge_multiple_qubit_matrix(
            number_of_qubits=noq, target_range=target_range,
            original_matrix=single_matrix)
        self.assertTrue(isinstance(new_matrix, SquareMatrix))
        for r in range(0, new_matrix.nrows):
            for l in range(0, new_matrix.ncols):
                self.assertTrue(expected[r][l] == new_matrix[r][l])
