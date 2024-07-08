#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    qubit.validator.py

Main test:
    Qubit state validator

Updated:
    28 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import ColumnVector
from quantum_state.quantum_state import QuantumState
from quantum_state.null_state import NULL_STATE

from qubit.validators import QubitStateValidator, QubitStateValidationError

def error_raiser(validator):
    validator.raise_last_error()


class TestQubitStateValidator_Init(unittest.TestCase):
    def test_sucess_with_vector(self):
        array = np.array([[1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(vector=vector)
        # validated data
        vd = validator.validated_data()
        vdvector = vd['vector']
        noq = vd['number_of_qubits']
        # validated vector might not be normalised
        self.assertTrue(vdvector == vector)
        self.assertTrue(noq==1)

    def test_sucess_with_state(self):
        array = np.array([[1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(state=state)
        # validated data
        vd = validator.validated_data()
        vdvector = vd['vector']
        noq = vd['number_of_qubits']
        # validated vector is normalised
        self.assertTrue(vdvector == state.as_vector())
        self.assertTrue(noq==1)


class TestQubitStateValidator_InitFail(unittest.TestCase):
    def test_without_either(self):
        array = np.array([[1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator()
        # Error: neither vector or state is provided.
        self.assertRaises(QubitStateValidationError, error_raiser, validator)

    def test_with_both(self):
        array = np.array([[1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(vector=vector, state=state)
        # Error: both vector and state are provided.
        self.assertRaises(QubitStateValidationError, error_raiser, validator)

    def test_wrong_vector_type(self):
        array = np.array([[1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(vector=array)
        # Error: vector is in wrong type.
        self.assertRaises(QubitStateValidationError, error_raiser, validator)

    def test_wrong_state_type(self):
        array = np.array([[1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(state=vector)
        # Error: vector is in wrong type.
        self.assertRaises(QubitStateValidationError, error_raiser, validator)


class TestQubitStateValidator_VectorSize(unittest.TestCase):
    def test_vector_too_short(self):
        # NOTE This error is triggered by Vector, not this validator.
        array = np.array([[1.0]])
        # Error: 
        try:
            vector = ColumnVector(array=array)
            state = QuantumState(vector=vector)
            #validator = QubitStateValidator(vector=vector)
            # Error: vector too short
            self.assertRaises(QubitStateValidationError, QubitStateValidator,
                          vector, None)
        except Exception as err:
            self.assertRaises(type(err))

    def test_vector_wrong_size(self):
        array = np.array([[1.0], [1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(vector=vector)
        # Error: incompatible size
        self.assertRaises(QubitStateValidationError, error_raiser, validator)


class Test_QubitStateValidator_StateDimension(unittest.TestCase):
    def test_state_wrong_dimension(self):
        array = np.array([[1.0], [1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        # Error: incompatible state vector size
        validator = QubitStateValidator(state=state)
        self.assertRaises(QubitStateValidationError, error_raiser, validator)

    def test_state_wrong_type(self):
        array = np.array([[1.0], [1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        # Error: not a qubit state
        validator = QubitStateValidator(state=state)
        self.assertRaises(QubitStateValidationError, error_raiser, validator)

    def test_state_wrong_type_2(self):
        array = np.array([[1.0], [1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        # Error: not a state
        validator = QubitStateValidator(state=vector)
        self.assertRaises(QubitStateValidationError, error_raiser, validator)
    
    def test_null_state(self):
        array = np.array([[1.0], [1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        # Error: zero state is not a QuantumState instance
        validator = QubitStateValidator(state=NULL_STATE)
        self.assertRaises(QubitStateValidationError, error_raiser, validator)


class TestQubitStateValidator_StateInit(unittest.TestCase):
    def test_state_1(self):
        array = np.array([[1.0], [1.0], [1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(state=state)
        vdvector = validator.validated_data()['vector']
        noq = validator.validated_data()['number_of_qubits']
        # validated vector and the vector used to initialise quantum state are
        # not equal, due to normalisation.
        self.assertFalse(vector == vdvector)
        self.assertEqual(noq, 2)
        # normalised vector equals the vector acquired from a state.
        self.assertTrue(vector.normalize() == vdvector)

    def test_state_2(self):
        array = np.array([[1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(state=state)
        vdvector = validator.validated_data()['vector']
        noq = validator.validated_data()['number_of_qubits']
        # validated vector and the vector used to initialise quantum state are
        # not equal, due to normalisation.
        self.assertFalse(vector == vdvector)
        self.assertEqual(noq, 3)
        # normalised vector equals the vector acquired from a state.
        self.assertTrue(vector.normalize() == vdvector)

    def test_state_3(self):
        array = np.array([[1.0], [1.0], [0.0], [1.0], [1.0], [0.0], [1.0], [1.0]])
        vector = ColumnVector(array=array)
        state = QuantumState(vector=vector)
        validator = QubitStateValidator(state=state)
        vdvector = validator.validated_data()['vector']
        noq = validator.validated_data()['number_of_qubits']
        # validated vector and the vector used to initialise quantum state are
        # not equal, due to normalisation.
        self.assertFalse(vector == vdvector)
        self.assertEqual(noq, 3)
        # normalised vector equals the vector acquired from a state.
        self.assertTrue(vector.normalize() == vdvector)




"""
class TestQubitBitlistValidator(unittest.TestCase):
    def test_pass(self):
        bitlist = [(0.25, '00'), (0.25, '01'), (0.25, '10')]
        validator = QubitBitlistValidator(bitlist=bitlist)
        vd = validator.validated_data()['bitlist']
        self.assertEqual(bitlist, vd)


class TestQubitBitlistValidator_Bitstring(unittest.TestCase):    
    def test_nonuniform_bitstring(self):
        bitlist = [(0.25, '00'), (0.25, '0'), (0.25, '10')]
        validator = QubitBitlistValidator(bitlist=bitlist)
        def error_raiser(dummy):
            raise validator.report_errors()[0]
        self.assertRaises(ValidationError, error_raiser, None)
    
    def test_nonstring_bitstring(self):
        bitlist = [(0.25, 90), (0.25, '00'), (0.25, '10')]
        validator = QubitBitlistValidator(bitlist=bitlist)
        def error_raiser(dummy):
            raise validator.report_errors()[0]
        self.assertRaises(ValidationError, error_raiser, None)
    
    def test_noninteger_bitstring(self):
        bitlist = [(0.25, 'aa'), (0.25, '00'), (0.25, '10')]
        try:
            validator = QubitBitlistValidator(bitlist=bitlist)
            def error_raiser(dummy):
                raise validator.report_errors()[0]
            self.assertRaises(ValidationError, error_raiser, None)
        except Exception as e:
            self.assertRaises(type(e))
        
        
class TestQubitBitlistValidator_Amplitude(unittest.TestCase):    
    def test_nonnumeric_amplitude(self):
        bitlist = [('0.25', '00'), (0.25, '01'), (0.25, '10')]
        validator = QubitBitlistValidator(bitlist=bitlist)
        def error_raiser(dummy):
            raise validator.report_errors()[0]
        self.assertRaises(ValidationError, error_raiser, None)


class TestQubitBitlistValidator_ListElement(unittest.TestCase):    
    def test_tuple_length(self):
        bitlist = [(0.25,'00',1.0), (0.25, '01'), (0.25, '10')]
        validator = QubitBitlistValidator(bitlist=bitlist)
        def error_raiser(dummy):
            raise validator.report_errors()[0]
        self.assertRaises(ValidationError, error_raiser, None)
    
    def test_nontuple_element_1(self):
        bitlist = [(0.25,'00'), [0.25, '01'], (0.25, '10')]
        validator = QubitBitlistValidator(bitlist=bitlist)
        def error_raiser(dummy):
            raise validator.report_errors()[0]
        self.assertRaises(ValidationError, error_raiser, None)
    
    def test_nontuple_element_2(self):
        bitlist = [(0.25,'00'), 0.25, (0.25, '10')]
        validator = QubitBitlistValidator(bitlist=bitlist)
        def error_raiser(dummy):
            raise validator.report_errors()[0]
        self.assertRaises(ValidationError, error_raiser, None)
"""