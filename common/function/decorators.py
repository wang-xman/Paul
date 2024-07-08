#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.function.decorator.py

PATH

[app_root]/common/function/decorator.py

INTRO

[Verifier function decorator]

Verifier (function) returns only `True` or `False`.
It usually takes only one argument. Can't call it
boolean function outright, since a boolean function
usually requires the input to be boolean, too.

Verifer function decorator replaces the original
function by an instance of this class. It garantees
that all verifiers (functions) are of the same type,
i.e. this class.

With this design, verifiers can be used in function
invocation decorator to replace a specific type.

[Function invocation decorator]

Invocation decorator is used to declare and validate
function arguments and invoke the decorated function.

Here, 'original function' refers to the function which
is to be decorated; 'decorated function' is the one that
is returned from the decorator.

In general, an argument that is declared in decorator
argument-type dict MUST exist in original function's
signature. However, an argument that appears in the
original signature does not have to be declared in
the argument type. This improves re-usability of a
function.

CONTENT

LOG

Updated on 06 October 2021 | Created on 27 September 2020
"""
from inspect import isclass as inspect_isclass

from .signature import function_signature
from .errors import VerifierFunctionDecoratorError, \
    FunctionInvocationDecoratorError


class VerifierFunctionDecorator:
    """ Verifier fucntion decorator

    Verifier (function) returns only `True` or `False`,
    i.e. boolean. It usually takes only one argument.

    Verifer function decorator replaces the original
    function by an instance of this class. It garantees
    that all verifiers (functions) are of the same type,
    i.e. this class.

    With this design, verifiers can be used in function
    invocation decorator to replace a specific type.
    """
    def __init__(self, *args, **kwargs):
        """ Verifier Function Decorator :: init """
        self._original_function = args[0]

    def __call__(self, *args, **kwargs):
        """ Verifier Function Decorator :: call """
        ret = None
        original_return = self._original_function(*args, **kwargs)
        if original_return is True or original_return is False:
            ret = original_return
        else:
            raise VerifierFunctionDecoratorError("Return of a " +\
                    "verifier function must be boolean.")
        return ret


class FunctionInvocationDecorator:
    """ Function invocation decorator

    Used as base class to most function invocation
    decorators.

    NOTE Should a verifier function be used in the
    argument type dictionary, it must return a boolean
    value for any type of input. Otherwise, error
    breaks out.

    ARGUMENTS

    `argument_type` : a dict with function argument
    names as keys, corresponding type (class)/verifier
    function as value
    """
    def __new__(cls, *args, **kwargs):
        """ Function Invocation Decorator :: new

        Enforce subclass to implement `error_class` class
        attribute.
        """
        if cls is not FunctionInvocationDecorator:
            if not getattr(cls, 'error_class', None):
                raise FunctionInvocationDecoratorError("Subclass "  +\
                    "'{}' ".format(cls.__name__) + "must implement" +\
                    "a class attribute 'error_class' to specify "   +\
                    "the errors raised by this decorator class.")
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        """ Function Invocation Decorator :: init

        Decorator arugments passed in here.
        """
        # argument type dict
        self._argument_type = kwargs['argument_type']

    def _validate_single_declared_type(self, declared_arg, declared_type):
        """ Function Invocation Decorator :: Verify single declared type """
        if not inspect_isclass(declared_type):
            if not isinstance(declared_type, VerifierFunctionDecorator):
                raise FunctionInvocationDecoratorError("Value of " +\
                    "declared argument '{}' ".format(declared_arg) +\
                    "declared is neither a class nor a verifier "  +\
                    "function.")

    def _validate_declaration(self, sigdict):
        """ Function Invocation Decorator :: Validate declaration

        Two aspects are verified.

        [1] Value in dictionary can be either a class (type),
        or verifier function (instance of verifier decorator).

        [2] Value can be a tuple.

        [3] A declared argument must also exist in the original
        signature. Otherwise, an error shall be raised.

        Arguments

        `sigdict` (`dict`) : function signature dict acquired
        from the original function
        """
        original_arguments = sigdict['args'] + tuple(sigdict['kwargs'].keys())
        for declared_arg, declared_type in self._argument_type.items():
            # types/verifiers in tuple
            if isinstance(declared_type, tuple):
                for item in declared_type:
                    self._validate_single_declared_type(declared_arg, item)
            # single type/verifier
            else:
                self._validate_single_declared_type(declared_arg, declared_type)

            if declared_arg not in original_arguments:
                raise FunctionInvocationDecoratorError("Argument " +\
                        "'{}' ".format(declared_arg) + "declared " +\
                        "in decorator is not an argument of the "  +\
                        "original function.")

    def _verify_against_single_type(self, argtype, argvalue):
        """ Function Invocation Decorator :: Single type declared """
        ret = False
        if isinstance(argtype, VerifierFunctionDecorator):
            if argtype(argvalue):
                ret = True
        # type is a class
        else:
            if isinstance(argvalue, argtype):
                ret= True
        return ret

    def _verify_against_type_tuple(self, argtype_tuple, argvalue):
        """ Function Invocation Decorator :: Types declared in tuple """
        ret = False
        for argtype in argtype_tuple:
            # if one fits, it is true
            if self._verify_against_single_type(argtype, argvalue):
                ret = True
        return ret

    def _verify_argument_value(self, argname, argvalue):
        """ Function Invocation Decorator :: Verify positional args """
        ret = False
        if isinstance(self._argument_type[argname], tuple):
            ret = self._verify_against_type_tuple(
                    self._argument_type[argname], argvalue)
        else:
            # type is a verifier
            ret = self._verify_against_single_type(
                    self._argument_type[argname], argvalue)
        return ret

    def __call__(self, original_function):
        # signature dict has two keys 'args' and 'kwargs'
        sigdict = function_signature(original_function)
        self._validate_declaration(sigdict)

        def function_parameter_acceptor(*args, **kwargs):
            """ Invocation parameters are passed in here """
            error_message = None
            invocargs = ()
            invockwargs = {}
            # prepare invocation positional arguments
            for idx, argname in enumerate(sigdict['args']):
                # if type is declared
                if argname in self._argument_type.keys():
                    if self._verify_argument_value(argname, args[idx]):
                        invocargs = invocargs + (args[idx],)
                    else:
                        error_message = "Argument '{}' ".format(argname)  +\
                                "value either failed verification or is " +\
                                "not the required type."
                # if type not declared, just take it
                else:
                    invocargs = invocargs + (args[idx],)
            # prepare invocation kwargs
            # signature carries the default value.
            for argname, argdefault in sigdict['kwargs'].items():
                # arg is declared
                if argname in self._argument_type.keys():
                    # arg also provided by caller
                    if argname in kwargs.keys():
                        if self._verify_argument_value(argname, kwargs[argname]):
                            invockwargs[argname] = kwargs[argname]
                        else:
                            # raise error
                            error_message = "Argument '{}' ".format(argname) +\
                                    "is not of the required type " +\
                                    "{}".format(self._argument_type[argname])
                    # if not provided by caller, use default
                    else:
                        invockwargs[argname] = argdefault
                # if type not declared, just take it
                else:
                    # if value is provided in kwargs
                    if argname in kwargs.keys():
                        invockwargs[argname] = kwargs[argname]
                    # if not, use default.
                    else:
                        invockwargs[argname] = argdefault
            # raise error
            if error_message is not None:
                raise self.error_class(error_message,
                        location='linear_space.linear_object.algebra.'+\
                                original_function.__name__)
            return original_function(*invocargs, **invockwargs)
        return function_parameter_acceptor
