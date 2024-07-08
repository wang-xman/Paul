#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

linear_space.algebra.functions.py

PATH

[app_root]/linear_space/algebra/functions.py

INTRO

Linear-space algebra functions (LSAF) for number,
vector or matrix.

CONTENT

`scale(factor, obj)` - Scale a linear object by a factor;
factor must be a number

`norm(obj)` - Calculate the two-norm of the given object;
the object must be flat-list like; returns a number

`inner()` - Inner product of vectors

`outer(vec_a, vec_b)` - Outer product of two vectors and
the result is a matrix object

`kronecker(obj_a, obj_b)` - Kronecker product of two object;
the objects can be either `Vector` or `Matrix` instances

`transpose(obj)` - Transpose a vector or a matrix; only for
`Vector` or `Matrix` instances

`complex_conjugate(obj)` - Complex conjugate of a vector or
matrix; applicable to only `Vector` or `Matrix` instances

`hermitian_conjugate(obj)` - Hermitian conjugate (transpose of
complex conjugated) of vector or matrix; applicable to only
`Vector` and `Matrix` instances

`matrix_product(obj_a, obj_b)` - Matrix product between a
matrix and a vector or matrix; applicable only to `Vector`
or `Matrix` instances; return can be a scalar, vector, or matrix

`matrix_maker(list_of_matrices, method)` - Construct a matrix
using a list of matrices via designated method

LOG

Updated on 30 September 2021 | Created on 15 April 2021
"""
from linear_space.numpy_lib import np_ndarray, np_array, np_norm
from linear_space.number import is_number, is_one
from linear_space.linear_object.linear_object import LinearObject
from linear_space.linear_object.utils import is_column_like, is_row_like, \
    is_matrix_like, is_scalar_like, is_flat_list_like, has_only_number
# use LOAF - linear object algebra function
import linear_space.linear_object.algebra as LOAF

from linear_space.vector import BaseVector, ColumnVector, UnitVector, RowVector
from linear_space.matrix import Matrix, SquareMatrix, IdentityMatrix

from .errors import LinearSpaceAlgebraFunctionError as LSAFE
from .decorator import linear_space_algebra_function_decorator as LSAF_Decorator

_MODULE_LOCATION_ = 'linear_space.algebra.functions'


def scale(factor, obj):
    """ Scale object by a scalar/number """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.scale'

    ret = None
    try:
        if is_number(obj):
            ret = factor * obj
        elif isinstance(obj, LinearObject):
            new_array = factor * obj.as_array()
            if isinstance(obj, UnitVector):
                if is_one(factor):
                    ret = obj
                else:
                    ret = ColumnVector(array=new_array)
            elif isinstance(obj, ColumnVector):
                ret = ColumnVector(array=new_array)
            elif isinstance(obj, RowVector):
                ret = RowVector(array=new_array)
            elif isinstance(obj, IdentityMatrix):
                if is_one(factor):
                    ret = obj
                else:
                    ret = SquareMatrix(array=new_array)
            elif isinstance(obj, SquareMatrix):
                ret = SquareMatrix(array=new_array)
            elif isinstance(obj, Matrix):
                ret = Matrix(array=new_array)
            else:
                pass
        else:
            raise LSAFE('Scale function is applicable ' +\
                    'only to scalar, vector and matrix objects.',
                    location=_ERROR_LOCATION_)
    except Exception as err:
        raise err
    return ret


def norm(obj):
    """ Two-norm

    Applicable to number, vector, numpy array,
    flat tuple and list.

    RETURN
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.norm'

    ret = None
    try:
        if isinstance(obj, BaseVector):
            ret = obj.norm
        elif isinstance(obj, np_ndarray):
            if obj.ndim == 1:
                ret = np_norm(obj)
            else:
                raise LSAFE('Two norm function is only ' +\
                        'for flat-list-like array of numbers.' +\
                        'The numpy array passed in is not 1D.',
                        location=_ERROR_LOCATION_)
        elif isinstance(obj, list):
            if is_flat_list_like(obj) and has_only_number(obj):
                ret = np_norm(np_array(obj))
            else:
                raise LSAFE('Two norm function is only '  +\
                        'for flat-list-like array of numbers. ' +\
                        'List contains non-numeric values.',
                        location=_ERROR_LOCATION_)
        elif isinstance(obj, tuple):
            if is_flat_list_like(obj) and has_only_number(obj):
                ret = np_norm(np_array(list(obj)))
            else:
                raise LSAFE('Two norm function is only '  +\
                        'for flat-list-like array of numbers. ' +\
                        'Tuple contains non-numeric values.',
                        location=_ERROR_LOCATION_)
        elif is_number(obj):
            ret = np_norm(obj)
        else:
            raise LSAFE('Two norm function is only ' +\
                    'for flat-list-like array or numbers.',
                    location=_ERROR_LOCATION_)
    except Exception as err:
        raise err
    return ret


@LSAF_Decorator(
    argument_type={
        'left_vector': BaseVector,
        'right_vector': BaseVector
    }
)
def inner(left_vector, right_vector):
    """ Inner product of vectors

    Left vector shall always be a row vector; right vector
    shall always be a column vector. If not, hermitian
    conjugate transforms it. Using Dirac braket notation,
    <row|col> where <row| referrs to row vector and |col>
    stands for column vector.

    Only applicable to vectors.

    ARGUMENTS

    `left_vector` (`BaseVector`) : vector on the left side
    of the inner product; if a column vector, its hermitian
    conjugate is used

    `right_vector` (`BaseVector`) : vector on the right side
    of the inner product; if a row vector, its hermitian
    conjugate is used

    RETURN

    A number scalar.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.inner'

    innerprod = None
    try:
        innerprod = LOAF.inner(left_vector, right_vector).as_array()[0][0]
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)
    return innerprod


@LSAF_Decorator(
    argument_type={
        'left_vector': BaseVector,
        'right_vector': BaseVector
    }
)
def outer(left_vector, right_vector):
    """ Outer product of vectors

    Symbolicaly `left_vector` o `right_vector`, where o
    represents the outer product. In Dirac notation, an
    outer product is |left_vector><right_vector|,
    meaning the left vector shall be column-like and the
    right vector must be row-like.

    Applicable to vector-like object with complex elements.
    Outer product of two vectors is a matrix. As both vectors
    contain complex elements, `right_vector` is hermitian
    conjugated.

    ARGUMENTS

    `left_vector` (`BaseVector`) : the vector on the left side
    of the outer product

    `right_vector` (`BaseVector`): the vector on the right side
    of the outer product; its hermitian conjugate (complex
    conjugate then transposed) is used

    REFERENCE

    https://en.wikipedia.org/wiki/Outer_product
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.outer'

    ret = None
    try:
        linobj = LOAF.outer(left_vector, right_vector)
        if len(linobj.as_array()) == len(linobj.as_array()[0]):
            ret = SquareMatrix(array=linobj.as_array())
        else:
            ret = Matrix(array=linobj.as_array())
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)
    return ret


@LSAF_Decorator(
    argument_type={
        'left_object': LinearObject,
        'right_object': LinearObject
    }
)
def kronecker(left_object, right_object):
    """ Kronecker product of two objects

    Kornecker product is applicable to both `BaseVector`
    and `Matrix` objects. Use of other types causes error.

    Kronecker function returns either a `ColumnVector`
    (`UnitVector`), `RowVector` or `Matrix` (`SquareMatrix`)
    instance.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.kronecker'

    ret = None
    try:
        linobj = LOAF.kronecker(left_object, right_object)
        if is_column_like(linobj):
            ret = ColumnVector(array=linobj.as_array())
            if is_one(ret.norm):
                ret = UnitVector(array=linobj.as_array())
        elif is_row_like(linobj):
            ret = RowVector(array=linobj.as_array())
        elif is_matrix_like(linobj):
            if linobj.get_ncols() == linobj.get_nrows():
                ret = SquareMatrix(array=linobj.as_array())
            else:
                ret = Matrix(array=linobj.as_array())
        else:
            raise LSAFE('Kronecker product of two '+\
                    'linear objects results in a non '   +\
                    'linear object.', location=_ERROR_LOCATION_)
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)
    return ret


@LSAF_Decorator(argument_type={'obj': LinearObject})
def transpose(obj):
    """ Transpose vector or matrix

    Transpose reshape the object but doesn't perform
    complex conjugate. Following rules apply:

    ColumnVector -> RowVector
    RowVector -> ColumnVector
    IdentityMatrix -> IdentityMatrix (returns itself)
    SquareMatrix -> SquareMatrix
    Matrix -> Matrix
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.transpose'

    ret = None
    try:
        if isinstance(obj, ColumnVector):
            ret = RowVector(array=LOAF.transpose(obj).as_array())
        elif isinstance(obj, RowVector):
            ret = ColumnVector(array=LOAF.transpose(obj).as_array())
        elif isinstance(obj, IdentityMatrix):
            ret = obj
        elif isinstance(obj, SquareMatrix):
            ret = SquareMatrix(array=LOAF.transpose(obj).as_array())
        elif isinstance(obj, Matrix):
            ret = Matrix(array=LOAF.transpose(obj).as_array())
        else:
            raise LSAFE('Transpose function is applicable ' +\
                    'only to vector and matrix objects.',
                    location=_ERROR_LOCATION_)
    except Exception as err:
        raise err
    return ret


@LSAF_Decorator(argument_type={'obj': LinearObject})
def complex_conjugate(obj):
    """ Complex conjugate

    Complex conjugate conserves the shape.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.complex_conjugate'

    ret = None
    try:
        if isinstance(obj, ColumnVector):
            ret = ColumnVector(array=LOAF.complex_conjugate(obj).as_array())
        elif isinstance(obj, RowVector):
            ret = RowVector(array=LOAF.complex_conjugate(obj).as_array())
        elif isinstance(obj, IdentityMatrix):
            ret = obj
        elif isinstance(obj, SquareMatrix):
            ret = SquareMatrix(array=LOAF.complex_conjugate(obj).as_array())
        elif isinstance(obj, Matrix):
            ret = Matrix(array=LOAF.complex_conjugate(obj).as_array())
        else:
            raise LSAFE('Complex conjugate function ' +\
                    'is applicable only to vector and '     +\
                    'matrix objects.', location=_ERROR_LOCATION_)
    except Exception as err:
        raise err
    return ret


@LSAF_Decorator(argument_type={'obj': LinearObject})
def hermitian_conjugate(obj):
    """ Hermitian conjugate

    Hermitian conjugate reshapes the object.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.hermitian_conjugate'

    ret = None
    try:
        if isinstance(obj, IdentityMatrix):
            ret = obj
        elif isinstance(obj, (ColumnVector, RowVector, SquareMatrix, Matrix)):
            ret = complex_conjugate(transpose(obj))
        else:
            raise LSAFE('Hermitian conjugate function is ' +\
                    'applicable only to vector and matrix objects.',
                    location=_ERROR_LOCATION_)
    except Exception as err:
        raise err
    return ret


@LSAF_Decorator(
    argument_type={
        'left_object': LinearObject,
        'right_object': LinearObject
    }
)
def matrix_product(left_object, right_object):
    """ Matrix product

    FIXME Tidy up a bit.

    If left object is row-like and the right is column-like,
    the result is a scalar (packed as a 2D numpy array),
    equivalent to inner product.

    If the left object is column-like and the right object
    is row-like, the result is a matrix, equivalent to outer
    product.

    If both objects are matrix-like, the result is a matrix,
    indicating regular matrix product.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.matrix_product'

    ret = None
    if left_object.get_ncols() == right_object.get_nrows():
        try:
            linobj = LOAF.dot(left_object, right_object)
            if is_column_like(linobj):
                ret = ColumnVector(array=linobj.as_array())
                if ret.is_normalized:
                    ret = UnitVector(array=linobj.as_array())
            elif is_row_like(linobj):
                ret = RowVector(array=linobj.as_array())
            elif is_matrix_like(linobj):
                if linobj.get_ncols() == linobj.get_nrows():
                    ret = SquareMatrix(array=linobj.as_array())
                else:
                    ret = Matrix(array=linobj.as_array())
            elif is_scalar_like(linobj):
                ret = linobj.as_array()[0][0]
            else:
                raise LSAFE('Matrix product ' +\
                        'created a non linear object.',
                        location=_ERROR_LOCATION_)
        except Exception as err:
            raise err.relocate(_ERROR_LOCATION_)
    else:
        raise LSAFE('Matrix product requires the ' +\
                'number of columns of the left object '  +\
                'matches the number of rows of the right object.',
                location=_ERROR_LOCATION_)
    return ret


def matrix_add(left_object, right_object):
    """ Matrix addition

    Matrix addition is applicable to vector and matrix.

    Matrix addition requires both object to have identical
    size along both row and column. Outcome of matrix
    addition has the same shape as the input object.

    If both objects are numbers, the result is a number.

    If both objects are row-like, the result is also
    row-like object.

    If both objects are column-like, the result is also
    column-like object.

    If both objects are matrix-like, the result is a matrix.

    NOTE Not unit tested! But successfully used in gate operations.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.matrix_add'
    ret = None
    if is_number(left_object) and is_number(right_object):
        ret = left_object + right_object
    elif is_scalar_like(left_object) and is_scalar_like(right_object):
        ret = left_object.as_array()[0][0] + right_object.as_array()[0][0]
    elif isinstance(left_object, LinearObject) \
            and isinstance(right_object, LinearObject):
        if left_object.size == right_object.size:
            try:
                linobj = LOAF.add(left_object, right_object)
                if is_column_like(linobj):
                    ret = ColumnVector(array=linobj.as_array())
                    if ret.is_normalized:
                        ret = UnitVector(array=linobj.as_array())
                elif is_row_like(linobj):
                    ret = RowVector(array=linobj.as_array())
                elif is_matrix_like(linobj):
                    if linobj.get_ncols() == linobj.get_nrows():
                        ret = SquareMatrix(array=linobj.as_array())
                    else:
                        ret = Matrix(array=linobj.as_array())
                else:
                    raise LSAFE('Matrix addition ' +\
                            'created a non linear object.',
                            location=_ERROR_LOCATION_)
            except Exception as err:
                raise err.relocate(_ERROR_LOCATION_)
        else:
            raise LSAFE('Matrix addition requires two ' +\
                    'linear objects to have the same size '   +\
                    'along either dimension.', location=_ERROR_LOCATION_)
    else:
        raise LSAFE('Matrix addition is applicable ' +\
                'to only scalar, vector, and matrix.',
                location=_ERROR_LOCATION_)
    return ret


# FIXME Function name doesn't really fit as a algebra function
def matrix_maker(list_of_matrices=None, method=None):
    """ Construct a matrix from a list of matrices

    TODO [2] Make this funtion accept list of strings
    representing matrices.

    Construct a matrix using the items in the list and
    method specified by argument `method`. This assumes
    item in the list has implemented the requested method.

    Argument `method` specifies the operation between two
    matrices in the list, such as `tensor` or `dot`.
    The former means of course the tensor product and the
    later refers to the common matrix multiplication.
    Addition is also allowed.

    Product rules.

    [1] Matrix with the lowest index in the list is placed
    at the left most position in the chain. For example,
    list `[A,B,C,D]` with `tensor` method is understood as
        `A x B x C x D`

    [2] Resulting matrix (M) is assumed to be applied to a
    vector (v) from the left, i.e. Mv.

    [3] In the chain of matrix tensor product, matrix on the
    left most is supposed to operate on the bits of the lowest
    indices. For example, if gate U is applying the first bit
    of a two-bit state, the `U x I` will do.

    ARGUMENTS

    `list_of_matrices` (`list`) : a list of matrices to
    be used to contruct a matrix using the requested
    method; if list contains only 1 matrix, that matrix
    is returned

    `method` (`str`) : a string variable must be one of
    the available methods; any matrix in the list must
    have implemented such method

    RETURN

    `returned_matrix` : a matrix object
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.matrix_maker'
    available_methods = ['tensor', 'dot', 'add']
    returned_matrix = None
    if method not in available_methods:
        raise LSAFE("Method requested from matrix maker " +\
                "is not available",location=_ERROR_LOCATION_)
    if not isinstance(list_of_matrices, list):
        raise LSAFE("List of matrices provided to matrix " +\
                "maker is not a list.",location=_ERROR_LOCATION_)
    # if only one matrix in list, that matrix is returned
    if len(list_of_matrices) == 1:
        returned_matrix = list_of_matrices[0]
    else:
        if method == 'tensor':
            returned_matrix = list_of_matrices[0]
            for index in range(1, len(list_of_matrices)):
                returned_matrix = \
                        kronecker(returned_matrix, list_of_matrices[index])
        if method == 'add':
            returned_matrix = list_of_matrices[0]
            for index in range(1, len(list_of_matrices)):
                returned_matrix = \
                        matrix_add(returned_matrix, list_of_matrices[index])
        if method == 'dot':
            returned_matrix = list_of_matrices[0]
            for index in range(1, len(list_of_matrices)):
                returned_matrix = \
                        matrix_product(returned_matrix, list_of_matrices[index])
    return returned_matrix
