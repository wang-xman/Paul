#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.single_qubit.py

PATH

[app_root]/gate/single_qubit.py

INTRO

Hardcoded single-qubit gates.

As a convention, prototype and decorator classes are named using
either lower case or mixture with underlines to emphasise that it
is not intended for instantiation as a common class. In the following,
letter `j` is used to represent imaginary unit, to be consistent
with numpy convention.

CONTENT

`Pauli_X` - Pauli X gate, flips a bit; symbol 'X'

`Pauli_Y` - Pauli Y gate; symbol 'Y'

`Pauli_Z` - Pauli Z gate; symbol 'Z'

`Phase` - Phase gate; symbol 'S'

`Flip_Single_Qubit` - Flips a single qubit, identical to Pauli X

`Walsh_Hadamard` - Walsh-Hadamard gate for single qubit

`Eighth_Pi` - One-eighth gate; symbol 'T'

`Rotation_About_X` - Rotation about x-axis in Bloch sphere; symbol 'Rx'

`Rotation_About_Y` - Rotation about y-axis in Bloch sphere; symbol 'Ry'

`Rotation_About_Z` - Rotation about z-axis in Bloch sphere; symbol 'Rz'

`Parameterised_Phase_Rotation` - Phase rotation with two parameters;
symbol 'PPR'

`Inverse_Parameterised_Phase_Rotation` - Inverse operation to parameterised
phase rotation

LOG

Updated on 22 September 2021 | Created on 29 June 2020
"""
import sys
import inspect
import numpy as np

from linear_space.matrix import SquareMatrix, PAULI_X, PAULI_Y, PAULI_Z, HADAMARD

from gate.base import GateRegistrationError
from gate.parameter import GateParameter
from gate.prototype.base import SingleQubitGatePrototype
from gate.decorator.decorator import as_gate


@as_gate
class Pauli_X(SingleQubitGatePrototype):
    """ Single Qubit Gate : Pauli matrix X

    ACTION

    Flips a single qubit state. For example
        `a|0> + b|1> -> a|1> + b|0>, |0> -> |1>, |1> -> |0>`

    PARAMS (None)

    MATRIX

    Pauli X matrix is
        `[[0 1], [1 0]]`

    SYMBOL `X`
    """
    minimal_number_of_qubits = 1
    alias = 'PauliX'
    symbol = 'X'
    parameters = {}

    def gate_matrix(self):
        return PAULI_X


@as_gate
class Pauli_Y(SingleQubitGatePrototype):
    """ Single Qubit Gate : Pauli matrix Y

    ACTION

    Flips a single qubit state. For example
        `|0> -> j|1>, |1> -> -j|0>`

    PARAMS (None)

    MATRIX

    Pauli Y matrix is
        `[[0 -j], [j 0]]`

    SYMBOL `Y`
    """
    minimal_number_of_qubits = 1
    alias = 'PauliY'
    symbol = 'Y'
    parameters = {}

    def gate_matrix(self):
        return PAULI_Y


@as_gate
class Pauli_Z(SingleQubitGatePrototype):
    """ Single Qubit Gate : Pauli matrix Z

    ACTION

    Flips a single qubit state. For example
        `|0> -> |0>, |1> -> -|1>`

    PARAMS (None)

    MATRIX

    Pauli Z matrix is
        `[[1 0], [0 -1]]`

    SYMBOL `Z`
    """
    minimal_number_of_qubits = 1
    alias = 'PauliZ'
    symbol = 'Z'
    parameters = {}

    def gate_matrix(self):
        return PAULI_Z


@as_gate
class Flip_Single_Qubit(SingleQubitGatePrototype):
    """ Single Qubit Gate : Single-qubit flip

    ACTION

    Flips a single qubit state. For example
        `a|0> + b|1> -> a|1> + b|0>, |0> -> |1>, |1> -> |0>`

    PARAMS (None)

    MATRIX

    Identical to Pauli X matrix
        `[[0 1], [1 0]]`

    SYMBOL `X`
    """
    minimal_number_of_qubits = 1
    alias = 'Flip'
    symbol = 'X'
    parameters = {}

    def gate_matrix(self):
        return PAULI_X


@as_gate
class Walsh_Hadamard(SingleQubitGatePrototype):
    """ Single Qubit Gate : Walsh-Hadamard gate

    ACTION

    Transform a state as
        `|0> -> (|0> + |1>) /sqrt(2), |1> -> (|0> - |1>) /sqrt(2)`

    PARAMS (None)

    MATRIX

    Identical to Pauli X matrix
        `[[1 1], [1 -1]] / sqrt(2)`

    SYMBOL `H`
    """
    minimal_number_of_qubits = 1
    alias = 'Hadamard'
    symbol = 'H'
    parameters = {}

    def gate_matrix(self):
        return HADAMARD


@as_gate
class Phase(SingleQubitGatePrototype):
    """ Phase gate

    ACTION

    Append a phase factor of half pi `exp(j pi/2)` to `|1>` component.
    Transform a state as
        `|0> -> |0>, |1> -> j |1>`

    PARAMS (None)

    MATRIX

    Identical to Pauli X matrix
        `[[1 0], [0 j]]`

    SYMBOL `S`
    """
    minimal_number_of_qubits = 1
    alias = 'Phase'
    symbol = 'S'
    parameters = {}

    def gate_matrix(self):
        return SquareMatrix(array=np.array([[1.0, 0.0], [0.0, 1.j]]))


@as_gate
class Eighth_Pi(SingleQubitGatePrototype):
    """ One-eighth pi gate

    ACTION

    Append a phase factor `exp(j*pi/4)` to `|1>` component.

    PARAMS (None)

    MATRIX

    Identical to Pauli X matrix
        `[[1 0], [0 exp(j*pi/4)]]`

    SYMBOL `T`
    """
    minimal_number_of_qubits = 1
    alias = 'EighthPi'
    symbol = 'T'
    parameters = {}

    def gate_matrix(self):
        phase_factor = np.exp(0.25 * 1.j * np.pi)
        return SquareMatrix(array=np.array([[1.0, 0.0], [0.0, phase_factor]]))


@as_gate
class Rotation_About_X(SingleQubitGatePrototype):
    """ Rotation about x-axis

    ACTION

    Rotation about x-axis in Bloch sphere for angle `theta`.
    Apply a phase rotation matrix `exp(- j*theta*X /2)` on the
    state vector, where `X` is the Pauli X matrix and `theta`
    the rotation angle.

    PARAMS

    `theta` (`float`): rotation angle; default is 0, then the
    matrix is an identity matrix

    MATRIX

    Diagonal entries are real, off-diagonal are imaginary
        `[[cos(theta/2) -j*sin(theta/2)], [-j*sin(theta/2) cos(theta/2)]]`

    SYMBOL `Rx`
    """
    minimal_number_of_qubits = 1
    alias = 'Rx'
    symbol = 'Rx'
    parameters = {
        'theta': GateParameter(paramtype=float, default=0.0)
    }

    def gate_matrix(self, theta):
        # cosine and sine of half angle
        cos_half_theta = np.cos(0.5*theta)
        sin_half_theta = np.sin(0.5*theta)
        return SquareMatrix(array=np.array([
            [cos_half_theta, 0.0 - 1.j * sin_half_theta],
            [0.0 - 1.j * sin_half_theta, cos_half_theta]]))


@as_gate
class Rotation_About_Y(SingleQubitGatePrototype):
    """ Rotation about y-axis

    ACTION

    Rotation about y-axis in Bloch sphere for angle `theta`.
    Apply a phase rotation matrix `exp(- j*theta*Y /2)` on the
    state vector, where `Y` is the Pauli Y matrix and `theta`
    the rotation angle.

    PARAMS

    `theta` (`float`): rotation angle; default is 0, then the
    matrix is an identity matrix

    MATRIX

    All entries are real
        `[[cos(theta/2) -sin(theta/2)], [sin(theta/2) cos(theta/2)]]`

    SYMBOL `Ry`
    """
    minimal_number_of_qubits = 1
    alias = 'Ry'
    symbol = 'Ry'
    parameters = {
        'theta': GateParameter(paramtype=float, default=0.0)
    }

    def gate_matrix(self, theta):
        # cosine and sine of half angle
        cos_half_theta = np.cos(0.5*theta)
        sin_half_theta = np.sin(0.5*theta)
        return SquareMatrix(array=np.array([
            [cos_half_theta, 0.0 - sin_half_theta],
            [sin_half_theta, cos_half_theta]]))


@as_gate
class Rotation_About_Z(SingleQubitGatePrototype):
    """ Rotation about z-axis

    ACTION

    Rotation about z-axis in Bloch sphere for angle `theta`.
    Apply a phase rotation matrix `exp(- j*theta*Z /2)` on the
    state vector, where `Z` is the Pauli Z matrix and `theta`
    the rotation angle.

    PARAMS

    `theta` (`float`): rotation angle; default is 0, then the
    matrix is an identity matrix

    MATRIX

    Off-diagonal entries are 0
        `[[exp(-j*theta/2) 0], [0 exp(j*theta/2)]]`

    SYMBOL `Rz`
    """
    minimal_number_of_qubits = 1
    alias = 'Rz'
    symbol = 'Rz'
    parameters = {
        'theta': GateParameter(paramtype=float, default=0.0)
    }

    def gate_matrix(self, theta):
        # phase factors
        pf1 = np.exp(0.0 - 1.j * 0.5 * theta)
        pf2 = np.exp(1.j * 0.5 * theta)
        return SquareMatrix(array=np.array([[pf1, 0.0], [0.0, pf2]]))


@as_gate
class Parameterised_Phase_Rotation(SingleQubitGatePrototype):
    """ Parameterised phase rotation gate

    ACTION

    Append a phase factor to state `|1>` of the state. See MATRIX for
    the exact phase factor.

    PARAMS

    `n` (required): an integer

    `m` (required): an integer

    MATRIX

    Generic operator matrix
        `[[1, 0], [0, exp(2.j*np.pi*n/(2**m))]]`

    SYMBOL `PhRot`
    """
    minimal_number_of_qubits = 1
    alias = 'PhaseRotation'
    symbol = 'PPR'
    parameters = {
        'n': GateParameter(paramtype=int, default=1),
        'm': GateParameter(paramtype=int, default=1)
    }

    def gate_matrix(self, n, m):
        phase_factor = np.exp(2.j * np.pi * n / (2**m))
        return SquareMatrix(array=np.array([[1, 0], [0, phase_factor]]))


@as_gate
class Inverse_Parameterised_Phase_Rotation(SingleQubitGatePrototype):
    """ Inverse parameterised phase rotation

    ACTION

    Append a phase factor to state `|1>` of the state. See MATRIX for
    the exact phase factor. Inverse operation of the `PhaseRotation`.

    PARAMS

    `n` (required): an integer

    `m` (required): an integer

    MATRIX

    Generic operator matrix
        `[[1, 0], [0, exp(-2.j*np.pi*n/(2**m))]]`
    differs from the matrix of `PhaseRotation` by a minus sign
    on the exponential.

    SYMBOL `InvPhRot`
    """
    minimal_number_of_qubits = 1
    alias = 'InversePhaseRotation'
    symbol = 'InvPPR'
    parameters = {
        'n': GateParameter(paramtype=int, default=1),
        'm': GateParameter(paramtype=int, default=1)
    }

    def gate_matrix(self, n, m):
        phase_factor = np.exp(-2.j * np.pi * n / (2**m))
        return SquareMatrix(array=np.array([[1, 0], [0, phase_factor]]))


gatelib = {}
""" Collection of qubit gates """


def registration():
    """ Register a hard-coded gate in library

    Only instances of decorator `as_gate` are considered as legitimate
    quantum gates and are thus registered.
    """
    for _ , obj in inspect.getmembers(sys.modules[__name__]):
        if isinstance(obj, as_gate):
            if isinstance(obj.alias, str):
                if not obj.alias in gatelib.keys():
                    gatelib[obj.alias] = obj
                else:
                    existing = gatelib[obj.alias].__name__
                    raise GateRegistrationError(message=
                        "Alias {} ".format(obj.alias) +\
                        "has been registered for gate {}.".format(existing),
                        location="gate.single.registration()")
