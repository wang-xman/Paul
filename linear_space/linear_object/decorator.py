"""
MODULE

linear_space.linear_object.decorator.py

PATH

[app_root]/linear_space/linear_object/decorator.py

INTRO

Decorator for linear algebra operation functions.
Function parameters are validated against their
declaration in decorator.

CONTENT

`algebra_function_decorator` - Decorator class for most
algebra functions; as it is not intended for direct
instantiation, class name consists of lower case and dash

LOG

Updated on 27 September 2021 | Created on 27 September 2021
"""
from common.function.decorators import FunctionInvocationDecorator
from .errors import LinearObjectAlgebraError

_MODULE_LOCATION_ = 'linear_space.linear_object.decorator'


class algebra_function_decorator(FunctionInvocationDecorator):
    """ Linear object algebra function decorator

    Decorator uses its arguments to declare the types of
    algebra function arguments.

    Parameters passed to an original algebra function are
    actually intercepted by `__call__` method of this class
    based decorator.
    """
    error_class = LinearObjectAlgebraError
