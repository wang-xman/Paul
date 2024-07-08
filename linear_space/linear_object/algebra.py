"""
MODULE

linear_space.linear_object.algebra.py

PATH

[app_root]/linear_space/linear_object/algebra.py

INTRO

Linear Object Algebra Functions, a.k.a. LOAF.

NOTE Most linear algebraic operations involved in
this Application are redirected to this module.
Actual computational routines are delegated to numpy
functions.

CONTENT

`transpose(linobj)` - Returns a linear object that is the
transpose

`complex_conjugate(linobj)` - Returns a linear object that is
the complex conjugate of the current; shape remains

`hermitian_conjugate(linobj)` - Hermitian conjugate is a complex
conjugate of the transposed linear object

`norm(obj)` - Two-norm of linear object, or absolute value of
a number

`scale(factor, linobj)` - Scale a linear object

`dot(left_item,right_item)` - Matrix-like multiplication;
returns a `LinearObject` instance.
Following rules are observed:
[1] if `left_item` is row-like and `right_item` is
column-like, the result is a scalar (packed as a 2D numpy array),
equivalent inner product;
[2] if `left_item` is column-like and the `right_item`
object is row-like, the result is a matrix, equivalent
to outer product;
[3] if both objects are matrix-like, the result is matrix-like,
equivalent to regular matrix product

`kronecker(left_item, right_item)` - Kronecker product for
two linear object; returns a linear object

`add(left_item, right_item)` - Matrix-like addition of two
linear objects of the same dimension; returns a `LinearObject`
instance

`subtract(left_item, right_item)` - Matrix-like subtraction
of two linear objects of the same size; returns a `LinearObject`
instance

`multiply(left_item, right_item)` - Multiplication; if either
is a scalar, returns a scalar or scaled linear object;
if both are linear objects, returns the Kronecker product

LOG

Updated on 27 September 2021 | Created on 22 April 2021
"""
from linear_space.numpy_lib import np_transpose, np_conj, np_norm, np_dot, \
    np_outer, np_kron, np_array
from linear_space.number import is_number, Number

from .linear_object import LinearObject
from .utils import is_column_like, is_row_like
from .types import Column_Like, Row_Like
from .errors import LinearObjectAlgebraError
from .decorator import algebra_function_decorator

_MODULE_LOCATION_ = 'linear_space.linear_object.algebra'


@algebra_function_decorator(argument_type = {'linobj': LinearObject})
def transpose(linobj):
    """ Operation : Transpose operation

    Matrix transpose operation.

    A column-like is transposed into a row-like, vice verse.

    RETURN

    A `LinearObject` instance.
    """
    new_array = np_transpose(linobj.as_array())
    return LinearObject(array=new_array)


@algebra_function_decorator(argument_type = {'linobj': LinearObject})
def complex_conjugate(linobj):
    """ Operation : Complex conjugate

    TODO Not tested.

    Complex conjugate is applied to every element.

    RETURN

    A `LinearObject` instance.
    """
    new_array = np_conj(linobj.as_array())
    return LinearObject(array=new_array)


@algebra_function_decorator(argument_type = {'linobj': LinearObject})
def hermitian_conjugate(linobj):
    """ Operation : Hermitian conjugate

    TODO Not directly tested. But tested in other functions.

    Hermitian conjugate is a complex conjugate then transposed.
    A column-like is transformed into row-like, vice verse.
    """
    new_array = np_transpose(np_conj(linobj.as_array()))
    return LinearObject(array=new_array)


@algebra_function_decorator(
    argument_type = {'obj': (Number, Column_Like, Row_Like,)}
)
def norm(obj):
    """ Linear Object Algebra Function : Norm

    Only accepts number and vector-like linear object.
    If real number, returns its absolute value. If a
    complex number or vector like object, returns two-norm.

    RETURN

    A positive number
    """

    ret = np_norm(obj) if isinstance(obj, Number) \
            else np_norm(obj.as_array())
    return ret


@algebra_function_decorator(
    argument_type = {
        'factor': Number,
        'linobj': LinearObject
    }
)
def scale(factor, linobj):
    """ Linear Object Algebra : Scale

    Scales a linear object by a scalar.

    ARGUMENTS

    `factor` (scalar) : a scalar, or number

    `linobj` (`LinearObject`) : either a scalar or
    an instance of `LinearObject` or its subclass

    RETURN

    A `LinearObject` instance.
    """
    new_array = factor * linobj.as_array()
    ret = LinearObject(array=new_array)
    return ret


@algebra_function_decorator(
    argument_type = {
        'left_item': (Column_Like, Row_Like,),
        'right_item': (Column_Like, Row_Like,)
    }
)
def inner(left_item, right_item):
    """ Linear Object Algebra : Inner product

    Inner product applies to column- and row-like linear
    objects. The left item will always be transformed
    into row-like; and the right item is always into
    column-like.

    RETURN

    A scalar-like object.
    """
    new_array = None
    left_array = left_item.as_array() if is_row_like(left_item) \
            else hermitian_conjugate(left_item).as_array()
    right_array = right_item.as_array() if is_column_like(right_item) \
            else hermitian_conjugate(right_item).as_array()
    # size check
    if len(left_array[0]) == len(right_array):
        new_array = np_dot(left_array, right_array)
    else:
        raise LinearObjectAlgebraError('Sizes of two linear ' +\
                'objects involved in inner product are incompatible.',
                location=_MODULE_LOCATION_+'.inner')
    return LinearObject(array=new_array)


@algebra_function_decorator(
    argument_type = {
        'left_item': (Column_Like, Row_Like,),
        'right_item': (Column_Like, Row_Like)
    }
)
def outer(left_item, right_item):
    """ Linear Object Algebra : Outer product

    Outer product for row- and column-like linear
    objects. Object on the left side must be always
    column-like; object on the right side must be
    row-like. Otherwise, hermitian conjugate is applied
    to transfrom them.
    """
    left_array = left_item.as_array() if is_column_like(left_item) \
            else hermitian_conjugate(left_item).as_array()
    right_array = right_item.as_array() if is_row_like(right_item) \
            else hermitian_conjugate(right_item).as_array()
    new_array = np_outer(left_array, right_array)
    return LinearObject(array=new_array)


@algebra_function_decorator(
    argument_type = {
        'left_item': LinearObject,
        'right_item': LinearObject
    }
)
def dot(left_item, right_item):
    """ Linear Object Algebra : Matrix product

    Matrix-like product of two linear objects returns
    a linear object.

    If left object is row-like and the right is column-like,
    the result is a scalar (packed as a 2D numpy array),
    indicating inner product.

    If the left object is column-like and the right object is
    row-like, the result is a matrix, indicating outer product.

    If both objects are matrix-like, the result is a matrix,
    indicating regular matrix product.

    ARGUMENTS

    `left_item` (`LinearObject` or subclass): an instance of
    `LinearObject` or its subclass

    `right_item` (`LinearObject` or subclass): an instance of
    `LinearObject` or its subclass

    RETURN

    A `LinearObject` instance.
    """
    new_array = None
    if left_item.get_number_of_columns() == right_item.get_number_of_rows():
        new_array = np_dot(left_item.as_array(), right_item.as_array())
    else:
        raise LinearObjectAlgebraError('Sizes of two linear ' +\
                'objects involved in multiplication are incompatible.',
                location=_MODULE_LOCATION_+'.dot')
    return LinearObject(array=new_array)


@algebra_function_decorator(
    argument_type={
        'left_item': LinearObject,
        'right_item': LinearObject
    }
)
def add(left_item, right_item):
    """ Operation : Addition

    Addition opeation performs matrix-like addition and thus
    requires the two linear objects to have the same size,
    i.e. same number of rows, and same number of columns.

    ARGUMENTS

    `left_item` (`LinearObject` or subclass): an instance of
    `LinearObject` or its subclass

    `right_item` (`LinearObject` or subclass): an instance of
    `LinearObject` or its subclass

    RETURN

    A `LinearObject` instance.
    """
    new_array = None
    if left_item.get_size() == right_item.get_size():
        new_array = left_item.as_array() + right_item.as_array()
    else:
        raise LinearObjectAlgebraError('Linear object addition ' +\
                'method requires two linear objects that ' +\
                'are of the same size.',
                location=_MODULE_LOCATION_+'.add')
    return LinearObject(array=new_array)


@algebra_function_decorator(
    argument_type={
        'left_item': LinearObject,
        'right_item': LinearObject
    }
)
def subtract(left_item, right_item):
    """ Linear Object :: Subtract method

    WARNING Not subtract operator (- or `__sub__`)

    Subtraction operator (-) performs matrix-like addition
    and thus requires the two linear objects to have the
    same size, i.e. same number of rows, and same number of
    columns.

    RETURNS

    A `LinearObject` instance.

    ARGUMENTS

    `right_item` (`LinearObject` or subclass): an instance of
    `LinearObject` or its subclass

    `right_item` (`LinearObject` or subclass): an instance of
    `LinearObject` or its subclass
    """
    new_array = None
    if left_item.get_size() == right_item.get_size():
        new_array = left_item.as_array() - right_item.as_array()
    else:
        raise LinearObjectAlgebraError('Linear object subtract '+\
                'method requires two linear objects that are '+\
                'of the same size.',
                location=_MODULE_LOCATION_+'.subtract')
    return LinearObject(array=new_array)


@algebra_function_decorator(
    argument_type = {
        'left_item': LinearObject,
        'right_item': LinearObject
    }
)
def kronecker(left_item, right_item):
    """ Operation : Kronecker tensor product

    Kronecker tensor product applies only to linear object.

    Returns

    a `LinearObject` instance.

    Arguments

    `right_item` (`LinearObject` or subclass): an instance of
    `LinearObject` or its subclass
    """
    new_array = np_kron(left_item.as_array(), right_item.as_array())
    return LinearObject(array=new_array)


@algebra_function_decorator(
    argument_type = {
        'left_item': (Number, LinearObject,),
        'right_item': (Number, LinearObject,)
    }
)
def multiply(left_item, right_item):
    """ Operation : Multiply method

    Multiply only applies to number and linear object.
    Following rules apply:

    If either item is a number, operation is a scalar product.

    If both items are linear objects, the operation is
    kronecker product.

    Returns a `LinearObject` instance.

    Arguments

    `left_item` (scalar or `LinearObject`): either a scalar or
    an instance of `LinearObject` or its subclass

    `right_item` (scalar or `LinearObject`): either a scalar or
    an instance of `LinearObject` or its subclass
    """
    new_array = None
    # left number, right LO
    if is_number(left_item) and isinstance(right_item, LinearObject):
        new_array = left_item * right_item.as_array()
        ret = LinearObject(array=new_array)
    # left LO, right number
    elif isinstance(left_item, LinearObject) and is_number(right_item):
        new_array = right_item * left_item.as_array()
        ret = LinearObject(array=new_array)
    # both numbers
    elif is_number(left_item) and is_number(right_item):
        # This is a scalar
        new_array = np_array([[right_item * left_item]])
        ret = LinearObject(array=new_array)
    # both LOs
    else:
        ret = kronecker(left_item, right_item)
    return ret
