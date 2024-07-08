#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_memory.managers.py

PATH

[app_root]/quantum_memory/managers.py

INTRO

Register and index managers for memory.

Both managers are embedded into memory via mixin.

CONTENT

`RegisterMetadataManager` - Mixin class that provides
methods on managing register metadata within a memory

`IndexManager` - Mixin class that tracks and maps qubit
indices in a particular register

LOG

Updated on 24 August 2021 | Created on 30 July 2021
"""
from common.string import is_string
from linear_space.number import is_integer

from .errors import RegisterMetadataManagerError, IndexManagerError

_MODULE_LOCATION_ = 'quantum_memory.managers'


class RegisterMetadataManager:
    """ Register metadata manager mixin

    Register metadata manager enters a memory class as mixin.

    Register metadata manager manages the metadata of registers,
    not states stored in registers. It interacts with host
    (qubit) memory mainly via `get_register_metadata_list()`
    method.

    ATTRIBUTES

    `self.get_all_labels()` : returns a list of register labels

    `self.has_register_label(, label)`: returns `True` (`False`)
    if a register of given label is (not) in metadata list

    `self.get_rank_by_label(,label)` : returns rank of a register
    by its label

    `self.get_label_by_rank(,rank)` : returns label of a register
    by its rank (in metadata list)

    `self.get_register_metadata_by_label(,label)` : returns metadata
    of a register by its label

    `self.get_register_metadata_by_rank(,rank)` : returns metadata
    of a register by its rank

    `self.get_noq_by_label(,label)` : returns number of qubits of
    the register determined by the given label

    `self.get_noq_by_rank(,rank)` : returns number of qubits of
    the register determined by the given rank
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.RegisterMetadataManager'

    def get_all_labels(self):
        """ Register Manager : Returns register labels as a list

        Returns

        A list of register labels. Order of labels in the list
        reflects the rank of register. If memory is empty,
        the list is empty.
        """
        existing_labels = []
        if self.has_register:
            existing_labels = \
                    [reg.label for reg in self.get_register_metadata_list()]
        return existing_labels

    def has_register_label(self, label):
        """ Register Manager : Verifies if a register label exists

        Returns

        `True` (`False`) if a register with the given label exists
        in the memory.
        """
        ret = False
        if is_string(label):
            if label in self.get_all_labels():
                ret = True
        return ret

    def get_rank_by_label(self, label):
        """ Register Manager : Returns rank of a register by its label

        Returns

        `rank` (`int`) : rank of a register in the metadata list

        If label can't be found, an error will be raised.
        """
        rank = None
        if label in self.get_all_labels():
            for i in range(0, self.number_of_registers, 1):
                if self.get_register_metadata_list()[i].label == label:
                    rank = i
        else:
            raise RegisterMetadataManagerError("Register with label " +\
                    "'{}' ".format(label) + "cannot be found in memory.",
                    location=self._ERROR_LOCATION_+'.get_rank_by_label')
        return rank

    def get_label_by_rank(self, rank):
        """ Register Manager : Returns a register label by its rank

        Returns

        `label` (`str`) : label of the register at given rank

        If the given label can't be found, an error is raised.
        """
        label = None
        if is_integer(rank):
            if rank in range(0, self.number_of_registers):
                label = self.get_register_metadata_list()[rank].label
            else:
                raise RegisterMetadataManagerError("Register " +\
                        "rank '{}' is out of ".format(rank) +\
                        "the memory range. Failed to provide the " +\
                        "corresponding label of the register.",
                        location=self._ERROR_LOCATION_+'.get_label_by_rank')
        else:
            raise RegisterMetadataManagerError(message="Register rank used " +\
                    "to retrieve its label is not an integer.",
                    location=self._ERROR_LOCATION_+'.get_label_by_rank')
        return label

    def get_register_metadata_by_label(self, label):
        """ Register Manager : Returns metadata of a register by label

        Using register label to return a dictionary contains
        the metadata about the designated register.

        Return

        `metadata_dict` (`dict`) : metadata dictionary of the register
        with the given label
        """
        metadata_dict = None
        if self.has_register_label(label):
            for i in range(0, self.number_of_registers, 1):
                if self.get_register_metadata_list()[i].label == label:
                    metadata_dict = self.get_register_metadata_list()[i]
        else:
            raise RegisterMetadataManagerError("Register with label " +\
                    "'{}' ".format(label) + "does not exist in." +\
                    "register list in memory." +\
                    "Failed to collect register metadata.",
                    location=self._ERROR_LOCATION_+\
                            '.get_register_metadata_by_label()')
        return metadata_dict

    def get_register_metadata_by_rank(self, rank):
        """ Register Manager : Returns metadata of a register by rank

        Return

        `metadata_dict` (`dict`) : metadata dictionary of the register
        with the given label
        """
        metadata_dict = None
        try:
            label = self.get_label_by_rank(rank)
            metadata_dict = self.get_register_metadata_by_label(label)
        except Exception as err:
            raise RegisterMetadataManagerError(str(err),
                    location=self._ERROR_LOCATION_+\
                            '.get_register_metadata_by_rank')
        return metadata_dict

    def get_noq_by_label(self, label):
        """ Register Manager : Returns noq of a register by label

        Return

        `noq` (`int`) : number of qubits in the requested register
        """
        noq = None
        try:
            metadata = self.get_register_metadata_by_label(label)
            noq = metadata.noq
        except Exception as err:
            raise RegisterMetadataManagerError(str(err),
                    location=self._ERROR_LOCATION_+'.get_noq_by_label')
        return noq

    def get_noq_by_rank(self, rank):
        """ Register Manager : Returns noq of a register by its rank

        Return

        `noq` (`int`) : number of qubits in the requested register
        """
        noq = None
        try:
            noq = self.get_noq_by_label(self.get_label_by_rank(rank))
        except Exception as err:
            raise RegisterMetadataManagerError(str(err),
                    location=self._ERROR_LOCATION_+'.get_noq_by_rank')
        return noq


class IndexManager:
    """ Memory index manager mixin

    Index manager is embedded into a memory via mixin.

    ATTRIBUTES

    `self.global_index_range()`: returns the index range of the
    global state formed by all qubit states in the registers

    `self.to_global_index(, local_index, label)`: returns the global
    index of a qubit in the register with label given by `label`;
    argument `local_index` is the index of the qubit with respect
    to the register

    `self.to_local_index(, global_index)`: returns the local index
    and the associated register label

    `self.get_local_index_range_by_label(,label)` : returns the
    local index range of a register; merely a shortcut to access
    the `local_index_range` value in its metadata

    `self.get_global_index_range_by_label(, label)`: returns the
    global index range of a register that is identified by `label`;
    the global index range refers to the range with respect to
    the global state

    `self.get_global_index_range_by_rank(, rank)`: returns the index
    range of a register that is identified by `rank` in the register
    list; this method assumes the caller knows the index (in register
    list) of the intended register

    `self.get_global_index_range_first_register()`: returns the global
    index range of the FIRST register

    `self.get_global_index_range_last_register()`: returns the global
    index range of the LAST register
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.IndexManager'

    def global_index_range(self):
        """ Index Manager : Return global index range of memory

        Qubit index range of the global state in the memory.
        This method is understood as 'global index range of the
        global state'.

        Returns

        A range object. For example, if the global index is from
        0 to 10, the returned range object is `range(0, 11, 1)`
        """
        accum_noq = 0
        for i in range(0, self.number_of_registers, 1):
            accum_noq += self.get_noq_by_rank(i)
        return range(0, accum_noq, 1)

    def to_global_index(self, local_index, label):
        """ Index Manager : Returns global index of a bit

        Converts a local index into a lobal one. A local index is the
        index of a qubit in one register.

        Arguments

        `local_index` (`int`): an integer the represents index of a
        qubit in the given register

        `label` (`str`): the label of the register where the qubit is
        indexed

        Return

        `global_index` (`int`) : index of designated qubit in the
        global state
        """
        accummulated_noq = 0
        global_index = 0
        # register with given label non-existent
        if not self.has_register_label(label):
            raise IndexManagerError("Register with label " +\
                    "'{}' ".format(label) +\
                    "doesn't exist in the memory.",
                    location=self._ERROR_LOCATION_+'.to_global_index')
        # all good
        for i in range(0, self.number_of_registers, 1):
            if self.get_label_by_rank(i) != label:
                accummulated_noq += self.get_noq_by_rank(i)
            else:
                if local_index in \
                        self.get_register_metadata_by_rank(i).local_index_range:
                    global_index = accummulated_noq + local_index
                else:
                    raise IndexManagerError("Local index " +\
                            "{}".format(local_index) + " is outside " +\
                            "the range of register {} ".format(label),
                            location=self._ERROR_LOCATION_+'.to_global_index')
        return global_index

    def to_local_index(self, global_index):
        """ Index Manager : Returns the local index of a qubit

        Converts a global index into a local index in a register.
        Local index is the index in a register and it starts
        from 0 and its maximum is (noq - 1).

        Arguments

        `global_index` (`int`): the global index (of qubit) that
        is to be mapped to a register and the associated local
        index in that register

        Return

        A dictionary that has two keys,
            {
                'label': register label,
                'local_index': local index in the register
            }
        """
        local_index = None
        label = None
        ret = None
        accum_noq = 0
        if not global_index in self.global_index_range():
            raise IndexManagerError('Global index is out of range',
                location=self._ERROR_LOCATION_+'.to_local_index')
        for i in range(0, self.number_of_registers, 1):
            current_upper_noq = accum_noq + self.get_noq_by_rank(i)
            if accum_noq <= global_index <= current_upper_noq - 1:
                local_index = global_index - accum_noq
                label = self.get_label_by_rank(i)
            accum_noq = current_upper_noq
        if not local_index is None:
            ret = {
                'label': label,
                'local_index': local_index
            }
        else:
            raise IndexManagerError("Index {}".format(global_index) +\
                    " is outside the available global index range of " +\
                    "quantum memory {}. ".format(self.label) +\
                    "Failed to find a local index in associated register.",
                    location=self._ERROR_LOCATION_+'.to_local_index')
        return ret

    def get_local_index_range_by_label(self, label):
        """ Index Manager : Returns local index range of a register

        Local index range reflects the total number of qubits in a
        register. For example, for a register of 3 qubits, its local
        index range is range(0, 3), irrespective of the total number
        of qubits in memory.

        Register metadata has a key `local_index_range`. This method
        merely returns that value.

        Argument

        `label` (`str`) : the label used to identify a register

        Returns

        A range object. For example, for a register of 3 qubits,
        its local index range is `range(0, 3)`.
        """
        local_index_range = None
        try:
            local_index_range = \
                self.get_register_metadata_by_label(label).local_index_range
        except Exception as err:
            raise IndexManagerError(str(err),
                    location=self._ERROR_LOCATION_+\
                            '.get_local_index_range_by_label')
        return local_index_range

    def get_global_index_range_by_label(self, label):
        """ Index Manager : Returns global index range for a register

        Global index range of a register is the index range of its
        qubits in the GLOBAL state.

        For example, in a memory with registers
            `[Reg1('010'), Reg2('11'), Reg3('00')]`
        the index range of register Reg2 is, in a list,
            `[3, 4]`
        or in a range object
            `range(3, 5, 1)`

        As long as there is no empty register(s), the index range of
        a register can always be determined its rank.

        Argument

        `label` (`str`): the label used to identify a register

        Return

        A range object. For the example above, returns `range(3, 5, 1)`.
        """
        index_range = []
        accummulated_noq = 0
        if label in self.get_all_labels():
            for i in range(0, self.number_of_registers, 1):
                #if self.get_register_list()[i].label != label:
                if self.get_label_by_rank(i) != label:
                    accummulated_noq += self.get_noq_by_rank(i)
                else:
                    index_range.append(accummulated_noq)
                    index_range.append(
                        accummulated_noq + self.get_noq_by_rank(i) - 1)
        else:
            raise IndexManagerError("Register with requested " +\
                    "label '{}' ".format(label) + "doesn't exist in " +\
                    "the memory.",
                    location=self._ERROR_LOCATION_+'.get_index_range')
        return range(index_range[0], index_range[1] + 1, 1)

    def get_global_index_range_by_rank(self, rank):
        """ Index Manager : Returns global index range by rank

        See `self.get_global_index_range_by_label` for explanation
        on the definition of global index range.

        Arguments

        `rank` (`int`): rank of register

        Return

        `global_index_range` (obj `range`) : global index range of
        the register
        """
        global_index_range = None
        try:
            # invoke RegisterManager.get_label_by_rank()
            global_index_range = self.get_global_index_range_by_label(
                self.get_label_by_rank(rank))
        except Exception as err:
            raise IndexManagerError(str(err), location=self._ERROR_LOCATION_+\
                    '.get_global_index_range_by_rank')
        return global_index_range

    def get_global_index_range_first_register(self):
        """ Index Manager : Returns index range of the first register """
        return self.get_global_index_range_by_rank(0)

    def get_global_index_range_last_register(self):
        """ Index Manager : Returns index range of the last register """
        return self.get_global_index_range_by_rank(self.number_of_registers - 1)
