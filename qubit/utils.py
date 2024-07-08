#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

qubit.utils.py

PATH

[app_root]/qubit/utils.py

INTRO

Utility functions for qubit module.

LOG

Updated on 30 September 2021 | Created on 19 April 2021
"""
from bit.validators import BitlistValidator
from bit.utils import bitlist_to_vector, integer_to_bitstring
from linear_space.number import is_zero, exponent_of_two
from quantum_state.superposition import QuantumSuperposition
from quantum_state.null_state import NULL_STATE

from .qubit import QubitState, ComputationalBasis, QubitSuperposition, \
    QubitStateError
from .algebra import qubit_kronecker

_MODULE_LOCATION_ = 'qubit.utils'


# Builders
def qubit_from_bitlist(bitlist):
    """ Create a generic qubit or basis from bitlist

    Convert the bitlist into a vector and then instantiate
    a qubit state using that vector.

    Caution. In case the bitlist contains only 1 tuple,
    there are further two scenarios. First, if the amplitude
    is zero, a zero state shall be returned; second, if the
    amplitude is not zero, a computational basis state shall be
    created and the amplitude is discarded since it is meaningless.
    """
    state = None
    validator = BitlistValidator(bitlist=bitlist)
    if validator.is_valid:
        validated_bitlist = bitlist
        if len(validated_bitlist) == 1:
            # single component with zero amplitude
            # a zero state shall be returned.
            if is_zero(validated_bitlist[0][0]):
                state = NULL_STATE
            # otherwise, a computational basis is returned
            else:
                state = ComputationalBasis(bitstring=validated_bitlist[0][1])
        else:
            vector = bitlist_to_vector(validated_bitlist)
            state = QubitState(vector=vector)
        return state
    else:
        validator.raise_last_error()


def qubit_from_superposition(superposition):
    """ Create a qubit from a superposition instance

    TODO Unittest?
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.qubit_from_superposition'
    if isinstance(superposition, QubitSuperposition):
        qubit = superposition.as_state()
    elif isinstance(superposition, QuantumSuperposition):
        qubit = QubitState(state=superposition.as_state())
    else:
        raise QubitStateError("Superposition intended for " +\
                "qubit is neither a qubit superposition "   +\
                "nor a quantum superposition.", location=_ERROR_LOCATION_)
    return qubit


def basis_from_bitstring(bitstring):
    """ Create a computational basis from a bit string

    Errors related to bitstrings are actually rooted in the
    validation of binary string ergo from `BinaryStringValidator`.

    NOTE In the current design, a computational basis is
    instantiated with a bitstring.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.basis_from_bitstring'
    try:
        basis = ComputationalBasis(bitstring=bitstring)
        return basis
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)


def vector_to_computational_basis_superlist(vector):
    """ Convert a vector to superlist of computational basis """
    basislist = []
    # calculate number of qubits
    noq = exponent_of_two(vector.size)
    # NOTE since vector internal array has changed to a N-by-1 array
    # each entry in the array is a list of single element.
    for i, amp in enumerate(vector.as_array()):
        if not is_zero(amp[0]):
            # convert an integer to binary string
            bitstring = integer_to_bitstring(integer=i, total_digits=noq)
            basislist.append((amp[0], ComputationalBasis(bitstring=bitstring),))
    return basislist


def qubit_state_by_tensor_product(state_list):
    """ Construct a tensor-product state from list

    Construct a qubit state using tensor product of states
    in the given list.
    """
    product_state = state_list[0]
    for index in range(1, len(state_list), 1):
        product_state = qubit_kronecker(product_state, state_list[index])
    return product_state
