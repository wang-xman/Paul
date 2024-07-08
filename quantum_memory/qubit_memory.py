#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_memory.qubit_memory.py

PATH

[app_root]/quantum_memory/qubit_memory.py

INTRO

Qubit memory is a specialised memory that stores
only qubits.

Register's metadata object is stored in a list,
named register metadata list. Rank of a register
is the index of it appering in this list.
For example, in a metadata list
    `[reg_a, reg_b, reg_z]`
the rank of 'reg_a' is 0, rank of 'reg_b' is 1.

A memory is considered 'iterable' only if it
contains non-emtpy qubit registers. Qubit memory
is exactly iterable. A generic quantum register
is not necessarily iterable, as it may not contain
a state that can be indexed.

CONTENT

`QubitRegisterMetadata` - Qubit register metadata
class is a subclass of `BaseRegisterMetadata`

`QubitMemory` - Qubit memory class specialised in store
qubit registers and qubit states; it implements register
manager and index managers; a subclass of `BaseMemory`

LOG

Updated on 01 October 2021 | Created on 11 August 2021
"""
from linear_space.number import is_integer
from quantum_operator.quantum_operators import QubitOperator
from density_matrix.density_matrix import DensityMatrix
from quantum_register.registers import QubitRegister

from .validators import QubitMemoryRegisterValidator, OperationLauncherValidator
from .managers import IndexManager, RegisterMetadataManager
from .base_memory import BaseMemory
from .metadata import BaseRegisterMetadata
from .errors import QubitRegisterMetadataError, QubitMemoryError

_MODULE_LOCATION_ = 'quantum_memory.qubit_memory'


class QubitRegisterMetadata(BaseRegisterMetadata):
    """ Qubit register metadata object

    Qubit register metadata is specialised in wrapping
    qubit registers.

    In addition to properties collected in base class
    `BaseRegisterMetadata`, the following information
    about the referenced register are also gathered,

    `self.noq` : integer, number of qubits in register

    `self.local_index_range` : range object, range of
    qubit index in register, merely reflects the number
    of qubits

    `self.rank` : integer, rank of a qubit register as
    its index in memory's metadata list

    `self.status` : binary 0 or 1, 0 reflects an inactive
    register, 1 is for an active one.

    In addition to setters and getter in base class, the
    following setters and getters are added,

    `self.set_rank(, new_rank)` : set the rank of the
    referenced register

    `self.set_status(,new_status)` : gives referenced
    register a new status

    `self.as_dict()` : returns metadata as a dictionary
    which has the following keys
        {
            'label': (due to base class)
            'register_type': (due to base class)
            'noq': number of qubits,
            'rank': rank in metadata list,
            'status': active or inactive
        }
    """
    def __init__(self, register):
        """ Qubit Register Metadata : """
        if isinstance(register, QubitRegister):
            super().__init__(register)
            # rank in memory
            self._rank = None
            # status in memory
            self._status = None
        else:
            raise QubitRegisterMetadataError("Qubit register metadata " +\
                    "object references only to qubit register or its " +\
                    "subclasses.")

    def set_rank(self, new_rank):
        if is_integer(new_rank):
            self._rank = new_rank
        else:
            raise QubitRegisterMetadataError("Qubit register rank in " +\
                    "qubit memory can only be an integer.")

    def set_status(self, new_status):
        self._status = new_status

    def set_register(self, new_register):
        """ Qubit Register Metadata : Sets referenced register

        Arguements

        `new_register` : a qubit register instance used to replace
        existing one
        """
        if isinstance(new_register, QubitRegister):
            super().set_register(new_register)
        else:
            raise QubitRegisterMetadataError("Qubit register metadata " +\
                    "object can only be set to reference a qubit register.")

    @property
    def noq(self):
        return self.get_register().noq

    @property
    def local_index_range(self):
        return self.get_register().local_index_range

    @property
    def rank(self):
        return self._rank

    @property
    def status(self):
        return self._status

    def as_dict(self):
        """ Qubit Register Metadata : Converts to dict """
        metadata_dict = super().as_dict()
        metadata_dict['noq'] = self.noq
        metadata_dict['local_index_range'] = self.local_index_range
        metadata_dict['rank'] = self.rank
        metadata_dict['status'] = self.status
        return metadata_dict


class QubitMemory(IndexManager, RegisterMetadataManager, BaseMemory):
    """ Qubit memory

    Qubit memory has an internal metadata list storing
    the metadata objects of registers.

    ATTRIBUTES

    `cls.register_class` (`class`) : class of accepted
    register

    `self._metadata_list` (`list`) : metadata objects of
    registers are stored in the list

    `self._global_density_matrix`: density matrix formed
    using the global state stored in memory

    `self._update_metadata_list(,register)` : method to
    create a metadata list using user-provided register or
    register list

    `self._update_memory_with_register(,register)` : update
    the current metadata list and thus the global state

    `self.get_register_metadata_list()` : getter; return the
    existing metadata list

    `self.number_of_registers` : property; returns the number
    of registers according to the metadata list

    `self.has_register()`: property; returns `True` if register
    list is not empty, otherwise `False`

    `self._make_global_density_matrix()` : create a density
    matrix using the existing global state and store it in
    `self._global_density_matrix`

    `self.get_global_density_matrix()` : getter; returns the
    global density matrix

    `self.append_register(,register)` : append register metadata
    to the existing metadata list and update the global state
    accordingly

    `self.operation_socket(,operation)` : method to accept
    operation object and launch it

    `self.on_global_state(,operator)` : method to accept a qubit
    operator and apply it on global state

    `self.remove_register_metadata_by_rank(,rank)` : method to
    remove a register metadata from the list using its rank;
    ranks of the remaining metadata are hence changed

    `self.remove_register_metadata_by_label(,label)` : method to
    remove a register metadata from the list using its label;
    ranks of the remaining metadata are hence changed

    CONSTRUCTOR

    `register` (`QubitRegister`) : either a valid qubit register,
    or a list of qubit registers; register can NOT be empty

    `lable` (`str`) : a string to label memory
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.QubitMemory'
    register_class = QubitRegister

    def __init__(self, register=None, label=None):
        """ Qubit Memory : Initialiser

        FIXME Label hasn't been tested.
        """
        super().__init__(label)
        self._metadata_list = []
        self._global_density_matrix = None
        validator = QubitMemoryRegisterValidator(register=register,
                register_class=self.register_class)
        # after validator, registers provided externally
        # won't have identical labels.
        if validator.is_valid:
            self._update_memory_with_register(register)
        else:
            validator.raise_last_error(
                    location=self._ERROR_LOCATION_+'.__init__')

    def _update_metadata_list(self, register):
        """ Qubit Memory : Updates metadata list

        Initialises and updates metadata list. Need to always
        check if a label exists already.
        """
        existing_labels = self.get_all_labels()
        if isinstance(register, list):
            for rank, reg in enumerate(register):
                if not reg.label in existing_labels:
                    metadata = QubitRegisterMetadata(reg)
                    metadata.set_rank(rank)
                    metadata.set_status(1)
                    existing_labels.append(reg.label)
                    self._metadata_list.append(metadata)
                else:
                    raise QubitMemoryError("A register " +\
                            "with label '{}' ".format(reg.label) +\
                            "already exists in memory.")
        else:
            if not register.label in existing_labels:
                metadata = QubitRegisterMetadata(register)
                metadata.set_rank(0)
                metadata.set_status(1)
                self._metadata_list.append(metadata)
            else:
                raise QubitMemoryError("A register " +\
                        "with label '{}' ".format(register.label) +\
                        "already exists in memory.")

    def _update_memory_with_register(self, register):
        """ Qubit Memory : Updates memory with register(s)

        Append the metadata of the user-provided register
        to the existing metadata list; then update the global
        state accordingly.

        NOTE Invoke this method only after validating user
        provided register or list of register(s).
        """
        try:
            # first update metadata list, in case of
            # error, global state update must be on hold.
            self._update_metadata_list(register)
            # then, update global state
            self._update_global_state_with_register(register)
        except Exception as err:
            raise err

    def get_register_metadata_list(self):
        """ Qubit Memory : Returns register metadata list """
        return self._metadata_list

    @property
    def number_of_registers(self):
        """ Qubit Memory : Returns number of registers """
        return len(self.get_register_metadata_list())

    @property
    def has_register(self):
        """ Qubit Memory : Verifies if memory has/no registers """
        ret = False
        if self.number_of_registers != 0:
            ret = True
        return ret

    def _make_global_density_matrix(self):
        """ Qubit Memory : Makes global density matrix

        NOTE For a large qubit state, creation of a density
        matrix can be resource consuming.
        """
        if self._global_state is not None:
            self._global_density_matrix = \
                    DensityMatrix(state=self._global_state)

    @property
    def has_global_density_matrix(self):
        """ Qubit Memory : Verifies existence of global density matrix """
        ret = False
        if isinstance(self._global_density_matrix, DensityMatrix):
            ret = True
        return ret

    def get_global_density_matrix(self):
        """ Qubit Memory : Returns global density matrix """
        return self._global_density_matrix

    def set_global_density_matrix(self, density_matrix):
        """ Qubit Memory : Manually set global density matrix

        Arguments

        `density_matrix` (`DensityMatrix`) : a density matrix
        to be set as the global density matrix
        """
        if isinstance(density_matrix, DensityMatrix):
            self._global_density_matrix = density_matrix
        else:
            raise QubitMemoryError('To set global density ' +\
                    "matrix, a density matrix instance is required.")

    def append_register(self, register):
        """ Qubit Memory : Appends register(s)

        Register or a list of registers is only appended
        to the end of the active metadata list, which also
        implies the formation of a new global state.
        """
        validator = QubitMemoryRegisterValidator(register=register,
                register_class=self.register_class)
        if validator.is_valid:
            self._update_memory_with_register(register)
        else:
            validator.raise_last_error()

    # operation related methods
    def operation_socket(self, operation):
        """ Qubit Memory : Operation socket

        Socket function that accepts operation object.

        Operation is required to have a launcher function
        named `launch_in_socket`. Launcher is required to
        have one positional argument `memory`, which is
        validated using a validator.

        Most importantly, operation socket launcher function
        must to implement all actions it takes on the global
        state and the memory.

        Arguments

        `operation` : an instance of operation class
        """
        ret = None
        # if launcher not found
        try:
            getattr(operation, 'launch_in_socket')
        except AttributeError as err:
            raise QubitMemoryError("Operation object passed " +\
                    "to memory operation socket is missing a launcher " +\
                    "method named 'launch_in_socket'.") from err
        # if launcher exists
        try:
            opl_validator = \
                    OperationLauncherValidator(operation.launch_in_socket)
            if opl_validator.is_valid:
                ret = operation.launch_in_socket(self)
            else:
                raise opl_validator.report_errors()[0]
        except Exception as err:
            raise err
        if ret is not None:
            return ret

    def on_global_state(self, operator):
        """ Qubit Memory : Invoke operator on global state

        Operator must be a qubit operator. After operator
        is applied to the global state, memory stores the
        newly generated global state.

        Arguments

        `operator` (`QubitOperator`) : operator must be an
        instance of `QubitOperator` class
        """
        try:
            if not isinstance(operator, QubitOperator):
                raise QubitMemoryError("Operator to be " +\
                        "applied on the global state in memory " +\
                        "is not a qubit operator.")
            new_global_state = operator.apply(self.get_global_state())
            self.set_global_state(new_global_state)
        except Exception as err:
            raise err

    def remove_register_metadata_by_rank(self, rank):
        """ Qubit Memory : Removes register metadata by rank

        Register's metadata is removed from the metadata list.

        NOTE Remove of a register's metadata must be triggered
        by change in global state or register list. This shall
        be a method only accessible to private methods.

        Arguments

        `rank` (`int`) : rank of the register of which metadata
        is to be removed from the list
        """
        if rank in range(0, self.number_of_registers):
            del self._metadata_list[rank]
        else:
            raise QubitMemoryError("No register found at " +\
                    "rank {}".format(rank))

    def remove_register_metadata_by_label(self, label):
        """ Qubit Memory : Remove register metadata by label

        NOTE Remove of a register's metadata must be triggered
        by change in global state or register list. This shall
        be a method only accessible to private methods.

        Arguments

        `label` (`str`) : a string, label of the register of which
        its metadata is to be removed from the list
        """
        if self.has_register_label(label):
            rank = self.get_rank_by_label(label)
            self.remove_register_metadata_by_rank(rank)
        else:
            raise QubitMemoryError("Register with label " +\
                    "'{}' wasn't found in memory.".format(label))
