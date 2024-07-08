#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.enlarge_matrix.common.py

PATH

[package_root]/gate/enlarge_matrix/common.py

INTRO

Common routines and matrix makers used in operator matrix
enlargement processes.

CONTENT

`GenericGateMatrixEnlargeValidator` - Most common validator
for parameters passed to matrix enlargement functions

LOG

Updated on 30 September 2021 | Created on 10 September 2021
"""
from linear_space.number import is_integer, power_of_two
from linear_space.matrix import SquareMatrix, STATE_ZERO_PROJECTION, \
    STATE_ONE_PROJECTION

from gate.base import GateBaseValidator
from .errors import GateMatrixEnlargeValidationError

_MODULE_LOCATION_ = 'gate.enlarge_matrix.common'


# TODO Create a dictionary to map these matrices to
# strings. For example, 'prj0' may represent |0><0|
# and 'proj1' for |1><1|. This helps to strinigify
# the entire process.

up_state_projection_matrix = STATE_ZERO_PROJECTION
proj0 = STATE_ZERO_PROJECTION
""" Aliases """


down_state_projection_matrix = STATE_ONE_PROJECTION
proj1 = STATE_ONE_PROJECTION
""" Aliases """

MATRIX_REPERTOIRE = {
    'proj0': proj0,
    'proj1': proj1
}


# FIXME Refactor it into more validators
class GenericGateMatrixEnlargeValidator(GateBaseValidator):
    """ Validator for generic MCMQ operator matrix

    Validate parameters against two main rules.

    [1] Control list must not overlap with target range.

    [2] Dimension of original matrix must be compatible
    with number of qubits in target range.

    CONSTRUCTOR

    `number_of_qubits` (`int`) : total number of qubits of
    the input state

    `control_list` (`list`) : a list of control tuples; each
    tuple contains 2 elements, such as (3, '0'), where the
    first element must be qubit index, the second is the control
    state, either '0' or '1'

    `target_range` (`list`) : a list of 2 integers defining
    qubits the original matrix is applying to; for example
    `[3,5]` means qubits 3, 4, and 5 are targeted

    `original_matrix` (`SquareMatrix`) : original gate matrix
    to be enlarged or expanded into controlled operator
    """
    error_class = GateMatrixEnlargeValidationError
    error_location = _MODULE_LOCATION_ + '.GenericGateMatrixEnlargeValidator'

    def __init__(self, number_of_qubits=None, control_list=None,
                 target_range=None, original_matrix=None):
        """ Generic validator

        Number of qubits (noq) and original gate matrix (om) are
        validated and stored before validation of other
        parameters.
        """
        super().__init__()
        # validated noq and original matrix (om)
        self._noq = None
        self._om = None
        # validate noq and matrix
        self.validate_noq(number_of_qubits)
        if self.is_valid:
            self.validate_original_matrix(original_matrix)
        # overall validation
        if self.is_valid:
            self.validate(control_list=control_list, target_range=target_range)

    def validate_noq(self, noq):
        """ Validate number of qubits

        Number of qubits must be an integer. Private member
        `self._noq` stores pre-validated number of qubits.
        """
        if not is_integer(noq):
            self.report_errors("Number of qubits is not an integer.")
        elif noq < 1:
            self.report_errors("Number of qubits is less than 1.")
        else:
            self._noq = noq

    def validate_original_matrix(self, original_matrix):
        """ Validate original matrix

        Two rules:

        [1] Original matrix must be an instance of `SquareMatrix`.

        [2] Total number of qubits cannot be less than what
        the original matrix requires.

        Private member `self._om` stores pre-validated
        original gate matrix.
        """
        if not isinstance(original_matrix, SquareMatrix):
            self.report_errors("Original gate " +\
                    "matrix is not a square matrix.")
        elif power_of_two(self._noq) < original_matrix.nrows:
            self.report_errors("Total number of qubits " +\
                    "too small even for the original gate matrix.")
        else:
            self._om = original_matrix

    def validate_target_range(self, target_range):
        """ Validate target range

        Rules

        [1] Target range must be a list of two integers.
        Two integers can be identical, which reduces to target index.

        [2] Target range must be within the number of qubits
        (of the global state).

        [3] First element must not be greater than the second one.

        [4] Original matrix must be compatible with number of
        qubits within the target range. Here, compatible means
        directly applicable to.
        """
        if isinstance(target_range, list) and len(target_range) == 2 \
                and is_integer(target_range[0]) and is_integer(target_range[1]):
            # target range must be in range of global state
            if target_range[0] not in range(0, self._noq) \
                    or target_range[1] not in range(0, self._noq):
                self.report_errors("Target range is out of range.")
            # must be in normal order
            if target_range[0] > target_range[1]:
                self.report_errors("Target range is not in " +\
                        "normal order: First element is greater than " +\
                        "the second one.")
            else:
                # original matrix is compatible with bits in range
                if self._om.nrows != power_of_two(
                        target_range[1] - target_range[0] + 1):
                    self.report_errors("Number of qubits in the " +\
                            "target range is incompatible with the " +\
                            "dimension of the original gate matrix.")
        else:
            self.report_errors("Target range is not a list " +\
                    "of two integers")

    def validate_control_list_item(self, item, target_range):
        """ Validate individual item in a control list

        Each individual element is called control tuple.

        Rules:

        [1] Each item must be a tuple of two elements.

        [2] First element must be an integer.

        [3] Second element must be either '0' or '1'.

        [4] Control indices must within range of global
        state.

        [5] Control and target indices must no overlap.
        """
        if not isinstance(item, tuple):
            self.report_errors("Control list " +\
                    "contains non-tuple element.")
        elif len(item) != 2:
            self.report_errors("Control tuple in control " +\
                    "list doesn't contain exactly two elements.")
        else:
            if not is_integer(item[0]):
                self.report_errors("First element of a control "+\
                        "tuple is not an integer.")
            else:
                if item[0] > (self._noq - 1) or item[0] < 0:
                    self.report_errors("Control index " +\
                            "{} is out of range.".format(item[0]))
                # cannot overlap with target
                if item[0] in target_range:
                    self.report_errors("Control index " +\
                            "{} is also a target.".format(item[0]))
            if item[1] not in ['0', '1']:
                self.report_errors("Control state of a " +\
                        "control bit {} is ".format(item[0]) +\
                        "neither '0' nor '1'.")

    def validate_control_list(self, target_range=None, control_list=None):
        """ Validate control list

        Individually validate control tuple. Control list must
        not contain duplicate indices.
        """
        if not isinstance(control_list, list):
            self.report_errors("Control indices and their " +\
                    "conditional states are not provided as a list.")
        else:
            for item in control_list:
                self.validate_control_list_item(item, target_range)
        # control index must not duplicate
        if self.is_valid:
            control_indices = list(zip(*control_list))[0]
            if len(set(control_indices)) != len(control_indices):
                self.report_errors("Duplicated control indices.")

    def validate(self, control_list=None, target_range=None):
        """ Main validation method """
        self.validate_target_range(target_range)
        # if has control
        if self.is_valid:
            if control_list is not None:
                # check if target range covers all
                if (target_range[1] - target_range[0] + 1) == self._noq:
                    self.report_errors("Number of qubits in " +\
                            "target range is equal to the given " +\
                            "number of qubits. No space for control bits.")
                else:
                    self.validate_control_list(target_range=target_range,
                                               control_list=control_list)
