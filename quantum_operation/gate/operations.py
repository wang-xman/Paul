#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.gate.operations.py

PATH

[app_root]/quantum_operation/gate/operations.py

INTRO

Gate operation applies gate operator on register or memory.
As gate is an instance of quantum operator, gate operation
is designed as a container object that wraps an instruction
and builds upon it a gate operator.

Instruction for gate operation has three sub-dictionaries to
describe Gate, Target and Control. (See gate-operation
instruction object for more information.)

In the current version, one gate operation describes only one
single-qubit gate operator. The target is thus required to be
a single qubit, too. Multiple-qubit target is in principle possible,
but the known difficulty in physical realisation in a near term
quantum computer puts it off from the current version.

Before applying operation on a state, there are two validations.
Primary validation validates user-provided operation dictionary
against the requirement. Memory validator validates operation
against an existing quantum memory for compatibility.

LOG

Updated on 02 October 2021 | Created on 12 July 2021
"""
from gate import single_qubit_gates as singles
from quantum_instruction.gate import GateInstruction
from quantum_operation.base_operation import BaseOperation

from .errors import GateOperationError
from .validators import GateOperationValidator

_MODULE_LOCATION_ = 'quantum_operation.gate.operations'


class GateOperationManager:
    """ Gate operation manager

    Implement launch method for operation class via a mixin.

    ATTRIBUTES

    `self.ready(, memory)` : check if an operationis ready;
    if not, raises errors

    `self.get_operator_matrix(, memory)` : returns an operator
    matrix compatible with the target memory

    `self.launch_in_socket(,memory)` : function to be invoked
    in memory `operation_socket` method
    """
    error_location = _MODULE_LOCATION_ + ".GateOperationManager"

    def ready(self, memory=None):
        """ Gate Operation Manager : Check if operation is ready

        Two checked are conducted. [1] Check operation - memory
        compatibility using memory validator class. [2] Check if
        memory has global state.

        Arguments

        `memory` (`BaseMemory`): an active quantum memory on which
        the operation is launched
        """
        memory_validator = self.memory_validator_class(
                instruction=self._instruction, memory=memory)
        if not memory_validator.is_valid:
            memory_validator.raise_last_error()
        if not memory.has_global_state:
            raise GateOperationError("Memory {} ".format(memory.label) +\
                    "has no global state formed. Operation aborted.",
                    location=self.error_location+".ready")

    def get_operator_matrix(self, memory):
        """ Gate Operation Manager : Returns operator matrix

        Returns an operator matrix, a `SquareMatrix` object,
        from the gate object.

        Arguments

        `memory` (`QubitMemory`) : a qubit memory instance on
        which gate operation is applied

        FIXME Lazy loading strategy. Try to make operator matrix
        or its creation process dependent on the total number of
        input state (i.e. metadata of state), not the state object.
        State vector (object) is only needed when actual computation
        takes place.
        """
        operator_matrix = None
        try:
            self.ready(memory)
            # prepare the gate operation parameters
            input_state = memory.get_global_state()
            target_index = memory.to_global_index(
                self.target_dict['local_index'],
                self.target_dict['register'])
            operation_parameters = {
                'input_state': input_state,
                'target_index': target_index
            }
            # merge parameters
            if 'parameters' in self.gate_dict \
                    and bool(self.gate_dict['parameters']):
                operation_parameters = {**operation_parameters,
                                        **self.gate_dict['parameters']}
            if self.has_control:
                control_list = []
                for el in self.control_dict['list']:
                    control_tuple = (
                        memory.to_global_index(
                            el['local_index'], el['register']), el['state'])
                    control_list.append(control_tuple)
                operation_parameters['control_list'] = control_list
            # renew global state in memory
            operator_matrix = self.gate.global_operator_matrix(
                    **operation_parameters)
        except Exception as err:
            raise err
        return operator_matrix

    def launch_in_socket(self, memory):
        """ Gate Operation Manager : Launch in (memory) socket

        Method to be invoked inside `memory.operation_socket`
        method. Operation readiness is checked and errors are
        raised if there is any.

        All actions on the memory and its global state must be
        implemented here. This includes, for example, manually
        remove from memory's metadata list a register that has
        been measured or partially traced out. Corresponding
        methods have already been implemented in memory object.

        Arguments

        `memory` (`BaseMemory`): an active quantum memory on which
        the operation is launched
        """
        try:
            operator_matrix = self.get_operator_matrix(memory)
            self.gate.update_matrix(matrix=operator_matrix)
            # renew global state in memory
            memory.set_global_state(
                    self.gate.apply(memory.get_global_state()))
        except Exception as err:
            raise err


class GateOperation(GateOperationManager, BaseOperation):
    """ Gate operation

    Gate operation wraps an instruction object and converts
    it into an gate operation object executable on a memory.
    (See instruction object for more explanation.)

    Validator stored in an operation verifies compatibility
    between instruction and memory. Therefore, validator
    used at operation stage is stored in a class attribute
        `cls.memory_validator_class`
    and is only needed when operation is executed.

    NOTE Current version allows only single-qubit target.
    Extention to multiple-qubit target state is onhold due
    to limitation in physical realisation.
    (See Nielsen and Chuang for more explanantion.)

    ATTRIBUTES

    [from `GateOperationManager`]

    `self.ready(, memory)` : checks if an operation is ready;
    if not, raises errors

    `self.get_operator_matrix(, memory)` : returns an operator
    matrix based on and compatible with the target memory

    `self.launch_in_socket(,memory)` : function to be executed
    inside memory's operation socket

    [own]

    `self.label` (`str`) : a string to label operation; default
    to `None`

    `self._instruction` (`GateOperationInstruction`) : validated
    instruction object

    `self.gate_dict` : property; returns validated gate subdict

    `self.gate` : property; return gate object

    `self.target_dict` : property; returns validated target subdict

    `self.has_control` : property; returns `True` (`False`) if
    operation is a controlled operation

    `self.control_dict` : property; returns validated control
    subdict
    """
    memory_validator_class = GateOperationValidator
    instruction_class = GateInstruction

    @property
    def gate_dict(self):
        """ Gate Operation :: Returns gate subdict """
        return self._instruction.gate_dict

    @property
    def gate(self):
        """ Gate Operation :: Returns gate object """
        if self._instruction.has_gate_instance:
            ret = self._instruction.gate_instance
        else:
            ret = singles.get(self._instruction.gate_alias)
        return ret

    @property
    def target_dict(self):
        """ Gate Operation :: Returns target subdict """
        return self._instruction.target_dict

    @property
    def has_control(self):
        """ Gate Operation :: Verify if operation is a controlled one """
        ret = False
        if self._instruction.has_control:
            ret = True
        return ret

    @property
    def control_dict(self):
        """ Gate Operation :: Returns control subdict """
        ret = None
        if self.has_control:
            ret = self._instruction.control_dict
        return ret
