"""
MODULE

linear_space.algebra.decorator.py

PATH

[app_root]/linear_space/algebra/decorator.py

INTRO

Decorator for pacakge-level algebra functions.
This decorator is a subclass of the decorator
used in linear-object algebra functions (LOAF).

CONTENT

LOG

Updated on 28 September 2021 | Created on 28 September 2021
"""
# decorator used in linear object
from linear_space.linear_object.decorator import algebra_function_decorator
from .errors import LinearSpaceAlgebraFunctionError


class linear_space_algebra_function_decorator(algebra_function_decorator):
    """ Linear space algebra function decorator """
    error_class = LinearSpaceAlgebraFunctionError
