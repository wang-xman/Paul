#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.measurement.operations.py

PATH

[app_root]/quantum_operation/measurement/operations.py

INTRO

Measurement operation applies measurement on register in
quantum memory.

To initialise a measurement operation, the dictionary must
be arranged according the following protocol. Two accepted
keys `register` and `state`.

[1] Required key `register`. With a string value being the
label of the register on which the measurement is performed.
By default, measurement is performed using computational
basis states compatible with the qubit stored in register.

[2] Optional key `state`. If `state` is None or absent,
measurement is performed in default basis, i.e. basis states
of the designated register. If a qubit state is given,
projective measurement is then performed in that qubit state.

Examples

[Measure a register in computational basis]
To measure an entire register labelled 'COMPREG' in its
computational basis
    {
        'register': 'COMPREG'
    }
is the required operation dictionary.

[Measure a register in designated state]
To measure a register labelled 'COMPUREG' using a given
qubit state, operation dictionary
    {
        'register': 'COMPREG',
        'state': QubitState instance
    }
where value to `state` is a `QubitState` instance.

NOTE Per the version 26 August 2021, only measurement
of an entire register is allowed. Therefore, instruction
dictionary contains the required key 'register' and an
optional key 'state'.

LOG

Updated on 02 October 2021 | Created on 01 August 2021
"""
from density_matrix.density_matrix import QubitDensityMatrix
from measurement.projective import projective_all, projective_on_state
from quantum_instruction.measurement import MeasurementInstruction

# from same package
from quantum_operation.partial_trace import partial_trace_on_memory
from quantum_operation.base_operation import BaseOperation

# from same subpack
from .errors import MeasurementOperationError
from .validators import MeasurementOperationValidator

_MODULE_LOCATION_ = 'quantum_operation.measurement.operations'


class MeasurementOperation(BaseOperation):
    """ Measurement operation

    Measurement operation class converts a JSON-like operation
    dictionary into a measurement operation object.

    Measurement operation dictionary has one required 'register'
    key and one optional 'state' key. If 'state' None or not given,
    the measurement is performed on all basis states of that register;
    if a qubit state is given, measurement is then performed use
    that qubit state.

    EXAMPLES

    [Measure a register in computational basis]
    To measure an entire register labelled 'COMPREG' in its
    computational basis
        {
            'register': 'COMPREG'
        }
    is the required operation dictionary.

    [Measure a register in designated state]
    To measure a register labelled 'COMPUREG' using a given
    qubit state, operation dictionary
        {
            'register': 'COMPREG',
            'state': QubitState instance
        }
    where value to `state` is a `QubitState` instance.
    """
    error_location = _MODULE_LOCATION_ + '.MeasurementOperation'
    memory_validator_class = MeasurementOperationValidator
    instruction_class = MeasurementInstruction

    def __registers_to_be_traced_out(self, memory):
        """ Measurement Operation : List of registers to be traced out
        """
        registers_to_be_traced_out = []
        for label in memory.get_all_labels():
            if label != self._instruction.register:
                registers_to_be_traced_out.append(label)
        return registers_to_be_traced_out

    def ready(self, memory):
        """ Measurement Operation : Check if operation is ready

        Two checks are conducted. [1] Check operation - memory
        compatibility using memory validator class. [2] Check if
        memory has global state and global density matrix.

        Arguments

        `memory` (`BaseMemory`): an active quantum memory on which
        the operation is launched
        """
        memory_validator = self.memory_validator_class(
                self._instruction, memory=memory)
        if not memory_validator.is_valid:
            raise memory_validator.report_errors()[0]
        if not memory.has_global_state:
            memory.form_global_state()
        # check if density matrix already exists
        if not memory.has_global_density_matrix:
            memory.set_global_density_matrix(
                    QubitDensityMatrix(state=memory.get_global_state()))

    def launch_in_socket(self, memory):
        """ Measurement Operation : Launcher for memory socket

        Registers that are not measured are traced out. Depending
        on if projection is on a specific state, returned probability
        is either a dictionary (projection on all basis) or a scalar
        (projection on the given state).

        Arguments

        `memory` (`BaseMemory`) : an active memory object
        """
        ret = None
        try:
            self.ready(memory)
            if memory.number_of_registers > 1:
                # trace out other registers
                for label in self.__registers_to_be_traced_out(memory):
                    partial_trace_on_memory({'register': label}, memory)
            # project all or on a state
            if self._instruction.has_state:
                ret = projective_on_state(memory.get_global_density_matrix(),
                                          self._instruction.state)
            else:
                ret = projective_all(memory.get_global_density_matrix())
        except Exception as err:
            raise MeasurementOperationError(str(err),
                    location=self.error_location) from err
        # returns probabilities
        return ret
