#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.enlarge_matrix.controlled.py

Main test:
    Generic validator for multiple-controlled
    multiple-qubit (MCMQ) operator matrix.

Updated:
    17 September 2021
"""
import unittest
import numpy as np
from linear_space.matrix import SquareMatrix
from linear_space.utils import identity_by_bits

from gate.enlarge_matrix.errors import GateMatrixEnlargeError, GateMatrixEnlargeValidationError
from gate.enlarge_matrix.common import GenericGateMatrixEnlargeValidator as Validator


# one-bit identity matrix
one_bit_identity = identity_by_bits(1)

# swap matrix for two bits
swap_matrix = SquareMatrix(array=np.array([
    [1,0,0,0],
    [0,0,1,0],
    [0,1,0,0],
    [0,0,0,1]
]))


def raiser(validator):
    if not validator.is_valid:
        validator.raise_last_error()


class Test_NOQ_Issues(unittest.TestCase):
    def test_noninteger_noq(self):
        noq = 0.5
        validator = Validator(number_of_qubits=noq)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: noq is not integer
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_negative_noq(self):
        noq = -10
        validator = Validator(number_of_qubits=noq)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: noq is less than 1
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_zero_noq(self):
        noq = 0
        validator = Validator(number_of_qubits=noq)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: noq is less than 1
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_string(self):
        noq = '2'
        validator = Validator(number_of_qubits=noq)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: noq is less than 1
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)


class Test_Original_Matrix(unittest.TestCase):
    def test_nonmatrix_1(self):
        noq = 2
        om = 1
        validator = Validator(number_of_qubits=noq, original_matrix=om)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: om is not a matrix
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_nonmatrix_array(self):
        noq = 2
        om = np.array([1,0])
        validator = Validator(number_of_qubits=noq, original_matrix=om)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: om is not a matrix
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_matrix_like_array(self):
        noq = 2
        om = np.array([[1,0], [0,1]])
        validator = Validator(number_of_qubits=noq, original_matrix=om)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: om is not a matrix
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_noq_too_small(self):
        noq = 1
        validator = Validator(number_of_qubits=noq, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: noq too small
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)


class Test_Target_Range(unittest.TestCase):
    def test_non_list(self):
        noq = 2
        tr = (0,2)
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: range not list
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_not_two_elements(self):
        noq = 2
        tr = [2,3,4]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: not a list of two integers
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_only_one_element(self):
        noq = 2
        tr = [2]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: not a list of two integers
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_not_normal_ordered(self):
        noq = 4
        tr = [3,1]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: not a list of two integers
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_higher_range_out_of_order(self):
        noq = 3
        tr = [1,3]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: higher range out of order
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_lower_range_out_of_order(self):
        noq = 3
        tr = [-1,3]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: lower range out of order
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_target_range_incompatible_with_matrix(self):
        noq = 4
        tr = [1,3]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: 3 bits in target range, matrix applies to two.
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)


class Test_Control_List(unittest.TestCase):
    def test_non_list(self):
        noq = 4
        tr = [0,1]
        cl = (0,10)
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control list is not a list
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_list_non_tuples(self):
        noq = 4
        tr = [0,1]
        cl = [0,10]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control list is not a list
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_control_index_out_of_range(self):
        noq = 4
        tr = [0,1]
        cl = [(2,'0'),(4,'1')]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control index out of range
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_control_index_clashes_with_target(self):
        noq = 4
        tr = [0,1]
        cl = [(0,'0'),(2,'1')]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control index is also a target
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_duplicated_control(self):
        noq = 4
        tr = [0,1]
        cl = [(2,'0'),(2,'1')]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control list is not a list
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_incorrect_control_state(self):
        noq = 4
        tr = [0,1]
        cl = [(2,'0'),(3,'2')]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control list is not a list
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_incorrect_control_state_1(self):
        noq = 4
        tr = [0,1]
        cl = [(2,0),(3,'2')]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control list is not a list
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_target_covers_all(self):
        noq = 2
        tr = [0,1]
        cl = [(1,'0')]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control list is not a list
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

    def test_control_tuple_has_more_then_2_elements(self):
        noq = 3
        tr = [0,1]
        cl = [(2,'0',1)]
        validator = Validator(number_of_qubits=noq, target_range=tr,
                              control_list=cl, original_matrix=swap_matrix)
        self.assertFalse(validator.is_valid)
        #raiser(validator)
        # Error: control index out of range
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)

class Test_Control_List_Failure(unittest.TestCase):
    def test_failure(self):
        #print("tested")
        noq = 3
        ci = 2
        tr = [0,2]
        validator = Validator(number_of_qubits=noq, control_list=[(ci, '1',)],
            target_range=tr, original_matrix=swap_matrix)
        # Error: range incompatible with original matrix
        #self.assertRaises(GateMatrixEnlargeError, scmq, number_of_qubits=noq,
        #    control_index=ci, target_range=tr, original_matrix=swap_matrix)
        #self.assertTrue(validator.is_valid)
        self.assertRaises(GateMatrixEnlargeValidationError, raiser, validator)
