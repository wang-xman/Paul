#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

gate.prototype.base.py

PATH

[app_root]/gate/prototype/base.py

INTRO

Quantum gate is a unitary quantum operator. A quantum
operator however isn't necessarily a quantum gate,
should it not be unitary.

Quantum gate, or simply gate, is a subclass of quantum
operator. A quantum gate usually operates on a qubit state
with a default number of qubits (noq). The minimum of noq
is 1, a single qubit, and the quantum gate that operates
on a single-qubit state is called single-qubit gate.
Single-qubit gate is fundamental to quantum circuits.
Multiple-qubit gate can in principle be decomposed into a
series of single ones. Such decomposition isn't always
simple and obvious. According to Nielsen and Chuang,
physical realisation of a multiple-qubit gate, especially
a controlled gate, isn't (yet) always possible.

In Qubit package, quantum gate is designed as 'prototype'
decorated by a decorator class. Prototype class has two
jobs. First, description -- via declaration -- of the
parameters/arguments that are used in gate operation.
Second, gate-dependent features and methods.

Decorator class, on the other hand, handles two tasks.
First, implements common methods for most, if not all,
gates. Second, regulates and validates arguments and
parameters against the description in parameter
descriptor.

In Qubit package, all gates (both single- or multi-qubit
gates) are assumed to operate on one unified input state
with indices to specify the single qubits. What this
architecture implies is that if a system consists of
multiple states, such as stored in multiple registers,
quantum gate applies to the tensor product of them.
This design unifies various basic operations such as
controlled ones, while giving prototype the freedom to
guide how such operations shall be carried out.

Such architecture, however, comes with pros and cons for
gate that requires multiple input qubits.

First, unified state. As mentioned above, one must merge
separate states into a unified input state. Should these
states be stored in separate registers, one must keep
tracking the index of each state the gate operates on.
Very often an operation acts on this merged state to
produce an entangled state, which prevents us from telling
the state of qubit at a particular location. To facilitate
this design of quantum gate, I have introduced a global index
tracking mechanism in the quantum register and memory.
(See NOTE 1.)

Second, due to the merge of states and dimension of quantum
operators so enlarged, the dimension of matrices involved
in state manipulation is higher, so is the computational
cost. To accommodate this issue, parallelisation and
distributed computing are among the most viable solutions.

Another important feature of the present architecture is
the departure from state object: The only information
required to construct a gate operator matrix is shall
be the metadata of a state, such as the total number
of qubits, target bit index, etc. The actual vector
of the state object is only needed until the application
of the operator, which is essentially a matrix product.
(See NOTE 2.)

CONTENT

`GatePrototype` - Base class to all gate prototype
classes

`SingleQubitGatePrototype` - Base class to all single-qubit
prototype; a subclass of `GatePrototype`

NOTE

[1] Register and quantum memory libraries implement
methods to track and manage qubit index in a merged
state.

[2] Lazy loading to delay the actual procedures or
subroutines of matrix computation.

TODO Long term

[1] Shall I use sparse matrix manipulation for state
and enlarged operators?

[2] How to lower the overall computational cost?

LOG

Updated on 30 September 2021 | Created on 12 March 2021
"""
from qubit import QubitState
from quantum_operator import QuantumOperator

from .errors import GatePrototypeValidationError
from .validators import GatePrototypeValidator, \
    GatePrototypeMethodSignatureValidator, \
    GatePrototypeMethodParametersValidator

_MODULE_LOCATION_ = 'gate.prototype.base'


class GatePrototype(QuantumOperator):
    """ Gate prototype base class

    Gate prototype is a subclass of `Quantum operator`.
    Quantum gate is a type of quantum operator and such
    inheritance is natural.

    Quantum operator class requires a class attribute
    `state_class` to specify the (base) type of object
    it operates on; for a quantum gate, it is `QubitState`.

    Behind every gate operation lies matrix manipulation,
    which is better processed by one method. Such numeric
    processing should be delayed to the last moment for
    higher efficiency and better performance. (See NOTE 2.)

    Any gate prototype must inherit from `GatePrototype`
    class. Validation of prototype class structure is
    performed at instantiation. A constructor is absent
    from this prototype class and `QuantumOperator.__init__`
    is hence invoked per instantiation, without providing
    the internal matrix, i.e. after instantiation the
    internal matrix (of `QuantumOperator`) is set to `None`.

    `GatePrototype` class also provides general verification
    and validation mechanisms to methods implemented in
    prototype.

    ATTRIBUTES

    `self.is_parameter_valid(,name,value)` : verifies if
    the value given to a parameter is valid;
    returns `True`(`False`) if valid(invalid)

    `self.verified_signature(,gate_method)` : signature of
    the given gate method is verified against the parameter
    descriptor; it checks if an argument in the signature is
    declared in the descriptor; it returns a dictionary that
    has two keys `args` and `kwargs`

    `self.validate_parameters(,gate_method,*args,**params)` :
    validate parameter values passed in via `params` against
    the signature of the method; undeclared argument triggers
    gate error
    """
    state_class = QubitState
    error_location = _MODULE_LOCATION_ + '.GatePrototype'

    def __new__(cls, *args, **kwargs):
        prototype = cls
        validator = GatePrototypeValidator(prototype=prototype)
        if not validator.is_valid:
            validator.raise_last_error(cls.error_location+'.__new__')
        return super().__new__(cls)

    def is_parameter_valid(self, name, value):
        """ Gate Prototype :: Validate individual parameter value """
        ret = False
        if name in self.parameters.keys():
            if self.parameters[name].is_valid(value):
                ret = True
        return ret

    def verified_signature(self, gate_method):
        """ Gate Prototype :: Verify signature of gate method

        Gate method is defined in a gate prototype.
        Any argument appearing in the signature of a gate
        method must be declared in the parameter descriptor.
        Verification is performed by
        `GatePrototypeMethodSignatureValidator`.

        This method scans the signature of the given gate
        method and ONLY checks if each argument in the
        signature is declared.

        Should an arugment be found undeclared, a gate
        operation error will be raised.

        RETURN

        Returns a verified signature as a dictionary. Returned
        dictionary contains two keys `args` and `kwargs`.
        """
        ret = None
        signature_validator = \
                GatePrototypeMethodSignatureValidator(self, gate_method)
        if signature_validator.is_valid:
            ret = signature_validator.validated_data()
        else:
            signature_validator.raise_last_error(
                    self.error_location+'.__init__')
        return ret

    def validate_parameters(self, gate_method, *args, **params):
        """ Gate Prototype :: Validate parameters

        Before invoking a method with given parameters,
        validation is performed against the descriptor
        and signature. Validation is perfomed by validator
        `GateMethodParametersValidator`.

        Positional and keyword arguments required by the
        method signature are prepared and validated against
        the declaration in the descriptor `parameters`.

        Returns validated operational args in a tuple
        (`opargs`) and kwargs in a dictionary (`opkwargs`).

        Caution. All parameters are passed in via keyword
        arguments `params`. Undeclared argument will trigger
        gate operation error.

        In case a parameter falls on its default value,
        a warning is issued.
        """
        opargs = None
        opkwargs = None
        validator = GatePrototypeMethodParametersValidator(
                self, gate_method, **params)
        if validator.is_valid:
            vd = validator.validated_data()
            opargs = vd['args']
            opkwargs = vd['kwargs']
        else:
            validator.raise_last_error(
                    self.error_location+'.valdiate_parameters')
        return opargs, opkwargs


class SingleQubitGatePrototype(GatePrototype):
    """ Prototype class for single qubit gate

    Single qubit gate must have a gate matrix method
    that is applicable to a single qubit. In addition,
    the default number of qubits of a single-qubit gate
    must be 1.
    """
    def __init__(self):
        """ Validate the default number of qubits """
        if self.minimal_number_of_qubits != 1:
            raise GatePrototypeValidationError("Minimal number " +\
                    "of qubits of single qubit " +\
                    "gate {} is not 1.".format(self.alias))
        super().__init__()
