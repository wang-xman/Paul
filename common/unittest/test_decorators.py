#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    common.function.decorator.py

Updated
    06 April 2021
"""
import unittest
from common.function.errors import VerifierFunctionDecoratorError
from common.function.decorators import VerifierFunctionDecorator, \
    FunctionInvocationDecorator



@VerifierFunctionDecorator
def is_something():
    pass

class Test_Verifier_as_Instance(unittest.TestCase):
    def test_okay(self):
        self.assertTrue(isinstance(is_something, VerifierFunctionDecorator))

@VerifierFunctionDecorator
def not_boolean_return():
    return 1

@VerifierFunctionDecorator
def return_string():
    return "bc"

@VerifierFunctionDecorator
def return_none():
    return None

class Test_Verifier_Non_Boolean_Return(unittest.TestCase):
    def test_return_interger(self):
        self.assertTrue(isinstance(not_boolean_return, VerifierFunctionDecorator))
        #not_boolean_return()
        self.assertRaises(VerifierFunctionDecoratorError, not_boolean_return)

    def test_return_string(self):
        self.assertTrue(isinstance(return_string, VerifierFunctionDecorator))
        #return_string()
        self.assertRaises(VerifierFunctionDecoratorError, return_string)

    def test_return_none(self):
        self.assertTrue(isinstance(return_none, VerifierFunctionDecorator))
        #return_string()
        self.assertRaises(VerifierFunctionDecoratorError, return_none)


@FunctionInvocationDecorator(
    argument_type = {
        'alpha': int,
        'beta': int
    }
)
def test_fully_declared(alpha, beta):
    return alpha + beta


class Test_Fully_Declared(unittest.TestCase):
    def test_okay(self):
        res = test_fully_declared(1,1)
        self.assertEqual(res, 2)
