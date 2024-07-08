#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_memory.base_memory.py

PATH

[app_root]/quantum_memory/base_memory.py

Quantum memory, or memory, is a container of quantum states
and is one of the most basic components in quantum circuit.
Memory shall be a static object, focusing on global state
storage.

Algorithm often requires states in different registers to
be merged into one single global state, due to creation
of entangled states. To implement exactly this feature,
quantum memory is designed in a 'duo-layer' architecture:
The bottom layer is a base memory that stores only the
global state and its associated density matrix, if needed;
The top layer is a specialised object that works with
metadata of registers to determine for example which bit
belong to which register. Qubit memory is one of the
specialised quantum memories.

Advantage of duo-layer architecture is double fold.
First. Working with metadata instead of register itself
frees memory from passing around the underlying state
vector which can be resource hungry for a large state.
All quantum gates designed in this simulation package
are only relying on information such as qubit's local
index and total number of qubits to resize its operator
matrix. Therefore, metadata alone is sufficient before
actual matrix manipulation procedures. Second. Particular
operation such as partial tracing or measurement reduces
the dimension of state vector (or density matrix), which
ends up with modified registers. Such duo-layer strcture
helps us track changes and reflect them on registers.
For users (observers), registers are physical. Yet the
states they store can change.

Also due to the entanglement state, quantum memory must
deny direct external access to states stored in its
registers, so long as the global state is formed. Only
measurement is allowed to be performed on a register,
leading to collapse of the state. This quantum-mechanical
integrity must be maintained in quantum memory.

NOTE Python has internal `MemoryError` class. To avoid name
clash, `QuantumMemory` is prefixed when needed.

CONTENT

`BaseMemory` - Base class to all memory classes;
base class implements getters and setters

LOG

Updated on 28 September 2021 | Created on 18 July 2021
"""
from quantum_state.quantum_state import QuantumState
from qubit.utils import qubit_state_by_tensor_product
from .errors import QuantumMemoryError

_MODULE_LOCATION_ = 'quantum_memory.base_memory'


class BaseMemory:
    """ Base quantum memory class

    Base class to quantum memories. NOT for direct instantiation.

    Base memory class is a container that stores a global state,
    formed by states stored in registers.

    Which part of the global state belongs to which register is not
    the concern of base memory class. This set of information is
    considered as metadata that is managed by the derived memory.

    FIXME What if memory initially stores a density matrix?

    ATTRIBUTES

    `self.label`: a string to label memory

    `self._global_state`: global state created and stored

    `self._update_global_state_with_register(,register)`: method
    to construct a global state with either one register or
    a list of registers

    `self.has_global_state`: property; verifies if the memory has
    a global state stored

    `self.get_global_state()` : getter; returns the global state
    in the memory

    `self.set_global_state(,state)` : setter; manually replace the
    existing global state by `state`; use with caution is advised
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.BaseMemory'

    def __init__(self, label=None):
        """ Base Memory : Constructor

        Base memory creates the most important attributes to a
        memory.

        Arguments

        `label` (`str`) : a string to label memory
        """
        self.label = label
        # global state
        self._global_state = None

    def _update_global_state_with_register(self, register):
        """ Base Memory : Updates global state from register(s)

        Global state is a tensor product of all states stored in
        registers. Argument `register` is either a single register
        or a list of registers.

        In case of a list of registers, the rank of the register
        stored in that list defines the order of the state in the
        tensor product. For example, consider a list
            `[Sa, Sb, Sg]`
        of states, the global state is
            `Sa * Sb * Sg`.

        Arguments

        `register` (register or `list`) : a single register or a
        list of non-empty registers

        TODO If to use this for non-qubit register, the helper
        function must be changed.
        """
        _global_state = None
        # list of registers
        if isinstance(register, list):
            # init
            if self._global_state is None:
                # only one register in list
                if len(register) == 1:
                    _global_state = register[0].state
                # more than one register
                else:
                    # use helper function to create state from list
                    _global_state = qubit_state_by_tensor_product(
                            [reg.state for reg in register])
            # update
            else:
                state_list = [self._global_state]
                for reg in register:
                    state_list.append(reg.state)
                _global_state = qubit_state_by_tensor_product(state_list)
        # single register
        else:
            # init, no existing global state
            if self._global_state is None:
                _global_state = register.state
            # update
            else:
                _global_state = qubit_state_by_tensor_product(
                        [self._global_state, register.state])
        self._global_state = _global_state

    @property
    def has_global_state(self):
        """ Base Memory : Verifies if global state exists """
        ret = False
        if not self._global_state is None:
            ret = True
        return ret

    def get_global_state(self):
        """ Base Memory : Returns global state """
        return self._global_state

    def set_global_state(self, state):
        """ Base Memory : Sets global state

        Manually overrides the existing global state.
        Use with caution.

        Arguments

        `state` (obj) : a quantum state instance used to
        replace the existing global state
        """
        if isinstance(state, QuantumState):
            self._global_state = state
        else:
            raise QuantumMemoryError("State to be stored " +\
                    "in quantum memory is not a valid quantum state.",
                    location=self._ERROR_LOCATION_+'.set_global_state')
