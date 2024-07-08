#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Main test:
    Partial trace function.
"""
import unittest
import numpy as np

from linear_space.matrix import SquareMatrix
from qubit import qubit_from_bitlist

from density_matrix.density_matrix import QubitDensityMatrix
from measurement.partial_trace import PartialTraceError, partial_trace


def complex_equal(c1, c2):
    ret = False
    inf = 1e-13
    if np.linalg.norm(c1 - c2) <= inf:
        ret = True
    return ret


class TestPartialTraceFunction(unittest.TestCase):
    """ Partial tracing via function """

    def test_last_bit(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        reduced = partial_trace(density_matrix, index_range_bound=[2,2])
        self.assertTrue(isinstance(reduced, SquareMatrix))

    def test_first_two_bit(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        reduced = partial_trace(density_matrix, index_range_bound=[0,1])
        expected = np.array([[0.5, 0.0],[0.0, 0.5]])
        for i in range(0, len(expected), 1):
            for j in range(0, len(expected), 1):
                self.assertTrue(complex_equal(reduced[i][j], expected[i][j]))

    def test_last_two_bit(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        reduced = partial_trace(density_matrix, index_range_bound=[1,2])
        expected = np.array([[1.0 + 0.j, 0.0+ 0.j],[0.0+ 0.j, 0.0+ 0.j]])
        for i in range(0, len(expected), 1):
            for j in range(0, len(expected), 1):
                self.assertTrue(complex_equal(reduced[i][j], expected[i][j]))

    def test_all_bit(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        # NOTE the output is still a matrix of dimension 2 [[1.0]]
        reduced = partial_trace(density_matrix, index_range_bound=[0,2])
        expected = np.array([[1.0]])
        self.assertTrue(complex_equal(reduced, expected[0][0]))


class TestPartialTrace(unittest.TestCase):
    def test_both_string_and_state(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        self.assertRaises(PartialTraceError, partial_trace, density_matrix,
                          **{'bitstring': '100', 'state': state})


class TestPartialTrace_withBitString(unittest.TestCase):
    def test_bitstring(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        prob = partial_trace(density_matrix,bitstring='100')
        self.assertTrue(prob == 0.0)

    def test_bitstring_2(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        prob = partial_trace(density_matrix,bitstring='000')
        self.assertTrue(complex_equal(prob, 0.5))

    def test_bitstring_3(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '111')])
        density_matrix = QubitDensityMatrix(state=state)
        prob = partial_trace(density_matrix,bitstring='111')
        self.assertTrue(complex_equal(prob, 0.5))

    def test_bitstring_too_long(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        self.assertRaises(PartialTraceError, partial_trace, density_matrix,
                          **{'bitstring': '1001'})

    def test_bitstring_too_short(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        self.assertRaises(PartialTraceError, partial_trace, density_matrix,
                          **{'bitstring': '10'})


class TestPartialTrace_withStringAndRange(unittest.TestCase):
    def test_reduced_to_zeros(self):
        state = qubit_from_bitlist([(1.0, '0010'), (1.0, '0110')])
        density_matrix = QubitDensityMatrix(state=state)
        reduced = partial_trace(density_matrix,bitstring='10', index_range_bound=[1,2])
        # should be zeros
        for i in range(0, reduced.nrows, 1):
            for j in range(0, reduced.ncols, 1):
                self.assertTrue(complex_equal(reduced[i][j], 0.0))

    def test_reduced_to_nonzeros(self):
        state = qubit_from_bitlist([(1.0, '0010'), (1.0, '0110')])
        density_matrix = QubitDensityMatrix(state=state)
        reduced = partial_trace(density_matrix, bitstring='11', index_range_bound=[1,2])
        # should be zeros
        for i in range(0, reduced.nrows, 1):
            for j in range(0, reduced.ncols, 1):
                if i!= 0 and j !=0:
                    self.assertTrue(complex_equal(reduced[i][j], 0.0))
                elif i== 0 and j ==0:
                    self.assertTrue(complex_equal(reduced[i][j], 0.5))
                else:
                    pass


class TestPartialTrace_withState(unittest.TestCase):
    def test_qubit_wholestate(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        prob = partial_trace(density_matrix, state=state)
        self.assertTrue(complex_equal(prob, 1.0))

    def test_qubit_componental(self):
        state = qubit_from_bitlist([(1.0, '000'), (1.0, '011')])
        density_matrix = QubitDensityMatrix(state=state)
        s = qubit_from_bitlist([(1.0, '000')])
        prob = partial_trace(density_matrix, state=s)
        self.assertTrue(complex_equal(prob, 0.5))

    def test_bell_state(self):
        state = qubit_from_bitlist([(1.0, '00'), (1.0, '01'),
                                    (1.0, '10'), (1.0, '11')])
        density_matrix = QubitDensityMatrix(state=state)
        bell1 = qubit_from_bitlist([(1.0, '10'), (1.0, '11')])
        prob1 = partial_trace(density_matrix, state=bell1)
        self.assertTrue(complex_equal(prob1, 0.5))
