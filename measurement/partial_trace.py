#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

measurement.partial_trace.py

PATH

[app_root]/measurement/partial_trace.py

INTRO

Partial trace over a density matrix or a quantum state.

Partial trace is an important operation often required
before measurement. In this package, it is an independent
module that can be used not only by measurement functions,
but also other quantum-mechanical operators.

The design philosophy is that partial trace must be
functional, not descriptive.

LOG

Updated on 13 October 2021 | Created on 08 April 2021
"""
from bit import integer_to_bitstring, Bitstring_Literal_Type
from linear_space.number import exponent_of_two, power_of_two
from linear_space.matrix import Matrix, SquareMatrix
from linear_space.algebra import matrix_product, matrix_add, kronecker,\
    hermitian_conjugate
from linear_space.utils import identity_by_bits

from quantum_state import QuantumState
from qubit.qubit import QubitState, ComputationalBasis
from qubit.index_range import IndexRangeValidator
from density_matrix.density_matrix import DensityMatrix, QubitDensityMatrix

from .errors import PartialTraceError
from .decorators import as_measurement_function

_MODULE_LOCATION_ = 'measurement.partial_trace'


# Support functions
@as_measurement_function(argument_type={
    'bitstring': Bitstring_Literal_Type
})
def _left_matrix_for_bitstring(total_noq, first_index, bitstring):
    """ Construct left matrix for a bitstring

    Left matrix is consrtucted according to
        `I x <01..0| x I`,
    where the bra covers the qubits to be partially
    traced out. Size of identity matrix is determined
    by the index of the first bit of the state (to be
    trace out). In general, there are 3 scenarios,
        `<01..0| x I`
    where partial tracing start from the first bit;
        `I x <01..0|`
    where the last few bits are to be traced out;
        `I x <01..0| x I`
    where the bits in the middle are to be traced out.

    ARGUMENTS

    `first_index` (`int`) : index of the first bit (of
    the computational basis) with respect to the joint
    state, usually the global state

    `bitstring` (`str`) : bitstring literal represents
    a computational basis state used for partial trace;
    length of this literal must not be longer than the
    total number of qubits in the joint state
    """
    ret = None
    # NOQ of the state to be traced out
    basis_noq = len(bitstring)
    compbasis = ComputationalBasis(bitstring=bitstring)
    if total_noq == basis_noq:
        ret = compbasis.as_bra().as_vector()
    else:
        if first_index == 0:
            idm = identity_by_bits(total_noq - basis_noq)
            ret = kronecker(compbasis.as_bra().as_vector(), idm)
        elif first_index == total_noq - basis_noq:
            idm = identity_by_bits(first_index)
            ret = kronecker(
                idm,
                compbasis.as_bra().as_vector()
            )
        else:
            lidm = identity_by_bits(first_index)
            ridm = identity_by_bits(total_noq - first_index - basis_noq)
            ret = kronecker(
                lidm,
                kronecker(
                    compbasis.as_bra().as_vector(),
                    ridm
                )
            )
    return ret


@as_measurement_function(argument_type={
    'state': QubitState
})
def _left_matrix_for_state(total_noq, first_index, state):
    """ Construct left matrix for a qubit state

    TODO Not unittested.

    Left matrix is consrtucted according to
        `I x <state| x I`,
    where the bra covers the qubits to be partially
    traced out. Size of identity matrix is determined
    by the index of the first bit of the state (to be
    trace out). In general, there are 3 scenarios,
        `<state| x I`
    where partial tracing start from the first bit;
        `I x <state|`
    where the last few bits are to be traced out;
        `I x <state| x I`
    where the bits in the middle are to be traced out.

    ARGUMENTS

    `first_index` (`int`) : index of the first bit (of
    the computational basis) with respect to the joint
    state, usually the global state

    `state` (`QubitState`) : qubit state used for partial
    trace; noq of this state must not be longer than the
    total noq in the joint state; qubit state can be a
    superposition of computational basis
    """
    ret = None
    # noq of the state to be traced out
    state_noq = state.noq
    # Generic qubit state has no as_bra method,
    # must manually calculate hermitian conjugate
    if total_noq == state_noq:
        ret = hermitian_conjugate(state.as_vector())
    else:
        if first_index == 0:
            idm = identity_by_bits(total_noq - state_noq)
            ret = kronecker(
                hermitian_conjugate(state.as_vector()),
                idm
            )
        elif first_index == total_noq - state_noq:
            idm = identity_by_bits(first_index)
            ret = kronecker(
                idm,
                hermitian_conjugate(state.as_vector())
            )
        else:
            lidm = identity_by_bits(first_index)
            ridm = identity_by_bits(total_noq - first_index - state_noq)
            ret = kronecker(
                lidm,
                kronecker(
                    hermitian_conjugate(state.as_vector()),
                    ridm
                )
            )
    return ret


@as_measurement_function(argument_type={
    'bitstring': Bitstring_Literal_Type,
    'state': QubitState
})
def _left_matrix(total_noq, first_index, bitstring=None, state=None):
    """ Construct left matrix for partial trace

    A dispatcher function.

    ARGUMENTS

    `first_index` (`int`) : index of the first bit (of
    the computational basis or qubit state) with respect
    to the joint state, usually the global state

    `bitstring` (`str`) : optional; bitstring literal represents
    a computational basis state used for partial trace;
    length of this literal must not be longer than the
    total number of qubits in the joint state

    `state` (`QubitState`) : optional; qubit state used for partial
    trace; noq of this state must not be longer than the
    total noq in the joint state; qubit state can be a
    superposition of computational basis
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '._left_matrix'
    ret = None
    if bitstring is not None and state is None:
        ret = _left_matrix_for_bitstring(total_noq, first_index, bitstring)
    elif bitstring is None and state is not None:
        ret = _left_matrix_for_state(total_noq, first_index, state)
    else:
        raise PartialTraceError("To construct a left matrix, " +\
                "either a bitstring or a qubit state must be " +\
                "provided, but not both.", location=_ERROR_LOCATION_)
    return ret


@as_measurement_function(argument_type={
    'bitstring': Bitstring_Literal_Type
})
def _right_matrix_for_bitstring(total_noq, first_index, bitstring):
    """ Construct right matrix for a bitstring

    The right counterpart of the left matrix.

    Right matrix is consrtucted according to
        `I x |01..0> x I`,
    where the ket covers the qubits to be partially
    traced out. Size of the identity matrix is
    determined by the same way as the left matrix.
    """
    ret = None
    # noq of state to be traced out
    basis_noq = len(bitstring)
    compbasis = ComputationalBasis(bitstring=bitstring)
    if total_noq == basis_noq:
        ret = compbasis.as_vector()
    else:
        if first_index == 0:
            idm = identity_by_bits(total_noq - basis_noq)
            ret = kronecker(compbasis.as_vector(), idm)
        elif first_index == total_noq - basis_noq:
            idm = identity_by_bits(first_index)
            ret = kronecker(idm, compbasis.as_vector())
        else:
            lidm = identity_by_bits(first_index)
            ridm = identity_by_bits(total_noq - first_index - basis_noq)
            ret = kronecker(
                lidm,
                kronecker(
                    compbasis.as_vector(),
                    ridm
                )
            )
    return ret


@as_measurement_function(argument_type={
    'state': QubitState
})
def _right_matrix_for_state(total_noq, first_index, state):
    """ Construct right matrix for a qubit state

    TODO Not unittested.

    The right counterpart of the left matrix.

    Right matrix is consrtucted according to
        `I x |01..0> x I`,
    where the ket covers the qubits to be partially
    traced out. Size of the identity matrix is
    determined by the same way as the left matrix.
    """
    ret = None
    # NOQ of state to be traced out
    state_noq = state.noq
    if total_noq == state_noq:
        ret = state.as_vector()
    else:
        if first_index == 0:
            idm = identity_by_bits(total_noq - state_noq)
            ret = kronecker(state.as_vector(), idm)
        elif first_index == total_noq - state_noq:
            idm = identity_by_bits(first_index)
            ret = kronecker(idm, state.as_vector())
        else:
            lidm = identity_by_bits(first_index)
            ridm = identity_by_bits(total_noq - first_index - state_noq)
            ret = kronecker(
                lidm,
                kronecker(
                    state.as_vector(),
                    ridm
                )
            )
    return ret


@as_measurement_function(argument_type={
    'bitstring': Bitstring_Literal_Type,
    'state': QubitState
})
def _right_matrix(total_noq, first_index, bitstring=None, state=None):
    """ Construct right matrix for partial trace """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '._right_matrix'
    ret = None
    if bitstring is not None and state is None:
        ret = _right_matrix_for_bitstring(total_noq, first_index, bitstring)
    elif bitstring is None and state is not None:
        ret = _right_matrix_for_state(total_noq, first_index, state)
    else:
        raise PartialTraceError("To construct a right matrix, " +\
                "either a bitstring or a qubit state must be " +\
                "provided, but not both.", location=_ERROR_LOCATION_)
    return ret


@as_measurement_function(argument_type={
    'density_matrix': QubitDensityMatrix
})
def partial_trace_out_index_range(density_matrix, index_range_bound):
    """ Partial tracing out a range of qubits

    Index range bound comprehension is based on the
    following rules.

    [Single bit]
    If `index_range_bound` is a list of two identical
    integers, bound represents one integer. The single
    qubit represented by this integer is traced out.
    This is the simplest case.

    [Multiple bits]
    If `index_range_bound` is a list of two non-identical
    integers, qubit state in this range will be traced out
    via computational basis. (NOTE Basis selection is yet
    to be implemented; current default is computational basis.)
    In this case, computational basis states for the given
    number of qubits (in the range) are used for partial
    tracing. For example, if in total 2 qubits are to be
    traced out, basis states are |00>, |01>, |10>, and |11>.

    ARGUMENTS

    `density_matrix` (`DensityMatrix`) : system represented
    by a density matrix

    `index_range_bound` (`list`) : index range bound that
    defines the range of a group of continuous qubits in the
    system; if both integers are identical, a single qubit
    specified by that index is traced out.

    RETURN

    Density matrix with reduced dimension.

    CASES

    Partially trace out one qubit register from a joint system.

    NOTE Don't create all matrices simultaneously; better
    create them per request.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.partial_trace_out_index_range'
    ret = None
    validated_bound = None
    reduced = 0
    first_index = 0
    system_noq = exponent_of_two(density_matrix.nrows)
    # Must validate against total noq
    validator = IndexRangeValidator(noq=system_noq, bound=index_range_bound)
    if validator.is_valid:
        validated_bound = validator.validated_data()['bound']
    else:
        validator.raise_last_error()
    # validated bound is always in normal order
    if validated_bound[1] > validated_bound[0]:
        # number of bits to be traced out
        number_of_bits = validated_bound[1] - validated_bound[0] + 1
        first_index = validated_bound[0]
    else:
        # only 1 bit to be traced out
        number_of_bits = 1
        first_index = validated_bound[0]
    # create first bitstring for computational basis
    initstring = integer_to_bitstring(integer=0, total_digits=number_of_bits)
    reduced = matrix_product(
        _left_matrix(system_noq,first_index, bitstring=initstring),
        matrix_product(
            density_matrix,
            _right_matrix(system_noq, first_index, bitstring=initstring)
        )
    )
    for integer in range(1, power_of_two(number_of_bits), 1):
        bit_string = integer_to_bitstring(integer=integer,
                total_digits=number_of_bits)
        reduced = matrix_add(
            reduced,
            matrix_product(
                _left_matrix(system_noq, first_index, bitstring=bit_string),
                matrix_product(
                    density_matrix,
                    _right_matrix(system_noq, first_index, bitstring=bit_string)
                )
            )
        )
    # reduced density matrix is either a matrix or a scalar/number
    if isinstance(reduced, Matrix):
        ret = QubitDensityMatrix(matrix=SquareMatrix(array=reduced.as_array()))
    else:
        # a scalar
        ret = reduced
    return ret


@as_measurement_function(argument_type={
    'density_matrix': QubitDensityMatrix,
    'bitstring': Bitstring_Literal_Type
})
def partial_trace_out_bitstring(density_matrix, bitstring):
    """ Partial trace out a basis given in bitstring

    Tracing out one computational basis from the
    density matrix. In fact, this operation measures
    the probability of finding the sytem in a given
    basis.

    Number of qubits in bitstring (length of the string)
    must match the total number of qubits implied in the
    density matrix.

    RETURN

    Probability of the basis represented by bitstring.

    ARGUMENTS

    `density_matrix` (`DensityMatrix`) : density matrix
    that represents the system on which the partial trace
    is performed

    `bitstring` (`str`) : the bit string that represents
    the computational basis state to be traced out from
    the density matrix

    CASES

    Measure the probability of finding the system in the
    given basis state.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.partial_trace_out_bitstring'
    total_noq = exponent_of_two(density_matrix.nrows)
    # NOQ of basis to be traced out
    basis_noq = len(bitstring)
    if basis_noq == total_noq:
        compbasis = ComputationalBasis(bitstring=bitstring)
        ret = matrix_product(compbasis.as_bra().as_vector(),
                matrix_product(density_matrix, compbasis.as_vector()))
    else:
        raise PartialTraceError("If only a bit string is "  +\
                "provided to perform a partial trace, its " +\
                "length must be the same as the number of " +\
                "qubits the density matrix represents.",
                location=_ERROR_LOCATION_)
    return ret


@as_measurement_function(argument_type={
    'density_matrix': QubitDensityMatrix,
    'bitstring': Bitstring_Literal_Type
})
def partial_trace_out_bitstring_in_index_range(
        density_matrix, bitstring, index_range_bound):
    """ Partial tracing out a basis in a given range

    RETURN

    Either a reduced density matrix, if range is narrower
    than the total noq; or a number (probability) if the
    range covers the entire system.

    CASES

    Measure the probability of finding the qubits in the
    given index range being in the given basis state.
    For example, in a joint state |0110101>, one wants to
    know the probability of qubits ranging [2,4] being in
    state |001>. In this case, range bound is [2,3] and
    bitstring is '001'.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ +\
            '.partial_trace_out_bitstring_in_index_range'
    system_noq = exponent_of_two(density_matrix.nrows)
    valid_bound = []
    number_of_bits = 0
    first_index = 0
    reduced = None
    ret = None

    bound_validator = IndexRangeValidator(
            noq=system_noq, bound=index_range_bound)
    # Validate index range bound
    if bound_validator.is_valid:
        valid_bound = bound_validator.validated_data()['bound']
    else:
        raise bound_validator.raise_last_error()
    # Get noq in the range
    if valid_bound[1] > valid_bound[0]:
        number_of_bits = valid_bound[1] - valid_bound[0] + 1
        first_index = valid_bound[0]
    else:
        number_of_bits = 1
        first_index = valid_bound[0]
    # Bitstring must have the same noq
    # defined by the index range bound.
    if number_of_bits == len(bitstring):
        reduced = matrix_product(
            _left_matrix(system_noq, first_index, bitstring=bitstring),
            matrix_product(
                density_matrix,
                _right_matrix(system_noq, first_index, bitstring=bitstring)
            )
        )
        # Make a density matrix.
        if isinstance(reduced, Matrix):
            ret = QubitDensityMatrix(matrix=SquareMatrix(array=reduced.as_array()))
        else:
            # If a scalar
            ret = reduced
    else:
        raise PartialTraceError("While partial tracing out a " +\
                "bitstring in index range, the number of qubits " +\
                "defined by the range is different from that of " +\
                "the bitstring. This is forbidden.",
                location=_ERROR_LOCATION_)
    return ret


@as_measurement_function(argument_type={
    'density_matrix': QubitDensityMatrix,
    'state': QubitState
})
def partial_trace_out_state_in_index_range(
        density_matrix, state, index_range_bound):
    """ Partially trace out a qubit state in a given range

    CASES

    Use cases of this function are quite similar to
    `partial_trace_out_bitstring_in_index_range`,
    except a generic qubit state replaces basis.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ +\
            '.partial_trace_out_state_in_index_range'
    system_noq = exponent_of_two(density_matrix.nrows)
    valid_bound = []
    number_of_bits = 0
    first_index = 0
    reduced = None
    ret = None

    bound_validator = IndexRangeValidator(noq=system_noq, bound=index_range_bound)
    # validate index range bound
    if bound_validator.is_valid:
        valid_bound = bound_validator.validated_data()['bound']
    else:
        raise bound_validator.raise_last_error()
    # Get noq in the range
    if valid_bound[1] > valid_bound[0]:
        number_of_bits = valid_bound[1] - valid_bound[0] + 1
        first_index = valid_bound[0]
    else:
        number_of_bits = 1
        first_index = valid_bound[0]
    # Bitstring must have the same noq
    # defined by the index range bound.
    if number_of_bits == state.noq:
        reduced = matrix_product(
            _left_matrix(system_noq, first_index, state=state),
            matrix_product(
                density_matrix,
                _right_matrix(system_noq, first_index, state=state)
            )
        )
        if isinstance(reduced, Matrix): # If matrix, make a density matrix.
            ret = QubitDensityMatrix(matrix=SquareMatrix(array=reduced.as_array()))
        else: # Otherwise, probability as a scalar
            ret = reduced
    else:
        raise PartialTraceError("While partial tracing out a " +\
                "state in index range, the number of qubits "  +\
                "defined by the range is different from that " +\
                "of the state. This is forbidden.", location=_ERROR_LOCATION_)
    return ret


@as_measurement_function(argument_type={
    'density_matrix': DensityMatrix,
    'state': QuantumState
})
def partial_trace_with_state(density_matrix, state):
    """ Partial tracing out one particular state

    Similar to the case with bit string, this is basically
    sandwichiing a density matrix with one particular state.
    Since the state here is not necessarily a qubit state,
    the size of state vector (of `state`) must match the size
    of system's density matrix.

    RETURN

    Probability of that particular state.

    ARGUMENTS

    `density_matrix` (`DensityMatrix`): the density matrix on
    which a quantum state is to be partially traced out

    `state` (`QuantumState`): the state to be traced out on
    the given density matrix; its dimension must be compatible
    with the density matrix
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.partial_trace_with_state'
    ret = 0
    if density_matrix.ncols == state.as_vector().size:
        # shall be a probability
        ret = matrix_product(
            hermitian_conjugate(state.as_vector()),
            matrix_product(density_matrix, state.as_vector()))
    else:
        raise PartialTraceError("Quantum state used in partial " +\
                "tracing has a size that doesn't match that of the " +\
                "density matrix.",
                location=_ERROR_LOCATION_)
    return ret


# Primary partial trace function
@as_measurement_function(argument_type={
    'system': (QubitDensityMatrix, QubitState,),
    'bitstring': Bitstring_Literal_Type,
    'state': QubitState
})
def partial_trace(system, bitstring=None, index_range_bound=None, state=None):
    """ Partial trace function

    Partial trace function is applied directly on a system to
    obtain a reduced density matrix or probability.

    ARGUMENTS

    `system`: the system on which a partial trace is performed;
    system must be either a density matrix or a qubit state;
    this argument is required

    `bitstring` (`str`) : partial trace out the state (computational
    basis) represented by a bit string; a bit string variable

    `index_range_bound` (`list`) : partial trace out the qubit states
    represented by the indices given in the range; must be a list
    of exactly two elements

    `state` (`QubitState`) : partial trace out the state represented
    by this argument; it must be an instance of `QubitState`;
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.partial_trace'
    ret = None
    density_matrix = None
    if isinstance(system, QubitDensityMatrix):
        density_matrix = system
    else:
        density_matrix = QubitDensityMatrix(state=system)

    # both bit string and state, error!
    if not state is None and not bitstring is None:
        raise PartialTraceError("Partial trace doesn't accept " +\
                "a bit string and a state simultaneously.",
                location=_ERROR_LOCATION_)
    # only bit string
    elif not bitstring is None and index_range_bound is None:
        try:
            ret = partial_trace_out_bitstring(density_matrix, bitstring)
        except Exception as e:
            raise PartialTraceError(str(e), location=_ERROR_LOCATION_)
    # both bit string and bit range
    elif not bitstring is None and not index_range_bound is None:
        try:
            ret = partial_trace_out_bitstring_in_index_range(
                    density_matrix, bitstring, index_range_bound)
        except Exception as e:
            raise PartialTraceError(str(e), location=_ERROR_LOCATION_)
    # only state
    elif not state is None and index_range_bound is None:
        try:
            ret = partial_trace_with_state(density_matrix, state)
        except Exception as e:
            raise PartialTraceError(str(e), location=_ERROR_LOCATION_)
    # state with bit range
    # TODO Yet to be implemented.
    elif not state is None and not index_range_bound is None:
        try:
            ret = partial_trace_out_state_in_index_range(
                    density_matrix, state, index_range_bound)
        except Exception as e:
            raise PartialTraceError(str(e), location=_ERROR_LOCATION_)
    # only bit range
    else:
        try:
            ret = partial_trace_out_index_range(density_matrix, index_range_bound)
        except Exception as e:
            raise PartialTraceError(str(e), location=_ERROR_LOCATION_)
    return ret
