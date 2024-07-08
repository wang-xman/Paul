#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

qubit.validators.py

PATH

[app_root]/qubit/validators.py

INTRO

Validators for objects in states. Instantiate the validator
with data for validation. Invoke `is_valid` method before
acquiring validated data.

CONTENT

LOG

Updated on 02 October 2021 | Created on 23 June 2020
"""
from linear_space.vector import ColumnVector
from linear_space.number import is_power_of_two, exponent_of_two
from quantum_state.quantum_state import QuantumState

from .base import QubitBaseValidator
from .errors import QubitStateValidationError, SingleQubitBasisValidationError

_MODULE_LOCATION_ = 'qubit.validators'


class QubitStateValidator(QubitBaseValidator):
    """ Qubit state validator

    TODO Refactor this validator.

    Only checks a vector or a quantum state against the
    required vector size or dimension to be a qubit state:
    internal vector of a qubit state must be of size that
    is power of 2 and is thus of minimum length 2.
    """
    error_class = QubitStateValidationError
    error_location = _MODULE_LOCATION_ + '.QubitStateValidator'

    def __init__(self, vector=None, state=None):
        """ Qubit State Validator : init """
        super().__init__()
        self._validated_state = None
        self._number_of_qubits = None
        self._validated_vector = None
        self.validate(vector=vector, state=state)

    def validate(self, vector=None, state=None):
        if vector is None and state is None:
            self.report_errors("To create a qubit state, " +\
                    "either a vector or a quantum state must be provded.")
        elif not vector is None and not state is None:
            self.report_errors("To create a qubit state, " +\
                    "either a vector or a quantum state must be " +\
                    "provded. Not both.")
        elif vector is None:
            self.validate_state(state=state)
        else:
            self.validate_vector(vector=vector)

    def validate_state(self, state=None):
        """ Validate state """
        if isinstance(state, QuantumState):
            if is_power_of_two(state.dim):
                if exponent_of_two(state.dim) < 1:
                    self.report_errors("State used to " +\
                            "instantiate a qubit has less than " +\
                            "2 elements. State must have at least " +\
                            "2 elements, corresponding to at least 1 qubit.")
                else:
                    # this vector should be normalised
                    self._validated_vector = state.as_vector()
                    self._number_of_qubits = exponent_of_two(state.dim)
            else:
                self.report_errors("State vector length is "+\
                        "incompatible with qubit.")
        else:
            self.report_errors("State used to instantiate " +\
                    "a qubit state is not an instance of QuantumState class.")

    def validate_vector(self, vector=None):
        """ Qubit State Validator : Validate vector

        After validation, vector is to be interpreted as the
        internal vector of a quantum state. To qualify as a
        qubit state, following criteria must be met:
        (1) Length of this vector must be a power of 2;
        number of qubits is implied from this vector.
        (2) According to (1), the minimal length of this vector is 2.
        """
        if isinstance(vector, ColumnVector):
            if is_power_of_two(vector.size):
                if exponent_of_two(vector.size) < 1:
                    self.report_errors("Vector used to " +\
                            "instantiate a qubit has less than " +\
                            "2 elements. Vector must have at " +\
                            "least 2 elements, corresponding to at " +\
                            "least 1 qubit.")
                else:
                    self._validated_vector = vector
                    self._number_of_qubits = exponent_of_two(vector.size)
            else:
                self.report_errors("Vector length is "+\
                        "incompatible with qubit.")
        else:
            self.report_errors("Vector used to instantiate " +\
                    "a qubit state is not an instance of Vector class.")

    def validated_data(self):
        ret = None
        if self.is_valid:
            ret = {
                'vector': self._validated_vector,
                'number_of_qubits': self._number_of_qubits
            }
        return ret


class SingleQubitBasisValidator(QubitBaseValidator):
    error_class = SingleQubitBasisValidationError
    error_location = _MODULE_LOCATION_ + '.SingleQubitBasisValidator'

    def __init__(self, bitstring=None):
        super().__init__()
        self._validated_bitstring = None
        self.validate(string=bitstring)

    def validate(self, string=None):
        if string is None:
            self.report_errors("To instantiate a single qubit " +\
                    "basis state, please provide either '0' "   +\
                    "or '1' in string.")
        elif string == '0':
            self._validated_bitstring = '0'
        elif string == '1':
            self._validated_bitstring = '1'
        else:
            self.report_errors("To instantiate a single qubit " +\
                    "basis state, only '0' or '1' is acceptable.")

    def validated_data(self):
        ret = {
            'bitstring': self._validated_bitstring
        }
        return ret
