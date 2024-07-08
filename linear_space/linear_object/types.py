#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.linear_object.types.py

PATH

[app_root]/linear_space/linear_object/types.py

INTRO

Artificially created linear object types are used to
categorise linear objects according to subtle features.

They are used solely for validation and in function
`isinstance`. Primary use case is inside algebra functions
to dispatch required methods with respect to fine features
defined by these types.

These artifical types are created using verifiers placed
inside method `__instancecheck__` of metaclass.

NOTE Types in this module are NEITHER subclassable NOR
instantiable. Any such attempt results in type error.

CONTENT

`Column_Like` - Column-like linear object, multiple rows
but only one column

`Row_Like` - Row-like linear object, multiple columns
but only one row

`Matrix_Like` - Matrix-like linear object, multiple columns
and multiple rows

LOG

Updated on 29 September 2021 | Created on 29 September 2021
"""

from common.mixins import Non_Instantiable_Mixin, Non_Subclassable_Mixin
from .linear_object import LinearObject
from .utils import is_column_like, is_row_like, is_matrix_like


# column-like object
class _ColumnLikeMeta_(Non_Subclassable_Mixin, type):
    """ Column-like object meta """
    def __instancecheck__(cls, _linobj):
        """ Manual instance check """
        ret = False
        if isinstance(_linobj, LinearObject) and is_column_like(_linobj):
            ret = True
        return ret

class Column_Like(Non_Instantiable_Mixin, metaclass=_ColumnLikeMeta_):
    """ Column-like linear object type """


# row-like linear object
class _RowLikeMeta_(Non_Subclassable_Mixin, type):
    """ Integer number meta """
    def __instancecheck__(cls, _linobj):
        """ Manual instance check """
        ret = False
        if isinstance(_linobj, LinearObject) and is_row_like(_linobj):
            ret = True
        return ret

class Row_Like(Non_Instantiable_Mixin, metaclass=_RowLikeMeta_):
    """ Row-like linear object type """


# matrix-like linear object
class _MatrixLikeMeta_(Non_Subclassable_Mixin, type):
    """ Integer number meta """
    def __instancecheck__(cls, _linobj):
        """ Manual instance check """
        ret = False
        if isinstance(_linobj, LinearObject) and is_matrix_like(_linobj):
            ret = True
        return ret

class Matrix_Like(Non_Instantiable_Mixin, metaclass=_MatrixLikeMeta_):
    """ Matrix-like linear object type """
