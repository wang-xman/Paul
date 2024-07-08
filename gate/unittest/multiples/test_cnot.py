#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Gate under test:
    Qubit flip

File under test:
    gate.multiple.py

Updated:
    20 April 2021
"""
import unittest
import numpy as np
from linear_space.vector import UnitVector
from qubit import QubitState, ComputationalBasis
from gate.base import GateBaseError
from gate import single_qubit_gates as singles
from gate.multiple_qubit import controlled_NOT
from gate.enlarge_matrix.errors import GateMatrixEnlargeValidationError

class Test(unittest.TestCase):
    def test(self):
        print("\n *** *** CNOT gate *** ***")


class TestCNOT_Fail(unittest.TestCase):
    gate = controlled_NOT

    def test_undeclared_arguments(self):
        test_state = ComputationalBasis(bitstring='00')
        ci = 0
        ti = 2 # Error
        params = {
            'input_state':test_state,
            'noq': test_state.noq,
            'control':ci, 
            'target':ti,
            'hellop_index': 2
        }
        # Error: hellop_index not declared
        #self.gate(**params)
        self.assertRaises(GateBaseError, self.gate, **params)

    def test_target_out_of_range(self):
        test_state = ComputationalBasis(bitstring='00')
        ci = 0
        ti = 2 # Error
        params = {
            'input_state':test_state, 
            'noq': test_state.noq,
            'control':ci, 
            'target':ti
        }
        # Error: target index out of range
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate, **params)

    def test_control_out_of_range(self):
        test_state = ComputationalBasis(bitstring='00')
        ci = 2
        ti = 1 # Error
        params = {
            'input_state':test_state, 
            'noq': test_state.noq,
            'control':ci, 
            'target':ti
        }
        # Error: control index out of range
        #self.gate(**params)
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate, **params)

    def test_control_target_identical(self):
        test_state = ComputationalBasis(bitstring='00')
        ci = 1
        ti = 1 
        params = {
            'input_state':test_state,
            'noq': test_state.noq,
            'control':ci, 
            'target':ti
        }
        # Error: control target indices identical
        #self.gate(**params)
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate, **params)


class TestCNOT_Basis(unittest.TestCase):
    gate = controlled_NOT

    def test_basis_2bits(self):
        test_state = ComputationalBasis(bitstring='00')
        # apply cnot
        ci = 0
        ti = 1
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'control':ci, 
            'target':ti
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='00')
        self.assertTrue(new_state == exp_state)

    def test_basis_2bits_2(self):
        test_state = ComputationalBasis(bitstring='10')
        # apply cnot
        ci = 0
        ti = 1
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'control':ci, 
            'target':ti
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='11')
        self.assertTrue(new_state == exp_state)

    def test_basis_4bits_1(self):
        test_state = ComputationalBasis(bitstring='0110')
        # apply cnot
        ci = 2
        ti = 3
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'control':ci, 
            'target':ti
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='0111')
        self.assertTrue(new_state == exp_state)

    def test_basis_4bits(self):
        test_state = ComputationalBasis(bitstring='0110')
        # apply cnot
        ci = 0
        ti = 3
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'control':ci, 
            'target':ti
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='0110')
        self.assertTrue(new_state == exp_state)


class TestCNOT_GenericQubitState(unittest.TestCase):
    gate = controlled_NOT

    def test_2bits(self):
        # |01> + |11>
        test_state = QubitState(vector=UnitVector(array=np.array([[0],[1],[0],[1]])))
        ci = 0
        ti = 1 
        params = {
            'input_state':test_state,
            'noq':test_state.noq,
            'control':ci,
            'target':ti
        }
        # new state |01> + |10>
        new_state = self.gate(**params)
        exp_state = QubitState(vector=UnitVector(array=np.array([[0],[1],[1],[0]])))
        self.assertTrue(new_state == exp_state)

    def test_2bits_2(self):
        # |01> + |11> + |10>
        test_state = QubitState(vector=UnitVector(array=np.array([[0],[1],[1],[1]])))
        ci = 0
        ti = 1 
        params = {
            'input_state':test_state,
            'noq':test_state.noq,
            'control':ci, 
            'target':ti
        }
        # new state |01> + |10> +|11>
        new_state = self.gate(**params)
        exp_state = QubitState(vector=UnitVector(array=np.array([[0],[1],[1],[1]])))
        self.assertTrue(new_state == exp_state)
