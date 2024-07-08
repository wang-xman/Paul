#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_memory.memory.py

Main test:
    Memory classes and objects.

Updated:
    10 August 2021
"""
import unittest
from quantum_memory.base_memory import BaseMemory


class memory_naked(BaseMemory):
    pass

class TestMemoryNaked(unittest.TestCase):
    def test_pass(self):
        memory_naked()


class memory_with_label(BaseMemory):
    label = "test memory"

class TestMemoryWithLabel(unittest.TestCase):
    def test_(self):
        memory_with_label()


class memory_okay(BaseMemory):
    label = "memory_okay"


class TestMemoryOkay(unittest.TestCase):

    def test_(self):
        memory_okay()
