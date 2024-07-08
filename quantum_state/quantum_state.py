#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.quantum_state.py

PATH

[app_root]/quantum_state/quantum_state.py

INTRO

Quantum state object.

CONTENT

`QuantumState` - Generic quantum state

CONVENTION

A tuple usually contains elements that are used to product
a new object via multiplication; a list contains elements
that are used to compose a new object via addition.
Here, multiplication and addition are abstract operations
subjected to specific interpretation.

TERMINOLOGY

Terminology used in this package falls into two categories:
general concept and technical concept. General concept refers
to concepts and definitions that are commonly accepted in
quantum mechanics; technical concept is introduced to connect
different objects used in this package.

General concepts:

Quantum state -- A quantum state defined in general quantum
mechanics. Its behaviour is centred around the concept of
linear superposition and this means, in a properly defined
Hilbert space, a quantum state can be described as vector
in which each element represents an amplitude of the
corresponding unit vector.

Ket -- Dirac ket notation of a quantum state. It is a
representation of a quantum state, with algebraic
operations implemented.

Standard basis -- Also known as natural basis is a vector
that has only 1 nonzero element. For example, (0,1,0,0).

Unit vector -- A unit vector has length 1.

Computational basis -- Also known as "basis" of a qubit
system. As a specialised quantum state, it is defined for
a qubit system. It is basically a unit vector with constraints
on its length. Any multiqubit basis can be decomposed as a
tensor product of single qubit basis states |0> and |1>.
For example, |00> = |0> * |0>, where operator * is understood
as tensor product, i.e. Kronecker product.
A generic qubit state is a linear superposition of basis states.

Single-qubit basis -- A computational basis for a single qubit.
It is a two-component unit vector that represents either spin-up
|0> or spin-down state |1>.

Technical concepts:

Member: a member contains a component (basis) and its
associated amplitude. A standalone component doesn't have
physical meaning, and it can only be deemed as a component
(as its name suggests) of a state. This concept helps to
decompose any qubit state into a superposition, i.e. a list
of members.

Index location (`iloc`): an integer represents the location of
the only non-zero element in the basis vector.

Dimension: Number of elements in a (unit) vector

LOG

Updated on 30 September 2021 | Created on 20 June 2020
"""
from linear_space.number import is_one
from linear_space.algebra import norm, inner

from .base import AbstractQuantumState
from .errors import QuantumStateError
from .validators import QuantumStateVectorValidator

_MODULE_LOCATION_ = 'quantum_state.quantum_state'


class QuantumState(AbstractQuantumState):
    """ Quantum state

    Quantum state is modelled as a container object that
    packs an internal vector dressed by common properties
    a quantum state. These common properties are:

    [1] Any quantum state is represented by a unit vector
    in a Hilbert space; it is modelled by `UnitVector` and
    often referred to as state vector.

    [2] Any state vector can be decomposed into a superposition,
    a linear combination of other state vectors in the same
    Hilbert space. Addition of two quantum states shall produce
    another quantum state. This is often referred to as the
    superposition principle.

    [3] A state vector can thus be a linear superposition of
    a set of orthonormal state vectors, i.e. basis states,
    that span the Hilbert space.

    [4] In case [3], the coefficient in this linear combination
    is the amplitude (a complex number) of the corresponding
    basis state vector.

    [5] Two state vectors are considered equal as they only differ
    by a constant complex number. For quantum states, only the
    orientation of the vector matters.

    [6] Inner product of two states is the projection of one state
    to the other; also considered as the overlap between two states.
    Therefore, this is used to distinguish two states.

    Here, a state is represented by an internal vector `vector`.

    NOTE

    For a generic quantum state, ket notation is not necessary.
    Conversion method, such as `as_ket()`, is not implmented.

    CONSTRUCTOR

    `vector` (`Vector`): to instantiate a quantum state,
    an instance of class `Vector` is needed; a validated
    `UnitVector` instance is stored in `self._vector` as
    the internal vector.

    ATTRIBUTES

    `self._vector` (`Vector`): internal vector is a `UnitVector`
    instance; each entry in this vector is a complex number that
    represents the amplitude of the standard basis state of the
    respective Hilbert space

    `self.as_vector()`: returns internal vector, a `UnitVector`
    instance

    `self.vector`: property; alias to `as_vector()`

    `self.as_array()`: returns the internal array of the internal
    vector

    `self.size`: property; returns the number of elements in the
    internal vector

    `self.dimension()`: returns the size of `self._vector`;
    same as `self.size`

    `self.dim`: property; alias to `self.dimension()`

    `self.as_list()`: returns amplitudes in a `list`

    `self.amplitude_list`: property; alias to `as_list()`

    `self.__getitem__(, elindex)`: returns an element of the unit
    vector at given element index; returned value is a complex
    number that represents the amplitude of repsective standard basis

    `self.norm`: property; returns norm of internal vector

    `self.is_normalised`: property; return `True` (`False`) if
    vector is (not) normalised

    `self.is_normalized`: property; alias to `self.is_normalised`

    `self.normalise()`: normalise internal vector array
    `self._vector`; then, internal vector is normalised

    `self.normalize()`: alias to `self.normalise()`

    `self.is_equal_to(, other_state)`: if two states have the same
    internal vector, returns `True`, otherwise `False`;
    for `QuantumState` instance only

    `self.__eq__(, other_state)`: overload operator `==` for two
    quantum states; alias to `self.is_equal_to()`

    `self.string_representation()`: returns a string to represent
    the state vector `self._vector`

    `self.__repr__()`: invokes method `self.string_representation()`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.QuantumState'

    def __init__(self, vector=None):
        """ Quantum State :: init

        A `Vector` instance is required to construct a quantum state.

        Vector passed in is not required to be normalised, as the
        validator performs normalisation automatically.

        Arguments:

        `vector` (`Vector`): required; after validation and
        normalisation this vector is assigned to `self._vector`
        as the internal state vector
        """
        validator = QuantumStateVectorValidator(vector=vector)
        if validator.is_valid:
            self._vector = validator.validated_data()['vector']
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    def as_vector(self):
        """ Quantum State :: Return internal vector """
        return self._vector

    @property
    def vector(self):
        """ Quantum State :: Alias property to `as_vector()` """
        return self.as_vector()

    def as_array(self):
        """ Quantum State :: Return internal vector as array """
        return self.as_vector().as_array()

    @property
    def size(self):
        """ Quantum State :: size of state vector """
        return self.as_vector().size

    def dimension(self):
        """ Quantum State :: Number of elements in internal vector

        Returns number of elements of `self._vector`.
        """
        return self.as_vector().size

    @property
    def dim(self):
        """ Quantum State :: Alias to `dimension()` """
        return self.dimension()

    def as_list(self):
        """ Quantum State :: Return a list of amplitudes (complex numbers) """
        return self.as_vector().as_1d_list()

    @property
    def amplitude_list(self):
        """ Quantum State :: Alias property to `self.as_list()` """
        return self.as_list()

    def __getitem__(self, element_index):
        """ Quantum State :: Returns a component of internal vector

        The returned is in general a complex number.
        This number is the amplitude of the standard basis state.
        """
        try:
            ele = self.as_vector()[element_index]
            return ele
        except Exception as err:
            raise err.relocate(
                location=_MODULE_LOCATION_+'QuantumState.__getitem__')

    @property
    def norm(self):
        """ Quantum State :: Norm of state vector """
        try:
            return self.as_vector().norm
        except Exception as e:
            raise e

    @property
    def is_normalized(self):
        """ Quantum State :: Verify if state is normalised

        Returns `True` (`False`) if internal vector is (not)
        normalised.
        """
        return self.as_vector().is_normalized

    def normalize(self):
        """ Quantum State :: Normalise internal vector array """
        self.as_vector().normalize()
        return self

    def is_equal_to(self, other_state):
        """ Quantum State :: Check if two states are identical

        Criterion for identical states is that the norm of
        their inner product is unity, meaning the projection
        of one state onto the other is (almost) itself, or
        two states have a complete overlap.

        Must not compare two states with element-by-element
        approach as in common vectors, since what matters to
        a state is the direction of it.

        Returns `True`, if two states overlap completely;
        otherwise `False`.

        Arguments

        `other_state` (`QuantumState`) : a `QuantumState`
        instance
        """
        ret = False
        if isinstance(other_state, QuantumState):
            if self.size == other_state.size:
                innerprod = inner(self.as_vector(), other_state.as_vector())
                if is_one(norm(innerprod)):
                    ret = True
        else:
            raise QuantumStateError("Cannot compare a quantum " +\
                    "state to other type of objects.",
                    location=_MODULE_LOCATION_+'QuantumState.is_equal_to')
        return ret

    def __eq__(self, other_state):
        """ Quantum State :: Operator (==) for two quantum states

        Only applicable to quantum state instances
        """
        return self.is_equal_to(other_state)

    def string_representation(self):
        """ Quantum State :: String representation of state

        Returns internal vector array as a string with each
        amplitude formatted as a complex number. This method
        invokes the same method of the internal vector object.

        Customise representation string to, e.g.
        `"state_vector(0.89, 0.45)"`, in which the numbers are
        formated to have maximal two decimal points.
        """
        return "state_vector" + self.as_vector().string_representation()

    def __repr__(self):
        """ Quantum State :: String representation """
        return self.string_representation()

    def __str__(self):
        """ Quantum State :: __str__ """
        return self.string_representation()
