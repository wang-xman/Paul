#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

density_matrix.validators.py

PATH

[app_root]/density_matrix/validators.py

INTRO

Density matrix initialization validators.

LOG

Updated on 30 September 2021 | Created on 23 February 2021
"""
from linear_space.number import is_real, is_one, is_power_of_two
from linear_space.matrix import SquareMatrix
from quantum_state import QuantumState

from .base import DensityMatrixBaseValidator
from .errors import DensityMatrixValidationError

_MODULE_LOCATION_ = 'density_matrix.validators'


class StateInitValidator(DensityMatrixBaseValidator):
    """ Validate state for making density matrix """
    error_class = DensityMatrixValidationError
    error_location = _MODULE_LOCATION_ + '.DensityMatrixValdiator'

    def __init__(self, state=None):
        super().__init__()
        self._validated_state = None
        self.validate(state=state)

    def validate(self, state=None):
        if isinstance(state, QuantumState):
            self._validated_state = state
        elif isinstance(state, list):
            self.validate_ensemble(ensemble=state)
        else:
            self.report_errors("To create a density matrix, " +\
                    "a quantum state or an ensemble of "      +\
                    "quantum states is required.")

    def validate_ensemble(self, ensemble=None):
        if len(ensemble) <= 1:
            self.report_errors('Only one item in the ' +\
                    'ensemble list. In this case, '    +\
                    'density matrix shall be created ' +\
                    'directly by using the state.')
        else:
            self.validate_ensemble_multiple(ensemble=ensemble)

    def validate_ensemble_multiple(self, ensemble=None):
        """ Ensemble is a list of probability-state tuples

        FIXME It appears the ensemble list is a superlist!
        Why not just use the concept of superlist.
        """
        total_probability = 0
        validated_list = []
        for pairtup in ensemble:
            if not isinstance(pairtup, tuple):
                self.report_errors("In the ensemble list, " +\
                        "each element must be a tuple.")
            else:
                if len(pairtup) != 2:
                    self.report_errors("To create density matrix, "    +\
                            "each tuple in the ensemble must contain " +\
                            "two elements.")
                else:
                    if not is_real(pairtup[0]) or pairtup[0] < 0:
                        self.report_errors("To create density"   +\
                                "matrix, probability must be a " +\
                                "positive real number.")
                    elif not isinstance(pairtup[1], QuantumState):
                        self.report_errors('To create density matrix ' +\
                                'using an ensemble of states, the '    +\
                                'second element in the tuple must be a state.')
                    else:
                        if pairtup[1].dim != ensemble[0][1].dim:
                            self.report_errors(message='To create density ' +\
                                    'matrix, all states must have the same ' +\
                                    'dimension.')
                        else:
                            validated_list.append(pairtup)
        # all probabilities must sum up to unity
        if len(self.get_errors()) == 0:
            for item in validated_list:
                total_probability += item[0]
            # check if probability sum to unity
            if is_one(total_probability):
                self._validated_state = validated_list
            else:
                self.report_errors('To creat a density matrix, '  +\
                        'all probabilities in the ensemble must ' +\
                        'sum up to unity.')

    def validated_data(self):
        ret = None
        if self.is_valid:
            ret = {
                'state': self._validated_state
            }
        return ret


class MatrixInitValidator(DensityMatrixBaseValidator):
    """ Validate matrix for init

    TODO Need more validation.
    """
    error_class = DensityMatrixValidationError
    error_location = _MODULE_LOCATION_ + '.MatrixInitValdiator'

    def __init__(self, matrix=None):
        super().__init__()
        self._validated_matrix = None
        if not isinstance(matrix, SquareMatrix):
            self.report_errors("Matrix passed in to initialise " +\
                    "a density matrix is not a square matrix.")
        else:
            self._validated_matrix = matrix

    def validated_data(self):
        ret = None
        if self.is_valid:
            ret = {
                'matrix': self._validated_matrix
            }
        return ret


class DensityMatrixInitValidator(DensityMatrixBaseValidator):
    """ Validate init parameters for density matrix

    Validator used for instantiation of density matrix
    object. According to the input object, it diverts
    validation to different validator for state or matrix.
    """
    error_class = DensityMatrixValidationError
    error_location = _MODULE_LOCATION_ + '.DensityMatrixInitValdiator'

    def __init__(self, state=None, matrix=None):
        super().__init__()
        self._validated_item = None
        self.validate(state, matrix)

    def validate(self, state, matrix):
        """ Main validate method """
        if not state is None and matrix is None:
            validator = StateInitValidator(state=state)
        elif not matrix is None and state is None:
            validator = MatrixInitValidator(matrix=matrix)
        else:
            self.report_errors("To construct a density " +\
                    "matrix, use either a state or a "  +\
                    "valid square matrix. Not both.")
        if not validator.is_valid:
            self.report_errors(validator.get_errors())
        else:
            self._validated_item = validator.validated_data()

    def validated_data(self):
        return self._validated_item


class QubitDensityMatrixInitValidator(DensityMatrixInitValidator):
    """ Validate init paramters for qubit density matrix

    For qubit systems, the size of a state vector must be
    power of two; so is the number of rows/cols of the
    corresponding density matrix.
    """
    def __init__(self, state=None, matrix=None):
        super().__init__(state=state, matrix=matrix)
        if self.is_valid:
            self.validate_dimension(state, matrix)

    def validate_dimension(self, state, matrix):
        if state is not None and matrix is None:
            if not is_power_of_two(state.dim):
                self.report_errors("Dimension of the state " +\
                        "used to construct a qubit density " +\
                        "is incompatible with qubit system.")
        else:
            #elif matrix is not None and state is None:
            if not is_power_of_two(matrix.nrows):
                self.report_errors("Dimension of the matrix " +\
                        "used to construct a qubit density "  +\
                        "is incompatible with qubit system.")
