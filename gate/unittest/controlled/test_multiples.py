#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.decorator.py

Main test:
    Test controlled operation using single-qubit gates.

Updated:
    05 July 2021
"""
import unittest

from qubit import ComputationalBasis
from gate import multiple_qubit as multiple


class Test(unittest.TestCase):
    def test(self):
        print("\n *** *** Controlled operation on multiple-qubit gates *** ***")


class Test_ControlledCNOT_Without_CISWAP(unittest.TestCase):
    gate = multiple.controlled_NOT

    def test_5bits_one(self):
        test_state = ComputationalBasis(bitstring='11110')
        ci = 0 # control_index
        control = 1
        target = 3
        params = {
            'input_state': test_state,
            'control_index': ci,
            'control': control,
            'target': target,
            'noq':3
        }
        exp_state = ComputationalBasis(bitstring='11100')
        new_state = self.gate.ctrl(**params)
        #print(new_state.as_vector().as_array())
        self.assertTrue(new_state == exp_state)


class TestControlledCNOT(unittest.TestCase):
    gate = multiple.controlled_NOT

    def test_one(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 2 # control_index
        control = 0
        target = 1
        params = {
            'input_state': test_state,
            'control_index': ci,
            'control': control,
            'target': target,
            'noq':2
        }
        exp_state = ComputationalBasis(bitstring='010')
        new_state = self.gate.ctrl(**params)
        #print(new_state.as_vector().as_array())
        self.assertTrue(new_state == exp_state)

    def test_one_2(self):
        test_state = ComputationalBasis(bitstring='110')
        ci = 0 # control_index
        control = 1
        target = 2
        params = {
            'input_state': test_state,
            'control_index': ci,
            'control': control,
            'target': target,
            'noq':2
        }
        exp_state = ComputationalBasis(bitstring='111')
        new_state = self.gate.ctrl(**params)
        #print(new_state.as_vector().as_array())
        self.assertTrue(new_state == exp_state)

    def test_5bits_one(self):
        test_state = ComputationalBasis(bitstring='11110')
        ci = 0 # control_index
        control = 1
        target = 3
        params = {
            'input_state': test_state,
            'control_index': ci,
            'control': control,
            'target': target,
            'noq':3
        }
        exp_state = ComputationalBasis(bitstring='11100')
        new_state = self.gate.ctrl(**params)
        #print(new_state.as_vector().as_array())
        self.assertTrue(new_state == exp_state)

    def test_5bits_two(self):
        test_state = ComputationalBasis(bitstring='11110')
        ci = 3 # control_index
        control = 2
        target = 0
        params = {
            'input_state': test_state,
            'control_index': ci,
            'control': control,
            'target': target,
            'noq':3
        }
        exp_state = ComputationalBasis(bitstring='01110')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)


class TestControlledCNOT_SandwichedControlIndex(unittest.TestCase):
    gate = multiple.controlled_NOT

    def test_one(self):
        test_state = ComputationalBasis(bitstring='110')
        # control_index in the middle
        ci = 1
        control = 0
        target = 2
        params = {
            'input_state': test_state,
            'control_index': ci,
            'control': control,
            'target': target,
            'noq':2
        }
        exp_state = ComputationalBasis(bitstring='111')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)


class TestControlledSWAP(unittest.TestCase):
    gate = multiple.SWAP

    def test_one(self):
        test_state = ComputationalBasis(bitstring='010')
        ci = 2 # control_index
        alpha = 0
        beta = 1
        params = {
            'input_state': test_state,
            'control_index': ci,
            'alpha': alpha,
            'beta': beta,
            'noq':2
        }
        exp_state = ComputationalBasis(bitstring='010')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)

    def test_two(self):
        test_state = ComputationalBasis(bitstring='110')
        ci = 0 # control_index
        alpha = 1
        beta = 2
        params = {
            'input_state': test_state,
            'control_index': ci,
            'alpha': alpha,
            'beta': beta,
            'noq':2
        }
        exp_state = ComputationalBasis(bitstring='101')
        new_state = self.gate.ctrl(**params)
        #print(new_state.as_vector().as_array())
        self.assertTrue(new_state == exp_state)

    def test_4bits_one(self):
        test_state = ComputationalBasis(bitstring='1110')
        ci = 0 # control_index
        alpha = 1
        beta = 3
        params = {
            'input_state': test_state,
            'control_index': ci,
            'alpha': alpha,
            'beta': beta,
            'noq':3
        }
        exp_state = ComputationalBasis(bitstring='1011')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)


class TestControlledSWAP_SandwichedControlIndex(unittest.TestCase):
    gate = multiple.SWAP

    def test_one(self):
        test_state = ComputationalBasis(bitstring='011')
        ci = 1 # control_index
        alpha = 0
        beta = 2
        params = {
            'input_state': test_state,
            'control_index': ci,
            'alpha': alpha,
            'beta': beta,
            'noq':2
        }
        exp_state = ComputationalBasis(bitstring='110')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)
    
    def test_two(self):
        test_state = ComputationalBasis(bitstring='10110')
        ci = 2 # control_index
        alpha = 1
        beta = 3
        params = {
            'input_state': test_state,
            'control_index': ci,
            'alpha': alpha,
            'beta': beta,
            'noq':2
        }
        exp_state = ComputationalBasis(bitstring='11100')
        new_state = self.gate.ctrl(**params)
        self.assertTrue(new_state == exp_state)
    
