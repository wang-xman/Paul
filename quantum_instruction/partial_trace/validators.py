#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_instruction.partial_trace.validators.py

PATH

[app_root]/quantum_instruction/partial_trace/validators.py

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
from qubit.index_range import IndexRangeBoundValidator
from quantum_instruction.base import InstructionBaseValidator
from .errors import PartialTraceInstructionDictValidationError

_MODULE_LOCATION_ = 'quantum_instruction.partial_trace.validators'


class LocalReferenceValidator(InstructionBaseValidator):
    """ Validator for local reference scheme dict

    [Local reference - key `register`]

    A partial trace dictionary with key `register`, value of
    which must be the label of that register, indicates partial
    trace is performed on the designated register. One optional
    key `local_index_range` determines if the entire register is
    traced out. It stores a list of two integers, for example
        `[0,2]`
    defines the lowest and highest indices of the qubits to be
    partially traced out. If this key is non-empty and valid,
    only the qubits lying in that given range are traced out.
        {
            'register': required; label of the register to be
                traced out,
            'local_index_range': optional; for example, [1,3]
                means bits at indice 1, 2, 3 will be traced out;
                it must be provided a list of two integers.
        }
    A dict example for tracing out entire register `REG1` is
        {
            'register': 'REG1'
        }
    whereas the following example only traces out bits 1,2,3
    from this register
        {
            'register': 'REG1',
            'local_index_range': [1,3]
        }

    NOTE Not independently tested.
    """
    error_class = PartialTraceInstructionDictValidationError
    error_location = _MODULE_LOCATION_ + '.LocalReferenceValidator'
    accepted_keys = ['register', 'local_index_range']

    def __init__(self, instruc_dict=None):
        super().__init__()
        self._validated_reference = None
        self.validate(instruc_dict=instruc_dict)

    def validate(self, instruc_dict=None):
        """ Validate local reference """
        if not isinstance(instruc_dict['register'], str):
            self.report_errors("Value to key 'register' must " +\
                    "be a string variable referencing to a register.")
        elif 'local_index_range' not in instruc_dict.keys() \
                or instruc_dict['local_index_range'] is None:
            self._validated_reference = {
                'register': instruc_dict['register']
            }
        else:
            irvalidator = IndexRangeBoundValidator(
                bound=instruc_dict['local_index_range'])
            if irvalidator.is_valid:
                self._validated_reference = {
                    'register': instruc_dict['register'],
                    'local_index_range': instruc_dict['local_index_range']
                }
            else:
                self.report_errors(irvalidator.get_errors())

    def validated_data(self):
        return self._validated_reference


class GlobalReferenceValidator(InstructionBaseValidator):
    """ Validate global reference schemed dict

    [Global reference - key 'global_index_range']

    With key `global_index_range`, the partial trace is meant
    to be applied on the qubits in the global index range.
    A global index range may cover more than one register.

    A global index range is a list of two integers setting
    the lowest and highest indices. For example, dictionary
        {
            'global_index_range': [3,8]
        }
    means that qubits indexed globally on global state, from
    3 to (and include) 8 will be traced out.

    NOTE Not independently tested.
    """
    error_class = PartialTraceInstructionDictValidationError
    error_location = _MODULE_LOCATION_ + '.GlobalReferenceValidator'
    accepted_keys = ['global_index_range']

    def __init__(self, instruc_dict=None):
        super().__init__()
        self._validated_reference = None
        self.validate(instruc_dict=instruc_dict)

    def validate(self, instruc_dict=None):
        """ Validate global reference """
        irvalidator = IndexRangeBoundValidator(
                bound=instruc_dict['global_index_range'])
        if irvalidator.is_valid:
            self._validated_reference = {
                'global_index_range': instruc_dict['global_index_range']
            }
        else:
            self.report_errors(irvalidator.get_errors())

    def validated_data(self):
        return self._validated_reference


class PartialTraceInstructionDictValidator(InstructionBaseValidator):
    """ Validate partial-trace-operation instruction dict

    Partial trace is applicable to either a register or
    designated qubit in the global state (in memory).
    Therefore, two reference schemes are available, namely,
    local (register)-reference and global reference.

    The lead key to a partial trace dictionary is either
    `register` for local reference, or `global_index_range`
    for global reference, but NOT both.

    [Local reference - key `register`]
    A partial trace dictionary with key `register`, value of
    which must be the label of that register, indicates partial
    trace is performed on the designated register. One optional
    key `local_index_range` determines if the entire register is
    traced out. It stores a list of two integers, for example
        `[0,2]`
    defines the lowest and highest indices of the qubits to be
    partially traced out. If this key is non-empty and valid,
    only the qubits lying in that given range are traced out.
        {
            'register': required; label of the register to be
                traced out,
            'local_index_range': optional; for example, [1,3]
                means bits at indice 1, 2, 3 will be traced out;
                it must be provided a list of two integers.
        }
    A dict example for tracing out entire register `REG1` is
        {
            'register': 'REG1'
        }
    whereas the following example only traces out bits 1,2,3
    from this register
        {
            'register': 'REG1',
            'local_index_range': [1,3]
        }

    [Global reference - key 'global_index_range']
    With key `global_index_range`, the partial trace is meant
    to be applied on the qubits in the global index range.
    A global index range may cover more than one register.

    A global index range is a list of two integers setting
    the lowest and highest indices. For example, dictionary
        {
            'global_index_range': [3,8]
        }
    means that qubits indexed globally on global state, from
    3 to (and include) 8 will be traced out.
    """
    error_class = PartialTraceInstructionDictValidationError
    error_location = _MODULE_LOCATION_ +\
            '.PartialTraceInstructionDictValidator'

    def __init__(self, instruc_dict=None):
        super().__init__()
        self._validated_reference = None
        self.validate(instruc_dict=instruc_dict)

    def validate(self, instruc_dict=None):
        """ Main validate method """
        validator = None
        if 'register' not in instruc_dict.keys() \
                and 'global_index_range' not in instruc_dict.keys():
            self.report_errors("Partial trace operation " +\
                    "requires reference to either a register or " +\
                    "a range of qubit in the global state.")
        elif 'register' in instruc_dict.keys() \
                and 'global_index_range' not in instruc_dict.keys():
            validator = LocalReferenceValidator(instruc_dict=instruc_dict)
        elif 'register' not in instruc_dict.keys() \
                and 'global_index_range' in instruc_dict.keys():
            validator = GlobalReferenceValidator(instruc_dict=instruc_dict)
        else:
            self.report_errors("Partial trace operation " +\
                    "must have reference to either a register or " +\
                    "a range of qubit in the global state. " +\
                    "But not both simultaneuously.")
        if self.is_valid:
            if validator.is_valid:
                self._validated_reference = validator.validated_data()
            else:
                self.report_errors(validator.get_errors())

    def validated_data(self):
        return self._validated_reference
