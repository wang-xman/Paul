#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.parameter.parameters.py

PATH

[app_root]/common/parameter/parameters.py

INTRO

Parameters

CONTENT

`Parameter` - Generic parameter class

`BoundedParameter` - Parameter with bounded values

LOG

Updated on 30 September 2021 | Created on 19 December 2020
"""
from .errors import ParameterError
from .validators import ParameterValidator, BoundedParameterValidator

_MODULE_LOCATION_ = 'common.parameter.parameters'


class Parameter:
    """ Parameter

    Generic parameter class for generic function invocation.
    Parameter is frequently used in, for example, quantum gates.

    CONSTRUCTOR

    `paramtype` (`class`) : class or a type of the parameter value

    `required` (Boolean) : a Boolean value with default to `True`
    to specify if a parameter is required; setting this value to
    `False` makes a parameter optional

    `default` (`paramtype`) : default parameter value that must be
    of the type as specified by `paramtype`

    ATTRIBUTES

    `self.__paramtype` : stores type of parameter

    `self.__required` : stores required or optional flag of
    a parameter

    `self.__default` : store the default value of the parameter
    """
    def __init__(self, paramtype=None, required=True, default=None):
        """ Constructor """
        validator = ParameterValidator(paramtype=paramtype, required=required,
                                       default=default)
        if validator.is_valid:
            self.__paramtype = paramtype
            self.__required = required
            self.__default = default
        else:
            validator.raise_last_error()

    @property
    def is_required(self):
        """ Verify if a parameter is required """
        return self.__required

    def validate(self, value):
        """ Validate a given value of the parameter """
        ret = False
        if isinstance(value, self.__paramtype):
            ret = True
        else:
            raise ParameterError(message="Parameter is not in the "+\
                    "required type.")
        return ret

    def is_correct_type(self, value):
        """ Verify if a value has the correct type as paramtype

        Return `True` (`False`) if a value is (not) of the
        same type as the given paramtype.
        """
        ret = False
        if isinstance(value, self.__paramtype):
            ret = True
        return ret

    def is_valid(self, value):
        return self.is_correct_type(value)

    @property
    def parameter_type(self):
        """ Return parameter type """
        return self.__paramtype

    @property
    def default_value(self):
        return self.__default


class BoundedParameter(Parameter):
    """ Parameter with maximum and minimum values

    Bounded parameter is a subclass of `Parameter` with a value
    bounded by the maximum and minimum.

    CONSTRUCTOR

    `paramtype` (class or type): type of the parameter

    `required` (Boolean): specify if a parameter is required; value
    can be either `True` or `False`, and its default is set to `True`

    `default` (`paramtype`): default value of the parameter; it must
    be of the type specified by `paramtype`

    `maximum` (`paramtype`): the upper limit of a bounded parameter

    `minimum` (`paramtype`): the lower limist of a bounded parameter,
    and it must be smaller than the maximum
    """
    def __init__(self, paramtype=None, required=True, default=None,
                 maximum=None, minimum=None):
        validator = BoundedParameterValidator(paramtype=paramtype,
                required=required, default=default, maximum=maximum,
                minimum=minimum)
        if validator.is_valid:
            super().__init__(paramtype=paramtype, required=required,
                             default=default)
            self.__maximum = maximum
            self.__minimum = minimum
        else:
            validator.raise_last_error()

    @property
    def minimum(self):
        return self.__minimum

    @property
    def maximum(self):
        return self.__maximum

    def validate(self, value):
        """ Validate a given value

        For a bounded parameter, the value must also be within the
        given bound.
        """
        ret = False
        # type has to be correct
        if self.is_correct_type(value):
            if self.__maximum is not None and self.__minimum is None:
                if value <= self.__maximum:
                    ret = True
            elif self.__maximum is None and not self.__minimum is None:
                if value >= self.__minimum:
                    ret = True
            elif not self.__maximum is None and not self.__minimum is None:
                if self.__minimum <= value <= self.__maximum:
                    ret = True
            else:
                ret = False
        else:
            ret = False
        return ret

    def is_valid(self, value):
        """ Customised is_valid verifier """
        return self.validate(value)
