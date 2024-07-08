#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

qubit.index_range.py

PATH

[app_root]/qubit/index_range.py

INTRO

Index range is a widely used concept and object in qubit
based system. It is derived from bitrange.

CONTENT

LOG

Updated on 06 October 2021 | Created on 23 June 2020
"""
from bit.validators import BitrangeBoundValidator, BitrangeValidator
from .errors import IndexRangeBoundValidationError, IndexRangeValidationError


class IndexRangeBoundValidator(BitrangeBoundValidator):
    """ Index range bound validator

    Index range bound is a specialised bitrange used
    for qubits.

    VALIDATED DATA

    A validated index range bound is always in normal
    order. For example, if a given bound is [5,3],
    the validated bound shall be [3,5].
    """
    error_class = IndexRangeBoundValidationError

    def __init__(self, bound=None):
        super().__init__(bound=bound)
        self._validated_bound = None
        if self.is_valid:
            self.in_normal_order(bound)

    def in_normal_order(self, bound):
        """ Range limits in normal order """
        if bound[0] > bound[1]:
            self._validated_bound = [bound[1], bound[0]]
        else:
            self._validated_bound = bound

    def validated_data(self):
        return {
            'bound': self._validated_bound
        }


class IndexRangeValidator(BitrangeValidator):
    """ Index range validator """
    error_class = IndexRangeValidationError

    def __init__(self, noq=None, bound=None):
        super().__init__(number_of_bits=noq, bound=bound)
        self._validated_bound = None
        if self.is_valid:
            self.in_normal_order(bound)

    def in_normal_order(self, bound):
        """ Range limits in normal order """
        if bound[0] > bound[1]:
            self._validated_bound = [bound[1], bound[0]]
        else:
            self._validated_bound = bound

    def validated_data(self):
        return {
            'bound': self._validated_bound
        }
