#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

common.validator.base_validator.py

TODO

[1] Prettify error messages.

PATH

[app_root]/common/validator/base_validator.py

INTRO

Application-wide base validator.

WARNING

This base class is NOT to be instantiated. To make
an instantiable validator a subclass must have a
`error_class` class attribute.

LOG

Updated on 30 September 2021 | Created on 29 June 2020
"""
from common.exception.base import Base_Error
from .errors import BaseValidatorError

_MODULE_LOCATION_ = 'common.validator.base_validator'


class Base_Validator:
    """ Base validator

    Base validator must be subclassed by all validators
    created in the application. It is a container that
    stores error instances.

    Validator does not raise errors automatically but
    holds them to the point errors need to be raised.

    Subclass MUST have a class attribute `error_class`
    to instantiate error instance.

    WARNING

    This base class is NOT to be instantiated. To make
    an instantiable validator a subclass must have a
    `error_class` class attribute.

    ATTRIBUTES

    `cls.error_class` (class) : required error class to
    be implemented by subclass as class attribute; it
    must be a subclass of `Base_Error`

    `self._errors` (`list`) : a list acting as an error
    container; error instances are appended to it; most
    important error container

    `self.make_error_instance(,message=None,location=None)` :
    method to make an error instance using the message and
    location provided; if message is already an error instance,
    then check if relocation is necessary should `location`
    argument is not `None`

    `self.report_errors(,message,location=None)` : collects
    errors from argument `message` is not `None`

    `self.get_errors()` : return errors in container

    `self.raise_last_error()` : raise the last error in the
    error container list

    `self.is_valid`: property; returns `True` if error container
    is empty or `False` if not empty

    `self.stringigy()` : return a string converted from all
    error instances in the container.

    `self.__str__()` : return `self.stringigy()`

    `self.as_error()` : return `self.stringigy()`
    """
    def __new__(cls, *args, **kwargs):
        """ Base_Validator :: new

        Coerce subclass to implement `error_class` attribute.
        Validator may inherit error class of the base class.
        """
        # prevent direct instantiation
        if cls is Base_Validator:
            raise BaseValidatorError("Base validator class " +\
                    "must not be instantiated")
        # check only subclass
        if cls.__name__ != 'BaseValidator':
            if getattr(cls, 'error_class', None):
                # error class not inheriting Base_Error
                if not issubclass(getattr(cls, 'error_class'), Base_Error):
                    raise BaseValidatorError("Error class to "  +\
                            "validator {}".format(cls.__name__) +\
                            "is not a subclass of 'BaseError'")
            else:
                raise BaseValidatorError("Any validator must " +\
                        "have a class attribute 'error_class' ")
        return super().__new__(cls)

    def __init__(self):
        """ Base_Valdiator :: init

        Creates an error instance container.
        """
        self._errors = []

    def make_error_instance(self, message=None, location=None):
        """ Base_Validator :: Make error instance

        If `message` is a string, it is converted into an
        error instance of `error_class`.

        If `message` is an instance of `Base_Error`, store
        it. Should relocation is required, new location is
        appended.
        """
        ret = None
        if location is None:
            # if validator has error location, use it
            if getattr(self, 'error_location', None):
                location = self.error_location
            # otherwise validator name
            else:
                location = self.__class__.__name__
        # message is an error instance
        if isinstance(message, Base_Error):
            if location is not None:
                message.relocate(location=location)
            ret = message
        # message is a string
        elif isinstance(message, str):
            ret = self.error_class(message=message, location=location)
        else:
            raise BaseValidatorError('Error has to be either a ' +\
                    'string or an instance of Base_Error.')
        return ret

    def report_errors(self, message, location=None):
        """ Base_Validator :: Error reporter

        This method calls `make_error_instance` method.

        If errors are given in a list, this method appends
        newly created error instances to the existing list;
        otherwise, just append the new error instance to
        error container. If not a list, collect the error
        with respect to the given message.

        Value for `message` can be string or exception instance.
        """
        if message is not None:
            if isinstance(message, list):
                for item in message:
                    self._errors.append(self.make_error_instance(
                            message=item, location=location))
            else:
                self._errors.append(self.make_error_instance(
                        message=message, location=location))
        else:
            raise BaseValidatorError("To report an error, one or a " +\
                    "list of error message or error instances " +\
                    "of BaseError must be provided.")

    def get_errors(self):
        """ Base_Validator :: Returns all errors in a list

        Return

        `self._errors` (`list`) : error container
        """
        return self._errors

    def raise_last_error(self, location=None):
        """ Base_Validator :: Raise last error

        If error instance is an instance of this error
        class, repack it as the current error class and
        raise it. This unifies error identification.

        Argument `location` helps to locate error where
        it was raised.

        However, this practice hides original error type.
        """
        error = None
        if not self.is_valid:
            if not self._errors[-1].__class__ is self.__class__:
                error = self.error_class(message=self._errors[-1].full_message)
            else:
                error = self._errors[-1]
            # check if need to relocate
            if location is not None:
                error.relocate(location)
            raise error

    @property
    def is_valid(self):
        """ Base_Validator :: If error container is empty """
        _valid = False
        if len(self._errors) == 0:
            _valid = True
        return _valid

    def stringify(self):
        """ Base_Validator :: Stringify messages from error instances

        TODO Make it prettier.

        Compose a string from all error instances stored in the
        error container.
        """
        errormsg = ''
        if len(self._errors) > 0:
            for error in self._errors:
                if isinstance(error, Base_Error):
                    errormsg += error.stringify() + ".\n"
                elif isinstance(error, str):
                    errormsg += error + ".\n"
        return errormsg

    def __str__(self):
        """ Base_Validator :: Print validator instance

        All errors in the error container will be stringified
        and displayed.
        """
        return self.stringify()

    def as_error(self):
        """ Base Validator :: Error as string """
        return self.stringify()
