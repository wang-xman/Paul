"""
MODULE

linear_space.linear_object.errors.py

PATH

[app_root]/linear_space/linear_object/errors.py

INTRO

CONTENT

`LinearObjectAlgebraError` - Error class used in algebra
functions

LOG

Updated on 28 September 2021 | Created on 27 September 2021
"""
from linear_space.base import LinearSpaceBaseError, \
    LinearSpaceBaseValidationError, LinearSpaceBaseAlgebraError


class LinearObjectValidationError(LinearSpaceBaseValidationError):
    """ Error raised in linear object validator

    ENTRY

    `validators.LinearObjectValidator`
    """
    header = 'Linear_Object_Validation_Error'


class LinearObjectError(LinearSpaceBaseError):
    """ Error raised linear object error

    ENTRY

    `linear_object.LinearObject`
    """
    header = 'Linear_Object_Error'


class LinearObjectAlgebraError(LinearSpaceBaseAlgebraError):
    """ Error raised in algebra functions """
    header = 'Linear_Object_Algebra_Error'
