#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operator.quantum_operators.py

PATH

[app_root]/quantum_operator/quantum_operators.py

NOTE

[IMPORTANT] Don't name any file as 'operator.py' due to
clash with Python's internal module of the same name.
To avoid such clashes and ambiguity, quantum operator
is used.

INTRO

Generic quantum operator and related classes.
Strictly speaking, quantum gates are quantum operators
acting on qubits. A generic quantum operator defined
here is qubit-agnostic, meaning that it is in principle
applicable to a quantum state of any number of qubits.

Therefore, quantum gates are natural subclasses of quantum
operator, but with more restrictions on for example the
number of qubits the gate is applicable.

CONTENT

`QuantumOperator` - Generic quantum operator

`QubitOperator` - Operator for qubit states

LOG

Updated on 29 September 2021 | Created on 08 March 2021
"""
from linear_space.matrix import  SquareMatrix
from linear_space.algebra import matrix_product

from quantum_state import QuantumState, NullState, NULL_STATE
from qubit import QubitState

from .errors import QuantumOperatorError

_MODULE_LOCATION_ = 'quantum_operator.quantum_operators'


class QuantumOperator:
    """ Quantum operator class

    A quantum operator is a matrix that acts on a state
    vector and produces a new state.

    Class attribute `state_class` defines the default
    type of state the operator acts on. By default,
    it is set to generic `QuantumState`.

    ATTRIBUTES

    `cls.state_class`: class attribute that declares the
    default state class compatible with the operator;
    the default is `QuantumState`

    `self.as_matrix()`: returns the internal matrix

    `self.has_matrix()`: verify if an operator has an
    internal matrix; returns `True` or `False`

    `self.update_matrix(, matrix)`: update the internal
    matrix of the operator

    `self.does_state_match(, state)`: verify if the state
    dimension matches the operator

    `self.apply(, state)`: default operator apply method
    that applies to operator to a state conforming to the
    declaration `cls.state_class`

    CONSTRUCTOR

    `matrix`: internal matrix of operator; must be an
    instance of class `SquareMatrix`; default to `None`
    """
    state_class = QuantumState

    def __init__(self, matrix=None):
        """ Quantum Operator :: Constructor """
        if isinstance(matrix, SquareMatrix):
            self._matrix = matrix
        else:
            self._matrix = None

    def as_matrix(self):
        """ Quantum Operator :: Returns internal matrix """
        return self._matrix

    def has_matrix(self):
        """ Quantum Operator :: Verify if internal matrix exists """
        ret = False
        if isinstance(self._matrix, SquareMatrix):
            ret = True
        return ret

    def update_matrix(self, matrix):
        """ Quantum Operator :: Update internal matrix """
        if isinstance(matrix, SquareMatrix):
            self._matrix = matrix
        else:
            raise QuantumOperatorError("Quantum operator " +\
                    "can only be a square matrix.",
                    location=_MODULE_LOCATION_+\
                        '.QuantumOperator.update_matrix')

    def does_state_match(self, state):
        """ Quantum Operator :: Verify state dimension

        Number of columns of the matrix must equal to
        the number of elements in the state vector.
        """
        ret = False
        if self._matrix.ncols == state.dim:
            ret = True
        return ret

    def apply(self, state):
        """ Quantum Operator :: default apply method

        If the state type is a subclass of the default
        `QuantumState`, the returned state is still an
        instance of `QuantumState`.

        To ensure the returned state is of proper type,
        subclass of the quantum operator must override
        this `apply` method.
        """
        new_state = None
        if self.has_matrix():
            if isinstance(state, self.state_class):
                if self.does_state_match(state):
                    try:
                        new_vector = matrix_product(self.as_matrix(),
                                                    state.as_vector())
                        # NOTE If state is a subclass of quantum state,
                        # the returned state would still be an instance of
                        # QuantumState
                        new_state = self.state_class(vector=new_vector)
                    except Exception as err:
                        raise QuantumOperatorError(
                            str(err.relocate(_MODULE_LOCATION_+\
                                    'QuantumOperator.apply'))) from err
                else:
                    raise QuantumOperatorError("Dimension of the " +\
                            "state doesn't match the quantum operator.",
                            location='QuantumOperator.apply()')
            # takes care of zero state
            elif isinstance(state, NullState):
                new_state = NULL_STATE
            else:
                raise QuantumOperatorError("Quantum operator is " +\
                        "applied to a wrong type.")
        else:
            raise QuantumOperatorError("Quantum operator has " +\
                    "no matrix to apply to a state.")
        return new_state


class QubitOperator(QuantumOperator):
    """ Qubit operator class

    Qubit operator is a quantum operator that acts on qubit.
    State class of qubit operator is thus `QubitState`.
    """
    state_class = QubitState
