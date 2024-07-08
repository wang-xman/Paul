"""
File under test
    quantum_instruction.base.py

Main test:
    Index range object.

Updated:
    13 August 2021
"""
import unittest
from quantum_instruction.index_range import IndexRangeValidator, IndexRange
from quantum_instruction.errors import IndexRangeError


class TestInit(unittest.TestCase):
    def test_okay(self):
        test_limits = [0,10]
        index_range = IndexRange(range_limit_list=test_limits)
        self.assertTrue(index_range.is_normal)

    def test_reversed_okay(self):
        test_limits = [10,7]
        index_range = IndexRange(range_limit_list=test_limits)
        self.assertFalse(index_range.is_normal)


class TestLimits(unittest.TestCase):
    def test_normal_order(self):
        test_limits = [0,10]
        index_range = IndexRange(range_limit_list=test_limits)
        self.assertTrue(index_range.is_normal)
        self.assertTrue(index_range.lower_limit == 0)
        self.assertTrue(index_range.upper_limit == 10)

    def test_reversed_order(self):
        test_limits = [8,5]
        index_range = IndexRange(range_limit_list=test_limits)
        self.assertFalse(index_range.is_normal)
        self.assertTrue(index_range.lower_limit == 5)
        self.assertTrue(index_range.upper_limit == 8)


class TestRangeObject(unittest.TestCase):
    def test_single_item(self):
        test_limits = [5,5]
        index_range = IndexRange(range_limit_list=test_limits)
        expected_range = range(5,6,1)
        self.assertTrue(index_range.as_range() == expected_range)

    def test_normal_order(self):
        test_limits = [0,10]
        index_range = IndexRange(range_limit_list=test_limits)
        expected_range = range(0,11,1)
        self.assertTrue(index_range.as_range() == expected_range)

    def test_reversed_order(self):
        test_limits = [9,3]
        index_range = IndexRange(range_limit_list=test_limits)
        expected_range = range(9,2,-1)
        self.assertTrue(index_range.as_range() == expected_range)


class TestIndexList(unittest.TestCase):
    def test_normal_order(self):
        test_limits = [0,10]
        index_range = IndexRange(range_limit_list=test_limits)
        expected_list = [0,1,2,3,4,5,6,7,8,9,10]
        self.assertTrue(index_range.as_index_list() == expected_list)

    def test_reversed_order(self):
        test_limits = [9,5]
        index_range = IndexRange(range_limit_list=test_limits)
        expected_list = [9,8,7,6,5]
        self.assertTrue(index_range.as_index_list() == expected_list)

    def test_single_item(self):
        test_limits = [9,9]
        index_range = IndexRange(range_limit_list=test_limits)
        print(index_range.as_index_list())
        expected_list = [9]
        self.assertTrue(index_range.as_index_list() == expected_list)
