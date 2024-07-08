#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_register.registers.py

PATH

[app_root]/quantum_register/registers.py

INTRO

Different types of registers.

All registers are, direct or indirect, subclasses of
`BaseRegister`. Following the base class `BaseRegister`,
the constructor requires two keyword arguments,

`state` (obj): a quantum state the register is initialised
to; it must be an instance of the declared state class,
or `None`; if `None`, the register is considered empty

`label` (`str`): a string variable used as a unique identifier
to the register; cannot be `None` or empty, cannot contain space

Difference between computational and other type of registers,
such as ancilla register, is mostly for the convenience of
reference.

LOG

Updated on 30 September 2021 | Created on 24 October 2020
"""
from quantum_state import QuantumState
from qubit import QubitState

from .base_register import BaseRegister, RegisterError

_MODULE_LOCATION_ = 'quantum_register.registers'


class QuantumRegister(BaseRegister):
    """ Generic quantum register class """
    state_class = QuantumState


class QuantumAncillaRegister(QuantumRegister):
    """ Ancilla register for generic quantum state

    A subclass of `QuantumRegister`, and the state class
    declared is thus `QuantumState`.
    """


#class QubitRegister(BaseRegister):
class QubitRegister(QuantumRegister):
    """ Qubit register

    State class of qubit register is of course `QubitState`.

    Two additional attributes,

    `self.noq` : property; an integer, the number of qubits
    of the qubit stored in register

    `self.info` : property; a Python dict contains `label`
    of the register and the `noq` of the state
    """
    state_class = QubitState

    @property
    def noq(self):
        if self.is_empty:
            raise RegisterError('Register {} '.format(self.label) +\
                    'has no state. Failed to return number of qubits.')
        return self.state.noq

    @property
    def local_index_range(self):
        """ Qubit Register : Local index range

        Returns a range object that is `range(0, self.noq, 1)`.
        """
        return range(0, self.noq, 1)

    @property
    def info(self):
        ret = {
            'label': self.label,
            'noq': self.noq
        }
        return ret


class ComputationalRegister(QubitRegister):
    """ Computational register

    Computational register is a qubit register.

    It stores a generic qubit state that includes
    computational basis state.

    Computational register is so defined to distinguish
    it from, for example, ancilla register, in order to
    highlight its role in a memory.
    """


class QubitAncillaRegister(QubitRegister):
    """ Ancilla register for qubits

    Qubit ancilla register specialised to store qubits.
    """
