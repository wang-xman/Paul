#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.enlarge_matrix.controlled.py

Main test:
    Control index swap (ciswap) routines.

Updated:
    20 September 2021
"""
import unittest
#import numpy as np

from gate.enlarge_matrix.controlled_target_tuple \
    import control_index_swap as ciswap, is_CISWAP_required


class Test_Ciswap_Needed(unittest.TestCase):
    def test_one_control_bit(self):
        ti = (4,2,6,)
        cl = [(3,'1')]
        expected_swap_list = [(2,3)]
        expected_new_cl = [(2,'1')]
        expected_new_ti = (4,3,6,)
        self.assertTrue(is_CISWAP_required(control_list=cl, target_tuple=ti))
        ret = ciswap(control_list=cl, target_tuple=ti)
        self.assertTrue(ret['swap_list'] == expected_swap_list)
        self.assertTrue(ret['control_list'] == expected_new_cl)
        self.assertTrue(ret['target_tuple'] == expected_new_ti)

    def test_one_swap(self):
        ti = (4,2,6,)
        cl = [(1,'1'), (5,'1')]
        expected_swap_list = [(2,5)]
        expected_new_cl = [(1,'1'),(2,'1')]
        expected_new_ti = (4,5,6,)
        self.assertTrue(is_CISWAP_required(control_list=cl, target_tuple=ti))
        ret = ciswap(control_list=cl, target_tuple=ti)
        self.assertTrue(ret['swap_list'] == expected_swap_list)
        self.assertTrue(ret['control_list'] == expected_new_cl)
        self.assertTrue(ret['target_tuple'] == expected_new_ti)

    def test_two_swaps(self):
        ti = (2,1,6,)
        cl = [(3,'1'), (5,'1')]
        expected_swap_list = [(1,3), (2,5)]
        expected_new_cl = [(1,'1'),(2,'1')]
        expected_new_ti = (5,3,6,)
        self.assertTrue(is_CISWAP_required(control_list=cl, target_tuple=ti))
        ret = ciswap(control_list=cl, target_tuple=ti)
        #print(ret)
        self.assertTrue(ret['swap_list'] == expected_swap_list)
        self.assertTrue(ret['control_list'] == expected_new_cl)
        self.assertTrue(ret['target_tuple'] == expected_new_ti)

    def test_three_swaps(self):
        ti = (3,6,1,)
        cl = [(2,'1'), (4,'1'),(5,'1')]
        expected_swap_list = [(1,2), (2,4),(3,5)]
        expected_new_cl = [(1,'1'),(2,'1'),(3,'1')]
        expected_new_ti = (5,6,4,)
        self.assertTrue(is_CISWAP_required(control_list=cl, target_tuple=ti))
        ret = ciswap(control_list=cl, target_tuple=ti)
        #print(ret)
        self.assertTrue(ret['swap_list'] == expected_swap_list)
        self.assertTrue(ret['control_list'] == expected_new_cl)
        self.assertTrue(ret['target_tuple'] == expected_new_ti)


class Test_No_Ciswap_Needed(unittest.TestCase):
    """ Ciswap not needed"""
    def test_one_control_bit(self):
        ti = (4,2,6,)
        cl = [(0,'1')]
        expected_swap_list = []
        expected_new_cl = [(0,'1')]
        expected_new_ti = (4,2,6,)
        self.assertFalse(is_CISWAP_required(control_list=cl, target_tuple=ti))
        ret = ciswap(control_list=cl, target_tuple=ti)
        self.assertTrue(ret['swap_list'] == expected_swap_list)
        self.assertTrue(ret['control_list'] == expected_new_cl)
        self.assertTrue(ret['target_tuple'] == expected_new_ti)

    def test_ci_low(self):
        ti = (4,2,6,)
        cl = [(0,'1'), (1,'1')]
        expected_swap_list = []
        expected_new_cl = [(0,'1'),(1,'1')]
        expected_new_ti = (4,2,6,)
        self.assertFalse(is_CISWAP_required(control_list=cl, target_tuple=ti))
        ret = ciswap(control_list=cl, target_tuple=ti)
        self.assertTrue(ret['swap_list'] == expected_swap_list)
        self.assertTrue(ret['control_list'] == expected_new_cl)
        self.assertTrue(ret['target_tuple'] == expected_new_ti)

    def test_ci_large(self):
        ti = (4,2,5,)
        cl = [(6,'1'), (7,'1')]
        expected_swap_list = []
        expected_new_cl = [(6,'1'),(7,'1')]
        expected_new_ti = (4,2,5,)
        self.assertFalse(is_CISWAP_required(control_list=cl, target_tuple=ti))
        ret = ciswap(control_list=cl, target_tuple=ti)
        self.assertTrue(ret['swap_list'] == expected_swap_list)
        self.assertTrue(ret['control_list'] == expected_new_cl)
        self.assertTrue(ret['target_tuple'] == expected_new_ti)

    def test_middle(self):
        """ Target window is sandwiched by control indices. """
        ti = (4,2,6,)
        cl = [(0,'1'), (7,'1')]
        expected_swap_list = []
        expected_new_cl = [(0,'1'),(7,'1')]
        expected_new_ti = (4,2,6,)
        self.assertFalse(is_CISWAP_required(control_list=cl, target_tuple=ti))
        ret = ciswap(control_list=cl, target_tuple=ti)
        self.assertTrue(ret['swap_list'] == expected_swap_list)
        self.assertTrue(ret['control_list'] == expected_new_cl)
        self.assertTrue(ret['target_tuple'] == expected_new_ti)
