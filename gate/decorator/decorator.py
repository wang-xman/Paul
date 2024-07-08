#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.decorator.decorator.py

PATH

[app_root]/gate/decorator/decorator.py

INTRO

Gate decorator is a quantum operator. Hence a subclass
of `QuantumOperator`. Gate decorator returns an instance
of the decorator class, maintaining its bond to
`QuantumOperator`.

The most important function of a gate decorator is to
provide, for specific target (input) state, an operator
matrix. Information or data required by decorator to
construct suitable operator matrix must be minimal.
For example, a decorator doesn't need a target state
object in order to enlarge a single-qubit gate matrix;
it only needs to 'know' the number of qubits of the
target state and the index of the target bit. In this
package, such information or data is called 'metadata'.
Working with metadata avoids unnecessary usage of memory,
as a state vector with a large number of qubits consumes
a siginicant amount of memory. Making copy of it shall be
avoided as much as possible.
(See NOTE 2 in module `gate.prototype`)

Execution of a gate on target state is not an intrinsic
part of gate decorator, although appending such methods
isn't difficult.

Besides producing operator matrix, a decorator also
performs the following actions,

[1] verifies input and validates procedures;

[2] executes controlled operations, if required;

[3] validates output (resulting state), if required.

There are two types of gate operations, non-controlled
(otherwise known as default) and controlled operations.
A controlled operation requires at least one control
bit (namely single-controlled), or more than one control
bit (namely, multiple-controlled). Two possible states
are available for a control bit, '0' and '1', also known
as conditional state. By default, a control bit is often
conditional on state '1' to operate. In many situations,
however, the conditional state is set to '0'.

Controlled operation often creates entanglement, which
is one of the most powerful features of quantum mechanics
and is a common outcome of gate that operates on multiple
bits. Therefore, in order to accommodate entanglement,
controlled operator must see the control and the target
bits as a unified state, a single state merged using tensor
product. Qubits used as control bits are selected from this
state. This merged state is often called 'unified state'
or 'global state' in Qubit package.

Depending on the number of control bits, controlled
operation can be divided into single-controlled and
multiple-controlled ones. CNOT is a typical example of
single-controlled single-qubit operator. It has only
one control bit (conditional on state '1') and one
single-qubit flip gate (X). Toffoli gate is an example
of multiple-controlled single-qubit gate; it has two
control bits (both are conditional on 1) and one
single-qubit flip gate (X). Toffoli gate is also
referred to as controlled-CNOT.

Multiple-controlled multiple-qubit gate is not rare
but facing difficulty in physical realisation. (See
NOTE 1.) Numeric implementation is, however, viable.

CONTENT

`NoncontrolledOperatorMixin` - Mixin class for construction
of non-controlled/default gate operators

`ControlledSingleQubitOperatorMixin` - Mixin class for
construction of controlled SINGLE-qubit operator; can
be single or multiple control bits; the gate prototype
must be a single-qubit gate

`ControlledMultipleQubitOperatorMixin` - Mixin class
for construction of single- and multiple-controlled
MULTIPLE-qubit operator; the gate prototype must be
a multiple-qubit gate. (See NOTE 1).

`ControlledOperatorMixin` - Mixin class for construction
of controlled gate operator; combines the above two
controlled-operator mixins

`as_gate` - Primary quantum gate decorator. In principle,
the only decorator any developer need to use

NOTE

[1] According to Nielsen and Chuang, physical realisation
of a multiple-controlled multiple-qubit gate. This suggests
the controlled multiple qubit gate implemented in the
present module are more of numeric simulation experiment
than circuit implementation.

[2] As a convention, decorator classe is named using lower
case (or with dash) to highlight that it is not intended
to be instantiated as common class.

LOG

Updated on 18 September 2021 | Created on 16 November 2020
"""
from quantum_state import NullState, null_state
from qubit import QubitState
from quantum_operator import QuantumOperator

from gate.base import  GateBaseValidationError, GateBaseError, GateBaseValidator
from gate.parameter import InputQubitState, QubitIndex, ControlIndexList
from gate.prototype.base import GatePrototype

from .noncontrolled import NoncontrolledOperatorMixin
from .controlled import ControlledOperatorMixin


class DecoratorPrototypeValidator(GateBaseValidator):
    """ Validator prototype inside decorator constructor

    Gate prototype parameter must not clash with operation
    parameter. However, existence of parameter is verified
    in prototype validator.

    CONSTRUCTOR

    `decorator` (`QuantumOperator`) : decorator class

    `prototype` (`QuantumOperator`) : gate prototype class
    """
    error_class = GateBaseValidationError

    def __init__(self, decorator=None, prototype=None):
        super().__init__()
        self.validate(decorator, prototype)

    def validate(self, decorator, prototype):
        """ Main validation method """
        if not issubclass(prototype, GatePrototype):
            self.report_errors(message="Gate prototype "\
                    "{} ".format(prototype.__name__) +\
                    "is not a subclass of GatePrototype class.")
        # prevent parameter clash
        if getattr(prototype, 'parameters', False):
            for item in prototype.parameters.keys():
                if item in decorator.operation_parameters.keys():
                    self.report_errors("Gate prototype "\
                        "{} ".format(prototype.__name__) +\
                        "has a parameter named {} ".format(item) +\
                        "and it clashes with parameter of the same " +\
                        "name declared in the decorator.")


class ParametersControlledMatrixValidator(GateBaseValidator):
    """ Validate parameters for controlled operator matrix

    Used in `as_gate.__controlled_matrix()` method.
    """
    error_class = GateBaseError

    def __init__(self, alias=None, **params):
        super().__init__()
        self.validate(alias=alias, **params)

    def validate(self, alias=None, **params):
        """ Main validate method """
        # neither control list nor index, noncontrolled.
        if 'control_index' not in params.keys() \
                and 'control_list' not in params.keys():
            self.report_errors("Failed to contruct a " +\
                    "controlled gate operator using gate " +\
                    "{} due to the absence of ".format(alias) +\
                    "either a control index or control list.")
        # if control list exists
        elif 'control_list' in params.keys():
            # if control index is not absent
            if 'control_index' in params.keys():
                self.report_errors("Forbidden to "+\
                        "provide both control list and " +\
                        "control index to gate {}.".format(alias))
            # control index is missing
            else:
                # control list can not be None
                if params['control_list'] is None:
                    self.report_errors("Control list " +\
                            "provided to gate {}.".format(alias) +\
                            "is None.")
        # if no control list, control index must not be None
        else:
            if params['control_index'] is None:
                self.report_errors("Control index " +\
                        "provided to gate {}.".format(alias) +\
                        "is None.")


class as_gate(ControlledOperatorMixin, NoncontrolledOperatorMixin,
              QuantumOperator):
    """ Decorator class for all quantum gate

    Class decorator returns an instance of decorator class,
    not the prototype. Besides hardcoded ones, decorator
    enables dynamic creation of quantum gates on the go.

    Decorator is a subclass of quantum operator with
    `state_class` set to `QubitState`. Therefore, an instance
    of this decorator class is an instance of `QuantumOperator`.

    ATTRIBUTES

    `cls.state_class` (`QubitState`) : used by `QuantumOperator`
    to define the type of state the operator acts on

    `cls.operation_parameters` (`dict`) : operation parameter
    descriptor used by decorator; it helps the decorator verify
    if an argument in the prototype's descriptor clashes with
    the one declared herein

    `self.gate_prototype` (`GatePrototype`) : an instance of
    gate prototype class; also an instance of `QuantumOperator`,
    but without an internal matrix; NOTE gate prototype is a
    subclass of `QuantumOperator`, too

    `self.alias` (`str`) : alias defined in gate prototype

    `self.all_parameters` (`dict`) : parameter descriptor
    that combines ones of prototype and decorator's operation
    parameters

    `self.regulate_arguments(,*args,**params)`: method to
    regulate arguments and parameters passed to `__call__`
    and `ctrl` methods; it garantees invocation via keyword
    arguments, checks the existence of an input state, and
    verfies if a parameter has been declared

    `self.__non_controlled_matrix(,*args,**params)` : returns
    the operator matrix of a non-controlled operation

    `self.__controlled_matrix(,*args,**params)` : returns
    the operatoe matrix of a controlled operation; parameters
    passed in must contain `control_index` or `control_list`

    `self.global_operator_matrix(,*args,**params)` : returns
    the desired operator matrix for the global state

    `self.__call__(,*args,gate_matrix_only=None,**params)` :
    primary call dispatcher; depending on parameters passed in,
    it determines if a non-controlled or controlled operation
    shall be dispatched; argument `gate_matrix_only` determines
    if a gate matrix or a state is returned; it invokes
    `self.global_operator_matrix` to return an operator matrix

    `self.ctrl(,*args,**params)`: controlled operation

    `self.cop(,*args,**params)`: identical to `self.ctrl()`
    """
    state_class = QubitState
    # input state refers to the global state
    # input noq is the number of qubits of global state
    # target range refers to a range of qubits in the input state
    operation_parameters = {
        'input_state': InputQubitState(),
        'input_noq': int,
        'target_index': QubitIndex(),
        'target_range': list,
        'control_index': QubitIndex(),
        'control_list': ControlIndexList()
    }

    def __new__(cls, *args):
        """ Validate gate prototype

        Validation is via decorator prototype validator.
        """
        prototype = args[0]
        validator = DecoratorPrototypeValidator(cls, prototype)
        if not validator.is_valid:
            validator.raise_last_error()
        return super().__new__(cls)

    def __init__(self, *args):
        """ Decorator as_gate :: Initialiser

        Decorator stores an instance of prototype in
        attribute `self.gate_prototype`. All errors
        generated at instantiation of a gate prototype
        are thus captured here.

        Arguments

        `args` (`tuple`) : prototype class is stored
        in the first element

        Attributes

        `self.gate_prototype` (`GatePrototype`) : an
        instance of gate prototype; no internal
        matrix provided so far to this operator

        `self.alias` (`str`) : alias of the gate prototype

        `self.all_parameters` (`dict`) : a dictionary
        that is merged by parameters of the prototype and
        operation parameters defined in the decorator;
        this attribute allows a fast check if a parameter
        has been declared twice
        """
        try:
            # instantiates and stores an instance of gate prototype
            self.gate_prototype = args[0]()
            self.alias = self.gate_prototype.alias
            # all declared parameters that combines ones from gate
            # prototype and this decorator
            self.all_parameters = {**self.operation_parameters,
                                   **self.gate_prototype.parameters}
        except Exception as err:
            raise err

    def regulate_arguments(self, *args, **params):
        """ Decorator as_gate :: Regulate caller-provided arguments

        Prevent parameters from being passed in as
        positional arguments. Only keyword arguments
        are allowed for ultimate clarity.

        All arguments are verified against all parameter
        descriptors to rule out undeclared parameters.

        Parameter named `input_state` must be provided to the gate.
        """
        if len(params.keys()) == 0 and len(args) != 0:
            raise GateBaseError("For ultimate clarity, parameters "+\
                    "required to invoke gate {} ".format(self.alias) +\
                    "must all be packed into a dictionary. "+\
                    "Positional arugments are forbidden.")
        # must have an input state
        if 'input_state' not in params.keys():
            raise GateBaseError("Input state is not "\
                    "provided to gate {}. ".format(self.alias))
        # rule out undeclared arugments by searching all parameters
        for arg, _ in params.items():
            if arg not in self.all_parameters.keys():
                raise GateBaseError("Argument " +\
                        "{} passed to gate {} ".format(arg, self.alias) +\
                        "is not declared.")

    def _is_valid_state(self, state):
        """ Decorator as_gate :: verifies a generated state """
        ret = False
        if isinstance(state, (self.state_class, NullState)):
            ret = True
        return ret

    def _non_controlled_matrix(self, *args, **params):
        """ Decorator as_gate :: non-controlled operator matrix

        Returns non-controlled operator matrix.
        """
        operator_matrix = None
        try:
            # first regulate parameters
            self.regulate_arguments(*args, **params)
            # divert to mixin method
            # `NoncontrolledOperatorMixin._noncontrolled_operator_matrix()`
            operator_matrix = \
                    self._noncontrolled_operator_matrix(*args, **params)
        except Exception as err:
            raise err
        return operator_matrix

    def _controlled_matrix(self, *args, **params):
        """ Decorator as_gate :: controlled operator matrix

        Either `control index` or `control list` is required.

        As this method can be invoked directly, it must regulate
        arguments and verify if the control index or list is provided.
        """
        operator_matrix = None
        try:
            # first regulate parameters
            self.regulate_arguments(*args, **params)
            validator = \
                    ParametersControlledMatrixValidator(self.alias, **params)
            if validator.is_valid:
                if 'control_list' in params.keys():
                    operator_matrix = \
                        self._controlled_operator_matrix(*args, **params)
                elif 'control_index' in params.keys():
                    # convert control index into list
                    newparams = {}
                    for pn, pv in params.items():
                        if pn == 'control_index':
                            if 'control_state' not in params.keys():
                                newparams['control_list'] = [(pv, '1')]
                            else:
                                newparams['control_list'] = \
                                        [(pv, params['control_state'])]
                        else:
                            newparams[pn] = pv
                    operator_matrix = \
                            self._controlled_operator_matrix(*args, **newparams)
            else:
                validator.raise_last_error()
        except Exception as err:
            raise err
        return operator_matrix

    def global_operator_matrix(self, *args, **params):
        """ Decorator as_gate :: Returns global operator matrix

        Only returns the requested operator matrix.

        Depending on the value of `control_index` or `control_index`
        in parameters, this method returns a global operator matrix
        either for a non-controlled or controlled operation.

        NOTE Since this method returns only the requested operator
        matrix, not a transformed state, it is particularly useful
        when we need to merge several gate operator matrices into
        one before applying it to input state. For a given input
        state, this method actually can be used to construct a
        multiple-target gate operator matrix.

        Unittest of this method is
            unittest/controlled/test_global_operator_matrix.py
        """
        operator_matrix = None
        try:
            self.regulate_arguments(*args, **params)
            if not isinstance(params['input_state'], NullState):
                # neither control list nor index, non-controlled
                if 'control_index' not in params.keys() \
                        and 'control_list' not in params.keys():
                    operator_matrix = \
                            self._non_controlled_matrix(*args, **params)
                # either control list or control index, controlled
                else:
                    operator_matrix = self._controlled_matrix(*args, **params)
            else:
                raise GateBaseError("To construct a meaningful " +\
                        "operator matrix, input state must not be a " +\
                        "zero state.")
        except Exception as err:
            raise err
        return operator_matrix

    def __call__(self, *args, global_matrix_only=False, **params):
        """ Decorator as_gate :: Main __call__ method

        Earliest data entry point for gate operation.

        When the decorator instance (decorated gate) is invoked,
        this method is invoked and is the earliest entrance to
        all user-provided parameters.

        Two steps are executed sequentially. First, invoke
        `self.global_operator_matrix()` method to return a operator
        matrix. Second, apply, if request, the operator matrix to
        the input state to generate a output state.

        For clarity, all parameters must be passed in as a dictionary
        via keyword arguments. NOTE Positional arguments are forbidden.
        """
        ret = None
        operator_matrix = None
        try:
            self.regulate_arguments(*args, **params)
            if isinstance(params['input_state'], NullState):
                ret = null_state
            else:
                operator_matrix = self.global_operator_matrix(*args, **params)
                self.update_matrix(matrix=operator_matrix)
            # if only matrix is requested
            if global_matrix_only:
                ret = operator_matrix
            else:
                # Only here is input state object required.
                state = self.apply(params['input_state'])
                if self._is_valid_state(state):
                    ret = state
        except Exception as err:
            raise err
        return ret

    def ctrl(self, *args, global_matrix_only=False, **params):
        """ Decorator as_gate : alias controlled operation

        Returns either controlled operator matrix or a state after
        applying the operator.
        """
        ret = None
        try:
            operator_matrix = self._controlled_matrix(*args, **params)
            self.update_matrix(matrix=operator_matrix)
            # if only matrix is requested
            if global_matrix_only:
                ret = operator_matrix
            else:
                state = self.apply(params['input_state'])
                if self._is_valid_state(state):
                    ret = state
        except Exception as err:
            raise err
        return ret

    def cop(self, *args, global_matrix_only=False, **params):
        """ Decorator as_gate : alias to controlled operation

        Returns either operation matrix or a state.

        Identical to method `self.ctrl()`.
        """
        return self.ctrl(*args, global_matrix_only=global_matrix_only, **params)
