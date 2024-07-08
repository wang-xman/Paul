#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Main test:
    Manually perform partial trace without using partial trace function.
"""
import unittest
import numpy as np

from linear_space.algebra import matrix_product, matrix_add, \
    kronecker
from linear_space.utils import identity_by_bits
from qubit import ComputationalBasis, qubit_from_bitlist
from density_matrix.density_matrix import DensityMatrix


def complex_equal(c1, c2):
    ret = False
    inf = 1e-15
    if np.linalg.norm(c1 - c2) <= inf:
        ret = True
    return ret


class TestPartialTrace(unittest.TestCase):
    def test_tracing_out_first_bit(self):
        """ Trace out one bit from a computational basis """
        state = ComputationalBasis(bitstring='010')
        state_zero = ComputationalBasis(bitstring='0')
        density_matrix = DensityMatrix(state=state)
        #idm = IdentityMatrix(row_size=4)
        idm = identity_by_bits(2)
        left_matrix = kronecker(state_zero.as_bra().as_vector(),idm)
        right_matrix = kronecker(state_zero.as_vector(), idm)
        final = matrix_product(left_matrix,
                               matrix_product(density_matrix, right_matrix))
        expect = np.array([[0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0]])
        self.assertTrue(np.array_equal(final.as_array(), expect))
        #print(final.as_array())

    def test_tracing_out_last_bit(self):
        state = ComputationalBasis(bitstring='010')
        state_zero = ComputationalBasis(bitstring='0')
        density_matrix = DensityMatrix(state=state)
        #idm = IdentityMatrix(row_size=4)
        idm = identity_by_bits(2)
        left_matrix = kronecker(idm, state_zero.as_bra().as_vector())
        right_matrix = kronecker(idm, state_zero.as_vector())
        final = matrix_product(left_matrix,
                               matrix_product(density_matrix, right_matrix))
        expect = np.array([[0.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0]])
        self.assertTrue(np.array_equal(final.as_array(), expect))
        #print(final.as_array())

    def test_tracing_out_middle_bit(self):
        state = ComputationalBasis(bitstring='010')
        state_zero = ComputationalBasis(bitstring='0')
        state_one = ComputationalBasis(bitstring='1')
        density_matrix = DensityMatrix(state=state)
        #idm = IdentityMatrix(row_size=4)
        # tracing out state 0
        idm_1bit = identity_by_bits(1)
        left_matrix_zero = kronecker(idm_1bit,
                kronecker(state_zero.as_bra().as_vector(), idm_1bit))
        right_matrix_zero = kronecker(idm_1bit,
                kronecker(state_zero.as_vector(), idm_1bit))
        final_zero = matrix_product(left_matrix_zero,
                matrix_product(density_matrix, right_matrix_zero))
        # tracing out state 1
        left_matrix_one = kronecker(idm_1bit,
                kronecker(state_one.as_bra().as_vector(), idm_1bit))
        right_matrix_one = kronecker(idm_1bit,
                kronecker(state_one.as_vector(), idm_1bit))
        final_one = matrix_product(left_matrix_one,
                matrix_product(density_matrix, right_matrix_one))
        final = matrix_add(final_zero, final_one)
        expect = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0]])
        self.assertTrue(np.array_equal(final.as_array(), expect))


class TestPartialTrace_Superposition(unittest.TestCase):
    def test_tracing_out_first_bit(self):
        # Tracing out the third bit
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=state)
        s0 = ComputationalBasis(bitstring='0')
        s1 = ComputationalBasis(bitstring='1')
        #idm = IdentityMatrix(row_size=4)
        idm = identity_by_bits(2)
        # tracing out the third bit
        lm0 = kronecker(s0.as_bra().as_vector(), idm)
        rm0 = kronecker(s0.as_vector(), idm)
        lm1 = kronecker(s1.as_bra().as_vector(), idm)
        rm1 = kronecker(s1.as_vector(), idm)
        # tracing out 0 and 1
        final = matrix_add(
                matrix_product(lm0, matrix_product(density_matrix, rm0)),
                matrix_product(lm1, matrix_product(density_matrix, rm1)))
        expect = np.array([[0.5, 0.0, 0.0, 0.5],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.5, 0.0, 0.0, 0.5]])
        self.assertTrue(complex_equal(final[0][0], expect[0][0]))
        self.assertTrue(complex_equal(final[0][1], expect[0][1]))
        self.assertTrue(complex_equal(final[0][2], expect[0][2]))
        self.assertTrue(complex_equal(final[0][3], expect[0][3]))

        self.assertTrue(complex_equal(final[1][0], expect[1][0]))
        self.assertTrue(complex_equal(final[1][1], expect[1][1]))
        self.assertTrue(complex_equal(final[1][2], expect[1][2]))
        self.assertTrue(complex_equal(final[1][3], expect[1][3]))

        self.assertTrue(complex_equal(final[3][0], expect[3][0]))
        self.assertTrue(complex_equal(final[3][1], expect[3][1]))
        self.assertTrue(complex_equal(final[3][2], expect[3][2]))
        self.assertTrue(complex_equal(final[3][3], expect[3][3]))

    def test_tracing_out_last_bit(self):
        # Tracing out the third bit
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = DensityMatrix(state=state)
        s0 = ComputationalBasis(bitstring='0')
        s1 = ComputationalBasis(bitstring='1')
        idm = identity_by_bits(2)
        # tracing out the third bit
        lm0 = kronecker(idm, s0.as_bra().as_vector())
        rm0 = kronecker(idm, s0.as_vector())
        lm1 = kronecker(idm, s1.as_bra().as_vector())
        rm1 = kronecker(idm, s1.as_vector())
        # tracing out 0 and 1
        final_0 = matrix_product(lm0,
                                 matrix_product(density_matrix, rm0))
        final_1 = matrix_product(lm1,
                                 matrix_product(density_matrix, rm1))
        final = matrix_add(final_0, final_1)
        expect = np.array([[0.5, 0.0, 0.0, 0.0],
                           [0.0, 0.5, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0]])
        #print(final.as_array())
        self.assertTrue(complex_equal(final[0][0], expect[0][0]))
        self.assertTrue(complex_equal(final[0][1], expect[0][1]))
        self.assertTrue(complex_equal(final[0][2], expect[0][2]))
        self.assertTrue(complex_equal(final[0][3], expect[0][3]))

        self.assertTrue(complex_equal(final[1][0], expect[1][0]))
        self.assertTrue(complex_equal(final[1][1], expect[1][1]))
        self.assertTrue(complex_equal(final[1][2], expect[1][2]))
        self.assertTrue(complex_equal(final[1][3], expect[1][3]))

        self.assertTrue(complex_equal(final[3][0], expect[3][0]))
        self.assertTrue(complex_equal(final[3][1], expect[3][1]))
        self.assertTrue(complex_equal(final[3][2], expect[3][2]))
        self.assertTrue(complex_equal(final[3][3], expect[3][3]))
