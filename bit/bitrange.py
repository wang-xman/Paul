#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

bit.bitrange.py

PATH

[app_root]/bit/bitrange.py

INTRO

Bitrange is initialised by a list of two integers,
such as [5,10], which set the boundary of the range.
This list is referred to as range bound, or bound.

Both integers are scientific indices and compatible
with total number of bits. Bitrange defined by this
list represents all integers between and include the
limits. For [5,10], it represents [5,6,7,8,9,10].

If the first integer is less than the second, such as
[5,10], this range is said to be in 'normal order',
opposite to the 'reversed' order, for example, [10,5].

Use of list coincides with the mathematical convention
that a range presented in a square brackets includes
values at the boundary, i.e. range [2, 10] includes 2
and 10.

LOG

Updated on 05 October 2021 | Created on 27 September 2021
"""
from linear_space.linear_object.utils import maximum, minimum
from .validators import BitrangeValidator

_MODULE_LOCATION_ = 'bit.bitrange'


class Bitrange:
    """ Bitrange """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.Bitrange'

    def __init__(self, number_of_bits=None, bound=None):
        """ Bitrange :: init """
        validator = BitrangeValidator(number_of_bits=number_of_bits,
                                           bound=bound)
        if validator.is_valid:
            self._bound = bound
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    @property
    def is_normal_range(self):
        """ Bitrange :: Check if range is normal """
        ret = False
        if self._bound[1] >= self._bound[0]:
            ret = True
        return ret

    def as_normal_range(self):
        """ Bitrange :: Returns a normal range object """
        lower_bound = None
        upper_bound = None
        if self.is_norm_range:
            lower_bound = self._bound[0]
            upper_bound = self._bound[1]
        else:
            lower_bound = self._bound[1]
            upper_bound = self._bound[0]
        return range(lower_bound, upper_bound + 1, 1)

    def as_range(self):
        """ Bitrange :: Returns a range object

        Respects the bound order.
        """
        ret = None
        if self.is_normal_range:
            ret = range(self._bound[0], self._bound[1] + 1, 1)
        else:
            # respect reversed order
            ret = range(self._bound[0], self._bound[1] - 1, -1)
        return ret

    @property
    def bound(self):
        """ Bitrange :: Returns bound """
        return self._bound

    @property
    def upper_bound(self):
        """ Bitrange :: Returns upper bound """
        return maximum(self._bound)

    @property
    def lower_bound(self):
        """ Bitrange :: Returns lower bound """
        return minimum(self._bound)

    def as_list(self):
        """ Bitrange :: Returns a list of indices """
        return list(self.as_range())

    def number_of_bits_in_range(self):
        """ Bitrange :: Number of bits in range """
        return maximum(self._bound) - minimum(self._bound) + 1
