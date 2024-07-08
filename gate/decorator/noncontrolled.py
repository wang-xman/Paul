#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.decorator.noncontrolled.py

PATH

[app_root]/gate/decorator/noncontrolled.py

INTRO

Noncontrolled operator mixin class for decorator.

LOG

Updated on 22 September 2021 | Created on 07 September 2021
"""
from gate.base import  GateBaseError
from gate.enlarge_matrix.noncontrolled import enlarge_single_qubit_matrix

_MODULE_LOCATION_ = 'gate.decorator.noncontrolled'


class NoncontrolledOperatorMixin:
    """ Construct a non-controlled operator

    Constructs and returns a properly resized operator
    matrix suitale for the input (target) state.

    Applying operator matrix on input state (invocation),
    is delayed to the last moment determined by the caller.
    There are several different scenarios.

    [Prototype has full control `_handover_to_gate`]
    Gate prototype has its own `gate_apply()` method,
    indicating that prototype retains full control of
    operator matrix creation. In this case, control is
    handed over to the gate prototype immediately.
    This is a common scenario for gate acting on multiple
    qubits by default, especially when target bits are
    scattered in global state.

    [Direct operation `_noncontrolled_direct`]
    Gate prototype has no `gate_apply()` method, indicating
    that it needs decorator for constructing generic operator.
    If `input_state` has the same number of qubits (for both
    single- and multiple-qubit gates) or more number of qubits
    (for multiple-qubit gates) as declared, the `default_direct`
    method is invoked. A multiple-qubit state falls naturally
    in the scaenario where the noq of an input state is greater
    than the declared.

    [Enlarge operation `_noncontrolled_enlarge`]
    Gate prototype has no `gate_apply()` method, as the above.
    If `input_state` has a greater noq than the declared,
    `_noncontrolled_enlarge` method is invoked. A frequent use
    case is to apply single-qubit gate to multiple-qubit state.

    Method `operate` determines and launches the operation,
    and returns the resulting qubit state.

    Numeric wise, last two default operations are designed
    such that computationally expensive linear-algebra
    operations are delayed to the last step of invoking
    `QuantumOperator.apply()` method. One advantage of this
    design enables future parallelization of linear algebra
    subroutines only concerns the changes made on methods
    dealing with linear algebra.
    """
    def _handover_to_gate(self, *args, **params):
        """ Default Operator Mixin :: Handover to prototype

        Should prototype have the `gate_apply()` method,
        it immediately takes over the task of producing
        and returning an operator matrix.

        In this case, internal logic of constructing the
        required operator matrix is completely determined
        by the prototype. Decorator mainly verifies and
        validates arguments and parameters.
        """
        try:
            opargs, opkwargs = self.gate_prototype.validate_parameters(
                    self.gate_prototype.gate_apply, *args, **params)
            operator_matrix = \
                    self.gate_prototype.gate_apply(*opargs, **opkwargs)
            return operator_matrix
        except Exception as err:
            raise err

    def _noncontrolled_enlarge(self, *args, **params):
        """ Noncontrolled Operator Mixin :: Enlarge operator matrix

        Gate prototype has both `gate_matrix` method and
        parameters descriptor.

        Frequent Use Case. Enlarges a single-qubit gate for
        a multiple-qubit input state. However, resizing a
        multiple-qubit gate doesn't always have a common
        pattern to follow. (See multiple-qubit gate mixin.)

        Return

        `operator_matrix` (`SquareMatrix`) : resized
        (enlarged) operator matrix.
        """
        if 'target_index' not in params.keys():
            raise GateBaseError("Input state has more qubits " +\
                    "than the gate declares; a target index is " +\
                    "thus required. However, the required target " +\
                    "index is missing from invocation parameter " +\
                    "for gate {}.".format(self.alias))
        if not self.all_parameters['target_index'].validate(
                params['target_index']):
            raise GateBaseError("Target index provided to gate "+\
                    "{} ".format(self.alias) + "is not valid.")
        try:
            opargs, opkwargs = self.gate_prototype.validate_parameters(
                    self.gate_prototype.gate_matrix, *args, **params)
            default_matrix = \
                    self.gate_prototype.gate_matrix(*opargs, **opkwargs)
            # resized operator matrix
            # input state object is not required
            operator_matrix = enlarge_single_qubit_matrix(
                    number_of_qubits=params['input_state'].noq,
                    target_index=params['target_index'],
                    original_matrix=default_matrix)      
            return operator_matrix
        except Exception as err:
            raise err

    def _noncontrolled_direct(self, *args, **params):
        """ Noncontrolled Operator Mixin :: Direct

        Prototype has no `gate_apply` method. Per invocation,
        the prototype has both `gate_matrix` method and
        parameters descriptor.

        Frequent Use Case. Input state has exactly the same
        number of qubit as declared in prototype.

        Return

        `operator_matrix` (`SquareMatrix`) : resized
        (enlarged) operator matrix.
        """
        try:
            opargs, opkwargs = self.gate_prototype.validate_parameters(
                    self.gate_prototype.gate_matrix, *args, **params)
            operator_matrix = \
                    self.gate_prototype.gate_matrix(*opargs, **opkwargs)
            return operator_matrix
        except Exception as e:
            raise e

    def _noncontrolled_operator_matrix(self, *args, **params):
        """ Noncontrolled Operator Mixin :: Construct operator matrix

        Determines and returns the proper non-controlled
        operator matrix by invoking selectively one of
        the above three methods.

        There are three scenarios.

        [Gate prototype gains full control]
        Gate prototype has own `gate_apply()` method.
        In this case, gate prototype acquries the full
        control of gate operation. Operator construction
        is handed over to theprototype immediately.

        [Direct]
        Gate prototype has no `gate_apply()` method.
        The noq of input state is compatible with what
        gate declares. In this case, direct application
        of gate matrix on the input state is possible.
        This scenario is common for both single-qubit
        and multiple-qubit gate. For multiple-bit gate,
        in particular, the noq of the input state can be
        greater than the declared, as a multiple-qubit gate
        usually is designed to handle this situation:
        Multiple-qubit gate natually has at least two input
        indices which are already mapped to a multiple-qubit
        state.

        [Resize]
        Gate prototype has no `gate_apply()` method. But the
        noq of input state is greater than the declared noq.
        In this case, default gate matrix must be resized to
        fit the input state. Most common scenario is to apply
        a single-qubit gate to a multiple-qubit state.

        Return

        `operator_matrix` (`SquareMatrix`) : resized
        (enlarged) operator matrix.
        """
        operator_matrix = None
        # prototype takes over construction
        if getattr(self.gate_prototype, "gate_apply", False):
            try:
                operator_matrix = self._handover_to_gate(*args, **params)
            except Exception as err:
                raise err
        # prototype turns to decorator
        else:
            # validate input state from operation parameters
            if self.operation_parameters['input_state'].is_valid(
                        params['input_state']):
                # Direct : input state has the same noq
                # as the prototype declares
                if params['input_state'].noq == \
                        self.gate_prototype.minimal_number_of_qubits:
                    try:
                        operator_matrix = \
                                self._noncontrolled_direct(*args, **params)
                    except Exception as err:
                        raise err
                # Enlarge : input state has more noq than declared
                elif params['input_state'].noq > \
                        self.gate_prototype.minimal_number_of_qubits:
                    # for a single-qubit gate, enlarge is needed.
                    if self.gate_prototype.minimal_number_of_qubits == 1:
                        try:
                            operator_matrix = \
                                    self._noncontrolled_enlarge(*args, **params)
                        except Exception as err:
                            raise err
                    # otherwise, just go for direct as multiple-bit
                    # gate is designed for more-than-or-equal-to-declared
                    else:
                        try:
                            operator_matrix = \
                                    self._noncontrolled_direct(*args, **params)
                        except Exception as err:
                            raise err
                else:
                    raise GateBaseError("Input state has " +\
                            "less number of qubits than gate " +\
                            "{} requires. ".format(self.alias) +\
                            "Gate operation aborted.")
            else:
                raise GateBaseError("Input state provided " +\
                        "to gate {} ".format(self.alias) +\
                        "is not valid. Gate operation aborted.")
        return operator_matrix
