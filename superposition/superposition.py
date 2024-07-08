#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
MODULE

superposition.superposition.py

PATH

[app_root]/superposition/superposition.py

INTRO

Superposition is an abstract principle that governs
addition of objects.

Central to the principle is that summing up two
linearly scaled objects must yield an object the same
type. Here linearly scaled object means the object is
multiplied by a number.

Superposition principle is a reflection of properties
of vector. Quantum state is the most important example.
The superposition class implemented here emulates this
principle.

Abstract superposition principle applies to object of
any type. The underlying object must EITHER implement
multiplication (*), addition (+), and equal (==)
operators, OR have access to external methods that can
fulfill such operation. These operations are required
to convert a superposition into an object of the same
type.

In this application, the realisation of superposition
is via a list of tuples, referred to as 'superlist'.
Within the superlist, each tuple has exactly 2 elements.
First element is referred to as 'amplitude' and is often
a number. The second element is an instance of the
specified type and is often referred to as 'component'.
The tuple is sometimes referred to as 'member'.

As a convention, in a superlist, the algebraic relationship
between any two tuples is assumed to be addition (+);
within each tuple, the relationship between amplitude
and component is assumed to be multiplication. However,
customised conventions are of course possible.

CONTENT

`SuperpositionError` - Error class for superposition

`SuperpositionValidationError` - Superposition validation
error

`SuperpositionValidator` - Superposition object validator

`Superposition` - Base class to all superpositions

LOG

Updated on 29 September 2021 | Created on 17 April 2021
"""
from .base import AbstractSuperposition
from .errors import SuperpositionError
from .validators import SuperpositionValidator

_MODULE_LOCATION_ = 'superposition.superposition'


class Superposition(AbstractSuperposition):
    """ Superposition base class

    Direct instantiation of this class is not meaningful.

    To implement a superposition for a specific object type,
    one must subclass from this base class and implement the
    required class attribute `component_type`.

    CONSTRUCTOR

    `superlist` (`list`) : a superlist is a list of amplitude-
    component tuples; component must be of the type defined in
    subclass `cls.component_type`
    """
    _ERROR_LOCATION_ = _MODULE_LOCATION_ + '.Superposition'

    def __new__(cls, *args, **kwargs):
        """ Superposition :: __new__

        For subclass, the component type must be specified.
        """
        # if cls is not superposition,
        # must be a subclass of this one.
        if cls is not Superposition:
            if not getattr(cls, 'component_type', None):
                raise SuperpositionError("Any subclass of "      +\
                        "superposition must implement class "    +\
                        "attribute 'component_type' to declare " +\
                        "the type of component object stored "   +\
                        "in the superlist.")
        return super().__new__(cls)

    def __init__(self, superlist=None):
        """ Superposition :: init

        After validation, private attribute `__superlist`
        is created.
        """
        self._superlist = None
        validator = SuperpositionValidator(
                superlist=superlist, component_type=self.component_type)
        if validator.is_valid:
            self._superlist = validator.validated_data()['superlist']
        else:
            validator.raise_last_error(self._ERROR_LOCATION_+'.__init__')

    def as_superlist(self):
        """ Superposition :: Return the superlist """
        return self._superlist

    @property
    def component_type(self):
        """ Superposition :: Return component type """
        return self.component_type

    def __getitem__(self, index):
        """ Superposition :: Return a tuple given by the index """
        ret = None
        if index in range(0, len(self._superlist), 1):
            ret = self._superlist[index]
        else:
            raise SuperpositionError("Index to reference a " +\
                    "member in the superlist is out of range.")
        return ret

    def string_representation(self):
        """ Superposition :: Subclass must implement """

    def __str__(self):
        return self.string_representation()
