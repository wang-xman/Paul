#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.prototype.valdiators.py

PATH

[app_root]/gate/prototype/validators.py

INTRO

Validators dedicated to gate prototype validation.

LOG

Updated on 30 September 2021 | Created on 12 March 2021
"""
import warnings

# verifiers
from common.string import is_string, has_space, is_empty_string
from common.function import function_signature, is_function
from linear_space.number import is_integer

from gate.base import GateBaseValidator
from .errors import GatePrototypeValidationError

_MODULE_LOCATION_ = 'gate.prototype.validators'


class GatePrototypeValidator(GateBaseValidator):
    """ Validate gate prototype class

    Validates gate prototype class, not its instance.

    Basic design philosophy. If a gate prototype has
    implemented `gate_apply()` method, any operation
    shall be handed over to it. Implementing `gate_apply`
    method declares that the gate has its own rules for
    operation. In this case, gate decorator assists with
    argument verification and parameter validation.

    The opposite case is that `gate_apply` is absent,
    decorator must manage all default (including controlled)
    gate operations.

    Following this architecture, gate prototype class is
    validated against implementation of four properties.

    Alias. Required. Must have a class attribute named
    `alias` and it must be string type. Gate alias is
    used to identify a gate uniquely.

    Minimal number of qubits. Required property. Property
    `minimal_number_of_qubits` stores an integer value to
    specify the minimal number of qubits of input state.
    Should input state has less number of qubits, gate
    is imcompatible and shall report error.

    Parameter descriptor. Prototype must have a `parameters`
    dictionary that contains parameter names as keys; their
    correponding values must be `Parameter` instances. Value
    of this dictionary, however, can be empty to emphasis
    that this prototype carries no parameters.

    Default gate matrix. If `gate_apply` method is absent,
    an instance method `gate_matrix` must be implemented to
    return an instance of `SquareMatrix`. Matrix returned
    from this method must be applicable to any qubit state
    with the declared `minimal_number_of_qubits`.
    """
    error_class = GatePrototypeValidationError
    error_location = _MODULE_LOCATION_ + '.GatePrototypeValidator'

    def __init__(self, prototype=None):
        super().__init__()
        self.protoname = prototype.__name__
        self.validate(prototype=prototype)

    def validate_alias(self, prototype=None):
        """ Validate alias """
        # 4. must have an alias attribute
        if getattr(prototype, 'alias', False) is False:
            self.report_errors("Gate prototype " +\
                    self.protoname + " is missing a " +\
                    "required 'alias' attribute.")
        else:
            if is_string(getattr(prototype, 'alias')):
                alias = getattr(prototype, 'alias')
                # alias cannot be empty string
                if is_empty_string(alias):
                    self.report_errors("In gate prototype class " +\
                            self.protoname + " alias is an empty string.")
                # alias cannot contain space
                if has_space(alias):
                    self.report_errors("Alias of gate prototype " +\
                            self.protoname + " contains space.")
                #else:
                #    pass
            else:
                self.report_errors("Alias of gate prototype " +\
                        self.protoname + " is not of string type.")

    def validate_minimal_noq(self, prototype=None):
        """ Validate minimal number of qubits """
        # 3. must have 'minimal_number_of_qubits' property
        if getattr(prototype, 'minimal_number_of_qubits', False) is False:
            self.report_errors("Gate prototype class " +\
                    self.protoname +\
                    " is missing the required 'minimal_number_of_qubits' " +\
                    "property.")
        else:
            if not is_integer(getattr(prototype, 'minimal_number_of_qubits')):
                self.report_errors("In gate prototype class " +\
                        self.protoname + " minimal number of qubits isn't " +\
                        "an integer.")

    def validate_parameters(self, prototype=None):
        """ Validate parameters descriptor """
        # must have parameter descriptor dictionary;
        # it can be empty; NOTE empty dict is logically
        # false, meaning 'not {}' is 'True'
        if getattr(prototype, 'parameters', False) is False:
            self.report_errors("Gate prototype class " +\
                    self.protoname +\
                    " doesn't have the required 'parameters' " +\
                    "decription dictionary.")
        else:
            # if not dictionary, error
            if not isinstance(getattr(prototype, 'parameters'), dict):
                self.report_errors("Parameter description of " +\
                        "gate prototype " + self.protoname + \
                        " is not a dictionary.")

    def validate_gate_matrix(self, prototype=None):
        """ Validate gate matrix and gate apply """
        # 2. if no 'gate_apply()', then must have a method
        # gate_matrix() to return a square matrix
        if getattr(prototype, 'gate_apply', False) is False:
            if getattr(prototype, 'gate_matrix', False) is False:
                self.report_errors("As gate prototype " + \
                        self.protoname +\
                        " has no 'gate_apply' method, a method " +\
                        "named 'gate_matrix' must be implemented.")
            # gate_matrix must be a method
            else:
                if not is_function(getattr(prototype, "gate_matrix")):
                    self.report_errors("Gate prototype " + \
                        self.protoname +\
                        " has 'gate_matrix' attribute, but it is not a " +\
                        "function.")
        else:
            # if gate_apply exists, it must be a method
            if not is_function(getattr(prototype, "gate_apply")):
                self.report_errors("Gate prototype " + \
                        self.protoname +\
                        " has 'gate_apply' attribute, but it is not a "\
                        "function.")

    def validate(self, prototype=None):
        """ Main validate method """
        self.validate_alias(prototype=prototype)
        self.validate_minimal_noq(prototype=prototype)
        self.validate_parameters(prototype=prototype)
        self.validate_gate_matrix(prototype=prototype)


class GatePrototypeMethodSignatureValidator(GateBaseValidator):
    """ Validate gate method signature

    Used by `GatePrototype` to verify signature of
    a gate method.

    See `GatePrototype.verified_signature()` for more
    detailed explanantion.
    """
    error_class = GatePrototypeValidationError
    error_location = _MODULE_LOCATION_ +\
            '.GatePrototypeMethodSignatureValidator'

    def __init__(self, prototype, gate_method):
        super().__init__()
        self.prototype = prototype
        self.validated_signature = None
        self.validate(gate_method)

    def validate(self, gate_method):
        # signature is a dictionary with two keys 'args' and 'kwargs'
        signature = function_signature(gate_method)
        # parameter names in signature
        paramnames = list(signature['args']) + list(signature['kwargs'].keys())
        # parameter names declared in parameter descriptor
        declared_parameters = list(self.prototype.parameters.keys())
        # check all arguments are defined in parameters descriptor
        for pn in paramnames:
            if pn not in declared_parameters:
                self.report_errors("In prototype class " +\
                        self.prototype.alias + " argument {} ".format(pn) +\
                        "in method {} ".format(gate_method.__name__) +\
                        "is not declared in the parameter descriptor.")
        if self.is_valid:
            self.validated_signature = signature

    def validated_data(self):
        return self.validated_signature


class GatePrototypeMethodParametersValidator(GateBaseValidator):
    """ Validate gate method and parameters

    Validator used by gate prototype to validate
    gate method and associated parameters.

    See `GatePrototype.validate_parameters()` for
    detailed explanation.
    """
    error_class = GatePrototypeValidationError
    error_location = _MODULE_LOCATION_ +\
            '.GatePrototypeMethodParametersValidator'

    def __init__(self, prototype, gate_method, **params):
        super().__init__()
        self._validated_opargs = None
        self._validated_opkwargs = None
        self.prototype = prototype
        signature_validator = \
                GatePrototypeMethodSignatureValidator(prototype, gate_method)
        if signature_validator.is_valid:
            self.signature = signature_validator.validated_data()
        else:
            self.report_errors(message=signature_validator.get_errors())
        self.paramskeys = params.keys()
        self.validate(gate_method, **params)


    def validate_args(self, gate_method, **params):
        """ Validate positional arguments """
        opargs = ()
        # validate positional args in signature
        for arg in self.signature['args']:
            # value provided by the caller
            if arg in self.paramskeys:
                # if arg has been declared in prototype, then validate it
                if arg in self.prototype.parameters.keys():
                    # validate each parameter
                    # only declared and valid parameter is selected
                    if self.prototype.parameters[arg].validate(params[arg]):
                        opargs += (params[arg],)
                else:
                    self.report_errors("Positional argument " +\
                            arg + " provided to invoke " +\
                            "method {} of ".format(gate_method.__name__) +\
                            "gate {} ".format(self.prototype.alias) +\
                            "is undeclared.")
            # if value is not provided by caller
            else:
                # a required parameter must have a default value
                if self.prototype.parameters[arg].is_required:
                    dv = self.prototype.parameters[arg].default_value
                    opargs += (self.prototype.parameters[arg].default_value,)
                    warnings.warn("In gate {}, ".format(self.prototype.alias) +\
                            "parameter {} ".format(arg) + "falls back on "+\
                            "its default value {}.".format(dv))
        if self.is_valid:
            self._validated_opargs = opargs

    def validate_kwargs(self, gate_method, **params):
        """ Validate keyword arguments """
        opkwargs = {}
        # validate parameter values for kwargs
        for kwarg in self.signature['kwargs'].keys():
            if kwarg in self.paramskeys:
                # if kwargs has been declared
                if kwarg in self.prototype.parameters.keys():
                    # validate each parameter value
                    if self.prototype.parameters[kwarg].validate(params[kwarg]):
                        opkwargs[kwarg] = params[kwarg]
                else:
                    self.report_errors("Keyword argument " +\
                            kwarg + " provided to invoke " +\
                            "method {} of ".format(gate_method.__name__) +\
                            "gate {} ".format(self.prototype.alias) +\
                            "is undeclared.")
            else:
                if self.prototype.parameters[kwarg].is_required:
                    dv = self.prototype.parameters[kwarg].default_value
                    opkwargs[kwarg] =\
                            self.prototype.parameters[kwarg].default_value
                    warnings.warn("In gate {}, ".format(self.prototype.alias) +\
                            "parameter {} uses its default ".format(kwarg) +\
                            " value {}.".format(dv))
        if self.is_valid:
            self._validated_opkwargs = opkwargs

    def validate(self, gate_method, **params):
        """ Main validation method """
        self.validate_args(gate_method, **params)
        self.validate_kwargs(gate_method, **params)

    def validated_data(self):
        return {
            'args': self._validated_opargs,
            'kwargs': self._validated_opkwargs
        }
