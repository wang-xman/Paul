#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

quantum_flow.quantum_flow.quantum_flow.py

PATH

[app_root]/quantum_flow/quantum_flow/quantum_flow.py

INTRO

Quantum operation flow (quantum flow or simply flow), is a
sequence of quantum operations.

In a gate-bases quantum computer, a flow executes operations
- transformation via application of quantum gates - on a memory,
along the direction of time evolution.

Viewed from the perspective of algorithm, a flow is equivalent to
executing algorithm steps; in a quantum circuit, these steps are
quantum operations applied on a quantum memory by quantum gates.

Here, flow object store a operations in an internal list. Index of
each operation in the list is referred to as its rank; operation
with a lower rank is executed earlier.

LOG

Updated on 02 October 2021 | Created on 26 August 2021
"""
from linear_space.algebra import matrix_product
from quantum_operator import QubitOperator

from .errors import QuantumFlowError
from .base_flow import BaseQuantumFlow

_MODULE_LOCATION_ = 'quantum_flow.quantum_flow.quantum_flow'


class QuantumFlow(BaseQuantumFlow):
    """ Quantum Flow

    Quantum flow object intended to applied to quantum memory.

    ATTRIBUTES

    `self.unified_matrix(, memory)` : constructs and returns a unified
    operator matrix applicable to global state in the given memory

    `self.as_unified_operator(,memory)` : returns and `QubitOperator`
    instance that is compatible with the global state in the user
    provided memory

    `self.ready(,memory)` : verifies if flow and memory are ready

    `self.launch(,memory)` : executes operation sequence in the
    designated memory
    """
    error_location = _MODULE_LOCATION_ + '.QuantumFlow'

    def unified_matrix(self, memory):
        """ Quantum Flow : Construct a unified operator matrix

        Constructs and returns a unified operator matrix using all
        operations in the sequence.

        FIXME What happens if one or more operations are partial
        trace or measurement?

        NOTE Construction of unified matrix involves a chained matrix
        product, which presumably consumes most of computational time.
        This is where parallelisation is needed.
        """
        unified_matrix = None
        if not self.is_empty:
            unified_matrix = \
                    self.get_operation_by_rank(0).get_operator_matrix(memory)
            if self.number_of_operations > 1:
                for rank in range(1, self.number_of_operations):
                    opmat = self.get_operation_by_rank(rank).get_operator_matrix(memory)
                    if unified_matrix.ncols == opmat.ncols \
                            and unified_matrix.nrows == opmat.nrows:
                        unified_matrix = matrix_product(opmat, unified_matrix)
                    else:
                        raise QuantumFlowError("Failed to construct " +\
                                "unified operator matrix due to mismatch " +\
                                "in operator matrices.",
                                location=self.error_location+'.unified_matrix')
        else:
            raise QuantumFlowError("Failed to construct unified " +\
                    "operator matrix due to empty operation sequence.",
                    location=self.error_location+'.unified_matrix')
        return unified_matrix

    def as_unified_operator(self, memory):
        """ Quantum Flow : Construct a quantum operator

        Constructs and returns a quantum operator object for
        the target memory.

        Return

        A qubit operator object.
        """
        return QubitOperator(matrix=self.unified_matrix(memory))

    def ready(self, memory):
        """ Quantum Flow : Check if flow and memory are ready """
        if self.is_empty:
            raise QuantumFlowError(
                    "Flow is empty.", location=self.error_location+'.ready')
        if memory is None:
            raise QuantumFlowError("Operation flow must be " +\
                    "executed on an active quantum memory.",
                    location=self.error_location+'.ready')
        if not memory.has_global_state:
            memory.form_global_state()

    def launch_on_memory(self, memory):
        """ Quantum Flow : Execute operation sequence on memory

        Launches operations on the target memory by sequentially
        passing operations to memory's operation socket.
        """
        try:
            ret = None
            self.ready(memory)
            for _ , operation in enumerate(self.get_sequence()):
                ret = memory.operation_socket(operation)
            if ret is not None:
                return ret
        except Exception as err:
            raise err

    def launch_on_global_state(self, memory):
        """ Quantum Flow : Execute unified operator on global state

        Passes unified operator to `memory.on_global_state()`
        method. Unified operator is applied to the global state.

        This method is designed for using the flow as a unified
        operator.

        TODO What happens if one operation is a partial trace or
        measurement and is thus having no operator?
        """
        ret = None
        try:
            self.ready(memory)
            ret = memory.on_global_state(self.as_unified_operator(memory))
        except Exception as err:
            raise err
        if ret is not None:
            return ret
