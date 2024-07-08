#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.braket.py

TODO How to link bra to quantum state conjugate?

PATH

[app_root]/quantum_state/braket.py

INTRO

Dirac braket and related objects.

Dirac ket is a quantum state with a particular
string representation. Yet Dirac bra is a linear
function, or a dual vector, acting on the ket.

In vector representation, a bra is represented by
Hermitean-transposed complex conjugate - of a quantum
state vector. Mostly important, bra defined a set of
linear operators acting on a ket.

CLASSES

LOG

Updated on 25 September 2021 | Created on 01 March 2021
"""
from linear_space.algebra import hermitian_conjugate

from .quantum_state import QuantumState
from .validators import BraketValidator

_MODULE_LOCATION_ = 'quantum_state.braket'


class Braket:
    """ Braket Mixin class """
    @property
    def label(self):
        """ Braket : Returns a string `self._label` """
        return self._label

    def __repr__(self):
        """ Braket: """
        return self.string_representation()

    def __str__(self):
        """ Braket: """
        return self.string_representation()


class Bra(Braket):
    """ Dirac bra

    TODO How to link this to quantum state conjugate?

    Dirac bra is NOT a quantum state (vector) but
    a dual vector.

    It is designed as holder of quantum state and
    it behaves as a linear function that transforms
    a `Ket` instance.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.Bra'
    def __init__(self, label=None, state=None):
        """ Bra :: init """
        self._label = None
        validator = BraketValidator(label=label, state=state)
        if validator.is_valid:
            validated_data = validator.validated_data()
            self._label = validated_data['label']
            self._state = state
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    def as_vector(self):
        """ Bra :: Returns a row vector """
        return hermitian_conjugate(self._state.as_vector())

    def as_array(self):
        """ Bra :: Returns an array """
        return self.as_vector().as_array()

    def string_representation(self):
        """ Bra ::  Returns a string representation

        For example, "<First|", or "<000|.
        """
        string = "<" + self._label + "| = " +\
                self.as_vector().string_representation()
        return string


class Ket(Braket, QuantumState):
    """ Dirac ket

    Dirac ket is a quantum state, and is thus designed as
    a subclass of `QuantumState`. To instantiate a ket,
    a ket string and an instance of quantum state are
    required.

    CONSTRUCTOR

    `label` (`str`) : a string variable used to represent
    a quantum state

    `state` (obj) : an instance of `QuantumState` class;
    vector of this object is used to invoke the constructor
    of base class `QuantumState`.

    ATTRIBUTES

    `self._label` (`str`) : a string that represents the ket,
    for example, in representation `'|AB>'`, string `'AB'`
    is the label

    `self.label()` : returns `self._label` string

    `self.string_representation()`: returns a string in for
    example `'|ABS>'`, where `self._label` is sandwiched
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.Ket'

    def __init__(self, label=None, state=None):
        self._label = None
        validator = BraketValidator(label=label, state=state)
        if validator.is_valid:
            validated_data = validator.validated_data()
            self._label = validated_data['label']
            super().__init__(vector=state.as_vector())
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    def string_representation(self):
        """ Ket: Returns a string representation of the ket object

        For example, "|First>", or "|000>".
        """
        string = "|" + self._label + "> = " \
                + self.as_vector().string_representation()
        return string
