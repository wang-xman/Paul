"""
Gate under test:
    Qubit SWAP

File under test:
    gate.multiple.py

Updated:
    20 April 2021
"""
import unittest
import numpy as np
from linear_space.vector import UnitVector
from qubit import QubitState, ComputationalBasis
from qubit.utils import qubit_from_bitlist
from gate import single_qubit_gates as singles

from gate.multiple_qubit import SWAP


class Test(unittest.TestCase):
    def test(self):
        print("\n *** *** SWAP gate *** ***")


class TestSWAP_Basis(unittest.TestCase):
    gate = SWAP

    def test_basis_2bits(self):
        test_state = ComputationalBasis(bitstring='01')
        # apply SWAP
        alpha = 0
        beta = 1
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'alpha':alpha, 
            'beta':beta
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='10')
        self.assertTrue(new_state == exp_state)
    
    def test_basis_3bits(self):
        test_state = ComputationalBasis(bitstring='010')
        # apply SWAP
        alpha = 1
        beta = 2
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'alpha':alpha, 
            'beta':beta
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='001')
        self.assertTrue(new_state == exp_state)
    
    def test_basis_5bits(self):
        test_state = ComputationalBasis(bitstring='01101')
        # apply SWAP
        alpha = 0
        beta = 4
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'alpha':alpha, 
            'beta':beta
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='11100')
        self.assertTrue(new_state == exp_state)
    
    def test_basis_8bits(self):
        test_state = ComputationalBasis(bitstring='01101010')
        # apply SWAP
        alpha = 2
        beta = 7
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'alpha':alpha, 
            'beta':beta
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='01001011')
        self.assertTrue(new_state == exp_state)
    
    def test_basis_8bits_2(self):
        test_state = ComputationalBasis(bitstring='01101010')
        # apply SWAP
        alpha = 0
        beta = 6
        params = {
            'input_state': test_state,
            'noq':test_state.noq, 
            'alpha':alpha, 
            'beta':beta
        }
        new_state = self.gate(**params)
        exp_state = ComputationalBasis(bitstring='11101000')
        self.assertTrue(new_state == exp_state)


class TestSWAP_GenericQubitState(unittest.TestCase):
    gate = SWAP

    def test_2bits(self):
        # |01> + |11>
        test_state = QubitState(vector=UnitVector(array=np.array([[0],[1],[0],[1]])))
        params = {
            'input_state':test_state,
            'noq':test_state.noq,
            'alpha':0, 
            'beta':1
        }
        # new state |10> + |11>
        new_state = self.gate(**params)
        exp_state = QubitState(vector=UnitVector(array=np.array([[0],[0],[1],[1]])))
        self.assertTrue(new_state == exp_state)
    
    def test_3bits(self):
        # |010> + |001> +|110>
        test_list = [(1.0, '010'),(1.0, '001'), (1.0,'110')]
        test_state = qubit_from_bitlist(test_list)
        params = {
            'input_state':test_state,
            'noq':test_state.noq,
            'alpha':1, 
            'beta':2
        }
        # new state |001> + |010> +|101>
        new_state = self.gate(**params)
        exp_state = qubit_from_bitlist([(1.0, '010'),(1.0, '001'), (1.0,'101')])
        self.assertTrue(new_state == exp_state)
    
    def test_4bits(self):
        # |0101> + |1101>
        test_list = [(1.0, '0101'), (1.0,'1101')]
        test_state = qubit_from_bitlist(test_list)
        params = {
            'input_state':test_state,
            'noq':test_state.noq,
            'alpha':1, 
            'beta':2
        }
        # new state |0011> + |1011>
        new_state = self.gate(**params)
        exp_state = qubit_from_bitlist([(1.0, '0011'), (1.0,'1011')])
        self.assertTrue(new_state == exp_state)
    
    def test_5bits(self):
        # 0.6 |01011> + 0.8 |11011>
        test_list = [(3.0, '01011'), (4.0,'11011')]
        test_state = qubit_from_bitlist(test_list)
        params = {
            'input_state':test_state, 
            'noq':test_state.noq,
            'alpha':4, 
            'beta':2
        }
        # new state 0.6 |01110> + 0.8 |11110>
        new_state = self.gate(**params)
        exp_state = qubit_from_bitlist([(3.0, '01110'), (4.0,'11110')])
        self.assertTrue(new_state == exp_state)


class TestSWAP_SequentialApplication(unittest.TestCase):
    gate = SWAP
    
    def test_swap_to_original(self):
        """ Performing the SWAP operation on the same bits twice
        shall generate the original state.
        """
        # 0.6 |01011> + 0.8 |11011>
        test_list = [(3.0, '01011'), (4.0,'11011')]
        test_state = qubit_from_bitlist(test_list)
        params = {
            'input_state':test_state,
            'noq':test_state.noq,
            'alpha':4, 
            'beta':2
        }
        # new state 0.6 |01110> + 0.8 |11110>
        new_state = self.gate(**params)
        # swap 4 and 2 again back to 0.6 |01011> + 0.8 |11011>
        params_2 = {
            'input_state':new_state, 
            'noq':test_state.noq,
            'alpha':4, 
            'beta':2
        }
        final = self.gate(**params_2)
        # should be back to the original
        self.assertTrue(final == test_state)

    def test_5bits(self):
        # 0.6 |01011> + 0.8 |11011>
        test_list = [(3.0, '01011'), (4.0,'11011')]
        test_state = qubit_from_bitlist(test_list)
        params = {
            'input_state':test_state, 
            'noq':test_state.noq,
            'alpha':4, 
            'beta':2
        }
        # new state 0.6 |01110> + 0.8 |11110>
        new_state = self.gate(**params)
        # swap 4 and 0
        # then the final 0.6 |01110> + 0.8 |01111>
        params_2 = {
            'input_state':new_state, 
            'noq':test_state.noq,
            'alpha':4, 
            'beta':0
        }
        final = self.gate(**params_2)
        exp_state = qubit_from_bitlist([(3.0, '01110'), (4.0,'01111')])
        self.assertTrue(final == exp_state)
