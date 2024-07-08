"""
SUBPACK

Linear object

PATH

[app_root]/linear_space/linear_object/

INTRO

Linear object is a generic 2D matrix defined in linear
algebra.

Linear object is constructed as a container object that
stores a 2D numpy array, ofeen referred to as internal array.
The first dimension of the internal array contains subarrays.
Each subarray is interpreted as row, and within each subarray
the position of number is interpreted as column.

For example, a matrix
    [[1, 2, 3, 4, 5]
     [9, 10, 11, 12, 13]]
is a linear object that stores a two-dimensional array of
2 rows and 5 columns.

Vector is a specialised linear object that has one dimension
restricted to size 1. From this perspective, a vector is
a container that stores a 2D array, too. There are two types
of vectors, column vector and row vector.

Column vector - A column vector is a matrix that has only 1
column, or each row (subarray) contains exactly one scalar.

For example, matrix
    [[0.1 + 0.1j]
     [0.9 + 1.0j]
     [1.2 + 0.5j]]
is understood as a column vector containing 3 rows and thus 3
(complex) elements.

Row vector - A row vector is a matrix with only 1 row.
For example, matrix
    [[0.1, 0.2, 0.3, 0.4]]
is understood as a row vector containing 4 columns and thus
4 elements. Row and column vector are interconvertible via a
matrix transpose operation.

Matrix is a specialised linear object that has both dimensions
with sizes higher than 1.

IMPORTANT Linear object does NOT implement operator methods
such as `__add__` (+), `__sub__` (-), `__mul__` (*), etc,
as linear object class is not intended for direct instantiation.
Instead, a set of algebra functions, namely Linear Object Algebra
Function (LOAF) are provided to operate on linear object.

Deriving vector and matrix from one base class has the clear
advantage to reduce most algebraic operations to a minimal
number of functions. In fact, almost all linear algebra
operations in the down-stream packages are delegated or
redirected to algebra functions introduced here.

LOG

Updated on 27 September 2021 | Created on 22 April 2021
"""
from .linear_object import LinearObject
from .utils import is_column_like, is_row_like, is_scalar_like, is_matrix_like,\
    maximum, minimum
from .types import Column_Like, Row_Like, Matrix_Like
