#!/usr/bin/env python3
#-*- coding:utf-8 -*- 
"""
Module under test:
    common.string.py

Updated
    20 April 2021
"""
import unittest

from ..string import is_string, is_empty_string, has_space


class Test_is_string(unittest.TestCase):
    def test_int(self):
        value = 1
        self.assertFalse(is_string(value))
    
    def test_float(self):
        value = 0.5
        self.assertFalse(is_string(value))
    
    def test_scientific(self):
        value = 0.08e-14
        self.assertFalse(is_string(value))