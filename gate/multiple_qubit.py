#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.multiple_qubit.py

PATH

[app_root]/gate/multiple_qubit.py

INTRO

Hardcoded multiple-qubit gates.

TODO More intro and content here.

CONTENT

LOG

Updated on 21 September 2021 | Created on 12 July 2020
"""
import numpy as np

from linear_space.matrix import SquareMatrix
from linear_space.algebra import matrix_product

from gate.parameter import QubitIndex, NumberOfQubits
from gate.decorator import as_gate
from gate.enlarge_matrix.controlled_kernel import kernel
from gate.prototype.base import GatePrototype


@as_gate
class controlled_NOT(GatePrototype):
    """ Controlled NOT gate

    Controlled-NOT (CNOT) gate operates on two qubits.
    Target state for CNOT has at least two qubits.
    """
    minimal_number_of_qubits = 2
    alias = 'CNOT'
    parameters = {
        'noq': NumberOfQubits(),
        'control': QubitIndex(),
        'target': QubitIndex()
    }

    def flip(self):
        return SquareMatrix(array=np.array([[0, 1], [1, 0]]))

    def gate_matrix(self, noq=None, control=None, target=None):
        """ Customise gate matrix """
        operator_matrix = kernel(
            number_of_qubits=noq,
            control_list=[(control, '1')],
            target_range=[target,target],
            original_matrix=self.flip())
        return operator_matrix


@as_gate
class SWAP(GatePrototype):
    """ Swap two qubits

    SWAP gate is implemented as three sequential CNOT gates.
    """
    minimal_number_of_qubits = 2
    alias = 'SWAP'
    parameters = {
        'noq': NumberOfQubits(),
        'alpha': QubitIndex(),
        'beta': QubitIndex()
    }

    def single_flip(self):
        return SquareMatrix(array=np.array([[0, 1], [1, 0]]))

    def gate_matrix(self, noq=None, alpha=None, beta=None):
        """ Customise gate matrix

        Generate a matrix product of three two-qubit CNOT matrices.
        """
        final_matrix = None
        try:
            # first CNOT
            matrix_of_first_CNOT = kernel(
                number_of_qubits=noq,
                control_list=[(alpha, '1')],
                target_range=[beta,beta],
                original_matrix=self.single_flip())
            # second CNOT
            matrix_of_second_CNOT = kernel(
                number_of_qubits=noq,
                control_list=[(beta,'1')],
                target_range=[alpha,alpha],
                original_matrix=self.single_flip())
            # TODO Use matrix maker utility
            final_matrix = matrix_product(
                matrix_of_first_CNOT,
                matrix_product(matrix_of_second_CNOT, matrix_of_first_CNOT))
        except Exception as err:
            raise err
        return final_matrix
