#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    quantum_state.null_state.py

Main test:
    Null state singleton test

Updated:
    25 September 2021
"""
import unittest
from quantum_state.null_state import NULL_STATE, NullState


class Test_NullState_Singleton(unittest.TestCase):
    def test_singleton(self):
        null_state = NullState()
        null_state_2 = NullState()
        self.assertEqual(null_state, null_state_2)
        self.assertEqual(null_state, NULL_STATE)
        self.assertEqual(null_state_2, NULL_STATE)
