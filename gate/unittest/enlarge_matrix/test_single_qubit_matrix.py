#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.enlarge_matrix.noncontrolled.py

Updated:
    13 September 2021
"""
import unittest
import numpy as np
from linear_space.matrix import Matrix, SquareMatrix
from gate.enlarge_matrix.errors import GateMatrixEnlargeValidationError
from gate.enlarge_matrix.noncontrolled import enlarge_single_qubit_matrix


class Test_Enlarge_Single_(unittest.TestCase):
    def test_on_first_bit(self):
        test_matrix = SquareMatrix(array=np.array([[0,1],[1,0]]))
        noq = 3
        index = 0
        new_matrix = enlarge_single_qubit_matrix(
            number_of_qubits=noq, target_index=index,
            original_matrix=test_matrix)
        self.assertTrue(isinstance(new_matrix, SquareMatrix))
        self.assertEqual(new_matrix.size, (8,8))

    def test_on_last_bit(self):
        test_matrix = SquareMatrix(array=np.array([[0,1],[1,0]]))
        noq = 3
        index = 2
        new_matrix = enlarge_single_qubit_matrix(
            number_of_qubits=noq, target_index=index,
            original_matrix=test_matrix)
        self.assertTrue(isinstance(new_matrix, SquareMatrix))
        self.assertEqual(new_matrix.size,(8,8))

    def test_on_middle_bit(self):
        test_matrix = SquareMatrix(array=np.array([[0,1],[1,0]]))
        noq = 3
        index = 1
        new_matrix = enlarge_single_qubit_matrix(
            number_of_qubits=noq, target_index=index,
            original_matrix=test_matrix)
        self.assertTrue(isinstance(new_matrix, SquareMatrix))
        self.assertEqual(new_matrix.size,(8,8))

    def test_target_index_too_large(self):
        test_matrix = SquareMatrix(array=np.array([[0,1],[1,0]]))
        noq = 3
        index = 4
        # Error: index too large
        self.assertRaises(GateMatrixEnlargeValidationError,
                enlarge_single_qubit_matrix, noq, index,test_matrix)

    def test_target_index_too_large_2(self):
        test_matrix = SquareMatrix(array=np.array([[0,1],[1,0]]))
        noq = 2
        index = 2
        # Error: index too large
        self.assertRaises(GateMatrixEnlargeValidationError,
                enlarge_single_qubit_matrix, noq, index,test_matrix)

    def test_target_index_negative(self):
        test_matrix = SquareMatrix(array=np.array([[0,1],[1,0]]))
        noq = 3
        index = -1
        # Error: negative index
        self.assertRaises(GateMatrixEnlargeValidationError,
                enlarge_single_qubit_matrix, noq, index,test_matrix)


class Test_Original_Matrix(unittest.TestCase):
    def test_nonsquare_matrix(self):
        test_matrix = Matrix(array=np.array([[0,1,1],[1,0,1]]))
        noq = 3
        index = 1
        # Error: matrix nonsquare
        self.assertRaises(GateMatrixEnlargeValidationError,
                enlarge_single_qubit_matrix, noq, index,test_matrix)

    def test_non_single_qubit_matrix(self):
        test_matrix = SquareMatrix(array=np.array([[0,1,1],[1,0,1],[1,1,1]]))
        noq = 3
        index = 1
        # Error: matrix is not for single qubit
        self.assertRaises(GateMatrixEnlargeValidationError,
                enlarge_single_qubit_matrix, noq, index,test_matrix)
