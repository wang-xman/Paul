#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_operation.partial_trace.operations.py

PATH

[app_root]/quantum_operation/partial_trace/operations.py

INTRO

Partial trace operation is frequently needed in both
measurement and other operations.

After partial trace, a reduced global density matrix
replaces the existing density matrix.

If a register has been traced out, it is removed from
the metadata list and is thus no longer accessible.

Validator mainly validates compatibility of instruction
(object) and target memory. Operation is a wrapper
object around quantum instruction.

NOTE In the current version (as per 25 August 2021),
only partial trace over a register is allowed. This
restriction is mainly due to the complication of
managing metadata list.

TODO Most urgent matters

[1] What happens to the global state?

LOG

Updated on 13 October 2021 | Created on 02 August 2021
"""
from density_matrix.density_matrix import QubitDensityMatrix
from measurement.partial_trace import partial_trace_out_index_range
from quantum_instruction.partial_trace import PartialTraceInstruction
from quantum_operation.base_operation import BaseOperation

from .errors import PartialTraceOperationError
from .validators import PartialTraceOperationValidator

_MODULE_LOCATION_ = 'quantum_operation.partial_trace.operations'


class PartialTraceOperation(BaseOperation):
    """ Partial trace operation

    Partial trace operation.
    """
    error_location = _MODULE_LOCATION_ + '.PartialTraceOperation'
    instruction_class = PartialTraceInstruction
    memory_validator_class = PartialTraceOperationValidator

    def _get_bitrange(self, memory):
        """ Partial Trace Operation : Determine bitrange

        An internal method to determine the bitrange used in
        partial trace function.
        """
        bitrange = None
        # local reference
        if self._instruction.has_register:
            # trace out entire register
            if not self._instruction.has_local_index_range:
                global_index_range_per_register = \
                        memory.get_global_index_range_by_label(
                            self._instruction.register)
                bitrange = [min(global_index_range_per_register),
                            max(global_index_range_per_register)]
            # trace out part of a register
            else:
                lower_global_index = memory.to_global_index(
                    min(self._instruction.local_index_range),
                    self._instruction.register
                )
                upper_global_index = memory.to_global_index(
                    max(self._instruction.local_index_range),
                    self._instruction.register
                )
                bitrange = [lower_global_index, upper_global_index]
        # global reference
        else:
            bitrange = [min(self._instruction.global_index_range),
                        max(self._instruction.global_index_range)]
        return bitrange

    def ready(self, memory):
        """ Partial Trace Operation : Check if operation is ready

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
        # check if global density matrix already exists
        if not memory.has_global_density_matrix:
            memory.set_global_density_matrix(
                    QubitDensityMatrix(state=memory.get_global_state()))

    def launch_in_socket(self, memory):
        """ Partial Trace Operation : Launcher for memory socket

        NOTE Only tracing out an entire register is allowed.
        After partial tracing, the register metadata is removed
        from the list. A reduced density matrix replaces the
        existing global density matrix.

        Arguments

        `memory` (`BaseMemory`): an active quantum memory on which
        the operation is launched
        """
        reduced_density_matrix = None
        try:
            self.ready(memory)
            reduced_density_matrix = partial_trace_out_index_range(
                    memory.get_global_density_matrix(),
                    self._get_bitrange(memory))
            memory.set_global_density_matrix(reduced_density_matrix)
            # remove register metadata
            memory.remove_register_metadata_by_label(self._instruction.register)
        except Exception as err:
            raise PartialTraceOperationError(str(err),
                    location=self.error_location) from err
        return reduced_density_matrix
