"""
MODULE

linear_space.utils.makers.py

PATH

[app_root]/linear_space/utils/makers.py

INTRO

Maker function constructs and returns an object using
the data (object) passed in.

CONTENT

`vector_from_list(obj)` - Construct a `Vector` instance
using a list of numbers; the input must be a list of numbers

`vector_from_tuple(obj)` - Construct a `Vector` instance
using a tuple of numbers; the input tuple must contain
only numbers

`vector(obj)` - Construct a `Vector` instance using the
given object; the object can be list, tuple, or numpy
array of proper dimension

`unitvector_from_list(obj)` - Construct a `UnitVector`
instance using a list of numbers

`unitvector_from_tuple(obj)` - Construct a `UnitVector`
instance using a tuple of numbers; the input tuple must
contain only numbers

`unitvector(obj)` - Construct a `UnitVector` instance
using the given object; the object can be list, tuple,
or numpy array of proper dimension

`equally_weighted_vector(number_of_elements)` - Create
a `UnitVector` of N elements and each element is 1/sqrt(N),
such that the vector is a unit vector

`matrix_from_array(array)` - Construct a matrix object
using the input array; returned matrix can be common
`Matrix` instance of `SquareMatrix` instnace, depending
on the dimension of the array

`matrix_from_list(obj)` - Construct a matrix using a list
of sublists

`matrix(obj)` - Construct a matrix object using an array
or a list

`identity_by_rows(n=2)` - Construct an identity matrix
using the number of rows

`identity_one_bit()` - Construct a 2-by-2 identity matrix

`identity_by_bits(n=1)` - Construct an identiy matrix using
the number of qubits n; the number of rows of the returned
matrix is thus 2^n

LOG

Updated on 30 September 2021 | Created on 15 April 2021
"""
from linear_space.numpy_lib import np_ndarray, np_power, np_array, \
    np_transpose, np_ones, np_sqrt
from linear_space.linear_object.utils import has_only_number
from linear_space.vector.column_vector import ColumnVector
from linear_space.vector.unit_vector import UnitVector
from linear_space.matrix.matrix import Matrix
from linear_space.matrix.square_matrix import SquareMatrix
from linear_space.matrix.identity_matrix import IdentityMatrix

from .errors import LinearSpaceUtilityFunctionError as UtilityError

_MODULE_LOCATION_ = 'linear_space.utils.makers'


def vector_from_list(src_list):
    """ Make column vector from list

    ARGUMENTS

    `src_list` (`list`) : Input must be a flat list of numbers.

    RETURN

    `column_vector` (`ColumnVector`) : a column vector instance
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.vector_from_list'

    column_vector = None
    if isinstance(src_list, list):
        if has_only_number(src_list):
            array = np_transpose([np_array(src_list)])
            column_vector = ColumnVector(array=array)
        else:
            raise UtilityError("Function 'vector_from_list' " +\
                    "accepts only a list of numbers.",
                    location=_ERROR_LOCATION_)
    else:
        raise UtilityError("Function 'vector_from_list' " +\
                "accepts only list as input.", location=_ERROR_LOCATION_)
    return column_vector


def vector_from_tuple(src_tuple):
    """ Make column vector from tuple

    ARGUMENTS

    `src_tuple` (`tuple`) : a tuple of numbers used for
    making column vector

    RETURN

    `column_vector` (`ColumnVector`) : a column vector instance
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.vector_from_tuple'

    column_vector = None
    if isinstance(src_tuple, tuple):
        if has_only_number(src_tuple):
            column_vector = vector_from_list(list(src_tuple))
        else:
            raise UtilityError("Function 'vector_from_tuple' " +\
                    "accepts only a tuple of numbers.",
                    location=_ERROR_LOCATION_)
    else:
        raise UtilityError("Function 'vector_from_tuple' " +\
                "accepts only tuple as input.",
                location=_ERROR_LOCATION_)
    return column_vector


def vector(src):
    """ Make a column vector from object

    ARGUMENTS

    `src` (obj) : Input object can be a numpy array,
    list, or tuple

    RETURN

    `column_vector` (`ColumnVector`) : a column vector instance
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.vector'

    column_vector = None
    try:
        if isinstance(src, list):
            column_vector = vector_from_list(src)
        elif isinstance(src, tuple):
            column_vector = vector_from_tuple(src)
        elif isinstance(src, np_ndarray):
            column_vector = ColumnVector(array=src)
        else:
            pass
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)
    return column_vector


def unitvector_from_list(src_list):
    """ Make a unit vector from list

    ARGUMENTS

    `src_list` (`list`) : a list of numbers

    RETURN

    `unitvec` (`UnitVector`) : an instance of unit vector
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.unitvector_from_list'

    unitvec = None
    if isinstance(src_list, list):
        if has_only_number(src_list):
            array = np_transpose([np_array(src_list)])
            unitvec = UnitVector(array=array)
        else:
            raise UtilityError("Function 'unitvector_from_list' " +\
                    "accepts only a list of numbers.",
                    location=_ERROR_LOCATION_)
    else:
        raise UtilityError("Function 'unitvector_from_list' " +\
                "accepts only list as input.",
                location=_ERROR_LOCATION_)
    return unitvec


def unitvector_from_tuple(src_tuple):
    """ Make a unit vector from tuple

    ARGUMENTS

    `src_tuple` (`tuple`) : a tuple of numbers

    RETURN

    `unitvec` (`UnitVector`) : an instance of unit vector
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.unitvector_from_tuple'

    unitvec = None
    if isinstance(src_tuple, tuple):
        if has_only_number(src_tuple):
            unitvec = unitvector_from_list(list(src_tuple))
        else:
            raise UtilityError("Function 'unitvector_from_tuple' " +\
                    "accepts only a tuple of numbers.",
                    location=_ERROR_LOCATION_)
    else:
        raise UtilityError("Function 'unitvector_from_tuple' " +\
                "accepts only tuple as input.",
                location=_ERROR_LOCATION_)
    return unitvec


def unitvector(src):
    """ Make a unit vector from an object

    ARGUMENTS

    `src` (obj) : input object can be a numpy array,
    list, or tuple

    RETURN

    `vec` (`UnitVector`) : an instance of unit vector
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.unitvector'

    vec = None
    try:
        if isinstance(src, list):
            vec = unitvector_from_list(src)
        elif isinstance(src, tuple):
            vec = unitvector_from_tuple(src)
        elif isinstance(src, np_ndarray):
            vec = UnitVector(array=src)
        else:
            pass
    except Exception as err:
        raise UtilityError(str(err), location=_ERROR_LOCATION_) from err
    return vec


def equally_weighted_vector(number_of_elements):
    """ Make an equally weighted vector

    Create a vector of N elements; each element is 1/sqrt(N),
    such that the vector is a unit vector.

    ARGUMENTS

    `number_of_elements` (`int`) : number of elements in
    the vector

    RETURN

    `unitvec` (`UnitVector`) : unit vector that is also
    an equally weighted vector
    """
    factor = 1.0 / np_sqrt(number_of_elements)
    array = np_transpose([np_ones(number_of_elements) * factor])
    unitvec = UnitVector(array=array)
    return unitvec


def matrix_from_array(src_array):
    """ Make a matrix from array-like object

    Matrix is by nature a two-dimensional object.

    ARGUMENTS

    `src_array` (`np_ndarray`) : Input array must be an
    instance of numpy array

    RETURN

    `new_matrix` (`Matrix`) : a matrix instance
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.matrix_from_array'

    new_matrix = None
    if isinstance(src_array, np_ndarray):
        try:
            if src_array.ndim == 1:
                new_matrix = Matrix(array=np_array([src_array]))
            elif src_array.ndim == 2:
                if len(src_array) == len(src_array[0]):
                    new_matrix = SquareMatrix(array=src_array)
                else:
                    new_matrix = Matrix(array=src_array)
            else:
                raise UtilityError("To create a matrix, dimension of " +\
                        "the array cannot be higher than 2.",
                        location=_ERROR_LOCATION_)
        except Exception as err:
            raise err.relocate(_ERROR_LOCATION_)
    else:
        raise UtilityError("Function 'matrix_from_array' requires " +\
                "a numpy array to make a matrix.", location=_ERROR_LOCATION_)
    return new_matrix


def matrix_from_list(src_list):
    """ Make a matrix instance from a list

    List used to build a matrix must be a list of sublists.
    All sublists must only contain numbers and must be of
    the same length.

    Each sublist represents a row.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.matrix_from_list'

    mat = None
    if isinstance(src_list, list):
        # elements are lists
        nonlist = 0
        for item in src_list:
            if not isinstance(item, list):
                nonlist += 1
        # check uniform length
        if nonlist == 0:
            length = len(src_list[0])
            uniform_length = True
            non_number = 0
            for item in src_list:
                if len(item) != length:
                    uniform_length = False
                if not has_only_number(item):
                    non_number += 1
            if uniform_length:
                if non_number == 0:
                    if length != 0:
                        array = np_array(src_list)
                        mat = matrix_from_array(array)
                    else:
                        raise UtilityError("Function 'matrix_from_list' " +\
                                "is given a list that has empty sublists.",
                                location=_ERROR_LOCATION_)
                else:
                    raise UtilityError("Function 'matrix_from_list' " +\
                            "is given a list that has sublists "     +\
                            "containing non-digital elements.",
                            location=_ERROR_LOCATION_)
            else:
                raise UtilityError("Function 'matrix_from_list' " +\
                        "is given a list that has sublists of "  +\
                        "different lengths.", location=_ERROR_LOCATION_)
        else:
            raise UtilityError("Function 'matrix_from_list' " +\
                    "is given a list that has an element "   +\
                    "that is not a list.", location=_ERROR_LOCATION_)
    else:
        raise UtilityError("Function 'matrix_from_list' accepts " +\
                "only a list of sublists.", location=_ERROR_LOCATION_)
    return mat


def matrix(src):
    """ Make a matrix from an array or a list

    ARGUMENTS

    `src` (`ndarray` or `list`) : an ndarray or a list
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.matrix'

    mat = None
    try:
        if isinstance(src, np_ndarray):
            mat = matrix_from_array(src)
        elif isinstance(src, list):
            mat = matrix_from_list(src)
    except Exception as err:
        raise UtilityError(str(err), location=_ERROR_LOCATION_) from err
    return mat


def identity_by_rows(nrows=2):
    """ Make an identity matrix using number of rows

    ARGUMENTS

    `nrows` (`int`) : number of rows of the desired identity
    matrix; default number of rows is set to 2
    """
    return IdentityMatrix(row_size=nrows)


def identity_one_bit():
    """ Make a 2-by-2 identity matrix """
    return IdentityMatrix()


def identity_by_bits(nbits=1):
    """ Make an identity matrix for a state of n qubits

    Size of the resulting matrix is 2^n by 2^n.

    ARGUMENTS

    `nbits` (`int`) : number of qubits

    RETURN

    An identity matrix of size (2^n, 2^n).
    """
    return IdentityMatrix(row_size=np_power(2, nbits))
