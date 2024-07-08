#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    common.function.py

Updated
    20 April 2021
"""
import unittest

from common.function import function_signature


def sample_function(self, alpha, beta, delta, chi, eta=10, 
                    gamma='Aloha', zeta=1e-14):
    pass


class TestSignature(unittest.TestCase):
    def test_all_args(self):
        sig = function_signature(sample_function)
        #print(sig)

    def test_with_skiplist(self):
        skiplist = ['self', 'zeta', 'eta', 'chi']
        sig = function_signature(sample_function, skip_list=skiplist)
        # check skipped arguments
        self.assertFalse('self' in sig['args'])
        self.assertFalse('chi' in sig['args'])
        self.assertFalse('zeta' in sig['kwargs'].keys())
