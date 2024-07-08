#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.decorator.py

Main test:
    Test decorator.global_operator_matrix() method.

Updated:
    26 July 2021
"""
import unittest
from linear_space.matrix import SquareMatrix
from linear_space.algebra import matrix_product
from qubit import ComputationalBasis
from gate import single_qubit_gates as singles


class TestFlipGate_Success(unittest.TestCase):
    gate = singles['Flip']

    def test_3bits(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 0 # control_index
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_index': ci,
        }
        #exp_state = ComputationalBasis(bitstring='010')
        opmat = self.gate.global_operator_matrix(**params)
        self.assertTrue(isinstance(opmat, SquareMatrix))
        #print(opmat.as_array())
        self.assertTrue(opmat[4][6] == 1)
        self.assertTrue(opmat[5][7] == 1)
        self.assertTrue(opmat[6][4] == 1)
        self.assertTrue(opmat[7][5] == 1)


class TestConsecutiveGateApplication(unittest.TestCase):
    """ Consecutive application of gates """
    gate = singles['Flip']

    def test_011(self):
        test_state = ComputationalBasis(bitstring='011')
        first_ci = 0 # control_index
        first_ti = 1 # target_index
        first_params = {
            'input_state': test_state,
            'target_index': first_ti,
            'control_index': first_ci,
        }
        #exp_state = ComputationalBasis(bitstring='010')
        first_opmat = self.gate.global_operator_matrix(**first_params)
        second_ci = 1 # control_index
        second_ti = 2 # target_index
        second_params = {
            'input_state': test_state,
            'target_index': second_ti,
            'control_index': second_ci,
        }
        #exp_state = ComputationalBasis(bitstring='010')
        second_opmat = self.gate.global_operator_matrix(**second_params)
        total_opmat = matrix_product(second_opmat, first_opmat)
        new_vector = matrix_product(total_opmat, test_state.as_vector())
        #print(new_vector)
        first_state = self.gate(**first_params) # 011
        second_state_params = {
            'input_state': first_state,
            'target_index': second_ti,
            'control_index': second_ci,
        }
        second_state = self.gate(**second_state_params) #010
        expected = ComputationalBasis(bitstring='010')
        #print(second_state.as_vector())
        self.assertTrue(second_state.as_vector() == new_vector)
        self.assertTrue(expected.as_vector() == new_vector)


    def test_110(self):
        test_state = ComputationalBasis(bitstring='110')
        first_ci = 0 # control_index
        first_ti = 1 # target_index
        first_params = {
            'input_state': test_state,
            'target_index': first_ti,
            'control_index': first_ci,
        }
        first_opmat = self.gate.global_operator_matrix(**first_params)
        second_ci = 1 # control_index
        second_ti = 2 # target_index
        second_params = {
            'input_state': test_state,
            'target_index': second_ti,
            'control_index': second_ci,
        }
        second_opmat = self.gate.global_operator_matrix(**second_params)
        total_opmat = matrix_product(second_opmat, first_opmat)
        new_vector = matrix_product(total_opmat, test_state.as_vector())
        #print(new_vector)
        first_state = self.gate(**first_params) # 100
        second_state_params = {
            'input_state': first_state,
            'target_index': second_ti,
            'control_index': second_ci,
        }
        second_state = self.gate(**second_state_params) # 100
        #print(second_state.as_vector())
        expected = ComputationalBasis(bitstring='100')
        self.assertTrue(second_state.as_vector() == new_vector)
        self.assertTrue(expected.as_vector() == new_vector)
