"""
PACKAGE

Qubit

PATH

[app_root]/qubit/

INTRO

Qubit package is one of the most essential packages
in the Application. It defines and constructs qubit
state and its derivateives that are fundamental to
qubit-based quantum computation algorithms.

Qubit package provides algebraic methods that are
needed to perform linear-algebra operations.

CONTENT

LOG

Updated on 26 September 2021 | Created on 20 June 2020
"""
from .qubit import QubitState, QubitSuperposition, ComputationalBasis, \
    SingleQubitBasis
from .special import EquallyWeightedSuperposition, EWS, AllDown, AllUp, \
    BellBasis
from .utils import qubit_from_bitlist, qubit_from_superposition, \
    vector_to_computational_basis_superlist
from .algebra import qubit_scale, qubit_add, qubit_sub, qubit_inner, \
    qubit_outer, qubit_kronecker, qubit_kron
