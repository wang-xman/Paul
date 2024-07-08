#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.linear_object.utils.py

TODO What type of errors is needed?

PATH

[app_root]/linear_space/linear_object/utils.py

INTRO

Utility functions for linear object.

CONTENT

`maximum(obj)` - Returns the maximum value in a
list-like object

`minimum(obj)` - Returns the minimal value in a
list-like object

LOG

Updated on 06 October 2021 | Created on 22 April 2021
"""
from common.function.decorators import VerifierFunctionDecorator
from linear_space.numpy_lib import np_ndarray, np_amax, np_amin
from linear_space.number import is_number, is_integer
from .linear_object import LinearObject

_MODULE_LOCATION_ = 'linear_space.linear_object.utils'


@VerifierFunctionDecorator
def is_scalar_like(linobj):
    """ Verify if a linear object is scalar-like

    A scalar-like object is a 2D numpy array containing
    exactly 1 element, for example,
        [[1.0]]
    which is interpreted as a scalar.
    """
    ret = False
    if not isinstance(linobj, LinearObject):
        if is_number(linobj):
            ret = True
    elif linobj.get_ncols() == 1 and linobj.get_nrows() == 1:
        ret = True
    return ret


@VerifierFunctionDecorator
def is_column_like(linobj):
    """ Verify if a linear object is column-like

    Column-like object has 1 column and at least 2 rows.
    For example
        [[1]
         [2]]
    which is commonly know as column vector or vector.
    """
    ret = False
    if isinstance(linobj, LinearObject):
        if linobj.get_ncols() == 1 and linobj.get_nrows() > 1:
            ret = True
    return ret


@VerifierFunctionDecorator
def is_row_like(linobj):
    """ Verify if a linear object is column-like

    Row-like object has 1 row and at least 2 columns.
    For example
        [[1,2,3,4]]
    which is often referred to as row vector.
    """
    ret = False
    if isinstance(linobj, LinearObject):
        if linobj.get_nrows() == 1 and linobj.get_ncols() > 1:
            ret = True
    return ret


@VerifierFunctionDecorator
def is_matrix_like(linobj):
    """ Verify if a linear object is matrix-like

    Matrix-like object has at least 2 columns and 2 rows.
    """
    ret = False
    if isinstance(linobj, LinearObject):
        if linobj.get_ncols() > 1 and linobj.get_nrows() > 1:
            ret = True
    return ret


@VerifierFunctionDecorator
def is_flat_list_like(obj):
    """ Verify if an object is flat list-like (FLL)

    Flat list-like object has one of the following
    types: `list`, `tuple`, `Vector` and 1D `numpy.ndarray`.
    Element in the object must NOT be another container.

    For example,
        `[12,3,4], ['1','a',5], (0.5,0.4,'A')`
    are considered FLLobjects; yet
        `[[1], [2], 3, Vector()]` or `([1], (1,), 0.5,)`
    are not FLL.

    Vector object has an internal array that is a de facto 2D
    numpy array, but it is still considered as a FLL object.
    """
    ret = False
    if type(obj) in [list, tuple]:
        container_counter = 0
        # element must not be container
        for item in obj:
            if type(item) in [list, tuple]:
                container_counter += 1
            elif isinstance(item, (np_ndarray, LinearObject,)):
                container_counter +=1
            else:
                pass
        if container_counter == 0:
            ret = True
    elif isinstance(obj, np_ndarray):
        if obj.ndim == 1:
            ret = True
    elif isinstance(obj, LinearObject):
        if is_column_like(obj) or is_row_like(obj):
            ret = True
    else:
        ret = False
    return ret


def is_empty(obj):
    """ Verify if a FLL object is empty

    NOTE Vector class forbids instantiataion with an
    empty array.

    FIXME What if not FLL? Should I raise error
    """
    ret = False
    if is_flat_list_like(obj):
        if isinstance(obj, LinearObject):
            if is_column_like(obj) or is_row_like(obj):
                if obj.size == 0:
                    ret = True
        else:
            if len(obj) == 0:
                ret = True
    else:
        raise TypeError("Helper function is_empty is " +\
                "only applicable to list like objects.")
    return ret


@VerifierFunctionDecorator
def has_only_number(obj):
    """ Verify if an object contains only number

    Applicable to one-dimensional list, tuple, array
    and Vector.
    """
    ret = False
    non_number_counter = 0
    if type(obj) in [list, tuple]:
        for item in obj:
            if not is_number(item):
                non_number_counter += 1
        if non_number_counter == 0:
            ret = True
    elif isinstance(obj, (np_ndarray, LinearObject)):
        # linear object contains only numbers
        ret = True
    else:
        pass
    return ret


@VerifierFunctionDecorator
def has_only_integer(obj):
    """ Verify if an object contains only integer

    Applicable to one-dimensional list, tuple, array,
    and Vector.

    NOTE Current implementation of vector force-converts
    number into complex type and the elements of a vector
    are thus not integer.

    TODO What if ndarray is multiple dimensional?
    """
    ret = False
    non_integer_counter = 0
    if type(obj) in [list, tuple]:
        for item in obj:
            if not is_integer(item):
                non_integer_counter += 1
    elif is_column_like(obj) or is_row_like(obj):
        for item in obj.as_1d_list():
            if not is_integer(item):
                non_integer_counter += 1
    elif isinstance(obj, np_ndarray):
        for item in list(obj):
            if not is_integer(item):
                non_integer_counter += 1
    else:
        pass
    if non_integer_counter == 0:
        ret = True
    return ret


@VerifierFunctionDecorator
def has_double_entry(obj):
    """ Verify if an object contains double entries

    NOTE Current version is only applicable to
    one-dimensional list and tuple.

    FIXME So far only for list and tuple
    """
    ret = False
    if type(obj) in [list, tuple]:
        if len(obj) != len(set(obj)):
            ret = True
    return ret


# NOTE moved here from linear_space.utils.filters
def maximum(obj):
    """ Maximal value in a FLL object """
    ret = None
    if type(obj) in [list, tuple]:
        if has_only_number(obj):
            if isinstance(obj, list):
                ret = np_amax(obj)
            # tuple
            else:
                ret = np_amax(list(obj))
        else:
            raise TypeError("Function 'maximum' is " +\
                    "only applicable to a list like "  +\
                    "object that contains only numbers.")
    elif isinstance(obj, np_ndarray):
        ret = np_amax(obj)
    #elif isinstance(obj, (ColumnVector, RowVector,)):
    elif is_column_like(obj) or is_row_like(obj):
        ret = np_amax(obj.as_1d_list())
    else:
        raise TypeError("Function 'maximum' is only " +\
                "applicable to list-like objects.")
    return ret


def minimum(obj):
    """ Minimal value in a FLL object """
    ret = None
    if type(obj) in [list, tuple]:
        if has_only_number(obj):
            if isinstance(obj, list):
                ret = np_amin(obj)
            # tuple
            else:
                ret = np_amin(list(obj))
        else:
            raise TypeError("Function 'minimum' is " +\
                    "only applicable to a list like "  +\
                    "object that contains only number.")
    elif isinstance(obj, np_ndarray):
        ret = np_amin(obj)
    #elif isinstance(obj, (ColumnVector, RowVector,)):
    elif is_column_like(obj) or is_row_like(obj):
        ret = np_amin(obj.as_1d_list())
    else:
        raise TypeError("Helper function 'minimum' is " +\
                "only applicable to a list-like object.")
    return ret
