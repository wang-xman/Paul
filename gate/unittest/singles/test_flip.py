#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
Gate under test:
    Qubit flip

File under test:
    gate.single.py

Updated:
    29 April 2021
"""
import unittest
import numpy as np

from linear_space.vector import UnitVector
from quantum_state import QuantumState, NULL_STATE, NullState
from qubit import QubitState, SingleQubitBasis, ComputationalBasis
from gate.base import GateBaseError
from gate.enlarge_matrix.errors import GateMatrixEnlargeValidationError
from gate import single_qubit_gates as singles


class TestFlipGate_SingleBitOperation(unittest.TestCase):

    gate = singles['Flip']

    def test_flip_single_basis(self):
        up = SingleQubitBasis(bitstring='0')
        down = SingleQubitBasis(bitstring='1')
        # apply flip gate
        new_state = self.gate(input_state=up)
        self.assertTrue(new_state == down)

    def test_flip_generic_qubit(self):
        down = QubitState(vector=UnitVector(array=np.array([[0], [1]])))
        up = QubitState(vector=UnitVector(array=np.array([[1], [0]])))
        new_state = self.gate(input_state=down)
        self.assertTrue(new_state == up)
        self.assertTrue(new_state.is_up)

    def test_mismatched_noq(self):
        test_state = QubitState(
            vector=UnitVector(array=np.array([[0],[0],[0],[1]])))
        #new_state = self.gate(input_state=test_state)
        self.assertRaises(GateBaseError, self.gate,
                          **{'input_state':test_state})

    def test_input_wrong_type(self):
        test_state = QuantumState(
            vector=UnitVector(array=np.array([[0],[0],[1]])))
        #new_state = self.gate(input_state=test_state)
        self.assertRaises(GateBaseError, self.gate,
                          **{'input_state':test_state})

    def test_flip_with_unused_parameter(self):
        down = QubitState(vector=UnitVector(array=np.array([[0],[1]])))
        up = QubitState(vector=UnitVector(array=np.array([[1],[0]])))
        # Here, target index doesn't do anything.
        new_state = self.gate(input_state=down, target_index=1)
        self.assertTrue(new_state == up)
        self.assertTrue(new_state.is_up)

    def test_flip_with_undelcared_argument(self):
        down = QubitState(vector=UnitVector(array=np.array([[0],[1]])))
        up = QubitState(vector=UnitVector(array=np.array([[1],[0]])))
        # Error: undeclared arguments
        #new_state = self.gate(input_state=down, hello_index=1)
        self.assertRaises(GateBaseError, self.gate,
                          **{'input_state':down, 'hello_index':1})

    def test_with_zero_state(self):
        state = NullState()
        self.assertTrue(self.gate(input_state=state) == NULL_STATE)


class TestFlipGate_MultiBitOperation(unittest.TestCase):
    gate = singles['Flip']

    def test_pass_0(self):
        test_state = QubitState(
            vector=UnitVector(array=np.array([[1],[0],[0],[0]])))
        new_state = self.gate(input_state=test_state, target_index=1)
        exp_state = QubitState(
            vector=UnitVector(array=np.array([[0],[1],[0],[0]])))
        self.assertTrue(exp_state == new_state)

    def test_pass_1(self):
        test_state = QubitState(
            vector=UnitVector(array=np.array([[0],[0],[0],[1]])))
        new_state = self.gate(input_state=test_state, target_index=1)
        exp_state = QubitState(
            vector=UnitVector(array=np.array([[0],[0],[1],[0]])))
        self.assertTrue(exp_state == new_state)

    def test_pass_3bits_0(self):
        # |000>
        test_state = QubitState(vector=UnitVector(
            array=np.array([[1],[0],[0],[0],[0],[0],[0],[0]])
        ))
        new_state = self.gate(input_state=test_state, target_index=0)
        # |100>
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[0],[0],[0],[0],[1],[0],[0],[0]])))
        self.assertTrue(exp_state == new_state)

    def test_pass_3bits_1(self):
        # |000>
        test_state = QubitState(vector=UnitVector(
            array=np.array([[1], [0], [0], [0], [0], [0], [0], [0]])
        ))
        new_state = self.gate(input_state=test_state, target_index=1)
        # |010>
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[0], [0], [1], [0], [0], [0], [0], [0]])
        ))
        self.assertTrue(exp_state == new_state)

    def test_pass_3bits_2(self):
        # |010>
        test_state = QubitState(vector=UnitVector(
            array=np.array([[0], [0], [1], [0], [0], [0], [0], [0]])
        ))
        new_state = self.gate(input_state=test_state, target_index=2)
        # |011>
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[0], [0], [0], [1], [0], [0], [0], [0]])
        ))
        self.assertTrue(exp_state == new_state)

    def test_pass_3bits_out_of_range(self):
        # |010>
        test_state = QubitState(vector=UnitVector(
            array=np.array([[0], [0], [1], [0], [0], [0], [0], [0]])
        ))
        self.assertRaises(GateMatrixEnlargeValidationError, self.gate,
                          **{'input_state':test_state, 'target_index':3})


class TestFlip_withBasis(unittest.TestCase):
    gate = singles['Flip']

    def test_with_basis_3bits(self):
        # |010>
        test_state = ComputationalBasis(bitstring='010')
        new_state = self.gate(input_state=test_state, target_index=2)
        # |011>
        exp_state = ComputationalBasis(bitstring='011')
        self.assertTrue(exp_state == new_state)

    def test_with_basis_8bits(self):
        # |01001101>
        test_state = ComputationalBasis(bitstring='01001101')
        new_state = self.gate(input_state=test_state, target_index=3)
        # |01011101>
        exp_state = ComputationalBasis(bitstring='01011101')
        self.assertTrue(exp_state == new_state)


class TestFlip_withGenericQubitState(unittest.TestCase):
    gate = singles['Flip']

    def test_with_generic_qubit(self):
        # |01> + |11>
        test_state = QubitState(vector=UnitVector(
            array=np.array([[0], [1], [0], [1]])
        ))
        # still |01> + |11>
        new_state = self.gate(input_state=test_state, target_index=0)
        self.assertTrue(new_state == test_state)

    def test_with_generic_qubit_2(self):
        # |01> + |11>
        test_state = QubitState(vector=UnitVector(
            array=np.array([[0], [1], [0], [1]])
        ))
        new_state = self.gate(input_state=test_state, target_index=1)
        # |00> + |10>
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[1], [0], [1], [0]])
        ))
        self.assertTrue(new_state == exp_state)

    def test_with_generic_qubit_3(self):
        # |00> + |01> + |11>
        test_state = QubitState(vector=UnitVector(
            array=np.array([[1], [1], [0], [1]])
        ))
        new_state = self.gate(input_state=test_state, target_index=1)
        # |00> + |01> + |10>
        exp_state = QubitState(vector=UnitVector(
            array=np.array([[1], [1], [1], [0]])
        ))
        self.assertTrue(new_state == exp_state)
