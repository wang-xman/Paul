#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_instruction.partial_trace.instructions.py

PATH

[app_root]/quantum_instruction/partial_trace/instructions.py

INTRO

Partial trace instruction describes an partial trace
operation on a qubit state.

Two reference schemes can be used to reference qubits
to be traced out, namely, local reference and global
reference schemes. Local reference scheme refers to
a register or a range of qubits on that register.
Global reference scheme refers to a range of qubits
in a larger qubit state (global state) without any
reference to any register.

LOG

Updated on 01 October 2021 | Created on 13 August 2021
"""
from .errors import PartialTraceInstructionError
from .validators import PartialTraceInstructionDictValidator

_MODULE_LOCATION_ = 'quantum_instruction.partial_trace.instructions'


class PartialTraceInstruction:
    """ Partial trace operation instruction

    Two possible mutually exclusive reference schemes,
    local and global.

    Local reference scheme must have register, yet the
    global one must have global index range.

    ATTRIBUTES

    `self._internal_dict` (`dict`) : validated internal
    dictionary of quantum instruction

    `self.has_register` : property, verifies if instruction
    contains register; if `True`, then a local reference scheme;
    otherwise a global reference

    `self.has_local_index_range` : property, verifies if
    instruction contains local index range

    `self.has_global_index_range` : property, verifies if
    instruction has global index range

    `self.register` : property, returns label of register in
    the instruction

    `self.local_index_range` : property, returns local index
    range if instruction carries it

    `self.global_index_range` : property, returns global index
    range if instruction carries it
    """
    def __init__(self, instruc_dict):
        validator = PartialTraceInstructionDictValidator(
                instruc_dict=instruc_dict)
        if validator.is_valid:
            self._internal_dict = validator.validated_data()
        else:
            validator.raise_last_error()

    @property
    def has_register(self):
        ret = False
        if 'register' in self._internal_dict.keys():
            ret = True
        return ret

    @property
    def has_local_index_range(self):
        ret = False
        if self.has_register \
                and 'local_index_range' in self._internal_dict.keys():
            ret = True
        return ret

    @property
    def has_global_index_range(self):
        ret = False
        if not self.has_register \
                and 'global_index_range' in self._internal_dict.keys():
            ret = True
        return ret

    @property
    def register(self):
        ret = None
        if self.has_register:
            ret = self._internal_dict['register']
        else:
            raise PartialTraceInstructionError("Partial trace instruction " +\
                    "is in global reference scheme and is thus " +\
                    "carrying no register.")
        return ret

    @property
    def local_index_range(self):
        ret = None
        if self.has_local_index_range:
            ret = self._internal_dict['local_index_range']
        else:
            raise PartialTraceInstructionError("Partial trace instruction " +\
                    "carries no local index range.")
        return ret

    @property
    def global_index_range(self):
        ret = None
        if not self.has_register:
            ret = self._internal_dict['global_index_range']
        else:
            raise PartialTraceInstructionError("Partial trace is in " +\
                    "local reference scheme and is thus having no" +\
                    "global index range.")
        return ret
    