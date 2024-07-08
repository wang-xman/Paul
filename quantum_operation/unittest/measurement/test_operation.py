"""
File under test
    operation.measurement_operation.py

Main test:
    Test measurement operation class

Updated:
    06 August 2021
"""
import unittest
from linear_space.algebra import norm
#from state.quantum_state import zero_state
#from qubit.qubit import QubitState
from qubit.utils import qubit_from_bitlist
#from density_matrix.density_matrix import DensityMatrix
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory
from quantum_instruction.measurement import MeasurementInstruction
from quantum_operation.measurement import MeasurementOperation
#from operation.measurement_operation import OperationValidationError


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
    s2 = qubit_from_bitlist([(1, '01')])
    reg2 = QubitRegister(label='reg2', state=s2)
    # memory
    memory = MemorySample(register=[reg1, reg2])
    return memory

class Test_Duo_Register_All(unittest.TestCase):
    def test_with_register_traced_out_1(self):
        instruc_dict = {
            'register': 'reg1'
        }
        memory = duo_register_memory()
        instruc = MeasurementInstruction(instruc_dict=instruc_dict)
        mop = MeasurementOperation(instruc)
        probs = memory.operation_socket(mop)
        # reg2 is traced out.
        self.assertTrue(norm(probs['11'] - 0.5) < 1e-15)
        self.assertTrue(norm(probs['10'] - 0.5) < 1e-15)


def trio_register_memory():
    """ Test memory state (|11> + |10>)|01> (|0>+|1>)"""
    # 1st register
    s1 = qubit_from_bitlist([(1, '11'), (1, '10')])
    reg1 = QubitRegister(label='reg1', state=s1)
    # 2nd register
    s2 = qubit_from_bitlist([(1, '01')])
    reg2 = QubitRegister(label='reg2', state=s2)
    # 3st register
    s3 = qubit_from_bitlist([(1, '0'), (1, '1')])
    reg3 = QubitRegister(label='reg3', state=s3)
    # memory
    memory = MemorySample(register=[reg1, reg2, reg3])
    return memory


class Test_Trio_Register_All(unittest.TestCase):
    def test_measure_reg1(self):
        instruc_dict = {
            'register': 'reg1'
        }
        memory = trio_register_memory()
        instruc = MeasurementInstruction(instruc_dict=instruc_dict)
        mop = MeasurementOperation(instruc)
        probs = memory.operation_socket(mop)
        self.assertListEqual(memory.get_all_labels(), ['reg1'])
        # reg2 and reg3 are traced out.
        self.assertTrue(norm(probs['11'] - 0.5) < 1e-15)
        self.assertTrue(norm(probs['10'] - 0.5) < 1e-15)

    def test_measure_reg2(self):
        instruc_dict = {
            'register': 'reg2'
        }
        memory = trio_register_memory()
        instruc = MeasurementInstruction(instruc_dict=instruc_dict)
        mop = MeasurementOperation(instruc)
        probs = memory.operation_socket(mop)
        self.assertListEqual(memory.get_all_labels(), ['reg2'])
        # reg1 and reg3 are traced out.
        self.assertTrue(norm(probs['01'] - 1.0) < 1e-15)

    def test_measure_reg3(self):
        instruc_dict = {
            'register': 'reg3'
        }
        memory = trio_register_memory()
        instruc = MeasurementInstruction(instruc_dict=instruc_dict)
        mop = MeasurementOperation(instruc)
        probs = memory.operation_socket(mop)
        self.assertListEqual(memory.get_all_labels(), ['reg3'])
        # reg1 and reg2 are traced out.
        self.assertTrue(norm(probs['0'] - 0.5) < 1e-15)
        self.assertTrue(norm(probs['1'] - 0.5) < 1e-15)


class Test_Trio_Register_on_State(unittest.TestCase):
    def test_measure_reg1(self):
        proj_state = qubit_from_bitlist([(1,'10')])
        instruc_dict = {
            'register': 'reg1',
            'state': proj_state
        }
        memory = trio_register_memory()
        instruc = MeasurementInstruction(instruc_dict=instruc_dict)
        mop = MeasurementOperation(instruc)
        probs = memory.operation_socket(mop)
        self.assertListEqual(memory.get_all_labels(), ['reg1'])
        # reg2 and reg3 are traced out.
        #self.assertTrue(norm(probs['11'] - 0.5) < 1e-15)
        self.assertTrue(norm(probs - 0.5) < 1e-15)

    def test_measure_reg2(self):
        proj_state = qubit_from_bitlist([(1,'01'),(1,'10')])
        instruc_dict = {
            'register': 'reg2',
            'state': proj_state
        }
        memory = trio_register_memory()
        instruc = MeasurementInstruction(instruc_dict=instruc_dict)
        mop = MeasurementOperation(instruc)
        probs = memory.operation_socket(mop)
        self.assertListEqual(memory.get_all_labels(), ['reg2'])
        # reg1 and reg3 are traced out.
        #print(probs)
        self.assertTrue(norm(probs - 0.5) < 1e-15)

    def test_measure_reg3(self):
        proj_state = qubit_from_bitlist([(1,'0'),(1,'1')])
        instruc_dict = {
            'register': 'reg3',
            'state': proj_state
        }
        memory = trio_register_memory()
        instruc = MeasurementInstruction(instruc_dict=instruc_dict)
        mop = MeasurementOperation(instruc)
        probs = memory.operation_socket(mop)
        self.assertListEqual(memory.get_all_labels(), ['reg3'])
        # reg1 and reg2 are traced out.
        #print(probs)
        self.assertTrue(norm(probs - 1.0) < 1e-15)
