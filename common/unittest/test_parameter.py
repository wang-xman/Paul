"""
Module under test:
    common.parameter.py

Main test:
    Parameter object

Updated:
    19 April 2021
"""
import unittest

from common.parameter import ParameterValidator, Parameter, ParameterError
from common.parameter import BoundedParameterValidator, BoundedParameter


class TrialParameterType:
    pass


class TestParameterValidator(unittest.TestCase):
    def test_paramtype_missing(self):
        validator = ParameterValidator(paramtype=None)
        # Error: parameter type can not be None
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_wrong_required_flag_value(self):
        validator = ParameterValidator(paramtype=int, required='Yes')
        # Error: required switch can either be True or False
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_default_value_mismatched_type(self):
        validator = ParameterValidator(paramtype=int, required=False, default='an')
        # Error: type of default value is not of the paramtype
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_success(self):
        validator = ParameterValidator(paramtype=TrialParameterType,
            required=False, default=TrialParameterType())
        # Okay
        self.assertTrue(validator.is_valid)


class TestParameter(unittest.TestCase):
    def test(self):
        default_value = TrialParameterType()
        param = Parameter(paramtype=TrialParameterType, required=False,
                          default=default_value)
        self.assertFalse(param.is_required)
        self.assertTrue(isinstance(param.default_value,TrialParameterType))
        self.assertFalse(param.is_correct_type(90))
        self.assertRaises(ParameterError, param.validate, '1b')
        self.assertTrue(param.parameter_type is TrialParameterType)


class TestBoundedParameterValidator(unittest.TestCase):
    def test_pass(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=1,
            maximum=10,
            minimum=0
        )
        self.assertTrue(validator.is_valid)

    def test_no_bounds(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=1,
            maximum=None,
            minimum=None
        )
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_only_upper_bound(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=1,
            maximum=10,
            minimum=None
        )
        self.assertTrue(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_only_upper_bound_but_out(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=12,
            maximum=10,
            minimum=None
        )
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_only_lower_bound_but_out(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=12,
            maximum=None,
            minimum=20
        )
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_bound_error(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=None,
            maximum=10,
            minimum=20
        )
        # Error: minimum exceed maximum
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_default_value_wrong_type(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=0.5,
            maximum=10,
            minimum=2
        )
        # Error: defalt value wrong type
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_upper_bound_wrong_type(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=5,
            maximum=10.2,
            minimum=2
        )
        # Error: maximum wrong type
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])

    def test_lower_bound_wrong_type(self):
        ptype = int
        validator = BoundedParameterValidator(
            paramtype=ptype,
            required=True,
            default=5,
            maximum=10,
            minimum=2.5
        )
        # Error: minimum wrong type
        self.assertFalse(validator.is_valid)
        #print(validator.report_errors()[0])


class TestBoundedParameter(unittest.TestCase):
    def test_success_with_default(self):
        ptype = int
        param = BoundedParameter(
            paramtype=ptype,
            required=True,
            default=5,
            maximum=10,
            minimum=0
        )
        self.assertTrue(param.default_value == 5)
        self.assertTrue(param.maximum == 10)
        self.assertTrue(param.minimum == 0)

    def test_success_with_upper(self):
        ptype = int
        param = BoundedParameter(
            paramtype=ptype,
            required=True,
            default=5,
            maximum=10,
            minimum=None
        )
        self.assertTrue(param.default_value == 5)
        self.assertTrue(param.maximum == 10)
        self.assertTrue(param.minimum is None)

    def test_success_with_lower(self):
        ptype = int
        param = BoundedParameter(
            paramtype=ptype,
            required=True,
            default=5,
            maximum=None,
            minimum=1
        )
        self.assertTrue(param.default_value == 5)
        self.assertTrue(param.maximum is None)
        self.assertTrue(param.minimum == 1)


class TestBoundedParameter_ValidateMethod(unittest.TestCase):
    def test_with_lower_bound(self):
        ptype = int
        param = BoundedParameter(
            paramtype=ptype,
            required=True,
            default=5,
            maximum=None,
            minimum=1
        )
        self.assertTrue(param.validate(6))
        self.assertFalse(param.validate(0))
        self.assertFalse(param.validate(-1))
        self.assertFalse(param.validate(0.5))
        self.assertFalse(param.validate('string'))

    def test_with_upper_bound(self):
        ptype = int
        param = BoundedParameter(
            paramtype=ptype,
            required=True,
            default=5,
            maximum=10,
            minimum=None
        )
        self.assertTrue(param.validate(9))
        self.assertTrue(param.validate(0))
        self.assertTrue(param.validate(-2))
        self.assertFalse(param.validate('string'))
        self.assertFalse(param.validate(11))

    def test_with_both_bound(self):
        ptype = int
        param = BoundedParameter(
            paramtype=ptype,
            required=True,
            default=5,
            maximum=10,
            minimum=1
        )
        self.assertTrue(param.validate(9))
        self.assertFalse(param.validate(0))
        self.assertFalse(param.validate(-2))
        self.assertFalse(param.validate('string'))
        self.assertFalse(param.validate(11))
