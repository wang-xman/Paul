#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

measurement.projective.py

PATH

[app_root]/measurement/projective.py

INTRO

Projective measurement.

Projective measurement is perhaps the most popular
measurement scheme used in qubit-base quantum computer.

Any projective measurement involves both a 'system' and
a quantum 'state', to which the system is projected.
The outcome of a projective measurement is a probability,
a real number, and a post-measurement system, usually
represented by a quantum state or a reduced density matrix.

A projective measurement on a sub-system usually requires
partially tracing out the rest of the system. In the current
design, the projective measurement is factored out as an
independent module that performs measuremnt using a state
on a system of the same dimension. This means if a measurement
on a subsystem is requested, a partial trace may have to be
performed manually and separately. One advantage of this design
is the separation of logics and functionalities.

Projective measurement mechanism is provided via helper
functions. Measurement is functional, not descriptive.

LOG

Updated on 08 October 2021 | Created on 10 April 2021
"""
from bit import integer_to_bitstring, Bitstring_Literal_Type
from linear_space.number import exponent_of_two, power_of_two
from linear_space.algebra import matrix_product
from quantum_state.quantum_state import QuantumState
from qubit import QubitState, ComputationalBasis
from density_matrix import DensityMatrix

from .errors import ProjectiveMeasurementError
from .decorators import as_measurement_function

_MODULE_LOCATION_ = 'measurement.projective'


@as_measurement_function(argument_type={
    'system': (DensityMatrix, QuantumState,),
    'state': QuantumState
})
def projective_on_state(system, state):
    """ Projective measurement on a generic quantum state

    ARGUMENTS

    `system` (`DensityMatrix` or `QuantumState`): required;
    quantum system on which measurement is perfromed;
    can be either a density matrix or a quantum state

    `state` (`QuantumState`): required; quantum state to which
    the projective measurement on the system is made
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.projective_on_state'
    system_density_matrix = None
    projection_matrix = None
    probability = None
    if isinstance(system, DensityMatrix):
        system_density_matrix = system
    else:
        system_density_matrix = DensityMatrix(state=system)
    projection_matrix = DensityMatrix(state=state)
    if system_density_matrix.ncols == projection_matrix.nrows:
        probability = matrix_product(system_density_matrix,
                                     projection_matrix).trace
    else:
        raise ProjectiveMeasurementError("Dimension of the " +\
                "state used in projection operation doesn't " +\
                "match the dimension of the system to be measured.",
                location=_ERROR_LOCATION_)
    return probability


@as_measurement_function(argument_type={
    'system': (DensityMatrix, QuantumState,),
    'basis': Bitstring_Literal_Type
})
def projective_on_basis(system, basis):
    """ Projective measurement on a computational basis

    ARGUMENTS

    `system` (`DensityMatrix` or `QuantumState`): required;
    system refers to the quantum system on which a measurement
    is performed; either a density matrix or a quantum state

    `basis` (`str`): required; a bitstring literal that represents
    a computational basis state; projective measurement is made
    using this basis state

    RETURN

    Probability of finding system in the given basis state.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.projective_on_basis'
    probability = 0.0
    system_match = False
    if isinstance(system, DensityMatrix):
        if len(basis) == exponent_of_two(system.nrows):
            system_match = True
    elif isinstance(system, QubitState):
        if len(basis) == system.noq:
            system_match = True
    else:
        if system.dim == power_of_two(2, len(basis)):
            system_match = True
    # system and basis must match
    if system_match is True:
        try:
            state = ComputationalBasis(bitstring=basis)
            probability = projective_on_state(system, state)
        except Exception as e:
            raise ProjectiveMeasurementError(str(e), location=_ERROR_LOCATION_)
    else:
        raise ProjectiveMeasurementError("Dimension of the " +\
                "state used in projection operation doesn't " +\
                "match the dimension of the system to be measured.",
                location=_ERROR_LOCATION_)
    return probability


@as_measurement_function(argument_type={
    'system': (DensityMatrix, QubitState,)
})
def projective_all(system):
    """ Projective measurement on all computational basis

    Density matrix or system must be originating from
    qubit state.

    RETURN

    A dictionary that contains bit string as keys and
    the corresponding probability as value,
        {
            '00': 0.5,
            '01': 0.0,
            '10': 0.0,
            '11': 0.5,
        }
    where all basis states allowed by the number of qubits
    are listed.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.projective_all'
    noq = None
    probdict = {}
    # validate system
    if isinstance(system, DensityMatrix):
        noq = exponent_of_two(system.nrows)
    elif isinstance(system, QubitState):
        noq = system.noq
    else:
        raise ProjectiveMeasurementError('Measurement in ' +\
                'basis requires the system be composed '   +\
                'of qubit states.', location=_ERROR_LOCATION_)
    # indeed qubit state based system
    if not noq is None:
        for i in range(0, power_of_two(noq), 1):
            bitstring = integer_to_bitstring(integer=i, total_digits=noq)
            prob = projective_on_basis(system, bitstring)
            probdict[bitstring] = prob
    return probdict


# Primary function
@as_measurement_function(argument_type={
    'system': (DensityMatrix, QubitState,),
    'basis': Bitstring_Literal_Type
})
def projective(system, basis=None, state=None):
    """ Projective measurement function

    Projective measurement is performed on a density
    matrix and the system is thus required to be either
    a density matrix or a quantum state. Projection
    operator is constructed using either a `basis`
    (computataional basis) or a generic `state` (quantum
    state); these two options are mutually exclusive.

    ARGUMENTS

    `system` (`DensityMatrix` or `QuantumState`) : required;
    system refers to the quantum system on which a measurement
    is performed; can be either a density matrix or quantum state

    `basis` (`ComputationalBasis`) : bitstring literal represents
    a computational basis state; projective measurement is made
    using this state; it is required when `state` is `None`

    `state` (`QuantumState`): quantum state with which the
    projective measurement on the system is made; it is
    required when `basis` is `None`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.projective'
    probability = None
    # both basis and state are provided, error!
    if not basis is None and not state is None:
        raise ProjectiveMeasurementError("To perform " +\
                "projective measuremnt, either a bit string of a " +\
                "computational basis or a quantum state must be " +\
                "provided. But not both.", location=_ERROR_LOCATION_)
    # only basis is provided
    elif not basis is None:
        try:
            probability = projective_on_basis(system, basis)
        except Exception as err:
            raise err
    # only state is provided
    elif not state is None:
        try:
            probability = projective_on_state(system, state)
        except Exception as err:
            raise err
    # neither basis nor state is provided
    else:
        try:
            probability = projective_all(system)
        except Exception as err:
            raise err
    return probability
