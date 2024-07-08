"""
MODULE

quantum_stater.algebra.decorator.py

PATH

[app_root]/quantum_state/algebra/decorator.py

INTRO

Quantum State Algebra Function Decorator - QSAF_Decorator.

Decorator for quantum state algebra functions.
This decorator is a subclass of the decorator
used in linear-object algebra functions (LOAF).

CONTENT

LOG

Updated on 28 September 2021 | Created on 28 September 2021
"""
# decorator used in linear object
from linear_space.linear_object.decorator import algebra_function_decorator

from .errors import QuantumStateAlgebraFunctionError


class quantum_state_algebra_function_decorator(algebra_function_decorator):
    """ Quantum state algebra function decorator """
    error_class = QuantumStateAlgebraFunctionError
