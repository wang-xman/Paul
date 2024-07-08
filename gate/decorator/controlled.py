#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.decorator.controlled.py

PATH

[app_root]/gate/decorator/controlled.py

INTRO

Controlled operator matrix mixin for decorator.
Two essential mixin classes.

LOG

Updated on 22 September 2021 | Created on 07 September 2021
"""
from linear_space.utils import minimum
from linear_space.algebra import matrix_product
from gate.parameter import QubitIndex
from gate.base import  GateBaseError
# essential enlarge functions
from gate.enlarge_matrix.controlled_kernel import kernel
from gate.enlarge_matrix.controlled_target_tuple import is_CISWAP_required, \
    control_index_swap, controlled_target_tuple, pre_CISWAP_matrix, \
    post_CISWAP_matrix


class ControlledTargetRange:
    """ Controlled Target Range mixin

    Controlled target range mixin deals with cases
    in which a continuous target range is provided.
    In this case, control index will not fall into
    the target range and control index swap maneuver
    is thus not required.

    Gate prototype must be able to construct an original
    operator matrix for the given target range.
    """
    def _controlled_target_range(self, *args, **params):
        """ Target range is provided

        A range of qubit indices is provided to decorator.
        Control list or index must not overlap or clash
        with target range.

        NOTE Input state is not passed to enlarge functions,
        only its metadata such as noq is.
        """
        operator_matrix = None
        opargs, opkwargs = self.gate_prototype.validate_parameters(
                self.gate_prototype.gate_matrix,
                *args, **params)
        original_matrix = self.gate_prototype.gate_matrix(*opargs, **opkwargs)
        # contruct operator matrix
        operator_matrix = kernel(
                number_of_qubits=params['input_state'].noq,
                control_list=params['control_list'],
                target_range=params['target_range'],
                original_matrix=original_matrix)
        return operator_matrix

    def _controlled_single(self, *args, **params):
        """ Controlled operator matrix for single-qubit gate

        Single qubit gate requires a `target_index` to work
        with. TODO Better use controlled target index.

        Both single- and multiple-controlled single-qubit gates,
        depending on invocation parameters.
        """
        operator_matrix = None
        # target index exists
        if 'target_index' in params.keys():
            target_range = [params['target_index'],params['target_index']]
            del params['target_index']
            params['target_range'] = target_range
            operator_matrix = self._controlled_target_range(*args, **params)
        # target index is missing
        else:
            raise GateBaseError("Failed to construct a controlled " +\
                    "operator using gate {}.".format(self.alias) +\
                    "Target index is missing.")
        return operator_matrix


class ControlledTargetIndex:
    """ Controlled Target Index mixin

    Controlled target index mixin manages cases where
    gate prototype only deals with discrete target
    index, thus the class name. For example, a prototype
    has the following gate matrix method,
        `def gate_matrix(self, alpha=None, beta=None, delta=None)`
    where all arguments are qubit indices.

    This case is more complex than target range, as it
    may require control-index swap (CISWAP) maneuver, as
    long as a control index is inside the target window.

    Core algorithm is to convert target indices into a target
    tuple and make use of utility function
        `controlled_target_tuple`
    to construct an operator matrix for the window state.
    """
    def _get_original_suite(self, **params):
        """ Controlled Target Index :: Returns original suite

        Original suite consists of `target_names`, a tuple of
        target index names; `target_tuple`, a tuple of target
        indices corresponding to the parameter at the same
        index in `params_names`; `control_list` is a list
        of control indices and their associated constrol state.

        Return

        A dictionary that consists of the following 3 keys:

        `target_names` (`tuple`) : a tuple of parameter names
        acquired from params dictionary; includes all parameters
        that are `QubitIndex`, but not for control

        `target_tuple` (`tuple`) : a tuple of target indices
        having one-to-one coorespondence with the target name
        in `targer_names`

        `control_list` (`list`) : is a list of control indices
        and their associated control state
        """
        target_names = ()
        target_tuple = ()
        for pn, pv in params.items():
            # parameter is a qubit index, but not control
            if not pn in ['control_index', 'control_list']:
                if isinstance(self.all_parameters[pn], QubitIndex):
                    target_names += (pn,)
                    target_tuple += (pv,)
        return {
            'target_names': target_names,
            'target_tuple': target_tuple,
            'control_list': params['control_list']
        }

    def _is_CISWAP_required(self, control_list=None, target_tuple=None):
        """ Controlled Target Index :: If CISWAP is required

        Return

        Either `True` or `False` should CISWAP maneuver is required.
        """
        return is_CISWAP_required(control_list=control_list,
                                  target_tuple=target_tuple)

    def _get_ciswaped_suite(self, **params):
        """ Controlled Target Index :: Return ciswaped suite

        Return

        Similar to orginal suite, a dictionary that consists of
        the following 3 keys:

        `target_names` (`tuple`) : a tuple of parameter names
        acquired from params dictionary; includes all parameters
        that are `QubitIndex`, but not for control

        `target_tuple` (`tuple`) : a tuple of target indices
        having one-to-one coorespondence with the target name
        in `targer_names`

        `control_list` (`list`) : is a list of control indices
        and their associated control state

        `swap_list` (`list`) : 
        """
        original_suite = self._get_original_suite(**params)
        # acquire controlled target index suite
        ciswaped_items = control_index_swap(
            control_list=original_suite['control_list'],
            target_tuple=original_suite['target_tuple'])

        return {
            'target_names': original_suite['target_names'],
            'target_tuple': ciswaped_items['target_tuple'],
            'control_list': ciswaped_items['control_list'],
            'swap_list': ciswaped_items['swap_list']
        }

    def _operator_matrix_without_CISWAP(self, *args, **params):
        """ Operator matrix without CISWAP

        Most important object is the target-window operator
        matrix. To create target window operator matrix, all
        target indices passed to prototype must be adjusted
        by the lowest index, meaning all target indices must
        be shifted by an amount of lowest index.
        """
        original_suite = self._get_original_suite(**params)
        index_shift = minimum(original_suite['target_tuple'])
        # prepare shifted params for target window
        target_window_params = {}
        for pn, pv in params.items():
            if pn in original_suite['target_names']:
                target_window_params[pn] = pv - index_shift
            else:
                target_window_params[pn] = params[pn]
        # validate and create target window operator matrix
        opargs, opkwargs = self.gate_prototype.validate_parameters(
            self.gate_prototype.gate_matrix,
            *args,
            **target_window_params)
        target_window_operator_matrix = \
                self.gate_prototype.gate_matrix(*opargs, **opkwargs)
        # controlled operator matrix
        operator_matrix = controlled_target_tuple(
            number_of_qubits=params['input_state'].noq,
            target_tuple=original_suite['target_tuple'],
            control_list=original_suite['control_list'],
            original_matrix=target_window_operator_matrix)
        return operator_matrix

    def _operator_matrix_with_CISWAP(self, *args, **params):
        """ Operator matrix with CISWAP maneuver """
        ciswaped_suite = self._get_ciswaped_suite(**params)
        # pack target with new value in a dictionary
        ciswapped_targets = dict(
            zip(ciswaped_suite['target_names'],ciswaped_suite['target_tuple']))
        new_parameters = {}
        # construct updated invocation parameters
        for pn, pv in params.items():
            if pn in ciswapped_targets.keys():
                new_parameters[pn] = ciswapped_targets[pn]
            elif pn == 'control_list':
                new_parameters[pn] = ciswaped_suite['control_list']
            else:
                new_parameters[pn] = pv
        # create operator matrix without CISWAP
        operator_matrix_without_CISWAP = \
            self._operator_matrix_without_CISWAP(*args, **new_parameters)
        # construct swap matrices
        # preciswap is before applying gate
        # postciswap is after applying gate
        pre_CISWAP = pre_CISWAP_matrix(
            params['input_state'].noq,
            swap_list=ciswaped_suite['swap_list'])
        post_CISWAP = post_CISWAP_matrix(
            params['input_state'].noq,
            swap_list=ciswaped_suite['swap_list'])
        return matrix_product(
            post_CISWAP,
            matrix_product(operator_matrix_without_CISWAP, pre_CISWAP))

    def _controlled_target_index(self, *args, **params):
        """ Target index is provided """
        operator_matrix = None
        # acquire original suite
        original_suite = self._get_original_suite(**params)
        # verify if CISWAP is needed
        if self._is_CISWAP_required(
                control_list=original_suite['control_list'],
                target_tuple=original_suite['target_tuple']):
            operator_matrix = \
                    self._operator_matrix_with_CISWAP(*args, **params)
        else:
            operator_matrix = \
                    self._operator_matrix_without_CISWAP(*args, **params)
        return operator_matrix


class ControlledOperatorMixin(ControlledTargetIndex, ControlledTargetRange):
    """ Controlled operator mixin

    Returns operator matrix, not transformed state. Application of
    a gate to the input state is delayed to `__call__` method in
    `as_gate` decorator.

    Target state wise, for both single- and multiple-qubit states.
    """
    def _controlled_operator_matrix(self, *args, **params):
        """ Controlled Operator Mixin : Controlled operation

        Verfiy and prepare gate and control arguments in the `params`.
        Note that upon invoking this method, arguments in params have
        been verified such that `input_state`, `control_index`, or
        `control_list` parameters are provided.

        Should a prototype has implemented `gate_apply()`, the control
        is handed over to this method to return an operator matrix.

        Otherwise, if the input state is a single qubit state,
        `self._controlled_single` is invoked; if the input is a
        multiple-qubit state, `self._controlled_multiple` is invoked.
        """
        operator_matrix = None
        # prototype takes over matrix creation
        if getattr(self.gate_prototype, "gate_apply", False):
            raise GateBaseError("Controlled operation on a " +\
                    "multiple-qubit gate that doesn't provide " +\
                    "gate matrix is yet to be implemented.")
        # prototype rolls back on decorator for controlled operation
        if self.gate_prototype.minimal_number_of_qubits == 1:
            try:
                operator_matrix = self._controlled_single(*args, **params)
            except Exception as err:
                raise err
        # gate is a multiple qubit gate,
        else:
            try:
                operator_matrix = self._controlled_target_index(*args, **params)
            except Exception as err:
                raise err
        return operator_matrix
