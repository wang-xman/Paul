#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    gate.decorator.py

Updated:
    26 July 2021
"""
import unittest
import numpy as np
from linear_space.vector import UnitVector
from linear_space.matrix import SquareMatrix
from qubit import QubitState

from gate.base import GateBaseError, GateBaseValidationError
from gate.parameter import InputQubitState
from gate.prototype.base import GatePrototype, SingleQubitGatePrototype
from gate.enlarge_matrix.errors import GateMatrixEnlargeValidationError
from gate.decorator.decorator import as_gate


class gate_pass_1(GatePrototype):
    """ Okay """
    minimal_number_of_qubits = 1
    alias = "Wookie"
    parameters = {}

    def gate_matrix(self):
        pass

class TestPass(unittest.TestCase):
    def test_pass_1(self):
        as_gate(gate_pass_1)


class gate_fail_1:
    """ Not a subclass of GatePrototype """
    minimal_number_of_qubits = 1
    alias = "Wookie"
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class TestGateDecorator_Fail_at_New(unittest.TestCase):
    def test_non_subclass(self):
        # Error: not a subclass of
        self.assertRaises(GateBaseValidationError, as_gate, gate_fail_1)


class gate_prototype_no_parameters(GatePrototype):
    """ No parameters """
    minimal_number_of_qubits = 1
    alias = "Wookie"
    #parameters = {'input_state': InputQubitState}

    def gate_matrix(self):
        pass

class gate_prototype_no_noq(GatePrototype):
    """ Non minimal noq """
    #minimal_number_of_qubits = 1
    alias = "Wookie"
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class gate_prototype_no_alias(GatePrototype):
    """ No alias """
    minimal_number_of_qubits = 1
    parameters = {'input_state': InputQubitState()}

    def gate_matrix(self):
        pass

class gate_prototype_no_gate_matrix(GatePrototype):
    """ No gate matrix """
    minimal_number_of_qubits = 1
    alias = "Wookie"
    parameters = {'input_state': InputQubitState()}

class gate_prototype_wrong_parameter_types(GatePrototype):
    """ Error: parameter value must be Parameter instance """
    minimal_number_of_qubits = 1
    alias = "Wookie"
    parameters = {'input_state': 1}

    def gate_apply(self):
        pass

class TestGateDecorator_Fail_at_Init(unittest.TestCase):
    def test_prototype_fail_no_parameters(self):
        # Error: no parameters
        #as_gate(gate_prototype_no_parameters)
        self.assertRaises(GateBaseValidationError, as_gate,
                          gate_prototype_no_parameters) 

    def test_prototype_fail_no_noq(self):
        # Error: no noq
        #as_gate(gate_prototype_no_noq)
        self.assertRaises(GateBaseValidationError, as_gate, gate_prototype_no_noq)

    def test_prototype_fail_no_alias(self):
        # Error: no alias
        #as_gate(gate_prototype_no_alias)
        self.assertRaises(GateBaseValidationError, as_gate, gate_prototype_no_alias)

    def test_prototype_fail_no_gate_matrix(self):
        # Error: no gate_matrix in the absence of gate_apply
        #as_gate(gate_prototype_no_gate_matrix)
        self.assertRaises(GateBaseValidationError, as_gate,
                          gate_prototype_no_gate_matrix)

    def test_prototype_wrong_parameter_types(self):
        # Error: parameter value must be parameter instance
        #as_gate(gate_prototype_wrong_parameter_types)
        self.assertRaises(GateBaseValidationError, as_gate,
                          gate_prototype_wrong_parameter_types)


""" Gate application and operation """
@as_gate
class sample_flip(SingleQubitGatePrototype):
    """ Without gate_apply and relies on decorator for generic operation """
    minimal_number_of_qubits = 1
    alias = "test_sample_flip"
    parameters = {}

    def gate_matrix(self):
        return SquareMatrix(array=np.array([[0, 1], [1, 0]]))

class TestSampleGateOperation_DefaultDirect(unittest.TestCase):
    def test_sample_pass(self):
        sample = sample_flip
        state = QubitState(vector=UnitVector(array=np.array([[0],[1]])))
        # Pass
        ns = sample(input_state=state)

    def test_sample_parameters_not_in_dict(self):
        sample = sample_flip
        state = QubitState(vector=UnitVector(array=np.array([[0],[1],[0],[1]])))
        # Error: parameters as positional arguments.
        #sample(state)
        self.assertRaises(Exception, sample, state)

    def test_sample_mismatched_noq(self):
        sample = sample_flip
        state = QubitState(vector=UnitVector(array=np.array([[0],[1],[0],[1]])))
        # Error: mismatched noq, gate operation error
        #sample(input_state=state)
        self.assertRaises(Exception, sample, **{'input_state': state})

class TestSampleGateOperation_DefaultResize(unittest.TestCase):
    def test_sample_gate_resize(self):
        sample = sample_flip
        state = QubitState(vector=UnitVector(array=np.array([[0],[1],[0],[1]])))
        # Pass
        ns = sample(input_state=state, target_index=1)
        #print(ns.as_vector().as_array())

    def test_sample_gate_resize_no_target_index(self):
        sample = sample_flip
        state = QubitState(vector=UnitVector(array=np.array([[0],[1],[0],[1]])))
        # Error: no target index
        #ns = sample(input_state=state)
        self.assertRaises(GateBaseError, sample, **{'input_state':state})

    def test_sample_gate_resize_invalid_target_index(self):
        sample = sample_flip
        state = QubitState(vector=UnitVector(array=np.array([[0],[1],[0],[1]])))
        # Error: index out of range
        #ns = sample(input_state=state, target_index=2)
        self.assertRaises(GateMatrixEnlargeValidationError, sample, 
                          **{'input_state':state, 'target_index':3})

    def test_sample_gate_no_input(self):
        sample = sample_flip
        state = QubitState(vector=UnitVector(array=np.array([[0],[1],[0],[1]])))
        # Error: input state is not provided
        #ns = sample(target_index=2)
        self.assertRaises(GateBaseError, sample, **{'target_index':3})

@as_gate
class sample_twobit_gate(GatePrototype):
    """ Sample two bit gate

    NOTE This gate is only for testing the mismatched number of qubits.
    """
    minimal_number_of_qubits = 2
    alias = "test_sample_flip"
    parameters = {}

    def gate_matrix(self):
        return SquareMatrix(array=np.array([[0, 1], [1, 0]]))

class TestSmallerQubitSize(unittest.TestCase):
    def test_twobit(self):
        sample = sample_twobit_gate
        state = QubitState(vector=UnitVector(array=np.array([[0], [1]])))
        # Error: too few number of qubits.
        #ns = sample(input_state=state)
        self.assertRaises(GateBaseError, sample, **{'input_state':state})
