#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.special.py

NOTE Specialised qubit states

Updated:
    25 September 2021
"""
import unittest
import numpy as np
from qubit.special import QubitState, EquallyWeightedSuperposition, EWS, \
    AllUp, AllDown


class TestEquallyWeightedSuperposition(unittest.TestCase):
    def test_noq_3(self):
        noq = 3
        ews = EquallyWeightedSuperposition(number_of_qubits=noq)
        complist = ews.as_basislist()
        # amplitude
        amp = 1.0/np.sqrt(2**noq)
        # read out the amplitude of 
        self.assertEqual(complist[3][0], amp)

    def test_noq_6(self):
        """ NOTE May take some time """
        noq = 6
        ews = EquallyWeightedSuperposition(number_of_qubits=noq)
        self.assertTrue(isinstance(ews, QubitState))
        complist = ews.as_basislist()
        # amplitude
        amp = 1.0/np.sqrt(2**noq)
        # read out the amplitude of 
        self.assertEqual(complist[3][0], amp)


class TestEWS(unittest.TestCase):
    def test_noq_3(self):
        noq = 3
        ews = EWS(number_of_qubits=noq)
        complist = ews.as_basislist()
        # amplitude
        amp = 1.0/np.sqrt(2**noq)
        # read out the amplitude of 
        self.assertEqual(complist[3][0], amp)

    def test_noq_10(self):
        noq = 10
        ews = EWS(number_of_qubits=noq)
        complist = ews.as_basislist()
        # amplitude
        amp = 1.0/np.sqrt(2**noq)
        # read out the amplitude of 
        self.assertEqual(complist[3][0], amp)


class TestAllUp(unittest.TestCase):
    def test(self):
        noq = 5
        allup = AllUp(number_of_qubits=noq)
        self.assertEqual(allup.as_bitlist(), [(1.0, '00000')])


class TestAllDown(unittest.TestCase):
    def test(self):
        noq = 10
        alldown = AllDown(number_of_qubits=noq)
        self.assertEqual(alldown.as_bitlist(), [(1.0, '1111111111')])
