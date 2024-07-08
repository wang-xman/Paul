#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.superposition.py

TODO String repr of superposition.

PATH

[app_root]/quantum_state/superposition.py

INTRO

Quantum superposition is a dedicated superposition
object for quantum state.

CONTENT

`QuantumSuperlistValidator` - Validator for superlist
used to instantiate quantum superposition

`QuantumSuperposition` - Superposition of quantum states

LOG

Updated on 30 September 2021 | Created on 20 June 2020
"""
from linear_space.number import is_zero
from linear_space.algebra import scale, matrix_add

from superposition.superposition import Superposition

from .validators import QuantumSuperlistValidator
from .null_state import NULL_STATE
from .quantum_state import QuantumState

_MODULE_LOCATION_ = 'quantum_state.superposition'


class QuantumSuperposition(Superposition):
    """ Quantum superposition

    As a dedicated superposition for quantum state,
    quantum superposition implements a `as_state` method
    to merge all components in the superlist and returns
    a quantum state.

    However, there is a catch. If the list contains only
    one tuple, the returned state shall be the state in
    the tuple.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.QuantumSuperposition'
    component_type = QuantumState

    def __init__(self, superlist=None):
        """ Quantum Superposition :: init """
        validator = QuantumSuperlistValidator(superlist=superlist,
                component_type=self.component_type)
        if validator.is_valid:
            super().__init__(superlist=superlist)
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    def as_state(self):
        """ Quantum Superposition :: convert to a state """
        state = None
        superlist = self.as_superlist()
        if len(superlist) == 1:
            state = superlist[0][1]
        else:
            new_vector = scale(superlist[0][0], superlist[0][1].as_vector())
            for i in range(1, len(superlist)):
                new_vector = matrix_add(new_vector,
                        scale(superlist[i][0], superlist[i][1].as_vector()))
            # take care of zero state
            if is_zero(new_vector.norm):
                state = NULL_STATE
            else:
                state = self.component_type(vector=new_vector)
        return state

    def as_vector(self):
        """ Quantum Superposition :: convert to a vector """
        return self.as_state().as_vector()

    def __str__(self):
        """ FIXME Make it prettier """
        return str(self.as_superlist())
