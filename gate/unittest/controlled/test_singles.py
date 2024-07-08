#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.decorator.py

Main test:
    Test controlled operation using single-qubit gates.

Updated:
    26 July 2021
"""
import unittest
#import numpy as np
from qubit import ComputationalBasis
from gate.base import GateBaseError
from gate import single_qubit_gates as singles
from gate.enlarge_matrix.errors import GateMatrixEnlargeValidationError


class Test(unittest.TestCase):
    def test(self):
        print("\n *** *** Controlled operation using single gates *** ***")


class TestFlipGate_Success(unittest.TestCase):
    gate = singles['Flip']

    def test_3bits_1(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 0 # control_index
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_index': ci,
        }
        exp_state = ComputationalBasis(bitstring='010')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_3bits_2(self):
        test_state = ComputationalBasis(bitstring='110')
        ci = 0 # control_index
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_index': ci,
        }
        exp_state = ComputationalBasis(bitstring='100')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_3bits_3(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 1 # control_index
        ti = 2 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_index': ci,
        }
        exp_state = ComputationalBasis(bitstring='011')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)


class TestFlipGate_MissingArguments(unittest.TestCase):
    gate = singles['Flip']

    def test_missing_input_state(self):
        #test_state = ComputationalBasis(bitstring='010')
        ci = 0 # control_index
        ti = 1 # target_index
        params = {
            #'input_state': test_state,
            'target_index': ti,
            'control_index': ci
        }
        # Error: missing input state
        #self.gate.ctrl(**params)
        self.assertRaises(GateBaseError, self.gate.ctrl, **params)

    def test_missing_control_index(self):
        test_state = ComputationalBasis(bitstring='010')
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
        }
        # Error: missing control index
        #self.gate.ctrl(**params)
        self.assertRaises(GateBaseError, self.gate.ctrl, **params)

    def test_missing_target_index(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 0 # control_index
        #ti = 1 # target_index
        params = {
            'input_state': test_state,
            'control_index': ci,
        }
        # Error: missing targetindex
        #self.gate.ctrl(**params)
        self.assertRaises(GateBaseError, self.gate.ctrl, **params)


class TestFlipGate_IndexOutOfRange(unittest.TestCase):
    gate = singles['Flip']

    def test_control_index_OOR(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 3 # control_index
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_index': ci
        }
        # Error: controlled indx out of range
        #self.gate.ctrl(**params)
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate.ctrl, **params)

    def test_target_index_OOR(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 0 # control_index
        ti = 3 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_index': ci
        }
        # Error: target index out of range
        #self.gate.ctrl(**params)
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate.ctrl, **params)

    def test_identical_indices(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 1 # control_index
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_index': ci
        }
        # Error: target and control indices are identical
        #self.gate.ctrl(**params)
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate.ctrl, **params)


class TestMultipleControl_FlipGate_TwoBitSystem_Success(unittest.TestCase):
    """ Demonstrates that a single-control can be achieved by control list """
    gate = singles['Flip']

    def test_2bits_1(self):
        """ CNOT """
        test_state = ComputationalBasis(bitstring='11')
        cl = [(0, '1')] # control list
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        exp_state = ComputationalBasis(bitstring='10')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_2bits_2(self):
        """ CNOT conditional on 0, not 1 """
        test_state = ComputationalBasis(bitstring='01')
        cl = [(0, '0')] # control list
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        exp_state = ComputationalBasis(bitstring='00')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_2bits_3(self):
        """ CNOT """
        test_state = ComputationalBasis(bitstring='01')
        cl = [(1, '1')] # control list
        ti = 0 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        exp_state = ComputationalBasis(bitstring='11')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)


class TestMultipleControl_FlipGate_Success(unittest.TestCase):
    gate = singles['Flip']

    def test_3bits_1(self):
        test_state = ComputationalBasis(bitstring='010')
        cl = [(0, '1')] # control list
        ti = 1 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        exp_state = ComputationalBasis(bitstring='010')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_3bits_with_two_control_bits(self):
        """ Toffoli gate """
        test_state = ComputationalBasis(bitstring='110')
        cl = [(0, '1'), (1, '1')] # control list
        ti = 2 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        exp_state = ComputationalBasis(bitstring='111')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_3bits_with_two_control_bits_different_conditionals(self):
        test_state = ComputationalBasis(bitstring='010')
        cl = [(0, '0'), (1, '1')] # control list
        ti = 2 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        exp_state = ComputationalBasis(bitstring='011')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_5bits_with_two_control_bits(self):
        test_state = ComputationalBasis(bitstring='11010')
        cl = [(0, '1'), (1, '1')] # control list
        ti = 2 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        exp_state = ComputationalBasis(bitstring='11110')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_5bits_with_two_different_control_bits(self):
        test_state = ComputationalBasis(bitstring='11010')
        cl = [(1, '1'), (2, '0')] # control list
        ti = 4 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        exp_state = ComputationalBasis(bitstring='11011')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)


class TestMultipleControl_FlipGate_Failure(unittest.TestCase):
    gate = singles['Flip']

    def test_5bits_with_target_error(self):
        test_state = ComputationalBasis(bitstring='11010')
        cl = [(1, '1'), (2, '0')] # control list
        ti = 5 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        # Error: target index out of range
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate.ctrl, **params)

    def test_5bits_with_control_index_error(self):
        test_state = ComputationalBasis(bitstring='11010')
        cl = [(5, '1'), (2, '0')] # control list
        ti = 4 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        # Error: control index out of range
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate.ctrl, **params)

    def test_5bits_with_control_value_error(self):
        test_state = ComputationalBasis(bitstring='11010')
        cl = [(0, '1'), (2, '0.4')] # control list
        ti = 4 # target_index
        params = {
            'input_state': test_state,
            'target_index': ti,
            'control_list': cl,
        }
        # Error: control value is neither 1 or 0
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate.ctrl, **params)
