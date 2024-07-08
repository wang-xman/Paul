#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.enlarge_matrix.controlled_target_tuple.py

PATH

[app_root]/gate/enlarge_matrix/controlled_target_tuple.py

INTRO

Construction of multiple-controlled multiple-qubit operator
matrix for input specified using target tuple. Target tuple
is a tuple consisting of target qubit indices on which the
multiple-qubit gate applies.

CONTENT

LOG

Updated on 17 September 2021 | Created on 17 September 2021
"""
from linear_space.utils import maximum, minimum
from linear_space.algebra import matrix_maker

from .errors import GateMatrixEnlargeError
from .controlled_kernel import kernel, universal_SWAP_matrix


def is_CISWAP_required(control_list=None, target_tuple=None):
    """ Verifies if ciswap is required

    CISWAP is only needed when one control index falls
    into the target window.
    """
    ret = False
    target_window = range(minimum(target_tuple), maximum(target_tuple), 1)
    for ci in control_list:
        if ci[0] in target_window:
            ret = True
    return ret


def control_index_swap(control_list=None, target_tuple=None):
    """ Construct control index swap (ciswap)

    Target index must be a tuple a qubit indices.

    Core algorithm.
    Always swaps an in-window control bit with the lowest
    target index (LTI). After every swap, the LTI may change.
    This alogrithm, however, keeps the dimension of the original
    operator matrix, operation window, unchanged.
    """
    # initialise new target index to the original,
    # but using list
    new_target_index_list = [idx for idx in target_tuple]
    new_control_index_list = []
    # sort control list by qubit index
    sorted_control_list = sorted(control_list, key=lambda x : x[0])
    swap_list = []
    for ci in sorted_control_list:
        # lowest and highest target index
        lti = minimum(new_target_index_list)
        target_window = range(lti, maximum(new_target_index_list), 1)
        # control in window
        if ci[0] in target_window:
            # swap with LTI
            swap_list.append((lti,ci[0]))
            for i, _ in enumerate(new_target_index_list):
                # update target index
                if new_target_index_list[i] == lti:
                    new_target_index_list[i] = ci[0]
            # update control index
            new_control_index_list.append((lti, ci[1],))
        else:
            new_control_index_list.append(ci)
    # if swap list if empty, no ciswap needed.
    return {
        'swap_list': swap_list,
        'control_list': new_control_index_list,
        'target_tuple': tuple(new_target_index_list)
    }


def pre_CISWAP_matrix(number_of_qubits=None, swap_list=None):
    """ Swap matrix before applying operator """
    pairwise_swap_matrix_list = []
    for pair in swap_list:
        pairwise_swap_matrix_list.append(universal_SWAP_matrix(
                number_of_qubits=number_of_qubits, alpha=pair[0], beta=pair[1])
        )
    return matrix_maker(list_of_matrices=pairwise_swap_matrix_list, method='dot')


def post_CISWAP_matrix(number_of_qubits=None, swap_list=None):
    """ Swap matrix after applying operator """
    pairwise_swap_matrix_list = []
    for pair in reversed(swap_list):
        pairwise_swap_matrix_list.append(universal_SWAP_matrix(
                number_of_qubits=number_of_qubits, alpha=pair[0], beta=pair[1])
        )
    return matrix_maker(list_of_matrices=pairwise_swap_matrix_list, method='dot')


def controlled_target_tuple(number_of_qubits=None, target_tuple=None,
                            control_list=None, original_matrix=None):
    """ Controlled operator matrix with target index

    Target index can be an integer or a tuple of integers.
    """
    ret = None
    # one target index, already convered in kernel
    if len(target_tuple) == 1:
        ret = kernel(
            number_of_qubits=number_of_qubits,
            control_list=control_list,
            target_range=[target_tuple[0], target_tuple[0]],
            original_matrix=original_matrix)
    # multiple target indices, FIXME not different from the above
    elif len(target_tuple) > 1:
        # call target range utility function
        ret = kernel(
            number_of_qubits=number_of_qubits,
            control_list=control_list,
            target_range=[minimum(target_tuple), maximum(target_tuple)],
            original_matrix=original_matrix)
    else:
        raise GateMatrixEnlargeError("Target tuple is empty.")
    return ret
