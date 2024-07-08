#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.enlarge_matrix.noncontrolled.py

PATH

[app_root]/gate/enlarge_matrix/noncontrolled.py

INTRO

Matrix enlarge routines and functions for non-controlled
gate operators.

CONTENT

`matrix_maker()`: create a matrix using a list of matrices
and specified method, 'tensor', 'add', or 'dot'

`enlarge_single_qubit_matrix()` : enlarge a single-qubit
matrix to fit for a multiple-qubit state

`enlarge_multiple_qubit_matrix()` : enlarge a multiple-qubit
matrix to fit for a multiple-qubit state

TODO

[1] One possible change to further realise lazy loading.
Matrix enlargement requires a chained tensor production.
Instead of returning a matrix, return a tuple of metadata
of matrices. For example, insteading of returning a zero
projection matrix, return a string 'proj0' to represent
this matrix. A list of such string hence represents the
desired enlarged matrix. Construction of the enlarged
matrix per se can be delayed to the last moment when the
matrix object is actually required.

LOG

Updated on 10 September 2021 | Created on 09 September 2021
"""
from linear_space.utils import identity_by_bits
from linear_space.algebra import matrix_maker
from .errors import GateMatrixEnlargeError
from .common import GenericGateMatrixEnlargeValidator

_MODULE_LOCATION_ = 'gate.enlarge_matrix.noncontrolled'


def enlarge_single_qubit_matrix(number_of_qubits=None, target_index=None,
                                original_matrix=None):
    """ Enlarge single-qubit operator matrix

    For application on multiple-qubit state.
    This must be a special case of multiple-qubit
    matrix in the following.

    For a single-qubit gate, matrix is enlarged
    according to the formula
        `I x...x I x...x U x...x I`,
    where `I` is the 2-by-2 identity matrix and `U`
    is the original single-qubit operator matrix
    (`original_matrix`); the location of U in the
    formula is determined by argument `target_index`;
    the total number of matrices in the formula is
    detemined by `number_of_qubits`; symbol `x` is
    the tensor product or Kronecker product.

    ARGUMENTS

    `number_of_qubits` (`int`) : total number of qubits
    in the multi-qubit state

    `target_index` (`int`) : index of the target bit in
    scientific index starting from 0; it must be
    validated before resizing

    `original_matrix` (`SquareMatirx`): the original
    single qubit matrix to be resized

    RETURN

    `new_matrix` (`SquareMatrix`) : enlarged operator matrix
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.enlarge_single_qubit_matrix'
    new_matrix = None
    validator = GenericGateMatrixEnlargeValidator(
        number_of_qubits=number_of_qubits,
        target_range=[target_index,target_index],
        original_matrix=original_matrix)
    matrix_list = []
    if validator.is_valid:
        try:
            if original_matrix.nrows != 2 or original_matrix.ncols != 2:
                raise GateMatrixEnlargeError("Original matrix " +\
                        "is not a single-qubit gate matrix.",
                        location=_ERROR_LOCATION_)
            # Case 0: If the number of qubits is exactly 1,
            # just return original matrix.
            if number_of_qubits == 1:
                matrix_list = [original_matrix]
            else:
                # Case 1: target is the first bit, matrix must tensor
                # an identity from the right
                if target_index == 0:
                    right_idm = identity_by_bits(number_of_qubits-1)
                    matrix_list = [original_matrix, right_idm]
                # Case 2: target is the last bit, an identity matrix
                # must tensor the matrix from the left
                elif target_index == number_of_qubits - 1:
                    left_idm = identity_by_bits(number_of_qubits-1)
                    matrix_list = [left_idm, original_matrix]
                # Case 3: target is in the middle, matrix is then
                # sandwiched between two identities
                else:
                    left_idm = identity_by_bits(target_index)
                    right_idm = identity_by_bits(
                            number_of_qubits - 1 - target_index)
                    matrix_list = [left_idm, original_matrix, right_idm]
            # make new matrix
            new_matrix = matrix_maker(list_of_matrices=matrix_list,
                                      method='tensor')
        except Exception as e:
            raise e
    else:
        validator.raise_last_error()
    return new_matrix


def enlarge_multiple_qubit_matrix(number_of_qubits=None, target_range=None,
                                  original_matrix=None):
    """ Enlarge a multiple-qubit gate matrix

    For application on an even larger multiple-qubit state.
    This function must covers the single-qubit case
    when the target range narrows down to one bit and
    the original matrix is for a single qubit.

    ARGUMENTS

    `number_of_qubits` (`int`) : total number of qubits
    in the multi-qubit state

    `target_range` (`list`) : range of target indices
    given in a list of two elements; given range must
    be continuous; for example, [1,3] means the target
    indices are 1, 2, and 3

    `original_matrix` (`SquareMatirx`): the original
    single qubit matrix to be resized

    RETURN

    `new_matrix` (`SquareMatrix`) : enlarged operator matrix
    """
    new_matrix = None
    validator = GenericGateMatrixEnlargeValidator(
        number_of_qubits=number_of_qubits,
        target_range=target_range,
        original_matrix=original_matrix)
    matrix_list = []
    if validator.is_valid:
        try:
            # if target range narrows to one index, single-qubit gate
            if target_range[0] == target_range[1]:
                new_matrix = enlarge_single_qubit_matrix(
                    number_of_qubits=number_of_qubits,
                    target_index=target_range[0],
                    original_matrix=original_matrix)
            # Case 0: exactly same number of qubits
            elif target_range[0] == 0 \
                    and target_range[1] == number_of_qubits - 1:
                matrix_list = [original_matrix]
            else:
                # Case 1: target range starts from the first bit,
                # matrix must tensor product an identity from the right
                if target_range[0] == 0:
                    right_idm = identity_by_bits(
                            number_of_qubits - 1 - target_range[1])
                    matrix_list = [original_matrix, right_idm]
                # Case 2: target range covers the last bit,
                # an identity matrix must tensor the matrix from the left
                elif target_range[1] == number_of_qubits - 1:
                    left_idm = identity_by_bits(target_range[0])
                    matrix_list = [left_idm, original_matrix]
                # Case 3: target range is in the middle,
                # matrix is then sandwiched between two identities
                else:
                    left_idm = identity_by_bits(target_range[0])
                    right_idm = identity_by_bits(
                            number_of_qubits - 1 - target_range[1])
                    matrix_list = [left_idm, original_matrix, right_idm]
            # create matrix
            if new_matrix is None:
                new_matrix = matrix_maker(list_of_matrices=matrix_list,
                                          method='tensor')
        except Exception as e:
            # TODO re-raise this
            raise e
    else:
        validator.raise_last_error()
    return new_matrix
