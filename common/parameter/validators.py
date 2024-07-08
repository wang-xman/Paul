#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.parameter.validators.py

PATH

[app_root]/common/parameter/validators.py

INTRO

Valdiators for various parameter classes

CONTENT


LOG

Updated on 30 September 2021 | Created on 19 December 2020
"""
import inspect
from common.validator import Base_Validator
from .errors import ParameterValidationError

_MODULE_LOCATION_ = 'common.parameter.validators'


class ParameterValidator(Base_Validator):
    """ Validate parameter instantiation

    Argument `paramtype` is required and it cannot be `None`. By default,
    the `required` switch is set to `True` and the value for this switch
    can be either `True` or `False`. The `default` argument is to store
    the default value of a parameter and it must be in the same type
    specified by `paramtype`.
    """
    error_class = ParameterValidationError
    error_location = _MODULE_LOCATION_ + '.ParameterValidator'

    def __init__(self, paramtype=None, required=True, default=None):
        """ """
        super().__init__()
        self.validate(paramtype, required, default)

    def validate(self, paramtype, required, default):
        if paramtype is None:
            self.report_errors("Parameter argument 'paramtype' is " +\
                    "missing. Parameter type cannot be None.",
                    location=self.error_location)
        else:
            if not inspect.isclass(paramtype):
                self.report_errors("Parameter argument 'paramtype' " +\
                        "must be a type or class.",
                    location=self.error_location)

        if not required in [True, False]:
            self.report_errors("Value to argument 'required' can " +\
                    "only be True or False.",
                    location=self.error_location)

        if default is not None:
            if not isinstance(default, paramtype):
                self.report_errors("Parameter default value is " +\
                        "inconsistent with the declared parameter type.",
                        location=self.error_location)


class BoundedParameterValidator(ParameterValidator):
    """ Bounded parameter validator

    Bounded parameter has upper and (or) lower limits.
    This validator subclasses from `ParameterValidator`.
    """
    error_class = ParameterValidationError
    error_location = _MODULE_LOCATION_ + '.BoundedParameterValidator'

    def __init__(self, paramtype=None, required=True, default=None,
                 maximum=None, minimum=None):
        super().__init__(paramtype=paramtype, required=required,
                         default=default)
        if len(self.get_errors()) == 0:
            # if maximum and minimum values exist, they must be valid
            if not maximum is None and minimum is None:
                if not isinstance(maximum, paramtype):
                    self.report_errors("Parameter maximum isn't of " +\
                            "the required type.",
                            location=self.error_location+'.__init__')
                if not default is None:
                    if default > maximum:
                        self.report_errors('Default value provided ' +\
                                'to parameter is greater than the ' +\
                                'specified upper bound.',
                                location=self.error_location+'.__init__')
            elif not minimum is None and maximum is None:
                if not isinstance(minimum, paramtype):
                    self.report_errors("Parameter maximum isn't of " +\
                            "the required type.",
                            location=self.error_location+'.__init__')
                if not default is None:
                    if default < minimum:
                        self.report_errors('Default value provided ' +\
                                'to parameter is less than the ' +\
                                'specified lower bound.',
                                location=self.error_location+'.__init__')
            # if bound exits, it must be logical
            elif not maximum is None and not minimum is None:
                if not isinstance(maximum, paramtype):
                    self.report_errors("Parameter maximum isn't of " +\
                            "the required type.",
                            location=self.error_location+'.__init__')
                if not isinstance(minimum, paramtype):
                    self.report_errors("Parameter minimum isn't of " +\
                            "the required type.",
                            location=self.error_location+'.__init__')
                if minimum > maximum:
                    self.report_errors("Parameter minimum exceeds " +\
                            "its maximum.",
                            location=self.error_location+'.__init__')
                if not default is None:
                    if default < minimum or default > maximum:
                        self.report_errors("Default is outside " +\
                                "the bound.",
                                location=self.error_location+'.__init__')
            elif maximum is None and minimum is None:
                self.report_errors('Bounded parameter must have at ' +\
                        'least either a upper or lower limit.',
                        location=self.error_location+'.__init__')
            else:
                pass
