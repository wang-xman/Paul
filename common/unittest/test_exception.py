#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    common.exception.base.py

Updated
    22 September 2021
"""
import unittest

from common.exception.base import Base_Error


class TestException(unittest.TestCase):
    def test_(self):
        err = Exception('THIS IS A ERROR MESSSAGE')
        # Get error message from an exception instance
        self.assertTrue(str(err) == 'THIS IS A ERROR MESSSAGE')


class TestBaseError(unittest.TestCase):
    def test_no_message(self):
        self.assertRaises(Exception, Base_Error, None)

    def test_wrong_message_type(self):
        msg = 10
        self.assertRaises(Exception, Base_Error, msg)


class CustomisedError(Base_Error):
    """ Customised error class for test """
    header = 'TestCustomisedError'
    #location = 'common.unittest.test_exception.py'
    level = 'Development'


class TestCustomisdBaseError(unittest.TestCase):
    def test(self):
        error = CustomisedError(message='There is something wrong!')
        # full message is not identical to raw message
        self.assertFalse(error.full_message == error.message)
        error.relocate("TEMP LOC")
        error.relocate("SECOND LOC")
        self.assertEqual(error.first_location,'common.exception.base.py')
        self.assertEqual(error.last_location,'SECOND LOC')

    def test_passed_in_location(self):
        error = CustomisedError(message='There is something wrong!',
                                location='HAhahHAHHAH')
        # error location is different from class attribute
        self.assertEqual(error.report_location, 'HAhahHAHHAH')
