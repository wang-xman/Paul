#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_register.base.py

PATH

[app_root]/quantum_register/base.py

INTRO

Quantum register is a container that stores quantum states.
Generic quantum register is designed to store, as the name
suggests, a generic quantum state.

A qubit register is a specialised quantum register that
stores a qubit. Separating qubit register from generic quantum
register has the advantage of easy verification and accessing
the indexing logic behind.

LOG

Updated on 30 September 2021 | Created on 09 May 2021
"""
from .base import AbstractQuantumRegister
from .errors import RegisterError
from .validators import RegisterClassValidator, BaseRegisterInitValidator


class BaseRegister(AbstractQuantumRegister):
    """ Base register class

    Register is a container that stores a state.

    A register provides method to updates the stored state.
    The state to be stored in a register must be compatible
    with the state class the register declares.

    To initialise a register, a state can be absent but the
    label is required.

    CONSTRUCTOR

    `state` (`QuantumState`): a quantum state the register
    is initialised with; it must be a quantum state; it can
    be `None`, then register is empty

    `label` (`str`): a string variable that uniquely
    identifies the register; cannot contain space, cannot
    be empty

    ATTRIBUTES

    `self._label` (`str`): a string to label the register

    `self._state` (`QuantumState` or subclass): quantum state
    object stored in this register

    `self.label`: property; returns the label of register

    `self.has_state`: property; returns `True` is register
    has a state, otherwise `False`

    `self.is_empty`: property; returns `True` (`False`) is
    register does (not) contain a state

    `self.intake(,state)`: replace the current state stored
    in the register by the one provided
    """
    def __new__(cls, *args, **kwargs):
        class_validator = RegisterClassValidator(register_class=cls)
        if not class_validator.is_valid:
            class_validator.raise_last_error()
        return super().__new__(cls)

    def __init__(self, state=None, label=None):
        """ Base register : Constructor

        All subclasses shall as much as possible (AMAP)
        inherit this constructor signature.

        Arguments:

        `state` (obj): a quantum state to be stored in the
        register; register is initialised to the state
        provided at instantiation, but the state can be absent

        `label` (`str`): a string used to label the register;
        a required argument
        """
        validator = BaseRegisterInitValidator(
               state=state, label=label, state_class=self.state_class)
        if validator.is_valid:
            self._label = validator.validated_data()['label']
            self._state = validator.validated_data()['state']
        else:
            validator.raise_last_error()

    @property
    def label(self):
        """ Base register : returns the label """
        return self._label

    @property
    def state(self):
        """ Base register : returns the state """
        if not self.has_state:
            raise RegisterError("Register {} ".format(self._label) +\
                    "is empty. Can't return any state.")
        return self._state

    @property
    def has_state(self):
        """ Base register : Check if a register has a state """
        ret = False
        if not self._state is None:
            ret = True
        return ret

    @property
    def is_empty(self):
        """ Base register : Check if a register is empty """
        ret = not self.has_state
        return ret

    def intake(self, state):
        """ Base register : Take in a state

        Replaces the state originally stored in the register.
        """
        if isinstance(state, self.state_class):
            self._state = state
        else:
            raise RegisterError("State provided to register " +\
                    "{} ".format(self._label) + "is incompatible " +\
                    "with the declared state class. " +\
                    "Register failed to store the state.")
