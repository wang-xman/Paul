"""
File under test
    quantum_instruction.gate_instruction.py

Main test:
    Gate-operation instruction class.

Updated:
    03 September 2021
"""
import unittest
from gate import single_qubit_gates as singles
from quantum_instruction.gate.instructions import GateInstruction


def error_raiser(validator):
    validator.raise_last_error()


class Test_Success(unittest.TestCase):
    def test_control(self):
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
        instruc_dict = {
            'gate': {
                'alias': 'Flip',
                'parameters': {}
            },
            'target': {
                'register': 'reg2',
                'local_index': 1
            },
            'control': {
                'list':[el, el2]
            }
        }
        instruction = GateInstruction(instruc_dict)
        self.assertDictEqual(instruction.gate_dict, instruc_dict['gate'])
        self.assertDictEqual(instruction.target_dict, instruc_dict['target'])
        self.assertDictEqual(instruction.control_dict, instruc_dict['control'])
        self.assertTrue(instruction.has_control)
        self.assertDictEqual(instruction.get_control_list()[0], el)


class Test_Noncontrol(unittest.TestCase):
    def test_non_control(self):
        instruc_dict = {
            'gate': {
                'alias': 'Flip',
                'parameters': {}
            },
            'target': {
                'register': 'reg2',
                'local_index': 1
            }
        }
        instruction = GateInstruction(instruc_dict)
        self.assertFalse(instruction.has_control)
        self.assertFalse(instruction.has_gate_instance)
        self.assertFalse(instruction.gate_instance is not None)


class Test_User_Defined_Gate(unittest.TestCase):
    def test_okay(self):
        gate_instance = singles['Flip']
        instruc_dict = {
            'gate': {
                'instance': gate_instance,
                'parameters': {}
            },
            'target': {
                'register': 'reg2',
                'local_index': 1
            }
        }
        instruction = GateInstruction(instruc_dict)
        self.assertTrue(instruction.gate_alias == 'Flip')
        self.assertTrue(instruction.has_gate_instance)
        self.assertTrue(instruction.gate_instance is not None)
