#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

qubit.algebra.py

PATH

[app_root]/qubit/algebra.py

INTRO

Algebra functions for qubit states.

NOTE Qubit algebra also accepts non-qubit quantum states
and superposition, which gives qubit algebra functions
broader interface than the algebras in quantum state
package. This may sound counter intuitive. But, since
qubit state is derived from quantum state, additional
features of qubit state are absent in generic quantum
state.

LOG

Updated on 02 October 2021 | Created on 13 November 2020
"""
from linear_space.number import is_number, is_zero, is_one
from linear_space.algebra import kronecker
from quantum_state import QuantumState, QuantumSuperposition, \
    NullState, NULL_STATE
from quantum_state.algebra import state_add, state_scale, state_inner, \
    state_outer, state_kronecker

from .qubit import QubitState, ComputationalBasis, QubitSuperposition
from .errors import QubitAlgebraFunctionError

_MODULE_LOCATION_ = 'qubit.algebra'


def qubit_scale(factor, state):
    """ Scale a qubit state or superposition

    Calculates `factor x |state>`

    RULES

    `QubitState` -> `QubitSuperposition`

    `QubitSuperposition` -> `QubitSuperposition`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.qubit_scale'

    ret = None
    if is_number(factor):
        if isinstance(state, (QubitState, QubitSuperposition)):
            if is_zero(factor):
                ret = NULL_STATE
            elif is_one(factor):
                ret = state
            else:
                if isinstance(state, QubitState):
                    ret = QubitSuperposition(superlist=[(factor, state)])
                elif isinstance(state, QubitSuperposition):
                    # multiply all amplitudes by same factor
                    new_superlist = [(factor*member[0], member[1],)
                                     for member in state.as_superlist()]
                    ret = QubitSuperposition(superlist=new_superlist)
        elif isinstance(state, (QuantumState, QuantumSuperposition, NullState)):
            ret = state_scale(factor, state)
        else:
            raise QubitAlgebraFunctionError("Qubit scale function "  +\
                    "is only applicable to qubits and generic " +\
                    "quantum state superposition.",
                    location=_ERROR_LOCATION_)
    else:
        raise QubitAlgebraFunctionError(
                "Scaling factor is not a number", location=_ERROR_LOCATION_)
    return ret


def qubit_add(lstate, rstate):
    """ Add two qubits

    TODO Create methods in qubit superposition to return
    the number of qubits.

    Calculates `|lstate> + |rstate>`

    Qubit states must all have the same dimension.
    If either of two states is not a qubit state, fall
    back to generic `state_add`.

    RULES

    `Qubit` + `Qubit` -> `QubitSuperposition`

    `Qubit` + `QubitSuperposition` - > `QubitSuperposition`

    `Qubit` + `NULL_STATE` - > `Qubit`

    `Qubit` + `QuantumState` - > `QuantumState`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.qubit_add'
    _MISMATCHED_DIMENSION_ERROR_ = QubitAlgebraFunctionError(
        "Fail to add two qubit states that have different dimension.",
        location=_ERROR_LOCATION_+'.qubit_add')

    ret = None
    if isinstance(lstate, QubitState) \
            and isinstance(rstate, QubitState):
        if lstate.noq == rstate.noq:
            sl = lstate.as_superposition().as_superlist()
            sl.extend(rstate.as_superposition().as_superlist())
            ret = QubitSuperposition(superlist=sl)
        else:
            raise  _MISMATCHED_DIMENSION_ERROR_
    elif isinstance(lstate, QubitState) \
            and isinstance(rstate, QubitSuperposition):
        # TODO Need to check size
        sl = lstate.as_superposition().as_superlist()
        sl.extend(rstate.as_superlist())
        ret = QubitSuperposition(superlist=sl)
    elif isinstance(lstate, QubitSuperposition) \
            and isinstance(rstate, QubitState):
        sl = lstate.as_superlist()
        sl.extend(rstate.as_superposition().as_superlist())
        ret = QubitSuperposition(superlist=sl)
    elif isinstance(lstate, QubitSuperposition) \
            and isinstance(rstate, QubitSuperposition):
        sl = lstate.as_superlist()
        sl.extend(rstate.as_superlist())
        ret = QubitSuperposition(superlist=sl)
    elif isinstance(lstate, (QubitState, QubitSuperposition,)) \
            and isinstance(rstate, NullState):
        ret = lstate
    elif isinstance(lstate, NullState) \
            and isinstance(rstate, (QubitState, QubitSuperposition,)):
        ret = rstate
    else:
        # fall back to generic state
        try:
            ret = state_add(lstate, rstate)
        except Exception as err:
            raise QubitAlgebraFunctionError(str(err)) from err
    return ret


def qubit_sub(lstate, rstate):
    """ Subtract one state from the other

    Calculates `|lstate> - |rstate>` using scale and addition
        `qubit_add(|lstate>, qubit_scale(-1.0,  |rstate>))`

    RULES

    `Qubit` - `Qubit` -> `QubitSuperposition` or `ZeroState`
    `Qubit` - `NullState` - > `Qubit`
    `Qubit` - `QuantumState` - > `QuantumState`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.qubit_sub'

    ret = None
    try:
        factor = -1.0
        ret = qubit_add(lstate, qubit_scale(factor, rstate))
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)
    return ret


def qubit_inner(lstate, rstate):
    """ Qubit inner product

    Calculates `<lstate|rstate>` via quantum state
    `state_inner`.

    Essentially the inner product of two vectors.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.qubit_inner'
    ret = None
    try:
        ret = state_inner(lstate, rstate)
    except Exception as err:
        raise QubitAlgebraFunctionError(str(err.relocate(_ERROR_LOCATION_)))
    return ret


def qubit_outer(lstate, rstate):
    """ Qubit outer product

    Calculates `|lstate><rstate|` via quantum state
    `state_outer`.

    Essentially the outer product of two vectors.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.qubit_outer'
    ret = None
    try:
        ret = state_outer(lstate, rstate)
    except Exception as err:
        raise QubitAlgebraFunctionError(str(err.relocate(_ERROR_LOCATION_)))
    return ret


def qubit_kronecker(lstate, rstate):
    """ Kronecker product of two qubits

    RULES

    `CompBasis o CompBasis` -> `CompBasis`

    `CompBasis o QubitState` -> `QubitState`

    `CompBasis o QubitSuperposition` -> `QubitState`

    `CompBasis o QuantumState` -> `QuantmState`

    `CompBasis o NullState` -> `NullState`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.qubit_kronecker'
    ret = None
    if isinstance(lstate, ComputationalBasis) \
            and isinstance(rstate, ComputationalBasis):
        newstring = lstate.bitstring + rstate.bitstring
        ret = ComputationalBasis(bitstring=newstring)
    elif isinstance(lstate, (QubitState, QubitSuperposition,)) \
            and isinstance(rstate, (QubitState, QubitSuperposition,)):
        ret = QubitState(
            vector=kronecker(lstate.as_vector(),rstate.as_vector()))
    elif isinstance(lstate, (QuantumState, QuantumSuperposition, NullState,)) \
            and isinstance(rstate,
                           (QuantumState, QuantumSuperposition, NullState,)):
        ret = state_kronecker(lstate, rstate)
    else:
        raise QubitAlgebraFunctionError("Kronecker product applies " +\
                "to quantum states only.", location=_ERROR_LOCATION_)
    return ret


def qubit_kron(lstate, rstate):
    """ Alias to `qubit_kronecker` """
    return qubit_kronecker(lstate, rstate)
