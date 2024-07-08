"""
File under test
    operation.measurement_operation.py

Main test:
    Test measurement operation on memory validator

Updated:
    25 August 2021
"""
import unittest
from quantum_state import NULL_STATE
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory
from quantum_instruction.base import InstructionBaseValidationError
from quantum_instruction.measurement import MeasurementInstruction

from quantum_operation.measurement import MeasurementOperationValidator as MOV
from quantum_operation.measurement import MeasurementOperationValidationError


def raiser(validator):
    validator.raise_last_error()

class MemorySample(QubitMemory):
    label = 'Test_QubitMemory'

def duo_register_memory():
    """ Test memory state (|11> + |10>)|0> """
    # 1st register
    s1 = qubit_from_bitlist([(1, '11'), (1, '10')])
    reg1 = QubitRegister(label='reg1', state=s1)
    # 2nd register
    s2 = qubit_from_bitlist([(1, '0')])
    reg2 = QubitRegister(label='reg2', state=s2)
    # memory
    memory = MemorySample(register=[reg1, reg2])
    return memory


class Test_Register_Only(unittest.TestCase):
    def test_okay(self):
        instruc_dict = {
            'register': 'reg2'
        }
        memory = duo_register_memory()
        minstruc = MeasurementInstruction(instruc_dict)
        validator = MOV(minstruc, memory)
        self.assertTrue(validator.is_valid)

    def test_non_existent_label(self):
        instruc_dict = {
            'register': 'reg5'
        }
        memory = duo_register_memory()
        minstruc = MeasurementInstruction(instruc_dict)
        validator = MOV(minstruc, memory)
        self.assertFalse(validator.is_valid)
        self.assertRaises(MeasurementOperationValidationError, raiser, validator)


class Test_with_State(unittest.TestCase):
    def test_okay(self):
        instruc_dict = {
            'register': 'reg2',
            'state': qubit_from_bitlist([(1,'0')])
        }
        memory = duo_register_memory()
        minstruc = MeasurementInstruction(instruc_dict)
        validator = MOV(minstruc, memory)
        self.assertTrue(validator.is_valid)

    def test_non_qubit(self):
        instruc_dict = {
            'register': 'reg2',
            'state': NULL_STATE
        }
        #memory = duo_register_memory()
        # Error: at instruction level
        self.assertRaises(InstructionBaseValidationError, MeasurementInstruction,
                          instruc_dict)

    def test_mismatched_noq(self):
        instruc_dict = {
            'register': 'reg2',
            'state': qubit_from_bitlist([(1,'01')])
        }
        memory = duo_register_memory()
        minstruc = MeasurementInstruction(instruc_dict)
        validator = MOV(minstruc, memory)
        self.assertFalse(validator.is_valid)
        self.assertRaises(MeasurementOperationValidationError, raiser, validator)
