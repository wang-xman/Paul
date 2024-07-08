#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

density_matrix.density_matrix.py

PATH

[app_root]/density_matrix/density_matrix.py

INTRO

Density matrix and related objects.

Density matrix is a quintessential quantity to
quantum measurement and dynamics of an ensemble.

LOG

Updated on 13 October 2021 | Created on 23 February 2021
"""
from linear_space.matrix import SquareMatrix
from linear_space.algebra import scale, matrix_add
from qubit.algebra import qubit_outer

from .validators import DensityMatrixInitValidator, \
    QubitDensityMatrixInitValidator

_MODULE_LOCATION_ = 'density_matrix.density_matrix'


class DensityMatrix(SquareMatrix):
    """ Density matrix

    Generic formulation of density matrix.

    A density matrix can be constructed for pure state or
    mixed state.

    For a pure state, a quantum state vector must be provided.
    For a mixed state, an ensemble of states must be provided
    in the form of a list
        [(prob, pure state 1), (prob, pure state 2), ...]
    where each element in the list is a tuple.
    FIXME This is exactly a superlist!

    Density matrix is a subclass of a square matrix.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.DensityMatrix'

    def __init__(self, state=None, matrix=None):
        """ Density Matrix : init

        An internal array is created to represent the
        density matrix.
        """
        validator = DensityMatrixInitValidator(state=state, matrix=matrix)
        if validator.is_valid:
            vd = validator.validated_data()
            if 'state' in vd.keys():
                super().__init__(array=self._to_internal_array(vd['state']))
            else:
                super().__init__(array=vd['matrix'].as_array())
        else:
            validator.raise_last_error(
                    location=self._ERROR_LOCATION_+'.__init__')

    def _to_internal_array(self, state):
        """ Density Matrix :: Create internal array

        Internal array is created out of internal state.

        If internal state is a single state, not an ensemble,
        the density matrix is simply of the form
            `|state><state|`.

        If internal state is an ensemble, a list of tuples
        indicating a mixed state, the internal array is constructed
        using
            `p1 * |s1><s1| + p2 * |s2><s2| + ...`
        In this case, a pure state can not be formed.
        """
        internal_array = None
        # An ensemble is a list of probability-state tuples
        if isinstance(state, list):
            outer_matrix = \
                    scale(state[0][0], qubit_outer(state[0][1], state[0][1]))
            for i in range(1, len(state)):
                outer_matrix = matrix_add(
                    outer_matrix,
                    scale(state[i][0], qubit_outer(state[i][1], state[i][1])))
            internal_array = outer_matrix.as_array()
        # a single state
        else:
            outer_matrix = qubit_outer(state, state)
            internal_array = outer_matrix.as_array()
        return internal_array


class QubitDensityMatrix(DensityMatrix):
    """ Qubit density matrix

    A dedicated density matrix with a dimension that
    is compatible with the dimension of qubit state.
    Number of rows (and of course number of columns)
    must be power of 2.
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.QubitDensityMatrix'

    def __init__(self, state=None, matrix=None):
        validator = QubitDensityMatrixInitValidator(state=state, matrix=matrix)
        if validator.is_valid:
            super().__init__(state=state, matrix=matrix)
        else:
            validator.raise_last_error(
                    location=self._ERROR_LOCATION_+'.__init__')
