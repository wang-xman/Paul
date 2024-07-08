#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
File under test:
    quantum_state.braket.py

Main test
    Braket representation of quantum state.

Updated:
    25 September 2021
"""
import unittest
import numpy as np

from linear_space.vector import UnitVector, RowVector

from quantum_state.errors import BraketValidationError
from quantum_state.braket import Bra, Ket, BraketValidator
from quantum_state.quantum_state import QuantumState


def error_raiser(validator):
    if not validator.is_valid:
        validator.raise_last_error()


class Test_BraketValidator_KetString(unittest.TestCase):
    test_state = QuantumState(vector=UnitVector(array=np.array([[1.0],[1.0]])))

    def test_label_wrong_types(self):
        # Error: ket string wrong type
        test_label = 20
        validator = BraketValidator(label=test_label, state=self.test_state)
        self.assertRaises(BraketValidationError, error_raiser, validator)

        # Error: ket string wrong type
        test_label = [0,1,0]
        validator = BraketValidator(label=test_label, state=self.test_state)
        self.assertRaises(BraketValidationError, error_raiser, validator)

    def test_label_empty(self):
        # Error: ket string is empty
        test_label = ""
        validator = BraketValidator(label=test_label, state=self.test_state)
        self.assertRaises(BraketValidationError, error_raiser, validator)

    def test_label_has_only_spaces(self):
        # Error: ket string contains only spaces
        test_label = " "
        validator = BraketValidator(label=test_label, state=self.test_state)
        self.assertRaises(BraketValidationError, error_raiser, validator)

    def test_label_begins_with_space(self):
        # Error: ket string begins with space
        test_label = " A"
        validator = BraketValidator(label=test_label, state=self.test_state)
        self.assertRaises(BraketValidationError, error_raiser, validator)

    def test_label_success(self):
        # Pass:
        test_label = "Alpha"
        test_obj = BraketValidator(label=test_label, state=self.test_state)
        validated_data = test_obj.validated_data()
        self.assertEqual(validated_data['label'], test_label)

        # Pass:
        test_label = "13xcasj908"
        test_obj = BraketValidator(label=test_label, state=self.test_state)
        validated_data = test_obj.validated_data()
        self.assertEqual(validated_data['label'], test_label)


class Test_Ket(unittest.TestCase):
    def test_missing_quantum_state(self):
        # Error: quantum state instance is missing.
        test_label = "Alpha"
        #self.assertRaises(KetInitError, Ket, test_label, None)
        self.assertRaises(BraketValidationError, Ket, test_label, None)

    def test_quantum_state_wrong_type(self):    
        # Error: quantum state is not an instance
        test_label = "Alpha"
        test_state = np.array([1, 2])
        self.assertRaises(BraketValidationError, Ket, test_label, test_state)

    def test_correct_quantum_state_instance(self):
        state = QuantumState(vector=UnitVector(array=np.array([[1.0],[1.0]])))
        label = 'AlphaBeta'
        ket = Ket(label=label, state=state)
        self.assertTrue(isinstance(ket, QuantumState))


class Test_Bra(unittest.TestCase):
    def test_init(self):
        state = QuantumState(vector=UnitVector(array=np.array([[1.0],[1.0]])))
        label = 'Alpha'
        bra = Bra(label=label, state=state)

    def test_init_without_label(self):
        state = QuantumState(vector=UnitVector(array=np.array([[1.0],[1.0]])))
        # Error
        self.assertRaises(BraketValidationError, Bra, None, state)

    def test_init_without_state(self):
        state = QuantumState(vector=UnitVector(array=np.array([[1.0],[1.0]])))
        # Error
        self.assertRaises(BraketValidationError, Bra, 'label', None)

    def test_init_without_both(self):
        # Error
        self.assertRaises(BraketValidationError, Bra, None, None)

    def test_label(self):
        state = QuantumState(vector=UnitVector(array=np.array([[1.0],[1.0]])))
        label = 'Alpha'
        bra = Bra(label=label, state=state)
        self.assertTrue(label == bra.label)

    def test_repr(self):
        state = QuantumState(vector=UnitVector(array=np.array([[1.0],[1.0]])))
        label = 'Alpha'
        bra = Bra(label=label, state=state)
        #print(bra)


class Test_BraKet_Vector(unittest.TestCase):
    def test_bra_vector(self):
        state = QuantumState(
            vector=UnitVector(array=np.array([[1.0],[1.0j],[1.0j],[1.0]])))
        label = 'Alpha'
        bra = Bra(label=label, state=state)
        self.assertTrue(isinstance(bra.as_vector(), RowVector))
        #ket = bra.hermitian_conjugate
        #self.assertTrue(isinstance(ket.as_vector(), UnitVector))
        #print(bra)

    def test_ket_vector(self):
        state = QuantumState(
            vector=UnitVector(array=np.array([[1.0],[1.0j],[1.0j],[1.0]])))
        label = 'Beta'
        ket = Ket(label=label, state=state)
        self.assertTrue(isinstance(ket.as_vector(), UnitVector))
        #bra = ket.hermitian_conjugate
        #self.assertTrue(isinstance(bra.as_vector(), RowVector))