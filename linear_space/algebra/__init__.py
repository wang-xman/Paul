"""
SUBPACK

Linear-Space Algebra Functions (LSAF)

PATH

[app_root]/linear_space/algebra/

INTRO

Package-level linear-space algebra functions (LSAF)
applicable to scale, vector and matrice.

LSAF can be considered as specialised linear-object
algebra function (LOAF) for more refined objects.

Linear algebra functions or operations in down-stream
packages are largely based on LSAF.

LOG

Updated on 28 September 2021 | Created on 15 November 2020
"""
from .functions import scale, norm, inner, outer, kronecker, transpose, \
    complex_conjugate, hermitian_conjugate, matrix_product, matrix_add, \
    matrix_maker
