"""
File under test
    operation.partial_trace_operation.py

Main test:
    Test partial trace operation.

Updated:
    14 August 2021
"""
import unittest
from linear_space.algebra import norm
from density_matrix.density_matrix import QubitDensityMatrix
from qubit.utils import qubit_from_bitlist
from quantum_register.registers import QubitRegister
from quantum_memory.qubit_memory import QubitMemory
from quantum_instruction.partial_trace import PartialTraceInstruction

from quantum_operation.partial_trace import PartialTraceOperation


def error_raiser(validator):
    validator.raise_last_error()


class MemorySample(QubitMemory):
    label = 'Test_QuantumMemory'


def single_register_memory():
    """ Single register memory for testing """
    # 1st register
    s1 = qubit_from_bitlist([(1, '111')])
    reg1 = QubitRegister(label='reg1', state=s1)
    memory = MemorySample(register=[reg1])
    return memory


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

def duo_register_memory_2():
    """ Test memory state (|11> + |10>)(|0> + |1>) """
    # 1st register
    s1 = qubit_from_bitlist([(1, '11'), (1, '10')])
    reg1 = QubitRegister(label='reg1', state=s1)
    # 2nd register
    s2 = qubit_from_bitlist([(1, '0'),(1, '1')])
    reg2 = QubitRegister(label='reg2', state=s2)
    # memory
    memory = MemorySample(register=[reg1, reg2])
    return memory

def multiple_register_memory():
    """ Test memory """
    # 1st register
    s1 = qubit_from_bitlist([(1, '0100'), (1, '1011')])
    reg1 = QubitRegister(label='reg1', state=s1)
    # 2nd register
    s2 = qubit_from_bitlist([(1, '001')])
    reg2 = QubitRegister(label='reg2', state=s2)
    # 3rd register
    s3 = qubit_from_bitlist([(1, '1010')])
    reg3 = QubitRegister(label='reg3', state=s3)
    # memory
    memory = MemorySample(register=[reg1, reg2, reg3])
    return memory


class Test_PartialTracing_EntireRegister(unittest.TestCase):
    def test_on_reg2(self):
        memory = duo_register_memory()
        pt_operation_dict = {
            'register': 'reg2'
        }
        pt_instruc = PartialTraceInstruction(pt_operation_dict)
        ptop = PartialTraceOperation(pt_instruc)
        reduced_density_matrix = ptop.launch_in_socket(memory)
        expected_density_matrix = QubitDensityMatrix(
                state=qubit_from_bitlist([(1, '11'), (1, '10')]))
        self.assertTrue(reduced_density_matrix[2][2] == expected_density_matrix[2][2])
        self.assertTrue(reduced_density_matrix[2][3] == expected_density_matrix[2][3])
        self.assertTrue(reduced_density_matrix[3][2] == expected_density_matrix[3][2])
        self.assertTrue(reduced_density_matrix[3][3] == expected_density_matrix[3][3])

    def test_on_reg1_duoreg(self):
        """ Initial state (|11> + |10>)(|0> + |1>)

        Can't directly compare two matrix elements, must use norm
        or other helper function to confine the difference into
        an infinitesimal number.
        """
        memory = duo_register_memory_2()
        pt_operation_dict = {
            'register': 'reg1'
        }
        pt_instruc = PartialTraceInstruction(pt_operation_dict)
        ptop = PartialTraceOperation(pt_instruc)
        reduced_density_matrix = ptop.launch_in_socket(memory)
        expected_density_matrix = QubitDensityMatrix(
                state=qubit_from_bitlist([(1, '1'), (1, '0')]))
        # don't compare them directly
        self.assertTrue(
            norm(reduced_density_matrix[0][0]- expected_density_matrix[0][0]) < 1e-15)
        self.assertTrue(norm(reduced_density_matrix[0][1]- expected_density_matrix[0][1]) < 1e-15)
        self.assertTrue(norm(reduced_density_matrix[1][0]- expected_density_matrix[1][0]) < 1e-15)
        self.assertTrue(norm(reduced_density_matrix[1][1]- expected_density_matrix[1][1]) < 1e-15)


class Test_PartialTracing_PartOfRegister(unittest.TestCase):
    def test_okay_off_1bit(self):
        memory = duo_register_memory()
        pt_operation_dict = {
            'register': 'reg1',
            'local_index_range': [1,1]
        }
        pt_instruc = PartialTraceInstruction(pt_operation_dict)
        ptop = PartialTraceOperation(pt_instruc)
        reduced_density_matrix = ptop.launch_in_socket(memory)
        # resulting density matrix is made from state |1>|0>
        expected_density_matrix = QubitDensityMatrix(
                state=qubit_from_bitlist([(1, '10')]))
        self.assertTrue(norm(reduced_density_matrix[0][0] -
                             expected_density_matrix[0][0]) < 1e-15)

    def test_on_reg1_via_range(self):
        """ Tracing out entire register using local index range """
        memory = duo_register_memory_2()
        pt_operation_dict = {
            'register': 'reg1',
            'local_index_range': [0,1]
        }
        pt_instruc = PartialTraceInstruction(pt_operation_dict)
        ptop = PartialTraceOperation(pt_instruc)
        reduced_density_matrix = ptop.launch_in_socket(memory)
        #memory.operation_socket()
        expected_density_matrix = QubitDensityMatrix(
                state=qubit_from_bitlist([(1, '1'), (1, '0')]))
        # don't compare them directly
        self.assertTrue(
            norm(reduced_density_matrix[0][0]-expected_density_matrix[0][0]) < 1e-15)
        self.assertTrue(norm(reduced_density_matrix[0][1]-expected_density_matrix[0][1]) < 1e-15)
        self.assertTrue(norm(reduced_density_matrix[1][0]-expected_density_matrix[1][0]) < 1e-15)
        self.assertTrue(norm(reduced_density_matrix[1][1]-expected_density_matrix[1][1]) < 1e-15)
