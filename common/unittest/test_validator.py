#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Module under test:
    common.validator.py

Updated
    22 September 2021
"""
import unittest

from common.exception.errors import Base_Error, Validation_Error

from common.validator.errors import BaseValidatorError
from common.validator.base_validator import Base_Validator

__MODULE_LOCATION__ = 'common.unittest.test_validator'


class Test_Instantiation(unittest.TestCase):
    def test_okay(self):
        self.assertRaises(BaseValidatorError, Base_Validator)


class NonBaseErrorSample:
    """ Error not subclass Base_Error """
    header = 'ValidatorTest'
    level = 'Test'
    location = 'test_validator.py'

class NonBaseErrorValidator(Base_Validator):
    error_class = NonBaseErrorSample

class Test_Validator_with_Non_Base_Error(unittest.TestCase):
    def test_okay(self):
        #NonBaseErrorValidator()
        self.assertRaises(BaseValidatorError, NonBaseErrorValidator, None)


class ErrorSample(Validation_Error):
    header = 'ValidatorTest'
    level = 'Test'
    location = 'test_validator.py'


class SampleValidator(Base_Validator):
    error_class = ErrorSample

    def __init__(self, value):
        super().__init__()
        if value > 10:
            self.report_errors(['Value is greater than 10!', 'Halola'],
                               location='Test')
        elif value < 0:
            self.report_errors('Value is negative!')


class TestValidator(unittest.TestCase):
    def test(self):
        validator = SampleValidator(11)
        self.assertFalse(validator.is_valid)
        #print(validator)

    def test_relocate_error_location(self):
        validator = SampleValidator(11)
        #validator.raise_errors()
        error0 = validator.get_errors()[0]
        error1 = validator.get_errors()[1]
        # relocate
        error0.relocate(location='Vormir')
        #print(error0.first_location)
        self.assertTrue(error0.last_location=='Vormir')
        self.assertEqual(error1.message, 'Halola')


class FailedSampleValidator(Base_Validator):
    """ Failed """

class Test_Failed_Sample(unittest.TestCase):
    def test(self):
        # Error: no error class
        #FailedSampleValidator()
        self.assertRaises(BaseValidatorError, FailedSampleValidator, None)


class ParentValidator(Base_Validator):
    error_class = ErrorSample

class ChildValidator(ParentValidator):
    """ Inherited error class """


class Test_Inherited_Error_Class(unittest.TestCase):
    def test(self):
        # Okay
        cv = ChildValidator()
        self.assertEqual(cv.error_class, ErrorSample)


class MultipleErrorValidator(Base_Validator):
    error_class = ErrorSample
    #error_location = 'HAHHAHHAH'

    def __init__(self, value):
        super().__init__()
        if value > 2:
            self.report_errors(['Value is greater than 2!', 'Halola'])
        elif value > 5:
            self.report_errors('Value is greater than 5!')


class Test_Multiple_Error_Validator(unittest.TestCase):
    def test_no_message(self):
        validator = MultipleErrorValidator(11)
        # Error: no error provided
        self.assertRaises(BaseValidatorError, validator.report_errors, None)
        # Error: neither string nor error instance
        self.assertRaises(BaseValidatorError, validator.report_errors, 3)

    def test_report_errors(self):
        validator = MultipleErrorValidator(11)
        validator.report_errors("Really!")
        # Now 3 errors
        self.assertEqual(len(validator.get_errors()), 3)

    def test_relocate_error_location(self):
        validator = MultipleErrorValidator(11)
        #validator.raise_last()
        error0 = validator.get_errors()[0]
        error1 = validator.get_errors()[1]
        # relocate
        #error0.relocate(location='Vormir')
        #print(error0.first_location)
        self.assertTrue(error0.first_location == 'MultipleErrorValidator')
        #self.assertTrue(error0.last_location=='Vormir')
        #self.assertEqual(error1.message, 'Halola')


class NewError(Base_Error):
    """ New error"""
    header = 'New_Error'

class Test_Report_Error_from_Different_Class(unittest.TestCase):
    def test_(self):
        validator = MultipleErrorValidator(11)
        new_error = NewError('A new error')
        validator.report_errors(new_error, location='HERE')
        # ErrorSample type is raised, not the original NewError
        self.assertRaises(ErrorSample, validator.raise_last_error)
