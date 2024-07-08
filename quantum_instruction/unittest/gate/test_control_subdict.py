"""
File under test
    quantum_instruction.gate.validators.py

Main test:
    Gate operation instruction control sub-dictionary validators.

Updated:
    12 August 2021
"""
import unittest
from quantum_instruction.base import InstructionBaseValidationError
from quantum_instruction.gate.validators import ControlSubdictValidator, \
    ControlSubdictElementValidator


def error_raiser(validator):
    validator.raise_last_error()


class TestControlElementValidator(unittest.TestCase):
    def test_okay(self):
        eledict = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        validator = ControlSubdictElementValidator(element=eledict)
        self.assertTrue(validator.is_valid)

    def test_missing_register(self):
        eledict = {
            #'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        validator = ControlSubdictElementValidator(element=eledict)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: key register is missing
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_missing_local_index(self):
        eledict = {
            'register': 'reg1',
            #'local_index': 0,
            'state': '1'
        }
        validator = ControlSubdictElementValidator(element=eledict)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: local index is missing
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_missing_value(self):
        eledict = {
            'register': 'reg1',
            'local_index': 0,
            #'state': '1'
        }
        validator = ControlSubdictElementValidator(element=eledict)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: control state is missing
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_unknown_key_warning(self):
        eledict = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1',
            'EXTRA': 0.5
        }
        validator = ControlSubdictElementValidator(element=eledict)
        #raise validator.report_errors()[0]
        self.assertTrue(validator.is_valid)


class TestControlDictValidator(unittest.TestCase):
    def test_okay(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        control_dict = {
            'list': [el]
        }
        target = {
            'register': 'reg1',
            'local_index': 1
        }
        validator = ControlSubdictValidator(control_dict=control_dict,
                                              target_dict=target)
        self.assertTrue(validator.is_valid)

    def test_missing_list(self):
        control_dict = {
            'nolist': 'ab'
        }
        target = {
            'register': 'reg1',
            'local_index': 1
        }
        validator = ControlSubdictValidator(control_dict=control_dict,
                                              target_dict=target)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: missing a key list
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_non_list_control_list(self):
        control_dict = {
            'list': 'ab'
        }
        target = {
            'register': 'reg1',
            'local_index': 1
        }
        validator = ControlSubdictValidator(control_dict=control_dict,
                                              target_dict=target)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        # Error: key list is non list
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_okay_multiple_els(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 1,
            'state': '1'
        }
        control_dict = {
            'list': [el, el2]
        }
        target = {
            'register': 'reg2',
            'local_index': 1
        }
        validator = ControlSubdictValidator(control_dict=control_dict,
                                              target_dict=target)
        #error_raiser(validator)
        self.assertTrue(validator.is_valid)

    def test_error_in_one_els(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 1,
        }
        control_dict = {
            'list': [el, el2]
        }
        target = {
            'register': 'reg2',
            'local_index': 1
        }
        validator = ControlSubdictValidator(control_dict=control_dict,
                                              target_dict=target)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)


class TestIdenticalControlBitsError(unittest.TestCase):
    def test_double_entry(self):
        el = {
            'register': 'reg1',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 0,
            'state': '0'
        }
        control_dict = {
            'list': [el, el2]
        }
        target = {
            'register': 'reg2',
            'local_index': 1
        }
        validator = ControlSubdictValidator(control_dict=control_dict,
                                              target_dict=target)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_non_double_entry(self):
        el = {
            'register': 'reg2',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 0,
            'state': '0'
        }
        control_dict = {
            'list': [el, el2]
        }
        target = {
            'register': 'reg2',
            'local_index': 1
        }
        validator = ControlSubdictValidator(control_dict=control_dict,
                                              target_dict=target)
        #raise validator.report_errors()[0]
        self.assertTrue(validator.is_valid)
        #self.assertRaises(InstructionBaseValidationError, error_raiser, validator)

    def test_clash_with_target_bit(self):
        el = {
            'register': 'reg2',
            'local_index': 0,
            'state': '1'
        }
        el2 = {
            'register': 'reg1',
            'local_index': 0,
            'state': '0'
        }
        control_dict = {
            'list': [el, el2]
        }
        target = {
            'register': 'reg2',
            'local_index': 0
        }
        validator = ControlSubdictValidator(control_dict=control_dict,
                                              target_dict=target)
        #raise validator.report_errors()[0]
        self.assertFalse(validator.is_valid)
        self.assertRaises(InstructionBaseValidationError, error_raiser, validator)
