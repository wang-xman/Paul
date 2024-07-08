#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.utils.py

PATH

[app_root]/quantum_state/utils.py

INTRO

Quantum state module helper functions are used
to verify or construct a particular object.

TODO Not tested.

LOG

Updated on 25 September 2021 | Created on 19 April 2021
"""
from linear_space.number import is_one
from linear_space.utils import unitvector

from .quantum_state import QuantumState
from .superposition import QuantumSuperposition
from .algebra import state_inner

_MODULE_LOCATION_ = 'quantum_state.utils'


# Builders
def quantum_state_from_list(obj):
    """ Create a quantum state using a list of numbers

    NOTE List passed in here is not a superlist,
    but simply a list of numbers.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.quantum_state_from_list'
    try:
        univec = unitvector(obj)
        state = QuantumState(vector=univec)
        return state
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)


def quantum_state_from_superlist(obj):
    """ Create a quantums state using a superlist """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.quantum_state_from_superlist'
    superlist = obj
    try:
        superposition = QuantumSuperposition(superlist=superlist)
        return superposition.as_state()
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)


# Verifiers
def is_spinup(state):
    """ state.helper : Verify if a state is spin-up (|0>)

    Needs to be in a spin-up state.

    Spin-up state satisfies three criteria,
    (1) has two element (single qubit),
    (2) has nonzero norm (exclude zero state),
    (3) is orthogonal to spin-down state.
    """
    ret = False
    up = quantum_state_from_list([1,0])
    if isinstance(state, QuantumState) and state.size == 2 \
            and is_one(state_inner(state, up)):
        ret = True
    return ret


def is_spindown(state):
    """ state.helper : Verify if a state is spin-down (1)

    Needs to be in a spin-down state.

    Spin-down state satisfies three criteria,
    (1) has two element (single qubit),
    (2) has nonzero norm (exclude zero state),
    (3) is orthogonal to spin-up state.
    """
    ret = False
    down = quantum_state_from_list([0,1])
    if isinstance(state, QuantumState) and state.size == 2 \
            and is_one(state_inner(state, down)):
        ret = True
    return ret
