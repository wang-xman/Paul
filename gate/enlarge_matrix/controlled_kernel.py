#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.enlarge_matrix.controlled_kernel.py

PATH

[app_root]/gate/enlarge_matrix/controlled_kernel.py

INTRO

Construction of multiple-controlled multiple-qubit (mcmq)
operator matrix. This function is the most generic kernel
to construction of any controlled operator matrix.

CONTENT

`multiple_controlled_multiple_qubit_operator_matrix()` -
generic function to construct a multiple-controlled
operator matrix for a multiple-qubit gate

`kernel()` - Alias to the function above

`universal_CNOT_matrix()` : construct a CNOT matrix for a
multiple-qubit state

`universal_SWAP_matrix()` : construct a SWAP matrix for a
multiple-qubit state

LOG

Updated on 30 September 2021 | Created on 13 September 2021
"""
from bit.utils import integer_to_bitstring
from linear_space.number import power_of_two
from linear_space.matrix import STATE_ZERO_PROJECTION, STATE_ONE_PROJECTION,\
    PAULI_X
from linear_space.utils import identity_by_bits
from linear_space.algebra import matrix_add, matrix_product, matrix_maker

from .errors import GateMatrixEnlargeError
from .common import GenericGateMatrixEnlargeValidator

_MODULE_LOCATION_ = 'gate.enlarge_matrix.controlled_kernel'


def do_nothing_part_matrix_list_per_bitstring(bitstring, number_of_qubits,
                                              control_indices):
    """ Matrix list for a bitstring that is not control string """
    matrix_list = []
    for i in range (0, number_of_qubits):
        if i in control_indices:
            if bitstring[control_indices.index(i)] == '0':
                matrix_list.append(STATE_ZERO_PROJECTION)
            else:
                matrix_list.append(STATE_ONE_PROJECTION)
        else:
            matrix_list.append(identity_by_bits(1))
    return matrix_list


def apply_part_matrix_list_per_bitstring(bs, number_of_qubits, control_indices,
                                         target_range, original_matrix):
    """ Matrix list for a bitstring that is control string """
    matrix_list = []
    # target range starts from 0
    if target_range[0] == 0:
        matrix_list.append(original_matrix)
        for i in range (target_range[1] + 1, number_of_qubits):
            if i in control_indices:
                if bs[control_indices.index(i)] == '0':
                    matrix_list.append(STATE_ZERO_PROJECTION)
                else:
                    matrix_list.append(STATE_ONE_PROJECTION)
            else:
                matrix_list.append(identity_by_bits(1))
    # target range covers the end
    elif target_range[1] == number_of_qubits - 1:
        for i in range (0, target_range[0]):
            if i in control_indices:
                if bs[control_indices.index(i)] == '0':
                    matrix_list.append(STATE_ZERO_PROJECTION)
                else:
                    matrix_list.append(STATE_ONE_PROJECTION)
            else:
                matrix_list.append(identity_by_bits(1))
        matrix_list.append(original_matrix)
    # target range in the middle
    else:
        for i in range (0, target_range[0]):
            if i in control_indices:
                if bs[control_indices.index(i)] == '0':
                    matrix_list.append(STATE_ZERO_PROJECTION)
                else:
                    matrix_list.append(STATE_ONE_PROJECTION)
            else:
                matrix_list.append(identity_by_bits(1))
        matrix_list.append(original_matrix)
        for i in range (target_range[1] + 1, number_of_qubits):
            if i in control_indices:
                if bs[control_indices.index(i)] == '0':
                    matrix_list.append(STATE_ZERO_PROJECTION)
                else:
                    matrix_list.append(STATE_ONE_PROJECTION)
            else:
                matrix_list.append(identity_by_bits(1))
    return matrix_list


def sort_control_list(control_list):
    """ Sort control list

    RETURN

    `ret` (`dict`) : a dictionary that has 3 keys, `sorted_list`,
    `control_indices`, and `control_bitstring`.
    """
    # sort control list according to first element,
    # i.e. control qubit index
    control_list.sort()
    # seperate control indices and control values
    control_indices = list(zip(*control_list))[0]
    control_values = list(zip(*control_list))[1]
    # construct control string such as '011'
    control_bitstring = ''.join(control_values)
    ret = {
        'sorted_list': control_list,
        'control_indices': control_indices,
        'control_bitstring': control_bitstring
    }
    return ret


def multiple_controlled_multiple_qubit_operator_matrix(number_of_qubits=None,
        control_list=None, target_range=None, original_matrix=None):
    """ Multiple-controlled multiple-qubit operator matrix maker

    Construct a multiple-controlled multiple-qubit (MCMQ)
    operator matrix.

    This function is the most generic routine for construction
    of controlled operator matrix with target range provided.
    """
    total_matrix = None
    validator = GenericGateMatrixEnlargeValidator(
        number_of_qubits=number_of_qubits,
        target_range=target_range,
        control_list=control_list,
        original_matrix=original_matrix)
    if validator.is_valid:
        sorted_list = sort_control_list(control_list)
        control_indices = sorted_list['control_indices']
        control_bitstring = sorted_list['control_bitstring']
        # Create all possible bitstrings corresponding
        # to the number of control bits.
        # iterate through all possible bitstrings
        for integer in range(0, power_of_two(len(control_indices))):
            # create bistring from the integer
            bs = integer_to_bitstring(integer, len(control_indices))
            # matrix list per bitstring
            matrix_list = []
            # if not control string
            if bs != control_bitstring:
                matrix_list = do_nothing_part_matrix_list_per_bitstring(
                        bs, number_of_qubits, control_indices)
            # control string
            else:
                matrix_list = apply_part_matrix_list_per_bitstring(bs,
                        number_of_qubits, control_indices, target_range,
                        original_matrix)
            # matrix for a bit string
            matrix_per_bitstring = \
                    matrix_maker(list_of_matrices=matrix_list, method='tensor')
            if integer == 0:
                total_matrix = matrix_per_bitstring
            else:
                total_matrix = matrix_add(total_matrix, matrix_per_bitstring)
    else:
        validator.raise_last_error()
    return total_matrix


def kernel(number_of_qubits=None, control_list=None, target_range=None,
           original_matrix=None):
    """ Controlled operator kernel function

    Alias to mcmq routine.
    """
    return multiple_controlled_multiple_qubit_operator_matrix(
        number_of_qubits=number_of_qubits,
        target_range=target_range,
        control_list=control_list,
        original_matrix=original_matrix
    )


def universal_CNOT_matrix(number_of_qubits=None, control_index=None,
                          target_index=None):
    """ CNOT operator matrix for multiple-bit state

    Returns a matrix that performs SWAP operation of any
    two qubits in a multiple-qubit state. Two qubits to
    be swapped are given in indices.

    Matrix is constructed as a single-controlled single
    qubit flip matrix.

    ARGUMENTS

    `number_of_qubits` (`int`) : total number of qubits
    in the multi-qubit state

    `target_index` (`int`) : index of the target bit in
    the scientific indexing scheme starting from 0

    `control_index` (`int`) : index of the control bit in
    the scientific indexing scheme starting from 0

    RETURN

    `operator_matrix` (`SquareMatrix`) : newly constructed
    operator matrix
    """
    single_qubit_flip_matrix = PAULI_X
    operator_matrix = None
    try:
        operator_matrix = kernel(
            number_of_qubits=number_of_qubits,
            control_list=[(control_index,'1')],
            target_range=[target_index, target_index],
            original_matrix=single_qubit_flip_matrix)
    except Exception as err:
        raise err
    return operator_matrix


def universal_SWAP_matrix(number_of_qubits=None, alpha=None, beta=None):
    """ SWAP matrix for multiple-bit state

    SWAP matrix is a two-bit operator that is enlarged
    to fit a multiple-bit state.

    SWAP matrix is implemented as three sequential CNOT
    operations with control and target bits swapped, i.e.
    SWAP(alpha,beta) -> CNOT(alpha, beta)CNOT(beta, alpha)CNOT(alpha, beta)

    All arguments are integers.

    ARGUMENTS

    `number_of_qubits` (`int`): total number of qubits
    in the multi-qubit state

    `alpha` and `beta` (`int`): indices of the qubits to
    be swapped; both are in the scientific indexing scheme
    starting from 0; they must NOT be the same
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.universal_SWAP_matrix'
    ret = None
    if alpha not in range(0, number_of_qubits):
        raise GateMatrixEnlargeError("Failed to construct a SWAP matrix. "+\
                "Index alpha is out of range.", location=_ERROR_LOCATION_)
    elif beta not in range(0, number_of_qubits):
        raise GateMatrixEnlargeError("Failed to construct a SWAP matrix. "+\
                "Index beta is out of range.", location=_ERROR_LOCATION_)
    elif alpha == beta:
        raise GateMatrixEnlargeError("Failed to construct a SWAP matrix. "+\
                "Indices alpha and beta are equal. It is " +\
                "meaningless to swap with itself.", location=_ERROR_LOCATION_)
    else:
        # first CNOT
        matrix_of_first_CNOT = universal_CNOT_matrix(
            number_of_qubits=number_of_qubits,
            control_index=alpha,
            target_index=beta)
        # second CNOT
        matrix_of_second_CNOT = universal_CNOT_matrix(
            number_of_qubits=number_of_qubits,
            control_index=beta,
            target_index=alpha)
        # operator matrix
        # TODO Use matrix maker
        total_matrix = matrix_product(matrix_of_first_CNOT,
            matrix_product(matrix_of_second_CNOT, matrix_of_first_CNOT))
        ret = total_matrix
    return ret
