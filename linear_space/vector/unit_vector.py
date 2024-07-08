#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.vector.unit_vector.py

PATH

[app_root]/linear_space/vector/unit_vector.py

INTRO

Unit vector is a subclass of column vector.
Unit vector has length 1.

CONTENT

`UnitVector` - Unit vector is a column vector that
has length 1 and is thus a subclass of `ColumnVector`

LOG

Updated on 24 September 2021 | Created on 07 November 2020
"""
from .column_vector import ColumnVector

_MODULE_LOCATION_ = 'linear_space.vector.unit_vector'


class UnitVector(ColumnVector):
    """ Unit vector

    A unit vector has a length 1, or the two-norm is 1.
    Generic unit vector does not always have a binary
    representation.

    Required methods `size` and `element` are inherited
    from column vector.

    Instantiation of a unit vector is the same as vector,
    but normalisation is enforced.
    """
    def __init__(self, array=None):
        """ Unit Vector :: Initialiser """
        try:
            super().__init__(array=array)
            self.normalize()
        except Exception as err:
            raise err.relocate(_MODULE_LOCATION_+'UnitVector.__init__')
