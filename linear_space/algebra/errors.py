"""
MODULE

linear_space.algebra.errors.py

PATH

[app_root]/linear_space/algebra/errors.py

INTRO

Linear space algebra function error (LAFE).

CONTENT

`LinearSpaceAlgebraFunctionError` - Error class used in all
linear-space algebra functions; also known as LSAFE

LOG

Updated on 28 September 2021 | Created on 28 September 2021
"""
from linear_space.base import LinearSpaceBaseAlgebraError


class LinearSpaceAlgebraFunctionError(LinearSpaceBaseAlgebraError):
    """ LSAF function error a.k.a LSAFE """
    header = 'Linear_Space_Algebra_Function_Error'
