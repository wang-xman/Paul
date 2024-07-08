#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    state.quantum_state.py

Updated:
    27 April 2021
"""
import unittest
import numpy as np
from linear_space.vector import ColumnVector, UnitVector
from quantum_state.quantum_state import QuantumState


class Test_QuantumState_VectorType(unittest.TestCase):
    """ Vector of a quantum state must be a unit vector

    Any vector, normalised or not, can be used to
    initialise a quantum state. But it will always
    be converted into a unit vector before it is
    stored as the internal vector of a quantum state.
    """
    def test_as_vector_method(self):
        # vector of a quantum state must be a unit vector
        test_vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        # if initial vector is not normalised, it won't be the same as
        # the vector of the quantum state.
        self.assertFalse(state.as_vector() == test_vector)
        # however, the vector of quantum state is the same as the normalised
        # initial test vector
        self.assertTrue(state.as_vector() == test_vector.normalize())

    def test_vector_type(self):
        # Pass
        test_vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        self.assertTrue(isinstance(state.as_vector(), UnitVector))

    def test_vector_from_a_quantum_state(self):
        test_vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        new_state = QuantumState(vector=state.as_vector())
        self.assertTrue(isinstance(state.as_vector(), UnitVector) and
                       isinstance(new_state.as_vector(), UnitVector))
        self.assertTrue(state.as_vector() == new_state.as_vector())


class Test_QuantumState_StateDimension(unittest.TestCase):

    def test_state_dimension(self):
        # Pass
        test_vector = ColumnVector(array=np.array([[1.0], [1.0], [1.0], [1.0]]))
        state = QuantumState(vector=test_vector)
        self.assertTrue(state.dim == test_vector.size)
        self.assertTrue(state.dimension() == 4)
