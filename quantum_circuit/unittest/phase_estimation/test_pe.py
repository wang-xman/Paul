#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test
    quantum_circuit.phase_estimation.py

Main test:
    Phase estimation circuit using newly designed quantum
    flow architecture.

Updated:
    04 September 2021
"""
import unittest
import numpy as np

from linear_space.algebra import matrix_product
from linear_space.matrix import SquareMatrix
from qubit import qubit_from_bitlist, ComputationalBasis
from gate.prototype import GatePrototype, SingleQubitGatePrototype
from gate.decorator import as_gate
from gate.parameter import GateParameter

from quantum_register import QubitRegister
from quantum_memory.qubit_memory import QubitMemory

from quantum_operation.measurement import \
    measurement_operation_from_instruction_dict as MOfID
from quantum_circuit.phase_estimation import phase_estimation


@as_gate
class one_bit_phase_oracle(GatePrototype):
    minimal_number_of_qubits = 1
    alias = 'phase_oracle'
    # exponent to calculate U^n
    parameters = {
        'n': GateParameter(paramtype=int, default=1)
    }

    def _default_matrix(self):
        """ When applies to [1/sqrt(2), 1/sqrt(2)] the eigenvalue is -1

        And -1 = exp(i pi).
        """
        # theta = 0 -> 00000
        #return SquareMatrix(array=np.array([[0, 1.0], [1.0, 0]]))
        # theta = pi/2 -> 10000
        #return SquareMatrix(array=np.array([[0, -1.0], [-1.0, 0]]))
        # theta = pi/4 -> 01000
        #return SquareMatrix(array=np.array([[0, 1.j], [1.j, 0]]))

        # theta = pi/8 -> 00100
        return SquareMatrix(array=np.array([
            [0, np.sqrt(2.0) / 2.0 + 1.j * np.sqrt(2.0) / 2.0],
            [np.sqrt(2.0) / 2.0 + 1.j * np.sqrt(2.0) / 2.0, 0]]))

        # theta = pi/2 + pi/4 -> 11000
        #return SquareMatrix(array=np.array([[0, -1.j], [-1.j, 0]]))

        # theta = pi/2 + pi/4 + pi/8 -> 11100
        #return SquareMatrix(array=np.array([
        #    [0, -1.j * (np.sqrt(2.0) / 2.0 + 1.j * np.sqrt(2.0) / 2.0)],
        #    [-1.j * (np.sqrt(2.0) / 2.0 + 1.j * np.sqrt(2.0) / 2.0), 0]]))

    def gate_matrix(self, n):
        """ Customise gate matrix """
        final_matrix = self._default_matrix()
        if n > 1:
            for _ in range(0, n-1):
                final_matrix = matrix_product(final_matrix,
                                              self._default_matrix())
        return final_matrix


class Test_Phase_Estimation_Single_Bit_Oracle(unittest.TestCase):
    def test_pass(self):
        # computational register
        # computational state has 5 bits initialised to 0
        compute_state = ComputationalBasis(bitstring='00000')
        compute_register = QubitRegister(state=compute_state, label='COMPUTER')
        # ancilla state
        ancilla_state = qubit_from_bitlist([(1.0, '0'), (1.0, '1')])
        ancilla_register = QubitRegister(state=ancilla_state, label='ANCILLA')
        memory = QubitMemory(register=[compute_register,ancilla_register])
        # main circuit
        pe_flow = phase_estimation(
            computer=compute_register,
            ancilla=ancilla_register,
            oracle=one_bit_phase_oracle)
        pe_flow.launch_on_memory(memory)
        # measurement
        measurement_operation = MOfID({
            'register': 'COMPUTER'
        })
        probs = memory.operation_socket(measurement_operation)
        # find the key corresponding to the largest value
        state_string = max(probs, key=(lambda key: probs[key]))
        print(state_string)
