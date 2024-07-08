#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.algebra.functions.py

TODO

[1] Decorator doesn't reduce much of the codes.
Change the algorithm in the function.

PATH

[app_root]/quantum_state/algebra/functions.py

INTRO

Algebra functions are in general applicable to
quantum state and quantum superposition.

CONTENT

`state_scale(factor, state)` - Scale a state or superposition
as `factor * |state>`

`state_add(lstate, rstate)` - Add two states `|lstate> + |rstate>`

`state_sub(lstate, rstate)` - State `lstate` subtracts `rstate`
as `|lstate> - |rstate>`

`state_inner(lstate, rstate)` - Inner product of two states,
which is defined as `<lstate|rstate>`; returns number

`state_outer(lstate, rstate)` - Outer product of two states,
which is defined as `|lstate><rstate|`; returns matrix

`state_kronecker(lstate, rstate)` - Kronecker product of two
states

`state_kronecker(lstate, rstate)` - Kronecker product of two
states

LOG

Updated on 29 September 2021 | Created on 20 June 2020
"""
from linear_space.number import is_zero, is_one, Number
from linear_space.algebra import inner, outer, kronecker

from quantum_state.null_state import NullState, NULL_STATE
from quantum_state.quantum_state import QuantumState
from quantum_state.superposition import QuantumSuperposition

from .errors import QuantumStateAlgebraFunctionError
from .decorator import quantum_state_algebra_function_decorator \
    as QSAF_Decorator

_MODULE_LOCATION_ = 'quantum_state.algebra.functions'


# One state operation
@QSAF_Decorator(
    argument_type={
        'factor': Number,
        'state': (QuantumState, QuantumSuperposition, NullState,)
    }
)
def state_scale(factor, state):
    """ Scale a state or superposition

    RULES

    `QuantumState` -> `QuantumSuperposition` : A single quantum
    state is scaled into a quantum superposition with one member

    `QuantumSuperposition` -> `QuantumSuperposition` : A quantum
    superposition is scaled by multiplying every amplitude with
    the factor
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.state_scale'

    ret = None
    if is_zero(factor):
        ret = NULL_STATE
    elif is_one(factor):
        ret = state
    else:
        if isinstance(state, NullState):
            ret = NULL_STATE
        elif isinstance(state, QuantumState):
            ret = QuantumSuperposition(superlist=[(factor, state)])
        elif isinstance(state, QuantumSuperposition):
            # multiply all amplitudes by same factor
            new_superlist = [(factor*member[0], member[1],)
                             for member in state.as_superlist()]
            ret = QuantumSuperposition(superlist=new_superlist)
    return ret


# Two state operation
def state_add(lstate, rstate):
    """ Addition of two states

    Calculates `|lstate> + |rstate>`.

    RULES

    `QuantumState` + `QuantumState` -> `QuantumSuperposition` :
    Summation of two states leads to a quantum superposition with
    equal amplitude. Simply adding two vectors makes no sense.

    `QuantumState` + `NULL_STATE` -> `QuantumState` : Quantum state
    adds a null state changes nothing.

    `QuantumState` + `QuantumSuperposition` -> `QuantumSuperposition` :
    Adding a quantum state to a superposition creates a new superposition.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.state_add'
    _NOT_APPLICABLE_ERROR_ = QuantumStateAlgebraFunctionError(
            "State add function is only applicable to quantum state and " +\
            "quantum superposition.", location=_ERROR_LOCATION_)

    ret = None
    if isinstance(lstate, QuantumState) and isinstance(rstate, QuantumState):
        ret = QuantumSuperposition(superlist=[(1.0, lstate), (1.0, rstate)])
    elif isinstance(lstate, QuantumState) \
            and isinstance(rstate, QuantumSuperposition):
        sl = rstate.as_superlist()
        sl.append((1.0, lstate,))
        ret = QuantumSuperposition(superlist=sl)
    elif isinstance(lstate, QuantumSuperposition) \
            and isinstance(rstate, QuantumState):
        sl = lstate.as_superlist()
        sl.append((1.0, rstate,))
        ret = QuantumSuperposition(superlist=sl)
    elif isinstance(lstate, NullState):
        if isinstance(rstate, (QuantumState, QuantumSuperposition, NullState,)):
            ret = rstate
        else:
            raise _NOT_APPLICABLE_ERROR_
    elif isinstance(rstate, NullState):
        if isinstance(lstate, (QuantumState, QuantumSuperposition, NullState,)):
            ret = lstate
        else:
            raise _NOT_APPLICABLE_ERROR_
    else:
        raise _NOT_APPLICABLE_ERROR_
    return ret


def state_sub(lstate, rstate):
    """ Subtraction of two states

    Calculate `|lstate> - |rstate>`.

    TODO What if two states are identical?

    RULES

    `QuantumState` - `QuantumState` -> `QuantumSuperposition`

    `QuantumState` - `NULL_STATE` -> `QuantumState`

    `NULL_STATE` - `QuantumState` -> `QuantumSuperposition`

    `QuantumState` - `QuantumSuperposition` -> `QuantumSuperposition`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.state_sub'
    _NOT_APPLICABLE_ERROR_ = QuantumStateAlgebraFunctionError(
            "State sub function is only applicable to quantum state and " +\
            "quantum superposition.", location=_ERROR_LOCATION_)

    ret = None
    if isinstance(lstate, QuantumState) and isinstance(rstate, QuantumState):
        ret = QuantumSuperposition(superlist=[(1.0, lstate), (-1.0, rstate)])
    elif isinstance(lstate, QuantumState) \
            and isinstance(rstate, QuantumSuperposition):
        super_list = state_scale(-1.0, rstate).as_superlist()
        super_list.append((1.0, lstate))
        ret = QuantumSuperposition(superlist=super_list)
    elif isinstance(lstate, QuantumSuperposition) \
            and isinstance(rstate, QuantumState):
        super_list = lstate.as_superlist()
        super_list.append((-1.0, rstate))
        ret = QuantumSuperposition(
                superlist=super_list)
    elif isinstance(rstate, NullState):
        if isinstance(lstate, (QuantumState, QuantumSuperposition, NullState,)):
            ret = lstate
        else:
            raise _NOT_APPLICABLE_ERROR_
    elif isinstance(lstate, NullState):
        if isinstance(rstate, NullState):
            ret = NULL_STATE
        elif isinstance(rstate, QuantumState):
            ret = QuantumSuperposition(superlist=[(-1.0, rstate)])
        elif isinstance(rstate, QuantumSuperposition):
            ret = state_scale(-1.0, rstate)
        else:
            raise _NOT_APPLICABLE_ERROR_
    else:
        raise _NOT_APPLICABLE_ERROR_
    return ret


def state_inner(lstate, rstate):
    """ Inner product of two states

    Inner product with a state or superposition, calculates
        `<lstate|rstate>`
    Superposition if first converted into state.

    Inner product of two states is by definition the
    inner product of complex conjugated vector of
    `lstate` and the vector of `lstate`. Two state
    vectors must have the same size.

    RETURN

    A complex number
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.state_inner'
    _NOT_APPLICABLE_ERROR_ = QuantumStateAlgebraFunctionError(
            "State inner product is only applicable to quantum " +\
            "state and quantum superposition of the same dimension.",
            location=_ERROR_LOCATION_)

    ret = None
    try:
        if lstate is NULL_STATE or rstate is NULL_STATE:
            ret = 0.0
        elif isinstance(lstate, (QuantumState, QuantumSuperposition,)) \
                and isinstance(rstate, (QuantumState, QuantumSuperposition,)):
            ret = inner(lstate.as_vector(), rstate.as_vector())
        else:
            raise _NOT_APPLICABLE_ERROR_
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)
    return ret


@QSAF_Decorator(
    argument_type={
        'lstate': (QuantumState, QuantumSuperposition,),
        'rstate': (QuantumState, QuantumSuperposition,)
    }
)
def state_outer(lstate, rstate):
    """ Outer product of two states

    Outer product calculates
        `|lstate><rstate|`
    where superposition is first converted into state.

    Object `lstate` is treated as ket (column vector)
    and `rstate` is treated as bra (row vector).

    RETURN

    Outcome of outer product is a square matrix.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.state_outer'
    return outer(lstate.as_vector(), rstate.as_vector())


@QSAF_Decorator(
    argument_type={
        'lstate': (QuantumState, QuantumSuperposition, NullState,),
        'rstate': (QuantumState, QuantumSuperposition, NullState,)
    }
)
def state_kronecker(lstate, rstate):
    """ Kronecker product of two states

    Calculate `|lstate> o |rstate>`, where `o` stands for
    Kronecker product.

    RULES

    `QuantumState` o `QuantumState` -> `QuantumState` : Kronecker
    of two quantum sate is a quantum state with larger size.

    `QuantumState` o `Superposition` -> `QuantumState` : Kronecker
    of quantum sate and superposition is a state with larger size.
    Superposition is first converted into a state.

    `Superposition` o `Superposition` -> `QuantumState` : Kronecker
    of two superpositions is a state with larger size.
    Superposition is first converted into a state.

    `QuantumState` o `NULL_STATE` -> `NULL_STATE` : With one null
    state, the result shall naturally a null state.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.state_kronecker'
    ret = None
    if isinstance(lstate, (QuantumState, QuantumSuperposition,)) \
            and isinstance(rstate, (QuantumState, QuantumSuperposition,)):
        ret = QuantumState(
            vector=kronecker(lstate.as_vector(),rstate.as_vector()))
    elif isinstance(lstate, NullState) or isinstance(rstate, NullState):
        ret = NULL_STATE
    else:
        raise QuantumStateAlgebraFunctionError("Tensor product applies " +\
                "to quantum states only.", location=_ERROR_LOCATION_)
    return ret


def state_kron(lstate, rstate):
    """ Alias to state_kronecker """
    return state_kronecker(lstate, rstate)


def state_tensor(lstate, rstate):
    """ Tensor product of two states """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.state_tensor'
    ret = None
    try:
        ret = state_kronecker(lstate, rstate)
    except Exception as err:
        raise err.relocate(_ERROR_LOCATION_)
    return ret
