#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.parameter.py

TODO Are these int types necessary? Already basic numeric types
defined in number, they are more general.

PATH

[app_root]/gate/parameter.py

INTRO

Parameters used in quantum gate application

LOG

Updated on 02 July 2021 | Created on 20 April 2021
"""
from common.parameter import Parameter, BoundedParameter
from linear_space.number import is_integer, is_float
from qubit import QubitState


class GateParameter(Parameter):
    """ Base gate parameter class """
    def is_valid(self, value):
        return self.is_correct_type(value)


class IntegerParameter(Parameter):
    """ Integer type parameter

    An `IntegerParameter` declares and validates
    an integer number.

    CONSTRUCTOR

    `default` (integer): default value given to the parameter
    """
    _parameter_type = int

    def __init__(self, default=None):
        super().__init__(paramtype=self._parameter_type, default=default)

    def is_correct_type(self, value):
        """ Override base class `is_correct_type` method

        In base class, this method only checks against
        the paramtype.

        However, there are several integer types introduced
        in numpy which must be taken into account.
        """
        ret = False
        if is_integer(value):
            ret = True
        return ret


class FloatParameter(Parameter):
    """ Float type parameter

    An `FloatParameter` declares and validates a
    float number.

    CONSTRUCTOR

    `default` (float): default value given to the parameter
    """
    _parameter_type = float

    def __init__(self, default=None):
        super().__init__(paramtype=self._parameter_type, default=default)

    def is_correct_type(self, value):
        """ Override base class `is_correct_type` method

        In base class, this method only checks against
        the paramtype.

        However, there are several float types introduced
        in numpy which must be taken into account.
        """
        ret = False
        if is_float(value):
            ret = True
        return ret


class InputQubitState(Parameter):
    """ Input qubit state parameter

    An `InputQubitState` parameter must be an instance
    of class `QubitState` or its subclass.

    CONSTRUCTOR

    `default` (`QubitState` or its subclass) : default
    qubit state instance given to the parameter
    """
    _parameter_type = QubitState

    def __init__(self, default=None):
        super().__init__(paramtype=self._parameter_type, default=default)


class QubitIndex(BoundedParameter):
    """ Qubit index parameter

    An `QubitIndex` parameter is a positive integer and
    is thus bounded from below. Scientific index scheme
    applies to the qubit indices, and the minimum value
    of a qubit index is thus defaulted to 0.

    CONSTRUCTOR

    `default` (integer): default value give to parameter

    `minimum` (integer): lower bound of the parameter value;
    default to 0

    `maximum` (integer): upper bound of the parameter vlaue;
    default to `None`
    """
    _parameter_type = int

    def __init__(self, default=None, minimum=0, maximum=None):
        """ """
        super().__init__(paramtype=self._parameter_type, required=True,
                         default=default, maximum=maximum, minimum=int(minimum))

    def is_correct_type(self, value):
        ret = False
        if is_integer(value):
            ret = True
        return ret


class ControlIndexList(Parameter):
    """ Control index list

    Control bits organised as a list of (index, value)
    tuples. Its type is obviously set to `list`.

    Used extensively in multiple-controlled gate operations.
    """
    _parameter_type = list

    def __init__(self, default=None):
        super().__init__(paramtype=self._parameter_type, default=default)


class NumberOfQubits(BoundedParameter):
    """ Number of qubits parameter

    An `NumberOfQubits` parameter is a positive
    integer that must be greater than 1.

    The minimum value of a number-of-qubits is
    thus defaulted to 1.

    CONSTRUCTOR

    `default` (integer): default value give to parameter

    `minimum` (integer): lower bound of the parameter value;
    default to 1

    `maximum` (integer): upper bound of the parameter vlaue;
    default to `None`
    """
    _parameter_type = int

    def __init__(self, default=None, minimum=1, maximum=None):
        """ """
        super().__init__(paramtype=self._parameter_type, required=True,
                         default=default, maximum=maximum, minimum=int(minimum))

    def is_correct_type(self, value):
        ret = False
        if is_integer(value):
            ret = True
        return ret
