#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_state.validators.py

PATH

[app_root]/quantum_state/validators.py

INTRO

Quantum state validator is a generic validator
that validates the (state) vector provided to
the quantum state constructor.

Vector of a quantum state must be a unit vector.

CONTENT

`QuantumStateVectorValidator` - Validate vector passed
to instantiate a quantum state object

LOG

Updated on 30 September 2021 | Created on 23 June 2020
"""
from linear_space.vector import ColumnVector, UnitVector
from superposition.validators import SuperlistValidator

from .base import QuantumStateBaseValidator, AbstractQuantumState

from .errors import QuantumStateVectorValidationError, \
    QuantumSuperlistValdiationError, BraketValidationError

_MODULE_LOCATION_ = 'quantum_state.validators'


class QuantumStateVectorValidator(QuantumStateBaseValidator):
    """ Quantum state vector validator

    Validate passed-in internal vector that is used to
    instantiate a qauntum state. Passed-in vector must
    be an instance of Vector class. Vector of a quantum
    state must be a unit vector, or normalised vector.

    If the passed-in vector is an instance of `Vector`,
    but not an instance of `UnitVector`, convert it into
    a `UnitVector` instance. In summary, the internal
    vector of a quantum state must be a unit vector.

    VALIDATED DATA

    A dictionary with one key
        {
            'vector': self._validated_data
        }
    """
    error_class = QuantumStateVectorValidationError
    error_location = _MODULE_LOCATION_ + '.QuantumStateVectorValidator'

    def __init__(self, vector=None):
        super().__init__()
        self._validated_vector = None
        self.validate(vector=vector)

    def validate(self, vector=None):
        """ Quantum State Vector Validator :: main """
        if vector is None:
            self.report_errors("To create a quantum state, " +\
                    "please provide a vector instance to "   +\
                    "represent a state.")
        else:
            if not isinstance(vector, ColumnVector):
                self.report_errors("To create a quantum state, " +\
                        "vector must be an instance of " +\
                        "ColumnVector class.")
            else:
                if vector.size < 2:
                    self.report_errors("To create a legitimate " +\
                            "state, the size of column vector "  +\
                            "must be at least 2.")

        if len(self.get_errors()) == 0:
            # Make a unit vector
            if not isinstance(vector, UnitVector):
                self._validated_vector = UnitVector(array=vector.as_array())
            else:
                self._validated_vector = vector

    def validated_data(self):
        """ Quantum State Vector Validator :: validated data """
        ret = {
            'vector': self._validated_vector
        }
        return ret


class QuantumSuperlistValidator(SuperlistValidator):
    """ Quantum superlist validator """
    error_class = QuantumSuperlistValdiationError
    error_location = _MODULE_LOCATION_ + '.QuantumSuperlistValidator'

    def __init__(self, superlist=None, component_type=None):
        super().__init__(superlist=superlist)
        if self.is_valid:
            self.validate_component_type(superlist,
                    component_type=component_type)
            if self.is_valid:
                self.validate_state_dimension(superlist)

    def validate_component_type(self, superlist, component_type=None):
        for member in superlist:
            # if component type is None, components must
            # have the same type
            if component_type is None:
                if not type(member[1]) is type(superlist[0][1]):
                    self.report_errors("Components in the " +\
                            "superlist do not have the same type.")
            # object type is given
            else:
                if not isinstance(member[1], component_type):
                    self.report_errors("Components in "  +\
                            "the superlist do not have " +\
                            "the given object type.")

    def validate_state_dimension(self, superlist):
        """ All state must have the same dimension """
        dim_first_component = superlist[0][1].dim
        for member in superlist:
            if member[1].dim != dim_first_component:
                self.report_errors("Componnet states in superlist " +\
                        "have different dimensions.")


class BraketValidator(QuantumStateBaseValidator):
    """ Validator for braket

    VALIDATED DATA:

    A dictionary that has one entry
        {
            'label':
        }
    """
    error_class = BraketValidationError
    error_location = _MODULE_LOCATION_ + '.BraketValidator'

    def __init__(self, label=None, state=None):
        super().__init__()
        self._validated_label = None
        self.validate(label=label, state=state)

    def validate(self, label=None, state=None):
        self._validate_label(label=label)
        self._validate_state(state=state)

    def _validate_label(self, label=None):
        if label is None:
            self.report_errors("Braket label is missing.")
        else:
            if not isinstance(label, str):
                self.report_errors("Braket label is not a string.")
            elif len(label) == 0:
                self.report_errors("Braket label is empty.")
            elif label.isspace():
                self.report_errors("Braket label contains only space.")
            elif label[0].isspace():
                self.report_errors("Braket label begins with space.")
            else:
                self._validated_label = label

    def _validate_state(self, state=None):
        if state is None:
            self.report_errors("To create a ket or bra, " +\
                    "a quantum state is required.")
        elif not isinstance(state, AbstractQuantumState):
            self.report_errors("Quantum state is not an " +\
                    "instance of class QuantumState.")

    def validated_data(self):
        ret = {
            'label': self._validated_label
        }
        return ret
