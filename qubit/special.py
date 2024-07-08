#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

qubit.special.py

PATH

[app_root]/qubit/special.py

TODO

2. Introduce Bell states object.

INTRO

Specialised qubit states

CONTENT

`EquallyWeightedSuperposition` - Equally weighted superposition

`EWS` - Equally weighted superposition

`AllUp` - All qubits are in up |0> state

`AllDown` - All qubits are in down |1> state

`BellBasis` - Bell states (TODO)

LOG

Updated on 25 September 2021 | Created on 07 March 2021
"""
from bit.utils import bitstring_to_standard_basis
from linear_space.number import is_integer, power_of_two
from linear_space.utils import equally_weighted_vector

from .qubit import QubitState, QubitStateError

_MODULE_LOCATION_ = 'qubit.special'


class EquallyWeightedSuperposition(QubitState):
    """ Equally weighted superposition state

    TODO Specialise this error.

    Multi-qubit state with all bits in
        `|+> = (|0> + |1>)/sqrt(2)`
    state.

    CONSTRUCTOR

    `number_of_qubits` (`int`): number of qubits of the
    multi-qubit state
    """
    def __init__(self, number_of_qubits=None):
        if is_integer(number_of_qubits) and not number_of_qubits < 1:
            vector = equally_weighted_vector(power_of_two(number_of_qubits))
            super().__init__(vector=vector)
        else:
            raise QubitStateError("To instantiate equally weighted " +\
                    "superposition state, number of qubits must be an " +\
                    "integer no less than 1.")


EWS = EquallyWeightedSuperposition
""" Alias to equally weighted superposition """


class AllUp(QubitState):
    """ All qubits are spin up |0>

    Multiqubit state with all bits in |0> state.

    CONSTRUCTOR

    `number_of_qubits` (`int`): number of qubits of the
    multi-qubit state
    """
    def __init__(self, number_of_qubits=None):
        bitstring = '0' * number_of_qubits
        basis_vector = bitstring_to_standard_basis(bitstring)
        super().__init__(vector=basis_vector)


class AllDown(QubitState):
    """ All qubits are spin down |1>

    Multiqubit state with all bits in |1> state.

    CONSTRUCTOR

    `number_of_qubits` (`int`): number of qubits of
    multi-qubit state
    """
    def __init__(self, number_of_qubits=None):
        bitstring = '1' * number_of_qubits
        basis_vector = bitstring_to_standard_basis(bitstring)
        super().__init__(vector=basis_vector)


class BellBasis(QubitState):
    """ TODO Implement this """
